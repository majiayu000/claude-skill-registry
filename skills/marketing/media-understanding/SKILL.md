---
name: media-understanding
description: 'Understand audio and video content. Use when user asks to transcribe,
  analyze, summarize, or extract information from audio/video files or YouTube URLs.
  Routes automatically: audio files use local fas'
---

---
name: media-understanding
description: Understand audio and video content. Use when user asks to transcribe, analyze, summarize, or extract information from audio/video files or YouTube URLs. Routes automatically: audio files use local faster-whisper (free, fast), video files use Gemini API (visual+audio understanding).
---

# Media Understanding

## Audio Files → faster-whisper (local)

For mp3, wav, m4a, flac, ogg, aac files:

```bash
faster-whisper "path/to/audio.mp3" -o /tmp --model large-v3
```

### Options

| Option | Description |
|--------|-------------|
| `-o DIR` | Output directory for .srt file |
| `--model SIZE` | tiny, base, small, medium, large-v3 (default: large-v3) |
| `--language LANG` | Force language (auto-detected by default) |
| `--task transcribe` | Transcribe in original language (default) |
| `--task translate` | Translate to English |
| `--word_timestamps true` | Include word-level timing |

Output: SRT subtitle file in output directory.

## Video Files → Gemini (visual + audio)

For mp4, mov, webm, avi, mkv files or YouTube URLs:

```bash
uv run ~/.claude/skills/media-understanding/scripts/understand_video.py \
  --source "path/to/video.mp4" \
  --prompt "Describe what happens in this video"
```

### Options

| Option | Description |
|--------|-------------|
| `--fast` | Use faster flash model |
| `--fps N` | Frame rate sampling (default: 1 fps) |
| `--start N` | Start time in seconds |
| `--end N` | End time in seconds |

### Example Prompts

- "Summarize this video in 3 bullet points"
- "Transcribe all spoken dialogue with timestamps"
- "What text appears on screen?"
- "Describe the main actions and events"

## API Key

Gemini requires `GEMINI_API_KEY` env var.
