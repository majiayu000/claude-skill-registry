---
name: python-developer
description: Эксперт Python разработки. Используй для Python best practices, async, typing и ecosystem.
---

# Python Developer Expert

Expert in modern Python development, type hints, and clean architecture.

## Core Principles

- Type hints for all function signatures
- PEP 8 compliance
- Idiomatic, Pythonic code
- Comprehensive docstrings

## Modern Python (3.10+)

### Type Hints

```python
from typing import Optional, Union
from collections.abc import Sequence

# Union types (3.10+)
def process(value: int | str | None) -> str:
    if value is None:
        return "empty"
    return str(value)

# Generic types
def first_item[T](items: Sequence[T]) -> T | None:
    return items[0] if items else None
```

### Pattern Matching

```python
def handle_response(response: dict) -> str:
    match response:
        case {"status": "success", "data": data}:
            return f"Success: {data}"
        case {"status": "error", "message": msg}:
            return f"Error: {msg}"
        case {"status": status}:
            return f"Unknown status: {status}"
        case _:
            return "Invalid response"
```

### Dataclasses

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.email = self.email.lower()
```

## Async Programming

```python
import asyncio
import aiohttp
from typing import Any

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict[str, Any]:
    async with session.get(url) as response:
        return await response.json()

async def fetch_all(urls: list[str]) -> list[dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Async generator
async def stream_data(source):
    async for item in source:
        yield process(item)
```

## Context Managers

```python
from contextlib import contextmanager, asynccontextmanager
from typing import Generator

@contextmanager
def managed_resource(name: str) -> Generator[Resource, None, None]:
    resource = acquire_resource(name)
    try:
        yield resource
    finally:
        resource.release()

@asynccontextmanager
async def async_db_session():
    session = await create_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
```

## Error Handling

```python
class ApplicationError(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, code: str, details: dict | None = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}

class ValidationError(ApplicationError):
    """Raised when validation fails."""
    def __init__(self, field: str, message: str):
        super().__init__(message, "VALIDATION_ERROR", {"field": field})

# Usage
def validate_user(data: dict) -> User:
    if not data.get("email"):
        raise ValidationError("email", "Email is required")
    if "@" not in data["email"]:
        raise ValidationError("email", "Invalid email format")
    return User(**data)
```

## Project Structure

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       ├── services/
│       └── utils/
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── README.md
```

### pyproject.toml

```toml
[project]
name = "my-package"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
strict = true
python_version = "3.11"

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

## Testing with Pytest

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def user_data():
    return {"id": 1, "email": "test@example.com", "name": "Test"}

@pytest.fixture
async def db_session():
    session = await create_test_session()
    yield session
    await session.rollback()

class TestUserService:
    async def test_create_user(self, db_session, user_data):
        service = UserService(db_session)
        user = await service.create(user_data)
        assert user.email == user_data["email"]

    async def test_create_user_duplicate_email(self, db_session, user_data):
        service = UserService(db_session)
        await service.create(user_data)
        with pytest.raises(ValidationError):
            await service.create(user_data)

    @patch("services.user.send_email", new_callable=AsyncMock)
    async def test_send_welcome_email(self, mock_send, db_session):
        service = UserService(db_session)
        await service.send_welcome(user_id=1)
        mock_send.assert_called_once()
```

## FastAPI Example

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

@app.post("/users", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        user = await service.create(data.model_dump())
        return UserResponse.model_validate(user)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Лучшие практики

1. **Type hints everywhere** — типизация улучшает читаемость и IDE support
2. **Dataclasses/Pydantic** — для структурированных данных
3. **Context managers** — для управления ресурсами
4. **Async when needed** — для I/O-bound операций
5. **Pytest fixtures** — для переиспользования тестовой логики
6. **Ruff + MyPy** — для линтинга и проверки типов
