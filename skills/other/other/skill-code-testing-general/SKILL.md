---
name: code-testing
description: Generate and run unit and integration tests using pytest (Python) or Jest (JavaScript) with fixtures, mocks, and async support. Use for test-driven development, code review validation, coverage verification, and regression testing. Target 80%+ code coverage. Supports pytest markers, Jest snapshots, and CI/CD integration. Triggers on "test", "TDD", "unit test", "integration test", "test coverage", "pytest", "jest".
---

# Code Testing

## Purpose

Generate and run comprehensive unit and integration tests following TDD principles with proper fixtures, mocking, and coverage measurement.

## When to Use

- Test-driven development (TDD)
- Code review validation
- Coverage verification
- Regression testing
- CI/CD pipeline integration
- Ensuring code quality

## Core Instructions

### Python Unit Test (pytest)

```python
import pytest
from my_module import calculate_total

@pytest.fixture
def sample_data():
    """Fixture providing test data"""
    return {
        "items": [
            {"price": 10.0, "quantity": 2},
            {"price": 5.0, "quantity": 3}
        ]
    }

def test_calculate_total(sample_data):
    """Test total calculation"""
    result = calculate_total(sample_data["items"])
    assert result == 35.0

def test_calculate_total_empty():
    """Test with empty list"""
    result = calculate_total([])
    assert result == 0.0

@pytest.mark.asyncio
async def test_async_function():
    """Test async operations"""
    result = await fetch_data()
    assert result is not None
    assert "id" in result
```

### JavaScript Test (Jest)

```javascript
import { render, screen } from '@testing-library/react';
import { calculateTotal } from './utils';
import Component from './Component';

describe('calculateTotal', () => {
  test('calculates total correctly', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 }
    ];
    expect(calculateTotal(items)).toBe(35);
  });

  test('handles empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
});

describe('Component', () => {
  test('renders correctly', () => {
    render(<Component />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });

  test('handles async data', async () => {
    render(<Component />);
    const data = await screen.findByTestId('data');
    expect(data).toHaveTextContent('Loaded');
  });
});
```

### Mocking External Dependencies

**Python (unittest.mock):**
```python
from unittest.mock import Mock, patch

@patch('my_module.external_api_call')
def test_with_mock(mock_api):
    """Mock external API"""
    mock_api.return_value = {"status": "success"}

    result = my_function()

    assert result["status"] == "success"
    mock_api.assert_called_once()
```

**JavaScript (Jest):**
```javascript
jest.mock('./api', () => ({
  fetchData: jest.fn()
}));

import { fetchData } from './api';

test('mocks API call', async () => {
  fetchData.mockResolvedValue({ status: 'success' });

  const result = await myFunction();

  expect(result.status).toBe('success');
  expect(fetchData).toHaveBeenCalledTimes(1);
});
```

## TDD Workflow (Red-Green-Refactor)

### 1. RED: Write Failing Test

```python
def test_new_feature():
    """Test for feature that doesn't exist yet"""
    result = new_feature(input_data)
    assert result == expected_output
```

Run test: `pytest` → ❌ FAILS (feature not implemented)

### 2. GREEN: Implement Minimum Code

```python
def new_feature(input_data):
    """Minimal implementation to pass test"""
    return expected_output
```

Run test: `pytest` → ✅ PASSES

### 3. REFACTOR: Improve Code

```python
def new_feature(input_data):
    """Refactored implementation"""
    # Clean, efficient implementation
    return process(input_data)
```

Run test: `pytest` → ✅ STILL PASSES

## Coverage Measurement

### Python (pytest-cov)

```bash
# Run tests with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Generate HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80
```

### JavaScript (Jest)

```bash
# Run tests with coverage
npm test -- --coverage

# Coverage thresholds in jest.config.js
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

## Best Practices

### Structure Tests (AAA Pattern)

```python
def test_user_creation():
    # ARRANGE: Setup test data
    user_data = {"name": "John", "email": "john@example.com"}

    # ACT: Execute the function
    user = create_user(user_data)

    # ASSERT: Verify results
    assert user.name == "John"
    assert user.email == "john@example.com"
    assert user.id is not None
```

### Use Descriptive Names

```python
# Good
def test_calculate_total_with_discount_applied():
    pass

# Bad
def test_calc():
    pass
```

### Test Edge Cases

```python
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_empty_input():
    result = process([])
    assert result == []

def test_null_input():
    result = process(None)
    assert result is None
```

### Use Fixtures for Setup

```python
@pytest.fixture
def database():
    """Setup test database"""
    db = create_test_db()
    yield db
    db.cleanup()

def test_with_db(database):
    user = database.create_user("test")
    assert user.name == "test"
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run tests
  run: |
    pytest tests/ --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

### Output Formats

**JUnit XML (for CI):**
```bash
pytest --junitxml=test-results.xml
```

**JSON (for parsing):**
```bash
pytest --json-report --json-report-file=report.json
```

## Performance Testing

```python
import pytest
import time

@pytest.mark.benchmark
def test_performance(benchmark):
    """Benchmark function performance"""
    result = benchmark(expensive_function, large_input)
    assert result is not None

@pytest.mark.timeout(5)
def test_timeout():
    """Test must complete within 5 seconds"""
    result = slow_function()
    assert result is not None
```

## Dependencies

**Python:**
- `pytest` - Test framework
- `pytest-cov` - Coverage plugin
- `pytest-asyncio` - Async test support
- `pytest-mock` - Mocking utilities

**JavaScript:**
- `jest` - Test framework
- `@testing-library/react` - React testing
- `@testing-library/jest-dom` - Custom matchers

## Version

v1.0.0 (2025-10-23)

