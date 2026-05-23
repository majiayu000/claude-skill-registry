---
name: task
description: Manage Contextium tasks - create, update, complete, and list tasks
allowed-tools: Bash, Read, Write, Edit
argument-hint: [create|complete|list|status] [task-id]
---

# Task Management

Manage tasks in `.contextium/tasks.json`.

## Commands

Based on `$ARGUMENTS`:

### `task create <id> <description>`
Create a new task:
```bash
# Read current tasks
cat .contextium/tasks.json

# Add new task using jq (or edit manually)
```

### `task complete <id>`
Mark a task as completed.

### `task list`
Show all tasks and their status.

### `task status`
Show current task and progress summary.

## Task Structure

Each task in `tasks.json`:
```json
{
  "id": "unique-task-id",
  "description": "What needs to be done",
  "status": "pending|in_progress|completed",
  "priority": "low|normal|high",
  "scope": ["src/path/*", "tests/path/*"],
  "dependencies": ["other-task-id"],
  "created": "2024-01-15T10:00:00Z",
  "completed": null
}
```

## Workflow

1. **Create tasks** when starting new work
2. **Set scope** to define which files/modules
3. **Update status** as you work
4. **Complete tasks** when done and verified

## Integration

Tasks integrate with:
- **Task Determiner** - Selects next task automatically
- **Context Fetcher** - Loads context based on task scope
- **Harness Pattern** - Works with `claude-progress.txt`
