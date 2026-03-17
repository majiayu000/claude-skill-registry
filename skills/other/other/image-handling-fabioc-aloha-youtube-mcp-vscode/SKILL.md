---
name: "Image Handling Skill"
description: "Right format, right size, right quality — plus AI image generation via Replicate"
applyTo: "**/*.png,**/*.jpg,**/*.jpeg,**/*.webp,**/*.svg,**/*.ico,**/*image*,**/*banner*,**/*icon*,**/*avatar*,**/*photo*"
triggers:
  - "convert svg"
  - "convert png"
  - "convert to png"
  - "convert to jpg"
  - "convert logo"
  - "logo to png"
  - "svg to png"
  - "png to jpg"
  - "image conversion"
  - "resize image"
  - "optimize image"
  - "banner"
  - "screenshot"
  - "rasterize"
  - "make png"
  - "export as png"
  - "export png"
  - "marketplace logo"
  - "marketplace icon"
  - "favicon"
  - "sharp-cli"
  - "generate image"
  - "create image"
  - "make image"
  - "replicate"
  - "flux"
  - "ai image"
  - "edit image"
  - "transform image"
  - "upscale"
  - "enhance image"
  - "flux schnell"
  - "flux dev"
  - "flux pro"
  - "flux 1.1"
  - "ideogram"
  - "ideogram v2"
  - "stable diffusion"
  - "sdxl"
  - "seedream"
  - "which model"
  - "best model for image"
  - "choose model"
  - "text in image"
  - "image with text"
  - "replicate model"
  - "run model"
  - "generate with replicate"
---

# Image Handling Skill

> Right format, right size, right quality.

## Format Selection

| Format | Best For | Supports |
| ------ | -------- | -------- |
| SVG | Icons, logos, diagrams | Infinite scale, animation |
| PNG | Screenshots, transparency | Lossless, alpha channel |
| JPEG | Photos, gradients | Small size, no transparency |
| WebP | Web images | Best compression, both |
| ICO | Favicons | Multi-resolution |

## Conversion Commands

```powershell
# SVG to PNG using sharp-cli (recommended)
# --density sets DPI for vector rendering (150 = crisp text)
npx sharp-cli -i input.svg -o output-folder/ --density 150 -f png

# Note: output must be a directory, filename preserved from input
npx sharp-cli -i banner.svg -o assets/ --density 150 -f png
# Creates: assets/banner.png

# ImageMagick (if installed)
magick input.svg -resize 512x512 output.png
magick input.png -quality 85 output.jpg

# Multiple sizes
foreach ($size in 16,32,64,128,256,512) {
  magick input.svg -resize ${size}x${size} "icon-$size.png"
}
```

## SVG to PNG Tips

- **Emojis don't convert well** - Use text-only or SVG icons
- **Use `--density 150+`** for crisp text rendering
- **Check file size** - README banners should be < 500KB

## GitHub README Images

```markdown
<!-- Absolute URL (always works) -->
![Banner](https://raw.githubusercontent.com/user/repo/main/assets/banner.svg)

<!-- Relative (works in repo) -->
![Banner](./assets/banner.png)

<!-- With dark/light variants -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="banner-dark.svg">
  <img src="banner-light.svg" alt="Banner">
</picture>
```

## Size Guidelines

| Use Case | Max Size | Recommended |
| -------- | -------- | ----------- |
| README banner | 500KB | < 100KB |
| Documentation | 200KB | < 50KB |
| Icons | 50KB | < 10KB |
| Favicon | 10KB | < 5KB |

## Optimization

```powershell
# PNG optimization
pngquant --quality=65-80 input.png -o output.png

# JPEG optimization
jpegoptim --max=85 input.jpg

# SVG optimization
npx svgo input.svg -o output.svg
```

## Batch Processing

```powershell
# Convert all SVGs to PNGs
Get-ChildItem *.svg | ForEach-Object {
  $out = $_.BaseName + ".png"
  magick $_.Name -resize 256x256 $out
}
```

## Replicate Model Selection

Match user intent to the right model. When a user names a specific model or describes a need, use this table.

| Model | Replicate ID | Cost | Best For | Trigger Words |
|-------|-------------|------|----------|---------------|
| **Flux Schnell** | `black-forest-labs/flux-schnell` | $0.003 | Fast iteration, prototyping | "flux schnell", "quick image", "fast generation" |
| **Flux Dev** | `black-forest-labs/flux-dev` | $0.025 | High quality no-text images | "flux dev", "high quality image" |
| **Flux 1.1 Pro** | `black-forest-labs/flux-1.1-pro` | $0.04 | Production, photorealistic | "flux pro", "flux 1.1", "production image" |
| **Ideogram v2** | `ideogram-ai/ideogram-v2` | $0.08 | Text in images, typography banners | "ideogram", "text in image", "image with text", "banner" |
| **Ideogram v2 Turbo** | `ideogram-ai/ideogram-v2-turbo` | $0.05 | Fast typography | "ideogram turbo", "fast text image" |
| **SDXL** | `stability-ai/sdxl` | $0.009 | Classic diffusion, LoRA styles | "sdxl", "stable diffusion", "stable diffusion xl" |
| **Seedream 5 Lite** | `bytedance/seedream-5-lite` | varies | 2K/3K with built-in reasoning | "seedream", "bytedance", "high resolution" |

### Model Selection Guide

- **"quick" / "test" / "prototype"** → Flux Schnell ($0.003, 4 steps)
- **"high quality" / "production"** → Flux 1.1 Pro ($0.04)
- **Text must appear in the image** → Ideogram v2 (only model with crystal-clear typography)
- **Painting style / custom LoRA** → SDXL or Flux Dev with LoRA weights
- **Largest / highest resolution output** → Seedream 5 Lite (2K or 3K)
- **README banner with text** → Ideogram v2 with `3:1` ratio; see `ai-generated-readme-banners` skill
- **README banner without text** → Flux 1.1 Pro with `21:9` ratio

### LoRA Support (Flux Dev / SDXL)

Both Flux Dev and SDXL accept LoRA weights:

```javascript
// Replicate format
extra_lora: "fofr/flux-pixar-cars"
// HuggingFace format
extra_lora: "huggingface.co/owner/model-name"
// CivitAI format
extra_lora: "civitai.com/models/<id>"
// Direct URL
extra_lora: "https://example.com/weights.safetensors"
```

### Aspect Ratio Reference

| Ratio | Models | Use Case |
|-------|--------|----------|
| `21:9` | Flux (all) | Ultra-wide README banner |
| `3:1` | Ideogram | Wide banner with typography |
| `16:9` | All | Standard widescreen |
| `1:1` | All | Square, avatar, icon |
| `9:16` | All | Mobile, portrait |

## Synapses

See [synapses.json](synapses.json) for connections.
