---
name: task-focus
description: Focus on a specific task with context loading
argument-hint: <task-id>
---

# task-focus

**Category**: Task Management

## Usage

```bash
task-focus <task-file>
```

## Arguments

- `<task-file>`: Required - Path to task file to focus on

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Check if focus/ directory is empty (enforce one-task rule)
2. If not empty, show current focus and ask to switch
3. Move the specified task file to tasks/focus/
4. Parse the task file to extract:
   - Task metadata (ID, title, status, priority)
   - All subtasks with their completion status
   - Current progress percentage
5. Load all tasks into TodoWrite tool
6. Update task file header with focus start time
7. Display current progress and next incomplete subtask
8. Show session restoration command for future use

## TodoTools Loading

Convert task file format to TodoWrite format:
```python
# File format: - [x] 1.1 Task description (2h)
# Todo format: {"id": "1.1", "content": "Task description", "status": "completed", "priority": "medium"}

# Status mapping:
# [ ] → "pending"
# [-] → "in_progress"
# [x] → "completed"
# [~] → "cancelled" (exclude from todos)
```

## Focus Session Start

Add to task file work log:
```markdown
## Work Log

### 2025-01-06 14:30 - SESSION START
- Moved to focus
- Current progress: 40%
- Next task: 2.3 Implement JWT tokens
```

## Output Format

```
🎯 Focusing on: TASK-001-user-authentication.md

📊 Task Overview:
   Title: Implement User Authentication
   Progress: 40% (4/10 subtasks)
   Estimated remaining: 4.5 hours
   Dependencies: All satisfied ✅

📋 Loading tasks into TodoTools...
   ✅ Loaded 10 tasks (4 completed, 6 pending)

🚀 Next subtask:
   2.3 Implement JWT tokens (est. 2h)

💡 To resume this session later:
   task-focus tasks/focus/TASK-001-user-authentication.md

Ready to work! Use 'task-done' when completing subtasks.
```

## Error Handling

- If task file not found: Show available tasks with `task-list`
- If focus not empty: Show current focus and confirm switch
- If task file invalid: Run validation and show errors
- If already in focus: Show message and continue

## Example

```bash
# Start focusing on a task
task-focus tasks/active/TASK-001-auth.md

# Focus on task from current directory
task-focus ./implement-search.md

# Switch focus (will prompt)
task-focus tasks/active/TASK-002-api.md
```

## Implementation Tips for Claude Code

1. **Atomic Move**: Use git mv if in git repo, ensure file moves successfully
2. **Parse Robustly**: Handle various task formats and indentation
3. **Preserve State**: Don't lose work log or metadata during move
4. **Time Tracking**: Start tracking time when focus begins
5. **Dependency Check**: Warn if dependencies not met
