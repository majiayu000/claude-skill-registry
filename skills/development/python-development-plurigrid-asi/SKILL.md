---
name: python-development
description: Modern Python development with Python 3.12+, Django, FastAPI, async patterns,
version: 1.0.0
---


# Python Development

## Project Setup

### Modern Python Project Structure
```
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### pyproject.toml
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
strict = true
```

## Type Hints

```python
from typing import TypeVar, Generic
from collections.abc import Sequence

T = TypeVar('T')

def process_items(items: Sequence[str]) -> list[str]:
    return [item.upper() for item in items]

class Repository(Generic[T]):
    def get(self, id: int) -> T | None: ...
    def save(self, item: T) -> T: ...
```

## Async Patterns

```python
import asyncio
from collections.abc import AsyncIterator

async def fetch_all(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def stream_data() -> AsyncIterator[bytes]:
    async with aiofiles.open('large_file.txt', 'rb') as f:
        async for chunk in f:
            yield chunk
```

## FastAPI Patterns

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

@app.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Database = Depends(get_db)
) -> UserResponse:
    result = await db.users.create(user.model_dump())
    return UserResponse(**result)
```

## Testing

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.users.get.return_value = {"id": 1, "name": "Test"}
    return db

@pytest.mark.asyncio
async def test_get_user(mock_db):
    result = await get_user(1, db=mock_db)
    assert result["name"] == "Test"
    mock_db.users.get.assert_called_once_with(1)
```

## Best Practices

- Use `ruff` for linting and formatting
- Use `mypy` with strict mode
- Prefer `pathlib.Path` over `os.path`
- Use dataclasses or Pydantic for data structures
- Use `asyncio` for I/O-bound operations
- Use `contextlib.asynccontextmanager` for async resources



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.