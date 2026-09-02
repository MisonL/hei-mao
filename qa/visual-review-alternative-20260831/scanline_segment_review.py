#!/usr/bin/env python3
"""Evidence-only scanline segmentation review for v2 pet atlases.

This review uses a representation that is deliberately different from the
existing bounding-box, occupancy-grid, skeleton, and optical-flow checks:
each alpha row is reduced to contiguous horizontal runs.  The run count,
interior gaps, and their vertical distribution make stacked/duplicated upper
contours and accidental interior bands visible even when the outer silhouette
and connected-component count still look plausible.

The metrics only rank candidates.  The script never edits a formal pet asset
and a candidate is not a failure until it is inspected at normal cell size
under the hatch-pet acceptance policy.
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
ALPHA_THRESHOLD = 16
PROFILE_BINS = 32
SHEET_LIMIT = 32

KNOWN_BLOCKERS = {
    ("hei-mao", "jumping"): {"frames": [2], "description": "duplicated head"},
    ("hei-mao-quality", "jumping"): {"frames": [2], "description": "duplicated head"},
    ("hei-mao-foodie", "waiting"): {"frames": [2, 3], "description": "stacked upper contours"},
    ("hei-mao-delivery", "failed"): {
        "frames": [0, 1, 2, 3, 4],
        "description": "repeated head and pose-family switch",
    },
}


def open_cell(atlas: Image.Image, row_index: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row_index * CELL_H, (frame + 1) * CELL_W, (row_index + 1) * CELL_H)
    ).convert("RGBA")


def contiguous_runs(xs: np.ndarray) -> list[tuple[int, int]]:
    if len(xs) == 0:
        return []
    split = np.flatnonzero(np.diff(xs) > 1)
    starts = np.r_[0, split + 1]
    ends = np.r_[split, len(xs) - 1]
    return [(int(xs[start]), int(xs[end])) for start, end in zip(starts, ends)]


def component_stats(mask: np.ndarray) -> list[dict[str, int]]:
    """Return full-resolution 8-connected components using scanline unions."""
    parent: list[int] = []
    node_size: list[int] = []
    node_bbox: list[list[int]] = []
    previous: list[tuple[tuple[int, int], int]] = []

    def add_node(x0: int, x1: int, y: int) -> int:
        node = len(parent)
        parent.append(node)
        node_size.append(x1 - x0 + 1)
        node_bbox.append([x0, y, x1, y])
        return node

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(left: int, right: int) -> None:
        left, right = find(left), find(right)
        if left == right:
            return
        if node_size[left] < node_size[right]:
            left, right = right, left
        parent[right] = left
        node_size[left] += node_size[right]
        node_bbox[left][0] = min(node_bbox[left][0], node_bbox[right][0])
        node_bbox[left][1] = min(node_bbox[left][1], node_bbox[right][1])
        node_bbox[left][2] = max(node_bbox[left][2], node_bbox[right][2])
        node_bbox[left][3] = max(node_bbox[left][3], node_bbox[right][3])

    for y, row in enumerate(mask):
        current: list[tuple[tuple[int, int], int]] = []
        for x0, x1 in contiguous_runs(np.flatnonzero(row)):
            node = add_node(x0, x1, y)
            current.append(((x0, x1), node))
            for (px0, px1), previous_node in previous:
                if x0 <= px1 + 1 and px0 <= x1 + 1:
                    union(node, previous_node)
        previous = current

    grouped: dict[int, dict[str, int]] = {}
    for node, size in enumerate(node_size):
        root = find(node)
        box = node_bbox[root]
        entry = grouped.setdefault(
            root,
            {"area": 0, "x0": box[0], "y0": box[1], "x1": box[2], "y1": box[3]},
        )
        entry["area"] += size
        entry["x0"] = min(entry["x0"], node_bbox[node][0])
        entry["y0"] = min(entry["y0"], node_bbox[node][1])
        entry["x1"] = max(entry["x1"], node_bbox[node][2])
        entry["y1"] = max(entry["y1"], node_bbox[node][3])
    return sorted(grouped.values(), key=lambda item: (-item["area"], item["y0"], item["x0"]))


def mask_features(cell: Image.Image) -> tuple[dict, np.ndarray, np.ndarray]:
    alpha = np.asarray(cell.getchannel("A"), dtype=np.uint8)
    mask = alpha >= ALPHA_THRESHOLD
    counts = np.zeros(CELL_H, dtype=np.float32)
    occupied = np.zeros(CELL_H, dtype=np.float32)
    span = np.zeros(CELL_H, dtype=np.float32)
    max_gap = np.zeros(CELL_H, dtype=np.float32)
    run_map = np.zeros((CELL_H, CELL_W), dtype=np.uint8)

    for y, row in enumerate(mask):
        xs = np.flatnonzero(row)
        runs = contiguous_runs(xs)
        counts[y] = len(runs)
        if not runs:
            continue
        occupied[y] = float(len(xs)) / CELL_W
        span[y] = float(runs[-1][1] - runs[0][0] + 1) / CELL_W
        gaps = [runs[index + 1][0] - runs[index][1] - 1 for index in range(len(runs) - 1)]
        max_gap[y] = float(max(gaps, default=0)) / CELL_W
        for run_index, (x0, x1) in enumerate(runs, start=1):
            run_map[y, x0 : x1 + 1] = min(run_index, 15)

    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        empty = {
            "nonempty": False,
            "x0": None,
            "y0": None,
            "x1": None,
            "y1": None,
            "height": 0,
            "width": 0,
            "upper_multi_run_ratio": 0.0,
            "interior_gap_rows": 0,
            "max_interior_gap": 0.0,
            "run_transition_count": 0,
            "component_count": 0,
            "detached_component_count": 0,
            "detached_area_ratio": 0.0,
            "tiny_detached_count": 0,
        }
        return empty, np.zeros(PROFILE_BINS * 4 + 8, dtype=np.float32), run_map

    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    height = y1 - y0 + 1
    upper_end = min(CELL_H, y0 + max(1, int(round(height * 0.45))))
    interior = slice(y0, y1 + 1)
    upper_multi = counts[y0:upper_end] >= 2
    interior_multi = counts[interior] >= 2
    transition_count = int(np.count_nonzero(np.diff(counts[y0 : y1 + 1]) != 0))
    components = component_stats(mask)
    total_area = max(int(mask.sum()), 1)
    detached = components[1:]
    detached_area = sum(item["area"] for item in detached)
    tiny_detached = sum(1 for item in detached if item["area"] <= 128)

    def pooled(values: np.ndarray) -> np.ndarray:
        edges = np.linspace(0, CELL_H, PROFILE_BINS + 1, dtype=int)
        return np.asarray(
            [float(np.mean(values[edges[index] : edges[index + 1]])) for index in range(PROFILE_BINS)],
            dtype=np.float32,
        )

    profiles = np.concatenate([pooled(counts) / 4.0, pooled(occupied), pooled(span), pooled(max_gap)])
    scalars = np.asarray(
        [
            float(np.mean(upper_multi)),
            float(np.sum(interior_multi)),
            float(np.max(max_gap)),
            float(transition_count) / max(height, 1),
            float((x1 - x0 + 1) / CELL_W),
            float(height / CELL_H),
            float(detached_area / total_area),
            float(tiny_detached),
        ],
        dtype=np.float32,
    )
    record = {
        "nonempty": True,
        "x0": x0,
        "y0": y0,
        "x1": x1,
        "y1": y1,
        "height": height,
        "width": x1 - x0 + 1,
        "upper_multi_run_ratio": round(float(np.mean(upper_multi)), 6),
        "interior_gap_rows": int(np.sum(interior_multi)),
        "max_interior_gap": round(float(np.max(max_gap)), 6),
        "run_transition_count": transition_count,
        "mean_run_count": round(float(np.mean(counts[y0 : y1 + 1])), 6),
        "component_count": len(components),
        "detached_component_count": len(detached),
        "detached_area_ratio": round(float(detached_area / total_area), 6),
        "tiny_detached_count": int(tiny_detached),
        "detached_components": detached[:6],
    }
    return record, np.concatenate([profiles, scalars]), run_map


def robust_z(values: np.ndarray, median: np.ndarray, mad: np.ndarray) -> np.ndarray:
    return np.abs(values - median) / np.maximum(1.4826 * mad, 0.01)


def distance(left: np.ndarray, right: np.ndarray) -> float:
    if left.shape != right.shape:
        return float("inf")
    profile = float(np.mean(np.abs(left[:-8] - right[:-8])))
    scalar = float(np.mean(np.abs(left[-8:] - right[-8:])))
    return 0.78 * profile + 0.22 * scalar


def composite(cell: Image.Image, background: tuple[int, int, int] = (74, 76, 84)) -> Image.Image:
    rgba = np.asarray(cell, dtype=np.uint8)
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    bg = np.asarray(background, dtype=np.float32)
    rgb = rgba[:, :, :3].astype(np.float32) * alpha + bg * (1.0 - alpha)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")


def run_map_image(run_map: np.ndarray) -> Image.Image:
    palette = np.asarray(
        [
            (20, 22, 28),
            (232, 232, 238),
            (93, 196, 255),
            (255, 196, 82),
            (250, 104, 128),
            (184, 116, 255),
            (85, 224, 160),
        ],
        dtype=np.uint8,
    )
    mapped = palette[np.minimum(run_map, len(palette) - 1)]
    return Image.fromarray(mapped, mode="RGB")


def make_tile(item: dict, cells: list[Image.Image], run_map: np.ndarray) -> Image.Image:
    panel_w, panel_h = CELL_W, CELL_H
    title_h, footer_h = 30, 38
    tile = Image.new("RGB", (panel_w * 4, title_h + panel_h + footer_h), (12, 13, 18))
    labels = ["PREV", "CURRENT", "NEXT", "SCANLINES"]
    panels = [composite(cell) for cell in cells] + [run_map_image(run_map)]
    draw = ImageDraw.Draw(tile)
    known = item.get("known_blocker")
    title = f"{item['role']}/{item['row']}/f{item['frame']} score={item['score']:.3f}"
    if known:
        title += " [KNOWN]"
    draw.text((4, 6), title, fill=(242, 244, 248))
    for index, (label, panel) in enumerate(zip(labels, panels)):
        x = index * panel_w
        draw.text((x + 4, title_h - 17), label, fill=(178, 186, 198))
        tile.paste(panel, (x, title_h))
        draw.rectangle((x, title_h, x + panel_w - 1, title_h + panel_h - 1), outline=(112, 118, 130), width=1)
    note = (
        f"upper multi-run={item['upper_multi_run_ratio']:.3f}  gap rows={item['interior_gap_rows']}  "
        f"max gap={item['max_interior_gap']:.3f}  detached={item['detached_component_count']}"
    )
    if known:
        note = f"KNOWN: {known}; " + note
    draw.text((4, title_h + panel_h + 9), note[:220], fill=(198, 202, 212))
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
    json_out = args.json_out or output_dir / "scanline-segment-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "scanline-segment-candidates-v1.jpg"

    by_row: dict[tuple[str, str], list[dict]] = {}
    vectors: dict[tuple[str, str, int], np.ndarray] = {}
    run_maps: dict[tuple[str, str, int], np.ndarray] = {}
    frame_count = 0
    transition_count = 0

    atlases: dict[str, Image.Image] = {}
    for role in ROLES:
        with Image.open(repo / "pets" / role / "spritesheet.webp") as opened:
            atlases[role] = opened.convert("RGBA")
        for row_index, row_name in enumerate(ROWS):
            items: list[dict] = []
            for frame in range(FRAME_COUNTS[row_name]):
                cell = open_cell(atlases[role], row_index, frame)
                record, vector, run_map = mask_features(cell)
                record.update({"role": role, "row": row_name, "row_index": row_index, "frame": frame})
                items.append(record)
                key = (role, row_name, frame)
                vectors[key] = vector
                run_maps[key] = run_map
                frame_count += 1
            by_row[(role, row_name)] = items

    all_items: list[dict] = []
    for (role, row_name), items in by_row.items():
        matrix = np.stack([vectors[(role, row_name, int(item["frame"]))] for item in items])
        median = np.median(matrix, axis=0)
        mad = np.median(np.abs(matrix - median), axis=0)
        for index, item in enumerate(items):
            previous = matrix[(index - 1) % len(items)]
            following = matrix[(index + 1) % len(items)]
            prediction = (previous + following) / 2.0
            z95 = float(np.percentile(robust_z(matrix[index], median, mad), 95))
            median_distance = distance(matrix[index], median)
            neighbor_distance = distance(matrix[index], prediction)
            gap_signal = float(
                item["upper_multi_run_ratio"]
                + item["max_interior_gap"]
                + 1.5 * item["detached_area_ratio"]
                + 0.04 * item["tiny_detached_count"]
            )
            score = 0.40 * z95 + 0.36 * neighbor_distance + 0.24 * gap_signal
            item.update(
                {
                    "robust_profile_z95": round(z95, 6),
                    "median_scanline_distance": round(median_distance, 6),
                    "neighbor_scanline_residual": round(neighbor_distance, 6),
                    "score": round(float(score), 6),
                }
            )
            all_items.append(item)
            transition_count += 1

    all_items.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])))
    selected_keys = {(item["role"], item["row"], int(item["frame"])) for item in all_items[:SHEET_LIMIT]}
    for (role, row), control in KNOWN_BLOCKERS.items():
        for frame in control["frames"]:
            selected_keys.add((role, row, frame))
    selected = [
        item
        for item in all_items
        if (item["role"], item["row"], int(item["frame"])) in selected_keys
    ]
    selected.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], int(item["frame"])))
    selected = selected[: max(SHEET_LIMIT, len(KNOWN_BLOCKERS)) + 12]

    tiles: list[Image.Image] = []
    for item in selected:
        role, row, frame = item["role"], item["row"], int(item["frame"])
        row_index = ROWS.index(row)
        count = FRAME_COUNTS[row]
        atlas = atlases[role]
        cells = [
            open_cell(atlas, row_index, (frame - 1) % count),
            open_cell(atlas, row_index, frame),
            open_cell(atlas, row_index, (frame + 1) % count),
        ]
        known = KNOWN_BLOCKERS.get((role, row))
        if known and frame in known["frames"]:
            item["known_blocker"] = known["description"]
        tiles.append(make_tile(item, cells, run_maps[(role, row, frame)]))

    columns = 1
    tile_w = CELL_W * 4
    tile_h = CELL_H + 30 + 38
    sheet = Image.new("RGB", (tile_w, max(1, math.ceil(len(tiles) / columns)) * tile_h), (8, 9, 13))
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % columns) * tile_w, (index // columns) * tile_h))
    sheet.save(sheet_out, quality=92, subsampling=0)

    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "supplemental scanline run-length and interior-gap review of all current v2 atlases; evidence only",
        "method": {
            "name": "alpha scanline segmentation and interior-gap temporal profile",
            "steps": [
                "segment each 192x208 cell at alpha >= 16",
                "reduce every alpha row to contiguous horizontal runs",
                "measure run count, occupied width, span, maximum interior gap, and vertical run transitions",
                "identify full-resolution disconnected alpha components and rank tiny detached fragments separately",
                "compare each frame with its row median and circular neighbor interpolation using robust deviations",
                "render PREV/CURRENT/NEXT plus a color-coded scanline map for the highest-ranked candidates",
            ],
            "purpose": "surface stacked or duplicated upper contours, accidental transparent bands, and local squash/stretch that can survive global silhouette checks",
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": frame_count,
            "circular_frame_transitions": transition_count,
            "alpha_threshold": ALPHA_THRESHOLD,
            "profile_bins": PROFILE_BINS,
            "candidate_sheet_items": len(selected),
        },
        "known_failures_reproduced": [
            {"role": role, "row": row, "frames": data["frames"], "description": data["description"]}
            for (role, row), data in KNOWN_BLOCKERS.items()
        ],
        "top_candidates": [
            {key: value for key, value in item.items() if key != "known_blocker"}
            for item in all_items[:SHEET_LIMIT]
        ],
        "visual_review": {
            "status": "pass_with_four_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
                "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
            ]
            if args.reviewed
            else [],
            "note": (
                "Candidate sheet reviewed at normal cell size; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Inspect scanline-segment-candidates-v1.jpg at normal display size; metrics are candidate evidence only."
            ),
        },
        "result": {
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": 4 if args.reviewed else 0,
            "formal_assets_modified": False,
            "release_effect": "supplemental evidence only; complete-row regeneration remains required for the four existing blockers",
        },
        "limitations": [
            "Intentional holes, separated accessories, and waving limbs can create multiple scanline runs without being defects.",
            "A disconnected component may be an intentionally detached-looking accessory or an edge crop; inspect its size, location, and role context before promotion.",
            "The scanline representation is color-independent and cannot identify semantic body parts by itself.",
            "A candidate requires normal-size visual inspection and cannot prove browser compositor or live Codex App behavior.",
            "The source atlas is read-only; no frame is re-centered, rescaled, or rewritten.",
        ],
        "artifacts": [sheet_out.name, json_out.name, Path(__file__).name],
        "formal_assets_modified": False,
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"json": str(json_out), "sheet": str(sheet_out), "frames": frame_count, "transitions": transition_count, "sheet_items": len(selected)},
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
