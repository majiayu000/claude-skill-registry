---
name: seedance-video
description: Generate AI dance and motion videos with Seedance (ByteDance) via AceDataCloud API. Use when creating videos from text prompts or animating images into motion videos. Supports multiple models with configurable resolution, duration, and service tiers.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable. Optionally pair with mcp-seedance for tool-use.
---

# Seedance Video Generation

Generate AI dance and motion videos through AceDataCloud's Seedance (ByteDance) API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/seedance/videos \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a dancer performing contemporary ballet in a misty forest", "model": "seedance-1.0", "wait": true}'
```

## Models

| Model | Best For |
|-------|----------|
| `seedance-1.0` | General-purpose motion/dance video |
| `seedance-1.0-lite` | Faster, lighter generation |
| `seedance-1.0-pro` | Higher quality output |
| `seedance-1.5-pro` | Latest model, best quality |
| `seedance-acting-pro` | Character acting and expression |

## Workflows

### 1. Text-to-Video

```json
POST /seedance/videos
{
  "prompt": "a street dancer doing breakdancing moves in an urban setting",
  "model": "seedance-1.0-pro",
  "resolution": "1080p",
  "duration": 5,
  "service_tier": "standard"
}
```

### 2. Image-to-Video

Animate a still image into a motion video.

```json
POST /seedance/videos
{
  "prompt": "the person starts dancing gracefully",
  "image_url": "https://example.com/dancer.jpg",
  "model": "seedance-1.5-pro",
  "resolution": "720p",
  "duration": 5
}
```

## Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `model` | See models table | Model to use |
| `resolution` | `"360p"`, `"540p"`, `"720p"`, `"1080p"` | Output resolution |
| `duration` | `2` – `12` | Duration in seconds |
| `service_tier` | `"standard"`, `"premium"` | Quality tier (premium = faster, higher priority) |
| `seed` | integer | Seed for reproducible results |

## Task Polling

```json
POST /seedance/tasks
{"task_id": "your-task-id"}
```

States: `pending` → `succeeded` or `failed`.

## MCP Server

```bash
pip install mcp-seedance
```

Or hosted: `https://seedance.mcp.acedata.cloud/mcp`

Key tools: `seedance_generate_video`, `seedance_generate_video_from_image`

## Gotchas

- Duration range is **2–12 seconds** — values outside this range will fail
- Higher resolutions (1080p) combined with longer durations take significantly more time
- `premium` service tier costs more but generates faster
- `seedance-acting-pro` excels at facial expressions and character acting versus pure dance
- Image-to-video requires a single `image_url` — the person/subject in the image becomes the animated subject
- Task states use `"succeeded"` (not "completed") — check for this value when polling
