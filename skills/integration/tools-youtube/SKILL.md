---
name: youtube
description: Common yt-dlp actions - download videos/audio, extract transcripts, get metadata, handle playlists
---

# YouTube Skill

Swiss army knife for YouTube using yt-dlp. Light scripts for the most common actions.

## Prerequisites

- Python 3.10+
- yt-dlp (`pip install yt-dlp` or `brew install yt-dlp`)
- ffmpeg (for audio extraction: `brew install ffmpeg`)

## Scripts

All scripts are in `skills/youtube/scripts/`. Output goes to `skills/youtube/output/`.

### transcript.py — Extract Subtitles

```bash
python transcript.py "URL"                    # Default: English
python transcript.py "URL" --lang es          # Spanish
python transcript.py "URL" --timestamps       # Keep timestamps
```

### download.py — Download Video/Audio

```bash
# Video
python download.py "URL"                      # Best quality
python download.py "URL" --quality 720        # 720p max

# Audio only
python download.py "URL" --audio              # Best audio → mp3
python download.py "URL" --audio --format m4a # Keep as m4a
```

### info.py — Get Metadata

```bash
python info.py "URL"                          # Title, duration, channel
python info.py "URL" --json                   # Full JSON dump
python info.py "URL" --formats                # Available formats
```

### playlist.py — Playlist Operations

```bash
python playlist.py "URL"                      # List all videos
python playlist.py "URL" --download           # Download all
python playlist.py "URL" --download --audio   # Audio only
python playlist.py "URL" --range 1-5          # Videos 1-5 only
```

## Common Workflows

**Research a video:**
```bash
python info.py "URL"              # Check what we're working with
python transcript.py "URL"        # Get transcript for AI analysis
```

**Archive a podcast:**
```bash
python download.py "URL" --audio  # Just the audio as mp3
```

**Download a course:**
```bash
python playlist.py "URL" --download --quality 720
```

## Output Structure

```
skills/youtube/output/
├── transcripts/      # .txt transcript files
├── videos/           # Downloaded videos
├── audio/            # Extracted audio files
└── info/             # JSON metadata dumps
```

## Notes

- Video IDs work as well as full URLs
- Rate limiting: wait a few minutes between bulk operations
- Some videos have no subtitles available
