---
name: git-commits
description: Git commit best practices with conventional commits format and atomic commit principles. Use when committing code to ensure clear, meaningful commit history with proper type prefixes and semantic versioning support.
user-invocable: false
---

# Git Commits Skill

This skill enforces git commit best practices and conventional commits format.

## Conventional Commits Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Commit Types

| Type | Description | Semver |
|------|-------------|--------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `docs` | Documentation only | - |
| `style` | Formatting, no code change | - |
| `refactor` | Code restructuring | - |
| `perf` | Performance improvement | PATCH |
| `test` | Adding tests | - |
| `chore` | Maintenance tasks | - |
| `ci` | CI configuration | - |
| `build` | Build system changes | - |

## Examples

### Feature
```
feat(auth): add OAuth2 login support

Implement OAuth2 flow with Google and GitHub providers.
Includes token refresh and secure storage.

Closes #123
```

### Bug Fix
```
fix(api): handle null response in user endpoint

The /users endpoint crashed when the database returned null.
Added proper null checking and error response.
```

### Breaking Change
```
feat(api)!: change response format for /users endpoint

BREAKING CHANGE: Response now returns array instead of object.
Migration guide available in docs/migrations/v2.md
```

## Atomic Commits

Each commit should:
1. Represent ONE logical change
2. Be independently revertible
3. Pass all tests
4. Be complete (not "WIP")

### Bad Example
```
git commit -m "Fix bugs and add features and update docs"
```

### Good Example
```
git commit -m "fix(auth): prevent session timeout on refresh"
git commit -m "feat(dashboard): add export to CSV button"
git commit -m "docs(api): update authentication examples"
```

## Commit Message Rules

1. **Type is required** and lowercase
2. **Description** starts lowercase, no period
3. **Imperative mood**: "add" not "added" or "adds"
4. **First line** under 72 characters
5. **Body** wraps at 72 characters
6. **Breaking changes** marked with `!` or footer

## Claude Code Commit Footer

When committing with Claude Code, include:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```
