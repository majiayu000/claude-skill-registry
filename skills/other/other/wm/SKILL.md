---
name: wm-git-worktree-manager
description: Use when working with git worktrees - creating isolated workspaces for branches, managing multiple features in parallel, or cleaning up worktrees
---

# WM - Git Worktree Manager

CLI tool for easy git worktree management.

## IMPORTANT: Non-Interactive Mode Required

**Always use explicit arguments. Interactive mode does not work in automated environments.**

```bash
# CORRECT - explicit arguments
wm add feature-auth
wm remove feature-auth

# WRONG - interactive mode (will hang)
wm add      # NO!
wm remove   # NO!
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `wm init` | Initialize project config (.wm.yaml) |
| `wm add <branch>` | Create worktree for branch |
| `wm add <branch> -p <path>` | Create worktree at custom path |
| `wm list` | List all worktrees |
| `wm remove <branch>` | Remove worktree by branch name |
| `wm remove <path>` | Remove worktree by path |
| `wm remove -b <branch>` | Remove worktree AND delete branch |
| `wm remove -f <branch>` | Force remove (skip confirmation) |

## Common Patterns

### Create Worktree

```bash
# Basic usage
wm add feature-login

# With custom path
wm add feature-login -p ./workspaces/login

# Branch with slash becomes hyphenated folder
wm add feature/auth
# Creates: ../wm_repo/feature-auth/
```

### Remove Worktree

```bash
# By branch name
wm remove feature-auth

# By path
wm remove ../wm_repo/feature-auth

# Also delete the git branch
wm remove -b feature-auth

# Force (skip confirmation)
wm remove -f feature-auth
```

### List Worktrees

```bash
wm list
# or
wm ls
```

## Configuration (.wm.yaml)

```yaml
version: 1

worktree:
  base_dir: "../wm_{repo}"  # {repo} replaced with repo name

sync:
  - ".env"                  # Copy to worktree
  - "apps/*/.env"           # Glob supported
  - src: ".env.example"
    dst: ".env"
    mode: copy              # or "symlink"
    when: missing           # or "always"

tasks:
  post_install:
    mode: background        # Async execution
    commands:
      - "npm install"
```

## When to Use

- Working on multiple features in parallel
- Reviewing PRs while continuing other work
- Running long builds/tests on separate branch
- Quick branch switching without stash

## Common Mistakes

| Mistake | Solution |
|---------|----------|
| Using interactive mode | Always provide branch/path argument |
| Expecting nested folders for `feature/auth` | Creates `feature-auth` (flat) since v0.1.1 |
| Trying to remove main worktree | Not allowed - main worktree is protected |
| Branch used by another worktree | Warning shown, requires confirmation |
