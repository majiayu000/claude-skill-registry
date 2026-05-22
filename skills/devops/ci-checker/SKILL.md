---
name: ci-checker
description: 'Checks GitHub CI status and guides fixing failures. Use when asked to check CI, verify PR checks, or diagnose CI failures after PR creation.'
---

# CI Checker

Checks GitHub CI status for PRs and guides fixing any failures.

## Prerequisites

- PR must exist
- Must be in a git repository with GitHub remote
- `gh` CLI authenticated

## Workflow

### 1. Get PR Info

Check for `status.json` in current directory:

```bash
cat status.json 2>/dev/null | jq -r '.prNumber // empty'
```

If not found, ask: "PR number? (or paste URL)"

### 2. Check CI Status

```bash
gh pr checks {pr-number}
```

Parse each check for status:

- ✅ pass
- ❌ fail
- 🔄 pending

### 3. Report Status

Present as table:

```markdown
# CI Status for PR #{number}

| Check     | Status     | Duration |
| --------- | ---------- | -------- |
| lint      | ✅ pass    | 2m       |
| typecheck | ✅ pass    | 3m       |
| test-unit | ❌ fail    | 5m       |
| test-e2e  | 🔄 pending | -        |
| build     | ✅ pass    | 4m       |

## Overall: {Passing / Failing / Pending}
```

### 4. Handle Pending

If checks still running:

```
CI checks still running. Estimated time: {X} minutes.

Options:
A) Wait and check again in 5 minutes
B) Check specific workflow status
C) Continue anyway (not recommended)
```

### 5. Handle Failures

For each failing check, get details:

```bash
# Get JSON with run IDs
gh pr checks {pr-number} --json name,status,conclusion,detailsUrl

# Get logs for failing run
gh run view {run-id} --log-failed
```

Present failure summary:

```markdown
## Failed: {check-name}

### Error Summary

{extracted error message}

### Failed Tests

- `src/components/Foo.test.ts` - "expected true, got false"

### Suggested Fix

{analysis based on error type}
```

### 6. Guide Fixes

```
Found {X} failing checks.

Options:
A) Investigate and fix locally
B) Re-run failed checks (if flaky)
C) View full logs for {check}
D) Ignore and proceed (not recommended)

Choice:
```

**Option A - Fix locally:**

- Provide commands to reproduce locally
- Dispatch subagent to investigate
- After fix, commit and push
- Re-check CI

**Option B - Re-run:**

```bash
gh run rerun {run-id} --failed
```

Wait and check again.

**Option C - View logs:**

```bash
gh run view {run-id} --log
```

Present relevant sections.

### 7. Handle All Passing

```
✅ All CI checks passing!

PR is ready for review.

Options:
A) Update Notion status to "Done"
B) Request specific reviewers
C) Done for now
```

**If updating Notion (Option A):**

⚠️ Follow [Notion Write Safety](docs/notion-write-safety.md) rules.

- Validate transition In Review → Done is valid
- Log to `status.json`:

```json
{
  "field": "Status",
  "value": "Done",
  "previousValue": "In Review",
  "at": "...",
  "skill": "ci-checker",
  "success": true
}
```

### 8. Update State

Update `status.json` if it exists:

```bash
jq '.ciStatus = "passing"' status.json > tmp.json && mv tmp.json status.json
```

## Common Issues & Solutions

### E2E Test Flakes

- **Cause:** Timing issues, async operations
- **Solution:** Re-run with `gh run rerun --failed`
- **If persists:** Fix the flaky test

### Lint Differences

- **Cause:** Different eslint/prettier versions
- **Solution:** Run `pnpm install` and `pnpm lint:fix` locally

### Type Errors in CI Only

- **Cause:** Stricter tsconfig or different TS version
- **Solution:** Run exact same typecheck command as CI

### Build Failures

- **Cause:** Missing files, import errors
- **Solution:** Run `pnpm build` locally to reproduce

## Key Commands

```bash
# List all checks
gh pr checks {pr-number}

# Get check details as JSON
gh pr checks {pr-number} --json name,status,conclusion,detailsUrl

# View run details
gh run view {run-id}

# View failed logs only
gh run view {run-id} --log-failed

# View full logs
gh run view {run-id} --log

# Re-run failed jobs
gh run rerun {run-id} --failed

# Re-run entire workflow
gh run rerun {run-id}
```

## Notes

- E2E tests can take 10-20 minutes - don't poll too frequently
- One re-run for flaky tests is acceptable
- If same test fails twice, it's a real issue
- Some checks are required for merge, some optional
- Never force merge with failing required checks
