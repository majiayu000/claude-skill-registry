---
description: Common git operations including branch management and status checks
triggers:
  - create branch
  - switch branch
  - git status summary
  - new branch
  - checkout branch
  - git workflow
  - branch status
---

# Git Workflow Helper

Common git operations for working with INAV repositories.

## 🚨 Read Git Guidelines First

**Before any git commit operation, read:** `claude/developer/guides/CRITICAL-BEFORE-COMMIT.md`

This checklist covers:
- Never use `git add -A`
- Human review of commit messages
- Commit message format and best practices
- When to use (and not use) `--amend`
- Hook handling

**Read it now using the Read tool when performing commit operations.**

---

## ⚠️ CRITICAL: Git Safety Rules ⚠️

### Questions Are Not Commands

**When the user asks a question, ONLY answer the question.**
- Do NOT take any action (delete, push, modify, etc.)
- Do NOT "fix" things while explaining them
- Do NOT assume you know what action should follow
- WAIT for explicit instructions before doing anything

### Never Destroy Evidence During Investigation

**When investigating a problem or answering questions about repository state:**
- Do NOT delete branches, tags, or commits
- Do NOT push, force-push, or overwrite anything
- Do NOT "clean up" anything
- PRESERVE the current state so it can be examined
- The evidence is needed to understand and fix the problem

### Never Alter the Public Record

**Once something is pushed to a public/shared repository:**
- It becomes part of the permanent record
- Other developers around the world may have fetched it
- Altering it (force push, amend+push) creates problems for EVERYONE
- It breaks other developers' local repositories
- It corrupts CI/CD pipelines, PR references, and git history
- The damage is often irreversible and far-reaching

**Force pushing after a PR is merged corrupts GitHub's PR display:**
- GitHub's "Files changed" tab shows the diff between base and the CURRENT branch head
- If you force push after merge, the PR now shows DIFFERENT code than what was actually merged
- Example: PR #2496 actually merged an `afterCopy` hook, but after force push GitHub shows `postPackage`
- Anyone reviewing the PR history sees FALSE information about what was merged
- This makes debugging, auditing, and understanding project history impossible
- The merge commit in master contains the ORIGINAL code, but the PR display shows the AMENDED code
- This is a permanent corruption of the project's historical record

### Force Push Rules

**NEVER, EVER force push to master, main, or any shared branch:**

```bash
# ❌ ABSOLUTELY FORBIDDEN - NEVER DO THIS:
git push -f origin master
git push --force origin main
git push -f upstream master

# These commands DESTROY other people's work permanently
# They rewrite history and can cause unrecoverable data loss
```

**If a regular push is rejected:**
1. STOP immediately
2. Do `git pull` to merge remote changes
3. Or ask the user what to do
4. NEVER use force push to "fix" it

**Force push is ONLY acceptable:**
- On your own feature branches that nobody else uses
- When explicitly requested by the user
- NEVER on master/main/shared branches under any circumstances

## 🔒 Sandbox Restrictions

**Claude Code runs in a sandbox that restricts network access:**

- Git operations requiring network (fetch, pull, push) may fail with "Network is unreachable" or "Connection refused"
- This is NOT a network outage - it's the sandbox blocking unapproved network operations
- SSH to github.com (port 22) is in the allowed list but may require permission prompts
- If git fetch/pull/push fails, the user needs to approve the network operation or run it manually

**When you see network errors:**
1. Don't assume the network is down
2. Recognize it as a sandbox restriction
3. Ask the user if they want to approve the operation or handle it manually
4. The user can run git commands directly (unsandboxed) if needed

## Repository Structure

The INAV project consists of **three standalone repositories**:
- `inav/` - Flight controller firmware (C/C99)
- `inav-configurator/` - Desktop GUI (JavaScript/Electron)
- `inavwiki/` - Documentation (Markdown)

Each repository has its own git history and must be managed independently.

## Creating Branches

### 🚨 CRITICAL: Always Specify Base Branch When Creating Branches

**NEVER create a branch without specifying the base branch:**

```bash
# ❌ WRONG - branches from current HEAD (may include unrelated changes)
git checkout -b my-new-branch

# ✅ CORRECT - explicitly specify base branch
git checkout -b my-new-branch upstream/maintenance-9.x
```

**Why this matters:** Creating a branch without specifying the base will branch from whatever you currently have checked out, which may include:
- Unrelated commits from another feature branch
- Work-in-progress changes
- The wrong base branch entirely
- This leads to PRs contaminated with unrelated changes

### Create a New Branch - Correct Commands

**First, verify you're not on a production branch:**
```bash
git branch --show-current
# Output should NOT be: secure_01, master, main, maintenance-9.x, maintenance-10.x
```

**For PrivacyLRS (secure_01 base):**
```bash
# Branch from secure_01 (the base branch for PrivacyLRS)
git checkout -b your-branch-name secure_01

# Push branch to remote
git push -u origin your-branch-name

# Branch naming: NO slashes (use: encryption-test-suite, fix-counter-sync)
```

**For INAV/inav-configurator (maintains backward compatibility):**
```bash
# Branch from maintenance-9.x (most common case)
git checkout -b your-branch-name upstream/maintenance-9.x

# Push branch to remote
git push -u origin your-branch-name

# Branch naming: kebab-case (use: fix-telemetry-bug, feature-battery-limit)
```

**For INAV/inav-configurator (breaking changes):**
```bash
# Branch from maintenance-10.x (MSP protocol changes, settings structure changes, etc.)
git checkout -b your-branch-name upstream/maintenance-10.x

# Push branch to remote
git push -u origin your-branch-name
```

**NEVER target PRs to master** - it receives merges only (maintenance-9.x → master → maintenance-10.x).

### Create Branch from Specific Commit

