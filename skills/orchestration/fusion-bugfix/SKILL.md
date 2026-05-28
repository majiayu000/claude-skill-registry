---
name: fusion-bugfix
description: Propose multiple bug-fix strategies and pick the safest; use when a bug has more than one viable fix.
---

# Fusion Bugfix

## Overview

Use an F-thread: three workers attempt different fixes in separate worktrees. The queen selects the safest fix.

## Inputs

- Bug description and repro steps

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

- Worker A: minimal change fix
- Worker B: structural fix
- Worker C: defensive fix with tests

## Queen Prompt Outline

- Compare risk, scope, test coverage, and maintainability

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Selected fix and rationale
