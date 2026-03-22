---
name: testing-patterns
description: Expert guidance on Python testing with pytest. Use when writing or reviewing tests requiring: (1) Pytest setup and configuration, (2) Unit tests with mocks and fixtures, (3) Integration testing workflows, (4) Async testing with pytest-asyncio, (5) Test coverage strategies (80%+ target), (6) TDD (Test-Driven Development) workflow. Invoke when user asks about testing patterns, writes tests, or needs test quality guidance.
---

# Testing Patterns

Expert guidance for writing effective Python tests with pytest.

## Quick Start

### Basic Test Structure

```python
import pytest
from src.services.task_manager import TaskManager

class TestTaskManager:
    """Group related tests in classes."""

    def test_create_task_with_valid_title(self) -> None:
        """Test names describe expected behavior."""
        manager = TaskManager(storage=InMemoryStorage())

        task = manager.create_task("Buy groceries")

        assert task.title == "Buy groceries"
        assert task.completed is False

    def test_create_task_raises_on_empty_title(self) -> None:
        """Test error conditions explicitly."""
        manager = TaskManager(storage=InMemoryStorage())

        with pytest.raises(ValidationError, match="Title cannot be empty"):
            manager.create_task("")
```

### Fixtures for Dependencies

```python
import pytest

@pytest.fixture
def storage() -> InMemoryStorage:
    """Create fresh storage for each test."""
    return InMemoryStorage()

@pytest.fixture
def task_manager(storage: InMemoryStorage) -> TaskManager:
    """Fixtures can depend on other fixtures."""
    return TaskManager(storage=storage)

def test_create_task(task_manager: TaskManager) -> None:
    task = task_manager.create_task("Test")
    assert task.id is not None
```

## Test Organization

### Directory Structure

```
tests/
├── conftest.py          # Shared fixtures
├── unit/                # Isolated unit tests
│   ├── conftest.py      # Unit-specific fixtures
│   ├── test_task_manager.py
│   └── test_storage.py
├── integration/         # Component integration
│   ├── conftest.py
│   └── test_agent_workflow.py
└── contract/            # API contract tests
    └── test_agent_contracts.py
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Test files | `test_*.py` | `test_task_manager.py` |
| Test classes | `Test*` | `TestTaskManager` |
| Test functions | `test_*` | `test_create_task_success` |
| Fixtures | descriptive noun | `task_manager`, `mock_storage` |

## Coverage Target: 80%+

```bash
# Run with coverage
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Generate HTML report
pytest --cov=src --cov-report=html
```

Coverage priorities:
1. Business logic (services, managers) - 90%+
2. Data models and validation - 85%+
3. Error handling paths - 80%+
4. Edge cases and boundaries - covered

## Reference Guides

For detailed patterns, see:

- **Pytest Setup**: See [references/pytest-setup.md](references/pytest-setup.md) for configuration, markers, and CLI options
- **Mocking Patterns**: See [references/mocking-patterns.md](references/mocking-patterns.md) for mocks, stubs, fakes, and dependency injection testing
- **Async Testing**: See [references/async-testing.md](references/async-testing.md) for pytest-asyncio patterns and async fixtures
- **TDD Workflow**: See [references/tdd-workflow.md](references/tdd-workflow.md) for Red-Green-Refactor cycle and best practices
- **Integration Testing**: See [references/integration-testing.md](references/integration-testing.md) for multi-component and workflow testing
