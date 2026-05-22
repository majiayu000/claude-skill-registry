---
name: seedream-image
description: Generate and edit AI images with Seedream (ByteDance) via AceDataCloud API. Use when creating images from text prompts, editing existing images with inpainting/outpainting, or working with ultra-high-resolution outputs. Supports Seedream 2.0, 2.1, 3.0, and 3.0 Turbo models.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable. Optionally pair with mcp-seedream for tool-use.
---

# Seedream Image Generation

Generate and edit AI images through AceDataCloud's Seedream (ByteDance) API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/seedream/images \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cyberpunk cat wearing VR goggles in a neon city", "model": "seedream-3.0"}'
```

## Models

| Model | Resolution | Speed | Best For |
|-------|-----------|-------|----------|
| `seedream-2.0` | Standard | Fast | Quick drafts |
| `seedream-2.1` | Standard | Fast | Improved quality over 2.0 |
| `seedream-3.0` | Up to 2048×2048 | Standard | High-quality generation (default) |
| `seedream-3.0-turbo` | Up to 2048×2048 | Faster | Speed-optimized with near-3.0 quality |

## Workflows

### 1. Text-to-Image

```json
POST /seedream/images
{
  "prompt": "a serene Japanese garden with cherry blossoms and a red bridge",
  "model": "seedream-3.0",
  "width": 1024,
  "height": 1024
}
```

### 2. Image Editing (Inpainting / Outpainting)

Edit regions of an existing image using a mask.

```json
POST /seedream/images/edit
{
  "prompt": "replace with a golden sunset sky",
  "image_url": "https://example.com/photo.jpg",
  "mask_url": "https://example.com/mask.png",
  "model": "seedream-3.0"
}
```

## Parameters

### Generation

| Parameter | Values | Description |
|-----------|--------|-------------|
| `model` | `"seedream-2.0"`, `"seedream-2.1"`, `"seedream-3.0"`, `"seedream-3.0-turbo"` | Model to use |
| `width` | 512 – 2048 | Image width in pixels |
| `height` | 512 – 2048 | Image height in pixels |
| `seed` | integer | Seed for reproducible results |

### Editing

| Parameter | Required | Description |
|-----------|----------|-------------|
| `image_url` | Yes | URL of the source image to edit |
| `mask_url` | Yes | URL of the binary mask (white = edit region) |
| `prompt` | Yes | Describe what to place in the masked area |

## MCP Server

```bash
pip install mcp-seedream
```

Or hosted: `https://seedream.mcp.acedata.cloud/mcp`

Key tools: `seedream_generate_image`, `seedream_edit_image`

## Gotchas

- Maximum resolution is **2048×2048** — exceed this and requests fail
- Mask images must be **binary** (black/white) with the same dimensions as the source image
- `seedream-3.0-turbo` offers a good speed/quality trade-off for iterative workflows
- Results return a direct image URL — no task polling needed for generation
- Editing always requires both `image_url` and `mask_url`
