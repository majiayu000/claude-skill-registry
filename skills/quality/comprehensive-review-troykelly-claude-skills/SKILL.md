---
name: comprehensive-review
description: Use after implementing features - 7-criteria code review with MANDATORY artifact posting to GitHub issue; blocks PR creation until complete
allowed-tools:
  - Read
  - Grep
  - Glob
  - mcp__github__*
model: opus
---

# Comprehensive Review

## Overview

Review code against 7 criteria before considering it complete.

**Core principle:** Self-review catches issues before they reach others.

**HARD REQUIREMENT:** Review artifact MUST be posted to the GitHub issue. This is enforced by hooks.

**Announce at start:** "I'm performing a comprehensive code review."

## Review Artifact Requirement

**This is not optional.** Before a PR can be created:

1. Complete review against all 7 criteria
2. Document all findings
3. Post artifact to issue comment using EXACT format below
4. Address all findings (fix or defer with tracking issues)
5. Update artifact to show "Unaddressed: 0"

The `review-gate` skill and `PreToolUse` hook will BLOCK PR creation without this artifact.

## The 7 Criteria

### 1. Blindspots

**Question:** What am I missing?

| Check | Ask Yourself |
|-------|--------------|
| Edge cases | What happens at boundaries? Empty input? Max values? |
| Error paths | What if external services fail? Network issues? |
| Concurrency | Multiple users/threads? Race conditions? |
| State | What if called in wrong order? Invalid state? |
| Dependencies | What if dependency behavior changes? |

```typescript
// Blindspot example: What if items is empty?
function calculateAverage(items: number[]): number {
  return items.reduce((a, b) => a + b, 0) / items.length;
  // Blindspot: Division by zero when items is empty!
}

// Fixed
function calculateAverage(items: number[]): number {
  if (items.length === 0) {
    throw new Error('Cannot calculate average of empty array');
  }
  return items.reduce((a, b) => a + b, 0) / items.length;
}
```

### 2. Clarity/Consistency

**Question:** Will someone else understand this?

| Check | Ask Yourself |
|-------|--------------|
| Names | Do names describe what things do/are? |
| Structure | Is code organized logically? |
| Complexity | Can this be simplified? |
| Patterns | Does this match existing patterns? |
| Surprises | Would anything surprise a reader? |

### 3. Maintainability

**Question:** Can this be changed safely?

| Check | Ask Yourself |
|-------|--------------|
| Coupling | Is this tightly bound to other code? |
| Cohesion | Does this do one thing well? |
| Duplication | Is logic repeated anywhere? |
| Tests | Do tests cover this adequately? |
| Extensibility | Can new features be added easily? |

### 4. Security Risks

**Question:** Can this be exploited?

| Check | Ask Yourself |
|-------|--------------|
| Input validation | Is all input validated and sanitized? |
| Authentication | Is access properly controlled? |
| Authorization | Are permissions checked? |
| Data exposure | Is sensitive data protected? |
| Injection | SQL, XSS, command injection possible? |
| Dependencies | Are dependencies secure and updated? |

**NOTE:** If security-sensitive files are changed (auth, api, middleware, etc.), invoke `security-review` skill for deeper analysis.

### 5. Performance Implications

**Question:** Will this scale?

| Check | Ask Yourself |
|-------|--------------|
| Algorithms | Is complexity appropriate? O(n²) when O(n) possible? |
| Database | N+1 queries? Missing indexes? Full table scans? |
| Memory | Large objects in memory? Memory leaks? |
| Network | Unnecessary requests? Large payloads? |
| Caching | Should results be cached? |

### 6. Documentation

**Question:** Is this documented adequately?

| Check | Ask Yourself |
|-------|--------------|
| Public APIs | Are all public functions documented? |
| Parameters | Are parameter types and purposes clear? |
| Returns | Is return value documented? |
| Errors | Are thrown errors documented? |
| Examples | Are complex usages demonstrated? |
| Why | Are non-obvious decisions explained? |

See `inline-documentation` skill for documentation standards.

### 7. Standards and Style

**Question:** Does this follow project conventions?

| Check | Ask Yourself |
|-------|--------------|
| Naming | Follows project naming conventions? |
| Formatting | Matches project formatting? |
| Patterns | Uses established patterns? |
| Types | Fully typed (no `any`)? |
| Language | Uses inclusive language? |
| IPv6-first | Network code uses IPv6 by default? IPv4 only for documented legacy? |
| Linting | Passes all linters? |

