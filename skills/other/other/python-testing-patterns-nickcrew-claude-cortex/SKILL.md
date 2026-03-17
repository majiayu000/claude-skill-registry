---
name: python-testing-patterns
description: Python testing patterns and best practices using pytest, mocking, and property-based testing. Use when writing unit tests, integration tests, or implementing test-driven development in Python projects.
---

# Python Testing Patterns

Comprehensive guide to implementing robust testing strategies in Python using pytest, fixtures, mocking, parameterization, and property-based testing.

## When to Use This Skill

- Writing unit tests for Python functions and classes
- Setting up comprehensive test suites and infrastructure
- Implementing test-driven development (TDD) workflows
- Creating integration tests for APIs, databases, and services
- Mocking external dependencies and third-party services
- Testing async code and concurrent operations
- Implementing property-based testing with Hypothesis
- Setting up CI/CD test automation
- Debugging failing tests and improving test coverage

## Core Concepts

**Test Discovery**: Files matching `test_*.py` or `*_test.py`, functions starting with `test_`

**Fixtures**: Reusable test resources with setup and teardown
- Scopes: `function` (default), `class`, `module`, `session`
- Composition: Build complex fixtures from simple ones
- Share via `conftest.py` for project-wide availability

**Assertions**: Use `assert` statements, `pytest.raises()` for exceptions

**Organization**: Separate `unit/`, `integration/`, `e2e/` directories

## Quick Reference

Load detailed references for specific topics:

| Task | Reference File |
|------|----------------|
| Pytest basics, test structure, AAA pattern | `skills/python-testing-patterns/references/pytest-fundamentals.md` |
| Fixtures, scopes, setup/teardown, conftest.py | `skills/python-testing-patterns/references/fixtures.md` |
| Parametrization, multiple test cases | `skills/python-testing-patterns/references/parametrized-tests.md` |
| Mocking, patching, unittest.mock, pytest-mock | `skills/python-testing-patterns/references/mocking.md` |
| Async tests, pytest-asyncio, event loops | `skills/python-testing-patterns/references/async-testing.md` |
| Property-based testing, Hypothesis, strategies | `skills/python-testing-patterns/references/property-based-testing.md` |
| Monkeypatch, environment variables, attributes | `skills/python-testing-patterns/references/monkeypatch.md` |
| Test structure, markers, conftest.py patterns | `skills/python-testing-patterns/references/test-organization.md` |
| Coverage measurement, reports, thresholds | `skills/python-testing-patterns/references/coverage.md` |
| Database, API, Redis, message queue testing | `skills/python-testing-patterns/references/integration-testing.md` |
| Best practices, test quality, fixture design | `skills/python-testing-patterns/references/best-practices.md` |

## Workflow

### 1. Basic Test Setup
```python
# test_example.py
import pytest

def test_something():
    """Descriptive test name."""
    # Arrange
    expected = 5

    # Act
    result = 2 + 3

    # Assert
    assert result == expected
```

**Run tests:**
```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/unit/        # Specific directory
pytest -k "test_user"     # Match pattern
pytest -m unit            # Run marked tests
```

### 2. Using Fixtures
```python
@pytest.fixture
def sample_data():
    """Provide test data."""
    data = {"key": "value"}
    yield data
    # Cleanup if needed

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"
```

### 3. Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

### 4. Mocking External Dependencies
```python
from unittest.mock import patch

@patch("module.external_api_call")
def test_with_mock(mock_api):
    mock_api.return_value = {"status": "ok"}

    result = my_function()

    assert result["status"] == "ok"
    mock_api.assert_called_once()
```

### 5. Coverage Measurement
```bash
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-report=html
pytest --cov=src --cov-fail-under=80
```

### 6. Test Configuration
**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --strict-markers --cov=src
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
```

## Common Patterns

**Exception testing:**
```python
with pytest.raises(ValueError, match="error message"):
    function_that_raises()
```

**Async testing:**
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result is not None
```

**Temporary files:**
```python
def test_file_operation(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    assert test_file.read_text() == "content"
```

**Markers for test selection:**
```python
@pytest.mark.slow
@pytest.mark.integration
def test_database_operation():
    pass
```

## Common Mistakes

1. **Not using fixtures**: Repeating setup code across tests
   - Solution: Create fixtures in conftest.py

2. **Tests depending on order**: Global state pollution
   - Solution: Ensure test independence with proper fixtures

3. **Over-mocking**: Mocking internal implementation
   - Solution: Mock only external boundaries (APIs, databases)

4. **Missing edge cases**: Only testing happy path
   - Solution: Test boundary conditions, errors, and invalid inputs

5. **Slow tests**: Running full integration tests frequently
   - Solution: Separate unit/integration, use markers, optimize fixtures

6. **Ignoring coverage gaps**: Not measuring test coverage
   - Solution: Use pytest-cov and track metrics

7. **Poor test names**: Generic names like `test_1()`
   - Solution: Use descriptive names: `test_<behavior>_<condition>_<expected>`

8. **No cleanup**: Resources not released
   - Solution: Use fixtures with proper teardown (yield pattern)

## Resources

- **pytest**: https://docs.pytest.org/
- **unittest.mock**: https://docs.python.org/3/library/unittest.mock.html
- **pytest-asyncio**: Testing async code
- **pytest-cov**: Coverage reporting
- **pytest-mock**: pytest wrapper for mock
- **Hypothesis**: https://hypothesis.readthedocs.io/
- **pytest-xdist**: Parallel test execution
- **testcontainers**: Docker containers for testing
