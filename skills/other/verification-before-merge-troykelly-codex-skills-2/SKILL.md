---
name: verification-before-merge
description: Use before merging PR - final gate ensuring all tests pass, review complete, CI green, and acceptance criteria verified
---

# Verification Before Merge

## Overview

Final verification before merging. All gates must pass.

**Core principle:** Never merge without complete verification.

**This is a HARD GATE.** Do not merge with any failure.

## The Gates

All must be GREEN to merge:

```
┌──────────────────────────────────────────────────────┐
│                  MERGE GATES                         │
├──────────────────────────────────────────────────────┤
│  [ ] CI Pipeline Green                               │
│  [ ] Local Integration Tests Pass (if services)     │
│  [ ] All Tests Pass                                  │
│  [ ] Code Review Approved                            │
│  [ ] Acceptance Criteria Verified                    │
│  [ ] No Unresolved Conversations                     │
│  [ ] Branch Up to Date                               │
│  [ ] No Merge Conflicts                              │
├──────────────────────────────────────────────────────┤
│  ALL GREEN → MERGE ALLOWED                           │
│  ANY RED → MERGE BLOCKED                             │
└──────────────────────────────────────────────────────┘
```

## Gate Details

### 1. CI Pipeline Green

```bash
# Check all CI checks
gh pr checks [PR_NUMBER]

# Expected: All passing
✓  build          passed
✓  lint           passed
✓  test           passed
✓  typecheck      passed
✓  security       passed
```

**If not green:** Use `ci-monitoring` to resolve.

### 1.5. Local Integration Tests Pass

**CRITICAL:** CI should validate, not discover. If CI found bugs, local testing was insufficient.

```bash
# Verify services are running (if project has docker-compose)
docker-compose ps

# Run integration tests against real services
pnpm test:integration

# Verify migrations work
pnpm migrate
```

**If project has docker-compose services:**
- Services MUST be running locally
- Integration tests MUST pass against real services
- Migrations MUST apply successfully
- NOT acceptable: "unit tests with mocks pass, I'll let CI verify the real services"

**Local testing evidence must be posted to issue before PR creation.**

**Skill:** `local-service-testing`

### 2. All Tests Pass

```bash
# Verify locally (CI should have done this, but verify)
pnpm test

# Check coverage
pnpm test --coverage
```

**If failing:** Fix tests before merge.

### 3. Code Review Approved

```bash
# Check review status
gh pr view [PR_NUMBER] --json reviews

# Expected: At least one approval, no changes requested
```

**If not approved:**
- Address feedback
- Re-request review
- Wait for approval

### 4. Acceptance Criteria Verified

Check the issue:

```bash
gh issue view [ISSUE_NUMBER] --json body
```

All acceptance criteria should be checked:

```markdown
## Acceptance Criteria
- [x] User can log in
- [x] Invalid credentials show error
- [x] Session persists
- [x] Logout clears session
```

**If not verified:** Complete verification before merge.

### 5. No Unresolved Conversations

```bash
# Check for unresolved threads
gh pr view [PR_NUMBER] --json reviewThreads
```

All review comments should be:
- Resolved
- Or responded to with explanation

**If unresolved:** Address the feedback.

### 6. Branch Up to Date

```bash
# Check if branch is behind target
gh pr view [PR_NUMBER] --json mergeable,mergeStateStatus

# If behind, update
git fetch origin
git rebase origin/main
git push --force-with-lease
```

**If not up to date:** Rebase or merge target branch.

### 7. No Merge Conflicts

```bash
# Check for conflicts
gh pr view [PR_NUMBER] --json mergeable
```

**If conflicts exist:** Resolve before merge.

```bash
git fetch origin
git rebase origin/main
# Resolve conflicts
git add .
git rebase --continue
git push --force-with-lease
```

## Pre-Merge Checklist

Run through this checklist before every merge:

```markdown
## Pre-Merge Verification

### CI/Tests
- [ ] All CI checks passing
- [ ] Tests pass locally
- [ ] Coverage acceptable

### Review
- [ ] PR approved
- [ ] All conversations resolved
- [ ] Feedback addressed

### Verification
- [ ] All acceptance criteria verified
- [ ] Verification report posted to issue
- [ ] Issue ready to close

### Branch
- [ ] Up to date with target
- [ ] No merge conflicts
- [ ] Commits clean

### Documentation
- [ ] PR description complete
- [ ] Issue updated
- [ ] Relevant docs updated
```

## Performing the Merge

Once all gates are green:

### Using GitHub CLI

```bash
# Merge with squash (recommended for clean history)
gh pr merge [PR_NUMBER] --squash --delete-branch

# Or merge commit
gh pr merge [PR_NUMBER] --merge --delete-branch

# Or rebase
gh pr merge [PR_NUMBER] --rebase --delete-branch
```

### Merge Strategy

| Strategy | When to Use |
|----------|-------------|
| Squash | Most PRs - creates single clean commit |
| Merge | When commit history is important |
| Rebase | When you want linear history without merge commit |

Follow project conventions for merge strategy.

## Post-Merge

After successful merge:

### 1. Verify Issue Closed

```bash
# Check issue status
gh issue view [ISSUE_NUMBER] --json state
# Should be: "CLOSED"

# If not closed automatically, close it
gh issue close [ISSUE_NUMBER] --comment "Closed by #[PR_NUMBER]"
```

### 2. Update Project Status

```bash
# Update GitHub Project fields
# Status → Done
# (Using project-status-sync)
```

### 3. Clean Up Local

```bash
# Switch to main
git checkout main

# Pull merged changes
git pull origin main

# Delete local branch
git branch -d feature/issue-123-description

# Prune remote tracking branches
git remote prune origin
```

### 4. Verify Deployment (if applicable)

If auto-deploy is configured:

- Check deployment status
- Verify feature works in deployed environment
- Monitor for errors

## Merge Blocked Scenarios

### Review Not Approved

```
Cannot merge: Review required

→ Request review
→ Address feedback
→ Get approval
```

### Failing CI

```
Cannot merge: CI checks failing

→ Use ci-monitoring skill
→ Fix failures
→ Wait for green
```

### Branch Behind

```
Cannot merge: Branch out of date

→ git fetch origin
→ git rebase origin/main
→ Resolve conflicts
→ git push --force-with-lease
```

### Unresolved Conversations

```
Cannot merge: Unresolved review threads

→ Address each comment
→ Mark as resolved
→ Re-request review if needed
```

## Never Merge When

| Situation | Action |
|-----------|--------|
| Tests failing | Fix tests first |
| CI red | Fix CI first |
| Review pending | Wait for review |
| Conflicts exist | Resolve conflicts |
| Acceptance criteria not met | Complete verification |
| Critical feedback unaddressed | Address feedback |

## Checklist

Final verification before clicking merge:

- [ ] All CI checks green
- [ ] Local integration tests pass (if services available)
- [ ] Local testing artifact posted to issue (if services used)
- [ ] All tests passing
- [ ] PR approved
- [ ] All conversations resolved
- [ ] Acceptance criteria verified
- [ ] Branch up to date
- [ ] No conflicts
- [ ] PR documentation complete
- [ ] Ready to close issue

## Integration

This skill is called by:
- `issue-driven-development` - Step 13

This skill follows:
- `ci-monitoring` - CI is green
- `pr-creation` - PR exists

This skill completes:
- The development cycle for an issue
