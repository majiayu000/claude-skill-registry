---
name: fastapi-architecture
description: |
  This skill designs FastAPI application structure, routing, middleware, and separation of concerns. It establishes architectural patterns for building scalable, maintainable Python APIs that integrate with the monorepo structure and support authentication and data persistence requirements. Use when designing overall FastAPI application structure, planning API routing, or establishing middleware chains.
allowed-tools: Read, Grep, Glob
---

# FastAPI Architecture

## What This Skill Does

This skill designs FastAPI application structure, routing, middleware, and separation of concerns. It establishes architectural patterns for building scalable, maintainable Python APIs that integrate with the monorepo structure and support authentication and data persistence requirements.

## When to Use

- When designing the overall FastAPI application structure
- When planning API routing and endpoint organization
- When establishing middleware chains and request processing
- When defining dependency injection patterns
- When creating architectural plans for backend features
- When integrating authentication and authorization middleware

## When NOT to Use

- When the backend technology hasn't been confirmed as FastAPI
- When working on frontend components
- When designing database schemas (use sqlmodel-design)
- When implementing specific endpoint logic
- When specifications haven't been validated

## Required Clarifications

Before implementing FastAPI architecture, clarify:

1. **API Versioning**: Will you use path-based (v1, v2) or header-based versioning?
2. **Authentication Method**: JWT tokens, OAuth2, API keys, or custom scheme?
3. **Database Integration**: SQLAlchemy, SQLModel, Tortoise ORM, or other?
4. **Async Requirements**: Pure async, sync, or mixed approach?
5. **Deployment Target**: Docker containers, serverless, traditional hosting?

## Application Structure Patterns

### Factory Pattern Structure
```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── main.py             # FastAPI instance creation
│   ├── core/               # Core configurations
│   │   ├── config.py       # Settings and configuration
│   │   ├── security.py     # Security utilities
│   │   └── middleware.py   # Middleware definitions
│   ├── api/                # API routers
│   │   ├── deps.py         # Dependency injection
│   │   ├── v1/             # Version 1 endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── tasks.py
│   │   └── v2/             # Version 2 endpoints (if needed)
│   ├── models/             # Pydantic models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── auth.py
│   ├── schemas/            # Pydantic schemas
│   │   ├── user.py
│   │   └── task.py
│   ├── database/           # Database operations
│   │   ├── __init__.py
│   │   ├── session.py      # Session management
│   │   └── models.py       # SQLModel/SQLAlchemy models
│   └── services/           # Business logic
│       ├── __init__.py
│       ├── user_service.py
│       └── task_service.py
├── tests/
├── requirements.txt
└── alembic/
    └── versions/
```

### Application Factory Implementation
```python
# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import api_router
from app.core.middleware import setup_middleware
from app.core.security import setup_security

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
        if settings.DEBUG
        else None,
    )

    # Setup middleware
    setup_middleware(app)

    # Setup security
    setup_security(app)

    # Include API routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()
```

## Router Organization

### Feature-Based Routing
```python
# app/api/v1/__init__.py
from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .tasks import router as tasks_router

api_router = APIRouter()
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
```

### Dependency Injection Patterns
```python
# app/api/v1/deps.py
from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.core.security import verify_token

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
) -> User:
    """Get current user from token."""
    user = db.query(User).filter(User.id == token.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

CurrentUser = Depends(get_current_user)
```

## Middleware Chain Design

### Security Middleware
```python
# app/core/middleware.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

def setup_middleware(app: FastAPI) -> None:
    """Configure application middleware."""

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure based on environment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting middleware
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # Security headers middleware
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response
```

### Authentication Middleware
```python
# app/core/security.py
from fastapi import FastAPI, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings

security = HTTPBearer()

def setup_security(app: FastAPI) -> None:
    """Setup security configurations."""
    # Add security schemes to OpenAPI docs
    pass

def verify_token(credentials: HTTPAuthorizationCredentials = security) -> dict:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

## Error Handling Strategy

### Standardized Error Responses
```python
# app/models/errors.py
from typing import Optional
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[dict] = None

# app/core/exceptions.py
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.models.errors import ErrorResponse

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            error_code=f"HTTP_{exc.status_code}"
        ).dict()
    )

