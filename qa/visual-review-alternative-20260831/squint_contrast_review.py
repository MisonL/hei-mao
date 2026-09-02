#!/usr/bin/env python3
"""Evidence-only small-display and contrast-pressure review for v2 atlases.

This review approximates a quick "squint" check instead of relying on one
alpha threshold or one nominal display size. It renders every used cell as a
grayscale/alpha-aware thumbnail at several display sizes on dark, light, and
saturated backgrounds, then ranks temporal outliers for normal-size review.
The formal spritesheets are never modified.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


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
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
    ("look-row-9", 8),
    ("look-row-10", 8),
]
CELL_W = 192
CELL_H = 208
ALPHA_THRESHOLD = 16
DISPLAY_SIZES = ((24, 26), (32, 35), (48, 52))
BACKGROUNDS = {
    "dark": (28, 30, 38),
    "light": (238, 240, 242),
    "saturated": (190, 26, 46),
}
KNOWN_BLOCKERS = {
    ("hei-mao", "jumping"): "frame 2 duplicated head",
    ("hei-mao-quality", "jumping"): "frame 2 duplicated head",
    ("hei-mao-foodie", "waiting"): "frames 2-3 stacked upper contours",
    ("hei-mao-delivery", "failed"): "frames 0-4 repeated head and pose-family switch",
    ("hei-mao-quality", "running-left"): "complete row regeneration required by combined QA",
    ("hei-mao-quality", "failed"): "complete row regeneration required by combined QA",
    ("hei-mao-traveler", "waiting"): "complete row regeneration required by combined QA",
    ("hei-mao-traveler", "review"): "complete row regeneration required by combined QA",
}


def open_cell(atlas: Image.Image, row_index: int, frame: int) -> Image.Image:
    return atlas.crop(
        (frame * CELL_W, row_index * CELL_H, (frame + 1) * CELL_W, (row_index + 1) * CELL_H)
    ).convert("RGBA")


def luma(pixel: tuple[int, int, int]) -> float:
    return 0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2]


def composite(cell: Image.Image, background: tuple[int, int, int]) -> Image.Image:
    base = Image.new("RGBA", cell.size, (*background, 255))
    return Image.alpha_composite(base, cell).convert("RGB")


def blurred_thumbnail(cell: Image.Image, size: tuple[int, int], background: tuple[int, int, int]) -> Image.Image:
    rendered = composite(cell.resize(size, Image.Resampling.LANCZOS), background)
    # A small blur models the loss of high-frequency detail when the pet is
    # viewed peripherally or while the user is scanning a busy desktop.
    radius = max(0.35, min(size) / 52.0)
    return rendered.filter(ImageFilter.GaussianBlur(radius=radius))


def alpha_thumbnail(cell: Image.Image, size: tuple[int, int]) -> Image.Image:
    return cell.getchannel("A").resize(size, Image.Resampling.LANCZOS)


def bbox_from_alpha(alpha: Image.Image, threshold: int = 24) -> tuple[int, int, int, int] | None:
    pixels = alpha.load()
    xs: list[int] = []
    ys: list[int] = []
    for y in range(alpha.height):
        for x in range(alpha.width):
            if pixels[x, y] >= threshold:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def display_features(cell: Image.Image, size: tuple[int, int]) -> tuple[dict[str, float], list[float]]:
    alpha = alpha_thumbnail(cell, size)
    alpha_pixels = alpha.load()
    visible = [(x, y, alpha_pixels[x, y]) for y in range(size[1]) for x in range(size[0]) if alpha_pixels[x, y] >= 24]
    if not visible:
        return (
            {
                "occupancy": 0.0,
                "bbox_width": 0.0,
                "bbox_height": 0.0,
                "cx": 0.0,
                "cy": 0.0,
                "min_contrast": 0.0,
                "mean_contrast": 0.0,
                "edge_energy": 0.0,
            },
            [0.0] * 8,
        )

    box = bbox_from_alpha(alpha)
    assert box is not None
    x0, y0, x1, y1 = box
    area = len(visible)
    total = size[0] * size[1]
    weighted = sum(weight for _, _, weight in visible)
    cx = sum(x * weight for x, _, weight in visible) / max(weighted, 1.0) / max(size[0] - 1, 1)
    cy = sum(y * weight for _, y, weight in visible) / max(weighted, 1.0) / max(size[1] - 1, 1)

    contrast_values: list[float] = []
    edge_values: list[float] = []
    for name, background in BACKGROUNDS.items():
        del name
        thumb = blurred_thumbnail(cell, size, background)
        pixels = thumb.load()
        background_luma = luma(background)
        local_contrast = [
            abs(luma(pixels[x, y]) - background_luma) / 255.0
            for x, y, _ in visible
        ]
        contrast_values.append(sum(local_contrast) / max(len(local_contrast), 1))
        strong = sum(1 for value in local_contrast if value >= 0.08)
        contrast_values.append(strong / max(len(local_contrast), 1))
        for y in range(size[1]):
            for x in range(size[0]):
                if x + 1 < size[0]:
                    edge_values.append(abs(luma(pixels[x + 1, y]) - luma(pixels[x, y])) / 255.0)
                if y + 1 < size[1]:
                    edge_values.append(abs(luma(pixels[x, y + 1]) - luma(pixels[x, y])) / 255.0)

    min_contrast = min(contrast_values[0::2])
    mean_contrast = sum(contrast_values[0::2]) / 3.0
    edge_energy = sum(edge_values) / max(len(edge_values), 1)
    metrics = {
        "occupancy": area / max(total, 1),
        "bbox_width": (x1 - x0 + 1) / max(size[0], 1),
        "bbox_height": (y1 - y0 + 1) / max(size[1], 1),
        "cx": cx,
        "cy": cy,
        "min_contrast": min_contrast,
        "mean_contrast": mean_contrast,
        "edge_energy": edge_energy,
    }
    vector = [metrics[key] for key in ("occupancy", "bbox_width", "bbox_height", "cx", "cy", "min_contrast", "mean_contrast", "edge_energy")]
    return metrics, vector


def median(values: list[float]) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def robust_score(vector: list[float], matrix: list[list[float]]) -> tuple[float, list[str]]:
    if not matrix:
        return 0.0, ["no-row-reference"]
    medians = [median([row[index] for row in matrix]) for index in range(len(vector))]
    scales: list[float] = []
    for index, value in enumerate(medians):
        deviations = [abs(row[index] - value) for row in matrix]
        scales.append(max(1.4826 * median(deviations), 0.015))
    z = [min(abs(value - medians[index]) / scales[index], 12.0) for index, value in enumerate(vector)]
    # Each display size contributes one block of eight descriptors.
    block_scores = [sum(z[offset : offset + 8]) / 8.0 for offset in range(0, len(z), 8)]
    score = sum(block_scores) / max(len(block_scores), 1)
    reasons: list[str] = []
    if block_scores and block_scores[0] >= 2.0:
        reasons.append(f"24x26_profile={block_scores[0]:.2f}")
    if len(block_scores) > 1 and block_scores[1] >= 2.0:
        reasons.append(f"32x35_profile={block_scores[1]:.2f}")
    if len(block_scores) > 2 and block_scores[2] >= 2.0:
        reasons.append(f"48x52_profile={block_scores[2]:.2f}")
    if vector[5] < 0.08:
        reasons.append("low_minimum_contrast")
    if vector[0] and vector[8] / max(vector[0], 1e-6) < 0.55:
        reasons.append("display_mass_drop")
    return score, reasons or ["combined-squint-profile"]


def panel(cell: Image.Image, mode: str) -> Image.Image:
    size = (48, 52)
    if mode == "dark":
        rendered = blurred_thumbnail(cell, size, BACKGROUNDS["dark"])
    elif mode == "light":
        rendered = blurred_thumbnail(cell, size, BACKGROUNDS["light"])
    elif mode == "saturated":
        rendered = blurred_thumbnail(cell, size, BACKGROUNDS["saturated"])
    else:
        alpha = alpha_thumbnail(cell, size)
        rendered = Image.new("RGB", size, (42, 44, 52))
        mask = alpha.load()
        source = composite(cell.resize(size, Image.Resampling.LANCZOS), (42, 44, 52)).load()
        target = rendered.load()
        for y in range(size[1]):
            for x in range(size[0]):
                if mask[x, y] >= 24:
                    value = int(round(luma(source[x, y])))
                    target[x, y] = (value, value, value)
                else:
                    target[x, y] = (42, 44, 52)
    return rendered.resize((96, 104), Image.Resampling.NEAREST)


def make_candidate_sheet(candidates: list[dict], atlases: dict[str, Image.Image], output: Path) -> None:
    font = ImageFont.load_default()
    tile_w = 410
    tile_h = 154
    columns = 4
    rows = max(1, math.ceil(len(candidates) / columns))
    sheet = Image.new("RGB", (columns * tile_w, rows * tile_h), (18, 20, 26))
    draw = ImageDraw.Draw(sheet)
    for index, item in enumerate(candidates):
        col = index % columns
        row = index // columns
        x = col * tile_w
        y = row * tile_h
        cell = open_cell(atlases[item["role"]], item["row_index"], item["frame"])
        draw.text((x + 4, y + 3), f"#{index + 1} {item['role']}/{item['row']}/{item['frame']}", fill=(242, 242, 242), font=font)
        draw.text((x + 4, y + 16), f"score={item['score']:.2f}  {'; '.join(item['reasons'])}", fill=(190, 198, 210), font=font)
        labels = ("dark", "light", "saturated", "gray+alpha")
        for panel_index, mode in enumerate(labels):
            px = x + 4 + panel_index * 101
            py = y + 34
            image = panel(cell, mode)
            sheet.paste(image, (px, py))
            draw.rectangle((px, py, px + 95, py + 103), outline=(88, 92, 104), width=1)
            draw.text((px + 2, py + 106), mode, fill=(166, 172, 184), font=font)
        if item.get("known_blocker"):
            draw.text((x + 4, y + 137), "known blocker control: " + item["known_blocker"], fill=(255, 176, 92), font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92, optimize=True)


def run(repo_dir: Path, output_dir: Path, candidate_count: int) -> dict:
    atlases: dict[str, Image.Image] = {}
    for role in ROLES:
        path = repo_dir / "pets" / role / "spritesheet.webp"
        atlases[role] = Image.open(path).convert("RGBA")

    records: list[dict] = []
    row_vectors: dict[tuple[str, str], list[list[float]]] = {}
    for role in ROLES:
        for row_index, (row_name, frame_count) in enumerate(ROWS):
            key = (role, row_name)
            row_vectors[key] = []
            for frame in range(frame_count):
                cell = open_cell(atlases[role], row_index, frame)
                vector: list[float] = []
                profiles: dict[str, dict] = {}
                for size in DISPLAY_SIZES:
                    metrics, block = display_features(cell, size)
                    vector.extend(block)
                    profiles[f"{size[0]}x{size[1]}"] = metrics
                record = {
                    "role": role,
                    "row": row_name,
                    "row_index": row_index,
                    "frame": frame,
                    "vector": vector,
                    "profiles": profiles,
                    "known_blocker": KNOWN_BLOCKERS.get(key),
                }
                records.append(record)
                row_vectors[key].append(vector)

    for record in records:
        key = (record["role"], record["row"])
        score, reasons = robust_score(record["vector"], row_vectors[key])
        record["score"] = round(score, 6)
        record["reasons"] = reasons

    ranked = sorted(records, key=lambda item: item["score"], reverse=True)
    selected: list[dict] = []
    selected_keys: set[tuple[str, str, int]] = set()
    # Keep the known controls in the sheet even if their numeric score is not
    # in the top group; they calibrate the human review threshold.
    controls = [item for item in ranked if item["known_blocker"]]
    for item in controls:
        key = (item["role"], item["row"], item["frame"])
        if key not in selected_keys:
            selected.append(item)
            selected_keys.add(key)
    for item in ranked:
        if len(selected) >= candidate_count:
            break
        key = (item["role"], item["row"], item["frame"])
        if key not in selected_keys:
            selected.append(item)
            selected_keys.add(key)
    selected = selected[:candidate_count]
    selected.sort(key=lambda item: item["score"], reverse=True)

    sheet_path = output_dir / "squint-contrast-candidates-v1.jpg"
    make_candidate_sheet(selected, atlases, sheet_path)
    candidate_records = []
    for rank, item in enumerate(selected, start=1):
        candidate_records.append(
            {
                "rank": rank,
                "role": item["role"],
                "row": item["row"],
                "frame": item["frame"],
                "score": item["score"],
                "reasons": item["reasons"],
                "known_blocker": item["known_blocker"],
                "profiles": item["profiles"],
            }
        )

    return {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "supplemental small-display grayscale and contrast-pressure review of all current v2 atlases",
        "method": {
            "name": "multi-size squint and contrast stress review",
            "implementation": "qa/visual-review-alternative-20260831/squint_contrast_review.py",
            "purpose": "用灰度、alpha 轮廓和轻度模糊模拟小尺寸扫视，在深色、浅色和高饱和背景下识别主体消失、局部压扁、边缘闪烁和对比度骤降",
            "display_sizes": ["24x26", "32x35", "48x52"],
            "backgrounds": list(BACKGROUNDS),
            "profile": "occupancy, bbox width/height, alpha-weighted centroid, minimum/mean contrast, and blurred edge energy",
            "selection": "row-local robust outlier ranking; numeric outliers are candidates only",
        },
        "coverage": {
            "roles": len(ROLES),
            "rows": len(ROLES) * len(ROWS),
            "frames": len(records),
            "candidate_sheet_items": len(selected),
        },
        "visual_review": {
            "status": "pending_normal_size_sheet_review",
            "new_hard_failures": [],
            "confirmed_existing_blockers": [],
        },
        "candidate_counts": {
            "ranked_frames": len(records),
            "selected_frames": len(selected),
            "known_control_frames": len(controls),
        },
        "candidates": candidate_records,
        "limitations": [
            "灰度和模糊压力测试只模拟感知风险，不能证明真实 Codex App GPU 合成、窗口层级或多屏定位",
            "对比度低可能是角色本身的合法深色材质，必须结合正常尺寸图和动作语义判断",
            "轮廓压力指标不替代完整行重生规则；发现硬失败时仍需按 hatch-pet 重生完整动作行",
        ],
        "formal_assets_modified": False,
        "artifacts": [
            "qa/visual-review-alternative-20260831/squint-contrast-candidates-v1.jpg",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-dir", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path("qa/visual-review-alternative-20260831"))
    parser.add_argument("--candidate-count", type=int, default=32)
    args = parser.parse_args()
    result = run(args.repo_dir, args.output_dir, max(1, args.candidate_count))
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "squint-contrast-review-20260831-v1.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json_path)
    print(result["coverage"])
    print("top_candidates", [(item["role"], item["row"], item["frame"], item["score"]) for item in result["candidates"][:12]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
