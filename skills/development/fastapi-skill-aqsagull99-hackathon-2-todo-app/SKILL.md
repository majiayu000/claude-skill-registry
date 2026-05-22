---
name: fastapi-skill
description: Reusable FastAPI skill with REST endpoint patterns, Pydantic models, dependencies, and async operations. Use for building Python web APIs.
---

# FastAPI Skill

Use this skill when building Python web APIs with FastAPI.

## Key Patterns

### Basic App Setup
```python
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to DB
    await connect_db()
    yield
    # Shutdown: close DB
    await close_db()

app = FastAPI(
    title="Todo API",
    description="API for managing tasks",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Path Parameters & Query Parameters
```python
from fastapi import Query, Path

@app.get("/tasks")
async def list_tasks(
    user_id: str = Query(...),
    status: str = Query(None, regex="^(all|pending|completed)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    return await get_tasks(user_id, status, skip, limit)

@app.get("/tasks/{task_id}")
async def get_task(
    task_id: int = Path(..., ge=1),
    user_id: str = Query(...),
):
    task = await get_task_by_id(task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

### Request Body with Pydantic
```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    completed: bool | None = None

@app.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    user_id: str = Query(...),
):
    task = await create_task(user_id, task_data.title, task_data.description)
    return task
```

### Dependencies
```python
from fastapi import Depends

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    token = credentials.credentials
    user_id = verify_jwt(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id

# Use in endpoint
@app.get("/tasks")
async def list_tasks(user_id: str = Depends(get_current_user)):
    return await get_tasks(user_id)
```

### Response Models
```python
from fastapi.response import JSONResponse

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@app.get("/tasks", response_model=list[TaskResponse])
async def list_tasks(user_id: str = Depends(get_current_user)):
    tasks = await get_tasks(user_id)
    return tasks
```

### Error Handling
```python
@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = await get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return task
```

### Async Database Operations
```python
from sqlalchemy.ext.asyncio import AsyncSession

async def get_tasks(user_id: str, db: AsyncSession) -> list[Task]:
    result = await db.execute(
        select(Task).where(Task.user_id == user_id)
    )
    return result.scalars().all()

# With pagination
async def get_tasks_paginated(
    user_id: str,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = None,
) -> list[Task]:
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Task.created_at.desc())
    )
    return result.scalars().all()
```

## Best Practices

1. Use async/await for I/O operations
2. Validate all inputs with Pydantic models
3. Use dependencies for reusable logic (auth, DB session)
4. Return proper HTTP status codes (201 for create, 204 for delete)
5. Add docstrings to all endpoints
6. Configure CORS for frontend origins
7. Use response_model for type hints
8. Handle exceptions with HTTPException
