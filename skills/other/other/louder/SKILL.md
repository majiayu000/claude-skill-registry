---
name: louder
description: Increase system volume by 10% during voice chat
disable-model-invocation: true
---

# Increase Volume

Increase the system output volume by 10%.

## Steps

1. Check if the audio server is running (Bash):
   ```bash
   claude-talk server status 2>/dev/null && echo "running" || echo "stopped"
   ```
   If stopped, tell the user: "Audio server is not running. Start voice chat with `/claude-talk:start` first."

2. Increase volume and get new level (Bash):
   ```bash
   claude-talk server volume-up
   ```

3. Say: "Volume increased to [X]%"
