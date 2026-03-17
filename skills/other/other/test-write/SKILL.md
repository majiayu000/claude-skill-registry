---
name: test:write
description: Write E2E and unit tests following Kagenti testing standards
---

# Write Tests

Write tests that follow Kagenti testing standards.

## When to Use

- Adding a new feature that needs tests
- Fixing a bug (write regression test first)
- Improving test coverage for existing code

## Test Structure

```
kagenti/tests/
├── e2e/
│   ├── common/          # Tests that run on all platforms
│   │   ├── test_agent_*.py
│   │   ├── test_mlflow_*.py
│   │   └── conftest.py
│   ├── conftest.py      # Shared fixtures
│   └── test_*.py        # Platform-specific tests
└── requirements.txt
```

## Test Template

```python
"""Test description - what scenario is being validated."""
import pytest


class TestFeatureName:
    """Tests for [feature] functionality."""

    def test_specific_behavior(self, fixture):
        """Verify [specific behavior] when [condition]."""
        # Arrange
        expected = "specific_value"

        # Act
        result = do_something(fixture)

        # Assert - ALWAYS assert specific values
        assert result.status_code == 200, f"Expected 200, got {result.status_code}"
        assert result.json()["key"] == expected
```

## Standards

1. **One assertion per concept** — test one thing per test method
2. **Descriptive names** — `test_agent_returns_weather_for_valid_city`
3. **AAA pattern** — Arrange, Act, Assert
4. **Specific assertions** — `assert x == 42` not `assert x`
5. **Timeout handling** — use `pytest.mark.timeout(300)` not `sleep()`
6. **Skip with reason** — `@pytest.mark.skip(reason="MLflow disabled in Kind")`

## Fixtures (conftest.py)

Key fixtures available:

```python
@pytest.fixture
def agent_url():
    """Agent URL from env or port-forward."""

@pytest.fixture
def kubeconfig():
    """KUBECONFIG path."""

@pytest.fixture
def kagenti_config():
    """Platform config from KAGENTI_CONFIG_FILE."""
```

## After Writing

1. Run `test:review` to verify quality
2. Run `test:run-kind` or `test:run-hypershift` to execute
3. Use `git:commit` to commit

## Related Skills

- `test:review` - Review test quality before committing
- `test:run-kind` - Run on Kind cluster
- `test:run-hypershift` - Run on HyperShift cluster
- `tdd:ci` - Full TDD workflow
