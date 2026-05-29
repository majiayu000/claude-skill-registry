---
name: volume
description: Set system volume to a specific level (0-100) during voice chat
args: level
disable-model-invocation: true
---

# Set Volume

Set the system output volume to a specific level.

## Steps

1. Check if the audio server is running (Bash):
   ```bash
   claude-talk server status 2>/dev/null && echo "running" || echo "stopped"
   ```
   If stopped, tell the user: "Audio server is not running. Start voice chat with `/claude-talk:start` first."

2. Set volume to the requested level (Bash). The argument is the level (0-100):
   ```bash
   claude-talk server set-volume <level>
   ```

3. Say: "Volume set to [X]%"
