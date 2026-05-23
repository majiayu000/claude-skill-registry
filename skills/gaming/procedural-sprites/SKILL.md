---
name: Procedural 2D Sprites & Pixel Art
description: |
  Use this skill to GENERATE 2D assets for ZX games.

  **Triggers:** "pixel art", "sprite sheet", "tileset", "autotile", "9-slice", "UI sprite", "health bar", "dithering", "indexed palette"

  **Before generating:** Check `.studio/visual-style.md` for project style specs.

  **Load references when:**
  - Project structure, multiple sprites → `generator-patterns` skill
  - Palette quantization → `references/palette-algorithms.md`
  - Dithering patterns → `references/dithering-patterns.md`
  - UI elements (9-slice, buttons) → `references/ui-sprites.md`
  - Tilesets/autotiles → `references/tileset-generation.md`
  - Sprite sheets/organization → `references/sprite-organization.md`

  For 3D TEXTURES: use `procedural-textures` skill.
version: 2.0.0
---

# Procedural 2D Sprites & Pixel Art

Generate 2D pixel art assets for ZX games: sprites, UI elements, tilesets, and sprite sheets.

## Output Requirements

- Format: PNG (RGBA or indexed)
- Color: Indexed palettes (4-256 colors) or full RGBA
- Compatible with: `draw_sprite()`, `draw_sprite_region()`

## Quick Decision Guide

| Need | Algorithm | Reference |
|------|-----------|-----------|
| Reduce colors | Median cut | `references/palette-algorithms.md` |
| Smooth gradients | Floyd-Steinberg | `references/dithering-patterns.md` |
| Retro look | Bayer ordered dither | `references/dithering-patterns.md` |
| Scalable panels | 9-slice | `references/ui-sprites.md` |
| Auto-connecting terrain | Autotile (16/47/256) | `references/tileset-generation.md` |
| Character animations | Sprite sheets | `references/sprite-organization.md` |

## Common Sprite Sizes

| Type | Size | Notes |
|------|------|-------|
| UI icon | 16x16, 32x32 | Power of 2 |
| Character | 32x32, 64x64 | 4-8 directions, 3-4 frames |
| Tile | 16x16, 32x32 | Must tile seamlessly |
| Health bar | 64x8, 128x12 | Segmented or continuous |

## Autotile Systems

| System | Tiles | Complexity | Use Case |
|--------|-------|------------|----------|
| 2-corner | 16 | Simple | Basic terrain |
| 4-corner | 47 | Medium | Standard RPG |
| Blob | 256 | Complex | Smooth transitions |

## Basic Palette Quantization

```python
from PIL import Image

def quantize_image(path, num_colors=16):
    """Quick palette extraction."""
    img = Image.open(path).convert('RGB')
    return img.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
```

For detailed algorithms, see `references/palette-algorithms.md`.

## Basic Dithering

```python
def apply_bayer_dither(img, palette):
    """Ordered dithering for retro look."""
    bayer = [[0,8,2,10], [12,4,14,6], [3,11,1,9], [15,7,13,5]]
    # Apply threshold matrix before quantizing
    # See references/dithering-patterns.md for full implementation
```

## ZX Integration

```toml
# nether.toml
[[assets.textures]]
id = "ui-sprites"
path = "generated/textures/ui_elements.png"
filter = "nearest"  # Critical for pixel art
```

```rust
// Drawing sprites
draw_sprite(sprites, x, y);

// Drawing from sprite sheet (e.g., button state 2)
draw_sprite_region(sprites, x, y, state * width, 0, width, height);
```

## File Organization

Author sprite sheets as texture specs under `.studio/specs/textures/` and generate with:

```bash
python .studio/generate.py --only textures
```

## References

- `references/palette-algorithms.md` - Median cut, k-means, quantization
- `references/dithering-patterns.md` - Bayer, Floyd-Steinberg, error diffusion
- `references/ui-sprites.md` - 9-slice, health bars, buttons
- `references/tileset-generation.md` - Autotiles, variations, animated tiles
- `references/sprite-organization.md` - Sprite sheets, palette swaps

## Related Skills

- `procedural-textures` - Noise algorithms for sprite bases
- `semantic-asset-language` - Style tokens for sprite generation
