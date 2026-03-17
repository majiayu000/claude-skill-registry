---
name: mastering-git-cli
description: Git CLI operations, workflows, and automation for modern development (2025). Use when working with repositories, commits, branches, merging, rebasing, worktrees, submodules, or multi-repo architectures. Includes parallel agent workflow patterns, merge strategies, conflict resolution, and large repo optimization. Triggers on git commands, version control, merge conflicts, worktree setup, submodule management, repository troubleshooting, branch strategy, rebase operations, cherry-pick decisions, and CI/CD git integration.
---

# Git CLI Skill (2025 Edition)

Production-ready Git workflows and automation for modern development.

> **Compatibility:** Git 2.38+ recommended. Git 2.51+ for full SHA-256/Reftable support.

## Triggers

This skill activates on:
- `git` commands and version control questions
- Merge conflicts, rebase operations, cherry-pick decisions
- Worktree setup and submodule management
- Branch strategy and repository troubleshooting
- Large repo optimization (Scalar, sparse checkout, blobless clones)
- CI/CD git integration and performance tuning

## Quick Start

### Most Common Patterns

```bash
# Clone and start working (use switch, not checkout)
git clone <url> && cd <repo>
git switch -c feature-x

# Commit workflow
git add -A && git commit -m "feat: description"
git push -u origin feature-x

# Merge feature to main
git switch main && git pull
git merge --no-ff feature-x
git push

# Large repo? Use partial clone
git clone --filter=blob:none <url>
```

### Modern Git Config (2025 Defaults)

```bash
# Core workflow
git config --global pull.rebase true
git config --global push.autoSetupRemote true
git config --global merge.conflictStyle zdiff3
git config --global diff.algorithm histogram
git config --global rerere.enabled true
git config --global rebase.autoStash true

# Performance (essential for large repos)
git config --global core.fsmonitor true
git config --global fetch.prune true
git config --global feature.manyFiles true

# SSH signing (simpler than GPG)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

# Enable background maintenance
git maintenance start
```

## Decision Trees

### Merge vs Rebase vs Cherry-pick

```
Need to integrate changes?
│
├─ All commits from a branch?
│  ├─ Shared branch (pushed/collaborative) → MERGE
│  └─ Local-only branch → REBASE (cleaner) or MERGE
│
└─ Specific commits only?
   └─ CHERRY-PICK
      ├─ Hotfix to release branch → cherry-pick -x
      └─ Backport to old version → cherry-pick -x

⚠️ AVOID: Rebasing shared/pushed branches (rewrites history others depend on)
```

### Worktrees vs Branches vs Stash

```
Need to switch context?
│
├─ Quick switch, will return soon → STASH
├─ Parallel work on same files → Not possible
├─ Parallel work on different features?
│  ├─ Short-lived (minutes) → STASH or COMMIT WIP
│  └─ Long-running or parallel builds → WORKTREE
│
└─ Multiple agents working simultaneously → WORKTREE (essential)
```

### Submodules vs Subtree vs Monorepo

```
External code dependency?
│
├─ Need to modify and contribute back → SUBMODULE
├─ Just embedding, no upstream → SUBTREE
├─ Tight coupling, single team → MONOREPO
└─ Standard library/package → PACKAGE MANAGER
```

### Reset vs Revert vs Restore

```
Undo something?
│
├─ Discard file changes (not staged) → git restore <file>
├─ Unstage files → git restore --staged <file>
├─ Undo commits (not pushed)?
│  ├─ Keep changes staged → git reset --soft HEAD~1
│  ├─ Keep changes unstaged → git reset HEAD~1
│  └─ Discard everything → git reset --hard HEAD~1
│
└─ Undo commits (already pushed) → git revert <sha>
```

### Clone Strategy (Large Repos)

