---
name: building-with-sqlmodel-async
description: Use when building async database layers with SQLModel and PostgreSQL. Triggers include async session management, create_async_engine, SQLModel relationships, CRUD operations with async/await, N+1 prevention with selectinload, JSONB columns, self-referential models, or Alembic async migrations. NOT when using sync SQLAlchemy (use sync patterns) or raw SQL (use SQLModel ORM).
---

# SQLModel Async Database Development Guide

Build production async database layers for FastAPI agent backends using SQLModel + SQLAlchemy 2.0 async patterns with PostgreSQL.

## Overview

SQLModel combines Pydantic and SQLAlchemy, providing type-safe ORM with async support. For agent backends, async database operations are essential for non-blocking I/O during agent tool calls, API requests, and concurrent operations.

## Quick Reference

### Installation

```bash
# Production stack
pip install sqlmodel sqlalchemy[asyncio] asyncpg alembic

# Development
pip install aiosqlite  # For SQLite async testing
```

### Core Imports

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, Field, Relationship, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
```

## Engine Setup

### Production PostgreSQL

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from collections.abc import AsyncGenerator

# Convert sync URL to async format
def get_async_database_url(url: str) -> str:
    """Convert postgresql:// to postgresql+asyncpg://"""
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url

DATABASE_URL = get_async_database_url(settings.database_url)

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,    # Essential for managed DBs (Neon, Supabase)
    pool_recycle=300,      # Recycle connections every 5 minutes
)
```

### SQLite for Testing

```python
if DATABASE_URL.startswith("sqlite"):
    engine = create_async_engine(
        DATABASE_URL,
        echo=settings.debug,
        connect_args={"check_same_thread": False},
    )
```

### Table Creation

```python
async def create_db_and_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

## Session Management

### FastAPI Dependency

```python
async def get_session() -> AsyncGenerator[AsyncSession]:
    """Dependency that yields async database sessions."""
    async with AsyncSession(engine) as session:
        yield session
```

### Using in Endpoints

```python
from fastapi import Depends

@router.get("/api/tasks/{task_id}")
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

## Model Design

### Basic Model with JSONB

```python
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class Task(SQLModel, table=True):
    """A unit of work with metadata."""

    __tablename__ = "task"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=500)
    description: str | None = Field(default=None)
    status: str = Field(default="pending")
    priority: str = Field(default="medium")

    # JSONB for list/dict fields (PostgreSQL)
    tags: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSONB, nullable=False, server_default="[]"),
    )

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Foreign Keys and Relationships

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .project import Project
    from .worker import Worker

class Task(SQLModel, table=True):
    # Foreign keys
    project_id: int = Field(foreign_key="project.id", index=True)
    assignee_id: int | None = Field(
        default=None,
        foreign_key="worker.id",
    )

    # Relationships
    project: "Project" = Relationship(back_populates="tasks")
    assignee: "Worker" = Relationship(
        back_populates="assigned_tasks",
        sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"},
    )
```

### Self-Referential Relationships (Parent-Child)

```python
class Task(SQLModel, table=True):
    parent_task_id: int | None = Field(
        default=None,
        foreign_key="task.id",
    )

    # Self-referential: parent
    parent: "Task" = Relationship(
        back_populates="subtasks",
        sa_relationship_kwargs={
            "remote_side": "Task.id",
            "foreign_keys": "[Task.parent_task_id]",
        },
    )

    # Self-referential: children
    subtasks: list["Task"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"foreign_keys": "[Task.parent_task_id]"},
    )
```

## CRUD Operations

### Create

```python
async def create_task(
    session: AsyncSession,
    data: TaskCreate,
    creator_id: int,
) -> Task:
    task = Task(
        title=data.title,
        description=data.description,
        project_id=data.project_id,
        created_by_id=creator_id,
    )
    session.add(task)
    await session.flush()    # Get task.id without committing
    await session.commit()
    await session.refresh(task)
    return task
```

### Read Single

```python
async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    return await session.get(Task, task_id)
```

### Read with Query

```python
async def list_tasks_by_project(
    session: AsyncSession,
    project_id: int,
    status: str | None = None,
) -> list[Task]:
    stmt = select(Task).where(Task.project_id == project_id)

    if status:
        stmt = stmt.where(Task.status == status)

    stmt = stmt.order_by(Task.created_at.desc())

    result = await session.exec(stmt)
    return list(result.all())
```

### Update

```python
async def update_task(
    session: AsyncSession,
    task: Task,
    data: TaskUpdate,
) -> Task:
    if data.title is not None:
        task.title = data.title
    if data.status is not None:
        task.status = data.status

    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

### Delete

```python
async def delete_task(session: AsyncSession, task: Task) -> None:
    await session.delete(task)
    await session.commit()
```

## N+1 Prevention with Eager Loading

### The Problem

```python
# BAD: N+1 queries - each task.assignee triggers a query
tasks = (await session.exec(select(Task))).all()
for task in tasks:
    print(task.assignee.name)  # N additional queries!
