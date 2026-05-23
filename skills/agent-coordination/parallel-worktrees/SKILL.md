---
name: parallel-worktrees
description: Parallel git worktrees for concurrent Claude Code sessions. Use when working on multiple features or writer/reviewer workflows.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
triggers:
  files: []
  keywords:
    - worktree
    - parallel
    - concurrent
    - writer
    - reviewer
    - multi-session
    - productivity
auto_suggest: true
---

# Parallel Worktrees

This skill provides guidance for running multiple Claude Code sessions concurrently using git worktrees.

See ../../rules/12-context-management.md for detailed documentation.

## Quick Reference

### Setup

```bash
git worktree add ../feature-name feature/branch-name
cd ../feature-name && claude
```

### Writer/Reviewer Pattern

| Terminal | Role | Command |
|----------|------|---------|
| Terminal 1 | Writer | `cd ../feature-auth && claude "Implement feature"` |
| Terminal 2 | Reviewer | `cd ../review-auth && claude "Review the code"` |

### Best Practices

- 3-5 worktrees maximum
- One worktree = one task
- Remove completed worktrees
- Never share sessions between worktrees
