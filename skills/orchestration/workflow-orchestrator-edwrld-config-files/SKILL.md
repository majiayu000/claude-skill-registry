---
name: workflow-orchestrator
description: Orchestrate multiple Codex CLI workflows using done-signal files, optional locks, and simple dependencies.
metadata:
  short-description: Orchestrate CLI workflows with done signals
---

# Workflow Orchestrator

Use this skill when the user wants multiple CLI workflows to coordinate via done-signal files, optionally with file locks.

## Core behavior

- Ask the user for a done-signal file naming scheme (default suggestion: `/tmp/workflow-<name>.done`).
- Ask the user whether any shared resources need locks (files, migration runner, build outputs). If yes, ask for lock file paths.
- Express dependencies by listing each workflow's `--wait-for` done files (one per dependency).
- Warn if a done file already exists from a prior run; recommend deleting it or using a run-specific name.

## Scripts

Use `scripts/run-workflow.sh` to run a workflow with dependencies and optional locking.

### Usage

```
run-workflow.sh \
  --wait-for /tmp/workflow-A.done \
  --done-file /tmp/workflow-B.done \
  --lock /tmp/workflow-shared.lock \
  -- ./your-workflow-command --with args
```

- `--wait-for` can be repeated for multiple dependencies.
- `--done-file` is touched only if the workflow exits successfully.
- `--lock` is optional; if provided, the script uses `flock` when available, otherwise a lock directory.

## Recommended dependency pattern

Use sentinel files as dependency edges:

- Workflow A: `--done-file /tmp/workflow-A.done`
- Workflow B: `--wait-for /tmp/workflow-A.done --done-file /tmp/workflow-B.done`
- Workflow C: `--wait-for /tmp/workflow-B.done`

If the user wants more structure, propose a small text config where each workflow lists its `done` and `wait_for` files, then translate it into the script calls.
