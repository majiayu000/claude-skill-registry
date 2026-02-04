---
name: pr-creation
description: Use after completing implementation - create pull request with complete documentation, proper labels, linked issues, and verification summary
---

# PR Creation

## Overview

Create pull requests with complete documentation and proper linking.

**Core principle:** A PR should tell the complete story of the change.

**Announce at start:** "I'm creating a PR with complete documentation."

## Before Creating PR

Verify these prerequisites:

- [ ] All tests pass locally
- [ ] Build succeeds locally
- [ ] Code review complete (`comprehensive-review`)
- [ ] All findings addressed (`apply-all-findings`)
- [ ] Commits are clean and atomic (`clean-commits`)
- [ ] Branch is up to date with target

### Ensure Branch is Current

```bash
# Fetch latest
git fetch origin

# Rebase on target (usually main)
git rebase origin/main

# Or merge if preferred
git merge origin/main

# Resolve any conflicts
# Push updated branch
git push --force-with-lease  # Safe force push after rebase
```

## PR Documentation Structure

### Title

Format: `[Type] Brief description (#issue)`

```
feat: Add user authentication (#123)
fix: Resolve session timeout loop (#456)
refactor: Extract validation middleware (#789)
docs: Update API documentation (#101)
chore: Update dependencies (#202)
```

### Body Template

```markdown
## Summary

[2-3 sentences describing what this PR does and why]

## Changes

- [Bullet point of key change 1]
- [Bullet point of key change 2]
- [Bullet point of key change 3]

## Related Issues

Closes #[ISSUE_NUMBER]

<!-- If multiple issues -->
Relates to #[OTHER_ISSUE]
Depends on #[DEPENDENCY_PR]

## Verification

### Automated Tests
- [x] Unit tests pass
- [x] Integration tests pass
- [ ] E2E tests pass (if applicable)

### Manual Verification
- [x] [Criterion 1 from acceptance criteria]
- [x] [Criterion 2 from acceptance criteria]
- [x] [Criterion 3 from acceptance criteria]

### Screenshots (if UI changes)

| Before | After |
|--------|-------|
| ![before](url) | ![after](url) |

## Checklist

- [x] Tests added/updated
- [x] Documentation updated
- [x] Types are complete (no `any`)
- [x] Code follows style guide
- [x] Self-review completed

## Notes for Reviewers

[Any special considerations, areas to focus on, or context]
```

## Creating the PR

### Using GitHub CLI

```bash
# Create PR with full body
gh pr create \
  --title "feat: Add user authentication (#123)" \
  --body "$(cat <<'EOF'
## Summary

Implements user authentication with JWT tokens and session management.
Adds login, logout, and protected route middleware.

## Changes

- Add authentication service with JWT signing
- Add login and logout endpoints
- Add authentication middleware for protected routes
- Add session management with Redis

## Related Issues

Closes #123

## Verification

### Automated Tests
- [x] Unit tests pass (47 new tests)
- [x] Integration tests pass
- [x] E2E tests pass

### Manual Verification
- [x] User can log in with valid credentials
- [x] Invalid credentials show error message
- [x] Session persists across page refreshes
- [x] Logout clears session

## Checklist

- [x] Tests added/updated
- [x] Documentation updated
- [x] Types are complete
- [x] Code follows style guide
- [x] Self-review completed
EOF
)" \
  --base main \
  --head feature/issue-123-user-authentication
```

### Adding Labels

```bash
# Add labels after creation
gh pr edit [PR_NUMBER] --add-label "feature,needs-review"

# Or during creation
gh pr create ... --label "feature" --label "needs-review"
```

### Adding Reviewers

```bash
# Request reviewers
gh pr edit [PR_NUMBER] --add-reviewer username1,username2

# Or during creation
gh pr create ... --reviewer username1
```

## Linking Issues

### Automatic Linking

Use keywords in PR body:

```markdown
Closes #123        # Closes issue when PR merges
Fixes #123         # Same as closes
Resolves #123      # Same as closes
Relates to #456    # Links but doesn't close
Depends on #789    # Links to dependency
```

### Multiple Issues

```markdown
## Related Issues

Closes #123, closes #124
Relates to #200

<!-- Or one per line -->
Closes #123
Closes #124
Relates to #200
```

## Verification Summary

Include verification results from `acceptance-criteria-verification`:

```markdown
## Verification

### Test Results

| Suite | Status | Coverage |
|-------|--------|----------|
| Unit | 47/47 passing | 98% |
| Integration | 12/12 passing | N/A |
| E2E | 5/5 passing | N/A |

### Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | User can log in | PASS |
| 2 | Invalid credentials show error | PASS |
| 3 | Session persists | PASS |
| 4 | Logout clears session | PASS |

Full verification report: [Link to issue comment]
```

## Special Cases

### Draft PRs

For work-in-progress or early feedback:

```bash
gh pr create --draft \
  --title "WIP: Add user authentication (#123)" \
  --body "..."
```

Convert to ready when complete:

```bash
gh pr ready [PR_NUMBER]
```

### Breaking Changes

Highlight breaking changes prominently:

```markdown
## Breaking Changes

:warning: **This PR contains breaking changes:**

- `AuthService.login()` now returns `Promise<Session>` instead of `Promise<User>`
- The `session` cookie name changed from `sid` to `session_id`
- Removed deprecated `authenticate()` function

### Migration Guide

1. Update all calls to `login()` to handle new return type
2. Update cookie configuration if hardcoded
3. Replace `authenticate()` with `validateSession()`
```

### Large PRs

If PR is large, help reviewers:

```markdown
## Review Guide

This PR is large. Suggested review order:

1. Start with `src/services/auth.ts` (core logic)
2. Then `src/middleware/authenticate.ts` (integration)
3. Then `src/routes/auth.ts` (API surface)
4. Finally tests in `tests/auth/`

### Files by Category

**Core Changes:**
- src/services/auth.ts
- src/models/session.ts

**Integration:**
- src/middleware/authenticate.ts

**API:**
- src/routes/auth.ts

**Tests:**
- tests/auth/*.test.ts
```

## After Creation

### Monitor Status

```bash
# Check PR status
gh pr view [PR_NUMBER]

# Check CI status
gh pr checks [PR_NUMBER]
```

### Respond to Feedback

When reviewers comment:
1. Address all feedback
2. Push fixes
3. Re-request review if significant changes
4. Mark conversations as resolved

## Checklist

Before creating PR:

- [ ] All tests pass locally
- [ ] Build succeeds
- [ ] Branch is current with target
- [ ] Commits are clean

PR content:

- [ ] Clear, descriptive title
- [ ] Summary explains what and why
- [ ] Changes listed
- [ ] Issue linked (Closes #X)
- [ ] Verification results included
- [ ] Checklist completed
- [ ] Labels applied
- [ ] Reviewers assigned (if required)

## Integration

This skill is called by:
- `issue-driven-development` - Step 12

This skill follows:
- `comprehensive-review` - Review complete
- `apply-all-findings` - Findings addressed
- `clean-commits` - Commits ready

This skill precedes:
- `ci-monitoring` - Monitor CI results
