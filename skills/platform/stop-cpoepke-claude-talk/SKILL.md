---
name: stop
description: Stop voice chat. Releases the current voice session and stops the audio server if no other sessions are active.
disable-model-invocation: true
---

# Stop Voice Chat

Gracefully shut down the voice chat session.

## Steps

1. Release this session and stop server if no others active (use Bash):
   ```bash
   source ~/.claude-talk/venvs/wlk/bin/activate
   claude-talk session release-current
   ```

2. Confirm to the user: "Voice chat stopped."
