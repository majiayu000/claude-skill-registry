---
name: fastapi-patterns
description: FastAPI development patterns - dependency injection, middleware, background tasks, Pydantic models, authentication, and production deployment. Auto-triggers when working with FastAPI.
---

# FastAPI Patterns Skill

## Application Structure

```
src/
├── main.py              # App creation and startup
├── config.py            # Settings via pydantic-settings
├── models/              # Pydantic models (request/response)
│   ├── __init__.py
│   └── user.py
├── routes/              # API route handlers
│   ├── __init__.py
│   └── users.py
├── services/            # Business logic
│   ├── __init__.py
│   └── user_service.py
├── db/                  # Database layer
│   ├── __init__.py
│   ├── session.py
│   └── models.py        # SQLAlchemy models
└── middleware/
    └── auth.py
```

## Pydantic Models

### Request/Response Separation

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Input model (what the client sends)
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)

# Output model (what the API returns)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}

# Update model (partial updates)
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
```

### Settings with pydantic-settings

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379"
    secret_key: str
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env"}

settings = Settings()
```

## Route Handlers

### CRUD Routes

```python
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 20,
    active: bool = True,
    db: AsyncSession = Depends(get_db),
):
    return await user_service.list_users(db, skip=skip, limit=limit, active=active)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, data)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
```

## Dependency Injection

### Database Session

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = verify_jwt(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    user = await user_service.get_user(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Use in routes
@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return user
```

### Composable Dependencies

```python
async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    return user

@router.delete("/users/{user_id}")
async def admin_delete(
    user_id: int,
    admin: User = Depends(require_admin),  # Chains with get_current_user
):
    ...
```

## Middleware

### CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Request Logging

```python
import time
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    logger.info(
        "%s %s %d %.3fs",
        request.method, request.url.path, response.status_code, duration,
    )
    return response
```

## Background Tasks

```python
from fastapi import BackgroundTasks

async def send_welcome_email(email: str, name: str):
    # Long-running task runs after response is sent
    await email_service.send(email, "Welcome!", f"Hi {name}")

@router.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(
    data: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.create_user(db, data)
    background_tasks.add_task(send_welcome_email, user.email, user.name)
    return user
```

## Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": type(exc).__name__, "message": exc.message}},
    )
```

## Production Deployment

```bash
# Run with uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

# Behind nginx/reverse proxy
uvicorn src.main:app --host 127.0.0.1 --port 8000 --proxy-headers --forwarded-allow-ips="*"
```

### Health Check

```python
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"status": "ready"}
```

## Activation Triggers

This skill auto-activates when prompts contain:

- "fastapi", "fast api"
- "uvicorn", "starlette"
- "pydantic", "basemodel", "pydantic-settings"
- "dependency injection", "depends"
- "api route", "router", "endpoint"

## Integration

- **api-design** skill: REST/GraphQL design principles
- **database-patterns** skill: Database layer patterns
- **async-patterns** skill: Async Python patterns
- **@python-pro** agent: Python expertise
- **@backend-architect** agent: Architecture decisions
