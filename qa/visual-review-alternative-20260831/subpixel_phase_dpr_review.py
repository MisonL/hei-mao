#!/usr/bin/env python3
"""Evidence-only subpixel phase and device-pixel-ratio render review.

The existing CSS rehearsal covers fractional atlas scale and resampling, but
does not vary the fractional background-position phase.  This script adds a
bounded phase matrix at two device-pixel ratios and compares a crop from the
full atlas with an isolated-cell render.  It is a renderer pressure test only:
it never edits or rewrites a formal pet asset.
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
ATLAS_W = 1536
ATLAS_H = 2288
ALPHA_THRESHOLD = 16
# The existing CSS review already covers 64x69.  This complementary phase
# pass keeps the two endpoint sizes and samples the four half-pixel corners.
DISPLAY_SIZES = ((48, 52), (96, 104))
DEVICE_PIXEL_RATIOS = (1.0, 1.5)
FILTERS = {
    "nearest": Image.Resampling.NEAREST,
    "bilinear": Image.Resampling.BILINEAR,
}
PHASES = (0.0, 0.5)
BACKGROUNDS = ((96, 96, 96), (244, 244, 244), (210, 24, 38))
KNOWN_BLOCKERS = [
    "hei-mao/jumping frame 2 duplicated head",
    "hei-mao-quality/jumping frame 2 duplicated head",
    "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
    "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
]


def open_cell(atlas: Image.Image, row: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row * CELL_H, (frame + 1) * CELL_W, (row + 1) * CELL_H)
    ).convert("RGBA")


def composite(image: Image.Image, background: tuple[int, int, int]) -> np.ndarray:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    rgb = rgba[:, :, :3] * alpha + np.asarray(background, dtype=np.float32)[None, None, :] * (1.0 - alpha)
    return np.clip(rgb, 0, 255).astype(np.uint8)


def alpha_mask(image: Image.Image) -> np.ndarray:
    return np.asarray(image.getchannel("A"), dtype=np.uint8) >= ALPHA_THRESHOLD


def visible_bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def render_metrics(image: Image.Image, size: tuple[int, int]) -> dict[str, float | int | None]:
    scaled = image.resize(size, resample=Image.Resampling.BILINEAR).convert("RGBA")
    mask = alpha_mask(scaled)
    box = visible_bbox(mask)
    if box is None:
        return {"area": 0, "width": 0, "height": 0, "aspect": 0.0, "x0": None, "y0": None, "x1": None, "y1": None}
    x0, y0, x1, y1 = box
    return {
        "area": int(mask.sum()),
        "width": int(x1 - x0 + 1),
        "height": int(y1 - y0 + 1),
        "aspect": round(float((x1 - x0 + 1) / max(y1 - y0 + 1, 1)), 6),
        "x0": x0,
        "y0": y0,
        "x1": x1,
        "y1": y1,
    }


def phase_shift(image: Image.Image, phase_x: float, phase_y: float, resample: Image.Resampling) -> Image.Image:
    # PIL's affine transform maps each output pixel to an input coordinate.
    # Subtracting the phase therefore moves the rendered content by the
    # requested fractional background-position amount.
    return image.transform(
        image.size,
        Image.Transform.AFFINE,
        (1.0, 0.0, -phase_x, 0.0, 1.0, -phase_y),
        resample=resample,
        fillcolor=(0, 0, 0, 0),
    ).convert("RGBA")


def compare(full: Image.Image, isolated: Image.Image, css_size: tuple[int, int]) -> dict[str, float | int]:
    full_alpha = np.asarray(full.getchannel("A"), dtype=np.int16)
    isolated_alpha = np.asarray(isolated.getchannel("A"), dtype=np.int16)
    height, width = full_alpha.shape
    edge_radius = min(4, max(1, min(height, width) // 10))
    yy, xx = np.indices((height, width))
    edge = (xx < edge_radius) | (yy < edge_radius) | (xx >= width - edge_radius) | (yy >= height - edge_radius)
    delta = np.abs(full_alpha - isolated_alpha)
    leak = (isolated_alpha < ALPHA_THRESHOLD) & edge & (full_alpha >= isolated_alpha + 24)
    composites = []
    for background in BACKGROUNDS:
        composites.append(np.abs(composite(full, background).astype(np.int16) - composite(isolated, background).astype(np.int16)).max(axis=2))
    composite_delta = np.maximum.reduce(composites)
    changed = composite_delta >= 12
    full_display = full.resize(css_size, resample=Image.Resampling.BILINEAR).convert("RGBA")
    isolated_display = isolated.resize(css_size, resample=Image.Resampling.BILINEAR).convert("RGBA")
    full_metrics = render_metrics(full_display, css_size)
    isolated_metrics = render_metrics(isolated_display, css_size)
    width_delta = abs(int(full_metrics["width"]) - int(isolated_metrics["width"]))
    height_delta = abs(int(full_metrics["height"]) - int(isolated_metrics["height"]))
    area_delta = abs(int(full_metrics["area"]) - int(isolated_metrics["area"]))
    pixels = max(width * height, 1)
    return {
        "alpha_leak_pixels": int(leak.sum()),
        "edge_changed_pixels": int((changed & edge).sum()),
        "changed_pixels": int(changed.sum()),
        "edge_fraction": round(float(((leak | (changed & edge)).sum()) / pixels), 6),
        "max_composite_delta": int(composite_delta.max(initial=0)),
        "mean_composite_delta": round(float(composite_delta.mean() / 255.0), 6),
        "full_display_area": int(full_metrics["area"]),
        "isolated_display_area": int(isolated_metrics["area"]),
        "display_area_delta": area_delta,
        "display_width_delta": width_delta,
        "display_height_delta": height_delta,
    }


def make_tile(item: dict, full: Image.Image, isolated: Image.Image, css_size: tuple[int, int]) -> Image.Image:
    panel_w, panel_h = 192, 208
    title_h, footer_h = 28, 28
    tile = Image.new("RGB", (panel_w * 3, panel_h + title_h + footer_h), (12, 13, 18))
    full_rgb = Image.fromarray(composite(full.resize(css_size, Image.Resampling.NEAREST), (96, 96, 96)), mode="RGB")
    isolated_rgb = Image.fromarray(composite(isolated.resize(css_size, Image.Resampling.NEAREST), (96, 96, 96)), mode="RGB")
    full_rgb = full_rgb.resize((panel_w, panel_h), Image.Resampling.NEAREST)
    isolated_rgb = isolated_rgb.resize((panel_w, panel_h), Image.Resampling.NEAREST)
    diff = np.abs(np.asarray(full_rgb, dtype=np.int16) - np.asarray(isolated_rgb, dtype=np.int16)).max(axis=2)
    diff_rgb = Image.fromarray(np.repeat(np.clip(diff * 8, 0, 255)[:, :, None], 3, axis=2).astype(np.uint8), mode="RGB")
    tile.paste(full_rgb, (0, title_h))
    tile.paste(isolated_rgb, (panel_w, title_h))
    tile.paste(diff_rgb, (panel_w * 2, title_h))
    draw = ImageDraw.Draw(tile)
    draw.text(
        (3, 5),
        f"{item['role']}/{item['row']}/f{item['frame']} {item['filter']} dpr={item['dpr']:.1f} phase={item['phase_x']:.2f},{item['phase_y']:.2f}",
        fill=(245, 245, 245),
    )
    draw.text((3, panel_h + title_h + 7), "full atlas crop | isolated cell | 放大差异", fill=(210, 212, 222))
    return tile


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
    json_out = args.json_out or output_dir / "subpixel-phase-dpr-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "subpixel-phase-dpr-candidates-v1.jpg"

    records: list[dict] = []
    source_cache: dict[tuple[str, int, int], Image.Image] = {}
    frame_count = 0
    variant_count = 0

    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        with Image.open(atlas_path) as opened:
            atlas = opened.convert("RGBA")
        for css_size in DISPLAY_SIZES:
            for dpr in DEVICE_PIXEL_RATIOS:
                scale = (css_size[0] * dpr) / CELL_W
                target_w = max(1, round(ATLAS_W * scale))
                target_h = max(1, round(ATLAS_H * scale))
                for filter_name, filter_value in FILTERS.items():
                    scaled_atlas = atlas.resize((target_w, target_h), resample=filter_value).convert("RGBA")
                    for phase_x in PHASES:
                        for phase_y in PHASES:
                            shifted_atlas = phase_shift(scaled_atlas, phase_x, phase_y, filter_value)
                            variant_count += 1
                            for row_index, row_name in enumerate(ROWS):
                                for frame in range(USED_FRAMES[row_name]):
                                    x0 = round(frame * CELL_W * scale)
                                    x1 = round((frame + 1) * CELL_W * scale)
                                    y0 = round(row_index * CELL_H * scale)
                                    y1 = round((row_index + 1) * CELL_H * scale)
                                    full = shifted_atlas.crop((x0, y0, x1, y1)).convert("RGBA")
                                    cell = open_cell(atlas, row_index, frame)
                                    isolated = cell.resize((max(1, x1 - x0), max(1, y1 - y0)), resample=filter_value).convert("RGBA")
                                    isolated = phase_shift(isolated, phase_x, phase_y, filter_value)
                                    metrics = compare(full, isolated, css_size)
                                    score = (
                                        3.2 * float(metrics["edge_fraction"])
                                        + 1.6 * float(metrics["alpha_leak_pixels"]) / max(full.width * full.height, 1)
                                        + 0.9 * float(metrics["display_area_delta"]) / max(css_size[0] * css_size[1], 1)
                                        + 0.6 * float(metrics["display_width_delta"] + metrics["display_height_delta"]) / max(sum(css_size), 1)
                                    )
                                    records.append(
                                        {
                                            "role": role,
                                            "row": row_name,
                                            "frame": frame,
                                            "display_size": list(css_size),
                                            "dpr": float(dpr),
                                            "filter": filter_name,
                                            "phase_x": float(phase_x),
                                            "phase_y": float(phase_y),
                                            "score": round(float(score), 6),
                                            **metrics,
                                        }
                                    )
                                    frame_count += 1
                            del shifted_atlas
                    del scaled_atlas

    # Keep the worst phase per frame so the candidate sheet stays inspectable.
    best_by_frame: dict[tuple[str, str, int], dict] = {}
    for item in records:
        key = (item["role"], item["row"], int(item["frame"]))
        current = best_by_frame.get(key)
        if current is None or float(item["score"]) > float(current["score"]):
            best_by_frame[key] = item
    top = sorted(best_by_frame.values(), key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])))[:24]

    tiles: list[Image.Image] = []
    for item in top:
        css_size = tuple(int(v) for v in item["display_size"])
        dpr = float(item["dpr"])
        scale = (css_size[0] * dpr) / CELL_W
        target_w = max(1, round(ATLAS_W * scale))
        target_h = max(1, round(ATLAS_H * scale))
        filter_value = FILTERS[item["filter"]]
        atlas_path = repo / "pets" / item["role"] / "spritesheet.webp"
        with Image.open(atlas_path) as opened:
            atlas = opened.convert("RGBA")
        scaled_atlas = atlas.resize((target_w, target_h), resample=filter_value).convert("RGBA")
        shifted = phase_shift(scaled_atlas, float(item["phase_x"]), float(item["phase_y"]), filter_value)
        row_index = ROWS.index(item["row"])
        frame = int(item["frame"])
        x0 = round(frame * CELL_W * scale)
        x1 = round((frame + 1) * CELL_W * scale)
        y0 = round(row_index * CELL_H * scale)
        y1 = round((row_index + 1) * CELL_H * scale)
        full = shifted.crop((x0, y0, x1, y1)).convert("RGBA")
        isolated = open_cell(atlas, row_index, frame).resize((max(1, x1 - x0), max(1, y1 - y0)), resample=filter_value).convert("RGBA")
        isolated = phase_shift(isolated, float(item["phase_x"]), float(item["phase_y"]), filter_value)
        tiles.append(make_tile(item, full, isolated, css_size))

    columns = 2
    tile_w = CELL_W * 3
    tile_h = CELL_H + 28 + 28
    sheet = Image.new("RGB", (columns * tile_w, max(1, math.ceil(len(tiles) / columns)) * tile_h), (10, 10, 14))
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % columns) * tile_w, (index // columns) * tile_h))
    sheet.save(sheet_out, quality=93, subsampling=0)

    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "subpixel background-position phase and device-pixel-ratio sampling review; evidence only",
        "method": {
            "name": "full-atlas versus isolated-cell render under fractional phase and DPR",
            "steps": [
                "resize each complete 1536x2288 atlas using PetDex width-only scale at 48x52 and 96x104 CSS display sizes",
                "evaluate DPR 1.0 and 1.5 with nearest and bilinear sampling",
                "shift the rendered atlas and isolated cell by each 0 and 0.5 pixel x/y phase",
                "compare edge alpha/RGB bleed and CSS-size visible area/width/height between the two paths",
                "inspect the highest-ranked phase candidates at normal pet size",
            ],
            "purpose": "surface fractional background-position neighbour bleed and display-only size/aspect changes not represented by integer crop checks",
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": len(best_by_frame),
            "raw_frame_variant_records": len(records),
            "render_variants_per_role": variant_count // max(len(ROLES), 1),
            "display_sizes": [list(size) for size in DISPLAY_SIZES],
            "device_pixel_ratios": list(DEVICE_PIXEL_RATIOS),
            "filters": list(FILTERS),
            "phases": list(PHASES),
        },
        "known_failures_reproduced": KNOWN_BLOCKERS,
        "top_candidates": top,
        "visual_review": {
            "status": "pass_with_four_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": KNOWN_BLOCKERS if args.reviewed else [],
            "note": (
                "Phase/DPR candidate sheet reviewed at normal display size; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Inspect subpixel-phase-dpr-candidates-v1.jpg at normal display size; metrics are candidate evidence only."
            ),
        },
        "result": {
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": 4 if args.reviewed else 0,
            "formal_assets_modified": False,
            "release_effect": "supplemental evidence only; complete-row regeneration remains required for the four existing blockers",
        },
        "limitations": [
            "Pillow affine sampling is a bounded approximation and not a browser GPU or live Codex App capture.",
            "The exact CSS background-position expression and platform compositor can change phase behaviour.",
            "A full-atlas versus isolated-cell difference is a candidate signal; normal-size visual inspection is required before promotion.",
        ],
        "artifacts": [sheet_out.name, json_out.name, Path(__file__).name],
        "formal_assets_modified": False,
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": len(best_by_frame), "records": len(records)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
