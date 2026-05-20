---
name: compact-reviewer:testing-review
description: Use when reviewing test coverage for Compact contracts, identifying missing edge cases, evaluating testing strategies, or assessing test quality and completeness.
---

# Testing Review Skill

Evaluate test coverage, quality, and testing strategy for Compact contracts.

## When to Use

This skill activates for queries about:
- Test coverage
- Testing strategies
- Edge cases
- Test quality
- Missing tests

**Trigger words**: test, coverage, edge case, testing strategy, unit test, integration test

## Quick Reference

### Testing Checklist

| Category | Items to Test |
|----------|--------------|
| Happy path | Normal operations succeed |
| Authorization | Only authorized callers succeed |
| Validation | Invalid inputs are rejected |
| Boundaries | Edge cases at limits |
| State | State changes correctly |
| Errors | Proper failures on errors |

### Coverage Requirements

| Priority | Coverage Target |
|----------|-----------------|
| Critical (security) | 100% |
| High (core logic) | 90%+ |
| Medium (features) | 80%+ |
| Low (utilities) | 70%+ |

## Review Process

### 1. Coverage Analysis

For each exported circuit:
- Is there a happy-path test?
- Are authorization checks tested?
- Are input validations tested?
- Are edge cases covered?

### 2. Test Quality

Evaluate test characteristics:
- Clear test names
- Single concern per test
- Proper assertions
- Meaningful error messages

### 3. Edge Case Identification

Check for coverage of:
- Zero values
- Maximum values
- Empty collections
- Boundary conditions
- Race conditions

## References

- [Coverage Requirements](./references/coverage-requirements.md) - Coverage guidelines
- [Edge Case Checklist](./references/edge-case-checklist.md) - Common edge cases

## Related Skills

- [critical-issues](../critical-issues/SKILL.md) - Bug detection
- [security-review](../security-review/SKILL.md) - Security testing
