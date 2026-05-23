---
name: gemini-caption-transcribe
description: Transcribe audio/video using Gemini 2.5/3 Pro API with structured output
---

# Gemini Transcription Skill

Use this skill to transcribe audio or video files using Google's Gemini API.

## Installation

```bash
# Using uv (recommended)
uv pip install gemini-caption-skills

# Or using pip
pip install gemini-caption-skills
```

## Prerequisites

### Get Your API Key

1. Visit: https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key

### Configure API Key (choose one)

**Option 1: Save to config (recommended)**
```python
from gemini_caption import set_api_key
set_api_key("your-api-key-here")
```
Config location: `~/.config/gemini-caption/config.json`

**Option 2: Environment variable**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option 3: Project .env file**
```bash
# In your project root, create .env
GEMINI_API_KEY=your-api-key-here
```

### Verify Setup
```python
from gemini_caption import get_api_key
print(get_api_key())  # Should print your key
```

## Usage

### From URL (YouTube, etc.)

```python
import asyncio
from gemini_caption import GeminiTranscriber

transcriber = GeminiTranscriber(verbose=True)
transcript = asyncio.run(transcriber.transcribe_url("https://www.youtube.com/watch?v=VIDEO_ID"))
print(transcript)
```

### From Local File

```python
import asyncio
from gemini_caption import GeminiTranscriber

transcriber = GeminiTranscriber(verbose=True)
transcript = asyncio.run(transcriber.transcribe_file("/path/to/audio.mp3"))
transcriber.write(transcript, "output.md")
```

### Sync API

```python
from gemini_caption import GeminiTranscriber

transcriber = GeminiTranscriber()
transcript = transcriber.transcribe_sync("/path/to/video.mp4")
```

## Output Format

The transcriber produces markdown output with:
- **Table of Contents** with timestamps
- **Chapter sections** with `## [HH:MM:SS] Title` headers
- **Speaker labels** in `**Speaker Name:**` format
- **Timestamps** at the end of each paragraph `[HH:MM:SS]`
- **Non-speech events** like `[Music] [00:00:08]`

## Configuration

```python
from gemini_caption.transcription import TranscriptionConfig, GeminiTranscriber

config = TranscriptionConfig(
    model_name="gemini-2.5-pro-preview-05-06",  # or "gemini-3.0-pro"
    language="zh",  # Optional: force specific language
    verbose=True,
    use_thinking=True,  # Enable Gemini thinking mode
)

transcriber = GeminiTranscriber(config=config)
```

## Prompt Customization

The system prompt is loaded from `src/gemini_caption/prompts/transcription_gem.txt`.
You can modify this file to customize transcription behavior.

## Key Features

- Verbatim transcription (no translation)
- Automatic speaker identification from metadata/audio
- Chapter generation from YouTube descriptions or topic shifts
- Filler words preserved (um, uh, like)
- Mixed-language support
