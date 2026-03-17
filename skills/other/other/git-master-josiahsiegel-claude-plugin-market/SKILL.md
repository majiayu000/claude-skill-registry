---
name: git-master
description: "Complete Git expertise system for ALL git operations. PROACTIVELY activate for: (1) ANY Git task (basic/advanced/dangerous), (2) Repository management, (3) Branch strategies and workflows, (4) Conflict resolution, (5) History rewriting/recovery, (6) Platform-specific operations (GitHub/Azure DevOps/Bitbucket), (7) Advanced commands (rebase/cherry-pick/filter-repo). Provides: complete Git command reference, safety guardrails for destructive operations, platform best practices, workflow strategies, reflog recovery techniques, and expert guidance for even the most risky operations. Always asks user preference for automatic commits vs manual control."
---

# Git Mastery - Complete Git Expertise

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation



---

Comprehensive guide for ALL Git operations from basic to advanced, including dangerous operations with safety guardrails.

---

## TL;DR QUICK REFERENCE

**Safety First - Before ANY Destructive Operation:**
```bash
# ALWAYS check status first
git status
git log --oneline -10

# For risky operations, create a safety branch
git branch backup-$(date +%Y%m%d-%H%M%S)

# Remember: git reflog is your safety net (90 days default)
git reflog
```

**User Preference Check:**
- **ALWAYS ASK:** "Would you like me to create commits automatically, or would you prefer to handle commits manually?"
- Respect user's choice throughout the session

---

## Overview

This skill provides COMPLETE Git expertise for ANY Git operation, no matter how advanced, niche, or risky. It covers:

**MUST use this skill for:**
- ✅ ANY Git command or operation
- ✅ Repository initialization, cloning, configuration
- ✅ Branch management and strategies
- ✅ Commit workflows and best practices
- ✅ Merge strategies and conflict resolution
- ✅ Rebase operations (interactive and non-interactive)
- ✅ History rewriting (filter-repo, reset, revert)
- ✅ Recovery operations (reflog, fsck)
- ✅ Dangerous operations (force push, hard reset)
- ✅ Platform-specific workflows (GitHub, Azure DevOps, Bitbucket)
- ✅ Advanced features (submodules, worktrees, hooks)
- ✅ Performance optimization
- ✅ Cross-platform compatibility (Windows/Linux/macOS)

---

## Core Principles

### 1. Safety Guardrails for Destructive Operations

**CRITICAL: Before ANY destructive operation (reset --hard, force push, filter-repo, etc.):**

1. **Always warn the user explicitly**
2. **Explain the risks clearly**
3. **Ask for confirmation**
4. **Suggest creating a backup branch first**
5. **Provide recovery instructions**

```bash
# Example safety pattern for dangerous operations
echo "⚠️  WARNING: This operation is DESTRUCTIVE and will:"
echo "   - Permanently delete uncommitted changes"
echo "   - Rewrite Git history"
echo "   - [specific risks for the operation]"
echo ""
echo "Safety recommendation: Creating backup branch first..."
git branch backup-before-reset-$(date +%Y%m%d-%H%M%S)
echo ""
echo "To recover if needed: git reset --hard backup-before-reset-XXXXXXXX"
echo ""
read -p "Are you SURE you want to proceed? (yes/NO): " confirm
if [[ "$confirm" != "yes" ]]; then
    echo "Operation cancelled."
    exit 1
fi
```

### 2. Commit Creation Policy

**ALWAYS ASK at the start of ANY Git task:**
"Would you like me to:
1. Create commits automatically with appropriate messages
2. Stage changes only (you handle commits manually)
3. Just provide guidance (no automatic operations)"

Respect this choice throughout the session.

### 3. Platform Awareness

Git behavior and workflows differ across platforms and hosting providers:

**Windows (Git Bash/PowerShell):**
- Line ending handling (core.autocrlf)
- Path separators and case sensitivity
- Credential management (Windows Credential Manager)

**Linux/macOS:**
- Case-sensitive filesystems
- SSH key management
- Permission handling

**Hosting Platforms:**
- GitHub: Pull requests, GitHub Actions, GitHub CLI
- Azure DevOps: Pull requests, Azure Pipelines, policies
- Bitbucket: Pull requests, Bitbucket Pipelines, Jira integration
- GitLab: Merge requests, GitLab CI/CD

---

## Basic Git Operations

### Repository Initialization and Cloning

```bash
# Initialize new repository
git init
git init --initial-branch=main  # Specify default branch name

# Clone repository
git clone <url>
git clone <url> <directory>
git clone --depth 1 <url>  # Shallow clone (faster, less history)
git clone --branch <branch> <url>  # Clone specific branch
git clone --recurse-submodules <url>  # Include submodules
```

