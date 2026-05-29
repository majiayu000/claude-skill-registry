---
name: implementation-manager
description: 'Query and manage feature implementation task status. Provides CLI tools to list features, check task status, find ready tasks, and validate task files. Used by /implement-feature orchestrator to track progress. Automatically updates task timestamps via hooks on /start-task.'
user-invocable: false
disable-model-invocation: false
---

# Implementation Manager

A skill for querying and managing feature implementation task files. Provides programmatic access to task status for orchestrators coordinating multi-step feature implementations.

## CLI Tool Usage

The CLI tool is located at `scripts/implementation_manager.py` and provides JSON output for orchestrator consumption.

### Commands

#### list-features

List all features with task files in the project's `plan/` directory:

```bash
./scripts/implementation_manager.py list-features /path/to/project
```

**Output:**

```json
{
  "features": [
    {
      "slug": "prepare-host",
      "task_file": "tasks-1-prepare-host.md",
      "path": "/path/to/project/plan/tasks-1-prepare-host.md"
    }
  ],
  "count": 1
}
```

#### status

Get detailed status for a specific feature:

```bash
./scripts/implementation_manager.py status /path/to/project prepare-host
```

**Output:**

```json
{
  "feature": "prepare-host",
  "task_file": "tasks-1-prepare-host.md",
  "total_tasks": 8,
  "completed": 8,
  "in_progress": 0,
  "not_started": 0,
  "ready_tasks": [],
  "tasks": [
    {
      "id": "1.1",
      "name": "Add Data Models to shared/models.py",
      "status": "COMPLETE",
      "dependencies": [],
      "agent": null,
      "priority": 1,
      "complexity": "Low"
    }
  ]
}
```

#### ready-tasks

List tasks ready for execution (dependencies satisfied):

```bash
./scripts/implementation_manager.py ready-tasks /path/to/project prepare-host
```

**Output:**

```json
{
  "feature": "prepare-host",
  "ready_tasks": [
    {
      "id": "1.3",
      "name": "Create core/prepare.py Business Logic",
      "agent": "python-cli-architect"
    }
  ],
  "count": 1
}
```

#### validate

Validate task file frontmatter and structure:

```bash
./scripts/implementation_manager.py validate /path/to/project prepare-host
```

**Output:**

```json
{
  "valid": true,
  "errors": [],
  "warnings": ["Task 1.3 missing Agent field"]
}
```

## Task File Format

The CLI parses task files with this format:

```markdown
## Task {ID}: {Name}

**Status**: NOT STARTED | IN PROGRESS | COMPLETE
**Dependencies**: Task 1, Task 2 | None
**Priority**: 1-5
**Complexity**: Low | Medium | High
**Agent**: agent-name
**Started**: {ISO timestamp} (optional, added by agent)
**Completed**: {ISO timestamp} (optional, added by hook)
**LastActivity**: {ISO timestamp} (optional, updated by hook)

**Acceptance Criteria**:
1. ...
```

### Status Values

- `NOT STARTED` (also matches emojis: `:x:`, `:cross_mark:`)
- `IN PROGRESS` (also matches emojis: `:arrows_counterclockwise:`)
- `COMPLETE` (also matches emojis: `:white_check_mark:`, `:heavy_check_mark:`)

### Dependency Resolution

A task is "ready" when:

1. Status is `NOT STARTED`
2. All dependencies are `COMPLETE` (or no dependencies)

## Hook Integration

The `task_status_hook.py` script provides automated task status tracking via Claude Code hooks.

### Hook Configuration

| Command              | Hook Event   | Matcher             | Purpose                                        |
| -------------------- | ------------ | ------------------- | ---------------------------------------------- |
| `/implement-feature` | SubagentStop | (all)               | Mark task COMPLETE, add Completed timestamp    |
| `/start-task`        | PostToolUse  | `Write\|Edit\|Bash` | Update LastActivity timestamp during execution |

### How It Works

**SubagentStop (Task Completion)**:

When `/implement-feature` launches a sub-agent via `/start-task {task_file} --task {id}`, the SubagentStop hook fires when the sub-agent completes. The hook script:

1. Parses the original prompt to extract task file path and task ID
2. Updates task status from `🔄 IN PROGRESS` to `✅ COMPLETE`
3. Adds `**Completed**: {ISO timestamp}` to the task section

**PostToolUse (Activity Tracking)**:

When `/start-task` runs, it creates a context file at `.claude/context/active-task-{session_id}.json` containing the task file path and task ID. On each Write, Edit, or Bash operation, the PostToolUse hook:

1. Reads the context file to identify the active task
2. Updates `**LastActivity**: {ISO timestamp}` in the task section

### Timestamp Field Responsibilities

| Field              | Added By                  | When                              |
| ------------------ | ------------------------- | --------------------------------- |
| `**Started**`      | Agent (via `/start-task`) | When agent begins work on task    |
| `**Completed**`    | Hook (SubagentStop)       | When sub-agent finishes           |
| `**LastActivity**` | Hook (PostToolUse)        | On each Write, Edit, or Bash call |

## Integration with /implement-feature

The `/implement-feature` orchestrator uses this skill to:

1. Query task file status via `implementation_manager.py status`
2. Find ready tasks via `implementation_manager.py ready-tasks`
3. Launch appropriate agents based on task's **Agent** field
4. Update timestamps via hook scripts when tasks start/complete
