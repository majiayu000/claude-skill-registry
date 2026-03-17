---
name: mute
description: Mute the microphone during a voice chat session. The capture loop pauses until unmuted.
disable-model-invocation: true
---

# Mute Microphone

Pause microphone capture during a voice chat session.

## Steps

1. Check that a voice session is active (use Bash):
   ```bash
   source ~/.claude-talk/venvs/wlk/bin/activate
   claude-talk state get SESSION
   ```
   If it returns non-zero or the value is not "active", tell the user: "No voice chat session is active. Start one with `/claude-talk:start`."

2. Set muted state (use Bash):
   ```bash
   source ~/.claude-talk/venvs/wlk/bin/activate
   claude-talk state set MUTED true
   claude-talk state set STATUS muted
   ```

3. Confirm: "Microphone muted. Run `/claude-talk:unmute` to resume."