### Configuration

```bash
# User identity (required for commits)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Default branch name
git config --global init.defaultBranch main

# Line ending handling (Windows)
git config --global core.autocrlf true  # Windows
git config --global core.autocrlf input  # macOS/Linux

# Editor
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "vim"

# Diff tool
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'

# Merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# View configuration
git config --list
git config --global --list
git config --local --list
git config user.name  # Get specific value
```

### Basic Workflow

```bash
# Check status
git status
git status -s  # Short format
git status -sb  # Short with branch info

# Add files
git add <file>
git add .  # Add all changes in current directory
git add -A  # Add all changes in repository
git add -p  # Interactive staging (patch mode)

# Remove files
git rm <file>
git rm --cached <file>  # Remove from index, keep in working directory
git rm -r <directory>

# Move/rename files
git mv <old> <new>

# Commit
git commit -m "message"
git commit -am "message"  # Add and commit tracked files
git commit --amend  # Amend last commit
git commit --amend --no-edit  # Amend without changing message
git commit --allow-empty -m "message"  # Empty commit (useful for triggers)

# View history
git log
git log --oneline
git log --graph --oneline --all --decorate
git log --stat  # Show file statistics
git log --patch  # Show diffs
git log -p -2  # Show last 2 commits with diffs
git log --since="2 weeks ago"
git log --until="2025-01-01"
git log --author="Name"
git log --grep="pattern"
git log -- <file>  # History of specific file
git log --follow <file>  # Follow renames

# Show changes
git diff  # Unstaged changes
git diff --staged  # Staged changes
git diff HEAD  # All changes since last commit
git diff <branch>  # Compare with another branch
git diff <commit1> <commit2>
git diff <commit>  # Changes since specific commit
git diff <branch1>...<branch2>  # Changes between branches

# Show commit details
git show <commit>
git show <commit>:<file>  # Show file at specific commit
```

---

## Branch Management

### Creating and Switching Branches

```bash
# List branches
git branch  # Local branches
git branch -r  # Remote branches
git branch -a  # All branches
git branch -v  # With last commit info
git branch -vv  # With tracking info

# Create branch
git branch <branch-name>
git branch <branch-name> <start-point>  # From specific commit/tag

# Switch branch
git switch <branch-name>
git checkout <branch-name>  # Old syntax, still works

# Create and switch
git switch -c <branch-name>
git checkout -b <branch-name>
git switch -c <branch-name> <start-point>

# Delete branch
git branch -d <branch-name>  # Safe delete (only if merged)
git branch -D <branch-name>  # Force delete (even if not merged)

# Rename branch
git branch -m <old-name> <new-name>
git branch -m <new-name>  # Rename current branch

# Set upstream tracking
git branch --set-upstream-to=origin/<branch>
git branch -u origin/<branch>
```

### Branch Strategies

**Git Flow:**
- `main/master`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `release/*`: Release preparation
- `hotfix/*`: Production fixes

**GitHub Flow:**
- `main`: Always deployable
- `feature/*`: Short-lived feature branches
- Create PR, review, merge

**Trunk-Based Development:**
- `main`: Single branch
- Short-lived feature branches (< 1 day)
- Feature flags for incomplete features

**GitLab Flow:**
- Environment branches: `production`, `staging`, `main`
- Feature branches merge to `main`
- Deploy from environment branches

---

## Merging and Rebasing

### Merge Strategies

```bash
# Fast-forward merge (default if possible)
git merge <branch>

# Force merge commit (even if fast-forward possible)
git merge --no-ff <branch>

# Squash merge (combine all commits into one)
git merge --squash <branch>
# Then commit manually: git commit -m "Merged feature X"

# Merge with specific strategy
git merge -s recursive <branch>  # Default strategy
git merge -s ours <branch>  # Always use "our" version
git merge -s theirs <branch>  # Always use "their" version (requires merge-theirs)
git merge -s octopus <branch1> <branch2> <branch3>  # Merge multiple branches

# Merge with strategy options
git merge -X ours <branch>  # Prefer "our" changes in conflicts
git merge -X theirs <branch>  # Prefer "their" changes in conflicts
git merge -X ignore-all-space <branch>
git merge -X ignore-space-change <branch>

# Abort merge
git merge --abort

# Continue after resolving conflicts
git merge --continue
```

### Conflict Resolution

