---
name: git-workspace
description: "Work with git worktrees and workspaces for concurrent development. Use when: (1) Creating new workspaces with \`git worktree add\`, (2) Listing existing worktrees with \`git worktree list\`, (3) Removing worktrees with \`git worktree remove\`, (4) Pruning stale worktree metadata with \`git worktree prune\`, (5) Managing multiple checked-out branches simultaneously, (6) Migrating uncommitted work between workspaces, or (7) Any git workspace/worktree operation. Requires Git 2.5+ for worktree support."
---

# Git Workspace Operations

Work with git worktrees to enable concurrent development across multiple branches without context switching or stashing conflicts.

## Prerequisites

- Git 2.5+ installed (worktree support introduced in 2.5)
- Working in a git repository
- Understanding of git branches and basic git operations

## Quick Start

**Create a new workspace:**
```bash
git worktree add -b <new-branch> <path> [<commit-ish>]
```

**List all worktrees:**
```bash
git worktree list
```

**Remove a worktree:**
```bash
git worktree remove <path>
```

## Core Operations

### Create Worktree

Create a new worktree (workspace) linked to the current repository:

```bash
# Create worktree with new branch
git worktree add -b <new-branch> <path> [<commit-ish>]

# Create worktree with existing branch
git worktree add <path> <branch-name>

# Create worktree at specific commit (detached HEAD)
git worktree add --detach <path> <commit-ish>
```

**Best practices:**
- Use relative paths outside current worktree (e.g., `../workspace-feature-x`)
- Branch name should be descriptive and match feature/task
- Default to creating new branch unless explicitly checking out existing branch

**Example:**
```bash
git worktree add -b feature-user-auth ../workspace-user-auth
```

### List Worktrees

List all worktrees associated with the repository:

```bash
# Basic list
git worktree list

# Verbose output (shows branch and commit)
git worktree list -v

# Machine-readable format (for scripting)
git worktree list --porcelain
```

**Output interpretation:**
- First line is main worktree (cannot be removed)
- Subsequent lines are linked worktrees
- Format: `<path> <commit> [<branch>]`

### Remove Worktree

Remove a worktree when done:

```bash
# Remove clean worktree (default - safe)
git worktree remove <path>

# Force remove unclean worktree (discards uncommitted changes)
git worktree remove --force <path>
```

**Safety considerations:**
- Default behavior only removes "clean" worktrees (no untracked files, no modified tracked files)
- Use `--force` only when intentionally discarding uncommitted work
- Main worktree cannot be removed
- Always verify worktree path before removal

**Example:**
```bash
git worktree remove ../workspace-feature-x
```

### Prune Stale Worktrees

Clean up administrative files from manually deleted worktrees:

```bash
# Dry run (see what would be pruned)
git worktree prune -n

# Prune stale worktrees
git worktree prune

# Prune with expiration (remove entries older than specified time)
git worktree prune --expire <time>
```

**When to use:**
- After manually deleting a worktree directory (outside of git commands)
- To clean up stale metadata in `.git/worktrees/`
- Regular maintenance to keep repository clean

## Common Patterns

### Concurrent Feature Development

Work on multiple features simultaneously:

```bash
# Main worktree: working on feature A
# Create new workspace for feature B
git worktree add -b feature-b ../workspace-feature-b

# Work in new workspace
cd ../workspace-feature-b
# ... make changes, commit ...

# Return to main worktree
cd ../devagent
# Continue working on feature A
```

### Emergency Fixes

Create temporary worktree for urgent fixes without disrupting main work:

```bash
# Create temporary worktree from main branch
git worktree add -b emergency-fix ../temp-fix main

# Make fix, commit
cd ../temp-fix
# ... fix bug ...
git commit -a -m "Emergency fix for production issue"

# Push and create PR
git push origin emergency-fix

# Clean up
cd ../devagent
git worktree remove ../temp-fix
```

### Migrating Uncommitted Work

Move uncommitted work to a new workspace:

```bash
# 1. Stash current work in main worktree
git stash push -m "Migrating to workspace feature-x"

# 2. Create new worktree
git worktree add -b feature-x ../workspace-feature-x

# 3. Apply stash in new worktree
cd ../workspace-feature-x
git stash pop

# 4. Verify work is in new worktree
git status

# Main worktree is now clean
cd ../devagent
git status  # Should show clean working tree
```

## Safety Considerations

### Worktree Limits

Git has limits on number of worktrees (typically 2-3 per repository, configurable). Check limits:

```bash
# Check current worktree count
git worktree list | wc -l

# If limit reached, remove unused worktrees before creating new ones
```

### Path Validation

- Always verify path doesn't already exist before creating worktree
- Use relative paths outside current worktree (recommended: `../workspace-<name>`)
- Avoid paths that conflict with existing directories

### Clean State Checks

Before removing worktrees:

```bash
# Check worktree status
git -C <worktree-path> status

# Only remove if clean, or use --force if intentionally discarding work
```

### Main Worktree Protection

- Main worktree (the one created by `git init` or `git clone`) cannot be removed
- Always verify you're not attempting to remove the main worktree
- Use `git worktree list` to identify which is the main worktree

## Error Handling

### Path Already Exists

If path already exists:
- Choose different path
- Or remove existing directory first (if safe)

### Branch Already Exists

If branch already exists:
- Use `-B` flag to force: `git worktree add -B <branch> <path>`
- Or choose different branch name
- Or checkout existing branch: `git worktree add <path> <existing-branch>`

### Worktree Limit Reached

If git reports worktree limit:
- Remove unused worktrees: `git worktree remove <unused-path>`
- Or increase limit in git config (advanced)

### Unclean Worktree Removal

If removal fails due to unclean state:
- Commit or discard changes in worktree
- Or use `--force` flag (discards uncommitted work)

## Integration Notes

- Worktrees share repository data (objects, refs) but have independent working directories
- Each worktree has its own index, HEAD, and config
- Changes in one worktree are immediately visible in others (same repository)
- Commits in any worktree update the shared repository

## Reference Documentation

- **Git Worktree Documentation**: [git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)
- **Research**: `.devagent/workspace/tasks/active/2026-01-14_git-workspace-setup-workflow/research/2026-01-14_workspace-best-practices-research.md` — Workspace best practices and patterns
