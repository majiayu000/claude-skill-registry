---
name: git-commit-smart
description: Generates meaningful, conventional commit messages automatically. Use when committing code changes. Analyzes diff to create descriptive commits following best practices.
---
# Smart Git Commit

> Inspired by [claude-code-plugins-plus](https://github.com/jeremylongshore/claude-code-plugins-plus)

## Purpose

Automatically generate meaningful commit messages by analyzing staged changes, following conventional commit format.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no new feature or fix |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `chore` | Maintenance tasks |
| `ci` | CI/CD changes |
| `build` | Build system changes |

### Scope

Optional, indicates the section of codebase:
- `auth`, `api`, `ui`, `db`, `config`, etc.

### Subject

- Imperative mood ("add" not "added")
- No period at end
- Max 50 characters
- Lowercase

### Body

- Explain WHAT and WHY, not HOW
- Wrap at 72 characters
- Separate from subject with blank line

### Footer

- Breaking changes: `BREAKING CHANGE: description`
- Issue references: `Closes #123`, `Fixes #456`

## Workflow

### 1. Analyze Changes

```bash
# View staged changes
git diff --staged

# View changed files
git diff --staged --name-only

# View stats
git diff --staged --stat
```

### 2. Determine Type

Based on changes:
- New files with features → `feat`
- Modified files fixing issues → `fix`
- Only .md files → `docs`
- Only test files → `test`
- package.json, configs → `chore` or `build`

### 3. Identify Scope

Look at file paths:
- `src/auth/*` → scope: `auth`
- `src/api/*` → scope: `api`
- `tests/*` → scope: `test`
- Multiple areas → omit scope or use broader term

### 4. Write Subject

Summarize the change:
```
feat(auth): add OAuth2 login support
fix(api): handle null response in user endpoint
docs: update README with installation steps
refactor(db): extract query builder to separate module
```

### 5. Write Body (if needed)

For complex changes:
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with support for
Google and GitHub providers. This allows users to sign
in without creating a separate account.

- Add OAuth2 client configuration
- Implement callback handlers
- Store OAuth tokens securely
- Add provider selection UI
```

## Examples

### Simple Feature
```
feat(ui): add dark mode toggle
```

### Bug Fix with Issue Reference
```
fix(api): prevent duplicate user creation

Check for existing email before inserting new user record.
Race condition could cause duplicate entries when requests
arrived simultaneously.

Fixes #234
```

### Breaking Change
```
feat(api)!: change response format to JSON:API

BREAKING CHANGE: All API responses now follow JSON:API
specification. Clients must update their parsers.

Migration guide: docs/migration-v2.md
```

### Multiple Files, Single Purpose
```
refactor: extract validation logic to shared module

Move duplicate validation code from controllers to
a shared validation module. Reduces code duplication
and ensures consistent validation across endpoints.
```

## Anti-Patterns to Avoid

```
❌ "fix stuff"
❌ "update code"
❌ "WIP"
❌ "changes"
❌ "fixed bug"
❌ "misc updates"
❌ Commits with 50+ files and vague message
```

## Best Practices

1. **Atomic commits** - One logical change per commit
2. **Meaningful messages** - Future you will thank present you
3. **Reference issues** - Link to tickets/issues when relevant
4. **Review before commit** - `git diff --staged` always
5. **Don't commit secrets** - Check for API keys, passwords

## Quick Reference

```bash
# Stage specific files
git add <file>

# Stage all changes
git add -A

# Interactive staging
git add -p

# Commit with message
git commit -m "type(scope): subject"

# Commit with body
git commit -m "type(scope): subject" -m "body paragraph"

# Amend last commit
git commit --amend
```
