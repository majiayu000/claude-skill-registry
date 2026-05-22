---
name: qa-workflow
description: 'QA validation and fix loop workflow. Use when implementation is complete and needs quality assurance before sign-off.'
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Be thorough - you are the last line of defense
  - Be specific with file paths and line numbers
  - Fix what QA found, don't add features
error_handling: graceful
streaming: supported
source: auto-claude
---

# QA Workflow Skill

## Overview

Comprehensive quality assurance workflow that validates implementation completeness and correctness, then iterates through fix cycles until approval. You are the last line of defense before shipping.

**Core principle:** You are the last line of defense. If you approve, the feature ships. Be thorough.

## When to Use

**Always:**

- After implementation is marked complete
- Before merging or deploying changes
- When validating acceptance criteria

**Exceptions:**

- Documentation-only changes (may use minimal validation)
- Trivial fixes with skip_validation flag

## The Iron Law

```
NO SIGN-OFF WITHOUT VERIFICATION OF ALL ACCEPTANCE CRITERIA
```

Every acceptance criterion must be verified before approval.

## Part 1: QA Review

### Phase 0: Load Context

```bash
# Read the spec (your source of truth for requirements)
cat .claude/context/specs/[task-name]-spec.md

# Read any previous QA reports
cat .claude/context/reports/qa-report.md 2>/dev/null || echo "No previous report"

# See what files were changed
git diff main...HEAD --name-status

# Read QA acceptance criteria from spec
grep -A 100 "## QA Acceptance" spec.md
```

### Phase 1: Verify All Work Completed

```bash
# Check git log for implementation commits
git log --oneline main..HEAD

# Verify expected files were modified
git diff main...HEAD --name-only
```

**STOP if implementation is not complete.** QA runs after implementation.

### Phase 2: Start Test Environment

```bash
# Start services as needed
npm run dev  # or appropriate command

# Verify services are running
curl http://localhost:3000/health 2>/dev/null || echo "Service not responding"
```

Wait for all services to be healthy before proceeding.

### Phase 3: Run Automated Tests

#### Unit Tests

Run all unit tests for affected areas:

```bash
# Run test suite
npm test
# or
pytest
# or
go test ./...
```

**Document results:**

```
UNIT TESTS:
- [area-name]: PASS/FAIL (X/Y tests)
```

#### Integration Tests

Run integration tests if applicable:

```bash
# Run integration test suite
npm run test:integration
```

**Document results:**

```
INTEGRATION TESTS:
- [test-name]: PASS/FAIL
```

#### End-to-End Tests

If E2E tests exist:

```bash
# Run E2E test suite
npm run test:e2e
```

**Document results:**

```
E2E TESTS:
- [flow-name]: PASS/FAIL
```

### Phase 4: Manual Verification

For each acceptance criterion in the spec:

1. **Navigate** to the relevant area
2. **Verify** the criterion is met
3. **Check** for console errors
4. **Test** edge cases
5. **Document** findings

```
MANUAL VERIFICATION:
- [Criterion 1]: PASS/FAIL
  - Evidence: [what you observed]
- [Criterion 2]: PASS/FAIL
  - Evidence: [what you observed]
```

### Phase 5: Code Review

#### Security Review

Check for common vulnerabilities:

```bash
# Look for security issues
grep -r "eval(" --include="*.js" --include="*.ts" . 2>/dev/null
grep -r "innerHTML" --include="*.js" --include="*.ts" . 2>/dev/null
grep -r "dangerouslySetInnerHTML" --include="*.tsx" --include="*.jsx" . 2>/dev/null

# Check for hardcoded secrets
grep -rE "(password|secret|api_key|token)\s*=\s*['\"][^'\"]+['\"]" . 2>/dev/null
```

#### Pattern Compliance

Verify code follows established patterns:

```bash
# Compare new code to existing patterns
# Read pattern files, compare structure
```

**Document findings:**

```
CODE REVIEW:
- Security issues: [list or "None"]
- Pattern violations: [list or "None"]
- Code quality: PASS/FAIL
```

### Phase 6: Regression Check

Run full test suite to catch regressions:

```bash
# Run ALL tests, not just new ones
npm test -- --coverage
```

Verify key existing functionality still works.

```
REGRESSION CHECK:
- Full test suite: PASS/FAIL (X/Y tests)
- Existing features verified: [list]
- Regressions found: [list or "None"]
```

### Phase 7: Generate QA Report