```bash
# When merge conflicts occur
git status  # See conflicted files

# Conflict markers in files:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> branch-name

# Resolve conflicts manually, then:
git add <resolved-file>
git commit  # Complete the merge

# Use mergetool
git mergetool

# Accept one side completely
git checkout --ours <file>  # Keep our version
git checkout --theirs <file>  # Keep their version
git add <file>

# View conflict diff
git diff  # Show conflicts
git diff --ours  # Compare with our version
git diff --theirs  # Compare with their version
git diff --base  # Compare with base version

# List conflicts
git diff --name-only --diff-filter=U
```

### Rebase Operations

**⚠️  WARNING: Rebase rewrites history. Never rebase commits that have been pushed to shared branches!**

```bash
# Basic rebase
git rebase <base-branch>
git rebase origin/main

# Interactive rebase (POWERFUL)
git rebase -i <base-commit>
git rebase -i HEAD~5  # Last 5 commits

# Interactive rebase commands:
# p, pick = use commit
# r, reword = use commit, but edit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like squash, but discard commit message
# x, exec = run command (rest of line) using shell
# b, break = stop here (continue rebase later with 'git rebase --continue')
# d, drop = remove commit
# l, label = label current HEAD with a name
# t, reset = reset HEAD to a label

# Rebase onto different base
git rebase --onto <new-base> <old-base> <branch>

# Continue after resolving conflicts
git rebase --continue

# Skip current commit
git rebase --skip

# Abort rebase
git rebase --abort

# Preserve merge commits
git rebase --preserve-merges <base>  # Deprecated
git rebase --rebase-merges <base>  # Modern approach

# Autosquash (with fixup commits)
git commit --fixup <commit>
git rebase -i --autosquash <base>
```

### Cherry-Pick

```bash
# Apply specific commit to current branch
git cherry-pick <commit>

# Cherry-pick multiple commits
git cherry-pick <commit1> <commit2>
git cherry-pick <commit1>..<commit5>

# Cherry-pick without committing
git cherry-pick -n <commit>
git cherry-pick --no-commit <commit>

# Continue after resolving conflicts
git cherry-pick --continue

# Abort cherry-pick
git cherry-pick --abort
```

---

## Remote Operations

### Remote Management

```bash
# List remotes
git remote
git remote -v  # With URLs

# Add remote
git remote add <name> <url>
git remote add origin https://github.com/user/repo.git

# Change remote URL
git remote set-url <name> <new-url>

# Remove remote
git remote remove <name>
git remote rm <name>

# Rename remote
git remote rename <old> <new>

# Show remote info
git remote show <name>
git remote show origin

# Prune stale remote branches
git remote prune origin
git fetch --prune
```

### Fetch and Pull

```bash
# Fetch from remote (doesn't merge)
git fetch
git fetch origin
git fetch --all  # All remotes
git fetch --prune  # Remove stale remote-tracking branches

# Pull (fetch + merge)
git pull
git pull origin <branch>
git pull --rebase  # Fetch + rebase instead of merge
git pull --no-ff  # Always create merge commit
git pull --ff-only  # Only if fast-forward possible

# Set default pull behavior
git config --global pull.rebase true  # Always rebase
git config --global pull.ff only  # Only fast-forward
```

### Push

```bash
# Push to remote
git push
git push origin <branch>
git push origin <local-branch>:<remote-branch>

# Push new branch and set upstream
git push -u origin <branch>
git push --set-upstream origin <branch>

# Push all branches
git push --all

# Push tags
git push --tags
git push origin <tag-name>

# Delete remote branch
git push origin --delete <branch>
git push origin :<branch>  # Old syntax

# Delete remote tag
git push origin --delete <tag>
git push origin :refs/tags/<tag>

# ⚠️ DANGEROUS: Force push (overwrites remote history)
# ALWAYS ASK USER FOR CONFIRMATION FIRST
git push --force
git push -f

# ⚠️ SAFER: Force push with lease (fails if remote updated)
git push --force-with-lease
git push --force-with-lease=<ref>:<expected-value>
```

**Force Push Safety Protocol:**

Before ANY force push, execute this safety check:

```bash
echo "⚠️  DANGER: Force push will overwrite remote history!"
echo ""
echo "Remote branch status:"
git fetch origin
git log --oneline origin/<branch> ^<branch> --decorate

if [ -z "$(git log --oneline origin/<branch> ^<branch>)" ]; then
    echo "✓ No commits will be lost (remote is behind local)"
else
    echo "❌ WARNING: Remote has commits that will be LOST:"
    git log --oneline --decorate origin/<branch> ^<branch>
    echo ""
    echo "These commits from other developers will be destroyed!"
fi

echo ""
echo "Consider using --force-with-lease instead of --force"
echo ""
read -p "Type 'force push' to confirm: " confirm
if [[ "$confirm" != "force push" ]]; then
    echo "Cancelled."
    exit 1
fi
```

