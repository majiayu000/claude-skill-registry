---
name: test-writing
description: Defines patterns for writing tests, including subsection tests for incremental development and acceptance criteria verification. Use when writing any tests to ensure consistent naming, structure, and coverage patterns.
license: MIT
metadata:
  version: "1.0.0"
  framework: "pytest"
  conventions: "subsection tests, AC verification, type annotations"
---

# Test Writing Pattern

This skill defines how to write tests following established patterns and best practices.

## Test Structure

### File Organization

- Unit tests: `tests/unit/<module>/test_<component>.py`
- Integration tests: `tests/integration/test_<feature>.py`
- API tests: `tests/integration/api/test_api_<endpoint>.py`

### Test Class Structure

```python
"""Tests for <component>: <description>.

Tests verify:
- <key requirement 1>
- <key requirement 2>
- <key requirement 3>
"""

import pytest
from <appropriate imports>

@pytest.fixture
def <fixture_name>():
    """Fixture description."""
    # Setup
    yield <value>
    # Cleanup (if needed)


class Test<ComponentName>:
    """Test <component>: <description>."""

    def test_feature_description(self, fixture) -> None:
        """Test specific feature requirement."""
        # Arrange
        # Act
        # Assert
```

## Naming Conventions

### Subsection Tests

For incremental development during phase implementation:

```python
def test_subsection_X_Y_Z_requirement_description(self) -> None:
    """Test subsection X.Y.Z requirement."""
```

Examples:
- `test_subsection_1_2_3_validates_input_bounds`
- `test_subsection_2_1_1_returns_200_with_healthy_status`
- `test_subsection_3_2_1_enforces_timeout`

### Acceptance Criteria Tests

For official verification (AC-X.Y.Z format):

```python
def test_ac_X_Y_Z_requirement_description(self) -> None:
    """Test AC-X.Y.Z: requirement description."""
```

Examples:
- `test_ac_2_1_1_returns_200_with_health_status`
- `test_ac_3_2_1_response_completes_within_100ms`

### General Tests

For other test cases:

```python
def test_feature_description(self) -> None:
    """Test that feature works correctly."""
```

## Type Annotations

**Always** include return type annotations:

```python
def test_something(self) -> None:
    """Test description."""
    pass
```

## Test Patterns

### Unit Tests

Test individual components in isolation:

```python
def test_component_behavior(self) -> None:
    """Test component does X."""
    # Create component
    component = Component()

    # Call method
    result = component.method()

    # Assert behavior
    assert result.expected_property == expected_value
```

### Integration Tests

Test interactions between components:

```python
@pytest.fixture
def service():
    """Create service for testing."""
    return Service()

def test_service_pipeline_integration(self, service) -> None:
    """Test full service pipeline."""
    # Set up test data
    test_data = create_test_data()

    # Run pipeline
    result = service.process(test_data)

    # Verify result
    assert result.success is True
    assert result.data is not None
```

### API Tests

Test FastAPI endpoints:

```python
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

def test_get_endpoint_returns_200(self, client: TestClient) -> None:
    """Test GET endpoint returns 200."""
    response = client.get("/endpoint")

    assert response.status_code == 200
    data = response.json()
    assert data["expected_field"] == expected_value
```

## Assertion Patterns

### Success Cases

```python
assert result.success is True
assert result.data is not None
assert result.data.expected_property == expected_value
```

### Error Cases

```python
assert result.success is False
assert result.error_code == "E_ERROR_CODE"
assert result.error_message is not None
```

### Status Codes

```python
assert response.status_code == 200  # Success
assert response.status_code == 400  # Bad Request
assert response.status_code == 404  # Not Found
assert response.status_code == 500  # Internal Error
assert response.status_code == 503  # Service Unavailable
```

## Fixtures

### Common Fixtures

```python
@pytest.fixture
def sample_data():
    """Create sample test data."""
    return {
        "id": "test-id",
        "name": "Test Item",
        "status": "active"
    }

@pytest.fixture
def service():
    """Create service instance."""
    return Service()
```

### Autouse Fixtures

For setup/teardown needed for all tests:

```python
@pytest.fixture(autouse=True)
def reset_state():
    """Reset state before each test."""
    # Setup
    yield
    # Cleanup
```

## Test Coverage Requirements

### Core Business Logic

- **Target**: 100% coverage
- Test all validators
- Test all edge cases
- Test model creation and serialization
- Test state transitions

### Service Layer

- **Target**: ≥90% coverage
- Test each service in isolation
- Test service integration
- Test timeout mechanisms
- Test error handling

### API Endpoints

- **Target**: ≥80% coverage
- Test all endpoints
- Test success and error cases
- Test request/response models
- Test error code mapping

### UI Components

- **Target**: ≥70% coverage
- Test component rendering
- Test user interactions
- Test state management
- Test error boundaries

## Best Practices

1. **Descriptive names**: Test names should clearly describe what is tested
2. **One assertion per concept**: Group related assertions, but test one concept per test
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Use fixtures**: Avoid code duplication with fixtures
5. **Test edge cases**: Include boundary conditions and error cases
6. **Test independently**: Tests should not depend on execution order
7. **Verify acceptance criteria**: Ensure AC-X.Y.Z requirements are met

## Common Edge Cases

### Testing Error Codes

```python
def test_returns_correct_error_code(self) -> None:
    """Test returns correct error code."""
    result = component.method(invalid_input)

    assert result.success is False
    assert result.error_code == "E_ERROR_CODE"
```

### Testing Timeouts

```python
def test_enforces_timeout(self) -> None:
    """Test timeout is enforced."""
    start_time = time.time()
    result = slow_operation()
    elapsed_time = time.time() - start_time

    assert result.error_code == "E_TIMEOUT"
    # Note: Don't assert exact timing, just that timeout occurred
```

### Testing State Changes

```python
def test_updates_state_correctly(self) -> None:
    """Test state is updated correctly."""
    initial_state = get_state()

    operation()

    updated_state = get_state()
    assert updated_state.property != initial_state.property
```
