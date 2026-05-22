---
name: git-worktrees
description: Work on multiple branches in parallel using git worktrees via the git-wt helper to avoid context switching or merge noise.
trigger: always_on
---
This skill follows `engineering-doctrine`.

## Core Model

- One branch == one directory == one line of work
- All worktrees share a single `.git` database
- Each worktree is bound to its branch while it exists

## Preferred Tooling

Use `git wt` (https://github.com/k1LoW/git-wt) as the default interface. It wraps `git worktree` with safer defaults and faster workflows.

## Standard Setup

Optional, if you want worktrees stored in `.worktrees`:

```sh
mkdir -p .worktrees
git config wt.basedir .worktrees
```

## Quick Start

```sh
git wt                       # list worktrees
git wt <branch|worktree>     # switch/create (creates branch and worktree if needed)
git wt --nocd <branch|worktree>
git wt -d <branch|worktree>  # safe delete (worktree + branch)
git wt -D <branch|worktree>  # force delete
```

## Configuration

Use `git config` for defaults; override with flags when needed.

- `wt.basedir` / `--basedir`: base directory for worktrees (default `../{gitroot}-wt`)
- `wt.copyignored` / `--copyignored`: copy gitignored files on create
- `wt.copyuntracked` / `--copyuntracked`: copy untracked files on create
- `wt.copymodified` / `--copymodified`: copy modified tracked files on create
- `wt.nocopy` / `--nocopy`: exclude files from copying (gitignore syntax)
- `wt.copy` / `--copy`: always copy specific patterns even if ignored
- `wt.hook` / `--hook`: run commands after creating a new worktree
- `wt.nocd` / `--nocd`: prevent automatic directory switching

## Shell Integration (PowerShell)

```powershell
Invoke-Expression (git wt --init powershell | Out-String)
```

## Cleanup
always check if there are uncommitted changes in a worktree before
- removing its branch
- deleting the local worktree folder

Use `git wt -d <branch|worktree>` for clean removals.
If a worktree folder was deleted manually, run `git worktree prune`.
Ask user what to do with those uncommitted changes.

