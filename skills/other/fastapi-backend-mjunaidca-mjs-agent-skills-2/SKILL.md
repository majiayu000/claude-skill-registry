---
name: fastapi-backend
description: Build production-grade FastAPI backends with SQLModel, Pydantic, and JWT authentication. Use this skill when building REST APIs, integrating with Neon PostgreSQL, implementing Better Auth JWT verification, or creating CRUD endpoints. Includes patterns for audit logging, worker/agent parity, and OpenAPI documentation.
---

# FastAPI Backend

Build production-grade FastAPI backends with SQLModel, Pydantic v2, and JWT/JWKS authentication patterns.

## When to Use

- Building REST API endpoints with FastAPI
- Creating SQLModel schemas for Neon PostgreSQL
- Implementing JWT verification against Better Auth JWKS
- Designing OpenAPI contracts for frontend consumption
- Adding audit logging to API operations
- Ensuring human-agent parity in API design

## Quick Start

```bash
# Project setup
uv init backend && cd backend
uv add fastapi sqlmodel pydantic httpx python-jose uvicorn

# Development
uv run uvicorn main:app --reload --port 8000

# Access docs
open http://localhost:8000/docs  # Swagger UI with Authorize button
```

## Core Patterns

### 1. SQLModel Schema (Database + API)

SQLModel combines SQLAlchemy and Pydantic. Use `table=True` for database models:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, Literal

# Base model (shared fields, no table)
class TaskBase(SQLModel):
    title: str = Field(max_length=200)
    description: Optional[str] = None
    status: Literal["pending", "in_progress", "review", "completed", "blocked"] = "pending"
    priority: Literal["low", "medium", "high", "critical"] = "medium"
    progress_percent: int = Field(default=0, ge=0, le=100)
    assigned_to: Optional[str] = None
    project_slug: Optional[str] = None
    parent_id: Optional[int] = None

# Database model (has table)
class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# API models (no table, for request/response)
class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    progress_percent: Optional[int] = None
    assigned_to: Optional[str] = None

class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
```

### 2. Neon PostgreSQL Connection

```python
from sqlmodel import create_engine, Session
import os

# Neon connection string
DATABASE_URL = os.getenv("DATABASE_URL")  # postgresql://user:pass@host/db?sslmode=require

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

### 3. CRUD Endpoints

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select

app = FastAPI(title="TaskFlow API", version="1.0.0")

@app.post("/api/tasks", response_model=TaskRead, status_code=201)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # Audit log
    log_action(session, "created", current_user.id, task_id=db_task.id)

    return db_task

@app.get("/api/tasks", response_model=list[TaskRead])
def list_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    status: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None),
    project: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
):
    query = select(Task)

    if status:
        query = query.where(Task.status == status)
    if assigned_to:
        query = query.where(Task.assigned_to == assigned_to)
    if project:
        query = query.where(Task.project_slug == project)

    query = query.offset(offset).limit(limit)
    return session.exec(query).all()