---

## Advanced Commands

### Stash

```bash
# Stash changes
git stash
git stash save "message"
git stash push -m "message"

# Stash including untracked files
git stash -u
git stash --include-untracked

# Stash including ignored files
git stash -a
git stash --all

# List stashes
git stash list

# Show stash contents
git stash show
git stash show -p  # With diff
git stash show stash@{2}

# Apply stash (keep in stash list)
git stash apply
git stash apply stash@{2}

# Pop stash (apply and remove)
git stash pop
git stash pop stash@{2}

# Drop stash
git stash drop
git stash drop stash@{2}

# Clear all stashes
git stash clear

# Create branch from stash
git stash branch <branch-name>
git stash branch <branch-name> stash@{1}

# Git 2.51+ : Import/Export stashes (share stashes between machines)
# Export stash to a file
git stash store --file=stash.patch stash@{0}

# Import stash from a file
git stash import --file=stash.patch

# Share stashes like branches/tags
git stash export > my-stash.patch
git stash import < my-stash.patch
```

### Reset

**⚠️  WARNING: reset can permanently delete changes!**

```bash
# Soft reset (keep changes staged)
git reset --soft <commit>
git reset --soft HEAD~1  # Undo last commit, keep changes staged

# Mixed reset (default - keep changes unstaged)
git reset <commit>
git reset HEAD~1  # Undo last commit, keep changes unstaged

# ⚠️ HARD reset (DELETE all changes - DANGEROUS!)
# ALWAYS create backup branch first!
git branch backup-$(date +%Y%m%d-%H%M%S)
git reset --hard <commit>
git reset --hard HEAD~1  # Undo last commit and DELETE all changes
git reset --hard origin/<branch>  # Reset to remote state

# Unstage files
git reset HEAD <file>
git reset -- <file>

# Reset specific file to commit
git checkout <commit> -- <file>
```

### Revert

```bash
# Revert commit (creates new commit that undoes changes)
# Safer than reset for shared branches
git revert <commit>

# Revert without creating commit
git revert -n <commit>
git revert --no-commit <commit>

# Revert merge commit
git revert -m 1 <merge-commit>  # Keep first parent
git revert -m 2 <merge-commit>  # Keep second parent

# Revert multiple commits
git revert <commit1> <commit2>
git revert <commit1>..<commit5>

# Continue after resolving conflicts
git revert --continue

# Abort revert
git revert --abort
```

### Reflog (Recovery)

**reflog is your safety net - it tracks all HEAD movements for 90 days (default)**

```bash
# View reflog
git reflog
git reflog show
git reflog show <branch>

# More detailed reflog
git log -g  # Reflog as log
git log -g --all

# Find lost commits
git reflog --all
git fsck --lost-found

# Recover deleted branch
git reflog  # Find commit where branch existed
git branch <branch-name> <commit-hash>

# Recover from hard reset
git reflog  # Find commit before reset
git reset --hard <commit-hash>

# Recover deleted commits
git cherry-pick <commit-hash>

# Reflog expiration (change retention)
git config gc.reflogExpire "90 days"
git config gc.reflogExpireUnreachable "30 days"
```

### Bisect (Find Bad Commits)

```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good <commit>

# Test each commit, then mark as good or bad
git bisect good  # Current commit is good
git bisect bad   # Current commit is bad

# Automate with test script
git bisect run <test-script>

# Bisect shows the first bad commit

# Finish bisect
git bisect reset

# Skip commit if unable to test
git bisect skip
```

### Clean

**⚠️  WARNING: clean permanently deletes untracked files!**

```bash
# Show what would be deleted (dry run - ALWAYS do this first!)
git clean -n
git clean --dry-run

# Delete untracked files
git clean -f

# Delete untracked files and directories
git clean -fd

# Delete untracked and ignored files
git clean -fdx

# Interactive clean
git clean -i
```

### Worktrees

```bash
# List worktrees
git worktree list

# Add new worktree
git worktree add <path> <branch>
git worktree add ../project-feature feature-branch

# Add worktree for new branch
git worktree add -b <new-branch> <path>

# Remove worktree
git worktree remove <path>

# Prune stale worktrees
git worktree prune
```

### Submodules

```bash
# Add submodule
git submodule add <url> <path>

# Initialize submodules (after clone)
git submodule init
git submodule update

# Clone with submodules
git clone --recurse-submodules <url>

# Update submodules
git submodule update --remote
git submodule update --init --recursive

# Execute command in all submodules
git submodule foreach <command>
git submodule foreach git pull origin main

# Remove submodule
git submodule deinit <path>
git rm <path>
rm -rf .git/modules/<path>
```

