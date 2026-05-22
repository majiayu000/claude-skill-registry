---
name: git-workflow-designer
description: Expert guide for designing Git branching strategies including Git Flow, GitHub Flow, trunk-based development, and release management. Use when establishing team workflows or improving version control practices.
---

# Git Workflow Designer Skill

## Overview

This skill helps you design and implement effective Git branching strategies for teams of any size. Covers Git Flow, GitHub Flow, trunk-based development, release management, and branch protection policies.

## Workflow Selection Philosophy

### Key Factors
1. **Team size**: Solo vs. small team vs. large organization
2. **Release frequency**: Continuous vs. scheduled releases
3. **Environment complexity**: Single vs. multiple deployment targets
4. **Risk tolerance**: Move fast vs. stability first

### Workflow Comparison

| Workflow | Best For | Release Frequency | Complexity |
|----------|----------|-------------------|------------|
| Trunk-Based | Small teams, CI/CD | Continuous | Low |
| GitHub Flow | Most web apps | On-demand | Low |
| Git Flow | Versioned software | Scheduled | High |
| GitLab Flow | Environment-based | Mixed | Medium |

## GitHub Flow (Recommended for Most)

### Overview
Simple, effective workflow for continuous deployment.

```
main ─────●─────●─────●─────●─────●─────●
            \       /   \       /
feature/x    ●─────●     ●─────●
```

### Process

1. **Branch from main**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/user-authentication
   ```

2. **Commit regularly**
   ```bash
   git add .
   git commit -m "feat: add login form component"
   ```

3. **Push and create PR**
   ```bash
   git push -u origin feature/user-authentication
   gh pr create --title "Add user authentication" --body "..."
   ```

4. **Review and merge**
   - CI runs tests
   - Peer review
   - Squash merge to main

5. **Deploy**
   - Automatic deploy on merge to main

### Branch Naming Convention

```
feature/  - New features
fix/      - Bug fixes
docs/     - Documentation
refactor/ - Code refactoring
test/     - Test additions
chore/    - Maintenance tasks
```

### Configuration

```yaml
# .github/branch-protection.yml (pseudo-config)
main:
  required_status_checks:
    strict: true
    contexts:
      - "ci/tests"
      - "ci/lint"
      - "ci/build"
  required_pull_request_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true
  enforce_admins: false
  restrictions: null
```

## Git Flow (For Versioned Releases)

### Overview
Structured workflow for scheduled release cycles.

```
main     ─────●─────────────────●─────────────●
               \               /               \
release         ●─────●─────●─                  ●───
                 \     \   /                   /
develop   ●─────●─●─────●─●─────●─────●─────●─●
            \   /   \       /     \       /
