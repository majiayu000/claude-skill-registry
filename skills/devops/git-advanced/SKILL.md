---
name: git-advanced
version: 1.0.0
description: Advanced git workflows including rebase, worktrees, bisect, hooks, and monorepo patterns
author: workspace-hub
category: devtools
capabilities:
  - Interactive rebase and history rewriting
  - Git worktrees for parallel development
  - Bisect for bug hunting
  - Rerere for conflict resolution
  - Reflog for recovery
  - Hooks and custom commands
  - Submodules and monorepo patterns
tools:
  - git
  - gh
  - git-lfs
  - pre-commit
  - husky
tags: [git, version-control, rebase, worktrees, bisect, hooks, monorepo]
platforms: [linux, macos, windows]
related_skills:
  - docker
  - cli-productivity
  - github-actions
---

# Git Advanced Skill

Master advanced git workflows for efficient version control. This skill covers interactive rebase, worktrees, bisect, rerere, reflog, hooks, and patterns for monorepos and submodules.

## When to Use This Skill

### USE when:
- Managing complex branch strategies
- Working on multiple features simultaneously
- Hunting down bugs with bisect
- Maintaining clean commit history
- Setting up team workflows with hooks
- Managing multi-repo dependencies
- Recovering from git mistakes

### DON'T USE when:
- Simple linear development (basic git suffices)
- Solo projects with simple history
- When team isn't familiar with advanced git
- Time-critical fixes (use simple commits)

## Prerequisites

### Installation

**Git Configuration:**
```bash
# Verify git version (2.23+ recommended)
git --version

# Global configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Recommended settings
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global push.autoSetupRemote true
git config --global rerere.enabled true
git config --global core.autocrlf input
git config --global core.editor "vim"

# Better diff
git config --global diff.algorithm histogram
git config --global merge.conflictStyle diff3
```

**GitHub CLI (optional):**
```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
```

**Pre-commit (for hooks):**
```bash
# Install pre-commit
pip install pre-commit

# Or with homebrew
brew install pre-commit
```

## Core Capabilities

### 1. Interactive Rebase

**Basic Interactive Rebase:**
```bash
# Rebase last 5 commits
git rebase -i HEAD~5

# Rebase onto main
git rebase -i main

# Rebase from specific commit
git rebase -i abc123^
```

**Interactive Rebase Commands:**
```
pick   abc123 First commit     # Use commit as-is
reword def456 Second commit    # Edit commit message
edit   ghi789 Third commit     # Stop to amend
squash jkl012 Fourth commit    # Combine with previous
fixup  mno345 Fifth commit     # Combine, discard message
drop   pqr678 Sixth commit     # Remove commit
```

**Common Rebase Workflows:**
```bash
# Squash all commits into one
git rebase -i main
# Change all but first 'pick' to 'squash'

# Reorder commits
git rebase -i HEAD~3
# Rearrange the pick lines

# Split a commit
git rebase -i HEAD~3
# Change 'pick' to 'edit' on target commit
git reset HEAD^
git add -p  # Add pieces
git commit -m "First part"
git add .
git commit -m "Second part"
git rebase --continue

# Edit commit message
git rebase -i HEAD~3
# Change 'pick' to 'reword'
```

**Autosquash Pattern:**
```bash
# Create fixup commit
git commit --fixup=abc123

# Create squash commit
git commit --squash=abc123

# Apply autosquash
git rebase -i --autosquash main

# Enable autosquash by default
git config --global rebase.autosquash true
```

### 2. Git Worktrees

**Basic Worktree Usage:**
```bash
# List worktrees
git worktree list

# Add worktree for existing branch
git worktree add ../feature-branch feature/new-feature

# Add worktree with new branch
git worktree add -b hotfix/urgent ../hotfix-urgent main

# Remove worktree
git worktree remove ../feature-branch

# Prune stale worktrees
git worktree prune
```

