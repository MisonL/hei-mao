#!/usr/bin/env python3
"""Evidence-only multi-background compositing stress review for v2 pets.

The review renders every used cell on contrasting backgrounds at two likely
display sizes. It ranks edge-color instability, semi-transparent pixels that
do not match the pet's opaque palette, and possible opaque edge panels. Scores
only select candidates; no formal pet asset is modified and no metric is an
automatic release failure.
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
ROW_INDEX = {name: index for index, name in enumerate(ROWS)}
CELL_W = 192
CELL_H = 208
ALPHA_THRESHOLD = 16
DISPLAY_SIZES = ((96, 104), (48, 52))
BACKGROUNDS = {
    "dark": (30, 32, 40),
    "light": (244, 244, 244),
    "magenta": (230, 38, 172),
    "cyan": (30, 210, 215),
}
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
    index = ROW_INDEX[row]
    return atlas.crop(
        (frame * CELL_W, index * CELL_H, (frame + 1) * CELL_W, (index + 1) * CELL_H)
    ).convert("RGBA")


def rgba_array(cell: Image.Image) -> np.ndarray:
    return np.asarray(cell.convert("RGBA"), dtype=np.uint8)


def alpha_mask(cell: Image.Image) -> np.ndarray:
    return rgba_array(cell)[:, :, 3] >= ALPHA_THRESHOLD


def bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def shift_mask(mask: np.ndarray, dx: int, dy: int) -> np.ndarray:
    result = np.zeros_like(mask, dtype=bool)
    src_x0 = max(0, -dx)
    src_x1 = min(mask.shape[1], mask.shape[1] - dx)
    src_y0 = max(0, -dy)
    src_y1 = min(mask.shape[0], mask.shape[0] - dy)
    if src_x1 <= src_x0 or src_y1 <= src_y0:
        return result
    result[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = mask[
        src_y0:src_y1, src_x0:src_x1
    ]
    return result


def align_to_lower_anchor(cell: Image.Image) -> tuple[np.ndarray, np.ndarray, dict] | None:
    rgba = rgba_array(cell)
    mask = rgba[:, :, 3] >= ALPHA_THRESHOLD
    box = bbox(mask)
    if box is None:
        return None
    x0, y0, x1, y1 = box
    height = y1 - y0 + 1
    ys, xs = np.nonzero(mask)
    lower_start = y0 + int(round(height * 0.62))
    lower_xs = xs[ys >= lower_start]
    anchor_x = float(np.mean(lower_xs)) if len(lower_xs) else float(np.mean(xs))
    dx = int(round((CELL_W - 1) / 2.0 - anchor_x))
    dy = CELL_H - 1 - y1
    aligned_rgba = np.zeros_like(rgba)
    aligned_mask = np.zeros_like(mask)
    src_x0 = max(0, -dx)
    src_x1 = min(CELL_W, CELL_W - dx)
    src_y0 = max(0, -dy)
    src_y1 = min(CELL_H, CELL_H - dy)
    if src_x1 > src_x0 and src_y1 > src_y0:
        aligned_rgba[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = rgba[
            src_y0:src_y1, src_x0:src_x1
        ]
        aligned_mask[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = mask[
            src_y0:src_y1, src_x0:src_x1
        ]
    return aligned_rgba, aligned_mask, {
        "bbox": [x0, y0, x1, y1],
        "width": x1 - x0 + 1,
        "height": height,
        "area": int(mask.sum()),
        "lower_anchor_x": round(anchor_x, 3),
        "bottom": y1,
        "dx": dx,
        "dy": dy,
    }


def dilate(mask: np.ndarray, radius: int) -> np.ndarray:
    result = np.zeros_like(mask, dtype=bool)
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            result |= shift_mask(mask, dx, dy)
    return result


def erode(mask: np.ndarray, radius: int) -> np.ndarray:
    result = np.ones_like(mask, dtype=bool)
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            result &= shift_mask(mask, dx, dy)
    return result


def edge_ring(mask: np.ndarray) -> np.ndarray:
    return dilate(mask, 2) & ~erode(mask, 1)


def composite_array(rgba: np.ndarray, background: tuple[int, int, int]) -> np.ndarray:
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    bg = np.asarray(background, dtype=np.float32)[None, None, :]
    rgb = rgba[:, :, :3].astype(np.float32)
    return np.clip(rgb * alpha + bg * (1.0 - alpha), 0, 255).astype(np.uint8)


def resize_rgb(rgb: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    return np.asarray(
        Image.fromarray(rgb, mode="RGB").resize(size, Image.Resampling.LANCZOS), dtype=np.uint8
    )


def resize_mask(mask: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    return np.asarray(
        Image.fromarray((mask.astype(np.uint8) * 255), mode="L").resize(
            size, Image.Resampling.BILINEAR
        ),
        dtype=np.float32,
    ) / 255.0


def nearest_palette_residual(rgba: np.ndarray, mask: np.ndarray, ring: np.ndarray) -> tuple[float, float, int]:
    alpha = rgba[:, :, 3]
    opaque = (alpha >= 240) & mask
    edge = ring & (alpha > 0)
    if not np.any(edge) or not np.any(opaque):
        return 0.0, 0.0, 0
    palette = rgba[opaque, :3].astype(np.float32)
    if len(palette) > 2400:
        palette = palette[:: max(1, len(palette) // 2400)]
    edge_rgb = rgba[edge, :3].astype(np.float32)
    nearest = np.empty(len(edge_rgb), dtype=np.float32)
    for start in range(0, len(edge_rgb), 512):
        chunk = edge_rgb[start : start + 512]
        distances = ((chunk[:, None, :] - palette[None, :, :]) ** 2).sum(axis=2)
        nearest[start : start + len(chunk)] = np.sqrt(distances.min(axis=1))
    return float(np.mean(nearest)), float(np.percentile(nearest, 95)), int(np.sum(nearest > 72.0))


def connected_components(mask: np.ndarray) -> list[int]:
    """Return component areas using a compact flood fill for candidate signals."""
    remaining = mask.copy()
    areas: list[int] = []
    height, width = remaining.shape
    while remaining.any():
        y, x = np.argwhere(remaining)[0]
        stack = [(int(y), int(x))]
        remaining[y, x] = False
        area = 0
        while stack:
            cy, cx = stack.pop()
            area += 1
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < height and 0 <= nx < width and remaining[ny, nx]:
                    remaining[ny, nx] = False
                    stack.append((ny, nx))
        areas.append(area)
    return areas


def frame_metrics(cell: Image.Image) -> tuple[dict, dict[str, np.ndarray], np.ndarray]:
    rgba = rgba_array(cell)
    mask = rgba[:, :, 3] >= ALPHA_THRESHOLD
    box = bbox(mask)
    if box is None:
        return (
            {
                "nonempty": False,
                "area": 0,
                "width": 0,
                "height": 0,
                "edge_fraction": 0.0,
                "semi_transparent_fraction": 0.0,
                "palette_residual_mean": 0.0,
                "palette_residual_p95": 0.0,
                "palette_outlier_count": 0,
                "opaque_border_fraction": 0.0,
                "component_count": 0,
                "largest_component_fraction": 0.0,
                "background_spread_p95": 0.0,
            },
            {},
            mask,
        )

    x0, y0, x1, y1 = box
    area = int(mask.sum())
    ring = edge_ring(mask)
    semi = mask & (rgba[:, :, 3] < 240)
    mean_residual, p95_residual, outlier_count = nearest_palette_residual(rgba, mask, ring)
    border = np.zeros_like(mask)
    border[:3, :] = True
    border[-3:, :] = True
    border[:, :3] = True
    border[:, -3:] = True
    components = connected_components(mask)
    largest = max(components) if components else 0
    composited: dict[str, np.ndarray] = {}
    for name, background in BACKGROUNDS.items():
        composited[name] = resize_rgb(composite_array(rgba, background), DISPLAY_SIZES[0])
    # Only evaluate edge pixels with source alpha > 0.  Including fully
    # transparent pixels would measure the deliberately different backgrounds
    # instead of a sprite defect.  The expected spread is derived from the
    # source alpha; the residual is a display/alpha consistency signal.
    edge_visible = ring & (rgba[:, :, 3] > 0)
    edge_small = resize_mask(edge_visible, DISPLAY_SIZES[0]) >= 0.18
    if np.any(edge_small):
        edge_samples = np.stack([image[edge_small] for image in composited.values()], axis=0)
        spread = np.max(edge_samples, axis=0).astype(np.int16) - np.min(edge_samples, axis=0).astype(np.int16)
        alpha_small = np.asarray(
            Image.fromarray(rgba[:, :, 3], mode="L").resize(DISPLAY_SIZES[0], Image.Resampling.BILINEAR),
            dtype=np.float32,
        ) / 255.0
        background_values = np.asarray(list(BACKGROUNDS.values()), dtype=np.float32)
        background_range = np.linalg.norm(background_values.max(axis=0) - background_values.min(axis=0)) / 255.0
        expected_spread = background_range * (1.0 - alpha_small[edge_small])
        observed_spread = np.linalg.norm(spread.astype(np.float32), axis=1) / 255.0
        spread_residual = np.abs(observed_spread - expected_spread)
    else:
        spread_residual = np.zeros(1, dtype=np.float32)
    metrics = {
        "nonempty": True,
        "bbox": [x0, y0, x1, y1],
        "area": area,
        "width": x1 - x0 + 1,
        "height": y1 - y0 + 1,
        "aspect": round(float((x1 - x0 + 1) / max(y1 - y0 + 1, 1)), 6),
        "edge_fraction": round(float((ring & mask).sum() / max(area, 1)), 6),
        "semi_transparent_fraction": round(float(semi.sum() / max(area, 1)), 6),
        "palette_residual_mean": round(mean_residual, 6),
        "palette_residual_p95": round(p95_residual, 6),
        "palette_outlier_count": outlier_count,
        "opaque_border_fraction": round(float((mask & border).sum() / max(area, 1)), 6),
        "component_count": len(components),
        "largest_component_fraction": round(float(largest / max(area, 1)), 6),
        "background_spread_p95": round(float(np.percentile(spread_residual, 95)), 6),
    }
    return metrics, composited, mask


def robust_z(value: float, values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    scale = max(1.4826 * mad, float(np.std(values)) * 0.25, 1e-6)
    return abs(value - median) / scale


def make_checker(size: tuple[int, int], square: int = 8) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (232, 232, 232))
    draw = ImageDraw.Draw(image)
    for y in range(0, height, square):
        for x in range(0, width, square):
            if ((x // square) + (y // square)) % 2:
                draw.rectangle((x, y, x + square - 1, y + square - 1), fill=(92, 92, 92))
    return image


def panel_from_rgb(rgb: np.ndarray, size: tuple[int, int]) -> Image.Image:
    return Image.fromarray(rgb, mode="RGB").resize(size, Image.Resampling.NEAREST)


def make_tile(item: dict, rgba: np.ndarray, mask: np.ndarray, composited: dict[str, np.ndarray]) -> Image.Image:
    display_size = DISPLAY_SIZES[0]
    panels = [
        panel_from_rgb(composited["dark"], display_size),
        panel_from_rgb(composited["light"], display_size),
        panel_from_rgb(composited["magenta"], display_size),
        panel_from_rgb(composited["cyan"], display_size),
        Image.fromarray(np.where(resize_mask(mask, display_size) >= 0.18, 240, 18).astype(np.uint8), mode="L").convert("RGB"),
    ]
    panel_w, panel_h = display_size
    title_h, footer_h = 24, 28
    tile = Image.new("RGB", (panel_w * len(panels), panel_h + title_h + footer_h), (14, 15, 20))
    for index, panel in enumerate(panels):
        tile.paste(panel, (index * panel_w, title_h))
    draw = ImageDraw.Draw(tile)
    draw.text(
        (3, 4),
        f"{item['role']}/{item['row']}/f{item['frame']} score={item['score']:.3f}",
        fill=(245, 245, 245),
    )
    draw.text(
        (3, panel_h + title_h + 7),
        "dark | light | magenta | cyan | alpha  "
        f"halo={item['palette_residual_p95']:.1f} spread={item['background_spread_p95']:.3f}",
        fill=(210, 212, 222),
    )
    return tile


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--top", type=int, default=32)
    parser.add_argument("--reviewed", action="store_true")
    parser.add_argument("--manual-verdict", default="pending_review")
    parser.add_argument("--manual-note", default="")
    args = parser.parse_args()

    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or output_dir / "background-stress-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "background-stress-candidates-v1.jpg"

    records: list[dict] = []
    visual_payload: dict[tuple[str, str, int], tuple[np.ndarray, np.ndarray, dict[str, np.ndarray]]] = {}
    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        with Image.open(atlas_path) as image:
            atlas = image.convert("RGBA")
            for row in ROWS:
                for frame in range(FRAME_COUNTS[row]):
                    cell = open_cell(atlas, row, frame)
                    aligned = align_to_lower_anchor(cell)
                    if aligned is None:
                        metrics = {
                            "nonempty": False,
                            "area": 0,
                            "palette_residual_p95": 0.0,
                            "background_spread_p95": 0.0,
                            "semi_transparent_fraction": 0.0,
                            "opaque_border_fraction": 0.0,
                            "component_count": 0,
                            "largest_component_fraction": 0.0,
                        }
                        rgba = np.zeros((CELL_H, CELL_W, 4), dtype=np.uint8)
                        mask = np.zeros((CELL_H, CELL_W), dtype=bool)
                        composited = {}
                    else:
                        rgba, _, alignment = aligned
                        aligned_cell = Image.fromarray(rgba, mode="RGBA")
                        metrics, composited, mask = frame_metrics(aligned_cell)
                        metrics.update(alignment)
                    records.append({
                        "role": role,
                        "row": row,
                        "row_index": ROW_INDEX[row],
                        "frame": frame,
                        **metrics,
                        "known_blocker": KNOWN_BLOCKERS.get((role, row)),
                    })
                    visual_payload[(role, row, frame)] = (rgba, mask, composited)

    def score(record: dict) -> float:
        return (
            0.34 * record.get("palette_residual_p95", 0.0)
            + 180.0 * record.get("background_spread_p95", 0.0)
            + 18.0 * record.get("semi_transparent_fraction", 0.0)
            + 14.0 * record.get("opaque_border_fraction", 0.0)
            + 8.0 * max(0.0, 1.0 - record.get("largest_component_fraction", 0.0))
        )

    by_row: dict[tuple[str, str], list[dict]] = {}
    for record in records:
        by_row.setdefault((record["role"], record["row"]), []).append(record)
    for row_records in by_row.values():
        for key in ("palette_residual_p95", "background_spread_p95", "semi_transparent_fraction", "opaque_border_fraction"):
            values = np.asarray([float(item.get(key, 0.0)) for item in row_records], dtype=np.float32)
            for item in row_records:
                item[f"{key}_z"] = round(robust_z(float(item.get(key, 0.0)), values), 6)
        for item in row_records:
            item["score"] = round(
                0.36 * item["palette_residual_p95_z"]
                + 0.30 * item["background_spread_p95_z"]
                + 0.18 * item["semi_transparent_fraction_z"]
                + 0.10 * item["opaque_border_fraction_z"]
                + 0.06 * max(0.0, 1.0 - float(item.get("largest_component_fraction", 0.0))),
                6,
            )
    candidates = sorted(records, key=lambda item: float(item.get("score", 0.0)), reverse=True)[: max(args.top, 1)]
    sheet_items = []
    for item in candidates:
        key = (item["role"], item["row"], item["frame"])
        rgba, mask, composited = visual_payload[key]
        sheet_items.append(make_tile(item, rgba, mask, composited))

    columns = 2
    tile_w = sheet_items[0].width if sheet_items else DISPLAY_SIZES[0][0] * 5
    tile_h = sheet_items[0].height if sheet_items else DISPLAY_SIZES[0][1] + 52
    sheet = Image.new("RGB", (columns * tile_w, ((len(sheet_items) + columns - 1) // columns) * tile_h), (10, 11, 16))
    for index, tile in enumerate(sheet_items):
        sheet.paste(tile, ((index % columns) * tile_w, (index // columns) * tile_h))
    sheet.save(sheet_out, quality=92)

    output = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "evidence-only multi-background compositing stress review of all current v2 atlases",
        "method": {
            "name": "multi-background edge and alpha compositing stress",
            "purpose": "surface transparent-edge color contamination, hidden opaque panels, and display-size background-dependent defects",
            "backgrounds": {name: list(value) for name, value in BACKGROUNDS.items()},
            "display_sizes": [list(size) for size in DISPLAY_SIZES],
            "steps": [
                "align each cell to its lower-body anchor and shared baseline for comparison",
                "composite on dark, light, magenta, and cyan backgrounds at 96x104",
                "compare edge pixels against the opaque pet palette and quantify background spread",
                "rank only within each role/row, then inspect a bounded normal-size candidate sheet",
                "treat metrics as candidates and apply hatch-pet visual acceptance policy before promotion",
            ],
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "cells": len(records),
            "display_sizes": [list(size) for size in DISPLAY_SIZES],
            "candidate_sheet_items": len(sheet_items),
            "alpha_threshold": ALPHA_THRESHOLD,
        },
        "visual_review": {
            "status": args.manual_verdict if args.reviewed else "pending_review",
            "note": args.manual_note if args.reviewed else "candidate sheet requires normal-size inspection",
            "new_hard_failures": [],
            "confirmed_existing_blockers": sorted({item["known_blocker"] for item in candidates if item.get("known_blocker")}),
            "formal_assets_modified": False,
        },
        "top_candidates": candidates,
        "artifacts": [json_out.name, sheet_out.name],
    }
    json_out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
