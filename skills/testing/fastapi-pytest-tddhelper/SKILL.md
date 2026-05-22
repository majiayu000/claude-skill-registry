---
name: FastAPI_Pytest_TDDHelper
description: |
  Senior Backend Architect and Principal QA Engineer skill for Test-Driven Development (TDD) with FastAPI and Pytest. Provides high-performance testing blueprints prioritizing execution speed and memory efficiency. Use when: (1) Setting up pytest for FastAPI projects, (2) Writing tests following Red-Green-Refactor TDD cycle, (3) Creating high-performance conftest.py with async fixtures, (4) Implementing transaction rollback patterns for fast test isolation, (5) Using httpx.AsyncClient for async endpoint testing, (6) Validating responses with Pydantic models, (7) Creating factory fixtures and dependency overrides, (8) Optimizing test execution speed and parallelization. Applies to FastAPI v0.100+ and Pytest v8.0+.
---

# FastAPI Pytest TDD Helper

High-performance TDD blueprint for FastAPI projects.

## Core Principles

| Principle | Implementation |
|-----------|----------------|
| **Speed** | AsyncClient over TestClient (~20% faster) |
| **Isolation** | Transaction rollback, not schema recreation |
| **TDD** | Red-Green-Refactor cycle strictly |
| **Validation** | Pydantic models, not just status codes |

## Quick Start

### 1. Install Dependencies

```bash
pip install pytest pytest-asyncio httpx aiosqlite pytest-cov
```

### 2. Configure pytest (pyproject.toml)

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = ["-v", "--tb=short", "-x"]
```

### 3. Create conftest.py

```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.main import app
from app.database import Base, get_db

@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine("sqlite+aiosqlite:///./test.db", poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session(async_engine):
    async_session = async_sessionmaker(async_engine, class_=AsyncSession)
    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()  # Fast isolation!

@pytest.fixture
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

## TDD Workflow: Red-Green-Refactor

### Step 1: RED - Write Failing Test

```python
from pydantic import BaseModel

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

async def test_create_item(client):
    response = await client.post("/items/", json={"name": "Widget", "price": 10.0})

    assert response.status_code == 201
    item = ItemResponse(**response.json())  # Validate shape!
    assert item.name == "Widget"
```

Run: `pytest -x` (fails - endpoint doesn't exist)

### Step 2: GREEN - Minimal Implementation

```python
@app.post("/items/", status_code=201, response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    return db_item
```

Run: `pytest -x` (passes)

### Step 3: REFACTOR - Optimize

Improve code quality, run tests to verify nothing breaks.

## Reference Documentation

| Task | Reference |
|------|-----------|
| conftest.py patterns, fixture scopes | [references/conftest-patterns.md](references/conftest-patterns.md) |
| Red-Green-Refactor examples | [references/tdd-workflow.md](references/tdd-workflow.md) |
| pyproject.toml, parallel execution | [references/pytest-optimization.md](references/pytest-optimization.md) |
| Response validation with Pydantic | [references/pydantic-validation.md](references/pydantic-validation.md) |
| CRUD tests, mocking, overrides | [references/testing-patterns.md](references/testing-patterns.md) |

## Assets

| Template | Description |
|----------|-------------|
| [assets/conftest_template.py](assets/conftest_template.py) | Complete conftest.py ready to customize |
| [assets/pyproject_template.toml](assets/pyproject_template.toml) | Optimized pytest configuration |

## Performance Decisions

### Why AsyncClient Over TestClient

```python
# AVOID: Sync-to-async bridge overhead
from fastapi.testclient import TestClient
client = TestClient(app)

# USE: Native async, ~20% faster
from httpx import AsyncClient, ASGITransport
async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
    response = await client.get("/")
```

### Why Transaction Rollback Over Schema Recreation

| Approach | 100 tests | 1000 tests |
|----------|-----------|------------|
| Schema recreation | ~60s | ~600s |
| Transaction rollback | ~5s | ~50s |

```python
# FAST: Rollback at end of each test
async with session.begin():
    yield session
    await session.rollback()
```

### Fixture Scoping Strategy

| Scope | Use For | Example |
|-------|---------|---------|
| `session` | Expensive setup | DB engine, app instance |
| `function` | Test isolation | DB session with rollback |

## Common Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test
pytest tests/test_items.py::test_create_item -v

# Run excluding slow tests
pytest -m "not slow"

# Parallel execution
pytest -n auto

# Stop on first failure (TDD mode)
pytest -x

# Run failed tests first
pytest --ff
```

## Parametrize Pattern

```python
@pytest.mark.parametrize("name,price,status", [
    ("Valid", 10.0, 201),
    ("", 10.0, 422),      # Empty name
    ("Item", -5.0, 422),  # Negative price
])
async def test_create_item_validation(client, name, price, status):
    response = await client.post("/items/", json={"name": name, "price": price})
    assert response.status_code == status
```

## Factory Fixture Pattern

```python
@pytest.fixture
def item_factory(db_session):
    async def _create(name="Item", price=10.0, **kwargs):
        item = Item(name=name, price=price, **kwargs)
        db_session.add(item)
        await db_session.flush()
        return item
    return _create

async def test_get_item(client, item_factory):
    item = await item_factory(name="Widget")
    response = await client.get(f"/items/{item.id}")
    assert response.json()["name"] == "Widget"
```
