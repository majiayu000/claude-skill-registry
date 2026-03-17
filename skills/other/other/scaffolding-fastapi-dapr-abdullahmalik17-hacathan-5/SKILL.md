---
name: scaffolding-fastapi-dapr
description: |
  Build production-grade FastAPI backends with SQLModel, Dapr integration, and JWT authentication.
  Use when building REST APIs with Neon PostgreSQL, implementing event-driven microservices with
  Dapr pub/sub, scheduling jobs, or creating CRUD endpoints with JWT/JWKS verification.
  NOT when building simple scripts or non-microservice architectures.
---

# FastAPI + Dapr Backend

Build production-grade FastAPI backends with SQLModel, Dapr integration, and JWT authentication.

## Quick Start

```bash
# Project setup
uv init backend && cd backend
uv add fastapi sqlmodel pydantic httpx python-jose uvicorn

# Development
uv run uvicorn main:app --reload --port 8000

# With Dapr sidecar
dapr run --app-id myapp --app-port 8000 -- uvicorn main:app
```

---

## FastAPI Core Patterns

### 1. SQLModel Schema (Database + API)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, Literal

class TaskBase(SQLModel):
    title: str = Field(max_length=200, index=True)
    status: Literal["pending", "in_progress", "completed"] = "pending"

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    created_at: datetime
```

### 2. Async Database Setup

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DATABASE_URL)

async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session
```

### 3. CRUD Endpoints

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select

app = FastAPI()

@app.post("/tasks", response_model=TaskRead, status_code=201)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    db_task = Task.model_validate(task)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, update: TaskUpdate, session: AsyncSession = Depends(get_session)):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    update_data = update.model_dump(exclude_unset=True)
    task.sqlmodel_update(update_data)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

### 4. JWT/JWKS Authentication

```python
from jose import jwt
import httpx

JWKS_URL = f"{SSO_URL}/.well-known/jwks.json"

async def get_current_user(authorization: str = Header()):
    token = authorization.replace("Bearer ", "")
    async with httpx.AsyncClient() as client:
        jwks = (await client.get(JWKS_URL)).json()
    payload = jwt.decode(token, jwks, algorithms=["RS256"])
    return payload

@app.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    return {"user": user["sub"]}
```

See [references/fastapi-patterns.md](references/fastapi-patterns.md) for audit logging, pagination, and OpenAPI configuration.

---

## Dapr Integration Patterns

### 1. Pub/Sub Subscription

```python
from fastapi import APIRouter, Request

router = APIRouter(prefix="/dapr", tags=["Dapr"])

@router.get("/subscribe")
async def subscribe():
    """Dapr calls this to discover subscriptions."""
    return [{
        "pubsubname": "pubsub",
        "topic": "task-created",
        "route": "/dapr/task-created"
    }]

@router.post("/task-created")
async def handle_task_created(request: Request, session: AsyncSession = Depends(get_session)):
    # CloudEvent wrapper - data is nested
    event = await request.json()
    task_data = event.get("data", event)  # Handle both wrapped and unwrapped

    # Process event
    task = Task.model_validate(task_data)
    session.add(task)
    await session.commit()
    return {"status": "processed"}
```

### 2. Publishing Events

```python
import httpx

DAPR_URL = "http://localhost:3500"

async def publish_event(topic: str, data: dict):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{DAPR_URL}/v1.0/publish/pubsub/{topic}",
            json=data,
            headers={"Content-Type": "application/json"}
        )
```

### 3. Scheduled Jobs

```python
# Schedule a job via Dapr Jobs API (alpha)
async def schedule_job(name: str, schedule: str, callback_url: str, data: dict):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{DAPR_URL}/v1.0-alpha1/jobs/{name}",
            json={
                "schedule": schedule,  # "@every 5m" or "0 */5 * * * *"
                "data": data,
            },
            headers={"dapr-app-callback-url": callback_url}
        )

# Job callback endpoint
@app.post("/jobs/process")
async def process_job(request: Request):
    job_data = await request.json()
    # Handle job execution
    return {"status": "completed"}
```

See [references/dapr-patterns.md](references/dapr-patterns.md) for state management and advanced patterns.

---

## Production Patterns

### Structured Logging

```python
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
log = structlog.get_logger()
log.info("task_created", task_id=task.id, user_id=user["sub"])
```

### Repository + Service Pattern

```python
# Repository: data access only
class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: TaskCreate) -> Task:
        db_task = Task.model_validate(task)
        self.session.add(db_task)
        await self.session.commit()
        return db_task

# Service: business logic
class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, task: TaskCreate, user_id: str) -> Task:
        # Business logic here
        return await self.repo.create(task)

# Dependency injection
def get_task_service(session: AsyncSession = Depends(get_session)):
    return TaskService(TaskRepository(session))
```

### Async Testing

```python
@pytest.fixture
async def client(session):
    app.dependency_overrides[get_session] = lambda: session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.mark.anyio
async def test_create_task(client: AsyncClient):
    response = await client.post("/tasks", json={"title": "Test"})
    assert response.status_code == 201
```

See [references/production-testing.md](references/production-testing.md) for full patterns.

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   ├── database.py       # Async engine + session
│   ├── models/           # SQLModel schemas
│   ├── routers/          # API routes
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic
│   └── dapr/             # Dapr handlers
├── tests/
│   ├── conftest.py       # Fixtures
│   └── test_*.py         # Test files
├── components/           # Dapr components (k8s)
│   ├── pubsub.yaml
│   └── statestore.yaml
└── pyproject.toml
```

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ scaffolding-fastapi-dapr skill ready`

## If Verification Fails

1. Check: references/ folder has both pattern files
2. **Stop and report** if still failing

## Related Skills

- **configuring-better-auth** - JWT/JWKS auth for API endpoints
- **fetching-library-docs** - FastAPI docs: `--library-id /fastapi/fastapi --topic dependencies`

## References

- [references/fastapi-patterns.md](references/fastapi-patterns.md) - Complete FastAPI backend patterns
- [references/dapr-patterns.md](references/dapr-patterns.md) - Dapr pub/sub, state, and jobs
- [references/sqlmodel-patterns.md](references/sqlmodel-patterns.md) - SQLModel database patterns and migrations
- [references/production-testing.md](references/production-testing.md) - Structured logging, DI, testing, versioning
