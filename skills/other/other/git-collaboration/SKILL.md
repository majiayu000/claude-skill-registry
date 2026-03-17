---
name: git-collaboration
description: Collaboration workflows for team-based Git development. Covers pull request workflows, merge vs rebase strategies, conflict resolution, code review practices, and branch protection. Helps AI agents follow team conventions and collaborate effectively.
---

# Git Collaboration Workflows

**Purpose:** This skill teaches AI agents to collaborate effectively in team environments using Git, including PR workflows, merge strategies, and conflict resolution.

## Core Principles

1. **Sync Early, Sync Often** - Stay up to date with main branch
2. **Small, Focused PRs** - Easier to review and merge
3. **Clean History** - Use rebase for clean, linear history
4. **Review-Friendly** - Structure changes for easy review

## Branch Workflow Strategies

### Strategy 1: Feature Branch Workflow (Recommended)

```bash
# ✓ RECOMMENDED: Standard feature branch workflow

# 1. Start from updated main
git switch main
git pull

# 2. Create feature branch
git switch -c feature/add-user-authentication

# 3. Work and commit
git add src/auth.js
git commit -m "feat(auth): add login endpoint"

# 4. Keep branch updated (daily or before PR)
git fetch origin
git rebase origin/main

# 5. Push and create PR
git push -u origin feature/add-user-authentication
gh pr create --title "Add user authentication" --body "..."

# 6. After PR merged, clean up
git switch main
git pull
git branch -d feature/add-user-authentication
```

**When to use:**
- Standard for most teams
- Clear separation of features
- Easy to review individual features

### Strategy 2: Trunk-Based Development

```bash
# ✓ ALTERNATIVE: Very short-lived branches

# 1. Start from main
git switch main
git pull

# 2. Create short-lived branch (< 1 day)
git switch -c fix/cart-validation

# 3. Make small change
git add src/cart.js
git commit -m "fix(cart): validate quantity range"

# 4. Push and merge quickly (same day)
git push -u origin fix/cart-validation
gh pr create --title "Fix cart validation"
# Get review and merge within hours

# 5. Immediate cleanup
git switch main
git pull
git branch -d fix/cart-validation
```

**When to use:**
- Fast-moving teams
- Continuous integration culture
- Small, incremental changes

### Strategy 3: Release Branch Workflow

```bash
# ✓ FOR RELEASES: Maintain release branches

# Main branch is development
git switch main

# Create release branch
git switch -c release/v2.0

# Only bug fixes go to release branch
git switch -c hotfix/fix-critical-bug
git add src/payment.js
git commit -m "fix(payment): prevent double charging"

# Merge to release
git switch release/v2.0
git merge hotfix/fix-critical-bug

# Also merge back to main
git switch main
git merge hotfix/fix-critical-bug

# Tag release
git switch release/v2.0
git tag -a v2.0.1 -m "Release v2.0.1"
git push origin v2.0.1
```

**When to use:**
- Supporting multiple versions
- Long release cycles
- Need stable release branches

## Pull Request Workflow

### Creating a Pull Request

```bash
# ✓ COMPLETE PR WORKFLOW

# 1. Ensure branch is up to date
git switch feature/new-feature
git fetch origin
git rebase origin/main

# 2. Review your changes
git log origin/main..HEAD  # Commits you're adding
git diff origin/main...HEAD  # All changes

# 3. Push to remote
git push -u origin feature/new-feature

# 4. Create PR with good description
gh pr create \
  --title "feat(auth): add OAuth2 authentication" \
  --body "$(cat <<'EOF'
## Summary
Adds OAuth2 authentication support for Google and GitHub providers.

## Changes
- Add OAuth2 client configuration
- Implement callback handler
- Add user profile mapping
- Update login UI with OAuth buttons

## Testing
- ✅ Manual testing with Google OAuth
- ✅ Manual testing with GitHub OAuth
- ✅ Added unit tests for profile mapping
- ✅ Verified error handling for invalid tokens

## Screenshots
[Attach screenshots of login page]

## Checklist
- [x] Tests added/updated
- [x] Documentation updated
- [x] No breaking changes
- [ ] Security review needed (OAuth credentials handling)

Closes #234
EOF
)"
```

