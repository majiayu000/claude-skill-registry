---
name: gpt-atelier
description: >
  OpenAI GPT Image generation and editing (gpt-image-2, 1.5, 1, mini).
  Text-to-image, mask-based inpainting, multi-reference composition,
  multi-turn conversational editing via Responses API, streaming with
  partial images. This skill should be used when generating or editing
  images via OpenAI's image models, when near-perfect text rendering
  in images is needed, when mask-based region-aware editing is required,
  when multi-turn conversational image editing is desired, or when
  streaming progressive image delivery is needed. Complements
  nano-banana-pro (Gemini) as a parallel image generation backend.
---

# GPT Atelier

OpenAI GPT Image generation and editing. Wraps both the Image API (one-shot) and Responses API (multi-turn conversational) with 6 scripts covering generate, edit, compose, converse, stream, and test workflows.

**Prerequisite:** `OPENAI_API_KEY` environment variable.

## Models

| Flag | Model | Strengths |
|------|-------|-----------|
| (default) | `gpt-image-2` | Reasoning-based, ~99% text rendering, up to 8 consistent images, 4K, streaming |
| `--fast` | `gpt-image-1.5` | Region-aware editing, 4x faster, cheaper |
| `--mini` | `gpt-image-1-mini` | Cheapest ($0.006/image low quality) |

## Quick Start

```bash
# Test connectivity
python3 scripts/test_connection.py --check-models

# Generate an image
python3 scripts/generate_image.py "A Minoan bull-leaper under golden light"

# Edit with mask
python3 scripts/edit_image.py "Replace the sky with a dramatic sunset" photo.png --mask sky_mask.png

# Compose from references
python3 scripts/compose_images.py "Create a gift basket containing these items" item1.png item2.png item3.png

# Multi-turn editing session
python3 scripts/converse_image.py

# Streaming with partial images
python3 scripts/stream_image.py "An ancient fresco being restored" --partials 3
```

Image API scripts share: `--output DIR`, `--filename NAME`, `--quality low|medium|high`, `--format png|jpeg|webp`, `--fast`, `--mini`. `converse_image.py` uses `--orchestrator` instead of `--fast`/`--mini`.

## Core Workflows

### 1. Text-to-Image Generation

```bash
python3 scripts/generate_image.py "prompt" [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--size` | auto | `WxH` or preset: square, landscape, portrait, wide, 2k, 4k, 4k-portrait |
| `--quality` | high | low, medium, high, auto |
| `--n` | 1 | Number of images (1-8) |
| `--format` | png | png, jpeg (faster), webp |
| `--compression` | — | 0-100 for jpeg/webp |
| `--background` | — | opaque, transparent, auto |
| `--moderation` | auto | auto, low |

```bash
# Product photography
python3 scripts/generate_image.py \
  "High-end product photography of luxury watch on black marble, dramatic key light, f/5.6, commercial quality" \
  --size square --quality high

# Budget thumbnails
python3 scripts/generate_image.py "Quick sketch of a coffee cup" --mini --quality low

# Multiple variations
python3 scripts/generate_image.py "Logo design for a tech startup" --n 4 --size square
```

### 2. Image Editing

```bash
python3 scripts/edit_image.py "instruction" input.png [options]
```

Additional options: `--mask`, `--images` (extra references).

Auto-converts B&W masks to RGBA (requires Pillow: `pip install Pillow`).

```bash
# Region-aware edit with mask
python3 scripts/edit_image.py "Add a flamingo to the pool" lounge.png --mask pool_mask.png

# Full-image restyle
python3 scripts/edit_image.py "Convert to watercolor painting style" photo.jpg

# Edit with reference images
python3 scripts/edit_image.py "Replace the car with this bicycle" street.png --images bicycle.png
```

### 3. Multi-Reference Composition

```bash
python3 scripts/compose_images.py "instruction" img1.png img2.png [img3.png ...] [options]
```

Requires 2+ reference images. The model creates a new image incorporating all references.

```bash
python3 scripts/compose_images.py \
  "Create a mood board combining these design elements" \
  texture.png palette.png sketch.png --size landscape
```

### 4. Multi-Turn Conversational Editing (Responses API)

