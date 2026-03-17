---
name: tdd-pytest
description: Python/pytest TDD specialist for test-driven development workflows. Use
  when writing tests, auditing test quality, running pytest, or generating test reports.
  Integrates with uv and pyproject.toml configuration.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# TDD-Pytest Skill

Activate this skill when the user needs help with:

- Writing tests using TDD methodology (Red-Green-Refactor)
- Auditing existing pytest test files for quality
- Running tests with coverage
- Generating test reports to `TESTING_REPORT.local.md`
- Setting up pytest configuration in `pyproject.toml`

## TDD Workflow

### Red-Green-Refactor Cycle

1. **RED** - Write a failing test first
   - Test should fail for the right reason (not import errors)
   - Test should be minimal and focused
   - Show the failing test output

2. **GREEN** - Write minimal code to pass
   - Only implement what's needed to pass the test
   - No premature optimization
   - Show the passing test output

3. **REFACTOR** - Improve code while keeping tests green
   - Clean up duplication
   - Improve naming
   - Extract functions/classes if needed
   - Run tests after each change

## Test Organization

### File Structure

```text
project/
  src/
    module.py
  tests/
    conftest.py          # Shared fixtures
    test_module.py       # Tests for module.py
  pyproject.toml         # Pytest configuration
```

### Naming Conventions

- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_*`
- Test classes: `Test*`
- Fixtures: Descriptive names (`mock_database`, `sample_user`)

## Pytest Best Practices

### Fixtures

```python
import pytest

@pytest.fixture
def sample_config():
    return {"key": "value"}

@pytest.fixture
def mock_client(mocker):
    return mocker.MagicMock()
```

### Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result == expected
```

### Exception Testing

```python
def test_raises_value_error():
    with pytest.raises(ValueError, match="invalid input"):
        process_input(None)
```

## Running Tests

### With uv

```bash
uv run pytest                              # Run all tests
uv run pytest tests/test_module.py         # Run specific file
uv run pytest -k "test_name"               # Run by name pattern
uv run pytest -v --tb=short                # Verbose with short traceback
uv run pytest --cov=src --cov-report=term  # With coverage
```

### Common Flags

- `-v` / `--verbose` - Detailed output
- `-x` / `--exitfirst` - Stop on first failure
- `--tb=short` - Short tracebacks
- `--tb=no` - No tracebacks
- `-k EXPR` - Run tests matching expression
- `-m MARKER` - Run tests with marker
- `--cov=PATH` - Coverage for path
- `--cov-report=term-missing` - Show missing lines

## pyproject.toml Configuration

### Minimal Setup

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### Full Configuration

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
fail_under = 80
show_missing = true
```

## Report Generation

The `TESTING_REPORT.local.md` file should contain:

1. Test execution summary (passed/failed/skipped)
2. Coverage metrics by module
3. Audit findings by severity
4. Recommendations with file:line references
5. Evidence (command outputs)

## Integration with Conversation

When the user asks to write tests:

1. Check conversation history for context about what to test
2. Identify the code/feature being discussed
3. If unclear, ask clarifying questions:
   - "What specific behavior should I test?"
   - "Should I include edge cases for X?"
   - "Do you want unit tests, integration tests, or both?"
4. Follow TDD: Write failing test first, then implement

## Commands Available

- `/tdd-pytest:init` - Initialize pytest configuration
- `/tdd-pytest:test [path]` - Write tests using TDD (context-aware)
- `/tdd-pytest:test-all` - Run all tests
- `/tdd-pytest:report` - Generate/update TESTING_REPORT.local.md
