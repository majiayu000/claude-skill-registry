---
name: fish-audio
description: Generate AI audio and synthesize voices with Fish Audio via AceDataCloud API. Use when creating text-to-speech audio, synthesizing voices, or generating audio content. Supports multiple voice models and TTS capabilities.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable.
---

# Fish Audio — Voice & Audio Synthesis

Generate AI audio and synthesize voices through AceDataCloud's Fish Audio API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/fish/audios \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a demonstration of AI voice synthesis."}'
```

## Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /fish/audios` | Generate audio from text or parameters |
| `POST /fish/voices` | Voice synthesis and cloning |
| `POST /fish/tasks` | Poll task status |

## Workflows

### 1. Text-to-Speech

```json
POST /fish/audios
{
  "text": "The quick brown fox jumps over the lazy dog.",
  "voice_id": "default"
}
```

### 2. Voice Synthesis with Custom Voice

```json
POST /fish/voices
{
  "text": "Welcome to our platform.",
  "audio_url": "https://example.com/reference-voice.mp3"
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | string | Text to synthesize into speech |
| `voice_id` | string | Voice model to use |
| `audio_url` | string | Reference audio for voice cloning |
| `speed` | number | Speech speed multiplier |

## Task Polling

```json
POST /fish/tasks
{"task_id": "your-task-id"}
```

## Response

```json
{
  "task_id": "abc123",
  "audio_url": "https://cdn.example.com/output.mp3",
  "success": true
}
```

## Gotchas

- Pricing is based on **byte count** of the generated audio
- Voice cloning requires a clear reference audio sample
- Text-to-speech supports multiple languages automatically
- Use the `/fish/voices` endpoint for voice cloning workflows
