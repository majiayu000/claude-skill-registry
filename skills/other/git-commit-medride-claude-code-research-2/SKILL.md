---
name: git-commit
description: Generate commit messages following conventional commits format
---

# Git Commit Skill

Generate consistent, descriptive commit messages following the Conventional Commits specification.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Components

| Part | Required | Description |
|------|----------|-------------|
| type | Yes | Category of change |
| scope | No | Module/component affected |
| subject | Yes | Brief description (imperative mood) |
| body | No | Detailed explanation |
| footer | No | Breaking changes, issue refs |

## Commit Types

| Type | When to Use | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add password reset flow` |
| `fix` | Bug fix | `fix(cart): correct total calculation` |
| `refactor` | Code restructuring | `refactor(api): extract validation logic` |
| `docs` | Documentation only | `docs: update API examples` |
| `style` | Formatting changes | `style: fix indentation` |
| `test` | Adding/updating tests | `test(user): add signup edge cases` |
| `chore` | Maintenance tasks | `chore: update dependencies` |
| `perf` | Performance improvement | `perf(query): add index for user lookup` |
| `ci` | CI/CD changes | `ci: add deployment workflow` |
| `build` | Build system changes | `build: configure webpack splitting` |

## Writing Guidelines

### Subject Line
- Max 50 characters
- Imperative mood ("Add" not "Added" or "Adds")
- No period at the end
- Capitalize first letter

### Body
- Wrap at 72 characters
- Explain **what** and **why**, not how
- Separate from subject with blank line

### Footer
- Reference issues: `Fixes #123`, `Closes #456`
- Note breaking changes: `BREAKING CHANGE: description`

## Process

1. **Check staged changes**
   ```bash
   git diff --staged
   ```

2. **Analyze the changes**
   - What files were modified?
   - What functionality changed?
   - Is this a feature, fix, or refactor?

3. **Determine scope**
   - What module/component is affected?
   - Use lowercase, hyphenated if needed

4. **Write the subject**
   - Start with imperative verb
   - Be specific but concise

5. **Add body if needed**
   - Complex changes need explanation
   - Bug fixes should mention root cause

6. **Add footer if applicable**
   - Link to issues
   - Note breaking changes

## Examples

### Simple Feature
```
feat(user): add email verification on signup
```

### Bug Fix with Context
```
fix(checkout): prevent double submission

Users could click the submit button multiple times before
the form disabled, causing duplicate orders.

Added loading state and disabled button during submission.

Fixes #234
```

### Breaking Change
```
feat(api): change authentication to use JWT

Migrate from session-based auth to JWT tokens.
Client applications need to update their auth handling.

BREAKING CHANGE: Authentication now requires Bearer token
in Authorization header instead of session cookie.

Migration guide: docs/migration/jwt-auth.md
```

### Refactoring
```
refactor(validation): extract form validation to shared util

Move repeated validation logic from multiple form components
into a shared validation utility for consistency.

No functional changes.
```

## Anti-Patterns

| Don't | Do |
|-------|-----|
| `fix stuff` | `fix(auth): handle expired token gracefully` |
| `wip` | `feat(dashboard): add chart component (partial)` |
| `changes` | `refactor(utils): simplify date formatting` |
| `Update file.ts` | `fix(user): correct email validation regex` |
| Mixed changes | Separate commits for separate concerns |

## Quick Reference

```
feat:     New feature
fix:      Bug fix
refactor: Code restructuring (no behavior change)
docs:     Documentation
style:    Formatting (no code change)
test:     Tests
chore:    Maintenance
perf:     Performance
```
