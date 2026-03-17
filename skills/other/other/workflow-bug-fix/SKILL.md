---
name: workflow-bug-fix
description: Systematic approach to identifying, fixing, and validating bug fixes. Use when fixing bugs, resolving issues, or addressing errors.
---

# Bug Fix Workflow

Systematic process for fixing bugs properly.

## Phase 1: Root Cause Analysis
**Agents:** `root-cause-analyst`

Methods:
- Error trace analysis
- Log investigation
- State inspection
- Reproduce the bug consistently

**Output:** Root cause, affected components, impact assessment

## Phase 2: Fix Implementation

Constraints:
- Minimal scope (fix the bug, nothing more)
- Backward compatible
- Well tested

## Phase 3: Code Review
**Agents:** `code-reviewer`

Focus:
- Fix correctness
- Side effects
- Edge cases

## Phase 4: Regression Testing
**Agents:** `test-automator`

Create tests:
- Regression test (prevents this bug from returning)
- Edge case tests
- Integration tests if affected

## Phase 5: Security Check
**Agents:** `security-auditor`

**Blocking:** Ensure fix doesn't introduce vulnerabilities

## Phase 6: Validation
**Agents:** `quality-engineer`

Checklist:
- [ ] Original issue resolved
- [ ] No new issues introduced
- [ ] All tests pass

## Phase 7: Documentation
**Agents:** `technical-writer`

- Changelog entry
- Incident report (for significant bugs)
- Prevention guide (what caused it, how to avoid)

## Phase 8: Deployment
**Agents:** `deployment-engineer`

Strategy: Hotfix if critical, normal release otherwise

Monitor for 24h:
- Error rate
- Performance metrics
- User reports

## Success Criteria
- [ ] Bug verified fixed
- [ ] Regression tests added
- [ ] No side effects
- [ ] Documentation updated

## Anti-patterns
- ❌ Fixing symptoms instead of root cause
- ❌ Large scope changes mixed with bug fix
- ❌ Skipping regression tests
- ❌ No documentation of what caused it