### PR Description Template

```markdown
## Summary
Brief description of what this PR does and why.

## Changes
- Bullet point list of main changes
- Keep it high-level (detailed changes visible in commits)

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] Edge cases verified

## Deployment Notes
Any special deployment steps, migrations, or config changes needed.

## Checklist
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Reviewed own code
- [ ] Ready for review

Closes #<issue-number>
```

### Responding to Review Feedback

```bash
# ✓ CORRECT: Address feedback in new commits

# Reviewer requested changes
# Make the changes
git add src/auth.js
git commit -m "refactor(auth): extract validation to separate function"

git add tests/auth.test.js
git commit -m "test(auth): add edge cases for token validation"

# Push updates
git push

# ✗ WRONG: Amending or force-pushing during review
git commit --amend  # Don't do this during review!
git push --force    # Reviewers lose context
```

**Why new commits during review:**
- Reviewers can see what changed since last review
- Clear history of feedback iterations
- Can be squashed later before merge

### Squashing Before Merge

```bash
# AFTER review approval, before merge:

# Option 1: GitHub "Squash and merge" button (easiest)
# Just click in UI

# Option 2: Manual squash
git switch feature/new-feature
git rebase -i origin/main

# In editor, squash commits:
pick abc123 feat(auth): add OAuth2 support
squash def456 refactor(auth): extract validation
squash ghi789 test(auth): add edge cases
squash jkl012 fix(auth): address review comments

# Result: One clean commit
git push --force-with-lease origin feature/new-feature

# Then merge
gh pr merge --squash
```

## Merge vs Rebase vs Squash

### Decision Tree

```
Are you working on a feature branch?
├─ Ready to integrate to main?
│  ├─ Want to preserve all commit history?
│  │  └─> Merge commit (git merge --no-ff)
│  │
│  └─ Want clean, single commit?
│     └─> Squash merge (git merge --squash)
│
└─ Want to stay up to date with main?
   └─> Rebase (git rebase origin/main)
```

### Strategy Comparison

| Strategy | Command | Result | Use When |
|----------|---------|--------|----------|
| **Merge** | `git merge feature` | Creates merge commit, preserves all commits | Want to preserve feature branch history |
| **Rebase** | `git rebase main` | Replays commits on top of main | Updating feature branch, want linear history |
| **Squash** | `git merge --squash feature` | Combines all commits into one | Want clean history, PRs with many small commits |

### Merge Commit

```bash
# ✓ WHEN: You want to preserve branch history

git switch main
git merge --no-ff feature/new-feature

# Creates merge commit:
#   * Merge branch 'feature/new-feature'
#   |\
#   | * feat(auth): add OAuth2 support
#   | * test(auth): add OAuth tests
#   |/
#   * Previous main commit

# Pros: Full history, easy to revert entire feature
# Cons: Non-linear history, cluttered with merge commits
```

### Rebase

```bash
# ✓ WHEN: Updating feature branch with main changes

git switch feature/new-feature
git fetch origin
git rebase origin/main

# Result: Your commits replayed on top of latest main
#   * feat(auth): add OAuth2 support (your commit)
#   * test(auth): add OAuth tests (your commit)
#   * Latest main commit
#   * Previous main commit

# Pros: Clean, linear history
# Cons: Rewrites history (don't rebase shared branches)

# Then push with force-with-lease
git push --force-with-lease origin feature/new-feature
```

### Squash Merge

```bash
# ✓ WHEN: PR has many small commits, want clean main history

# Option 1: GitHub squash button (recommended)
gh pr merge --squash

# Option 2: Manual squash
git switch main
git merge --squash feature/new-feature
git commit -m "feat(auth): add OAuth2 authentication

Summary of all changes from feature branch.
Includes implementation, tests, and documentation.

Closes #234"

# Result: One commit on main with all changes
#   * feat(auth): add OAuth2 authentication
#   * Previous main commit

# Pros: Clean main history, easy to revert
# Cons: Loses individual commit history from PR
```

