---
name: unmute
description: Unmute the microphone during a voice chat session. Resumes capture on the next loop cycle.
disable-model-invocation: true
---

# Unmute Microphone

Resume microphone capture during a voice chat session.

## Steps

1. Check that a voice session is active (use Bash):
   ```bash
   source ~/.claude-talk/venvs/wlk/bin/activate
   claude-talk state get SESSION
   ```
   If it returns non-zero or the value is not "active", tell the user: "No voice chat session is active. Start one with `/claude-talk:start`."

2. Clear muted state (use Bash):
   ```bash
   source ~/.claude-talk/venvs/wlk/bin/activate
   claude-talk state set MUTED false
   claude-talk state set STATUS listening
   ```

3. Confirm: "Microphone unmuted. Listening for speech."
