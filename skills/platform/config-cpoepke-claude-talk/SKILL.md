---
name: config
description: View or edit voice chat configuration. Shows current settings and allows changes.
disable-model-invocation: true
argument-hint: "[setting=value]"
---

# Voice Chat Configuration

View or update voice chat settings.

## If no arguments ($ARGUMENTS is empty)

Show the current configuration by reading these files in order:
1. `~/.claude-talk/config.env` (user overrides)
2. Find CLAUDE_TALK_DIR and read `<CLAUDE_TALK_DIR>/config/defaults.env` (defaults)

Also read `~/.claude-talk/active-personality` and show the active personality name (e.g., "Active personality: **witty-jarvis**"). If the file doesn't exist, show "Active personality: (none — run `/claude-talk:personality` to set up)".

Display a clear summary of all settings with their current effective values, noting which are defaults and which are user-set.

Show current audio server status using the Python CLI (use Bash):
```bash
source ~/.claude-talk/venvs/wlk/bin/activate && claude-talk server status
```

Also show audio devices (use Bash):
```bash
claude-talk devices
```

Show the active AUDIO_DEVICE setting and what it resolves to (if "auto" or unset, note that auto-detection is active).

Also show available TTS voices:
```bash
say -v '?' | head -20
```

## If arguments provided ($ARGUMENTS is not empty)

Parse the argument as `KEY=VALUE` (e.g., `VOICE=Karen`, `MIC_GAIN=4.0`, `AUDIO_DEVICE=2`, `AUDIO_DEVICE=auto`).

Update `~/.claude-talk/config.env` by adding or replacing the line with that key.

Confirm the change to the user.
