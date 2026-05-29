---
name: yt-dlp
description: Video and audio downloader supporting thousands of websites including YouTube, Bilibili, Vimeo, and more. Use when Claude needs to download videos or audio from URLs for: (1) Downloading single videos, (2) Extracting audio from videos, (3) Downloading playlists, (4) Downloading subtitles, (5) Format selection and quality control. Automatically handles format merging, subtitle embedding, and metadata preservation.
---

# yt-dlp Video Downloader

yt-dlp is a powerful command-line tool that downloads videos/audio from thousands of websites.

## Prerequisites

Check if yt-dlp is installed:

```bash
yt-dlp --version
```

If not installed, install with:

```bash
# Using pip
pip install yt-dlp

# Or using package managers
# Windows: winget install yt-dlp
# macOS: brew install yt-dlp
# Linux: See https://github.com/yt-dlp/yt-dlp#installation
```

## Quick Start

### Basic Video Download

Download a video in best quality:

```bash
yt-dlp "VIDEO_URL"
```

Download to specific directory with custom filename:

```bash
yt-dlp -o "downloads/%(title)s.%(ext)s" "VIDEO_URL"
```

### Audio Only

Extract audio (MP3/Opus/etc):

```bash
yt-dlp -x --audio-format mp3 "VIDEO_URL"
```

### Format Selection

Select specific quality:

```bash
# Best quality up to 1080p
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "VIDEO_URL"

# Best MP4 video
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" "VIDEO_URL"

# Worst quality (for testing)
yt-dlp -f "worst" "VIDEO_URL"
```

### Playlist Download

Download entire playlist:

```bash
yt-dlp "PLAYLIST_URL"
```

Download specific range from playlist:

```bash
yt-dlp --playlist-start 5 --playlist-end 10 "PLAYLIST_URL"
```

### Subtitles

Download subtitles:

```bash
# Download available subtitles
yt-dlp --write-subs --sub-langs en "VIDEO_URL"

# Embed subtitles into video
yt-dlp --embed-subs --convert-subs srt "VIDEO_URL"

# Download auto-generated subs
yt-dlp --write-auto-subs "VIDEO_URL"
```

## Common Options

| Option | Description |
|--------|-------------|
| `-o OUTPUT` | Output filename template |
| `-f FORMAT` | Format selector |
| `--no-playlist` | Download single video from playlist URL |
| `--playlist-items START-END` | Download playlist range |
| `-x` | Extract audio |
| `--audio-format FORMAT` | Audio format (mp3, m4a, opus, etc) |
| `--write-subs` | Download subtitles |
| `--embed-subs` | Embed subtitles in video |
| `--write-description` | Write video description |
| `--write-info-json` | Write video metadata JSON |
| `--concat-playlist` | Download playlist as single file |
| `--no-overwrites` | Skip existing files |
| `--continue` | Resume incomplete downloads |
| `--proxy URL` | Use proxy |
| `--rate-limit LIMIT` | Download rate limit (e.g., 50K) |

## Python Script

For more complex operations, use the bundled Python script:

```bash
.claude/skills/yt-dlp/scripts/download.py URL [options]
```

The script provides a simple interface with progress bars and error handling.

## Output Templates

Common output template variables:

| Variable | Description |
|----------|-------------|
| `%(id)s` | Video ID |
| `%(title)s` | Video title |
| `%(uploader)s` | Uploader name |
| `%(ext)s` | File extension |
| `%(duration)s` | Duration in seconds |
| `%(view_count)s` | View count |
| `%(upload_date)s` | Upload date (YYYYMMDD) |

Example templates:

```bash
# Organize by uploader
-o "downloads/%(uploader)s/%(title)s.%(ext)s"

# Include date
-o "downloads/%(upload_date)s - %(title)s.%(ext)s"

# Flat directory with ID
-o "downloads/%(id)s.%(ext)s"
```

## Troubleshooting

**Format not available**: Try different format selector or use `-f "best"`

**Download fails**: Check network connection, try `--retry-sleep`

**Subtitle not available**: Video may not have subtitles, try `--list-subs` first

**Rate limiting**: Use `--rate-limit` to avoid being blocked

**Age restricted**: Use `--cookies-from-browser chrome` to pass authentication

## Supported Sites

yt-dlp supports 1000+ websites including:
- YouTube (all features)
- Bilibili
- Vimeo
- Twitter/X
- Instagram
- TikTok
- Twitch
- And many more...

See https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md for full list.
