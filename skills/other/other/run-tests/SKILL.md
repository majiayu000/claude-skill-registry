---
name: run-tests
description: "Execute test suites and report results. Use when validating code functionality."
mcp_fallback: none
category: testing
tier: 1
user-invocable: false
---

# Run Tests

Execute test suites to verify code functionality and identify regressions or failures.

## When to Use

- Pre-commit validation
- Running tests after changes
- Verifying test suite passes
- Generating test reports

## Quick Reference

```bash
# Run all tests with Mojo
pixi run mojo test -I . tests/

# Run specific test file
mojo test -I . tests/shared/core/test_example.mojo

# Run with verbose output
mojo test -I . tests/ -v

# Python pytest
pytest tests/
pytest tests/ -v --tb=short
```

## Workflow

1. **Set up test environment**: Ensure all dependencies installed
2. **Select tests**: Choose which test suite or specific tests to run
3. **Execute tests**: Run test runner with appropriate options
4. **Review results**: Check pass/fail status and output
5. **Debug failures**: Investigate and fix failing tests

## Output Format

Test results:

- Total tests run
- Passed/failed/skipped counts
- Failure details (assertion message, stack trace)
- Execution time per test
- Test coverage metrics (if applicable)

## References

- See `generate-tests` skill for creating tests
- See `calculate-coverage` skill for coverage analysis
- See CLAUDE.md > TDD in Key Development Principles
