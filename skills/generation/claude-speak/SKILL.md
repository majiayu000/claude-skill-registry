---
name: claude-speak
description: Speak text aloud using high-quality AI voice synthesis (Kokoro TTS on Apple Silicon). Use when user asks to vocalize, narrate, or speak text out loud.
---

# Claude Speak

Vocalize text using high-quality text-to-speech. British male voice (bm_george) by default.

## When to Use

Invoke when user:
- Asks to "say this out loud" or "speak this"
- Wants narration or audio feedback
- Uses `/speak` command
- Requests vocalization of content

## Core Command

```bash
~/Projects/claude-speak/.venv/bin/claude-speak-client "Text to speak"
```

**That's it.** The daemon runs in background via launchd - instant response.

**IMPORTANT:** When using the Bash tool, set `timeout: 300000` (5 min) to avoid Claude Code's default 2-minute timeout on longer text.

## Options

```bash
# Different voice
~/Projects/claude-speak/.venv/bin/claude-speak-client -v af_heart "Warm female voice"

# Adjust speed (default 1.0)
~/Projects/claude-speak/.venv/bin/claude-speak-client -s 1.2 "Speaking faster"

# Quiet mode (suppress errors)
~/Projects/claude-speak/.venv/bin/claude-speak-client -q "Silent on success"

# Custom timeout (default: 300s / 5 min)
~/Projects/claude-speak/.venv/bin/claude-speak-client -t 600 "Very long text..."
```

## Long Text (3+ sentences)

For longer content, either:

1. **Set longer timeout:** Use `timeout: 300000` in Bash tool call
2. **Run in background:** Use `run_in_background: true` to avoid blocking

```bash
# Background mode - Claude continues while audio plays
~/Projects/claude-speak/.venv/bin/claude-speak-client "Your longer text here..."
```

Background mode is cleaner for paragraphs and avoids timeout issues entirely.

## Available Voices

| Voice | Description |
|-------|-------------|
| `bm_george` | British male, distinguished (DEFAULT) |
| `af_heart` | American female, warm |
| `am_adam` | American male, deep |
| `bf_emma` | British female, elegant |

## Troubleshooting

If "Daemon not running" error:
```bash
~/Projects/claude-speak/.venv/bin/claude-speak-daemon start
```

## Best Practices

- Keep utterances concise (1-2 sentences)
- Use for key points, not entire responses
- Check daemon status if issues arise
