---
name: Procedural Normal Map Generation for ZX
description: |
  Generate normal maps for ZX 3D meshes using Python + NumPy.

  **Triggers:** "generate normal map", "normal map", "bump map", "surface detail", "height to normal".

  **Before generating:** Check `.studio/visual-style.md` for relief intensity.

  **Load references when:**
  - Height-to-normal algorithms → `references/normal-map-generation.md`
  - Pattern generators (bricks, tiles, scratches) → `references/pattern-generators.md`
  - BC5 format, 2-channel encoding → `references/bc5-format.md`
  - Mesh integration, FFI usage → `references/integration-guide.md`

  **Related skills:**
  - ALBEDO/MRE/SSE: `procedural-textures`
  - MESH with tangents: `procedural-meshes`
version: 1.1.0
---

# Procedural Normal Map Generation

Generate tangent-space normal maps for surface detail without increasing geometry.

```bash
pip install pillow numpy pyfastnoiselite
```

## Output Requirements

- **Format:** PNG (RGB or RG)
- **Resolution:** Power of 2 (64, 128, 256, 512 max)
- **Naming:** `*_normal.png` (triggers auto-BC5 compression)
- **Color Space:** Linear (NOT sRGB)

## What Normal Maps Do

| Benefit | Cost |
|---------|------|
| Per-pixel lighting detail | +4 bytes/vertex (tangents) |
| Scratches, pores, fabric weave | Texture slot 3 |
| Enhanced specular/shadows | BC5: (w*h)/2 bytes |

## Tangent Space Channels

| Channel | Axis | Range | Meaning |
|---------|------|-------|---------|
| R | X (tangent) | 0-255 → [-1, 1] | Left/Right |
| G | Y (bitangent) | 0-255 → [-1, 1] | Up/Down |
| B | Z (normal) | Reconstructed | Forward |

**Neutral:** RGB(128, 128, 255) = no deviation

Z reconstructed in shader: `z = sqrt(1 - x² - y²)`

## Spec-Based Workflow

Create `.spec.py` in `.studio/specs/normals/`:

```python
NORMAL = {
    "normal": {
        "name": "brick_wall",
        "size": [256, 256],
        "method": "from_pattern",
        "pattern": {
            "type": "bricks",
            "brick_size": [64, 32],
            "mortar_depth": 0.35
        },
        "processing": {"strength": 1.2}
    }
}
```

Run: `python .studio/generate.py --only normals`

**Pattern types:** `bricks`, `tiles`, `hexagons`, `noise`, `scratches`, `rivets`, `weave`

## Height to Normal (Quick)

```python
import numpy as np
from PIL import Image

def height_to_normal(height_map: np.ndarray, strength: float = 1.0) -> np.ndarray:
    dx = np.roll(height_map, -1, axis=1) - np.roll(height_map, 1, axis=1)
    dy = np.roll(height_map, -1, axis=0) - np.roll(height_map, 1, axis=0)
    dx *= strength; dy *= strength

    normal = np.zeros((*height_map.shape, 3), dtype=np.float32)
    normal[:, :, 0] = -dx
    normal[:, :, 1] = -dy
    normal[:, :, 2] = 1.0

    length = np.maximum(np.sqrt(np.sum(normal**2, axis=2, keepdims=True)), 1e-8)
    normal /= length
    return ((normal + 1.0) * 0.5 * 255).astype(np.uint8)
```

See `references/pattern-generators.md` for brick, tile, scratch, rivet patterns.

## Strength Guidelines

| Material | Strength |
|----------|----------|
| Smooth plastic | 0.3 |
| Fabric/cloth | 0.5-0.8 |
| Stone/concrete | 1.0 |
| Brick/tile | 1.0-1.5 |
| Metal scratches | 1.5-2.5 |

## Memory Budget

| Resolution | BC5 Size |
|------------|----------|
| 64x64 | 2 KB |
| 128x128 | 8 KB |
| 256x256 | 32 KB |
| 512x512 | 128 KB |

## Integration Checklist

1. Mesh has tangent data (`export_tangents=True`)
2. Mesh has UVs
3. Mesh has normals
4. Texture named `*_normal.png`
5. FFI binds normal map

See `references/integration-guide.md` for complete workflow.
