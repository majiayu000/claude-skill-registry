---
name: fusion-algorithm
description: Compare multiple algorithm options and pick the best; use when choosing or optimizing an algorithm.
---

# Fusion Algorithm

## Overview

Use an F-thread: three workers in separate git worktrees plus a judge queen. Each worker implements the algorithm differently. The queen compares and selects a winner.

## Inputs

- Algorithm description

## Workflow

1. Verify `git` and `mprocs`.
2. Create session variables:
   - `SESSION_ID`, `BASE_BRANCH`, `PROJECT_ROOT`, `WORKTREE_ROOT`
3. Create `.hive/sessions/<session-id>` and `WORKTREE_ROOT`.
4. Create worktrees:

```bash
git worktree add "{WORKTREE_ROOT}/impl-a" -b fusion/{SESSION_ID}/impl-a
git worktree add "{WORKTREE_ROOT}/impl-b" -b fusion/{SESSION_ID}/impl-b
git worktree add "{WORKTREE_ROOT}/impl-c" -b fusion/{SESSION_ID}/impl-c
```

5. Write `tasks.json` and worker prompts.
6. Write `.hive/mprocs.yaml` and launch mprocs.

## tasks.json Template

```json
{
  "session": "{SESSION_ID}",
  "created": "{ISO_TIMESTAMP}",
  "status": "active",
  "thread_type": "F-Thread (Fusion)",
  "task_type": "fusion-algorithm",
  "algorithm": {"description": "{ALGO_DESC}"},
  "base_branch": "{BASE_BRANCH}",
  "worktrees": {
    "impl-a": {"path": "{WORKTREE_ROOT}/impl-a", "branch": "fusion/{SESSION_ID}/impl-a", "worker": "worker-a"},
    "impl-b": {"path": "{WORKTREE_ROOT}/impl-b", "branch": "fusion/{SESSION_ID}/impl-b", "worker": "worker-b"},
    "impl-c": {"path": "{WORKTREE_ROOT}/impl-c", "branch": "fusion/{SESSION_ID}/impl-c", "worker": "worker-c"}
  }
}
```

## Worker Prompt Outline

- Worker A: clean, readable implementation
- Worker B: alternative approach or data structure
- Worker C: performance-focused implementation

## Queen Prompt Outline

- Compare correctness, complexity, readability, and test results
- Pick a winner or merge best elements

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Three implementations in worktrees and a final evaluation
