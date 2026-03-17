---
name: ci:monitoring
description: Monitor running CI jobs, wait for completion, create tasks for results
---

# CI Monitoring

Monitor running CI pipelines and report results. Creates task items for each CI check being monitored.

## When to Use

- After pushing to a PR, to track CI completion
- When user says "monitor CI" or "check CI"
- When waiting for HyperShift E2E (long-running, needs manual trigger)
- To track multiple CI checks in parallel

## Workflow

### 1. Create Monitoring Tasks

For each pending CI check, create a task:

```
TaskCreate: "<worktree> | <PR> | CI | Monitor | <check-name>"
  metadata: plan="ad-hoc", runner="main-session"
```

Example:
```
#33 [in_progress] mlflow-ci | PR#569 | CI | Monitor | Kind Deploy & Test
#34 [pending]     mlflow-ci | PR#569 | CI | Monitor | HyperShift E2E
```

### 2. Check Status Periodically

```bash
gh pr checks <PR-number>
```

### 3. On Completion

For each check that completes:
- Mark monitoring task as `completed`
- If **passed**: note in task description
- If **failed**: create RCA task and invoke `rca:ci`

```
TaskUpdate: #33 status=completed
TaskCreate: "<worktree> | <PR> | Kind CI | RCA | <failure summary>"
```

### 4. Report Summary

Present final status table:

| # | Check | Status | Action |
|---|-------|--------|--------|
| #33 | Kind Deploy & Test | passed | - |
| #34 | HyperShift E2E | failed | → #35 RCA created |
| #35 | Kind CI | RCA | Agent empty response |

## CI Check Types

| Check | Trigger | Duration | Manual? |
|-------|---------|----------|---------|
| CodeQL | Auto on push | ~2 min | No |
| Deploy & Test (Kind) | Auto on push | ~12 min | No |
| E2E HyperShift | `/test` comment | ~45 min | Yes |
| Build, Lint, Security | Auto on push | ~1 min | No |

## HyperShift E2E

HyperShift requires manual trigger:
```bash
# Trigger via PR comment (done by user in GitHub UI)
# The workflow responds to issue_comment with "/test"
```

Monitor:
```bash
gh run view <run-id> --json status --jq '.status'
gh run view <run-id> | head -25
```

## Task Tracking

On invocation:
1. TaskList - find existing CI monitoring tasks for this PR
2. Update completed checks
3. Create new monitoring tasks for pending checks
4. For failures, create RCA tasks linked to `rca:ci` or `rca:hypershift`

Naming: `<worktree> | <PR> | CI | Monitor | <check-name>`

## Troubleshooting

### HyperShift not starting
- Needs `/test` comment on PR
- Check if previous run is still cleaning up
- Check slot availability: CI has limited concurrent HyperShift clusters

### CI running on old commit
- Push triggers new run on latest commit
- Old runs may still be in progress
- Check `headSha` matches expected commit

## Related Skills

- `ci:status` - One-time status check
- `rca:ci` - RCA when CI fails
- `tdd:ci` - TDD iteration using CI
- `tdd:kind` - Local Kind testing (faster feedback)
