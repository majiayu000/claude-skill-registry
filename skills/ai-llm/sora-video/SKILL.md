---
name: sora-video
description: Generate AI videos with OpenAI Sora via AceDataCloud API. Use when creating videos from text prompts, generating videos from reference images, or using character references from existing videos. Supports text-to-video, image-to-video, and character-driven generation with multiple models and resolutions.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable. Optionally pair with mcp-sora for tool-use.
---

# Sora Video Generation

Generate AI videos through AceDataCloud's OpenAI Sora API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/sora/videos \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a golden retriever running on a beach at sunset", "model": "sora-2", "wait": true}'
```

## Models

| Model | Duration | Quality | Best For |
|-------|----------|---------|----------|
| `sora-2` | 10–15s | Standard | Most tasks (default) |
| `sora-2-pro` | 10–25s | Higher | Premium quality, longer videos |

## Workflows

### 1. Text-to-Video

```json
POST /sora/videos
{
  "prompt": "a busy Tokyo street at night with neon signs reflecting in rain puddles",
  "model": "sora-2",
  "size": "small",
  "duration": 10,
  "orientation": "landscape"
}
```

### 2. Image-to-Video

Use reference images to guide generation.

```json
POST /sora/videos
{
  "prompt": "the scene gradually comes alive with gentle motion",
  "image_urls": ["https://example.com/scene.jpg"],
  "model": "sora-2",
  "orientation": "landscape"
}
```

### 3. Character-Driven Video

Extract a character from an existing video and use them in a new scene.

```json
POST /sora/videos
{
  "prompt": "the character walks through a futuristic city",
  "character_url": "https://example.com/source-video.mp4",
  "character_start": 2.0,
  "character_end": 5.0,
  "model": "sora-2-pro"
}
```

## Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `size` | `"small"`, `"large"` | Video resolution |
| `duration` | `10`, `15`, `25` | Duration in seconds (25 only with sora-2-pro) |
| `orientation` | `"landscape"` (16:9), `"portrait"` (9:16), `"square"` (1:1) | Video orientation |

## Task Polling

```json
POST /sora/tasks
{"task_id": "your-task-id"}
```

States: `pending` → `succeeded` or `failed`.

## MCP Server

```bash
pip install mcp-sora
```

Or hosted: `https://sora.mcp.acedata.cloud/mcp`

Key tools: `sora_generate_video`, `sora_generate_video_from_image`, `sora_generate_video_with_character`

## Gotchas

- Duration of **25 seconds** is only available with `sora-2-pro` model
- `size: "large"` produces higher resolution but costs more and takes longer
- Character-driven generation requires `character_start` and `character_end` timestamps (in seconds) from the source video
- `orientation` sets the aspect ratio — use `"portrait"` for mobile-first content
- Task states use `"succeeded"` (not "completed") — check for this value when polling
