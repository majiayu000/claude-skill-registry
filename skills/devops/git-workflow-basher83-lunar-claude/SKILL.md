---
name: git-workflow
description: This skill should be used when the user asks to "make commits", "commit all changes", "create a branch", "name a branch", "organize commits", "conventional commits", "generate changelog", "release version", "bump version", or needs guidance on git workflow best practices including commit organization, branch naming, and conventional commit format.
---

# Git Workflow Best Practices

Guidance for creating clean, atomic commits and organizing git workflows effectively.

## Available Commands

This plugin provides commands to automate git workflows:

| Command | Purpose |
|---------|---------|
| `/git-status` | Quick repository status summary |
| `/git-commit` | Create commits with pre-commit hooks |
| `/branch-cleanup` | Clean up merged/stale branches |
| `/generate-changelog` | Generate CHANGELOG.md using git-cliff |

### Changelog Generation

Use `/generate-changelog` after creating commits to update CHANGELOG.md. The command uses a workflow-driven approach:

1. Shows current state (branch, recent commits, latest tag, unreleased changes)
2. Prompts to select action: Preview, Generate, or Release
3. For releases, analyzes commits and recommends version bump level

## Conventional Commit Format

Structure commit messages following the conventional commit specification. Project-specific CLAUDE.md conventions take precedence over these defaults.

```text
type(scope): subject

body (optional)

footer (optional)
```

### Commit Types

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `build` | Build system changes |
| `ci` | CI configuration |
| `chore` | Maintenance tasks |
| `revert` | Revert previous commit |

### Subject Line Rules

- Maximum 50 characters
- Use imperative mood ("Add feature" not "Added feature")
- No period at end
- Capitalize first letter

### Body Guidelines

- Wrap at 72 characters
- Explain what and why, not how
- Separate from subject with blank line

### Footer Conventions

- Reference issues: `Fixes #123` or `Relates to #456`
- Breaking changes: `BREAKING CHANGE: description`
- Co-authors: `Co-Authored-By: Name <email>`

## Branch Naming Conventions

Use descriptive, prefixed branch names:

### Branch Prefixes

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New functionality | `feature/user-authentication` |
| `fix/` | Bug fixes | `fix/login-redirect-loop` |
| `hotfix/` | Urgent production fixes | `hotfix/security-patch` |
| `release/` | Release preparation | `release/v2.1.0` |
| `docs/` | Documentation updates | `docs/api-reference` |
| `refactor/` | Code restructuring | `refactor/database-layer` |
| `test/` | Test additions | `test/integration-suite` |
| `chore/` | Maintenance | `chore/dependency-updates` |

### Naming Rules

- Use kebab-case (lowercase with hyphens)
- Keep names descriptive but concise
- Include ticket/issue number when applicable: `feature/123-user-auth`
- Avoid generic names like `feature/update` or `fix/bug`

## Atomic Commit Principles

Create commits that are:

1. **Self-contained**: Each commit represents one logical change
2. **Complete**: Code compiles and tests pass after each commit
3. **Reviewable**: Small enough to understand in one review session

### Grouping Guidelines

- Keep implementation and tests together
- Separate infrastructure from application changes
- Isolate documentation unless integral to code changes
- Group by feature/component/purpose
- Keep related lock files with their manifests (package-lock.json with package.json)

### What NOT to Mix

- Unrelated bug fixes in the same commit
- Formatting changes with logic changes
- Multiple features in one commit
- Refactoring with new functionality

## Pre-Commit Workflow

Before committing:

1. **Review changes**: `git diff` and `git status`
2. **Check for sensitive files**: Never commit `.env`, credentials, API keys
3. **Run pre-commit hooks**: Let formatters and linters process files
4. **Re-stage if hooks modify files**: Add reformatted files and retry commit

### Handling Pre-Commit Hook Failures

When hooks modify files:

1. Review the changes made by hooks
2. Re-add the modified files: `git add <files>`
3. Retry the commit
4. Document any issues for manual review

## Commit Message Template

Use heredoc format for multi-line messages:

```bash
git commit -m "$(cat <<'EOF'
type(scope): subject line here

- Detailed bullet point explaining change
- Another relevant detail

Fixes #123
EOF
)"
```

## Protected Branches

Never force-push or directly commit to:

- `main` / `master`
- `develop`
- `staging` / `production`
- `release/*` branches

Always use pull requests for these branches.

## Quick Reference

### Creating a Feature Branch

```bash
git checkout -b feature/descriptive-name
```

### Checking What to Commit

```bash
git status                    # See all changes
git diff                      # Unstaged changes
git diff --cached             # Staged changes
git log --oneline -5          # Recent commit style
```

### Staging Selectively

```bash
git add path/to/specific/file.ext
git add -p                    # Interactive staging
```

### Writing Good Commits

```bash
# Simple commit
git commit -m "feat(auth): add OAuth2 login support"

# Multi-line commit
git commit -m "$(cat <<'EOF'
fix(api): resolve race condition in request handler

- Add mutex lock around shared state
- Implement request queuing for high load
- Add timeout handling for stale requests

Fixes #456
EOF
)"
```
