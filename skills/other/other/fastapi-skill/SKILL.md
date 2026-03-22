---
name: fastapi-skill
description: Expert guidance on FastAPI backend development. Use when building or reviewing FastAPI applications requiring: (1) App structure and routing organization, (2) Pydantic models for request/response validation, (3) Dependency injection with Depends(), (4) CORS configuration for frontend integration, (5) Async route handlers, (6) SQLModel for database operations. Invoke when creating APIs, endpoints, middleware, or database integrations in FastAPI.
---

# FastAPI Development

Expert guidance for building modern FastAPI backends.

## Quick Start

### Minimal App

```python
from fastapi import FastAPI

app = FastAPI(title="Todo API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Run with Uvicorn

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Request/Response Models

```python
from pydantic import BaseModel, Field
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}

@app.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate) -> TaskResponse:
    # task is already validated
    new_task = await save_task(task)
    return new_task
```

## Dependency Injection

```python
from fastapi import Depends
from typing import Annotated

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

DB = Annotated[AsyncSession, Depends(get_db)]

@app.get("/tasks")
async def list_tasks(db: DB) -> list[TaskResponse]:
    tasks = await db.execute(select(Task))
    return tasks.scalars().all()
```

## CORS for Frontend

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Project Structure

```
src/
├── main.py              # FastAPI app creation
├── config.py            # Settings with pydantic-settings
├── routers/
│   ├── __init__.py
│   ├── tasks.py         # /tasks endpoints
│   └── users.py         # /users endpoints
├── models/
│   ├── __init__.py
│   ├── task.py          # SQLModel Task
│   └── user.py          # SQLModel User
├── schemas/
│   ├── __init__.py
│   ├── task.py          # Pydantic request/response
│   └── user.py
├── services/
│   ├── __init__.py
│   └── task_service.py  # Business logic
├── dependencies/
│   ├── __init__.py
│   ├── database.py      # DB session
│   └── auth.py          # Auth dependencies
└── database.py          # SQLModel engine setup
```

## Reference Guides

For detailed patterns, see:

- **App Structure**: See [references/app-structure.md](references/app-structure.md) for routing, routers, and middleware
- **Pydantic Models**: See [references/pydantic-models.md](references/pydantic-models.md) for validation and serialization
- **Dependency Injection**: See [references/dependency-injection.md](references/dependency-injection.md) for Depends() patterns
- **CORS Config**: See [references/cors-config.md](references/cors-config.md) for frontend integration
- **Async Handlers**: See [references/async-handlers.md](references/async-handlers.md) for async/await patterns
- **SQLModel**: See [references/sqlmodel-patterns.md](references/sqlmodel-patterns.md) for database operations
