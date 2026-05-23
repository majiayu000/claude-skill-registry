---
name: Procedural Texture Generation for ZX
description: |
  Generate textures for ZX 3D meshes using Python + NumPy + FastNoiseLite.

  **Triggers:** "generate texture", "procedural texture", "noise pattern", "MRE texture", "albedo", "matcap", "seamless texture".

  **Before generating:** Check `.studio/visual-style.md` for project style specs.

  **Load references when:**
  - Render modes (0-3), MRE/SSE → `references/render-modes.md`
  - Noise algorithms → `references/noise-algorithms.md`
  - Material recipes → `references/material-recipes.md`
  - Matcap library → `references/matcap-generation.md`
  - Layer composition → `references/layer-system.md`
  - Atlas packing → `references/atlas-packing.md`
  - Seamless tiling → `references/seamless-textures.md`
  - Project structure → `generator-patterns` skill

  **Related skills:**
  - NORMAL MAPS: `procedural-normal-maps`
  - UV-AWARE TEXTURING: `mesh-texturing-workflows`
  - 2D SPRITES: `procedural-sprites`
version: 2.3.0
---

# Procedural Texture Generation

Generate game-ready textures using Python with Pillow, NumPy, and FastNoiseLite.

```bash
pip install pillow numpy pyfastnoiselite
```

## Output Requirements

- **Format:** PNG (RGBA or RGB)
- **Resolution:** Power of 2 (64, 128, 256, 512 max)
- **Aesthetic:** Low Poly / N64 / PS1 / PS2 era

## Render Mode Quick Reference

| Mode | Maps | Use Case |
|------|------|----------|
| 0 | Albedo | UI, sprites, flat-shaded |
| 1 | Albedo + Matcaps | Stylized toon |
| 2 | Albedo + MRE | Modern PBR |
| 3 | Albedo + SSE + Specular | Retro PS1/N64 |

See `references/render-modes.md` for complete mode documentation.

## Quick Start

Create a texture spec under `.studio/specs/textures/` and run the unified generator.

## Noise Algorithms

| Algorithm | Best For |
|-----------|----------|
| Perlin | Smooth organic patterns |
| Simplex | Faster Perlin, fewer artifacts |
| Cellular | Cells, cracks, scales |
| Value | Hard-edged noise |
| Fractal FBM | Complex organic detail |

See `references/noise-algorithms.md` for complete reference.

## Multi-Layer Composition

```
1. BASE: Solid color + subtle noise
2. DETAIL: Perlin/Simplex overlay
3. FEATURES: Scratches, cracks, grain
4. WEATHERING: Rust, stains, dust
5. FINAL: Contrast, color grading
```

See `references/layer-system.md` for layer system details.

## Spec-Based Workflow

Create `.spec.py` files for deterministic generation:

```python
TEXTURE = {
    "texture": {
        "name": "wood_plank",
        "size": [256, 256],
        "layers": [
            {"type": "solid", "color": 0.5},
            {"type": "wood_grain", "ring_count": 12, "blend": "multiply"},
            {"type": "noise", "noise_type": "perlin", "scale": 0.15, "opacity": 0.3}
        ],
        "color_ramp": ["#4A3728", "#6B4423", "#8B4513"]
    }
}
```

Run: `python .studio/generate.py --only textures`

**Layer types:** `solid`, `noise`, `gradient`, `wood_grain`, `brick`, `checkerboard`, `stripes`
**Blend modes:** `normal`, `multiply`, `add`, `screen`, `overlay`, `soft_light`

## Console Constraints

| Constraint | Limit |
|------------|-------|
| Max resolution | 512 x 512 |
| Sizes | Power of 2 |
| VRAM budget | 4MB total |

## File Organization

```
.studio/specs/textures/
├── wood_plank.spec.py
└── metal_brushed.spec.py

generated/textures/
├── wood_plank.png
└── metal_brushed.png
```

See `generator-patterns` skill for full project setup.
