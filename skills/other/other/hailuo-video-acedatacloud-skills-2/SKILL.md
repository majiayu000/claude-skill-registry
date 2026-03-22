---
name: hailuo-video
description: Generate AI videos with Hailuo (MiniMax) via AceDataCloud API. Use when creating videos from text descriptions or animating images into video. Supports text-to-video and image-to-video with director mode for precise control.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable.
---

# Hailuo Video Generation

Generate AI videos through AceDataCloud's Hailuo (MiniMax) API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/hailuo/videos \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "generate", "prompt": "a dolphin jumping through ocean waves at golden hour", "model": "minimax-t2v"}'
```

## Models

| Model | Type | Best For |
|-------|------|----------|
| `minimax-t2v` | Text-to-Video | Creating video from text description |
| `minimax-i2v` | Image-to-Video | Animating a still image |
| `minimax-i2v-director` | Image-to-Video (Director) | Precise control over animation from image |

## Workflows

### 1. Text-to-Video

```json
POST /hailuo/videos
{
  "action": "generate",
  "prompt": "a time-lapse of flowers blooming in a meadow",
  "model": "minimax-t2v"
}
```

### 2. Image-to-Video

Animate a still image into a video clip.

```json
POST /hailuo/videos
{
  "action": "generate",
  "prompt": "gentle wind blows through the scene",
  "model": "minimax-i2v",
  "first_image_url": "https://example.com/landscape.jpg"
}
```

### 3. Image-to-Video (Director Mode)

More precise control over the animation.

```json
POST /hailuo/videos
{
  "action": "generate",
  "prompt": "camera slowly zooms in while leaves fall gently",
  "model": "minimax-i2v-director",
  "first_image_url": "https://example.com/scene.jpg"
}
```

## Parameters

| Parameter | Required | Values | Description |
|-----------|----------|--------|-------------|
| `action` | Yes | `"generate"` | Action type |
| `prompt` | Yes | string | Video description |
| `model` | Yes | `"minimax-t2v"`, `"minimax-i2v"`, `"minimax-i2v-director"` | Model |
| `first_image_url` | For i2v | string | Source image URL (required for image-to-video) |
| `mirror` | No | boolean | Mirror the output |
| `callback_url` | No | string | Async callback URL |

## Task Polling

```json
POST /hailuo/tasks
{"task_id": "your-task-id"}
```

States: `processing` → `succeed` or `failed`.

## Gotchas

- `first_image_url` is **required** for `minimax-i2v` and `minimax-i2v-director` models
- Director mode (`minimax-i2v-director`) provides finer camera/motion control than standard i2v
- The `action` field currently only supports `"generate"` — no extend or edit
- Flat pricing per generation regardless of model
- Use `mirror: true` to horizontally flip the output if needed
