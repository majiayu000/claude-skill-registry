---
name: tasks
description: "Create, load, or summarize tasks via Graphiti MCP; triggers on 'tasks', 'list tasks', 'add task', usable by any model (Claude, Gemini)."
---

## Purpose
Model-neutral helper to add/list tasks in Graphiti MCP so any agent can keep a shared task board.

## Triggers
Use when the user says: "add a task", "list tasks", "load tasks", "task status".

## How to use
1) List: `lisa tasks list --cache [--group <id>] [--limit 20]`
2) Add: `lisa tasks add "<task text>" [--status todo|doing|done] [--tag foo] [--group <id>] --cache`
3) Defaults: reads ${GRAPHITI_ENDPOINT} / ${GRAPHITI_GROUP_ID} from `.lisa/.env` (written by init); see root `AGENTS.md` for canonical defaults.
4) Cache fallback: writes/reads `cache/tasks.log` when `--cache` is passed, returning last cached result on MCP failure.
5) Keep prompts model-neutral; models only orchestrate script calls and summarize JSON output.

## I/O contract (examples)
- List: `{ status: "ok", action: "list", tasks: [...] }`
- Add: `{ status: "ok", action: "add", task: { text, status, group } }`
- Fallback: `{ status: "fallback", error, fallback: <cached object> }`

## Cross-model checklist
- Claude: concise instructions; avoid role tokens; keep outputs small.
- Gemini: explicit commands and minimal formatting.

## Notes
- Node.js script expects fetch (Node ≥18). Use `node --experimental-fetch` on older runtimes.
- Tasks are stored via Graphiti MCP `add_task`/`list_tasks` (tool names referenced in script). Adjust if server differs.
- Folder `.lisa/skills/tasks/` keeps this decoupled from model-specific bindings.
