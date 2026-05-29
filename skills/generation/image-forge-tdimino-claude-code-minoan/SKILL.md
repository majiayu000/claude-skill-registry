---
name: image-forge
description: Precision image editing using ImageMagick 7, sips, rembg, and Pillow with intelligent routing to AI semantic editing (Gemini/nano-banana-pro) for content-aware operations. This skill should be used when performing any image manipulation task including cropping, resizing, compositing, annotating, format conversion, color adjustment, batch processing, montage creation, or when combining deterministic edits with AI-powered semantic edits.
---

# Image Forge

Pixel-precise image editing with three-tier routing: deterministic CLI tools for exact operations, AI models for semantic edits, vision models for analysis.

## Routing Decision

**Use AI when the edit requires understanding what is in the image. Use ImageMagick when the edit requires knowing exactly what to do to the pixels.**

### Tier 1: Deterministic (magick, sips, rembg)

Use for operations with exact, numeric parameters:

| Task | Tool | Command |
|------|------|---------|
| Resize to exact dimensions | magick | `magick in.jpg -resize 800x600! out.jpg` |
| Resize fit (preserve aspect) | magick | `magick in.jpg -resize 800x600 out.jpg` |
| Resize fill + crop | magick | `magick in.jpg -resize 800x600^ -gravity center -extent 800x600 out.jpg` |
| Resize shrink only | magick | `magick in.jpg -resize '800x600>' out.jpg` |
| Crop at offset | magick | `magick in.jpg -crop 600x400+100+50 +repage out.jpg` |
| Center crop | magick | `magick in.jpg -gravity center -crop 600x400+0+0 +repage out.jpg` |
| Auto-trim whitespace | magick | `magick in.jpg -fuzz 10% -trim +repage out.jpg` |
| Format convert | magick | `magick in.png -quality 85 out.jpg` |
| Add text | magick | `magick in.jpg -fill white -pointsize 36 -annotate +10+50 'Text' out.jpg` |
| Composite overlay | magick | `magick bg.png fg.png -geometry +50+100 -composite out.png` |
| Watermark | magick | `magick photo.jpg wm.png -gravity SouthEast -geometry +10+10 -compose Dissolve -define compose:args=25 -composite out.jpg` |
| Adjust brightness/contrast | magick | `magick in.jpg -brightness-contrast 10x20 out.jpg` |
| Adjust saturation | magick | `magick in.jpg -modulate 100,130,100 out.jpg` |
| Grayscale | magick | `magick in.jpg -colorspace Gray out.jpg` |
| Sepia | magick | `magick in.jpg -sepia-tone 80% out.jpg` |
| Blur | magick | `magick in.jpg -blur 0x3 out.jpg` |
| Sharpen | magick | `magick in.jpg -sharpen 0x1 out.jpg` |
| Remove background | rembg | `rembg i in.jpg out.png` |
| Strip metadata | magick | `magick in.jpg -strip out.jpg` |
| Set DPI | magick | `magick in.jpg -density 300 out.jpg` |
| Batch resize | `batch_ops.py` | `python3 scripts/batch_ops.py *.jpg --op resize --width 800 --output resized/` |
| Montage/contact sheet | magick | `magick montage *.jpg -geometry 200x200+5+5 -tile 4x out.jpg` |
| Quick format convert (macOS) | sips | `sips -s format jpeg in.png --out out.jpg` |
| Quick resize (macOS) | sips | `sips -Z 800 in.jpg --out out.jpg` |

### Tier 2: AI Semantic (nano-banana-pro / Gemini)

Delegate to the `nano-banana-pro` skill when the edit requires understanding image content:

- Remove a person/object from a photo
- Change sky, weather, time of day
- Apply artistic style transfer
- Inpaint/outpaint regions
- Generate new image from scratch
- Content-aware fill after object removal

### Tier 3: Vision Analysis (Claude Read tool)

Use the Read tool to inspect images before/after edits:

- Verify an edit succeeded
- Describe image contents
- Check composition and framing
- Identify colors, objects, text in image

## Scripts

All scripts are in `~/.claude/skills/image-forge/scripts/`. Run with `python3`.

### image_info.py — Inspect Image Metadata

```bash
python3 ~/.claude/skills/image-forge/scripts/image_info.py photo.jpg
python3 ~/.claude/skills/image-forge/scripts/image_info.py photo.jpg --field dimensions
python3 ~/.claude/skills/image-forge/scripts/image_info.py photo.jpg --field width
```

