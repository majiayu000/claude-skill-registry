---
name: git-github-ops
description: Manage GitHub and Git operations with Conventional Commits support. Create commits, push branches, create/approve/merge PRs. Use proactively when asked to commit changes, create pull requests, or manage GitHub workflows.
---

# GitHub & Git Operations Skill

This skill provides comprehensive guidance for managing Git and GitHub operations using native CLI commands, with full support for the Conventional Commits v1.0.0 specification.

## Prerequisites

Before using this skill, ensure you have:

1. **Git** (v2.23+)
   ```bash
   git --version
   ```

2. **GitHub CLI** (v2.0+)
   ```bash
   # Install
   brew install gh  # macOS

   # Authenticate
   gh auth login

   # Verify authentication
   gh auth status
   ```

## Git Command Reference

### Staging Changes

| Operation | Command |
|-----------|---------|
| Stage all changes | `git add -A` |
| Stage specific files | `git add <file1> <file2>` |
| Stage interactively | `git add -p` |
| Unstage file | `git restore --staged <file>` |
| Check staged changes | `git diff --cached --name-only` |

### Creating Commits

| Operation | Command |
|-----------|---------|
| Simple commit | `git commit -m "message"` |
| Commit with body | `git commit -m "subject" -m "body"` |
| Skip pre-commit hooks | `git commit --no-verify -m "message"` |
| Amend last commit | `git commit --amend -m "new message"` |
| Empty commit (for CI triggers) | `git commit --allow-empty -m "message"` |

### Branch Operations

| Operation | Command |
|-----------|---------|
| Get current branch | `git rev-parse --abbrev-ref HEAD` |
| Create new branch | `git checkout -b <branch-name>` |
| Switch branches | `git checkout <branch-name>` |
| Delete local branch | `git branch -d <branch-name>` |
| Delete remote branch | `git push origin --delete <branch-name>` |
| List branches | `git branch -a` |

### Status and History

| Operation | Command |
|-----------|---------|
| Check status | `git status` |
| Check status (porcelain) | `git status --porcelain` |
| View commit history | `git log --oneline` |
| Commits since branch | `git log <base>..HEAD --oneline` |
| Show diff | `git diff` |
| Show staged diff | `git diff --cached` |

### Push Operations

| Operation | Command |
|-----------|---------|
| Push with upstream | `git push -u origin <branch>` |
| Push current branch | `git push` |
| Force push | `git push --force` |
| Force push with lease (safer) | `git push --force-with-lease` |

### Pull and Fetch

| Operation | Command |
|-----------|---------|
| Pull changes | `git pull origin <branch>` |
| Fetch all | `git fetch --all` |
| Rebase on pull | `git pull --rebase origin <branch>` |

## GitHub CLI Command Reference

### Authentication

| Operation | Command |
|-----------|---------|
| Check auth status | `gh auth status` |
| Login | `gh auth login` |
| Logout | `gh auth logout` |

### Pull Request Creation

| Operation | Command |
|-----------|---------|
| Create PR | `gh pr create --title "title" --body "body"` |
| Create draft PR | `gh pr create --title "title" --body "body" --draft` |
| Create PR with base | `gh pr create --title "title" --body "body" --base <branch>` |
| Create PR (web browser) | `gh pr create --web` |

### Pull Request Management

| Operation | Command |
|-----------|---------|
| View PR | `gh pr view <number>` |
| View PR in browser | `gh pr view <number> --web` |
| List PRs | `gh pr list` |
| List PRs for branch | `gh pr list --head <branch> --json number,url` |
| Check PR status | `gh pr checks <number>` |
| Check if mergeable | `gh pr view <number> --json mergeable,mergeStateStatus` |

### Pull Request Review

| Operation | Command |
|-----------|---------|
| Approve PR | `gh pr review <number> --approve` |
| Approve with message | `gh pr review <number> --approve --body "message"` |
| Request changes | `gh pr review <number> --request-changes --body "message"` |
| Comment on PR | `gh pr review <number> --comment --body "message"` |

### Pull Request Merge

| Operation | Command |
|-----------|---------|
| Merge with squash | `gh pr merge <number> --squash` |
| Merge with merge commit | `gh pr merge <number> --merge` |
| Merge with rebase | `gh pr merge <number> --rebase` |
| Merge and delete branch | `gh pr merge <number> --squash --delete-branch` |
| Auto-merge when checks pass | `gh pr merge <number> --auto --squash` |

### Issues

| Operation | Command |
|-----------|---------|
| List issues | `gh issue list` |
| View issue | `gh issue view <number>` |
| Create issue | `gh issue create --title "title" --body "body"` |
| Close issue | `gh issue close <number>` |

## Conventional Commits Specification

### Message Format

```
<type>[(scope)][!]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type | Description | Version Bump |
|------|-------------|--------------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `docs` | Documentation changes | None |
| `style` | Code style (formatting) | None |
| `refactor` | Code refactoring | None |
| `test` | Adding/updating tests | None |
| `chore` | Maintenance tasks | None |
| `perf` | Performance improvements | PATCH |
| `ci` | CI/CD changes | None |
| `build` | Build system changes | None |
| `revert` | Revert previous commit | Varies |

### Breaking Changes

Breaking changes trigger a MAJOR version bump. Indicate them by:

1. **Append '!' after type/scope:**
   ```bash
   git commit -m "feat!: remove deprecated API endpoints"
   git commit -m "feat(api)!: change response format"
   ```

2. **Use BREAKING CHANGE footer:**
   ```bash
   git commit -m "feat: update user model" -m "" -m "BREAKING CHANGE: email field is now required"
   ```

### Commit Examples

```bash
# Simple feature
git commit -m "feat: add dark mode toggle"

