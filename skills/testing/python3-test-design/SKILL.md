---
name: python3-test-design
description: 'This skill should be used when the user asks to "design a test strategy", "plan test coverage", "create test architecture", "review test structure", or mentions test planning patterns like TDD, BDD, or property-based testing. Provides guidance for pytest test suite architecture and design decisions.'
version: "1.0.0"
last_updated: "2026-01-25"
python_compatibility: "3.11+"
---

# Python Test Design Skill

Guidance for designing pytest test suites with modern Python 3.11+ patterns.

## When to Use This Skill

Use this skill for test **design** decisions:

- Planning test suite architecture
- Choosing testing strategies (unit, integration, e2e)
- Designing fixture hierarchies
- Determining coverage strategies
- Planning property-based testing approach

For test **implementation**, use the `python-pytest-architect` agent instead.

## Test Design Principles

### Test Pyramid

Structure test suites following the test pyramid:

```text
        /\
       /  \     E2E (few, slow, high confidence)
      /----\
     /      \   Integration (moderate, medium speed)
    /--------\
   /          \ Unit (many, fast, focused)
  /------------\
```

**Distribution targets:**

- Unit tests: 70-80% of test count
- Integration tests: 15-25% of test count
- E2E tests: 5-10% of test count

### Test Naming Convention

Use behavioral naming that describes what is being tested:

```python
# Pattern: test_{function}_{scenario}_{expected_result}

def test_validate_email_with_invalid_format_raises_validation_error():
    """Validate that malformed emails are rejected."""
    ...

def test_process_payment_when_insufficient_funds_returns_declined():
    """Payment processing declines when balance is insufficient."""
    ...
```

### AAA Pattern (Arrange-Act-Assert)

Structure every test with clear sections:

```python
def test_user_registration_creates_account():
    # Arrange
    user_data = {"email": "test@example.com", "name": "Test User"}
    repository = InMemoryUserRepository()
    service = UserService(repository)

    # Act
    result = service.register(user_data)

    # Assert
    assert result.success is True
    assert repository.count() == 1
```

## Test Strategy Selection

### When to Use Unit Tests

- Pure functions with no side effects
- Business logic validation
- Data transformation
- Algorithm correctness

### When to Use Integration Tests

- Database interactions
- External API calls
- File system operations
- Multi-component workflows

### When to Use Property-Based Tests

- Functions with mathematical properties (commutativity, associativity)
- Parsers and serializers (round-trip property)
- Data validation (valid inputs always accepted)
- State machines (invariants maintained)

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_maintains_length(data):
    """Sorting preserves all elements."""
    result = sorted(data)
    assert len(result) == len(data)
```

### When to Use BDD Tests

- User-facing features with acceptance criteria
- Requirements traceability needed
- Non-technical stakeholder visibility
- Complex user workflows

## Fixture Design

### Fixture Hierarchy

Organize fixtures by scope and purpose:

```text
conftest.py (root)
├── Session fixtures (db connections, servers)
├── Module fixtures (shared test data)
└── Function fixtures (isolated per-test data)

tests/
├── conftest.py              # Shared fixtures
├── unit/
│   └── conftest.py          # Unit-specific fixtures
└── integration/
    └── conftest.py          # Integration-specific fixtures
```

### Factory Pattern for Test Data

Use factories for complex test objects:

```python
import factory
from datetime import datetime, UTC

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    email = factory.LazyAttribute(lambda o: f"user{o.id}@example.com")
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))
```

## Coverage Strategy

### Minimum Coverage Requirements

| Code Type         | Minimum Coverage       |
| ----------------- | ---------------------- |
| Business logic    | 90%                    |
| Standard code     | 80%                    |
| Scripts/utilities | 70%                    |
| Critical paths    | 95% + mutation testing |

### Coverage Configuration

```toml
# pyproject.toml
[tool.coverage.run]
branch = true
source = ["packages"]
omit = ["**/tests/**", "**/__pycache__/**"]

[tool.coverage.report]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

## Mutation Testing for Critical Code

Apply mutation testing to security-critical and payment-related code:

```bash
# Run mutation tests on auth module
uv run mutmut run --paths-to-mutate=packages/auth/

# View surviving mutants
uv run mutmut results
```

**Target: >90% mutation score for critical code paths**

## Test Directory Structure

```text
tests/
├── conftest.py              # Shared fixtures, pytest plugins
├── unit/                    # Fast, isolated tests
│   ├── test_validators.py
│   └── test_models.py
├── integration/             # Tests with external dependencies
│   ├── test_database.py
│   └── test_api_client.py
├── e2e/                     # End-to-end workflows
│   └── test_user_flows.py
├── fixtures/                # Test data files
│   ├── sample_config.yaml
│   └── test_data.json
└── conftest.py              # Root-level configuration
```

## Related Resources

- **Agent**: Use `python-pytest-architect` for test implementation
- **Skill**: `python3-development` for general Python patterns
- **Command**: `/modernpython` for modern Python syntax reference
