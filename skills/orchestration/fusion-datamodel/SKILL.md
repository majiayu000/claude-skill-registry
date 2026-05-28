---
name: fusion-datamodel
description: Compare data model designs and pick the best fit; use when modeling new data or refactoring schemas.
---

# Fusion Data Model

## Overview

Use an F-thread: three workers propose different data models. The queen evaluates tradeoffs.

## Inputs

- Entities, relationships, and access patterns

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

- Worker A: normalized relational model
- Worker B: denormalized or document model
- Worker C: hybrid or event-based model

## Queen Prompt Outline

- Compare performance, migration cost, and correctness

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Selected model with rationale and migration notes