# Feature with scope
git commit -m "feat(ui): add settings page"

# Bug fix with issue reference
git commit -m "fix(auth): resolve login timeout" -m "" -m "Fixes #123"

# Breaking change
git commit -m "feat!: redesign API response format" -m "" -m "BREAKING CHANGE: all responses now use snake_case"

# Documentation
git commit -m "docs: update API documentation"

# Chore with scope
git commit -m "chore(deps): update dependencies"

# Multiple footers
git commit -m "feat(payments): implement Stripe integration" -m "" -m "Closes #100" -m "Reviewed-by: Alice <alice@example.com>"
```

### Rules

- Keep subject line under 72 characters
- Use lowercase for type and scope
- Use imperative mood ("add" not "added" or "adds")
- Do not end subject with a period
- Separate subject from body with blank line

## Common Workflows

### Feature Development

```bash
# 1. Create feature branch
git checkout -b feat/user-profile

# 2. Make changes and stage them
git add -A

# 3. Create conventional commit
git commit -m "feat(users): add profile page" -m "" -m "Implement user profile with avatar upload and bio editing."

# 4. Push to remote with upstream tracking
git push -u origin feat/user-profile

# 5. Create pull request
gh pr create --title "feat(users): add profile page" --body "## Summary
- Add user profile page with avatar upload
- Implement bio editing functionality

## Test Plan
- [ ] Test avatar upload with various file types
- [ ] Verify bio saves correctly"
```

### Bug Fix

```bash
# 1. Create fix branch
git checkout -b fix/login-timeout

# 2. Make changes and stage
git add -A

# 3. Create fix commit with issue reference
git commit -m "fix(auth): resolve login timeout issue" -m "" -m "Increase session timeout from 5 to 30 minutes." -m "" -m "Fixes #456"

# 4. Push and create PR
git push -u origin fix/login-timeout
gh pr create --title "fix(auth): resolve login timeout issue" --body "## Summary
- Fix session timeout causing premature logouts

## Test Plan
- [ ] Verify sessions persist for 30 minutes
- [ ] Test remember me functionality

Fixes #456"
```

### Code Review and Merge

```bash
# 1. Review PR changes
gh pr view 123
gh pr diff 123

# 2. Check if CI passes
gh pr checks 123

# 3. Approve PR
gh pr review 123 --approve --body "LGTM! Code looks clean and tests pass."

# 4. Merge with squash and delete branch
gh pr merge 123 --squash --delete-branch
```

### Hotfix

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix

# 2. Make fix and commit
git add -A
git commit -m "fix(security): patch XSS vulnerability" -m "" -m "Sanitize user input in comment rendering." -m "" -m "Security: CVE-2024-1234"

# 3. Push and create urgent PR
git push -u origin hotfix/critical-security-fix
gh pr create --title "fix(security): patch XSS vulnerability" --body "## URGENT: Security Fix

Patches critical XSS vulnerability in comment rendering.

CVE: CVE-2024-1234

## Test Plan
- [ ] Verify malicious scripts are sanitized
- [ ] Test comment rendering still works"

# 4. Fast-track review and merge
gh pr merge <number> --squash --delete-branch
```

### Rebase and Update

```bash
# 1. Fetch latest changes
git fetch origin main

# 2. Rebase current branch on main
git rebase origin/main

# 3. Resolve conflicts if any, then continue
git add -A
git rebase --continue

# 4. Force push (with lease for safety)
git push --force-with-lease
```

### Draft PR Workflow

```bash
# 1. Create branch and make initial changes
git checkout -b feat/experimental-feature
git add -A
git commit -m "feat: add experimental feature (WIP)"

# 2. Push and create draft PR for early feedback
git push -u origin feat/experimental-feature
gh pr create --title "feat: add experimental feature" --body "WIP - seeking early feedback" --draft

# 3. Continue development, push updates
git add -A
git commit -m "feat: complete experimental feature"
git push

# 4. Mark ready for review when done
gh pr ready <number>
```

## Troubleshooting

### Authentication Issues

```bash
# Check GitHub CLI auth status
gh auth status

# Re-authenticate if needed
gh auth login

# Check SSH key
ssh -T git@github.com
```

### Push Rejected

```bash
# If behind remote, pull and rebase
git pull --rebase origin <branch>

# Then push
git push

# If after intentional rebase, force push (with lease)
git push --force-with-lease
```

### Merge Conflicts

```bash
# Fetch and rebase
git fetch origin main
git rebase origin/main

# After resolving conflicts in each file
git add <resolved-file>
git rebase --continue

# If you want to abort
git rebase --abort
```

### Pre-commit Hook Failures

```bash
# Fix the issues reported by hooks, then
git add -A
git commit -m "your message"

# Skip hooks only if absolutely necessary (not recommended)
git commit --no-verify -m "your message"
```

### Wrong Branch

```bash
# Stash current changes
git stash

# Switch to correct branch
git checkout <correct-branch>

# Apply stashed changes
git stash pop
```

### Undo Last Commit (keeping changes)

```bash
# Undo last commit but keep changes staged
git reset --soft HEAD~1

# Undo last commit and unstage changes
git reset HEAD~1
```

## Documentation

- [Conventional Commits Reference](./docs/conventional-commits.md)
- [PR Workflows](./docs/pr-workflows.md)
- [Troubleshooting Guide](./docs/troubleshooting.md)

## Examples

See [commit-examples.md](./templates/commit-examples.md) for more commit message examples.

## External Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Semantic Versioning](https://semver.org/)
