---
name: sprite-forge
description: "Generate game sprites, SVG characters, ASCII art, animated mascots, and isometric turnarounds from images or descriptions. Covers 5 output modes: SVG characters (Gemini code-gen or pixel-art rects), game sprite sheets (with atlas metadata), 8-way isometric turnarounds (chongdashu pipeline), ASCII/Unicode terminal art, and GSAP-animated mascots. This skill should be used when creating pixel art, sprite sheets, walk cycles, character turnarounds, SVG icons, ASCII art, or animated mascots. Triggers on: sprite, pixel art, SVG character, ASCII art, mascot, sprite sheet, isometric, walk cycle, turnaround, game asset, character animation."
argument-hint: "[description or image path] [--mode svg|sprite|isometric|ascii|mascot]"
---

# Sprite Forge

Generate game-ready sprites, SVG characters, ASCII art, animated mascots, and isometric turnarounds from images or text descriptions. Five output modes, each with proven pipelines.

## When to Use

- Creating pixel-art characters or converting images to pixel art
- Generating sprite sheets with walk cycles, idle, attack animations
- Building 8-way isometric character turnarounds for tactics/RPG games
- Producing clean, hand-editable SVG characters or icons
- Converting images to ASCII/Unicode terminal art
- Animating mascots with GSAP walk, bounce, wave, or typing presets
- Generating lil-agents macOS dock companion videos

**When not to use agents**: Each pipeline is sequential — generate image, then process, then stitch. Work directly rather than spawning subagents, because intermediate outputs from one step feed the next. Parallel agents only help when generating multiple independent characters simultaneously.

## Quick Start

```bash
# Isometric 8-way turnaround from a character image
python3 scripts/isometric_pipeline.py --reference character.png --output-dir ./iso/

# Video walk cycle → game sprite sheet with atlas
python3 scripts/video_to_spritesheet.py --input walk.mp4 --fps 12 --cell-size 64x64 --atlas json

# Image → pixel-art SVG mascot with walk animation
magick input.png -fuzz 15% -trim +repage /tmp/trimmed.png
python3 scripts/pixel_art_generator.py /tmp/trimmed.png --grid 20 --colors 4 --merge --remove-bg -o mascot.svg
python3 scripts/animation_builder.py --preset walk-and-bounce --svg-id mascot

# Image → terminal ASCII art
python3 scripts/image_to_ascii.py input.png --mode color --width 80

# Stitch frames into a sprite sheet with atlas
python3 scripts/stitch_spritesheet.py --input-dir frames/ --cols 8 --atlas json -o sheet.png

# Remove green screen background
python3 scripts/chroma_key.py --input sprite.png --output sprite_alpha.png --despill
```

## Pipeline 1: Isometric Turnaround

Generate an 8-way directional character sprite from a single reference image. Based on chongdashu's FFT-style pipeline (github.com/chongdashu/vibe-isometric-sprites, Mar 2026).

**Core insight**: Never generate all 8 directions at once — generate 4 cardinals, then derive 4 diagonals.

```bash
python3 scripts/isometric_pipeline.py \
  --reference portrait.png \
  --character-desc "young adventurer, red scarf, blue tunic, leather belts" \
  --output-dir ./iso-output/ \
  --chroma-key
```

Steps orchestrated by the script:
1. Reference → full-body asset (identity anchor)
2. Full-body → isometric anchor (¾ view, facing down-right)
3. Apply chroma key green (`#00FF00`) for Nano Banana models
4. Generate 4 cardinal directions (N/E/S/W) as 2×2 sheet
5. Generate 4 diagonals (NE/NW/SE/SW) from anchor + cardinals
6. Optionally generate walk cycle via video model
7. Normalize, crop, stitch into final 8-direction sprite sheet

See `references/isometric-turnaround.md` for the full prompt library and model comparison.

## Pipeline 2: Video to Sprite Sheet

Convert animation videos into game-ready sprite sheets. The proven approach for walk cycles because image models lack temporal coherence for multi-frame animation.

```bash
python3 scripts/video_to_spritesheet.py \
  --input walk_cycle.mp4 \
  --fps 12 --cell-size 64x64 \
  --remove-bg rembg \
  --cols 8 --atlas json \
  --output walk_sheet.png
```

Produces: `walk_sheet.png` + `walk_sheet.json` (atlas with frame coordinates for Phaser/Unity/Godot).

See `references/video-to-spritesheet.md` for practitioner workflows and engine integration.

## Pipeline 3: SVG Character Generation

Two approaches depending on the output needed:

**Gemini SVG-as-code** — Clean, hand-editable vector SVGs with CSS custom properties. Gemini 3.1 Pro writes raw XML, not traced raster. Use for icons, logos, simple characters, interactive SVGs. Generate via nano-banana-pro with a prompt requesting SVG XML output. See `references/gemini-svg-generation.md`.

**Pixel-art rect SVGs** — Retro pixel-art characters built entirely from `<rect>` elements. Use when targeting GSAP animation or the ayotomcs-style mascot aesthetic.

```bash
magick input.png -fuzz 15% -trim +repage /tmp/trimmed.png
python3 scripts/pixel_art_generator.py /tmp/trimmed.png --grid 20 --colors 4 --merge --remove-bg -o char.svg
```

