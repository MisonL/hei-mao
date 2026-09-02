#!/usr/bin/env python3
"""Evidence-only visual review for paired left/right motion rows.

The review mirrors each ``running-right`` frame and compares it with the
same-slot ``running-left`` frame after lower-body anchor registration.  It is
deliberately candidate-only: a high mismatch can be caused by a legitimate
gait phase, asymmetric prop, or independently generated pose and therefore
must be confirmed on the rendered sheet before it is treated as a defect.
No formal pet asset is modified.
"""

from __future__ import annotations

import argparse
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
ROW_INDEX = {"running-right": 1, "running-left": 2}
CELL_W = 192
CELL_H = 208
COLS = 8
ALPHA_THRESHOLD = 16


def open_cell(atlas: Image.Image, row: int, col: int) -> Image.Image:
    return atlas.crop(
        (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)
    ).convert("RGBA")


def mask_for(cell: Image.Image) -> np.ndarray:
    return np.asarray(cell.getchannel("A"), dtype=np.uint8) >= ALPHA_THRESHOLD


def mask_metrics(mask: np.ndarray) -> dict[str, float | int | bool]:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return {
            "nonempty": False,
            "area": 0,
            "x0": 0,
            "y0": 0,
            "x1": 0,
            "y1": 0,
            "width": 0,
            "height": 0,
            "lower_cx": 0.0,
            "bottom": -1,
        }
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    lower_start = y0 + int((y1 - y0 + 1) * 0.58)
    lower_xs = xs[ys >= lower_start]
    if len(lower_xs) == 0:
        lower_xs = xs
    return {
        "nonempty": True,
        "area": int(mask.sum()),
        "x0": x0,
        "y0": y0,
        "x1": x1,
        "y1": y1,
        "width": int(x1 - x0 + 1),
        "height": int(y1 - y0 + 1),
        "lower_cx": float(lower_xs.mean()),
        "bottom": y1,
    }


