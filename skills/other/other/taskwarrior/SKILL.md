---
name: taskwarrior
description: Manage tasks and reminders using Taskwarrior (CLI).
metadata: {"requires": ["taskwarrior"]}
---

# Taskwarrior Skill

Manage local tasks and reminders using the high-performance `taskwarrior` CLI database.

## Tools
Access via `mcp__taskwarrior__*`:
- `task_add(description, due, priority, project, tags)`: Create a task.
- `task_list(filter_str)`: List pending tasks. Default filter: "status:pending".
- `task_done(id)`: Mark a task as complete.
- `task_modify(id, ...)`: Update task details.

## Best Practices
- **Descriptions**: Keep them actionable (verb-object).
- **Projects**: Use projects to group tasks (e.g., `proj:Work`).
- **Tags**: Use tags for context (e.g., `+email`, `+urgent`).
- **Filtering**: When listing, use `task_list(filter_str="prob:Work status:pending")` to narrow down.

## Integration
This skill runs via a local MCP server that wraps `tasklib`. It requires `taskwarrior` (binary) to be installed on the system.
