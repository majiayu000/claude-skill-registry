---
name: inworld
description: "Inworld TTS API. Covers voice cloning, audio markups, timestamps. Keywords: text-to-speech, visemes."
version: "1.5"
release_date: "2026-01-21"
---

# Inworld AI

Text-to-Speech platform with voice cloning, audio markups, and timestamp alignment.

## Quick Navigation

| Topic         | Reference                                       |
| ------------- | ----------------------------------------------- |
| Installation  | [installation.md](references/installation.md)   |
| Voice Cloning | [cloning.md](references/cloning.md)             |
| Voice Control | [voice-control.md](references/voice-control.md) |
| API Reference | [api.md](references/api.md)                     |

## When to Use

- Text-to-speech audio generation
- Voice cloning from 5-15 seconds of audio
- Emotion-controlled speech (`[happy]`, `[sad]`, etc.)
- Word/phoneme timestamps for lip sync
- Custom pronunciation with IPA

## Models

| Model        | ID                     | Latency | Price        |
| ------------ | ---------------------- | ------- | ------------ |
| TTS 1.5 Max  | `inworld-tts-1.5-max`  | ~200ms  | $10/1M chars |
| TTS 1.5 Mini | `inworld-tts-1.5-mini` | ~120ms  | $5/1M chars  |

## Minimal Example

```python
import requests, base64, os

response = requests.post(
    "https://api.inworld.ai/tts/v1/voice",
    headers={"Authorization": f"Basic {os.getenv('INWORLD_API_KEY')}"},
    json={"text": "Hello!", "voiceId": "Ashley", "modelId": "inworld-tts-1.5-max"}
)
audio = base64.b64decode(response.json()['audioContent'])
```

## Key Features

- **15 languages** — en, zh, ja, ko, ru, it, es, pt, fr, de, pl, nl, hi, he, ar
- **Instant cloning** — 5-15 seconds audio, no training
- **Audio markups** — `[happy]`, `[laughing]`, `[sigh]` (English only)
- **Timestamps** — word, phoneme, viseme timing for lip sync
- **Streaming** — `/voice:stream` endpoint

## Prohibitions

- Audio markups work **only in English**
- Use **ONE** emotion markup at text **beginning**
- Match voice language to text language
- Instant cloning may not work for children's voices or unique accents

## Links

- Docs: https://docs.inworld.ai/docs/tts/tts
- Platform: https://platform.inworld.ai/
