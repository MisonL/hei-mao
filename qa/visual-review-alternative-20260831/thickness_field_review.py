#!/usr/bin/env python3
"""Evidence-only local-thickness review for the current PetDex v2 atlases.

The method measures the distance-to-alpha-boundary field of every used cell.
It is intended to expose a locally flattened, pinched, or thinned head/body
that can keep a plausible outer bounding box. Metrics rank candidates only;
the formal spritesheets are never modified.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path

import cv2
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
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
    ("look-row-9", 8),
    ("look-row-10", 8),
]
CELL_W = 192
CELL_H = 208
ALPHA_THRESHOLD = 16
DISPLAY_W = 48
DISPLAY_H = 52
PROFILE_BANDS = 16
BACKGROUND = (92, 94, 102)

KNOWN_BLOCKERS = {
    ("hei-mao", "jumping", 2): "duplicated head",
    ("hei-mao-quality", "jumping", 2): "duplicated head",
    ("hei-mao-foodie", "waiting", 2): "stacked upper contours",
    ("hei-mao-foodie", "waiting", 3): "stacked upper contours",
    ("hei-mao-delivery", "failed", 0): "repeated head and pose-family switch",
    ("hei-mao-delivery", "failed", 1): "repeated head and pose-family switch",
    ("hei-mao-delivery", "failed", 2): "repeated head and pose-family switch",
    ("hei-mao-delivery", "failed", 3): "repeated head and pose-family switch",
    ("hei-mao-delivery", "failed", 4): "repeated head and pose-family switch",
}


def open_cell(atlas: Image.Image, row: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row * CELL_H, (frame + 1) * CELL_W, (row + 1) * CELL_H)
    ).convert("RGBA")


def alpha_mask(cell: Image.Image) -> np.ndarray:
    return np.asarray(cell.getchannel("A"), dtype=np.uint8) >= ALPHA_THRESHOLD


def resize_vector(values: np.ndarray, size: int) -> np.ndarray:
    if values.size == 0:
        return np.zeros(size, dtype=np.float32)
    if values.size == 1:
        return np.repeat(values.astype(np.float32), size)
    source = np.linspace(0.0, 1.0, values.size)
    target = np.linspace(0.0, 1.0, size)
    return np.interp(target, source, values).astype(np.float32)


def composite(cell: Image.Image) -> Image.Image:
    rgba = np.asarray(cell, dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    rgb = rgba[:, :, :3] * alpha + np.asarray(BACKGROUND, dtype=np.float32)[None, None, :] * (1.0 - alpha)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")


def mask_bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def distance_field(mask: np.ndarray) -> np.ndarray:
    # OpenCV treats non-zero pixels as foreground and returns the distance to
    # the nearest zero pixel. A one-pixel border prevents edge-connected masks
    # from receiving a misleading infinite interior distance.
    padded = np.pad(mask.astype(np.uint8), 1, mode="constant")
    distances = cv2.distanceTransform(padded, cv2.DIST_L2, 5)
    return distances[1:-1, 1:-1].astype(np.float32)


def relative_band_profile(field: np.ndarray, mask: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    _, y0, _, y1 = box
    height = max(y1 - y0 + 1, 1)
    values: list[float] = []
    for index in range(PROFILE_BANDS):
        start = y0 + int(round(index * height / PROFILE_BANDS))
        end = y0 + int(round((index + 1) * height / PROFILE_BANDS))
        band_mask = mask[start:max(end, start + 1)]
        band_field = field[start:max(end, start + 1)]
        selected = band_field[band_mask]
        values.append(float(np.median(selected) / height) if selected.size else 0.0)
    return np.asarray(values, dtype=np.float32)


def feature_record(cell: Image.Image) -> tuple[dict, np.ndarray, np.ndarray, np.ndarray]:
    mask = alpha_mask(cell)
    box = mask_bbox(mask)
    if box is None:
        empty = np.zeros(PROFILE_BANDS * 2 + 9, dtype=np.float32)
        return (
            {"nonempty": False, "area": 0, "width": 0, "height": 0, "median_thickness": 0.0},
            empty,
            np.zeros_like(mask, dtype=np.float32),
            mask,
        )

    x0, y0, x1, y1 = box
    height = y1 - y0 + 1
    width = x1 - x0 + 1
    field = distance_field(mask)
    band = relative_band_profile(field, mask, box)
    # A display-sized field captures thickness that survives the actual small
    # pet rendering, while the full-resolution profile preserves local shape.
    display_mask = np.asarray(
        Image.fromarray((mask.astype(np.uint8) * 255), mode="L").resize(
            (DISPLAY_W, DISPLAY_H), Image.Resampling.BOX
        ),
        dtype=np.uint8,
    ) >= 128
    display_field = distance_field(display_mask)
    display_box = mask_bbox(display_mask)
    if display_box is None:
        display_band = np.zeros(PROFILE_BANDS, dtype=np.float32)
    else:
        display_band = relative_band_profile(display_field, display_mask, display_box)

    selected = field[mask]
    normalized = selected / max(float(height), 1.0)
    quantiles = np.percentile(normalized, [10, 25, 50, 75, 90]).astype(np.float32)
    upper_slice = slice(y0, y0 + max(1, int(round(height * 0.38))))
    upper = field[upper_slice][mask[upper_slice]] / max(float(height), 1.0)
    middle_start = y0 + int(round(height * 0.38))
    middle_end = y0 + int(round(height * 0.72))
    middle_slice = slice(middle_start, max(middle_end, middle_start + 1))
    middle = field[middle_slice][mask[middle_slice]] / max(float(height), 1.0)
    lower_slice = slice(middle_end, y1 + 1)
    lower = field[lower_slice][mask[lower_slice]] / max(float(height), 1.0)
    region_medians = np.asarray(
        [
            float(np.median(upper)) if upper.size else 0.0,
            float(np.median(middle)) if middle.size else 0.0,
            float(np.median(lower)) if lower.size else 0.0,
        ],
        dtype=np.float32,
    )
    display_selected = display_field[display_mask]
    display_median = float(np.median(display_selected)) if display_selected.size else 0.0
    display_p90 = float(np.percentile(display_selected, 90)) if display_selected.size else 0.0
    core_fraction = float(np.mean(selected >= max(float(height) * 0.08, 1.0))) if selected.size else 0.0
    vector = np.concatenate(
        [
            band,
            display_band,
            quantiles,
            region_medians,
            np.asarray(
                [
                    float(width / max(height, 1)),
                    float(np.median(selected) / max(height, 1)),
                    float(np.percentile(selected, 90) / max(height, 1)),
                    display_median / max(DISPLAY_H, 1),
                    display_p90 / max(DISPLAY_H, 1),
                    core_fraction,
                ],
                dtype=np.float32,
            ),
        ]
    ).astype(np.float32)
    metrics = {
        "nonempty": True,
        "bbox": [x0, y0, x1, y1],
        "area": int(mask.sum()),
        "width": int(width),
        "height": int(height),
        "aspect": round(float(width / max(height, 1)), 6),
        "median_thickness": round(float(np.median(selected) * 2.0), 4),
        "p90_thickness": round(float(np.percentile(selected, 90) * 2.0), 4),
        "display_median_radius": round(display_median, 4),
        "display_core_fraction": round(core_fraction, 6),
    }
    return metrics, vector, field, mask


def robust_score(vector: np.ndarray, matrix: np.ndarray) -> tuple[float, list[str]]:
    median = np.median(matrix, axis=0)
    mad = np.median(np.abs(matrix - median), axis=0)
    scale = np.maximum(1.4826 * mad, 0.012)
    z = np.abs(vector - median) / scale
    z = np.minimum(z, 12.0)
    profile_a = float(np.mean(z[:PROFILE_BANDS]))
    profile_b = float(np.mean(z[PROFILE_BANDS : PROFILE_BANDS * 2]))
    stats = float(np.mean(z[PROFILE_BANDS * 2 :]))
    score = 0.45 * profile_a + 0.35 * profile_b + 0.20 * stats
    reasons: list[str] = []
    if profile_a >= 2.0:
        reasons.append(f"full_resolution_profile={profile_a:.2f}")
    if profile_b >= 2.0:
        reasons.append(f"display_profile={profile_b:.2f}")
    if stats >= 2.0:
        reasons.append(f"thickness_stats={stats:.2f}")
    return float(score), reasons or ["combined-thickness-distance"]


def heatmap(field: np.ndarray, mask: np.ndarray) -> Image.Image:
    values = field.copy()
    visible = values[mask]
    high = float(np.percentile(visible, 95)) if visible.size else 1.0
    normalized = np.clip(values / max(high, 1e-6), 0.0, 1.0)
    rgb = np.zeros((*values.shape, 3), dtype=np.uint8)
    rgb[:, :, 0] = np.clip(255.0 * normalized, 0, 255).astype(np.uint8)
    rgb[:, :, 1] = np.clip(220.0 * (1.0 - np.abs(normalized - 0.5) * 2.0), 0, 255).astype(np.uint8)
    rgb[:, :, 2] = np.clip(255.0 * (1.0 - normalized), 0, 255).astype(np.uint8)
    rgb[~mask] = (24, 26, 32)
    return Image.fromarray(rgb, mode="RGB")


def silhouette(mask: np.ndarray) -> Image.Image:
    rgb = np.full((*mask.shape, 3), (24, 26, 32), dtype=np.uint8)
    rgb[mask] = (238, 240, 245)
    return Image.fromarray(rgb, mode="RGB")


def tile(item: dict) -> Image.Image:
    panel_w, panel_h = CELL_W, CELL_H
    title_h, footer_h = 28, 24
    canvas = Image.new("RGB", (panel_w * 4, panel_h + title_h + footer_h), (12, 13, 18))
    panels = [
        composite(item["cell"]),
        silhouette(item["mask"]),
        heatmap(item["field"], item["mask"]),
        silhouette(item["row_median_mask"]),
    ]
    for index, panel in enumerate(panels):
        canvas.paste(panel, (index * panel_w, title_h))
    draw = ImageDraw.Draw(canvas)
    key = (item["role"], item["row"], int(item["frame"]))
    label = f"{item['role']}/{item['row']} f{item['frame']} score={item['score']:.2f}"
    if key in KNOWN_BLOCKERS:
        label += " CONTROL"
    draw.text((3, 5), label, fill=(245, 245, 248))
    draw.text((3, panel_h + title_h + 4), "原帧 | 当前轮廓 | 厚度场 | 行中值轮廓", fill=(214, 216, 224))
    return canvas


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--sheet-out", type=Path)
    parser.add_argument("--reviewed", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or output_dir / "thickness-field-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "thickness-field-candidates-v1.jpg"

    records: list[dict] = []
    row_groups: dict[tuple[str, str], list[dict]] = {}
    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        atlas = Image.open(atlas_path).convert("RGBA")
        for row_index, (row_name, frame_count) in enumerate(ROWS):
            group: list[dict] = []
            for frame in range(frame_count):
                cell = open_cell(atlas, row_index, frame)
                metrics, vector, field, mask = feature_record(cell)
                item = {
                    "role": role,
                    "row": row_name,
                    "row_index": row_index,
                    "frame": frame,
                    "metrics": metrics,
                    "vector": vector,
                    "field": field,
                    "mask": mask,
                    "cell": cell,
                }
                group.append(item)
                records.append(item)
            row_groups[(role, row_name)] = group

    for key, group in row_groups.items():
        if not group:
            continue
        vectors = np.stack([item["vector"] for item in group], axis=0)
        row_median_mask = np.mean(np.stack([item["mask"] for item in group], axis=0), axis=0) >= 0.5
        for item in group:
            score, reasons = robust_score(item["vector"], vectors)
            item["score"] = score
            item["reasons"] = reasons
            item["row_median_mask"] = row_median_mask

    records.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])))
    controls = [item for item in records if (item["role"], item["row"], int(item["frame"])) in KNOWN_BLOCKERS]
    selected: list[dict] = []
    seen: set[tuple[str, str, int]] = set()
    for item in controls + records:
        key = (item["role"], item["row"], int(item["frame"]))
        if key in seen:
            continue
        seen.add(key)
        selected.append(item)
        if len(selected) >= 32:
            break

    sheet_cols = 2
    tile_w = CELL_W * 4
    tile_h = CELL_H + 28 + 24
    sheet = Image.new("RGB", (sheet_cols * tile_w, max(1, math.ceil(len(selected) / sheet_cols)) * tile_h), (9, 10, 14))
    for index, item in enumerate(selected):
        sheet.paste(tile(item), ((index % sheet_cols) * tile_w, (index // sheet_cols) * tile_h))
    sheet.save(sheet_out, quality=93, subsampling=0)

    serializable = []
    for item in records:
        serializable.append(
            {
                "role": item["role"],
                "row": item["row"],
                "row_index": item["row_index"],
                "frame": item["frame"],
                "score": round(float(item["score"]), 6),
                "reasons": item["reasons"],
                "metrics": item["metrics"],
                "known_blocker": KNOWN_BLOCKERS.get((item["role"], item["row"], int(item["frame"]))),
            }
        )
    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "supplemental visual recheck using full-resolution and display-sized alpha distance fields; evidence only",
        "method": {
            "name": "silhouette thickness-field and local-width review",
            "steps": [
                "threshold each used RGBA cell at alpha 16 and compute an Euclidean distance-to-boundary field",
                "compare relative vertical thickness profiles, regional thickness quantiles, and display-sized thickness profiles against each row median",
                "rank candidates and render the current frame, binary silhouette, thickness heatmap, and row-median silhouette at 192x208",
                "treat numeric outliers as triage evidence and promote only visibly confirmed defects under hatch-pet policy",
            ],
            "purpose": "detect local head/body flattening, pinching, or thinning that can preserve a plausible outer bounding box",
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": len(records),
            "display_size": [DISPLAY_W, DISPLAY_H],
            "alpha_threshold": ALPHA_THRESHOLD,
            "candidate_sheet_items": len(selected),
        },
        "top_candidates": serializable[:64],
        "known_blocker_candidates": [
            f"{role}/{row}/f{frame}: {reason}" for (role, row, frame), reason in sorted(KNOWN_BLOCKERS.items())
        ],
        "visual_review": {
            "status": "pass_with_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
                "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
            ] if args.reviewed else [],
            "note": (
                "Candidate sheet reviewed at normal display size; the thickness-field method reproduced the existing blockers and added no new hard failure."
                if args.reviewed
                else "Review thickness-field-candidates-v1.jpg at normal display size; metric outliers are evidence only."
            ),
        },
        "formal_assets_modified": False,
        "artifacts": [sheet_out.name, json_out.name],
        "limitations": [
            "Distance fields are silhouette-based and do not identify semantic body parts; expected limb or prop motion can be a candidate.",
            "Row-median comparison can miss a defect shared by every frame in a row; it complements, but does not replace, canonical idle-envelope review.",
            "This is an asset-level check and cannot prove Codex App window layering, multi-display placement, or GPU compositing.",
            "The heatmap and binary overlays are review artifacts and are never written into formal pet assets.",
        ],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": len(records), "candidates": len(selected)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
