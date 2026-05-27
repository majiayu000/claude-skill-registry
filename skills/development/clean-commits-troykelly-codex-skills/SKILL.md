---
name: clean-commits
description: Use when committing code - ensures atomic, descriptive commits that leave the codebase in a merge-ready state at every point
---

# Clean Commits

## Overview

Every commit is atomic, descriptive, and leaves code in a working state.

**Core principle:** Anyone should be able to checkout any commit and have working code.

**Announce at use:** "I'm committing with a descriptive message following clean-commits standards."

## Commit Message Format

### Structure

```
[type](scope): Short description (max 72 chars)

[Optional body - what and why, not how]

[Optional footer - issue references, breaking changes]

Refs: #[ISSUE_NUMBER]
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding/fixing tests |
| `chore` | Maintenance, dependencies |

### Examples

```
feat(auth): Add user registration endpoint

Implement POST /api/users/register with email validation,
password hashing, and duplicate detection.

- Validates email format and uniqueness
- Hashes password with bcrypt
- Returns user object without password

Refs: #123
```

```
fix(auth): Prevent redirect loop on expired session

Session expiry was triggering redirect to login, which
checked session, found expired, and redirected again.

Now clears session cookie before redirecting.

Refs: #456
```

```
test(auth): Add integration tests for registration

Cover success case, duplicate email, invalid format,
and weak password scenarios.

Refs: #123
```

## Atomic Commits

### What Makes a Commit Atomic

| Atomic | Not Atomic |
|--------|------------|
| One logical change | Multiple unrelated changes |
| Passes all tests | Breaks tests |
| Complete feature slice | Half-implemented feature |
| Can be reverted cleanly | Reverts would break things |

### Signs of Non-Atomic Commits

- Commit message uses "and" to describe multiple things
- Diff includes unrelated files
- Some tests fail after commit
- "WIP" in commit message

### Splitting Large Changes

If you have multiple changes, commit them separately:

```bash
# Stage specific files
git add src/auth/register.ts
git add src/auth/register.test.ts
git commit -m "feat(auth): Add registration endpoint"

# Stage next logical unit
git add src/auth/login.ts
git add src/auth/login.test.ts
git commit -m "feat(auth): Add login endpoint"
```

## Working State Requirement

Every commit must leave the codebase in a state where:

- [ ] All tests pass
- [ ] Build succeeds
- [ ] Application runs
- [ ] No TypeScript errors
- [ ] No linting errors

**Before committing:**

```bash
# Run tests
pnpm test

# Check build
pnpm build

# Check types
pnpm typecheck

# Check lint
pnpm lint
```

If any fail, fix before committing.

## Commit Frequency

### Commit Often

- After each passing test in TDD cycle
- After each refactoring step
- After completing a logical unit

### Don't Wait Too Long

| Too Infrequent | Just Right |
|----------------|------------|
| "Implement entire feature" | "Add user model" |
| "Fix all bugs" | "Fix session expiry redirect" |
| "Update everything" | "Update auth dependencies" |

### Small is Good

Smaller commits are:
- Easier to review
- Easier to revert
- Easier to bisect
- Easier to understand

## The Commit Process

### 1. Stage Selectively

```bash
# Review what changed
git diff

# Stage specific files
git add [specific files]

# Or stage interactively
git add -p
```

### 2. Review Staged Changes

```bash
# See what will be committed
git diff --staged
```

### 3. Write Descriptive Message

```bash
# Short message (if simple)
git commit -m "fix(auth): Handle null user in session check"

# Long message (if complex)
git commit
# Opens editor for full message
```

### 4. Verify After Commit

```bash
# Check commit looks right
git show --stat

# Verify tests still pass
pnpm test
```

## Commit Message Body

When to include a body:

- **Why** the change was made (not just what)
- **Context** that isn't obvious from code
- **Trade-offs** or alternatives considered
- **Breaking changes** if any

### Body Examples

```
refactor(api): Extract validation middleware

Validation logic was duplicated across 12 endpoints.
Extracted to reusable middleware that can be composed.

Alternative considered: validation library.
Rejected because our rules are domain-specific.
```

```
fix(data): Use optimistic locking for updates

Race condition was causing lost updates when two users
edited the same record simultaneously.

BREAKING CHANGE: Update operations now require
version field in request body.
```

## Issue References

Always reference the issue:

```bash
# In commit message
Refs: #123

# Or if commit closes the issue
Closes: #123
```

## Amending Commits

### When to Amend

- Typo in message (if not pushed)
- Forgot to stage a file (if not pushed)

```bash
# Amend last commit (before push only!)
git add forgotten-file.ts
git commit --amend
```

### When NOT to Amend

- After pushing to remote
- Changing commits others have based work on

## Revert, Don't Delete

If a commit was wrong:

```bash
# Create a new commit that undoes the change
git revert [commit-sha]

# DON'T rewrite history on shared branches
# DON'T force push to fix mistakes
```

## Checklist

Before each commit:

- [ ] Tests pass
- [ ] Build succeeds
- [ ] Change is atomic (one logical unit)
- [ ] Message follows format
- [ ] Message describes why, not just what
- [ ] Issue is referenced
- [ ] No "WIP" or placeholder messages

## Integration

This skill is called by:
- `issue-driven-development` - Throughout development
- `pr-creation` - Before creating PR

This skill enforces:
- Reviewable history
- Revertible changes
- Clear project narrative
