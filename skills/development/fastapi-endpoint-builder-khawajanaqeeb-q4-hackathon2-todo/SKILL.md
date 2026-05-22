---
name: "FastAPI Endpoint Builder"
description: "Create secure FastAPI routes for task CRUD with search/filter/sort query params and JWT auth when backend endpoints are needed"
version: "1.0.0"
---

# FastAPI Endpoint Builder Skill

## Purpose

Automatically generate production-ready FastAPI backend endpoints with proper authentication, user isolation, input validation, and error handling when the user requests API implementation for the Phase II full-stack todo application.

## When This Skill Triggers

Use this skill when the user asks to:
- "Create an API endpoint for todos"
- "Build the todo CRUD routes"
- "Add search and filter to the API"
- "Implement the backend for task management"
- "Create authenticated endpoints"
- Any request to build backend API routes or endpoints

## Prerequisites

Before generating endpoints:
1. Read `specs/phase-2/spec.md` for API requirements
2. Read `.specify/memory/constitution.md` for backend standards
3. Verify FastAPI project exists in `backend/` directory
4. Ensure database models (SQLModel) are defined
5. Confirm JWT auth utilities exist

## Step-by-Step Procedure

### Step 1: Analyze Requirements
- Identify resource (e.g., todos, users)
- Determine operations needed (Create, Read, Update, Delete)
- Check for filtering, sorting, pagination requirements
- Verify authentication requirements
- Review user isolation needs

### Step 2: Create Pydantic Schemas

Define request/response models in `app/schemas/`:

```python
# app/schemas/todo.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    """Base todo schema with common fields."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    tags: list[str] = Field(default_factory=list)

class TodoCreate(TodoBase):
    """Schema for creating a new todo."""
    pass

class TodoUpdate(BaseModel):
    """Schema for updating a todo (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    tags: Optional[list[str]] = None
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    """Schema for todo response."""
    id: int
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Step 3: Create Router with CRUD Operations

Generate router in `app/routers/`:

```python
# app/routers/todos.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col
from typing import List, Optional
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_session
from app.models.user import User
from datetime import datetime

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

@router.post(
    "/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
)
async def create_todo(
    todo_data: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new todo for the authenticated user.

    - **title**: Required, 1-500 characters
    - **description**: Optional, max 5000 characters
    - **priority**: low, medium (default), or high
    - **tags**: Optional array of strings
    """
    todo = Todo(
        **todo_data.model_dump(),
        user_id=current_user.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.get(
    "/",
    response_model=List[TodoResponse],
    summary="Get all todos with optional filters",
)
async def get_todos(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max records to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, pattern="^(low|medium|high)$", description="Filter by priority"),
    search: Optional[str] = Query(None, max_length=100, description="Search in title"),
    sort_by: str = Query("created_at", pattern="^(created_at|priority|title)$", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get all todos for the authenticated user with optional filtering, search, sorting, and pagination.

    **Filters:**
    - `completed`: Filter by completion status (true/false)
    - `priority`: Filter by priority (low/medium/high)
    - `search`: Search in title (case-insensitive)

    **Pagination:**
    - `skip`: Offset (default: 0)
    - `limit`: Max results (default: 100, max: 100)

    **Sorting:**
    - `sort_by`: Field to sort by (created_at, priority, title)
    - `sort_order`: asc or desc (default: desc)
    """
    # Base query with user isolation
    query = select(Todo).where(Todo.user_id == current_user.id)

    # Apply filters
    if completed is not None:
        query = query.where(Todo.completed == completed)
    if priority:
        query = query.where(Todo.priority == priority)
    if search:
        query = query.where(col(Todo.title).contains(search))

    # Apply sorting
    sort_column = getattr(Todo, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    query = query.offset(skip).limit(limit)

    todos = session.exec(query).all()
    return todos

@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Get a specific todo by ID",
)
async def get_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific todo by ID.

    **User Isolation:** Users can only access their own todos.
    """
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    # CRITICAL: Enforce user isolation
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return todo

@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Update a todo",
)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Update a todo's fields.

    Only provided fields will be updated. User isolation enforced.
    """
    todo = session.get(Todo, todo_id)

    if not todo or todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    # Update only provided fields
    update_data = todo_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
)
async def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a todo.

    User isolation enforced - users can only delete their own todos.
    """
    todo = session.get(Todo, todo_id)

    if not todo or todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    session.delete(todo)
    session.commit()
    return None

@router.post(
    "/{todo_id}/toggle",
    response_model=TodoResponse,
    summary="Toggle todo completion status",
)
async def toggle_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Toggle a todo's completion status (completed ↔ pending).
    """
    todo = session.get(Todo, todo_id)

    if not todo or todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    todo.completed = not todo.completed
    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
```

### Step 4: Register Router in Main App

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import todos, auth

app = FastAPI(
    title="Todo API",
    version="2.0.0",
    description="Phase II Full-Stack Todo Application API",
)

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)

@app.get("/")
async def root():
    return {"message": "Todo API v2.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Step 5: Add Input Validation

Use Pydantic validators for complex validation:

```python
from pydantic import field_validator

