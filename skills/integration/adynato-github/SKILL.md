---
name: adynato-github
description: GitHub workflow conventions for Adynato projects. Covers creating PRs with gh CLI, writing thorough descriptions, and using stacked PRs for large deliverables. Use when creating pull requests, managing branches, or breaking down large features.
---

# GitHub Skill

Use this skill when working with GitHub on Adynato projects.

## Always Use gh CLI

Use the `gh` CLI for all GitHub operations instead of the web interface:

```bash
# Create PR
gh pr create --title "Title" --body "Description"

# View PR
gh pr view 123

# Check PR status
gh pr checks 123

# Merge PR
gh pr merge 123 --squash
```

## PR Descriptions

Every PR must have a thorough description. Use this template:

```bash
gh pr create --title "feat: add user authentication" --body "$(cat <<'EOF'
## Summary

Brief description of what this PR does and why.

- Added JWT-based authentication flow
- Implemented login/logout endpoints
- Added auth middleware for protected routes

## Changes

- `lib/auth.ts` - Auth utilities and token management
- `app/api/auth/login/route.ts` - Login endpoint
- `app/api/auth/logout/route.ts` - Logout endpoint
- `middleware.ts` - Route protection

## Testing

- [ ] Login with valid credentials returns token
- [ ] Login with invalid credentials returns 401
- [ ] Protected routes reject unauthenticated requests
- [ ] Logout invalidates token

## Screenshots

(if UI changes)

## Related

- Closes #123
- Part of #456
EOF
)"
```

### Required Sections

| Section | When Required | Purpose |
|---------|---------------|---------|
| **Summary** | Always | What and why in 2-3 sentences |
| **Changes** | Always | List of files/areas modified |
| **Testing** | Always | How to verify it works |
| **Screenshots** | UI changes | Visual proof of changes |
| **Related** | If applicable | Linked issues/PRs |

## Stacked PRs

For large deliverables, break work into small, stacked PRs that build on each other.

### Why Stack PRs

- **Easier review** - Reviewers can focus on one concern at a time
- **Faster merges** - Small PRs get approved faster
- **Lower risk** - Each PR is independently deployable
- **Better history** - Clear progression of changes

### Stacking Strategy

For a feature like "Add user dashboard":

```
PR 1: Add user API endpoints (base)
  ↓
PR 2: Add dashboard data fetching (stacked on PR 1)
  ↓
PR 3: Add dashboard UI components (stacked on PR 2)
  ↓
PR 4: Add dashboard tests (stacked on PR 3)
```

### Creating Stacked PRs

```bash
# PR 1: Base branch
git checkout -b feat/user-api
# ... make changes ...
git push -u origin feat/user-api
gh pr create --base main --title "feat: add user API endpoints"

# PR 2: Stack on PR 1
git checkout -b feat/dashboard-data feat/user-api
# ... make changes ...
git push -u origin feat/dashboard-data
gh pr create --base feat/user-api --title "feat: add dashboard data fetching"

# PR 3: Stack on PR 2
git checkout -b feat/dashboard-ui feat/dashboard-data
# ... make changes ...
git push -u origin feat/dashboard-ui
gh pr create --base feat/dashboard-data --title "feat: add dashboard UI"
```

### Stack Description

In stacked PRs, note the relationship:

```markdown
## Summary

Adds dashboard UI components.

## Stack

This PR is part of a stack:
1. #101 - Add user API endpoints ← **merged**
2. #102 - Add dashboard data fetching ← **base**
3. **#103 - Add dashboard UI** ← you are here
4. #104 - Add dashboard tests

Please review and merge in order.
```

### Updating Stacked PRs

When the base PR changes:

```bash
# Update your branch with changes from base
git checkout feat/dashboard-ui
git rebase feat/dashboard-data
git push --force-with-lease
```

When base PR merges:

```bash
# Rebase onto new base
git checkout feat/dashboard-data
git rebase main
git push --force-with-lease

# Update PR base branch
gh pr edit 102 --base main
```

## PR Size Guidelines

| Size | Lines Changed | Review Time | Recommendation |
|------|---------------|-------------|----------------|
| XS | < 50 | Minutes | Ideal |
| S | 50-200 | < 1 hour | Good |
| M | 200-500 | 1-2 hours | Acceptable |
| L | 500-1000 | 2-4 hours | Split if possible |
| XL | > 1000 | Days | Must split |

**Target: Keep PRs under 300 lines changed.**

