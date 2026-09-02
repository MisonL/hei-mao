#!/usr/bin/env python3
"""Evidence-only frame cadence and compression stress review for v2 pets.

This review is deliberately independent from the atlas validator.  It treats
each used cell as a small rendered frame and checks two failure classes that
static structure gates do not prove by themselves:

* temporal interpolation residuals, including an upper-body-only jump that can
  indicate a duplicated head or a pose-family switch;
* frame-order perturbation and WebP re-encoding pressure at pet display size.

Metrics only select candidates.  A candidate becomes a hard failure only after
normal-size visual inspection under the hatch-pet acceptance policy.  Formal
assets are never modified.
"""

from __future__ import annotations

import argparse
import json
import math
from io import BytesIO
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
DISPLAY_SIZE = (96, 104)
# Lossy pressure is intentionally sampled after the cheap temporal pass.  A
# full per-frame, high-method WebP encode is not a useful QA gate and can make
# the review itself a long-running task.
WEBP_QUALITIES = (75, 50)
COMPRESSION_SAMPLE_PER_ROW = 2
TEMPORAL_SAMPLE_COUNT = 32
BACKGROUND = (96, 96, 96)
KNOWN_BLOCKERS = [
    "hei-mao/jumping frame 2 duplicated head",
    "hei-mao-quality/jumping frame 2 duplicated head",
    "hei-mao-foodie/waiting frame 2-3 stacked upper contours",
    "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
]


def open_cell(atlas: Image.Image, row: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row * CELL_H, (frame + 1) * CELL_W, (row + 1) * CELL_H)
    ).convert("RGBA")


def rgba_array(image: Image.Image) -> np.ndarray:
    return np.asarray(image.convert("RGBA"), dtype=np.uint8)


def alpha_mask(image: Image.Image) -> np.ndarray:
    return rgba_array(image)[:, :, 3] >= ALPHA_THRESHOLD


