#!/usr/bin/env python3
"""Extract a compact, weighted palette from one or more source photos."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def _sample_pixels(path: Path, sample_size: int) -> Iterable[tuple[int, int, int]]:
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        image.thumbnail((sample_size, sample_size), Image.Resampling.LANCZOS)
        if hasattr(image, "get_flattened_data"):
            return list(image.get_flattened_data())
        return list(image.getdata())


def extract_palette(
    paths: Iterable[str | Path], colors: int = 6, sample_size: int = 256
) -> dict:
    """Return dominant colors using stable 5-bit RGB bins.

    The weighted centroid of each bin is reported instead of the bin corner, which
    keeps the result closer to the photographed colors while remaining fast.
    """

    source_paths = [Path(path) for path in paths]
    if not source_paths:
        raise ValueError("At least one source image is required.")
    if colors < 1:
        raise ValueError("colors must be at least 1")

    bins: dict[tuple[int, int, int], list[int]] = defaultdict(
        lambda: [0, 0, 0, 0]
    )
    total = 0
    for path in source_paths:
        if not path.is_file():
            raise FileNotFoundError(path)
        for red, green, blue in _sample_pixels(path, sample_size):
            key = (red >> 3, green >> 3, blue >> 3)
            bucket = bins[key]
            bucket[0] += red
            bucket[1] += green
            bucket[2] += blue
            bucket[3] += 1
            total += 1

    ranked = sorted(bins.values(), key=lambda item: item[3], reverse=True)[:colors]
    palette = []
    for red_sum, green_sum, blue_sum, count in ranked:
        rgb = (
            round(red_sum / count),
            round(green_sum / count),
            round(blue_sum / count),
        )
        palette.append(
            {
                "hex": rgb_to_hex(rgb),
                "rgb": list(rgb),
                "weight": round(count / total, 4),
            }
        )

    return {
        "source_count": len(source_paths),
        "sampled_pixels": total,
        "palette": palette,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", help="Source image paths")
    parser.add_argument("--colors", type=int, default=6, help="Number of colors")
    parser.add_argument(
        "--sample-size",
        type=int,
        default=256,
        help="Maximum width and height sampled per image",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    result = extract_palette(args.images, args.colors, args.sample_size)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
