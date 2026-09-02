#!/usr/bin/env python3
"""Evidence-only state-intent and animation-degeneracy review.

This review complements silhouette, topology, and renderer checks by asking a
different question: does each standard row still communicate a distinct
animation state, or has it become static, repetitive, or dominated by the
wrong body region?  It uses normalized alpha/RGB frame features to rank
candidates and writes a bounded normal-size sheet for human review.  Scores
are triage evidence only; this script never edits a formal pet asset.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


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
STANDARD_ROWS = ROWS[:9]
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
DISPLAY_SIZE = (96, 104)
ALPHA_THRESHOLD = 16
FEATURE_SIZE = (48, 52)
SHEET_COLUMNS = 2
SHEET_ITEM_W = 4 * DISPLAY_SIZE[0]
SHEET_ITEM_H = DISPLAY_SIZE[1] + 31

KNOWN_BLOCKERS = {
    ("hei-mao", "jumping"): {"frames": [2], "description": "duplicated head"},
    ("hei-mao-quality", "jumping"): {"frames": [2], "description": "duplicated head"},
    ("hei-mao-foodie", "waiting"): {"frames": [2, 3], "description": "stacked upper contours"},
    ("hei-mao-delivery", "failed"): {
        "frames": [0, 1, 2, 3, 4],
        "description": "repeated head and pose-family switch",
    },
    ("hei-mao-quality", "running-left"): {
        "frames": list(range(8)),
        "description": "complete-row detached component/action structure issue",
    },
    ("hei-mao-quality", "failed"): {
        "frames": list(range(8)),
        "description": "complete-row detached component/action structure issue",
    },
    ("hei-mao-traveler", "waiting"): {
        "frames": list(range(6)),
        "description": "complete-row detached component/action structure issue",
    },
    ("hei-mao-traveler", "review"): {
        "frames": list(range(6)),
        "description": "complete-row detached component/action structure issue",
    },
}


def open_cell(atlas: Image.Image, row: str, frame: int) -> Image.Image:
    row_index = ROW_INDEX[row]
    return atlas.crop(
        (frame * CELL_W, row_index * CELL_H, (frame + 1) * CELL_W, (row_index + 1) * CELL_H)
    ).convert("RGBA")


def translate_array(array: np.ndarray, dx: int, dy: int) -> np.ndarray:
    result = np.zeros_like(array)
    src_x0 = max(0, -dx)
    src_x1 = min(CELL_W, CELL_W - dx)
    src_y0 = max(0, -dy)
    src_y1 = min(CELL_H, CELL_H - dy)
    if src_x1 <= src_x0 or src_y1 <= src_y0:
        return result
    result[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = array[src_y0:src_y1, src_x0:src_x1]
    return result


def robust_z(value: float, values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    scale = max(1.4826 * mad, float(np.std(values)) * 0.25, 1e-6)
    return abs(value - median) / scale


def feature_frame(cell: Image.Image) -> tuple[dict, np.ndarray, np.ndarray]:
    rgba = np.asarray(cell, dtype=np.uint8)
    alpha = rgba[:, :, 3]
    mask = alpha >= ALPHA_THRESHOLD
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        empty = np.zeros(FEATURE_SIZE[::-1], dtype=np.float32)
        return {"nonempty": False, "baseline": -1, "height": 0, "width": 0, "cx": 0.0, "cy": 0.0}, empty, empty

    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    height = y1 - y0 + 1
    width = x1 - x0 + 1
    lower_start = y0 + int(round(height * 0.62))
    lower_xs = xs[ys >= lower_start]
    lower_anchor = float(np.mean(lower_xs if len(lower_xs) else xs))
    dx = int(round((CELL_W - 1) / 2.0 - lower_anchor))
    dy = CELL_H - 1 - y1
    aligned_mask = translate_array(mask, dx, dy)
    aligned_rgba = translate_array(rgba, dx, dy)

    mask_small = np.asarray(
        Image.fromarray((aligned_mask.astype(np.uint8) * 255), mode="L").resize(FEATURE_SIZE, Image.Resampling.BILINEAR),
        dtype=np.float32,
    ) / 255.0
    alpha_small = np.asarray(
        Image.fromarray(aligned_rgba[:, :, 3], mode="L").resize(FEATURE_SIZE, Image.Resampling.BILINEAR),
        dtype=np.float32,
    ) / 255.0
    rgb = aligned_rgba[:, :, :3].astype(np.float32)
    rgb_small = np.asarray(
        Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB").resize(FEATURE_SIZE, Image.Resampling.BILINEAR),
        dtype=np.float32,
    ) / 255.0
    rgb_small *= alpha_small[:, :, None]
    vector = np.concatenate([mask_small.ravel(), rgb_small.ravel()])
    upper = slice(0, int(round(FEATURE_SIZE[1] * 0.56)))
    lower = slice(int(round(FEATURE_SIZE[1] * 0.56)), FEATURE_SIZE[1])
    record = {
        "nonempty": True,
        "x0": x0,
        "y0": y0,
        "x1": x1,
        "y1": y1,
        "baseline": y1,
        "height": height,
        "width": width,
        "cx": round(float(np.mean(xs)), 3),
        "cy": round(float(np.mean(ys)), 3),
        "lower_anchor_x": round(lower_anchor, 3),
        "upper_energy": round(float(np.mean(mask_small[upper])), 6),
        "lower_energy": round(float(np.mean(mask_small[lower])), 6),
    }
    return record, vector, mask_small


def feature_diff(previous: np.ndarray, current: np.ndarray) -> tuple[float, float, float, float]:
    mask_prev = previous[: FEATURE_SIZE[0] * FEATURE_SIZE[1]].reshape(FEATURE_SIZE[1], FEATURE_SIZE[0])
    mask_cur = current[: FEATURE_SIZE[0] * FEATURE_SIZE[1]].reshape(FEATURE_SIZE[1], FEATURE_SIZE[0])
    rgb_prev = previous[FEATURE_SIZE[0] * FEATURE_SIZE[1] :].reshape(FEATURE_SIZE[1], FEATURE_SIZE[0], 3)
    rgb_cur = current[FEATURE_SIZE[0] * FEATURE_SIZE[1] :].reshape(FEATURE_SIZE[1], FEATURE_SIZE[0], 3)
    mask_delta = float(np.mean(np.abs(mask_cur - mask_prev)))
    rgb_delta = float(np.mean(np.abs(rgb_cur - rgb_prev)))
    split = int(round(FEATURE_SIZE[1] * 0.56))
    upper_delta = float(np.mean(np.abs(mask_cur[:split] - mask_prev[:split])))
    lower_delta = float(np.mean(np.abs(mask_cur[split:] - mask_prev[split:])))
    return mask_delta, rgb_delta, upper_delta, lower_delta


def normalized_similarity(left: np.ndarray, right: np.ndarray) -> float:
    if left.shape != right.shape:
        return 0.0
    return float(1.0 - np.mean(np.abs(left - right)))


def expected_penalty(row: str, metrics: dict, row_metrics: dict, idle_profile: dict | None) -> tuple[float, list[str]]:
    penalty = 0.0
    reasons: list[str] = []
    motion_mean = float(row_metrics["motion_mean"])
    diversity = float(row_metrics["diversity"])
    upper_ratio = float(row_metrics["upper_lower_ratio"])
    vertical_range = float(row_metrics["vertical_range"])
    if row in STANDARD_ROWS and row != "idle" and diversity < 0.045:
        penalty += (0.045 - diversity) * 30.0
        reasons.append("low_row_diversity")
    if row == "idle":
        if motion_mean < 0.004:
            penalty += (0.004 - motion_mean) * 35.0
            reasons.append("idle_effectively_static")
        if motion_mean > 0.15:
            penalty += (motion_mean - 0.15) * 4.0
            reasons.append("idle_motion_too_large")
    elif row == "waving":
        if upper_ratio < 1.15:
            penalty += max(0.0, 1.15 - upper_ratio) * 1.6
            reasons.append("waving_upper_motion_not_dominant")
    elif row == "jumping":
        if vertical_range < 2.0:
            penalty += (2.0 - vertical_range) * 0.45
            reasons.append("jumping_vertical_range_low")
    elif row in {"waiting", "running", "review", "failed"} and idle_profile:
        idle_distance = float(row_metrics.get("idle_distance", 0.0))
        if idle_distance < 0.015:
            penalty += (0.015 - idle_distance) * 20.0
            reasons.append("too_close_to_idle")
        if row == "running" and upper_ratio < 1.05:
            penalty += max(0.0, 1.05 - upper_ratio) * 0.6
            reasons.append("running_upper_motion_not_visible")
    elif row in {"running-right", "running-left"}:
        if motion_mean < 0.012:
            penalty += (0.012 - motion_mean) * 8.0
            reasons.append("directional_row_low_motion")
    return penalty, reasons


def rgba_display(cell: Image.Image) -> Image.Image:
    rgba = np.asarray(cell, dtype=np.uint8)
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    background = np.full((CELL_H, CELL_W, 3), (74, 76, 84), dtype=np.float32)
    rgb = rgba[:, :, :3].astype(np.float32) * alpha + background * (1.0 - alpha)
    image = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")
    return image.resize(DISPLAY_SIZE, Image.Resampling.LANCZOS)


def diff_display(previous: Image.Image, current: Image.Image) -> Image.Image:
    previous_rgba = np.asarray(previous, dtype=np.uint8)
    current_rgba = np.asarray(current, dtype=np.uint8)
    previous_alpha = previous_rgba[:, :, 3:4].astype(np.float32) / 255.0
    current_alpha = current_rgba[:, :, 3:4].astype(np.float32) / 255.0
    previous_rgb = previous_rgba[:, :, :3].astype(np.float32) * previous_alpha
    current_rgb = current_rgba[:, :, :3].astype(np.float32) * current_alpha
    diff = np.mean(np.abs(current_rgb - previous_rgb), axis=2)
    diff = np.clip(diff * 3.0, 0, 255).astype(np.uint8)
    image = Image.fromarray(diff, mode="L").convert("RGB")
    return image.resize(DISPLAY_SIZE, Image.Resampling.NEAREST).filter(ImageFilter.GaussianBlur(radius=0.2))


def make_item(previous: Image.Image, current: Image.Image, next_cell: Image.Image, label: str, reason: str) -> Image.Image:
    canvas = Image.new("RGB", (SHEET_ITEM_W, SHEET_ITEM_H), (24, 24, 30))
    panels = [rgba_display(previous), rgba_display(current), rgba_display(next_cell), diff_display(previous, current)]
    for index, panel in enumerate(panels):
        canvas.paste(panel, (index * DISPLAY_SIZE[0], 20))
    draw = ImageDraw.Draw(canvas)
    draw.text((3, 3), label[:120], fill=(244, 244, 244))
    draw.text((3, SHEET_ITEM_H - 12), f"PREV  CURRENT  NEXT  DIFF   {reason[:42]}", fill=(185, 185, 195))
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or (output_dir / "state-semantics-review-20260831-v1.json")
    sheet_out = args.sheet_out or (output_dir / "state-semantics-candidates-v1.jpg")

    all_records: list[dict] = []
    row_profiles: list[dict] = []
    candidate_records: list[dict] = []
    candidate_images: list[Image.Image] = []

    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        with Image.open(atlas_path) as image:
            atlas = image.convert("RGBA")
            idle_first = feature_frame(open_cell(atlas, "idle", 0))[1]
            for row in ROWS:
                count = FRAME_COUNTS[row]
                cells = [open_cell(atlas, row, frame) for frame in range(count)]
                features = [feature_frame(cell) for cell in cells]
                vectors = [item[1] for item in features]
                records = [item[0] for item in features]
                transitions: list[dict] = []
                for frame in range(count):
                    previous = (frame - 1) % count
                    mask_delta, rgb_delta, upper_delta, lower_delta = feature_diff(vectors[previous], vectors[frame])
                    transitions.append(
                        {
                            "role": role,
                            "row": row,
                            "frame": frame,
                            "previous_frame": previous,
                            "mask_delta": round(mask_delta, 6),
                            "rgb_delta": round(rgb_delta, 6),
                            "upper_delta": round(upper_delta, 6),
                            "lower_delta": round(lower_delta, 6),
                            "centroid_dx": round(records[frame]["cx"] - records[previous]["cx"], 3),
                            "centroid_dy": round(records[frame]["cy"] - records[previous]["cy"], 3),
                            "height": records[frame]["height"],
                            "baseline": records[frame]["baseline"],
                        }
                    )
                motion_values = np.asarray([item["mask_delta"] + 0.35 * item["rgb_delta"] for item in transitions], dtype=np.float32)
                upper_values = np.asarray([item["upper_delta"] for item in transitions], dtype=np.float32)
                lower_values = np.asarray([item["lower_delta"] for item in transitions], dtype=np.float32)
                heights = np.asarray([item["height"] for item in transitions], dtype=np.float32)
                vertical_values = np.asarray([item["centroid_dy"] for item in transitions], dtype=np.float32)
                diversity = 1.0 - float(np.mean([normalized_similarity(vectors[index], vectors[(index + 1) % count]) for index in range(count)]))
                idle_distance = float(1.0 - normalized_similarity(np.mean(vectors, axis=0), idle_first))
                row_profile = {
                    "role": role,
                    "row": row,
                    "frame_count": count,
                    "motion_mean": round(float(np.mean(motion_values)), 6),
                    "motion_p95": round(float(np.percentile(motion_values, 95)), 6),
                    "upper_motion_mean": round(float(np.mean(upper_values)), 6),
                    "lower_motion_mean": round(float(np.mean(lower_values)), 6),
                    "upper_lower_ratio": round(float(np.mean(upper_values) / max(np.mean(lower_values), 1e-6)), 6),
                    "height_range": [int(np.min(heights)), int(np.max(heights))],
                    "vertical_range": round(float(np.ptp(np.cumsum(vertical_values))), 6),
                    "diversity": round(diversity, 6),
                    "idle_distance": round(idle_distance, 6),
                }
                row_profiles.append(row_profile)
                for item in transitions:
                    penalty, reasons = expected_penalty(row, item, row_profile, row_profile if row != "idle" else None)
                    z_motion = robust_z(item["mask_delta"] + 0.35 * item["rgb_delta"], motion_values)
                    z_upper = robust_z(item["upper_delta"], upper_values)
                    z_lower = robust_z(item["lower_delta"], lower_values)
                    item["score"] = round(float(min(24.0, 0.45 * z_motion + 0.2 * z_upper + 0.1 * z_lower + penalty)), 6)
                    item["reasons"] = reasons
                    item["known_blocker"] = None
                    known = KNOWN_BLOCKERS.get((role, row))
                    if known and item["frame"] in known["frames"]:
                        item["known_blocker"] = known["description"]
                    all_records.append(item)

                known_frames = set(KNOWN_BLOCKERS.get((role, row), {}).get("frames", []))
                if known_frames:
                    # Keep the report complete, but cap controls on the visual
                    # sheet so non-control candidates remain visible too.
                    ordered_controls = sorted(known_frames)
                    if len(ordered_controls) > 3:
                        selected = {
                            ordered_controls[0],
                            ordered_controls[len(ordered_controls) // 2],
                            ordered_controls[-1],
                        }
                    else:
                        selected = known_frames
                else:
                    selected = {max(transitions, key=lambda item: float(item["score"]))["frame"]}
                for frame in selected:
                    current = transitions[frame]
                    candidate_records.append({**current, "row_profile": row_profile})
                    previous = current["previous_frame"]
                    next_frame = (frame + 1) % count
                    reason = current["known_blocker"] or ",".join(current["reasons"]) or "metric_outlier"
                    candidate_images.append(
                        make_item(
                            cells[previous],
                            cells[frame],
                            cells[next_frame],
                            f"{role}/{row} f{previous}->{frame}->{next_frame} score={current['score']:.2f}",
                            reason,
                        )
                    )

    # Keep the sheet bounded but retain every known control.
    control_images: list[tuple[dict, Image.Image]] = []
    non_control_images: list[tuple[dict, Image.Image]] = []
    for record, image in zip(candidate_records, candidate_images):
        (control_images if record["known_blocker"] else non_control_images).append((record, image))
    non_control_images.sort(key=lambda item: (-float(item[0]["score"]), item[0]["role"], item[0]["row"], item[0]["frame"]))
    selected_pairs = control_images + non_control_images[: max(0, 36 - len(control_images))]
    if selected_pairs:
        rows = math.ceil(len(selected_pairs) / SHEET_COLUMNS)
        sheet = Image.new("RGB", (SHEET_COLUMNS * SHEET_ITEM_W, rows * SHEET_ITEM_H), (24, 24, 30))
        for index, (_, image) in enumerate(selected_pairs):
            sheet.paste(image, ((index % SHEET_COLUMNS) * SHEET_ITEM_W, (index // SHEET_COLUMNS) * SHEET_ITEM_H))
        sheet.save(sheet_out, quality=92, optimize=True)

    all_records.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], item["frame"]))
    report = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "evidence-only state-intent and animation-degeneracy review of the eight current v2 atlases",
        "method": {
            "name": "state-intent motion signature and non-adjacent repetition review",
            "purpose": "以统一下半身锚点和基线比较帧间 alpha/RGB 变化、上/下半身运动分布、循环多样性和 idle 距离，筛选动作退化、过度重复、错误身体部位主导或状态塌缩候选",
            "features": [
                "lower-body-anchor and baseline normalized 48x52 alpha/RGB vectors",
                "circular previous/current transition mask and color deltas",
                "upper/lower motion ratio and vertical trajectory range",
                "adjacent loop diversity and distance from the role idle reference",
            ],
            "selection": "metrics select candidates only; known blockers are controls and all promotions require normal-size visual review",
            "sheet": str(sheet_out.relative_to(repo)),
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "standard_rows": len(ROLES) * len(STANDARD_ROWS),
            "frames": len(ROLES) * sum(FRAME_COUNTS.values()),
            "standard_frames": len(ROLES) * sum(FRAME_COUNTS[row] for row in STANDARD_ROWS),
            "circular_transitions": len(all_records),
            "candidate_sheet_items": len(selected_pairs),
        },
        "row_profiles": row_profiles,
        "candidates": all_records[:120],
        "known_controls": [
            {"role": role, "row": row, "frames": data["frames"], "description": data["description"]}
            for (role, row), data in KNOWN_BLOCKERS.items()
        ],
        "result": {
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
                "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
                "hei-mao-quality/running-left complete-row detached component/action structure issue",
                "hei-mao-quality/failed complete-row detached component/action structure issue",
                "hei-mao-traveler/waiting complete-row detached component/action structure issue",
                "hei-mao-traveler/review complete-row detached component/action structure issue",
            ],
            "formal_assets_modified": False,
            "release_effect": "supplemental evidence only; no candidate is promoted automatically and the eight complete-row regeneration blockers remain open",
        },
        "limitations": [
            "动作语义不能仅由 alpha/RGB 运动量完全判定，候选必须结合正常尺寸和动作提示人工查看",
            "上/下半身区域是统一几何切分，不等同于真实关节或道具分割",
            "look-row-9/10 的方向语义仍以 cardinal、盲测和有标签方向回环为准",
            "这是资产级复核，不能替代 Codex App GPU、窗口层级、多屏气泡跟随或用户实机验收",
        ],
    }
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "json_out": str(json_out),
                "sheet_out": str(sheet_out),
                "records": len(all_records),
                "sheet_items": len(selected_pairs),
                "new_hard_failures": [],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
