---
name: youtube-transcription
description: >-
  Transcribe YouTube videos to text using OpenAI Whisper and yt-dlp. Use when
  the user wants to get a transcript from a YouTube video, generate subtitles,
  convert video speech to text, create SRT/VTT captions, or extract spoken
  content from YouTube URLs.
license: Apache-2.0
compatibility: >-
  Requires Python 3.8+, ffmpeg, and CUDA GPU recommended for large models.
  Install: pip install openai-whisper yt-dlp. CPU works but is slower.
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: content
  tags: [youtube, transcription, whisper, subtitles, speech-to-text]
---

# YouTube Video Transcription

Transcribe YouTube videos to text using OpenAI Whisper and yt-dlp.

## Overview

This skill downloads audio from YouTube videos using yt-dlp and transcribes it using OpenAI's Whisper model. Supports multiple output formats (txt, srt, vtt, json) and various model sizes for different accuracy/speed tradeoffs.

## Instructions

### 1. Install dependencies

```bash
# Install whisper and yt-dlp
pip install openai-whisper yt-dlp

# Verify ffmpeg is installed (required for audio processing)
ffmpeg -version
```

If ffmpeg is missing:
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt install ffmpeg`
- Windows: Download from https://ffmpeg.org/download.html

### 2. Download audio from YouTube

```bash
# Download best audio quality as WAV
yt-dlp -x --audio-format wav -o "%(title)s.%(ext)s" "YOUTUBE_URL"

# Download as MP3 (smaller file)
yt-dlp -x --audio-format mp3 -o "%(title)s.%(ext)s" "YOUTUBE_URL"

# Download with video ID as filename (safer for special characters)
yt-dlp -x --audio-format wav -o "%(id)s.%(ext)s" "YOUTUBE_URL"
```

### 3. Choose Whisper model

| Model | Parameters | VRAM | Relative Speed | Use Case |
|-------|------------|------|----------------|----------|
| tiny | 39M | ~1 GB | ~32x | Quick drafts, testing |
| base | 74M | ~1 GB | ~16x | Fast transcription |
| small | 244M | ~2 GB | ~6x | Good balance |
| medium | 769M | ~5 GB | ~2x | High accuracy |
| large | 1550M | ~10 GB | 1x | Best accuracy |

English-only models (`tiny.en`, `base.en`, `small.en`, `medium.en`) are faster for English content.

### 4. Run transcription

**CLI approach:**
```bash
# Basic transcription (auto-detect language)
whisper audio.wav --model medium

# Specify language for better accuracy
whisper audio.wav --model medium --language en

# Output specific format
whisper audio.wav --model medium --output_format srt

# All formats at once
whisper audio.wav --model medium --output_format all

# Specify output directory
whisper audio.wav --model medium --output_dir ./transcripts
```

**Python approach:**
```python
import whisper

# Load model (downloads on first run)
model = whisper.load_model("medium")

# Transcribe
result = model.transcribe("audio.wav", language="en")

# Get plain text
print(result["text"])

# Get segments with timestamps
for segment in result["segments"]:
    print(f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}")
```

### 5. One-liner pipeline

Combine download and transcription:
```bash
# Download and transcribe in one command
yt-dlp -x --audio-format wav -o "audio.wav" "YOUTUBE_URL" && whisper audio.wav --model medium --output_format all
```

### 6. Alternative: yt-whisper tool

For simpler workflow, use the dedicated yt-whisper package:
```bash
# Install
pip install git+https://github.com/m1guelpf/yt-whisper.git

# Transcribe directly from URL
yt_whisper "https://www.youtube.com/watch?v=VIDEO_ID"

# With options
yt_whisper "YOUTUBE_URL" --model medium --language en --output_format srt
```

## Output Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| txt | .txt | Plain text transcript |
| srt | .srt | SubRip subtitle format (with timestamps) |
| vtt | .vtt | WebVTT subtitle format |
| tsv | .tsv | Tab-separated values |
| json | .json | Full data with word-level timestamps |

## Examples

<example>
User: Transcribe this YouTube video to text
Steps:
1. yt-dlp -x --audio-format wav -o "video.wav" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
2. whisper video.wav --model medium --language en --output_format txt
Output: video.txt with full transcript
</example>

<example>
User: Generate SRT subtitles for a YouTube lecture
Steps:
1. yt-dlp -x --audio-format wav -o "lecture.wav" "https://www.youtube.com/watch?v=LECTURE_ID"
2. whisper lecture.wav --model medium --output_format srt
Output: lecture.srt with timestamped subtitles
</example>

<example>
User: Transcribe a Spanish YouTube video
Steps:
1. yt-dlp -x --audio-format wav -o "spanish.wav" "https://www.youtube.com/watch?v=VIDEO_ID"
2. whisper spanish.wav --model medium --language es --output_format all
Output: spanish.txt, spanish.srt, spanish.vtt, spanish.json
</example>

<example>
User: Quick transcription of a short video (speed over accuracy)
Command: yt-dlp -x --audio-format mp3 -o "quick.mp3" "URL" && whisper quick.mp3 --model tiny.en
</example>

<example>
User: Get transcript with timestamps in Python
```python
import whisper
model = whisper.load_model("medium")
result = model.transcribe("audio.wav")
for seg in result["segments"]:
    print(f"[{seg['start']:.1f}s] {seg['text']}")
```
</example>

## Guidelines

- Use `--language` flag when you know the spoken language for significantly better accuracy
- For long videos (>1 hour), use `small` or `medium` model to balance speed and accuracy
- English-only models (`.en` suffix) are faster and more accurate for English content
- GPU with CUDA dramatically speeds up transcription; CPU works but is 5-10x slower
- If transcription fails, ensure ffmpeg is properly installed and in PATH
- For videos with background music, larger models (medium/large) handle it better
- Clean up audio files after transcription to save disk space
- Use `--output_format all` to get every format at once, then choose what you need
