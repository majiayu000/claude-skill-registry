---
name: fastapi-patterns
description: Automatically applies when creating FastAPI endpoints, routers, and API structures. Enforces best practices for endpoint definitions, dependency injection, error handling, and documentation.
---

# FastAPI Endpoint Pattern Enforcer

When building APIs with FastAPI, follow these patterns for consistent, well-documented, and maintainable endpoints.

## ✅ Correct Pattern

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1/users", tags=["users"])


class UserCreate(BaseModel):
    """Request model for user creation."""
    email: str
    name: str
    age: Optional[int] = None


class UserResponse(BaseModel):
    """Response model for user endpoints."""
    id: str
    email: str
    name: str
    created_at: str


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "Email already registered"},
        422: {"description": "Validation error"}
    }
)
async def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends()
) -> UserResponse:
    """
    Create a new user account.

    - **email**: Valid email address
    - **name**: User's full name
    - **age**: Optional user age
    """
    try:
        return await user_service.create(user)
    except DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
```

## Router Organization

```python
from fastapi import APIRouter

# Organize endpoints by resource
users_router = APIRouter(prefix="/api/v1/users", tags=["users"])
products_router = APIRouter(prefix="/api/v1/products", tags=["products"])
orders_router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

# Register routers in main app
app = FastAPI()
app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)
```

## Dependency Injection

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Extract and validate current user from token."""
    token = credentials.credentials
    user = await verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user


async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify user has admin privileges."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


# Use in endpoints
@router.get("/admin-only")
async def admin_endpoint(
    admin: User = Depends(get_admin_user)
) -> dict:
    """Admin-only endpoint."""
    return {"message": "Admin access granted"}
```

## Request Validation

```python
from fastapi import Query, Path, Body
from pydantic import Field

@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, min_length=1, max_length=100),
    sort_by: str = Query("created_at", regex="^(name|email|created_at)$")
) -> list[UserResponse]:
    """List users with pagination and filtering."""
    return await user_service.list(
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by
    )


@router.get("/users/{user_id}")
async def get_user(
    user_id: str = Path(..., min_length=1, description="User ID")
) -> UserResponse:
    """Get user by ID."""
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user


@router.patch("/users/{user_id}")
async def update_user(
    user_id: str = Path(...),
    update: dict = Body(..., example={"name": "New Name"})
) -> UserResponse:
    """Partially update user."""
    return await user_service.update(user_id, update)
```

## Error Handling

```python
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Service layer exceptions
class ServiceError(Exception):
    """Base service exception."""
    pass


class NotFoundError(ServiceError):
    """Resource not found."""
    pass


class DuplicateError(ServiceError):
    """Duplicate resource."""
    pass


# Convert service exceptions to HTTP exceptions
@router.post("/users")
async def create_user(user: UserCreate) -> UserResponse:
    """Create user with proper error handling."""
    try:
        return await user_service.create(user)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(ServiceError)
async def service_exception_handler(request, exc):
    """Handle service errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
```

## Response Models

```python
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    has_next: bool


class SuccessResponse(BaseModel):
    """Generic success response."""
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str
    code: Optional[str] = None


@router.get(
    "/users",
    response_model=PaginatedResponse[UserResponse]
)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
) -> PaginatedResponse[UserResponse]:
    """List users with pagination."""
    users, total = await user_service.list_paginated(page, page_size)
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        has_next=total > page * page_size
    )
```

## Async Operations

```python
import httpx
from fastapi import BackgroundTasks


async def fetch_external_data(user_id: str) -> dict:
    """Fetch data from external service."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        response.raise_for_status()
        return response.json()


async def send_email(email: str, subject: str, body: str):
    """Send email asynchronously."""
    # Email sending logic
    pass


@router.post("/users/{user_id}/notify")
async def notify_user(
    user_id: str,
    background_tasks: BackgroundTasks
) -> SuccessResponse:
    """Notify user via email in background."""
    user = await user_service.get(user_id)

    # Add task to background
    background_tasks.add_task(
        send_email,
        email=user.email,
        subject="Notification",
        body="You have a new notification"
    )

    return SuccessResponse(message="Notification scheduled")
```