**Worktree Workflow:**
```bash
# Project structure
workspace/
├── main/           # Main development
├── feature-auth/   # Feature branch
├── hotfix-critical/# Hotfix branch
└── experiment/     # Experimental work

# Setup
cd main
git worktree add ../feature-auth feature/authentication
git worktree add ../hotfix-critical -b hotfix/critical-bug
git worktree add ../experiment -b experiment/new-approach

# Work on feature
cd ../feature-auth
# make changes...
git commit -am "Add authentication"

# Quick switch to fix bug
cd ../hotfix-critical
# fix bug...
git commit -am "Fix critical bug"
git push

# Back to feature
cd ../feature-auth
```

**Worktree Helper Script:**
```bash
#!/bin/bash
# scripts/worktree.sh
# ABOUTME: Git worktree management helper
# ABOUTME: Simplifies creating and managing worktrees

set -e

WORKTREE_BASE="${WORKTREE_BASE:-$(dirname $(git rev-parse --git-dir))}"

case "$1" in
    add)
        BRANCH="$2"
        DIR="${3:-$WORKTREE_BASE/../$(echo $BRANCH | tr '/' '-')}"
        if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
            git worktree add "$DIR" "$BRANCH"
        else
            git worktree add -b "$BRANCH" "$DIR"
        fi
        echo "Created worktree at: $DIR"
        ;;
    remove)
        git worktree remove "$2"
        ;;
    list)
        git worktree list
        ;;
    *)
        echo "Usage: $0 {add|remove|list} [branch] [directory]"
        exit 1
        ;;
esac
```

### 3. Git Bisect

**Basic Bisect:**
```bash
# Start bisect
git bisect start

# Mark current version as bad
git bisect bad

# Mark known good commit
git bisect good v1.0.0

# Git checks out a commit - test it
# If bad:
git bisect bad
# If good:
git bisect good

# Continue until found
# Git will show: "abc123 is the first bad commit"

# End bisect
git bisect reset
```

**Automated Bisect:**
```bash
# Create test script
cat > test-bug.sh << 'EOF'
#!/bin/bash
# Return 0 if good, non-zero if bad
npm test -- --grep "specific test"
EOF
chmod +x test-bug.sh

# Run automated bisect
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run ./test-bug.sh

# Git will find the bad commit automatically
git bisect reset
```

**Bisect with Skip:**
```bash
# If commit can't be tested (won't build)
git bisect skip

# Skip range of commits
git bisect skip abc123..def456
```

**Bisect Log and Replay:**
```bash
# Save bisect session
git bisect log > bisect.log

# Replay session
git bisect replay bisect.log
```

### 4. Git Rerere (Reuse Recorded Resolution)

**Enable Rerere:**
```bash
# Enable globally
git config --global rerere.enabled true

# Check status
git config --get rerere.enabled
```

**Using Rerere:**
```bash
# When you resolve a conflict, git records the resolution
git merge feature-branch
# Resolve conflicts...
git add .
git commit

# Next time same conflict occurs, git auto-applies resolution
git merge another-branch
# "Resolved 'file.txt' using previous resolution."

# If auto-resolution is wrong, forget it
git rerere forget path/to/file
```

**Rerere Management:**
```bash
# View recorded resolutions
ls .git/rr-cache/

# Clean old resolutions
git rerere gc

# Show diff of recorded resolution
git rerere diff
```

### 5. Git Reflog

**Basic Reflog:**
```bash
# Show reflog
git reflog

# Show reflog with dates
git reflog --date=relative

# Show reflog for specific ref
git reflog show feature-branch

# Output
# abc123 HEAD@{0}: commit: Latest commit
# def456 HEAD@{1}: checkout: moving from main to feature
# ghi789 HEAD@{2}: commit: Previous commit
```

**Recovery with Reflog:**
```bash
# Recover deleted branch
git reflog
# Find last commit of deleted branch: abc123
git checkout -b recovered-branch abc123

# Undo hard reset
git reflog
# Find state before reset: HEAD@{2}
git reset --hard HEAD@{2}

# Recover lost stash
git fsck --unreachable | grep commit
git show <commit-hash>
git stash apply <commit-hash>

# Recover from bad rebase
git reflog
# Find pre-rebase state: HEAD@{5}
git reset --hard HEAD@{5}
```