## Conflict Resolution

### Preventing Conflicts

```bash
# ✓ BEST PRACTICE: Stay up to date

# Daily or before creating PR
git switch feature/new-feature
git fetch origin
git rebase origin/main

# If conflicts occur during rebase, resolve them incrementally
```

### Resolving Merge Conflicts

```bash
# Conflict during rebase
git rebase origin/main

# Output:
# CONFLICT (content): Merge conflict in src/auth.js
# error: could not apply abc123... feat(auth): add OAuth

# 1. Check conflicted files
git status

# 2. Open file and look for conflict markers
# <<<<<<< HEAD (current main)
# code from main
# =======
# code from your branch
# >>>>>>> abc123 (your commit)

# 3. Resolve conflict by editing file
# Remove markers, keep correct code

# 4. Stage resolved file
git add src/auth.js

# 5. Continue rebase
git rebase --continue

# 6. Push updated branch
git push --force-with-lease origin feature/new-feature
```

### Conflict Resolution Strategies

```bash
# ✓ STRATEGY 1: Accept main version, reapply your changes
# In conflict:
git checkout --ours src/auth.js  # Keep your version
# OR
git checkout --theirs src/auth.js  # Keep main version (during rebase)

# Then manually reapply needed changes
git add src/auth.js
git rebase --continue

# ✓ STRATEGY 2: Use merge tool
git mergetool

# ✓ STRATEGY 3: Abort and restart
git rebase --abort  # Start over
git merge --abort   # If in merge
```

### Complex Conflict Example

```bash
# You: Modified function signature
# Main: Modified function body

# <<<<<<< HEAD (main)
function authenticate(username, password) {
  // New validation added in main
  if (!username || !password) {
    throw new Error('Missing credentials');
  }
  return validateCredentials(username, password);
}
# =======
function authenticate(credentials) {
  // Your change: accept object instead
  return validateCredentials(credentials.username, credentials.password);
}
# >>>>>>> your-commit

# ✓ RESOLVE: Combine both changes
function authenticate(credentials) {
  // Keep new validation from main
  if (!credentials.username || !credentials.password) {
    throw new Error('Missing credentials');
  }
  // Keep your signature change
  return validateCredentials(credentials.username, credentials.password);
}

git add src/auth.js
git rebase --continue
```

## Code Review Best Practices

### For PR Authors

```bash
# ✓ BEFORE creating PR:

# 1. Review your own changes first
git diff origin/main...HEAD

# 2. Ensure tests pass
npm test

# 3. Ensure linting passes
npm run lint

# 4. Check for debug code
git diff origin/main...HEAD | grep -i console.log
git diff origin/main...HEAD | grep -i debugger

# 5. Verify commit messages
git log origin/main..HEAD --oneline

# 6. Rebase if needed
git rebase -i origin/main  # Cleanup commits
```

### PR Size Guidelines

```bash
# ✓ GOOD: Small, focused PR
# Files changed: 5-10
# Lines changed: 100-300
# Easy to review in 15-30 minutes

# ✗ TOO LARGE: Difficult to review
# Files changed: 50+
# Lines changed: 1000+
# Takes hours to review properly

# If PR is too large, split it:
git switch -c feature/part-1
git cherry-pick <commits for part 1>
git push -u origin feature/part-1

git switch -c feature/part-2
git cherry-pick <commits for part 2>
git push -u origin feature/part-2
```

### For Reviewers

**Review checklist:**
- [ ] Does code solve the stated problem?
- [ ] Are edge cases handled?
- [ ] Are tests comprehensive?
- [ ] Is error handling appropriate?
- [ ] Are there security concerns?
- [ ] Is performance acceptable?
- [ ] Is code readable and maintainable?
- [ ] Does it follow team conventions?

## Branch Protection Rules

### Recommended Settings

