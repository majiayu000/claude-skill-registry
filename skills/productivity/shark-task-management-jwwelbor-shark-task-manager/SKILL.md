---
name: shark-task-management
description: Task lifecycle management using the shark CLI for tracking implementation progress, status updates, and team visibility
when_to_use: when starting tasks, completing tasks, or querying task status during implementation work
version: 1.0.0
---

# Shark Task Management

## Overview

The shark CLI provides task lifecycle management for implementation work. It tracks task status in a SQLite database, enabling team visibility, accurate progress reporting, and implementation history.

## Quick Reference

### Slash Commands

Use these slash commands for task management:

- **`/task-start <task-id>`** - Start working on a task (updates status to "in-progress")
- **`/task-complete <task-id>`** - Mark task as completed (records completion time)
- **`/task-next`** - Get the next available task to work on
- **`/task-list [filters]`** - List all tasks with optional filters
- **`/task-info <task-id>`** - Get detailed information about a task

### Direct CLI Usage

```bash
# Start a task
shark task start T-E04-F02-001

# Complete a task
shark task complete T-E04-F02-001

# Get next task
shark task next

# List tasks by status
shark task list --status=todo

# Get task details
shark task get T-E04-F02-001

# List tasks by epic
shark task list --epic=E04
```

## Integration with Implementation Workflows

### Standard Implementation Flow

```
1. Get next task: /task-next
   ↓
2. Review task requirements and dependencies
   ↓
3. Start task: /task-start <task-id>
   ↓
4. Implement following the appropriate workflow
   ↓
5. Run validation gates
   ↓
6. Complete task: /task-complete <task-id>
```

### When to Use Task Management

**Always use `/task-start` when:**
- Beginning implementation of a task
- Starting work on a PRP (Product Requirement Prompt)
- Following an implementation workflow (API, backend, frontend, database, tests)

**Always use `/task-complete` when:**
- All validation gates have passed
- Implementation is complete and tested
- Documentation is updated
- Ready to move to the next task

## What Shark Tracks

When you use shark task management, the database automatically records:

- **Status transitions** - from "todo" → "in-progress" → "completed"
- **Timestamps** - when tasks start and complete
- **Implementation history** - full audit trail of task lifecycle
- **Team visibility** - all developers can see current task status
- **Progress metrics** - enables accurate reporting and dashboards

## Task Status States

- **`todo`** - Task ready to be started, dependencies met
- **`in-progress`** - Task currently being worked on
- **`completed`** - Task finished, validated, and documented
- **`blocked`** - Task waiting on dependencies or decisions
- **`cancelled`** - Task no longer needed

## Benefits

### For Individual Developers

- Clear tracking of what you're working on
- Automatic timestamp recording
- Easy to see progress through task list
- No manual status updates needed

### For Teams

- Real-time visibility into who's working on what
- Accurate progress reporting for standups
- Historical data for velocity calculations
- Audit trail for completed work

### For Implementation Skills

Other skills reference task management:
- `implementation` skill includes task commands in all workflows
- `quality` skill checks task status before reviews
- `orchestration` skill uses task tracking for multi-agent coordination

## Examples

### Starting a New Task

```bash
# Get next task
/task-next

# Review task: T-E04-F02-003 "Implement user service layer"

# Start the task
/task-start T-E04-F02-003

# Output:
# ✓ Task T-E04-F02-003 started
# - Status: in-progress
# - Timestamp recorded in database
# - Progress tracking enabled
```

### Completing a Task

```bash
# After implementation, tests passing, documentation updated
/task-complete T-E04-F02-003

# Output:
# ✓ Task T-E04-F02-003 completed
# - Status: completed
# - Completion time recorded in database
# - Implementation tracking closed
```

### Listing Tasks

```bash
# See all tasks
/task-list

# See only todo tasks
/task-list --status=todo

# See tasks in epic E04
/task-list --epic=E04
```

## Integration Points

### With Implementation Skill

The `implementation` skill references task management:

```markdown
## Phase 0: Start Task Tracking

Before beginning implementation, start task tracking:

```bash
/task-start <task-id>
```

This updates task status and enables progress tracking.
```

### With Other Skills

- **quality**: Validates task is in-progress before code review
- **orchestration**: Coordinates task assignment across agents
- **devops**: Links deployments to completed tasks

## CLI Reference

For complete CLI documentation, see [docs/CLI.md](../../docs/CLI.md).

### Global Flags

- `--json` - Output in JSON format (machine-readable)
- `--no-color` - Disable colored output
- `--verbose` / `-v` - Enable verbose/debug output

### Task Commands

```bash
shark task list                    # List all tasks
shark task list --status=todo      # Filter by status
shark task list --epic=E04         # Filter by epic
shark task get T-E01-F01-001      # Get task details
shark task start T-E01-F01-001    # Start working on a task
shark task complete T-E01-F01-001 # Mark task as complete
shark task next                    # Get next available task
```

## Best Practices

### Do

- ✓ Start tasks before beginning implementation
- ✓ Complete tasks only after all validation gates pass
- ✓ Use `/task-next` to stay focused on prioritized work
- ✓ Check task dependencies before starting
- ✓ Update documentation before completing tasks

### Don't

- ✗ Skip task tracking "to save time"
- ✗ Complete tasks before tests pass
- ✗ Work on multiple tasks simultaneously (update status correctly)
- ✗ Start tasks with unmet dependencies
- ✗ Forget to complete tasks when finished

## Troubleshooting

### Task start fails

```bash
# Check if task exists
shark task get T-E04-F02-001

# Check if dependencies are met
shark task get T-E04-F02-001 | jq '.dependencies'
```

### Task already in-progress

```bash
# If you accidentally started wrong task, complete it first
shark task complete T-E04-F02-001

# Or check who's working on it
shark task get T-E04-F02-001 | jq '.status'
```

## See Also

- [CLI Documentation](../../docs/CLI.md) - Complete shark CLI reference
- [Implementation Skill](../implementation/SKILL.md) - Integration with implementation workflows
- [Task Index](../../docs/tasks/) - Browse all tasks by epic/feature

---

**Remember:** Task tracking provides visibility and accountability. Use it consistently to enable accurate reporting and team coordination.