```bash
# Create branch from specific commit
git checkout -b bugfix-123 <commit-hash>

# Or from a tag
git checkout -b new-feature v9.0.0
```

### Branch Naming Conventions

**PrivacyLRS:**
- Use flat naming WITHOUT slashes
- ✅ Good: `encryption-test-suite`, `fix-counter-sync`, `add-telemetry`
- ❌ Bad: `feature/encryption-tests`, `security/fixes`

**INAV:**
- Use kebab-case with descriptive names
- ✅ Good: `fix-telemetry-bug`, `feature-battery-limit`, `update-sitl-binary`
- Bug fixes: `fix-<description>`
- Features: `feature-<description>`

## Switching Branches

### Safe Branch Switching

Always check for uncommitted changes before switching:

```bash
# Check status first
git status

# If clean, switch branches
git checkout <branch-name>

# Or use switch
git switch <branch-name>
```

### Handling Uncommitted Changes

If you have uncommitted changes:

**Option 1: Stash changes**
```bash
git stash save "WIP: description of changes"
git checkout <branch-name>

# Later, restore changes
git stash pop
```

**Option 2: Commit changes**
```bash
git add .
git commit -m "WIP: save progress"
git checkout <branch-name>
```

**Option 3: Discard changes (careful!)**
```bash
git checkout -- .  # Discard all changes
git checkout <branch-name>
```

## Git Status Summary

### Quick Status Check

```bash
# Basic status
git status

# Short format
git status -s

# Show branch and tracking info
git status -sb
```

### Comprehensive Status

Get a complete picture of your repository:

```bash
# Branch information
echo "=== Current Branch ==="
git branch --show-current

# Status
echo "=== Working Tree Status ==="
git status

# Commits ahead/behind remote
echo "=== Remote Tracking ==="
git status -sb | head -1

# Recent commits
echo "=== Recent Commits ==="
git log --oneline -5

# Staged changes
echo "=== Staged Changes ==="
git diff --cached --stat

# Unstaged changes
echo "=== Unstaged Changes ==="
git diff --stat
```

## Branch Management

### List Branches

```bash
# Local branches
git branch

# Remote branches
git branch -r

# All branches with last commit
git branch -v

# All branches including remote
git branch -a
```

### Delete Branches

```bash
# Delete local branch (safe - only if merged)
git branch -d <branch-name>

# Force delete local branch
git branch -D <branch-name>

# Delete remote branch
git push origin --delete <branch-name>
```

### Rename Branch

```bash
# Rename current branch
git branch -m <new-name>

# Rename specific branch
git branch -m <old-name> <new-name>

# Update remote
git push origin -u <new-name>
git push origin --delete <old-name>
```

## Checking Branch Status

### Compare with Remote

```bash
# Fetch latest from remote
git fetch origin

# Check if branch is ahead/behind
git status

# See commits not pushed
git log origin/<branch-name>..<branch-name>

# See commits not pulled
git log <branch-name>..origin/<branch-name>
```

### Compare with Other Branches

```bash
# See commits in current branch not in master
git log master..HEAD

# See files changed between branches
git diff master..HEAD --stat

# Show branch divergence
git log --oneline --graph --all --decorate -10
```

## Working with Multiple Repositories

Since `inav/`, `inav-configurator/`, and `inavwiki/` are standalone repos:

### Check Status Across All Repos

```bash
# From project root
for repo in inav inav-configurator inavwiki; do
  if [ -d "$repo" ]; then
    echo "=== $repo ==="
    cd $repo
    git status -sb
    cd ..
    echo ""
  fi
done
```

### Create Matching Branches

If working on a feature that spans multiple repos:

```bash
# Firmware
cd inav
git checkout -b my-feature
git push -u origin my-feature

# Configurator
cd ../inav-configurator
git checkout -b my-feature
git push -u origin my-feature

# Documentation
cd ../inavwiki
git checkout -b my-feature
git push -u origin my-feature
```

## Common Workflows

### Starting New Feature

```bash
# 1. Ensure you're on master and up to date
git checkout master
git pull origin master

# 2. Create feature branch
git checkout -b my-feature

# 3. Make changes and commit
git add <files>
git commit -m "Add: initial implementation"

# 4. Push to remote
git push -u origin my-feature
```

### Updating Feature Branch with Latest Master

```bash
# Option 1: Rebase (cleaner history)
git checkout my-feature
git fetch origin
git rebase origin/master

# Option 2: Merge (preserves history)
git checkout my-feature
git fetch origin
git merge origin/master
```

### Switching Between Tasks

```bash
# Save current work
git stash save "WIP: current task description"

# Switch to other branch
git checkout other-branch

# Work on other task...

# Return to original branch
git checkout original-branch
git stash pop
```

## Troubleshooting

### Branch is Behind Remote

```bash
# Pull latest changes
git pull origin <branch-name>

# Or fetch and merge manually
git fetch origin
git merge origin/<branch-name>
```

### Branch Has Diverged

```bash
# View divergence
git status

# Option 1: Rebase your changes
git pull --rebase origin <branch-name>

# Option 2: Merge
git pull origin <branch-name>
```

### Accidentally Committed to Wrong Branch

```bash
# Move last commit to new branch
git checkout -b correct-branch
git checkout wrong-branch
git reset --hard HEAD~1
git checkout correct-branch
```

## Resources

- **Git basics:** `git --help`
- **Project workflow:** See `claude/manager/README.md` and `claude/developer/README.md`

---

## Related Skills

- **create-pr** - Create pull requests after committing changes
- **pr-review** - Review pull requests and check out PR branches
- **check-builds** - Check CI build status for branches and PRs
- **start-task** - Begin tasks with proper branch setup
- **finish-task** - Complete tasks with commits and cleanup
