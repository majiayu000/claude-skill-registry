---
name: voice-reply
description: Generate voice replies using OpenAI TTS API and send audio responses.
version: 1.0.0
created: 2026-01-22
author: Oscar Baracos
tags:
  - tts
  - voice
  - openai
  - audio
requires:
  env:
    - OPENAI_API_KEY
  bins:
    - curl
---

# Voice Reply Skill

Generate spoken audio responses using OpenAI's Text-to-Speech API.

## When to Use

1. When the user asks to "reply by voice", "voice reply", "speak this", or similar voice-related requests.

2. **Command trigger:** When user sends `/voice_note`, resend the last message as a voice note.
   - **Remove all emojis** from the text before converting to speech
   - **Rephrase if needed** to make it sound natural when spoken (e.g., convert bullet points to flowing sentences)

## How to Use

### 1. Prepare the Response

Write your response **without emojis** — they don't translate well to speech.

### 2. Generate Audio

**Important:** Use `opus` format for Telegram voice notes (shows waveform bubble).

```bash
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini-tts",
    "input": "<your text here>",
    "voice": "echo",
    "speed": 1.2,
    "response_format": "opus"
  }' -s --output /tmp/voice_reply.ogg
```

### 3. Send the Audio

Copy to outbound folder and send via message tool:

```bash
mkdir -p /home/exedev/.clawdbot/media/outbound
cp /tmp/voice_reply.ogg /home/exedev/.clawdbot/media/outbound/voice_reply.ogg
```

Then use the message tool with `asVoice: true` for proper voice message format:
```json
{
  "action": "send",
  "channel": "telegram",
  "to": "<user_id>",
  "media": "/home/exedev/.clawdbot/media/outbound/voice_reply.ogg",
  "asVoice": true
}
```

**Important:**
- Use `.ogg` (opus) format — required for Telegram voice notes
- `asVoice: true` sends as voice bubble with waveform
- `message` caption is optional for voice notes

## Configuration Options

### Voice Options
| Voice | Description |
|-------|-------------|
| `alloy` | Neutral, balanced |
| `echo` | Warm, conversational (default) |
| `fable` | British, expressive |
| `onyx` | Deep, authoritative |
| `nova` | Friendly, upbeat |
| `shimmer` | Soft, calm |

### Speed
- Range: `0.25` to `4.0`
- Default: `1.2` (slightly faster than normal)

### Model
- `gpt-4o-mini-tts` — Fast, cost-effective
- `tts-1` — Standard quality
- `tts-1-hd` — High definition

## Example Workflow

```bash
# 1. Generate audio (opus format for Telegram voice notes)
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini-tts",
    "input": "Hey Oscar! Your main task today is Create Task Skill. Let me know if you need help!",
    "voice": "echo",
    "speed": 1.2,
    "response_format": "opus"
  }' -s --output /tmp/reply.ogg

# 2. Copy to outbound
cp /tmp/reply.ogg ~/.clawdbot/media/outbound/reply.ogg

# 3. Send via message tool with asVoice: true
```

## Tips

- Keep responses concise for voice — long text becomes tiring to listen to
- Avoid special characters, URLs, and code blocks
- Use natural language, as if speaking to someone
- Numbers and dates should be written out naturally

## References

- [OpenAI TTS Documentation](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI Audio API Reference](https://platform.openai.com/docs/api-reference/audio)
