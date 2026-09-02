#!/usr/bin/env python3
"""Evidence-only cross-role identity and proportion review.

The eight hei-mao variants intentionally have different outfits and props, so
ordinary whole-sprite similarity is not a useful identity test.  This review
aligns each cell to its lower-body anchor, then compares the upper core (head,
face, and upper-body proportion) against the role's own idle reference and the
cross-role neutral cohort.  Metrics only rank candidates; no formal asset is
modified.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROLES = [
    "hei-mao",
    "hei-mao-quality",
    "hei-mao-butler",
    "hei-mao-chef",
    "hei-mao-foodie",
    "hei-mao-delivery",
    "hei-mao-fortune",
    "hei-mao-traveler",
]
ROWS = [
    "idle",
    "running-right",
    "running-left",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
    "look-row-9",
    "look-row-10",
]
FRAME_COUNTS = {
    "idle": 6,
    "running-right": 8,
    "running-left": 8,
    "waving": 4,
    "jumping": 5,
    "failed": 8,
    "waiting": 6,
    "running": 6,
    "review": 6,
    "look-row-9": 8,
    "look-row-10": 8,
}
ROW_INDEX = {row: index for index, row in enumerate(ROWS)}
CELL_W = 192
CELL_H = 208
ALPHA_THRESHOLD = 16
DISPLAY_SIZE = (96, 104)
FEATURE_SIZE = (32, 28)
SHEET_COLUMNS = 3
PANEL_W = 3 * DISPLAY_SIZE[0]
PANEL_H = DISPLAY_SIZE[1] + 26

KNOWN_BLOCKERS = {
    ("hei-mao", "jumping"): "duplicated head",
    ("hei-mao-quality", "jumping"): "duplicated head",
    ("hei-mao-foodie", "waiting"): "stacked upper contours",
    ("hei-mao-delivery", "failed"): "repeated head and pose-family switch",
    ("hei-mao-quality", "running-left"): "complete-row detached component/action structure issue",
    ("hei-mao-quality", "failed"): "complete-row detached component/action structure issue",
    ("hei-mao-traveler", "waiting"): "complete-row detached component/action structure issue",
    ("hei-mao-traveler", "review"): "complete-row detached component/action structure issue",
}


def open_cell(atlas: Image.Image, row: str, frame: int) -> Image.Image:
    row_index = ROW_INDEX[row]
    return atlas.crop(
        (frame * CELL_W, row_index * CELL_H, (frame + 1) * CELL_W, (row_index + 1) * CELL_H)
    ).convert("RGBA")


def mask_for(cell: Image.Image) -> np.ndarray:
    return np.asarray(cell.getchannel("A"), dtype=np.uint8) >= ALPHA_THRESHOLD


def bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def translate(array: np.ndarray, dx: int, dy: int) -> np.ndarray:
    result = np.zeros_like(array)
    src_x0 = max(0, -dx)
    src_x1 = min(CELL_W, CELL_W - dx)
    src_y0 = max(0, -dy)
    src_y1 = min(CELL_H, CELL_H - dy)
    if src_x1 <= src_x0 or src_y1 <= src_y0:
        return result
    result[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = array[
        src_y0:src_y1, src_x0:src_x1
    ]
    return result


def align(cell: Image.Image) -> tuple[Image.Image, np.ndarray, dict] | None:
    rgba = np.asarray(cell, dtype=np.uint8)
    mask = mask_for(cell)
    box = bbox(mask)
    if box is None:
        return None
    x0, y0, x1, y1 = box
    height = y1 - y0 + 1
    lower_start = y0 + int(round(height * 0.60))
    lower_x = np.nonzero(mask[lower_start : y1 + 1])[1]
    lower_anchor = float(lower_x.mean()) if len(lower_x) else float(np.nonzero(mask)[1].mean())
    dx = int(round((CELL_W - 1) / 2.0 - lower_anchor))
    dy = CELL_H - 1 - y1
    aligned_rgba = translate(rgba, dx, dy)
    aligned_mask = translate(mask, dx, dy)
    return Image.fromarray(aligned_rgba, mode="RGBA"), aligned_mask, {
        "bbox": [x0, y0, x1, y1],
        "width": x1 - x0 + 1,
        "height": height,
        "area": int(mask.sum()),
        "lower_anchor_x": round(lower_anchor, 3),
        "bottom": y1,
        "dx": dx,
        "dy": dy,
    }


def resize_vector(values: np.ndarray, size: int) -> np.ndarray:
    if values.size == 0:
        return np.zeros(size, dtype=np.float32)
    if values.size == 1:
        return np.repeat(values.astype(np.float32), size)
    source = np.linspace(0.0, 1.0, values.size)
    target = np.linspace(0.0, 1.0, size)
    return np.interp(target, source, values).astype(np.float32)


def core_feature(aligned: Image.Image, mask: np.ndarray, metrics: dict) -> tuple[np.ndarray, dict]:
    box = bbox(mask)
    if box is None:
        return np.zeros(FEATURE_SIZE[0] * FEATURE_SIZE[1] * 4 + 48, dtype=np.float32), {
            "nonempty": False
        }
    x0, y0, x1, y1 = box
    height = max(y1 - y0 + 1, 1)
    width = max(x1 - x0 + 1, 1)
    head_end = min(y1 + 1, y0 + max(1, int(round(height * 0.46))))
    head_mask = mask[y0:head_end]
    head_area = float(head_mask.sum())
    upper_area = float(mask[y0 : y0 + max(1, int(round(height * 0.58)))].sum())
    lower_area = float(mask[y0 + int(round(height * 0.58)) : y1 + 1].sum())

    # Stable, outfit-tolerant vertical proportions.  Values remain in source
    # pixels after lower-body alignment, so a squashed head does not disappear
    # through per-frame bbox normalization.
    head_width_profile = resize_vector(head_mask.sum(axis=1) / CELL_W, 16)
    upper_width_profile = resize_vector(
        mask[y0 : y0 + max(1, int(round(height * 0.58)))].sum(axis=1) / CELL_W, 16
    )
    head_x_profile = resize_vector(head_mask.sum(axis=0) / max(height, 1), 16)
    head_crop = np.asarray(
        Image.fromarray((head_mask.astype(np.uint8) * 255), mode="L").resize(
            (FEATURE_SIZE[0], FEATURE_SIZE[1]), Image.Resampling.BOX
        ),
        dtype=np.float32,
    ) / 255.0

    rgba = np.asarray(aligned, dtype=np.uint8)
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    # Fixed aligned face/upper-body window preserves absolute head scale while
    # still allowing hats and props to extend outside the core mask.
    fixed = rgba[:112, 32:160]
    fixed_alpha = fixed[:, :, 3:4].astype(np.float32) / 255.0
    fixed_rgb = fixed[:, :, :3].astype(np.float32) * fixed_alpha + 96.0 * (1.0 - fixed_alpha)
    fixed_rgb_small = np.asarray(
        Image.fromarray(np.clip(fixed_rgb, 0, 255).astype(np.uint8), mode="RGB").resize(
            FEATURE_SIZE, Image.Resampling.BILINEAR
        ),
        dtype=np.float32,
    ) / 255.0
    fixed_alpha_small = np.asarray(
        Image.fromarray((fixed[:, :, 3]), mode="L").resize(
            FEATURE_SIZE, Image.Resampling.BILINEAR
        ),
        dtype=np.float32,
    ) / 255.0

    vector = np.concatenate(
        [
            head_crop.ravel(),
            fixed_alpha_small.ravel(),
            fixed_rgb_small.ravel(),
            head_width_profile,
            upper_width_profile,
            head_x_profile,
        ]
    ).astype(np.float32)
    head_box = bbox(head_mask)
    if head_box is None:
        head_width = 0
        head_height = 0
        head_center_x = 0.0
    else:
        head_width = head_box[2] - head_box[0] + 1
        head_height = head_box[3] - head_box[1] + 1
        head_center_x = float(np.average(np.nonzero(head_mask)[1]))
    core = {
        "nonempty": True,
        "head_area_ratio": round(head_area / max(float(metrics["area"]), 1.0), 6),
        "upper_lower_area_ratio": round(upper_area / max(lower_area, 1.0), 6),
        "head_width": int(head_width),
        "head_height": int(head_height),
        "head_aspect": round(float(head_width / max(head_height, 1)), 6),
        "head_center_x": round(head_center_x, 3),
        "upper_area": int(upper_area),
        "lower_area": int(lower_area),
    }
    return vector, core


def normalized_distance(left: np.ndarray, right: np.ndarray) -> float:
    if left.shape != right.shape:
        return 1.0
    scale = max(float(np.linalg.norm(left)), float(np.linalg.norm(right)), 1e-6)
    return float(np.linalg.norm(left - right) / scale)


def robust_z(value: float, values: np.ndarray, floor: float = 1e-6) -> float:
    if values.size == 0:
        return 0.0
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    scale = max(1.4826 * mad, float(np.std(values)) * 0.25, floor)
    return abs(value - median) / scale


def composite(cell: Image.Image, size: tuple[int, int] = DISPLAY_SIZE) -> Image.Image:
    rgba = np.asarray(cell, dtype=np.uint8)
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    background = np.full((CELL_H, CELL_W, 3), (72, 74, 82), dtype=np.float32)
    rgb = rgba[:, :, :3].astype(np.float32) * alpha + background * (1.0 - alpha)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB").resize(
        size, Image.Resampling.LANCZOS
    )


def alpha_display(mask: np.ndarray, size: tuple[int, int] = DISPLAY_SIZE) -> Image.Image:
    image = Image.fromarray((mask.astype(np.uint8) * 255), mode="L").convert("RGB")
    return image.resize(size, Image.Resampling.NEAREST)


def diff_display(left: np.ndarray, right: np.ndarray, size: tuple[int, int] = DISPLAY_SIZE) -> Image.Image:
    count = min(left.size, right.size)
    diff = np.abs(left[:count] - right[:count])
    side = int(round(np.sqrt(count)))
    # The feature vector is not a rectangular image; use a compact heat strip
    # so the candidate panel remains an honest visual cue rather than a fake
    # reconstruction of the sprite.
    heat = np.zeros((16, 16), dtype=np.uint8)
    values = np.asarray(diff, dtype=np.float32)
    if values.size:
        values = np.resize(values, heat.shape)
        values = np.clip(values / max(float(np.percentile(values, 95)), 1e-6) * 255.0, 0, 255)
        heat = values.astype(np.uint8)
    return Image.fromarray(heat, mode="L").convert("RGB").resize(size, Image.Resampling.NEAREST)


def make_panel(record: dict, reference: dict | None) -> Image.Image:
    panel = Image.new("RGB", (PANEL_W, PANEL_H), (24, 24, 30))
    draw = ImageDraw.Draw(panel)
    current = composite(record["cell"])
    current_alpha = alpha_display(record["mask"])
    if reference:
        ref = composite(reference["cell"])
        diff = diff_display(record["feature"], reference["feature"])
    else:
        ref = Image.new("RGB", DISPLAY_SIZE, (48, 48, 56))
        diff = Image.new("RGB", DISPLAY_SIZE, (48, 48, 56))
    panel.paste(current, (0, 24))
    panel.paste(ref, (DISPLAY_SIZE[0], 24))
    panel.paste(diff, (2 * DISPLAY_SIZE[0], 24))
    draw.text((3, 4), f"{record['role']} {record['row']}[{record['frame']}]", fill=(244, 244, 244))
    draw.text((3, 14), f"d={record['identity_distance']:.3f} z={record['score']:.2f}", fill=(205, 205, 214))
    draw.text((3, 25 + DISPLAY_SIZE[1]), "current / idle / feature-diff", fill=(190, 190, 200))
    return panel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo.resolve()
    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or (out_dir / "cross-role-identity-review-20260831-v1.json")
    sheet_out = args.sheet_out or (out_dir / "cross-role-identity-candidates-v1.jpg")

    records: list[dict] = []
    by_key: dict[tuple[str, str, int], dict] = {}
    neutral: dict[str, dict] = {}
    for role in ROLES:
        atlas = Image.open(repo / "pets" / role / "spritesheet.webp").convert("RGBA")
        for row in ROWS:
            for frame in range(FRAME_COUNTS[row]):
                cell = open_cell(atlas, row, frame)
                aligned_result = align(cell)
                if aligned_result is None:
                    continue
                aligned, mask, metrics = aligned_result
                feature, core = core_feature(aligned, mask, metrics)
                record = {
                    "role": role,
                    "row": row,
                    "frame": frame,
                    "cell": cell,
                    "aligned": aligned,
                    "mask": mask,
                    "feature": feature,
                    "metrics": metrics,
                    "core": core,
                }
                records.append(record)
                by_key[(role, row, frame)] = record
        neutral[role] = by_key[(role, "idle", 0)]

    neutral_matrix = np.stack([neutral[role]["feature"] for role in ROLES])
    neutral_median = np.median(neutral_matrix, axis=0)
    neutral_scalar = {
        key: np.asarray([neutral[role]["core"].get(key, 0.0) for role in ROLES], dtype=np.float32)
        for key in ("head_area_ratio", "upper_lower_area_ratio", "head_aspect", "head_center_x")
    }
    neutral_records = []
    for role in ROLES:
        item = neutral[role]
        cross_distance = normalized_distance(item["feature"], neutral_median)
        scalar_z = [robust_z(float(item["core"][key]), values) for key, values in neutral_scalar.items()]
        score = float(cross_distance + 0.04 * np.mean(scalar_z))
        neutral_records.append(
            {
                "role": role,
                "frame": 0,
                "cross_role_distance": round(cross_distance, 6),
                "scalar_z": {key: round(value, 4) for key, value in zip(neutral_scalar, scalar_z)},
                "score": round(score, 6),
                "core": item["core"],
            }
        )

    # Compare each frame with its own idle core.  Row medians are used as the
    # reference for scoring so expected gestures do not make every action look
    # like identity drift.
    row_distances: dict[tuple[str, str], list[float]] = {}
    for record in records:
        distance = normalized_distance(record["feature"], neutral[record["role"]]["feature"])
        row_distances.setdefault((record["role"], record["row"]), []).append(distance)
        record["identity_distance"] = distance
    row_medians = {key: float(np.median(values)) for key, values in row_distances.items()}
    scored: list[dict] = []
    for record in records:
        row_median = row_medians[(record["role"], record["row"])]
        residual = abs(record["identity_distance"] - row_median)
        peer = np.asarray(row_distances[(record["role"], record["row"])], dtype=np.float32)
        # A very low-variance idle row can make a harmless subpixel-sized
        # feature change look like an extreme z-score.  Keep the robust score
        # sensitive to genuine identity drift, but impose a small absolute
        # distance scale for candidate ranking.
        score = robust_z(record["identity_distance"], peer, floor=0.01) + residual * 8.0
        record["score"] = float(score)
        if record["frame"] != 0 or record["row"] != "idle":
            scored.append(record)
    scored.sort(key=lambda item: item["score"], reverse=True)

    # Keep the sheet bounded and include every role at least once when possible.
    selected: list[dict] = []
    selected_keys: set[tuple[str, str, int]] = set()
    for role in ROLES:
        role_candidate = next((item for item in scored if item["role"] == role), None)
        if role_candidate:
            selected.append(role_candidate)
            selected_keys.add((role_candidate["role"], role_candidate["row"], role_candidate["frame"]))
    for item in scored:
        key = (item["role"], item["row"], item["frame"])
        if key not in selected_keys:
            selected.append(item)
            selected_keys.add(key)
        if len(selected) >= 24:
            break
    selected = selected[:24]

    panels = [make_panel(item, neutral[item["role"]]) for item in selected]
    sheet = Image.new(
        "RGB",
        (SHEET_COLUMNS * PANEL_W, ((len(panels) + SHEET_COLUMNS - 1) // SHEET_COLUMNS) * PANEL_H),
        (18, 18, 24),
    )
    for index, panel in enumerate(panels):
        sheet.paste(panel, ((index % SHEET_COLUMNS) * PANEL_W, (index // SHEET_COLUMNS) * PANEL_H))
    sheet.save(sheet_out, quality=92, optimize=True)

    report = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "supplemental cross-role identity and core-proportion review; evidence only",
        "method": {
            "name": "lower-anchor aligned core identity signature",
            "steps": [
                "align every cell to its lower-body anchor and shared bottom baseline",
                "extract upper 46% head mask, upper/lower area ratio, head width profile, and fixed-scale face/upper-body alpha/RGB signature",
                "compare eight idle references against a cross-role neutral cohort while retaining outfit and prop differences",
                "rank within-role frame deviations from that role's idle core and render bounded normal-size candidate panels",
                "promote no failure from metrics alone; require normal-size visual confirmation under hatch-pet policy",
            ],
            "why_complementary": "This isolates shared black-cat identity and absolute head/upper-body scale, which whole-silhouette and temporal residual checks can hide behind costume or prop motion.",
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": len(records),
            "neutral_references": len(neutral),
            "alpha_threshold": ALPHA_THRESHOLD,
            "candidate_panels": len(selected),
        },
        "neutral_role_records": neutral_records,
        "top_candidates": [
            {
                "role": item["role"],
                "row": item["row"],
                "frame": item["frame"],
                "score": round(float(item["score"]), 6),
                "identity_distance": round(float(item["identity_distance"]), 6),
                "known_blocker": KNOWN_BLOCKERS.get((item["role"], item["row"])),
                "core": item["core"],
            }
            for item in selected
        ],
        "result": {
            "new_hard_failures": [],
            "known_blockers_in_candidates": sum(
                1 for item in selected if (item["role"], item["row"]) in KNOWN_BLOCKERS
            ),
            "formal_assets_modified": False,
            "manual_review_required": True,
        },
        "artifacts": [json_out.name, sheet_out.name],
    }
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json_out": str(json_out), "sheet_out": str(sheet_out), "frames": len(records), "candidates": len(selected)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
