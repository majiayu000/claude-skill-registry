---
name: commit-conventions
description: >
  Enforce conventional commits format with proper types, scopes, and breaking change notation.
  Use when the user is committing code, writing commit messages, asks about commit format,
  or when you are about to create a git commit. Always apply this skill before running git commit.
---

# Conventional Commits

Standard format for commit messages that enables automated changelogs, semantic versioning, and clear project history.

## When to Use

- Writing any git commit message
- Reviewing commit history for consistency
- Setting up commit linting (commitlint, husky)
- Generating changelogs or release notes
- Any time `git commit` is about to be executed

## Core Patterns

### Commit Message Structure

Follow this exact format:

```
<type>(<optional-scope>): <description>

<optional body>

<optional footer(s)>
```

The first line (subject) must be under 72 characters. Use imperative mood ("add feature" not "added feature" or "adds feature").

```bash
# Simple commit
git commit -m "feat: add user registration endpoint"

# With scope
git commit -m "fix(auth): prevent token refresh race condition"

# With body and footer
git commit -m "feat(api): add pagination to list endpoints

Implement cursor-based pagination for all collection endpoints.
Default page size is 20, max is 100.

Closes #142"
```

### Commit Types

| Type       | When to Use                              | Triggers Version Bump |
|------------|------------------------------------------|-----------------------|
| `feat`     | New feature or capability                | MINOR (0.X.0)         |
| `fix`      | Bug fix                                  | PATCH (0.0.X)         |
| `refactor` | Code change that neither fixes nor adds  | None                  |
| `docs`     | Documentation only                       | None                  |
| `test`     | Adding or fixing tests                   | None                  |
| `chore`    | Maintenance, deps, tooling              | None                  |
| `perf`     | Performance improvement                  | None                  |
| `ci`       | CI/CD configuration changes              | None                  |
| `style`    | Formatting, whitespace, semicolons       | None                  |
| `build`    | Build system or external deps            | None                  |
| `revert`   | Reverts a previous commit                | Depends               |

### Breaking Changes

Mark breaking changes with `!` after the type/scope, and include a `BREAKING CHANGE:` footer:

```bash
# Breaking change with bang notation
git commit -m "feat(api)!: change authentication from API keys to OAuth2

BREAKING CHANGE: All API consumers must migrate to OAuth2 tokens.
API key authentication is removed entirely."

# Breaking change in refactor
git commit -m "refactor!: rename User model fields

BREAKING CHANGE: firstName -> givenName, lastName -> familyName.
Run migration 2024_03_rename_user_fields."
```

### Scopes

Scopes indicate the area of the codebase affected. Keep them consistent within a project:

```bash
# Good: consistent, short scopes
feat(auth): add SSO login
fix(auth): handle expired refresh tokens
feat(api): add rate limiting middleware
fix(ui): correct modal z-index on mobile
chore(deps): upgrade express to v5
test(api): add integration tests for /users

# Bad: inconsistent or verbose scopes
feat(authentication-module): add SSO          # too verbose
fix(src/components/Modal): fix z-index        # file path as scope
feat(USER_API): add endpoint                  # inconsistent casing
```

## Anti-Patterns

### What NOT to Do

- **Vague messages**: `fix: stuff`, `chore: updates`, `feat: changes`
- **Past tense**: `feat: added login page` (use `feat: add login page`)
- **Uppercase first letter**: `feat: Add login` (use `feat: add login`)
- **Trailing period**: `fix: correct null check.` (drop the period)
- **Multiple concerns**: One commit doing a feat + fix + refactor — split them
- **Missing type**: `update dependencies` (use `chore: update dependencies`)
- **Type as description**: `refactor: refactor auth module` (use `refactor(auth): extract token validation`)

```bash
# BAD
git commit -m "fixed bug"
git commit -m "WIP"
git commit -m "feat: Added new feature to handle the user login flow and also fixed a bug"

# GOOD
git commit -m "fix(auth): prevent null pointer on missing session cookie"
git commit -m "feat(auth): add login flow with email verification"
```

## Quick Reference

```
feat:     New feature                    -> MINOR version bump
fix:      Bug fix                        -> PATCH version bump
refactor: Code restructuring             -> No version bump
docs:     Documentation                  -> No version bump
test:     Tests                          -> No version bump
chore:    Maintenance                    -> No version bump
perf:     Performance                    -> No version bump
ci:       CI/CD changes                  -> No version bump
style:    Formatting only                -> No version bump
build:    Build system                   -> No version bump
revert:   Revert previous commit         -> Depends

Format:   <type>(<scope>): <description>
Breaking: Add ! after type/scope + BREAKING CHANGE footer
Subject:  Imperative, lowercase, no period, under 72 chars
Body:     Wrap at 72 chars, explain WHY not WHAT
```
