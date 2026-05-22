---
name: genai-image
description: Generate images using Google GenAI Nano Banana Pro model via CLI. Use when the user asks to create images, generate pictures, make AI art, do image-to-image transformations, place people in scenes, or create character variations.
---

# GenAI Image Generation Skill

Generate high-quality images using the `genai-cli image` command with Nano Banana Pro.

## Quick Start

```bash
# Basic image generation
uv run genai-cli image "your prompt here" --aspect 16:9

# Image-to-image (use existing image as reference)
uv run genai-cli image "place this person in a datacenter" --input ./photo.png --aspect 16:9

# With all options
uv run genai-cli image "robot in tuxedo" --aspect 9:16 --variations 3 --quality 90
```

## CLI Reference

```
uv run genai-cli image [OPTIONS] PROMPT

Options:
  --aspect, -a      Aspect ratio (1:1, 9:16, 16:9, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9)
  --resolution, -r  Resolution: 1K or 4K
  --variations, -v  Number of images (1-10)
  --quality, -q     Output quality (0-100)
  --guidance, -g    Prompt adherence (0-20)
  --enhance         Auto-improve prompt
  --format, -f      Output format: png, jpeg, webp
  --output, -o      Output directory (default: ./genai_outputs/)
  --input, -i       Input image for image-to-image generation
  --json            Output as JSON
```

## Image-to-Image Generation

Use an existing image as a reference to generate new images:

```bash
# Place a person in a new scene
uv run genai-cli image "Place this person in a modern datacenter with server racks and blue LED lights" \
  --input ./person.png \
  --aspect 16:9

# Transform a photo
uv run genai-cli image "Convert to anime style, vibrant colors" \
  --input ./photo.jpg

# Add elements to an existing image
uv run genai-cli image "Add a sunset background and dramatic lighting" \
  --input ./portrait.png
```

**Use cases for image-to-image:**
- Place people in new environments/scenes
- Style transfer (photorealistic to anime, etc.)
- Add or modify elements in existing images
- Create variations of a reference image
- Professional headshots in different settings

## Supported Aspect Ratios

| Ratio | Use Case |
|-------|----------|
| 1:1 | Square, social media |
| 9:16 | Vertical, mobile, stories |
| 16:9 | Horizontal, widescreen |
| 4:3 | Standard photo |
| 3:4 | Portrait |
| 3:2 | Classic photo |
| 2:3 | Portrait photo |
| 4:5 | Instagram portrait |
| 5:4 | Large format |
| 21:9 | Ultrawide, cinematic |

## Examples

### Basic Generation
```bash
uv run genai-cli image "A sunset over mountains" --aspect 16:9
```

### High Quality Portrait
```bash
uv run genai-cli image "Professional headshot, studio lighting" --aspect 3:4 --quality 95
```

### Batch Generation
```bash
uv run genai-cli image "Abstract art, vibrant colors" --variations 5 --aspect 1:1
```

### Person in Datacenter (Image-to-Image)
```bash
uv run genai-cli image "Place this person in a modern datacenter environment with server racks, blue LED lights, professional IT atmosphere" \
  --input ./team_photo.png \
  --aspect 16:9
```

### With JSON Output (for automation)
```bash
uv run genai-cli image "Product photo" --json
```

## Output

Images are saved to `./genai_outputs/` by default:
- `genai_image_001.png`
- `genai_image_002.png` (if variations > 1)
- etc.

## Prompt Tips

1. **Be specific**: "A robot in a black tuxedo with bow tie" > "A robot in a suit"
2. **Include lighting**: "Cinematic dramatic lighting"
3. **Specify style**: "Photorealistic", "Cinematic", "Film noir"
4. **Add text**: "Bold text reads: 'YOUR TEXT HERE'"
5. **For image-to-image**: Describe what you want to happen to/with the input image

## Prerequisites

API key must be configured:
```bash
uv run genai-cli auth set-key
```
