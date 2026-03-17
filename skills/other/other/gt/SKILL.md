---
name: gt
description:
  This skill should be used when working with Graphite (gt) for stacked
  pull requests. Use when users mention gt commands, stack management, PR workflows,
  or when dealing with dependent branches. Essential for understanding stack navigation,
  branch relationships, and Graphite's mental model.
---

# Graphite

## Overview

Graphite (gt) is a CLI tool for managing stacked pull requests - breaking large features into small, incremental changes built on top of each other. This skill provides the mental model, command reference, and workflow patterns needed to work effectively with gt.

## Core Mental Model

### Stacks are Linear Chains

A **stack** is a sequence of branches where each branch (except trunk) has exactly one parent:

```
VALID STACK (linear):
main → feature-a → feature-b → feature-c

INVALID (not a stack):
main → feature-a → feature-b
            └─────→ feature-x
```

### Key Concepts

- **Parent-Child Relationships**: Every branch tracked by gt (except trunk) has exactly one parent branch it builds upon
- **Auto-restacking**: When modifying a branch, gt automatically rebases all upstack branches to include changes
- **Directional Navigation**:
  - **Downstack/Down**: Toward trunk (toward the base) - `gt down` moves from feature-b → feature-a → main
  - **Upstack/Up**: Away from trunk (toward the tip) - `gt up` moves from feature-a → feature-b → feature-c
- **Trunk**: The main branch (usually `main` or `master`) that all stacks build upon

### Stack Visualization - CRITICAL MENTAL MODEL

**When working with Graphite stacks, always visualize trunk at the BOTTOM:**

```
TOP ↑    feat-3  ← upstack (leaf)
         feat-2
         feat-1
BOTTOM ↓ main    ← downstack (trunk)
```

### Directional Terminology - MUST UNDERSTAND

- **UPSTACK / UP** = away from trunk = toward TOP = toward leaves
- **DOWNSTACK / DOWN** = toward trunk = toward BOTTOM = toward main

### Detailed Examples

Given stack: `main → feat-1 → feat-2 → feat-3`

**If current branch is `feat-1`:**

- Upstack: `feat-2`, `feat-3` (children, toward top)
- Downstack: `main` (parent, toward bottom)

**If current branch is `feat-3` (at top):**

- Upstack: _(nothing, already at top/leaf)_
- Downstack: `feat-2`, `feat-1`, `main` (ancestors, toward bottom)

### Why This Mental Model Is Critical

🔴 **Commands depend on this visualization:**

- `gt up` / `gt down` navigate the stack
- `land-stack` traverses branches in specific direction
- Stack traversal logic (parent/child relationships)

🔴 **Common mistake:** Thinking "upstack" means "toward trunk"

- **WRONG**: upstack = toward main ❌
- **CORRECT**: upstack = away from main ✅

🔴 **PR landing order:** Always bottom→top (main first, then each layer up)

### Metadata Storage

All gt metadata is stored in the shared `.git` directory (accessible across worktrees):

- `.git/.graphite_repo_config` - Repository-level configuration (trunk branch)
- `.git/.graphite_cache_persist` - Branch relationships (parent-child graph)
- `.git/.graphite_pr_info` - Cached GitHub PR information

**Important**: Metadata is shared across all worktrees since it's in the common `.git` directory.

## Essential Commands

### Common Workflow Commands

| Command             | Alias   | Purpose                                                               |
| ------------------- | ------- | --------------------------------------------------------------------- |
| `gt create [name]`  | `gt c`  | Create new branch stacked on current branch and commit staged changes |
| `gt modify`         | `gt m`  | Modify current branch (amend commit) and auto-restack children        |
| `gt submit`         | `gt s`  | Push branches and create/update PRs                                   |
| `gt submit --stack` | `gt ss` | Submit entire stack (up + down)                                       |
| `gt sync`           | -       | Sync from remote and prompt to delete merged branches                 |

### Navigation Commands

| Command                | Alias   | Purpose                         |
| ---------------------- | ------- | ------------------------------- |
| `gt up [steps]`        | `gt u`  | Move up stack (away from trunk) |
| `gt down [steps]`      | `gt d`  | Move down stack (toward trunk)  |
| `gt top`               | `gt t`  | Move to tip of stack            |
| `gt bottom`            | `gt b`  | Move to bottom of stack         |
| `gt checkout [branch]` | `gt co` | Interactive branch checkout     |

### Stack Management

