---
name: youtube-downloader
description: Download videos, audio, playlists, and channels from YouTube and 1000+ websites using yt-dlp. Supports quality selection, format conversion, subtitle download, playlist filtering, metadata extraction, thumbnail download, and batch operations. Use when downloading YouTube videos in any quality (4K, 8K, HDR), extracting audio as MP3/M4A/FLAC, downloading entire playlists/channels, getting subtitles in multiple languages, converting to specific formats, downloading live streams, archiving content, or batch processing multiple URLs. Optimized for reliability with automatic retries, rate limiting, and error handling.
license: MIT
---

# YouTube & Video Downloader Skill

Download videos and audio from YouTube and 1000+ other websites using yt-dlp, the most powerful and actively maintained YouTube downloader.

## When to Use This Skill

Use when you need to:
- Download YouTube videos in any quality (144p to 8K, HDR, 60fps)
- Extract audio from videos (MP3, M4A, FLAC, WAV, Opus)
- Download entire playlists or channels
- Get video subtitles/captions in multiple languages
- Download live streams or premieres
- Archive content before it's deleted
- Download from 1000+ websites (not just YouTube)
- Batch download multiple videos
- Download with custom naming and organization
- Extract video metadata and thumbnails

## Supported Websites (1000+)

### Video Platforms
- YouTube (videos, playlists, channels, shorts, live streams)
- Vimeo, Dailymotion, Twitter/X, Facebook
- TikTok, Instagram (videos, reels, stories)
- Twitch (VODs, clips, live streams)
- Reddit (v.redd.it videos)
- Pornhub (videos)
- Youporn (videos)

### Educational
- Coursera, Udemy, Khan Academy
- edX, Pluralsight, LinkedIn Learning

### News & Media
- CNN, BBC, NBC, CBS
- ESPN, Sky Sports

### And 1000+ more...

## Installation

yt-dlp requires Python 3.7+ and ffmpeg for format conversion:

```bash
# Install yt-dlp (if not already installed)
pip install -U yt-dlp

# Install ffmpeg (required for format conversion)
# Ubuntu/Debian:
sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# Verify installation
yt-dlp --version
ffmpeg -version
```

## Basic Usage

### Download Best Quality Video
```bash
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download Best Quality Audio (as M4A)
```bash
yt-dlp -f "bestaudio" "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download and Convert to MP3
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download Specific Quality
```bash
# 1080p video with best audio
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" "URL"

# 4K video
yt-dlp -f "bestvideo[height<=2160]+bestaudio/best" "URL"

# 720p video
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" "URL"
```

## Advanced Features

### Download Entire Playlist
```bash
yt-dlp "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

### Download Playlist Range
```bash
# Videos 1-10
yt-dlp --playlist-start 1 --playlist-end 10 "PLAYLIST_URL"

# Videos from #5 onwards
yt-dlp --playlist-start 5 "PLAYLIST_URL"
```

### Download All Videos from Channel
```bash
yt-dlp "https://www.youtube.com/@ChannelName/videos"
```

### Download with Subtitles
```bash
# Download all available subtitles
yt-dlp --write-subs --write-auto-subs --sub-langs "en,es,fr" "URL"

# Download and embed subtitles
yt-dlp --write-subs --embed-subs --sub-langs "en.*" "URL"

# Download only subtitles (no video)
yt-dlp --skip-download --write-subs --write-auto-subs "URL"
```

### Custom Naming and Organization
```bash
# Custom filename template
yt-dlp -o "%(uploader)s/%(playlist)s/%(title)s.%(ext)s" "PLAYLIST_URL"

# By date uploaded
yt-dlp -o "%(upload_date)s - %(title)s.%(ext)s" "URL"

# With video ID
yt-dlp -o "%(title)s [%(id)s].%(ext)s" "URL"
```

### Download Thumbnails
```bash
# Download and embed thumbnail
yt-dlp --write-thumbnail --embed-thumbnail "URL"

# Download thumbnail only
yt-dlp --write-thumbnail --skip-download "URL"
```

### Download Metadata
```bash
# Write metadata to JSON file
yt-dlp --write-info-json "URL"

# Write metadata to description file
yt-dlp --write-description "URL"
```

## Quality Selection Guide

### Video Quality Formats
```bash
# Best overall quality (may be WebM)
yt-dlp -f "bestvideo+bestaudio/best" "URL"

