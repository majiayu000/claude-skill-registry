---
name: epic-cli
description: Use the Epic CLI for project management, issue tracking, PR workflows, git worktrees, and debugging. Triggers on requests like "create a project", "start an issue", "work on PR", "create worktree", or "add debug statements".
---

# Epic CLI

## Overview

Epic CLI is a project and issue management tool that integrates with GitHub. It handles project creation, issue tracking, PR workflows, git worktrees, and debugging utilities.

## Commands

### Project Management

Create new projects with GitHub repository:

```bash
epic project new my-awesome-project
epic project new org/repo-name
epic project new my-web-app --web    # Use web template
```

### Issue Management

| Command | Description |
|---------|-------------|
| `epic issue new "Title"` | Create new issue with title |
| `epic issue new` | Create new issue interactively |
| `epic issue new --no-sync` | Create local issue without GitHub sync |
| `epic issue list` | List all issues |
| `epic issue list open` | List open issues |
| `epic issue list closed` | List closed issues |
| `epic issue show <id>` | Show issue details |
| `epic issue get <id>` | Download issue from GitHub |
| `epic issue sync <file>` | Sync markdown file with GitHub issue |
| `epic issue start <id>` | Start working (creates worktree + tmux + claude) |
| `epic issue start <id> --no-switch` | Create session but don't switch to it |
| `epic issue start <id> --no-tmux` | Create worktree only (no tmux) |
| `epic issue start <id> --branch` | Create branch only (no worktree) |
| `epic issue assign <id> <user>` | Assign issue to user |
| `epic issue close <id>` | Close issue and delete local file |

Issue IDs can be: markdown file path, issue number, or prefix-number (e.g., `SCA-8`).

### PR Management

Start working on a pull request:

```bash
epic pr start 359            # Creates worktree + tmux session
epic pr start 359 --no-tmux  # Creates worktree only
```

### Worktree

Open a shell in a worktree directory:

```bash
epic worktree <branch-name>
```

### Ask (LLM Query)

Query an LLM for assistance:

```bash
epic ask "What is the purpose of git worktrees?"
epic ask "Explain async/await" --model gpt-4o
```

Available models: gpt-4.1 (default), gpt-4.1-mini, gpt-4.1-nano, gpt-4o, o1-mini, o1

### Debug

Add/remove debug statements and diagnostic tools:

```bash
epic debug add <function-name> <file-path>      # Add debug statement
epic debug remove <function-name> <file-path>   # Remove debug statement
epic debug remove-all                           # Remove all console.debug from project
epic debug check-gitignore                      # Check .gitignore for worktrees
epic debug check-gitignore --fix                # Fix .gitignore if needed
```

### Draft

Create draft files:

```bash
epic draft new
```

## Issue File Format

Issues are stored in `docs/issues/` with pattern `{prefix}-{number}-{slug}.md`. Contains:
- Title and GitHub issue number (if synced)
- Status
- Description
- Functional and Technical specifications
- Task checklist

## Common Workflows

**Start working on an issue:**
```bash
epic issue start SCA-8
```
This creates a worktree, tmux session, runs claude, and switches to the session.

**Create and sync a new issue:**
```bash
epic issue new "Add dark mode support"
```

**Review open issues:**
```bash
epic issue list open
```

**Work on a PR:**
```bash
epic pr start 359
```
