---
name: sqlalchemy-2-async
description: SQLAlchemy 2.0 async patterns with AsyncSession, async_sessionmaker, and FastAPI integration. Use when implementing async database operations, connection pooling, or async ORM queries.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [sqlalchemy, async, database, orm, fastapi, python, 2026]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
author: SkillForge
user-invocable: false
---

# SQLAlchemy 2.0 Async Patterns (2026)

Modern async database patterns with SQLAlchemy 2.0, AsyncSession, and FastAPI integration.

## Overview

- Building async FastAPI applications with database access
- Implementing async repository patterns
- Configuring async connection pooling
- Running concurrent database queries
- Avoiding N+1 queries in async context

## Quick Reference

### Engine and Session Factory

```python
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

# Create async engine - ONE per application
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False,          # Set True for SQL logging in dev
)

# Session factory - use this to create sessions
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy load issues
    autoflush=False,         # Explicit flush control
)
```

### FastAPI Dependency Injection

```python
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides async database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Usage in route
@router.get("/users/{user_id}")
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return UserResponse.model_validate(user)
```

### Async Model Definition

```python
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Relationship with explicit lazy loading strategy
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
        lazy="raise",  # Prevent accidental lazy loads - MUST use selectinload
    )

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    total: Mapped[int]

    user: Mapped["User"] = relationship(back_populates="orders", lazy="raise")
```

### Eager Loading (Avoid N+1)

```python
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select

async def get_user_with_orders(db: AsyncSession, user_id: UUID) -> User | None:
    """Load user with orders in single query - NO N+1."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.orders))  # Eager load orders
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def get_users_with_orders(db: AsyncSession, limit: int = 100) -> list[User]:
    """Load multiple users with orders efficiently."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.orders))
        .limit(limit)
    )
    return list(result.scalars().all())
```

### Bulk Operations (2026 Optimized)

```python
async def bulk_insert_users(db: AsyncSession, users_data: list[dict]) -> int:
    """Efficient bulk insert - SQLAlchemy 2.0 uses multi-value INSERT."""
    # SQLAlchemy 2.0 automatically batches as single INSERT with multiple VALUES
    users = [User(**data) for data in users_data]
    db.add_all(users)
    await db.flush()  # Get IDs without committing
    return len(users)

async def bulk_insert_chunked(
    db: AsyncSession,
    items: list[dict],
    chunk_size: int = 1000,
) -> int:
    """Insert large datasets in chunks to manage memory."""
    total = 0
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        db.add_all([Item(**data) for data in chunk])
        await db.flush()
        total += len(chunk)
    return total
```

### Repository Pattern

```python
from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Base)

class AsyncRepository(Generic[T]):
    """Generic async repository for CRUD operations."""

    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)

    async def get_many(self, ids: list[UUID]) -> list[T]:
        result = await self.session.execute(
            select(self.model).where(self.model.id.in_(ids))
        )
        return list(result.scalars().all())

    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.flush()
        return instance

    async def delete(self, instance: T) -> None:
        await self.session.delete(instance)
        await self.session.flush()
```

### Concurrent Queries with TaskGroup

```python
import asyncio

async def get_dashboard_data(db: AsyncSession, user_id: UUID) -> dict:
    """Run multiple queries concurrently - same session is NOT thread-safe."""
    # WRONG: Don't share AsyncSession across tasks
    # async with asyncio.TaskGroup() as tg:
    #     tg.create_task(db.execute(...))  # NOT SAFE

    # CORRECT: Sequential queries with same session
    user = await db.get(User, user_id)
    orders_result = await db.execute(
        select(Order).where(Order.user_id == user_id).limit(10)
    )
    stats_result = await db.execute(
        select(func.count(Order.id)).where(Order.user_id == user_id)
    )

    return {
        "user": user,
        "recent_orders": list(orders_result.scalars().all()),
        "total_orders": stats_result.scalar(),
    }

async def get_data_from_multiple_users(user_ids: list[UUID]) -> list[dict]:
    """Concurrent queries - each task gets its own session."""
    async def fetch_user(user_id: UUID) -> dict:
        async with async_session_factory() as session:
            user = await session.get(User, user_id)
            return {"id": user_id, "email": user.email if user else None}

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_user(uid)) for uid in user_ids]

    return [t.result() for t in tasks]
```

## Key Decisions

| Decision | 2026 Recommendation | Rationale |
|----------|---------------------|-----------|
| Session scope | One AsyncSession per task/request | SQLAlchemy docs: "AsyncSession per task" |
| Scoped sessions | **Avoid** for async | Maintainers discourage for async code |
| Lazy loading | Use `lazy="raise"` + explicit loads | Prevents accidental N+1 in async |
| Eager loading | `selectinload` for collections | Better than joinedload for async |
| expire_on_commit | Set to `False` | Prevents lazy load errors after commit |
| Connection pool | `pool_pre_ping=True` | Validates connections before use |
| Bulk inserts | Chunk 1000-10000 rows | Memory management for large inserts |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER share AsyncSession across tasks
async with asyncio.TaskGroup() as tg:
    tg.create_task(session.execute(...))  # RACE CONDITION

# NEVER use sync Session in async code
from sqlalchemy.orm import Session
session = Session(engine)  # BLOCKS EVENT LOOP

# NEVER access lazy-loaded relationships without eager loading
user = await session.get(User)
orders = user.orders  # RAISES if lazy="raise", or BLOCKS if not

# NEVER use scoped_session with async
from sqlalchemy.orm import scoped_session
ScopedSession = scoped_session(session_factory)  # WRONG for async

# NEVER forget to handle session lifecycle
session = async_session_factory()
result = await session.execute(...)
# MISSING: session.close() - connection leak!

# NEVER use create_async_engine without pool_pre_ping in production
engine = create_async_engine(url)  # May use stale connections
```

## Related Skills

- `asyncio-advanced` - TaskGroup and structured concurrency patterns
- `alembic-migrations` - Database migration with async support
- `fastapi-advanced` - Full FastAPI integration patterns
- `database-schema-designer` - Schema design best practices

## Capability Details

### async-session
**Keywords:** AsyncSession, async_sessionmaker, session factory, connection
**Solves:**
- How do I create async database sessions?
- Configure async connection pooling
- Session lifecycle management

### fastapi-integration
**Keywords:** Depends, dependency injection, get_db, request scope
**Solves:**
- How do I integrate SQLAlchemy with FastAPI?
- Request-scoped database sessions
- Automatic commit/rollback handling

### eager-loading
**Keywords:** selectinload, joinedload, eager load, N+1, relationship
**Solves:**
- How do I avoid N+1 queries in async?
- Load relationships efficiently
- Configure lazy loading behavior

### bulk-operations
**Keywords:** bulk insert, batch, chunk, add_all, performance
**Solves:**
- How do I insert many rows efficiently?
- Chunk large inserts for memory
- SQLAlchemy 2.0 bulk optimizations

### repository-pattern
**Keywords:** repository, CRUD, generic, base repository
**Solves:**
- How do I implement repository pattern?
- Generic async CRUD operations
- Clean architecture with SQLAlchemy
