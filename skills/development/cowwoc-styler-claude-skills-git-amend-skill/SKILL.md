---
name: git-amend
description: Safely amend commits (HEAD or non-HEAD) with selective staging and safety checks
allowed-tools: Bash, Read
---

# Git Amend Skill

**Purpose**: Safely amend git commits (both HEAD and older commits) with proper
authorship verification, selective staging, and push status checks.

**When to Use**:
- User asks to "amend X file into commit Y"
- Adding forgotten changes to the last commit (HEAD)
- Adding changes to an older commit (non-HEAD) via fixup workflow
- Fixing commit message of the most recent commit
- Adding pre-commit hook modifications to a commit

## Core Principles

### 1. Selective Staging (CRITICAL)

**When user specifies files to amend, stage ONLY those files.**

❌ **WRONG - Stages unrelated changes**:
```bash
# User: "Amend foo.md in commit ABC"
git status  # Shows: M foo.md, M bar.md
git add foo.md bar.md  # ← WRONG: Added bar.md too!
git commit --amend --no-edit
```

✅ **CORRECT - Only specified file**:
```bash
# User: "Amend foo.md in commit ABC"
git status  # Shows: M foo.md, M bar.md
git add foo.md  # ← Only the specified file
git commit --amend --no-edit
```

**Rule**: User's request is the scope. Don't assume other modified files should be
included unless explicitly requested.

### 2. Authorship Verification

**NEVER amend commits authored by others without explicit permission.**

```bash
# Check authorship before amending
git log -1 --format='%an <%ae>'

# If author is NOT the current user or Claude:
# - Ask user for permission
# - OR create a new commit instead
```

### 3. Push Status Check

**Verify commit hasn't been pushed before amending.**

```bash
# Check if commit is ahead of remote (safe to amend)
git status | grep -E "ahead|behind"

# If pushed: WARN user that amending will require force push
```

## Amend Workflow

### Step 1: Verify Target Commit

```bash
# Confirm HEAD is the commit to amend
git log -1 --oneline

# Check if target commit is HEAD
git log -1 --format='%H' HEAD
# Compare with target commit hash
```

**If target is NOT HEAD**: Use the fixup workflow in "Amending Non-HEAD Commits" section below.

### Step 2: Check Safety Conditions

```bash
# 1. Check authorship
AUTHOR=$(git log -1 --format='%an %ae')
echo "Commit author: $AUTHOR"

# 2. Check push status
git status | grep -E "Your branch is (ahead|behind)"

# 3. Check for merge commits (don't amend these)
PARENT_COUNT=$(git cat-file -p HEAD | grep -c "^parent")
if [[ $PARENT_COUNT -gt 1 ]]; then
  echo "WARNING: This is a merge commit - consider not amending"
fi
```

### Step 3: Stage ONLY Specified Files

```bash
# List what user wants to amend
echo "Files to amend:"
echo "  - file1.md"
echo "  - file2.md"

# Show current status for context
git status --short

# Stage ONLY specified files
git add file1.md file2.md

# Verify staging is correct
git diff --cached --name-only
```

### Step 4: Amend the Commit

```bash
# Amend without changing message
git commit --amend --no-edit

# OR amend with new message
git commit --amend -m "New commit message"

# OR amend and open editor for message
git commit --amend
```

### Step 5: Verify Result

```bash
# Show the amended commit
git log -1 --stat

# Verify files are as expected
git show --name-only HEAD
```

## Common Scenarios

### Scenario 1: Add Forgotten File to Last Commit

```bash
# User: "I forgot to add config.json to the last commit"

# 1. Check it's safe to amend
git log -1 --format='%an %ae'  # Verify authorship
git status | grep ahead  # Verify not pushed

# 2. Stage only the forgotten file
git add config.json

# 3. Amend
git commit --amend --no-edit

# 4. Verify
git show --name-only HEAD
```

### Scenario 2: Amend Specific File (User Request)

```bash
# User: "Amend shrink-doc.md in commit 55e28bf"

# 1. Verify HEAD is the target commit
git log -1 --oneline
# Output: 55e28bf [config] Redesign shrink-doc...

# 2. Check safety
git log -1 --format='%an %ae'

# 3. Stage ONLY shrink-doc.md (even if other files modified)
git status --short
# M .claude/commands/shrink-doc.md
# M CLAUDE.md  ← Do NOT add this!

git add .claude/commands/shrink-doc.md  # Only specified file

# 4. Amend
git commit --amend --no-edit
```

### Scenario 3: Fix Pre-commit Hook Changes

```bash
# Pre-commit hook modified files, need to include in commit

# 1. See what hook changed
git status --short
git diff

# 2. Stage hook-modified files
git add -A  # Usually safe for hook changes

# 3. Amend
git commit --amend --no-edit
```

### Scenario 4: Fix Commit Message Only

