---
name: nanobanana
description: Generate images from text prompts or edit existing images using Gemini Image Generation API. Supports text-to-image generation and image editing with multiple reference images. Use when creating visuals, editing photos, or generating illustrations.
---

# Nano Banana Pro - Image Generation & Editing

Generate or edit images using Gemini Image Generation API.

## Modes

1. **Text-to-Image**: Generate new images from text prompts
2. **Image Editing**: Edit existing images with instructions

## Usage

```bash
# Text-to-image
python scripts/nanobanana.py "{prompt}" --aspect-ratio "{ratio}"

# Image editing
python scripts/nanobanana.py "{prompt}" --input "{image_path}"

# Multiple reference images
python scripts/nanobanana.py "{prompt}" --input "{image1}" --input "{image2}"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| prompt | Yes | - | Generation/edit instruction |
| --input, -i | No | - | Input image(s) for editing |
| --output, -o | No | auto | Output path |
| --aspect-ratio, -ar | No | 16:9 | Output ratio |
| --session, -s | No | - | Session name for organizing output |
| --force-ar | No | false | Force aspect ratio in edit mode |

## Aspect Ratios

`1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `21:9`

## Examples

```bash
# Generate landscape
python scripts/nanobanana.py "Mt. Fuji at sunset, photorealistic"

# Edit image
python scripts/nanobanana.py "Remove the background" --input photo.jpg

# Combine images
python scripts/nanobanana.py "Merge these into one composition" --input img1.png --input img2.png

# With session organization
python scripts/nanobanana.py "Company logo design" --session "brand_assets" --aspect-ratio 1:1
```

## Requirements

- GEMINI_API_KEY or GOOGLE_API_KEY in environment
- Python packages: google-genai, Pillow, python-dotenv
