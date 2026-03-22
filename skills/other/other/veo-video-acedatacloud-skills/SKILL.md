---
name: veo-video
description: Generate AI videos with Google Veo via AceDataCloud API. Use when creating videos from text descriptions, animating still images into video, or converting lower-resolution results to full 1080p. Supports Veo 2, Veo 3, and Veo 3.1 models.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable. Optionally pair with mcp-veo for tool-use.
---

# Veo Video Generation

Generate AI videos through AceDataCloud's Google Veo API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/veo/videos \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a whale breaching in slow motion at golden hour", "model": "veo-3", "wait": true}'
```

## Models

| Model | Duration | Audio | Best For |
|-------|----------|-------|----------|
| `veo-2` | 5–8s | No | Fast, cost-effective generation |
| `veo-3` | 8s | Yes (native) | Full audiovisual generation |
| `veo-3.1` | 8s | Yes (native) | Latest model, highest quality |

## Workflows

### 1. Text-to-Video

```json
POST /veo/videos
{
  "prompt": "cinematic aerial shot of the Northern Lights over Iceland",
  "model": "veo-3",
  "aspect_ratio": "16:9",
  "duration": 8
}
```

### 2. Image-to-Video

Animate a still image into video.

```json
POST /veo/videos
{
  "prompt": "the scene gently comes to life with wind and subtle motion",
  "image_url": "https://example.com/landscape.jpg",
  "model": "veo-2",
  "aspect_ratio": "16:9"
}
```

### 3. Upscale to 1080p

Convert a generated video to full 1080p resolution.

```json
POST /veo/videos/1080p
{
  "video_url": "https://example.com/generated-video.mp4",
  "model": "veo-3"
}
```

## Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `model` | `"veo-2"`, `"veo-3"`, `"veo-3.1"` | Model to use |
| `aspect_ratio` | `"16:9"`, `"9:16"` | Video aspect ratio |
| `duration` | `5` – `8` | Duration in seconds |
| `generate_audio` | `true` / `false` | Enable/disable audio (veo-3, veo-3.1 default to true) |
| `enhance_prompt` | `true` / `false` | Let the model expand your prompt for better results |

## Task Polling

```json
POST /veo/tasks
{"task_id": "your-task-id"}
```

States: `pending` → `succeeded` or `failed`.

## MCP Server

```bash
pip install mcp-veo
```

Or hosted: `https://veo.mcp.acedata.cloud/mcp`

Key tools: `veo_generate_video`, `veo_generate_video_from_image`, `veo_get_1080p_video`

## Gotchas

- Veo 3 and 3.1 generate **native audio** — use `generate_audio: false` to suppress
- The 1080p endpoint (`/veo/videos/1080p`) only upscales previously generated videos
- `enhance_prompt` can significantly improve results but may deviate from literal interpretation
- Veo 2 does NOT support audio generation
- Duration is capped at 8 seconds for all models
- Task states use `"succeeded"` (not "completed") — check for this value when polling
