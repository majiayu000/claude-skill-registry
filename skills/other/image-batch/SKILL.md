---
name: image-batch
description: "Batch process images for marketing. Use when: resizing images for social media; compressing images for web; removing backgrounds; adding watermarks; converting formats to WebP; optimizing for Core Web Vitals"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Image Batch Processing

> Automate repetitive image tasks using Pillow and rembg - resize, compress, remove backgrounds, and watermark hundreds of images in seconds.

## When to Use This Skill

- **Social media prep** - Resize images for multiple platforms at once
- **Website optimization** - Compress and convert to WebP for faster loading
- **Product photos** - Remove backgrounds, add consistent styling
- **Brand protection** - Add watermarks to marketing assets
- **Batch conversion** - Convert legacy formats to modern ones


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures video workflow | Final creative vision |
| Suggests shot compositions | Equipment selection |
| Creates storyboard templates | Brand aesthetics |
| Generates script frameworks | Final approval |
| Identifies technical requirements | Budget allocation |

## Dependencies

```bash
pip install Pillow rembg click
# For GPU-accelerated background removal:
# pip install rembg[gpu]
```

## Commands

### Resize Images
```bash
python scripts/main.py resize ./images/ --width 1200
python scripts/main.py resize ./images/ --format instagram  # 1080x1080
python scripts/main.py resize ./images/ --format linkedin   # 1200x627
```

### Compress Images
```bash
python scripts/main.py compress ./images/ --quality 80
python scripts/main.py compress ./images/ --max-size 500  # Max 500KB
```

### Remove Background
```bash
python scripts/main.py remove-bg photo.jpg
python scripts/main.py remove-bg ./products/ --output ./transparent/
```

### Add Watermark
```bash
python scripts/main.py watermark ./images/ --logo logo.png --position bottom-right
python scripts/main.py watermark ./images/ --text "© 2024 Company" --opacity 0.3
```

### Convert Format
```bash
python scripts/main.py convert ./images/ --format webp
python scripts/main.py convert ./images/ --format avif --quality 80
```

## Examples

### Example 1: Prepare Product Images for E-commerce
```bash
# Remove backgrounds
python scripts/main.py remove-bg ./raw-products/ --output ./transparent/

# Resize to standard size
python scripts/main.py resize ./transparent/ --width 1000 --height 1000 --fit contain

# Compress for web
python scripts/main.py compress ./transparent/ --quality 85 --format webp

# Output: ./transparent/*.webp (optimized, transparent background)
```

### Example 2: Social Media Image Kit
```bash
# Create multiple sizes from one source
python scripts/main.py resize hero-image.jpg --format instagram --output hero_ig.jpg
python scripts/main.py resize hero-image.jpg --format linkedin --output hero_li.jpg
python scripts/main.py resize hero-image.jpg --format twitter --output hero_tw.jpg
python scripts/main.py resize hero-image.jpg --format facebook --output hero_fb.jpg

# Or batch process entire folder for one platform
python scripts/main.py resize ./campaign-images/ --format instagram --output ./instagram/
```

### Example 3: Website Image Optimization
```bash
# Convert all images to WebP
python scripts/main.py convert ./website-images/ --format webp --quality 80

# Ensure no image exceeds 200KB
python scripts/main.py compress ./website-images/ --max-size 200

# Results in 60-80% smaller file sizes
```

## Social Media Format Presets

| Format | Dimensions | Aspect Ratio | Use Case |
|--------|------------|--------------|----------|
| `instagram` | 1080x1080 | 1:1 | Feed posts |
| `instagram-story` | 1080x1920 | 9:16 | Stories/Reels |
| `linkedin` | 1200x627 | 1.91:1 | Link previews |
| `linkedin-post` | 1200x1200 | 1:1 | Feed posts |
| `twitter` | 1200x675 | 16:9 | Cards |
| `facebook` | 1200x630 | 1.91:1 | Link previews |
| `pinterest` | 1000x1500 | 2:3 | Pins |
| `youtube` | 1280x720 | 16:9 | Thumbnails |

## Fit Modes

| Mode | Behavior |
|------|----------|
| `cover` | Fill area, crop excess (default) |
| `contain` | Fit inside, add padding |
| `stretch` | Distort to fit exactly |
| `crop` | Smart crop focusing on subject |

## Output Formats

| Format | Best For | Compression |
|--------|----------|-------------|
| `webp` | Web images | 25-35% smaller than JPEG |
| `avif` | Modern browsers | 50% smaller than JPEG |
| `jpg` | Photos, gradients | Lossy, universal |
| `png` | Transparency, graphics | Lossless |

## Skill Boundaries

### What This Skill Does Well
- Structuring video production workflows
- Creating storyboard frameworks
- Suggesting technical approaches
- Providing creative direction templates

### What This Skill Cannot Do
- Replace professional videography
- Edit video files directly
- Make final creative judgments
- Guarantee audience engagement

## Related Skills

- [video-processing](../video-processing/) - Process video thumbnails
- [lighthouse-audit](../../seo-tools/lighthouse-audit/) - Check image impact on LCP

## Skill Metadata


- **Mode**: cyborg
```yaml
category: automation
subcategory: image-processing
dependencies: [Pillow, rembg]
difficulty: beginner
time_saved: 5+ hours/week
```
