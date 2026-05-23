---
name: preserving-context
description: Captures working state before it is lost. Use before context compaction, when switching between unrelated tasks, after completing a logical phase of multi-step work, or when work will resume in a new session. Triggers on long tasks, multi-file changes, context warnings, or "continue later" scenarios.
---

# Preserving Context

## Overview

**Capture state proactively, not reactively.** Before compaction or task switches, write down everything needed to resume seamlessly. If you wait until after compaction, the context is already gone.

## What to Capture

| Category | Capture |
|----------|---------|
| **Current work** | Exact task, file path, progress (X of Y) |
| **Completed items** | Which files changed and what was done |
| **Remaining items** | What still needs doing, in order |
| **Pattern** | The transformation being applied (so it continues consistently) |
| **Decisions** | Key choices made and why (not just what) |
| **Blockers** | Issues discovered, dependencies, failing tests |
| **Test state** | Are tests passing? Which are failing and why? |

## Checkpoint Template

Write this as a task description (via `TaskUpdate`) so it persists across compaction, and also communicate it to the user so they have it too:

```
## Checkpoint — [Task Name]

**Working on:** [specific task]
**Current file:** [path]
**Progress:** [X of Y complete]

### Completed
- [file1] — [what was done]
- [file2] — [what was done]

### Remaining
- [file3] — [what needs doing]
- [file4] — [what needs doing]

### Pattern Being Applied
[Describe the transformation so it can be continued consistently]

### Key Decisions
- [Decision]: [why this over alternatives]

### Blockers / Notes
- [Any issues or dependencies]
```

## Good vs Bad Checkpoints

**Bad:** "Working on refactor. Some files done."

**Good:** "Renaming `getUserById` to `fetchUserById` across the codebase. Completed: `src/services/user.ts`, `src/api/routes.ts`, `src/tests/user.test.ts`. Remaining: `src/middleware/auth.ts`, `src/utils/cache.ts`. Pattern: find-and-replace function name + update all call sites + update test assertions. Tests currently failing on 2 import mismatches."

## Red Flags — STOP and Checkpoint

| Thought | Action |
|---------|--------|
| "I'll remember where I was" | Write it down NOW |
| "It's obvious what's next" | Obvious now ≠ obvious after compaction |
| "Just one more thing then I'll document" | Checkpoint first, then continue |
| "This is too small to checkpoint" | Small context loss compounds |

## Integration with tracking-tasks

These two skills complement each other:
- **tracking-tasks**: Tracks WHAT tasks exist and their status
- **preserving-context**: Captures HOW to resume each task

Both should be used together before compaction.
