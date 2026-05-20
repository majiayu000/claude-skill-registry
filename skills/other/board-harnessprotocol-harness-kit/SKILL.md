---
name: board
description: Use when the user invokes /board or wants to view, create, move, or manage tasks on the Harness Board.
---

# Harness Board

Use this skill when the user invokes `/board` or asks to manage tasks, create epics, move tasks, or check project status on the Harness Board.

## What is Harness Board?

A lightweight Kanban board with real-time two-way sync between Claude and a web UI. Tasks live in `~/.harness/board/projects/<slug>.yaml`. Claude interacts via MCP tools; humans interact via browser.

## MCP Tools Available

| Tool | Purpose |
|------|---------|
| `create_project` | Create a new project |
| `create_epic` | Create an epic under a project |
| `create_task` | Create a task under an epic |
| `update_task` | Edit title, description, flags |
| `move_task` | Change status column |
| `add_comment` | Post a comment as "claude" or "user" |
| `list_tasks` | Read board state (filterable) |
| `link_branch` | Associate branch/worktree with task |
| `link_commit` | Attach a commit SHA |
| `request_review` | Flag task ready for human review |
| `block_task` | Mark blocked with reason |
| `unblock_task` | Clear blocked status |

## Usage Patterns

### `/board` — Open the board UI
Open the board web UI (requires the board server to be running as a background service):
```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/start-board.sh
```
If the server is not running, the script prints instructions to install it as a persistent launchd service with `pnpm board:install`.

### `/board create <title>` — Create a task
1. Call `list_tasks` to find the active project and epic
2. Call `create_task` with the current project + epic
3. Confirm task ID and status to the user

### `/board status` — Show current board state
Call `list_tasks` and format a concise summary grouped by status.

### `/board move <task-id> <status>` — Move a task
Call `move_task` with the appropriate project, task_id, and status.

## Workflow Integration

When starting work on a task:
1. `move_task` → "in-progress"
2. `link_branch` with the worktree branch
3. Add progress comments via `add_comment` (author: "claude")
4. `request_review` when ready
5. `move_task` → "done" after merge

## Status Values

- `backlog` — not started
- `in-progress` — being worked on
- `review` — ready for human review
- `done` — complete
