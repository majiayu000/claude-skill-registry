---
name: checkpoint
description: Quick save of current session state for recovery after failures
---

# Session Checkpoint

**Purpose:** Quickly save current state so you can recover after a session
failure.

## Instructions

Update the Quick Recovery section at the top of SESSION_CONTEXT.md with:

1. **Current timestamp**
2. **Branch name** (run `git rev-parse --abbrev-ref HEAD`)
3. **Working on** - Brief description of current task
4. **Files modified** - List files changed since last commit
   (`git diff --name-only`)
5. **Next step** - What to do next if session dies
6. **Uncommitted work** - Yes/No

## Quick Recovery Template

Update SESSION_CONTEXT.md "Quick Recovery" section with this format:

```markdown
## 🔄 Quick Recovery

**Last Checkpoint**: YYYY-MM-DD HH:MM **Branch**: `branch-name-here` **Working
On**: [brief task description] **Files Modified**: [list or "none"] **Next
Step**: [what to do next] **Uncommitted Work**: yes/no
```

## Also Update State Files

Write current task state to `.claude/state/` for compaction recovery:

1. If working on a multi-step task, write/update
   `.claude/state/task-{name}.state.json`:

   ```json
   {
     "task": "task-name",
     "started": "ISO datetime",
     "lastUpdated": "ISO datetime",
     "steps": [
       { "name": "Step 1", "status": "completed" },
       { "name": "Step 2", "status": "in_progress" },
       { "name": "Step 3", "status": "pending" }
     ],
     "context": { "branch": "branch-name", "notes": "key info" }
   }
   ```

2. Update `.claude/state/handoff.json` with current progress (the
   `compaction-handoff.js` hook does this automatically, but manual updates add
   richer task-specific context).

## Also Consider

- If uncommitted work exists, consider committing now:

  ```bash
  git add -A && git commit -m "WIP: checkpoint before potential failure"
  ```

- If working on risky operations, push the branch:
  ```bash
  git push -u origin $(git rev-parse --abbrev-ref HEAD)
  ```

## When to Use This Command

- Before large file operations
- Before complex multi-step tasks
- When you notice session becoming slow
- Periodically during long sessions (every 30-60 minutes)
- Before any operation that previously caused failures

---

**Run this checkpoint now and update SESSION_CONTEXT.md.**
