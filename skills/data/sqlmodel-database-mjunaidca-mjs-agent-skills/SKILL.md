---
name: sqlmodel-database
description: Design and implement database schemas using SQLModel with sync and async patterns. Use this skill when creating database models, setting up Neon PostgreSQL connections, defining relationships (one-to-many, many-to-many), implementing FastAPI dependency injection, or migrating schemas. Covers both sync Session and async AsyncSession patterns.
---

# SQLModel Database

Design and implement database schemas using SQLModel - the library that combines SQLAlchemy's power with Pydantic's validation.

## When to Use

- Creating database models for FastAPI applications
- Setting up PostgreSQL/Neon database connections
- Defining model relationships (one-to-many, many-to-many)
- Implementing async database operations
- Creating API request/response schemas from database models
- FastAPI dependency injection for sessions

## Quick Start

```bash
# Sync only
uv add sqlmodel

# Async support (recommended for FastAPI)
uv add sqlmodel sqlalchemy[asyncio] asyncpg  # PostgreSQL
# or
uv add sqlmodel sqlalchemy[asyncio] aiosqlite  # SQLite
```

## Core Patterns

### 1. Model Hierarchy (Base → Table → API)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, Literal

# Base model - shared fields, validation, NO table
class TaskBase(SQLModel):
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = None
    status: Literal["pending", "in_progress", "completed"] = "pending"
    priority: Literal["low", "medium", "high"] = "medium"
    progress_percent: int = Field(default=0, ge=0, le=100)

# Table model - has table=True, adds id and timestamps
class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# Create model - for POST requests (inherits validation)
class TaskCreate(TaskBase):
    pass

# Update model - all fields optional for PATCH
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    progress_percent: Optional[int] = Field(default=None, ge=0, le=100)

# Read model - for responses (includes id)
class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
```

### 2. Sync Database Connection

```python
from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# PostgreSQL: postgresql://user:pass@host/db?sslmode=require
# SQLite: sqlite:///database.db

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### 3. Async Database Connection (Recommended)

```python
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
import os

# Async URLs use different drivers
DATABASE_URL = os.getenv("DATABASE_URL")
# PostgreSQL async: postgresql+asyncpg://user:pass@host/db
# SQLite async: sqlite+aiosqlite:///database.db

async_engine = create_async_engine(DATABASE_URL, echo=True)

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async with AsyncSession(async_engine) as session:
        yield session
```

### 4. FastAPI Integration (Async)

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

@app.post("/tasks", response_model=TaskRead, status_code=201)
async def create_task(
    task: TaskCreate,
    session: AsyncSession = Depends(get_session),
):
    db_task = Task.model_validate(task)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=list[TaskRead])
async def list_tasks(
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = 100,
):
    statement = select(Task).offset(offset).limit(limit)
    results = await session.exec(statement)
    return results.all()

@app.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only update fields that were explicitly set
    update_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(update_data)

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
    return {"ok": True}
```

### 5. Relationships

#### One-to-Many (Task belongs to Project)

```python
from sqlmodel import Field, Relationship
from typing import Optional, List

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    slug: str = Field(unique=True)

    # One project has many tasks
    tasks: List["Task"] = Relationship(back_populates="project")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    # Foreign key
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")

    # Relationship back to project
    project: Optional[Project] = Relationship(back_populates="tasks")
