---
name: Meeting Transcription
description: Transcribe audio recordings from meetings (MP3, WAV, M4A) into text using AWS Transcribe service
---

# Meeting Transcription Skill

This skill enables transcription of meeting audio files to text using AWS Transcribe.

## When to Use This Skill

Use this skill when the user:
- Provides an audio recording of a meeting
- Asks to transcribe a meeting
- Wants to analyze meeting content from an audio file
- Mentions audio files with extensions like .mp3, .wav, .m4a, .mp4, .flac

## How It Works

1. User provides path to an audio file
2. This skill calls the `transcribe_audio.py` script with optional language parameter
3. The script uploads audio to S3 and uses AWS Transcribe
4. Returns the full transcript as plain text with speaker labels (if applicable)
5. You (the agent) can then analyze the transcript

## Usage

**IMPORTANT: Always specify the language to get speaker labels (spk_0, spk_1).**

```bash
# English meeting (default)
python transcribe_audio.py /path/to/audio.mp3

# Chinese meeting
python transcribe_audio.py /path/to/audio.mp3 --language zh-CN

# Other languages
python transcribe_audio.py /path/to/audio.mp3 --language es-ES
```

**Supported Languages:**
- `en-US`: English (US) - **default**
- `zh-CN`: Mandarin Chinese (Simplified)
- `zh-TW`: Traditional Chinese (Taiwan)
- `es-ES`: Spanish (Spain)
- `fr-FR`: French
- `de-DE`: German
- `ja-JP`: Japanese
- `ko-KR`: Korean

**Speaker Labels:**
All transcriptions include speaker labels (spk_0, spk_1, spk_2, etc.) to identify different speakers in the conversation. You must know the language beforehand.

## Supported Audio Formats

- MP3
- MP4
- WAV
- FLAC
- M4A
- OGG
- WebM

## Usage Example

When the user says: "Analyze my 1:1 meeting recording at ./recordings/meeting.mp3"

1. Use this skill to transcribe the audio first
2. Once you have the transcript, analyze it for insights
3. Provide actionable feedback to the user

## What to Do After Transcription

After getting the transcript, analyze it for:
- **Key discussion topics**: What were the main themes?
- **Action items**: What tasks were assigned or agreed upon?
- **Speaking balance**: Who spoke more? Is it balanced?
- **Questions**: What questions were asked? Were they answered?
- **Communication patterns**: Any interruptions, pauses, or unclear moments?
- **Tone and engagement**: Is the conversation collaborative or one-sided?
- **Constructive feedback**: What could be improved for next time?

## Technical Details

- Requires AWS credentials configured
- Requires S3 bucket for temporary audio storage
- Audio files are automatically cleaned up after transcription
- Transcription job names are timestamped to avoid conflicts

