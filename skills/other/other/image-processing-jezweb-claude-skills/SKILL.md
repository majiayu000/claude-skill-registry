---
name: image-processing
description: "Process images for web development — resize, crop, trim whitespace, convert formats (PNG/WebP/JPG), optimise file size, generate thumbnails, create OG card images. Uses Pillow (Python) — no ImageMagick needed. Trigger with 'resize image', 'convert to webp', 'trim logo', 'optimise images', 'make thumbnail', 'create OG image', 'crop whitespace', 'process image', or 'image too large'."
compatibility: claude-code-only
---

# Image Processing

Process images for web development. Generate a Pillow script adapted to the user's environment and specific needs.

## Prerequisites

Pillow is usually pre-installed. If not:

```bash
pip install Pillow
```

If Pillow is unavailable, adapt using alternatives:

| Alternative | Platform | Install | Capabilities |
|-------------|----------|---------|-------------|
| `sips` | macOS (built-in) | None | Resize, convert (no trim/OG) |
| `sharp` | Node.js | `npm install sharp` | Full feature set |
| `ffmpeg` | Cross-platform | `brew install ffmpeg` | Resize, convert |

## Capabilities

Generate a Python script using Pillow for any of these operations. See `references/pillow-patterns.md` for implementation patterns, especially RGBA-to-JPG compositing and cross-platform font discovery.

### Resize

Scale to specific dimensions or by width/height (maintain aspect ratio if only one given). Use `Image.LANCZOS` for high-quality downscaling.

### Convert Format

Convert between PNG, JPG, WebP. Handle RGBA-to-JPG by compositing onto white background. Apply format-specific quality settings (WebP: 85, JPG: 90, PNG: optimize).

### Trim Whitespace

Auto-crop surrounding whitespace from logos and icons. Convert to RGBA first, then use `getbbox()` to find content bounds.

### Thumbnail

Fit within max dimensions while maintaining aspect ratio. Use `img.thumbnail((size, size), Image.LANCZOS)`.

### Optimise for Web

Resize + compress in one step. Convert to WebP for best compression. Typical settings: width 1920, quality 85.

### OG Card (1200x630)

Generate Open Graph card with title/subtitle overlay on a background image or solid colour. Apply semi-transparent overlay for text readability. Centre text horizontally.

## Common Workflows

### Logo Cleanup (client-supplied JPG with white background)

1. Trim whitespace
2. Convert to PNG (for transparency)
3. Create favicon-sized version (thumbnail at 512px)

### Prepare Hero Image for Production

Resize to max width 1920, convert to WebP, compress at quality 85.

### Batch Process

For multiple images, generate a single script that loops over all files rather than processing one at a time.

## Pipeline with Gemini Image Gen

Generate images with the gemini-image-gen skill, then process them:

1. Generate with Gemini (raw PNG output)
2. User picks favourite
3. Optimise: resize to target width, convert to WebP, compress

## Output Format Guide

| Use case | Format | Why |
|----------|--------|-----|
| Photos, hero images | WebP | Best compression, wide browser support |
| Logos, icons (need transparency) | PNG | Lossless, supports alpha |
| Fallback for older browsers | JPG | Universal support |
| Thumbnails | WebP or JPG | Small file size priority |
| OG cards | PNG | Social platforms handle PNG best |

## Reference Files

| When | Read |
|------|------|
| Implementing any Pillow operation | [references/pillow-patterns.md](references/pillow-patterns.md) |
