---
name: task-list
description: List tasks by directory with progress and visual indicators
argument-hint: "[--dir <directory>] [--status <status>] [--format <format>]"
---

# task-list

**Category**: Task Management

## Usage

```bash
task-list [--dir <directory>] [--status <status>] [--format <format>]
```

## Arguments

- `--dir`: Optional - Specific directory (focus, active, paused, completed, all). Default: all
- `--status`: Optional - Filter by status (pending, in_progress, completed, blocked)
- `--format`: Optional - Output format (table, list, json). Default: table

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Scan specified directories for task files (*.md)
2. Parse each task file header to extract:
   - Task ID and title
   - Status and priority
   - Progress percentage
   - Estimated/actual hours
   - Blocked status
   - Dependencies
3. Apply any filters (status, etc.)
4. Calculate aggregate statistics
5. Display in requested format

## Directory Scanning Order

1. **focus/** - Show first (current work)
2. **active/** - Ready tasks
3. **paused/** - Context switched
4. **completed/** - Recently done
5. **archive/** - If requested

## Output Formats

### Table Format (default)
```
📋 Task List Overview

FOCUS (1 task)
ID        | Title                      | Progress | Est/Act | Priority | Status
----------|----------------------------|----------|---------|----------|------------
TASK-001  | User Authentication       | 50%      | 8h/4h   | 🔴 High  | In Progress

ACTIVE (3 tasks)
ID        | Title                      | Progress | Est/Act | Priority | Status
----------|----------------------------|----------|---------|----------|------------
TASK-002  | API Documentation         | 0%       | 4h/0h   | 🟡 Med   | Pending
TASK-003  | Search Implementation     | 20%      | 12h/2h  | 🔴 High  | In Progress
TASK-004  | Performance Optimization  | 0%       | 6h/0h   | 🟢 Low   | Blocked ⚠️

PAUSED (1 task)
ID        | Title                      | Progress | Est/Act | Priority | Reason
----------|----------------------------|----------|---------|----------|------------
TASK-005  | Data Migration           | 30%      | 10h/3h  | 🟡 Med   | Waiting for DB

Summary: 5 tasks | 2 in progress | 1 blocked | Total: 40h estimated, 9h actual
```

### List Format
```
📋 Task List

🎯 FOCUS
└── TASK-001: User Authentication
    Progress: 50% | 8h estimated, 4h actual | High priority
    Status: In Progress | Next: 2.3 Implement JWT tokens

📂 ACTIVE (3)
├── TASK-002: API Documentation
│   Progress: 0% | 4h estimated | Medium priority
│   Status: Pending | Dependencies: TASK-001
│
├── TASK-003: Search Implementation
│   Progress: 20% | 12h estimated, 2h actual | High priority
│   Status: In Progress
│
└── TASK-004: Performance Optimization
    Progress: 0% | 6h estimated | Low priority
    Status: Blocked ⚠️ | Reason: Waiting for profiling tools
```

### JSON Format
```json
{
  "summary": {
    "total_tasks": 5,
    "in_progress": 2,
    "blocked": 1,
    "total_estimated_hours": 40,
    "total_actual_hours": 9
  },
  "tasks": {
    "focus": [...],
    "active": [...],
    "paused": [...],
    "completed": [...]
  }
}
```

## Progress Indicators

- `████████░░` - Visual progress bar
- Percentage with color coding:
  - 0-25%: 🔴 Red
  - 26-75%: 🟡 Yellow
  - 76-100%: 🟢 Green

## Error Handling

- If no tasks found: Show helpful message about creating tasks
- If task file corrupted: Mark with ❌ and continue
- If no task directories: Suggest running `task-system-init`

## Example

```bash
# List all tasks
task-list

# Show only focused task
task-list --dir focus

# Show all in-progress tasks
task-list --status in_progress

# Get JSON for automation
task-list --format json > tasks.json

# Show only active directory in list format
task-list --dir active --format list
```

## Implementation Tips for Claude Code

1. **Efficient Parsing**: Cache parsed headers for performance
2. **Smart Sorting**: Focus first, then by priority and progress
3. **Dependency Tracking**: Show dependency chains if relevant
4. **Time Calculations**: Sum estimates and actuals by directory
5. **Visual Appeal**: Use Unicode characters for better formatting