async def validation_exception_handler(request: Request, exc):
    """Handle request validation exceptions."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="Validation error",
            error_code="VALIDATION_ERROR",
            details={"errors": exc.errors()}
        ).dict()
    )
```

### Error Handler Registration
```python
# app/main.py (updated)
from fastapi import FastAPI
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler
)
from fastapi.exceptions import RequestValidationError

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
        if settings.DEBUG
        else None,
    )

    # Register exception handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler
    )

    # Setup middleware and routes...
    setup_middleware(app)
    setup_security(app)
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app
```

## Database Integration Patterns

### Session Management
```python
# app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Repository Pattern
```python
# app/database/repositories/base.py
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import handle_database_error

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: T, db_session: Session):
        self.model = model
        self.db = db_session

    def get(self, id: int) -> Optional[T]:
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            handle_database_error(e)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        try:
            return self.db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            handle_database_error(e)
```

## API Response Standardization

### Response Models
```python
# app/models/responses.py
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from datetime import datetime

T = TypeVar('T')

class BaseResponse(BaseModel):
    success: bool = True
    timestamp: datetime = datetime.utcnow()

class SingleResponse(BaseResponse, Generic[T]):
    data: T

class ListResponse(BaseResponse, Generic[T]):
    data: List[T]
    total: int
    page: Optional[int] = None
    limit: Optional[int] = None

class MessageResponse(BaseResponse):
    message: str
```

### Standard Response Usage
```python
# app/api/v1/tasks.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.task_service import TaskService
from app.models.responses import SingleResponse, ListResponse
from app.models.task import Task

router = APIRouter()

@router.get("/{task_id}", response_model=SingleResponse[Task])
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = await TaskService.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return SingleResponse(data=task)

@router.get("/", response_model=ListResponse[Task])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    tasks, total = await TaskService.get_tasks(db, skip, limit)

    return ListResponse(data=tasks, total=total, page=skip//limit + 1, limit=limit)
```

## Performance Optimization

### Caching Strategies
```python
# app/core/cache.py
import redis
from typing import Optional, Any
import pickle
from app.core.config import settings

class Cache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=False
        )

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            data = self.redis_client.get(key)
            if data:
                return pickle.loads(data)
        except:
            pass
        return None

    def set(self, key: str, value: Any, expire: int = 3600):
        """Set value in cache."""
        try:
            serialized = pickle.dumps(value)
            self.redis_client.setex(key, expire, serialized)
        except:
            pass
```

### Background Tasks
```python
# app/api/v1/tasks.py (updated)
from fastapi import BackgroundTasks
from app.core.background import send_notification

@router.post("/", response_model=SingleResponse[Task])
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = await TaskService.create_task(db, task_data, current_user.id)

    # Send notification in background
    background_tasks.add_task(
        send_notification,
        user_id=current_user.id,
        message=f"New task created: {task.title}"
    )

    return SingleResponse(data=task)
```

## Security Best Practices

### Input Validation
```python
# app/models/task.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()
```

### Rate Limiting
```python
# app/api/v1/tasks.py (updated)
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

@router.get("/", response_model=ListResponse[Task])
@limiter.limit("10/minute")
async def get_tasks(
    request: Request,  # Required for rate limiting
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # Implementation
    pass
```

## Testing Strategy

### Test Structure
```
tests/
├── conftest.py             # Test fixtures
├── test_main.py            # Application tests
├── api/
│   ├── test_auth.py        # Authentication tests
│   ├── test_users.py       # User endpoint tests
│   └── test_tasks.py       # Task endpoint tests
├── services/
│   ├── test_user_service.py
│   └── test_task_service.py
└── database/
    └── test_models.py
```

### Test Example
```python
# tests/api/test_tasks.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import get_db
from app.models.task import Task

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    # Create mock database session
    pass

def test_create_task():
    response = client.post("/api/v1/tasks/", json={
        "title": "Test task",
        "description": "Test description"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == "Test task"
```

## Anti-Patterns to Avoid

- **God Router**: Single router handling all endpoints
- **Middleware Bypass**: Authenticated endpoints without auth middleware
- **Direct DB Access**: Controllers directly querying database without service layer
- **Response Inconsistency**: Different response formats across endpoints
- **Error Leakage**: Exposing stack traces or internal details in responses
- **Tight Coupling**: Routers depending directly on concrete implementations
- **Configuration Chaos**: Settings scattered across multiple locations

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions to integrate with |
| **Conversation** | User's specific requirements, constraints, preferences |
| **Skill References** | Domain patterns from `references/` (library docs, best practices, examples) |
| **User Guidelines** | Project-specific conventions, team standards |

## Interaction With Other Skills

- **python-backend-structure**: Operates within defined backend directory structure
- **rest-api-design**: Implements REST conventions in FastAPI routers
- **jwt-verification**: Integrates JWT middleware into FastAPI
- **sqlmodel-design**: Coordinates with database models for data access
- **monorepo-architecture**: Fits within monorepo backend layer

## Phase Applicability

Phase II only. Phase I uses console-based Python without API framework.
