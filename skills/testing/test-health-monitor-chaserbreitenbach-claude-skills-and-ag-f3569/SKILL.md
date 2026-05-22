---
name: test-health-monitor
description: |
  Intelligent agent that monitors, analyzes, and improves test suite health. Detects flaky tests,
  identifies coverage gaps, tracks test performance trends, and recommends improvements. Ensures
  test suites remain valuable and maintainable over time.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
compatibility:
  claude-code: ">=1.0.0"
metadata:
  version: "1.0.0"
  author: "QuantQuiver AI R&D"
  category: "testing"
  tags:
    - test-health
    - flaky-tests
    - test-coverage
    - test-maintenance
---

# Test Health Monitor

## Purpose

Intelligent agent that monitors, analyzes, and improves test suite health. Detects flaky tests, identifies coverage gaps, tracks test performance trends, and recommends improvements. Ensures test suites remain valuable and maintainable.

## Triggers

Use this skill when:
- "analyze test suite health"
- "find flaky tests"
- "improve test coverage"
- "why are tests slow"
- "test maintenance report"
- "optimize test suite"
- "fix broken tests"
- "test health check"

## When to Use

- CI/CD pipeline slowdowns
- Intermittent test failures
- Declining test coverage
- Test maintenance burden increasing
- New team members struggling with tests
- Tests that no one trusts

## When NOT to Use

- Writing new tests (use unit-test-generator)
- Running tests (use CI/CD directly)
- Testing specific functionality (use appropriate test skill)

---

## Core Instructions

### Health Monitoring Dimensions

| Dimension | Description | Weight |
|-----------|-------------|--------|
| **Reliability** | Flaky test rate, consistent pass/fail | 30% |
| **Coverage** | Line/branch/path coverage | 25% |
| **Performance** | Test execution time | 20% |
| **Maintainability** | Code complexity, duplication | 15% |
| **Value** | Bug detection capability | 10% |

### Health Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Flaky Rate** | % tests that pass/fail intermittently | < 1% |
| **Coverage** | Code covered by tests | > 80% |
| **Pass Rate** | % tests passing consistently | > 99% |
| **Avg Duration** | Mean test execution time | < 100ms |
| **Total Duration** | Full suite runtime | < 10 min |
| **Duplication** | Duplicate test logic | < 5% |
| **Complexity** | Avg test complexity score | < 10 |

### Flaky Test Detection

A test is considered flaky when:
- Same code produces different results
- Passes in some runs, fails in others
- Failure rate between 2% and 98%

**Common Causes:**
- Race conditions
- External service dependencies
- Time-dependent logic
- Resource contention
- Network latency

---

## Templates

### Health Report

```markdown
# Test Suite Health Report

**Report ID:** {report_id}
**Generated:** {generated_at}
**Analysis Period:** {period_days} days

## Health Score

### Overall: {overall_score}/100

| Dimension | Score | Status |
|-----------|-------|--------|
| Reliability | {reliability} | {status} |
| Coverage | {coverage} | {status} |
| Performance | {performance} | {status} |
| Maintainability | {maintainability} | {status} |

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | {total_tests} |
| Passing | {passing_tests} |
| Flaky | {flaky_tests} |
| Slow Tests | {slow_tests} |

## Flaky Tests

| Test | Flaky Rate | Runs | Last Failure |
|------|------------|------|--------------|
| `{test_name}` | {flaky_rate}% | {runs} | {last_failure} |

## Recommendations

### {title}

**Priority:** {priority}
**Impact:** {impact}

{description}

**Steps:**
1. {step}
```

---

## Example

**Input**: Analyze 30 days of CI history for flaky tests

**Output**:
```markdown
## Health Score

### Overall: 72.3/100

| Dimension | Score | Status |
|-----------|-------|--------|
| Reliability | 65.0 | Warn |
| Coverage | 78.5 | Warn |
| Performance | 75.0 | Warn |
| Maintainability | 85.0 | Pass |

## Flaky Tests

| Test | Flaky Rate | Runs | Last Failure |
|------|------------|------|--------------|
| `test_api_timeout` | 15.2% | 125 | 2025-01-10 |
| `test_database_connection` | 8.3% | 96 | 2025-01-11 |

### Suspected Causes

**test_api_timeout:**
- Network latency or slow external dependencies
- High timing variance (possible race condition)

## Recommendations

### Fix Critical Flaky Tests

**Priority:** Critical
**Impact:** Reduce CI failures by 50-80%

2 tests fail >10% of the time, causing CI unreliability

**Steps:**
1. Review failure patterns for each test
2. Add retry logic or increase timeouts
3. Mock flaky external dependencies
4. Add deterministic test data
```

---

## Validation Checklist

- [ ] Sufficient CI history analyzed (>= 10 runs per test)
- [ ] Coverage data is current
- [ ] Flaky tests have suspected causes
- [ ] Performance baseline established
- [ ] Recommendations are actionable
- [ ] Priority reflects business impact
- [ ] Effort estimates are realistic

---

## Related Skills

- `unit-test-generator` - For generating new tests
- `api-contract-validator` - For API test coverage
- `security-test-suite` - For security test coverage
- `data-validation` - For data quality test patterns
