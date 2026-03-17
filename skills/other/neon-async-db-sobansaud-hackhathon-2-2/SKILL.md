---
name: neon-async-db
description: This skill should be used when setting up and managing reliable, high-performance asynchronous database connections for Neon Serverless PostgreSQL using SQLModel and SQLAlchemy's async capabilities.
---

# Neon PostgreSQL Async Connection

This skill providing guidance on setting up and managing reliable asynchronous database connections for Neon Serverless PostgreSQL.

## Purpose
Setting up and managing reliable, high-performance asynchronous database connections for Neon Serverless PostgreSQL using SQLModel and SQLAlchemy's async capabilities.

## Capabilities
- Environment-aware configuration using `DATABASE_URL`.
- Creating an asynchronous SQLAlchemy engine using the `asyncpg` driver.
- Implementing a `get_async_session` dependency utilizing proper async context management.
- Centralized `Base` metadata management for SQLModel tables.
- Connection health check utilities for operational monitoring.
- Serverless-optimized connection pooling configuration.

## Implementation Details

### Driver & Engine
Ensuring the `DATABASE_URL` uses the `postgresql+asyncpg://` scheme.
```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        yield session
```

### Health Check
Implementing a lightweight query to verify connectivity.
```python
async def check_db_health():
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
```

## Best Practices
- Using `pool_pre_ping=True` to handle stale connections commonly found in serverless environments.
- Setting `expire_on_commit=False` in async sessions to allow access to object attributes after a commit.
- Always using async context managers (`async with`) for sessions to ensure they are properly returned to the pool.
