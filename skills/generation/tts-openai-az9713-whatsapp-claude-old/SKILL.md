---
name: tts-openai
description: Generate high-quality voiceover using OpenAI TTS API
allowed-tools:
  - Bash
  - Read
  - Write
---

# TTS (Text-to-Speech) Skill

Generate professional voiceover audio using OpenAI's TTS API.

## Prerequisites

- OpenAI API key set as environment variable: `OPENAI_API_KEY`
- `curl` installed (standard on most systems)

## Available Voices

| Voice | Description | Best For |
|-------|-------------|----------|
| alloy | Neutral, balanced | General purpose |
| echo | Warm, conversational | Storytelling |
| fable | British accent, narrative | Documentaries |
| onyx | Deep, authoritative | News, serious topics |
| nova | Friendly, upbeat | Tutorials, explainers |
| shimmer | Soft, gentle | Meditation, ASMR |

## Available Models

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| tts-1 | Standard | Fast | Lower |
| tts-1-hd | High-definition | Slower | Higher |

## Generate Voiceover

### Using curl (Recommended)

```bash
# Generate voiceover
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1-hd",
    "input": "Your script text goes here. This will be converted to speech.",
    "voice": "nova"
  }' \
  --output output/voiceover.mp3
```

### For Long Scripts

Split into chunks if text is very long (max ~4000 characters per request):

```bash
# Generate part 1
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1-hd",
    "input": "First part of the script...",
    "voice": "nova"
  }' \
  --output output/vo_part1.mp3

# Generate part 2
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1-hd",
    "input": "Second part of the script...",
    "voice": "nova"
  }' \
  --output output/vo_part2.mp3

# Combine parts
ffmpeg -i "concat:output/vo_part1.mp3|output/vo_part2.mp3" \
  -acodec copy output/voiceover_combined.mp3
```

## Audio Post-Processing

### Normalize Audio Levels

```bash
ffmpeg -i output/voiceover.mp3 \
  -filter:a loudnorm=I=-16:TP=-1.5:LRA=11 \
  output/voiceover_normalized.mp3
```

### Add Background Music

```bash
# Mix voiceover with background music (music at 15% volume)
ffmpeg -i output/voiceover.mp3 -i assets/music/background.mp3 \
  -filter_complex "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first" \
  output/voiceover_with_music.mp3
```

### Get Audio Duration

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  output/voiceover.mp3
```

## Voice Selection Guide

| Content Type | Recommended Voice |
|--------------|-------------------|
| Tech news | onyx (authoritative) |
| Tutorials | nova (friendly) |
| Storytelling | fable or echo |
| General | alloy |
| Calm/ASMR | shimmer |

## Best Practices

1. **Clean the script**: Remove stage directions, keep only spoken text
2. **Add punctuation**: Periods and commas create natural pauses
3. **Use SSML-like formatting**: "..." creates pauses in speech
4. **Test voices**: Generate samples before full production
5. **Normalize audio**: Ensure consistent levels
6. **Save originals**: Keep unprocessed audio for re-editing

## Cost Estimation

| Model | Cost per 1M chars | ~Cost per minute |
|-------|-------------------|------------------|
| tts-1 | $15.00 | ~$0.10 |
| tts-1-hd | $30.00 | ~$0.20 |

(Based on ~150 words/min, ~6 chars/word = ~900 chars/min)

## Output Files

Save audio files to:
- Raw TTS: `output/voiceover_{project}.mp3`
- Normalized: `output/voiceover_{project}_normalized.mp3`
- With music: `output/voiceover_{project}_final.mp3`
