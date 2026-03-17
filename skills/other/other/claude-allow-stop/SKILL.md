---
name: claude-allow-stop
description: Return to normal stop behavior. Use PROACTIVELY after completing all tasks in continuous work mode, when work is committed and tests pass, or when reaching natural stopping point. User can invoke with /claude-allow-stop.
allowed-tools: Bash, Read
---

# Disable Stop Hook Automation

Allow normal completion and wait for user input.

```bash
.claude/skills/claude-allow-stop/scripts/allow-stop.sh
```

Or user invokes: `/claude-allow-stop`

Re-enable with `/claude-do-not-stop [reason]`