Design constraints for animatable pixel-art characters:
- **Standing pose, side view** — legs must be distinct blocks so walk cycle `scaleY` squash works on them independently
- **4-6 colors max** — fewer colors produces cleaner quantization and more iconic, readable sprites at small sizes
- **Symmetric body parts** — left/right hand and leg pairs enable GSAP alternating animation without per-frame redrawing
- **Grid size 16-24** — below 16 the character loses recognizable features; above 24 it stops reading as pixel art

See `references/pixel-art-svgs.md` for the rect conversion technique.

## Pipeline 4: ASCII Art

Convert images to terminal-renderable character art.

```bash
# Grayscale density ramp
python3 scripts/image_to_ascii.py photo.png --mode gray --width 80

# Color Unicode half-block (▀▄█)
python3 scripts/image_to_ascii.py photo.png --mode color --width 120

# jp2a wrapper (if installed)
python3 scripts/image_to_ascii.py photo.png --mode jp2a --width 80
```

See `references/ascii-art-techniques.md` for character sets, density ramps, and color modes.

## Pipeline 5: Animated Mascot

The ayotomcs-derived pipeline. Convert images to pixel-art SVG characters and animate with GSAP timelines.

```bash
# Generate SVG
python3 scripts/pixel_art_generator.py trimmed.png --grid 24 --colors 6 --merge --remove-bg -o mascot.svg

# Add animation preset
python3 scripts/animation_builder.py --preset walk-and-bounce --svg-id mascot

# Assemble standalone HTML demo
python3 scripts/animation_builder.py --preset walk-and-bounce --svg-id mascot --standalone -o mascot.html
```

**Presets**: `idle`, `bounce`, `lean`, `wave`, `walk`, `walk-and-bounce`, `walk-and-wave`, `typing`

**Output formats**: `standalone` (HTML + GSAP CDN), `react` (TSX component), `svg-only` (SMIL fallback)

**Frame-by-frame**: For complex choreography, generate N SVG frames as `<g>` groups, then use `generate_frame_switcher()` from `animation_builder.py` with variable timing.

### lil-agents Dock Companion

Generate transparent HEVC walk cycle videos for the lil-agents macOS dock app:

```bash
python3 scripts/generate_walk_video.py spritesheet.png --cols 6 --name robot
# Output: walk-robot-01.mov (1080x1920, HEVC with alpha, ~10s)
```

See `references/lil-agents-character-spec.md` for the full format spec and `references/gsap-timeline-patterns.md` for animation recipes.

## Model Selection Guide

| Task | Best Model | Why |
|------|-----------|-----|
| Identity preservation (anchor) | GPT Image 1.5 | Best at maintaining character features across edits |
| Direction sheets (N/E/S/W) | Nano Banana 2 | Good isometric style, cheaper, fast |
| True transparent background | GPT Image 1.5 | Only model that reliably produces alpha |
| Walk cycle animation | Veo 3.1 (video) | Image models have zero temporal coherence |
| Clean vector SVG | Gemini 3.1 Pro | Writes SVG as code, not traced raster |
| Pixel-art reference image | Nano Banana Pro | Good at retro game art styles |

## Gotchas

**ImageMagick trim is mandatory.** AI-generated images have large white borders. Without `magick -fuzz 15% -trim`, the character occupies <10% of the grid. Always trim before converting.

**Nano Banana can't do true transparency.** Use chroma key `#00FF00` green and remove with `chroma_key.py`. Do NOT use magenta — it contaminates warm costume colors. See `references/chroma-key-transparency.md`.

**Never generate all 8 isometric directions at once.** Results are inconsistent. Generate 4 cardinals, then derive diagonals from anchor + cardinals.

**Walk animation requires standing characters.** Auto-grouping puts bottom 30% of rects into `legs`. For sitting characters, use `idle` or `bounce` presets.

**SVG id required for GSAP.** Add `id="mascot"` to the root `<svg>` before animation.

**Near-white quantization.** JPEG sources produce near-white colors that background removal misses. Use `--colors 4` or PNG sources with true transparent backgrounds.

## Dependencies

- **Pillow**: `uv pip install Pillow` (all pipelines)
- **ImageMagick 7**: Pre-processing (`magick -trim`, `-fuzz`)
- **ffmpeg**: Video frame extraction (Pipeline 2)
- **rembg**: Background removal (optional, `uv pip install rembg`)
- **jp2a**: ASCII art (optional, `brew install jp2a`)
- **GSAP 3**: Via CDN in standalone HTML templates (Pipeline 5)
- **nano-banana-pro skill**: AI image generation/editing

## Reference

- `references/isometric-turnaround.md` — Chongdashu 8-way turnaround prompts and methodology
- `references/chroma-key-transparency.md` — Model-specific transparency handling
- `references/video-to-spritesheet.md` — Video-first animation workflow
- `references/gemini-svg-generation.md` — Gemini SVG-as-code prompt patterns
- `references/ascii-art-techniques.md` — ASCII/Unicode art techniques
- `references/sprite-generation-landscape.md` — Tool comparison (SEELE, Ludo, SpriteCook, etc.)
- `references/pixel-art-svgs.md` — Pixel grid to SVG rect conversion
- `references/gsap-timeline-patterns.md` — GSAP animation recipes
- `references/ayotomcs-deconstruction.md` — Original ayotomcs.me reference deconstruction
- `references/lil-agents-character-spec.md` — lil-agents video format spec
