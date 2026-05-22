---
name: setup-pytest-fixtures
description: |
  Create pytest fixtures following project patterns including factory fixtures,
  async fixtures, and multi-layer organization. Use when setting up test fixtures,
  creating test data, organizing test utilities, or structuring conftest.py files.
  Works with Python test files, pytest configuration, and .py test utilities.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Setup Pytest Fixtures

## Purpose

Creates pytest fixtures following project-watch-mcp patterns: factory fixtures for customization, async fixtures for async code, centralized organization in tests/utils/, and proper conftest.py hierarchy.

## Quick Start

**Create a basic fixture:**
```python
import pytest

@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    settings = MagicMock()
    settings.project = MagicMock()
    settings.project.project_name = "test_project"
    return settings
```

**Create a factory fixture:**
```python
@pytest.fixture
def mock_settings_factory():
    """Factory for custom mock settings."""
    def create_settings(**kwargs):
        settings = MagicMock()
        settings.project = MagicMock()
        settings.project.project_name = kwargs.get("project_name", "test_project")
        return settings
    return create_settings
```

## Instructions

### Step 1: Identify Fixture Type

Determine which fixture pattern to use:

1. **Basic Fixture**: Simple, reusable test data
   - Use for: Constant values, simple mocks
   - Example: `mock_settings_minimal`

2. **Factory Fixture**: Customizable with parameters
   - Use for: Configurable test data, parameterized tests
   - Example: `mock_settings_factory(**kwargs)`

3. **Async Fixture**: For async operations
   - Use for: Async setup/teardown, async resources
   - Example: `@pytest_asyncio.fixture async def...`

4. **Scoped Fixture**: Shared across multiple tests
   - Use for: Expensive setup, session-wide resources
   - Example: `@pytest.fixture(scope="session")`

### Step 2: Choose Organization Strategy

**Centralized Utilities** (Recommended for reusable fixtures):
- Location: `tests/utils/`
- Files: `mock_settings.py`, `mock_services.py`, `mock_drivers.py`, `environmental_helpers.py`
- Import in: `tests/conftest.py` to make available project-wide

**Local Conftest** (For layer-specific fixtures):
- Location: `tests/unit/conftest.py`, `tests/integration/conftest.py`, `tests/e2e/conftest.py`
- Use for: Fixtures specific to that test layer

**Test File** (For test-specific fixtures):
- Location: Same file as tests
- Use for: One-off fixtures not reused elsewhere

### Step 3: Implement Fixture

**For Basic Fixtures:**
```python
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def fixture_name():
    """Clear docstring explaining purpose."""
    # Setup
    obj = MagicMock()
    obj.attribute = "value"

    # Return (no yield for simple fixtures)
    return obj
```

**For Factory Fixtures:**
```python
@pytest.fixture
def fixture_factory():
    """Factory for custom fixture."""
    def create_fixture(**kwargs):
        """Create fixture with custom attributes.

        Args:
            **kwargs: Attributes to customize

        Returns:
            MagicMock: Configured fixture
        """
        obj = MagicMock()
        obj.attribute = kwargs.get("attribute", "default_value")
        return obj
    return create_fixture
```

**For Async Fixtures:**
```python
import pytest_asyncio
from collections.abc import AsyncGenerator

@pytest_asyncio.fixture(scope="function")
async def async_fixture() -> AsyncGenerator[Resource, None]:
    """Async fixture with setup and teardown."""
    # Setup
    resource = await create_resource()

    yield resource

    # Teardown
    await resource.close()
```

**For Scoped Fixtures:**
```python
@pytest.fixture(scope="session")
def session_fixture():
    """Session-scoped fixture created once."""
    # Expensive setup
    resource = expensive_setup()

    yield resource

    # Cleanup after all tests
    resource.cleanup()
```

### Step 4: Add to Conftest Hierarchy

**In `tests/utils/mock_*.py`:**
```python
"""Reusable mock fixtures for [component] components."""
from unittest.mock import MagicMock
import pytest

@pytest.fixture
def fixture_name():
    """Fixture docstring."""
    return MagicMock()
```

**In `tests/conftest.py`:**
```python
# Import to make available project-wide
from tests.utils.mock_settings import (
    fixture_name,
)

__all__ = [
    "fixture_name",
]
```

**In layer-specific conftest:**
```python
# tests/unit/conftest.py
import pytest

@pytest.fixture
def unit_specific_fixture():
    """Fixture only for unit tests."""
    return MagicMock()
```

### Step 5: Use Fixtures in Tests

**Basic usage:**
```python
def test_something(fixture_name):
    """Test using fixture."""
    assert fixture_name.attribute == "value"
```

**Factory usage:**
```python
def test_with_factory(fixture_factory):
    """Test using factory fixture."""
    custom = fixture_factory(attribute="custom_value")
    assert custom.attribute == "custom_value"
```

**Async usage:**
```python
@pytest.mark.asyncio
async def test_async(async_fixture):
    """Test using async fixture."""
    result = await async_fixture.operation()
    assert result == expected
```

**Multiple fixtures:**
```python
def test_with_multiple(fixture_one, fixture_two, fixture_factory):
    """Test using multiple fixtures."""
    custom = fixture_factory(value="test")
    assert fixture_one.works_with(fixture_two, custom)
```

## Examples

### Example 1: Basic Mock Fixture

```python
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_settings_minimal():
    """Create minimal mock settings for basic testing."""
    settings = MagicMock()
    settings.project = MagicMock()
    settings.project.project_name = "test_project"
    settings.neo4j = MagicMock()
    settings.neo4j.database_name = "test_db"
    return settings
```

