---
name: mission-solo
description: "HOUSTON executes feature tasks directly. No agents. Best for small features (1-3 tasks)."
---

# /mission-solo - Direct Execution

HOUSTON executes tasks directly without spawning agents. Fast for small features, but context fills quickly.

## Warning

```
HOUSTON: Solo mode fills context fast. Only use for:
         - Small features (1-3 tasks)
         - Quick demos
         - Debugging a single task

         For larger work, use /mission-orchestrated.
```

## The Process

1. **Load feature** - Run `bd show FEATURE_ID` to get feature details and tasks
2. **Activate feature** - Run `bd update FEATURE_ID --status in_progress`
3. **Get next task** - Run `bd list --parent FEATURE_ID --status open` (pick highest priority)
4. **Scout** - Spawn Explore agent to gather codebase context (facts only, no suggestions)
5. **Execute task** - Implement the work directly using scout context (write code, run tests)
6. **Mark complete** - Run `bd close TASK_ID`
7. **Loop** - Repeat steps 3-6 until no tasks remain
8. **Complete feature** - Run `bd close FEATURE_ID`

## On Completion

```
HOUSTON: Feature complete. {N} tasks executed.
         Run /capcom for status summary.
```

## On Blocker

If you hit a blocker you cannot resolve:

```bash
bd create -t bug --title "Blocker: description" --blocks TASK_ID
```

Then inform user and suggest switching to orchestrated mode.
