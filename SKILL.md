---
name: luma-mosaic
description: "Turn one or more user-supplied photos into three distinct, finished wallpaper artworks: source-matched, intelligently extended, and boldly reimagined. Use for multi-photo wallpaper, photo collage, subject-preserving fantasy scene, or three-direction visual concept requests. Do not use for simple deterministic crops, color correction, or prompt-only advice."
---

# LumaMosaic · 光影织境

Create three usable bitmap wallpapers from the user's photos. The default set is one **source-matched** version, one **intelligent extension**, and one **bold reimagination**. Preserve recognisable subjects across all three while making the compositions genuinely different.

## Before generating

1. Inspect every supplied photo. Record the subject identity, features that must not change, useful poses, dominant colors, lighting, environment, and defects that should not be copied.
2. Assign each image a role: hero portrait, supporting pose, texture or environmental cue. Do not force every image into every composition.
3. Infer the output ratio from the request. If unspecified, use 16:9 landscape at 3840×2160 and keep one side visually quiet for desktop icons.
4. Ask a question only when a missing choice would materially change the result, such as an unknown device ratio or uncertainty about which person or pet is the subject.

For repeatable palette extraction, run `scripts/analyze_palette.py`. For a structured three-version brief, run `scripts/plan_wallpapers.py`. These helpers inform visual judgment; they do not replace inspection of the photographs.

## Generate the three directions

Read [references/modes.md](references/modes.md) for the mode boundaries and [references/prompt-patterns.md](references/prompt-patterns.md) when constructing image-generation prompts.

- **01 Source Match / 原图跟色:** Stay close to the source palette, light, setting, and emotional register. Improve composition without inventing a different world.
- **02 Intelligent Extension / 智能延展:** Derive a new scene from visible evidence. Transform colors, materials, shapes, weather, or objects into a coherent expanded environment.
- **03 Bold Reimagination / 大胆创新:** Keep subject identity but choose a new art direction that fits the subject. Vary the direction from request to request; do not default to cyberpunk, purple skies, moons, or other recurring motifs.

Use the available image-generation or image-editing capability and include the actual source images as references. Do not redraw or composite final bitmap art with Python unless the user explicitly asks for a deterministic collage. When the user asks for wallpapers, deliver the images rather than stopping at prompts.

## Identity and composition invariants

- Preserve face shape, fur or hair pattern, markings, body proportions, product geometry, and other identity anchors.
- Treat different poses of the same subject as one identity. Do not create extra limbs, faces, fingers, tails, logos, or duplicate subjects.
- Integrate edges, shadows, scale, grain, and light direction so the result is one scene, not cutouts pasted on a background.
- Keep the focal subject clear at thumbnail size. Avoid placing eyes or important details where common desktop UI elements will cover them.
- Do not add text, signatures, frames, or watermarks unless requested.
- Respect the source content. Do not infer sensitive traits or change a real person's identity.

## Review and delivery

Read [references/quality-checklist.md](references/quality-checklist.md) before final delivery. Generate at least one candidate per direction, inspect the full-resolution outputs, and revise defects that materially affect identity, anatomy, legibility, or wallpaper usability.

When local files are available, run:

```bash
python scripts/validate_images.py output-01.png output-02.png output-03.png --ratio 16:9
```

Deliver three separate full-resolution images with short labels. Briefly explain how each version uses the source evidence. Include prompts only when the user asks for them.