### Example 2: Factory Fixture

```python
@pytest.fixture
def mock_settings_factory():
    """Factory for custom mock settings."""
    def create_settings(**kwargs):
        settings = MagicMock()
        settings.project = MagicMock()
        settings.project.project_name = kwargs.get("project_name", "test_project")
        settings.neo4j = MagicMock()
        settings.neo4j.database_name = kwargs.get("database_name", "test_db")
        settings.chunking = MagicMock()
        settings.chunking.chunk_size = kwargs.get("chunk_size", 50)
        return settings
    return create_settings
```

### Example 3: Async Fixture with Cleanup

```python
import pytest_asyncio
from collections.abc import AsyncGenerator
from neo4j import AsyncGraphDatabase, AsyncDriver

@pytest_asyncio.fixture(scope="function")
async def real_neo4j_driver() -> AsyncGenerator[AsyncDriver, None]:
    """Create a real Neo4j driver with cleanup."""
    driver = AsyncGraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "password")
    )

    # Setup: Clear test data
    async with driver.session(database="test_db") as session:
        await session.run("MATCH (n {project_name: 'test_project'}) DETACH DELETE n")

    yield driver

    # Teardown: Close driver
    await driver.close()
```

**Script Files:**
- [scripts/generate_fixture.py](./scripts/generate_fixture.py) - Auto-generate pytest fixtures following project patterns
- [scripts/analyze_fixture_usage.py](./scripts/analyze_fixture_usage.py) - Analyze pytest fixture usage and find optimization opportunities
- [scripts/organize_fixtures.py](./scripts/organize_fixtures.py) - Reorganize fixtures by layer and update imports

## Requirements

- pytest installed: `uv pip install pytest`
- pytest-asyncio for async fixtures: `uv pip install pytest-asyncio`
- Understanding of project structure:
  - `tests/utils/` - Centralized reusable fixtures
  - `tests/conftest.py` - Project-wide fixture imports
  - `tests/unit/conftest.py` - Unit test specific fixtures
  - `tests/integration/conftest.py` - Integration test specific fixtures
  - `tests/e2e/conftest.py` - E2E test specific fixtures

## Fixture Best Practices

1. **Naming**: Use descriptive names with `mock_` prefix for mocks
2. **Docstrings**: Always document what the fixture provides
3. **Scope**: Default to `function` scope, use `session`/`module` only when needed
4. **Cleanup**: Use `yield` for fixtures that need teardown
5. **Factory Pattern**: Return callable for customizable fixtures
6. **Type Hints**: Add return type hints for better IDE support
7. **Reusability**: Place reusable fixtures in `tests/utils/`, import in `conftest.py`
8. **Layer Isolation**: Keep layer-specific fixtures in layer conftest files

## Common Patterns

**Settings Mock:**
```python
@pytest.fixture
def mock_settings():
    """Standard settings mock."""
    settings = MagicMock()
    settings.project = MagicMock()
    settings.neo4j = MagicMock()
    return settings
```

**Service Result Mock:**
```python
@pytest.fixture
def mock_service_result():
    """Factory for ServiceResult mocks."""
    def create_result(success=True, data=None, error=None):
        result = MagicMock()
        result.is_success = success
        result.data = data
        result.error = error
        return result
    return create_result
```

**Async Service Mock:**
```python
@pytest.fixture
def mock_embedding_service():
    """Async embedding service mock."""
    service = AsyncMock()
    service.generate_embeddings = AsyncMock(
        return_value=MagicMock(success=True, data=[[0.1] * 384])
    )
    return service
```

## Troubleshooting

**Fixture not found:**
- Check it's imported in `tests/conftest.py`
- Verify file is in Python path
- Ensure `__all__` includes fixture name

**Async fixture errors:**
- Install `pytest-asyncio`: `uv pip install pytest-asyncio`
- Use `@pytest_asyncio.fixture` not `@pytest.fixture`
- Mark test with `@pytest.mark.asyncio`

**Scope issues:**
- Session fixtures can't use function fixtures
- Use broader scope for dependent fixtures
- Consider fixture dependencies carefully

**Cleanup not running:**
- Use `yield` not `return`
- Ensure async cleanup uses `await`
- Check for exceptions during test

## Automation Scripts

**NEW:** Powerful automation utilities for fixture management:

### [scripts/generate_fixture.py](./scripts/generate_fixture.py)
Auto-generate fixtures with proper patterns:
```bash
python .claude/skills/setup-pytest-fixtures/scripts/generate_fixture.py \
  --name mock_service --type factory --attributes host,port,timeout
```

### [scripts/analyze_fixture_usage.py](./scripts/analyze_fixture_usage.py)
Analyze fixture usage and find optimization opportunities:
```bash
python .claude/skills/setup-pytest-fixtures/scripts/analyze_fixture_usage.py --unused
```

### [scripts/organize_fixtures.py](./scripts/organize_fixtures.py)
Reorganize fixtures by layer and update imports:
```bash
python .claude/skills/setup-pytest-fixtures/scripts/organize_fixtures.py --validate
```

## See Also

- [templates/fixture-templates.md](./templates/fixture-templates.md) - Copy-paste templates
- `tests/utils/mock_settings.py` - Settings fixture reference
- `tests/utils/mock_services.py` - Service fixture reference
- `tests/utils/mock_drivers.py` - Driver fixture reference
- `tests/utils/environmental_helpers.py` - Environment fixture reference
