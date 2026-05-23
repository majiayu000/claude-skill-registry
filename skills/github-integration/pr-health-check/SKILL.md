---
name: pr-health-check
description: Use when checking if PR is ready to merge. Validates merge-readiness and PR status patterns.
version: "1.0.0"
author: "JacobPEvans"
---

# PR Health Check

<!-- markdownlint-disable-file MD013 -->

Standardized patterns for validating PR health, merge-readiness, and determining if a PR can proceed through its workflow.

## Purpose

Provides a single source of truth for PR status validation. All commands that need to verify PR readiness should use these patterns instead of duplicating health check logic.

## Merge-Readiness Criteria

A PR is ready to merge when ALL of the following are true:

1. **State**: `OPEN` (not draft, closed, or merged)
2. **Mergeable**: `MERGEABLE` (no conflicts)
3. **Status Checks**: ALL must be `SUCCESS` (no failures, no pending)
4. **Reviews**: All required reviews must be `APPROVED`
5. **Conversations**: ALL review threads must be `isResolved: true` (use the pr-thread-resolution-enforcement skill)

## Quick Health Check Query

Get comprehensive PR status:

```bash
gh pr view <PR_NUMBER> --json state,mergeable,statusCheckRollup,reviews,reviewDecision
```

**Interpretation**:

| Field | Values | Meaning |
| --- | --- | --- |
| `state` | `OPEN`, `CLOSED`, `MERGED` | Current state; must be OPEN |
| `mergeable` | `MERGEABLE`, `CONFLICTING`, `UNKNOWN` | Merge conflict status; must be MERGEABLE |
| `statusCheckRollup` | Array with `status` and `conclusion` | CI status; all must be SUCCESS |
| `reviewDecision` | `APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED`, null | Review status |

## Detailed Health Check Pattern

For comprehensive validation before merge attempts:

```bash
# Get full PR details
gh pr view <PR_NUMBER> --json state,mergeable,statusCheckRollup,reviews,reviewDecision,comments

# Verify each criterion:
# 1. State check: output should show "state": "OPEN"
# 2. Mergeable: output should show "mergeable": "MERGEABLE"
# 3. Status rollup: all items should have "conclusion": "SUCCESS"
# 4. Reviews: should show "reviewDecision": "APPROVED"
# 5. Conversations: use PR Thread Resolution Enforcement Skill verification query
```

## Status Check Rollup Understanding

The `statusCheckRollup` field contains an array of check results:

```json
{
  "state": "SUCCESS|FAILURE|PENDING",
  "contexts": [
    {"context": "Check Name", "state": "SUCCESS|FAILURE|PENDING"}
  ]
}
```

**Interpretation**:

- `state: SUCCESS` - All checks passed
- `state: FAILURE` - One or more checks failed
- `state: PENDING` - One or more checks still running

**Actions**:

- **SUCCESS**: Proceed if other criteria met
- **FAILURE**: Must fix before merge (see `/fix-pr-ci` command)
- **PENDING**: Must wait for checks to complete (use `gh pr checks <PR_NUMBER> --watch`)

## PR Filtering Logic

### Identify Healthy PRs

Use this logic to filter PRs that are merge-ready:

```bash
# List all open PRs
gh pr list --state open --json number,title,state,mergeable,statusCheckRollup,reviewDecision

# Filter for healthy PRs:
# - state == OPEN
# - mergeable == MERGEABLE
# - statusCheckRollup.state == SUCCESS
# - reviewDecision == APPROVED (for repos requiring reviews)
```

### Identify PRs Needing Attention

Use this logic to find PRs with issues:

```bash
# List all PRs with issues
gh pr list --state open --json number,title,state,mergeable,statusCheckRollup

# Filter for unhealthy PRs:
# - state != OPEN (unusual, but check)
# - mergeable == CONFLICTING or UNKNOWN
# - statusCheckRollup.state != SUCCESS
# - Reviews not approved
```

## Common Health Check Scenarios

### Scenario 1: PR Ready to Merge

- `state`: OPEN ✓
- `mergeable`: MERGEABLE ✓
- `statusCheckRollup.state`: SUCCESS ✓
- `reviewDecision`: APPROVED ✓
- **Action**: Proceed with merge

### Scenario 2: PR Has Merge Conflict

- `mergeable`: CONFLICTING ✗
- **Action**: Run `/sync-main` or manually resolve conflict

### Scenario 3: CI Checks Failing

- `statusCheckRollup.state`: FAILURE ✗
- **Action**: Run `/fix-pr-ci` to diagnose and fix

### Scenario 4: Checks Still Running

- `statusCheckRollup.state`: PENDING ⏳
- **Action**: Wait using `gh pr checks <PR_NUMBER> --watch`

### Scenario 5: Missing Approvals

- `reviewDecision`: CHANGES_REQUESTED or REVIEW_REQUIRED ✗
- **Action**: Address feedback using `/resolve-pr-review-thread`

## Commands Using This Skill

- `/manage-pr` - Phase 2.1 (PR Health Check)
- `/fix-pr-ci` - To filter which PRs need fixing
- `/ready-player-one` - To verify PRs are healthy before merge
- Any workflow needing PR status validation

## Related Resources

- github-graphql skill - Detailed GraphQL queries for PR fields
- pr-thread-resolution-enforcement skill - Review conversation validation

## Integration Points

### With Manage PR

In `/manage-pr` Phase 2.1, use this skill to determine next action:

```bash
# Get health status
gh pr view <PR_NUMBER> --json state,mergeable,statusCheckRollup,reviews,reviewDecision

# Determine action:
if mergeable != MERGEABLE: → /sync-main (conflict resolution)
if statusCheckRollup != SUCCESS: → /fix-pr-ci (CI fixes)
if reviewDecision != APPROVED: → /resolve-pr-review-thread (review feedback)
if all healthy: → Proceed to Phase 3
```

### With Fix PR CI

Use PR health check to prioritize which PRs to fix:

```bash
# Get all PRs with failing checks
gh pr list --state open --json number,statusCheckRollup

# Filter where statusCheckRollup.state == FAILURE
# These PRs are candidates for /fix-pr-ci
```

## Troubleshooting

### Issue: statusCheckRollup returns null

**Cause**: PR checks haven't started yet

**Solution**: Wait a few seconds and retry, or use `gh pr checks <PR_NUMBER>`

### Issue: mergeable returns UNKNOWN

**Cause**: GitHub is still calculating merge status

**Solution**: Wait 10-30 seconds and retry

### Issue: Check shows SUCCESS but merge fails

**Cause**: Different checks ran since last query (rare race condition)

**Solution**: Re-run health check immediately before merge

## Best Practices

1. **Always check before merge** - Use full health check even if PR "looks ready"
2. **Interpret reviewDecision carefully** - May differ from individual review states
3. **Monitor pending checks** - Use `--watch` flag to block until complete
4. **Fix conflicts early** - CONFLICTING status blocks everything else
5. **Respect required reviews** - Some repos require explicit approvals
6. **Use skill queries verbatim** - Exact same query each time ensures consistency
