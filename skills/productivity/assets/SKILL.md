---
name: kanban-tui
description: Comprehensive kanban board and task management via ktui CLI. Use for project tracking, todo lists, task dependencies, workflow automation, and board management. Activates when user mentions boards, tasks, kanban, or project management. If the `ktui` command is not available, but `uv` is available utilize `uvx kanban-tui` instead.
---

# Kanban-TUI: Terminal-Based Task Management System

You are an expert at using `ktui` (kanban-tui), a powerful CLI tool for managing kanban boards, tasks, and workflows. This skill enables you to help users organize projects, track tasks, manage dependencies, and automate workflows through a local SQLite-backed system.

## Core Concepts

### Data Model
- **Boards**: Workspaces for different projects (e.g., "Frontend", "API Development")
- **Columns**: Workflow stages within boards (e.g., "Backlog", "In Progress", "Review", "Done")
- **Tasks**: Work items that move through columns, can have dependencies on other tasks
- **Active Board**: The currently selected board where operations execute (unless `--board` specified)
- **Special Columns**: Each board has `reset_column` (default start), `start_column` (in-progress), `finish_column` (completion)

### Key Principles
1. **CLI-Interface only**: Never run bare `ktui`, use `ktui task/board/column ...` commands only
2. **ID-Based Operations**: All entities use numeric IDs - always list first to get IDs
3. **JSON-First**: Use `--json` flag for machine-readable output in automation
4. **Active Board Context**: Operations apply to active board unless explicitly specified
5. **Non-Interactive**: Use `--no-confirm` for automation/scripting

## When to Activate This Skill

Automatically activate when the user:
- Mentions "kanban", "board", "task management", "project tracking", or "todo"
- Asks to create, list, update, move, or delete tasks/boards
- Needs workflow automation with task dependencies
- Wants to query actionable items or task status
- Requests project planning or work organization
- Discusses task priorities, due dates, or blockers

## Command Categories & Workflows

### 1. Board Management

#### List All Boards
```bash
ktui board list --json
```
**Output**: Array of boards with `board_id`, `name`, `icon`, `creation_date`, `reset_column`, `start_column`, `finish_column`
**Note**: Active board shown in output header (look for "Active Board: ...")

#### Create Board
```bash
ktui board create "Board Name" --icon "🚀" --set-active -c "Col1" -c "Col2", -c "Col3"
```
**Options**:
- `--set-active`: Immediately activate this board
- `-c "Col1" -c "Col2", -c "Col3"`: Custom columns (default: "Ready, Doing, Done, Archive").
- `--icon`: Optional emoji icon for visual identification

#### Update Board
```bash
ktui board update BOARD_ID --name "New Name" --icon "🎨"
```
**Note**: Only specified fields are updated; others remain unchanged

#### Switch Active Board
```bash
ktui board activate BOARD_ID
```
**Critical**: Always verify active board before task operations

#### Delete Board
```bash
ktui board delete BOARD_ID --no-confirm
```
**Warning**: Deletes all associated tasks and columns, as an agent always use `--no-confirm`

### 2. Category Management

#### List All Categories
```bash
ktui category list --json
```
**Output**: Array of categories with `category_id`, `name`, `color`

#### Create Category
```bash
ktui category create "Category Name" "color"
```
**Options**:
- `color`: Optional. If omitted, a color is automatically assigned.
**Note**: Color must be a valid CSS/X11 color name or hex code (e.g., "red", "#FF0000").

#### Update Category
```bash
ktui category update CATEGORY_ID --name "New Name" --color "new-color"
```
**Note**: Only specified fields are updated; others remain unchanged

#### Delete Category
```bash
ktui category delete CATEGORY_ID --no-confirm
```
**Impact**: Resets the category of all associated tasks to null, as an agent always use `--no-confirm`

### 3. Task Management

#### List Tasks
```bash
ktui task list --json
```
**Filters**:
- `--column COLUMN_ID`: Tasks in specific column
- `--board BOARD_ID`: Tasks on specific board
- `--actionable`: Only non-blocked tasks (no unfinished dependencies)

