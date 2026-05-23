---
name: claude-do-not-stop
description: Enable continuous work mode. Use PROACTIVELY when user says "keep working", "don't stop", "finish everything", "complete all tasks". Automatically continues until work is complete. User can invoke with /claude-do-not-stop [reason].
---

# Enable Stop Hook Automation

**Enabled by default in BitBot.**

```bash
.claude/skills/claude-do-not-stop/scripts/do-not-stop.sh [reason]
```

Or user invokes: `/claude-do-not-stop [reason]`

Default: "Resume work!"
