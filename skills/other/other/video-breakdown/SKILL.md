---
name: video-breakdown
version: 2.0.0
author: "@wells1137"
tags: ["video", "breakdown", "analysis", "critique", "shot-by-shot", "拉片", "gemini", "bytedance"]

---

# Video Breakdown

A professional video analysis skill powered by a **dual-model architecture**: ByteDance **Seed-2.0-Mini** for rapid previews and Google **Gemini 2.5 Pro** for deep, cinematic-grade analysis. It provides quantitative quality assessments and meticulous shot-by-shot breakdowns (拉片) for content creators, editors, and filmmakers.

## Core Capabilities

| Capability | Description | Use Case |
| :--- | :--- | :--- |
| **Quality Critique** | Scores 7 technical dimensions (resolution, lighting, audio, stability, composition, pacing, overall) on a 1-10 scale with professional commentary. | Evaluate UGC quality; compare video versions; pre-publish QA. |
| **Shot Breakdown (拉片)** | Deconstructs every shot with precise timestamps, shot type, camera movement, subject, action, and narrative function. | Analyze competitor videos; study cinematic techniques; create shot lists. |
| **Content Strategy** | Assesses hook strength, retention curve, platform fit (TikTok/YouTube/Instagram/LinkedIn), and viral potential. | Optimize content for distribution; identify drop-off points; improve engagement. |

## Model Selection

This skill uses two models, selectable via the `model` parameter:

| Model | ID | Best For |
| :--- | :--- | :--- |
| `quick` | `bytedance-seed/seed-2.0-mini` | Fast previews, cost-sensitive tasks, initial screening |
| `full` (default) | `google/gemini-2.5-pro` | Deep analysis, precise timestamps, cinematic-grade breakdowns |

## How It Works

The skill calls a hosted proxy service that routes requests to OpenRouter, which dispatches to the selected model. The response is synchronous — the full analysis result is returned directly in the API response.

### Workflow

1. **Agent**: Calls `POST /api/analyze` with `video_url`, `analysis_type`, and optionally `model`.
2. **Proxy**: Forwards the request to OpenRouter with the selected model.
3. **Model**: Analyzes the video and returns structured JSON.
4. **Agent**: Presents the parsed result to the user.

## Usage

### 1. Quick Quality Assessment (Seed-2.0-Mini)

**Goal**: Get a fast quality report for a video.

**Agent Action**:

```json
{
  "tool": "video-breakdown.analyze",
  "args": {
    "video_url": "https://example.com/my-video.mp4",
    "analysis_type": "quality_critique",
    "model": "quick"
  }
}
```

### 2. Deep Shot-by-Shot Analysis (Gemini 2.5 Pro)

**Goal**: Get a professional, frame-accurate shot breakdown.

**Agent Action**:

```json
{
  "tool": "video-breakdown.analyze",
  "args": {
    "video_url": "https://example.com/scene.mp4",
    "analysis_type": "shot_breakdown",
    "model": "full"
  }
}
```

**Expected Output**:

```json
[
  {
    "shot_number": 1,
    "start_time": "00:00",
    "end_time": "00:04",
    "duration_seconds": 4,
    "shot_type": "Medium Shot",
    "camera_movement": "Static",
    "subject": "Young woman walking toward camera",
    "action": "Subject walks confidently, making direct eye contact",
    "narrative_function": "Establishes protagonist and sets confident tone",
    "audio_notes": "Upbeat music begins, no dialogue"
  }
]
```

### 3. Content Strategy Analysis

**Goal**: Evaluate a video's social media performance potential.

**Agent Action**:

```json
{
  "tool": "video-breakdown.analyze",
  "args": {
    "video_url": "https://example.com/reel.mp4",
    "analysis_type": "content_strategy",
    "model": "full"
  }
}
```

## Backend Service API Reference

The proxy service is deployed on Vercel Pro (300s timeout).

### `POST /api/analyze`

Submits a video for analysis.

**Request Body**:

```json
{
  "video_url": "string (required)",
  "analysis_type": "quality_critique | shot_breakdown | content_strategy (required)",
  "model": "quick | full (optional, default: full)"
}
```

**Response**:

```json
{
  "model_used": "google/gemini-2.5-pro",
  "analysis_type": "shot_breakdown",
  "result": { ... }
}
```

### `GET /api/health`

Returns service status and available models.

## Deployment

The proxy service requires one environment variable:

```
OPENROUTER_API_KEY=<your-openrouter-api-key>
```

Deploy to Vercel from the `proxy/` directory within this skill.
