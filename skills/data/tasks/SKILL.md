---
name: tasks
description: "Create, load, or summarize tasks via Graphiti MCP; triggers on 'tasks', 'list tasks', 'add task', usable by any model (Claude, Gemini)."
---

## Purpose
Model-neutral helper to add/list tasks in Graphiti MCP so any agent can keep a shared task board.

## Triggers
Use when the user says: "add a task", "list tasks", "load tasks", "task status".

## How to use
1) List: `lisa tasks list --cache [--group <id>] [--limit 20] [--all|--since today]`
2) Add: `lisa tasks add "<task text>" [--status todo|doing|done] [--tag foo] [--group <id>] --cache`
3) Defaults: reads ${GRAPHITI_ENDPOINT} from `.lisa/.env` (written by init); group ID is automatically derived from the project folder path. List defaults to `--since today` unless `--all` or `--since` is provided.
4) Cache fallback: writes/reads `cache/tasks.log` when `--cache` is passed, returning last cached result on MCP failure.
5) Keep prompts model-neutral; models only orchestrate CLI commands and summarize JSON output.

## I/O contract (examples)
- List: `{ status: "ok", action: "list", tasks: [...] }`
- Add: `{ status: "ok", action: "add", task: { text, status, group } }`
- Fallback: `{ status: "fallback", error, fallback: <cached object> }`

## Cross-model checklist
- Claude: concise instructions; avoid role tokens; keep outputs small.
- Gemini: explicit commands and minimal formatting.

## Notes
- All commands use the `lisa` CLI binary — no scripts to run directly.
- Tasks are stored via Graphiti MCP `add_task`/`list_tasks`.
