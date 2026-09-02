#!/usr/bin/env python3
"""Evidence-only color-vision and low-saturation stress review for v2 pets.

The review keeps the alpha channel and geometry unchanged, applies common
color-vision simulations to a rendered copy, and ranks frames whose small-size
foreground/background or internal feature contrast drops the most.  A metric
is only a triage signal: it never modifies or invalidates a formal pet asset.
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
BACKGROUND = (112, 114, 122)

# Brettel-style linear approximations are sufficient for an evidence-only
# stress pass.  They are intentionally documented and deterministic rather
# than presented as a clinical color-vision diagnosis.
TRANSFORMS = {
    "original": np.eye(3, dtype=np.float32),
    "grayscale": np.asarray(
        [
            [0.2126, 0.7152, 0.0722],
            [0.2126, 0.7152, 0.0722],
            [0.2126, 0.7152, 0.0722],
        ],
        dtype=np.float32,
    ),
    "protan": np.asarray(
        [
            [0.567, 0.433, 0.000],
            [0.558, 0.442, 0.000],
            [0.000, 0.242, 0.758],
        ],
        dtype=np.float32,
    ),
    "deutan": np.asarray(
        [
            [0.625, 0.375, 0.000],
            [0.700, 0.300, 0.000],
            [0.000, 0.300, 0.700],
        ],
        dtype=np.float32,
    ),
    "tritan": np.asarray(
        [
            [0.950, 0.050, 0.000],
            [0.000, 0.433, 0.567],
            [0.000, 0.475, 0.525],
        ],
        dtype=np.float32,
    ),
}
VARIANTS = tuple(TRANSFORMS)
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
    row_index = ROW_INDEX[row]
    return atlas.crop(
        (frame * CELL_W, row_index * CELL_H, (frame + 1) * CELL_W, (row_index + 1) * CELL_H)
    ).convert("RGBA")


def transform_rgba(cell: Image.Image, name: str) -> Image.Image:
    rgba = np.asarray(cell.convert("RGBA"), dtype=np.uint8)
    rgb = rgba[:, :, :3].astype(np.float32) / 255.0
    transformed = np.einsum("...c,dc->...d", rgb, TRANSFORMS[name])
    output = np.clip(transformed * 255.0, 0.0, 255.0).astype(np.uint8)
    return Image.fromarray(np.dstack((output, rgba[:, :, 3])), mode="RGBA")


def composite(cell: Image.Image, size: tuple[int, int]) -> np.ndarray:
    background = np.asarray(BACKGROUND, dtype=np.float32)[None, None, :]
    scaled = np.asarray(cell.resize(size, Image.Resampling.LANCZOS), dtype=np.uint8)
    alpha = scaled[:, :, 3:4].astype(np.float32) / 255.0
    rgb = scaled[:, :, :3].astype(np.float32) * alpha + background * (1.0 - alpha)
    return np.clip(rgb, 0.0, 255.0).astype(np.uint8)


def mask_at_size(cell: Image.Image, size: tuple[int, int]) -> np.ndarray:
    alpha = np.asarray(cell.getchannel("A").resize(size, Image.Resampling.BILINEAR), dtype=np.uint8)
    return alpha >= 48


def luma(rgb: np.ndarray) -> np.ndarray:
    return (
        0.2126 * rgb[:, :, 0].astype(np.float32)
        + 0.7152 * rgb[:, :, 1].astype(np.float32)
        + 0.0722 * rgb[:, :, 2].astype(np.float32)
    )


def edge_energy(gray: np.ndarray) -> float:
    dx = np.diff(gray, axis=1, prepend=gray[:, :1])
    dy = np.diff(gray, axis=0, prepend=gray[:1, :])
    return float(np.mean(np.hypot(dx, dy)) / 255.0)


def feature_metrics(cell: Image.Image, size: tuple[int, int]) -> dict[str, float]:
    rendered = composite(cell, size)
    gray = luma(rendered)
    mask = mask_at_size(cell, size)
    if not np.any(mask):
        return {
            "foreground_contrast": 0.0,
            "internal_luma_std": 0.0,
            "edge_energy": 0.0,
            "strong_edge_fraction": 0.0,
            "visible_fraction": 0.0,
        }
    background_luma = luma(np.asarray([[BACKGROUND]], dtype=np.uint8))[0, 0]
    foreground = gray[mask]
    contrast = np.abs(foreground - background_luma) / 255.0
    local_dx = np.diff(gray, axis=1, prepend=gray[:, :1])
    local_dy = np.diff(gray, axis=0, prepend=gray[:1, :])
    local_edge = np.hypot(local_dx, local_dy)
    strong = local_edge[mask] >= 18.0
    return {
        "foreground_contrast": float(np.mean(contrast)),
        "internal_luma_std": float(np.std(foreground) / 255.0),
        "edge_energy": edge_energy(gray),
        "strong_edge_fraction": float(np.mean(strong)),
        "visible_fraction": float(np.mean(mask)),
    }


def relative_loss(original: dict[str, float], variant: dict[str, float], key: str) -> float:
    baseline = max(float(original[key]), 1e-6)
    return max(0.0, float(original[key]) - float(variant[key])) / baseline


def frame_record(cell: Image.Image, role: str, row: str, frame: int) -> tuple[dict, dict[str, Image.Image]]:
    transformed = {name: transform_rgba(cell, name) for name in VARIANTS}
    by_size: dict[str, dict[str, dict[str, float]]] = {}
    losses: list[float] = []
    for size in DISPLAY_SIZES:
        size_key = f"{size[0]}x{size[1]}"
        original_metrics = feature_metrics(transformed["original"], size)
        variants: dict[str, dict[str, float]] = {"original": original_metrics}
        for name in VARIANTS[1:]:
            metrics = feature_metrics(transformed[name], size)
            variants[name] = metrics
            for key in ("foreground_contrast", "internal_luma_std", "edge_energy", "strong_edge_fraction"):
                losses.append(relative_loss(original_metrics, metrics, key))
        by_size[size_key] = variants
    worst = max(losses) if losses else 0.0
    mean_loss = float(np.mean(losses)) if losses else 0.0
    score = 0.72 * worst + 0.28 * mean_loss
    return (
        {
            "role": role,
            "row": row,
            "row_index": ROW_INDEX[row],
            "frame": frame,
            "score": round(float(score), 6),
            "worst_relative_loss": round(float(worst), 6),
            "mean_relative_loss": round(float(mean_loss), 6),
            "metrics": by_size,
            "known_blocker": KNOWN_BLOCKERS.get((role, row)),
        },
        transformed,
    )


def panel(cell: Image.Image, size: tuple[int, int] = DISPLAY_SIZES[0]) -> Image.Image:
    rendered = Image.fromarray(composite(cell, size), mode="RGB")
    return rendered.resize((size[0] * 2, size[1] * 2), Image.Resampling.NEAREST)


def alpha_panel(cell: Image.Image, size: tuple[int, int] = DISPLAY_SIZES[0]) -> Image.Image:
    mask = mask_at_size(cell, size)
    image = np.full((size[1], size[0], 3), (22, 24, 30), dtype=np.uint8)
    image[mask] = (238, 238, 242)
    return Image.fromarray(image, mode="RGB").resize((size[0] * 2, size[1] * 2), Image.Resampling.NEAREST)


def make_tile(record: dict, transformed: dict[str, Image.Image], size: tuple[int, int]) -> Image.Image:
    labels = ("original", "grayscale", "protan", "deutan", "tritan", "alpha")
    tile_w = size[0] * 2 * len(labels)
    tile_h = size[1] * 2 + 48
    tile = Image.new("RGB", (tile_w, tile_h), (14, 15, 20))
    draw = ImageDraw.Draw(tile)
    title = f"{record['role']}/{record['row']}/f{record['frame']} score={record['score']:.3f}"
    draw.text((3, 3), title, fill=(245, 245, 245))
    for index, label in enumerate(labels):
        image = alpha_panel(transformed["original"], size) if label == "alpha" else panel(transformed[label], size)
        x = index * size[0] * 2
        tile.paste(image, (x, 22))
        draw.text((x + 3, tile_h - 20), label, fill=(205, 208, 218))
    return tile


def make_sheet(
    candidates: list[dict],
    visual_payload: dict[tuple[str, str, int], dict[str, Image.Image]],
    output: Path,
    size: tuple[int, int],
) -> None:
    tiles = [
        make_tile(item, visual_payload[(item["role"], item["row"], item["frame"])], size)
        for item in candidates
    ]
    columns = 2
    tile_w = tiles[0].width if tiles else size[0] * 2 * 6
    tile_h = tiles[0].height if tiles else size[1] * 2 + 48
    sheet = Image.new(
        "RGB",
        (columns * tile_w, max(1, (len(tiles) + columns - 1) // columns) * tile_h),
        (10, 11, 16),
    )
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % columns) * tile_w, (index // columns) * tile_h))
    sheet.save(output, quality=92, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--small-sheet-out", type=Path, default=None)
    parser.add_argument("--top", type=int, default=32)
    parser.add_argument("--reviewed", action="store_true")
    parser.add_argument("--manual-verdict", default="pending_review")
    parser.add_argument("--manual-note", default="")
    args = parser.parse_args()

    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or output_dir / "color-vision-stress-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "color-vision-stress-candidates-v1.jpg"
    small_sheet_out = args.small_sheet_out or output_dir / "color-vision-stress-candidates-48x52-v1.jpg"

    records: list[dict] = []
    visual_payload: dict[tuple[str, str, int], dict[str, Image.Image]] = {}
    for role in ROLES:
        with Image.open(repo / "pets" / role / "spritesheet.webp") as opened:
            atlas = opened.convert("RGBA")
        for row in ROWS:
            for frame in range(FRAME_COUNTS[row]):
                cell = open_cell(atlas, row, frame)
                record, transformed = frame_record(cell, role, row, frame)
                records.append(record)
                visual_payload[(role, row, frame)] = transformed

    candidates = sorted(records, key=lambda item: float(item["score"]), reverse=True)[: max(args.top, 1)]
    # Keep each known blocker visible in the bounded sheet when it is not
    # already selected by the score, so the control sensitivity is auditable.
    selected_keys = {(item["role"], item["row"], item["frame"]) for item in candidates}
    for (role, row), _description in KNOWN_BLOCKERS.items():
        control_frame = 0
        if row == "jumping":
            control_frame = 2
        elif row == "waiting" and role == "hei-mao-foodie":
            control_frame = 2
        elif row == "failed" and role == "hei-mao-delivery":
            control_frame = 2
        key = (role, row, control_frame)
        if key not in selected_keys:
            match = next(item for item in records if (item["role"], item["row"], item["frame"]) == key)
            candidates.append(match)
            selected_keys.add(key)
    candidates = candidates[: max(args.top, 1) + len(KNOWN_BLOCKERS)]

    make_sheet(candidates, visual_payload, sheet_out, DISPLAY_SIZES[0])
    make_sheet(candidates, visual_payload, small_sheet_out, DISPLAY_SIZES[1])

    output = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "evidence-only color-vision and low-saturation stress review of all current v2 atlases",
        "method": {
            "name": "color-vision simulation and low-saturation display stress",
            "purpose": "surface loss of foreground/background or internal feature contrast when color information is reduced",
            "transforms": list(VARIANTS),
            "display_sizes": [list(size) for size in DISPLAY_SIZES],
            "background": list(BACKGROUND),
            "steps": [
                "preserve source alpha and geometry while applying deterministic color-vision simulations",
                "render original, grayscale, protan, deutan, and tritan variants at 96x104 and 48x52",
                "compare foreground contrast, internal luminance separation, and edge retention against the original",
                "rank candidates and retain known-blocker controls in a bounded normal-size sheet",
                "treat all metrics as triage evidence; promote only visible defects under hatch-pet policy",
            ],
        },
        "scope_details": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "cells": len(records),
            "candidate_sheet_items": len(candidates),
            "alpha_threshold": ALPHA_THRESHOLD,
        },
        "visual_review": {
            "status": args.manual_verdict if args.reviewed else "pending_review",
            "note": args.manual_note if args.reviewed else "96x104 and 48x52 candidate sheets require normal-size inspection",
            "new_hard_failures": [],
            "new_warnings": [],
            "confirmed_existing_blockers": sorted(
                {
                    f"{role}/{row}: {description}"
                    for (role, row), description in KNOWN_BLOCKERS.items()
                    if any(
                        item["role"] == role and item["row"] == row
                        for item in candidates
                    )
                }
            ),
            "formal_assets_modified": False,
        },
        "top_candidates": candidates,
        "artifacts": [json_out.name, sheet_out.name, small_sheet_out.name, Path(__file__).name],
        "limitations": [
            "The simulation is an accessibility-oriented display stress test, not a clinical color-vision model.",
            "Color loss can be intentional for a role or prop; metrics do not infer semantic importance of an unlabeled component.",
            "This is offline asset evidence and cannot prove Codex App window layering, multi-screen placement, bubble tracking, or GPU composition.",
            "The authoritative alpha/despill and v2 atlas validators remain the release gates for transparency and structure.",
        ],
    }
    json_out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
