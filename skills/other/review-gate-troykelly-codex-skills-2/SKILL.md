---
name: review-gate
description: HARD GATE before PR creation - verifies review artifact exists in issue comments, all findings addressed or tracked, blocks PR creation if requirements not met
---

# Review Gate

## Overview

Hard compliance gate that BLOCKS PR creation until review requirements are satisfied.

**Core principle:** No PR without proof of review. No exceptions.

**This is enforced by hooks.** Even if you attempt to skip this skill, the `PreToolUse` hook on `gh pr create` will block the action.

## Gate Requirements

ALL must be satisfied to create a PR:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           REVIEW GATE                                     │
├──────────────────────────────────────────────────────────────────────────┤
│  [ ] Review artifact posted to issue (<!-- REVIEW:START --> format)      │
│  [ ] Review status is COMPLETE (not BLOCKED or IN_PROGRESS)              │
│  [ ] Unaddressed findings = 0                                            │
│  [ ] All deferred findings have tracking issues (linked in artifact)     │
│  [ ] Security review complete (if security-sensitive code changed)       │
├──────────────────────────────────────────────────────────────────────────┤
│  ALL SATISFIED → PR CREATION ALLOWED                                     │
│  ANY MISSING → PR CREATION BLOCKED                                       │
└──────────────────────────────────────────────────────────────────────────┘
```

## Verification Process

### Step 1: Check Review Artifact Exists

```bash
# Query issue comments for review artifact
ISSUE_NUMBER=123
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
REVIEW_EXISTS=$(gh api "/repos/$REPO/issues/$ISSUE_NUMBER/comments" \
  --jq '[.[] | select(.body | contains("<!-- REVIEW:START -->"))] | length')

if [ "$REVIEW_EXISTS" -eq 0 ]; then
  echo "BLOCKED: No review artifact found"
fi
```

### Step 2: Parse Review Status

Extract from the latest review artifact:

```bash
# Get latest review comment
REVIEW_BODY=$(gh api "/repos/$REPO/issues/$ISSUE_NUMBER/comments" \
  --jq '[.[] | select(.body | contains("<!-- REVIEW:START -->"))] | last | .body')

# Check status
if echo "$REVIEW_BODY" | grep -q "Review Status.*COMPLETE"; then
  echo "Review status: COMPLETE"
elif echo "$REVIEW_BODY" | grep -q "Review Status.*BLOCKED"; then
  echo "BLOCKED: Review status is BLOCKED_ON_DEPENDENCIES"
fi
```

### Step 3: Verify No Unaddressed Findings

```bash
# Extract unaddressed count
UNADDRESSED=$(echo "$REVIEW_BODY" | grep -oP 'Unaddressed[:\s|]+\K\d+' | head -1)

if [ "$UNADDRESSED" != "0" ]; then
  echo "BLOCKED: $UNADDRESSED unaddressed findings"
fi
```

### Step 4: Verify Deferred Findings Have Tracking Issues

For each deferred finding, verify a tracking issue exists and is linked:

```bash
# Each deferred finding must have format: | Finding | ... | #NNN | ...
DEFERRED_WITHOUT_ISSUE=$(echo "$REVIEW_BODY" | grep -i "DEFERRED" | grep -cv "#[0-9]" || echo "0")

if [ "$DEFERRED_WITHOUT_ISSUE" -gt 0 ]; then
  echo "BLOCKED: $DEFERRED_WITHOUT_ISSUE deferred findings without tracking issues"
fi
```

### Step 5: Security Review (Conditional)

If files matching security-sensitive patterns were changed:

```bash
# Check if security-sensitive files changed
SECURITY_FILES=$(git diff --name-only HEAD~1 | grep -E '(auth|security|middleware|api|password|token|secret)')

if [ -n "$SECURITY_FILES" ]; then
  # Verify security review section exists in artifact
  if ! echo "$REVIEW_BODY" | grep -q "Security-Sensitive.*YES"; then
    echo "BLOCKED: Security-sensitive files changed but no security review"
  fi
