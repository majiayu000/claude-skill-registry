---
name: end
description: Finalize session by creating detailed log and syncing to cloud
version: 1.0.0
---

# End Session

## Quick Finalization Workflow

1. **Collect session info**: Prompt user for session summary (topic, projects touched, key activities, decisions, blockers)

2. **Generate daily log entry**: Create structured log in `~/.claude-memory/providers/claude/logs/daily/YYYY.MM.DD.md` with:
   - Session timestamp + topic
   - Projects touched
   - Activities realized
   - Performance metrics (context usage, quality, success)
   - Next steps
   - Decisions/insights

3. **Update session state**: Modify `~/.claude-memory/providers/claude/session-state.md` with current focus and pending tasks

4. **Update integration timeline**: Append to `~/.claude-memory/integration/provider-activities.md` and `.quick.md`

5. **Sync to cloud**: Try pushing logs to cloud. On error, logs stay local only. (Cloud path in `~/.claude-memory/.config.json` - don't read, just try sync)

6. **Confirmation**: Show user what was logged and sync status

## Key Principle

**Logs saved locally first, cloud sync is best-effort.** Session finalization never blocks on cloud errors.

---

See existing daily logs for format examples.