# Best MP4 format (most compatible)
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" "URL"

# 4K (2160p) maximum
yt-dlp -f "bestvideo[height<=2160]+bestaudio" "URL"

# 1080p maximum
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "URL"

# 720p maximum
yt-dlp -f "bestvideo[height<=720]+bestaudio" "URL"

# 60fps preferred
yt-dlp -f "bestvideo[fps>30]+bestaudio/best" "URL"
```

### Audio Quality Formats
```bash
# Best audio quality (extract as M4A)
yt-dlp -f "bestaudio" "URL"

# Extract as MP3 (best quality)
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"

# Extract as FLAC (lossless)
yt-dlp -x --audio-format flac "URL"

# Extract as Opus (efficient)
yt-dlp -x --audio-format opus "URL"

# Extract as WAV (uncompressed)
yt-dlp -x --audio-format wav "URL"
```

## List Available Formats

Before downloading, check what formats are available:

```bash
yt-dlp -F "URL"
```

This shows all available video and audio streams with:
- Format ID
- Extension
- Resolution
- FPS
- Codec
- File size
- Bitrate

Then download specific format:
```bash
yt-dlp -f FORMAT_ID "URL"
```

## Batch Download

### From File
Create a text file with URLs (one per line):
```
https://www.youtube.com/watch?v=VIDEO1
https://www.youtube.com/watch?v=VIDEO2
https://www.youtube.com/watch?v=VIDEO3
```

Download all:
```bash
yt-dlp -a urls.txt
```

### With Archive
Track downloaded videos to avoid re-downloading:
```bash
yt-dlp --download-archive archive.txt "PLAYLIST_URL"
```

This creates `archive.txt` with IDs of downloaded videos. On subsequent runs, yt-dlp skips already downloaded videos.

## Filtering and Selection

### Date Filters
```bash
# Videos from 2024
yt-dlp --dateafter 20240101 "CHANNEL_URL"

# Videos before 2023
yt-dlp --datebefore 20230101 "CHANNEL_URL"

# Videos between dates
yt-dlp --dateafter 20230101 --datebefore 20231231 "CHANNEL_URL"
```

### View Count Filters
```bash
# Videos with 1M+ views
yt-dlp --match-filter "view_count > 1000000" "CHANNEL_URL"

# Videos with less than 10K views
yt-dlp --match-filter "view_count < 10000" "CHANNEL_URL"
```

### Duration Filters
```bash
# Videos longer than 10 minutes
yt-dlp --match-filter "duration > 600" "PLAYLIST_URL"

# Videos shorter than 5 minutes
yt-dlp --match-filter "duration < 300" "PLAYLIST_URL"
```

## Live Streams

### Download Live Stream
```bash
# Wait for stream to start and download
yt-dlp --wait-for-video 60 "LIVE_STREAM_URL"

# Download stream as it's happening (may be incomplete if interrupted)
yt-dlp "LIVE_STREAM_URL"
```

## Rate Limiting and Network Options

```bash
# Limit download speed (e.g., 1MB/s)
yt-dlp --limit-rate 1M "URL"

# Set number of retries
yt-dlp --retries 10 "URL"

# Wait between downloads (in seconds)
yt-dlp --sleep-interval 5 "PLAYLIST_URL"

# Use specific proxy
yt-dlp --proxy "http://proxy.server:port" "URL"

# Use cookies from browser (bypass age restrictions)
yt-dlp --cookies-from-browser chrome "URL"
```

## Geo-Restriction Bypass

```bash
# Use proxy
yt-dlp --proxy "socks5://proxy.server:1080" "URL"

# Use specific geo-bypass country
yt-dlp --geo-bypass-country US "URL"
```

## Post-Processing

### Video Post-Processing
```bash
# Merge video and audio to MP4
yt-dlp --merge-output-format mp4 "URL"

# Re-encode to H.264
yt-dlp --recode-video mp4 "URL"

# Add metadata
yt-dlp --add-metadata "URL"

# Embed thumbnail
yt-dlp --embed-thumbnail "URL"
```

### Audio Post-Processing
```bash
# Extract audio and convert to MP3
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"

# Add metadata to audio file
yt-dlp -x --audio-format mp3 --add-metadata "URL"
```

## Common Use Cases

### 1. Download Music from YouTube
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 \
  -o "%(artist)s - %(title)s.%(ext)s" \
  --add-metadata \
  --embed-thumbnail \
  "MUSIC_VIDEO_URL"
```

