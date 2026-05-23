---
name: talk-to-user
description: Speak to the user via PC speakers or send voice messages. Use when delivering audio briefings, status updates, alerts, or when the user requests spoken output.
---

# Talk to User — Voice Output Skill

## Voice Profiles

Each agent has a distinct voice configured via Nix (`openclaw.tts` option in home.nix).

| Agent   | Voice                    | Accent   | Style              |
|---------|--------------------------|----------|---------------------|
| Cleber  | `en-GB-RyanNeural`       | British  | Calm, professional  |
| Romário | `pt-BR-AntonioNeural`    | Brazilian| Direct, casual      |

**Config file**: `~/.nix/tts.json` (Nix-managed, read-only)
```json
{"engine":"edge-tts","voice":"en-GB-RyanNeural","voiceAlt":"pt-BR-AntonioNeural"}
```

Read your voice config: `cat ~/clawd/.nix/tts.json | jq -r .voice`
Default TTS engine: `edge-tts` (Microsoft Edge, free, no API key).

## When to Speak

- **Briefings**: Morning summary, night shift results, research findings
- **Alerts**: Something broke, security issue, urgent notification
- **Status updates**: Task complete, build finished, deploy done
- **User requests**: "Tell me about...", "Read this to me", "What happened?"

## When NOT to Speak

- Routine heartbeats or internal housekeeping
- When the user is clearly asleep (unless it's an alert)
- For trivial confirmations — text is fine for "done" or "ok"
- Never speak passwords, tokens, or sensitive data aloud

## Conduct — How to Speak

1. **Be brief.** 30 seconds max for status updates. 2 minutes max for briefings.
2. **Lead with the point.** "Your build passed" not "So I've been looking at the CI pipeline..."
3. **No filler.** Skip "Great news!", "I wanted to let you know", "So basically..."
4. **Natural tone.** Speak like a colleague, not a press release.
5. **One topic per utterance.** Multiple things? Pause between them or list upfront.
6. **Context first for alerts.** "The gateway went down 5 minutes ago — I restarted it, it's back."

## Flow — PC Speakers

```bash
# 1. Generate audio
tts(text="Your message here")  # Returns MEDIA:/tmp/tts-XXX/voice-YYY.mp3

# 2. Unmute & set volume
XDG_RUNTIME_DIR=/run/user/1000 wpctl set-mute @DEFAULT_AUDIO_SINK@ 0
XDG_RUNTIME_DIR=/run/user/1000 wpctl set-volume @DEFAULT_AUDIO_SINK@ 0.8

# 3. Play — MUST use background: true (exec has 10s timeout, audio is longer)
exec(command="XDG_RUNTIME_DIR=/run/user/1000 mpv --no-video --ao=pipewire <file>.mp3", background=true, yieldMs=20000)
```

### If Music is Playing

Lower the media app volume, play TTS at full system volume, then restore:

```bash
# Find stream ID: look for app name in wpctl status under Streams
XDG_RUNTIME_DIR=/run/user/1000 wpctl set-volume <STREAM_ID> 0.4   # Lower music
# Play TTS...
XDG_RUNTIME_DIR=/run/user/1000 wpctl set-volume <STREAM_ID> 1.0   # Restore
```

## Flow — WhatsApp Voice Message

```bash
# 1. Generate audio
tts(text="Your message here")  # Returns MEDIA path

# 2. Send as voice note
message(action=send, channel=whatsapp, target="554899768269", message="🎤", filePath=<mp3_path>, asVoice=true)
```

## Flow — Telegram Voice Message

```bash
# 1. Generate audio
tts(text="Your message here")

# 2. Send as voice
message(action=send, channel=telegram, target="8128478854", message="🎤", filePath=<mp3_path>, asVoice=true)
```

## Critical Rules

- **ALWAYS `background: true`** for mpv playback. Without it, exec's 10s timeout sends SIGKILL mid-playback.
- **Set `yieldMs: 20000`** (or longer for lengthy audio) so the process has time to finish.
- **Never play audio in a blocking exec call.** The SIGKILL will corrupt the audio session.
- **Check volume before playing.** Unmute + set level every time (user may have muted).
- Edge-tts is free and unlimited — don't worry about rate limits.
- For custom voices, see: `edge-tts --list-voices | grep en-`

## Generating with Custom Voice

```bash
# Direct edge-tts (if tts tool doesn't support voice selection):
edge-tts --voice "en-GB-RyanNeural" --text "Hello Lucas" --write-media /tmp/custom-voice.mp3
# Then play with mpv as above
```

## Troubleshooting

- **No sound?** Check `wpctl status` — is the default sink correct? Is volume > 0?
- **SIGKILL at ~10s?** You forgot `background: true` on the mpv exec call.
- **Garbled audio?** PipeWire issue — `systemctl --user restart pipewire` (may need user to do this).
- **Wrong voice?** Verify with `edge-tts --list-voices | grep Neural` for available voices.
