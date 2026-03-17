---
name: tasks-sync
description: This skill should be used when syncing current session tasks to a project directory. It exports all tasks from the current Claude Code session to JSON files in the project's tasks directory, enabling persistence across sessions.
allowed-tools: ["Read", "Write", "Bash", "TaskList", "TaskGet"]
---

# Sync Tasks to Project

Sync all tasks from the current session to `projects/$ARGUMENTS/tasks/{session-id}/`.

This skill is for manual syncing when work started without setting an active project. Once synced, the automatic hook handles future task updates.

## Process

### Step 1: Validate Project

Check if the project directory exists:

```bash
ls -d projects/$ARGUMENTS 2>/dev/null
```

If the project doesn't exist, ask: "Project '$ARGUMENTS' doesn't exist. Create it?"

If yes, create the project structure:

```bash
mkdir -p projects/$ARGUMENTS/tasks
```

### Step 2: Determine Session ID

Find the current session by looking for the most recently modified task directory:

```bash
ls -dt ~/.claude/tasks/*/ 2>/dev/null | head -1 | xargs basename
```

If no session found, use a timestamp-based identifier:

```bash
echo "manual-$(date +%Y%m%d-%H%M%S)"
```

Store the session ID for use in subsequent steps.

### Step 3: Set Active Project

Create/update the active project marker:

```bash
echo "$ARGUMENTS" > .claude-active-project
```

### Step 4: Get Current Tasks

Use TaskList to get all tasks in the current session.

### Step 5: Sync Each Task

For each task from TaskList:

1. Use TaskGet to get full task details
2. Create the session directory:

```bash
mkdir -p projects/$ARGUMENTS/tasks/{session-id}
```

3. Create a JSON file with the task data:

```json
{
  "id": "<task-id>",
  "subject": "<subject>",
  "description": "<description>",
  "activeForm": "<activeForm>",
  "status": "<status>",
  "blocks": [],
  "blockedBy": []
}
```

4. Write to `projects/$ARGUMENTS/tasks/{session-id}/<id>.json`

### Step 6: Stage for Git

```bash
git add projects/$ARGUMENTS/tasks/{session-id}/*.json
```

### Step 7: Report

```
Synced X tasks to projects/$ARGUMENTS/tasks/{session-id}/
- Pending: Y
- In Progress: Z
- Completed: W

Files staged for commit. Run /git-commit when ready.
```

## Notes

- This skill manually syncs all current tasks to a project
- Use this when work started without a project context
- After syncing, the active project is set so future tasks auto-sync via the hook
- Each sync creates a new session directory to preserve history
