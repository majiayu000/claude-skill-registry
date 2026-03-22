---
name: luma-video
description: Generate AI videos with Luma Dream Machine via AceDataCloud API. Use when creating videos from text prompts, generating videos from reference images, extending existing videos, or any video generation task with Luma. Supports text-to-video, image-to-video, and video extension.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable. Optionally pair with mcp-luma for tool-use.
---

# Luma Video Generation

Generate AI videos through AceDataCloud's Luma Dream Machine API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/luma/videos \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a drone flying over a mountain lake at sunrise", "action": "generate", "wait": true}'
```

## Workflows

### 1. Text-to-Video

Generate video purely from a text description.

```json
POST /luma/videos
{
  "prompt": "a timelapse of flowers blooming in a garden",
  "action": "generate",
  "aspect_ratio": "16:9",
  "loop": false,
  "enhancement": true
}
```

### 2. Image-to-Video

Use start and/or end reference images to guide generation.

```json
POST /luma/videos
{
  "prompt": "the scene comes alive with gentle wind",
  "action": "generate",
  "start_image_url": "https://example.com/scene.jpg",
  "end_image_url": "https://example.com/scene-end.jpg",
  "aspect_ratio": "16:9"
}
```

### 3. Extend a Video

Continue an existing video with a new prompt.

```json
POST /luma/videos
{
  "action": "extend",
  "video_id": "existing-video-id",
  "prompt": "the camera continues forward through the forest"
}
```

## Aspect Ratios

| Ratio | Use Case |
|-------|----------|
| `16:9` | Landscape (default) — YouTube, TV |
| `9:16` | Portrait — TikTok, Instagram Stories |
| `1:1` | Square — Social media |
| `4:3` | Classic — Presentations |
| `21:9` | Ultra-wide — Cinematic |

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | — | Text description of the video (required) |
| `action` | string | `"generate"` | `"generate"` or `"extend"` |
| `aspect_ratio` | string | `"16:9"` | Video aspect ratio |
| `loop` | bool | `false` | Create seamless loop |
| `enhancement` | bool | `true` | Enhance prompt for better results |
| `start_image_url` | string | — | Reference image for first frame |
| `end_image_url` | string | — | Reference image for last frame |
| `video_id` | string | — | Required for extend action |

## Task Polling

```json
POST /luma/tasks
{"task_id": "your-task-id"}
```

Poll every 5 seconds. States: `pending` → `completed` or `failed`.

## MCP Server

```bash
pip install mcp-luma
```

Or hosted: `https://luma.mcp.acedata.cloud/mcp`

Key tools: `luma_generate_video`, `luma_generate_video_from_image`, `luma_extend_video`

## Gotchas

- `enhancement: true` (default) improves prompt quality but may alter your intent — set to `false` for literal prompts
- Start/end image URLs must be publicly accessible
- `loop: true` creates seamless looping video — good for backgrounds and social media
- Extend requires the `video_id` from a previously completed generation
- Video generation takes 1–5 minutes depending on complexity
- Both start and end images are optional — you can use just one for partial guidance