```
How to clone?
│
├─ Small repo (<500MB) → Full clone (default)
├─ Large repo, developer workstation
│  └─ BLOBLESS clone → git clone --filter=blob:none <url>
├─ Large repo, CI build
│  ├─ Need only HEAD → SHALLOW → git clone --depth 1
│  └─ Need history → TREELESS → git clone --filter=tree:0
│
└─ Monorepo, specific directories only
   └─ SCALAR + SPARSE → scalar clone <url>, then sparse-checkout

⚠️ AVOID: Shallow clone for development (breaks blame, log, push)
```

### checkout vs switch/restore

```
Which command?
│
├─ Changing branches → git switch <branch>
├─ Creating branch → git switch -c <new-branch>
├─ Discarding file changes → git restore <file>
├─ Unstaging files → git restore --staged <file>
│
└─ git checkout → Legacy (avoid in new scripts)
```

## Merge Easy Buttons

### Integrate feature into main
```bash
git checkout main
git merge --no-ff feature    # Always creates merge commit
```

### Update feature with latest main
```bash
git checkout feature
git merge main               # Safe for shared branches
# OR
git rebase main              # Only if branch not shared
```

### Resolve all conflicts using theirs
```bash
git checkout --theirs .
git add .
git commit
```

### Resolve all conflicts using ours
```bash
git checkout --ours .
git add .
git commit
```

### Abort a broken merge
```bash
git merge --abort
```

### Undo a pushed merge
```bash
git revert -m 1 <merge-sha>
git push
```

### Merge multiple branches at once
```bash
git merge feature-a feature-b feature-c  # Octopus merge (no conflicts allowed)
```

## Script Usage

### Agent Worktree Setup
Create isolated worktrees for parallel agent development:
```bash
scripts/setup-agent-worktrees.sh [num_agents] [base_branch]
# Example: scripts/setup-agent-worktrees.sh 3 main
# Creates: ../agent-1, ../agent-2, ../agent-3, ../integration
# Output: "Created 3 agent worktrees from main"
```
**Use case:** Running 3 Claude agents in parallel on different features, each with isolated working directories.

### Agent Worktree Cleanup
Remove all agent worktrees and optionally delete branches:
```bash
scripts/cleanup-agent-worktrees.sh [--delete-branches] [--force]
# Example: scripts/cleanup-agent-worktrees.sh --delete-branches
# Removes worktrees and their associated branches
```

### Submodule Status Report
Get readable status of all submodules:
```bash
scripts/submodule-report.sh
# Output: Table showing submodule path, branch, commit, and sync status
```

### Git Health Check
Diagnose common repository issues:
```bash
scripts/git-health-check.sh [--verbose]
# Checks: dangling objects, broken refs, large files, stale branches
```

## Reference Navigation

Read the appropriate reference file based on your task:

| Task | Reference File |
|------|----------------|
| Understand Git internals, object model, DAG | [references/foundations.md](references/foundations.md) |
| Configure Git, set up 2025 defaults | [references/foundations.md](references/foundations.md) |
| Clone, commit, log, branch basics | [references/daily-usage.md](references/daily-usage.md) |
| Create/manage worktrees | [references/worktrees.md](references/worktrees.md) |
| Set up parallel agent workflows | [references/worktrees.md](references/worktrees.md) |
| Choose merge strategy | [references/merge-operations.md](references/merge-operations.md) |
| Resolve merge conflicts | [references/merge-operations.md](references/merge-operations.md) |
| Use rerere for conflict resolution | [references/merge-operations.md](references/merge-operations.md) |
| Add/update/manage submodules | [references/submodules.md](references/submodules.md) |
| Multi-repo project architecture | [references/submodules.md](references/submodules.md) |
| Reset, revert, restore operations | [references/advanced-operations.md](references/advanced-operations.md) |
| Interactive rebase, squashing | [references/advanced-operations.md](references/advanced-operations.md) |
| Stashing, tags, hooks | [references/advanced-operations.md](references/advanced-operations.md) |
| Recover lost commits/branches | [references/recovery.md](references/recovery.md) |
| Troubleshoot common errors | [references/recovery.md](references/recovery.md) |
| Command cheat sheet | [references/recovery.md](references/recovery.md) |
| **SHA-256, Reftable, SSH signing** | [references/git-2025-features.md](references/git-2025-features.md) |
| **git switch/restore, range-diff** | [references/git-2025-features.md](references/git-2025-features.md) |
| **Git maintenance, bisect run** | [references/git-2025-features.md](references/git-2025-features.md) |
| **Merge queues, pre-commit framework** | [references/git-2025-features.md](references/git-2025-features.md) |
| **Partial/blobless clones, Scalar** | [references/large-repos.md](references/large-repos.md) |
| **Sparse checkout for monorepos** | [references/large-repos.md](references/large-repos.md) |
| **Bare repo + worktree layout** | [references/large-repos.md](references/large-repos.md) |
| **CI/CD Git optimization** | [references/large-repos.md](references/large-repos.md) |

