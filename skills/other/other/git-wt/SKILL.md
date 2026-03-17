---
name: git-wt
description: Git worktree workflow management using bare repository pattern. Use when working with multiple git branches simultaneously, managing AI agent worktrees, or setting up isolated development environments. Handles cloning, migration, creation, switching, and cleanup of worktrees with automatic upstream tracking.
---

# Git Worktree Workflow (git-wt)

## Overview

This skill provides a streamlined Git workflow using the **bare repository pattern** with the `git-wt` tool. Instead of stashing and switching branches, worktrees allow multiple branches to coexist simultaneously in separate directories while sharing a single git history.

**Key Benefits:**
- No more `git stash` context switching
- Parallel development on multiple features
- Isolated environments for AI agents
- Clean, organized workspace with branches as directories

## Quick Start

### Installation

The skill includes the `git-wt` script. Install it to your PATH:

```bash
# Copy to a directory in your PATH
cp /Users/mac/.claude/skills/git-wt/scripts/git-wt ~/.local/bin/
chmod +x ~/.local/bin/git-wt

# Or use the install helper
bash /Users/mac/.claude/skills/git-wt/scripts/install.sh
```

**Requirements:**
- Git 2.7+
- fzf (optional, for interactive commands)

### Clone a New Repository

```bash
git wt clone https://github.com/user/repo.git
cd repo/main
```

This creates the bare structure:
```
repo/
├── .bare/          # All git data
├── .git            # Pointer to .bare
└── main/           # Worktree for main branch
```

### Migrate Existing Repository

```bash
cd existing-repo
git wt migrate
```

## Daily Workflow

### Create a Worktree

**Interactive mode** (with fzf):
```bash
git wt add
```

**Direct mode**:
```bash
# From remote branch
git wt add feature-auth origin/feature-auth

# Create new branch
git wt add -b my-feature my-feature
```

### Switch Between Worktrees

```bash
# Interactive picker
cd $(git wt switch)

# Or add a shell function to .bashrc/.zshrc:
wt() {
    local dir
    dir=$(git wt switch)
    [[ -n "$dir" ]] && cd "$dir"
}
```

### Remove Worktrees

```bash
# Remove worktree and local branch
git wt remove feature-branch

# Remove worktree, local AND remote branch (destructive)
git wt destroy old-experiment

# Dry run to preview what would be removed
git wt remove --dry-run
```

### Update Repository

```bash
# Fetch all remotes and fast-forward default branch
git wt update
```

## Commands Reference

See [references/commands.md](references/commands.md) for detailed command documentation.

| Command | Description |
|---------|-------------|
| `git wt clone <url>` | Clone with bare structure |
| `git wt migrate` | Convert existing repo to worktree |
| `git wt add [options]` | Create worktree (interactive or direct) |
| `git wt remove [name]` | Remove worktree and local branch |
| `git wt destroy [name]` | Remove worktree + local + remote branch |
| `git wt switch` | Interactive worktree picker |
| `git wt update` / `u` | Fetch all and update default branch |
| `git wt list` | List all worktrees |

## Best Practices

1. **Keep `main/` pristine** - Never work directly in it. Use as clean reference for diffing.
2. **Name worktrees after branches** - Directory = branch = no confusion.
3. **Limit active worktrees** - 2-3 is ideal. Each is a full checkout.
4. **Project-level config** - Store `.claude/`, `.cursor/`, `.env` at project root (outside worktrees).

## AI Agent Workflow

Worktrees are ideal for AI coding agents:

```bash
# You're working on feature-A
cd ~/project/feature-A

# Spin up worktree for agent
git wt add -b agent-refactor ../agent-refactor

# Agent works independently
# You keep working uninterrupted

# Review agent's work
git diff main...agent-refactor
```

## The Bare Repo Pattern

See [references/bare-repo-pattern.md](references/bare-repo-pattern.md) for detailed explanation.

**Structure:**
```
my-project/
├── .bare/            # All git data (bare repository)
├── .git              # File pointing to .bare
├── main/             # Worktree: main branch
└── feature/          # Worktree: feature branch
```

**Why it works:**
- Single `.bare/` directory for all git data
- Worktrees are subdirectories (organized)
- Delete the folder = everything gone (no orphans)
- Project-level configs outside version control

## Troubleshooting

**"git wt: command not found"**
- Ensure `git-wt` is in your PATH
- Try: `~/.local/bin/git-wt --help`

**Worktree already exists**
- Use `git wt remove <name>` first
- Or choose a different name

**No upstream configured**
- `git wt add` sets upstream automatically
- Manual fix: `git branch --set-upstream-to=origin/<branch>`

## Resources

- [Bare Repo Pattern](references/bare-repo-pattern.md) - Detailed pattern explanation
- [Commands Reference](references/commands.md) - Full command documentation
- [Original Tool](https://github.com/ahmedelgabri/git-wt) - GitHub repository
