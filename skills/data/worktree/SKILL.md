---
name: worktree
description: Manage git worktrees for parallel feature development. Use when user mentions worktree, wants to work on multiple branches simultaneously, or runs /worktree. Supports task-aware naming (phase-XX/task-YY-description).
allowed-tools: Bash, AskUserQuestion
---

# Git Worktree Manager

Manage git worktrees for parallel feature development.

## Current Worktrees

!git worktree list

## Usage

```
/worktree                     # List worktrees (default)
/worktree add <name> [base]   # Create new worktree
/worktree remove <name>       # Remove worktree
/worktree status              # Detailed status of all worktrees
```

## Arguments

- `$1` - Subcommand: `add`, `list`, `remove`, `status` (default: `list`)
- `$2` - For `add`: feature/branch name; For `remove`: worktree name/path
- `$3` - For `add`: base branch (default: main/master)

---

## Command: `add`

Create a new worktree in a sibling directory.

**Task-Aware Naming**: When name matches `task-XX`:
1. Detect current phase from `specification/`
2. Generate branch: `phase-XX/task-YY-description`
3. Ask for description if not provided

**Examples**:
- `/worktree add task-02` → `phase-01/task-02-shared-kernel`
- `/worktree add feature-auth` → `feature-auth` (non-task)

**Process**:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")
WORKTREE_PATH="${REPO_ROOT}/../${REPO_NAME}-<branch-name>"
git worktree add -b <branch-name> "$WORKTREE_PATH" <base-branch>
```

---

## Command: `list`

List all worktrees with their details.

```bash
git worktree list
```

---

## Command: `remove`

Remove a worktree safely.

**Process**:
1. If no argument, list worktrees and ask which to remove
2. Check for uncommitted changes
3. If changes exist, WARN and ask for confirmation
4. Remove worktree and prune

```bash
git -C "<worktree-path>" status --porcelain
git worktree remove "<worktree-path>"
git worktree prune
```

---

## Command: `status`

Show detailed status of all worktrees.

For each worktree, show:
- Path and branch name
- Uncommitted changes (if any)
- Last commit info

```bash
git -C "<path>" status --short
git -C "<path>" log --oneline -1
```

---

## Interactive Mode

When `/worktree` is called without arguments or unclear input:
1. Show current worktrees
2. Ask what user wants to do (create, remove, view status)

## Safety Rules

1. NEVER remove the main worktree
2. ALWAYS check for uncommitted changes before removal
3. ALWAYS confirm destructive operations with user
4. Use `git worktree prune` after removals

## Finishing Work in Worktree

When done working in a worktree, use `/finish-task` to:
1. Squash merge all commits to main (in main repo)
2. Optionally remove the worktree directory

The `/finish-task` skill auto-detects WORKTREE mode and handles the merge correctly.