class TodoCreate(TodoBase):
    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()

    @field_validator("tags")
    @classmethod
    def tags_unique(cls, v: list[str]) -> list[str]:
        if len(v) != len(set(v)):
            raise ValueError("Tags must be unique")
        return list(set(v))

    @field_validator("tags")
    @classmethod
    def tags_max_count(cls, v: list[str]) -> list[str]:
        if len(v) > 10:
            raise ValueError("Maximum 10 tags allowed")
        return v
```

## Output Format

### Generated Files Structure
```
backend/
├── app/
│   ├── main.py                    # Updated with router
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── todos.py              # Generated router
│   │   └── auth.py               # Auth router
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── todo.py               # Generated schemas
│   │   └── user.py
│   └── dependencies/
│       ├── auth.py               # get_current_user
│       └── database.py           # get_session
```

### API Documentation

FastAPI auto-generates OpenAPI docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Quality Criteria

**Security (CRITICAL):**
- ✅ User isolation enforced on ALL operations
- ✅ JWT authentication required (Depends(get_current_user))
- ✅ No user can access another user's data
- ✅ Proper HTTP status codes (401, 403, 404)
- ✅ Input validation with Pydantic

**Performance:**
- ✅ Async operations (async def)
- ✅ Efficient queries (avoid N+1)
- ✅ Pagination for list endpoints
- ✅ Indexes on filtered/sorted columns

**Code Quality:**
- ✅ Type hints on all functions
- ✅ Docstrings with parameter descriptions
- ✅ Proper error handling
- ✅ DRY principles (no code duplication)

**API Design:**
- ✅ RESTful conventions
- ✅ Consistent response structures
- ✅ Clear parameter descriptions
- ✅ OpenAPI documentation complete

## Testing

Generate test file alongside router:

```python
# tests/test_todos_api.py
import pytest
from fastapi.testclient import TestClient

def test_create_todo_requires_auth(client):
    """Ensure endpoint requires authentication."""
    response = client.post("/todos", json={"title": "Test"})
    assert response.status_code == 401

def test_create_todo_with_valid_data(client, auth_headers):
    """Test creating todo with valid data."""
    response = client.post(
        "/todos",
        json={"title": "Buy groceries", "priority": "high"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["priority"] == "high"

def test_get_todos_filters_by_user(client, test_user, other_user, auth_headers):
    """Ensure users only see their own todos."""
    # Create todos for both users
    # ... setup code ...

    response = client.get("/todos", headers=auth_headers)
    todos = response.json()

    # Verify only test_user's todos returned
    assert all(todo["user_id"] == test_user.id for todo in todos)

def test_user_cannot_update_other_user_todo(client, auth_headers, other_todo):
    """Security test: user isolation on update."""
    response = client.put(
        f"/todos/{other_todo.id}",
        json={"title": "Hacked"},
        headers=auth_headers,
    )
    assert response.status_code == 404
```

## Examples

### Example 1: Simple CRUD Endpoint

**User Request:** "Create todo CRUD endpoints"

**Generated:** Complete router with Create, Read, Update, Delete operations (see Step 3 above)

### Example 2: Advanced Filtering

**User Request:** "Add search and filter to todos API"

**Generated Query Parameters:**
```python
@router.get("/")
async def get_todos(
    search: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    completed: Optional[bool] = Query(None),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    ...
):
    query = select(Todo).where(Todo.user_id == current_user.id)

    if search:
        query = query.where(col(Todo.title).contains(search))
    if priority:
        query = query.where(Todo.priority == priority)
    if completed is not None:
        query = query.where(Todo.completed == completed)
    if tags:
        tag_list = tags.split(",")
        # Filter todos that have ANY of the specified tags
        query = query.where(col(Todo.tags).overlap(tag_list))

    return session.exec(query).all()
```

### Example 3: Batch Operations

**User Request:** "Add endpoint to mark multiple todos complete"

**Generated:**
```python
@router.post("/batch/complete", response_model=dict)
async def batch_complete_todos(
    todo_ids: list[int],
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Mark multiple todos as complete in one request."""
    if len(todo_ids) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 50 todos per batch operation",
        )

    # Fetch todos with user isolation
    todos = session.exec(
        select(Todo)
        .where(Todo.id.in_(todo_ids))
        .where(Todo.user_id == current_user.id)
    ).all()

    # Update completion status
    for todo in todos:
        todo.completed = True
        todo.updated_at = datetime.utcnow()

    session.commit()

    return {
        "updated_count": len(todos),
        "requested_ids": todo_ids,
    }
```

## Success Indicators

The skill execution is successful when:
- ✅ All endpoints return proper HTTP status codes
- ✅ User isolation verified (cannot access other users' data)
- ✅ Input validation working (rejects invalid data)
- ✅ OpenAPI docs generated correctly
- ✅ Tests pass for authentication and CRUD operations
- ✅ No security vulnerabilities (SQL injection, XSS)
- ✅ Async operations used throughout
- ✅ Error messages are user-friendly
