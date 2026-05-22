---
name: youtube-transcripts
description: >
  Extract transcripts from YouTube videos. Use when user says "get transcript",
  "transcribe this video", "what does this YouTube video say", "extract captions",
  "youtube transcript", or provides a YouTube URL and wants the text content.
allowed-tools: Bash, Read
triggers:
  - get transcript
  - transcribe video
  - youtube transcript
  - extract captions
  - what does this video say
  - get subtitles from
  - youtube url text
metadata:
  short-description: YouTube transcript extraction
---

# YouTube Transcripts Skill

Extract transcripts from YouTube videos with **three-tier fallback**:

1. **Direct** - youtube-transcript-api (fastest)
2. **Proxy** - IPRoyal residential proxy rotation (handles rate limits)
3. **Whisper** - yt-dlp audio download → OpenAI Whisper (last resort)

## Quick Start

```bash
# Get transcript (auto-fallback through all tiers)
python .agents/skills/youtube-transcripts/youtube_transcript.py get -i dQw4w9WgXcQ

# Skip proxy tier
python .agents/skills/youtube-transcripts/youtube_transcript.py get -i VIDEO_ID --no-proxy

# Skip whisper tier
python .agents/skills/youtube-transcripts/youtube_transcript.py get -i VIDEO_ID --no-whisper

# List available transcript languages
python .agents/skills/youtube-transcripts/youtube_transcript.py list-languages -i VIDEO_ID

# Check proxy configuration
python .agents/skills/youtube-transcripts/youtube_transcript.py check-proxy
```

## Commands

### Get Transcript
```bash
python .agents/skills/youtube-transcripts/youtube_transcript.py get \
  --url "https://youtube.com/watch?v=dQw4w9WgXcQ" \
  --lang en
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--url` | `-u` | YouTube video URL |
| `--video-id` | `-i` | Video ID directly |
| `--lang` | `-l` | Language code (default: en) |
| `--no-proxy` | | Skip proxy tier |
| `--no-whisper` | | Skip Whisper fallback tier |
| `--retries` | `-r` | Max retries per tier (default: 3) |

**Output:** JSON with transcript segments (text, start time, duration)

### List Available Languages
```bash
python .agents/skills/youtube-transcripts/youtube_transcript.py list-languages -i VIDEO_ID
```

**Output:** JSON with available transcript languages

### Check Proxy
```bash
python .agents/skills/youtube-transcripts/youtube_transcript.py check-proxy
python .agents/skills/youtube-transcripts/youtube_transcript.py check-proxy --test-rotation
```

Tests IPRoyal proxy connectivity and IP rotation.

## Output Format

```json
{
  "meta": {
    "video_id": "dQw4w9WgXcQ",
    "language": "en",
    "took_ms": 3029,
    "method": "direct"
  },
  "transcript": [
    {"text": "Hello world", "start": 0.0, "duration": 2.5},
    {"text": "This is a test", "start": 2.5, "duration": 3.0}
  ],
  "full_text": "Hello world This is a test...",
  "errors": []
}
```

**Method values:** `direct`, `proxy`, `whisper`, or `null` (if all failed)

## Three-Tier Fallback

### Tier 1: Direct
- Uses youtube-transcript-api without proxy
- Fastest, no additional cost
- May fail with rate limits on repeated requests

### Tier 2: IPRoyal Proxy
- Uses IPRoyal residential proxy (auto-rotates IPs)
- Handles rate limiting (429) and blocking (403)
- Requires proxy credentials

**Environment variables:**
| Variable | Description |
|----------|-------------|
| `IPROYAL_HOST` | Proxy host (e.g., geo.iproyal.com) |
| `IPROYAL_PORT` | Proxy port (e.g., 12321) |
| `IPROYAL_USER` | Proxy username |
| `IPROYAL_PASSWORD` | Proxy password |

### Tier 3: Whisper Fallback
- Downloads audio with yt-dlp
- Transcribes with OpenAI Whisper API
- Works for videos with disabled captions
- Costs ~$0.006/minute of audio

**Environment variables:**
| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for Whisper |

## Dependencies

```bash
pip install youtube-transcript-api requests yt-dlp openai
```

- `youtube-transcript-api` - Tier 1 & 2
- `requests` - Proxy support
- `yt-dlp` - Tier 3 audio download
- `openai` - Tier 3 transcription

## Integration with Memory

```bash
# Get transcript
python .agents/skills/youtube-transcripts/youtube_transcript.py get -i VIDEO_ID > transcript.json

# Ingest into memory
memory-agent workspace-ingest --source transcript.json --scope youtube
```

## Limitations

- Tier 1-2 require captions (auto-generated or manual)
- Tier 3 (Whisper) works for any video but costs money
- Private/unlisted videos may not be accessible
- Very long videos may exceed Whisper file size limits (25MB)