def composite(image: Image.Image, background: tuple[int, int, int] = BACKGROUND) -> Image.Image:
    rgba = rgba_array(image).astype(np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    rgb = rgba[:, :, :3] * alpha + np.asarray(background, dtype=np.float32)[None, None, :] * (1.0 - alpha)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")


def descriptor(image: Image.Image, crop: tuple[int, int, int, int] | None = None) -> np.ndarray:
    """Return a small alpha-plus-luminance descriptor at display scale."""
    if crop is not None:
        image = image.crop(crop)
    rendered = composite(image).resize(DISPLAY_SIZE, Image.Resampling.LANCZOS)
    gray = np.asarray(rendered.convert("L"), dtype=np.float32) / 255.0
    alpha = np.asarray(image.getchannel("A").resize(DISPLAY_SIZE, Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    # Include low-cost edge energy so a duplicated upper contour is not hidden
    # by a similar average colour.
    dx = np.diff(gray, axis=1, prepend=gray[:, :1])
    dy = np.diff(gray, axis=0, prepend=gray[:1, :])
    return np.concatenate((gray.ravel(), alpha.ravel(), np.abs(dx).ravel(), np.abs(dy).ravel())).astype(np.float32)


def distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean(np.abs(a - b)))


def bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def bbox_delta(a: Image.Image, b: Image.Image) -> float:
    ba = bbox(alpha_mask(a))
    bb = bbox(alpha_mask(b))
    if ba is None or bb is None:
        return 1.0 if ba != bb else 0.0
    return float(np.mean(np.abs(np.asarray(ba, dtype=np.float32) - np.asarray(bb, dtype=np.float32))) / max(CELL_W, CELL_H))


def webp_roundtrip(image: Image.Image, quality: int) -> Image.Image:
    buffer = BytesIO()
    image.save(buffer, format="WEBP", lossless=False, quality=quality, method=0)
    buffer.seek(0)
    with Image.open(buffer) as decoded:
        return decoded.convert("RGBA")


def compression_metrics(image: Image.Image) -> dict[str, float | int]:
    source_mask = alpha_mask(image)
    source_display = np.asarray(composite(image).resize(DISPLAY_SIZE, Image.Resampling.LANCZOS), dtype=np.int16)
    worst = {
        "quality": WEBP_QUALITIES[-1],
        "rgb_delta": 0.0,
        "alpha_delta": 0.0,
        "visible_loss_fraction": 0.0,
        "bbox_delta": 0.0,
    }
    for quality in WEBP_QUALITIES:
        decoded = webp_roundtrip(image, quality)
        decoded_mask = alpha_mask(decoded)
        decoded_display = np.asarray(composite(decoded).resize(DISPLAY_SIZE, Image.Resampling.LANCZOS), dtype=np.int16)
        source_small_mask = np.asarray(Image.fromarray(source_mask.astype(np.uint8) * 255).resize(DISPLAY_SIZE, Image.Resampling.BILINEAR), dtype=np.float32) >= 32
        decoded_small_mask = np.asarray(Image.fromarray(decoded_mask.astype(np.uint8) * 255).resize(DISPLAY_SIZE, Image.Resampling.BILINEAR), dtype=np.float32) >= 32
        visible = int(source_small_mask.sum())
        lost = int(np.logical_and(source_small_mask, ~decoded_small_mask).sum())
        item = {
            "quality": int(quality),
            "rgb_delta": float(np.mean(np.abs(source_display - decoded_display)) / 255.0),
            "alpha_delta": float(np.mean(np.abs(source_small_mask.astype(np.float32) - decoded_small_mask.astype(np.float32)))),
            "visible_loss_fraction": float(lost / max(visible, 1)),
            "bbox_delta": bbox_delta(image, decoded),
        }
        if (
            item["visible_loss_fraction"] > worst["visible_loss_fraction"]
            or item["alpha_delta"] > worst["alpha_delta"]
            or item["rgb_delta"] > worst["rgb_delta"]
        ):
            worst = item
    return worst


def heatmap(source: Image.Image, stressed: Image.Image) -> Image.Image:
    a = np.asarray(composite(source).resize((CELL_W, CELL_H), Image.Resampling.NEAREST), dtype=np.int16)
    b = np.asarray(composite(stressed).resize((CELL_W, CELL_H), Image.Resampling.NEAREST), dtype=np.int16)
    diff = np.abs(a - b).max(axis=2)
    scaled = np.clip(diff.astype(np.float32) * 8.0, 0, 255).astype(np.uint8)
    rgb = np.zeros((CELL_H, CELL_W, 3), dtype=np.uint8)
    rgb[:, :, 0] = scaled
    rgb[:, :, 1] = np.clip(scaled // 3, 0, 255)
    return Image.fromarray(rgb, mode="RGB")


def tile(item: dict, source: Image.Image, stressed: Image.Image, previous: Image.Image, current: Image.Image, following: Image.Image) -> Image.Image:
    panel_w, panel_h = CELL_W, CELL_H
    tile_w = panel_w * 4
    tile_h = panel_h + 30
    canvas = Image.new("RGB", (tile_w, tile_h), (14, 14, 20))
    panels = [
        composite(source).resize((panel_w, panel_h), Image.Resampling.NEAREST),
        composite(stressed).resize((panel_w, panel_h), Image.Resampling.NEAREST),
        heatmap(source, stressed),
        composite(current).resize((panel_w, panel_h), Image.Resampling.NEAREST),
    ]
    for index, panel in enumerate(panels):
        canvas.paste(panel, (index * panel_w, 24))
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (3, 4),
        f"{item['role']} {item['row']} f{item['frame']} score={item['score']:.4f} top={item['top_residual']:.4f} q={item['compression_quality']}",
        fill=(245, 245, 245),
    )
    draw.text(
        (3, panel_h + 8),
        "原帧 | 压缩压力 | 差异热图 | 当前帧（时间候选）",
        fill=(215, 215, 225),
    )
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--reviewed", action="store_true", help="record normal-size visual review of the candidate sheet")
    args = parser.parse_args()

    repo = args.repo.resolve()
    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or out_dir / "frame-cadence-compression-review-20260831-v1.json"
    sheet_out = args.sheet_out or out_dir / "frame-cadence-compression-candidates-v1.jpg"

    records: list[dict] = []
    row_summaries: list[dict] = []
    frame_count = 0
    transition_count = 0
    for role in ROLES:
        atlas = Image.open(repo / "pets" / role / "spritesheet.webp").convert("RGBA")
        for row_index, row_name in enumerate(ROWS):
            frames = [open_cell(atlas, row_index, frame) for frame in range(USED_FRAMES[row_name])]
            frame_count += len(frames)
            transition_count += len(frames)
            descriptors = [descriptor(frame) for frame in frames]
            top_descriptors = [descriptor(frame, (0, 0, CELL_W, int(CELL_H * 0.48))) for frame in frames]
            lower_descriptors = [descriptor(frame, (0, int(CELL_H * 0.48), CELL_W, CELL_H)) for frame in frames]
            motion: list[float] = []
            for index in range(len(frames)):
                motion.append(distance(descriptors[index], descriptors[(index + 1) % len(frames)]))
            row_jerk = [abs(motion[index] - motion[(index - 1) % len(motion)]) for index in range(len(motion))]
            # Simulate a dropped frame by measuring the direct previous-to-next
            # jump.  Simulate a duplicated frame by recording the pause before
            # each transition.  Neither is a defect by itself; they are useful
            # stress indicators for a renderer or a scheduler.
            drop_skip_delta = []
            duplicate_hold = []
            for index in range(len(frames)):
                skip_distance = distance(
                    descriptors[(index - 1) % len(frames)],
                    descriptors[(index + 1) % len(frames)],
                )
                local_motion = max(motion[(index - 1) % len(motion)], motion[index])
                drop_skip_delta.append(max(0.0, skip_distance - local_motion))
                duplicate_hold.append(motion[index])
            row_summaries.append(
                {
                    "role": role,
                    "row": row_name,
                    "frames": len(frames),
                    "normal_motion_mean": round(float(np.mean(motion)), 6),
                    "normal_motion_max": round(float(np.max(motion)), 6),
                    "cadence_jerk_max": round(float(np.max(row_jerk)), 6),
                    "cadence_jerk_mean": round(float(np.mean(row_jerk)), 6),
                    "drop_skip_delta_max": round(float(np.max(drop_skip_delta)), 6),
                    "duplicate_hold_motion_max": round(float(np.max(duplicate_hold)), 6),
                    "loop_seam_motion": round(float(motion[-1]), 6),
                }
            )
            for index, current in enumerate(frames):
                previous = frames[(index - 1) % len(frames)]
                following = frames[(index + 1) % len(frames)]
                predicted = (descriptors[(index - 1) % len(frames)] + descriptors[(index + 1) % len(frames)]) / 2.0
                top_predicted = (top_descriptors[(index - 1) % len(frames)] + top_descriptors[(index + 1) % len(frames)]) / 2.0
                lower_predicted = (lower_descriptors[(index - 1) % len(frames)] + lower_descriptors[(index + 1) % len(frames)]) / 2.0
                residual = distance(descriptors[index], predicted)
                top_residual = distance(top_descriptors[index], top_predicted)
                lower_residual = distance(lower_descriptors[index], lower_predicted)
                # A top-only residual is intentionally weighted: it catches a
                # duplicated head while not rejecting an ordinary whole-body
                # gesture whose upper and lower parts move together.
                top_only = max(0.0, top_residual - 0.55 * lower_residual)
                cadence = row_jerk[index]
                score = (
                    1.8 * residual
                    + 2.6 * top_only
                    + 0.8 * cadence
                    + 0.35 * bbox_delta(previous, following)
                )
                records.append(
                    {
                        "role": role,
                        "row": row_name,
                        "frame": index,
                        "score": round(float(score), 6),
                        "residual": round(float(residual), 6),
                        "top_residual": round(float(top_residual), 6),
                        "lower_residual": round(float(lower_residual), 6),
                        "top_only_residual": round(float(top_only), 6),
                        "cadence_jerk": round(float(cadence), 6),
                        "drop_skip_delta": round(float(drop_skip_delta[index]), 6),
                        "duplicate_hold_motion": round(float(duplicate_hold[index]), 6),
                        "compression_sampled": False,
                        "compression_quality": None,
                        "compression_visible_loss_fraction": 0.0,
                        "compression_alpha_delta": 0.0,
                        "compression_rgb_delta": 0.0,
                        "compression_bbox_delta": 0.0,
                        "base_score": round(float(score), 6),
                    }
                )

    # First pass is cheap and covers every frame.  Only temporal outliers and
    # two stable reference frames per row go through the slower WebP path.
    records.sort(key=lambda item: (-float(item["base_score"]), item["role"], item["row"], int(item["frame"])))
    sample_keys = {
        (item["role"], item["row"], int(item["frame"])) for item in records[:TEMPORAL_SAMPLE_COUNT]
    }
    by_row: dict[tuple[str, str], list[dict]] = {}
    for item in records:
        by_row.setdefault((item["role"], item["row"]), []).append(item)
    for row_items in by_row.values():
        ordered = sorted(row_items, key=lambda value: int(value["frame"]))
        reference_items = ordered[:1] + ordered[len(ordered) // 2 : len(ordered) // 2 + 1]
        for item in reference_items[:COMPRESSION_SAMPLE_PER_ROW]:
            sample_keys.add((item["role"], item["row"], int(item["frame"])))

    compression_cache: dict[tuple[str, str, int], tuple[int, Image.Image]] = {}
    for item in records:
        key = (item["role"], item["row"], int(item["frame"]))
        if key not in sample_keys:
            continue
        atlas = Image.open(repo / "pets" / item["role"] / "spritesheet.webp").convert("RGBA")
        current = open_cell(atlas, ROWS.index(item["row"]), int(item["frame"]))
        compression = compression_metrics(current)
        item["compression_sampled"] = True
        item["compression_quality"] = int(compression["quality"])
        item["compression_visible_loss_fraction"] = round(float(compression["visible_loss_fraction"]), 6)
        item["compression_alpha_delta"] = round(float(compression["alpha_delta"]), 6)
        item["compression_rgb_delta"] = round(float(compression["rgb_delta"]), 6)
        item["compression_bbox_delta"] = round(float(compression["bbox_delta"]), 6)
        item["score"] = round(
            float(item["base_score"])
            + 0.9 * float(compression["visible_loss_fraction"])
            + 0.7 * float(compression["alpha_delta"])
            + 0.25 * float(compression["rgb_delta"]),
            6,
        )
        stressed = webp_roundtrip(current, int(compression["quality"]))
        compression_cache[key] = (int(compression["quality"]), stressed)

    for item in records:
        item.setdefault("score", item["base_score"])
    records.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])))
    top = records[:24]

    tiles: list[Image.Image] = []
    for item in top[:16]:
        atlas = Image.open(repo / "pets" / item["role"] / "spritesheet.webp").convert("RGBA")
        row_index = ROWS.index(item["row"])
        current = open_cell(atlas, row_index, int(item["frame"]))
        previous = open_cell(atlas, row_index, (int(item["frame"]) - 1) % USED_FRAMES[item["row"]])
        following = open_cell(atlas, row_index, (int(item["frame"]) + 1) % USED_FRAMES[item["row"]])
        key = (item["role"], item["row"], int(item["frame"]))
        if key in compression_cache:
            _, stressed = compression_cache[key]
        else:
            # Keep the candidate sheet bounded if an unsampled temporal
            # candidate outranks a sampled frame.
            stressed = webp_roundtrip(current, WEBP_QUALITIES[-1])
        tiles.append(tile(item, current, stressed, previous, current, following))
    columns = 2
    tile_w = CELL_W * 4
    tile_h = CELL_H + 30
    sheet = Image.new("RGB", (columns * tile_w, max(1, math.ceil(len(tiles) / columns)) * tile_h), (10, 10, 14))
    for index, item in enumerate(tiles):
        sheet.paste(item, ((index % columns) * tile_w, (index // columns) * tile_h))
    sheet.save(sheet_out, quality=93, subsampling=0)

    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "frame-order perturbation, upper/lower temporal residual, and WebP compression stress; evidence only",
        "formal_assets_modified": False,
        "methods": [
            {
                "name": "upper/lower temporal interpolation residual",
                "details": "Compare each frame with the midpoint predicted from its previous and following frame at 96x104, separately for the full cell, upper 48 percent, and lower 52 percent.",
                "purpose": "isolate a single-frame head/upper-contour jump from an intentional whole-body gesture",
            },
            {
                "name": "frame-order and cadence perturbation",
                "details": "Measure normal loop motion and first-order cadence changes, then simulate a dropped frame (previous-to-next jump) and a duplicated frame (visible hold before the next transition), including the loop-closing transition; these are stress indicators, not automatic failures.",
                "purpose": "find duplicate/held frames, frame-order sensitivity, and loop seam pops that static rows can hide",
            },
            {
                "name": "display-size WebP pressure",
                "details": "Round-trip a bounded sample of temporal outliers plus two reference frames per row through WebP qualities 75 and 50, resize to 96x104, and compare alpha retention, visible-pixel loss, bbox drift, and RGB residual.",
                "purpose": "check whether thin identity features or silhouette edges disappear or change size under realistic encoded display pressure",
            },
        ],
        "coverage": {
            "roles": len(ROLES),
            "rows": len(row_summaries),
            "frames": frame_count,
            "transitions_including_loop": transition_count,
            "display_size": list(DISPLAY_SIZE),
            "webp_qualities": list(WEBP_QUALITIES),
            "compression_sample_frames": len(sample_keys),
        },
        "candidate_counts": {
            "scored_frames": len(records),
            "sheet_frames": len(top[:16]),
            "top_only_residual_candidates": sum(1 for item in records if float(item["top_only_residual"]) > 0.04),
            "compression_visible_loss_candidates": sum(1 for item in records if item["compression_sampled"] and float(item["compression_visible_loss_fraction"]) > 0.01),
        },
        "row_summaries": row_summaries,
        "top_candidates": top,
        "visual_review": {
            "status": "pass_with_four_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": KNOWN_BLOCKERS if args.reviewed else [],
            "note": (
                "Normal-size cadence/compression candidate sheet reviewed; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Inspect frame-cadence-compression-candidates-v1.jpg at normal display size; all metrics are candidate evidence only."
            ),
        },
        "limitations": [
            "This is a Pillow/WebP rehearsal, not a browser GPU capture or live Codex App playback.",
            "A high temporal residual can be an intentional gesture; only the normal-size sheet and hatch-pet policy promote a candidate.",
            "Lossy WebP qualities 75 and 50 are adversarial stress cases and are not packaging-quality recommendations; compression is sampled after temporal ranking.",
            "The four previously confirmed complete-row failures remain blockers even if no additional candidate is promoted.",
        ],
        "artifacts": [sheet_out.name, json_out.name, Path(__file__).name],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": frame_count, "rows": len(row_summaries)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