Returns clean JSON: dimensions, format, color space, depth, alpha, DPI, ICC profile, EXIF.

### image_pipeline.py — Declarative Edit Pipeline

Write a JSON spec, get a single chained `magick` command. No intermediate files.

```bash
# Create spec
cat > /tmp/pipeline.json << 'EOF'
{
    "input": "photo.jpg",
    "output": "result.png",
    "steps": [
        {"op": "resize", "width": 800, "height": 600, "mode": "fill"},
        {"op": "brightness_contrast", "brightness": 5, "contrast": 10},
        {"op": "annotate", "text": "Title", "gravity": "South", "pointsize": 36, "fill": "white", "stroke": "black", "strokewidth": 2},
        {"op": "composite", "overlay": "watermark.png", "gravity": "SouthEast", "opacity": 25},
        {"op": "quality", "value": 90},
        {"op": "strip"}
    ]
}
EOF

# Dry run (print command)
python3 ~/.claude/skills/image-forge/scripts/image_pipeline.py /tmp/pipeline.json --dry-run

# Execute
python3 ~/.claude/skills/image-forge/scripts/image_pipeline.py /tmp/pipeline.json
```

**Available operations:**

| Op | Parameters |
|----|-----------|
| `resize` | `width`, `height`, `mode` (fit/fill/exact/shrink/enlarge/percent), `filter` |
| `crop` | `w`/`width`, `h`/`height`, `x`, `y`, `gravity` |
| `trim` | `fuzz` (%) |
| `annotate` | `text`, `font`, `pointsize`, `fill`, `stroke`, `strokewidth`, `gravity`, `x`, `y` |
| `composite` | `overlay`, `gravity`, `x`, `y`, `opacity`, `compose`, `resize` |
| `rotate` | `angle`, `background` |
| `blur` | `sigma`, `radius` |
| `sharpen` | `sigma`, `radius` |
| `unsharp` | `sigma`, `radius`, `amount`, `threshold` |
| `modulate` | `brightness`, `saturation`, `hue` (100 = no change) |
| `brightness_contrast` | `brightness`, `contrast` |
| `levels` | `black`, `white`, `gamma` |
| `gamma` | `value` |
| `sigmoidal_contrast` | `strength`, `midpoint` |
| `colorize` | `color`, `amount` (%) |
| `sepia` | `threshold` (%) |
| `grayscale` | (none) |
| `negate` | (none) |
| `auto_level` | (none) |
| `normalize` | (none) |
| `auto_orient` | (none) |
| `flip` / `flop` | (none) |
| `border` | `color`, `size` |
| `extent` | `width`, `height`, `background`, `gravity` |
| `shadow` | `opacity`, `sigma`, `x`, `y` |
| `transparent` | `color`, `fuzz` (%) |
| `alpha_remove` | `background` |
| `alpha_set` | (none) |
| `quality` | `value` (1-100) |
| `strip` | (none) |
| `density` | `value` (DPI) |
| `draw` | `primitive`, `fill`, `stroke`, `strokewidth` |
| `raw` | `args` (string or array of raw magick args) |

### smart_crop.py — Gravity-Based Smart Crop

```bash
python3 ~/.claude/skills/image-forge/scripts/smart_crop.py photo.jpg --target 800x600
python3 ~/.claude/skills/image-forge/scripts/smart_crop.py photo.jpg --target 800x600 --gravity north
python3 ~/.claude/skills/image-forge/scripts/smart_crop.py photo.jpg --target 1080x1080 --output cropped/
python3 ~/.claude/skills/image-forge/scripts/smart_crop.py photo.jpg --target 800x600 --dry-run
```

Gravities: `center`, `north`, `south`, `east`, `west`, `northwest`, `northeast`, `southwest`, `southeast`.

### batch_ops.py — Parallel Batch Processing

```bash
python3 ~/.claude/skills/image-forge/scripts/batch_ops.py *.jpg --op resize --width 800 --output resized/
python3 ~/.claude/skills/image-forge/scripts/batch_ops.py *.png --op format --to jpg --quality 85 --output converted/
python3 ~/.claude/skills/image-forge/scripts/batch_ops.py *.jpg --op thumbnail --width 200 --height 200 --output thumbs/
python3 ~/.claude/skills/image-forge/scripts/batch_ops.py *.jpg --op strip --output clean/
python3 ~/.claude/skills/image-forge/scripts/batch_ops.py *.jpg --op watermark --overlay wm.png --opacity 25 --output marked/
python3 ~/.claude/skills/image-forge/scripts/batch_ops.py *.jpg --op resize --width 800 --parallel 8 --output resized/
```

