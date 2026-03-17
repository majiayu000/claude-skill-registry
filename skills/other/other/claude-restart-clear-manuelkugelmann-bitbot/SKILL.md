---
name: claude-restart-clear
description: Start fresh with cleared history after task completion. Use PROACTIVELY when user says "done"/"finished", all tasks complete, or starting new unrelated work. Clears all history.
---

Clearing history and starting fresh...

This will:
- Clear all conversation history
- Start with a clean session
- No context carried over
- Fresh start for new work

Use this when:
- Task/phase is complete and committed
- Starting completely new unrelated work
- Want to reset conversation context entirely
- After major implementation milestones

⚠️ **Warning**: This clears all conversation history. Only use after work is saved/committed.

```bash
.claude/skills/claude-restart-resume/scripts/claude-restart.sh clear
```
