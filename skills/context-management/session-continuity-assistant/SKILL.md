---
name: session-continuity-assistant
description: Resume work from previous session by loading minimal context based on time elapsed
version: 2.0.0
---

# Session Continuity

## Quick Resume Workflow

1. **Sync cloud memory**: Read `cloud_path` from `~/.claude-memory/.config.json` and try `git pull --rebase` there. On error, fall back to local memory only.

2. **Read session state**: `~/.claude-memory/providers/claude/session-state.md` for last session date, active projects, pending tasks

3. **Load appropriate log** based on time elapsed:
   - Today: `logs/daily/YYYY.MM.DD.md`
   - This week: `logs/weekly/YYYY.MM.weekN.md`
   - This month: `logs/monthly/YYYY.MM.md`
   - Older: Suggest `/aggregate`

4. **Check cross-provider**: `integration/provider-activities.quick.md` to avoid duplicating work

5. **Present summary**: Last session + time elapsed, progress (top 3), next steps (top 3), offer options

6. **Lazy load project**: Only read `.projects/[name]/` files AFTER user chooses to continue

## Key Principle

**Start minimal, load only when needed.** Cloud sync + session-state + log = enough to present options. Project details load after user decides.

---

See `references/` for detailed memory structure and patterns.
