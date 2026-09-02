#!/usr/bin/env python3
"""Evidence-only review of atlas sampling boundaries and rendered flicker.

The PetDex renderer uses a full spritesheet as a CSS background and clips one
192x208 cell.  This review samples the complete atlas at fractional scales,
then compares each cropped cell with an isolated-cell render.  It also renders
each animation row at small display sizes and separates shape motion from
colour-only changes.  Metrics select candidates only; no formal asset is
modified and no candidate is an automatic failure.
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
DISPLAY_SIZES = ((48, 52), (64, 69), (96, 104))
PHYSICAL_SCALES = (0.67, 0.83, 1.0, 1.17, 1.33)
FILTERS = {
    "nearest": Image.Resampling.NEAREST,
    "bilinear": Image.Resampling.BILINEAR,
    "lanczos": Image.Resampling.LANCZOS,
}
BACKGROUNDS = {
    "mid": (96, 96, 96),
    "light": (244, 244, 244),
    "red": (210, 24, 38),
}
KNOWN_BLOCKERS = [
    "hei-mao/jumping frame 2 duplicated head",
    "hei-mao-quality/jumping frame 2 duplicated head",
    "hei-mao-foodie/waiting stacked upper contours",
    "hei-mao-delivery/failed repeated head and pose-family switch",
]


def open_cell(atlas: Image.Image, row: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row * CELL_H, (frame + 1) * CELL_W, (row + 1) * CELL_H)
    ).convert("RGBA")


def rgba_array(image: Image.Image) -> np.ndarray:
    return np.asarray(image.convert("RGBA"), dtype=np.uint8)


def composite(image: Image.Image, background: tuple[int, int, int]) -> np.ndarray:
    rgba = rgba_array(image).astype(np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    rgb = rgba[:, :, :3] * alpha + np.asarray(background, dtype=np.float32)[None, None, :] * (1.0 - alpha)
    return np.clip(rgb, 0, 255).astype(np.uint8)


def alpha_mask(image: Image.Image, threshold: int = ALPHA_THRESHOLD) -> np.ndarray:
    return rgba_array(image)[:, :, 3] >= threshold


def border_mask(height: int, width: int, radius: int = 4) -> np.ndarray:
    yy, xx = np.indices((height, width))
    return (xx < radius) | (yy < radius) | (xx >= width - radius) | (yy >= height - radius)


def visible_bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def resample_cell_pair(
    atlas: Image.Image,
    row: int,
    frame: int,
    scale: float,
    resample: Image.Resampling,
    scaled_atlas: Image.Image | None = None,
) -> tuple[Image.Image, Image.Image]:
    """Return full-atlas crop and isolated-cell crop at the same CSS phase."""
    target_w = max(1, round(ATLAS_W * scale))
    target_h = max(1, round(ATLAS_H * scale))
    if scaled_atlas is None:
        scaled_atlas = atlas.resize((target_w, target_h), resample=resample)
    x0 = round(frame * CELL_W * scale)
    y0 = round(row * CELL_H * scale)
    x1 = round((frame + 1) * CELL_W * scale)
    y1 = round((row + 1) * CELL_H * scale)
    full = scaled_atlas.crop((x0, y0, x1, y1)).convert("RGBA")

    # Use the same physical crop size for the isolated cell.  Differences at
    # the clipped boundary therefore represent neighbouring atlas pixels,
    # rather than a different output geometry.
    source_cell = open_cell(atlas, row, frame)
    isolated = source_cell.resize((max(1, x1 - x0), max(1, y1 - y0)), resample=resample).convert("RGBA")
    return full, isolated


def sampling_metrics(full: Image.Image, isolated: Image.Image) -> dict[str, float | int]:
    full_rgba = rgba_array(full)
    isolated_rgba = rgba_array(isolated)
    height, width = full_rgba.shape[:2]
    full_alpha = full_rgba[:, :, 3].astype(np.int16)
    isolated_alpha = isolated_rgba[:, :, 3].astype(np.int16)
    alpha_delta = full_alpha - isolated_alpha
    edge = border_mask(height, width, radius=min(4, max(1, min(height, width) // 10)))
    transparent_edge = (isolated_alpha < 16) & edge
    alpha_leak = transparent_edge & (alpha_delta >= 24)
    composited = []
    for background in BACKGROUNDS.values():
        a = composite(full, background).astype(np.int16)
        b = composite(isolated, background).astype(np.int16)
        composited.append(np.abs(a - b).max(axis=2))
    composite_delta = np.maximum.reduce(composited)
    changed = composite_delta >= 12
    leak_or_edge = alpha_leak | (changed & edge)
    return {
        "width": int(width),
        "height": int(height),
        "alpha_leak_pixels": int(alpha_leak.sum()),
        "edge_changed_pixels": int((changed & edge).sum()),
        "changed_pixels": int(changed.sum()),
        "edge_fraction": round(float(leak_or_edge.mean()), 6),
        "max_composite_delta": int(composite_delta.max(initial=0)),
        "mean_composite_delta": round(float(composite_delta.mean() / 255.0), 6),
        "visible_full_pixels": int((full_alpha >= ALPHA_THRESHOLD).sum()),
        "visible_isolated_pixels": int((isolated_alpha >= ALPHA_THRESHOLD).sum()),
    }


def render_display(image: Image.Image, size: tuple[int, int], resample: Image.Resampling) -> np.ndarray:
    return composite(image.resize(size, resample=resample), BACKGROUNDS["mid"]).astype(np.float32) / 255.0


def shift_array(array: np.ndarray, dx: int, dy: int) -> np.ndarray:
    height, width = array.shape[:2]
    result = np.zeros_like(array)
    src_x0 = max(0, -dx)
    src_x1 = min(width, width - dx)
    src_y0 = max(0, -dy)
    src_y1 = min(height, height - dy)
    if src_x1 <= src_x0 or src_y1 <= src_y0:
        return result
    result[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = array[src_y0:src_y1, src_x0:src_x1]
    return result


def best_shift(previous: np.ndarray, current: np.ndarray) -> tuple[int, int, float]:
    best = (0, 0, float("inf"))
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            shifted = shift_array(current, dx, dy)
            score = float(np.mean(np.abs(previous - shifted)))
            if score < best[2]:
                best = (dx, dy, score)
    return best


def display_flicker_metrics(previous: Image.Image, current: Image.Image) -> dict[str, float | int]:
    size = (96, 104)
    prev_rgb = render_display(previous, size, Image.Resampling.BILINEAR)
    cur_rgb = render_display(current, size, Image.Resampling.BILINEAR)
    prev_alpha = np.asarray(previous.getchannel("A").resize(size, Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    cur_alpha = np.asarray(current.getchannel("A").resize(size, Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    dx, dy, _ = best_shift(prev_alpha, cur_alpha)
    cur_alpha_shifted = shift_array(cur_alpha, dx, dy)
    cur_rgb_shifted = shift_array(cur_rgb, dx, dy)
    shape_delta = float(np.mean(np.abs(prev_alpha - cur_alpha_shifted)))
    rgb_delta = float(np.mean(np.abs(prev_rgb - cur_rgb_shifted)))
    stable = (prev_alpha >= 0.72) & (cur_alpha_shifted >= 0.72)
    if int(stable.sum()) >= 64:
        stable_colour_delta = float(np.mean(np.abs(prev_rgb[stable] - cur_rgb_shifted[stable])))
    else:
        stable_colour_delta = 0.0
    colour_only = max(0.0, stable_colour_delta - 0.35 * shape_delta)
    return {
        "dx": int(dx),
        "dy": int(dy),
        "shape_delta": round(shape_delta, 6),
        "rgb_delta": round(rgb_delta, 6),
        "stable_pixels": int(stable.sum()),
        "stable_colour_delta": round(stable_colour_delta, 6),
        "colour_only_score": round(colour_only, 6),
    }


def difference_image(full: Image.Image, isolated: Image.Image, size: tuple[int, int] = (192, 208)) -> Image.Image:
    full_rgb = composite(full.resize(size, Image.Resampling.NEAREST), BACKGROUNDS["mid"]).astype(np.int16)
    iso_rgb = composite(isolated.resize(size, Image.Resampling.NEAREST), BACKGROUNDS["mid"]).astype(np.int16)
    diff = np.abs(full_rgb - iso_rgb).max(axis=2)
    amplified = np.clip(diff[:, :, None] * 8, 0, 255).astype(np.uint8)
    return Image.fromarray(np.repeat(amplified, 3, axis=2), mode="RGB")


def make_sampling_tile(item: dict, full: Image.Image, isolated: Image.Image) -> Image.Image:
    panel_w, panel_h = 192, 208
    tile = Image.new("RGB", (panel_w * 3, panel_h + 28), (14, 14, 20))
    for index, image in enumerate((full, isolated, difference_image(full, isolated))):
        if index < 2:
            rendered = composite(image.resize((panel_w, panel_h), Image.Resampling.NEAREST), BACKGROUNDS["mid"])
            tile.paste(Image.fromarray(rendered, mode="RGB"), (index * panel_w, 24))
        else:
            tile.paste(image, (index * panel_w, 24))
    draw = ImageDraw.Draw(tile)
    draw.text((3, 4), f"BLEED {item['role']}/{item['row']}/f{item['frame']} {item['filter']} s{item['scale']:.2f}", fill=(245, 245, 245))
    draw.text((3, panel_h + 8), "full atlas | isolated cell | amplified delta", fill=(215, 215, 225))
    return tile


def make_flicker_tile(item: dict, frames: list[Image.Image]) -> Image.Image:
    panel_w, panel_h = 192, 208
    tile = Image.new("RGB", (panel_w * 3, panel_h + 28), (14, 14, 20))
    for index, image in enumerate(frames):
        rendered = composite(image.resize((panel_w, panel_h), Image.Resampling.NEAREST), BACKGROUNDS["mid"])
        tile.paste(Image.fromarray(rendered, mode="RGB"), (index * panel_w, 24))
    draw = ImageDraw.Draw(tile)
    draw.text((3, 4), f"FLICKER {item['role']}/{item['row']} {item['previous']}->{item['current']} c{item['colour_only_score']:.3f}", fill=(245, 245, 245))
    draw.text((3, panel_h + 8), "previous | current | next", fill=(215, 215, 225))
    return tile


def clean_sampling(item: dict) -> dict:
    return {key: value for key, value in item.items() if key not in {"full", "isolated"}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--reviewed", action="store_true", help="record that the candidate sheet was reviewed at normal size")
    args = parser.parse_args()

    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or output_dir / "css-sampling-flicker-review-20260831.json"
    sheet_out = args.sheet_out or output_dir / "css-sampling-flicker-candidates.jpg"

    sampling_candidates: list[dict] = []
    flicker_candidates: list[dict] = []
    frame_count = 0
    transition_count = 0

    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        with Image.open(atlas_path) as opened:
            atlas = opened.convert("RGBA")
        rows = {
            (row_index, row_name): [
                open_cell(atlas, row_index, frame)
                for frame in range(USED_FRAMES[row_name])
            ]
            for row_index, row_name in enumerate(ROWS)
        }
        frame_count += sum(len(frames) for frames in rows.values())

        # Resize each complete atlas variant once per role.  The previous
        # implementation repeated these expensive operations once per row;
        # keeping the variant outside the row loop makes the review bounded
        # without changing any sampled pixels.
        best_by_frame: dict[tuple[int, int], dict] = {}
        for scale in PHYSICAL_SCALES:
            for filter_name, filter_value in FILTERS.items():
                scaled_atlas = atlas.resize(
                    (max(1, round(ATLAS_W * scale)), max(1, round(ATLAS_H * scale))),
                    resample=filter_value,
                )
                for (row_index, row_name), row_frames in rows.items():
                    for frame in range(len(row_frames)):
                        full, isolated = resample_cell_pair(
                            atlas,
                            row_index,
                            frame,
                            scale,
                            filter_value,
                            scaled_atlas=scaled_atlas,
                        )
                        metrics = sampling_metrics(full, isolated)
                        score = (
                            3.5 * float(metrics["edge_fraction"])
                            + 2.0 * float(metrics["alpha_leak_pixels"])
                            / max(metrics["width"] * metrics["height"], 1)
                            + 0.8 * float(metrics["mean_composite_delta"])
                        )
                        item = {
                            "role": role,
                            "row": row_name,
                            "frame": frame,
                            "filter": filter_name,
                            "scale": round(float(scale), 2),
                            "score": round(float(score), 6),
                            **metrics,
                        }
                        key = (row_index, frame)
                        current = best_by_frame.get(key)
                        if current is None or float(item["score"]) > float(current["score"]):
                            best_by_frame[key] = item
                del scaled_atlas
        sampling_candidates.extend(best_by_frame.values())

        for (row_index, row_name), row_frames in rows.items():
            if len(row_frames) <= 1:
                continue
            for frame in range(len(row_frames)):
                previous = row_frames[frame]
                current = row_frames[(frame + 1) % len(row_frames)]
                metrics = display_flicker_metrics(previous, current)
                transition_count += 1
                # The score intentionally rewards colour-only changes and
                # keeps ordinary large gestures as review candidates.
                score = 2.4 * float(metrics["colour_only_score"]) + 0.35 * float(metrics["stable_colour_delta"])
                flicker_candidates.append(
                    {
                        "role": role,
                        "row": row_name,
                        "previous": frame,
                        "current": (frame + 1) % len(row_frames),
                        "score": round(float(score), 6),
                        **metrics,
                    }
                )

    sampling_candidates.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])))
    flicker_candidates.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["previous"])))
    top_sampling = sampling_candidates[:20]
    top_flicker = flicker_candidates[:20]

    tiles: list[Image.Image] = []
    for item in top_sampling[:12]:
        atlas_path = repo / "pets" / item["role"] / "spritesheet.webp"
        with Image.open(atlas_path) as opened:
            atlas = opened.convert("RGBA")
        full, isolated = resample_cell_pair(
            atlas,
            ROWS.index(item["row"]),
            int(item["frame"]),
            float(item["scale"]),
            FILTERS[item["filter"]],
        )
        tiles.append(make_sampling_tile(item, full, isolated))
    for item in top_flicker[:12]:
        atlas_path = repo / "pets" / item["role"] / "spritesheet.webp"
        with Image.open(atlas_path) as opened:
            atlas = opened.convert("RGBA")
        row_index = ROWS.index(item["row"])
        count = USED_FRAMES[item["row"]]
        visuals = [
            open_cell(atlas, row_index, int(item["previous"])),
            open_cell(atlas, row_index, int(item["current"])),
            open_cell(atlas, row_index, (int(item["current"]) + 1) % count),
        ]
        tiles.append(make_flicker_tile(item, visuals))
    columns = 2
    tile_w = 192 * 3
    tile_h = 208 + 28
    sheet = Image.new("RGB", (columns * tile_w, max(1, math.ceil(len(tiles) / columns)) * tile_h), (10, 10, 14))
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % columns) * tile_w, (index // columns) * tile_h))
    sheet.save(sheet_out, quality=93, subsampling=0)

    serial_sampling = []
    for item in top_sampling:
        serial_sampling.append(clean_sampling(item))
    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "CSS spritesheet boundary sampling and rendered small-size flicker review; evidence only",
        "formal_assets_modified": False,
        "source_contract": {
            "atlas": "1536x2288",
            "cell": "192x208",
            "renderer_reference": "PetDex .pet-sprite uses background-size width-only, image-rendering pixelated, and zoom-based scale",
        },
        "methods": [
            {
                "name": "full-atlas versus isolated-cell sampling",
                "details": "Resize the complete atlas at five fractional physical scales with nearest, bilinear, and Lanczos filters; crop each CSS cell and compare it with the same-size isolated cell render on mid, light, and saturated-red backgrounds.",
                "purpose": "surface neighbouring-cell alpha/RGB bleed, subpixel boundary contamination, and edge changes that a per-cell resize cannot expose",
            },
            {
                "name": "display-size shape/colour residual split",
                "details": "Render adjacent and loop-closing frames at 96x104 with bilinear sampling, search a bounded translation, then measure alpha shape residual separately from stable-interior RGB residual.",
                "purpose": "surface material or palette flashes that can be mistaken for ordinary pose motion",
            },
            {
                "name": "three-background render pressure",
                "details": "Repeat sampling comparisons after compositing on mid-gray, light, and saturated-red backgrounds; only boundary-consistent differences are retained as candidates.",
                "purpose": "distinguish real transparency/edge defects from a single background's contrast illusion",
            },
        ],
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": frame_count,
            "transitions_including_loop": transition_count,
            "physical_scales": list(PHYSICAL_SCALES),
            "filters": list(FILTERS),
            "display_sizes": [list(size) for size in DISPLAY_SIZES],
            "backgrounds": list(BACKGROUNDS),
            "sampling_variants_evaluated": len(sampling_candidates) * len(PHYSICAL_SCALES) * len(FILTERS),
        },
        "candidate_counts": {
            "sampling_frames": len(sampling_candidates),
            "sampling_sheet_frames": len(top_sampling),
            "flicker_transitions": len(flicker_candidates),
            "flicker_sheet_transitions": len(top_flicker),
            "sampling_alpha_leak_candidates": sum(1 for item in sampling_candidates if int(item["alpha_leak_pixels"]) > 0),
            "flicker_colour_only_candidates": sum(1 for item in flicker_candidates if float(item["colour_only_score"]) > 0.08),
        },
        "top_sampling_candidates": serial_sampling,
        "top_flicker_candidates": top_flicker,
        "visual_review": {
            "status": "pass_with_four_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": KNOWN_BLOCKERS if args.reviewed else [],
            "note": (
                "Candidate sheet reviewed at normal display size; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Inspect css-sampling-flicker-candidates.jpg at normal display size; metrics are candidate evidence only."
            ),
        },
        "limitations": [
            "This is a Pillow renderer rehearsal, not a browser GPU capture and not live Codex App playback.",
            "Browser interpolation and device pixel ratio can differ; the fractional-scale matrix is adversarial evidence, not an exact browser trace.",
            "Colour residuals can be intentional for effects or lighting; only a normal-size visual review can promote a candidate.",
            "The four previously confirmed complete-row failures remain blockers even if this method finds no additional issue.",
        ],
        "artifacts": [sheet_out.name, json_out.name, Path(__file__).name],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": frame_count, "transitions": transition_count}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
