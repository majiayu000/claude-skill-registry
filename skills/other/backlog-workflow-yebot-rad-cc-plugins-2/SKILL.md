---
name: backlog-workflow
description: Expert knowledge for working with Backlog.md task management. Use when managing tasks, organizing epics, handling dependencies, or tracking project progress. Automatically applies Backlog.md best practices.
allowed-tools: Read, Bash, Grep, Glob
---

# Backlog.md Workflow Skill

Expert guidance for managing projects with Backlog.md - a markdown-native task manager with MCP support.

## Core Concepts

### Tasks
- Stored as markdown files in `backlog/tasks/`
- Named pattern: `task-<id> - <title>.md`
- Support: status, priority, labels, assignees, acceptance criteria, notes, plans, dependencies

### Epics (Parent-Child)
- Parent tasks group related work
- Create subtasks with `-p <parent-id>`
- Track epic progress via subtask completion

### Dependencies
- Tasks can depend on other tasks
- Prevents starting blocked work
- Creates execution sequences
- Validated for circular references

### Statuses
- "To Do": Not started
- "In Progress": Currently being worked on
- "Done": Completed

## Command Reference

### Task Operations
```bash
backlog task create "Title" [options]
backlog task edit <id> [options]
backlog task <id>              # View task
backlog task list [filters]    # List tasks
backlog task archive <id>      # Archive completed task
```

### Common Options
```bash
--desc, -d     Description
--status, -s   Task status
--priority     high/medium/low
--labels, -l   Comma-separated labels
--assignee, -a @username
--ac           Acceptance criteria (repeatable)
--dep          Dependencies (task-1,task-2)
--plan         Implementation plan
--notes        Implementation notes
--append-notes Add to existing notes
-p             Parent task ID (for subtasks)
```

### Board & Search
```bash
backlog board              # Interactive Kanban board
backlog board export       # Export to markdown
backlog search "query"     # Fuzzy search tasks
backlog overview           # Project statistics
```

### Acceptance Criteria
```bash
--ac "Criterion"           # Add criterion
--check-ac 1               # Mark #1 complete
--uncheck-ac 2             # Mark #2 incomplete
--remove-ac 3              # Remove criterion
```

## Workflow Patterns

### Starting New Work
1. Search for existing tasks: `backlog search "<keywords>"`
2. If exists, update status to "In Progress"
3. If new, create task with full context
4. Set dependencies if applicable

### During Work
1. Add implementation notes as you learn
2. Check acceptance criteria as completed
3. Update status appropriately
4. Create subtasks for discovered work

### Completing Work
1. Verify all acceptance criteria are checked
2. Add final implementation notes
3. Move to "Done" status
4. Archive if no longer needed

### Epic Planning
1. Create parent task with epic overview
2. Break into 5-10 focused subtasks
3. Establish dependencies between subtasks
4. Track progress via subtask completion

## Multi-line Input (Bash/Zsh)

Use ANSI-C quoting for newlines:
```bash
backlog task edit <id> --notes $'Line 1\nLine 2\n\nParagraph 2'
```

## MCP Integration

When MCP is available, use backlog tools directly:
- `backlog.task_create` - Create tasks
- `backlog.task_update` - Update tasks
- `backlog.task_list` - List tasks
- `backlog.acceptance_criteria_check` - Check criteria
- `backlog.implementation_notes_append` - Add notes
- `backlog.dependencies_add` - Add dependencies
