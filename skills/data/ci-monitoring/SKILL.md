---
name: ci-monitoring
description: Use after creating PR - monitor CI pipeline, resolve failures cyclically until green or issue is identified as unresolvable
---

# CI Monitoring

## Overview

Monitor CI pipeline and resolve failures until green.

**CRITICAL: CI is validation, not discovery.**

> **If CI finds a bug you didn't find locally, your local testing was insufficient.**
>
> Before blaming CI, ask yourself:
> 1. Did you run all tests locally?
> 2. Did you test against local services (postgres, redis)?
> 3. Did you run the same checks CI runs?
> 4. Did you run integration tests, not just unit tests with mocks?
>
> CI should only fail for: environment differences, flaky tests, or infrastructure issues—never for bugs you could have caught locally.

**Core principle:** CI failures are blockers. But they should never be surprises.

**Announce at start:** "I'm monitoring CI and will resolve any failures."

## The CI Loop

```
PR Created
     │
     ▼
┌─────────────┐
│ Wait for CI │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ CI Status?  │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
 Green   Red/Failed
   │       │
   ▼       ▼
┌─────────┐  ┌─────────────┐
│ MERGE   │  │ Diagnose    │
│ THE PR  │  │ failure     │
└────┬────┘  └──────┬──────┘
     │              │
     ▼              ▼
┌─────────┐  ┌─────────────┐
│ Continue│  │ Fixable?    │
│ to next │  └──────┬──────┘
│ issue   │         │
└─────────┘    ┌────┴────┐
               │         │
              Yes        No
               │         │
               ▼         ▼
          ┌─────────┐  ┌─────────────┐
          │ Fix and │  │ Document as │
          │ push    │  │ unresolvable│
          └────┬────┘  └─────────────┘
               │
               └────► Back to "Wait for CI"
```

## CRITICAL: Green CI = Merge Immediately

**When CI passes, you MUST merge the PR and continue working.**

Do NOT:
- Stop and report "CI is green, ready for review"
- Wait for user confirmation
- Summarize and ask what to do next

DO:
- Merge the PR immediately: `gh pr merge [PR_NUMBER] --squash --delete-branch`
- Mark the linked issue as Done
- Continue to the next issue in scope

```bash
# When CI passes
gh pr merge [PR_NUMBER] --squash --delete-branch

# Update linked issue status
gh issue edit [ISSUE_NUMBER] --remove-label "status:in-review" --add-label "status:done"

# Continue to next issue (do not stop)
```

**The only exception:** PRs with `do-not-merge` label require explicit user action.

## Checking CI Status

### Using GitHub CLI

```bash
# Check all CI checks
gh pr checks [PR_NUMBER]

# Watch CI in real-time
gh pr checks [PR_NUMBER] --watch

# Get detailed status
gh pr view [PR_NUMBER] --json statusCheckRollup
```

### Expected Output

```
All checks were successful
0 failing, 0 pending, 5 passing

CHECKS
✓  build          1m23s
✓  lint           45s
✓  test           3m12s
✓  typecheck      1m05s
✓  security-scan  2m30s
```

## Handling Failures

### Step 1: Identify the Failure

```bash
# Get failed check details
gh pr checks [PR_NUMBER]

# View workflow run logs
gh run view [RUN_ID] --log-failed
```

### Step 2: Diagnose the Cause

Common failure types:

| Type | Symptoms | Cause |
|------|----------|-------|
| Test failure | `FAIL` in test output | Code bug or test bug |
| Build failure | Compilation errors | Type errors, syntax errors |
| Lint failure | Style violations | Formatting, conventions |
| Typecheck failure | Type errors | Missing types, wrong types |
| Timeout | Job exceeded time limit | Performance issue or stuck test |
| Flaky test | Passes locally, fails CI | Race condition, environment difference |

### Step 3: Fix the Issue

#### Test Failures

```bash
# Reproduce locally
pnpm test

# Run specific failing test
pnpm test --grep "test name"

# Fix the code or test
# Commit and push
```

#### Build Failures

```bash
# Reproduce locally
pnpm build

# Fix compilation errors
# Commit and push
```

#### Lint Failures

