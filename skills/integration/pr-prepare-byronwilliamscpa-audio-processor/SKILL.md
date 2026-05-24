---
name: pr-prepare
description: "Prepare pull request descriptions following project template. Activates on: prepare PR, create PR, pull request, ready for PR, draft PR, write PR"
---

# PR Preparation Skill

Automatically prepare pull request descriptions following project standards.

## Activation

This skill activates on keywords:
- "prepare PR", "prepare the PR", "prepare a PR"
- "create PR", "create pull request"
- "PR description", "pull request description"
- "ready for PR", "ready to PR"
- "draft PR", "write PR"

## Workflow

When activated, follow these steps:

### 1. Gather Context

Run these commands to understand the changes:

```bash
# Current state
git status

# Branch comparison (adjust 'main' if different base branch)
git log $(git merge-base HEAD main)..HEAD --oneline

# Files changed
git diff $(git merge-base HEAD main)..HEAD --stat

# Actual diff (for smaller changes)
git diff $(git merge-base HEAD main)..HEAD
```

### 2. Analyze Changes

Identify:
- **Components modified**: Which files/modules changed
- **Purpose**: Why these changes were made
- **Impact**: Benefits, risks, breaking changes
- **Testing**: What validation was done or needed

### 3. Generate PR Description

Use this template format:

```markdown
## Summary

[1-3 sentences: what changed and why]

## Changes

- **[Component]**: [What changed and why]
- **[Component]**: [What changed and why]

## Impact

- ✅ [Key benefit or outcome]
- ✅ [Another benefit]
- ✅ No breaking changes

## Testing

- [ ] Tests pass (`uv run pytest`)
- [ ] Linting passes (`uv run ruff check`)

## Notes

[Optional: known issues, follow-up work, dependencies]
```

### 4. Suggest PR Title

Follow conventional commits format:

| Type | When to Use |
|------|-------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code restructuring |
| `test:` | Adding tests |
| `perf:` | Performance improvement |
| `chore:` | Maintenance, dependencies |

### 6. Output

Present the complete PR description ready to copy-paste into GitHub.

Remind the user:
- CodeRabbit will auto-fill `@coderabbitai summary` placeholder
- They can push and create PR with `gh pr create`

## Example Interaction

**User**: "Can you prepare the PR for this branch?"

**Claude**:
1. Runs git commands to gather context
2. Analyzes the changes
3. Outputs:

---

**Suggested Title**: `feat: add user authentication with OAuth2`

**PR Description**:

```markdown
## Summary

Add OAuth2 authentication supporting Google and GitHub providers.

## Changes

- **auth/oauth.py**: OAuth2 client implementation with token refresh
- **api/routes/auth.py**: Login, logout, and callback endpoints
- **models/user.py**: User model with OAuth provider fields

## Impact

- ✅ Users can sign in with Google or GitHub
- ✅ Secure session management with httponly cookies
- ✅ No breaking changes to existing API

## Testing

- [x] Tests pass (`uv run pytest`)
- [x] Linting passes (`uv run ruff check`)

## Notes

Follow-up: Add Microsoft provider support
```

---

Ready to copy! Push with:
```bash
git push -u origin HEAD
gh pr create --fill
```