@app.get("/api/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/api/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.now()
    session.add(task)
    session.commit()
    session.refresh(task)

    # Audit log
    log_action(session, "updated", current_user.id, task_id=task.id, context=update_data)

    return task
```

### 4. JWT Authentication (Better Auth JWKS)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, jwk, JWTError
import httpx
import time

security = HTTPBearer()

# Cache JWKS keys
_jwks_cache = None
_jwks_cache_time = 0
JWKS_CACHE_TTL = 3600  # 1 hour

AUTH_SERVER_URL = os.getenv("AUTH_SERVER_URL", "http://localhost:3001")
JWKS_URL = f"{AUTH_SERVER_URL}/api/auth/jwks"

async def get_jwks():
    """Fetch and cache JWKS from Better Auth server."""
    global _jwks_cache, _jwks_cache_time

    now = time.time()
    if _jwks_cache and (now - _jwks_cache_time) < JWKS_CACHE_TTL:
        return _jwks_cache

    async with httpx.AsyncClient() as client:
        response = await client.get(JWKS_URL)
        response.raise_for_status()
        _jwks_cache = response.json()
        _jwks_cache_time = now
        return _jwks_cache

async def verify_token(token: str) -> dict:
    """Verify JWT against Better Auth JWKS."""
    try:
        # Get JWKS
        jwks = await get_jwks()

        # Get unverified header to find key ID
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        # Find matching key
        rsa_key = None
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                rsa_key = key
                break

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Key not found")

        # Verify token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            options={"verify_aud": False}  # Adjust based on your setup
        )
        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Extract and verify current user from JWT."""
    token = credentials.credentials
    payload = await verify_token(token)

    return {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role", "user"),
    }
```

### 5. Swagger UI Authentication

FastAPI automatically adds an "Authorize" button when using `HTTPBearer`:

```python
from fastapi import FastAPI
from fastapi.security import HTTPBearer

app = FastAPI(
    title="TaskFlow API",
    description="Human-Agent Task Management API",
    version="1.0.0",
)

# This adds the "Authorize" button to Swagger UI
security = HTTPBearer()

# Testing flow:
# 1. Login to your SSO (browser) → Get JWT
# 2. Open http://localhost:8000/docs
# 3. Click "Authorize" button
# 4. Paste JWT token (without "Bearer " prefix)
# 5. All requests now include Authorization header
```

### 6. Audit Logging

```python
from sqlalchemy import JSON

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: Optional[int] = None
    project_slug: Optional[str] = None
    actor_id: str
    actor_type: Literal["human", "agent"]
    action: str
    context: Optional[dict] = Field(default=None, sa_column_kwargs={"type_": JSON})
    timestamp: datetime = Field(default_factory=datetime.now)

def log_action(
    session: Session,
    action: str,
    actor_id: str,
    task_id: Optional[int] = None,
    project_slug: Optional[str] = None,
    context: Optional[dict] = None,
):
    """Create audit log entry."""
    # Determine actor type from worker registry
    worker = session.exec(select(Worker).where(Worker.id == actor_id)).first()
    actor_type = worker.type if worker else "human"

    log = AuditLog(
        task_id=task_id,
        project_slug=project_slug,
        actor_id=actor_id,
        actor_type=actor_type,
        action=action,
        context=context,
    )
    session.add(log)
    session.commit()
    return log
```

### 7. Agent Parity (MCP Compatibility)

Design endpoints that work for both CLI and MCP clients:

```python
# Same endpoint serves:
# - CLI: taskflow start 1 → POST /api/tasks/1/start
# - MCP: claim_task(1) → POST /api/tasks/1/start
# - Web: Button click → POST /api/tasks/1/start

@app.post("/api/tasks/{task_id}/start", response_model=TaskRead)
def start_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Start a task (claim and begin work)."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start task with status '{task.status}'"
        )

    task.status = "in_progress"
    task.assigned_to = current_user["id"]
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)

    log_action(session, "started", current_user["id"], task_id=task.id)

    return task

@app.post("/api/tasks/{task_id}/progress", response_model=TaskRead)
def update_progress(
    task_id: int,
    percent: int = Query(..., ge=0, le=100),
    note: Optional[str] = Query(None),
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Update task progress."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != "in_progress":
        raise HTTPException(status_code=400, detail="Task must be in_progress")

    task.progress_percent = percent
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)

    log_action(
        session, "progressed", current_user["id"],
        task_id=task.id,
        context={"percent": percent, "note": note}
    )

    return task

@app.post("/api/tasks/{task_id}/complete", response_model=TaskRead)
def complete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Complete a task."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status not in ["in_progress", "review"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete task with status '{task.status}'"
        )

    task.status = "completed"
    task.progress_percent = 100
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)

    log_action(session, "completed", current_user["id"], task_id=task.id)

    return task
```

## Project Structure

```
backend/
├── main.py              # FastAPI app, routes
├── models.py            # SQLModel schemas
├── database.py          # Neon connection
├── auth.py              # JWT/JWKS verification
├── audit.py             # Audit logging
├── dependencies.py      # Shared dependencies
└── tests/
    ├── conftest.py      # Test fixtures
    ├── test_tasks.py    # Task endpoint tests
    └── test_auth.py     # Auth tests
```

## Critical: Async Session Patterns (MissingGreenlet Prevention)

After `session.commit()`, SQLAlchemy objects become **detached**. Accessing attributes triggers lazy loading which fails in async context with `MissingGreenlet` error.

### The Pattern: Extract → Flush → Commit

```python
@app.post("/api/tasks", response_model=TaskRead, status_code=201)
async def create_task(
    task: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    # 1. Extract primitives from user BEFORE any commits
    actor_id = current_user["id"]

    # 2. Create entity and flush to get ID
    db_task = Task.model_validate(task)
    session.add(db_task)
    await session.flush()
    task_id = db_task.id  # Extract immediately after flush

    # 3. Call services with primitives (NOT objects)
    await log_action(session, actor_id=actor_id, task_id=task_id)

    # 4. Single commit at end
    await session.commit()
    await session.refresh(db_task)
    return db_task
```

### Service Functions: Never Commit Internally

```python
# WRONG - breaks caller's transaction
async def log_action(session: AsyncSession, ...):
    log = AuditLog(...)
    session.add(log)
    await session.commit()  # ❌ Caller loses control

# CORRECT - caller owns transaction
async def log_action(session: AsyncSession, ...):
    log = AuditLog(...)
    session.add(log)
    return log  # No commit
```

### Input Validation for API Schemas

```python
from pydantic import field_validator
from datetime import UTC, datetime

class TaskCreate(SQLModel):
    assignee_id: int | None = None
    due_date: datetime | None = None

    @field_validator("assignee_id", mode="after")
    @classmethod
    def zero_to_none(cls, v: int | None) -> int | None:
        """Swagger UI sends 0 for empty int fields."""
        return None if v == 0 else v

    @field_validator("due_date", mode="after")
    @classmethod
    def normalize_datetime(cls, v: datetime | None) -> datetime | None:
        """Strip timezone for naive UTC database columns."""
        if v and v.tzinfo:
            return v.astimezone(UTC).replace(tzinfo=None)
        return v
```

## Testing with Pytest

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from main import app, get_session

@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    """Mock authenticated headers for testing."""
    return {"Authorization": "Bearer test-token"}

# tests/test_tasks.py
def test_create_task(client, auth_headers, mocker):
    # Mock auth
    mocker.patch("auth.get_current_user", return_value={"id": "@testuser"})

    response = client.post(
        "/api/tasks",
        json={"title": "Test Task"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"
```

## Common Patterns

### Error Handling

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
        },
    )

# Validation errors are handled automatically by Pydantic
# Returns 422 with detailed error messages
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Health Check

```python
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/health/db")
def db_health(session: Session = Depends(get_session)):
    try:
        session.exec(select(1))
        return {"database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")
```

## References

For additional documentation, use Context7 MCP:
```
mcp__context7__resolve-library-id with libraryName="fastapi"
mcp__context7__get-library-docs with topic="authentication" or "sqlmodel"
```

See also: `references/jwt-verification.md` for detailed JWKS patterns.

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# Auth
AUTH_SERVER_URL=http://localhost:3001
JWKS_URL=http://localhost:3001/api/auth/jwks

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Optional
LOG_LEVEL=INFO
```