| Command      | Purpose                                                   |
| ------------ | --------------------------------------------------------- |
| `gt restack` | Ensure each branch has its parent in git history          |
| `gt move`    | Rebase current branch onto different parent               |
| `gt fold`    | Fold branch's changes into parent                         |
| `gt split`   | Split current branch into multiple single-commit branches |
| `gt log`     | Visualize stack structure                                 |

### Branch Info & Management

| Command               | Purpose                                         |
| --------------------- | ----------------------------------------------- |
| `gt branch info`      | Show branch info (parent, children, commit SHA) |
| `gt parent`           | Show parent branch name                         |
| `gt children`         | Show children branch names                      |
| `gt track [branch]`   | Start tracking branch with gt (set parent)      |
| `gt untrack [branch]` | Stop tracking branch with gt                    |
| `gt delete [name]`    | Delete branch and update metadata               |
| `gt rename [name]`    | Rename branch and update metadata               |

## Workflow Patterns

### Pattern 1: Creating a New Stack

Build a feature in multiple reviewable chunks:

```bash
# 1. Start from trunk
gt checkout main
git pull

# 2. Create first branch
gt create phase-1 -m "Add API endpoints"
# ... make changes ...
git add .
gt modify -m "Add API endpoints"

# 3. Create second branch on top
gt create phase-2 -m "Update frontend"
# ... make changes ...
git add .
gt modify -m "Update frontend"

# 4. Submit entire stack
gt submit --stack

# Result: 2 PRs created
# PR #101: phase-1 (base: main)
# PR #102: phase-2 (base: phase-1)
```

### Pattern 2: Responding to Review Feedback

Update a branch in the middle of a stack:

```bash
# Navigate down to target branch
gt down  # Repeat as needed

# Make changes
# ... edit files ...
git add .

# Modify (auto-restacks upstack branches)
gt modify -m "Address review feedback"

# Resubmit stack
gt submit --stack
```

### Pattern 3: Adding to Existing Stack

Insert a new branch in the middle:

```bash
# Checkout the parent where you want to insert
gt checkout phase-1

# Create new branch with --insert
gt create phase-1.5 --insert -m "Add validation"

# Select which child to move onto new branch
# Interactive prompt appears

# Submit new PR
gt submit
```

### Pattern 4: Syncing After Merges

Clean up after PRs merge on GitHub:

```bash
# Run sync
gt sync

# Prompts to delete merged branches
# Confirms deletion
y

# Result:
# - Merged branches deleted locally
# - Remaining branches rebased onto trunk
# - PR bases updated on GitHub
```

### Pattern 5: Splitting Large Changes

Break up a large commit into reviewable pieces:

```bash
# Checkout branch with large commit
gt checkout large-feature

# Split into single-commit branches
gt split

# Rename branches meaningfully
gt rename add-api-endpoints
gt up
gt rename add-frontend
gt up
gt rename add-tests

# Submit
gt submit --stack
```

## Common Mistakes to Avoid

1. **Don't use `git rebase` directly**: Use `gt modify` or `gt restack` - gt needs to update metadata during rebasing

2. **Don't delete branches with `git branch -d`**: Use `gt delete` - metadata needs to be updated to re-parent children

3. **Don't assume `gt submit` only affects current branch**: It submits downstack too (all ancestors). Use `gt submit --stack` to include upstack

4. **Don't forget to `gt sync` after merges**: Stale branches accumulate and metadata gets outdated

5. **⚠️ NEVER use `gt log short` for branch status**: The output format is counterintuitive and confuses agents. Use `gt branch info`, `gt parent`, or `gt children` for explicit metadata access instead

## Quick Decision Tree

**When to use gt commands:**

- **Start new work** → `gt create` (sets parent relationship)
- **Edit current branch** → `gt modify` (auto-restacks children)
- **Navigate stack** → `gt up/down/top/bottom` (move through chain)
- **View structure** → `gt log` (see visualization)
- **Get parent branch** → `gt branch info` (parse "Parent:" line)
- **Get branch relationships** → `gt parent` / `gt children` (quick access)
- **Submit PRs** → `gt submit --stack` (create/update all PRs)
- **After merges** → `gt sync` (clean up + rebase)
- **Reorganize** → `gt move` (change parent)
- **Combine work** → `gt fold` (merge into parent)
- **Split work** → `gt split` (break into branches)

## Resources

### references/

Contains detailed command reference and comprehensive mental model documentation:

- `gt-reference.md` - Complete command reference, metadata format details, and advanced patterns

Load this reference when users need detailed information about specific gt commands, metadata structure, or complex workflow scenarios.
