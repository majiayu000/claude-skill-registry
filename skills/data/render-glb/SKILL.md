---
name: render-glb
description: 'Render GLB 3D models to PNG images for visual verification. Use when
  you need to SEE your generated 3D model, verify geometry, check visual correctness,
  or show results to users. Triggers on: render G'
---

---
name: render-glb
description: Render GLB 3D models to PNG images for visual verification. Use when you need to SEE your generated 3D model, verify geometry, check visual correctness, or show results to users. Triggers on: render GLB, preview model, visualize 3D, see my model, check geometry, visual verification, screenshot model, model preview.
---

# Render GLB to Image

Render 3D GLB files to PNG images so agents can **visually verify their work**.

## Zero-Setup with bunx

```bash
bunx render-glb model.glb output.png
```

No installation required. First run downloads the tool, subsequent runs are instant.

## Why This Matters

Agents can generate 3D models but typically can't see them. This creates a **visual verification loop**:

1. Generate model → export GLB
2. Render GLB → PNG
3. Read PNG → see what you built
4. Iterate if needed

## Basic Usage

```bash
# Render with defaults (good for most cases)
bunx render-glb model.glb preview.png

# Then read the image to see your work
# (use Read tool on preview.png)
```

## Options

```bash
bunx render-glb <input.glb> <output.png> [options]

Options:
  --width <n>      Image width in pixels (default: 800)
  --height <n>     Image height in pixels (default: 600)
  --background <hex>  Background color (default: #808080)
```

## Visual Verification Workflow

When building 3D models, use this pattern:

```python
# 1. Build your model
from build123d import Box, Sphere, export_gltf
model = Box(20, 20, 20) + Sphere(radius=15)
export_gltf(model, "./model.glb", binary=True)
```

```bash
# 2. Render to image
bunx render-glb model.glb preview.png
```

```
# 3. Read the image (using Read tool)
# Now you can SEE what you built and verify it's correct
```

## Integration with CAD Skills

This skill complements:
- **build123d** - Python CAD modeling
- Any tool that exports GLB format

Typical workflow:
1. Use CAD skill to generate geometry
2. Export to GLB
3. Use render-glb to verify visually
4. Iterate if model isn't correct

## Links

- npm: https://www.npmjs.com/package/render-glb
- GitHub: https://github.com/rawwerks/render-glb
