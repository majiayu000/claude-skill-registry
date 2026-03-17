---
name: jat-complete
description: Complete current JAT task with full verification. Verifies work (tests/lint), commits changes, writes memory entry, closes task, releases file reservations, and emits final signal. Session ends after completion.
metadata:
  author: jat
  version: "1.0"
---

# /skill:jat-complete - Finish Task Properly

Complete current task with full verification protocol. Session ends after completion.

## Usage

```
/skill:jat-complete         # Complete task, show completion block
/skill:jat-complete --kill  # Complete and auto-kill session
```

## What This Does

1. **Verify task** (tests, lint, security)
2. **Commit changes** with proper message
3. **Write memory entry** - Save context for future agents
4. **Mark task complete** (`jt close`)
5. **Release file reservations**
6. **Emit completion signal** to IDE

## Prerequisites

You MUST have emitted a `review` signal before running this:

```bash
jat-signal review '{
  "taskId": "TASK_ID",
  "taskTitle": "TASK_TITLE",
  "summary": ["What you accomplished"],
  "filesModified": [
    {"path": "src/file.ts", "changeType": "modified", "linesAdded": 50, "linesRemoved": 10}
  ]
}'
```

## Step-by-Step Instructions

### STEP 1: Get Current Task and Agent Identity

#### 1A: Get Agent Name

Check the tmux session name or identity file:

```bash
TMUX_SESSION=$(tmux display-message -p '#S' 2>/dev/null)
# Agent name is the tmux session without "jat-" prefix
AGENT_NAME="${TMUX_SESSION#jat-}"
```

#### 1B: Get Current Task

Find your in-progress task:

```bash
jt list --json | jq -r '.[] | select(.assignee == "AGENT_NAME" and .status == "in_progress") | .id'
```

If no task found, check for spontaneous work (uncommitted changes without a formal task).

### STEP 1D: Spontaneous Work Detection

**Only if no in_progress task was found.**

Check git status and conversation context for work that was done without a formal task:

```bash
git status --porcelain
git diff --stat
git log --oneline -5
```

If work is detected, propose creating a backfill task record:

```bash
jt create "INFERRED_TITLE" \
  --type INFERRED_TYPE \
  --description "INFERRED_DESCRIPTION" \
  --assignee "$AGENT_NAME" \
  --status in_progress
```

If no work detected, exit the completion flow.

### STEP 2: Verify Task

Run verification checks appropriate to the project:

```bash
# Emit verifying signal
jat-step verifying --task "$TASK_ID" --title "$TASK_TITLE" --agent "$AGENT_NAME"

# Then run checks:
# - Tests (npm test, pytest, etc.)
# - Lint (eslint, ruff, etc.)
# - Type check (tsc --noEmit, etc.)
# - Build (npm run build, etc.)
```

If verification fails, stop and fix issues before continuing.

### STEP 2.5: Update Documentation (If Appropriate)

Only update docs when changes affect how others use the codebase:
- New tool/command added
- New API endpoint
- Breaking change
- New configuration option

Most tasks do NOT need doc updates.

### STEP 3: Commit Changes

```bash
# Get task type for commit prefix
TASK_TYPE=$(jt show "$TASK_ID" --json | jq -r '.[0].issue_type // "task"')

# Commit with proper message format
jat-step committing --task "$TASK_ID" --title "$TASK_TITLE" --agent "$AGENT_NAME" --type "$TASK_TYPE"
```

If `jat-step` is not available, commit manually:

```bash
git add -A
git commit -m "TASK_TYPE($TASK_ID): TASK_TITLE

Co-Authored-By: Pi Agent <noreply@pi.dev>"
```

### STEP 3.5: Write Memory Entry

Save context from this session for future agents. Use the Write tool to create:

```
.jat/memory/{YYYY-MM-DD}-{taskId}-{slug}.md
```

Include YAML frontmatter (task, agent, project, completed, files, tags, labels, priority, type) and sections: Summary, Approach, Decisions (if notable), Key Files, Lessons (if any).

Then trigger incremental index:

```bash
jat-memory index --project "$(pwd)"
```

If indexing fails, log the error but continue. Memory is non-blocking.

### STEP 4: Mark Task Complete

```bash
jat-step closing --task "$TASK_ID" --title "$TASK_TITLE" --agent "$AGENT_NAME"
```

Or manually:

```bash
jt close "$TASK_ID" --reason "Completed by $AGENT_NAME"
```

### STEP 4.5: Auto-Close Eligible Epics

```bash
jt epic close-eligible
```

### STEP 5: Release File Reservations

```bash
jat-step releasing --task "$TASK_ID" --title "$TASK_TITLE" --agent "$AGENT_NAME"
```

Or manually:

```bash
am-reservations --agent "$AGENT_NAME" --json | jq -r '.[].pattern' | while read pattern; do
  am-release "$pattern" --agent "$AGENT_NAME"
done
```

### STEP 6: Emit Completion Signal

```bash
jat-step complete --task "$TASK_ID" --title "$TASK_TITLE" --agent "$AGENT_NAME"
```

This generates a structured completion bundle and emits the final `complete` signal.

Then output the completion banner:

```
TASK COMPLETED: $TASK_ID
Agent: $AGENT_NAME

Summary:
  - [accomplishment 1]
  - [accomplishment 2]

Quality: tests passing, build clean

Session complete. Spawn a new agent for the next task.
```

## "Ready for Review" vs "Complete"

| State | Meaning | Task Status |
|-------|---------|--------------|
| Ready for Review | Code done, awaiting user decision | in_progress |
| Complete | Closed, reservations released | closed |

**Never say "Task Complete" until jt close has run.**

## Error Handling

**No task in progress:**
```
No task in progress. Run /skill:jat-start to pick a task.
```

**Verification failed:**
```
Verification failed:
  - 2 tests failing
  - 5 lint errors
Fix issues and try again.
```

## Step Summary

| Step | Name | Tool |
|------|------|------|
| 1 | Get Task and Agent Identity | jt list, tmux |
| 1D | Spontaneous Work Detection | git status |
| 2 | Verify Task | jat-step verifying |
| 2.5 | Update Documentation | (if appropriate) |
| 3 | Commit Changes | jat-step committing |
| 3.5 | Write Memory Entry | Write tool + jat-memory index |
| 4 | Mark Task Complete | jat-step closing |
| 4.5 | Auto-Close Epics | jt epic close-eligible |
| 5 | Release Reservations | jat-step releasing |
| 6 | Emit Completion Signal | jat-step complete |
