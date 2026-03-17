---
name: test-diff-analyzer
description: "Analyze test differences between runs to identify flaky tests and consistency issues. Use to find tests that fail intermittently."
category: testing
mcp_fallback: none
user-invocable: false
---

# Analyze Test Differences Between Runs

Compare test results across multiple runs to identify flaky tests.

## When to Use

- Test passes locally but fails in CI
- Test sometimes passes, sometimes fails (flaky test)
- Need to understand test consistency issues
- Comparing test results before/after code changes
- Debugging intermittent test failures

## Quick Reference

```bash
# Run tests and capture output
pixi run mojo test -I . tests/ > /tmp/test_run_1.log

# Compare two test runs
diff -u /tmp/test_run_1.log /tmp/test_run_2.log

# Extract failures from log
grep "FAILED" /tmp/test_run_*.log | sort | uniq -c

# Show tests that sometimes pass, sometimes fail
grep "FAILED\|PASSED" /tmp/test_run_*.log | cut -d: -f2 | sort | uniq -d
```

## Analysis Workflow

1. **Collect baseline**: Run tests locally N times
2. **Collect CI data**: Get CI test results from recent runs
3. **Compare outputs**: Diff between test runs
4. **Identify flaky tests**: Tests with inconsistent results
5. **Find patterns**: When does test fail vs pass
6. **Root cause**: Timing, randomness, resource issues
7. **Remediation**: Fix or isolate flaky test

## Flaky Test Indicators

**Timing Issues**:

- Test passes when run in isolation
- Test fails when run with other tests
- Timeout values too aggressive
- Race conditions in setup/teardown

**Randomness Issues**:

- Random seed not fixed
- Hash ordering varies
- Dictionary/set iteration order
- Floating point precision

**Resource Issues**:

- Test passes locally but fails in CI
- Fails under resource constraints
- Out of memory errors intermittently
- Disk space dependent

## Output Format

Report analysis with:

1. **Flaky Tests** - Tests with inconsistent results
2. **Consistency Score** - Pass rate across runs (e.g., 80% pass rate)
3. **Failure Patterns** - When/how tests fail
4. **Impact** - How many test runs affected
5. **Root Cause Hypothesis** - What likely causes instability
6. **Recommendations** - How to fix or isolate flaky test

## Error Handling

| Problem | Solution |
|---------|----------|
| Different environment | Run in controlled environment (docker) |
| Insufficient data | Run more iterations to get pattern |
| No failure info | Enable debug output, increase verbosity |
| External dependencies | Mock or isolate external services |
| Timing-dependent | Add explicit waits or retry logic |

## References

- See mojo-test-runner for test execution options
- See extract-test-failures for failure analysis
- See CLAUDE.md for test standards and TDD workflow
