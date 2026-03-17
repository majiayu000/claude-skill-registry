---
name: git-workflow-mastery
description: Advanced Git workflows, branching strategies, and commit conventions
license: MIT
compatibility: git 2.30+
allowed-tools: run_command read_file write_file
---

# Git Workflow Mastery

## Branching Strategies

### GitHub Flow (Simple)
```
main ────●────●────●────●────●────
              \         /
feature        ●───●───●
```

Best for: Continuous deployment, small teams

### Git Flow (Structured)
```
main    ────●─────────────────●────
             \               /
release       ●─────●───────●
               \   /
develop ────●───●───●───●───●────
             \     /
feature       ●───●
```

Best for: Scheduled releases, larger teams

## Branch Naming

```bash
# Feature branches
feature/user-authentication
feature/JIRA-123-add-login

# Bug fixes
fix/login-redirect-loop
fix/JIRA-456-null-pointer

# Releases
release/v1.2.0
release/2024-q1

# Hotfixes
hotfix/security-patch
hotfix/v1.2.1
```

## Commit Messages

### Conventional Commits
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types
```bash
feat:     # New feature
fix:      # Bug fix
docs:     # Documentation only
style:    # Formatting, no code change
refactor: # Code change without feature/fix
perf:     # Performance improvement
test:     # Adding/updating tests
chore:    # Build process, dependencies
ci:       # CI configuration
revert:   # Revert previous commit
```

### Examples
```bash
# Simple
feat(auth): add OAuth2 login support

# With body
fix(api): handle null response from external service

The external payment API occasionally returns null
instead of an error object. Added defensive check.

Fixes #234

# Breaking change
feat(api)!: change response format to JSON:API

BREAKING CHANGE: All API responses now follow JSON:API spec.
Clients need to update their parsers.
```

## Common Operations

### Interactive Rebase
```bash
# Squash last 3 commits
git rebase -i HEAD~3

# In editor:
pick abc1234 First commit
squash def5678 Second commit
squash ghi9012 Third commit
```

### Cherry Pick
```bash
# Apply specific commit to current branch
git cherry-pick abc1234

# Cherry pick range
git cherry-pick abc1234..def5678
```

### Stashing
```bash
# Save work in progress
git stash push -m "WIP: feature login"

# List stashes
git stash list

# Apply and remove
git stash pop

# Apply specific stash
git stash apply stash@{2}
```

### Undoing Changes
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Undo a pushed commit (new revert commit)
git revert abc1234

# Discard all local changes
git checkout -- .
git clean -fd
```

## Advanced Techniques

### Bisect (Find Bug Introduction)
```bash
git bisect start
git bisect bad           # Current commit is broken
git bisect good v1.0.0   # Known good commit

# Git checks out middle commit
# Test and mark:
git bisect good  # or
git bisect bad

# Continue until bug found
git bisect reset
```

### Reflog (Recover Lost Commits)
```bash
# View reflog
git reflog

# Recover deleted branch
git checkout -b recovered-branch abc1234

# Undo hard reset
git reset --hard HEAD@{2}
```

### Worktrees (Multiple Working Directories)
```bash
# Create worktree for feature branch
git worktree add ../feature-branch feature/new-ui

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../feature-branch
```

## Hooks

### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run linter
npm run lint
if [ $? -ne 0 ]; then
  echo "Lint failed. Commit aborted."
  exit 1
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
  echo "Tests failed. Commit aborted."
  exit 1
fi
```

### Commit-msg Hook
```bash
#!/bin/sh
# .git/hooks/commit-msg

# Validate conventional commit format
commit_regex='^(feat|fix|docs|style|refactor|perf|test|chore|ci|revert)(\(.+\))?: .{1,72}'

if ! grep -qE "$commit_regex" "$1"; then
  echo "Invalid commit message format."
  echo "Use: type(scope): description"
  exit 1
fi
```

## Git Aliases

```bash
# ~/.gitconfig
[alias]
  co = checkout
  br = branch
  ci = commit
  st = status
  lg = log --oneline --graph --decorate
  undo = reset --soft HEAD~1
  amend = commit --amend --no-edit
  wip = !git add -A && git commit -m 'WIP'
  sync = !git fetch origin && git rebase origin/main
```

## Best Practices

1. **Commit early, commit often** - Small, focused commits
2. **Write meaningful commit messages** - Explain why, not just what
3. **Keep main/master deployable** - Always in working state
4. **Review before merging** - Use pull requests
5. **Delete merged branches** - Keep repository clean
6. **Never rewrite shared history** - No force push to shared branches
7. **Use tags for releases** - Semantic versioning
