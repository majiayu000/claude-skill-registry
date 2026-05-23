---
name: python
description: Write Python code following best practices. Use when developing Python applications. Covers type hints, async, and modern tooling.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Python Development

## Project Setup

```bash
# Create project with uv
uv init my-project
cd my-project

# Add dependencies
uv add litestar
uv add --dev pytest ruff mypy
```

### pyproject.toml
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["litestar>=2.0"]

[tool.ruff]
line-length = 88
target-version = "py313"

[tool.mypy]
strict = true
python_version = "3.13"
```

## Type Hints

```python
from typing import TypeVar, Generic
from collections.abc import Sequence

T = TypeVar('T')

class Repository(Generic[T]):
    async def find_by_id(self, id: str) -> T | None:
        ...

    async def save(self, entity: T) -> T:
        ...

def process_items(items: Sequence[str]) -> list[str]:
    return [item.upper() for item in items]
```

## Async Patterns

```python
import asyncio
from collections.abc import AsyncIterator

async def fetch_all(urls: list[str]) -> list[Response]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def stream_data() -> AsyncIterator[bytes]:
    async with aiofiles.open('large.csv', 'rb') as f:
        async for chunk in f:
            yield chunk
```

## Error Handling

```python
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass
class Err(Generic[E]):
    error: E

Result = Ok[T] | Err[E]

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)
```

## Testing with pytest

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_create_user():
    repo = AsyncMock()
    service = UserService(repo)

    user = await service.create("test@example.com")

    assert user.email == "test@example.com"
    repo.save.assert_called_once()

@pytest.fixture
def mock_database():
    with patch('app.database') as mock:
        yield mock
```

## Tooling

```bash
# Ruff (linting + formatting)
ruff check --fix .
ruff format .

# MyPy (type checking)
mypy --strict .

# pytest
pytest -v --cov=src
```