## Commit Messages

Use conventional commits:

```bash
feat: add user authentication
fix: resolve login redirect loop
docs: update API documentation
refactor: extract auth utilities
test: add auth endpoint tests
chore: update dependencies
```

Format:
```
<type>: <short description>

<optional body explaining why>

<optional footer with references>
```

## Branch Naming

```
feat/short-description    # New features
fix/issue-description     # Bug fixes
refactor/what-changed     # Code refactoring
docs/what-documented      # Documentation
test/what-tested          # Test additions
```

## Common gh Commands

```bash
# Create PR with labels
gh pr create --title "feat: thing" --label "enhancement" --label "needs-review"

# Create draft PR
gh pr create --title "wip: thing" --draft

# Request reviewers
gh pr edit 123 --add-reviewer @username

# Check CI status
gh pr checks 123 --watch

# View PR diff
gh pr diff 123

# Checkout PR locally
gh pr checkout 123

# Close PR
gh pr close 123

# Reopen PR
gh pr reopen 123

# List open PRs
gh pr list

# View PR comments
gh pr view 123 --comments
```

## Review Process

1. **Self-review first** - Read your own diff before requesting review
2. **CI must pass** - Don't request review until checks are green
3. **Respond to feedback** - Address or discuss all comments
4. **Squash on merge** - Keep main history clean

```bash
# Merge with squash (preferred)
gh pr merge 123 --squash --delete-branch

# Merge with rebase (for stacks)
gh pr merge 123 --rebase --delete-branch
```

## Addressing PR Comments

When fixing review comments, follow this workflow for **each comment**:

### 1. Make Individual Commits

Create a separate conventional commit for each review comment fix:

```bash
# Fix first comment
git add src/auth.ts
git commit -m "fix: add null check for user token

Addresses review comment about potential null reference"

# Fix second comment
git add src/api/users.ts
git commit -m "refactor: extract validation logic to separate function

Addresses review comment about function complexity"

# Fix third comment
git add src/utils.ts
git commit -m "fix: handle edge case for empty array

Addresses review comment about missing edge case handling"
```

**Do NOT batch multiple comment fixes into one commit.** Each fix should be atomic and traceable.

### 2. Reply to the Comment

After committing the fix, reply to the review comment:

**If fixed:**
```
Fixed in <commit-sha>
```

Or with more context:
```
Fixed in abc1234 - added null check before accessing token property.
```

**If not valid or won't fix:**
```
I don't think this change is necessary because [reason].

[Explanation of why current implementation is correct/preferred]
```

Or:
```
This is intentional - [explanation]. Happy to discuss further if you disagree.
```

### 3. Resolve the Comment

After replying, resolve the conversation:

```bash
# View comments to get comment IDs
gh api repos/{owner}/{repo}/pulls/{pr}/comments

# Or use the web UI to resolve after replying
```

In the GitHub web UI: Click "Resolve conversation" after your reply.

### Complete Workflow Example

```bash
# 1. Read all comments
gh pr view 123 --comments

# 2. For each valid comment, fix and commit individually
git add src/auth.ts
git commit -m "fix: validate token expiry before use

Addresses review feedback on auth token handling"

# 3. Push all fixes
git push

# 4. Reply to each comment in GitHub UI or via API
gh api repos/adynato/myrepo/pulls/123/comments/456789/replies \
  -f body="Fixed in $(git rev-parse --short HEAD)"

# 5. Resolve each conversation in GitHub UI
```

### Comment Response Templates

| Scenario | Response |
|----------|----------|
| Fixed | "Fixed in `abc1234`" |
| Fixed with explanation | "Fixed in `abc1234` - moved validation to middleware as suggested" |
| Needs discussion | "I see your point, but [reasoning]. What do you think about [alternative]?" |
| Won't fix (valid reason) | "Intentionally kept as-is because [reason]. The tradeoff is [explanation]." |
| Won't fix (out of scope) | "Good catch, but out of scope for this PR. Created #456 to track." |
| Question/clarification | "Good question - [explanation of why code works this way]" |

### Rules

1. **One commit per comment** - Makes it easy to trace what fixed what
2. **Always reply** - Never leave comments unaddressed
3. **Always resolve** - Clean up the conversation thread
4. **Reference commits** - Include SHA so reviewer can verify the fix
5. **Be respectful** - Even when disagreeing, explain your reasoning
6. **Create issues for scope creep** - If a comment suggests something bigger, create an issue instead
