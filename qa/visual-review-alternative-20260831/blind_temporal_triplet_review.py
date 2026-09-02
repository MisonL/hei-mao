#!/usr/bin/env python3
"""Build an anonymous temporal-triplet sheet for independent visual review.

This is an evidence-only method.  It presents previous/current/next frames at
the normal 192x208 cell size without role, row, frame, score, or defect labels.
The hidden answer key keeps provenance and known control samples separate from
the sheet given to a reviewer.  It never changes a formal pet asset.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import random

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
PANEL_GAP = 8
HEADER_H = 28
FOOTER_H = 22
SHEET_COLUMNS = 2
MAX_TRIPLETS = 40
SEED = 20260831

KNOWN_BLOCKERS = {
    ("hei-mao", "jumping", 2): "duplicated upper head",
    ("hei-mao-quality", "jumping", 2): "duplicated upper head",
    ("hei-mao-foodie", "waiting", 2): "stacked upper contours",
    ("hei-mao-foodie", "waiting", 3): "stacked upper contours",
    ("hei-mao-delivery", "failed", 0): "repeated head and pose-family switch",
    ("hei-mao-delivery", "failed", 1): "repeated head and pose-family switch",
    ("hei-mao-delivery", "failed", 2): "repeated head and pose-family switch",
    ("hei-mao-delivery", "failed", 3): "repeated head and pose-family switch",
    ("hei-mao-delivery", "failed", 4): "repeated head and pose-family switch",
}


def open_cell(atlas: Image.Image, row_index: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row_index * CELL_H, (frame + 1) * CELL_W, (row_index + 1) * CELL_H)
    ).convert("RGBA")


def composite(cell: Image.Image, background: tuple[int, int, int] = (46, 48, 56)) -> Image.Image:
    rgba = cell.convert("RGBA")
    alpha = rgba.getchannel("A")
    result = Image.new("RGB", rgba.size, background)
    result.paste(rgba.convert("RGB"), mask=alpha)
    return result


def read_ranked_candidates(root: Path) -> list[tuple[str, str, int, str]]:
    """Read candidate provenance without trusting scores as verdicts."""

    sources = [
        ("proportion-profile-review-20260831-v1.json", "proportion profile"),
        ("supplemental-invariant-review-20260831-v6.json", "invariant profile"),
        ("dense-optical-flow-review-20260831-v1.json", "dense optical flow"),
        ("topology-skeleton-review-20260831-v1.json", "skeleton topology"),
        ("display-alpha-lobe-review-20260831-v4.json", "display alpha lobe"),
        ("subpixel-phase-dpr-review-20260831-v1.json", "DPR phase"),
    ]
    found: list[tuple[str, str, int, str]] = []
    seen: set[tuple[str, str, int]] = set()
    for filename, method in sources:
        path = root / filename
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for item in payload.get("top_candidates", []):
            role = item.get("role")
            row = item.get("row")
            frame = item.get("frame")
            if not isinstance(role, str) or not isinstance(row, str) or not isinstance(frame, int):
                continue
            key = (role, row, frame)
            if role not in ROLES or row not in ROWS or frame < 0 or frame >= USED_FRAMES[row] or key in seen:
                continue
            seen.add(key)
            found.append((role, row, frame, method))
    return found


def choose_triplets(root: Path) -> list[dict]:
    selected: list[dict] = []
    seen: set[tuple[str, str, int]] = set()

    def add(role: str, row: str, frame: int, source: str, control: bool = False) -> None:
        key = (role, row, frame)
        if key in seen or role not in ROLES or row not in ROWS or not (0 <= frame < USED_FRAMES[row]):
            return
        seen.add(key)
        selected.append({"role": role, "row": row, "frame": frame, "source": source, "control": control})

    # Controls are deliberately included to test reviewer sensitivity to the
    # four already confirmed row-level failures, but their labels stay hidden.
    for (role, row, frame), description in KNOWN_BLOCKERS.items():
        add(role, row, frame, f"known control: {description}", control=True)

    # Reserve deterministic, non-control coverage before importing ranked
    # outliers.  This keeps the blind sheet from becoming only a defect sheet
    # and exercises each role plus quiet, directional, gesture, waiting,
    # working, review, and both look loops.
    action_rows = [
        "running-right",
        "running-left",
        "waving",
        "jumping",
        "failed",
        "waiting",
        "running",
        "review",
    ]
    for index, role in enumerate(ROLES):
        add(role, "idle", 0, "stratified blind coverage")
        add(role, "look-row-9", 4, "stratified blind coverage")
        add(role, action_rows[index], 0, "stratified blind coverage")
    add(ROLES[0], "look-row-10", 4, "stratified blind coverage")

    for role, row, frame, source in read_ranked_candidates(root):
        add(role, row, frame, source)
        if len(selected) >= MAX_TRIPLETS:
            break

    # If a source method has too few readable candidates, fill only the
    # remaining slots with a deterministic random sample.
    rng = random.Random(SEED)
    fill_pool = [(role, row, frame) for role in ROLES for row in ROWS for frame in range(USED_FRAMES[row])]
    rng.shuffle(fill_pool)
    for role, row, frame in fill_pool:
        add(role, row, frame, "stratified blind coverage")
        if len(selected) >= MAX_TRIPLETS:
            break

    # Keep a compact sheet while ensuring all roles appear when possible.
    if len(selected) > MAX_TRIPLETS:
        selected = selected[:MAX_TRIPLETS]
    return selected


def make_triplet_tile(index: int, atlas: Image.Image, row_index: int, frame: int, frame_count: int) -> Image.Image:
    tile_w = CELL_W * 3 + PANEL_GAP * 2
    tile_h = HEADER_H + CELL_H + FOOTER_H
    tile = Image.new("RGB", (tile_w, tile_h), (16, 17, 22))
    draw = ImageDraw.Draw(tile)
    draw.text((4, 6), f"T{index:02d}", fill=(242, 244, 248))
    labels = ("PREV", "CURRENT", "NEXT")
    for slot, label in enumerate(labels):
        draw.text((slot * (CELL_W + PANEL_GAP) + 4, HEADER_H - 15), label, fill=(170, 178, 190))
    for slot, relative in enumerate((-1, 0, 1)):
        source_frame = (frame + relative) % frame_count
        cell = composite(open_cell(atlas, row_index, source_frame))
        x = slot * (CELL_W + PANEL_GAP)
        tile.paste(cell, (x, HEADER_H))
        draw.rectangle((x, HEADER_H, x + CELL_W - 1, HEADER_H + CELL_H - 1), outline=(112, 118, 130), width=1)
    draw.text((4, HEADER_H + CELL_H + 5), "judge only visible continuity, identity, and proportion", fill=(180, 186, 196))
    return tile


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--answer-key-out", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or output_dir / "blind-temporal-triplet-review-20260831-v1.json"
    sheet_out = args.sheet_out or output_dir / "blind-temporal-triplet-sheet-v1.png"
    answer_key_out = args.answer_key_out or output_dir / "blind-temporal-triplet-answer-key-v1.json"

    triplets = choose_triplets(output_dir)
    tiles: list[Image.Image] = []
    answer_key: list[dict] = []
    for index, item in enumerate(triplets, start=1):
        atlas_path = repo / "pets" / item["role"] / "spritesheet.webp"
        with Image.open(atlas_path) as opened:
            atlas = opened.convert("RGBA")
        row_index = ROWS.index(item["row"])
        frame_count = USED_FRAMES[item["row"]]
        tiles.append(make_triplet_tile(index, atlas, row_index, item["frame"], frame_count))
        answer_key.append(
            {
                "id": f"T{index:02d}",
                "role": item["role"],
                "row": item["row"],
                "frame": item["frame"],
                "previous": (item["frame"] - 1) % frame_count,
                "next": (item["frame"] + 1) % frame_count,
                "source": item["source"],
                "control": item["control"],
                "control_description": KNOWN_BLOCKERS.get((item["role"], item["row"], item["frame"])),
            }
        )

    tile_w = CELL_W * 3 + PANEL_GAP * 2
    tile_h = HEADER_H + CELL_H + FOOTER_H
    sheet = Image.new(
        "RGB",
        (SHEET_COLUMNS * tile_w, max(1, math.ceil(len(tiles) / SHEET_COLUMNS)) * tile_h),
        (10, 11, 15),
    )
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % SHEET_COLUMNS) * tile_w, (index // SHEET_COLUMNS) * tile_h))
    sheet.save(sheet_out, format="PNG", optimize=True)

    answer_key_payload = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sheet": sheet_out.name,
        "note": "Keep this file away from blind reviewers; it contains role, row, frame, and known-control labels.",
        "triplets": answer_key,
    }
    answer_key_out.write_text(json.dumps(answer_key_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    payload = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "anonymous normal-size temporal-triplet visual review; evidence only",
        "method": {
            "name": "blind previous-current-next triplet review",
            "purpose": "test whether an independent reviewer can see proportion pops, duplicated contours, identity drift, or continuity breaks without metric labels or row semantics",
            "presentation": "three 192x208 panels per triplet on a fixed mid-gray background; only anonymous id and PREV/CURRENT/NEXT labels are visible",
            "selection": "known control samples plus ranked candidates from orthogonal raster methods and deterministic stratified coverage",
            "interpretation": "reviewer verdicts are evidence; no candidate or control is an automatic package failure",
        },
        "coverage": {
            "roles": len({item["role"] for item in triplets}),
            "triplets": len(triplets),
            "frames_shown": len(triplets) * 3,
            "known_controls": sum(1 for item in triplets if item["control"]),
            "normal_cell_size": [CELL_W, CELL_H],
            "random_seed": SEED,
        },
        "artifacts": [sheet_out.name, answer_key_out.name, json_out.name],
        "review_status": "pending_independent_review",
        "formal_assets_modified": False,
        "limitations": [
            "The sheet is still asset-only and cannot prove live Codex App z-order, multi-screen placement, bubble tracking, or platform compositor behavior.",
            "A blind reviewer can identify visible continuity defects but cannot know whether an unusual pose is intentional without the hidden provenance and labeled row context.",
            "Known controls validate sensitivity; passing controls does not prove that every unshown frame is defect-free.",
        ],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "answer_key": str(answer_key_out), "triplets": len(triplets)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
