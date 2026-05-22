---
name: youtube-to-ebook
description: Transform YouTube videos into beautifully formatted ebook articles with transcripts
---

# YouTube to Ebook

Transform YouTube videos from your favorite channels into well-written magazine-style articles, delivered as an EPUB ebook.

## What This Skill Does

1. Fetches latest videos from YouTube channels (filtering out Shorts)
2. Extracts transcripts from those videos
3. Transforms transcripts into polished articles using Claude
4. Packages articles into an EPUB ebook for reading on any device

## Quick Start

Ask: "Set up YouTube to ebook for me"

I'll guide you through:
1. Creating a project folder
2. Setting up YouTube API access
3. Configuring your favorite channels
4. Generating your first ebook

## Requirements

- Python 3.8+
- YouTube Data API key (free from Google Cloud Console)
- Anthropic API key (for Claude)

## Commands

| Command | Description |
|---------|-------------|
| `python main.py` | Generate ebook from latest videos |
| `python main.py --channels` | Edit channel list |
| `python dashboard.py` | Launch web dashboard |

## Key Files

```
youtube-newsletter/
├── get_videos.py      # Fetch latest videos
├── get_transcripts.py # Extract transcripts
├── write_articles.py  # Transform to articles
├── send_email.py      # Create EPUB & send
├── main.py            # Run full pipeline
├── channels.txt       # Your channel list
└── .env               # API keys
```

## Known Pitfalls & Solutions

### 1. YouTube Shorts Detection
**Problem**: Filtering by duration doesn't work—some Shorts are longer than 60 seconds.

**Solution**: Check if the `/shorts/` URL resolves:
```python
def is_youtube_short(video_id):
    shorts_url = f"https://www.youtube.com/shorts/{video_id}"
    response = requests.head(shorts_url, allow_redirects=True, timeout=5)
    return "/shorts/" in response.url
```

### 2. Videos Not in Chronological Order
**Problem**: YouTube Search API doesn't return truly chronological results.

**Solution**: Use the channel's uploads playlist via `playlistItems` API:
```python
# Get uploads playlist ID from channel
channel_info = youtube.channels().list(
    part="contentDetails",
    forHandle=handle
).execute()
uploads_playlist_id = channel_info["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# Fetch from uploads playlist (always chronological)
youtube.playlistItems().list(
    part="snippet",
    playlistId=uploads_playlist_id,
    maxResults=15
).execute()
```

### 3. Transcript API Syntax
**Problem**: `YouTubeTranscriptApi.get_transcript()` no longer works.

**Solution**: Use instance method:
```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch(video_id)
```

### 4. Rate Limiting on Transcripts
**Problem**: Fetching many transcripts quickly triggers rate limits.

**Solution**: Add 2-second delays between requests:
```python
import time
for video in videos:
    transcript = get_transcript(video["video_id"])
    time.sleep(2)
```

### 5. Transcript Accuracy (Names, Terms)
**Problem**: Auto-transcripts misspell names and technical terms.

**Solution**: Include video title and description in Claude's context—these usually have correct spellings.

### 6. Cloud Automation Blocked
**Problem**: GitHub Actions and cloud servers are blocked by YouTube for transcript fetching.

**Solution**: Run automation locally on your Mac using `launchd`:
```xml
<!-- ~/Library/LaunchAgents/com.youtube.ebook.plist -->
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.youtube.ebook</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/main.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>3</integer>
        <key>Hour</key>
        <integer>7</integer>
    </dict>
</dict>
</plist>
```

## Customization

### Writing Style
Edit the prompt in `write_articles.py` to change article tone:
- Magazine style (default)
- Academic summary
- Casual blog post
- Technical documentation

### Email Delivery (Optional)
Add Gmail credentials to `.env` to receive ebooks via email:
```
GMAIL_ADDRESS=your@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

## Workflow

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐    ┌────────────┐
│ Fetch Videos│───▶│Get Transcripts│───▶│Write Articles │───▶│Create EPUB │
│ (YouTube API)│    │(Transcript API)│    │  (Claude AI)  │    │ (ebooklib) │
└─────────────┘    └──────────────┘    └───────────────┘    └────────────┘
```

## Example Output

The generated EPUB contains:
- Table of contents with all articles
- Clean, readable formatting
- Original video links for reference
- Mobile-friendly styling
