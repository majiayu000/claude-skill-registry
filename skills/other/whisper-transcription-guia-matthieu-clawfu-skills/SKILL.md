---
name: whisper-transcription
description: "Transcribe audio and video files to text using OpenAI Whisper. Use when: converting podcasts to blog posts; creating video subtitles; extracting quotes from interviews; repurposing video content to text; building searchable audio archives"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Whisper Transcription

> Transcribe any audio or video to text using OpenAI's Whisper model - the same technology powering ChatGPT voice features.

## When to Use This Skill

- **Podcast repurposing** - Convert episodes to blog posts, show notes, social snippets
- **Video subtitles** - Generate SRT/VTT files for YouTube, social media
- **Interview extraction** - Pull quotes and insights from recorded calls
- **Content audit** - Make audio/video libraries searchable
- **Translation** - Transcribe and translate foreign language content


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
pip install openai-whisper torch ffmpeg-python click
# Also requires ffmpeg installed on system
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

## Commands

### Transcribe Single File
```bash
python scripts/main.py transcribe audio.mp3 --model medium --output transcript.txt
python scripts/main.py transcribe video.mp4 --format srt --output subtitles.srt
```

### Batch Transcription
```bash
python scripts/main.py batch ./recordings/ --format txt --output ./transcripts/
```

### Transcribe + Translate
```bash
python scripts/main.py translate foreign-audio.mp3 --to en
```

### Extract Timestamps
```bash
python scripts/main.py timestamps podcast.mp3 --format json
```

## Examples

### Example 1: Podcast to Blog Post
```bash
# Transcribe 1-hour podcast
python scripts/main.py transcribe episode-42.mp3 --model medium

# Output: episode-42.txt (full transcript with timestamps)
# Processing time: ~5 min for 1 hour audio on M1 Mac
```

### Example 2: YouTube Subtitles
```bash
# Generate SRT for video upload
python scripts/main.py transcribe marketing-video.mp4 --format srt

# Output: marketing-video.srt
# Upload directly to YouTube/Vimeo
```

### Example 3: Batch Process Interview Library
```bash
# Transcribe all recordings in folder
python scripts/main.py batch ./customer-interviews/ --model small --format txt

# Output: ./customer-interviews/*.txt (one per audio file)
```

## Model Selection Guide

| Model | Speed | Accuracy | VRAM | Best For |
|-------|-------|----------|------|----------|
| `tiny` | Fastest | ~70% | 1GB | Quick drafts, short clips |
| `base` | Fast | ~80% | 1GB | Social media clips |
| `small` | Medium | ~85% | 2GB | Podcasts, interviews |
| `medium` | Slow | ~90% | 5GB | Professional transcripts |
| `large` | Slowest | ~95% | 10GB | Critical accuracy needs |

**Recommendation:** Start with `small` for most marketing content. Use `medium` for client deliverables.

## Output Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| `txt` | .txt | Blog posts, analysis |
| `srt` | .srt | Video subtitles (YouTube) |
| `vtt` | .vtt | Web video subtitles |
| `json` | .json | Programmatic access |
| `tsv` | .tsv | Spreadsheet analysis |

## Performance Tips

1. **GPU acceleration** - 10x faster with CUDA GPU
2. **Audio extraction** - Script auto-extracts audio from video
3. **Chunking** - Long files auto-split for memory efficiency
4. **Language detection** - Automatic, or specify with `--language`

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

- [video-processing](../video-processing/) - Extract audio from video
- [youtube-downloader](../youtube-downloader/) - Download videos to transcribe
- [content-repurposer](../content-repurposer/) - Transform transcripts to content
- [podcast-production](../../audio/podcast-production/) - Create podcasts

## Skill Metadata


- **Mode**: cyborg
```yaml
category: automation
subcategory: audio-processing
dependencies: [openai-whisper, torch, ffmpeg-python]
difficulty: beginner
time_saved: 10+ hours/week
```
