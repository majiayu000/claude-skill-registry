---
name: worktree
description: Use when managing git worktrees (list, create/switch, delete, configure) in this repo; prefer the git-wt subcommand for worktree operations and its configuration options.
---
# Worktree

## Overview

Use `git wt` as the default interface for git worktree tasks. It wraps `git worktree` to list, create, switch, and delete worktrees with safer defaults.

## Quick Start

```console
git wt                       # list worktrees
git wt <branch|worktree>     # switch/create (creates branch and worktree if needed)
git wt -d <branch|worktree>  # delete worktree and branch (safe)
git wt -D <branch|worktree>  # force delete worktree and branch
```

## Task Playbook

### List worktrees

Run `git wt` and parse the output. Use this to confirm names and paths before switching or deleting.

### Create or switch worktree

Prefer `git wt <branch|worktree>` for both actions. It will create the branch/worktree if missing, otherwise switch to it.

If staying in the current directory matters, use `--nocd`:

```console
git wt --nocd feature-branch
```

### Delete worktree

Use `git wt -d <branch|worktree>` for a safe delete. Only use `-D` if explicitly requested or when cleanup must be forced.

## Configuration Guidance

Use `git config` for defaults; override with flags when needed.

- `wt.basedir` / `--basedir`: set the worktree base directory (default is `../{gitroot}-wt`).
- `wt.copyignored` / `--copyignored`: copy gitignored files (for example, `.env`) when creating.
- `wt.copyuntracked` / `--copyuntracked`: copy untracked files on create.
- `wt.copymodified` / `--copymodified`: copy modified tracked files on create.
- `wt.nocopy` / `--nocopy`: exclude files from copying (gitignore syntax).
- `wt.copy` / `--copy`: always copy specific patterns even if ignored.
- `wt.hook` / `--hook`: run commands after creating a new worktree.
- `wt.nocd` / `--nocd`: prevent automatic directory switching.

## Shell Integration

When asked to enable shell integration, use the appropriate init command:

```powershell
Invoke-Expression (git wt --init powershell | Out-String)
```

Use `--nocd` with `--init` to enable completion without wrapping `git` when required.
