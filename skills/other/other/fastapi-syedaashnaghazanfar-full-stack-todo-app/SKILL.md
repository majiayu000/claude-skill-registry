---
name: fastapi
description: FastAPI patterns for building high-performance Python APIs. Covers routing, dependency injection, Pydantic models, background tasks, WebSockets, testing, and production deployment.
---

# FastAPI Skill

Modern FastAPI patterns for building high-performance Python APIs.

## Quick Start

### Installation

```bash
# pip
pip install fastapi uvicorn[standard]

# poetry
poetry add fastapi uvicorn[standard]

# uv
uv add fastapi uvicorn[standard]
```

### Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI app entry
├── config.py            # Settings/configuration
├── database.py          # DB connection
├── models/              # SQLModel/SQLAlchemy models
│   ├── __init__.py
│   └── task.py
├── schemas/             # Pydantic schemas
│   ├── __init__.py
│   └── task.py
├── routers/             # API routes
│   ├── __init__.py
│   └── tasks.py
├── services/            # Business logic
│   ├── __init__.py
│   └── task_service.py
├── dependencies/        # Shared dependencies
│   ├── __init__.py
│   └── auth.py
└── tests/
    └── test_tasks.py
```

## Key Concepts

| Concept | Guide |
|---------|-------|
| **Routing** | [reference/routing.md](reference/routing.md) |
| **Dependencies** | [reference/dependencies.md](reference/dependencies.md) |
| **Pydantic Models** | [reference/pydantic.md](reference/pydantic.md) |
| **Background Tasks** | [reference/background-tasks.md](reference/background-tasks.md) |
| **WebSockets** | [reference/websockets.md](reference/websockets.md) |

## Examples

| Pattern | Guide |
|---------|-------|
| **CRUD Operations** | [examples/crud.md](examples/crud.md) |
| **Authentication** | [examples/authentication.md](examples/authentication.md) |
| **File Upload** | [examples/file-upload.md](examples/file-upload.md) |
| **Testing** | [examples/testing.md](examples/testing.md) |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/main.py](templates/main.py) | App entry point |
| [templates/router.py](templates/router.py) | Router template |
| [templates/config.py](templates/config.py) | Settings with Pydantic |

## Basic App

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

## Routers

```python
# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate
from app.dependencies.auth import get_current_user, User

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
async def get_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Task).where(Task.user_id == user.id)
    return session.exec(statement).all()


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = Task(**task_data.model_dump(), user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
```

## Dependency Injection

```python
# app/dependencies/auth.py
from fastapi import Depends, HTTPException, Header
from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str

async def get_current_user(
    authorization: str = Header(..., alias="Authorization")
) -> User:
    # Verify JWT token
    # ... verification logic ...
    return User(id="user_123", email="user@example.com")


def require_role(role: str):
    async def checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
```

## Pydantic Schemas

```python
# app/schemas/task.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic
    pass

@router.post("/notify")
async def notify(
    email: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(send_email, email, "Hello!")
    return {"message": "Notification queued"}
```

## Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str
    better_auth_url: str = "http://localhost:3000"
    debug: bool = False

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## Error Handling

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
```

## Testing

```python
# tests/test_tasks.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_task(auth_headers):
    response = client.post(
        "/api/tasks",
        json={"title": "Test task"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"
```
