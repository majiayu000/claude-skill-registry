---
name: cancel-ralph
description: Cancel active Ralph loop
category: orchestration
---

# Cancel Ralph

Cancel the active Ralph Wiggum loop.

## Action

1. Read `prd.json.session` if it exists
2. Update status to "terminated"
3. Report current progress to the user

## Report Format

```
Ralph loop cancelled.

Session: {session name}
Iterations completed: {n}/{max}
Tasks completed: {n}/{total}

Progress preserved in:
- prd.json.items (completed tasks still marked)
- prd.json.session (session state)
- progress.txt (session log)

To resume: /ralph
```

That's it. Just cancel and report.
