#!/usr/bin/env python3
"""Evidence-only dense optical-flow review for the current PetDex v2 atlases.

This review never rewrites a formal sprite. It composites each cell on a flat
background, computes forward/backward dense optical flow for every adjacent
transition (including the loop-closing transition), and emits only candidate
metrics plus a bounded arrow-overlay sheet for normal-size visual inspection.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
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
DISPLAY_W = 96
DISPLAY_H = 104
BACKGROUND = np.array([116, 124, 136], dtype=np.float32)
KNOWN_BLOCKERS = [
    "hei-mao/jumping frame 2 duplicated head",
    "hei-mao-quality/jumping frame 2 duplicated head",
    "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
    "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--sheet-out", type=Path)
    parser.add_argument("--reviewed", action="store_true")
    return parser.parse_args()


def open_cell(atlas: Image.Image, row: int, frame: int) -> Image.Image:
    return atlas.crop((frame * CELL_W, row * CELL_H, (frame + 1) * CELL_W, (row + 1) * CELL_H))


def composite(cell: Image.Image) -> tuple[np.ndarray, np.ndarray]:
    rgba = np.asarray(cell.convert("RGBA"), dtype=np.uint8)
    resized = cv2.resize(rgba, (DISPLAY_W, DISPLAY_H), interpolation=cv2.INTER_AREA)
    alpha = resized[..., 3].astype(np.float32) / 255.0
    rgb = resized[..., :3].astype(np.float32)
    out = rgb * alpha[..., None] + BACKGROUND[None, None, :] * (1.0 - alpha[..., None])
    return np.clip(out, 0, 255).astype(np.uint8), alpha >= (16.0 / 255.0)


def flow_pair(first: np.ndarray, second: np.ndarray, first_mask: np.ndarray, second_mask: np.ndarray) -> dict[str, float]:
    first_gray = cv2.cvtColor(first, cv2.COLOR_RGB2GRAY)
    second_gray = cv2.cvtColor(second, cv2.COLOR_RGB2GRAY)
    params = dict(
        pyr_scale=0.5,
        levels=3,
        winsize=15,
        iterations=3,
        poly_n=5,
        poly_sigma=1.2,
        flags=0,
    )
    forward = cv2.calcOpticalFlowFarneback(first_gray, second_gray, None, **params)
    backward = cv2.calcOpticalFlowFarneback(second_gray, first_gray, None, **params)
    height, width = first_gray.shape
    grid_x, grid_y = np.meshgrid(np.arange(width, dtype=np.float32), np.arange(height, dtype=np.float32))
    sample_x = np.clip(grid_x + forward[..., 0], 0, width - 1)
    sample_y = np.clip(grid_y + forward[..., 1], 0, height - 1)
    back_at_target = np.stack(
        [cv2.remap(backward[..., channel], sample_x, sample_y, cv2.INTER_LINEAR) for channel in range(2)],
        axis=-1,
    )
    fb_error = np.linalg.norm(forward + back_at_target, axis=-1)
    magnitude = np.linalg.norm(forward, axis=-1)
    union = first_mask | second_mask
    # Exclude the one-pixel contour where anti-aliased alpha and background
    # compositing can create unstable vectors. The full mask remains in the
    # candidate overlay, so this is only a metric stabilization step.
    interior = cv2.erode(union.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1).astype(bool)
    sample = interior if int(interior.sum()) >= 16 else union
    if not np.any(sample):
        sample = np.ones_like(union, dtype=bool)
    values = magnitude[sample]
    consistency = fb_error[sample]
    return {
        "median_magnitude": float(np.median(values)),
        "p95_magnitude": float(np.percentile(values, 95)),
        "median_fb_error": float(np.median(consistency)),
        "p95_fb_error": float(np.percentile(consistency, 95)),
        "visible_pixels": int(union.sum()),
        "forward": forward,
        "mask": union,
    }


def robust_z(value: float, values: list[float]) -> float:
    if len(values) < 3:
        return 0.0
    median = float(np.median(values))
    mad = float(np.median(np.abs(np.asarray(values) - median)))
    # A nearly static row can have an almost-zero MAD. Cap the candidate
    # ranking so that a legitimate blink or tiny prop movement is not
    # presented as an unbounded severity score.
    return min(12.0, max(0.0, (value - median) / max(1.4826 * mad, 0.02)))


def arrow_overlay(image: np.ndarray, flow: np.ndarray, mask: np.ndarray) -> Image.Image:
    overlay = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR)
    step = 12
    for y in range(step // 2, DISPLAY_H, step):
        for x in range(step // 2, DISPLAY_W, step):
            if not mask[y, x]:
                continue
            dx, dy = flow[y, x]
            length = float(math.hypot(float(dx), float(dy)))
            if length < 0.35:
                continue
            scale = min(2.8, max(0.8, 7.0 / max(length, 0.01)))
            end_x = int(round(x + float(dx) * scale))
            end_y = int(round(y + float(dy) * scale))
            end_x = max(0, min(DISPLAY_W - 1, end_x))
            end_y = max(0, min(DISPLAY_H - 1, end_y))
            cv2.arrowedLine(overlay, (x, y), (end_x, end_y), (35, 235, 255), 1, cv2.LINE_AA, tipLength=0.25)
    return Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))


def make_tile(item: dict, first: Image.Image, second: Image.Image, overlay: Image.Image) -> Image.Image:
    panel_w, panel_h = DISPLAY_W, DISPLAY_H
    label_h = 28
    tile = Image.new("RGB", (panel_w * 3 + 12, panel_h + label_h), (18, 21, 28))
    draw = ImageDraw.Draw(tile)
    title = f"{item['role']} / {item['row']} f{item['frame']}->{item['next_frame']}"
    draw.text((4, 2), title, fill=(238, 242, 250))
    tile.paste(first, (0, label_h))
    tile.paste(second, (panel_w + 6, label_h))
    tile.paste(overlay, ((panel_w + 6) * 2, label_h))
    draw.text((4, label_h - 13), "A", fill=(175, 190, 215))
    draw.text((panel_w + 10, label_h - 13), "B", fill=(175, 190, 215))
    draw.text(((panel_w + 6) * 2 + 4, label_h - 13), "flow", fill=(175, 190, 215))
    return tile


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or (args.output_dir / "dense-optical-flow-review-20260831-v1.json")
    sheet_out = args.sheet_out or (args.output_dir / "dense-optical-flow-candidates-v1.jpg")

    records: list[dict] = []
    cached: dict[tuple[str, str, int], tuple[Image.Image, np.ndarray, np.ndarray]] = {}
    row_medians: dict[tuple[str, str], dict[str, list[float]]] = {}
    atlases: dict[str, Image.Image] = {}
    for role in ROLES:
        atlases[role] = Image.open(args.repo / "pets" / role / "spritesheet.webp").convert("RGBA")

    for role in ROLES:
        atlas = atlases[role]
        for row_index, (row_name, frame_count) in enumerate(ROWS):
            row_key = (role, row_name)
            row_records: list[dict] = []
            for frame in range(frame_count):
                next_frame = (frame + 1) % frame_count
                key_a = (role, row_name, frame)
                key_b = (role, row_name, next_frame)
                if key_a not in cached:
                    rgba, mask = composite(open_cell(atlas, row_index, frame))
                    cached[key_a] = (Image.fromarray(rgba), rgba, mask)
                if key_b not in cached:
                    rgba, mask = composite(open_cell(atlas, row_index, next_frame))
                    cached[key_b] = (Image.fromarray(rgba), rgba, mask)
                first_img, first, first_mask = cached[key_a]
                second_img, second, second_mask = cached[key_b]
                flow = flow_pair(first, second, first_mask, second_mask)
                item = {
                    "role": role,
                    "row": row_name,
                    "frame": frame,
                    "next_frame": next_frame,
                    "median_magnitude": round(flow["median_magnitude"], 6),
                    "p95_magnitude": round(flow["p95_magnitude"], 6),
                    "median_fb_error": round(flow["median_fb_error"], 6),
                    "p95_fb_error": round(flow["p95_fb_error"], 6),
                    "visible_pixels": flow["visible_pixels"],
                    "_first": first_img,
                    "_second": second_img,
                    "_overlay": arrow_overlay(second, flow["forward"], flow["mask"]),
                }
                row_records.append(item)
                records.append(item)
            row_medians[row_key] = {
                "p95_magnitude": [float(x["p95_magnitude"]) for x in row_records],
                "p95_fb_error": [float(x["p95_fb_error"]) for x in row_records],
            }

    for item in records:
        row_key = (item["role"], item["row"])
        mag_values = row_medians[row_key]["p95_magnitude"]
        fb_values = row_medians[row_key]["p95_fb_error"]
        item["motion_z"] = round(robust_z(float(item["p95_magnitude"]), mag_values), 6)
        item["fb_z"] = round(robust_z(float(item["p95_fb_error"]), fb_values), 6)
        item["score"] = round(max(float(item["motion_z"]), float(item["fb_z"])), 6)

    records.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])))
    top = records[:24]
    columns = 2
    tile_w = DISPLAY_W * 3 + 12
    tile_h = DISPLAY_H + 28
    sheet = Image.new("RGB", (columns * tile_w, max(1, math.ceil(len(top) / columns)) * tile_h), (10, 12, 17))
    for index, item in enumerate(top):
        tile = make_tile(item, item["_first"], item["_second"], item["_overlay"])
        sheet.paste(tile, ((index % columns) * tile_w, (index // columns) * tile_h))
    sheet.save(sheet_out, quality=94, subsampling=0)

    serializable = []
    for item in records:
        serializable.append({key: value for key, value in item.items() if not key.startswith("_")})
    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "supplemental dense optical-flow and forward/backward consistency review; evidence only",
        "method": {
            "name": "masked dense optical flow with arrow-overlay review",
            "steps": [
                "composite every 192x208 RGBA cell on a fixed mid-gray background and resize to 96x104",
                "calculate Farneback dense flow for every adjacent transition, including the loop-closing transition",
                "exclude the unstable one-pixel anti-aliased contour for metrics while retaining it in the visual overlay",
                "measure p95 motion magnitude and forward/backward flow consistency error",
                "rank only within each role/row using robust deviation and inspect a bounded normal-size arrow sheet",
            ],
            "purpose": "surface texture-bearing head, face, prop, and material jumps that can preserve similar alpha silhouettes while still breaking temporal coherence",
            "interpretation": "flow outliers are candidates only; hatch-pet visual policy and normal-size review determine whether a row fails",
            "score_cap": 12.0,
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": len(records),
            "transitions_including_loop": len(records),
            "display_size": [DISPLAY_W, DISPLAY_H],
            "algorithm": "OpenCV Farneback dense optical flow",
        },
        "top_candidates": serializable[:24],
        "result": {
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": 4 if args.reviewed else 0,
            "formal_assets_modified": False,
            "release_effect": "supplemental evidence only; the four complete-row regeneration blockers remain open",
        },
        "visual_review": {
            "status": "pass_with_four_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": KNOWN_BLOCKERS if args.reviewed else [],
            "note": (
                "Normal-size flow-arrow sheet reviewed; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Inspect dense-optical-flow-candidates-v1.jpg at normal display size; all flow outliers are candidate evidence only."
            ),
        },
        "limitations": [
            "Farneback flow on a composited raster is not semantic part tracking and cannot by itself distinguish an intentional gesture from a defect.",
            "The review is asset-only and does not replace browser GPU, live Codex App, multi-screen, or user-interface playback validation.",
            "Thin props and near-static idle frames can produce unstable local vectors; robust within-row ranking and visual confirmation are required.",
        ],
        "artifacts": [sheet_out.name, json_out.name, Path(__file__).name],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": len(records)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
