---
name: generate-test
description: Generates test files following TDD patterns with Given-When-Then structure. Use when creating tests for domain logic, API endpoints, or repositories.
allowed-tools: Read, Write, Glob, Grep
---

# Generate Tests

Creates test files following the project's TDD conventions.

## Test Naming Convention

**Mandatory format**:
```python
def test_when_<condition>_then_<expected_outcome>():
```

**Examples**:
```python
def test_when_item_already_exists_then_raise_ItemAlreadyExistsException():
def test_when_item_does_not_exist_then_create_item():
def test_when_user_not_authenticated_then_return_401():
def test_when_valid_request_then_return_created_item():
```

## Test Structure

Use Given-When-Then structure **without comments**:

```python
def test_when_item_already_exists_then_raise_ItemAlreadyExistsException(
    item_repository: IItemRepository,
):
    # Given - setup
    item_db = ItemDb(id=uuid.uuid4(), user_id=user_id, name="Test", description="Desc")
    item_repository.create(item_db)

    # When/Then - action and assertion
    with pytest.raises(ItemAlreadyExistsException):
        create_item(user_id, "Test", "Another desc", item_repository)
```

## Test File Location

Mirror the source structure:
```
back/src/api/{module}/domain/create_item.py
back/tests/api/{module}/domain/test_create_item.py

back/src/api/{module}/infrastructure/repository.py
back/tests/api/{module}/infrastructure/test_{entity}_repository.py
```

## Domain Test Template

```python
import uuid

import pytest
from freezegun import freeze_time

from src.api.{module}.domain.{action} import {action_function}
from src.api.{module}.domain.exception import {Entity}NotFoundException, {Entity}AlreadyExistsException
from src.api.{module}.infrastructure.models import {Entity}Db
from src.api.{module}.infrastructure.repository import I{Entity}Repository

user_id = "test_user_123"


def test_when_{condition}_then_{outcome}(
    {entity}_repository: I{Entity}Repository,
):
    {entity}_db = {Entity}Db(id=uuid.uuid4(), user_id=user_id, name="Test", description="Desc")
    {entity}_repository.create({entity}_db)

    with pytest.raises({Entity}AlreadyExistsException):
        {action_function}(user_id, "Test", "Another desc", {entity}_repository)


@freeze_time("2023-01-01 00:00:00", tz_offset=0)
def test_when_{condition}_then_{outcome}(
    {entity}_repository: I{Entity}Repository,
    frozen_datetime,
):
    {entity}_db = {action_function}(user_id, "Test", "Description", {entity}_repository)

    assert {entity}_db.user_id == user_id
    assert {entity}_db.name == "Test"
    assert {entity}_db.created_at == frozen_datetime
```

## Common Fixtures

Available in `back/tests/conftest.py`:

```python
@pytest.fixture
def session():
    """Database session for tests."""

@pytest.fixture
def client(session):
    """FastAPI test client."""

@pytest.fixture
def frozen_datetime():
    """Current frozen time for freezegun tests."""

@pytest.fixture
def {entity}_repository(session) -> I{Entity}Repository:
    """Repository instance for testing."""
    return {Entity}Repository(session=session)
```

## Testing Patterns

### Exception Testing
```python
def test_when_not_found_then_raise_NotFoundException(repository):
    with pytest.raises(EntityNotFoundException):
        get_entity(uuid.uuid4(), repository)
```

### Datetime Testing
```python
@freeze_time("2023-01-01 00:00:00", tz_offset=0)
def test_when_created_then_timestamps_set(repository, frozen_datetime):
    entity = create_entity("name", repository)
    assert entity.created_at == frozen_datetime
    assert entity.updated_at == frozen_datetime
```

### Parameterized Testing
```python
@pytest.mark.parametrize("name,expected", [
    ("valid", True),
    ("", False),
    (None, False),
])
def test_when_name_varies_then_validation_correct(name, expected):
    result = validate_name(name)
    assert result == expected
```

## Running Tests

```bash
# All tests
cd back && task tests

# Specific module
uv run pytest tests/api/{module}/ -v

# Single file
uv run pytest tests/api/{module}/domain/test_create_{entity}.py -v

# Single test
uv run pytest tests/api/{module}/domain/test_create_{entity}.py::test_when_... -v
```
