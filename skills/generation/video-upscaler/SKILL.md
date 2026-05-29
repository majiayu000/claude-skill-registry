---
name: video-upscaler
version: 1.0.0
display_name: Video Upscaler
author: wells1137
description: "Intelligently upscale and enhance videos to cinematic quality using a multi-model backend (Topaz, SeedVR2)."
tags: [video, upscale, enhance, topaz, seedvr, 4k, quality]
---

## Summary

The **Video Upscaler** skill provides professional-grade video quality enhancement by leveraging a powerful, multi-model backend. It intelligently selects the best AI model (Topaz, SeedVR2, etc.) based on the user-defined profile to achieve optimal results, transforming low-resolution or noisy footage into crisp, cinematic-quality video.

This skill abstracts away the complexity of choosing and configuring different AI upscaling models. Instead of dealing with dozens of technical parameters, the user simply chooses a high-level goal, and the skill handles the rest.

## Features

- **Multi-Model Backend**: Dynamically routes requests to the best model for the job (Topaz, SeedVR2, etc.) via a unified API.
- **Profile-Based Enhancement**: Offers a range of pre-configured profiles for common use cases, from standard 2x upscaling to 4K cinematic conversion and 60 FPS frame boosting.
- **Asynchronous by Design**: Handles long-running video processing jobs without blocking the agent.
- **Simple Interface**: Requires only a video URL and a profile name to start.

## How It Works

The skill operates in a simple, two-step asynchronous workflow:

1.  **Submit Job**: The agent calls the `/upscale` endpoint with a video URL and a profile name. The service validates the request, selects the appropriate AI model, and submits the job to the `fal.ai` backend. It immediately returns a `task_id`.

2.  **Poll for Status**: The agent uses the `task_id` to periodically call the `/status/{task_id}` endpoint. The status will be `queued`, `in_progress`, or `completed`. Once completed, the response will contain the URL of the final, upscaled video.

## Available Profiles

| Profile Name | Description |
| :--- | :--- |
| `standard_x2` | **2x upscale** using Topaz Proteus v4. Best all-around quality for live-action footage. |
| `cinema_4k` | Upscale to **4K (2160p)** using SeedVR2. Best for cinematic content requiring temporal consistency. |
| `frame_boost_60fps` | 2x upscale + **frame interpolation to 60 FPS** using Topaz Apollo v8. Best for sports and action. |
| `ai_video_enhance` | **4x upscale** using Topaz. Best for AI-generated videos that need resolution boosting. |
| `web_optimized` | Upscale to **1080p** with web-optimized H264 output. Best for social media and web publishing. |

## End-to-End Example

**User Request:** "Enhance this video to 4K cinematic quality: [video_url]"

**1. Agent -> Skill (Submit Job)**

The agent identifies the user's intent and calls the `/upscale` endpoint with the `cinema_4k` profile.

```bash
curl -X POST http://<your_backend_url>/upscale \
  -H "Content-Type: application/json" \
  -d 
    "video_url": "[video_url]",
    "profile": "cinema_4k"
  }
```

**Response:**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "model_used": "fal-ai/seedvr/upscale/video",
  "profile": "cinema_4k"
}
```

**2. Agent -> Skill (Poll for Status)**

The agent waits and then polls the status endpoint.

```bash
curl http://<your_backend_url>/status/a1b2c3d4-e5f6-7890-1234-567890abcdef
```

**Response (In Progress):**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "in_progress",
  "logs": ["Processing frame 100/1200..."]
}
```

**Response (Completed):**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "completed",
  "result": {
    "video_url": "https://.../upscaled_video.mp4"
  }
}
```

**3. Agent -> User**

The agent delivers the final, upscaled video URL to the user.
