---
name: grab
description: Download and archive content from URLs (tweets, X articles, Reddit, YouTube). Saves media, text, transcripts, and AI summaries into organized folders.
homepage: https://github.com/jamesalmeida/grab
when: "User shares a URL and wants to download/save/grab it, or asks to download a tweet video, YouTube video, Reddit post, or any media from a URL"
examples:
  - "grab this https://x.com/..."
  - "download this tweet"
  - "save this video"
  - "grab https://youtube.com/..."
  - "grab this reddit post"
tags:
  - download
  - media
  - twitter
  - youtube
  - reddit
  - transcript
  - archive
metadata: { "openclaw": { "emoji": "🫳", "requires": { "bins": ["yt-dlp", "ffmpeg", "whisper"] }, "install": [{ "id": "yt-dlp", "kind": "brew", "formula": "yt-dlp", "bins": ["yt-dlp"], "label": "Install yt-dlp (brew)" }, { "id": "ffmpeg", "kind": "brew", "formula": "ffmpeg", "bins": ["ffmpeg"], "label": "Install ffmpeg (brew)" }, { "id": "openai-whisper", "kind": "brew", "formula": "openai-whisper", "bins": ["whisper"], "label": "Install Whisper (brew)" }] } }
---

# grab 🫳

Download and archive content from URLs into organized folders.

## Setup

### Dependencies
```bash
brew install yt-dlp ffmpeg openai-whisper
```

### Save Location
On first run, `grab` asks where to save files (default: `~/Dropbox/ClawdBox/`).
Config stored in `~/.config/grab/config`. Reconfigure anytime with `grab --config`.

### Transcription (Local Whisper)
Transcription runs locally via Whisper (`turbo` model) — no API key or network calls needed.

### AI Summaries & Smart Titles (Optional)
Set `OPENAI_API_KEY` to enable:
- AI-generated summaries of content
- Smart descriptive folder names (from transcript/image analysis)

Without it, everything still works — you just won't get summaries or auto-renamed folders.

## What It Does

### Tweets (x.com / twitter.com)
- `tweet.txt` — tweet text, author, date, engagement stats
- `video.mp4` — attached video (if any)
- `image_01.jpg`, etc. — attached images (if any)
- `transcript.txt` — auto-transcribed from video (if video)
- `summary.txt` — AI summary of video (if video)
- Folder named by content description

### X Articles
- `article.txt` — full article text with title, author, date
- `summary.txt` — AI summary of article
- Agent handles via OpenClaw browser snapshot
- Script exits with code 2 and `ARTICLE_DETECTED:<id>:<url>` when it detects an article

### Reddit
- `post.txt` — title, author, subreddit, score, date, body text
- `comments.txt` — top comments with authors and scores
- `image_01.jpg`, etc. — attached images or gallery (if any)
- `video.mp4` — attached video (if any)
- `transcript.txt` — auto-transcribed from video (if video)
- `summary.txt` — AI summary of post + discussion
- If Reddit JSON API is blocked (exit code 3), agent uses OpenClaw browser

### YouTube
- `video.mp4` — the video
- `description.txt` — video description
- `thumbnail.jpg` — video thumbnail
- `transcript.txt` — transcribed audio
- `summary.txt` — AI summary

## Output

Downloads are organized by type:
```
<save_dir>/
  XPosts/
    2026-02-03_embrace-change-you-can-shape-your-life/
      tweet.txt, video.mp4, transcript.txt, summary.txt
  XArticles/
    2026-01-20_the-arctic-smokescreen/
      article.txt, summary.txt
  Youtube/
    2026-02-03_how-to-build-an-ai-agent/
      video.mp4, description.txt, thumbnail.jpg, transcript.txt, summary.txt
  Reddit/
    2026-02-03_maybe-maybe-maybe/
      post.txt, comments.txt, video.mp4, summary.txt
```

## Usage

```bash
grab <url>              # Download and archive a URL
grab --config           # Reconfigure save directory
grab --help             # Show help
```

## Requirements

```bash
brew install yt-dlp ffmpeg openai-whisper
```

Transcription uses local Whisper — no API key needed.
`OPENAI_API_KEY` env var optional — enables AI summaries and smart folder titles.
Without it, media downloads and transcription still work.
