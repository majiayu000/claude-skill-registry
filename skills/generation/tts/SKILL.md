---
name: tts
description: Speak text aloud using the local ElevenLabs TTS script; use when the user asks to read or speak text.
---

# TTS

## Overview

Use this skill to synthesize speech from text.

## Inputs

- Text to speak

## Workflow

1. Extract the text to speak.
2. Run the local TTS script:
   `uv run C:\Users\USERNAME\.claude\hooks\utils\tts\elevenlabs_tts.py --voice OCIdyYxzVR7iuL9fyP9f --model eleven_v3 "<TEXT>"`
3. Create the skip marker file:
   `echo skip > C:\Users\USERNAME\.claude\hooks\utils\tts\.skip_endhook`
4. Confirm success.

## Output

- Short confirmation that speech ran.