**Reflog Expiration:**
```bash
# Check expiration settings
git config --get gc.reflogexpire  # Default: 90 days
git config --get gc.reflogexpireunreachable  # Default: 30 days

# Extend reflog retention
git config --global gc.reflogexpire 180.days
```

### 6. Git Hooks

**Available Hooks:**
```
client-side:
  pre-commit      # Before commit message prompt
  prepare-commit-msg  # Edit default message
  commit-msg      # Validate commit message
  post-commit     # After commit completes
  pre-push        # Before push

server-side:
  pre-receive     # Before accepting push
  update          # Per-branch check
  post-receive    # After push completes
```

**Pre-commit Hook Example:**
```bash
#!/bin/bash
# .git/hooks/pre-commit
# ABOUTME: Pre-commit hook for code quality
# ABOUTME: Runs linting and tests before commit

set -e

echo "Running pre-commit checks..."

# Check for debug statements
if git diff --cached --name-only | xargs grep -l 'console.log\|debugger\|binding.pry' 2>/dev/null; then
    echo "ERROR: Debug statements found. Remove before committing."
    exit 1
fi

# Run linter
if [ -f "package.json" ] && grep -q '"lint"' package.json; then
    echo "Running linter..."
    npm run lint --quiet || exit 1
fi

# Run tests
if [ -f "package.json" ] && grep -q '"test"' package.json; then
    echo "Running tests..."
    npm test --quiet || exit 1
fi

echo "Pre-commit checks passed!"
```

**Commit-msg Hook Example:**
```bash
#!/bin/bash
# .git/hooks/commit-msg
# ABOUTME: Validates commit message format
# ABOUTME: Enforces conventional commits

COMMIT_MSG_FILE="$1"
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Conventional commit pattern
PATTERN="^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .{1,50}"

if ! echo "$COMMIT_MSG" | grep -qE "$PATTERN"; then
    echo "ERROR: Invalid commit message format."
    echo ""
    echo "Expected format: <type>(<scope>): <subject>"
    echo "Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert"
    echo ""
    echo "Examples:"
    echo "  feat(auth): add login functionality"
    echo "  fix(api): handle null response"
    echo "  docs: update README"
    exit 1
fi
```

**Pre-push Hook Example:**
```bash
#!/bin/bash
# .git/hooks/pre-push
# ABOUTME: Pre-push hook for safety checks
# ABOUTME: Prevents pushing to protected branches

BRANCH=$(git rev-parse --abbrev-ref HEAD)
PROTECTED_BRANCHES="^(main|master|production)$"

if echo "$BRANCH" | grep -qE "$PROTECTED_BRANCHES"; then
    echo "ERROR: Direct push to $BRANCH is not allowed."
    echo "Please create a pull request instead."
    exit 1
fi

# Run full test suite before push
echo "Running tests before push..."
npm test || exit 1

echo "Pre-push checks passed!"
```

**Using pre-commit Framework:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: local
    hooks:
      - id: run-tests
        name: Run tests
        entry: npm test
        language: system
        pass_filenames: false
        always_run: true
```

**Install pre-commit hooks:**
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Install commit-msg hook
pre-commit install --hook-type commit-msg

# Run manually
pre-commit run --all-files
```

### 7. Git Aliases