### 2. Download Educational Course
```bash
yt-dlp -o "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" \
  --write-subs --embed-subs \
  --write-info-json \
  "COURSE_PLAYLIST_URL"
```

### 3. Archive Channel (New Videos Only)
```bash
yt-dlp --download-archive downloaded.txt \
  -o "%(uploader)s/%(upload_date)s - %(title)s.%(ext)s" \
  -f "bestvideo[height<=1080]+bestaudio/best" \
  "https://www.youtube.com/@ChannelName/videos"
```

### 4. Download Podcast as Audio
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 \
  -o "%(playlist)s/%(playlist_index)s. %(title)s.%(ext)s" \
  --add-metadata \
  "PODCAST_PLAYLIST_URL"
```

### 5. Download Conference Talks
```bash
yt-dlp -f "bestvideo[height<=720]+bestaudio" \
  -o "Conference/%(title)s.%(ext)s" \
  --write-subs --embed-subs --sub-langs en \
  "CONFERENCE_PLAYLIST_URL"
```

### 6. Batch Download from Multiple Sites
```bash
# Create urls.txt with mixed URLs (YouTube, Vimeo, etc.)
yt-dlp -a urls.txt \
  -f "bestvideo+bestaudio/best" \
  -o "%(extractor)s/%(uploader)s/%(title)s.%(ext)s"
```

## Configuration File

Create `~/.config/yt-dlp/config` for default options:

```
# Default format
-f bestvideo[height<=1080]+bestaudio/best

# Output template
-o ~/Downloads/%(uploader)s/%(title)s.%(ext)s

# Embed metadata
--add-metadata
--embed-thumbnail

# Write subtitles
--write-subs
--sub-langs en

# Continue on errors
--ignore-errors

# Rate limit
--limit-rate 5M
```

## Troubleshooting

### Video Unavailable
```bash
# Try with cookies from browser
yt-dlp --cookies-from-browser chrome "URL"

# Update yt-dlp
pip install -U yt-dlp
```

### Age-Restricted Content
```bash
# Use browser cookies
yt-dlp --cookies-from-browser firefox "URL"

# Or login with credentials
yt-dlp --username YOUR_USERNAME --password YOUR_PASSWORD "URL"
```

### Format Not Available
```bash
# List all formats first
yt-dlp -F "URL"

# Then select specific format
yt-dlp -f FORMAT_ID "URL"
```

### Slow Downloads
```bash
# Use multiple connections
yt-dlp --concurrent-fragments 4 "URL"

# Or use external downloader
yt-dlp --external-downloader aria2c "URL"
```

## Integration with Other Tools

### FFmpeg Integration
yt-dlp automatically uses ffmpeg when installed for:
- Merging video and audio streams
- Converting formats
- Embedding thumbnails and metadata
- Post-processing

### Aria2c for Faster Downloads
```bash
yt-dlp --external-downloader aria2c \
  --external-downloader-args "-x 16 -s 16 -k 1M" \
  "URL"
```

## Legal and Ethical Considerations

⚠️ **Important**:
- Only download content you have rights to
- Respect copyright and Terms of Service
- Don't distribute copyrighted content
- YouTube's ToS prohibits downloading most content
- Use for personal archival and educational purposes
- Many creators offer official download options
- Consider supporting creators through official channels

## Performance Tips

1. **Use Archive Files**: Track downloads to avoid re-downloading
2. **Limit Rate**: Prevent network congestion with `--limit-rate`
3. **Concurrent Fragments**: Speed up with `--concurrent-fragments 4`
4. **Choose Format Wisely**: Lower quality = faster download
5. **Use External Downloader**: aria2c can be faster than built-in
6. **Batch Smartly**: Process in chunks, not all at once

## Updates

Keep yt-dlp updated for best compatibility:
```bash
# Update via pip
pip install -U yt-dlp

# Check version
yt-dlp --version
```

## Resources

- **yt-dlp GitHub**: https://github.com/yt-dlp/yt-dlp
- **Supported Sites**: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
- **Format Selection**: https://github.com/yt-dlp/yt-dlp#format-selection

---

**Version**: 1.0.0
**Last Updated**: 2025-11-07
**Maintained by**: Claude Code Skills Collection
