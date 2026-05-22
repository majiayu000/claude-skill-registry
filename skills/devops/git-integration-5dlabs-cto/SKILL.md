---
name: git-integration
description: Git and GitHub integration patterns including branching, conflict resolution, and GitHub Actions.
agents: [atlas]
triggers: [git, github, merge, conflict, pr, branch, release]
---

# Git and GitHub Integration

Patterns for Git workflows, conflict resolution, and GitHub automation.

## Core Specialization

- **Git Operations**: Branching, merging, rebasing, conflict resolution
- **GitHub Features**: PRs, Issues, Actions, Releases
- **Workflow Automation**: GitHub Actions, webhooks
- **Release Management**: Semantic versioning, changelogs
- **Repository Management**: Branch protection, CODEOWNERS

## Execution Rules

1. **Clean history.** Meaningful commits, squash when appropriate
2. **Conventional commits.** `feat:`, `fix:`, `chore:`, etc.
3. **PR best practices.** Clear description, linked issues
4. **Conflict resolution.** Prefer rebase over merge for feature branches
5. **Automation.** Automate repetitive tasks with Actions

## Branch Management

### Create Feature Branch

```bash
# From latest main
git fetch origin main
git checkout -b feature/task-123 origin/main
```

### Rebase Before PR

```bash
git fetch origin main
git rebase origin/main
git push --force-with-lease
```

### Interactive Rebase

```bash
# Clean up last 3 commits
git rebase -i HEAD~3
```

## Conflict Resolution

### During Rebase

```bash
git status                    # See conflicted files
# Edit files to resolve conflicts
git add <resolved-files>
git rebase --continue

# Abort if needed
git rebase --abort
```

### Resolution Strategy

1. Understand both sides of the conflict
2. Preserve intent of all changes where possible
3. Run tests after resolving
4. Document non-obvious resolution decisions
5. Escalate if resolution risks breaking functionality

## GitHub CLI

```bash
# Create PR
gh pr create --title "feat: description" --body "Closes #123"

# List PRs
gh pr list --state open

# Merge PR (squash)
gh pr merge --squash --auto

# Create release
gh release create v1.0.0 --generate-notes

# View PR checks
gh pr checks
```

## GitHub Actions Patterns

### Basic CI Workflow

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: make build
      - name: Test
        run: make test
```

### Auto-merge for Dependabot

```yaml
name: Dependabot auto-merge
on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Auto-merge
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Conventional Commits

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feat:` | New feature | `feat: add user authentication` |
| `fix:` | Bug fix | `fix: resolve login timeout` |
| `docs:` | Documentation | `docs: update API reference` |
| `style:` | Formatting | `style: fix indentation` |
| `refactor:` | Code refactoring | `refactor: extract auth service` |
| `test:` | Adding tests | `test: add auth unit tests` |
| `chore:` | Maintenance | `chore: update dependencies` |

## Release Management

### Semantic Versioning

- **MAJOR** (1.x.x): Breaking changes
- **MINOR** (x.1.x): New features, backward compatible
- **PATCH** (x.x.1): Bug fixes

### Release Process

```bash
# Tag release
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# Create GitHub release
gh release create v1.2.0 --generate-notes
```

## Guidelines

- Understand both sides of a conflict before resolving
- Preserve intent of all changes where possible
- Run tests after resolving conflicts
- Document non-obvious resolution decisions
- Escalate if resolution risks breaking functionality
