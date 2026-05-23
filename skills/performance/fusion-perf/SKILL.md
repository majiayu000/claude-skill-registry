---
name: fusion-perf
description: Compare performance optimization options and choose the most effective; use when tuning or speeding up a system.
---

# Fusion Performance

## Overview

Use an F-thread: three workers implement different optimizations in separate worktrees. The queen compares results.

## Inputs

- Performance problem and metrics

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

- Worker A: algorithmic improvements
- Worker B: caching or batching
- Worker C: concurrency or IO tuning

## Queen Prompt Outline

- Compare benchmarks, complexity, and regression risk

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Selected optimization strategy with benchmarks
