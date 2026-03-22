---
name: voice-mode
description: >-
  Activates voice conversation mode using Pocket TTS Docker container.
  Use when user says "voice mode", "let's talk", "talk to me",
  "speak your responses", or wants Claude to respond with spoken audio.
  Speaks all responses through TTS and plays via speakers.
allowed-tools:
  - Bash(*/tts.sh:*)
argument-hint: "[voice]"
---

# Voice Mode

Voice conversation mode where all responses are spoken aloud via Pocket TTS.

## Setup

The `tts.sh` script lives in this skill's `scripts/` directory. Resolve it relative to this SKILL.md:

```
SKILL_DIR="<absolute path to this skill's directory>"
TTS="${SKILL_DIR}/scripts/tts.sh"
```

Use `${TTS}` for all commands below.

## Activation

On activation, ALWAYS run these steps in order before anything else:

1. Check the TTS container is running:
   ```bash
   ${TTS} ensure
   ```
   If this fails (exit code 1), tell the user the container is down and stop. Do NOT attempt to start it.

2. Confirm voice mode is active by speaking:
   ```bash
   ${TTS} play "Voice mode activated. I'm listening." -v eponine
   ```

## Response Rules

While voice mode is active:

1. **ALWAYS speak every response** using tts.sh:
   ```bash
   ${TTS} play "<response text>" -v eponine
   ```

2. **Prefer concise responses** — aim for 1-3 sentences when used standalone. When combined with another skill, match the response length that skill requires.

3. **Write naturally for speech** — avoid markdown, bullet points, code blocks, URLs. Write as you'd speak in conversation.

4. **Also output text** — print a brief text version so the conversation is readable in the terminal.

5. **Handle STT input gracefully** — user input arrives as `[STT]...[/STT]` tags from their whisper script. The transcription may be imperfect. Infer intent from context rather than asking for clarification on every garbled word.

6. **Split long responses** — if you need to say more than ~2 sentences, make multiple tts.sh calls so audio starts playing sooner.

## Voice Selection

Default voice: `eponine`

If the user provided an argument (e.g., `/voice-mode jean`), use that voice instead.

Available: alba, marius, javert, jean, fantine, cosette, eponine, azelma

## Deactivation

Voice mode ends when the user says "stop voice mode", "text mode", or "stop talking".
Confirm with a final spoken message: "Voice mode off. Back to text."

## Configuration

All configurable via environment variables:
- `POCKET_TTS_PORT` — server port (default: 18731)
- `POCKET_TTS_VOICE` — default voice (default: eponine)
- `POCKET_TTS_SPEED` — playback speed (default: 1.2)

## Dependencies

- Docker with pocket-tts container running (`docker compose up -d` from the pocket-tts repo)
- mpv (audio playback)
- curl