**Output Fields**: `task_id`, `title`, `description`, `column_id`, `board_id`, `due_date`, `category_id`, `depends_on` (array), `creation_date`

#### Create Task
```bash
ktui task create "Task Title" --description "Details" --column COLUMN_ID --category CATEGORY_ID --due-date 2026-01-20 --depends-on TASK_ID
```
**Options**:
- `--column`: Target column ID (omit for leftmost visible column of active board)
- `--category`: Category ID to assign to the task
- `--due-date`: Format MUST be `YYYY-MM-DD` (e.g., "2026-01-20")
- `--depends-on`: Dependency task ID (use multiple times for multiple dependencies)

**Example Multi-Dependency**:
```bash
ktui task create "Deploy to prod" --depends-on 5 --depends-on 7 --depends-on 9
```

**Note**: To create tasks on other boards, only use the `--column` flag to reference a column on that board

#### Update Task
```bash
ktui task update TASK_ID --title "New Title" --description "New Desc" --category CATEGORY_ID --due-date 2026-01-21 --depends-on TASK_ID --remove-dependency TASK_ID
```
**Options**:
- `--title`: Update task title
- `--description`: Update task description
- `--category`: Update category ID
- `--due-date`: Update due date (format: `YYYY-MM-DD`)
- `--depends-on`: Add dependency task ID (use multiple times for multiple dependencies)
- `--remove-dependency`: Remove dependency task ID (use multiple times for multiple dependencies)

**Note**: Only specified fields are updated; others remain unchanged

**Dependency Management Examples**:
```bash
# Add single dependency
ktui task update 42 --depends-on 15

# Add multiple dependencies
ktui task update 42 --depends-on 15 --depends-on 20 --depends-on 25

# Remove dependency
ktui task update 42 --remove-dependency 15

# Update title and add dependencies
ktui task update 42 --title "Updated Task" --depends-on 15 --depends-on 20
```

**Validation**: The system validates dependencies when updating:
- Checks if dependency tasks exist and prevents duplicate and circular dependencies

#### Move Task Between Columns
```bash
ktui task move TASK_ID TARGET_COLUMN_ID
```
**Dependency Blocking**: Tasks with unfinished dependencies cannot move to start/finish columns

#### Delete Task
```bash
ktui task delete TASK_ID --no-confirm
```
**Impact**: Removes task and all its dependency relationships, as an agent always use `--no-confirm`

### 4. Column Operations

#### List Columns
```bash
ktui column list --json
```
**Filters**: `--board BOARD_ID` to show columns for specific board
**Output**: `column_id`, `name`, `board_id`, `position`, `visible`

**CLI Capabilities**:
- ✅ **Available**: `ktui column list` (read-only query)
- ❌ **TUI Only**: Column creation, deletion, reordering, and renaming requires human in interactive mode (`ktui`)

## Task Dependencies System

### Dependency Behavior
- **Blocking**: Tasks with unfinished dependencies cannot move to start column

### Dependency Patterns

**Sequential Workflow**:
```bash
# Create tasks with chain dependencies
ktui task create "Design API" --column 1
ktui task create "Implement API" --column 1 --depends-on 1
ktui task create "Write Tests" --column 1 --depends-on 2
ktui task create "Deploy" --column 1 --depends-on 3
```

**Parallel Dependencies**:
```bash
# Multiple tasks must complete before final task
ktui task create "Frontend" --column 1
ktui task create "Backend" --column 1
ktui task create "Database" --column 1
ktui task create "Integration" --column 1 --depends-on 1 --depends-on 2 --depends-on 3
```

### Query Actionable Tasks
```bash
ktui task list --json --actionable
```
**Use Case**: Find tasks ready to work on (no blocking dependencies)

## Standard Operational Procedure

Follow this sequence for all operations:

### Step 1: Discover IDs
```bash
# Get board IDs and identify active board
ktui board list --json

# Get column IDs for current board
ktui column list --json

# Get task IDs
ktui task list --json
```