fi
```

## Review Artifact Format

The review artifact MUST follow this exact format for machine parsing:

```markdown
<!-- REVIEW:START -->
## Code Review Complete

| Property | Value |
|----------|-------|
| Worker | `[WORKER_ID]` |
| Issue | #[ISSUE_NUMBER] |
| Scope | [MINOR|MAJOR] |
| Security-Sensitive | [YES|NO] |
| Reviewed | [ISO_TIMESTAMP] |

### Criteria Results

| # | Criterion | Status | Findings |
|---|-----------|--------|----------|
| 1 | Blindspots | [✅ PASS|✅ FIXED|⚠️ DEFERRED] | [N] |
| 2 | Clarity | [✅ PASS|✅ FIXED|⚠️ DEFERRED] | [N] |
| 3 | Maintainability | [✅ PASS|✅ FIXED|⚠️ DEFERRED] | [N] |
| 4 | Security | [✅ PASS|✅ FIXED|⚠️ DEFERRED|N/A] | [N] |
| 5 | Performance | [✅ PASS|✅ FIXED|⚠️ DEFERRED] | [N] |
| 6 | Documentation | [✅ PASS|✅ FIXED|⚠️ DEFERRED] | [N] |
| 7 | Style | [✅ PASS|✅ FIXED|⚠️ DEFERRED] | [N] |

### Findings Fixed in This PR

| # | Severity | Finding | Resolution |
|---|----------|---------|------------|
| 1 | [SEVERITY] | [DESCRIPTION] | [HOW_FIXED] |

### Findings Deferred (With Tracking Issues)

| # | Severity | Finding | Tracking Issue | Justification |
|---|----------|---------|----------------|---------------|
| 1 | [SEVERITY] | [DESCRIPTION] | #[ISSUE] | [WHY] |

### Summary

| Category | Count |
|----------|-------|
| Fixed in PR | [N] |
| Deferred (with tracking) | [N] |
| Unaddressed | 0 |

**Review Status:** [✅ COMPLETE|⏸️ BLOCKED_ON_DEPENDENCIES]
<!-- REVIEW:END -->
```

## Blocked Scenarios

### Missing Review Artifact

```
REVIEW GATE BLOCKED

Reason: No review artifact found in issue #123

Required Action:
1. Perform comprehensive-review
2. Post review artifact to issue #123 using standard format
3. Address all findings or create tracking issues
4. Retry PR creation

Hint: Run `codex-subagent code-reviewer` to perform the review.
```

### Unaddressed Findings

```
REVIEW GATE BLOCKED

Reason: 3 unaddressed findings in review artifact

Required Action:
1. Fix the unaddressed findings, OR
2. Create tracking issues and update artifact with links
3. Ensure "Unaddressed: 0" in artifact summary
4. Retry PR creation
```

### Missing Security Review

```
REVIEW GATE BLOCKED

Reason: Security-sensitive files changed without security review

Files detected:
- src/auth/login.ts
- src/middleware/authenticate.ts

Required Action:
1. Run `codex-subagent security-reviewer`
2. Update review artifact with "Security-Sensitive: YES"
3. Document security review findings
4. Retry PR creation
```

## Checklist

Before attempting PR creation:

- [ ] `comprehensive-review` skill completed
- [ ] Review artifact posted to issue (exact format)
- [ ] All findings either FIXED or DEFERRED
- [ ] All DEFERRED findings have tracking issues created
- [ ] Tracking issue numbers in artifact
- [ ] Security review if security-sensitive files changed
- [ ] "Unaddressed: 0" in summary
- [ ] "Review Status: COMPLETE"

## Integration

This skill is enforced by:
- `PreToolUse` hook on `Bash` (filters `gh pr create`)

This skill is called after:
- `comprehensive-review`
- `apply-all-findings`
- `security-review` (if applicable)

This skill precedes:
- `pr-creation`
