---
name: finish-worktree
description: Completes feature branch work by rebasing, pushing, monitoring CI, and squash merging to main
user-invocable: true
---

# Finish Worktree Skill

**CLAUDE: When this skill is invoked with `/finish-worktree`, immediately run:**
```bash
./.claude/skills/finish-worktree/finish-worktree.sh
```
**Then guide the user through CI monitoring and merge-and-cleanup.**

## Purpose
Completes feature branch work with proper rebase, CI validation, and squash merge back to main.

## Usage
```bash
/finish-worktree
```

## Workflow Steps

### Step 1: Rebase onto main
```bash
./.claude/skills/finish-worktree/finish-worktree.sh
```

This script:
1. Fetches latest from origin/main
2. Rebases your branch onto main
3. Runs local validation (fmt, architectural, clippy)
4. Pushes with `--force-with-lease`

### Step 2: Monitor CI
Check GitHub Actions:
```
https://github.com/Async-IO/pierre_mcp_server/actions
```

Wait for all checks to pass (green).

### Step 3: If CI Fails
Fix the issues locally, then:
```bash
# Make fixes
cargo fmt
cargo clippy --all-targets -- -D warnings -D clippy::all -D clippy::pedantic -D clippy::nursery

# Amend or add commit
git add .
git commit --amend --no-edit  # or new commit

# Push again
git push --force-with-lease origin <branch-name>
```

Repeat until CI is green.

### Step 4: Squash Merge and Cleanup
Once CI is green, run from the **main worktree**:
```bash
cd /path/to/main/worktree
./.claude/skills/finish-worktree/merge-and-cleanup.sh
```

No arguments needed - branch info is saved by `finish-worktree.sh`.

This script:
1. Pulls latest main
2. Squash merges the feature branch
3. Prompts for commit message
4. Pushes main
5. Removes the worktree
6. Deletes the feature branch

## Complete Example Session
```bash
# On feature branch in worktree
./.claude/skills/finish-worktree/finish-worktree.sh

# Wait for CI...
# If red, fix and push again
# Once green, go to main worktree:

cd /path/to/main/worktree
./.claude/skills/finish-worktree/merge-and-cleanup.sh
```

## Related Skills
- `create-worktree` - Creates worktree with environment setup