## OpenAPI Documentation

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="Comprehensive API for user management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


@router.post(
    "/users",
    summary="Create user",
    description="Create a new user with email and name",
    response_description="Created user object",
    tags=["users"],
    responses={
        201: {
            "description": "User created",
            "content": {
                "application/json": {
                    "example": {
                        "id": "usr_123",
                        "email": "user@example.com",
                        "name": "John Doe"
                    }
                }
            }
        },
        409: {"description": "Email already exists"}
    }
)
async def create_user(user: UserCreate) -> UserResponse:
    """
    Create a new user.

    Parameters:
    - **email**: User email address (required)
    - **name**: User full name (required)
    """
    return await user_service.create(user)
```

## Middleware

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Custom middleware
class TimingMiddleware(BaseHTTPMiddleware):
    """Log request timing."""

    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        response.headers["X-Process-Time"] = str(duration)
        return response


app.add_middleware(TimingMiddleware)
```

## ❌ Anti-Patterns

```python
# ❌ No type hints
@app.get("/users")
async def get_users():  # Missing return type and parameter types
    pass

# ✅ Better: full type hints
@app.get("/users")
async def get_users(
    page: int = Query(1)
) -> list[UserResponse]:
    pass


# ❌ No response model
@app.get("/users")
async def get_users() -> dict:  # Returns dict (no validation)
    return {"users": [...]}

# ✅ Better: use Pydantic response model
@app.get("/users", response_model=list[UserResponse])
async def get_users() -> list[UserResponse]:
    return await user_service.list()


# ❌ Generic exception handling
@app.post("/users")
async def create_user(user: UserCreate):
    try:
        return await user_service.create(user)
    except Exception:  # Too broad!
        raise HTTPException(500, "Error")

# ✅ Better: specific exception handling
@app.post("/users")
async def create_user(user: UserCreate):
    try:
        return await user_service.create(user)
    except DuplicateError as e:
        raise HTTPException(409, str(e))
    except ValidationError as e:
        raise HTTPException(422, str(e))


# ❌ Blocking I/O in async endpoint
@app.get("/data")
async def get_data():
    data = requests.get("https://api.example.com")  # Blocking!
    return data.json()

# ✅ Better: use async HTTP client
@app.get("/data")
async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()
```

## Best Practices Checklist

- ✅ Use `APIRouter` for organizing endpoints
- ✅ Define Pydantic models for requests and responses
- ✅ Add `response_model` to all endpoints
- ✅ Use appropriate HTTP status codes
- ✅ Document endpoints with docstrings
- ✅ Handle service exceptions and convert to HTTP exceptions
- ✅ Use dependency injection with `Depends()`
- ✅ Add validation to query/path/body parameters
- ✅ Use async/await for all I/O operations
- ✅ Add OpenAPI documentation
- ✅ Use background tasks for long-running operations
- ✅ Implement proper error responses

## Auto-Apply

When creating FastAPI endpoints:
1. Define request/response Pydantic models
2. Use `APIRouter` with prefix and tags
3. Add type hints to all parameters
4. Specify `response_model` and `status_code`
5. Document with docstring
6. Handle exceptions properly
7. Use `Depends()` for authentication and services

## References

For comprehensive examples, see:
- [Python Patterns Guide](../../../docs/python-patterns.md#fastapi-endpoints)
- [Pydantic Models Skill](../pydantic-models/SKILL.md)
- [Async/Await Patterns Skill](../async-await-checker/SKILL.md)

## Related Skills

- pydantic-models - For request/response models
- async-await-checker - For async endpoint patterns
- structured-errors - For error handling
- docstring-format - For endpoint documentation
