---
name: producer-music
description: Generate AI music with Producer via AceDataCloud API. Use when creating songs, generating lyrics, extending tracks, creating covers, swapping vocals/instrumentals, replacing song sections, or uploading reference audio. Supports custom lyrics, instrumental-only mode, and multiple creative actions.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable.
---

# Producer Music Generation

Generate AI music through AceDataCloud's Producer API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/producer/audios \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "generate", "prompt": "upbeat electronic dance track with synth leads"}'
```

## Actions

| Action | Description |
|--------|-------------|
| `generate` | Create a new song from prompt or custom lyrics |
| `cover` | Create a cover version of an existing song |
| `extend` | Continue a song from a specific timestamp |
| `upload_cover` | Create a cover from an uploaded reference audio |
| `upload_extend` | Extend from an uploaded reference audio |
| `replace_section` | Replace a time range in an existing song |
| `swap_vocals` | Extract and swap vocal tracks |
| `swap_instrumentals` | Extract and swap instrumental tracks |
| `variation` | Generate a variation of an existing song |

## Workflows

### 1. Generate from Prompt

```json
POST /producer/audios
{
  "action": "generate",
  "prompt": "chill lo-fi hip hop with rain sounds and soft piano"
}
```

### 2. Custom Lyrics Mode

```json
POST /producer/audios
{
  "action": "generate",
  "custom": true,
  "title": "Midnight City",
  "lyric": "[Verse]\nNeon lights reflect on wet streets\n[Chorus]\nMidnight city never sleeps",
  "instrumental": false
}
```

### 3. Instrumental Only

```json
POST /producer/audios
{
  "action": "generate",
  "prompt": "epic orchestral soundtrack for a movie trailer",
  "instrumental": true
}
```

### 4. Extend Song

```json
POST /producer/audios
{
  "action": "extend",
  "audio_id": "existing-audio-id",
  "continue_at": 30
}
```

### 5. Replace Section

```json
POST /producer/audios
{
  "action": "replace_section",
  "audio_id": "existing-audio-id",
  "replace_section_start": 15,
  "replace_section_end": 30
}
```

### 6. Cover from Upload

```json
POST /producer/audios
{
  "action": "upload_cover",
  "audio_id": "uploaded-reference-id",
  "cover_strength": 0.8
}
```

### 7. Generate Lyrics

```json
POST /producer/lyrics
{
  "prompt": "a love song about stargazing on a summer night"
}
```

### 8. Get WAV / Video

```json
POST /producer/wav
{"audio_id": "your-audio-id"}

POST /producer/videos
{"audio_id": "your-audio-id"}
```

### 9. Upload Reference Audio

```json
POST /producer/upload
{
  "audio_url": "https://example.com/reference.mp3"
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | string | See actions table |
| `prompt` | string | Song description (for non-custom mode) |
| `model` | string | Model (e.g., `"FUZZ-2.0 Pro"`) |
| `custom` | boolean | Enable custom lyrics mode |
| `instrumental` | boolean | Pure instrumental (no vocals) |
| `title` | string | Song title |
| `lyric` | string | Custom lyrics with `[Verse]`, `[Chorus]` tags |
| `audio_id` | string | Existing audio ID (for edit actions) |
| `continue_at` | number | Seconds — where to extend from |
| `replace_section_start` | number | Start time of section to replace |
| `replace_section_end` | number | End time of section to replace |
| `lyrics_strength` | 0–1 | Lyrics adherence (default: 0.7) |
| `sound_strength` | 0.2–1 | Sound quality weight (default: 0.7) |
| `cover_strength` | 0.2–1 | Cover similarity (default: 1.0) |
| `weirdness` | 0–1 | Creative randomness (default: 0.5) |
| `seed` | string | Seed for reproducibility |

## Task Polling

```json
POST /producer/tasks
{"task_id": "your-task-id"}
```

## Response Structure

```json
{
  "data": [
    {
      "id": "audio-id",
      "audio_url": "https://cdn.example.com/song.mp3",
      "video_url": "https://cdn.example.com/video.mp4",
      "image_url": "https://cdn.example.com/cover.jpg",
      "title": "Song Title",
      "lyric": "full lyrics...",
      "style": "electronic, dance",
      "model": "FUZZ-2.0 Pro"
    }
  ]
}
```

## Gotchas

- Use `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]` tags in custom lyrics
- `continue_at` is in **seconds** — the song extends from that point
- `replace_section_start` / `replace_section_end` define the time range to regenerate
- `weirdness` at 0 = predictable, at 1 = highly experimental
- Upload a reference audio first (`/producer/upload`), then use the returned ID for `upload_cover` or `upload_extend`
- WAV and video downloads are separate endpoints — call them after the main generation completes