```bash
python3 scripts/converse_image.py [prompt] [options]
```

Without a prompt, enters interactive REPL. Maintains conversation state via `previous_response_id`.

```bash
# Interactive session
python3 scripts/converse_image.py --auto-save
> A cyberpunk street scene at night
> Now add neon signs with Japanese text
> Make it rain and add reflections
> /save final_scene

# Single-shot
python3 scripts/converse_image.py "Design a coffee brand logo" --output ./logos
```

Interactive commands: `/save`, `/action auto|generate|edit`, `/model`, `/clear`, `/history`, `/help`, `/quit`.

Attach images with `@path`: `@logo.png Add this logo to the top-right corner`.

Additional options:

| Flag | Orchestrator | Tradeoff |
|------|-------------|----------|
| (default) | `gpt-5.4` | Standard quality, fastest |
| `--thinking` | `gpt-5.4-thinking` | Better composition for complex scenes, slower |
| `--pro` | `gpt-5.4-pro` | Highest quality, most expensive |
| `--orchestrator MODEL` | any | Manual override |

### 5. Streaming with Partial Images

```bash
python3 scripts/stream_image.py "prompt" --partials N [options]
```

Outputs partial images as they generate, then the final image.

```bash
# Stream with 3 progressively sharper partials
python3 scripts/stream_image.py "A detailed architectural drawing" --partials 3 --save-partials
```

Additional option: `--save-partials` to save intermediate images.

## Prompting Quick-Hits

1. **Lead with scene/style, not subject.** First words carry highest visual weight. Specify intended use (ad, UI mockup, editorial) so the model picks the right polish level.
2. **Always double-quote literal text.** `"HELLO WORLD"` engages the high-accuracy text rendering engine.
3. **Pixel dimensions in prompt.** For custom aspect ratios, append `"Output in exactly WxH (R:R ratio) resolution"` — the API `size` param alone is unreliable. Done automatically by `inject_size_hint()` for gpt-image-2.
4. **Use `--thinking` for complex scenes.** The orchestrator model matters — Thinking models produce significantly better multi-element compositions.
5. **Generate fresh, don't edit.** Reference-image editing on gpt-image-2 produces yellow tint and poor prompt adherence. For design-final work, generate from scratch.

See `references/prompting-guide.md` for full details.

## When to Use GPT Atelier vs Nano Banana Pro

| Task | GPT Atelier | Nano Banana Pro |
|------|-------------|-----------------|
| Text rendering (complex, non-Latin) | Best | Good |
| Mask-based inpainting | Native, low drift | Higher drift (~40%) |
| Reference-image editing | Yellow tint risk — use `--fast` | Better fidelity |
| Multi-turn editing with state | Responses API | Multi-turn chat |
| Photorealism | Excellent | Excellent |
| Cinematic digital painting | Good | Best |
| UI mockups / screenshots | Best | Good |
| Multi-image consistency | Up to 8/prompt | Up to 14 references |
| Streaming partial delivery | Native | Not available |
| Dark/artistic themes | Stricter policy | More permissive |
| Budget/volume | $0.006/img (mini low) | Gemini pricing |
| Arbitrary aspect ratios | Any (16px multiples) | 10 presets |

## Cost Control

Start with `--quality low` ($0.006/image) for ideation. Graduate to `medium` ($0.05) for review, `high` ($0.21) for final assets. Use `--fast` for cheaper generation, `--mini` for maximum cost savings. Use `--format jpeg` for faster response times.

## Script Reference

| Script | Purpose | API |
|--------|---------|-----|
| `generate_image.py` | Text-to-image | Image API |
| `edit_image.py` | Edit with mask/references | Image API |
| `compose_images.py` | Multi-reference composition | Image API |
| `converse_image.py` | Multi-turn editing | Responses API |
| `stream_image.py` | Streaming with partials | Image API |
| `test_connection.py` | Connectivity check | Models API |

## Reference Documentation

| File | Contents |
|------|----------|
| `references/api-reference.md` | Full parameter reference, pricing, size constraints |
| `references/prompting-guide.md` | Prompt engineering patterns, text rendering, style keywords |
| `references/troubleshooting.md` | Error codes, content policy, rate limits |
