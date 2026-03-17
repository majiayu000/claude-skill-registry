---
name: status
description: Use when the user returns to a session and asks about progress, current state, what happened, or where they left off. Provides status dashboard and execution recovery.
invocation: agent
---

# Status

Inspect and recover workflow state. Use this to check progress, find where a session left off, or resume interrupted execution.

## Resume Checks

Restore state from:

1. Beads status (`bd ready`, `bd list --status in_progress`)
2. Task list state if `CLAUDE_CODE_TASK_LIST_ID` is set
3. Last known plan/spec references in workspace
4. `.arc/state.json` persisted by `execute`

`CLAUDE_CODE_TASK_LIST_ID` source of truth:

1. Current shell env var
2. `.claude/settings.json` -> `env.CLAUDE_CODE_TASK_LIST_ID`

If missing from both locations, resume with Beads-only state and print a warning.

Prefer `.arc/state.json` for last known mode/source/paths, then reconcile with live Beads and task list.

Resume state read example:

```bash
if [[ -f .arc/state.json ]]; then
  cat .arc/state.json
else
  echo "ARC: no .arc/state.json found; resuming from live Beads/task state only"
fi
```

## Output

Report:
- Current execution mode
- Ready/blocked/in-progress counts
- Recommended next command
