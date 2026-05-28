---
name: fusion-ui
description: Propose multiple UI component designs and select the best; use when exploring UI variants or visual direction.
---

# Fusion UI

## Overview

Use an F-thread: three workers propose UI variants in separate worktrees. The queen selects the best direction.

## Inputs

- UI goal and constraints

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

- Worker A: minimal and clean
- Worker B: bold and expressive
- Worker C: data-dense or enterprise

## Queen Prompt Outline

- Compare usability, consistency, and implementation cost

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Selected UI variant and implementation notes
