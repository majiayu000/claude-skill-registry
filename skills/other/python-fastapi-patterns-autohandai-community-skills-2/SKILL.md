---
name: python-fastapi-patterns
description: FastAPI best practices, async patterns, and Pydantic validation
license: MIT
compatibility: python 3.11+, fastapi 0.100+, pydantic 2+
allowed-tools: read_file write_file apply_patch run_command
---

# Python FastAPI Patterns

## Project Structure

```
src/
├── main.py           # App entry point
├── config.py         # Settings management
├── dependencies.py   # Shared dependencies
├── models/           # Pydantic models
├── routes/           # API endpoints
├── services/         # Business logic
├── repositories/     # Data access
└── utils/            # Helpers
```

## Basic Setup

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(
    title="My API",
    version="1.0.0",
    lifespan=lifespan,
)
```

## Pydantic Models

```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=2, max_length=100)
```

## Route Organization

```python
# routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
):
    return await user_service.get_all(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = await user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    return await user_service.create(db, user_in)
```

## Dependency Injection

```python
# dependencies.py
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await user_service.get_by_id(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Type alias for cleaner signatures
CurrentUser = Annotated[User, Depends(get_current_user)]
```

## Async Patterns

```python
import asyncio
from httpx import AsyncClient

# Parallel requests
async def fetch_all_data(user_id: int):
    async with AsyncClient() as client:
        tasks = [
            client.get(f"/api/user/{user_id}"),
            client.get(f"/api/user/{user_id}/posts"),
            client.get(f"/api/user/{user_id}/stats"),
        ]
        results = await asyncio.gather(*tasks)
        return {
            "user": results[0].json(),
            "posts": results[1].json(),
            "stats": results[2].json(),
        }

# Background tasks
from fastapi import BackgroundTasks

@router.post("/notify")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(send_email, email)
    return {"message": "Notification queued"}
```

## Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {"code": exc.code, "message": exc.message}
        },
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {"code": "INTERNAL_ERROR", "message": "Something went wrong"}
        },
    )
```

## Settings Management

```python
# config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "My API"
    debug: bool = False
    database_url: str
    secret_key: str

    model_config = {"env_file": ".env"}

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## Middleware

```python
from fastapi import Request
from time import time
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time()
    response = await call_next(request)
    duration = time() - start

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.3f}s"
    )
    return response
```

## Testing

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/users/",
        json={"email": "test@example.com", "name": "Test", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

## Best Practices

1. **Use type hints everywhere** for auto-documentation
2. **Validate at boundaries** with Pydantic models
3. **Inject dependencies** for testability
4. **Handle errors consistently** with custom exceptions
5. **Use async/await** for I/O operations
6. **Keep routes thin** - business logic in services
7. **Document with OpenAPI** annotations