```bash
# Check lint errors
pnpm lint

# Auto-fix what's possible
pnpm lint:fix

# Manually fix remaining
# Commit and push
```

#### Type Failures

```bash
# Check type errors
pnpm typecheck

# Fix type issues
# Commit and push
```

### Step 4: Push Fix and Wait

```bash
# Commit fix
git add .
git commit -m "fix(ci): Resolve test failure in user validation"

# Push
git push

# Wait for CI again
gh pr checks [PR_NUMBER] --watch
```

### Step 5: Repeat Until Green

Loop through diagnose → fix → push → wait until all checks pass.

## Flaky Tests

### Identifying Flakiness

```
Test passes locally
Test fails in CI
Test passes on retry in CI
```

### Handling Flakiness

1. **Don't just retry** - Find the root cause
2. **Check for race conditions** - Timing-dependent code
3. **Check for environment differences** - Paths, env vars, services
4. **Check for state pollution** - Tests affecting each other

```typescript
// Common flaky pattern: timing dependency
// BAD
await saveData();
await delay(100);  // Hoping 100ms is enough
const result = await loadData();

// GOOD: Wait for condition
await saveData();
await waitFor(() => dataExists());
const result = await loadData();
```

## Unresolvable Failures

Sometimes failures can't be fixed in the current PR:

### Legitimate Unresolvable Cases

| Case | Example |
|------|---------|
| CI infrastructure issue | Service down, rate limited |
| Pre-existing flaky test | Not introduced by this PR |
| Upstream dependency issue | External API changed |
| Requires manual intervention | Needs secrets, permissions |

### Process for Unresolvable

1. **Document the issue**

```bash
gh pr comment [PR_NUMBER] --body "## CI Issue

The \`security-scan\` check is failing due to a known issue with the scanner service (see #999).

This is not related to changes in this PR. The scan passes when run locally.

Requesting bypass approval from @maintainer."
```

2. **Create issue if new**

```bash
gh issue create \
  --title "CI: Security scanner service timeout" \
  --body "The security scanner is timing out in CI..."
```

3. **Request bypass if appropriate**

Some teams allow merging with known infrastructure failures.

4. **Do NOT merge with real failures**

If the failure is from your code, it must be fixed.

## CI Best Practices

### Run Locally First (MANDATORY)

**CI is the last resort, not the first check.**

Before pushing, run EVERYTHING CI will run:

```bash
# Run the same checks CI will run
pnpm lint
pnpm typecheck
pnpm test              # Unit tests
pnpm test:integration  # Integration tests against real services
pnpm build

# If you have database changes
docker-compose up -d postgres
pnpm migrate
```

**If your project has docker-compose services:**
- Start them before testing: `docker-compose up -d`
- Run integration tests against real services
- Verify migrations apply to real database
- Don't rely on mocks alone

**Skill:** `local-service-testing`

### Commit Incrementally

Don't push 10 commits at once. Push smaller changes:

```bash
# Small fix, push, verify
git push

# Wait for CI
gh pr checks --watch

# Then next change
```

### Monitor Actively

Don't "push and forget":

```bash
# Watch CI after each push
gh pr checks [PR_NUMBER] --watch
```

## Checklist

For each CI run:

- [ ] Waited for CI to complete
- [ ] All checks examined
- [ ] Failures diagnosed (if any)
- [ ] Fixes implemented (if needed)
- [ ] Re-pushed and re-checked (if fixed)
- [ ] All green

When CI is green:

- [ ] **PR merged immediately** (`gh pr merge --squash --delete-branch`)
- [ ] Linked issue marked Done
- [ ] **Continued to next issue** (do NOT stop and report)

For unresolvable issues:

- [ ] Root cause identified
- [ ] Not caused by PR changes
- [ ] Documented in PR comment
- [ ] Issue created if new problem
- [ ] Bypass approval requested if appropriate

## Integration

This skill is called by:
- `issue-driven-development` - Step 13
- `autonomous-orchestration` - Main loop and bootstrap

This skill follows:
- `pr-creation` - PR exists

This skill completes:
- The PR lifecycle - merge is the final step, not "verification-before-merge"

This skill may trigger:
- `error-recovery` - If CI reveals deeper issues
