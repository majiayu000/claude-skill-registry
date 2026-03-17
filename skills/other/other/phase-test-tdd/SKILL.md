---
name: phase-test-tdd
description: "Generate test files and coordinate test-driven development (TDD). Use when creating tests before implementation or during test phase."
mcp_fallback: none
category: phase
phase: Test
user-invocable: false
---

# Test-Driven Development Skill

Coordinate test-driven development by writing tests first, then implementing to make them pass.

## When to Use

- Creating tests before implementation (TDD workflow)
- Starting test phase of 5-phase workflow
- Writing unit, integration, or performance tests
- Need test files following Mojo or Python patterns

## Quick Reference

```bash
# TDD Cycle: Write test → Run (fail) → Implement → Run (pass) → Refactor

# Generate test file
cat > tests/test_component.mojo << 'EOF'
from testing import assert_equal

fn test_basic_behavior() raises:
    """Test basic functionality."""
    let result = function_under_test()
    assert_equal(result, expected_value)
EOF

# Run test (should fail initially)
mojo test tests/test_component.mojo

# Implement code to make test pass
# Re-run test (should pass)
mojo test tests/test_component.mojo
```

## Workflow

1. **Write test first** - Define expected behavior before implementation
2. **Run test** (Red phase) - Test fails because code doesn't exist yet
3. **Implement code** (Green phase) - Write minimal code to make test pass
4. **Refactor** (Refactor phase) - Clean up while keeping tests passing
5. **Repeat** - Add next test and repeat cycle

## Test Types

| Type | Location | Purpose |
|------|----------|---------|
| Unit | `tests/unit/` | Test individual functions in isolation |
| Integration | `tests/integration/` | Test component interactions |
| Performance | `tests/performance/` | Benchmark SIMD and critical paths |

## Mojo Test Pattern

```mojo
from testing import assert_equal, assert_true

fn test_add() raises:
    """Test addition operation."""
    # Arrange
    var a = 1
    var b = 2

    # Act
    var result = add(a, b)

    # Assert
    assert_equal(result, 3)
```

## Python Test Pattern

```python
import pytest

class TestComponent:
    """Test suite for component."""

    def test_basic(self):
        """Test basic functionality."""
        # Arrange
        data = prepare_data()

        # Act
        result = process(data)

        # Assert
        assert result == expected
```

## Test Coverage Requirements

- **Minimum**: 80% for new code
- **Critical paths**: 100% coverage required
- **Edge cases**: Must be tested (null, empty, boundary values)
- **Error handling**: All error paths tested

## Phase Dependencies

- **Precedes**: Implementation phase (tests drive implementation)
- **Parallel with**: Implementation and Package phases (all run after Plan)
- **Receives input from**: Plan phase (specifications, acceptance criteria)
- **Produces for**: Implementation phase (test contracts for code)

## Output Location

- **Test files**: `/tests/<type>/<module>_test.mojo` or `.py`
- **Test documentation**: `/notes/issues/<issue-number>/README.md`
- **Coverage reports**: `coverage/` directory

## Error Handling

| Error | Fix |
|-------|-----|
| Test import fails | Check file path and module structure |
| Test timeout | Optimize code or increase timeout |
| Flaky tests | Add setup/teardown, check for randomness |
| Low coverage | Add tests for uncovered branches |

## References

- `CLAUDE.md` - "Key Development Principles" (TDD section)
- `CLAUDE.md` - "Common Mistakes to Avoid" (test failure patterns)
- `notes/review/mojo-test-failure-learnings.md` - Real test failure solutions

---

**Key Principle**: Red → Green → Refactor. Don't skip the red phase.