```markdown
# QA Validation Report

**Task**: [task-name]
**Date**: [timestamp]

## Summary

| Category            | Status    | Details     |
| ------------------- | --------- | ----------- |
| Unit Tests          | PASS/FAIL | X/Y passing |
| Integration Tests   | PASS/FAIL | X/Y passing |
| E2E Tests           | PASS/FAIL | X/Y passing |
| Manual Verification | PASS/FAIL | [summary]   |
| Security Review     | PASS/FAIL | [summary]   |
| Pattern Compliance  | PASS/FAIL | [summary]   |
| Regression Check    | PASS/FAIL | [summary]   |

## Issues Found

### Critical (Blocks Sign-off)

1. [Issue description] - [File/Location]

### Major (Should Fix)

1. [Issue description] - [File/Location]

### Minor (Nice to Fix)

1. [Issue description] - [File/Location]

## Verdict

**SIGN-OFF**: [APPROVED / REJECTED]

**Reason**: [Explanation]

**Next Steps**:

- [If approved: Ready for merge]
- [If rejected: List of fixes needed]
```

Save report to `.claude/context/reports/qa-report.md`

### Phase 8: Decision

#### If APPROVED

```
=== QA VALIDATION COMPLETE ===

Status: APPROVED

All acceptance criteria verified:
- Unit tests: PASS
- Integration tests: PASS
- Manual verification: PASS
- Security review: PASS
- Regression check: PASS

The implementation is production-ready.
Ready for merge.
```

#### If REJECTED

Create fix request and proceed to Part 2.

---

## Part 2: QA Fix Loop

### Phase 0: Load Fix Request

```bash
# Read the QA report with issues
cat .claude/context/reports/qa-report.md

# Identify issues to fix
grep -A 50 "## Issues Found" .claude/context/reports/qa-report.md
```

Extract from report:

- Exact issues to fix
- File locations
- Required fixes
- Verification criteria

### Phase 1: Parse Fix Requirements

Create a checklist from the QA report:

```
FIXES REQUIRED:
1. [Issue Title]
   - Location: [file:line]
   - Problem: [description]
   - Fix: [what to do]
   - Verify: [how to check]

2. [Issue Title]
   ...
```

You must address EVERY issue.

### Phase 2: Fix Issues One by One

For each issue:

1. **Read** the problem area
2. **Understand** what's wrong
3. **Implement** the fix
4. **Verify** the fix locally

**Follow these rules:**

- Make the MINIMAL change needed
- Don't refactor surrounding code
- Don't add features
- Match existing patterns
- Test after each fix

### Phase 3: Run Tests

After all fixes are applied:

```bash
# Run the full test suite
npm test

# Run specific tests that were failing
[failed test commands from QA report]
```

**All tests must pass before proceeding.**

### Phase 4: Self-Verification

Before requesting re-review, verify each fix:

```
SELF-VERIFICATION:
[ ] Issue 1: [title] - FIXED
    - Verified by: [how you verified]
[ ] Issue 2: [title] - FIXED
    - Verified by: [how you verified]
...

ALL ISSUES ADDRESSED: YES/NO
```

If any issue is not fixed, go back to Phase 2.

### Phase 5: Commit Fixes

```bash
# Add fixed files
git add [fixed-files]

# Commit with descriptive message
git commit -m "fix: Address QA issues

Fixes:
- [Issue 1 title]
- [Issue 2 title]

Verified:
- All tests pass
- Issues verified locally"
```

### Phase 6: Signal for Re-Review

```
=== QA FIXES COMPLETE ===

Issues fixed: [N]

1. [Issue 1] - FIXED
   Commit: [hash]

2. [Issue 2] - FIXED
   Commit: [hash]

All tests passing.
Ready for QA re-validation.
```

---

## QA Loop Behavior

The QA → Fix → QA loop continues until:

1. **All critical issues resolved**
2. **All tests pass**
3. **No regressions**
4. **QA approves**

Maximum iterations: 5

If max iterations reached without approval:

- Escalate to human review
- Document all remaining issues
- Save detailed report

## Severity Guidelines

**CRITICAL** - Blocks sign-off:

- Failing tests
- Security vulnerabilities
- Missing required functionality
- Data corruption risks

**MAJOR** - Should fix:

- Missing edge case handling
- Performance issues
- UX problems
- Pattern violations

**MINOR** - Nice to fix:

- Style inconsistencies
- Documentation gaps
- Minor optimizations

## Verification Checklist

Before approving:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass (if applicable)
- [ ] Manual verification of acceptance criteria
- [ ] Security review complete
- [ ] Pattern compliance verified
- [ ] No regressions found
- [ ] QA report generated

## Common Mistakes

### Approving Too Quickly

**Why it's wrong:** Shipping bugs to users.

**Do this instead:** Check EVERYTHING in the acceptance criteria.

### Vague Issue Reports

**Why it's wrong:** Developer can't fix what they don't understand.

**Do this instead:** Exact file paths, line numbers, reproducible steps.

### Fixing Too Much

**Why it's wrong:** Introducing new bugs while fixing old ones.

**Do this instead:** Minimal changes. Fix only what QA found.

## Integration with Other Skills

This skill works well with:

- **complexity-assessment**: Determines validation depth
- **tdd**: Use TDD to write tests for fixes
- **debugging**: Use when investigating test failures

## Memory Protocol

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