### Step 2: Verify Context
- Check active board from output header
- Activate correct board if needed: `ktui board activate BOARD_ID`
- Note column IDs for task placement

### Step 3: Execute Operation
- Use retrieved IDs in commands
- Always use `--json` for automation
- Use `--no-confirm` for non-interactive execution

### Step 4: Validate Result
- Re-list entities to confirm changes
- Check task status after moves
- Verify dependency relationships if relevant

## Practical Scenarios

### Scenario 1: New Project Setup
**User Request**: "Set up a new project board for our API development"

**Actions**:
```bash
# Create board with workflow columns Always prefer default columns, i.e. no -c options, if not told otherwise, to ensure already working status columns

ktui board create "API Development" --icon "⚙️" --set-active

# Get column IDs
ktui column list --json

# Create initial tasks with dependencies
ktui task create "Define API spec" --column 1 --due-date 2026-01-25
ktui task create "Implement endpoints" --column 1 --depends-on 1 --due-date 2026-02-01
ktui task create "Write unit tests" --column 1 --depends-on 2 --due-date 2026-02-05
ktui task create "Integration testing" --column 1 --depends-on 3 --due-date 2026-02-08
```

### Scenario 2: Daily Workflow Check
**User Request**: "What tasks can I work on today?"

**Actions**:
```bash
# List actionable tasks (no blockers)
ktui task list --json --actionable

# Check for overdue tasks (compare due_date to today's date)
ktui task list --json

# Review specific column (e.g., "In Progress")
ktui task list --json --column 2
```

### Scenario 3: Task Lifecycle Management
**User Request**: "Move task 42 to the next stage"

**Actions**:
```bash
# Get current task status
ktui task list --json | grep -A 10 '"task_id": 42'

# Get column IDs
ktui column list --json

# Move task (if no blockers)
ktui task move 42 3

# Update task details if needed
ktui task update 42 --description "Completed code review feedback"
```

### Scenario 4: Multi-Board Project Tracking
**User Request**: "Show me all boards and their urgent tasks"

**Actions**:
```bash
# List all boards
ktui board list --json

# For each board, check actionable tasks
ktui task list --json --board 1 --actionable
ktui task list --json --board 2 --actionable
```

## JSON Response Structures

### Board Object
```json
{
  "board_id": 1,
  "name": "Project X",
  "icon": "🚀",
  "creation_date": "2026-01-19T01:36:33",
  "reset_column": 1,
  "start_column": 2,
  "finish_column": 3
}
```

### Task Object
```json
{
  "task_id": 42,
  "title": "Implement feature",
  "description": "Add user authentication",
  "column_id": 2,
  "board_id": 1,
  "due_date": "2026-01-25",
  "depends_on": [12, 15],
  "creation_date": "2026-01-20T10:30:00"
}
```

### Column Object
```json
{
  "column_id": 2,
  "name": "In Progress",
  "board_id": 1,
  "position": 1,
  "visible": true
}
```

## Critical Rules & Constraints

### Date Formatting
- **ONLY VALID FORMAT**: `YYYY-MM-DD`
- **Examples**: "2026-01-20", "2026-12-31"
- **Invalid**: "01/20/2026", "20-01-2026", "Jan 20 2026"

### ID Requirements
- All IDs are numeric integers
- IDs are auto-generated and permanent
- Always retrieve IDs via `list --json` commands
- Never guess or invent IDs

### Text Handling
- Quote strings with spaces: `"Task Title"`, `"Multi-word description"`
- The task description also supports markdown
- Escape special shell characters if present
- Use descriptive task titles (user-facing) and detailed descriptions

### Dependency Constraints
- Cannot create circular dependencies
- Cannot move blocked tasks to start/finish columns (without `--force`)
- Deleting a task removes all its dependency relationships
- A task can have multiple dependencies

### Active Board Context
- **Default behavior**: All operations affect the active board
- **Override**: Use `--board BOARD_ID` to target specific board when listing
- **Verify before operations**: Check active board with `ktui board list --json`

