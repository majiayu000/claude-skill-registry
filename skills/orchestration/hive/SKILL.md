---
name: hive
description: Orchestrate a multi-step workflow as coordinated sub-tasks; use when a task is large and benefits from structured coordination.
---

# Hive

## Overview

Use mprocs to run a queen plus workers in parallel with shared session state.

## Inputs

- Session name
- Worker count (default 4, max 5)
- Task description

## Workflow

1. Verify prerequisites:
   - `git --version`
   - `mprocs --version`
2. Parse session name and worker count.
3. Choose `GEMINI_MODEL`:
   - `gemini-3-flash-preview` for research and discovery
   - `gemini-3-pro-preview` for code generation or implementation
4. Run a lightweight pre-scan with Codex CLI (commands below).
5. Create `.hive/sessions/<session-id>` and write `tasks.json`.
6. Write `queen-prompt.md` and `worker-*.md` prompts.
7. Write `.hive/mprocs.yaml` and launch mprocs.

## Pre-scan Commands

```bash
codex exec -m gpt-5.2 -s read-only -c model_reasoning_effort="low" --skip-git-repo-check \
  "Scan this codebase and identify key entry points and core logic for: {TASK_DESC}. Return file paths with brief notes."

codex exec -m gpt-5.2 -s read-only -c model_reasoning_effort="low" --skip-git-repo-check \
  "Find high-coupling files, config files, and package definitions for: {TASK_DESC}. Return file paths with brief notes."
```

## tasks.json Template

```json
{
  "session": "{SESSION_ID}",
  "created": "{ISO_TIMESTAMP}",
  "status": "active",
  "session_status": "active",
  "task_description": "{TASK_DESC}",
  "workers": {WORKER_COUNT},
  "tasks": [],
  "synthesis": {
    "status": "pending",
    "result_file": "results.md"
  }
}
```

## mprocs.yaml Template

```yaml
procs:
  queen:
    cmd: ["claude", "--model", "opus", "--dangerously-skip-permissions", "Read .hive/sessions/{SESSION_ID}/queen-prompt.md"]
    cwd: "{PROJECT_ROOT_FORWARD}"
  worker-1:
    cmd: ["claude", "--model", "opus", "--dangerously-skip-permissions", "Read .hive/sessions/{SESSION_ID}/worker-1-prompt.md"]
    cwd: "{PROJECT_ROOT_FORWARD}"
  worker-2:
    cmd: ["powershell", "-NoProfile", "-Command", "gemini -m {GEMINI_MODEL} -y -i 'Read .hive/sessions/{SESSION_ID}/worker-2-prompt.md'"]
    cwd: "{PROJECT_ROOT_FORWARD}"
  worker-3:
    cmd: ["powershell", "-NoProfile", "-Command", "codex --dangerously-bypass-approvals-and-sandbox -m gpt-5.2 'Read .hive/sessions/{SESSION_ID}/worker-3-prompt.md'"]
    cwd: "{PROJECT_ROOT_FORWARD}"
```

## Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Session folder with prompts, tasks, and results
- Final synthesis in `.hive/sessions/<session-id>/results.md`
