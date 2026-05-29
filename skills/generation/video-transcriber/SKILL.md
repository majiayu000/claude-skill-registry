---
name: video-transcriber
description: Transcribe audio from videos using Whisper (local) or Gemini API (gemini-flash-lite-latest). Use when you need to convert video/audio to text for further processing, subtitle generation, or content analysis. Supports multiple languages, speaker diarization, and timestamp-accurate transcription. Gemini provides additional features like emotion detection and viral segment analysis.
allowed-tools: Bash(ffmpeg:*) Bash(python:*)
compatibility: Requires FFmpeg, optional OpenAI/Google Cloud API keys
metadata:
  version: "1.0"
  models: "whisper, gemini-flash-lite-latest"
---

# Video Transcriber

This skill enables AI agents to transcribe audio from video files using either Whisper (local processing) or Gemini API (cloud processing with advanced features).

## When to Use

- User wants to transcribe a video or audio file
- User needs subtitles/captions for a video
- User wants to analyze video content through transcription
- User needs to identify viral-worthy segments
- User wants speaker diarization or emotion detection

## Model Selection

### Whisper (Local)

**Pros:**
- Free to use
- 100% privacy (no cloud upload)
- Good for sensitive content
- Lower cost for high volume

**Cons:**
- Requires local processing power
- No built-in speaker diarization
- No emotion detection
- Limited to 99 languages

**Models:**
- `tiny` - Fastest, lower accuracy (~32MB)
- `base` - Fast, good accuracy (~74MB)
- `small` - Balanced speed/accuracy (~244MB)
- `medium` - Good accuracy, slower (~769MB)
- `large-v3` - Highest accuracy, slowest (~1550MB)

### Gemini API (Cloud)

**Pros:**
- High accuracy with gemini-flash-lite-latest
- Built-in speaker diarization
- Emotion detection from speech
- Context understanding
- Can identify viral segments
- 125+ language support
- Faster processing (cloud-based)

**Cons:**
- Requires API key
- Cloud upload (privacy consideration)
- Cost per usage
- Internet required

## Available Scripts

### `scripts/transcribe.py`

Transcribe audio from video file.

**Usage:**
```bash
python skills/video-transcriber/scripts/transcribe.py <video_path> [options]
```

**Options:**
- `--model, -m`: Model to use (whisper, gemini) - default: auto
- `--whisper-model`: Whisper model size (tiny, base, small, medium, large-v3) - default: medium
- `--use-faster`: Use faster-whisper for speed - default: True
- `--output, -o`: Output file path (default: `<video_path>.srt`)
- `--format`: Output format (srt, vtt, json) - default: srt
- `--language`: Language code (e.g., en, id) - default: auto
- `--speaker-diarization`: Enable speaker labels (Gemini only)
- `--emotion-detection`: Enable emotion detection (Gemini only)
- `--device`: Device for Whisper (auto, cpu, cuda) - default: auto

**Examples:**

Transcribe with Whisper (default):
```bash
python skills/video-transcriber/scripts/transcribe.py video.mp4
```

Transcribe with Gemini API:
```bash
python skills/video-transcriber/scripts/transcribe.py video.mp4 --model gemini
```

Transcribe with speaker diarization and emotion detection (Gemini):
```bash
python skills/video-transcriber/scripts/transcribe.py video.mp4 --model gemini --speaker-diarization --emotion-detection
```

Transcribe with large Whisper model:
```bash
python skills/video-transcriber/scripts/transcribe.py video.mp4 --whisper-model large-v3
```

Output to JSON:
```bash
python skills/video-transcriber/scripts/transcribe.py video.mp4 --format json
```

### `scripts/analyze.py`

Analyze audio content using Gemini API for viral segments, summary, or emotions.

**Usage:**
```bash
python skills/video-transcriber/scripts/analyze.py <video_path> [options]
```

**Options:**
- `--analysis-type`: Type of analysis (viral, summary, emotions, questions) - default: viral
- `--num-segments`: Number of segments to identify (for viral analysis) - default: 5
- `--model`: Model to use (default: gemini)

**Examples:**

Detect viral segments:
```bash
python skills/video-transcriber/scripts/analyze.py video.mp4 --analysis-type viral
```

Get summary:
```bash
python skills/video-transcriber/scripts/analyze.py video.mp4 --analysis-type summary
```

Analyze emotions:
```bash
python skills/video-transcriber/scripts/analyze.py video.mp4 --analysis-type emotions
```

## Output Format

### SRT Format

```srt
1
00:00:00,000 --> 00:00:05,000
This is the first subtitle.

2
00:00:05,500 --> 00:00:10,000
This is the second subtitle.
```

### JSON Format

```json
[
  {
    "index": 1,
    "start": 0.0,
    "end": 5.0,
    "text": "This is the first subtitle.",
    "speaker": "Speaker A",
    "emotion": "neutral"
  }
]
```

## Auto Selection Logic

When `--model auto`, the system selects based on:

1. **Privacy priority**: Always use Whisper
2. **Quality needed**: Use gemini for highest quality
3. **Content length**: Use faster-whisper for long content (> 1 hour)
4. **Feature requirements**: Use gemini if speaker diarization or emotion detection needed
5. **Default**: Use gemini-flash-lite-latest

## Environment Variables

```bash
# For Gemini API
export GEMINI_API_KEY="your-api-key"

# Optional: For Vertex AI
export GOOGLE_PROJECT_ID="your-project-id"
export GOOGLE_LOCATION="us-central1"
```

## Integration with Other Skills

After transcription, you can use these skills:

- `highlight-scanner`: Analyze transcript for viral moments
- `subtitle-overlay`: Add captions to video
- `autocut-shorts`: Full workflow for creating short clips

## Common Workflow

1. User provides video file or URL
2. Download if needed (youtube-downloader)
3. Transcribe using this skill
4. Analyze transcript for highlights (highlight-scanner)
5. Create short clips (autocut-shorts)

## Tips

- Use `--use-faster` with Whisper for faster processing
- Use Gemini when you need speaker diarization
- Use `--format json` for programmatic processing
- For long videos, consider splitting into segments
- Use `--analysis-type viral` to identify best segments for short-form content

## References

- Whisper documentation: https://github.com/openai/whisper
- Gemini API: https://ai.google.dev/gemini-api/docs/audio
- Language codes: ISO 639-1 codes (en, id, es, etc.)
