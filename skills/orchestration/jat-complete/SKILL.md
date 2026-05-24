---
name: jat-complete
description: Complete current JAT task with full verification. Checks Agent Mail, verifies work (tests/lint), commits changes, closes task in Beads, releases file reservations, announces completion, and emits final signal. Session ends after completion.
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

1. **Read & Respond to Agent Mail** (always, before completing)
2. **Verify task** (tests, lint, security)
3. **Commit changes** with proper message
4. **Mark task complete** in Beads (`bd close`)
5. **Release file reservations**
6. **Announce completion** via Agent Mail
7. **Emit completion signal** to IDE

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
bd list --json | jq -r '.[] | select(.assignee == "AGENT_NAME" and .status == "in_progress") | .id'
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
bd create "INFERRED_TITLE" \
  --type INFERRED_TYPE \
  --description "INFERRED_DESCRIPTION" \
  --assignee "$AGENT_NAME" \
  --status in_progress
```

If no work detected, exit the completion flow.

### STEP 2: Read & Respond to Agent Mail

**Mandatory. Do NOT skip.**

```bash
am-inbox "$AGENT_NAME" --unread
```

- Read each message
- Reply if needed: `am-reply MSG_ID "response" --agent "$AGENT_NAME"`
- Acknowledge: `am-ack MSG_ID --agent "$AGENT_NAME"`

Messages might say "don't complete yet" or "requirements changed" - check before proceeding.

### STEP 3: Verify Task

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

### STEP 3.5: Update Documentation (If Appropriate)

Only update docs when changes affect how others use the codebase:
- New tool/command added
- New API endpoint
- Breaking change
- New configuration option

Most tasks do NOT need doc updates.

### STEP 4: Commit Changes

```bash
# Get task type for commit prefix
TASK_TYPE=$(bd show "$TASK_ID" --json | jq -r '.[0].issue_type // "task"')

# Commit with proper message format
jat-step committing --task "$TASK_ID" --title "$TASK_TITLE" --agent "$AGENT_NAME" --type "$TASK_TYPE"
```

If `jat-step` is not available, commit manually:

```bash
git add -A
git commit -m "TASK_TYPE($TASK_ID): TASK_TITLE

Co-Authored-By: Pi Agent <noreply@pi.dev>"
```

### STEP 5: Mark Task Complete in Beads

```bash
jat-step closing --task "$TASK_ID" --title "$TASK_TITLE" --agent "$AGENT_NAME"
```

Or manually:

```bash
bd close "$TASK_ID" --reason "Completed by $AGENT_NAME"
```

### STEP 5.5: Auto-Close Eligible Epics

```bash
bd epic close-eligible
```

### STEP 6: Release File Reservations

```bash
jat-step releasing --task "$TASK_ID" --title "$TASK_TITLE" --agent "$AGENT_NAME"
```

Or manually:

```bash
am-reservations --agent "$AGENT_NAME" --json | jq -r '.[].pattern' | while read pattern; do
  am-release "$pattern" --agent "$AGENT_NAME"
done
```

### STEP 7: Announce Completion

```bash
jat-step announcing --task "$TASK_ID" --title "$TASK_TITLE" --agent "$AGENT_NAME" --type "$TASK_TYPE"
```

Or manually:

```bash
am-send "[$TASK_ID] Completed: $TASK_TITLE" "Task completed successfully." \
  --from "$AGENT_NAME" --to @active --thread "$TASK_ID"
```

### STEP 8: Emit Completion Signal

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

| State | Meaning | Beads Status |
|-------|---------|--------------|
| Ready for Review | Code done, awaiting user decision | in_progress |
| Complete | Closed in Beads, reservations released | closed |

**Never say "Task Complete" until bd close has run.**

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
| 1 | Get Task and Agent Identity | bd list, tmux |
| 1D | Spontaneous Work Detection | git status |
| 2 | Read & Respond to Mail | am-inbox, am-ack |
| 3 | Verify Task | jat-step verifying |
| 3.5 | Update Documentation | (if appropriate) |
| 4 | Commit Changes | jat-step committing |
| 5 | Mark Task Complete | jat-step closing |
| 5.5 | Auto-Close Epics | bd epic close-eligible |
| 6 | Release Reservations | jat-step releasing |
| 7 | Announce Completion | jat-step announcing |
| 8 | Emit Completion Signal | jat-step complete |
