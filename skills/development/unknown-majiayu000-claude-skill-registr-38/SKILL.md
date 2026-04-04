---
name: worktree-tending
description: Manage git worktrees for parallel branch development using custom git scripts (git-newtree, git-killtree, git-maingulp). Use when creating new worktrees, listing active worktrees, or closing/merging worktrees back to main. All worktrees are stored in .tree/ subdirectories of the repository.
---

# Worktree Tending

## Overview

This skill helps manage git worktrees using a customized workflow with scripts stored in `~/bin/`. Worktrees enable working on multiple branches simultaneously by creating separate working directories that share the same git repository. All worktrees are stored in `.tree/` subdirectories.

## Core Workflow

The typical worktree lifecycle:

1. **Create** a new worktree for a branch using `git newtree`
2. **Work** in that worktree (user navigates manually)
3. **Close** the worktree when done, optionally merging back to main

## Important: Always Display Worktrees

**CRITICAL INSTRUCTION:** After completing any worktree operation (create, merge, delete, archive), you MUST always run `git worktree list` and display the current state of all worktrees before yielding control back to the user.

This helps the user maintain awareness of their worktree state and verify that operations completed successfully.

**Example output format:**
```
**Current worktrees (N total):**

- `/path/to/repo` - detached HEAD (commit-hash)
- `/path/to/repo.bare` - detached HEAD (commit-hash)
- `feature-name` - branch: feature-name
- `maincomp` - branch: main
```

## Available Operations

### Creating a New Worktree

To create a new worktree for a branch:

```bash
git newtree <tree-name> [branch-name]
```

**Behavior:**
- Creates worktree at `.tree/<tree-name>`
- If branch exists, checks it out; otherwise creates new branch
- Branch name defaults to tree-name if not specified
- Copies `.env`, `.envrc`, and `.claude/` to the new worktree if present
- Reports the path for manual navigation

**Examples:**
```bash
git newtree feature-x              # Creates .tree/feature-x with branch 'feature-x'
git newtree fix check/lint-graphql # Creates .tree/fix with existing branch 'check/lint-graphql'
```

**When to use:** User asks to create a new worktree, start work on a new branch, or work on a branch in parallel.

### Listing Active Worktrees

To show all active worktrees with status:

```bash
git worktree list
```

**Output format:**
```
/path/to/repo                      commit-hash (detached HEAD)
/path/to/repo/.tree/feature-x      commit-hash [feature-x]
/path/to/repo/.tree/maincomp       commit-hash [main]
```

**Interactive selection with fzf:** When closing or switching worktrees, use fzf for interactive selection of worktrees from the list.

**When to use:** User asks to see active worktrees, list branches being worked on, or needs to select a worktree to close.

### Closing a Worktree

When closing a worktree, **always ask the user** whether to merge back to main or just remove the worktree.

#### Option 1: Merge to Main and Cleanup

Use `git maingulp` to merge changes back to main and cleanup:

```bash
cd .tree/maincomp  # or wherever main branch worktree is
git maingulp <branch-name> <worktree-path>
```

**Requirements:**
- Must be run from the main branch worktree
- Performs fast-forward merge (rebases main onto branch)
- Pushes main to remote
- Removes worktree and deletes branch

**Example:**
```bash
cd .tree/maincomp
git maingulp feature-x .tree/feature-x
```

**When to use:** Work is complete and ready to be merged into main.

#### Option 2: Just Remove Worktree

Use `git killtree` to remove worktree without merging:

```bash
git killtree <worktree-path> [--force]
```

**Behavior:**
- Removes worktree at specified path
- Deletes branch only if fully merged (unless --force)
- Use --force to remove dirty worktree and force-delete unmerged branch

**Examples:**
```bash
git killtree .tree/feature-x          # Remove worktree, delete if merged
git killtree .tree/experiment --force # Force remove unmerged work
```

**When to use:** Work is abandoned, experimental, or will be merged manually later.

### Interactive Worktree Selection

When the user asks to close a worktree without specifying which one, use fzf for interactive selection:

```bash
# First list worktrees
git worktree list

# Parse the output and use fzf to let user select
# Then confirm merge vs. remove decision
```

**Example interaction:**
1. User: "Close a worktree"
2. Show `git worktree list` output
3. Use fzf or present choices for selection
4. Ask: "Merge to main or just remove?"
5. Execute appropriate command

## References

See `references/git-scripts-reference.md` for detailed documentation of all git scripts including `git-archivebranch` and `git-substat`.

## Working Directory Conventions

- **Main repo (root worktree):** Should stay in detached HEAD on freshest `origin/main`
  - After merging branches, update with: `git checkout --detach origin/main`
  - This prevents conflicts with other worktrees checking out branches
- **Worktrees:** Located in `.tree/` subdirectory
- **Main branch:** Typically lives in `.tree/maincomp` or similar
- **Feature branches:** Each in its own `.tree/<name>` directory

## Common Patterns

**Starting new feature work:**
```bash
git newtree my-feature
cd .tree/my-feature
# work on feature
```

**Completing and merging feature:**
```bash
cd .tree/maincomp
git maingulp my-feature .tree/my-feature
```

**Abandoning experimental work:**
```bash
git killtree .tree/experiment --force
```
