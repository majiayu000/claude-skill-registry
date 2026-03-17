---
name: tasks-load
description: This skill should be used when loading tasks from a project directory into the current Claude Code session. It reads task JSON files from session subdirectories, recreates them in the current session, and sets the active project marker.
allowed-tools: ["Read", "Bash", "TaskCreate", "TaskUpdate", "TaskList"]
---

# Load Project Tasks

Load tasks from `projects/$ARGUMENTS/tasks/` into the current Claude Code session.

Tasks are stored in session subdirectories to preserve history across `/clear` commands:
```
projects/$ARGUMENTS/tasks/
├── {session-1-uuid}/
│   ├── 1.json
│   └── 2.json
└── {session-2-uuid}/
    ├── 1.json
    └── 2.json
```

## Process

### Step 1: Validate Project

Check if the project exists and has task files:

```bash
find projects/$ARGUMENTS/tasks -name "*.json" 2>/dev/null | head -5
```

If no task files exist, report: "No tasks found in projects/$ARGUMENTS/tasks/"

List available sessions:

```bash
ls -dt projects/$ARGUMENTS/tasks/*/ 2>/dev/null | head -10
```

### Step 2: Set Active Project

Create the active project marker:

```bash
echo "$ARGUMENTS" > .claude-active-project
```

This ensures any new tasks created will sync back to this project.

### Step 3: Load Tasks

Find and load all task JSON files from ALL session directories:

```bash
find projects/$ARGUMENTS/tasks -name "*.json" -type f
```

For each JSON file found:

1. Read the task JSON file
2. Use TaskCreate to recreate the task with:
   - subject from JSON
   - description from JSON
   - activeForm from JSON
   - metadata: `{ "project": "$ARGUMENTS" }`
3. If the task was already completed (status: "completed"), use TaskUpdate to mark it completed

### Step 4: Report

After loading all tasks, report:

```
Loaded X tasks from projects/$ARGUMENTS/tasks/
- Sessions found: N
- Pending: Y
- Completed: Z

Active project set to: $ARGUMENTS
New tasks will automatically sync to this project.
```

## Notes

- Tasks are recreated with new IDs in the current session
- The original task IDs from the project are not preserved
- Tasks from ALL sessions are loaded (full history)
- Task dependencies (blocks/blockedBy) are NOT currently preserved across load/sync cycles
- Use TaskList to see the loaded tasks
