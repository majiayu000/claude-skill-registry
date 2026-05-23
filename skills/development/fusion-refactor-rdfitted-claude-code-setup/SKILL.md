---
name: fusion-refactor
description: Compare refactoring approaches and pick the safest path; use when multiple refactor strategies are possible.
---

# Fusion Refactor

## Overview

Use an F-thread: three workers propose different refactor strategies in separate worktrees. The queen selects the safest path.

## Inputs

- Refactor goal and constraints

## Workflow

1. Verify `git` and `mprocs`.
2. Create session variables and worktrees.
3. Write `tasks.json`, worker prompts, and queen prompt.
4. Launch mprocs.

## Worktree Commands

```bash
git worktree add "{WORKTREE_ROOT}/impl-a" -b fusion/{SESSION_ID}/impl-a
git worktree add "{WORKTREE_ROOT}/impl-b" -b fusion/{SESSION_ID}/impl-b
git worktree add "{WORKTREE_ROOT}/impl-c" -b fusion/{SESSION_ID}/impl-c
```

## Worker Prompt Outline

- Worker A: incremental refactor
- Worker B: module-by-module
- Worker C: larger rewrite with safeguards

## Queen Prompt Outline

- Compare risk, test impact, and migration cost

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Selected refactor strategy and staged plan
