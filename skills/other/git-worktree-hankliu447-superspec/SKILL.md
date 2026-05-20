---
name: git-worktree
description: |
  Use when starting feature work that needs isolation from current workspace.
  Creates isolated git worktrees with smart directory selection and safety verification.
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

**Announce at start:** "I'm using the git-worktree skill to set up an isolated workspace."

## When to Use

- Before executing implementation plans (`/superspec:execute`)
- When starting a new change that needs isolation
- When you need to work on multiple changes simultaneously

## Directory Selection Process

Follow this priority order:

### 1. Check Existing Directories

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found:** Use that directory. If both exist, `.worktrees` wins.

### 2. Check Project Configuration

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
grep -i "worktree.*director" superspec/project.md 2>/dev/null
```

**If preference specified:** Use it without asking.

### 3. Ask User

If no directory exists and no preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden) - Recommended
2. worktrees/ (project-local, visible)

Which would you prefer?
```

## Safety Verification

### For Project-Local Directories

**MUST verify directory is ignored before creating worktree:**

```bash
# Check if directory is ignored
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored:**

1. Add to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents to repository.

## Creation Steps

### 1. Determine Change ID

Use the change ID from SuperSpec:
```bash
change_id="add-2fa"  # From superspec/changes/[change-id]/
```

### 2. Create Worktree

```bash
# Create worktree with new branch
git worktree add .worktrees/$change_id -b feature/$change_id

# Navigate to worktree
cd .worktrees/$change_id
```

### 3. Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verify Clean Baseline

Run tests to ensure worktree starts clean:

```bash
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.

**If tests pass:** Report ready.

### 5. Report Location

```
Worktree ready at .worktrees/[change-id]
Branch: feature/[change-id]
Tests: Passing (N tests, 0 failures)

SuperSpec documents:
- Proposal: superspec/changes/[change-id]/proposal.md
- Design: superspec/changes/[change-id]/design.md
- Specs: superspec/changes/[change-id]/specs/

Ready to implement. Next: /superspec:execute
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check config → Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |

## Common Mistakes

### Skipping ignore verification

- **Problem:** Worktree contents get tracked, pollute git status
- **Fix:** Always use `git check-ignore` before creating project-local worktree

### Proceeding with failing tests

- **Problem:** Can't distinguish new bugs from pre-existing issues
- **Fix:** Report failures, get explicit permission to proceed

## Red Flags

**Never:**
- Create worktree without verifying it's ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking

**Always:**
- Follow directory priority: existing > config > ask
- Verify directory is ignored for project-local
- Auto-detect and run project setup
- Verify clean test baseline

## Integration

**Called by:**
- `plan-writing` - After plan creation, before execution

**Pairs with:**
- `finish-branch` - Cleans up worktree after work complete
- `subagent-development` - Work happens in this worktree
