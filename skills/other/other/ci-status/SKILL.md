---
name: ci:status
description: Check PR CI status - all checks, failures, test results, and artifacts
---

# CI Status

Check the current CI status for a PR and create task items for any failures.

## When to Use

- After pushing changes to a PR
- When asked "what's the CI status?"
- Before deciding whether to push more changes
- After CI completes to summarize results

## Workflow

### 1. Get PR Status

```bash
gh pr checks <PR-number>
```

### 2. Summarize Results

Present as a table:

| Check | Status | Details |
|-------|--------|---------|
| CodeQL | pass/fail | N alerts |
| Deploy & Test (Kind) | pass/fail | N passed, N failed |
| E2E HyperShift | pass/fail/pending | N passed, N failed |
| Build | pass | - |
| Linting | pass | - |

### 3. For Failures - Get Details

```bash
# Kind CI test results
gh run download <run-id> -n e2e-test-results -D /tmp/ci-results
grep -oE 'errors="[0-9]+" failures="[0-9]+" skipped="[0-9]+" tests="[0-9]+"' /tmp/ci-results/e2e-results.xml

# Failed test names
grep '<failure' /tmp/ci-results/e2e-results.xml

# HyperShift logs
gh run view <run-id> --log-failed | tail -30

# CodeQL alerts
gh api repos/<owner>/<repo>/check-runs/<check-id>/annotations --jq '.[] | {path, line: .start_line, message: .message[:100]}'
```

### 4. Create Tasks for Failures

For each distinct failure, create a task:

```
TaskCreate: "<worktree> | <PR> | <topic> | RCA | <failure description>"
```

## Task Tracking

On invocation:
1. TaskList - check for existing CI-related tasks
2. TaskCreate for each new failure found
3. Link to plan doc if failures relate to planned work
4. Metadata: `plan: "ad-hoc"`, `runner: "main-session"`

## Troubleshooting

### CI check not appearing
- Push may not have triggered the workflow
- Check workflow trigger conditions in `.github/workflows/`
- HyperShift E2E requires manual `/test` comment

### Stale results
- CI runs on the commit at push time, not current HEAD
- Check `headSha` matches expected commit

## Related Skills

- `ci:monitoring` - Wait for and monitor running CI jobs
- `rca:ci` - Root cause analysis of CI failures
- `tdd:ci` - TDD iteration using CI as test environment
