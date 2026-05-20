---
name: Audio to SRT Converter
description: This skill should be used when the user asks to "convert audio to srt", "generate subtitles from audio", "create srt from mp3/wav/m4a/flac", "transcribe audio to subtitles", or needs to generate SRT subtitle files from audio files (MP3, WAV, M4A, FLAC, etc.) with customizable character limits and timeline adjustments.
version: 0.1.0
---

# Audio to SRT Converter

This skill provides a Python-based workflow for converting audio files (MP3, WAV, M4A, FLAC, etc.) into SRT subtitle files with automatic speech recognition, customizable text formatting, and timeline optimization.

## Purpose

Convert audio files (MP3, WAV, M4A, FLAC, etc.) into properly formatted SRT subtitle files with:
- Automatic speech recognition and transcription
- Support for multiple audio formats (MP3, WAV, M4A, FLAC, and more)
- Customizable character limits per subtitle line (default: 22 characters, minimum: 4 characters)
- Automatic timeline gap filling (gaps < 0.3s are merged)
- Environment and dependency validation
- Output naming convention: `origin.srt`

## When to Use This Skill

Use this skill when:
- Converting audio files to subtitle format
- Generating transcriptions with timeline information
- Creating SRT files for video editing or accessibility
- Processing Chinese or multilingual audio content

## Core Workflow

### 1. Environment Validation

Before processing, validate:
- Python 3.7+ is installed
- Required packages are available (see Dependencies section)
- Input MP3 file exists and is readable
- Output directory is writable

### 2. Audio Transcription

Process the audio file using speech recognition:
- Load audio file (supports MP3, WAV, M4A, FLAC, etc.)
- Perform speech-to-text conversion
- Extract timestamps for each segment
- Handle silence detection and word boundaries

### 3. Text Formatting

Format transcribed text according to parameters:
- Split text into lines based on character limit
- Ensure minimum 4 characters per line
- Respect word boundaries when possible
- Handle Chinese character counting correctly

### 4. Timeline Optimization

Adjust subtitle timing:
- Identify gaps between subtitle segments
- Merge segments when gap < 0.3 seconds
- Extend previous subtitle end time to next subtitle start time
- Maintain synchronization with audio

### 5. SRT Generation

Create final SRT file:
- Format according to SRT specification
- Number subtitles sequentially
- Use proper timestamp format (HH:MM:SS,mmm)
- Save as `origin.srt`

## Using the Conversion Script

The main conversion script is located at `scripts/audio_to_srt.py`.

### Basic Usage

```bash
python scripts/audio_to_srt.py <audio_file> [--max-chars MAX_CHARS]
```

### Parameters

- `audio_file` (required): Path to the input audio file (MP3, WAV, M4A, FLAC, etc.)
- `--max-chars` (optional): Maximum characters per subtitle line (default: 22, minimum: 4)

### Examples

See `examples/usage_example.sh` for complete usage examples.

## Dependencies

The script requires the following Python packages:
- `openai-whisper` - For speech recognition
- `pydub` - For audio processing
- `ffmpeg` - System dependency for audio handling

Install with:
```bash
pip install openai-whisper pydub
brew install ffmpeg  # macOS
```

## Output Format

The generated SRT file follows this format:

```
1
00:00:00,000 --> 00:00:03,500
這是第一行字幕

2
00:00:03,500 --> 00:00:07,200
這是第二行字幕
```

## Additional Resources

### Scripts
- **`scripts/audio_to_srt.py`** - Main conversion script with environment validation
- **`scripts/check_environment.py`** - Standalone environment checker

### Examples
- **`examples/usage_example.sh`** - Complete usage examples with different parameters
