---
name: flux-image
description: Generate and edit images with Flux (Black Forest Labs) via AceDataCloud API. Use when creating images from text prompts, editing existing images with text instructions, or when high-quality image generation is needed. Supports multiple Flux models including dev, pro, ultra, and kontext for editing.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable. Optionally pair with mcp-flux for tool-use.
---

# Flux Image Generation

Generate and edit images through AceDataCloud's Flux API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/flux/images \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cat wearing a space helmet, photorealistic", "model": "flux-dev", "wait": true}'
```

## Models

| Model | Quality | Speed | Sizes | Best For |
|-------|---------|-------|-------|----------|
| `flux-dev` | Good | Fast | 256–1440px | Quick generation (default) |
| `flux-pro` | High | Medium | 256–1440px | Production work |
| `flux-pro-1.1` | Higher | Medium | 256–1440px | Better prompt following |
| `flux-pro-1.1-ultra` | Highest | Slow | Aspect ratios | Maximum quality |
| `flux-kontext-pro` | High | Medium | Aspect ratios | Image editing |
| `flux-kontext-max` | Highest | Slow | Aspect ratios | Complex editing |

## Generate Images

```json
POST /flux/images
{
  "prompt": "a minimalist logo of a mountain",
  "action": "generate",
  "model": "flux-pro-1.1",
  "size": "1024x1024",
  "count": 1
}
```

### Size Options

**For dev/pro/pro-1.1** (pixel dimensions):
- `"1024x1024"`, `"1344x768"`, `"768x1344"`, `"1024x576"`, `"576x1024"`

**For ultra/kontext** (aspect ratios):
- `"1:1"`, `"16:9"`, `"9:16"`, `"4:3"`, `"3:4"`, `"3:2"`, `"2:3"`, `"21:9"`, `"9:21"`

## Edit Images

Use kontext models for text-guided image editing:

```json
POST /flux/images
{
  "prompt": "change the background to a beach sunset",
  "action": "edit",
  "image_url": "https://example.com/photo.jpg",
  "model": "flux-kontext-pro"
}
```

## Task Polling

```json
POST /flux/tasks
{"task_id": "your-task-id"}
```

## MCP Server

```bash
pip install mcp-flux
```

Or hosted: `https://flux.mcp.acedata.cloud/mcp`

Key tools: `flux_generate_image`, `flux_edit_image`

## Gotchas

- Use pixel dimensions (e.g., `"1024x1024"`) with dev/pro models, aspect ratios (e.g., `"16:9"`) with ultra/kontext models
- Editing requires kontext models (`flux-kontext-pro` or `flux-kontext-max`) — other models only support generation
- `count` parameter generates multiple images in one request (increases cost proportionally)
- Ultra model produces highest quality but is slowest — use dev for iteration, ultra for final output
- All generation is async — use `"wait": true` or poll `/flux/tasks`
