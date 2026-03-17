---
name: claude-get-session-info
description: Shared utility script for getting Claude PID and Session ID. Source this in other scripts to access CLAUDE_PID and SESSION_ID variables.
---

# Get Session Info

Shared utility for session management - not directly invoked.

**Usage (source in scripts):**

```bash
source .claude/skills/claude-get-session-info/scripts/get-session-info.sh
echo "Claude PID: $CLAUDE_PID"
echo "Session ID: $SESSION_ID"
```

Exports `CLAUDE_PID` and `SESSION_ID` environment variables.
