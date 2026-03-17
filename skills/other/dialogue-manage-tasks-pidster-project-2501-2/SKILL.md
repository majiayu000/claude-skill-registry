---
name: dialogue-manage-tasks
description: Always use this skill to manage tasks in .dialogue/tasks/. Each task is a separate YAML file for merge-friendly multi-user workflows. Triggers on "create task", "new task", "next task", "update task", "list tasks", "tasks", "active tasks", "task status", "status", "show status", "what's in progress", "what tasks", "pending tasks", "current tasks".
---

# Skill: Manage Tasks

Manage persistent tasks in `.dialogue/tasks/`. Each task is stored as a separate YAML file (e.g., `FW-008.yaml`) for merge-friendly multi-user workflows.

## Schema

See [schema.md](./schema.md) for the complete task schema definition.

## When to Use

- Creating new tasks
- Updating task status
- Listing or filtering tasks
- Archiving completed items
- Adding notes to existing items

## When NOT to Use

- Session-level task tracking → use TodoWrite tool directly
- One-off tasks that don't need cross-session persistence

## Approach

Task management is an **editing problem**, not a scripting problem:

1. List tasks: `ls ${CLAUDE_PROJECT_DIR}/.dialogue/tasks/`
2. Read specific task: `${CLAUDE_PROJECT_DIR}/.dialogue/tasks/{ID}.yaml`
3. Consult [schema.md](./schema.md) for field definitions
4. Edit using the Edit tool (or Write for new tasks)
5. Validate changes match schema

## Quick Reference

### Required Fields

| Field | Pattern | Example |
|-------|---------|---------|
| `id` | `[A-Z]{2,4}-[0-9]{3}` | `FW-006` |
| `title` | Non-empty string | `task Management` |
| `status` | Enum | `READY` |
| `created` | ISO 8601 | `2026-01-14T17:30:00Z` |

### Status Values

`BACKLOG` → `READY` → `IN_PROGRESS` → `COMPLETED`

Also: `BLOCKED`, `CANCELLED`

### Standard Prefixes

| Prefix | Purpose |
|--------|---------|
| `SH` | Self-Hosting |
| `CD` | Conceptual Debt |
| `FW` | Framework |
| `DOC` | Documentation |
| `VAL` | Validation |

## Utility Scripts

The `scripts/` directory contains utility scripts for common operations:

### list-tasks.sh

List tasks with filtering and sorting options.

```bash
# List all active tasks (excludes COMPLETED/CANCELLED by default)
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh

# List in-progress tasks only
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --active

# List ready tasks only
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --ready

# Filter by type
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --type CAPABILITY

# Filter by priority
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --priority HIGH

# Filter by prefix
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --prefix FW

# Sort by priority
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --sort priority

# Include completed/cancelled tasks
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --all

# Output formats: table (default), brief, json
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --format json

# JSON output includes: id, status, type, priority, title, created, updated, blocked_by, blocks
# Use with jq for advanced queries:

# List by priority with dependencies
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --format json --sort priority | jq -r '
  ["ID", "PRIORITY", "STATUS", "BLOCKED_BY", "BLOCKS"],
  (.[] | [.id, .priority, .status, (.blocked_by | join(",")), (.blocks | join(","))]) | @tsv
' | column -t

# Find blocked tasks
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --format json | jq '.[] | select(.blocked_by | length > 0)'

# Find tasks blocking others
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/list-tasks.sh --format json | jq '.[] | select(.blocks | length > 0)'
```

### count-tasks.sh

Count tasks with optional grouping.

```bash
# Total count (active tasks)
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/count-tasks.sh

# Count by status
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/count-tasks.sh --by status

# Count by type
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/count-tasks.sh --by type

# Count by priority
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/count-tasks.sh --by priority

# Count by prefix
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/count-tasks.sh --by prefix

# Count only READY tasks by type
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/count-tasks.sh --status READY --by type

# JSON output
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/count-tasks.sh --by status --format json
```

### create-task.sh

Create a new task with auto-generated ID.

```bash
# Minimal: creates BACKLOG task with MEDIUM priority
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/create-task.sh FW "New feature implementation"

# With options
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/create-task.sh FW "Implement caching" \
  --status READY \
  --type CAPABILITY \
  --priority HIGH \
  --description "Add caching layer to improve performance" \
  --objective "Response times under 100ms" \
  --rationale "Current response times are 500ms+"

# With dependencies
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/create-task.sh FW "Deploy to production" \
  --blocked-by "FW-015,FW-016" \
  --status BLOCKED

# Use specific ID
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/create-task.sh FW "Specific task" --id FW-099
```

**Output**: Prints the created task ID (e.g., `FW-018`)

### next-id.sh

Get the next available ID for a prefix.

```bash
# Returns next available ID (e.g., FW-018)
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/next-id.sh FW

# Works with any valid prefix
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/next-id.sh SH
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/next-id.sh DOC
```

### task-summary.sh

Present a task status summary with counts and highlights.

```bash
# Show summary (table format)
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/task-summary.sh

# JSON output
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-manage-tasks/scripts/task-summary.sh --format json
```

**Output includes:**
- Counts by status (in-progress, ready, blocked, backlog, completed, cancelled)
- Active and total counts
- List of in-progress tasks with titles
- High-priority ready tasks (HIGH/CRITICAL)
- Blocked tasks

---

## Manual Operations

For operations not covered by scripts, edit task files directly:

### Update Status

1. Edit the task file: `.dialogue/tasks/{ID}.yaml`
2. Change `status` field
3. Update `updated` timestamp
4. If completing: add `completed` timestamp
5. Append to `notes` with context

### Add Notes

```yaml
notes: |
  Previous notes...

  Progress 14 January 2026:
  - What was done
  - What was decided
```

## Relationship to TodoWrite

| Aspect | TodoWrite | Task Files |
|--------|-----------|------------|
| Scope | Session | Cross-session |
| Storage | In-memory | `.dialogue/tasks/*.yaml` |
| Use case | "Do X, Y, Z now" | "FW-006 tracks this feature" |

## TMS Alignment

Tasks externalise directory knowledge, allocation, and history—enabling AI to "rejoin" ongoing work across sessions.

## Multi-User Workflow

Each task is a separate file, enabling:
- Independent changes to different tasks
- Clean git merges when users work on different tasks
- Conflict isolation to single-task scope

## Sharing

**Always commit and push immediately after creating or updating a task.** This ensures team visibility and prevents conflicts from concurrent work on the same task.

```bash
git add .dialogue/tasks/<ID>.yaml && git commit -m "<ID>: <brief description>" && git push
```
