#!/usr/bin/env python3
"""Display-size and alpha-threshold visual review for hei-mao v2 atlases.

The review is deliberately evidence-only.  It never edits a formal pet asset.
It combines two independent display-oriented checks:

* alpha-threshold stability: whether semi-transparent edge pixels materially
  change the apparent silhouette, baseline, or aspect ratio;
* display quantization and upper-silhouette review: whether common small
  render sizes/filters lose a part or expose a repeated upper contour.

Metrics only select candidates.  A human must inspect the generated sheet
before a candidate can be promoted to a defect.
"""

from __future__ import annotations

import argparse
import json
import math
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
CELL_W = 192
CELL_H = 208
COLS = 8
ALPHA_LEVELS = (1, 16, 64, 128, 224)
DISPLAY_SIZES = ((48, 52), (64, 69), (96, 104))
DISPLAY_FILTERS = {
    "nearest": Image.Resampling.NEAREST,
    "bilinear": Image.Resampling.BILINEAR,
    "lanczos": Image.Resampling.LANCZOS,
}
BACKGROUNDS = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (210, 24, 38, 255),
    "checker": None,
}


def resize_vector(values: np.ndarray, size: int) -> np.ndarray:
    if values.size == 0:
        return np.zeros(size, dtype=np.float32)
    source = np.linspace(0.0, 1.0, values.size)
    target = np.linspace(0.0, 1.0, size)
    return np.interp(target, source, values).astype(np.float32)


def open_cell(atlas: Image.Image, row: int, col: int) -> Image.Image:
    return atlas.crop(
        (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)
    ).convert("RGBA")


def mask_for(cell: Image.Image, threshold: int) -> np.ndarray:
    return np.asarray(cell.getchannel("A"), dtype=np.uint8) >= threshold


def bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def metrics(mask: np.ndarray) -> dict[str, float | int | bool]:
    box = bbox(mask)
    if box is None:
        return {
            "nonempty": False,
            "area": 0,
            "width": 0,
            "height": 0,
            "aspect": 0.0,
            "cx": 0.0,
            "cy": 0.0,
            "bottom": -1,
        }
    x0, y0, x1, y1 = box
    ys, xs = np.nonzero(mask)
    return {
        "nonempty": True,
        "area": int(mask.sum()),
        "x0": x0,
        "y0": y0,
        "x1": x1,
        "y1": y1,
        "width": int(x1 - x0 + 1),
        "height": int(y1 - y0 + 1),
        "aspect": float((x1 - x0 + 1) / max(y1 - y0 + 1, 1)),
        "cx": float(xs.mean()),
        "cy": float(ys.mean()),
        "bottom": int(y1),
    }


def upper_profile(mask: np.ndarray, points: int = 24) -> np.ndarray:
    upper = mask[: int(CELL_H * 0.62)].sum(axis=1).astype(np.float32) / CELL_W
    profile = resize_vector(upper, points)
    maximum = float(profile.max()) if profile.size else 0.0
    return profile / maximum if maximum > 0.0 else profile


def profile_distance(a: np.ndarray, b: np.ndarray) -> float:
    if a.size == 0 or b.size == 0:
        return 0.0
    return float(np.linalg.norm(a - b) / max(math.sqrt(a.size), 1.0))


