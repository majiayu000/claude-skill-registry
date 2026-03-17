---
name: download-video
description: Download videos from social media URLs (X/Twitter, YouTube, Instagram, TikTok, etc.) using yt-dlp. Use when saving a video locally, extracting content for transcription, or archiving video references.
argument-hint: "[url]"
allowed-tools: Bash(yt-dlp:*), Bash(ls:*), Bash(mkdir:*)
---

# Video Download Skill

Download a video from `$ARGUMENTS` (a social media URL) to the current directory using `yt-dlp`.

Supports X/Twitter, YouTube, Instagram, TikTok, Reddit, and [1400+ other sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Process

1. **Verify yt-dlp is installed** - check with `which yt-dlp`, suggest `brew install yt-dlp` if missing
2. **Download the video** in the best available quality
3. **Report results** with filename, format, and file size

## Download Command

```bash
yt-dlp -o "%(title)s.%(ext)s" "URL"
```

### Options Reference

```bash
# Best video+audio (default)
yt-dlp -o "%(title)s.%(ext)s" "URL"

# List available formats first
yt-dlp -F "URL"

# Pick a specific format
yt-dlp -f "FORMAT_ID" -o "%(title)s.%(ext)s" "URL"

# Audio only (e.g. for podcasts)
yt-dlp -x --audio-format mp3 -o "%(title)s.%(ext)s" "URL"

# Custom output directory
yt-dlp -o "/path/to/dir/%(title)s.%(ext)s" "URL"
```

## Platform-Specific Notes

| Platform | Notes |
|----------|-------|
| X/Twitter | Works with tweet URLs containing video. May need `--cookies-from-browser` for age-restricted content |
| YouTube | Supports playlists, channels, shorts. Use `-F` to pick resolution |
| Instagram | Reels and stories supported. May require authentication for private accounts |
| TikTok | Direct video URLs work. Watermark-free when available |
| Reddit | Handles v.redd.it links with audio merging automatically |

## After Download

1. **Verify the file**: `ls -lh *.mp4` (or whatever extension was downloaded)
2. Report the filename, format, resolution, and file size to the user
3. If the user wants subtitles or a transcript, suggest using `/transcribe-video`
