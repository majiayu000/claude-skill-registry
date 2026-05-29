---
name: ingest-youtube
description: >
  Extract transcripts from YouTube videos. Use when user says "get transcript",
  "transcribe this video", "what does this YouTube video say", "extract captions",
  "youtube transcript", or provides a YouTube URL and wants the text content.
allowed-tools: Bash, Read
triggers:
  - ingest youtube
  - youtube ingest
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
3. **Whisper** - yt-dlp audio download → faster-whisper local transcription (free, GPU-accelerated)

## Quick Start

```bash
cd .pi/skills/ingest-youtube

# Get transcript (auto-fallback through all tiers)
uv run python youtube_transcript.py get -i dQw4w9WgXcQ

# Skip proxy tier
uv run python youtube_transcript.py get -i VIDEO_ID --no-proxy

# Skip whisper tier
uv run python youtube_transcript.py get -i VIDEO_ID --no-whisper

# List available transcript languages
uv run python youtube_transcript.py list-languages -i VIDEO_ID

# Check proxy configuration
uv run python youtube_transcript.py check-proxy
```

## Commands

### Get Transcript
```bash
uv run python youtube_transcript.py get \
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
uv run python youtube_transcript.py list-languages -i VIDEO_ID
```

**Output:** JSON with available transcript languages

### Check Proxy
```bash
uv run python youtube_transcript.py check-proxy
uv run python youtube_transcript.py check-proxy --test-rotation
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

**Method values:** `direct`, `proxy`, `whisper-local`, `whisper-api`, or `null` (if all failed)

## Three-Tier Fallback

### Tier 1: Direct
- Uses youtube-transcript-api without proxy
- Fastest, no additional cost
- May fail with rate limits on repeated requests

### Tier 2: IPRoyal Proxy
- Uses IPRoyal residential proxy (auto-rotates IPs)
- Handles rate limiting (429) and blocking (403)
- Requires proxy credentials in `.env` file

**Environment variables (in .env):**
| Variable | Description |
|----------|-------------|
| `IPROYAL_HOST` | Proxy host (e.g., geo.iproyal.com) |
| `IPROYAL_PORT` | Proxy port (e.g., 12321) |
| `IPROYAL_USER` | Proxy username |
| `IPROYAL_PASSWORD` | Proxy password |

### Tier 3: Whisper Fallback
- Downloads audio with yt-dlp
- Transcribes with **faster-whisper** (local, free, GPU-accelerated)
- Falls back to OpenAI Whisper API if local fails
- Works for videos with disabled/unavailable captions

**Note:** Some channels (like TheRemembrancer) have NO native captions, so 100% of videos require Whisper fallback. This is significantly slower but fully automatic.

## Dependencies

```bash
pip install youtube-transcript-api requests yt-dlp openai faster-whisper rich
```

- `youtube-transcript-api` - Tier 1 & 2
- `requests` - Proxy support
- `yt-dlp` - Tier 3 audio download
- `faster-whisper` - Tier 3 local transcription (CTranslate2, 4-8x faster than openai-whisper)
- `openai` - Tier 3 API transcription (fallback if local fails)
- `rich` - Progress display

## Batch Processing

Download transcripts from entire channels with intelligent rate limiting:

### Get Video IDs from Channel

```bash
# Get all video IDs from a YouTube channel
yt-dlp --flat-playlist --print id "https://www.youtube.com/@ChannelName/videos" > videos.txt
```

### Batch Command

```bash
uv run python youtube_transcript.py batch \
    --input videos.txt \
    --output ./transcripts \
    --delay-min 5 --delay-max 15 \
    --whisper \
    --resume
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--input` | `-f` | File with video IDs (one per line) |
| `--output` | `-o` | Output directory for transcripts |
| `--delay-min` | | Minimum delay between requests (default: 30) |
| `--delay-max` | | Maximum delay between requests (default: 60) |
| `--lang` | `-l` | Language code (default: en) |
| `--no-proxy` | | Skip proxy tier |
| `--whisper/--no-whisper` | | Enable/disable Whisper fallback |
| `--resume/--no-resume` | | Resume from last position (default: True) |
| `--max` | `-n` | Max videos to process (0 = all) |

### Smart Delay Logic

The batch processor uses **adaptive delays** based on fetch method:
- **Direct fetch success:** 2-5 seconds (low risk with rotating IPs)
- **Proxy fetch success:** 5-15 seconds
- **Whisper/failed:** Uses configured delay-min/delay-max

This dramatically speeds up channels with native captions while remaining cautious after failures.

### Resume Support

Batch processing saves state after each video to `.batch_state.json` in the output directory. State includes:
- Completed video IDs
- Stats (success, failed, skipped, rate_limited, whisper)
- Current video being processed
- Current method (fetching, whisper)

If interrupted, simply re-run the same command to resume from where it left off.

## Supervisor (Auto-Restart, Hung Detection & Rich Progress)

The supervisor provides:
- **nvtop-style progress display** with GPU monitoring
- **Auto-restart** if batch processes crash
- **Hung detection** - automatically restarts stalled processes
- **Multi-job management** for parallel batch processing
- **JSON status** for agent integration

### Run with Supervisor

```bash
cd .pi/skills/ingest-youtube

# Single batch with supervisor
uv run python supervisor.py run \
    --input videos.txt \
    --output ./transcripts \
    --delay-min 5 --delay-max 15

