---
name: sprinter-tasks
description: Manage tasks in the Sprinter kanban board using MCP tools. This skill
  enables AI agents to create, claim, and complete tasks programmatically.
---

# Sprinter Task Management Skill

## Description

Manage tasks in the Sprinter kanban board using MCP tools. This skill enables AI agents to create, claim, and complete tasks programmatically.

## When to Use

- **Tech-Lead Planning**: After creating an implementation plan, use `create_tasks_batch` to create tasks
- **Worker Agents**: Use `get_next_task`, `claim_task`, and `complete_task` to work through tasks
- **Task Visibility**: Use `list_tasks` to see current task board state

## Available Tools

### Task Creation

**create_task** - Create a single task
```
mcp__sprinter__create_task(title: "Task title", description: "Optional description")
```

**create_tasks_batch** - Create multiple tasks at once (for tech-lead planning)
```
mcp__sprinter__create_tasks_batch(tasks: [
  {title: "Task 1", description: "Description 1"},
  {title: "Task 2", description: "Description 2"}
])
```

### Task Discovery

**list_tasks** - List all tasks or filter by status
```
mcp__sprinter__list_tasks()                    # All tasks
mcp__sprinter__list_tasks(status: "todo")      # Only todo tasks
mcp__sprinter__list_tasks(status: "in_progress")
mcp__sprinter__list_tasks(status: "done")
```

**get_task** - Get details of a specific task
```
mcp__sprinter__get_task(task_id: "uuid-here")
```

**get_next_task** - Get the next available unclaimed task
```
mcp__sprinter__get_next_task()
```

### Task Workflow

**claim_task** - Atomically claim a task for work
```
# Claim specific task
mcp__sprinter__claim_task(agent_id: "claude-session-123", task_id: "uuid-here")

# Claim next available task
mcp__sprinter__claim_task(agent_id: "claude-session-123")
```

**complete_task** - Mark a task as done
```
mcp__sprinter__complete_task(agent_id: "claude-session-123", task_id: "uuid-here")
```

### Agent Status

**get_agent_status** - Check agent's current state
```
mcp__sprinter__get_agent_status(agent_id: "claude-session-123")
```

## Workflows

### Tech-Lead: Create Tasks After Planning

After completing a plan and exiting plan mode:

1. Extract tasks from the plan
2. Call `create_tasks_batch` with all tasks:
```
mcp__sprinter__create_tasks_batch(tasks: [
  {title: "Implement user authentication", description: "Add login/logout endpoints"},
  {title: "Add database migrations", description: "Create users table"},
  {title: "Write unit tests", description: "Test auth handlers"}
])
```

### Worker: Process Tasks

1. **Poll for work**:
```
mcp__sprinter__get_next_task()
```

2. **Claim the task** (atomic - prevents race conditions):
```
mcp__sprinter__claim_task(agent_id: "claude-session-123", task_id: "task-uuid")
```

3. **Work on the task** - implement the required changes

4. **Complete the task**:
```
mcp__sprinter__complete_task(agent_id: "claude-session-123", task_id: "task-uuid")
```

5. **Repeat** - poll for next task

## Agent ID Convention

Use a consistent agent ID format for your session:
- Format: `claude-{unique-identifier}`
- Examples: `claude-abc123`, `claude-feature-auth`, `claude-worker-1`

The agent ID is used to:
- Track which agent claimed which task
- Prevent multiple agents from claiming the same task
- Monitor agent status (idle/working)

## Task Statuses

| Status | Description |
|--------|-------------|
| `todo` | Task is available for claiming |
| `in_progress` | Task has been claimed by an agent |
| `done` | Task has been completed |

## Best Practices

1. **Always claim before working** - Prevents duplicate work
2. **Use descriptive titles** - Makes task board readable
3. **Complete tasks promptly** - Keeps agent status accurate
4. **Check task list** - Before creating tasks, verify they don't already exist
