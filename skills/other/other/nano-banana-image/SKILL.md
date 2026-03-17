---
name: nano-banana-image
description: Generate and edit images using Google's Gemini image generation models.
---

# nano-banana-image

Generate and edit images using Google's Gemini image generation models.

## When to use this skill

Use this skill when the user wants to:
- Generate images from text prompts
- Edit or transform existing images with instructions
- Create logos, illustrations, product photos, or any visual content

## Usage

```bash
cd ~/.claude/skills/nano-banana-image
node scripts/nano_banana.js [options]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--model` | Model to use: `flash` (fast) or `pro` (higher quality) | `flash` |
| `--prompt` | Text prompt describing the image to generate | required |
| `--input` | Path to input image for editing (flash only) | none |
| `--out` | Output path for generated image | `outputs/output.png` |
| `--aspect` | Aspect ratio: `1:1`, `16:9`, `9:16`, `4:3`, `3:4` | `1:1` |

### Models

| Model | API Name | Features |
|-------|----------|----------|
| `flash` | `gemini-2.5-flash-image` | Fast, supports image editing, good quality |
| `pro` | `imagen-4.0-generate-001` | Higher quality, text-to-image only |

### Examples

**Text to image:**
```bash
node scripts/nano_banana.js \
  --model flash \
  --prompt "A clean minimalist ninja logo, bold outline, white background" \
  --out outputs/logo.png
```

**Widescreen background:**
```bash
node scripts/nano_banana.js \
  --model flash \
  --aspect 16:9 \
  --prompt "Abstract background with purple and blue gradients, geometric shapes" \
  --out outputs/background.png
```

**High quality generation:**
```bash
node scripts/nano_banana.js \
  --model pro \
  --aspect 16:9 \
  --prompt "A cinematic product photo of a smartwatch on a reflective surface" \
  --out outputs/product.png
```

**Edit existing image:**
```bash
node scripts/nano_banana.js \
  --model flash \
  --input inputs/room.png \
  --prompt "Restyle this room as modern Japanese minimalism" \
  --out outputs/room_edited.png
```

## How it works

1. Script sends prompt to Gemini API with `responseModalities: ["TEXT", "IMAGE"]`
2. Model generates image and returns base64-encoded data
3. Script decodes and saves to output file

## Requirements

- Node.js 18+
- `GEMINI_API_KEY` environment variable (get one at [Google AI Studio](https://aistudio.google.com/apikey))

## Setup

```bash
cd ~/.claude/skills/nano-banana-image
bun install
export GEMINI_API_KEY="your-key-here"
```

## Rate Limits (Free Tier)

- ~2-3 images per day
- Resets at midnight Pacific Time
- Upgrade billing for higher limits
