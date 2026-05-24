---
name: parallelizing-with-worktrees
description: "Create and manage Git worktrees to parallelize agent tasks safely. Use when you need multiple concurrent checkouts (sub-agents, parallel edits, or isolated experiments) and want deterministic setup/cleanup with manifests and logs."
---

# Parallelizing With Worktrees

## Overview
Create isolated worktrees per task so parallel agents can edit, test, and commit without colliding. Use the scripts to generate a manifest, inspect status, and clean up deterministically.

## Quick start
1) Write a task list file (one task per line, optional `task:branch`).
2) Run `scripts/create_worktrees.py` to create worktrees and a manifest.
3) Dispatch sub-agents to the worktree paths in the manifest.
4) Use `scripts/status_worktrees.py` to inspect state.
5) Use `scripts/cleanup_worktrees.py` to remove worktrees when done.

## Core Guidance
- Confirm with the user before creating or removing worktrees (filesystem changes).
- Keep worktrees outside the repo root to avoid nesting; default root is `../<repo>-worktrees/<run-id>`.
- Prefer `mode=branch` for real edits; use `mode=detach` for read-only or analysis-only sub-agents.
- Log actions to `progress.log` (JSONL) in the repo root for resumability.
- Keep the manifest; it is the single source of truth for cleanup.

## Resources
- `scripts/create_worktrees.py`: Create worktrees from a task list and write `manifest.json`.
- `scripts/status_worktrees.py`: List worktrees (human text or JSON).
- `scripts/cleanup_worktrees.py`: Remove worktrees using the manifest; optionally delete branches and prune.

## Examples
Create worktrees from a task list:

```text
python -c "from pathlib import Path; Path('tasks.txt').write_text('api-auth\\nui-refresh:feature/ui-refresh\\ndocs\\n')"

python skills/parallelizing-with-worktrees/scripts/create_worktrees.py --tasks-file tasks.txt --run-id run-001
```

Inspect worktree status:

```text
python skills/parallelizing-with-worktrees/scripts/status_worktrees.py
```

Cleanup:

```text
python skills/parallelizing-with-worktrees/scripts/cleanup_worktrees.py --manifest ../<repo-name>-worktrees/run-001/manifest.json --delete-branches --prune
```

## Validation
- Create a throwaway branch and two dummy tasks; verify worktrees are created and listed.
- Remove worktrees with `scripts/cleanup_worktrees.py` and confirm `git worktree list` is clean.
