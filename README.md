# LumaMosaic · 光影织境

**Weave source photos into three visual worlds.**

LumaMosaic is an Agent Skill for turning one or more reference photos into three finished wallpaper directions:

1. **Source Match** — faithful to the source palette, light, setting, and mood.
2. **Intelligent Extension** — grows a new environment from visible colors, forms, materials, or light.
3. **Bold Reimagination** — chooses a fresh art direction while preserving the subject's identity.

It works with pets, people, products, cars, food, architecture, and travel photography. The third direction is deliberately adaptive: it does not default every request to cyberpunk, purple skies, or moonlit fantasy.

[中文说明](README.zh-CN.md)

## Install

```bash
npx skills add fledgling-david/luma-mosaic
```

Or copy the `luma-mosaic` folder into your skills directory and restart your agent host.

## Use

Attach one or more photos and ask:

> Use $luma-mosaic to turn these photos into three 16:9 desktop wallpapers. Keep the same subject recognizable and leave the left side quiet for icons.

The skill analyses identity anchors, source palette, lighting, mood, image roles, and desktop-safe zones before generating three separate bitmaps. If the user chooses one mode, it can produce only that direction.

## Included helpers

The skill remains useful without the Python helpers, but they make planning and validation repeatable.

```bash
python -m pip install -r requirements.txt

# Extract a weighted source palette
python scripts/analyze_palette.py photo-1.jpg photo-2.jpg --output palette.json

# Build a structured three-direction brief
python scripts/plan_wallpapers.py --subject "tabby cat" --mood "quiet and warm" \
  --palette-file palette.json --output plan.json

# Check size, aspect ratio, and near-duplicates
python scripts/validate_images.py output-01.png output-02.png output-03.png --ratio 16:9
```

## Repository structure

```text
luma-mosaic/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── modes.md
│   ├── prompt-patterns.md
│   └── quality-checklist.md
├── scripts/
│   ├── analyze_palette.py
│   ├── plan_wallpapers.py
│   └── validate_images.py
├── tests/
├── examples/
└── .github/workflows/ci.yml
```

## Requirements and privacy

- An image-generation or image-editing capability that accepts reference images.
- Python 3.10+ and Pillow only when using the optional helper scripts.
- Source photos stay wherever the host tool processes them; this repository contains no upload or telemetry code.

LumaMosaic guides generation and review. The final visual fidelity still depends on the image model and the quality of the supplied references.

## Test

```bash
python -m unittest discover -s tests -v
```

## License

MIT
