---
name: ai-image-tools
description: Generate and edit images using either OpenAI GPT Image 1.5 or Google's Nano Banana Pro (Gemini 3 Pro Image). Use when the user asks to generate/create/edit/modify images. Supports image-to-image editing for both providers and optional mask-based inpainting for OpenAI.
---

# AI Image Tools (OpenAI + Gemini)

One unified skill for image generation + editing, supporting:

- **OpenAI**: GPT Image 1.5 (generation + edits, optional mask inpainting)
- **Gemini**: Nano Banana Pro (Gemini 3 Pro Image) (generation + image-to-image edits)

## Usage

Run from your current working directory so outputs save where you're working.

### Generate (text → image)

```bash
uv run scripts/generate_image.py --prompt "A moody cinematic portrait of a golden retriever" --filename "out.png"
```

Pick a provider explicitly:

```bash
# OpenAI (GPT Image 1.5)
uv run scripts/generate_image.py --provider openai --prompt "..." --filename "out.png"

# Gemini (Nano Banana Pro)
uv run scripts/generate_image.py --provider gemini --prompt "..." --filename "out.png"
```

### Edit (image → image)

```bash
uv run scripts/generate_image.py --prompt "Make it look like a watercolor painting" --filename "out.png" --input-image "input.png"
```

Mask-based inpainting (OpenAI only):

```bash
uv run scripts/generate_image.py --provider openai --prompt "A red balloon" --filename "out.png" --input-image "input.png" --mask "mask.png"
```

## Provider Selection

- Default `--provider auto`:
  - uses OpenAI if `OPENAI_API_KEY` (or `--openai-api-key`) is available
  - otherwise uses Gemini if `GEMINI_API_KEY` (or `--gemini-api-key`) is available
- Set `--provider openai` or `--provider gemini` to force one.

## API Keys

- **OpenAI**:
  - env: `OPENAI_API_KEY`
  - flag: `--openai-api-key`
- **Gemini**:
  - env: `GEMINI_API_KEY`
  - flag: `--gemini-api-key`

## Options (Provider-Specific)

### OpenAI options

- `--quality low|medium|high` (generation only; default `medium`)
- `--size 1024x1024|1024x1536|1536x1024|auto` (default `1024x1024`)
- `--background transparent|opaque|auto` (generation only; default `auto`)
- `--mask path/to/mask.png` (edits only)

### Gemini options

- `--resolution 1K|2K|4K` (default `1K`)

## Notes

- Output is always saved as **PNG** at `--filename`.
- Don’t read the output image back into the model unless explicitly requested.
