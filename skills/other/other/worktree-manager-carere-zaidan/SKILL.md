---
name: worktree-manager
description: Manages the full lifecycle of git worktrees — create, list, update, and remove. Handles environment setup (.env), dependency installation (bun install), and port allocation using setup-dev-env script. Use when the user wants to create a worktree, list worktrees, update a worktree, remove a worktree, or set up a parallel development environment.
---

# Worktree Manager

Complete git worktree lifecycle management for parallel development environments with isolated dependencies and configuration.

## When to use this skill

Use this skill when the user wants to:
- **Create** a new worktree for parallel development
- **List** all worktrees and their status
- **Update** an existing worktree (pull changes, reinstall deps)
- **Remove** an existing worktree and clean up

**Do NOT use this skill when:**
- User wants to manually run git commands directly
- The task is unrelated to worktree management
- User just wants to switch branches (use `git checkout` instead)

## Operations Overview

| Operation | When to Use |
|-----------|-------------|
| **Create** | User wants a new parallel development environment |
| **List** | User wants to see existing worktrees and their status |
| **Update** | User wants to refresh a worktree (pull, reinstall deps) |
| **Remove** | User wants to delete a worktree and clean up |

## Decision Tree

### 1. User wants to CREATE a worktree
**Keywords:** create, new, setup, make, start, initialize, add
**Action:** Follow the [CREATE operation](OPERATIONS.md#create)

### 2. User wants to LIST worktrees
**Keywords:** list, show, display, what, which, status, check, view
**Action:** Follow the [LIST operation](OPERATIONS.md#list)

### 3. User wants to UPDATE a worktree
**Keywords:** update, refresh, pull, sync, reinstall, rebuild
**Action:** Follow the [UPDATE operation](OPERATIONS.md#update)

### 4. User wants to REMOVE a worktree
**Keywords:** remove, delete, cleanup, destroy, stop, kill, terminate
**Action:** Follow the [REMOVE operation](OPERATIONS.md#remove)

## Quick Start

For step-by-step operation instructions, see [OPERATIONS.md](OPERATIONS.md).

For concrete usage examples, see [EXAMPLES.md](EXAMPLES.md).

For troubleshooting common issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Important Notes

### Directory Convention
All worktrees are created under `trees/` at the project root:
```
project/
└── trees/
    ├── feature-auth/
    ├── fix-bug-123/
    └── refactor-api/
```

### Environment Setup
- The `.env` file from the main project is copied into the worktree
- The bundled [scripts/setup-dev-env.ts](scripts/setup-dev-env.ts) script is used to allocate free ports
- It resolves `.env` from `process.cwd()`, so always `cd` into the worktree before running it
- The `--env-key` flag writes a free port value directly to the worktree `.env`
- `bun install` is run after creation to install dependencies

### Do NOT attempt to:
- Create worktrees manually outside the `trees/` directory
- Skip `bun install` after creating a worktree
- Remove worktree directories with `rm -rf` (use `git worktree remove`)
- Manually edit ports when setup-dev-env is available
