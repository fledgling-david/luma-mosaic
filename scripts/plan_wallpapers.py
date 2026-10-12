#!/usr/bin/env python3
"""Build a deterministic three-direction wallpaper brief."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence


BOLD_DIRECTIONS = (
    "editorial surrealism with sculptural negative space",
    "ink-and-mineral landscape with restrained metallic accents",
    "luminous paper theatre with layered cut-paper depth",
    "retro scientific plate with precise graphic specimens",
    "quiet brutalist architecture with tactile concrete and light",
    "maximal botanical opera with oversized organic rhythm",
    "analogue film dream with practical light and imperfect grain",
    "graphic folk art with flat shapes and hand-made texture",
)


def choose_bold_direction(subject: str, mood: str) -> str:
    seed = f"{subject.strip().lower()}|{mood.strip().lower()}".encode("utf-8")
    index = int.from_bytes(hashlib.sha256(seed).digest()[:4], "big") % len(
        BOLD_DIRECTIONS
    )
    return BOLD_DIRECTIONS[index]


def _normalize_palette(colors: Sequence[str]) -> list[str]:
    cleaned = []
    for color in colors:
        value = color.strip().upper()
        if not value:
            continue
        if not value.startswith("#"):
            value = "#" + value
        if len(value) != 7 or any(c not in "#0123456789ABCDEF" for c in value):
            raise ValueError(f"Invalid HEX color: {color}")
        if value not in cleaned:
            cleaned.append(value)
    return cleaned


def build_plan(
    subject: str,
    mood: str,
    colors: Sequence[str],
    ratio: str = "16:9",
    safe_side: str = "left",
) -> dict:
    if safe_side not in {"left", "right", "none"}:
        raise ValueError("safe_side must be left, right, or none")
    palette = _normalize_palette(colors)
    if not palette:
        raise ValueError("At least one palette color is required")

    bold_direction = choose_bold_direction(subject, mood)
    shared = {
        "subject": subject,
        "identity_rule": "Preserve recognisable features and proportions.",
        "ratio": ratio,
        "desktop_safe_side": safe_side,
    }
    return {
        "shared": shared,
        "directions": [
            {
                "id": "01-source-match",
                "label": "原图跟色 / Source Match",
                "palette": palette,
                "brief": f"Polish the photographed world while retaining its {mood} mood.",
            },
            {
                "id": "02-intelligent-extension",
                "label": "智能延展 / Intelligent Extension",
                "palette": palette[:3],
                "brief": "Transform visible colors, shapes, materials, or light into a connected new environment.",
            },
            {
                "id": "03-bold-reimagination",
                "label": "大胆创新 / Bold Reimagination",
                "palette": [],
                "brief": f"Reframe the subject as {bold_direction}; keep identity stable.",
            },
        ],
    }


def _colors_from_palette_file(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [entry["hex"] for entry in data.get("palette", [])]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", required=True, help="Main subject description")
    parser.add_argument("--mood", default="natural", help="Observed source mood")
    parser.add_argument("--colors", nargs="*", default=[], help="HEX palette colors")
    parser.add_argument("--palette-file", type=Path, help="JSON from analyze_palette.py")
    parser.add_argument("--ratio", default="16:9")
    parser.add_argument("--safe-side", choices=("left", "right", "none"), default="left")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    colors = list(args.colors)
    if args.palette_file:
        colors = _colors_from_palette_file(args.palette_file)
    plan = build_plan(args.subject, args.mood, colors, args.ratio, args.safe_side)
    payload = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
