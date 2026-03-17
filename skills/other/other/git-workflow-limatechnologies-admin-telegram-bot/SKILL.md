---
name: git-workflow
description: Git workflow patterns and best practices. Branch management, conventional commits, direct merge to main, hooks. Use when working with git operations.
allowed-tools: Bash, Read, Grep, Glob
---

# Git Workflow - Version Control Best Practices

## Purpose

Expert guidance for Git:

- **Branch Management** - Feature, fix, release branches
- **Conventional Commits** - Standardized commit messages
- **Direct Merge to Main** - NO Pull Requests, merge directly
- **Git Hooks** - Automated quality gates
- **Merge Strategies** - Local merge, no remote PRs

---

## Branch Naming Conventions

### Format

```
<type>/<description>
```

### Types

| Type        | Use Case               |
| ----------- | ---------------------- |
| `feature/`  | New functionality      |
| `fix/`      | Bug fixes              |
| `refactor/` | Code restructuring     |
| `test/`     | Test additions/changes |
| `docs/`     | Documentation only     |
| `chore/`    | Maintenance tasks      |

### Examples

```bash
feature/user-authentication
feature/add-dark-mode
fix/login-validation-error
fix/memory-leak-dashboard
refactor/api-client-structure
test/e2e-checkout-flow
docs/api-documentation
chore/update-dependencies
```

---

## Branch Workflow

### Create Feature Branch

```bash
# From main branch
git checkout main
git pull origin main

# Create and switch to new branch
git checkout -b feature/my-feature

# Alternative
git switch -c feature/my-feature
```

### Keep Branch Updated

```bash
# Fetch latest changes
git fetch origin

# Rebase on main
git rebase origin/main

# If conflicts, resolve and continue
git add .
git rebase --continue

# Or abort if needed
git rebase --abort
```

### Push Branch

```bash
# First push (set upstream)
git push -u origin feature/my-feature

# Subsequent pushes
git push

# After rebase (force with lease is safer)
git push --force-with-lease
```

---

## Conventional Commits

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type       | Description                 |
| ---------- | --------------------------- |
| `feat`     | New feature for the user    |
| `fix`      | Bug fix for the user        |
| `docs`     | Documentation only          |
| `style`    | Formatting, no code change  |
| `refactor` | Code change, no feature/fix |
| `perf`     | Performance improvement     |
| `test`     | Adding/updating tests       |
| `chore`    | Maintenance, deps update    |
| `ci`       | CI/CD changes               |
| `build`    | Build system changes        |

### Examples

```bash
# Feature
git commit -m "feat(auth): add OAuth2 Google login"

# Fix
git commit -m "fix(cart): prevent duplicate items on rapid click"

# With body (use HEREDOC for multi-line)
git commit -m "$(cat <<'EOF'
feat(api): add rate limiting middleware

- Implement token bucket algorithm
- Add configurable limits per endpoint
- Include bypass for authenticated users

Closes #123
EOF
)"
```

### Scopes (Project-Specific)

```
api, auth, cart, checkout, dashboard, db, docker, ui, tests
```

---

## Commit Message Template

```bash
# Set up template
git config commit.template .gitmessage

# .gitmessage file
# <type>(<scope>): <description>
#
# [body - explain what and why]
#
# [footer - issue references]
#
# Types: feat, fix, docs, style, refactor, perf, test, chore, ci, build
# Scopes: api, auth, ui, db, tests, docker, etc.
```

---

## Direct Merge to Main (NO Pull Requests)

### Complete Workflow

This project uses **direct merge to main** instead of Pull Requests.

```bash
# 1. Create feature branch
git checkout main
git pull origin main
git checkout -b feature/my-feature

# 2. Work on feature, commit changes
git add -A
git commit -m "$(cat <<'EOF'
feat(scope): description

- Detail 1
- Detail 2

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# 3. Switch to main
git checkout main

# 4. Merge branch
git merge feature/my-feature

# 5. Sync with remote
git pull origin main --rebase || true
git push origin main

# 6. Delete feature branch (cleanup)
git branch -d feature/my-feature
```

### Key Rules

| Rule | Description |
|------|-------------|
| NO Pull Requests | Merge directly to main |
| Always end on main | Checkout main after merge |
| Delete branch after merge | Keep repo clean |
| Push after merge | Sync with remote |

---

## Git Hooks (Husky)

### Setup

```bash
# Install Husky
bun add -D husky lint-staged

# Initialize
bunx husky init

# Create hooks
echo "bun run lint-staged" > .husky/pre-commit
echo "bun run typecheck" > .husky/pre-push
```

### lint-staged Configuration

```json
// package.json
{
	"lint-staged": {
		"*.{ts,tsx}": ["eslint --fix", "prettier --write"],
		"*.{json,md}": ["prettier --write"]
	}
}
```

### Commit Message Hook

```bash
# .husky/commit-msg
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

bunx --no -- commitlint --edit "$1"
```

### commitlint Configuration

```javascript
// commitlint.config.js
export default {
	extends: ['@commitlint/config-conventional'],
	rules: {
		'type-enum': [
			2,
			'always',
			['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'chore', 'ci', 'build'],
		],
		'scope-enum': [1, 'always', ['api', 'auth', 'ui', 'db', 'tests', 'docker']],
		'subject-case': [2, 'always', 'lower-case'],
		'body-max-line-length': [2, 'always', 100],
	},
};
```

---

## Merge Strategies (Local)

### Standard Merge (Recommended)

```bash
# Simple merge - preserves commits
git checkout main
git merge feature/my-feature
git push origin main
```

### Squash Merge (Clean History)

```bash
# Combines all branch commits into one
git checkout main
git merge --squash feature/my-feature
git commit -m "feat: complete feature description"
git push origin main
```

### Rebase Then Merge (Linear History)

```bash
# Rebase branch first
git checkout feature/my-feature
git rebase main
git checkout main
git merge feature/my-feature  # Fast-forward
git push origin main
```

### Recommendation

| Branch Type | Strategy |
| ----------- | -------- |
| feature/\*  | Merge    |
| fix/\*      | Merge    |
| refactor/\* | Squash   |
| chore/\*    | Squash   |

---

## Useful Git Commands

### Status & Diff

```bash
# Status
git status

# Diff unstaged
git diff

# Diff staged
git diff --staged

# Diff between branches
git diff main..feature/my-feature
```

### History

```bash
# Recent commits
git log --oneline -10

# Commits in branch not in main
git log main..HEAD --oneline

# Files changed in last commit
git diff-tree --no-commit-id --name-only -r HEAD

# Who changed a file
git blame src/file.ts
```

### Undo Changes

```bash
# Unstage file
git reset HEAD file.ts

# Discard local changes
git checkout -- file.ts

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Stash

```bash
# Stash changes
git stash

# Stash with message
git stash push -m "WIP: feature X"

# List stashes
git stash list

# Apply latest stash
git stash pop

# Apply specific stash
git stash apply stash@{2}
```

---

## Agent Integration

This skill is used by:

- **commit-manager** agent - commits and merges to main
- **branch-manager** agent - creates feature branches
- **quality-checker** for pre-commit validation

---

## FORBIDDEN

1. **Force push to main/master** - Never without explicit permission
2. **Commit directly to main** - Use feature branches
3. **Skip hooks** - Don't use `--no-verify` unless absolutely necessary
4. **Vague commit messages** - Be specific and descriptive
5. **Large unrelated changes in one commit** - Keep commits focused
6. **Committing secrets** - Never commit .env, tokens, passwords

---

## Version

- **v1.0.0** - Initial implementation based on 2024-2025 Git workflow patterns
