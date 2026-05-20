---
name: generate-image
description: AI image generation CLI using Gemini. Use when generating images, checking syntax for resolution, aspect ratio, and reference image options.
disable-model-invocation: false
---

# generate-image - AI Image Generation

Uses Google Gemini (gemini-3-pro-image-preview) to generate images from text prompts.

## Synopsis

```bash
codev generate-image "<prompt>" [options]
```

## Options

```bash
-o, --output <file>        # Output file path (default: output.png)
-r, --resolution <res>     # Resolution: 1K, 2K, 4K (default: 1K)
-a, --aspect <ratio>       # Aspect ratio (default: 1:1)
--ref <image>              # Reference image (repeatable, max 14)
```

## Aspect Ratios

`1:1` | `16:9` | `9:16` | `3:4` | `4:3` | `3:2` | `2:3`

## Examples

```bash
# Basic generation
codev generate-image "A sunset over mountains"

# High-res widescreen
codev generate-image "A futuristic city" -r 4K -a 16:9 -o city.png

# With reference images (style transfer)
codev generate-image "Same style but with cats" --ref style.png --ref layout.png

# Prompt from file
codev generate-image prompt.txt -o result.png
```

## Prerequisites

Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable.
Get a key at https://aistudio.google.com/apikey

## Common Mistakes

- Prompt must be **quoted** if it contains spaces
- Prompt can also be a `.txt` file path (auto-detected by extension)
- Reference images must exist on disk — max 14 images
- Output defaults to `output.png` in current directory — use `-o` to change
