---
name: calculate-coverage
description: "Measure test coverage and identify untested code. Use when assessing test completeness."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Calculate Coverage

Measure code coverage percentage and identify which code paths are untested to ensure comprehensive testing.

## When to Use

- Checking test coverage for modules
- Identifying gaps in test suites
- Meeting coverage thresholds (typically 80%+)
- Planning additional test cases

## Quick Reference

```bash
# Python coverage with pytest
pip install coverage pytest-cov
pytest --cov=module_name --cov-report=html tests/

# View coverage report
open htmlcov/index.html

# Check coverage threshold
coverage report --fail-under=80
```

## Workflow

1. **Install coverage tool**: Set up measurement infrastructure
2. **Run tests with coverage**: Execute test suite capturing coverage data
3. **Generate report**: Create HTML or text coverage report
4. **Analyze gaps**: Identify untested functions, branches, edge cases
5. **Plan improvements**: Create tests for uncovered code paths

## Output Format

Coverage analysis:

- Overall coverage percentage
- Per-module coverage breakdown
- Uncovered lines (with line numbers)
- Branch coverage (if applicable)
- Recommendations for improvement

## References

- See `run-tests` skill for test execution
- See `generate-tests` skill for test creation
- See CLAUDE.md > Key Development Principles (TDD) for testing strategy