See `style-guide-adherence`, `strict-typing`, `inclusive-language`, `ipv6-first` skills.

## Review Process

### Step 1: Prepare

```bash
# Get list of changed files
git diff --name-only HEAD~1

# Get full diff
git diff HEAD~1

# Check for security-sensitive files
git diff --name-only HEAD~1 | grep -E '(auth|security|middleware|api|password|token|secret)'
# If matches found, security-review skill is MANDATORY
```

### Step 2: Review Each Criterion

For each of the 7 criteria:

1. Review all changed code
2. Note any issues found
3. Determine severity (Critical/Major/Minor)

### Step 3: Check Security-Sensitive

If ANY security-sensitive files were changed:
1. Invoke `security-review` skill OR `security-reviewer` subagent
2. Include security review results in artifact
3. Mark "Security-Sensitive: YES" in artifact

### Step 4: Document Findings

```markdown
## Code Review Findings

### 1. Blindspots
- [ ] **Critical**: No handling for empty array in `calculateAverage()`
- [ ] **Minor**: Missing null check in `formatUser()`

### 2. Clarity/Consistency
- [ ] **Major**: Variable `x` should have descriptive name

### 3. Maintainability
- [x] No issues found

### 4. Security Risks
- [ ] **Critical**: SQL injection possible in `findUser()`

### 5. Performance Implications
- [ ] **Major**: N+1 query in `getOrdersWithUsers()`

### 6. Documentation
- [ ] **Minor**: Missing JSDoc on `processOrder()`

### 7. Standards and Style
- [x] Passes all checks
```

### Step 5: Address All Findings

Use `apply-all-findings` skill to address every issue.

For findings that cannot be fixed:
1. Use `deferred-finding` skill to create tracking issue
2. Link tracking issue in artifact
3. "Deferred without tracking issue" is NOT PERMITTED

### Step 6: Post Artifact to Issue (MANDATORY)

Post review artifact as comment on the GitHub issue:

```bash
ISSUE_NUMBER=123
gh issue comment $ISSUE_NUMBER --body "$(cat <<'EOF'
<!-- REVIEW:START -->
## Code Review Complete

| Property | Value |
|----------|-------|
| Worker | `[WORKER_ID]` |
| Issue | #123 |
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

**Review Status:** ✅ COMPLETE
<!-- REVIEW:END -->
EOF
)"
```

**CRITICAL:** "Unaddressed" MUST be 0. "Review Status" MUST be "COMPLETE".

## Severity Levels

| Severity | Description | Action |
|----------|-------------|--------|
| **Critical** | Security issue, data loss, crash | Must fix before merge |
| **Major** | Significant bug, performance issue | Must fix before merge |
| **Minor** | Style, clarity, small improvement | Should fix before merge |

## Checklist

Complete for every code review:

- [ ] Blindspots: Edge cases, errors, concurrency checked
- [ ] Clarity: Names, structure, complexity reviewed
- [ ] Maintainability: Coupling, cohesion, tests evaluated
- [ ] Security: Input, auth, injection, exposure checked (MANDATORY for sensitive files)
- [ ] Performance: Algorithms, queries, memory reviewed
- [ ] Documentation: Public APIs documented
- [ ] Style: Conventions followed
- [ ] All findings documented
- [ ] All findings addressed OR deferred with tracking issues
- [ ] Review artifact posted to issue (exact format)
- [ ] "Unaddressed: 0" in artifact
- [ ] "Review Status: COMPLETE" in artifact

## Integration

This skill is called by:
- `issue-driven-development` - Step 9

This skill uses:
- `review-scope` - Determine review breadth
- `apply-all-findings` - Address issues
- `security-review` - For security-sensitive changes
- `deferred-finding` - For creating tracking issues

This skill is enforced by:
- `review-gate` - Verifies artifact before PR
- `PreToolUse` hook - Blocks PR without artifact

This skill references:
- `inline-documentation` - Documentation standards
- `strict-typing` - Type requirements
- `style-guide-adherence` - Style requirements
- `inclusive-language` - Language requirements
- `ipv6-first` - Network code requirements (IPv6 primary, IPv4 legacy)
