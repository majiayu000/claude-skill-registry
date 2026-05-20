---
name: fastapi-templates
description: FastAPI architecture opinions and non-obvious patterns. Use when building FastAPI applications.
---

# FastAPI Templates

Architecture decisions and gotchas for FastAPI projects.

## Style Guide

Source: Google Python Style Guide. Extends Python Patterns skill conventions.

- **Naming**: follow Python Patterns skill conventions (`_internal` prefix, descriptive names, boolean `is_`/`has_` prefix)
- Google-style docstrings (`Args:`/`Returns:`/`Raises:`) on all endpoints and services
- Type annotations on all public functions — FastAPI uses them for validation and docs generation

## Preferred Structure

```
app/
    api/v1/endpoints/, api/v1/router.py, api/dependencies.py
    core/config.py, core/security.py, core/database.py
    models/, schemas/, services/, repositories/
    main.py
```

## Architecture Opinions

- **Service layer is mandatory** -- no business logic in route handlers
- **Repository pattern** -- separate data access from business logic
- **Pydantic schemas for everything** -- request, response, internal DTOs
- **`pydantic-settings`** for config with `.env` loading
- **Async SQLAlchemy** with `AsyncSession` (not sync drivers)

## Lifespan Pattern (not on_event)

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="API", lifespan=lifespan)
```

## Database Session Dependency

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

## Config with pydantic-settings

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

## Generic CRUD Repository

```python
class BaseRepository(Generic[ModelType, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CreateSchema) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
```

## Testing Setup

```python
@pytest.fixture
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
```

## Gotchas

- **Blocking in async handlers** -- never use sync DB drivers; use `run_in_executor` for blocking libs
- **Missing type hints** -- FastAPI loses validation/docs without them
- **Direct DB in routes** -- always go through service layer
- **`on_event` deprecated** -- use lifespan context manager
- **`obj.dict()` deprecated** -- use `obj.model_dump()` (Pydantic v2)

## Cross-References

- **languages:pydantic-and-data-validation** -- model design, validators, serialization patterns
- **languages:async-python-patterns** -- asyncio patterns, structured concurrency, event loop debugging
- **architecture:api-design-principles** -- REST/GraphQL design, pagination, error handling conventions
