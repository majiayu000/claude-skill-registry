---
name: database-ops
description: SQLModel async database operations with Neon PostgreSQL, migrations, user isolation, and proper indexing. Use when defining models, queries, or database operations.
---

# SQLModel Database Operations

## Model Definition
```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Always indexed
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Connection Setup
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

engine = create_async_engine(os.getenv("DATABASE_URL"))
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session():
    async with async_session() as session:
        yield session
```

## CRUD with User Isolation (CRITICAL)
```python
from sqlmodel import select

# Always filter by user_id
async def get_tasks(session: AsyncSession, user_id: str, status: str = "all"):
    stmt = select(Task).where(Task.user_id == user_id)
    if status == "pending":
        stmt = stmt.where(Task.completed == False)
    result = await session.execute(stmt)
    return result.scalars().all()

# Update with user isolation
async def update_task(session: AsyncSession, user_id: str, task_id: int, **kwargs):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        return None
    for key, value in kwargs.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    await session.commit()
    return task
```

## Testing
```python
@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        yield session
```