**Useful Aliases:**
```bash
# Add to ~/.gitconfig
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

**Advanced Aliases:**
```gitconfig
# ~/.gitconfig
[alias]
    # Status
    st = status -sb
    ss = status

    # Branch operations
    br = branch
    bra = branch -a
    brd = branch -d
    brD = branch -D

    # Checkout
    co = checkout
    cob = checkout -b
    com = checkout main

    # Commit
    ci = commit
    cia = commit --amend
    ciane = commit --amend --no-edit
    wip = !git add -A && git commit -m 'WIP'

    # Diff
    df = diff
    dfs = diff --staged
    dfw = diff --word-diff

    # Log
    lg = log --graph --oneline --decorate -20
    lga = log --graph --oneline --decorate --all
    ll = log --pretty=format:'%C(yellow)%h%C(reset) %s %C(blue)<%an>%C(reset) %C(green)(%cr)%C(reset)' -20
    hist = log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short

    # Stash
    sl = stash list
    sp = stash pop
    ss = stash save
    sd = stash drop

    # Remote
    pu = push
    puf = push --force-with-lease
    pl = pull
    plr = pull --rebase
    fe = fetch --all --prune

    # Rebase
    rb = rebase
    rbi = rebase -i
    rbc = rebase --continue
    rba = rebase --abort

    # Reset
    undo = reset --soft HEAD~1
    nuke = reset --hard HEAD

    # Clean
    clean-branches = !git branch --merged | grep -v '*' | xargs -n 1 git branch -d

    # Find
    find = !git ls-files | grep -i
    grep = grep -Ii

    # Utility
    aliases = !git config --get-regexp '^alias\\.' | sed 's/alias\\.\\([^ ]*\\) \\(.*\\)/\\1\\\t => \\2/' | sort
    contributors = shortlog -sn
```

### 8. Submodules

**Basic Submodule Operations:**
```bash
# Add submodule
git submodule add https://github.com/user/repo libs/repo

# Clone with submodules
git clone --recurse-submodules https://github.com/user/main-repo

# Initialize submodules after clone
git submodule init
git submodule update

# Or combined
git submodule update --init --recursive

# Update submodule to latest
cd libs/repo
git checkout main
git pull
cd ../..
git add libs/repo
git commit -m "Update submodule"

# Update all submodules
git submodule update --remote
```

**Submodule Configuration:**
```bash
# Track specific branch
git config -f .gitmodules submodule.libs/repo.branch main

# Shallow clone submodules
git config -f .gitmodules submodule.libs/repo.shallow true

# Update strategy
git submodule update --remote --merge  # Merge changes
git submodule update --remote --rebase # Rebase changes
```

**Submodule Workflow Script:**
```bash
#!/bin/bash
# scripts/submodule-sync.sh
# ABOUTME: Synchronize all submodules
# ABOUTME: Updates submodules to latest remote commits

set -e

echo "Synchronizing submodules..."

# Initialize any new submodules
git submodule init

# Update all submodules to tracked branch
git submodule update --remote --merge

# Show status
git submodule status

echo "Submodules synchronized!"
```

### 9. Monorepo Patterns

**Sparse Checkout:**
```bash
# Enable sparse checkout
git sparse-checkout init

# Set patterns
git sparse-checkout set packages/app packages/shared

# Add more patterns
git sparse-checkout add docs

# Disable sparse checkout
git sparse-checkout disable
```

**Working with Monorepos:**
```bash
# Clone specific directory only
git clone --filter=blob:none --sparse https://github.com/user/monorepo
cd monorepo
git sparse-checkout set packages/my-package

# Shallow clone for faster checkout
git clone --depth 1 --filter=blob:none --sparse https://github.com/user/monorepo

# Partial clone (fetch objects on demand)
git clone --filter=blob:none https://github.com/user/monorepo
```

**Monorepo Commit Strategy:**
```bash
# Commit message with scope
git commit -m "feat(package-name): add feature X"

# Using conventional commits
feat(api): add new endpoint
fix(web): resolve routing issue
chore(deps): update dependencies
docs(shared): improve API documentation
```

## Integration Examples

### 1. Complete .gitconfig

```gitconfig
# ~/.gitconfig

[user]
    name = Your Name
    email = your.email@example.com

[core]
    editor = vim
    autocrlf = input
    pager = delta

[init]
    defaultBranch = main

[pull]
    rebase = true

[push]
    autoSetupRemote = true
    default = current

[fetch]
    prune = true
    pruneTags = true

[merge]
    conflictStyle = diff3
    ff = false

[rebase]
    autosquash = true
    autostash = true

[rerere]
    enabled = true

[diff]
    algorithm = histogram
    colorMoved = default

[status]
    showUntrackedFiles = all

[credential]
    helper = cache --timeout=3600