---

## Dangerous Operations (High Risk)

### Filter-Repo (History Rewriting)

**⚠️  EXTREMELY DANGEROUS: Rewrites entire repository history!**

```bash
# Install git-filter-repo (not built-in)
# pip install git-filter-repo

# Remove file from all history
git filter-repo --path <file> --invert-paths

# Remove directory from all history
git filter-repo --path <directory> --invert-paths

# Change author info
git filter-repo --name-callback 'return name.replace(b"Old Name", b"New Name")'
git filter-repo --email-callback 'return email.replace(b"old@email.com", b"new@email.com")'

# Remove large files
git filter-repo --strip-blobs-bigger-than 10M

# ⚠️ After filter-repo, force push required
git push --force --all
git push --force --tags
```

**Safety protocol for filter-repo:**

```bash
echo "⚠️⚠️⚠️  EXTREME DANGER  ⚠️⚠️⚠️"
echo "This operation will:"
echo "  - Rewrite ENTIRE repository history"
echo "  - Change ALL commit hashes"
echo "  - Break all existing clones"
echo "  - Require all team members to re-clone"
echo "  - Cannot be undone after force push"
echo ""
echo "MANDATORY: Create full backup:"
git clone --mirror <repo-url> backup-$(date +%Y%m%d-%H%M%S)
echo ""
echo "Notify ALL team members before proceeding!"
echo ""
read -p "Type 'I UNDERSTAND THE RISKS' to continue: " confirm
if [[ "$confirm" != "I UNDERSTAND THE RISKS" ]]; then
    echo "Cancelled."
    exit 1
fi
```

### Amend Pushed Commits

**⚠️  DANGER: Changing pushed commits requires force push!**

```bash
# Amend last commit
git commit --amend

# Amend without changing message
git commit --amend --no-edit

# Change author of last commit
git commit --amend --author="Name <email>"

# ⚠️ Force push required if already pushed
git push --force-with-lease
```

### Rewrite Multiple Commits

**⚠️  DANGER: Interactive rebase on pushed commits!**

```bash
# Interactive rebase
git rebase -i HEAD~5

# Change author of older commits
git rebase -i <commit>^
# Mark commit as "edit"
# When stopped:
git commit --amend --author="Name <email>" --no-edit
git rebase --continue

# ⚠️ Force push required
git push --force-with-lease
```

---

## Platform-Specific Workflows

### GitHub

**Pull Requests:**
```bash
# Install GitHub CLI
# https://cli.github.com/

# Create PR
gh pr create
gh pr create --title "Title" --body "Description"
gh pr create --base main --head feature-branch

# List PRs
gh pr list

# View PR
gh pr view
gh pr view <number>

# Check out PR locally
gh pr checkout <number>

# Review PR
gh pr review
gh pr review --approve
gh pr review --request-changes
gh pr review --comment

# Merge PR
gh pr merge
gh pr merge --squash
gh pr merge --rebase
gh pr merge --merge

# Close PR
gh pr close <number>
```

**GitHub Actions:**
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
```

### Azure DevOps

**Pull Requests:**
```bash
# Install Azure DevOps CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Create PR
az repos pr create --title "Title" --description "Description"
az repos pr create --source-branch feature --target-branch main

# List PRs
az repos pr list

# View PR
az repos pr show --id <id>

# Complete PR
az repos pr update --id <id> --status completed

# Branch policies
az repos policy list
az repos policy create --config policy.json
```

**Azure Pipelines:**
```yaml
# azure-pipelines.yml
trigger:
  - main
pool:
  vmImage: 'ubuntu-latest'
steps:
  - script: npm test
    displayName: 'Run tests'
```

### Bitbucket

**Pull Requests:**
```bash
# Create PR (via web or Bitbucket CLI)
bb pr create

# Review PR
bb pr list
bb pr view <id>

# Merge PR
bb pr merge <id>
```

**Bitbucket Pipelines:**
```yaml
# bitbucket-pipelines.yml
pipelines:
  default:
    - step:
        script:
          - npm test
```

### GitLab

**Merge Requests:**
```bash
# Install GitLab CLI (glab)
# https://gitlab.com/gitlab-org/cli

# Create MR
glab mr create
glab mr create --title "Title" --description "Description"

# List MRs
glab mr list

# View MR
glab mr view <id>

# Merge MR
glab mr merge <id>

# Close MR
glab mr close <id>
```

**GitLab CI:**
```yaml
# .gitlab-ci.yml
stages:
  - test
test:
  stage: test
  script:
    - npm test