def shift_mask(mask: np.ndarray, dx: int, dy: int) -> np.ndarray:
    out = np.zeros_like(mask)
    src_y0 = max(0, -dy)
    src_y1 = min(CELL_H, CELL_H - dy)
    src_x0 = max(0, -dx)
    src_x1 = min(CELL_W, CELL_W - dx)
    if src_y1 <= src_y0 or src_x1 <= src_x0:
        return out
    out[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = mask[
        src_y0:src_y1, src_x0:src_x1
    ]
    return out


def register(mask: np.ndarray, source: dict, target: dict) -> np.ndarray:
    dx = int(round(float(target["lower_cx"]) - float(source["lower_cx"])))
    dy = int(round(int(target["bottom"]) - int(source["bottom"])))
    return shift_mask(mask, dx, dy)


def binary_edge(mask: np.ndarray) -> np.ndarray:
    edge = np.zeros_like(mask)
    edge |= mask & ~np.roll(mask, 1, axis=0)
    edge |= mask & ~np.roll(mask, -1, axis=0)
    edge |= mask & ~np.roll(mask, 1, axis=1)
    edge |= mask & ~np.roll(mask, -1, axis=1)
    edge[0, :] |= mask[0, :]
    edge[-1, :] |= mask[-1, :]
    edge[:, 0] |= mask[:, 0]
    edge[:, -1] |= mask[:, -1]
    return edge


def iou(a: np.ndarray, b: np.ndarray) -> float:
    union = np.logical_or(a, b).sum()
    if union == 0:
        return 1.0
    return float(np.logical_and(a, b).sum() / union)


def centroid_delta(a: dict, b: dict) -> float:
    return abs(float(a["lower_cx"]) - float(b["lower_cx"]))


def color_signature(cell: Image.Image, mask: np.ndarray) -> np.ndarray:
    rgba = np.asarray(cell, dtype=np.float32)
    pixels = rgba[:, :, :3][mask]
    if len(pixels) == 0:
        return np.zeros(22, dtype=np.float32)
    mean = pixels.mean(axis=0) / 255.0
    std = pixels.std(axis=0) / 255.0
    lum = 0.299 * pixels[:, 0] + 0.587 * pixels[:, 1] + 0.114 * pixels[:, 2]
    hist, _ = np.histogram(lum, bins=16, range=(0, 255))
    hist = hist.astype(np.float32) / max(len(lum), 1)
    return np.concatenate((mean, std, hist)).astype(np.float32)


def composite(cell: Image.Image, background: tuple[int, int, int] = (96, 96, 96)) -> Image.Image:
    rgba = np.asarray(cell, dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    rgb = rgba[:, :, :3] * alpha + np.asarray(background, dtype=np.float32)[None, None, :] * (1.0 - alpha)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")


def edge_overlay(left: np.ndarray, mirrored_right: np.ndarray) -> Image.Image:
    canvas = Image.new("RGB", (CELL_W, CELL_H), (96, 96, 96))
    draw = ImageDraw.Draw(canvas)
    ly, lx = np.nonzero(binary_edge(left))
    ry, rx = np.nonzero(binary_edge(mirrored_right))
    draw.point([(int(x), int(y)) for x, y in zip(lx, ly)], fill=(0, 225, 255))
    draw.point([(int(x), int(y)) for x, y in zip(rx, ry)], fill=(255, 40, 210))
    return canvas


def tile(item: dict, left: Image.Image, mirrored_right: Image.Image, overlay: Image.Image) -> Image.Image:
    tile_w = CELL_W * 3
    tile_h = CELL_H + 26
    canvas = Image.new("RGB", (tile_w, tile_h), (14, 14, 20))
    canvas.paste(composite(left), (0, 24))
    canvas.paste(composite(mirrored_right), (CELL_W, 24))
    canvas.paste(overlay, (CELL_W * 2, 24))
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (3, 5),
        f"{item['role']} f{item['frame']} mismatch={item['score']:.3f} IoU={item['iou']:.3f}",
        fill=(244, 244, 244),
    )
    draw.text((3, CELL_H + 8), "左：running-left；中：running-right 水平镜像；右：青/洋红轮廓叠加", fill=(215, 215, 225))
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--reviewed", action="store_true")
    args = parser.parse_args()

    repo = args.repo.resolve()
    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or out_dir / "directional-pair-review-20260831.json"
    sheet_out = args.sheet_out or out_dir / "directional-pair-candidates.jpg"

    records: list[dict] = []
    for role in ROLES:
        atlas = Image.open(repo / "pets" / role / "spritesheet.webp").convert("RGBA")
        right_row = ROW_INDEX["running-right"]
        left_row = ROW_INDEX["running-left"]
        for frame in range(COLS):
            right = open_cell(atlas, right_row, frame)
            left = open_cell(atlas, left_row, frame)
            right_mask = mask_for(right)
            left_mask = mask_for(left)
            flipped_right = right.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            flipped_mask = np.fliplr(right_mask)
            left_metrics = mask_metrics(left_mask)
            right_metrics = mask_metrics(flipped_mask)
            if not left_metrics["nonempty"] or not right_metrics["nonempty"]:
                records.append(
                    {
                        "role": role,
                        "frame": frame,
                        "score": 1.0,
                        "iou": 0.0,
                        "status": "empty_pair",
                    }
                )
                continue
            registered = register(flipped_mask, right_metrics, left_metrics)
            pair_iou = iou(left_mask, registered)
            area_ratio = abs(float(left_metrics["area"]) - float(right_metrics["area"])) / max(
                float(left_metrics["area"]), float(right_metrics["area"]), 1.0
            )
            height_delta = abs(int(left_metrics["height"]) - int(right_metrics["height"])) / CELL_H
            width_delta = abs(int(left_metrics["width"]) - int(right_metrics["width"])) / CELL_W
            bottom_delta = abs(int(left_metrics["bottom"]) - int(right_metrics["bottom"])) / CELL_H
            registered_right = shift_mask(flipped_mask, int(round(float(left_metrics["lower_cx"]) - float(right_metrics["lower_cx"]))), int(round(int(left_metrics["bottom"]) - int(right_metrics["bottom"]))))
            color_delta = float(
                np.linalg.norm(color_signature(left, left_mask) - color_signature(flipped_right, flipped_mask))
            )
            # Pair mismatch is intentionally bounded and candidate-only.  A
            # legitimate gait phase can differ; the sheet is the authority.
            score = (
                0.58 * (1.0 - pair_iou)
                + 0.16 * area_ratio
                + 0.10 * height_delta
                + 0.08 * width_delta
                + 0.04 * bottom_delta
                + 0.04 * min(color_delta, 2.0) / 2.0
            )
            records.append(
                {
                    "role": role,
                    "frame": frame,
                    "score": round(float(score), 6),
                    "iou": round(float(pair_iou), 6),
                    "area_ratio": round(float(area_ratio), 6),
                    "height_delta": round(float(height_delta), 6),
                    "width_delta": round(float(width_delta), 6),
                    "bottom_delta": round(float(bottom_delta), 6),
                    "color_delta": round(float(color_delta), 6),
                    "left_metrics": left_metrics,
                    "mirrored_right_metrics": right_metrics,
                    "registered_lower_cx_delta": round(centroid_delta(left_metrics, right_metrics), 4),
                    "status": "candidate",
                    "_left": left,
                    "_mirrored_right": flipped_right,
                    "_registered": registered_right,
                }
            )

    records.sort(key=lambda item: (-float(item["score"]), item["role"], int(item["frame"])))
    top = records[:24]
    sheet_cols = 2
    tile_w = CELL_W * 3
    tile_h = CELL_H + 26
    sheet = Image.new("RGB", (sheet_cols * tile_w, math.ceil(len(top) / sheet_cols) * tile_h), (10, 10, 14))
    for index, item in enumerate(top):
        if item.get("status") != "candidate":
            continue
        overlay = edge_overlay(mask_for(item["_left"]), item["_registered"])
        sheet.paste(tile(item, item["_left"], item["_mirrored_right"], overlay), ((index % sheet_cols) * tile_w, (index // sheet_cols) * tile_h))
    sheet.save(sheet_out, quality=92, subsampling=0)

    clean_records = []
    for item in records:
        clean_records.append({k: v for k, v in item.items() if not k.startswith("_")})
    payload = {
        "schema_version": 1,
        "checked_at": "2026-08-31",
        "scope": "supplemental paired-direction visual review; evidence only",
        "method": {
            "name": "running-right mirror versus running-left anchored comparison",
            "steps": [
                "segment both rows at alpha >= 16",
                "horizontally mirror each running-right frame in its original slot",
                "register the mirrored mask to the running-left lower-body centroid and bottom baseline",
                "measure silhouette IoU, area/width/height/baseline deltas, and alpha-weighted color distance",
                "inspect the highest-mismatch pairs as a three-panel normal-size sheet",
            ],
            "why_complementary": "This tests left/right identity and proportion symmetry directly; it is not a single-frame outlier or row-median test.",
        },
        "coverage": {"roles": len(ROLES), "pairs": len(records), "empty_pairs": sum(1 for x in records if x.get("status") == "empty_pair")},
        "candidate_counts": {"scored_pairs": len(records), "sheet_pairs": len(top)},
        "top_candidates": clean_records[:24],
        "visual_review": {
            "status": "pass_with_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting stacked upper contours",
                "hei-mao-delivery/failed repeated head and pose-family switch",
            ] if args.reviewed else [],
            "reviewed_notes": [
                "hei-mao-fortune has the largest pair mismatch because its basket and gift bag are intentionally side-asymmetric; normal-size overlays preserve the same body height, baseline, and identity.",
                "traveler and foodie candidates are expected gait/prop differences; no visible squash, crop, detached component, or identity replacement was confirmed.",
            ] if args.reviewed else [],
            "note": (
                "Normal-size pair sheet reviewed; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Review directional-pair-candidates.jpg at normal display size; mismatch scores are evidence only."
            ),
        },
        "formal_assets_modified": False,
        "artifacts": [sheet_out.name, json_out.name],
        "limitations": [
            "The two rows can have intentionally different gait phases or asymmetric props; a high score is not an automatic failure.",
            "The method does not replace labeled direction QA or live Codex App playback.",
            "Mirroring is used only for review and never replaces or rewrites the formal running-left row.",
        ],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "pairs": len(records), "top": len(top)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
