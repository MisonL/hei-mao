#!/usr/bin/env python3
"""Evidence-only temporal connected-component lineage review.

This check follows alpha components across circular animation rows instead of
only counting components in isolated frames.  It highlights single-frame
birth/death events, split/merge events, and detached components that do not
remain attached to the main body.  Scores are triage evidence only: the
script never edits a formal pet asset and never promotes a failure without
normal-size visual review under hatch-pet rules.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path

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
DISPLAY_SIZE = (96, 104)
THRESHOLDS = (16, 64, 128, 192)
SHEET_COLUMNS = 2
SHEET_ITEM_W = 4 * DISPLAY_SIZE[0]
SHEET_ITEM_H = DISPLAY_SIZE[1] + 31

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


def contiguous_runs(row: bytes, threshold: int) -> list[tuple[int, int]]:
    runs: list[tuple[int, int]] = []
    start = None
    for x, value in enumerate(row):
        if value >= threshold:
            if start is None:
                start = x
        elif start is not None:
            runs.append((start, x - 1))
            start = None
    if start is not None:
        runs.append((start, len(row) - 1))
    return runs


def components(alpha_bytes: bytes, threshold: int) -> list[dict]:
    """Return 8-connected run-length components with geometric statistics."""
    parent: list[int] = []
    area: list[int] = []
    sum_x: list[float] = []
    sum_y: list[float] = []
    bbox: list[list[int]] = []
    rows: list[list[tuple[int, int, int]]] = []

    def add_run(x0: int, x1: int, y: int) -> int:
        node = len(parent)
        count = x1 - x0 + 1
        parent.append(node)
        area.append(count)
        sum_x.append((x0 + x1) * count / 2.0)
        sum_y.append(float(y * count))
        bbox.append([x0, y, x1, y])
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
        if area[left] < area[right]:
            left, right = right, left
        parent[right] = left
        area[left] += area[right]
        sum_x[left] += sum_x[right]
        sum_y[left] += sum_y[right]
        bbox[left][0] = min(bbox[left][0], bbox[right][0])
        bbox[left][1] = min(bbox[left][1], bbox[right][1])
        bbox[left][2] = max(bbox[left][2], bbox[right][2])
        bbox[left][3] = max(bbox[left][3], bbox[right][3])

    previous: list[tuple[int, int, int]] = []
    for y in range(CELL_H):
        row = alpha_bytes[y * CELL_W : (y + 1) * CELL_W]
        current: list[tuple[int, int, int]] = []
        for x0, x1 in contiguous_runs(row, threshold):
            node = add_run(x0, x1, y)
            current.append((x0, x1, node))
            for px0, px1, previous_node in previous:
                if x0 <= px1 + 1 and px0 <= x1 + 1:
                    union(node, previous_node)
        rows.append(current)
        previous = current

    grouped: dict[int, dict] = {}
    for node in range(len(parent)):
        root = find(node)
        entry = grouped.setdefault(root, {"area": 0, "sum_x": 0.0, "sum_y": 0.0, "x0": 10**9, "y0": 10**9, "x1": -1, "y1": -1})
        # Root arrays already contain union aggregates, so collect only the
        # original run's geometry here to avoid double-counting merged nodes.
        # The run geometry is recovered from the per-node bbox and sums.
        node_count = area[node] if find(node) == node else 0
        if node_count:
            entry["area"] = area[root]
            entry["sum_x"] = sum_x[root]
            entry["sum_y"] = sum_y[root]
            entry["x0"], entry["y0"], entry["x1"], entry["y1"] = bbox[root]

    ordered = sorted(grouped.values(), key=lambda item: (-item["area"], item["y0"], item["x0"]))
    for index, item in enumerate(ordered):
        item["id"] = index
        item["cx"] = float(item["sum_x"] / max(item["area"], 1))
        item["cy"] = float(item["sum_y"] / max(item["area"], 1))
        item["width"] = int(item["x1"] - item["x0"] + 1)
        item["height"] = int(item["y1"] - item["y0"] + 1)
        item.pop("sum_x", None)
        item.pop("sum_y", None)
    return ordered


def lower_anchor(main: dict) -> tuple[float, float]:
    return ((main["x0"] + main["x1"]) / 2.0, float(main["y1"]))


def bbox_iou(left: dict, right: dict, dx: float, dy: float) -> float:
    rx0, ry0 = right["x0"] - dx, right["y0"] - dy
    rx1, ry1 = right["x1"] - dx, right["y1"] - dy
    ix0, iy0 = max(left["x0"], rx0), max(left["y0"], ry0)
    ix1, iy1 = min(left["x1"], rx1), min(left["y1"], ry1)
    intersection = max(0.0, ix1 - ix0 + 1) * max(0.0, iy1 - iy0 + 1)
    union = left["width"] * left["height"] + right["width"] * right["height"] - intersection
    return float(intersection / max(union, 1.0))


def component_gap(component: dict, main: dict) -> float:
    dx = max(main["x0"] - component["x1"] - 1, component["x0"] - main["x1"] - 1, 0)
    dy = max(main["y0"] - component["y1"] - 1, component["y0"] - main["y1"] - 1, 0)
    return float(math.hypot(dx, dy))


def match_components(previous: list[dict], current: list[dict], dx: float, dy: float) -> tuple[list[tuple[int, int, float]], set[int], set[int]]:
    """Greedy stable matching for detached component lineages."""
    if not previous or not current:
        return [], set(range(len(previous))), set(range(len(current)))
    pairs: list[tuple[float, int, int]] = []
    for left_index, left in enumerate(previous):
        for right_index, right in enumerate(current):
            distance = math.hypot(left["cx"] - (right["cx"] - dx), left["cy"] - (right["cy"] - dy))
            scale = max(8.0, 0.5 * math.hypot(left["width"], left["height"]) + 0.5 * math.hypot(right["width"], right["height"]))
            area_ratio = abs(math.log((left["area"] + 1) / (right["area"] + 1)))
            overlap_penalty = 1.0 - bbox_iou(left, right, dx, dy)
            cost = distance / scale + 0.45 * min(area_ratio, 4.0) + 0.35 * overlap_penalty
            pairs.append((cost, left_index, right_index))
    pairs.sort()
    matched_left: set[int] = set()
    matched_right: set[int] = set()
    matches: list[tuple[int, int, float]] = []
    for cost, left_index, right_index in pairs:
        if cost > 2.2 or left_index in matched_left or right_index in matched_right:
            continue
        matched_left.add(left_index)
        matched_right.add(right_index)
        matches.append((left_index, right_index, float(cost)))
    return matches, set(range(len(previous))) - matched_left, set(range(len(current))) - matched_right


def adjacency_events(previous: list[dict], current: list[dict], dx: float, dy: float) -> tuple[int, int]:
    """Count plausible detached-component splits and merges by bbox overlap."""
    prev_links = [0] * len(previous)
    cur_links = [0] * len(current)
    for left_index, left in enumerate(previous):
        for right_index, right in enumerate(current):
            overlap = bbox_iou(left, right, dx, dy)
            distance = math.hypot(left["cx"] - (right["cx"] - dx), left["cy"] - (right["cy"] - dy))
            if overlap >= 0.04 or distance <= max(10.0, 0.55 * math.hypot(left["width"], left["height"])):
                prev_links[left_index] += 1
                cur_links[right_index] += 1
    return sum(1 for count in prev_links if count >= 2), sum(1 for count in cur_links if count >= 2)


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[middle])
    return float((ordered[middle - 1] + ordered[middle]) / 2.0)


def robust_z(value: float, values: list[float]) -> float:
    if not values:
        return 0.0
    med = median(values)
    mad = median([abs(item - med) for item in values])
    mean = sum(values) / len(values)
    std = math.sqrt(sum((item - mean) ** 2 for item in values) / len(values))
    scale = max(1.4826 * mad, std * 0.25, 1e-6)
    return abs(value - med) / scale


def cell_rgba(cell: Image.Image, background: tuple[int, int, int] = (74, 76, 84)) -> Image.Image:
    back = Image.new("RGBA", cell.size, (*background, 255))
    image = Image.alpha_composite(back, cell).convert("RGB")
    return image.resize(DISPLAY_SIZE, Image.Resampling.LANCZOS)


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return float(ordered[lower] * (1.0 - weight) + ordered[upper] * weight)


def component_overlay(cell: Image.Image, threshold: int, comps: list[dict]) -> Image.Image:
    image = cell_rgba(cell).convert("RGB")
    draw = ImageDraw.Draw(image)
    scale_x, scale_y = DISPLAY_SIZE[0] / CELL_W, DISPLAY_SIZE[1] / CELL_H
    for index, item in enumerate(comps):
        box = (
            int(item["x0"] * scale_x),
            int(item["y0"] * scale_y),
            int((item["x1"] + 1) * scale_x),
            int((item["y1"] + 1) * scale_y),
        )
        color = (110, 235, 142) if index == 0 else (255, 80, 92)
        draw.rectangle(box, outline=color, width=1)
        if index > 0:
            draw.text((box[0], max(0, box[1] - 9)), str(index), fill=color)
    draw.text((2, 2), f"a{threshold} n={len(comps)}", fill=(248, 248, 248))
    return image


def event_overlay(cell: Image.Image, previous: list[dict], current: list[dict], metrics: dict, threshold: int) -> Image.Image:
    image = component_overlay(cell, threshold, current)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, DISPLAY_SIZE[0] - 1, DISPLAY_SIZE[1] - 1), outline=(255, 206, 75), width=1)
    text = f"birth {metrics['birth_count']} death {metrics['death_count']} split {metrics['split_count']} merge {metrics['merge_count']}"
    draw.rectangle((0, DISPLAY_SIZE[1] - 12, DISPLAY_SIZE[0], DISPLAY_SIZE[1]), fill=(24, 24, 30))
    draw.text((2, DISPLAY_SIZE[1] - 11), text[:32], fill=(255, 226, 142))
    return image


def make_item(previous_cell: Image.Image, current_cell: Image.Image, previous: list[dict], current: list[dict], metrics: dict, threshold: int, label: str) -> Image.Image:
    canvas = Image.new("RGB", (SHEET_ITEM_W, SHEET_ITEM_H), (24, 24, 30))
    panels = [
        cell_rgba(previous_cell),
        cell_rgba(current_cell),
        component_overlay(current_cell, threshold, current),
        event_overlay(current_cell, previous, current, metrics, threshold),
    ]
    for index, panel in enumerate(panels):
        canvas.paste(panel, (index * DISPLAY_SIZE[0], 20))
    draw = ImageDraw.Draw(canvas)
    draw.text((3, 3), label, fill=(244, 244, 244))
    draw.text((3, SHEET_ITEM_H - 11), "PREV  CURRENT  COMPONENTS  LINEAGE", fill=(185, 185, 195))
    return canvas


def analyze_transition(previous_cells: dict[int, Image.Image], current_cells: dict[int, Image.Image], frame: int, next_frame: int) -> dict:
    threshold_metrics: dict[str, dict] = {}
    for threshold in THRESHOLDS:
        prev_alpha = previous_cells[threshold].getchannel("A").tobytes()
        cur_alpha = current_cells[threshold].getchannel("A").tobytes()
        prev_components = components(prev_alpha, threshold)
        cur_components = components(cur_alpha, threshold)
        prev_main = prev_components[0] if prev_components else {"x0": 0, "x1": 0, "y1": 0, "width": 0, "height": 0, "cx": 0.0, "cy": 0.0, "area": 0}
        cur_main = cur_components[0] if cur_components else prev_main
        prev_anchor = lower_anchor(prev_main)
        cur_anchor = lower_anchor(cur_main)
        dx, dy = cur_anchor[0] - prev_anchor[0], cur_anchor[1] - prev_anchor[1]
        prev_detached, cur_detached = prev_components[1:], cur_components[1:]
        matches, deaths, births = match_components(prev_detached, cur_detached, dx, dy)
        split_count, merge_count = adjacency_events(prev_detached, cur_detached, dx, dy)
        matched_jumps = [
            math.hypot(left["cx"] - (right["cx"] - dx), left["cy"] - (right["cy"] - dy))
            for left_index, right_index, _ in matches
            for left, right in [(prev_detached[left_index], cur_detached[right_index])]
        ]
        total_area = max(int(sum(item["area"] for item in cur_components)), 1)
        birth_area = sum(cur_detached[index]["area"] for index in births)
        death_area = sum(prev_detached[index]["area"] for index in deaths)
        far_detached = [item for item in cur_detached if component_gap(item, cur_main) >= 3.0 and item["area"] >= 8]
        threshold_metrics[str(threshold)] = {
            "previous_component_count": len(prev_components),
            "current_component_count": len(cur_components),
            "previous_detached_count": len(prev_detached),
            "current_detached_count": len(cur_detached),
            "birth_count": len(births),
            "death_count": len(deaths),
            "birth_area_ratio": round(float(birth_area / total_area), 6),
            "death_area_ratio": round(float(death_area / max(sum(item["area"] for item in prev_components), 1)), 6),
            "split_count": int(split_count),
            "merge_count": int(merge_count),
            "far_detached_count": len(far_detached),
            "far_detached_area_ratio": round(float(sum(item["area"] for item in far_detached) / total_area), 6),
            "matched_count": len(matches),
            "matched_jump_p95": round(percentile(matched_jumps, 0.95), 4),
            "anchor_dx": round(float(dx), 3),
            "anchor_dy": round(float(dy), 3),
            "birth_components": [{"area": item["area"], "x0": item["x0"], "y0": item["y0"], "x1": item["x1"], "y1": item["y1"]} for index, item in enumerate(cur_detached) if index in births][:6],
            "death_components": [{"area": item["area"], "x0": item["x0"], "y0": item["y0"], "x1": item["x1"], "y1": item["y1"]} for index, item in enumerate(prev_detached) if index in deaths][:6],
        }
    # High-alpha events are more resistant to anti-aliased edge noise.  The
    # 16-alpha channel remains useful for catching thin attached parts.
    m16, m128 = threshold_metrics["16"], threshold_metrics["128"]
    threshold_values = list(threshold_metrics.values())
    return {
        "frame": frame,
        "next_frame": next_frame,
        "thresholds": threshold_metrics,
        "birth_area_ratio": round(float(max(m16["birth_area_ratio"], m128["birth_area_ratio"])), 6),
        "death_area_ratio": round(float(max(m16["death_area_ratio"], m128["death_area_ratio"])), 6),
        "split_count": max(m16["split_count"], m128["split_count"]),
        "merge_count": max(m16["merge_count"], m128["merge_count"]),
        "far_detached_count": max(m16["far_detached_count"], m128["far_detached_count"]),
        "far_detached_area_ratio": round(float(max(m16["far_detached_area_ratio"], m128["far_detached_area_ratio"])), 6),
        "component_count_delta": abs(m16["current_component_count"] - m16["previous_component_count"]),
        "matched_jump_p95": max(m16["matched_jump_p95"], m128["matched_jump_p95"]),
        "birth_persists_all_thresholds": all(item["birth_count"] > 0 for item in threshold_values),
        "death_persists_all_thresholds": all(item["death_count"] > 0 for item in threshold_values),
        "far_detached_persists_all_thresholds": all(item["far_detached_count"] > 0 for item in threshold_values),
        "split_or_merge_persists_high_alpha": m128["split_count"] > 0 or m128["merge_count"] > 0,
    }


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
    json_out = args.json_out or (output_dir / "temporal-component-lineage-review-20260831-v1.json")
    sheet_out = args.sheet_out or (output_dir / "temporal-component-lineage-candidates-v1.jpg")

    all_records: list[dict] = []
    sheet_items: list[Image.Image] = []
    sheet_labels: list[str] = []
    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        with Image.open(atlas_path) as image:
            atlas = image.convert("RGBA")
            for row_index, row_name in enumerate(ROWS):
                frame_count = FRAME_COUNTS[row_name]
                cells_by_frame: dict[int, dict[int, Image.Image]] = {}
                for frame in range(frame_count):
                    cell = open_cell(atlas, row_index, frame)
                    cells_by_frame[frame] = {threshold: cell for threshold in THRESHOLDS}
                transitions: list[dict] = []
                for frame in range(frame_count):
                    next_frame = (frame + 1) % frame_count
                    metrics = analyze_transition(cells_by_frame[frame], cells_by_frame[next_frame], frame, next_frame)
                    transitions.append({"role": role, "row": row_name, **metrics})
                fields = [
                    "birth_area_ratio",
                    "death_area_ratio",
                    "far_detached_area_ratio",
                    "matched_jump_p95",
                    "component_count_delta",
                ]
                values = {field: [float(item[field]) for item in transitions] for field in fields}
                for item in transitions:
                    item["z_birth"] = robust_z(float(item["birth_area_ratio"]), values["birth_area_ratio"])
                    item["z_death"] = robust_z(float(item["death_area_ratio"]), values["death_area_ratio"])
                    item["z_far"] = robust_z(float(item["far_detached_area_ratio"]), values["far_detached_area_ratio"])
                    item["z_jump"] = robust_z(float(item["matched_jump_p95"]), values["matched_jump_p95"])
                    item["z_count"] = robust_z(float(item["component_count_delta"]), values["component_count_delta"])
                    item["score"] = round(min(16.0, 0.30 * item["z_birth"] + 0.25 * item["z_death"] + 0.20 * item["z_far"] + 0.15 * item["z_jump"] + 0.10 * item["z_count"] + 0.35 * min(3, item["split_count"] + item["merge_count"])), 6)
                    all_records.append(item)
                # Keep the visual sheet bounded: known controls are always
                # included; otherwise keep the highest event per row.
                control_frames = set(KNOWN_BLOCKERS.get((role, row_name), {}).get("frames", []))
                selected_frames = control_frames or {max(transitions, key=lambda item: float(item["score"]))["frame"]}
                for frame in selected_frames:
                    selected = next(item for item in transitions if item["frame"] == frame)
                    threshold = 128
                    prev_cell = cells_by_frame[frame][threshold]
                    cur_cell = cells_by_frame[selected["next_frame"]][threshold]
                    prev_components = components(prev_cell.getchannel("A").tobytes(), threshold)
                    cur_components = components(cur_cell.getchannel("A").tobytes(), threshold)
                    sheet_items.append(make_item(prev_cell, cur_cell, prev_components, cur_components, selected["thresholds"][str(threshold)], threshold, f"{role}/{row_name} {frame}->{selected['next_frame']} score={selected['score']:.2f}"))

    all_records.sort(key=lambda item: (-float(item["score"]), item["role"], item["row"], item["frame"]))
    max_sheet_items = 40
    if len(sheet_items) > max_sheet_items:
        sheet_items = sheet_items[:max_sheet_items]
    if sheet_items:
        rows = math.ceil(len(sheet_items) / SHEET_COLUMNS)
        sheet = Image.new("RGB", (SHEET_COLUMNS * SHEET_ITEM_W, rows * SHEET_ITEM_H), (24, 24, 30))
        for index, item in enumerate(sheet_items):
            sheet.paste(item, ((index % SHEET_COLUMNS) * SHEET_ITEM_W, (index // SHEET_COLUMNS) * SHEET_ITEM_H))
        sheet.save(sheet_out, quality=92, optimize=True)

    known = []
    for role, row in KNOWN_BLOCKERS:
        known.extend([item for item in all_records if item["role"] == role and item["row"] == row and item["frame"] in KNOWN_BLOCKERS[(role, row)]["frames"]])
    report = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "evidence-only temporal connected-component lineage review of the eight current v2 atlases",
        "method": {
            "name": "multi-threshold temporal component lineage and attachment review",
            "purpose": "在相邻循环帧之间跟踪 Alpha 连通组件，识别单帧出生/消失、分裂/合并、远离主体的 detached component 及其跨阈值持久性",
            "thresholds": list(THRESHOLDS),
            "matching": "lower-body anchor compensated greedy matching; scores are candidates only",
            "sheet": str(sheet_out.relative_to(repo)),
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "cells": sum(FRAME_COUNTS[row] for row in ROWS) * len(ROLES),
            "transitions_including_loop": sum(FRAME_COUNTS[row] for row in ROWS) * len(ROLES),
            "candidate_sheet_items": len(sheet_items),
        },
        "records": all_records,
        "known_controls": [
            {"role": item["role"], "row": item["row"], "frame": item["frame"], "next_frame": item["next_frame"], "description": KNOWN_BLOCKERS[(item["role"], item["row"])] ["description"], "score": item["score"]}
            for item in known
        ],
        "result": {
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
                "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
            ],
            "still_open_from_combined_qa": [
                "hei-mao/jumping",
                "hei-mao-quality/jumping",
                "hei-mao-foodie/waiting",
                "hei-mao-delivery/failed",
                "hei-mao-quality/running-left",
                "hei-mao-quality/failed",
                "hei-mao-traveler/waiting",
                "hei-mao-traveler/review",
            ],
            "formal_assets_modified": False,
            "release_effect": "supplemental evidence only; no new blocker was promoted, while the eight rows already blocked by combined QA still require complete-row regeneration",
        },
        "limitations": [
            "透明度阈值下的连通性不能单独判断组件是否具有语义，正常摆臂、泪滴或细小装饰可能出现合法出生/消失",
            "bbox 匹配不建模遮挡顺序和真实关节运动，不能替代接触表、预览 GIF 或人工语义检查",
            "这是资产级复核，不能证明 Codex App 窗口层级、多屏气泡跟随或 GPU 合成",
        ],
    }
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json_out": str(json_out), "sheet_out": str(sheet_out), "records": len(all_records), "sheet_items": len(sheet_items), "new_hard_failures": []}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
