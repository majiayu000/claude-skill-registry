---
name: af
description: Agent Farm CLI quick reference. Use when running af commands to check correct syntax, subcommands, and flags. Prevents guessing at command names.
disable-model-invocation: false
---

# Agent Farm Quick Reference

## Tower (Dashboard Server)

```bash
af tower start             # Start Tower on port 4100
af tower stop              # Stop Tower
af tower log               # Tail Tower logs
af tower status            # Check if Tower is running
```

There is NO `af tower restart` — use `af tower stop && af tower start`.

## Dashboard

```bash
af dash start              # Start architect dashboard for current project
af dash stop               # Stop dashboard for current project
af dash open               # Open dashboard in browser
```

## Builder Management

```bash
af spawn -p 0003           # Spawn builder for spec (strict mode, default)
af spawn --soft -p 0003    # Spawn builder (soft mode)
af spawn --issue 42        # Spawn builder for a bugfix
af spawn -p 0003 --resume  # Resume builder in existing worktree
af status                  # Check all builder status
af cleanup --project 0003  # Clean up builder worktree (safe)
af cleanup --project 0003 -f  # Force cleanup
```

### Resuming Builders

When a builder's Claude process dies but the worktree and porch state survive,
use `--resume` to restart it without recreating the worktree:

```bash
af spawn -p 0003 --resume
```

This reuses the existing `.builders/0003` worktree, creates a fresh terminal
session registered with the Tower (so it appears in the dashboard), and lets
porch pick up from whatever phase the builder was in. Works with all spawn
modes: `-p`, `--issue`, `--task`, `--protocol`, `--worktree`.

## Utility

```bash
af util                    # Open utility shell
af open file.ts            # Open file in annotation viewer
af ports list              # List port allocations
af send <builder> "msg"    # Send message to a builder
```

## Configuration

Edit `af-config.json` at project root to customize shell commands.

```json
{
  "shell": {
    "architect": "claude",
    "builder": "claude",
    "shell": "bash"
  }
}
```

## Pre-Spawn Checklist

**Before `af spawn`, commit all local changes.** Builders work in git worktrees
branched from HEAD — uncommitted files (specs, plans, codev updates) are invisible
to the builder. The spawn command will refuse if the worktree is dirty (override
with `--force`).

## Common Mistakes

- **Spawning with uncommitted changes** — builder won't see specs, plans, or codev updates
- There is NO `codev tower` command — Tower is managed via `af tower`
- There is NO `restart` subcommand — stop then start
- There is NO `af start` for Tower — use `af tower start` or `af dash start`
