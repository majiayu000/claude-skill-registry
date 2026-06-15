---
name: generating-images
description: Generate images using AI models via OpenRouter API. Supports text-to-image and image-based generation with customizable aspect ratios. Use when the user asks to generate, create, or synthesize images based on text descriptions or reference images.
---

# Generating Images

Use AI models to generate images from text descriptions or reference images via OpenRouter API.

## Quick start

### Text-to-image generation

Generate an image from a text description:

```bash
python scripts/generate.py \
  --prompt "A serene landscape with mountains and a lake at sunset" \
  --output "landscape.png"
```

### Image-to-image generation

Generate a new image based on a reference image:

```bash
python scripts/generate.py \
  --reference "girl.png" \
  --prompt "Same art style, but the girl is happily eating delicious braised pork" \
  --output "result.png"
```

## Configuration

### Initial setup

Set your OpenRouter API key as environment variable:

```bash
export OPENROUTER_API_KEY="${OPENROUTER_API_KEY}"
```

## Aspect ratios

Specify custom aspect ratios with `--aspect-ratio`:

```bash
# Square image (1024x1024)
python scripts/generate.py --prompt "..." --aspect-ratio "1:1"

# Landscape (1344x768)
python scripts/generate.py --prompt "..." --aspect-ratio "16:9"

# Portrait (768x1344)
python scripts/generate.py --prompt "..." --aspect-ratio "9:16"
```

Supported ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`

## Advanced features

### Choose a different model

See [MODELS.md](MODELS.md) for available models and their capabilities.

```bash
python scripts/generate.py \
  --model "google/gemini-2.5-flash-image" \
  --prompt "..." \
  --output "result.png"
```

### More examples

See [EXAMPLES.md](EXAMPLES.md) for common use cases and scenarios.

## Scripts reference

### generate.py

Main image generation script.

**Required arguments:**
- `--prompt`: Text description of the image to generate
- `--output`: Output file path (e.g., `result.png`)

**Optional arguments:**
- `--reference`: Path to reference image for image-to-image generation
- `--aspect-ratio`: Image aspect ratio (default: `1:1`)
- `--model`: Model to use (default: from config.json)
- `--timeout`: Request timeout in seconds (default: 60)

**Examples:**

Text-to-image:
```bash
python scripts/generate.py \
  --prompt "Anime style girl drinking coffee" \
  --aspect-ratio "16:9" \
  --output "coffee.png"
```

Image-to-image:
```bash
python scripts/generate.py \
  --reference "style_reference.png" \
  --prompt "Same style, different scene: girl eating ramen" \
  --output "ramen.png"
```

## Error handling

The script handles common errors:
- Missing API key: Shows clear error message
- Network errors: Retries automatically
- Invalid image format: Validates before saving
- Missing reference file: Reports file not found

Check script output for detailed error messages.
