---
name: YT Meta - YouTube Metadata Extractor
description: Extract YouTube video info, channel stats, playlists, comments. No API key required. Free CLI tool for content research and analysis.
---

# YT Meta

Extract YouTube metadata without API keys. Videos, channels, playlists, comments.

## Installation

```bash
npm install -g yt-meta-cli
```

## Commands

### Video Metadata

```bash
yt-meta video dQw4w9WgXcQ
yt-meta video https://youtu.be/dQw4w9WgXcQ
yt-meta video "https://youtube.com/watch?v=VIDEO_ID"
```

Returns: title, description, views, likes, duration, upload date, tags, thumbnails.

### Channel Info

```bash
yt-meta channel @mkbhd
yt-meta channel @channel --videos           # Include recent videos
yt-meta channel @channel --videos --limit 100
```

### Playlist

```bash
yt-meta playlist PLrAXtmErZgOei...
yt-meta playlist PLxxx --all               # Entire playlist
```

### Search

```bash
yt-meta search "react hooks tutorial"
yt-meta search "javascript" --limit 50
yt-meta search "gaming" --sort views
```

### Comments

```bash
yt-meta comments dQw4w9WgXcQ
yt-meta comments VIDEO_ID --limit 500
yt-meta comments VIDEO_ID --sort top
```

## Output Formats

```bash
yt-meta video ID                 # JSON (default)
yt-meta playlist ID -o jsonl     # One per line
yt-meta search "query" -o csv    # Spreadsheet
yt-meta video ID -o table        # Terminal
yt-meta channel @x --save out.json
```

## Example Output

```json
{
  "id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "channel": "Rick Astley",
  "views": 1400000000,
  "likes": 15000000,
  "duration": "3:33",
  "uploadDate": "2009-10-25",
  "tags": ["rick astley", "never gonna give you up"]
}
```

## Common Use Cases

**Analyze video performance:**
```bash
yt-meta video VIDEO_ID -o json
```

**Export channel's videos:**
```bash
yt-meta channel @mkbhd --videos --limit 500 > videos.json
```

**Research trending topics:**
```bash
yt-meta search "ai tools 2024" --sort views -o csv
```

---

**Built by [LXGIC Studios](https://lxgicstudios.com)**

🔗 [GitHub](https://github.com/lxgicstudios/yt-meta) · [Twitter](https://x.com/lxgicstudios)
