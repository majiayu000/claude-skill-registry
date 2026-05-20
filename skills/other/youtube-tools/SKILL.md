---
name: youtube-tools
description: Free YouTube video downloading, transcript extraction, and metadata retrieval using yt-dlp. Use this skill for downloading YouTube videos (single or bulk), extracting transcripts/subtitles, getting video metadata, or downloading audio-only. This is FREE (no API keys) unlike Apify. Triggers on YouTube download requests, transcript extraction, video metadata, or bulk video downloads.
---

# YouTube Tools (yt-dlp)

## Overview

Free, local YouTube operations using yt-dlp. No API keys required, no per-video costs. Works offline after installation.

## When to Use This vs Apify

```
┌─────────────────────────────────────────────────────────────────┐
│ DECISION: YouTube Tools (yt-dlp) vs Apify                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Use youtube-tools (FREE) when:                                  │
│ ├── Downloading videos to local storage                         │
│ ├── Extracting transcripts/subtitles                            │
│ ├── Getting video metadata (title, duration, views, etc.)       │
│ ├── Bulk downloading playlists or channels                      │
│ ├── Converting to audio-only (MP3)                              │
│ └── You want zero API costs                                     │
│                                                                 │
│ Use apify-scrapers when:                                        │
│ ├── Scraping YouTube SEARCH results                             │
│ ├── Getting comments at scale                                   │
│ ├── Channel analytics and statistics                            │
│ ├── Trending video discovery                                    │
│ └── You need cloud-based processing                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Decision Tree

```
What do you need?
│
├── Download video(s)
│   ├── Single video → scripts/download_video.py URL
│   ├── Multiple videos → scripts/download_video.py --urls-file list.txt
│   ├── Playlist → scripts/download_video.py "playlist_url"
│   ├── Audio only → scripts/download_video.py URL --audio-only
│   └── Specific quality → scripts/download_video.py URL --quality 720p
│
├── Get transcript/subtitles
│   ├── Auto-generated captions → scripts/get_transcript.py URL
│   ├── Manual subtitles → scripts/get_transcript.py URL --manual-only
│   ├── Specific language → scripts/get_transcript.py URL --lang es
│   └── All available → scripts/get_transcript.py URL --all-langs
│
├── Get video metadata
│   ├── Single video → scripts/get_video_info.py URL
│   ├── Multiple videos → scripts/get_video_info.py --urls-file list.txt
│   └── Playlist info → scripts/get_video_info.py "playlist_url"
│
└── Advanced
    ├── Age-restricted → scripts/download_video.py URL --cookies-from-browser chrome
    ├── Private videos → Requires authentication (see references/yt-dlp-guide.md)
    └── Live streams → scripts/download_video.py URL --live-from-start
```

## Environment Setup

```bash
# Install yt-dlp (required)
pip install yt-dlp

# Optional: Install ffmpeg for format conversion
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
winget install ffmpeg
```

**No API keys required!** This is completely free.

## Common Usage

### Download Single Video
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download with Specific Quality
```bash
python scripts/download_video.py "https://youtu.be/VIDEO_ID" --quality 1080p
```

### Download Audio Only (MP3)
```bash
python scripts/download_video.py "https://youtube.com/watch?v=VIDEO_ID" --audio-only
```

### Download Entire Playlist
```bash
python scripts/download_video.py "https://youtube.com/playlist?list=PLAYLIST_ID" --output-dir ./videos
```

### Bulk Download from File
```bash
# Create urls.txt with one URL per line
python scripts/download_video.py --urls-file urls.txt --output-dir ./downloads
```

### Get Transcript
```bash
python scripts/get_transcript.py "https://youtube.com/watch?v=VIDEO_ID"
```

### Get Transcript in Specific Language
```bash
python scripts/get_transcript.py "https://youtu.be/VIDEO_ID" --lang es
```

### Get Video Metadata
```bash
python scripts/get_video_info.py "https://youtube.com/watch?v=VIDEO_ID"
```

### Get Metadata for Multiple Videos
```bash
python scripts/get_video_info.py --urls-file videos.txt --output metadata.json
```

## Output Location

All outputs save to `.tmp/youtube/` by default:
- Videos: `.tmp/youtube/videos/`
- Audio: `.tmp/youtube/audio/`
- Transcripts: `.tmp/youtube/transcripts/`
- Metadata: `.tmp/youtube/metadata/`

## Cost

**FREE** - No API keys, no per-video costs, no subscriptions.

## Security Notes

### Safe by Design
- URL validation: Only accepts YouTube URLs (youtube.com, youtu.be)
- Filename sanitization: Removes dangerous characters
- Output restriction: Only writes to `.tmp/` directory
- No shell injection: Uses subprocess with argument lists, not string concatenation
- No stored credentials: Cookies only used when explicitly requested

### Copyright Warning
- Only download content you have rights to access
- Respect YouTube's Terms of Service
- Do not redistribute copyrighted content
- Use for personal/educational purposes

### Rate Limiting
- yt-dlp has built-in rate limiting
- For bulk downloads, use `--sleep-interval 5` to avoid throttling
- YouTube may temporarily block IPs with excessive requests

## Troubleshooting

### Issue: "Video unavailable"
**Cause:** Video is private, age-restricted, or region-locked
**Solution:** Use `--cookies-from-browser chrome` for age-restricted content

### Issue: "Unable to extract video data"
**Cause:** YouTube changed their page structure
**Solution:** Update yt-dlp: `pip install -U yt-dlp`

### Issue: No subtitles found
**Cause:** Video has no captions (auto or manual)
**Solution:** Use `--list-subs` to see available subtitles first

### Issue: Slow downloads
**Cause:** YouTube throttling or network issues
**Solution:** Try `--concurrent-fragments 4` for faster downloads

### Issue: Format conversion failed
**Cause:** ffmpeg not installed
**Solution:** Install ffmpeg (see Environment Setup)

## Integration Patterns

### Download + Transcribe + Summarize
```bash
# 1. Download video
python scripts/download_video.py "URL" --output-dir .tmp/video

# 2. Get transcript
python scripts/get_transcript.py "URL" --output .tmp/transcript.txt

# 3. Use content-generation to summarize
# (transcript file is now ready for summarization)
```

### Bulk Research Workflow
```bash
# 1. Get metadata for research videos
python scripts/get_video_info.py --urls-file research_videos.txt --output .tmp/metadata.json

# 2. Download transcripts for text analysis
python scripts/get_transcript.py --urls-file research_videos.txt --output-dir .tmp/transcripts

# 3. Use parallel-research to analyze content
```

### Course Content Download
```bash
# Download entire playlist as course modules
python scripts/download_video.py "PLAYLIST_URL" --output-dir .tmp/course --quality 720p

# Get all transcripts for notes
python scripts/get_transcript.py "PLAYLIST_URL" --output-dir .tmp/course/transcripts
```

## Resources

- **references/yt-dlp-guide.md** - Complete yt-dlp reference with all options
- **yt-dlp documentation**: https://github.com/yt-dlp/yt-dlp#readme
