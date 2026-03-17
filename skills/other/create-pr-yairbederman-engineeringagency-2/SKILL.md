---
name: create-pr
description: Creates GitHub pull requests with properly formatted titles. Use when creating PRs, submitting changes for review, or when the user says /pr or asks to create a pull request.
---

# Create Pull Request

Creates GitHub PRs with properly formatted titles following conventional commit standards.

## PR Title Format

```
<type>(<scope>): <summary>
```

### Types (required)

| Type       | Description                                      | Changelog |
|------------|--------------------------------------------------|-----------|
| `feat`     | New feature                                      | Yes       |
| `fix`      | Bug fix                                          | Yes       |
| `perf`     | Performance improvement                          | Yes       |
| `test`     | Adding/correcting tests                          | No        |
| `docs`     | Documentation only                               | No        |
| `refactor` | Code change (no bug fix or feature)              | No        |
| `build`    | Build system or dependencies                     | No        |
| `ci`       | CI configuration                                 | No        |
| `chore`    | Routine tasks, maintenance                       | No        |

### Scopes (optional but recommended)

- `API` - Public API changes
- `core` - Core/backend/private API
- `editor` - Editor UI changes
- `ui` - User interface changes
- `db` - Database changes

### Summary Rules

- Use imperative present tense: "Add" not "Added"
- Capitalize first letter
- No period at the end
- No ticket IDs in title (put in body)
- Add `(no-changelog)` suffix to exclude from changelog

## Steps

1. **Check current state**:
   ```bash
   git status
   git diff --stat
   git log origin/main..HEAD --oneline
   ```

2. **Analyze changes** to determine:
   - Type: What kind of change is this?
   - Scope: What area does it affect?
   - Summary: What does it do?

3. **Create PR with GitHub CLI**:
   ```bash
   gh pr create --title "<type>(<scope>): <summary>" --body "<body>"
   ```

## PR Body Template

```markdown
## Summary
Brief description of the changes.

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual verification done

## Related Issues
Closes #123
```

### Linking Issues

Link to GitHub issues using keywords to auto-close:
- `closes #123` / `fixes #123` / `resolves #123`

### Checklist

All items should be addressed before merging:
- PR title follows conventions
- Docs updated or follow-up ticket created
- Tests included (bugs need regression tests, features need coverage)

## Examples

### Feature in editor
```
feat(editor): Add workflow performance metrics display
```

### Bug fix in core
```
fix(core): Resolve memory leak in execution engine
```

### Breaking change (add exclamation mark before colon)
```
feat(API)!: Remove deprecated v1 endpoints
```

### No changelog entry
```
refactor(core): Simplify error handling (no-changelog)
```

### No scope (affects multiple areas)
```
chore: Update dependencies to latest versions
```

## Validation

The PR title must match this pattern:
```
^(feat|fix|perf|test|docs|refactor|build|ci|chore|revert)(\([a-zA-Z0-9 ]+\))?!?: [A-Z].+[^.]$
```

Key validation rules:
- Type must be one of the allowed types
- Scope is optional but must be in parentheses if present
- Exclamation mark for breaking changes goes before the colon
- Summary must start with capital letter
- Summary must not end with a period