```

### The Solution: selectinload

```python
from sqlalchemy.orm import selectinload

# GOOD: Eager load relationships in single query
stmt = (
    select(Task)
    .options(
        selectinload(Task.assignee),
        selectinload(Task.subtasks),
    )
    .where(Task.project_id == project_id)
)

result = await session.exec(stmt)
tasks = result.unique().all()  # unique() required with selectinload

for task in tasks:
    print(task.assignee.name)  # No additional queries!
```

### When to Use Each Strategy

| Relationship Type | Strategy | Why |
|-------------------|----------|-----|
| Many-to-one (task → assignee) | `selectinload` or `joinedload` | Both efficient |
| One-to-many (project → tasks) | `selectinload` | Avoids row explosion |
| Many-to-many | `selectinload` | Single efficient query |
| Self-referential | `selectinload` | Handles recursion |

## Transaction Patterns

### flush() vs commit()

```python
async def create_with_audit(session: AsyncSession, data: dict):
    # Create main record
    task = Task(**data)
    session.add(task)
    await session.flush()  # Get task.id, keep transaction open

    # Create audit record using task.id
    audit = AuditLog(entity_id=task.id, action="created")
    session.add(audit)

    # Single commit for both
    await session.commit()
```

### Rollback on Error

```python
async def transactional_operation(session: AsyncSession):
    try:
        task = Task(title="New task")
        session.add(task)
        await session.flush()

        # Might fail
        await some_risky_operation(task.id)

        await session.commit()
    except Exception:
        await session.rollback()
        raise
```

### Context Manager Pattern

```python
async with AsyncSession(engine) as session:
    async with session.begin():
        # All operations in single transaction
        session.add(task1)
        session.add(task2)
    # Auto-commit on exit, rollback on exception
```

## Alembic Async Migrations

### Initialize

```bash
alembic init -t async alembic
```

### Configure alembic.ini

```ini
sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/dbname
```

### Configure env.py

```python
from sqlmodel import SQLModel
from your_app.models import Task, Project  # Import all models

target_metadata = SQLModel.metadata

def run_migrations_offline():
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = create_async_engine(
        get_async_database_url(settings.database_url)
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    asyncio.run(run_async_migrations())
```

### Generate and Run

```bash
alembic revision --autogenerate -m "Add tasks table"
alembic upgrade head
```

## Common Patterns

### Pagination

```python
async def list_paginated(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[Task]:
    stmt = (
        select(Task)
        .order_by(Task.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.exec(stmt)
    return list(result.all())
```

### Soft Delete

```python
class Task(SQLModel, table=True):
    deleted_at: datetime | None = Field(default=None)

async def soft_delete(session: AsyncSession, task: Task):
    task.deleted_at = datetime.utcnow()
    session.add(task)
    await session.commit()
```

### Bulk Insert

```python
async def bulk_create_tasks(
    session: AsyncSession,
    tasks_data: list[dict],
) -> list[Task]:
    tasks = [Task(**data) for data in tasks_data]
    session.add_all(tasks)
    await session.commit()
    return tasks
```

## Safety & Guardrails

### NEVER
- Use sync SQLAlchemy in async code (blocks event loop)
- Share AsyncSession across concurrent tasks (not thread-safe)
- Access lazy-loaded relationships without eager loading in async
- Forget `result.unique().all()` with selectinload

### ALWAYS
- Use `pool_pre_ping=True` for managed databases
- Import models before `create_db_and_tables()`
- Use `TYPE_CHECKING` for relationship type hints
- Handle MissingGreenlet errors (indicates lazy load in async)

### Error Handling

```python
from sqlalchemy.exc import IntegrityError

try:
    await session.commit()
except IntegrityError as e:
    await session.rollback()
    if "unique constraint" in str(e):
        raise HTTPException(400, "Duplicate entry")
    raise
```

## TaskManager Database Example

Complete database layer for Task API:

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/taskdb",
    pool_pre_ping=True,
    pool_size=5,
)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

# models/task.py
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    status: str = Field(default="pending")
    project_id: int = Field(foreign_key="project.id")
    assignee_id: int | None = Field(foreign_key="worker.id")

    project: "Project" = Relationship(back_populates="tasks")
    assignee: "Worker" = Relationship(back_populates="tasks")

# routers/tasks.py
@router.get("/tasks")
async def list_tasks(
    session: AsyncSession = Depends(get_session),
    project_id: int = Query(...),
):
    stmt = (
        select(Task)
        .options(selectinload(Task.assignee))
        .where(Task.project_id == project_id)
    )
    result = await session.exec(stmt)
    return result.unique().all()
```

## References

Load these for detailed patterns:
- [Async Patterns](references/async-patterns.md) - Advanced async session patterns
- [Relationships](references/relationships.md) - Complex relationship configurations
- [Migrations](references/migrations.md) - Alembic migration patterns
