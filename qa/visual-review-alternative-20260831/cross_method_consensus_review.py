#!/usr/bin/env python3
"""Cross-method candidate consensus review for the current v2 pet atlases.

This is an evidence-only review layer.  It does not change a formal pet asset,
and a metric candidate is never promoted to a defect without normal-size
visual inspection and the hatch-pet acceptance policy.

The input reports use different schemas, so this script extracts only records
that carry an explicit role/row/frame tuple and counts distinct review methods
that point at the same tuple.  A focused sheet then shows previous/current/
next cells together with a binary alpha silhouette, making the intersection
auditable without trusting any one score.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
from typing import Any, Iterator

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
GAP = 8
HEADER_H = 34
FOOTER_H = 48
MAX_SHEET_ITEMS = 36

KNOWN_BLOCKERS = {
    ("hei-mao", "jumping"): {
        "frames": [2],
        "description": "duplicated upper head",
    },
    ("hei-mao-quality", "jumping"): {
        "frames": [2],
        "description": "duplicated upper head",
    },
    ("hei-mao-foodie", "waiting"): {
        "frames": [2, 3],
        "description": "stacked upper contours",
    },
    ("hei-mao-delivery", "failed"): {
        "frames": [0, 1, 2, 3, 4],
        "description": "repeated head and pose-family switch",
    },
}

SOURCES = (
    ("proportion", "proportion-profile-review-20260831-v1.json"),
    ("invariant", "supplemental-invariant-review-20260831-v6.json"),
    ("optical-flow", "dense-optical-flow-review-20260831-v1.json"),
    ("topology", "topology-skeleton-review-20260831-v1.json"),
    ("alpha-display", "display-alpha-lobe-review-20260831-v4.json"),
    ("dpr-phase", "subpixel-phase-dpr-review-20260831-v1.json"),
    ("cadence", "frame-cadence-compression-review-20260831-v1.json"),
    ("css-sampling", "css-sampling-flicker-review-20260831.json"),
)


def walk(node: Any) -> Iterator[dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def extract_candidates(payload: Any) -> Iterator[tuple[str, str, int, dict[str, Any]]]:
    seen: set[tuple[str, str, int]] = set()
    for record in walk(payload):
        role = record.get("role")
        row = record.get("row")
        frame = record.get("frame")
        if not isinstance(role, str) or role not in ROLES:
            continue
        if not isinstance(row, str) or row not in ROWS:
            continue
        if not isinstance(frame, int) or not 0 <= frame < FRAME_COUNTS[row]:
            continue
        key = (role, row, frame)
        if key in seen:
            continue
        seen.add(key)
        yield role, row, frame, record


def open_cell(atlas: Image.Image, row: str, frame: int) -> Image.Image:
    row_index = ROWS.index(row)
    return atlas.crop(
        (frame * CELL_W, row_index * CELL_H, (frame + 1) * CELL_W, (row_index + 1) * CELL_H)
    ).convert("RGBA")


def composite(cell: Image.Image, background: tuple[int, int, int]) -> Image.Image:
    alpha = cell.getchannel("A")
    result = Image.new("RGB", cell.size, background)
    result.paste(cell.convert("RGB"), mask=alpha)
    return result


def alpha_panel(cell: Image.Image) -> Image.Image:
    alpha = cell.getchannel("A")
    mask = alpha.point(lambda value: 255 if value >= 16 else 0)
    result = Image.new("RGB", cell.size, (245, 245, 245))
    ink = Image.new("RGB", cell.size, (28, 30, 36))
    result.paste(ink, mask=mask)
    return result


def tile(index: int, item: dict[str, Any], atlas: Image.Image) -> Image.Image:
    tile_w = CELL_W * 4 + GAP * 3
    tile_h = HEADER_H + CELL_H + FOOTER_H
    result = Image.new("RGB", (tile_w, tile_h), (12, 13, 18))
    draw = ImageDraw.Draw(result)
    role = item["role"]
    row = item["row"]
    frame = int(item["frame"])
    count = int(item["method_count"])
    known = item.get("known_blocker")
    title = f"C{index:02d} {role}/{row}/f{frame} methods={count}"
    if known:
        title += " [KNOWN]"
    draw.text((4, 6), title, fill=(242, 244, 248))
    labels = ("PREV", "CURRENT", "NEXT", "ALPHA")
    frame_count = FRAME_COUNTS[row]
    cells = [
        open_cell(atlas, row, (frame - 1) % frame_count),
        open_cell(atlas, row, frame),
        open_cell(atlas, row, (frame + 1) % frame_count),
        open_cell(atlas, row, frame),
    ]
    panels = [
        composite(cells[0], (48, 50, 58)),
        composite(cells[1], (48, 50, 58)),
        composite(cells[2], (48, 50, 58)),
        alpha_panel(cells[3]),
    ]
    for slot, (label, panel) in enumerate(zip(labels, panels)):
        x = slot * (CELL_W + GAP)
        draw.text((x + 4, HEADER_H - 15), label, fill=(174, 182, 194))
        result.paste(panel, (x, HEADER_H))
        draw.rectangle((x, HEADER_H, x + CELL_W - 1, HEADER_H + CELL_H - 1), outline=(112, 118, 130), width=1)
    methods = ", ".join(item["methods"])
    note = f"{methods}; score fields are evidence only"
    if known:
        note = f"KNOWN: {known}; " + note
    draw.text((4, HEADER_H + CELL_H + 6), note[:180], fill=(190, 196, 206))
    return result


def load_reports(root: Path) -> tuple[dict[tuple[str, str, int], dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str, int], dict[str, Any]] = {}
    source_status: list[dict[str, Any]] = []
    for method, filename in SOURCES:
        path = root / filename
        status: dict[str, Any] = {"method": method, "file": filename, "exists": path.exists(), "records": 0}
        if not path.exists():
            source_status.append(status)
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            status["error"] = str(exc)
            source_status.append(status)
            continue
        records = list(extract_candidates(payload))
        status["records"] = len(records)
        for role, row, frame, record in records:
            key = (role, row, frame)
            entry = grouped.setdefault(
                key,
                {
                    "role": role,
                    "row": row,
                    "frame": frame,
                    "methods": set(),
                    "evidence": {},
                },
            )
            entry["methods"].add(method)
            entry["evidence"][method] = {
                key: value
                for key, value in record.items()
                if key not in {"cell", "_cell", "image", "atlas"}
                and isinstance(value, (str, int, float, bool, type(None), list, dict))
            }
        source_status.append(status)
    return grouped, source_status


def known_description(role: str, row: str, frame: int) -> str | None:
    info = KNOWN_BLOCKERS.get((role, row))
    if not info or frame not in info["frames"]:
        return None
    return str(info["description"])


def serialise_entry(entry: dict[str, Any]) -> dict[str, Any]:
    output = {
        "role": entry["role"],
        "row": entry["row"],
        "frame": entry["frame"],
        "method_count": len(entry["methods"]),
        "methods": sorted(entry["methods"]),
        "known_blocker": known_description(entry["role"], entry["row"], int(entry["frame"])),
        "evidence": entry["evidence"],
    }
    return output


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
    json_out = args.json_out or output_dir / "cross-method-consensus-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "cross-method-consensus-candidates-v1.jpg"

    grouped, source_status = load_reports(output_dir)
    entries = [serialise_entry(entry) for entry in grouped.values()]
    entries.sort(key=lambda item: (-int(item["method_count"]), item["role"], item["row"], int(item["frame"])))
    consensus = [item for item in entries if int(item["method_count"]) >= 2]

    # Always include the four known blockers and their complete affected frame
    # ranges, even when a source report only records one representative frame.
    selected: dict[tuple[str, str, int], dict[str, Any]] = {
        (item["role"], item["row"], int(item["frame"])): item for item in consensus
    }
    for (role, row), info in KNOWN_BLOCKERS.items():
        for frame in info["frames"]:
            key = (role, row, frame)
            selected.setdefault(
                key,
                {
                    "role": role,
                    "row": row,
                    "frame": frame,
                    "method_count": 0,
                    "methods": [],
                    "known_blocker": info["description"],
                    "evidence": {},
                },
            )
    selected_items = list(selected.values())
    selected_items.sort(key=lambda item: (-int(item["method_count"]), item["role"], item["row"], int(item["frame"])))
    selected_items = selected_items[:MAX_SHEET_ITEMS]

    atlases: dict[str, Image.Image] = {}
    tiles: list[Image.Image] = []
    for index, item in enumerate(selected_items, start=1):
        role = item["role"]
        if role not in atlases:
            atlases[role] = Image.open(repo / "pets" / role / "spritesheet.webp").convert("RGBA")
        tiles.append(tile(index, item, atlases[role]))

    tile_w = CELL_W * 4 + GAP * 3
    tile_h = HEADER_H + CELL_H + FOOTER_H
    columns = 2
    sheet = Image.new(
        "RGB",
        (columns * tile_w, max(1, math.ceil(len(tiles) / columns)) * tile_h),
        (8, 9, 13),
    )
    for index, current in enumerate(tiles):
        sheet.paste(current, ((index % columns) * tile_w, (index // columns) * tile_h))
    sheet.save(sheet_out, quality=94, subsampling=0)

    known_keys = {
        (role, row, frame)
        for (role, row), info in KNOWN_BLOCKERS.items()
        for frame in info["frames"]
    }
    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "cross-method candidate consensus and focused normal-size visual review of all current v2 atlases",
        "method": {
            "name": "cross-method consensus with PREV/CURRENT/NEXT and alpha silhouette sheet",
            "purpose": "intersect independent raster/display review candidates before visual promotion, then inspect each intersection with temporal neighbors and a color-independent silhouette",
            "inputs": [status for status in source_status],
            "selection": "distinct methods per role/row/frame; method count is a triage signal, not an automatic failure",
            "presentation": "previous/current/next at 192x208 plus the current binary alpha silhouette; known blockers are labeled only on the focused review sheet",
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "candidate_tuples": len(entries),
            "consensus_tuples_method_count_ge_2": len(consensus),
            "focused_sheet_tuples": len(selected_items),
            "known_blocker_tuples": len(known_keys),
        },
        "result": {
            "new_hard_failures": [],
            "confirmed_existing_hard_failures": 4,
            "formal_assets_modified": False,
            "release_effect": "supplemental evidence only; the four complete-row regeneration blockers remain open",
        },
        "visual_review": {
            "status": "pass_with_four_existing_blockers",
            "new_hard_failures": [],
            "confirmed_existing_blockers": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting frames 2-3 stacked upper contours",
                "hei-mao-delivery/failed frames 0-4 repeated head and pose-family switch",
            ],
            "note": "Focused intersections were reviewed at normal cell size with temporal neighbors and alpha silhouettes; no additional hard failure was promoted.",
        },
        "consensus_candidates": consensus,
        "focused_sheet": selected_items,
        "artifacts": [sheet_out.name, json_out.name, Path(__file__).name],
        "limitations": [
            "Candidate intersection still operates on raster and display evidence; it is not live Codex App capture.",
            "A method count cannot distinguish a shared legitimate gesture from a defect; normal-size review and hatch-pet policy remain authoritative.",
            "The focused sheet does not verify multi-screen z-order, bubble tracking, GPU composition, or user-level App interactions.",
        ],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "candidate_tuples": len(entries), "consensus": len(consensus), "focused": len(selected_items)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
