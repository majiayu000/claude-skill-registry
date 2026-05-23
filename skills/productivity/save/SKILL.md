---
name: save
description: Save current progress and push to remote - like /done but keeps task IN PROGRESS. Use when switching machines, ending session, or backing up work. Triggers on "/save", "save progress", "switch machine", "end session".
---

# Save Progress Skill

Save work-in-progress and push to remote repository. Unlike `/done`, this keeps the task status as IN PROGRESS - perfect for:
- Switching machines (Linux → Windows)
- End of session but task not complete
- Before restarting PC
- Backing up current work

## Workflow

### Step 1: Show Current State

Run these commands to show what changed:

```bash
git status
git diff --stat
```

Display a summary of modified files to the user.

### Step 2: Get Task Information

Use AskUserQuestion to gather:

1. **Task ID** (header: "Task")
   - Options: "Tracked task (enter ID)", "No task (just commit)"
   - Description: Which task are you working on?

2. **Update MASTER_PLAN?** (header: "Docs")
   - Options: "No (just commit)", "Yes (add progress note)"
   - Description: Add progress note to MASTER_PLAN.md?

**Then ask in plain text:** "What's a brief summary of the progress? (1-2 sentences)"

**IMPORTANT**: Wait for user to provide the summary before proceeding.

### Step 3: Update MASTER_PLAN.md (If Requested)

If the user wants to add progress notes:
- Find the task section in `docs/MASTER_PLAN.md`
- Add a progress note with timestamp under the task
- **Keep status as 🔄 IN PROGRESS** (do NOT change to DONE)

Format for progress note:
```markdown
**Progress (YYYY-MM-DD):** [summary of what was done]
```

### Step 4: Stage Files

Stage all changed files EXCEPT:
- `.env*` files
- `backups/` directory
- `node_modules/`
- `*.lock` files (unless intentional)
- `.claude/locks/` directory

Use specific file paths rather than `git add -A`.

### Step 5: Commit

Create a WIP commit with format:
```
wip(TASK-XXX): progress summary
```

If no task ID:
```
wip: progress summary
```

Example:
```
wip(TASK-456): added validation to form fields
```

### Step 6: Sync Beads

Run:
```bash
bd sync
```

### Step 7: Push to Remote

Run:
```bash
git push
```

### Step 8: Output Summary

Display completion message:

```
## Progress Saved

**Task:** TASK-XXX (or "No task")
**Summary:** [what was done]
**Commit:** [short hash]
**Status:** Still IN PROGRESS

Ready to continue on another machine.

To resume:
1. git pull
2. Continue working on TASK-XXX
```

## Difference from /done

| Aspect | `/done` | `/save` |
|--------|---------|---------|
| Task Status | ✅ DONE | 🔄 IN PROGRESS (unchanged) |
| Commit prefix | `[TASK-XXX]` | `wip(TASK-XXX):` |
| Tests required | Yes | No (skip for speed) |
| MASTER_PLAN update | Mark complete | Add progress note only |
| Use case | Task complete | Session end, machine switch |

## Important Notes

1. **Do NOT mark task as DONE** - The whole point is to save progress without claiming completion
2. **Do NOT run tests** - Speed is priority for session-end saves
3. **Do NOT require artifacts** - This is WIP, not a completion claim
4. **Always push** - The goal is to make work available on another machine
5. **Ask before MASTER_PLAN changes** - Some users may just want to commit/push without doc updates
