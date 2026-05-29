---
name: cli-guide
description: SIMBL CLI command reference and usage guide. Use when working with SIMBL tasks or needing CLI syntax reference.
allowed-tools: Read, Bash, Grep, Glob
---

# SIMBL CLI Guide

Complete command reference for SIMBL, the CLI backlog manager.

## Installation

```bash
npm install -g simbl
# or
bun install -g simbl
```

## Initialize in a Project

```bash
simbl init
```

Creates `.simbl/tasks.md` with `# Backlog` and `# Done` sections.

## Core Commands

### Adding Tasks

```bash
simbl add "Task title"
simbl add "Task title" --priority 2
simbl add "Task title" --tags "backend,api"
simbl add "Task title" --content "Description here"
simbl add "Task title" --priority 2 --tags "backend,api" --content "Description here"
```

### Listing Tasks

```bash
simbl list                      # All backlog tasks
simbl list --status in-progress # Only in-progress
simbl list --status done        # Completed tasks
simbl list --tag backend        # Filter by tag
simbl list --project auth       # Filter by project
simbl list --search "login"     # Search titles/content
simbl list --limit 5            # Limit results
```

### Viewing a Task

```bash
simbl show task-1
simbl show 1                    # Short form (digits only)
```

> **Note:** Any command accepting a task ID supports short form. If user provides just digits (e.g., "9"), treat as "task-9" (or "{prefix}-9" with custom prefix).

### Updating Tasks

```bash
simbl update task-1 --title "New title"
simbl update task-1 --content "Replace content"
simbl update task-1 --append "Add to content"
```

### Managing Tags

```bash
simbl tag add task-1 backend
simbl tag add task-1 p1         # Sets priority (replaces existing)
simbl tag add task-1 in-progress # Marks as in-progress
simbl tag remove task-1 backend
```

### Completing Tasks

```bash
simbl done task-1               # Move to Done section
```

### Canceling Tasks

```bash
simbl cancel task-1             # Adds [canceled] tag
```

### Relationships

```bash
simbl relate task-2 --parent task-1      # task-2 is child of task-1
simbl relate task-3 --depends-on task-2  # task-3 depends on task-2
simbl unrelate task-2 --parent           # Remove parent relationship
simbl unrelate task-3 --depends-on task-2 # Remove dependency
```

### Validation

```bash
simbl doctor                    # Check for issues
```

### Web UI

```bash
simbl serve                     # Start browser UI on port 3497
```

## Tag Reference

### Priority Tags
- `[p1]` - Highest priority (urgent/critical)
- `[p2]` - High priority
- `[p3]` - Medium-high priority
- `[p4]` - Medium priority
- `[p5]` - Medium-low priority
- `[p6]` - Low priority
- `[p7]` - Lower priority
- `[p8]` - Very low priority
- `[p9]` - Lowest priority

Only one priority tag per task. Adding a new priority replaces the existing one.

### Status Tags
- `[in-progress]` - Currently being worked on
- `[canceled]` - Task was canceled
- `[refined]` - Task has been refined/detailed

### Project Tags
- `[project:name]` - Associates task with a project

### Relationship Tags
- `[child-of-task-1]` - This task is a subtask of task-1
- `[depends-on-task-2]` - This task is blocked by task-2

### Custom Tags
Any other `[tag-name]` format for categorization.

## Task File Format

Tasks are stored in `.simbl/tasks.md`:

```markdown
# Backlog

## task-1 Implement user authentication
[p2] [backend] [project:auth]

### Description
Add JWT-based auth to the API.

### Acceptance Criteria
- [ ] Login endpoint works
- [ ] Token refresh works

## task-2 Fix null pointer bug
[p1] [in-progress] [depends-on-task-1]

### Description
UserService.getProfile() crashes on null user.

# Done

## task-0 Set up project structure
[p2] [backend]

### Description
Initial project scaffolding.
```

## Multi-line Content

Use quotes for multi-line content:

```bash
simbl add "Task title" --content "Line 1
Line 2
Line 3"

simbl update task-1 --append "### Notes
- Point 1
- Point 2"
```

## Common Mistakes

### Wrong flags/commands

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| `--description` | `--content` |
| `simbl edit` | `simbl update` |
| `simbl modify` | `simbl update` |

### Relationship syntax (flags required, not positional)

```bash
# ❌ Wrong - positional args don't work
simbl relate task-2 depends-on task-1

# ✅ Correct - use flag syntax
simbl relate task-2 --depends-on task-1
simbl relate task-2 --parent task-1
```

### Available flags reference

**`simbl add`**:
- `--priority <N>` - Set priority (1-9)
- `--tags "tag1,tag2"` - Add tags (comma-separated)
- `--content "..."` - Set description/content

**`simbl update`**:
- `--title "..."` - Replace title
- `--content "..."` - Replace content
- `--append "..."` - Add to existing content

**`simbl relate`**:
- `--depends-on <id>` - This task depends on another
- `--parent <id>` - This task is a subtask of another