```

---

## Performance Optimization

### Repository Maintenance

```bash
# Garbage collection
git gc
git gc --aggressive  # More thorough, slower

# Prune unreachable objects
git prune

# Verify repository
git fsck
git fsck --full

# Optimize repository
git repack -a -d --depth=250 --window=250

# Git 2.51+: Path-walk repacking (generates smaller packs)
# More efficient delta compression by walking paths
git repack --path-walk -a -d

# Count objects
git count-objects -v

# Repository size
du -sh .git
```

### Large Files

```bash
# Find large files in history
git rev-list --objects --all |
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
  sed -n 's/^blob //p' |
  sort --numeric-sort --key=2 |
  tail -n 10

# Git LFS (Large File Storage)
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"
git add .gitattributes
git add file.psd
git commit -m "Add large file"

# List LFS files
git lfs ls-files

# Fetch LFS files
git lfs fetch
git lfs pull
```

### Shallow Clones

```bash
# Shallow clone (faster, less disk space)
git clone --depth 1 <url>

# Unshallow (convert to full clone)
git fetch --unshallow

# Fetch more history
git fetch --depth=100
```

---

## Tags and Releases

### Creating Tags

```bash
# Lightweight tag
git tag <tag-name>
git tag v1.0.0

# Annotated tag (recommended - includes metadata)
git tag -a <tag-name> -m "message"
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tag specific commit
git tag -a <tag-name> <commit>

# Signed tag (GPG signature)
git tag -s <tag-name> -m "message"
```

### Managing Tags

```bash
# List tags
git tag
git tag -l "v1.*"  # Pattern matching

# Show tag info
git show <tag-name>

# Delete local tag
git tag -d <tag-name>

# Delete remote tag
git push origin --delete <tag-name>
git push origin :refs/tags/<tag-name>

# Push tags
git push origin <tag-name>
git push --tags  # All tags
git push --follow-tags  # Only annotated tags
```

---

## Git Hooks

### Client-Side Hooks

```bash
# Hooks location: .git/hooks/

# pre-commit: Run before commit
# Example: .git/hooks/pre-commit
#!/bin/bash
npm run lint || exit 1

# prepare-commit-msg: Edit commit message before editor opens
# commit-msg: Validate commit message
#!/bin/bash
msg=$(cat "$1")
if ! echo "$msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore):"; then
    echo "Error: Commit message must start with type (feat|fix|docs|...):"
    exit 1
fi

# post-commit: Run after commit
# pre-push: Run before push
# post-checkout: Run after checkout
# post-merge: Run after merge

# Make hook executable
chmod +x .git/hooks/pre-commit
```

### Server-Side Hooks

```bash
# pre-receive: Run before refs are updated
# update: Run for each branch being updated
# post-receive: Run after refs are updated

# Example: Reject force pushes
#!/bin/bash
while read oldrev newrev refname; do
    if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
        if ! git merge-base --is-ancestor "$oldrev" "$newrev"; then
            echo "Error: Force push rejected"
            exit 1
        fi
    fi
done
```

---

## Troubleshooting and Recovery

### Common Problems

**Detached HEAD:**
```bash
# You're in detached HEAD state
git branch temp  # Create branch at current commit
git switch main
git merge temp
git branch -d temp
```

**Merge conflicts:**
```bash
# During merge/rebase
git status  # See conflicted files
# Edit files to resolve conflicts
git add <resolved-files>
git merge --continue  # or git rebase --continue

# Abort and start over
git merge --abort
git rebase --abort
```

**Accidentally deleted branch:**
```bash
# Find branch in reflog
git reflog
# Create branch at commit
git branch <branch-name> <commit-hash>
```

**Committed to wrong branch:**
```bash
# Move commit to correct branch
git switch correct-branch
git cherry-pick <commit>
git switch wrong-branch
git reset --hard HEAD~1  # Remove from wrong branch
```

**Pushed sensitive data:**
```bash
# ⚠️ URGENT: Remove from history immediately
git filter-repo --path <sensitive-file> --invert-paths
git push --force --all
# Then: Rotate compromised credentials immediately!
```

**Large commit by mistake:**
```bash
# Before pushing
git reset --soft HEAD~1
git reset HEAD <large-file>
git commit -m "message"

# After pushing - use filter-repo or BFG
```

### Recovery Scenarios

**Recover after hard reset:**
```bash
git reflog
git reset --hard <commit-before-reset>
```

**Recover deleted file:**
```bash
git log --all --full-history -- <file>
git checkout <commit>^ -- <file>
```

**Recover deleted commits:**
```bash
git reflog  # Find commit hash
git cherry-pick <commit>
# or
git merge <commit>
# or
git reset --hard <commit>
```

**Recover from corrupted repository:**
```bash
# Verify corruption
git fsck --full