```

#### Many-to-Many (Task has many Workers, Worker has many Tasks)

```python
# Link table (no extra fields)
class TaskWorkerLink(SQLModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    worker_id: Optional[str] = Field(
        default=None, foreign_key="worker.id", primary_key=True
    )

class Worker(SQLModel, table=True):
    id: str = Field(primary_key=True)  # e.g., "@claude-code"
    name: str
    type: Literal["human", "agent"]

    tasks: List["Task"] = Relationship(
        back_populates="workers",
        link_model=TaskWorkerLink
    )

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    workers: List[Worker] = Relationship(
        back_populates="tasks",
        link_model=TaskWorkerLink
    )
```

#### Many-to-Many with Extra Fields

```python
# Link table WITH extra fields
class TaskAssignment(SQLModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    worker_id: Optional[str] = Field(
        default=None, foreign_key="worker.id", primary_key=True
    )
    assigned_at: datetime = Field(default_factory=datetime.now)
    role: str = "assignee"  # assignee, reviewer, etc.

    # Relationships to both sides
    task: "Task" = Relationship(back_populates="assignments")
    worker: "Worker" = Relationship(back_populates="assignments")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    assignments: List[TaskAssignment] = Relationship(back_populates="task")

class Worker(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    assignments: List[TaskAssignment] = Relationship(back_populates="worker")
```

### 6. Self-Referential (Parent-Child Tasks)

```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    # Self-referential foreign key
    parent_id: Optional[int] = Field(default=None, foreign_key="task.id")

    # Parent relationship
    parent: Optional["Task"] = Relationship(
        back_populates="subtasks",
        sa_relationship_kwargs={"remote_side": "Task.id"}
    )

    # Children relationship
    subtasks: List["Task"] = Relationship(back_populates="parent")
```

### 7. Partial Updates with exclude_unset

```python
# The key pattern for PATCH endpoints
update_data = task_update.model_dump(exclude_unset=True)
db_task.sqlmodel_update(update_data)

# This ensures:
# - Fields not in request body are NOT overwritten
# - Fields explicitly set to null ARE updated to null
# - Only provided fields are modified
```

### 8. Query Patterns

```python
from sqlmodel import select, or_, and_, col

# Basic select
statement = select(Task)
results = await session.exec(statement)
tasks = results.all()

# With filters
statement = select(Task).where(Task.status == "pending")

# Multiple conditions (AND)
statement = select(Task).where(
    Task.status == "in_progress",
    Task.priority == "high"
)

# OR conditions
statement = select(Task).where(
    or_(Task.status == "pending", Task.status == "in_progress")
)

# With ordering
statement = select(Task).order_by(Task.created_at.desc())

# With pagination
statement = select(Task).offset(20).limit(10)

# Get single by ID
task = await session.get(Task, task_id)

# Get first match
statement = select(Task).where(Task.title == "Example")
result = await session.exec(statement)
task = result.first()

# Count
from sqlalchemy import func
statement = select(func.count()).select_from(Task)
result = await session.exec(statement)
count = result.one()

# Join with eager loading
from sqlalchemy.orm import selectinload
statement = select(Task).options(selectinload(Task.project))
```

### 9. Neon PostgreSQL Connection

```python
import os
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

# Neon connection string (async)
# Original: postgresql://user:pass@host/db?sslmode=require
# Async: postgresql+asyncpg://user:pass@host/db?ssl=require

DATABASE_URL = os.getenv("DATABASE_URL")

# Convert sync URL to async if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1
    ).replace("sslmode=", "ssl=")

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
)
```

## Testing Patterns

```python
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

@pytest.fixture
def session():
    """In-memory SQLite for fast tests."""
    engine = create_engine(
        "sqlite://",  # In-memory
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    """Test client with overridden session."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test"

def test_update_partial(client, session):
    # Create task
    task = Task(title="Original", priority="low")
    session.add(task)
    session.commit()

    # Partial update - only change priority
    response = client.patch(
        f"/tasks/{task.id}",
        json={"priority": "high"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Original"  # Unchanged
    assert response.json()["priority"] == "high"   # Updated
```

## Critical: Async Session Patterns (MissingGreenlet Prevention)

After `session.commit()`, SQLAlchemy objects become **detached**. Accessing attributes on detached objects triggers lazy loading, which fails in async context with `MissingGreenlet` error.

### The Pattern: Extract → Flush → Commit

```python
@router.post("/entities", response_model=EntityRead, status_code=201)
async def create_entity(
    data: EntityCreate,
    session: AsyncSession = Depends(get_session),
    user: CurrentUser = Depends(get_current_user),
) -> EntityRead:
    # 1. Get related objects and EXTRACT primitives immediately
    worker = await get_worker(session, user.id)
    worker_id = worker.id        # Extract BEFORE any commit
    worker_type = worker.type    # Extract BEFORE any commit

    # 2. Create entity
    entity = Entity(**data.model_dump())
    session.add(entity)

    # 3. Use flush() to get generated ID without committing
    await session.flush()
    entity_id = entity.id        # Extract immediately after flush

    # 4. Do related operations (audit logging, etc.)
    # Pass primitives, NOT objects
    await log_action(
        session,
        entity_id=entity_id,
        actor_id=worker_id,
        actor_type=worker_type,  # String, not object
    )

    # 5. Single commit at the end
    await session.commit()

    # 6. Refresh if you need to return the object
    await session.refresh(entity)
    return entity
```

### Service Functions: Never Commit Internally

```python
# WRONG - service commits, caller loses transaction control
async def log_action(session: AsyncSession, ...):
    log = AuditLog(...)
    session.add(log)
    await session.commit()  # ❌ Don't do this!

# CORRECT - caller owns the transaction
async def log_action(session: AsyncSession, ...):
    log = AuditLog(...)
    session.add(log)
    # No commit - caller will commit
    return log
```

### The Problem: Object Detachment After Commit

```python
# ❌ WRONG - causes MissingGreenlet
worker = await session.get(Worker, 1)
await session.commit()           # Worker is now DETACHED
print(worker.name)               # ERROR! Triggers lazy load in async

# ✅ CORRECT - extract before commit
worker = await session.get(Worker, 1)
worker_name = worker.name        # Extract while attached
await session.commit()
print(worker_name)               # Safe - it's a string
```

### When Passing Objects Between Functions

```python
# ❌ WRONG - passing ORM object that may be detached
async def do_work(entity: Entity):
    print(entity.name)  # May fail if entity was detached

# ✅ CORRECT - pass primitive IDs
async def do_work(entity_id: int, session: AsyncSession):
    entity = await session.get(Entity, entity_id)  # Fresh fetch
    print(entity.name)
```

---

## Common Pitfalls

### 1. Forgetting table=True
```python
# WRONG - no table created
class Task(SQLModel):
    id: int

# CORRECT
class Task(SQLModel, table=True):
    id: int
```

### 2. Using sync Session with async engine
```python
# WRONG
from sqlmodel import Session
async with Session(async_engine) as session:  # Error!

# CORRECT
from sqlmodel.ext.asyncio.session import AsyncSession
async with AsyncSession(async_engine) as session:
```

### 3. Missing await on async operations
```python
# WRONG
task = session.get(Task, 1)  # Returns coroutine, not Task!

# CORRECT
task = await session.get(Task, 1)
```

### 4. Relationship without back_populates
```python
# WRONG - can cause issues
tasks: List["Task"] = Relationship()

# CORRECT
tasks: List["Task"] = Relationship(back_populates="project")
```

### 5. MissingGreenlet after commit (see "Critical: Async Session Patterns" above)
```python
# WRONG - accessing detached object
await session.commit()
print(entity.name)  # MissingGreenlet error!

# CORRECT - extract before commit or refresh after
name = entity.name  # Before commit
await session.commit()
# OR
await session.commit()
await session.refresh(entity)  # Reattach
print(entity.name)
```

### 6. MissingGreenlet in log statements (sneaky!)

**This is a common trap** - log statements that access ORM attributes after commit:

```python
# WRONG - logger.info triggers attribute access after commit!
session.add(notification)
await session.commit()
logger.info("Created notification %d for %s", notification.id, notification.user_id)
#                                              ^^^^^^^^^^^^^^^ MissingGreenlet!

# CORRECT - refresh after commit before accessing any attributes
session.add(notification)
await session.commit()
await session.refresh(notification)  # Reattach to session
logger.info("Created notification %d for %s", notification.id, notification.user_id)

# ALTERNATIVE - extract values before commit
session.add(notification)
await session.flush()  # Get ID without committing
notif_id = notification.id  # Extract while attached
user_id = notification.user_id
await session.commit()
logger.info("Created notification %d for %s", notif_id, user_id)
```

**Why this is sneaky**: The commit succeeds, data is saved, but then the log line crashes.
The notification exists in the database, but you get an error in logs.

---

## Input Validation Patterns

### Converting 0 to None for nullable foreign keys

Swagger UI and some clients send `0` as default for optional int fields. This violates FK constraints.

```python
from pydantic import field_validator

class TaskCreate(SQLModel):
    assignee_id: int | None = None
    parent_task_id: int | None = None

    @field_validator("assignee_id", "parent_task_id", mode="after")
    @classmethod
    def zero_to_none(cls, v: int | None) -> int | None:
        """Convert 0 to None (0 is not a valid FK)."""
        return None if v == 0 else v
```

### Normalizing timezone-aware datetimes

Database stores naive UTC, but clients may send ISO 8601 with timezone.

```python
from datetime import UTC, datetime
from pydantic import field_validator

class TaskCreate(SQLModel):
    due_date: datetime | None = None

    @field_validator("due_date", mode="after")
    @classmethod
    def normalize_datetime(cls, v: datetime | None) -> datetime | None:
        """Strip timezone after converting to UTC."""
        if v is None:
            return None
        if v.tzinfo is not None:
            v = v.astimezone(UTC).replace(tzinfo=None)
        return v
```

## References

For additional documentation, use Context7 MCP:
```
mcp__context7__resolve-library-id with libraryName="sqlmodel"
mcp__context7__get-library-docs with topic="relationships" or "async"
```

See also: `references/migrations.md` for schema migration patterns.