[alias]
    # Core aliases
    st = status -sb
    co = checkout
    br = branch
    ci = commit
    lg = log --graph --oneline --decorate -20

    # Workflow aliases
    undo = reset --soft HEAD~1
    wip = !git add -A && git commit -m 'WIP'
    sync = !git fetch --all --prune && git pull --rebase

    # Branch cleanup
    cleanup = !git branch --merged main | grep -v '^[ *]*main$' | xargs git branch -d

[delta]
    navigate = true
    side-by-side = true
    line-numbers = true

[interactive]
    diffFilter = delta --color-only
```

### 2. GitHub Workflow with Hooks

```yaml
# .github/workflows/pr-check.yml
name: PR Checks

on:
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Validate commit messages
        run: |
          COMMITS=$(git log --format="%s" origin/main..HEAD)
          PATTERN="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"
          while IFS= read -r commit; do
            if ! echo "$commit" | grep -qE "$PATTERN"; then
              echo "Invalid commit message: $commit"
              exit 1
            fi
          done <<< "$COMMITS"

      - name: Check for merge commits
        run: |
          MERGE_COMMITS=$(git log --merges origin/main..HEAD --oneline)
          if [ -n "$MERGE_COMMITS" ]; then
            echo "Merge commits found. Please rebase instead."
            echo "$MERGE_COMMITS"
            exit 1
          fi

      - name: Run tests
        run: npm test
```

### 3. Git Flow Helper Functions

```bash
# Add to ~/.bashrc

# Start feature
gf-start() {
    local feature="$1"
    git checkout main
    git pull
    git checkout -b "feature/$feature"
}

# Finish feature
gf-finish() {
    local branch=$(git rev-parse --abbrev-ref HEAD)
    git checkout main
    git pull
    git merge --no-ff "$branch"
    git branch -d "$branch"
}

# Start hotfix
gh-start() {
    local hotfix="$1"
    git checkout main
    git pull
    git checkout -b "hotfix/$hotfix"
}

# Sync branch with main
gsync() {
    local branch=$(git rev-parse --abbrev-ref HEAD)
    git fetch origin main:main
    git rebase main
}
```

## Best Practices

### 1. Commit History

```bash
# Write good commit messages
git commit -m "feat(auth): add OAuth2 support

- Add Google OAuth provider
- Implement token refresh logic
- Add user profile sync

Closes #123"

# Keep commits atomic
# One logical change per commit

# Use conventional commits
# feat: new feature
# fix: bug fix
# docs: documentation
# style: formatting
# refactor: code restructure
# test: add tests
# chore: maintenance
```

### 2. Branch Strategy

```bash
# Feature branches from main
git checkout -b feature/add-auth main

# Hotfix branches from main
git checkout -b hotfix/fix-login main

# Keep branches short-lived
# Merge frequently

# Delete merged branches
git branch -d feature/add-auth
```

### 3. Rebase vs Merge

```bash
# Use rebase for:
# - Cleaning up local commits
# - Updating feature branch from main
git rebase main

# Use merge for:
# - Integrating feature into main
# - Preserving branch history
git merge --no-ff feature/add-auth
```

## Troubleshooting

### Common Issues

**Accidental commit to wrong branch:**
```bash
# Move commit to new branch
git branch new-branch
git reset --hard HEAD~1
git checkout new-branch
```

**Undo merge:**
```bash
# If not pushed
git reset --hard HEAD~1

# If pushed
git revert -m 1 <merge-commit>
```

**Lost changes after checkout:**
```bash
# Check reflog
git reflog

# Recover from reflog
git checkout HEAD@{2}
```

**Resolve rebase conflicts:**
```bash
# During rebase conflict
git status
# Edit conflicted files
git add <resolved-files>
git rebase --continue

# Abort if needed
git rebase --abort
```

**Clean up after failed rebase:**
```bash
git rebase --abort
# Or
git reflog
git reset --hard HEAD@{n}
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Interactive rebase patterns
  - Git worktrees for parallel development
  - Bisect for bug hunting
  - Rerere and reflog for recovery
  - Hooks and custom commands
  - Submodules and monorepo patterns

---

**Use this skill to master advanced git workflows and maintain clean, professional version control!**
