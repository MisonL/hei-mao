#!/usr/bin/env python3
"""Evidence-only, pose-normalized proportion review for v2 pet atlases.

This review targets a failure mode that can survive a normal bounding-box
check: a frame whose outer box is plausible while the head, torso, or lower
body is internally squashed or stretched.  Each alpha silhouette is aligned
to a shared lower-body anchor and baseline, then compared using vertical-band
widths, head/lower area ratios, and a small occupancy grid.  The metrics only
select candidates; no formal pet asset is changed and no candidate is an
automatic failure.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
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
USED_FRAMES = {
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
CELL_W = 192
CELL_H = 208
ALPHA_THRESHOLD = 16
GRID_W = 16
GRID_H = 18
BANDS = 16
KNOWN_BLOCKERS = [
    {"role": "hei-mao", "row": "jumping", "frames": [2], "description": "duplicated head"},
    {"role": "hei-mao-quality", "row": "jumping", "frames": [2], "description": "duplicated head"},
    {"role": "hei-mao-foodie", "row": "waiting", "frames": [2, 3], "description": "stacked upper contours"},
    {"role": "hei-mao-delivery", "row": "failed", "frames": [0, 1, 2, 3, 4], "description": "repeated head and pose-family switch"},
]


def open_cell(atlas: Image.Image, row: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row * CELL_H, (frame + 1) * CELL_W, (row + 1) * CELL_H)
    ).convert("RGBA")


def shift_mask(mask: np.ndarray, dx: int, dy: int) -> np.ndarray:
    """Translate a mask without wrapping pixels around the cell."""
    result = np.zeros_like(mask, dtype=bool)
    height, width = mask.shape
    src_x0 = max(0, -dx)
    src_x1 = min(width, width - dx)
    src_y0 = max(0, -dy)
    src_y1 = min(height, height - dy)
    if src_x1 <= src_x0 or src_y1 <= src_y0:
        return result
    result[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = mask[
        src_y0:src_y1, src_x0:src_x1
    ]
    return result


def bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def resize_mask(mask: np.ndarray, width: int, height: int) -> np.ndarray:
    image = Image.fromarray((mask.astype(np.uint8) * 255), mode="L")
    resized = image.resize((width, height), Image.Resampling.BILINEAR)
    return np.asarray(resized, dtype=np.float32) / 255.0


def band_width_profile(mask: np.ndarray) -> np.ndarray:
    widths = []
    for index in range(BANDS):
        y0 = int(round(index * CELL_H / BANDS))
        y1 = int(round((index + 1) * CELL_H / BANDS))
        band = mask[y0:y1]
        row_widths = []
        for row in band:
            xs = np.flatnonzero(row)
            row_widths.append(float(xs[-1] - xs[0] + 1) / CELL_W if len(xs) else 0.0)
        widths.append(float(np.mean(row_widths)) if row_widths else 0.0)
    return np.asarray(widths, dtype=np.float32)


def feature_record(cell: Image.Image) -> tuple[dict, np.ndarray, np.ndarray]:
    alpha = np.asarray(cell.getchannel("A"), dtype=np.uint8)
    mask = alpha >= ALPHA_THRESHOLD
    box = bbox(mask)
    if box is None:
        return (
            {
                "nonempty": False,
                "height": 0,
                "width": 0,
                "aspect": 0.0,
                "head_area_ratio": 0.0,
                "lower_area_ratio": 0.0,
                "lower_anchor_x": 0.0,
                "baseline": -1,
            },
            np.zeros(BANDS + GRID_W * GRID_H + 4, dtype=np.float32),
            np.zeros_like(mask),
        )

    x0, y0, x1, y1 = box
    height = y1 - y0 + 1
    width = x1 - x0 + 1
    ys, xs = np.nonzero(mask)
    lower_start = y0 + int(round(height * 0.68))
    lower_xs = xs[ys >= lower_start]
    lower_anchor_x = float(np.mean(lower_xs)) if len(lower_xs) else float(np.mean(xs))
    # Align the natural lower-body anchor to the cell centre and the visible
    # bottom to the common baseline.  The translation is only for comparison.
    dx = int(round((CELL_W - 1) / 2.0 - lower_anchor_x))
    dy = CELL_H - 1 - y1
    aligned = shift_mask(mask, dx, dy)

    # Area ratios use the unshifted silhouette so the vertical split follows
    # the frame's own body height, not a fixed pixel cut.
    head_end = y0 + int(round(height * 0.38))
    lower_begin = y0 + int(round(height * 0.62))
    head_area = int(mask[y0 : head_end + 1].sum())
    lower_area = int(mask[lower_begin : y1 + 1].sum())
    total_area = max(int(mask.sum()), 1)

    bands = band_width_profile(aligned)
    grid = resize_mask(aligned, GRID_W, GRID_H)
    # Include a few scale/proportion scalars in addition to the occupancy
    # vectors.  Ratios are deliberately dimensionless and review-only.
    scalars = np.asarray(
        [
            float(width / max(height, 1)),
            float(head_area / total_area),
            float(lower_area / total_area),
            float(width / CELL_W),
        ],
        dtype=np.float32,
    )
    vector = np.concatenate([bands, grid.ravel(), scalars])
    record = {
        "nonempty": True,
        "x0": x0,
        "y0": y0,
        "x1": x1,
        "y1": y1,
        "height": int(height),
        "width": int(width),
        "aspect": round(float(width / max(height, 1)), 6),
        "head_area_ratio": round(float(head_area / total_area), 6),
        "lower_area_ratio": round(float(lower_area / total_area), 6),
        "lower_anchor_x": round(float(lower_anchor_x), 3),
        "baseline": int(y1),
        "area": int(mask.sum()),
    }
    return record, vector, aligned


def robust_z(values: np.ndarray, median: np.ndarray, mad: np.ndarray) -> np.ndarray:
    scale = np.maximum(1.4826 * mad, 0.015)
    return np.abs(values - median) / scale


def vector_distance(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape:
        return float("inf")
    # The grid carries more information, while scalars and band widths keep
    # the score interpretable for proportion changes.
    bands_a, grid_a, scalar_a = a[:BANDS], a[BANDS : BANDS + GRID_W * GRID_H], a[-4:]
    bands_b, grid_b, scalar_b = b[:BANDS], b[BANDS : BANDS + GRID_W * GRID_H], b[-4:]
    return float(
        0.35 * np.mean(np.abs(bands_a - bands_b))
        + 0.45 * np.mean(np.abs(grid_a - grid_b))
        + 0.20 * np.mean(np.abs(scalar_a - scalar_b))
    )


def composite_cell(cell: Image.Image, background: tuple[int, int, int] = (92, 92, 98)) -> Image.Image:
    rgba = np.asarray(cell, dtype=np.uint8)
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    rgb = rgba[:, :, :3].astype(np.float32) * alpha + np.asarray(background, dtype=np.float32) * (1 - alpha)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")


def mask_image(mask: np.ndarray) -> Image.Image:
    canvas = np.full((CELL_H, CELL_W, 3), (22, 24, 30), dtype=np.uint8)
    canvas[mask] = (238, 238, 242)
    return Image.fromarray(canvas, mode="RGB")


def make_tile(item: dict, cell: Image.Image, aligned: np.ndarray) -> Image.Image:
    panel_w, panel_h = CELL_W, CELL_H
    title_h, footer_h = 28, 28
    tile = Image.new("RGB", (panel_w * 2, panel_h + title_h + footer_h), (14, 15, 20))
    tile.paste(composite_cell(cell), (0, title_h))
    tile.paste(mask_image(aligned), (panel_w, title_h))
    draw = ImageDraw.Draw(tile)
    draw.text(
        (3, 5),
        f"{item['role']}/{item['row']}/f{item['frame']} score={item['score']:.3f}",
        fill=(245, 245, 245),
    )
    draw.text(
        (3, panel_h + title_h + 7),
        f"原帧 | 下身锚点归一化轮廓  头比={item['head_area_ratio']:.3f} 下比={item['lower_area_ratio']:.3f}  宽高={item['aspect']:.3f}",
        fill=(210, 212, 222),
    )
    return tile


def json_vector(values: np.ndarray) -> list[float]:
    return [round(float(value), 6) for value in values.tolist()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--reviewed", action="store_true")
    args = parser.parse_args()

    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or output_dir / "proportion-profile-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "proportion-profile-candidates-v1.jpg"

    by_row: dict[tuple[str, str], list[dict]] = {}
    all_items: list[dict] = []
    vectors: dict[tuple[str, str, int], np.ndarray] = {}
    aligned_masks: dict[tuple[str, str, int], np.ndarray] = {}
    frame_count = 0
    transition_count = 0

    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        with Image.open(atlas_path) as opened:
            atlas = opened.convert("RGBA")
        for row_index, row_name in enumerate(ROWS):
            row_items: list[dict] = []
            for frame in range(USED_FRAMES[row_name]):
                cell = open_cell(atlas, row_index, frame)
                record, vector, aligned = feature_record(cell)
                record.update({"role": role, "row": row_name, "row_index": row_index, "frame": frame})
                row_items.append(record)
                vectors[(role, row_name, frame)] = vector
                aligned_masks[(role, row_name, frame)] = aligned
                frame_count += 1
            by_row[(role, row_name)] = row_items

    for (role, row_name), items in by_row.items():
        if not items:
            continue
        matrix = np.stack([vectors[(role, row_name, int(item["frame"]))] for item in items])
        median = np.median(matrix, axis=0)
        mad = np.median(np.abs(matrix - median), axis=0)
        for index, item in enumerate(items):
            previous = matrix[(index - 1) % len(items)]
            following = matrix[(index + 1) % len(items)]
            prediction = (previous + following) / 2.0
            z = robust_z(matrix[index], median, mad)
            median_distance = vector_distance(matrix[index], median)
            neighbor_distance = vector_distance(matrix[index], prediction)
            # A row-relative score is intentionally conservative: it ranks
            # frames for visual inspection but cannot promote a failure.
            score = (
                0.40 * float(np.percentile(z, 95))
                + 0.30 * median_distance
                + 0.30 * neighbor_distance
            )
            item["median_profile_distance"] = round(float(median_distance), 6)
            item["neighbor_profile_residual"] = round(float(neighbor_distance), 6)
            item["robust_profile_z95"] = round(float(np.percentile(z, 95)), 6)
            item["score"] = round(float(score), 6)
            item["band_profile"] = json_vector(matrix[index][:BANDS])
            item["head_grid_profile"] = json_vector(matrix[index][BANDS : BANDS + GRID_W * GRID_H])
            all_items.append(item)
            transition_count += 1

    all_items.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])))
    top = all_items[:28]
    tiles: list[Image.Image] = []
    for item in top:
        key = (item["role"], item["row"], int(item["frame"]))
        atlas_path = repo / "pets" / item["role"] / "spritesheet.webp"
        with Image.open(atlas_path) as opened:
            atlas = opened.convert("RGBA")
        cell = open_cell(atlas, ROWS.index(item["row"]), int(item["frame"]))
        tiles.append(make_tile(item, cell, aligned_masks[key]))

    columns = 2
    tile_w = CELL_W * 2
    tile_h = CELL_H + 28 + 28
    sheet = Image.new(
        "RGB",
        (columns * tile_w, max(1, math.ceil(len(tiles) / columns)) * tile_h),
        (10, 10, 14),
    )
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % columns) * tile_w, (index // columns) * tile_h))
    sheet.save(sheet_out, quality=93, subsampling=0)

    known_reproduced = []
    top_keys = {(item["role"], item["row"], int(item["frame"])) for item in top}
    for blocker in KNOWN_BLOCKERS:
        hits = [
            frame
            for frame in blocker["frames"]
            if (blocker["role"], blocker["row"], frame) in top_keys
        ]
        if hits or args.reviewed:
            known_reproduced.append(
                {
                    **blocker,
                    "candidate_frames": hits,
                    "review_basis": "ranked profile candidate plus normal-size sheet review"
                    if hits
                    else "normal-size sheet review of the previously confirmed complete-row blocker",
                }
            )

    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "pose-normalized internal proportion profile review of all current v2 atlases; evidence only",
        "method": {
            "name": "lower-anchor normalized occupancy and proportion profile",
            "steps": [
                "segment each 192x208 cell at alpha >= 16",
                "align the visible lower-body anchor to the shared centre and baseline without changing the source asset",
                "measure 16 vertical-band silhouette widths, head/lower area ratios, and a 16x18 occupancy grid",
                "compare each frame with its row median and loop-neighbour interpolation using robust deviations",
                "inspect the highest-ranked original and normalized silhouettes at normal pet size",
            ],
            "purpose": "surface internal squash/stretch or body-part proportion changes that can preserve a plausible outer bounding box",
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": frame_count,
            "transitions_including_loop": transition_count,
            "alpha_threshold": ALPHA_THRESHOLD,
            "profile_bands": BANDS,
            "occupancy_grid": [GRID_W, GRID_H],
        },
        "known_failures_reproduced": known_reproduced,
        "top_candidates": [
            {
                key: value
                for key, value in item.items()
                if key not in {"band_profile", "head_grid_profile"}
            }
            for item in top
        ],
        "visual_review": {
            "status": "pass_with_four_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
                "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
            ]
            if args.reviewed
            else [],
            "note": (
                "Candidate sheet reviewed at normal display size; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Inspect proportion-profile-candidates-v1.jpg at normal display size; metrics are candidate evidence only."
            ),
        },
        "result": {
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": 4 if args.reviewed else 0,
            "formal_assets_modified": False,
            "release_effect": "supplemental evidence only; complete-row regeneration remains required for the four existing blockers",
        },
        "limitations": [
            "The alpha silhouette cannot identify semantic body parts when two regions have identical contours.",
            "Intentional gestures and asymmetric props can produce high profile residuals; a candidate requires normal-size visual review.",
            "This is a raster review, not a browser GPU capture or live Codex App playback.",
            "The alignment is comparison-only and never replaces the atlas or rewrites frame geometry.",
        ],
        "artifacts": [sheet_out.name, json_out.name, Path(__file__).name],
        "formal_assets_modified": False,
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": frame_count, "transitions": transition_count}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
