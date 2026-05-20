---
name: gitworfkflows
description: Git workflows including branching strategies, commits, merging, rebasing, and GitHub collaboration. Activate for git commands, version control, PRs, and repository management.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Git Workflows Skill

Provides comprehensive Git version control capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Git commands and operations
- Branching strategies
- Commit management
- Pull requests and merges
- Repository configuration

## Quick Reference

### Basic Commands
\`\`\`bash
# Status and info
git status
git log --oneline -10
git diff
git diff --staged

# Staging
git add <file>
git add .
git add -p              # Interactive staging

# Committing
git commit -m "message"
git commit -am "message"  # Add and commit
git commit --amend

# Branching
git branch
git branch <name>
git checkout <branch>
git checkout -b <branch>
git switch <branch>
git switch -c <branch>

# Merging
git merge <branch>
git merge --no-ff <branch>
git rebase <branch>

# Remote
git fetch
git pull
git push
git push -u origin <branch>
\`\`\`

## Branching Strategy (Git Flow)

\`\`\`
main          ─────●─────────────●─────────────●───────
                   │             │             │
release       ─────┼─────●───────┼─────────────┼───────
                   │     │       │             │
develop       ─────●─────┼───────●─────────────●───────
                   │     │       │             │
feature       ─────●─────┘       │             │
                                 │             │
hotfix        ───────────────────●─────────────┘
\`\`\`

### Branch Naming
\`\`\`bash
# Features
feature/add-agent-api
feature/GA-123-user-auth

# Bugfixes
bugfix/fix-agent-timeout
bugfix/GA-456-memory-leak

# Hotfixes
hotfix/critical-security-patch

# Releases
release/v1.0.0
\`\`\`

## Commit Message Convention

\`\`\`bash
# Format
<type>(<scope>): <subject>

<body>

<footer>

# Types
feat:     New feature
fix:      Bug fix
docs:     Documentation
style:    Formatting (no code change)
refactor: Code refactoring
test:     Adding tests
chore:    Maintenance

# Examples
git commit -m "feat(agent): add Claude agent support"
git commit -m "fix(api): resolve timeout in task processing"
git commit -m "docs: update deployment instructions"
\`\`\`

## Common Workflows

### Start Feature
\`\`\`bash
git checkout develop
git pull origin develop
git checkout -b feature/new-feature
# ... work ...
git add .
git commit -m "feat: implement new feature"
git push -u origin feature/new-feature
# Create PR to develop
\`\`\`

### Sync Feature Branch
\`\`\`bash
git checkout develop
git pull origin develop
git checkout feature/my-feature
git rebase develop
# Resolve conflicts if any
git push --force-with-lease
\`\`\`

### Squash Commits
\`\`\`bash
git rebase -i HEAD~3  # Interactive rebase last 3 commits
# Change 'pick' to 'squash' for commits to combine
\`\`\`

### Undo Changes
\`\`\`bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Undo staged changes
git restore --staged <file>

# Discard working directory changes
git restore <file>

# Revert a commit (creates new commit)
git revert <commit-hash>
\`\`\`

## GitHub CLI

\`\`\`bash
# PR Management
gh pr create --title "Feature: Add agent API" --body "Description"
gh pr list
gh pr checkout <number>
gh pr merge <number>
gh pr review <number> --approve

# Issues
gh issue create --title "Bug: Agent timeout" --label bug
gh issue list
gh issue close <number>

# Repository
gh repo clone <owner>/<repo>
gh repo view --web
\`\`\`

## .gitignore Patterns

\`\`\`gitignore
# Dependencies
node_modules/
venv/
__pycache__/

# Build outputs
dist/
build/
*.egg-info/

# Environment
.env
.env.local
*.local

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Secrets (never commit!)
*.pem
*.key
credentials.json
\`\`\`

## Git Hooks

\`\`\`bash
# .git/hooks/pre-commit
#!/bin/sh
npm run lint
npm run test

# .git/hooks/commit-msg
#!/bin/sh
if ! grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}" "$1"; then
    echo "Invalid commit message format"
    exit 1
fi
\`\`\`
