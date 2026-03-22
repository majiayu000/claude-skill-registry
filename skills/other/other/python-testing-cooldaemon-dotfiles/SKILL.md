---
name: python-testing
description: pytest testing policies for Python projects. Use when writing or reviewing Python test code. Do NOT use for application code -- use python-patterns instead.
durability: encoded-preference
---

# Python Testing Policies

## Project Structure

```
project/
├── mypackage/
├── tests/
│   ├── conftest.py       # Shared fixtures
│   ├── test_module.py
│   └── integration/
└── pyproject.toml
```

## Test Naming

```python
# Pattern: test_<action>_<condition/scenario>
def test_create_user_with_valid_input(): ...
def test_create_user_raises_when_email_invalid(): ...
```

## Fixture Policies

### Scope Selection

| Scope | Use When |
|-------|----------|
| `function` (default) | Independent per test |
| `class` | Shared within test class |
| `module` | Expensive setup, tests don't mutate |
| `session` | DB connections, containers |

### Always Use yield for Cleanup

```python
@pytest.fixture
def db():
    database = Database(":memory:")
    yield database
    database.close()  # Cleanup guaranteed
```

## Parametrize Policies

### Use IDs for Clarity

```python
@pytest.mark.parametrize("input,expected", [
    pytest.param("hello", "HELLO", id="lowercase"),
    pytest.param("", "", id="empty-string"),
])
def test_uppercase(input, expected): ...
```

### Prefer parametrize Over Duplicate Tests

```python
# BAD: Duplicate tests
def test_add_positive(): assert add(2, 3) == 5
def test_add_negative(): assert add(-1, -2) == -3

# GOOD: Parametrize
@pytest.mark.parametrize("a,b,expected", [(2,3,5), (-1,-2,-3)])
def test_add(a, b, expected): assert add(a, b) == expected
```

## Coverage Targets

| Code Type | Target |
|-----------|--------|
| Business logic | 80%+ |
| Public APIs | 90%+ |
| Generated code | Exclude |

```toml
# pyproject.toml
[tool.coverage.report]
fail_under = 80
```

## Commands

**See `makefile-first` skill** for command execution policy.

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| `time.sleep()` in tests | Use mocks or async waiting |
| Shared mutable state | Isolated fixtures per test |
| Ignoring flaky tests | Fix or remove immediately |