```yaml
Protected Branch Rules for 'main':
  Require pull request reviews:
    ✓ Enabled
    Required approvals: 1-2
    Dismiss stale reviews: ✓
    Require review from code owners: ✓

  Require status checks:
    ✓ Enabled
    Required checks:
      - CI tests
      - Linting
      - Security scan

  Require branches to be up to date: ✓
  Require linear history: ✓ (no merge commits)

  Restrictions:
    ✓ Include administrators
    Allow force pushes: ✗
    Allow deletions: ✗
```

### Working with Protected Branches

```bash
# ✓ CORRECT: Cannot push directly to main
git switch main
git commit -m "feat: quick fix"
git push origin main
# Error: Protected branch

# ✓ CORRECT: Use feature branch + PR
git switch -c fix/quick-fix
git commit -m "feat: quick fix"
git push -u origin fix/quick-fix
gh pr create
```

## Common Workflows

### Workflow 1: Standard Feature Development

```bash
# Day 1: Start feature
git switch main
git pull
git switch -c feature/user-notifications

# Work
git add src/notifications.js
git commit -m "feat(notifications): add email notification service"

git add tests/notifications.test.js
git commit -m "test(notifications): add email service tests"

git push -u origin feature/user-notifications

# Day 2: Update with main changes
git fetch origin
git rebase origin/main
git push --force-with-lease origin feature/user-notifications

# Day 3: More work
git add src/notifications.js
git commit -m "feat(notifications): add SMS notification support"
git push

# Day 4: Create PR
gh pr create --title "Add user notification system"

# Day 5: Address review feedback
git add src/notifications.js
git commit -m "refactor(notifications): extract provider interface"
git push

# Day 6: PR approved and merged
gh pr merge --squash

# Cleanup
git switch main
git pull
git branch -d feature/user-notifications
```

### Workflow 2: Hotfix

```bash
# ✓ URGENT: Production bug fix

# 1. Create hotfix branch from main (or release branch)
git switch main
git pull
git switch -c hotfix/fix-payment-crash

# 2. Fix and test
git add src/payment.js
git commit -m "fix(payment): prevent crash on null amount"

# 3. Push immediately
git push -u origin hotfix/fix-payment-crash

# 4. Create PR with "HOTFIX" label
gh pr create \
  --title "HOTFIX: Fix payment crash on null amount" \
  --label "hotfix" \
  --body "Critical bug causing payment crashes in production"

# 5. Get expedited review and merge
gh pr merge --squash

# 6. Verify deployment
# 7. Cleanup
git switch main
git pull
git branch -d hotfix/fix-payment-crash
```

### Workflow 3: Collaborative Feature

```bash
# ✓ MULTIPLE DEVELOPERS: Working on same feature

# Developer A: Creates base feature branch
git switch -c feature/new-dashboard
git push -u origin feature/new-dashboard

# Developer B: Creates sub-branch from feature branch
git fetch origin
git switch -c feature/new-dashboard-widgets origin/feature/new-dashboard

# Work on widgets
git add src/widgets.js
git commit -m "feat(dashboard): add widget system"
git push -u origin feature/new-dashboard-widgets

# Create PR to merge into feature/new-dashboard
gh pr create --base feature/new-dashboard

# After widgets PR merged to feature/new-dashboard:
# Developer A: Update local feature branch
git switch feature/new-dashboard
git pull

# Continue working
# When feature complete, create PR to main
git switch feature/new-dashboard
gh pr create --base main
```

## Summary

**Key Principles:**
1. **Feature branch workflow** - Standard for most teams
2. **Small, focused PRs** - Easier to review and merge
3. **Rebase to stay current** - Linear history, cleaner log
4. **Squash before merge** - Clean main branch history
5. **Resolve conflicts early** - Rebase frequently

**Essential Commands:**
```bash
git switch -c feature/name        # Create feature branch
git rebase origin/main            # Update with main
git push --force-with-lease       # Safe force push after rebase
gh pr create                      # Create pull request
gh pr merge --squash              # Squash and merge PR
git branch -d feature/name        # Delete merged branch
```

**Remember:** Good collaboration is about clear communication, clean history, and making reviewers' lives easier.
