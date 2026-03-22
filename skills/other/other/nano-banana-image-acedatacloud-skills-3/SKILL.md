---
name: nano-banana-image
description: Generate and edit AI images with NanoBanana (Gemini-based) via AceDataCloud API. Use when creating images from text prompts or editing existing images with text instructions. Supports nano-banana and nano-banana-pro models.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable. Optionally pair with mcp-nano-banana for tool-use.
---

# NanoBanana Image Generation

Generate and edit AI images through AceDataCloud's NanoBanana (Gemini-based) API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/nano-banana/images \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a watercolor painting of a French countryside village", "model": "nano-banana"}'
```

## Models

| Model | Best For |
|-------|----------|
| `nano-banana` | Standard image generation (default) |
| `nano-banana-pro` | Higher quality, more detailed output |

## Workflows

### 1. Text-to-Image

```json
POST /nano-banana/images
{
  "prompt": "a photorealistic macro shot of morning dew on a spider web",
  "model": "nano-banana-pro",
  "aspect_ratio": "16:9"
}
```

### 2. Image Editing

Edit an existing image using natural language instructions — no mask needed.

```json
POST /nano-banana/images/edit
{
  "prompt": "change the background to a starry night sky",
  "image_url": "https://example.com/photo.jpg",
  "model": "nano-banana"
}
```

## Parameters

### Generation

| Parameter | Values | Description |
|-----------|--------|-------------|
| `model` | `"nano-banana"`, `"nano-banana-pro"` | Model to use |
| `aspect_ratio` | `"1:1"`, `"3:4"`, `"4:3"`, `"9:16"`, `"16:9"` | Output aspect ratio |

### Editing

| Parameter | Required | Description |
|-----------|----------|-------------|
| `image_url` | Yes | URL of the source image |
| `prompt` | Yes | Natural language editing instruction |
| `model` | No | Model to use (defaults to `"nano-banana"`) |
| `aspect_ratio` | No | Output aspect ratio |

## MCP Server

```bash
pip install mcp-nano-banana
```

Or hosted: `https://nano-banana.mcp.acedata.cloud/mcp`

Key tools: `nano_banana_generate_image`, `nano_banana_edit_image`

## Gotchas

- Editing does **NOT** require a mask — just describe the change in natural language
- `nano-banana-pro` produces significantly more detailed results but costs more
- Results return a direct image URL — no task polling needed
- Aspect ratio uses colon notation (e.g., `"16:9"`) not pixel dimensions
- The Gemini-based model excels at understanding complex, conversational editing instructions
