---
name: test-writer
description: Generates comprehensive test files for functions and classes. Use after writing a function, method, or class to quickly create unit tests with edge cases, assertions, and proper test structure. Supports multiple testing frameworks (pytest, unittest, jest, etc.) and follows testing best practices (AAA pattern, mocking, fixtures).
---

# Test Writer

## Overview

Generates well-structured test files for your code. Analyzes functions/classes, identifies test cases (including edge cases), and creates complete test files following best practices.

## Workflow

### Step 1: Analyze Code

Identify what to test:
- Function signature (parameters, types, return type)
- Behavior and dependencies
- Edge cases (None, empty, invalid input, boundaries)
- Error conditions (exceptions)

### Step 2: Identify Test Cases

Systematically categorize test cases:

**Test case categories:**
1. **Happy path**: Normal expected inputs
2. **Edge cases**: Boundary values, empty collections, None
3. **Error cases**: Invalid inputs that should raise exceptions
4. **Type variations**: Different valid types (if applicable)
5. **State-dependent**: Different object states (for classes)

**Example for `calculate_discount(price, discount_percent)`:**
- Normal: 20% discount → 80.0
- Edge: 0% → 100.0, 100% → 0.0
- Error: negative → ValueError, >100% → ValueError

### Step 3: Determine Framework

Choose testing framework (ask user if unclear):
- **Python**: pytest (default), unittest
- **JavaScript**: jest (default), mocha
- **Others**: Use language-appropriate framework

### Step 4: Generate Test Structure

Create test file with proper structure:

**File naming:**
- Python: `test_[module].py` in `tests/` directory
- JavaScript: `[module].test.js` or `[module].spec.js`

**Use AAA pattern** (Arrange-Act-Assert):
```python
def test_calculate_discount():
    # Arrange - Set up test data
    price = 100.0
    discount = 20.0

    # Act - Call function
    result = calculate_discount(price, discount)

    # Assert - Verify outcome
    assert result == 80.0
```

### Step 5: Write Tests

For each test case, create test function:
- Descriptive name (`test_calculate_discount_with_normal_input`)
- Docstring explaining what is tested
- Follow AAA pattern
- Use appropriate assertions

**Common assertions:**
- Equality: `assert result == expected`
- Exceptions: `with pytest.raises(ValueError):`
- Floating point: `assert result == pytest.approx(80.0)`
- Collections: `assert item in result`

### Step 6: Add Mocks/Fixtures (if needed)

**Fixtures for setup:**
```python
@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"
```

**Mocking dependencies:**
```python
from unittest.mock import patch

def test_api_call():
    with patch('module.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'status': 'ok'}
        result = fetch_data()
        assert result['status'] == 'ok'
```

**Parametrized tests:**
```python
@pytest.mark.parametrize("price,discount,expected", [
    (100, 20, 80),
    (100, 0, 100),
    (50, 10, 45),
])
def test_various_inputs(price, discount, expected):
    assert calculate_discount(price, discount) == expected
```

### Step 7: Write Test File

Create complete test file with:
- Module docstring
- Imports
- Fixtures (if needed)
- Test classes/functions organized logically
- Helpful comments

**Example structure:**
```python
"""Tests for calculator module."""
import pytest
from module import function_to_test

class TestFunctionName:
    """Test suite for function_to_test."""

    def test_happy_path(self):
        """Test normal expected behavior."""
        # Arrange
        input_data = ...
        # Act
        result = function_to_test(input_data)
        # Assert
        assert result == expected

    def test_edge_case(self):
        """Test with empty input."""
        assert function_to_test([]) == []

    def test_error_handling(self):
        """Test invalid input raises ValueError."""
        with pytest.raises(ValueError):
            function_to_test(invalid)
```

### Step 8: Add Documentation

Include:
- Module docstring with test coverage summary
- Run instructions: `pytest test_module.py`
- Individual test docstrings

## Best Practices

### Test Independence
Each test must be independent - no shared state between tests.

### Descriptive Names
`test_calculate_discount_raises_error_for_negative_input` not `test_1`

### Organize Tests
Group related tests in classes:
```python
class TestUserAuthentication:
    def test_login_success(self): ...
    def test_login_failure(self): ...
```

### Assertion Messages
Add helpful debug messages:
```python
assert len(result) == 5, f"Expected 5 items, got {len(result)}"
```

## Framework Templates

### pytest (Python)
```python
import pytest

def test_basic():
    assert function(input) == expected

@pytest.mark.parametrize("input,expected", [(1, 2), (2, 4)])
def test_parametrized(input, expected):
    assert function(input) == expected

def test_exception():
    with pytest.raises(ValueError):
        function(invalid)
```

### jest (JavaScript)
```javascript
describe('function', () => {
  test('basic functionality', () => {
    expect(function(input)).toBe(expected);
  });

  test('throws error', () => {
    expect(() => function(invalid)).toThrow(Error);
  });
});
```

## Advanced Patterns

For complex scenarios, see references:

- **Async/database/API testing**: See [test_patterns.md](references/test_patterns.md)
- **Framework-specific features**: See [framework_guides.md](references/framework_guides.md)
- **Mocking strategies**: See [mocking_guide.md](references/mocking_guide.md)

## Resources

### references/test_patterns.md
Comprehensive patterns for:
- Async code (asyncio, async/await)
- Database operations (fixtures, mocking)
- API endpoints (HTTP, Flask/FastAPI)
- File I/O (tmp_path, mocking)
- Time-dependent code (freezing time)
- CLI applications
- And more...

### references/framework_guides.md
Quick reference for pytest, unittest, jest features and configuration.

### references/mocking_guide.md
Strategies for mocking dependencies, external services, and complex scenarios.

## Skill Contract

**Stable:** 8-step workflow, AAA pattern, test case categories, framework selection
**Mutable:** Framework templates, test patterns, examples
**Update rules:** See `references/contract.md`

> Full contract in `references/contract.md`