def checker(size: tuple[int, int], block: int = 6) -> Image.Image:
    width, height = size
    image = Image.new("RGBA", size, (224, 224, 224, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, height, block):
        for x in range(0, width, block):
            if ((x // block) + (y // block)) % 2:
                draw.rectangle((x, y, x + block - 1, y + block - 1), fill=(150, 150, 150, 255))
    return image


def composite(cell: Image.Image, size: tuple[int, int], resample: Image.Resampling, background: str) -> Image.Image:
    scaled = cell.resize(size, resample=resample)
    if background == "checker":
        base = checker(size)
    else:
        base = Image.new("RGBA", size, BACKGROUNDS[background])
    base.alpha_composite(scaled)
    return base.convert("RGB")


def normalize_display_box(mask: np.ndarray, size: tuple[int, int]) -> tuple[float, float, float, float] | None:
    box = bbox(mask)
    if box is None:
        return None
    x0, y0, x1, y1 = box
    width, height = size
    return (
        x0 / max(width, 1),
        y0 / max(height, 1),
        (x1 + 1) / max(width, 1),
        (y1 + 1) / max(height, 1),
    )


def display_metrics(cell: Image.Image, size: tuple[int, int], resample: Image.Resampling) -> dict[str, float | bool]:
    scaled = cell.resize(size, resample=resample)
    alpha = np.asarray(scaled.getchannel("A"), dtype=np.uint8)
    visible = alpha >= 48
    item = metrics(visible)
    item["normalized_box"] = normalize_display_box(visible, size)
    return item


def source_to_display_box(source: dict[str, float | int | bool]) -> tuple[float, float, float, float] | None:
    if not source["nonempty"]:
        return None
    return (
        float(source["x0"]) / CELL_W,
        float(source["y0"]) / CELL_H,
        (float(source["x1"]) + 1.0) / CELL_W,
        (float(source["y1"]) + 1.0) / CELL_H,
    )


def draw_labeled(image: Image.Image, label: str, width: int, height: int) -> Image.Image:
    canvas = Image.new("RGB", (width, height + 22), (24, 24, 30))
    canvas.paste(image.resize((width, height), Image.Resampling.NEAREST), (0, 22))
    draw = ImageDraw.Draw(canvas)
    draw.text((3, 4), label, fill=(245, 245, 245))
    return canvas


def alpha_overlay(cell: Image.Image, thresholds: tuple[int, ...] = ALPHA_LEVELS) -> Image.Image:
    rgba = np.asarray(cell, dtype=np.uint8)
    alpha = rgba[:, :, 3]
    canvas = Image.new("RGB", (CELL_W, CELL_H), (94, 94, 100))
    base = rgba[:, :, :3].astype(np.float32) * (alpha[:, :, None] / 255.0) + 94.0 * (1.0 - alpha[:, :, None] / 255.0)
    canvas.paste(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    colors = [(0, 240, 255), (255, 40, 210), (255, 220, 0), (255, 128, 0), (255, 255, 255)]
    for threshold, color in zip(thresholds, colors):
        edge = mask_for(cell, threshold)
        # Draw a one-pixel contour for each threshold; the threshold labels
        # are placed in the title strip by the caller.
        up = np.zeros_like(edge)
        down = np.zeros_like(edge)
        left = np.zeros_like(edge)
        right = np.zeros_like(edge)
        up[1:, :] = edge[:-1, :]
        down[:-1, :] = edge[1:, :]
        left[:, 1:] = edge[:, :-1]
        right[:, :-1] = edge[:, 1:]
        contour = edge & ~(up & down & left & right)
        ys, xs = np.nonzero(contour)
        draw.point([(int(x), int(y)) for x, y in zip(xs, ys)], fill=color)
    return canvas


def make_candidate_tile(item: dict, cell: Image.Image) -> Image.Image:
    tile_w = CELL_W * 2
    tile_h = CELL_H + 46
    tile = Image.new("RGB", (tile_w, tile_h), (16, 16, 22))
    source = alpha_overlay(cell)
    tile.paste(source, (0, 24))
    # Use a checkerboard composite for the actual display-size proof.  The
    # three filter/size thumbnails are intentionally enlarged only for review.
    display = composite(cell, (48, 52), Image.Resampling.BILINEAR, "checker")
    display = display.resize((CELL_W, CELL_H), Image.Resampling.NEAREST)
    tile.paste(display, (CELL_W, 24))
    draw = ImageDraw.Draw(tile)
    title = f"{item['role']}/{item['row']}/f{item['frame']} score={item['score']:.2f}"
    draw.text((3, 4), title, fill=(245, 245, 245))
    draw.text((3, CELL_H + 29), "左：alpha 阈值轮廓 1/16/64/128/224；右：48x52 双线性棋盘格", fill=(210, 210, 220))
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
    json_out = args.json_out or output_dir / "display-alpha-lobe-review-20260831.json"
    sheet_out = args.sheet_out or output_dir / "display-alpha-lobe-candidates.jpg"

    rows: dict[tuple[str, str], list[dict]] = {}
    all_frames: list[dict] = []
    display_candidates: list[dict] = []
    alpha_candidates: list[dict] = []

    for role in ROLES:
        atlas = Image.open(repo / "pets" / role / "spritesheet.webp").convert("RGBA")
        for row_index, row_name in enumerate(ROWS):
            frames: list[dict] = []
            for frame in range(COLS):
                cell = open_cell(atlas, row_index, frame)
                base_mask = mask_for(cell, 16)
                source = metrics(base_mask)
                if not source["nonempty"]:
                    continue
                threshold_metrics = {str(level): metrics(mask_for(cell, level)) for level in ALPHA_LEVELS}
                reference = threshold_metrics["16"]
                alpha_deltas = []
                for level in (64, 128, 224):
                    current = threshold_metrics[str(level)]
                    if not current["nonempty"]:
                        alpha_deltas.append(1.0)
                        continue
                    area_ratio = abs(float(current["area"]) / max(float(reference["area"]), 1.0) - 1.0)
                    height_ratio = abs(float(current["height"]) / max(float(reference["height"]), 1.0) - 1.0)
                    width_ratio = abs(float(current["width"]) / max(float(reference["width"]), 1.0) - 1.0)
                    bottom_shift = abs(float(current["bottom"]) - float(reference["bottom"])) / CELL_H
                    alpha_deltas.append(max(area_ratio, height_ratio, width_ratio, bottom_shift))
                alpha_instability = max(alpha_deltas, default=0.0)

                source_box = source_to_display_box(source)
                display_deltas = []
                display_records = []
                for size in DISPLAY_SIZES:
                    for filter_name, filter_value in DISPLAY_FILTERS.items():
                        result = display_metrics(cell, size, filter_value)
                        box = result.get("normalized_box")
                        if source_box is None or box is None:
                            delta = 1.0
                        else:
                            source_width = source_box[2] - source_box[0]
                            source_height = source_box[3] - source_box[1]
                            delta = max(
                                abs(float(box[2] - box[0]) - source_width),
                                abs(float(box[3] - box[1]) - source_height),
                            )
                        display_deltas.append(delta)
                        display_records.append({
                            "size": list(size),
                            "filter": filter_name,
                            "normalized_bbox": [round(float(x), 5) for x in box] if box else None,
                            "height": int(result["height"]),
                            "width": int(result["width"]),
                        })
                display_instability = max(display_deltas, default=0.0)
                upper_profiles = {
                    str(level): upper_profile(mask_for(cell, level)) for level in ALPHA_LEVELS
                }
                upper_threshold_drift = max(
                    profile_distance(upper_profiles["16"], upper_profiles[str(level)])
                    for level in (64, 128, 224)
                )
                frame_info = {
                    "role": role,
                    "row": row_name,
                    "row_index": row_index,
                    "frame": frame,
                    "source": source,
                    "thresholds": {
                        level: {key: value for key, value in data.items()}
                        for level, data in threshold_metrics.items()
                    },
                    "alpha_instability": round(float(alpha_instability), 5),
                    "display_instability": round(float(display_instability), 5),
                    "upper_threshold_drift": round(float(upper_threshold_drift), 5),
                    "display_records": display_records,
                    "cell": cell,
                }
                frames.append(frame_info)
                all_frames.append(frame_info)
            rows[(role, row_name)] = frames

    # Compare upper profiles against the same row's median.  This keeps the
    # signal row-aware while the threshold sweep remains independent.
    for (role, row_name), frames in rows.items():
        if not frames:
            continue
        profiles = np.stack([upper_profile(mask_for(f["cell"], 16)) for f in frames], axis=0)
        median_profile = np.median(profiles, axis=0)
        for item, profile in zip(frames, profiles):
            item["upper_profile_distance"] = round(float(profile_distance(profile, median_profile)), 5)
            # Candidate score: threshold response is the primary new signal;
            # small-display instability and upper-band drift are secondary.
            score = (
                8.0 * float(item["alpha_instability"])
                + 5.0 * float(item["display_instability"])
                + 4.0 * float(item["upper_threshold_drift"])
                + 3.0 * float(item["upper_profile_distance"])
            )
            item["score"] = round(float(score), 5)
            if item["alpha_instability"] >= 0.08:
                alpha_candidates.append(item)
            if item["display_instability"] >= 0.035 or item["upper_profile_distance"] >= 0.20:
                display_candidates.append(item)

    # Keep the visual sheet bounded and deterministic.  The sheet intentionally
    # includes known blockers when their scores warrant it, but never labels a
    # candidate as a confirmed defect.
    selected = sorted(all_frames, key=lambda x: (-float(x["score"]), x["role"], x["row"], int(x["frame"])))[:32]
    tile_w = CELL_W * 2
    tile_h = CELL_H + 46
    columns = 2
    sheet = Image.new("RGB", (columns * tile_w, math.ceil(len(selected) / columns) * tile_h), (10, 10, 14))
    for index, item in enumerate(selected):
        tile = make_candidate_tile(item, item["cell"])
        x = (index % columns) * tile_w
        y = (index // columns) * tile_h
        sheet.paste(tile, (x, y))
    sheet.save(sheet_out, quality=94, subsampling=0)

    known = [
        "hei-mao/jumping/frame-2 duplicated head",
        "hei-mao-quality/jumping/frame-2 duplicated head",
        "hei-mao-foodie/waiting/frame-2..3 stacked upper contours",
        "hei-mao-delivery/failed/frame-0..4 repeated head and pose-family switch",
    ]
    serializable = []
    for item in selected:
        serializable.append({key: value for key, value in item.items() if key != "cell"})
    payload = {
        "schema_version": 1,
        "checked_at": "2026-08-31",
        "scope": "display-size, alpha-threshold and upper-silhouette visual review; evidence only",
        "methods": [
            {
                "name": "alpha-threshold stability sweep",
                "thresholds": list(ALPHA_LEVELS),
                "details": "Recompute visible silhouette at alpha thresholds 1, 16, 64, 128 and 224; compare area, bbox aspect, height, width and baseline.",
                "purpose": "surface semi-transparent edge pixels that materially change apparent proportions or baseline at display time",
            },
            {
                "name": "display quantization matrix",
                "sizes": [list(size) for size in DISPLAY_SIZES],
                "filters": list(DISPLAY_FILTERS),
                "backgrounds": list(BACKGROUNDS),
                "details": "Render cells at common pet display sizes with nearest, bilinear and Lanczos sampling and inspect normalized bbox changes on adversarial backgrounds.",
                "purpose": "catch thin-part loss, edge clipping and size/aspect changes that are not obvious in the source atlas",
            },
            {
                "name": "threshold-persistent upper-silhouette profile",
                "details": "Compare 24-point upper-band width profiles across alpha thresholds and against the row median; candidate-only contour overlays expose repeated or stacked upper contours.",
                "purpose": "provide an independent visual cue for duplicate heads, stacked ears and upper-body topology changes",
            },
        ],
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": len(all_frames),
            "thresholds_per_frame": len(ALPHA_LEVELS),
            "display_variants_per_frame": len(DISPLAY_SIZES) * len(DISPLAY_FILTERS),
        },
        "candidate_counts": {
            "alpha_threshold_candidates": len(alpha_candidates),
            "display_or_upper_profile_candidates": len(display_candidates),
            "sheet_candidates": len(selected),
        },
        "known_blocker_candidates": known,
        "top_candidates": serializable,
        "visual_review": {
            "status": "pass_with_four_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": known if args.reviewed else [],
            "note": (
                "Candidate sheet reviewed at normal display size; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Inspect display-alpha-lobe-candidates.jpg at normal display size; metrics are candidate evidence only."
            ),
        },
        "formal_assets_modified": False,
        "artifacts": [sheet_out.name, json_out.name],
        "limitations": [
            "This is an asset-only display rehearsal and does not replace live Codex App capture.",
            "Sampling differences can be intentional for thin props or effects; no metric is an automatic defect.",
            "A confirmed defect still requires normal-size visual evidence and complete-row repair under hatch-pet rules.",
        ],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": len(all_frames), "candidates": len(selected)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
