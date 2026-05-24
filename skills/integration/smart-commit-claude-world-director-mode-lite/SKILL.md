---
name: smart-commit
description: Conventional Commits with quality checks
user-invocable: true
---

# Smart Commit

Create a high-quality commit for current changes.

## Pre-Commit Checklist

### Scope Check
- [ ] Solves one problem only
- [ ] No unrelated changes
- [ ] No debug code
- [ ] No temporary files

### Quality Check
- [ ] All tests pass
- [ ] Code is formatted
- [ ] No linting errors
- [ ] Documentation updated

---

## Commit Message Format

```
<type>(<scope>): <description>

<body>

<footer>
```

### Type (Required)
| Type | Use When |
|------|----------|
| `feat` | New feature (user-visible) |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding/updating tests |
| `refactor` | Code restructure (no behavior change) |
| `style` | Formatting (no logic change) |
| `chore` | Maintenance, dependencies |
| `perf` | Performance improvement |

### Scope (Optional)
Module, component, or file affected:
- `feat(auth): add login endpoint`
- `fix(api): handle null response`
- `docs(readme): update installation steps`

### Description (Required)
- 50 characters or less
- Present tense, imperative mood
- Lowercase first letter
- No period at end
- Describe WHAT, not HOW

---

## Examples

### Feature
```
feat(user): add email verification

Implement email verification flow for new user registration.
Users must verify email before accessing protected features.

Closes #42
```

### Bug Fix
```
fix(api): handle null response in user endpoint

Previously threw uncaught exception when user not found.
Now returns 404 with proper error message.

Fixes #67
```

---

## Commit Checklist

Before committing:
- [ ] Follows Conventional Commits format
- [ ] Subject clearly describes the change
- [ ] One commit = one logical change
- [ ] No sensitive information (.env, credentials)
- [ ] All tests pass