# Attempt repair
git gc --aggressive

# Last resort: clone from remote
```

---

## Best Practices

### Commit Messages

**Conventional Commits format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Example:**
```
feat(auth): add OAuth2 authentication

Implement OAuth2 flow for Google and GitHub providers.
Includes token refresh and revocation.

Closes #123
```

### Branching Best Practices

1. **Keep branches short-lived** (< 2 days ideal)
2. **Use descriptive names**: `feature/user-auth`, `fix/header-crash`
3. **One purpose per branch**
4. **Rebase before merge** to keep history clean
5. **Delete merged branches**

### Workflow Best Practices

1. **Commit often** (small, logical chunks)
2. **Pull before push** (stay up to date)
3. **Review before commit** (`git diff --staged`)
4. **Write meaningful messages**
5. **Test before commit**
6. **Never commit secrets** (use `.gitignore`, environment variables)

### .gitignore Best Practices

```gitignore
# Environment files
.env
.env.local
*.env

# Dependencies
node_modules/
vendor/
venv/

# Build outputs
dist/
build/
*.exe
*.dll
*.so

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp
```

---

## Security Best Practices

### Credential Management

```bash
# Store credentials (cache for 1 hour)
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'

# Store credentials (permanent - use with caution)
git config --global credential.helper store

# Windows: Use Credential Manager
git config --global credential.helper wincred

# macOS: Use Keychain
git config --global credential.helper osxkeychain

# Linux: Use libsecret
git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret
```

### SSH Keys

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"  # If ed25519 not supported

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key to ssh-agent
ssh-add ~/.ssh/id_ed25519

# Test connection
ssh -T git@github.com
ssh -T git@ssh.dev.azure.com
```

### GPG Signing

```bash
# Generate GPG key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format LONG

# Configure Git to sign commits
git config --global user.signingkey <key-id>
git config --global commit.gpgsign true

# Sign commits
git commit -S -m "message"

# Verify signatures
git log --show-signature
```

### Preventing Secrets

```bash
# Git-secrets (AWS tool)
git secrets --install
git secrets --register-aws

# Gitleaks
gitleaks detect

# Pre-commit hook
#!/bin/bash
if git diff --cached | grep -E "(password|secret|api_key)" ; then
    echo "Potential secret detected!"
    exit 1
fi
```

---

## Cross-Platform Considerations

### Line Endings

```bash
# Windows (CRLF in working directory, LF in repository)
git config --global core.autocrlf true

# macOS/Linux (LF everywhere)
git config --global core.autocrlf input

# No conversion (not recommended)
git config --global core.autocrlf false

# Use .gitattributes for consistency
# .gitattributes:
* text=auto
*.sh text eol=lf
*.bat text eol=crlf
```

### Case Sensitivity

```bash
# macOS/Windows: Case-insensitive filesystems
# Linux: Case-sensitive filesystem

# Enable case sensitivity in Git
git config --global core.ignorecase false

# Rename file (case-only change)
git mv --force myfile.txt MyFile.txt
```

### Path Handling

```bash
# Git always uses forward slashes internally
# Works on all platforms:
git add src/components/Header.jsx

# Windows-specific tools may need backslashes in some contexts
```

### Git Bash / MINGW Path Conversion (Windows)

**CRITICAL: Git Bash is the primary Git environment on Windows!**

Git Bash (MINGW/MSYS2) automatically converts Unix-style paths to Windows paths for native executables, which can cause issues with Git operations.

**Path Conversion Behavior:**
```bash
# Automatic conversions that occur:
/foo          → C:/Program Files/Git/usr/foo
/foo:/bar     → C:\msys64\foo;C:\msys64\bar
--dir=/foo    → --dir=C:/msys64/foo

# What triggers conversion:
# ✓ Leading forward slash (/) in arguments
# ✓ Colon-separated path lists
# ✓ Arguments after - or , with path components

# What's exempt from conversion:
# ✓ Arguments containing = (variable assignments)
# ✓ Drive specifiers (C:)
# ✓ Arguments with ; (already Windows format)
# ✓ Arguments starting with // (Windows switches)
```

**Controlling Path Conversion:**

