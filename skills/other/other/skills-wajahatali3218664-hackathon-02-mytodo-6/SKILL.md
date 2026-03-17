---
name: fastapi-backend-skill
description: Create and manage FastAPI routes, dependencies, and models
when-to-use: Adding new API endpoints, auth, database operations
---
# FastAPI Backend Skill

## Instructions

This skill provides guidance for building and maintaining the FastAPI backend for the Todo Web Application.

### Project Structure
```
backend/
├── main.py              # Application entry point
├── config.py            # Environment configuration
├── auth/
│   ├── __init__.py
│   ├── service.py       # Auth business logic
│   ├── dependencies.py  # Auth dependencies (OAuth2PasswordBearer, etc.)
│   └── routes.py        # Auth endpoints (/auth/register, /auth/login)
├── tasks/
│   ├── __init__.py
│   ├── models.py        # Pydantic models for tasks
│   ├── service.py       # Task CRUD business logic
│   └── routes.py        # Task endpoints (/tasks)
└── users/
    ├── __init__.py
    ├── models.py        # User Pydantic models
    └── routes.py        # User endpoints (/users)
```

### Creating a New Route

1. **Define Pydantic Models** in `models.py`:
   ```python
   from pydantic import BaseModel
   from datetime import datetime
   from typing import Optional

   class TaskCreate(BaseModel):
       title: str
       description: Optional[str] = None
       due_date: Optional[datetime] = None

   class TaskResponse(TaskCreate):
       id: int
       created_at: datetime
       updated_at: datetime
       owner_id: int
   ```

2. **Create Service Layer** in `service.py`:
   ```python
   from sqlalchemy.ext.asyncio import AsyncSession
   from sqlalchemy import select
   from models import Task, TaskCreate

   async def create_task(db: AsyncSession, task: TaskCreate, owner_id: int):
       db_task = Task(**task.model_dump(), owner_id=owner_id)
       db.add(db_task)
       await db.commit()
       await db.refresh(db_task)
       return db_task

   async def get_tasks(db: AsyncSession, owner_id: int):
       result = await db.execute(
           select(Task).where(Task.owner_id == owner_id)
       )
       return result.scalars().all()
   ```

3. **Define Routes** in `routes.py`:
   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from sqlalchemy.ext.asyncio import AsyncSession
   from dependencies import get_db, get_current_user
   from service import create_task, get_tasks
   from models import TaskCreate, TaskResponse

   router = APIRouter()

   @router.post("/tasks", response_model=TaskResponse)
   async def create_task_endpoint(
       task: TaskCreate,
       db: AsyncSession = Depends(get_db),
       current_user = Depends(get_current_user)
   ):
       return await create_task(db, task, current_user.id)

   @router.get("/tasks", response_model=list[TaskResponse])
   async def get_tasks_endpoint(
       db: AsyncSession = Depends(get_db),
       current_user = Depends(get_current_user)
   ):
       return await get_tasks(db, current_user.id)
   ```

4. **Register Router** in `main.py`:
   ```python
   from fastapi import FastAPI
   from tasks.routes import router as tasks_router

   app = FastAPI()
   app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])
   ```

### Using Dependencies

```python
from fastapi import Depends, HTTPException, status
from auth.dependencies import get_current_user

@router.get("/tasks/{task_id}")
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = await get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

### Error Handling

```python
from fastapi import HTTPException

async def update_task(db, task_id, user_id, updates):
    task = await get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    if task.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    # Update logic...
    return task
```

### Environment Variables

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    OPENAI_API_KEY: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
```

## Examples

### Complete Task CRUD Example

```python
# backend/tasks/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.dependencies import get_current_user
from database import get_db
from models import TaskCreate, TaskUpdate, TaskResponse
from service import (
    create_task, get_task, get_tasks,
    update_task, delete_task
)

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await create_task(db, task, current_user.id)

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await get_tasks(db, current_user.id)

@router.get("/{task_id}", response_model=TaskResponse)
async def retrieve(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = await get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await update_task(db, task_id, task_update, current_user.id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    await delete_task(db, task_id, current_user.id)
```

### CORS Configuration

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Health Check Endpoint

```python
# main.py
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "todo-api"}
```
