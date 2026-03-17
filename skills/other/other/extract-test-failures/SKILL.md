---
name: extract-test-failures
description: "Extract and summarize test failures from logs. Use to quickly understand what tests failed and why."
category: testing
mcp_fallback: none
user-invocable: false
---

# Extract and Summarize Test Failures

Parse test logs to extract failure information and create summary.

## When to Use

- CI test run failed, need to understand failures
- Large test suite with many failures, need summary
- Categorizing failures by type (assertion, runtime, timeout)
- Creating PR review comments about failures
- Tracking which tests are failing over time

## Quick Reference

```bash
# Extract failed test names
grep "FAILED" test_output.log

# Get failure details with context
grep -A 10 "FAILED\|Error\|AssertionError" test_output.log

# Count failures by type
grep "FAILED\|AssertionError\|ValueError\|TypeError" test_output.log | sort | uniq -c

# Extract test summary line
tail -20 test_output.log | grep -E "passed|failed|error"

# Get specific failure info
grep -B 5 "AssertionError" test_output.log | head -50
```

## Failure Extraction Workflow

1. **Collect log**: Get test output from CI or local run
2. **Find failures**: Extract FAILED markers and error types
3. **Group by type**: Categorize assertion vs runtime vs timeout
4. **Extract details**: Get error messages and stack traces
5. **Count totals**: Summary of how many failures
6. **Identify patterns**: Common failure causes
7. **Summarize**: Create concise failure report

## Failure Categories

**Assertion Failures**:

- `AssertionError` - Expected value check failed
- `assert_equal()` - Values don't match
- `assert_true()` - Condition not true
- Fix: Check test logic and expected values

**Type/Attribute Errors**:

- `AttributeError` - Missing method/attribute
- `TypeError` - Wrong argument type
- `ValueError` - Invalid value for operation
- Fix: Check code syntax and types

**Runtime Errors**:

- `IndexError` - Out of bounds access
- `KeyError` - Dictionary key not found
- `ZeroDivisionError` - Division by zero
- Fix: Check boundary conditions

**Timeout/Hanging**:

- Test takes too long
- Infinite loop or deadlock
- Resource exhaustion
- Fix: Optimize or add timeout

## Output Format

Report failures with:

1. **Total Failures** - Count and percentage of total tests
2. **Failure Summary** - By type (assertion, runtime, timeout, other)
3. **Failed Tests** - List of test names that failed
4. **Top Issues** - Most common failure patterns
5. **Error Messages** - Representative error snippets
6. **Recommendations** - Which tests to focus on first

## Error Handling

| Problem | Solution |
|---------|----------|
| No FAILED markers | Check log format, may use different pattern |
| Truncated output | Get full log from artifacts instead of view |
| Mixed output types | Filter by log level or timestamp |
| Encoding issues | Convert to UTF-8 first |
| Very large logs | Split and process in chunks |

## References

- See test-diff-analyzer for identifying flaky tests
- See analyze-ci-failure-logs for CI-specific failures
- See generate-fix-suggestions for automated fixes