feature      ●─●     ●─────●       ●─────●
```

### Branches

| Branch | Purpose | Merges To |
|--------|---------|-----------|
| `main` | Production-ready code | - |
| `develop` | Integration branch | `main` |
| `feature/*` | New features | `develop` |
| `release/*` | Release preparation | `main`, `develop` |
| `hotfix/*` | Emergency fixes | `main`, `develop` |

### Feature Development

```bash
# Start feature
git checkout develop
git pull origin develop
git checkout -b feature/new-dashboard

# Work on feature
git commit -m "feat: add dashboard layout"
git commit -m "feat: add dashboard charts"

# Complete feature
git checkout develop
git merge --no-ff feature/new-dashboard
git branch -d feature/new-dashboard
git push origin develop
```

### Release Process

```bash
# Start release
git checkout develop
git checkout -b release/1.2.0

# Bump version
npm version 1.2.0 --no-git-tag-version
git commit -am "chore: bump version to 1.2.0"

# Fix release issues
git commit -m "fix: correct typo in release notes"

# Complete release
git checkout main
git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin main --tags

git checkout develop
git merge --no-ff release/1.2.0
git push origin develop

git branch -d release/1.2.0
```

### Hotfix Process

```bash
# Start hotfix
git checkout main
git checkout -b hotfix/1.2.1

# Fix the issue
git commit -m "fix: critical security vulnerability"

# Complete hotfix
git checkout main
git merge --no-ff hotfix/1.2.1
git tag -a v1.2.1 -m "Hotfix 1.2.1"
git push origin main --tags

git checkout develop
git merge --no-ff hotfix/1.2.1
git push origin develop

git branch -d hotfix/1.2.1
```

## Trunk-Based Development

### Overview
Everyone commits to main with short-lived branches.

```
main ─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●
        \─/   \─/       \─/
        PR    PR        PR
```

### Principles

1. **Short-lived branches** (< 1 day)
2. **Small, frequent commits**
3. **Feature flags for incomplete work**
4. **Comprehensive CI/CD**

### Feature Flags Integration

```typescript
// src/lib/features.ts
export const features = {
  newCheckout: process.env.FEATURE_NEW_CHECKOUT === 'true',
  darkMode: process.env.FEATURE_DARK_MODE === 'true',
};

// Usage
if (features.newCheckout) {
  return <NewCheckout />;
}
return <OldCheckout />;
```

### Branch Rules

```bash
# Quick feature (< 4 hours)
git checkout main
git pull
git checkout -b quick/fix-typo
# ... work ...
git push -u origin quick/fix-typo
gh pr create --title "Fix typo" --body ""
# Merge immediately after CI passes
```

## Release Management

### Semantic Versioning

```
MAJOR.MINOR.PATCH

1.0.0 - Initial release
1.1.0 - New feature (backwards compatible)
1.1.1 - Bug fix
2.0.0 - Breaking change
```

### Automated Version Bumping

```json
// package.json
{
  "scripts": {
    "release:patch": "npm version patch && git push --follow-tags",
    "release:minor": "npm version minor && git push --follow-tags",
    "release:major": "npm version major && git push --follow-tags"
  }
}
```

### Changelog Generation

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        uses: metcalfc/changelog-generator@v4
        with:
          myToken: ${{ secrets.GITHUB_TOKEN }}

      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: ${{ steps.changelog.outputs.changelog }}
```

### Conventional Commits

```bash
# Format
<type>(<scope>): <description>

[optional body]

[optional footer(s)]

# Types
feat:     New feature
fix:      Bug fix
docs:     Documentation
style:    Formatting, no code change
refactor: Refactoring
test:     Tests
chore:    Maintenance

# Examples
feat(auth): add password reset flow
fix(api): handle null user gracefully
docs: update README with new API endpoints
chore(deps): update dependencies
```

### Commitlint Configuration

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'test',
        'chore',
        'perf',
        'ci',
        'build',
        'revert',
      ],
    ],
    'subject-case': [2, 'always', 'lower-case'],
    'header-max-length': [2, 'always', 72],
  },
};
```

## Branch Protection

### GitHub Branch Protection Rules

```yaml
# Recommended settings for main branch

Required status checks:
  - ci/test
  - ci/lint
  - ci/build
  - ci/typecheck

Required reviews: 1
Dismiss stale reviews: true
Require review from code owners: true

Require signed commits: false  # Optional
Require linear history: true   # Encourages squash/rebase

Include administrators: false  # Allow admins to bypass

Restrict who can push:
  - Maintainers only
```

### CODEOWNERS

```
# .github/CODEOWNERS

# Default owners
* @team-lead

# Frontend
/src/components/ @frontend-team
/src/app/ @frontend-team

# Backend
/src/api/ @backend-team
/src/lib/db/ @backend-team

# Infrastructure
/.github/ @devops-team
/docker/ @devops-team

# Docs
/docs/ @tech-writer
*.md @tech-writer
```

## Merge Strategies

### Squash and Merge (Recommended)

```bash
# Clean history, one commit per feature
git merge --squash feature/branch
git commit -m "feat: complete feature description"
```

**Pros:**
- Clean main history
- Easy to revert features
- Commit message can be edited

**Cons:**
- Loses individual commit history

### Rebase and Merge

```bash
# Linear history, preserves commits
git rebase main feature/branch
git checkout main
git merge feature/branch
```

**Pros:**
- Linear history
- Preserves individual commits
- Bisect-friendly

**Cons:**
- Requires clean commits
- Force push may be needed

### Merge Commit

```bash
# Preserves full history with merge points
git merge --no-ff feature/branch
```

**Pros:**
- Complete history preserved
- Clear merge points
- No force push needed

**Cons:**
- Noisy history
- Harder to navigate

## Common Scenarios

### Sync Feature Branch with Main

```bash
# Option 1: Rebase (clean history)
git checkout feature/my-feature
git fetch origin
git rebase origin/main
git push --force-with-lease

# Option 2: Merge (safe, but noisy)
git checkout feature/my-feature
git merge origin/main
git push
```

### Undo Last Commit (Not Pushed)

```bash
# Keep changes staged
git reset --soft HEAD~1

# Keep changes unstaged
git reset HEAD~1

# Discard changes
git reset --hard HEAD~1
```

### Fix Commit Message

```bash
# Last commit only
git commit --amend -m "new message"

# Older commits (interactive rebase)
git rebase -i HEAD~3
# Change 'pick' to 'reword' for target commit
```

### Cherry-Pick Specific Commit

```bash
# Apply specific commit to current branch
git cherry-pick abc123

# Cherry-pick without committing
git cherry-pick --no-commit abc123
```

### Recover Deleted Branch

```bash
# Find the commit
git reflog

# Recreate branch
git checkout -b recovered-branch abc123
```

## Workflow Scripts

### Git Aliases

```bash
# ~/.gitconfig
[alias]
    # Status
    s = status -sb

    # Branching
    co = checkout
    cob = checkout -b
    br = branch -vv

    # Commits
    cm = commit -m
    ca = commit --amend --no-edit

    # Logging
    lg = log --oneline --graph --decorate -20
    lga = log --oneline --graph --decorate --all -20

    # Sync
    sync = !git fetch origin && git rebase origin/main

    # Cleanup
    cleanup = !git branch --merged | grep -v main | xargs git branch -d

    # Undo
    undo = reset --soft HEAD~1
```

### Feature Branch Script

```bash
#!/bin/bash
# scripts/feature.sh

set -e

BRANCH_TYPE=${1:-feature}
BRANCH_NAME=$2

if [ -z "$BRANCH_NAME" ]; then
    echo "Usage: ./scripts/feature.sh [type] <name>"
    echo "Types: feature, fix, docs, chore"
    exit 1
fi

FULL_BRANCH="$BRANCH_TYPE/$BRANCH_NAME"

echo "Creating branch: $FULL_BRANCH"

git checkout main
git pull origin main
git checkout -b "$FULL_BRANCH"

echo "Branch '$FULL_BRANCH' created and checked out"
echo "Run: git push -u origin $FULL_BRANCH"
```

## Workflow Checklist

### Before Selecting Workflow
- [ ] Understand team size and distribution
- [ ] Define release frequency
- [ ] Assess CI/CD maturity
- [ ] Consider deployment environments

### Implementation
- [ ] Document workflow in CONTRIBUTING.md
- [ ] Configure branch protection rules
- [ ] Set up CODEOWNERS
- [ ] Configure merge strategy
- [ ] Add commit message linting
- [ ] Create Git aliases/scripts

### Maintenance
- [ ] Regular branch cleanup
- [ ] Monitor merge queue
- [ ] Review and update protection rules
- [ ] Train new team members

## When to Use This Skill

Invoke this skill when:
- Starting a new project and choosing a workflow
- Scaling from solo to team development
- Improving release management
- Setting up branch protection rules
- Creating contribution guidelines
- Resolving Git workflow conflicts
- Implementing conventional commits
