---
name: using-git-spice
description: Use when working with stacked branches, managing dependent PRs/CRs, or uncertain about git-spice commands (stack vs upstack vs downstack) - provides command reference, workflow patterns, and common pitfalls for the git-spice CLI tool
---

# Using git-spice

## Overview

**git-spice (`gs`) is a CLI tool for managing stacked Git branches and their Change Requests.**

Core principle: git-spice tracks branch relationships (stacks) and automates rebasing/submitting dependent branches.

## Key Concepts

**Stack terminology:**
- **Stack**: All branches connected to current branch (both upstack and downstack)
- **Upstack**: Branches built on top of current branch (children and descendants)
- **Downstack**: Branches below current branch down to trunk (parents and ancestors)
- **Trunk**: Main integration branch (typically `main` or `master`)

**Example stack:**
```
┌── feature-c     ← upstack from feature-b
├── feature-b     ← upstack from feature-a, downstack from feature-c
├── feature-a     ← downstack from feature-b
main (trunk)
```

When on `feature-b`:
- **Upstack**: feature-c
- **Downstack**: feature-a, main
- **Stack**: feature-a, feature-b, feature-c

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| **Initialize repo** | `gs repo init` | Required once per repo. Sets trunk branch. |
| **Create stacked branch** | `gs branch create <name>` | Creates branch on top of current. Use `gs bc` shorthand. |
| **View stack** | `gs log short` | Shows current stack. Use `gs ls` or `gs log long` (`gs ll`) for details. |
| **Submit stack as PRs** | `gs stack submit` | Submits entire stack. Use `gs ss` shorthand. |
| **Submit upstack only** | `gs upstack submit` | Current branch + children. Use `gs us s` shorthand. |
| **Submit downstack only** | `gs downstack submit` | Current branch + parents to trunk. Use `gs ds s` shorthand. |
| **Rebase entire stack** | `gs repo restack` | Rebases all tracked branches on their bases. |
| **Rebase current stack** | `gs stack restack` | Rebases current branch's stack. Use `gs sr` shorthand. |
| **Rebase upstack** | `gs upstack restack` | Current branch + children. Use `gs us r` shorthand. |
| **Move branch to new base** | `gs upstack onto <base>` | Moves current + upstack to new base. |
| **Sync with remote** | `gs repo sync` | Pulls latest, deletes merged branches. |
| **Track existing branch** | `gs branch track [branch]` | Adds branch to git-spice tracking. |
| **Delete branch** | `gs branch delete [branch]` | Deletes branch, restacks children. Use `gs bd` shorthand. |

**Command shortcuts:** Most commands have short aliases. Use `gs --help` to see all aliases.

## Common Workflows