```bash
# User: "Fix the typo in the last commit message"

# No staging needed - just amend message
git commit --amend -m "Corrected commit message"
```

## Amending Non-HEAD Commits

**When the target commit is NOT HEAD**, use the fixup + autosquash workflow.

### Why This Workflow?

- Cannot use `git rebase -i` interactively (requires terminal input)
- Simple `--autosquash` alone doesn't work reliably
- Must use `GIT_SEQUENCE_EDITOR` to automate the rebase sequence

### Step-by-Step Workflow

```bash
# 1. Identify the target commit and verify it's not HEAD
TARGET_COMMIT="b5ea793"
git log -1 --format='%H' HEAD  # Compare with target

# 2. Make your changes to the file(s)
# (edit files as needed)

# 3. Create a fixup commit targeting the old commit
git add <specific-files>
git commit --fixup=$TARGET_COMMIT

# 4. Find the parent of target commit (rebase base)
git log --oneline $TARGET_COMMIT~1 -1  # This is the rebase base

# 5. Run autosquash rebase with automated sequence editor
GIT_SEQUENCE_EDITOR="sed -i 's/^pick \([a-f0-9]*\) fixup!/fixup \1 fixup!/'" \
  git rebase -i --autosquash $TARGET_COMMIT~1

# 6. Verify the result
git log --oneline -5
git show <new-commit-hash> --stat
```

### Common Mistakes to Avoid

❌ **WRONG - Using wrong rebase base**:
```bash
# Target is b5ea793, but rebase from HEAD~1
GIT_SEQUENCE_EDITOR=: git rebase --autosquash HEAD~1
# Result: Fixup not applied to correct commit
```

✅ **CORRECT - Rebase from target's parent**:
```bash
# Target is b5ea793, rebase from b5ea793~1
GIT_SEQUENCE_EDITOR="sed -i 's/^pick \([a-f0-9]*\) fixup!/fixup \1 fixup!/'" \
  git rebase -i --autosquash b5ea793~1
```

❌ **WRONG - Soft reset with multiple commits ahead**:
```bash
# Multiple commits between target and HEAD
git reset --soft $TARGET_COMMIT~1  # Stages ALL changes from multiple commits!
# Result: Difficult to separate which changes belong to which commit
```

✅ **CORRECT - Use fixup workflow**:
```bash
# Preserves intermediate commits, only modifies target
git commit --fixup=$TARGET_COMMIT
# Then autosquash rebase
```

### Example: Amend File in Old Commit

```bash
# User: "Copy CLAUDE.md from commit 55e28bf to b5ea793"

# 1. Verify b5ea793 is not HEAD
git log -1 --format='%H' HEAD
# Output: 7e1ed90...  (different from b5ea793)

# 2. Restore the file content
git show 55e28bf:CLAUDE.md > CLAUDE.md

# 3. Create fixup commit
git add CLAUDE.md
git commit --fixup=b5ea793

# 4. Autosquash into target (rebase from b5ea793's parent)
GIT_SEQUENCE_EDITOR="sed -i 's/^pick \([a-f0-9]*\) fixup!/fixup \1 fixup!/'" \
  git rebase -i --autosquash b5ea793~1

# 5. Verify
git log --oneline -3
grep -c "expected content" CLAUDE.md
```

## Safety Checks Summary

| Check | Command | Action if Failed |
|-------|---------|------------------|
| Authorship | `git log -1 --format='%an'` | Ask permission or new commit |
| Not pushed | `git status \| grep ahead` | Warn about force push |
| Not merge | `git cat-file -p HEAD` | Consider not amending |
| Correct commit | `git log -1 --oneline` | Verify or use rebase |

## Anti-Patterns

### ❌ Staging All Modified Files

```bash
# User: "Amend foo.md"
git add .  # WRONG: Adds everything
git add -A  # WRONG: Adds everything
git add foo.md bar.md  # WRONG: Added unrequested file
```

### ❌ Amending Pushed Commits Without Warning

```bash
# Commit already pushed
git commit --amend  # Will require force push!
# MUST warn user first
```

### ❌ Amending Others' Commits

```bash
# Commit by "Jane Developer"
git commit --amend  # Changes authorship attribution
# Ask permission first
```

### ❌ Amending Merge Commits

```bash
# Merge commit with multiple parents
git commit --amend  # Can cause issues
# Usually better to create new commit
```

## Quick Reference

```bash
# Safe amend workflow
git log -1 --format='%an %ae'          # 1. Check author
git status | grep ahead                 # 2. Check not pushed
git add <specific-files-only>          # 3. Stage selectively
git commit --amend --no-edit           # 4. Amend
git log -1 --stat                      # 5. Verify
```

## Related Skills

- **git-commit**: Commit message guidelines
- **git-squash**: Combining multiple commits into one
- **git-rebase**: Reordering, splitting, or complex history editing