# Multiple batches from config
uv run python supervisor.py multi --config batches.json
```

### Config File Format (batches.json)

```json
{
    "jobs": [
        {
            "name": "Luetin09",
            "input": "/path/to/luetin09_videos.txt",
            "output": "/path/to/luetin09",
            "delay_min": 5,
            "delay_max": 15,
            "max_restarts": 20,
            "hung_timeout": 600
        },
        {
            "name": "Remembrancer",
            "input": "/path/to/remembrancer_videos.txt",
            "output": "/path/to/remembrancer",
            "delay_min": 5,
            "delay_max": 15,
            "max_restarts": 20,
            "hung_timeout": 2700
        }
    ]
}
```

**Config options:**
| Option | Description | Default |
|--------|-------------|---------|
| `name` | Job display name | filename |
| `input` | Path to video IDs file | required |
| `output` | Output directory | required |
| `delay_min` | Min delay seconds | 30 |
| `delay_max` | Max delay seconds | 60 |
| `max_restarts` | Max automatic restarts | 10 |
| `hung_timeout` | Seconds without progress before restart | 1800 |

**Hung timeout recommendations:**
- Channels with native captions: 600 seconds (10 min)
- Channels requiring Whisper (no captions): 2700 seconds (45 min) - allows time for long video transcription

### Check Status (Agent-Friendly)

```bash
# Human-readable output
uv run python supervisor.py status --output ./transcripts

# JSON output for agents
uv run python supervisor.py status --output ./transcripts --json
```

**JSON output:**
```json
{
  "output_dir": "./transcripts",
  "completed": 150,
  "stats": {"success": 145, "failed": 3, "skipped": 2, "rate_limited": 0, "whisper": 50},
  "current_video": "dQw4w9WgXcQ",
  "current_method": "whisper",
  "last_updated": "2026-01-21 15:30:00",
  "consecutive_failures": 0
}
```

## Local Whisper (Free & Fast)

Tier 3 uses **faster-whisper** (CTranslate2 optimized) by default:
- **Free** - no API key or costs
- **4-8x faster** than openai-whisper
- **GPU accelerated** - uses CUDA float16 when available
- **VAD filtering** - skips silence for additional speed
- **Automatic fallback** - falls back to OpenAI API if local fails

Model size: `base` (good balance of speed/quality)

**Performance benchmarks:**
| Video Length | GPU Time | CPU Time |
|--------------|----------|----------|
| 10 min | ~30 sec | ~2 min |
| 1 hour | ~3 min | ~15 min |
| 10 hours | ~15 min | ~90 min |

## Rate Estimates

| Channel Type | Native Captions | Rate | ETA (1000 videos) |
|--------------|-----------------|------|-------------------|
| Most channels | Yes | ~200-400/hr | 3-5 hours |
| No captions (e.g., Remembrancer) | No (100% Whisper) | ~4-12/hr | 80-250 hours |

## Cross-Agent Monitoring

### Option 1: HTTP API (Recommended)

Start the status API server:
```bash
cd .pi/skills/ingest-youtube
uv run python status_api.py --port 8765
```

Then from any project/agent:
```bash
# List all jobs
curl http://localhost:8765/

# Get all job status (aggregated)
curl http://localhost:8765/all

# Get specific job status
curl http://localhost:8765/status/luetin09
curl http://localhost:8765/status/remembrancer
```

**Response format:**
```json
{
  "jobs": {
    "luetin09": {"completed": 535, "stats": {...}, "current_video": "..."},
    "remembrancer": {"completed": 183, "stats": {...}, "current_video": "..."}
  },
  "totals": {"completed": 718, "success": 88, "failed": 2, "whisper": 24}
}
```

### Option 2: CLI Script

```bash
# Simple status check
python .pi/skills/ingest-youtube/status.py /path/to/transcripts

# Watch mode (updates every 5s)
python .pi/skills/ingest-youtube/status.py /path/to/transcripts --watch
```

### Option 3: Direct File Read

```bash
# Read state file directly (no dependencies)
cat /path/to/transcripts/.batch_state.json | jq '{completed: .completed | length, stats, current_video, last_updated}'
```

**Active batch locations:**
- Luetin09: `/home/graham/workspace/experiments/pi-mono/run/youtube-transcripts/luetin09`
- Remembrancer: `/home/graham/workspace/experiments/pi-mono/run/youtube-transcripts/remembrancer`

## Troubleshooting

### Process appears hung
The supervisor monitors progress and auto-restarts hung processes. If a process shows no progress for `hung_timeout` seconds, it will be killed and restarted.

**Symptoms:**
- `current_method: "fetching"` for >10 minutes → likely hung
- `current_method: "whisper"` for >45 minutes on non-huge video → may be hung

**Manual restart:**
```bash
# Kill specific batch process
kill -9 <PID>
# Supervisor will auto-restart it
```

### All videos using Whisper fallback
Some channels have NO native captions. Check:
```bash
uv run python youtube_transcript.py list-languages -i VIDEO_ID
```
If empty, the video has no captions and requires Whisper.

### Rate limiting despite proxy
- Check proxy is configured: `uv run python youtube_transcript.py check-proxy`
- Verify .env file has correct credentials
- Try `--test-rotation` to verify IP rotation

## Limitations

- Tier 1-2 require captions (auto-generated or manual)
- Tier 3 (Whisper) works for any video but takes longer
- Private/unlisted videos may not be accessible
- Very long videos (>10 hours) may take 15-45 minutes with Whisper
- Some videos may fail due to regional restrictions or removal
