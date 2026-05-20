---
name: youtube-downloader
description: "Download and process YouTube content for research. Use when: downloading competitor videos for analysis; extracting audio for podcasts; getting transcripts for content repurposing; archiving webinars; research content curation"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# YouTube Downloader

> Download YouTube videos, extract audio, and get transcripts using yt-dlp - the most reliable YouTube extraction tool.

## When to Use This Skill

- **Competitor research** - Download and analyze competitor videos
- **Content repurposing** - Extract audio for podcasts or transcripts for blogs
- **Training material** - Archive webinars and tutorials
- **Quote extraction** - Get transcripts for pulling quotable moments
- **Offline access** - Save videos for travel or presentations


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## Dependencies

```bash
pip install yt-dlp click
# Optional for transcription:
pip install openai-whisper
```

## Commands

### Download Video
```bash
python scripts/main.py download "https://youtube.com/watch?v=..." --format mp4
python scripts/main.py download "https://youtube.com/watch?v=..." --quality 1080p
```

### Extract Audio
```bash
python scripts/main.py audio "https://youtube.com/watch?v=..." --format mp3
python scripts/main.py audio "https://youtube.com/watch?v=..." --format wav
```

### Get Transcript
```bash
python scripts/main.py transcript "https://youtube.com/watch?v=..."
python scripts/main.py transcript "https://youtube.com/watch?v=..." --translate en
```

### Download Playlist
```bash
python scripts/main.py playlist "https://youtube.com/playlist?list=..." --limit 10
python scripts/main.py playlist "https://youtube.com/playlist?list=..." --audio-only
```

### Get Metadata
```bash
python scripts/main.py info "https://youtube.com/watch?v=..."
python scripts/main.py info "https://youtube.com/watch?v=..." --format json
```

## Examples

### Example 1: Research Competitor Content
```bash
# Get video metadata
python scripts/main.py info "https://youtube.com/watch?v=ABC123"

# Output:
# Title: How We Grew to $1M ARR
# Channel: SaaS Founder
# Duration: 15:32
# Views: 45,230
# Published: 2024-01-15
# Tags: saas, growth, startup

# Download transcript for analysis
python scripts/main.py transcript "https://youtube.com/watch?v=ABC123"
# Output: how-we-grew-to-1m-arr.txt
```

### Example 2: Create Podcast from Webinar
```bash
# Download audio only
python scripts/main.py audio "https://youtube.com/watch?v=WEBINAR" --format mp3 --quality best

# Output: webinar-title.mp3 (ready for podcast editing)

# Get transcript for show notes
python scripts/main.py transcript "https://youtube.com/watch?v=WEBINAR"
# Output: webinar-title.txt
```

### Example 3: Archive Training Playlist
```bash
# Download entire playlist
python scripts/main.py playlist "https://youtube.com/playlist?list=TRAINING" \
  --output ./training-videos/ \
  --limit 20

# Output:
# ./training-videos/
# ├── 01-introduction.mp4
# ├── 02-getting-started.mp4
# └── ...
```

## Quality Options

| Option | Resolution | File Size | Use Case |
|--------|------------|-----------|----------|
| `best` | Highest available | Largest | Archival |
| `1080p` | 1920x1080 | ~1GB/hour | Standard |
| `720p` | 1280x720 | ~500MB/hour | Balance |
| `480p` | 854x480 | ~250MB/hour | Mobile |
| `audio` | N/A | ~100MB/hour | Podcasts |

## Audio Formats

| Format | Quality | Size | Compatibility |
|--------|---------|------|---------------|
| `mp3` | Good | Small | Universal |
| `m4a` | Better | Medium | Apple/Modern |
| `wav` | Lossless | Large | Editing |
| `opus` | Best | Smallest | Modern apps |

## Legal Considerations

⚠️ **Important**: Only download content you have rights to use.

**Generally OK:**
- Your own videos
- Creative Commons content
- Content for personal research/reference
- Content with explicit download permission

**Check First:**
- Competitor content (fair use analysis)
- Content for derivative works
- Anything for commercial use

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## Related Skills

- [whisper-transcription](../whisper-transcription/) - Transcribe downloaded audio
- [video-processing](../video-processing/) - Process downloaded videos
- [content-repurposer](../content-repurposer/) - Repurpose transcripts

## Skill Metadata


- **Mode**: cyborg
```yaml
category: automation
subcategory: content-extraction
dependencies: [yt-dlp]
difficulty: beginner
time_saved: 4+ hours/week
```