```bash
# Method 1: MSYS_NO_PATHCONV (Git for Windows only)
# Disable ALL path conversion for a command
MSYS_NO_PATHCONV=1 git command --option=/path

# Permanently disable (use with caution - can break scripts)
export MSYS_NO_PATHCONV=1

# Method 2: MSYS2_ARG_CONV_EXCL (MSYS2)
# Exclude specific argument patterns
export MSYS2_ARG_CONV_EXCL="*"              # Exclude everything
export MSYS2_ARG_CONV_EXCL="--dir=;/test"  # Specific prefixes

# Method 3: Manual conversion with cygpath
cygpath -u "C:\path"     # → Unix format: /c/path
cygpath -w "/c/path"     # → Windows format: C:\path
cygpath -m "/c/path"     # → Mixed format: C:/path

# Method 4: Workarounds
# Use double slashes: //e //s instead of /e /s
# Use dash notation: -e -s instead of /e /s
# Quote paths with spaces: "/c/Program Files/file.txt"
```

**Shell Detection in Git Workflows:**

```bash
# Method 1: $MSYSTEM (Most Reliable for Git Bash)
case "$MSYSTEM" in
  MINGW64)  echo "Git Bash 64-bit" ;;
  MINGW32)  echo "Git Bash 32-bit" ;;
  MSYS)     echo "MSYS environment" ;;
esac

# Method 2: uname -s (Portable)
case "$(uname -s)" in
  MINGW64_NT*)  echo "Git Bash 64-bit" ;;
  MINGW32_NT*)  echo "Git Bash 32-bit" ;;
  MSYS_NT*)     echo "MSYS" ;;
  CYGWIN*)      echo "Cygwin" ;;
  Darwin*)      echo "macOS" ;;
  Linux*)       echo "Linux" ;;
esac

# Method 3: $OSTYPE (Bash-only, fast)
case "$OSTYPE" in
  msys*)       echo "Git Bash/MSYS" ;;
  cygwin*)     echo "Cygwin" ;;
  darwin*)     echo "macOS" ;;
  linux-gnu*)  echo "Linux" ;;
esac
```

**Git Bash Path Issues & Solutions:**

```bash
# Issue: Git commands with paths fail in Git Bash
# Example: git log --follow /path/to/file fails

# Solution 1: Use relative paths
git log --follow ./path/to/file

# Solution 2: Disable path conversion
MSYS_NO_PATHCONV=1 git log --follow /path/to/file

# Solution 3: Use Windows-style paths
git log --follow C:/path/to/file

# Issue: Spaces in paths (Program Files)
# Solution: Always quote paths
git add "/c/Program Files/project/file.txt"

# Issue: Drive letter duplication (D:\dev → D:\d\dev)
# Solution: Use cygpath for conversion
file=$(cygpath -u "D:\dev\file.txt")
git add "$file"
```

**Git Bash Best Practices:**

1. **Always use forward slashes in Git commands** - Git handles them on all platforms
2. **Quote paths with spaces** - Essential in Git Bash
3. **Use relative paths when possible** - Avoids conversion issues
4. **Detect shell environment** - Use $MSYSTEM for Git Bash detection
5. **Test scripts on Git Bash** - Primary Windows Git environment
6. **Use MSYS_NO_PATHCONV selectively** - Only when needed, not globally

---

## Success Criteria

A Git workflow using this skill should:

1. ✓ ALWAYS ask user preference for automatic commits vs manual
2. ✓ ALWAYS warn before destructive operations
3. ✓ ALWAYS create backup branches before risky operations
4. ✓ ALWAYS explain recovery procedures
5. ✓ Use appropriate branch strategy for the project
6. ✓ Write meaningful commit messages
7. ✓ Keep commit history clean and linear
8. ✓ Never commit secrets or large binary files
9. ✓ Test code before committing
10. ✓ Know how to recover from any mistake

---

## Emergency Recovery Reference

**Quick recovery commands:**

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo changes to file
git checkout -- <file>

# Recover deleted branch
git reflog
git branch <name> <commit>

# Undo force push (if recent)
git reflog
git reset --hard <commit-before-push>
git push --force-with-lease

# Recover from hard reset
git reflog
git reset --hard <commit-before-reset>

# Find lost commits
git fsck --lost-found
git reflog --all

# Recover deleted file
git log --all --full-history -- <file>
git checkout <commit>^ -- <file>
```

---

## When to Use This Skill

**Always activate for:**
- Any Git command or operation
- Repository management questions
- Branch strategy decisions
- Merge conflict resolution
- History rewriting needs
- Recovery from Git mistakes
- Platform-specific Git questions
- Dangerous operations (with appropriate warnings)

**Key indicators:**
- User mentions Git, GitHub, GitLab, Bitbucket, Azure DevOps
- Version control questions
- Commit, push, pull, merge, rebase operations
- Branch management
- History modification
- Recovery scenarios

---

This skill provides COMPLETE Git expertise. Combined with the reference files and safety guardrails, you have the knowledge to handle ANY Git operation safely and effectively.
