---
name: text-to-speech
description: 将文本转换为语音音频文件，支持多种声音和语言。
metadata:
  short-description: 文字转语音
source:
  repository: https://github.com/pyttsx3/pyttsx3
  license: MPL-2.0
---

# Text to Speech Tool

## Description
Convert text to speech audio files with support for multiple voices, languages, and speech rates.

## Trigger
- `/tts` command
- User needs text to speech
- User wants to generate audio

## Usage

```bash
# Speak text
python scripts/text_to_speech.py "Hello World"

# Save to file
python scripts/text_to_speech.py "Hello World" --output hello.mp3

# Change voice/rate
python scripts/text_to_speech.py "Hello" --rate 150 --voice 1

# Read from file
python scripts/text_to_speech.py --file document.txt --output audio.mp3
```

## Tags
`tts`, `speech`, `audio`, `voice`, `accessibility`

## Compatibility
- Codex: ✅
- Claude Code: ✅