## Critical Knowledge

### The `-X ours` vs `-s ours` Trap

```bash
# -X ours: Prefer our changes ONLY IN CONFLICTS
git merge -X ours feature
# ↑ Merges all non-conflicting changes from feature

# -s ours: IGNORE EVERYTHING from other branch
git merge -s ours feature
# ↑ Keeps our tree exactly, just records the merge
```

### Conflict Style Recommendation

```bash
git config --global merge.conflictStyle zdiff3
```

Shows base version in conflicts, making resolution clearer:
```
<<<<<<< HEAD
our version
||||||| merged common ancestor
original version
=======
their version
>>>>>>> feature
```

### Branch Can Only Exist in One Worktree

A branch can only be checked out in ONE worktree. To work on it elsewhere:
```bash
git worktree add -b feature-copy ../feature-copy feature  # Create copy
```

### Submodules Default to Detached HEAD

After `git submodule update`, always checkout a branch before making changes:
```bash
cd submodule-dir
git checkout main  # Then make changes
```

## 2025 Easy Buttons

### Find the bug-introducing commit automatically
```bash
# Create test script: exit 0 = good, exit 1 = bad
echo '#!/bin/bash
npm test -- --grep="broken feature"' > test.sh
chmod +x test.sh

git bisect start HEAD v1.0.0
git bisect run ./test.sh
git bisect reset
```

### Compare rebased PR (what actually changed)
```bash
git range-diff main..feature@{1} main..feature
```

### Monorepo: checkout only what you need
```bash
git clone --filter=blob:none <url>
cd repo
git sparse-checkout init --cone
git sparse-checkout set backend/api frontend/app
```

### Set up performance optimization
```bash
scalar register                 # Enable all optimizations
# OR manually:
git maintenance start          # Background maintenance
git config core.fsmonitor true # Filesystem watcher
```

### SSH signing setup (simpler than GPG)
```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

### Migrate to reftable (10K+ branches)
```bash
git refs migrate --ref-format=reftable
```

## Anti-Patterns (Avoid These)

### Don't use checkout for file operations
```bash
# Bad: ambiguous, can lose data
git checkout file.txt

# Good: explicit intent
git restore file.txt
```

### Don't shallow clone for development
```bash
# Bad: breaks blame, log, push
git clone --depth 1 <url>

# Good: blobless preserves history
git clone --filter=blob:none <url>
```

### Don't skip --force-with-lease
```bash
# Bad: can overwrite teammates' work
git push --force

# Good: fails if remote has new commits
git push --force-with-lease
```

### Don't run git gc manually
```bash
# Bad: blocks, runs everything at once
git gc

# Good: scheduled, incremental
git maintenance start
```

### Don't rebase shared branches
```bash
# Bad: rewrites history others depend on
git rebase main  # on a pushed branch

# Good: merge instead for shared branches
git merge main
```

### Don't commit secrets or generated files
```bash
# Bad: committing sensitive or generated files
git add .env node_modules/

# Good: ensure .gitignore is set first
echo -e ".env\nnode_modules/" >> .gitignore
git add .gitignore
```

### Don't ignore merge conflicts
```bash
# Bad: accepting all changes blindly
git checkout --theirs .  # without reviewing

# Good: review each conflict
git mergetool  # or manual review with zdiff3
```
