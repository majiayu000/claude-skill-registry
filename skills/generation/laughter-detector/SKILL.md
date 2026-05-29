---
name: laughter-detector
description: Detect laughter and humorous segments in audio/video. Use when you want to find funny moments, identify audience reactions, or create viral clips from humorous content. Supports both AI model detection and keyword-based detection from transcripts.
allowed-tools: Bash(ffmpeg:*) Bash(python:*)
compatibility: Requires audio processing libraries and optional ML models
metadata:
  version: "1.0"
  methods: "AI Model + Keyword Detection"
---

# Laughter Detector

This skill enables AI agents to detect laughter and humorous segments in audio or video files.

## When to Use

- User wants to find funny moments in a video
- Detecting audience reactions (laughter, applause)
- Creating viral clips from humorous content
- Analyzing podcast or comedy content

## Detection Methods

### 1. Keyword-Based Detection (Default)

Analyzes transcript for laughter-related keywords and phrases:
- laugh, laughter, haha, lmao, lol
- chuckle, giggle, snicker
- (laughing), (laughter)

### 2. Audio Feature Detection

Analyzes audio characteristics:
- High energy segments
- Repetitive patterns
- Voice characteristics

### 3. AI Model Detection

Uses trained laughter detection models:
- LaughterSegmentation model
- Custom trained models

## Available Scripts

### `scripts/detect_laughter.py`

Detect laughter segments in audio/video.

**Usage:**
```bash
python skills/laughter-detector/scripts/detect_laughter.py <video_path> [options]
```

**Options:**
- `--method`: Detection method (keywords, audio, ai) - default: keywords
- `--transcript-path`: Path to transcript SRT/VTT file (for keyword detection)
- `--threshold`: Detection threshold (0.0-1.0) - default: 0.5
- `--min-duration`: Minimum laughter segment duration (seconds) - default: 0.3
- `--output, -o`: Output JSON path (default: `<video_path>_laughter.json`)

**Examples:**

Detect laughter from transcript:
```bash
python skills/laughter-detector/scripts/detect_laughter.py video.mp4 --transcript-path video.srt
```

Detect with audio analysis:
```bash
python skills/laughter-detector/scripts/detect_laughter.py video.mp4 --method audio --threshold 0.4
```

### `scripts/detect_from_transcript.py`

Detect laughter from transcript file only.

**Usage:**
```bash
python skills/laughter-detector/scripts/detect_from_transcript.py <transcript_path> [options]
```

**Options:**
- `--keywords`: Custom keywords (comma-separated)
- `--output, -o`: Output JSON path

**Example:**
```bash
python skills/laughter-detector/scripts/detect_from_transcript.py video.srt --keywords "laugh,laughter,haha"
```

## Output Format

```json
{
  "video_path": "video.mp4",
  "method": "keywords",
  "total_laughter_segments": 8,
  "laughter_segments": [
    {
      "segment_number": 1,
      "start_time": 12.5,
      "end_time": 15.2,
      "duration": 2.7,
      "confidence": 0.85,
      "text": "[laughter] That's hilarious!",
      "type": "explicit"
    },
    {
      "segment_number": 2,
      "start_time": 45.0,
      "end_time": 47.8,
      "duration": 2.8,
      "confidence": 0.92,
      "text": "(laughing) I can't believe it",
      "type": "explicit"
    }
  ],
  "total_laughter_duration": 15.5,
  "laughter_percentage": 12.5
}
```

## Integration with Other Skills

After laughter detection, you can use these skills:

- `highlight-scanner`: Combine laughter with other signals
- `video-trimmer`: Create clips from laughter segments
- `autocut-shorts`: Full workflow for creating short clips

## Common Workflow

1. User provides video file
2. Transcribe using `video-transcriber`
3. Detect laughter using this skill
4. Create short clips from funny moments

## Tips

- Laughter segments are excellent for viral content
- Combine with scene detection for better cut points
- Longer laughter = higher viral potential
- Consider surrounding context (3-5 seconds before/after)
- Keyword detection is faster, AI model is more accurate

## References

- Laughter detection research: Interspeech 2024 papers
- Audio feature extraction: Librosa documentation
