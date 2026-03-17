---
name: youtube-handling
description: Download video/audio, get captions/transcripts, generate AI summaries, analyze comments, take screenshots, and extract metadata from YouTube videos using VidCap.xyz API. Use when working with YouTube content extraction, video summarization, transcript retrieval, comment analysis, or screenshot capture.
---

# YouTube Handling with VidCap.xyz API

Process YouTube videos: download, caption, summarize, screenshot, analyze comments.

## Setup

1. Get API key from [VidCap.xyz](https://vidcap.xyz)
2. Set env: `VIDCAP_API_KEY=your_api_key`

## Quick Reference

| Task | Endpoint | Key Params |
|------|----------|------------|
| Video info | `GET /api/v1/youtube/info` | `url` |
| Download | `GET /api/v1/youtube/download` | `url` |
| Captions | `GET /api/v1/youtube/caption` | `url`, `locale`, `ext` |
| Summary | `GET /api/v1/youtube/summary` | `url`, `model`, `screenshot` |
| Custom summary | `POST /api/v1/youtube/summary-custom` | `url`, `prompt` |
| Article | `GET /api/v1/youtube/article` | `url`, `model` |
| Screenshot | `GET /api/v1/youtube/screenshot` | `url`, `second` |
| Multi-screenshot | `GET /api/v1/youtube/screenshot-multiple` | `url`, `second[]` |
| Comments | `GET /api/v1/youtube/comments` | `url`, `order`, `includeReplies` |
| Search | `GET /api/v1/youtube/search` | `q`, `maxResults`, `order` |

## Authentication

```
Header: X-API-Key: <api_key>
# or
Header: Authorization: Bearer <api_key>
```

## Usage Examples

```bash
# Get video info
curl "https://vidcap.xyz/api/v1/youtube/info?url=https://youtube.com/watch?v=VIDEO_ID" \
  -H "X-API-Key: $VIDCAP_API_KEY"

# Get captions as VTT
curl "https://vidcap.xyz/api/v1/youtube/caption?url=URL&ext=vtt" \
  -H "X-API-Key: $VIDCAP_API_KEY"

# Generate summary with screenshots
curl "https://vidcap.xyz/api/v1/youtube/summary?url=URL&screenshot=1" \
  -H "X-API-Key: $VIDCAP_API_KEY"

# Screenshot at specific time
curl "https://vidcap.xyz/api/v1/youtube/screenshot?url=URL&second=120" \
  -H "X-API-Key: $VIDCAP_API_KEY"
```

## Script Usage

Run the Python script for common tasks:

```bash
# Get video info
python scripts/vidcap.py info "https://youtube.com/watch?v=VIDEO_ID"

# Download video
python scripts/vidcap.py download "URL"

# Get captions
python scripts/vidcap.py caption "URL" --locale en --ext vtt

# Generate summary
python scripts/vidcap.py summary "URL" --screenshot

# Custom summary with prompt
python scripts/vidcap.py summary-custom "URL" --prompt "List key points"

# Take screenshot at 2 minutes
python scripts/vidcap.py screenshot "URL" --second 120

# Get comments
python scripts/vidcap.py comments "URL" --order relevance

# Search YouTube
python scripts/vidcap.py search "query" --max-results 20
```

## References

- Content/AI endpoints: `references/api-content.md`
- Media/Search endpoints: `references/api-media.md`
- Caption formats: `json3`, `srv1`, `srv2`, `srv3`, `ttml`, `vtt`
- AI models: `GET /api/v1/ai/models`
