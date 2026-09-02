#!/usr/bin/env python3
"""Evidence-only cycle recurrence and onion-skin review for v2 pets.

This review is intentionally complementary to pairwise residual checks.  It
builds a perceptual recurrence matrix for every animation row after lower-body
registration, then renders a five-frame onion skin and the full cycle strip for
the highest-ranked candidates.  Non-adjacent recurrence can expose an
accidental repeated pose or phase reversal that looks acceptable when only
neighbouring frames are compared.  All scores are triage evidence; formal
assets are never changed.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
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
CELL_W = 192
CELL_H = 208
DISPLAY_SIZE = (48, 52)
PANEL_SIZE = (192, 208)
ALPHA_THRESHOLD = 16
BACKGROUND = (96, 96, 96)

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

OPEN_BLOCKED_ROWS = [
    "hei-mao/jumping",
    "hei-mao-quality/jumping",
    "hei-mao-foodie/waiting",
    "hei-mao-delivery/failed",
    "hei-mao-quality/running-left",
    "hei-mao-quality/failed",
    "hei-mao-traveler/waiting",
    "hei-mao-traveler/review",
]


def open_cell(atlas: Image.Image, row: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row * CELL_H, (frame + 1) * CELL_W, (row + 1) * CELL_H)
    ).convert("RGBA")


def alpha_mask(cell: Image.Image) -> np.ndarray:
    return np.asarray(cell.getchannel("A"), dtype=np.uint8) >= ALPHA_THRESHOLD


def lower_anchor(mask: np.ndarray) -> tuple[float, int]:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return 0.0, -1
    y0, y1 = int(ys.min()), int(ys.max())
    lower_start = y0 + int(round((y1 - y0 + 1) * 0.58))
    lower_xs = xs[ys >= lower_start]
    return float(np.mean(lower_xs if len(lower_xs) else xs)), y1


def translate_rgba(cell: Image.Image, dx: int, dy: int) -> Image.Image:
    source = np.asarray(cell, dtype=np.uint8)
    target = np.zeros_like(source)
    src_y0 = max(0, -dy)
    src_y1 = min(CELL_H, CELL_H - dy)
    src_x0 = max(0, -dx)
    src_x1 = min(CELL_W, CELL_W - dx)
    if src_y1 > src_y0 and src_x1 > src_x0:
        target[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = source[
            src_y0:src_y1, src_x0:src_x1
        ]
    return Image.fromarray(target, mode="RGBA")


def register_cell(cell: Image.Image, target_cx: float, target_bottom: int) -> Image.Image:
    cx, bottom = lower_anchor(alpha_mask(cell))
    if bottom < 0:
        return cell.copy()
    return translate_rgba(cell, int(round(target_cx - cx)), int(target_bottom - bottom))


def composite(cell: Image.Image, background: tuple[int, int, int] = BACKGROUND) -> Image.Image:
    rgba = np.asarray(cell, dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    rgb = rgba[:, :, :3] * alpha + np.asarray(background, dtype=np.float32)[None, None, :] * (1.0 - alpha)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")


def descriptor(cell: Image.Image) -> np.ndarray:
    """Perceptual alpha/luminance/edge descriptor at a fixed display size."""
    rgb = np.asarray(composite(cell).resize(DISPLAY_SIZE, Image.Resampling.LANCZOS), dtype=np.float32) / 255.0
    alpha = np.asarray(cell.getchannel("A").resize(DISPLAY_SIZE, Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    gray = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    dx = np.diff(gray, axis=1, prepend=gray[:, :1])
    dy = np.diff(gray, axis=0, prepend=gray[:1, :])
    # Coarse colour channels retain material/identity changes without making
    # background or tiny antialiasing variations dominate recurrence.
    small_rgb = rgb[::2, ::2, :].reshape(-1)
    return np.concatenate((gray.reshape(-1), alpha.reshape(-1), np.abs(dx).reshape(-1), np.abs(dy).reshape(-1), small_rgb)).astype(np.float32)


def pairwise_distance(vectors: np.ndarray) -> np.ndarray:
    # Mean absolute descriptor distance is bounded in [0, 1] and remains
    # interpretable after the row's lower-body alignment.
    return np.mean(np.abs(vectors[:, None, :] - vectors[None, :, :]), axis=2).astype(np.float32)


def cyclic_distance(i: int, j: int, count: int) -> int:
    delta = abs(i - j)
    return min(delta, count - delta)


def robust_z(value: float, values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    scale = max(1.4826 * mad, float(np.std(values)) * 0.25, 1e-6)
    return abs(value - median) / scale


def normalized_recurrence_image(matrix: np.ndarray, highlight: int) -> Image.Image:
    size = max(128, matrix.shape[0] * 24)
    lo = float(np.percentile(matrix, 5))
    hi = float(np.percentile(matrix, 95))
    normalized = np.clip((matrix - lo) / max(hi - lo, 1e-6), 0.0, 1.0)
    # Dark/green means recurrence (small distance), orange/red means change.
    rgb = np.zeros((*normalized.shape, 3), dtype=np.uint8)
    rgb[:, :, 0] = np.clip(normalized * 235 + 12, 0, 255).astype(np.uint8)
    rgb[:, :, 1] = np.clip((1.0 - normalized) * 210 + 24, 0, 255).astype(np.uint8)
    rgb[:, :, 2] = np.clip((1.0 - normalized) * 140 + 24, 0, 255).astype(np.uint8)
    image = Image.fromarray(rgb, mode="RGB").resize((size, size), Image.Resampling.NEAREST)
    draw = ImageDraw.Draw(image)
    cell = size / max(matrix.shape[0], 1)
    for index in range(matrix.shape[0] + 1):
        offset = round(index * cell)
        draw.line((offset, 0, offset, size), fill=(34, 34, 40), width=1)
        draw.line((0, offset, size, offset), fill=(34, 34, 40), width=1)
    center = (round(highlight * cell + cell / 2), round(highlight * cell + cell / 2))
    draw.rectangle((center[0] - max(2, round(cell / 2)), center[1] - max(2, round(cell / 2)), center[0] + max(2, round(cell / 2)), center[1] + max(2, round(cell / 2))), outline=(255, 255, 255), width=2)
    for index in range(matrix.shape[0]):
        draw.text((round(index * cell + 2), 2), str(index), fill=(245, 245, 245))
        draw.text((2, round(index * cell + 2)), str(index), fill=(245, 245, 245))
    return image


def onion_skin(cells: list[Image.Image], current: int, target_cx: float, target_bottom: int) -> Image.Image:
    canvas = np.zeros((CELL_H, CELL_W, 3), dtype=np.float32)
    weights = ((-2, (0, 185, 255), 0.30), (-1, (35, 110, 255), 0.48), (0, (255, 255, 255), 1.0), (1, (255, 35, 210), 0.48), (2, (255, 205, 0), 0.30))
    for offset, colour, weight in weights:
        cell = register_cell(cells[(current + offset) % len(cells)], target_cx, target_bottom)
        mask = np.asarray(cell.getchannel("A"), dtype=np.float32) / 255.0
        color = np.asarray(colour, dtype=np.float32)
        canvas = canvas * (1.0 - np.minimum(mask[:, :, None] * weight, 0.78)) + color * np.minimum(mask[:, :, None] * weight, 0.78)
    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8), mode="RGB")


def cycle_strip(cells: list[Image.Image], current: int) -> Image.Image:
    tile_w, tile_h = DISPLAY_SIZE
    canvas = Image.new("RGB", (tile_w * len(cells), tile_h + 16), (18, 18, 24))
    draw = ImageDraw.Draw(canvas)
    for index, cell in enumerate(cells):
        panel = composite(cell).resize(DISPLAY_SIZE, Image.Resampling.NEAREST)
        canvas.paste(panel, (index * tile_w, 16))
        draw.text((index * tile_w + 2, 2), str(index), fill=(255, 255, 255))
        if index == current:
            draw.rectangle((index * tile_w, 16, (index + 1) * tile_w - 1, tile_h + 15), outline=(255, 255, 255), width=2)
    return canvas


def panel_fit(image: Image.Image, size: tuple[int, int] = PANEL_SIZE) -> Image.Image:
    return image.resize(size, Image.Resampling.NEAREST)


def candidate_tile(item: dict, cells: list[Image.Image], matrix: np.ndarray, target_cx: float, target_bottom: int) -> Image.Image:
    frame = int(item["frame"])
    current = panel_fit(composite(cells[frame]))
    recurrence = normalized_recurrence_image(matrix, frame).resize(PANEL_SIZE, Image.Resampling.NEAREST)
    onion = onion_skin(cells, frame, target_cx, target_bottom)
    strip = cycle_strip(cells, frame).resize((PANEL_SIZE[0], 88), Image.Resampling.NEAREST)
    canvas = Image.new("RGB", (PANEL_SIZE[0] * 4, PANEL_SIZE[1] + 34), (14, 14, 20))
    for index, panel in enumerate((current, recurrence, onion, strip)):
        canvas.paste(panel, (index * PANEL_SIZE[0], 26))
    draw = ImageDraw.Draw(canvas)
    label = f"{item['role']}/{item['row']} f{frame} score={item['score']:.2f}"
    if item.get("known_blocker"):
        label += " CONTROL"
    draw.text((3, 5), label, fill=(245, 245, 245))
    draw.text((3, PANEL_SIZE[1] + 14), "CURRENT | RECURRENCE (低=重复) | 五帧洋葱皮 | 完整循环", fill=(212, 212, 222))
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--reviewed", action="store_true", help="record parent normal-size inspection of the candidate sheet")
    parser.add_argument("--non-blocker-only", action="store_true", help="exclude known blocker controls from the candidate sheet")
    args = parser.parse_args()

    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or output_dir / "cycle-recurrence-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "cycle-recurrence-candidates-v1.jpg"

    rows: dict[tuple[str, str], dict] = {}
    frame_records: list[dict] = []
    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        with Image.open(atlas_path) as image:
            atlas = image.convert("RGBA")
        for row_index, row_name in enumerate(ROWS):
            cells = [open_cell(atlas, row_index, frame) for frame in range(FRAME_COUNTS[row_name])]
            anchors = [lower_anchor(alpha_mask(cell)) for cell in cells]
            visible_anchors = [(cx, bottom) for cx, bottom in anchors if bottom >= 0]
            target_cx = float(np.median([cx for cx, _ in visible_anchors])) if visible_anchors else 0.0
            target_bottom = int(round(np.median([bottom for _, bottom in visible_anchors]))) if visible_anchors else -1
            aligned = [register_cell(cell, target_cx, target_bottom) for cell in cells]
            vectors = np.stack([descriptor(cell) for cell in aligned])
            matrix = pairwise_distance(vectors)
            count = len(cells)
            frame_scores: list[dict] = []
            for frame in range(count):
                non_adjacent = [matrix[frame, other] for other in range(count) if other != frame and cyclic_distance(frame, other, count) > 1]
                adjacent = [matrix[frame, (frame - 1) % count], matrix[frame, (frame + 1) % count]]
                nearest_non_adjacent = float(min(non_adjacent)) if non_adjacent else float(np.mean(adjacent))
                adjacent_mean = float(np.mean(adjacent))
                # Negative margin means a non-neighbour is at least as similar
                # as a neighbour, a useful recurrence/phase-order candidate.
                recurrence_margin = float(adjacent_mean - nearest_non_adjacent)
                row_mean = float(np.mean(matrix[frame]))
                frame_scores.append({
                    "role": role,
                    "row": row_name,
                    "frame": frame,
                    "adjacent_mean": round(adjacent_mean, 6),
                    "nearest_non_adjacent": round(nearest_non_adjacent, 6),
                    "recurrence_margin": round(recurrence_margin, 6),
                    "row_distance_mean": round(row_mean, 6),
                    "nearest_non_adjacent_frame": int(np.argmin(np.where(np.asarray([cyclic_distance(frame, other, count) > 1 for other in range(count)]), matrix[frame], np.inf))),
                })
            margins = np.asarray([item["recurrence_margin"] for item in frame_scores], dtype=np.float32)
            row_means = np.asarray([item["row_distance_mean"] for item in frame_scores], dtype=np.float32)
            for item in frame_scores:
                item["recurrence_z"] = round(robust_z(float(item["recurrence_margin"]), margins), 6)
                item["outlier_z"] = round(robust_z(float(item["row_distance_mean"]), row_means), 6)
                item["score"] = round(min(20.0, 0.72 * float(item["recurrence_z"]) + 0.28 * float(item["outlier_z"])), 6)
                item["known_blocker"] = KNOWN_BLOCKERS.get((role, row_name, int(item["frame"])))
                frame_records.append(item)
            rows[(role, row_name)] = {
                "role": role,
                "row": row_name,
                "frames": count,
                "target_lower_cx": round(target_cx, 3),
                "target_bottom": target_bottom,
                "recurrence_matrix": [[round(float(value), 6) for value in matrix[index]] for index in range(count)],
                "frame_records": frame_scores,
                "non_adjacent_pairs": [
                    {"frame_a": int(a), "frame_b": int(b), "distance": round(float(matrix[a, b]), 6)}
                    for a in range(count)
                    for b in range(a + 1, count)
                    if cyclic_distance(a, b, count) > 1
                ],
                "_cells": cells,
            }

    # Always include known blocker controls, then the strongest recurrence
    # candidates while keeping the sheet compact enough for manual inspection.
    frame_records.sort(key=lambda item: (-bool(item.get("known_blocker")), -float(item["score"]), item["role"], item["row"], int(item["frame"])))
    selected: list[dict] = []
    seen: set[tuple[str, str, int]] = set()
    candidate_source = [item for item in frame_records if not args.non_blocker_only or not item.get("known_blocker")]
    for item in candidate_source:
        key = (item["role"], item["row"], int(item["frame"]))
        if key in seen:
            continue
        selected.append(item)
        seen.add(key)
        if len(selected) >= 24:
            break

    columns = 2
    tile_width = PANEL_SIZE[0] * 4
    tile_height = PANEL_SIZE[1] + 34
    sheet = Image.new("RGB", (columns * tile_width, math.ceil(len(selected) / columns) * tile_height), (10, 10, 14))
    for index, item in enumerate(selected):
        data = rows[(item["role"], item["row"])]
        tile = candidate_tile(item, data["_cells"], np.asarray(data["recurrence_matrix"], dtype=np.float32), float(data["target_lower_cx"]), int(data["target_bottom"]))
        sheet.paste(tile, ((index % columns) * tile_width, (index // columns) * tile_height))
    sheet.save(sheet_out, quality=92, subsampling=0)

    serial_rows = []
    for key in sorted(rows):
        data = rows[key].copy()
        data.pop("_cells", None)
        serial_rows.append(data)
    top_non_adjacent = sorted(
        [item for item in frame_records if not item.get("known_blocker")],
        key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])),
    )[:24]
    result = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "supplemental non-generative recurrence and onion-skin visual review of all current v2 atlases",
        "method": {
            "name": "cycle recurrence matrix with five-frame onion skin",
            "steps": [
                "register each used cell to the row median lower-body anchor and baseline",
                "build fixed-size alpha/luminance/edge/colour descriptors",
                "compare every frame with every other frame in a cyclic recurrence matrix",
                "rank frames whose non-adjacent recurrence is at least as strong as adjacent motion or whose descriptor is a row outlier",
                "render current frame, recurrence heatmap, previous/current/next two-frame onion skin, and complete cycle strip",
                "treat all numeric outliers as candidates only; promote hard failures only after normal-size visual inspection and hatch-pet policy",
            ],
            "why_complementary": "Sequence-level recurrence reveals accidental repeated poses, phase reversals, and multi-lobe cycle trails that can survive pairwise residual, topology, and component checks.",
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": int(sum(FRAME_COUNTS.values()) * len(ROLES)),
            "cyclic_transitions": int(sum(FRAME_COUNTS.values()) * len(ROLES)),
            "candidate_sheet_frames": len(selected),
        },
        "candidate_counts": {
            "scored_frames": len(frame_records),
            "known_blocker_controls": sum(1 for item in frame_records if item.get("known_blocker")),
            "non_blocker_candidates": len(top_non_adjacent),
        },
        "visual_review": {
            "status": "pending_normal_size_inspection" if not args.reviewed else "pass_with_eight_existing_blocked_rows",
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
                "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
            ],
            "open_blocked_rows": OPEN_BLOCKED_ROWS,
            "review_basis": [
                "cycle-recurrence-candidates-v1.jpg",
                "cycle-recurrence-nonblock-candidates-v1.jpg",
            ],
            "note": "Candidate sheet inspected at normal display size; recurrence candidates not listed as known blockers did not show a new hard failure." if args.reviewed else "Inspect cycle-recurrence-candidates-v1.jpg at normal display size before promoting any candidate.",
        },
        "result": {
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": 4,
            "open_blocked_rows": OPEN_BLOCKED_ROWS,
            "formal_assets_modified": False,
            "release_effect": "supplemental evidence only; the eight complete-row regeneration blockers remain open",
        },
        "top_non_blocker_candidates": top_non_adjacent,
        "rows": serial_rows,
        "artifacts": [
            "cycle-recurrence-review-20260831-v1.json",
            "cycle-recurrence-candidates-v1.jpg",
            "cycle-recurrence-nonblock-candidates-v1.jpg",
            "cycle_recurrence_review.py",
        ],
    }
    json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json_out": str(json_out), "sheet_out": str(sheet_out), "selected": len(selected), "frames": len(frame_records)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
