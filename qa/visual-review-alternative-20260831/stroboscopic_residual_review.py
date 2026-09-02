#!/usr/bin/env python3
"""Evidence-only pose-normalized stroboscopic residual review.

The review aligns adjacent frames by their lower-body anchor, then presents a
normal-size previous/current/difference triplet.  It is intentionally
complementary to silhouette-only and optical-flow checks: a high-frequency
interior residual can expose a material, face, or prop redraw even when the
outer bounding box remains plausible.  Scores are candidates only and never
rewrite a formal asset.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance


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
ALPHA_THRESHOLD = 16
DISPLAY_SIZE = (96, 104)
SHEET_COLUMNS = 2
SHEET_ITEM_W = 4 * DISPLAY_SIZE[0]
SHEET_ITEM_H = DISPLAY_SIZE[1] + 27

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


def robust_z(value: float, values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    med = float(np.median(values))
    mad = float(np.median(np.abs(values - med)))
    scale = max(1.4826 * mad, float(np.std(values)) * 0.25, 1e-6)
    return abs(value - med) / scale


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
    lower_x = xs[ys >= lower_start]
    return float(np.mean(lower_x if len(lower_x) else xs)), y1


def translate_rgba(cell: Image.Image, dx: int, dy: int) -> Image.Image:
    src = np.asarray(cell, dtype=np.uint8)
    out = np.zeros_like(src)
    src_y0 = max(0, -dy)
    src_y1 = min(CELL_H, CELL_H - dy)
    src_x0 = max(0, -dx)
    src_x1 = min(CELL_W, CELL_W - dx)
    if src_y1 > src_y0 and src_x1 > src_x0:
        out[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = src[
            src_y0:src_y1, src_x0:src_x1
        ]
    return Image.fromarray(out, mode="RGBA")


def erode(mask: np.ndarray) -> np.ndarray:
    out = mask.copy()
    out[:-1, :] &= mask[1:, :]
    out[1:, :] &= mask[:-1, :]
    out[:, :-1] &= mask[:, 1:]
    out[:, 1:] &= mask[:, :-1]
    return out


def composite(cell: Image.Image, background: int = 96) -> np.ndarray:
    rgba = np.asarray(cell, dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    return rgba[:, :, :3] * alpha + background * (1.0 - alpha)


def resize_display(rgb: np.ndarray) -> np.ndarray:
    image = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")
    return np.asarray(image.resize(DISPLAY_SIZE, Image.Resampling.LANCZOS), dtype=np.float32)


def residual_metrics(previous: Image.Image, current: Image.Image) -> tuple[dict, Image.Image]:
    previous_mask = alpha_mask(previous)
    current_mask = alpha_mask(current)
    prev_cx, prev_bottom = lower_anchor(previous_mask)
    cur_cx, cur_bottom = lower_anchor(current_mask)
    dx = int(round(cur_cx - prev_cx))
    dy = int(cur_bottom - prev_bottom)
    aligned_previous = translate_rgba(previous, dx, dy)

    prev_rgb = composite(aligned_previous)
    cur_rgb = composite(current)
    diff = np.abs(cur_rgb - prev_rgb)
    union = np.logical_or(alpha_mask(aligned_previous), current_mask)
    overlap = np.logical_and(alpha_mask(aligned_previous), current_mask)
    interior = erode(alpha_mask(aligned_previous)) & erode(current_mask)
    if not np.any(union):
        union = np.ones((CELL_H, CELL_W), dtype=bool)
    edge = union & ~interior
    interior_values = diff[interior] if np.any(interior) else diff[union]
    edge_values = diff[edge] if np.any(edge) else diff[union]
    shape_iou = float(overlap.sum() / max(union.sum(), 1))
    interior_mean = float(np.mean(interior_values) / 255.0)
    edge_mean = float(np.mean(edge_values) / 255.0)
    diff_energy = float(np.mean(diff[union]) / 255.0)

    diff_display = np.clip(resize_display(diff * 4.0), 0, 255).astype(np.uint8)
    diff_image = Image.fromarray(diff_display, mode="RGB")
    return {
        "anchor_dx": dx,
        "anchor_dy": dy,
        "shape_iou": shape_iou,
        "interior_residual": interior_mean,
        "edge_residual": edge_mean,
        "residual_energy": diff_energy,
    }, diff_image


def normal_display(cell: Image.Image) -> Image.Image:
    return Image.fromarray(np.clip(resize_display(composite(cell)), 0, 255).astype(np.uint8), mode="RGB")


def make_item(previous: Image.Image, current: Image.Image, diff: Image.Image, label: str) -> Image.Image:
    canvas = Image.new("RGB", (SHEET_ITEM_W, SHEET_ITEM_H), (24, 24, 30))
    panels = [normal_display(previous), normal_display(current), diff]
    # Fourth panel is a high-contrast alpha union.  This separates a real
    # silhouette/topology change from a chroma or material-only difference.
    prev_mask = np.asarray(previous.getchannel("A"), dtype=np.uint8)
    cur_mask = np.asarray(current.getchannel("A"), dtype=np.uint8)
    union = np.maximum(prev_mask, cur_mask)
    union_display = Image.fromarray(union, mode="L").resize(DISPLAY_SIZE, Image.Resampling.NEAREST)
    union_rgb = Image.new("RGB", DISPLAY_SIZE, (20, 20, 24))
    union_rgb.paste((236, 236, 236), mask=union_display)
    panels.append(union_rgb)
    for index, panel in enumerate(panels):
        canvas.paste(panel, (index * DISPLAY_SIZE[0], 22))
    draw = ImageDraw.Draw(canvas)
    draw.text((3, 4), label, fill=(244, 244, 244))
    draw.text((3, SHEET_ITEM_H - 12), "PREV  CURRENT  DIFFx4  ALPHA-UNION", fill=(185, 185, 195))
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
    json_out = args.json_out or (output_dir / "stroboscopic-residual-review-20260831-v1.json")
    sheet_out = args.sheet_out or (output_dir / "stroboscopic-residual-candidates-v1.jpg")

    records: list[dict] = []
    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        with Image.open(atlas_path) as image:
            atlas = image.convert("RGBA")
        for row_index, row_name in enumerate(ROWS):
            transitions: list[dict] = []
            for frame in range(FRAME_COUNTS[row_name]):
                next_frame = (frame + 1) % FRAME_COUNTS[row_name]
                previous = open_cell(atlas, row_index, frame)
                current = open_cell(atlas, row_index, next_frame)
                metrics, _diff = residual_metrics(previous, current)
                transitions.append({
                    "role": role,
                    "row": row_name,
                    "frame": frame,
                    "next_frame": next_frame,
                    **metrics,
                })
            interior_values = np.asarray([r["interior_residual"] for r in transitions], dtype=np.float32)
            edge_values = np.asarray([r["edge_residual"] for r in transitions], dtype=np.float32)
            energy_values = np.asarray([r["residual_energy"] for r in transitions], dtype=np.float32)
            for record in transitions:
                record["interior_z"] = robust_z(record["interior_residual"], interior_values)
                record["edge_z"] = robust_z(record["edge_residual"], edge_values)
                record["energy_z"] = robust_z(record["residual_energy"], energy_values)
                record["score"] = round(
                    min(12.0, 0.45 * record["interior_z"] + 0.35 * record["edge_z"] + 0.20 * record["energy_z"]),
                    6,
                )
                records.append(record)

    records.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], item["frame"]))
    known = [r for r in records if (r["role"], r["row"], r["frame"]) in KNOWN_BLOCKERS]
    selected: list[dict] = []
    seen: set[tuple[str, str, int]] = set()
    for record in known + records:
        key = (record["role"], record["row"], int(record["frame"]))
        if key in seen:
            continue
        selected.append(record)
        seen.add(key)
        if len(selected) >= 24:
            break

    sheet = Image.new("RGB", (SHEET_COLUMNS * SHEET_ITEM_W, math.ceil(len(selected) / SHEET_COLUMNS) * SHEET_ITEM_H), (14, 14, 18))
    for index, record in enumerate(selected):
        atlas_path = repo / "pets" / record["role"] / "spritesheet.webp"
        with Image.open(atlas_path) as image:
            atlas = image.convert("RGBA")
        previous = open_cell(atlas, ROWS.index(record["row"]), int(record["frame"]))
        current = open_cell(atlas, ROWS.index(record["row"]), int(record["next_frame"]))
        metrics, diff = residual_metrics(previous, current)
        control = KNOWN_BLOCKERS.get((record["role"], record["row"], int(record["frame"])))
        label = f"{record['role']}/{record['row']} {record['frame']}->{record['next_frame']} s={record['score']:.2f}"
        if control:
            label += " CONTROL"
        item = make_item(previous, current, diff, label)
        x = (index % SHEET_COLUMNS) * SHEET_ITEM_W
        y = (index // SHEET_COLUMNS) * SHEET_ITEM_H
        sheet.paste(item, (x, y))
    sheet.save(sheet_out, quality=92, subsampling=0)

    report = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "supplemental pose-normalized stroboscopic residual review of all current v2 atlases; evidence only",
        "formal_assets_modified": False,
        "method": {
            "name": "lower-anchor aligned stroboscopic residual and alpha-union review",
            "steps": [
                "align each adjacent frame by the lower-body centroid and bottom baseline",
                "compare composited RGB in the aligned interior and boundary bands",
                "rank transitions within each role and row using robust residual scores",
                "render normal-size PREV/CURRENT/DIFFx4/ALPHA-UNION panels",
                "include loop-closing transitions and known blocker controls",
                "treat every score as a candidate requiring visual confirmation",
            ],
            "purpose": "suppress whole-body translation and expose internal face/material/prop redraws or abrupt contour changes that may be diluted in raw bbox and flow metrics",
            "display_size": list(DISPLAY_SIZE),
            "alpha_threshold": ALPHA_THRESHOLD,
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": len(records),
            "transitions_including_loop": len(records),
            "candidate_sheet_items": len(selected),
        },
        "known_blockers_reproduced": [
            f"{role}/{row} frame {frame}: {description}"
            for (role, row, frame), description in KNOWN_BLOCKERS.items()
            if any(r["role"] == role and r["row"] == row and r["frame"] == frame for r in selected)
        ],
        "top_candidates": selected,
        "visual_review": {
            "status": "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": [],
            "note": "Inspect the normal-size candidate sheet; residual scores are evidence only and do not replace hatch-pet semantic review.",
        },
        "artifacts": [sheet_out.name, json_out.name],
        "limitations": [
            "translation alignment does not model articulated part motion or physical occlusion",
            "intentional gestures, look arcs, and asymmetric props can produce high residuals",
            "the review is asset-only and cannot prove browser GPU, live Codex App, multi-screen, or bubble tracking behavior",
            "a confirmed defect still requires complete-row regeneration and the standard deterministic and visual gates",
        ],
    }
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": len(records), "selected": len(selected)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