These workflows apply to **single-repository** scenarios. For features spanning multiple repositories, see [Multi-Repo Workflows](#multi-repo-workflows) below.

### Workflow 1: Create and Submit Stack

```bash
# One-time setup
gs repo init
# Prompt asks for trunk branch (usually 'main')

# Create stacked branches
gs branch create feature-a
# Make changes, commit with git
git add . && git commit -m "Implement A"

gs branch create feature-b  # Stacks on feature-a
# Make changes, commit
git add . && git commit -m "Implement B"

gs branch create feature-c  # Stacks on feature-b
# Make changes, commit
git add . && git commit -m "Implement C"

# View the stack
gs log short

# Submit entire stack as PRs
gs stack submit
# Creates/updates PRs for all branches in stack
```

### Workflow 2: Update Branch After Review

```bash
# You have feature-a → feature-b → feature-c
# Reviewer requested changes on feature-b

git checkout feature-b
# Make changes, commit
git add . && git commit -m "Address review feedback"

# Rebase upstack (feature-c) on updated feature-b
gs upstack restack

# Submit changes to update PRs
gs upstack submit
# Note: restack only rebases locally, submit pushes and updates PRs
```

**CRITICAL: Don't manually rebase feature-c!** Use `gs upstack restack` to maintain stack relationships.

### Workflow 3: Sync After Upstream Merge

```bash
# feature-a was merged to main
# Need to update feature-b and feature-c

# Sync with remote (pulls main, deletes merged branches)
gs repo sync

# Restack everything on new main
gs repo restack

# Verify stack looks correct
gs log short

# Push updated branches
gs stack submit
```

**CRITICAL: Don't rebase feature-c onto main!** After feature-a merges:
- feature-b rebases onto main (its new base)
- feature-c rebases onto feature-b (maintains dependency)

## When to Use Git vs git-spice

**Use git-spice for:**
- Creating branches in a stack: `gs branch create`
- Rebasing stacks: `gs upstack restack`, `gs repo restack`
- Submitting PRs: `gs stack submit`, `gs upstack submit`
- Viewing stack structure: `gs log short`
- Deleting branches: `gs branch delete` (restacks children)

**Use git for:**
- Making changes: `git add`, `git commit`
- Checking status: `git status`, `git diff`
- Viewing commit history: `git log`
- Individual branch operations: `git checkout`, `git switch`

**Never use `git rebase` directly on stacked branches** - use git-spice restack commands to maintain relationships.

## Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| Rebasing child onto trunk after parent merges | Breaks stack relationships, creates conflicts | Use `gs repo sync && gs repo restack` |
| Using `git push --force` after changes | Bypasses git-spice tracking | Use `gs upstack submit` or `gs stack submit` |
| Manually rebasing with `git rebase` | git-spice doesn't track the rebase | Use `gs upstack restack` or `gs stack restack` |
| Running `gs stack submit` on wrong branch | Might submit unintended branches | Check `gs log short` first to see what's in stack |
| Forgetting `gs repo init` | Commands fail with unclear errors | Run `gs repo init` once per repository |
| Using `stack` when you mean `upstack` | Submits downstack branches too (parents) | Use `upstack` to submit only current + children |
| Assuming `restack` runs automatically | After commits, stack can drift | Explicitly run `gs upstack restack` after changes |

## Red Flags - Check Documentation

- Confused about stack/upstack/downstack scope
- About to run `git rebase` on a tracked branch
- Unsure which submit command to use
- Getting "not tracked" errors

**When uncertain, run `gs <command> --help` for detailed usage.**

## Authentication and Setup

**First time setup:**
```bash
# Authenticate with GitHub/GitLab
gs auth login
# Follow prompts for OAuth or token auth

# Initialize repository
gs repo init
# Sets trunk branch and remote

# Verify setup
gs auth status
```

## Handling Conflicts

If `gs upstack restack` or `gs repo restack` encounters conflicts:
1. Resolve conflicts using standard git workflow (`git status`, edit files, `git add`)
2. Continue with `git rebase --continue`
3. git-spice will resume restacking remaining branches
4. After resolution, run `gs upstack submit` to push changes

If you need to abort a restack, check `gs --help` for recovery options.

## Multi-Repo Workflows

### Per-Repo Stacking Limitation

Git-spice operates on ONE repository at a time. In multi-repo spectacular features:
- Each repo has its own independent stack
- Cannot create a cross-repo linear stack
- Branches stay within their respective repos

### Multi-Repo PR Submission

For features spanning multiple repos, submit PRs in phase order:

**Phase-ordered submission:**
```bash
# Phase 1 repos first (foundation)
cd shared-lib
gs stack submit
cd ..

# Phase 2 repos second
cd backend
gs stack submit
cd ..

# Phase 3 repos last (depends on earlier phases)
cd frontend
gs stack submit
cd ..
```

**Why phase order matters:**
- Phase 1 changes (e.g., shared types) must merge before Phase 2 consumers
- Prevents broken builds from missing dependencies
- Mirrors the execution order during development

### Multi-Repo Stack Visualization

View stacks across all repos:

```bash
# From workspace root
for repo in backend frontend shared-lib; do
  echo "=== $repo ==="
  cd $repo && gs log short && cd ..
done
```

### Multi-Repo Sync

After PRs merge, sync all repos:

```bash
# From workspace root
for repo in backend frontend shared-lib; do
  echo "Syncing $repo..."
  cd $repo && gs repo sync && cd ..
done
```

### Coordinating Cross-Repo Dependencies

If PR in repo A depends on PR in repo B:

1. Merge repo B's PR first
2. Update repo A to use the merged changes
3. Then merge repo A's PR

**Example:**
```
shared-lib: PR for new types
  ↓ (merge first)
backend: PR using new types
  ↓ (merge second)
frontend: PR using backend API
  ↓ (merge third)
```

## Additional Resources

- Full CLI reference: `gs --help`
- Command-specific help: `gs <command> --help`
- Configuration: `gs config --help`
- Official docs: https://abhinav.github.io/git-spice/
