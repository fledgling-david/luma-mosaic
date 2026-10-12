#!/usr/bin/env python3
"""Validate wallpaper dimensions, aspect ratio, and near-duplicates."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

from PIL import Image, ImageOps


def parse_ratio(value: str) -> float:
    if ":" in value:
        width, height = value.split(":", 1)
        ratio = float(width) / float(height)
    else:
        ratio = float(value)
    if ratio <= 0:
        raise ValueError("ratio must be positive")
    return ratio


def difference_hash(path: str | Path, size: int = 16) -> int:
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("L").resize(
            (size + 1, size), Image.Resampling.LANCZOS
        )
        if hasattr(image, "get_flattened_data"):
            pixels = list(image.get_flattened_data())
        else:
            pixels = list(image.getdata())
    value = 0
    for row in range(size):
        offset = row * (size + 1)
        for column in range(size):
            value = (value << 1) | int(
                pixels[offset + column] > pixels[offset + column + 1]
            )
    return value


def validate_images(
    paths: list[str | Path],
    ratio: float,
    min_width: int = 1920,
    min_height: int = 1080,
    tolerance: float = 0.02,
    duplicate_distance: int = 8,
    expected: int = 3,
) -> dict:
    files = [Path(path) for path in paths]
    issues: list[str] = []
    details = []
    hashes: dict[Path, int] = {}

    if len(files) != expected:
        issues.append(f"Expected {expected} images, received {len(files)}.")

    for path in files:
        if not path.is_file():
            issues.append(f"Missing file: {path}")
            continue
        try:
            with Image.open(path) as image:
                width, height = image.size
                image.verify()
        except Exception as exc:  # Pillow raises format-specific exceptions
            issues.append(f"Unreadable image {path}: {exc}")
            continue

        actual_ratio = width / height
        details.append(
            {
                "path": str(path),
                "width": width,
                "height": height,
                "ratio": round(actual_ratio, 4),
            }
        )
        if width < min_width or height < min_height:
            issues.append(
                f"{path} is {width}x{height}; minimum is {min_width}x{min_height}."
            )
        if abs(actual_ratio - ratio) / ratio > tolerance:
            issues.append(
                f"{path} has ratio {actual_ratio:.4f}; expected {ratio:.4f}."
            )
        hashes[path] = difference_hash(path)

    for left, right in combinations(hashes, 2):
        distance = (hashes[left] ^ hashes[right]).bit_count()
        if distance <= duplicate_distance:
            issues.append(
                f"Possible near-duplicate: {left} and {right} (dHash distance {distance})."
            )

    return {"ok": not issues, "images": details, "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+")
    parser.add_argument("--ratio", default="16:9")
    parser.add_argument("--min-width", type=int, default=1920)
    parser.add_argument("--min-height", type=int, default=1080)
    parser.add_argument("--tolerance", type=float, default=0.02)
    parser.add_argument("--duplicate-distance", type=int, default=8)
    parser.add_argument("--expected", type=int, default=3)
    args = parser.parse_args()

    result = validate_images(
        args.images,
        parse_ratio(args.ratio),
        args.min_width,
        args.min_height,
        args.tolerance,
        args.duplicate_distance,
        args.expected,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
