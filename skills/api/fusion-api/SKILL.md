---
name: fusion-api
description: Design and compare alternative API shapes; use when deciding on endpoints, request or response formats, or versioning.
---

# Fusion API

## Overview

Use an F-thread: three workers in separate worktrees propose competing API designs. The queen evaluates ergonomics and tradeoffs.

## Inputs

- API description and constraints

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

- Worker A: REST-first, simple endpoints
- Worker B: resource-oriented with versioning
- Worker C: alternative (GraphQL or RPC-style)

## Queen Prompt Outline

- Compare consistency, usability, versioning, and backward compatibility

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- API design comparison and chosen spec
