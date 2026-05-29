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

## Synapses

See [synapses.json](synapses.json) for connections.
