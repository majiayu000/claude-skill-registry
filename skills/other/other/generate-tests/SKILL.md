---
name: generate-tests
description: "Create test cases for functions and modules. Use when implementing TDD or improving coverage."
mcp_fallback: none
category: testing
tier: 2
user-invocable: false
---

# Generate Tests

Create comprehensive test cases for functions and modules to ensure correctness and improve code coverage.

## When to Use

- Following test-driven development (TDD) approach
- Adding tests to increase coverage
- Testing edge cases and error conditions
- Validating refactoring doesn't break functionality

## Quick Reference

```python
# Test generation pattern
def generate_tests(function, test_cases: List[Tuple]):
    """Create test cases for a function"""
    for inputs, expected_output in test_cases:
        result = function(*inputs)
        assert result == expected_output, f"Failed for {inputs}"

# Example: test matrix multiply
test_cases = [
    (([[1, 2], [3, 4]], [[1, 0], [0, 1]]), [[1, 2], [3, 4]]),  # Identity
    (([], []), []),  # Empty
]
```

## Workflow

1. **Analyze function**: Understand inputs, outputs, side effects
2. **Identify test cases**: Normal cases, edge cases, error cases
3. **Write assertions**: Create expected output for each case
4. **Implement tests**: Create test functions in test file
5. **Verify coverage**: Check that tests exercise all code paths

## Output Format

Test suite:

- Test class/module with clear naming
- Test methods (test_normal_case, test_edge_case, test_error_case)
- Setup/teardown if needed
- Clear assertions with error messages
- Coverage report showing lines tested

## References

- See `run-tests` skill for executing tests
- See `calculate-coverage` skill for coverage analysis
- See CLAUDE.md > TDD in Key Development Principles
