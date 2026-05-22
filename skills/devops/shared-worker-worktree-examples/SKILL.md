---
name: worker-worktree-examples
description: Git worktree practical examples for parallel agent development
---

# Worker Worktree Examples

This file provides practical examples for using git worktrees in the Ralph Orchestra multi-agent workflow.

## Example 1: Developer Agent First-Time Setup

```bash
# Developer agent starts, checks for worktree
git worktree list
# Output: /path/to/main  main

# No developer-worktree exists, create it
git worktree add ../developer-worktree -b developer-worktree
# Output: Preparing worktree (checking out developer-worktree)

# Verify creation
git worktree list
# Output:
# /path/to/main              main
# /path/to/developer-worktree  developer-worktree

# Navigate to worktree
cd ../developer-worktree

# Verify current branch
git branch --show-current
# Output: developer-worktree
```

## Example 2: Daily Developer Workflow

```bash
# Start of task - Developer agent wakes up
cd ../developer-worktree

# Pull latest from main
git fetch origin main
git merge origin/main
# Output: Updating abc1234..def5678

# Check status
git status
# Output: On branch developer-worktree, your branch is up to date

# Make changes, commit, push
# ... (code changes) ...
git add .
git commit -m "[ralph] [developer] feat-001: Implement player movement"
git push origin developer-worktree

# Send to QA, exit
```

## Example 3: Tech Artist Parallel Work

```bash
# Tech Artist starts while Developer is working
cd ../techartist-worktree

# Pull latest from main
git fetch origin main
git merge origin/main

# Make visual changes, commit
# ... (shader changes) ...
git add src/assets/shaders/
git commit -m "[ralph] [techartist] vis-001: Create water shader"
git push origin techartist-worktree

# Send to QA, exit
```

## Example 4: QA Validating Developer Work

```bash
# QA receives validation request for Developer work

# Navigate to Developer worktree
cd ../developer-worktree

# Pull latest changes
git pull origin developer-worktree

# Run feedback loops
npm run type-check
npm run lint
npm run build

# Run browser tests with Playwright MCP
# ... (testing actions) ...

# If validation PASSES:
cd ..
git checkout main
git merge origin/developer-worktree
git push origin main

# Update PRD with pass status, commit
git add prd.json
git commit -m "[ralph] [qa] feat-001: Validation PASSED"

# If validation FAILS:
# Stay in main, do NOT merge
# Send bug_report to Developer
# Developer fixes in developer-worktree
```

## Example 5: QA Validating Tech Artist Work

```bash
# QA receives validation request for Tech Artist work

# Navigate to Tech Artist worktree
cd ../techartist-worktree

# Pull latest changes
git pull origin techartist-worktree

# Run feedback loops
npm run type-check
npm run lint
npm run build

# Visual testing with Playwright MCP
# ... (screenshot, visual analysis) ...

# If validation PASSES:
cd ..
git checkout main
git merge origin/techartist-worktree
git push origin main

# Update PRD with pass status, commit
git add prd.json
git commit -m "[ralph] [qa] vis-001: Validation PASSED"

# If validation FAILS:
# Send bug_report to Tech Artist
# Tech Artist fixes in techartist-worktree
```

## Example 6: Resolving Merge Conflicts

```bash
# Developer pulls main and gets conflicts
cd ../developer-worktree
git fetch origin main
git merge origin/main

# Output: CONFLICT (content): Merge conflict in src/game/Game.tsx

# Check conflicts
git status
# Output: both modified: src/game/Game.tsx

# Edit conflicted file, resolve markers
# ... (manual resolution) ...

# Mark as resolved
git add src/game/Game.tsx

# Complete merge
git commit -m "Merge main into developer-worktree - resolved conflicts"

# Continue work
```

## Example 7: PM Assigning Parallel Tasks

```bash
# PM checks both agents are idle
# prd.json.agents.developer.status = "idle"
# prd.json.agents.techartist.status = "idle"

# PM finds non-conflicting tasks:
# - feat-001: Player movement (Developer) -> src/hooks/, src/components/
# - vis-001: Water shader (Tech Artist) -> src/assets/shaders/

# PM assigns to both simultaneously:
# 1. Update prd.json items status for both tasks
# 2. Send task_assignment to developer
# 3. Send task_assignment to techartist
# 4. Exit, let both agents work in parallel
```

## Example 8: Full Parallel Development Cycle

```
Timeline: Parallel Task Execution

00:00  PM assigns feat-001 to Developer, vis-001 to Tech Artist
       |
       |-- Developer: cd ../developer-worktree, git merge main, starts coding
       |-- Tech Artist: cd ../techartist-worktree, git merge main, creates shader

00:30  Developer: Commits work, pushes to developer-worktree branch
       Developer: Sends implementation_complete to QA

01:00  Tech Artist: Commits work, pushes to techartist-worktree branch
       Tech Artist: Sends validation_request to QA

01:30  QA: Receives Developer work, tests in ../developer-worktree
       QA: Validation PASSES
       QA: git checkout main, merge developer-worktree, push main

02:00  QA: Receives Tech Artist work, tests in ../techartist-worktree
       QA: Validation PASSES
       QA: git checkout main, merge techartist-worktree, push main

02:30  PM: Both tasks complete, triggers retrospective
```

## Example 9: Bug Fix Cycle After Failed Validation

```bash
# QA tests Developer work, finds bug
cd ../developer-worktree
# ... (testing) ...
# FAIL: Type error in PlayerController.ts

# QA stays in main, does NOT merge
# QA sends bug_report to Developer

# Developer receives bug_report
cd ../developer-worktree

# Fix the bug
# ... (code fix) ...
git add src/player/PlayerController.ts
git commit -m "[ralph] [developer] feat-001: Fix type error per QA feedback"
git push origin developer-worktree

# Send implementation_complete to QA

# QA re-tests in developer-worktree
cd ../developer-worktree
# ... (testing) ...
# PASS: All checks pass

# QA merges to main
cd ..
git checkout main
git merge origin/developer-worktree
git push origin main
```

## Example 10: Worktree Cleanup (After Task Complete)

```bash
# After QA validation passes and work is merged to main

# Agent (Developer or Tech Artist) can clean up worktree branch
# Note: Keep the worktree directory, just clean the branch

cd ../developer-worktree

# Option 1: Reset to match main (clean slate for next task)
git fetch origin main
git reset --hard origin/main
git push -f origin developer-worktree

# Option 2: Merge main into worktree (preserves history)
git fetch origin main
git merge origin/main
git push origin developer-worktree

# Ready for next task
```

## Common Worktree Commands Quick Reference

```bash
# List all worktrees
git worktree list

# Create new worktree
git worktree add ../{agent}-worktree -b {agent}-worktree

# Remove worktree
git worktree remove ../{agent}-worktree

# Move worktree to new location
git worktree move ../{agent}-worktree /new/path/{agent}-worktree

# Prune stale worktree references
git worktree prune

# Check worktree status
git worktree list --porcelain
```