Operations: `resize`, `thumbnail`, `format`, `strip`, `auto_orient`, `watermark`, `crop`.

### montage_builder.py — Contact Sheets

```bash
python3 ~/.claude/skills/image-forge/scripts/montage_builder.py *.jpg --output contact.jpg
python3 ~/.claude/skills/image-forge/scripts/montage_builder.py *.jpg --cols 3 --thumb 300x300 --label --output grid.jpg
python3 ~/.claude/skills/image-forge/scripts/montage_builder.py *.jpg --background '#1a1a2e' --border 2 --output dark_grid.jpg
```

## Quick Recipes

### Social Media Crops

```bash
# Instagram square
magick in.jpg -resize 1080x1080^ -gravity center -extent 1080x1080 instagram.jpg

# Instagram story
magick in.jpg -resize 1080x1920^ -gravity center -extent 1080x1920 story.jpg

# Twitter/X header
magick in.jpg -resize 1500x500^ -gravity center -extent 1500x500 header.jpg

# OG image
magick in.jpg -resize 1200x630^ -gravity center -extent 1200x630 og.jpg
```

### Watermark

```bash
# Text watermark
magick photo.jpg -fill 'rgba(255,255,255,0.3)' -gravity SouthEast \
  -font Helvetica -pointsize 24 -annotate +10+10 '© 2026' out.jpg

# Image watermark at 25%
magick photo.jpg wm.png -gravity SouthEast -geometry +10+10 \
  -compose Dissolve -define compose:args=25 -composite out.jpg
```

### Borders and Shadows

```bash
# Solid border
magick in.jpg -bordercolor '#333' -border 10 out.jpg

# Drop shadow
magick in.png \( +clone -background black -shadow 60x5+5+5 \) \
  +swap -background none -layers merge +repage shadow.png
```

### Color Effects

```bash
# Vintage
magick in.jpg -modulate 105,80,100 -fill '#704214' -colorize 15% \
  -sigmoidal-contrast 3x60% vintage.jpg

# High contrast B&W
magick in.jpg -colorspace Gray -sigmoidal-contrast 10x50% bw.jpg
```

## Geometry Syntax Quick Reference

| Syntax | Meaning |
|--------|---------|
| `800x600` | Fit within box, preserve aspect |
| `800x600!` | Force exact (distort) |
| `800x600>` | Shrink only if larger |
| `800x600<` | Enlarge only if smaller |
| `800x600^` | Fill box (minimum dimension matches) |
| `50%` | Scale by percentage |
| `+X+Y` | Offset from gravity anchor |

**Shell escaping**: Quote geometry with `>`, `<`, `^`:
```bash
magick in.jpg -resize '800x600>' out.jpg
```

## Critical Reminders

1. **Always `+repage` after `-crop`** — Virtual canvas offset persists without it
2. **`-modulate` order is B,S,H** — Brightness, Saturation, Hue (not H,S,L)
3. **Settings persist, operators execute immediately** — Order matters in magick commands
4. **Use `rembg` for background removal** — `rembg i input.jpg output.png` (add `-a` for alpha matting)
5. **Quote geometry** — `>`, `<`, `^` are shell metacharacters
6. **`-alpha off` is permanent in IM7** — Use `-alpha deactivate`/`-alpha activate` for temporary toggle
7. **Inspect before editing** — Run `image_info.py` first to know dimensions, format, alpha state
8. **Pipeline for multi-step** — Use `image_pipeline.py` instead of chaining shell commands

## References

Detailed references in `~/.claude/skills/image-forge/references/`:

- `magick-reference.md` — Complete ImageMagick 7 command reference (resize, crop, color, text, drawing, batch, identify)
- `compositing.md` — All compositing operators (Duff-Porter, mathematical, lighting, HSL, special)
- `recipes.md` — 30+ recipes (borders, shadows, watermarks, social sizing, color effects, sprites, batch patterns)

## Dependencies

| Tool | Version | Install |
|------|---------|---------|
| ImageMagick | 7.1.2-7 (Q16-HDRI) | `brew install imagemagick` |
| rembg | 2.0.72 | `uv pip install rembg` |
| sips | macOS built-in | — |
| Pillow | 10.4.0 | `uv pip install Pillow` |
