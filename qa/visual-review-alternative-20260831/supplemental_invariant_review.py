#!/usr/bin/env python3
"""Supplemental invariant visual review for the current hei-mao v2 atlases.

This is evidence generation only. It never changes a formal pet asset.
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
THRESHOLD = 16


def robust_z(value: float, values: np.ndarray, floor: float = 1e-6) -> float:
    med = float(np.median(values))
    mad = float(np.median(np.abs(values - med)))
    if mad == 0.0 and np.allclose(values, med):
        return 0.0
    # A one-pixel change in a constant-height row is meaningful, but it
    # should not become an unbounded score simply because MAD is zero.
    scale = max(1.4826 * mad, float(np.std(values)) * 0.25, floor)
    return abs(value - med) / scale


def resize_vector(values: np.ndarray, size: int) -> np.ndarray:
    if values.size == 0:
        return np.zeros(size, dtype=np.float32)
    source = np.linspace(0.0, 1.0, values.size)
    target = np.linspace(0.0, 1.0, size)
    return np.interp(target, source, values).astype(np.float32)


def open_cell(atlas: Image.Image, row: int, col: int) -> Image.Image:
    return atlas.crop((col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)).convert("RGBA")


def mask_for(cell: Image.Image) -> np.ndarray:
    return np.asarray(cell.getchannel("A"), dtype=np.uint8) >= THRESHOLD


def mask_metrics(mask: np.ndarray) -> dict[str, float | int | list[int] | bool]:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return {
            "nonempty": False,
            "area": 0,
            "bbox": [0, 0, 0, 0],
            "width": 0,
            "height": 0,
            "aspect": 0.0,
            "cx": 0.0,
            "cy": 0.0,
            "bottom": -1,
            "lower_cx": 0.0,
        }
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    lower = ys >= max(y0, y0 + int((y1 - y0 + 1) * 0.58))
    lower_x = xs[lower] if np.any(lower) else xs
    return {
        "nonempty": True,
        "area": int(mask.sum()),
        "bbox": [x0, y0, x1, y1],
        "width": int(x1 - x0 + 1),
        "height": int(y1 - y0 + 1),
        "aspect": float((x1 - x0 + 1) / max(y1 - y0 + 1, 1)),
        "cx": float(xs.mean()),
        "cy": float(ys.mean()),
        "bottom": int(y1),
        "lower_cx": float(lower_x.mean()),
    }


def profile_vectors(mask: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    height_profile = mask.sum(axis=1).astype(np.float32) / CELL_W
    width_profile = mask.sum(axis=0).astype(np.float32) / CELL_H
    top = mask[: int(CELL_H * 0.46)]
    top_profile = top.sum(axis=1).astype(np.float32) / CELL_W
    return (
        resize_vector(height_profile, 32),
        resize_vector(width_profile, 32),
        resize_vector(top_profile, 24),
    )


def edge_signature(cell: Image.Image, mask: np.ndarray) -> np.ndarray:
    rgba = np.asarray(cell, dtype=np.float32)
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3] / 255.0
    # Composite on a fixed mid-gray so RGB and alpha are judged together.
    comp = rgb * alpha[:, :, None] + 96.0 * (1.0 - alpha[:, :, None])
    gray = 0.299 * comp[:, :, 0] + 0.587 * comp[:, :, 1] + 0.114 * comp[:, :, 2]
    gray_image = Image.fromarray(np.clip(gray, 0, 255).astype(np.uint8))
    mask_image = Image.fromarray((mask.astype(np.uint8) * 255))
    parts: list[np.ndarray] = []
    for width, height in ((16, 18), (24, 26), (32, 35), (48, 52)):
        small = np.asarray(gray_image.resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32) / 255.0
        dx = np.diff(small, axis=1, prepend=small[:, :1])
        dy = np.diff(small, axis=0, prepend=small[:1, :])
        alpha_small = np.asarray(mask_image.resize((width, height), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
        parts.append(np.concatenate([small.ravel(), np.abs(dx).ravel(), np.abs(dy).ravel(), alpha_small.ravel()]))
    return np.concatenate(parts).astype(np.float32)


def color_signature(cell: Image.Image, mask: np.ndarray) -> np.ndarray:
    rgba = np.asarray(cell, dtype=np.float32)
    rgb = rgba[:, :, :3]
    if not np.any(mask):
        return np.zeros(24, dtype=np.float32)
    pixels = rgb[mask]
    means = pixels.mean(axis=0) / 255.0
    stds = pixels.std(axis=0) / 255.0
    luminance = 0.299 * pixels[:, 0] + 0.587 * pixels[:, 1] + 0.114 * pixels[:, 2]
    hist, _ = np.histogram(luminance, bins=16, range=(0, 255), density=False)
    hist = hist.astype(np.float32) / max(len(luminance), 1)
    return np.concatenate([means, stds, hist]).astype(np.float32)


def aligned_mask(mask: np.ndarray, metric: dict[str, float | int | list[int] | bool], target_cx: float, target_bottom: int) -> np.ndarray:
    dx = int(round(target_cx - float(metric["lower_cx"])))
    dy = int(round(target_bottom - int(metric["bottom"])))
    out = np.zeros_like(mask)
    src_y0 = max(0, -dy)
    src_y1 = min(CELL_H, CELL_H - dy)
    src_x0 = max(0, -dx)
    src_x1 = min(CELL_W, CELL_W - dx)
    if src_y1 <= src_y0 or src_x1 <= src_x0:
        return out
    out[src_y0 + dy : src_y1 + dy, src_x0 + dx : src_x1 + dx] = mask[src_y0:src_y1, src_x0:src_x1]
    return out


def binary_edge(mask: np.ndarray) -> np.ndarray:
    # Four-neighbor boundary, no external morphology dependency required.
    edge = mask.copy()
    edge[1:, :] &= ~mask[:-1, :]
    edge[:-1, :] |= mask[:-1, :] & ~mask[1:, :]
    edge[:, 1:] |= mask[:, 1:] & ~mask[:, :-1]
    edge[:, :-1] |= mask[:, :-1] & ~mask[:, 1:]
    return edge


def make_overlay(cell: Image.Image, mask: np.ndarray, reference: np.ndarray, label: str) -> Image.Image:
    canvas = Image.new("RGB", (CELL_W, CELL_H + 24), (22, 22, 28))
    rgba = np.asarray(cell, dtype=np.uint8)
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    rgb = rgba[:, :, :3].astype(np.float32) * alpha + 96.0 * (1.0 - alpha)
    canvas.paste(Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)), (0, 24))
    draw = ImageDraw.Draw(canvas)
    ref_edge = binary_edge(reference)
    cur_edge = binary_edge(mask)
    ref_y, ref_x = np.nonzero(ref_edge)
    cur_y, cur_x = np.nonzero(cur_edge)
    draw.point([(int(x), int(y + 24)) for x, y in zip(ref_x, ref_y)], fill=(0, 225, 255))
    draw.point([(int(x), int(y + 24)) for x, y in zip(cur_x, cur_y)], fill=(255, 30, 210))
    draw.text((3, 4), label, fill=(240, 240, 240))
    return canvas


def l2_normalized(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0.0 or nb == 0.0:
        return float(np.linalg.norm(a - b))
    return float(np.linalg.norm(a / na - b / nb))


def canonical_lower_profile(mask: np.ndarray) -> np.ndarray:
    """Return a scale-free lower-body width profile for cross-state comparison."""
    start = int(CELL_H * 0.46)
    profile = mask[start:, :].sum(axis=1).astype(np.float32) / CELL_W
    return resize_vector(profile, 24)


def lower_iou(a: np.ndarray, b: np.ndarray) -> float:
    ay = a[int(CELL_H * 0.46) :]
    by = b[int(CELL_H * 0.46) :]
    union = np.logical_or(ay, by).sum()
    if union == 0:
        return 1.0
    return float(np.logical_and(ay, by).sum() / union)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--sheet-out", type=Path, default=None)
    parser.add_argument("--reviewed", action="store_true", help="mark the generated candidate sheet as visually reviewed by the parent")
    args = parser.parse_args()

    repo = args.repo.resolve()
    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.json_out or (out_dir / "supplemental-invariant-review-20260831.json")
    sheet_out = args.sheet_out or (out_dir / "supplemental-invariant-candidates.jpg")

    rows_data: dict[tuple[str, str], list[dict]] = {}
    scored: list[dict] = []
    frame_count = 0

    for role in ROLES:
        atlas_path = repo / "pets" / role / "spritesheet.webp"
        atlas = Image.open(atlas_path).convert("RGBA")
        for row_index, row_name in enumerate(ROWS):
            frames: list[dict] = []
            for col in range(COLS):
                cell = open_cell(atlas, row_index, col)
                mask = mask_for(cell)
                metrics = mask_metrics(mask)
                if not metrics["nonempty"]:
                    continue
                hp, wp, tp = profile_vectors(mask)
                frames.append({
                    "role": role,
                    "row": row_name,
                    "row_index": row_index,
                    "frame": col,
                    "cell": cell,
                    "mask": mask,
                    "metrics": metrics,
                    "height_profile": hp,
                    "width_profile": wp,
                    "top_profile": tp,
                    "edge": edge_signature(cell, mask),
                    "color": color_signature(cell, mask),
                })
                frame_count += 1
            rows_data[(role, row_name)] = frames

            if not frames:
                continue
            target_cx = float(np.median([float(f["metrics"]["lower_cx"]) for f in frames]))
            target_bottom = int(round(np.median([int(f["metrics"]["bottom"]) for f in frames])))
            aligned = [aligned_mask(f["mask"], f["metrics"], target_cx, target_bottom) for f in frames]
            occupancy = np.mean(np.stack(aligned, axis=0), axis=0)
            reference = occupancy >= 0.5
            ref_hp, ref_wp, ref_tp = profile_vectors(reference)
            ref_edge = edge_signature(Image.fromarray((reference.astype(np.uint8) * 255), mode="L").convert("RGBA"), reference)
            ref_color = np.mean(np.stack([f["color"] for f in frames], axis=0), axis=0)

            for f in frames:
                m = f["metrics"]
                hp_dist = float(np.linalg.norm(f["height_profile"] - ref_hp))
                wp_dist = float(np.linalg.norm(f["width_profile"] - ref_wp))
                tp_dist = float(np.linalg.norm(f["top_profile"] - ref_tp))
                edge_dist = l2_normalized(f["edge"], ref_edge)
                color_dist = float(np.linalg.norm(f["color"] - ref_color))
                raw_aspect_z = robust_z(float(m["aspect"]), np.asarray([float(x["metrics"]["aspect"]) for x in frames]), floor=0.01)
                raw_height_z = robust_z(float(m["height"]), np.asarray([float(x["metrics"]["height"]) for x in frames]), floor=1.0)
                score = (
                    2.2 * hp_dist
                    + 1.4 * wp_dist
                    + 1.9 * tp_dist
                    + 1.2 * edge_dist
                    + 0.7 * color_dist
                    + 0.65 * min(raw_aspect_z, 12.0)
                    + 0.65 * min(raw_height_z, 12.0)
                )
                reasons: list[str] = []
                if raw_aspect_z >= 4.0:
                    reasons.append(f"aspect_z={raw_aspect_z:.1f}")
                if raw_height_z >= 4.0:
                    reasons.append(f"height_z={raw_height_z:.1f}")
                if hp_dist >= 0.18:
                    reasons.append(f"vertical_profile={hp_dist:.3f}")
                if tp_dist >= 0.12:
                    reasons.append(f"upper_profile={tp_dist:.3f}")
                if edge_dist >= 0.50:
                    reasons.append(f"edge_fp={edge_dist:.3f}")
                if color_dist >= 0.25:
                    reasons.append(f"color_fp={color_dist:.3f}")
                scored.append({
                    "role": role,
                    "row": row_name,
                    "frame": int(f["frame"]),
                    "score": round(float(score), 4),
                    "reasons": reasons or ["combined-invariant-distance"],
                    "metrics": m,
                    "reference": {"lower_cx": round(target_cx, 3), "bottom": target_bottom},
                    "reference_mask": reference,
                    "mask": f["mask"],
                    "cell": f["cell"],
                })

    # A row-relative reference can miss a defect shared by every frame in a row.
    # Compare every state against that role's idle lower-body envelope as a
    # second, independent signal. This does not auto-fail action rows because
    # gestures and jumps are expected to change the lower silhouette.
    role_idle_refs: dict[str, tuple[float, int, np.ndarray, np.ndarray]] = {}
    for role in ROLES:
        idle_frames = rows_data[(role, "idle")]
        if not idle_frames:
            continue
        idle_cx = float(np.median([float(f["metrics"]["lower_cx"]) for f in idle_frames]))
        idle_bottom = int(round(np.median([int(f["metrics"]["bottom"]) for f in idle_frames])))
        idle_aligned = [aligned_mask(f["mask"], f["metrics"], idle_cx, idle_bottom) for f in idle_frames]
        idle_ref = np.mean(np.stack(idle_aligned, axis=0), axis=0) >= 0.5
        role_idle_refs[role] = (idle_cx, idle_bottom, idle_ref, canonical_lower_profile(idle_ref))

    for (role, row_name), frames in rows_data.items():
        if role not in role_idle_refs:
            continue
        idle_cx, idle_bottom, idle_ref, idle_lower_profile = role_idle_refs[role]
        for f in frames:
            aligned = aligned_mask(f["mask"], f["metrics"], idle_cx, idle_bottom)
            iou = lower_iou(aligned, idle_ref)
            lower_profile_distance = float(np.linalg.norm(canonical_lower_profile(aligned) - idle_lower_profile))
            f["canonical_lower_iou"] = iou
            f["canonical_lower_profile_distance"] = lower_profile_distance
            # Keep this signal deliberately bounded: state-specific action
            # rows are expected to differ, but a shared compression/stretch
            # pattern should still surface for review.
            canonical_penalty = 0.55 * max(0.0, 0.72 - iou) + 0.35 * min(lower_profile_distance, 1.0)
            f["canonical_penalty"] = canonical_penalty

    for item in scored:
        source = rows_data[(item["role"], item["row"])][item["frame"]]
        item["canonical_lower_iou"] = round(float(source.get("canonical_lower_iou", 0.0)), 4)
        item["canonical_lower_profile_distance"] = round(float(source.get("canonical_lower_profile_distance", 0.0)), 4)
        item["canonical_penalty"] = round(float(source.get("canonical_penalty", 0.0)), 4)
        item["score"] = round(float(item["score"]) + float(source.get("canonical_penalty", 0.0)), 4)
        if float(source.get("canonical_lower_iou", 1.0)) < 0.55:
            item["reasons"].append(f"idle_lower_iou={float(source['canonical_lower_iou']):.3f}")
        if float(source.get("canonical_lower_profile_distance", 0.0)) >= 0.25:
            item["reasons"].append(f"idle_lower_profile={float(source['canonical_lower_profile_distance']):.3f}")

    scored.sort(key=lambda x: (-float(x["score"]), x["role"], x["row"], int(x["frame"])))
    top = scored[:32]

    tile_w, tile_h = CELL_W, CELL_H + 24
    cols = 4
    rows = int(math.ceil(len(top) / cols))
    sheet = Image.new("RGB", (cols * tile_w, rows * tile_h), (12, 12, 16))
    for index, item in enumerate(top):
        x = (index % cols) * tile_w
        y = (index // cols) * tile_h
        tile = make_overlay(item["cell"], item["mask"], item["reference_mask"], f"{item['role']}/{item['row']}/f{item['frame']} s{item['score']:.1f}")
        sheet.paste(tile, (x, y))
    sheet.save(sheet_out, quality=92, subsampling=0)

    known = {
        "hei-mao/jumping/f2",
        "hei-mao-quality/jumping/f2",
        "hei-mao-foodie/waiting/f2",
        "hei-mao-foodie/waiting/f3",
        "hei-mao-delivery/failed/f4",
        "hei-mao-delivery/failed/f5",
    }
    json_top = []
    for item in top:
        clean = {k: v for k, v in item.items() if k not in {"cell", "mask", "reference_mask"}}
        json_top.append(clean)
    payload = {
        "schema_version": 1,
        "checked_at": "2026-08-31",
        "scope": "supplemental non-generative visual recheck using anchor-normalized shape, canonical identity envelopes, multi-scale perceptual, and material fingerprints",
        "methods": [
            {
                "name": "anchor-normalized silhouette fingerprint",
                "details": "Align each frame by lower-body centroid and bottom baseline, then compare resampled vertical, horizontal, and upper-band occupancy profiles against the row ensemble median.",
                "purpose": "surface flattened or stretched proportions, duplicated upper contours, and body registration drift that can be diluted by raw bbox metrics",
            },
            {
                "name": "multi-scale composited edge fingerprint",
                "details": "Composite RGBA on a fixed mid-gray, downsample to 32x35, and compare luminance gradients plus alpha occupancy.",
                "purpose": "check final-size silhouette readability, blur/detail loss, and shape changes independent of exact pixel alignment",
            },
            {
                "name": "alpha-weighted material fingerprint",
                "details": "Compare alpha-weighted RGB mean/std and luminance histogram against the row ensemble.",
                "purpose": "detect frame-level palette/material drift that geometry-only review can miss",
            },
            {
                "name": "canonical idle-envelope comparison",
                "details": "Register every state to that role's idle lower-body anchor and compare lower-body IoU and width profiles.",
                "purpose": "catch a whole row that is consistently squashed, stretched, or displaced even when a row-relative median would hide it",
            },
            {
                "name": "candidate-only edge overlay",
                "details": "Render the candidate contour in magenta against the aligned row-ensemble contour in cyan; scores never auto-promote failures.",
                "purpose": "human confirmation of whether an outlier is a real visual defect or an intentional gesture",
            },
        ],
        "roles": ROLES,
        "rows_checked": len(ROLES) * len(ROWS),
        "frames_checked": frame_count,
        "animation_frames_checked": frame_count - len(ROLES),
        "v2_neutral_look_cells_checked": len(ROLES),
        "candidate_counts": {
            "scored_frames": len(scored),
            "top_sheet_frames": len(top),
            "known_blocker_candidates": sum(1 for x in top if f"{x['role']}/{x['row']}/f{x['frame']}" in known),
            "canonical_lower_iou_review_candidates": sum(1 for x in scored if float(x.get("canonical_lower_iou", 1.0)) < 0.55),
        },
        "top_candidates": json_top,
        "known_blocker_candidates": sorted(known),
        "visual_review": {
            "status": "pass_with_four_existing_blockers" if args.reviewed else "pending_manual_confirmation",
            "new_hard_failures": [],
            "confirmed_existing_blockers": [
                "hei-mao/jumping frame 2 duplicated head",
                "hei-mao-quality/jumping frame 2 duplicated head",
                "hei-mao-foodie/waiting stacked upper contours",
                "hei-mao-delivery/failed repeated head and pose-family switch",
            ] if args.reviewed else [],
            "note": (
                "Candidate sheet reviewed at normal display size; no new hard failure beyond the four existing blockers."
                if args.reviewed
                else "Review supplemental-invariant-candidates.jpg at normal display size; metric outliers are evidence only."
            ),
        },
        "formal_assets_modified": False,
        "artifacts": [sheet_out.name, json_out.name],
        "limitations": [
            "The method is raster/alpha based and does not replace live Codex App window capture.",
            "Row-ensemble references intentionally treat gestures, props, and look arcs as candidates rather than automatic failures.",
            "Material fingerprints can flag legitimate state-specific effects and require visual confirmation.",
        ],
    }
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_out), "sheet": str(sheet_out), "frames": frame_count, "candidates": len(top)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
