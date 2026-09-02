#!/usr/bin/env python3
"""Evidence-only skeleton/topology review for the current PetDex v2 atlases.

The review is intentionally conservative.  It ranks shape-topology and
temporal-residual candidates for normal-size inspection, but never rewrites a
formal pet asset and never promotes a metric outlier to a failure by itself.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


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
ALPHA_THRESHOLD = 16
ANALYSIS_W = 96
ANALYSIS_H = 104

KNOWN_BLOCKERS = {
    "hei-mao/jumping/f2": "duplicated upper head",
    "hei-mao-quality/jumping/f2": "duplicated upper head",
    "hei-mao-foodie/waiting/f2": "stacked upper contours",
    "hei-mao-foodie/waiting/f3": "stacked upper contours",
    "hei-mao-delivery/failed/f0": "repeated head and pose-family switch",
    "hei-mao-delivery/failed/f1": "repeated head and pose-family switch",
    "hei-mao-delivery/failed/f2": "repeated head and pose-family switch",
    "hei-mao-delivery/failed/f3": "repeated head and pose-family switch",
    "hei-mao-delivery/failed/f4": "repeated head and pose-family switch",
}


def open_cell(atlas: Image.Image, row: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row * CELL_H, (frame + 1) * CELL_W, (row + 1) * CELL_H)
    ).convert("RGBA")


def alpha_mask(cell: Image.Image) -> np.ndarray:
    return np.asarray(cell.getchannel("A"), dtype=np.uint8) >= ALPHA_THRESHOLD


def reduce_mask(mask: np.ndarray) -> np.ndarray:
    reduced_image = Image.fromarray((mask.astype(np.uint8) * 255), mode="L").resize(
        (ANALYSIS_W, ANALYSIS_H),
        resample=Image.Resampling.BOX,
    )
    reduced = np.asarray(reduced_image, dtype=np.uint8).astype(np.float32) / 255.0
    # The source mask is represented as 0/1, not 0/255.  Use an occupancy
    # threshold in that same scale after area reduction.
    reduced = reduced >= 0.5
    # Close only one-pixel holes introduced by the half-size reduction.  The
    # original full-size mask remains the source for the proof-sheet overlay.
    reduced_image = Image.fromarray((reduced.astype(np.uint8) * 255), mode="L")
    closed = reduced_image.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    return np.asarray(closed, dtype=np.uint8) >= 128


def zhang_suen_thin(binary: np.ndarray) -> np.ndarray:
    """Return a one-pixel skeleton using the Zhang-Suen thinning algorithm."""

    image = binary.astype(np.uint8).copy()
    rows, cols = image.shape
    if not image.any():
        return image.astype(bool)

    changed = True
    iterations = 0
    while changed and iterations < 128:
        changed = False
        iterations += 1
        padded = np.pad(image, 1, mode="constant")
        p2 = padded[0:rows, 1 : cols + 1]
        p3 = padded[0:rows, 2 : cols + 2]
        p4 = padded[1 : rows + 1, 2 : cols + 2]
        p5 = padded[2 : rows + 2, 2 : cols + 2]
        p6 = padded[2 : rows + 2, 1 : cols + 1]
        p7 = padded[2 : rows + 2, 0:cols]
        p8 = padded[1 : rows + 1, 0:cols]
        p9 = padded[0:rows, 0:cols]
        neighbours = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
        transitions = (
            ((p2 == 0) & (p3 == 1)).astype(np.uint8)
            + ((p3 == 0) & (p4 == 1)).astype(np.uint8)
            + ((p4 == 0) & (p5 == 1)).astype(np.uint8)
            + ((p5 == 0) & (p6 == 1)).astype(np.uint8)
            + ((p6 == 0) & (p7 == 1)).astype(np.uint8)
            + ((p7 == 0) & (p8 == 1)).astype(np.uint8)
            + ((p8 == 0) & (p9 == 1)).astype(np.uint8)
            + ((p9 == 0) & (p2 == 1)).astype(np.uint8)
        )
        remove_a = (
            (image == 1)
            & (neighbours >= 2)
            & (neighbours <= 6)
            & (transitions == 1)
            & ((p2 * p4 * p6) == 0)
            & ((p4 * p6 * p8) == 0)
        )
        if np.any(remove_a):
            image[remove_a] = 0
            changed = True

        padded = np.pad(image, 1, mode="constant")
        p2 = padded[0:rows, 1 : cols + 1]
        p3 = padded[0:rows, 2 : cols + 2]
        p4 = padded[1 : rows + 1, 2 : cols + 2]
        p5 = padded[2 : rows + 2, 2 : cols + 2]
        p6 = padded[2 : rows + 2, 1 : cols + 1]
        p7 = padded[2 : rows + 2, 0:cols]
        p8 = padded[1 : rows + 1, 0:cols]
        p9 = padded[0:rows, 0:cols]
        neighbours = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
        transitions = (
            ((p2 == 0) & (p3 == 1)).astype(np.uint8)
            + ((p3 == 0) & (p4 == 1)).astype(np.uint8)
            + ((p4 == 0) & (p5 == 1)).astype(np.uint8)
            + ((p5 == 0) & (p6 == 1)).astype(np.uint8)
            + ((p6 == 0) & (p7 == 1)).astype(np.uint8)
            + ((p7 == 0) & (p8 == 1)).astype(np.uint8)
            + ((p8 == 0) & (p9 == 1)).astype(np.uint8)
            + ((p9 == 0) & (p2 == 1)).astype(np.uint8)
        )
        remove_b = (
            (image == 1)
            & (neighbours >= 2)
            & (neighbours <= 6)
            & (transitions == 1)
            & ((p2 * p4 * p8) == 0)
            & ((p2 * p6 * p8) == 0)
        )
        if np.any(remove_b):
            image[remove_b] = 0
            changed = True
    return image.astype(bool)


def label_components(mask: np.ndarray) -> tuple[int, np.ndarray]:
    """Label an 8-connected binary mask without a native CV dependency."""

    height, width = mask.shape
    labels = np.zeros((height, width), dtype=np.int32)
    label = 0
    for y, x in zip(*np.nonzero(mask)):
        if labels[y, x] != 0:
            continue
        label += 1
        labels[y, x] = label
        stack = [(int(y), int(x))]
        while stack:
            cy, cx = stack.pop()
            for dy in (-1, 0, 1):
                ny = cy + dy
                if ny < 0 or ny >= height:
                    continue
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx = cx + dx
                    if nx < 0 or nx >= width or not mask[ny, nx] or labels[ny, nx] != 0:
                        continue
                    labels[ny, nx] = label
                    stack.append((ny, nx))
    return label, labels


def holes_and_components(mask: np.ndarray) -> tuple[int, int]:
    component_count, _labels = label_components(mask)
    inverse = ~mask
    inverse_count, inverse_labels = label_components(inverse)
    border_labels = set(np.unique(np.concatenate([
        inverse_labels[0, :] if inverse_labels.size else np.array([], dtype=np.int32),
        inverse_labels[-1, :] if inverse_labels.size else np.array([], dtype=np.int32),
        inverse_labels[:, 0] if inverse_labels.size else np.array([], dtype=np.int32),
        inverse_labels[:, -1] if inverse_labels.size else np.array([], dtype=np.int32),
    ])))
    holes = sum(1 for label in range(1, inverse_count) if label not in border_labels)
    return int(component_count), int(holes)


def skeleton_metrics(mask: np.ndarray) -> tuple[dict[str, float | int], np.ndarray, np.ndarray]:
    reduced = reduce_mask(mask)
    components, holes = holes_and_components(reduced)
    skeleton = zhang_suen_thin(reduced)
    padded = np.pad(skeleton.astype(np.uint8), 1, mode="constant")
    neighbours = np.zeros_like(skeleton, dtype=np.uint16)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            neighbours += padded[1 + dy : 1 + dy + ANALYSIS_H, 1 + dx : 1 + dx + ANALYSIS_W]
    endpoints = int(np.logical_and(skeleton, neighbours == 1).sum())
    branchpoints = int(np.logical_and(skeleton, neighbours >= 3).sum())
    ys, xs = np.nonzero(reduced)
    if len(xs) == 0:
        return (
            {
                "components": 0,
                "holes": 0,
                "euler": 0,
                "skeleton_pixels": 0,
                "endpoints": 0,
                "branchpoints": 0,
                "skeleton_fraction": 0.0,
                "bbox_fill": 0.0,
                "upper_skeleton_fraction": 0.0,
                "lower_skeleton_fraction": 0.0,
            },
            reduced,
            skeleton,
        )
    area = float(reduced.sum())
    bbox_area = float((xs.max() - xs.min() + 1) * (ys.max() - ys.min() + 1))
    upper = skeleton[: int(ANALYSIS_H * 0.46)].sum()
    lower = skeleton[int(ANALYSIS_H * 0.46) :].sum()
    total_skeleton = int(skeleton.sum())
    return (
        {
            "components": components,
            "holes": holes,
            "euler": int(components - holes),
            "skeleton_pixels": total_skeleton,
            "endpoints": endpoints,
            "branchpoints": branchpoints,
            "skeleton_fraction": float(total_skeleton / max(area, 1.0)),
            "bbox_fill": float(area / max(bbox_area, 1.0)),
            "upper_skeleton_fraction": float(upper / max(total_skeleton, 1)),
            "lower_skeleton_fraction": float(lower / max(total_skeleton, 1)),
        },
        reduced,
        skeleton,
    )


METRIC_NAMES = [
    "components",
    "holes",
    "euler",
    "skeleton_pixels",
    "endpoints",
    "branchpoints",
    "skeleton_fraction",
    "bbox_fill",
    "upper_skeleton_fraction",
    "lower_skeleton_fraction",
]


def robust_z(value: float, values: np.ndarray, floor: float = 1e-4) -> float:
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    scale = max(1.4826 * mad, float(np.std(values)) * 0.25, floor)
    return abs(value - median) / scale


def metric_vector(metrics: dict[str, float | int]) -> np.ndarray:
    return np.asarray([float(metrics[name]) for name in METRIC_NAMES], dtype=np.float32)


def normalized_residual(current: np.ndarray, previous: np.ndarray, following: np.ndarray, scale: np.ndarray) -> float:
    expected = (previous + following) / 2.0
    residual = np.abs(current - expected) / np.maximum(scale, 1e-4)
    return float(np.mean(np.minimum(residual, 12.0)))


def composite(cell: Image.Image, background: tuple[int, int, int] = (34, 36, 44)) -> Image.Image:
    rgba = np.asarray(cell, dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    rgb = rgba[:, :, :3] * alpha + np.asarray(background, dtype=np.float32) * (1.0 - alpha)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")


def make_tile(item: dict, cell: Image.Image, reduced: np.ndarray, skeleton: np.ndarray) -> Image.Image:
    tile = Image.new("RGB", (CELL_W, CELL_H + 28), (14, 15, 20))
    tile.paste(composite(cell), (0, 28))
    draw = ImageDraw.Draw(tile)
    sk_y, sk_x = np.nonzero(skeleton)
    draw.point([(int(x * 2), int(y * 2 + 28)) for x, y in zip(sk_x, sk_y)], fill=(255, 224, 0))
    padded = np.pad(skeleton.astype(np.uint8), 1, mode="constant")
    neighbour_count = np.zeros_like(skeleton, dtype=np.uint16)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            neighbour_count += padded[1 + dy : 1 + dy + ANALYSIS_H, 1 + dx : 1 + dx + ANALYSIS_W]
    branch_y, branch_x = np.nonzero(np.logical_and(skeleton, neighbour_count >= 3))
    for x, y in zip(branch_x, branch_y):
        draw.ellipse((int(x * 2 - 2), int(y * 2 + 26), int(x * 2 + 3), int(y * 2 + 31)), fill=(255, 50, 50))
    control_tag = " CONTROL" if item.get("control") else ""
    title = f"{item['role']}/{item['row']}/f{item['frame']} s{item['score']:.1f}{control_tag}"
    subtitle = f"c{item['metrics']['components']} h{item['metrics']['holes']} e{item['metrics']['endpoints']} b{item['metrics']['branchpoints']}"
    draw.text((3, 3), title, fill=(240, 240, 240))
    draw.text((3, 15), subtitle, fill=(180, 190, 205))
    return tile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--reviewed", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or output_dir / "topology-skeleton-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "topology-skeleton-candidates-v1.jpg"

    rows: dict[tuple[str, str], list[dict]] = {}
    scored: list[dict] = []
    frame_count = 0
    transitions = 0

    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        atlas = Image.open(atlas_path).convert("RGBA")
        for row_index, row_name in enumerate(ROWS):
            frames: list[dict] = []
            for frame in range(COLS):
                cell = open_cell(atlas, row_index, frame)
                mask = alpha_mask(cell)
                metrics, reduced, skeleton = skeleton_metrics(mask)
                if metrics["components"] == 0:
                    continue
                frames.append({
                    "role": role,
                    "row": row_name,
                    "row_index": row_index,
                    "frame": frame,
                    "cell": cell,
                    "metrics": metrics,
                    "reduced": reduced,
                    "skeleton": skeleton,
                })
                frame_count += 1
            rows[(role, row_name)] = frames
            if not frames:
                continue
            vectors = np.stack([metric_vector(frame["metrics"]) for frame in frames], axis=0)
            scales = np.asarray([
                max(1.4826 * float(np.median(np.abs(vectors[:, index] - np.median(vectors[:, index])))),
                    float(np.std(vectors[:, index])) * 0.25,
                    0.01 if index >= 6 else 1.0)
                for index in range(vectors.shape[1])
            ], dtype=np.float32)
            for index, frame in enumerate(frames):
                z_score = 0.0
                reasons: list[str] = []
                for metric_index, name in enumerate(METRIC_NAMES):
                    value = float(frame["metrics"][name])
                    score = robust_z(value, vectors[:, metric_index], floor=float(scales[metric_index]))
                    weight = 1.25 if name in {"components", "holes", "euler", "branchpoints"} else 0.55
                    z_score += weight * min(score, 12.0)
                    if score >= 4.0:
                        reasons.append(f"{name}_z={score:.1f}")
                previous = vectors[(index - 1) % len(frames)]
                following = vectors[(index + 1) % len(frames)]
                residual = normalized_residual(vectors[index], previous, following, scales)
                score = min(24.0, z_score + 0.9 * residual)
                if residual >= 3.0:
                    reasons.append(f"temporal_topology_residual={residual:.2f}")
                item = {
                    "role": role,
                    "row": row_name,
                    "frame": int(frame["frame"]),
                    "score": round(float(score), 4),
                    "reasons": reasons or ["combined-skeleton-topology-distance"],
                    "metrics": frame["metrics"],
                    "analysis_size": [ANALYSIS_W, ANALYSIS_H],
                    "temporal_topology_residual": round(float(residual), 4),
                    "reduced": frame["reduced"],
                    "skeleton": frame["skeleton"],
                    "cell": frame["cell"],
                }
                scored.append(item)
                transitions += 1

    scored.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])))
    top = scored[:28]
    by_key = {
        f"{item['role']}/{item['row']}/f{item['frame']}": item
        for item in scored
    }
    # Keep the known visual blockers as explicit controls even when unrelated
    # texture-rich rows outrank them.  Controls are evidence for comparison,
    # not evidence that this metric independently rediscovered the defect.
    control_items = []
    for key in KNOWN_BLOCKERS:
        item = by_key.get(key)
        if item is not None and item not in top:
            control = dict(item)
            control["control"] = True
            control_items.append(control)
    sheet_items = top + control_items
    columns = 4
    tile_h = CELL_H + 28
    sheet = Image.new("RGB", (columns * CELL_W, max(1, math.ceil(len(sheet_items) / columns)) * tile_h), (10, 10, 14))
    for index, item in enumerate(sheet_items):
        tile = make_tile(item, item["cell"], item["reduced"], item["skeleton"])
        sheet.paste(tile, ((index % columns) * CELL_W, (index // columns) * tile_h))
    sheet.save(sheet_out, quality=92, subsampling=0)

    known_candidates = []
    for item in top:
        key = f"{item['role']}/{item['row']}/f{item['frame']}"
        if key in KNOWN_BLOCKERS:
            known_candidates.append({
                "role": item["role"],
                "row": item["row"],
                "frame": item["frame"],
                "reason": KNOWN_BLOCKERS[key],
            })

    serializable_top = []
    for item in top:
        serializable_top.append({
            key: value
            for key, value in item.items()
            if key not in {"cell", "reduced", "skeleton"}
        })

    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "supplemental non-generative skeleton, topology, and temporal-residual review of all current v2 atlases; evidence only",
        "method": {
            "name": "downsampled alpha topology and skeleton residual review",
            "steps": [
                "threshold each 192x208 cell at alpha >= 16 and reduce to 96x104",
                "measure connected components, enclosed holes, Euler characteristic, bounding-box fill, and skeleton occupancy",
                "thin the reduced silhouette with Zhang-Suen and count endpoints and branchpoints",
                "compare topology features within each row and calculate circular second-order temporal residuals",
                "render yellow skeletons and red junction markers for the highest-ranked normal-size candidates",
                "treat all outliers as review evidence; promote no hard failure without visual confirmation",
            ],
            "why_complementary": "Topology and skeleton changes can expose duplicated contours, unexpected internal seams, collapsed limbs, or pose-family switches even when bounding boxes and raw pixel residuals remain plausible.",
            "analysis_size": [ANALYSIS_W, ANALYSIS_H],
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": frame_count,
            "circular_frame_transitions": transitions,
            "empty_used_cells": len(ROLES) * len(ROWS) * COLS - frame_count,
        },
        "candidate_counts": {
            "scored_frames": len(scored),
            "visual_sheet_frames": len(top),
            "topology_or_skeleton_outliers": sum(1 for item in scored if float(item["score"]) >= 8.0),
            "known_blocker_candidates": len(known_candidates),
            "known_blocker_controls": len(control_items) + len(known_candidates),
        },
        "top_candidates": serializable_top,
        "known_blocker_candidates": known_candidates,
        "visual_review": {
            "status": "pass_with_four_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
                "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
            ] if args.reviewed else [],
            "note": (
                "Skeleton/topology candidate sheet reviewed at normal display size; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Inspect topology-skeleton-candidates-v1.jpg at normal display size; metrics are candidate evidence only."
            ),
        },
        "formal_assets_modified": False,
        "artifacts": [sheet_out.name, json_out.name],
        "limitations": [
            "The topology is measured on a 96x104 reduced alpha mask, so very thin appendages can merge or disappear and require visual confirmation.",
            "Skeleton branch counts are sensitive to antialiasing and intentional gestures; they never auto-fail a row.",
            "This is an asset-only review and does not replace live Codex App, browser GPU, multi-screen, or bubble-tracking validation.",
        ],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": frame_count, "candidates": len(top)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