## Error Prevention Checklist

Before executing commands:
- [ ] Retrieved all necessary IDs via list commands
- [ ] Verified correct board is active
- [ ] Validated date format is `YYYY-MM-DD`
- [ ] Checked for dependency blockers before moving tasks
- [ ] Quoted strings with spaces or special characters
- [ ] Used `--no-confirm` for non-interactive operations
- [ ] Used `--json` for machine-readable output

## System Information

### Additional Commands for humans
- `ktui`: Launch TUI interface (exit with `ctrl+q`)
- `ktui demo`: Temporary demo instance with example data
- `ktui demo --clean`: Empty demo instance
- `ktui demo --keep`: Don't delete demo data after exit
- `ktui --web`: Launch web interface (requires textual-serve)
- `ktui clear`: Delete all data and config
- `ktui info`: Show file locations
- `ktui --version`: Display version

### Database Schema Overview
- **tasks** table: Task details with foreign keys to columns and categories
- **task_dependencies** table: Many-to-many task relationships
- **boards** table: Board configurations
- **columns** table: Workflow stages per board
- **categories** table: Task categorization (TUI only)
- **audits** table: Change tracking (automatic)

## Best Practices for Agent Use

### 1. Always Start with Discovery
```bash
# Standard initialization sequence
ktui board list --json
ktui column list --json
ktui task list --json
```

### 2. Communicate Intent
Before executing operations, explain to the user:
- What board/tasks you're working with
- What changes you're about to make
- Any potential impacts (e.g., dependency blocking)

### 3. Validate Assumptions
- Confirm board names and IDs before operations
- Check task dependencies before moving
- Verify date formats before setting due dates

### 4. Handle Errors Gracefully
- If a command fails, explain why (e.g., "Task 42 cannot move because task 15 is unfinished")
- Suggest alternatives (e.g., "Use --force to override" or "Complete dependency first")

### 5. Batch Related Operations
```bash
# Instead of multiple separate commands, chain related operations:
ktui task create "Task 1" --column 1 && \
ktui task create "Task 2" --column 1 --depends-on 1 && \
ktui task create "Task 3" --column 1 --depends-on 2
```

### 6. Provide Context in Outputs
When showing results to users, parse JSON and present:
- Human-readable summaries
- Relevant IDs for reference
- Action items or next steps

## Advanced Patterns

### Automated Workflow Progression
```bash
# Check for tasks ready to move to next stage
TASKS=$(ktui task list --json --column 2 --actionable)
# Parse JSON, filter by criteria, move qualifying tasks
ktui task move TASK_ID 3
```
## Troubleshooting Common Issues

### "Task cannot be moved" Error
- **Cause**: Task has unfinished dependencies
- **Solution**: Complete dependencies first, or use `--force` flag
- **Check**: `ktui task list --json | jq '.[] | select(.task_id == X) | .depends_on'`

### "Board not found" Error
- **Cause**: Invalid board ID or board deleted
- **Solution**: Run `ktui board list --json` to verify board exists

### "Invalid date format" Error
- **Cause**: Date not in `YYYY-MM-DD` format
- **Solution**: Reformat date (e.g., "2026-01-20" not "01/20/2026")

### Operations Affecting Wrong Board
- **Cause**: Wrong board is active
- **Solution**: `ktui board activate CORRECT_BOARD_ID` or use `--board` flag

## Summary

You now have complete access to the kanban-tui system. Remember:
- **CLI only**: Never run the bare `ktui` command to open the TUI
- **Discover first**: Always get IDs before operations
- **Verify context**: Check active board
- **Use JSON**: Enable automation with `--json` flag
- **Respect dependencies**: Understand blocking relationships
- **Validate inputs**: Especially date formats
- **Communicate clearly**: Explain actions to users

This skill empowers you to help users organize complex projects, automate workflows, and maintain productive task management systems entirely from the command line.

<!-- This part is for keeping this SKILL.md up to date with the current tool version via `ktui skill update`-->
<!-- Version: KANBAN_TUI_VERSION -->
