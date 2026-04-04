---
name: codex-taskloop-plugin
description: Run in-session task loops via the codex-taskloop-plugin MCP server and stop hook.
metadata:
  short-description: Taskloop MCP usage
---

# Codex Taskloop Plugin

## When to use

Use this skill when a user asks to start, continue, list, rename, resume, or delete
Taskloop tasks inside a single Codex session.

## Preconditions

- The codex-taskloop-plugin MCP server is registered.
- The codex-taskloop-plugin stop hook is installed.

If not installed:
- Project scope: `scripts/install.sh --scope project --project "<path>"`
- User scope: `scripts/install.sh --scope user`

## Core workflow

1) Start a loop with the MCP tool `task_loop` and a clear prompt.
2) Use `completion_promise` so the loop stops when the assistant outputs
   `<promise>...</promise>`.
3) Control tasks with `task_list`, `task_resume`, `task_rename`, and `task_delete`.
4) Storage:
   - Project install enforces project-only storage.
   - User install allows `project` or `user` per tool call.

## Tool quick reference

- `task_loop`: prompt (required), task_name, max_iterations, completion_promise,
  completion_matcher, history_limit, storage, project_dir
- `task_list`: storage, project_dir, limit, offset
- `task_resume`: task_name, storage, project_dir
- `task_rename`: task_name, new_name, storage, project_dir
- `task_delete`: task_name, storage, project_dir

## Conventions

- Use a short, meaningful task_name or let it auto-generate from the first line.
- Put the promise text inside `<promise>...</promise>` exactly when done.
