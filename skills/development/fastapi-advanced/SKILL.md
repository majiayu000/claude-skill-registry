---
name: fastapi-advanced
description: FastAPI 2026 advanced patterns including lifespan, dependencies, middleware, and Pydantic settings. Use when configuring FastAPI lifespan events, creating dependency injection, building Starlette middleware, or managing async Python services with uvicorn.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [fastapi, python, async, middleware, dependencies, 2026]
author: SkillForge
user-invocable: false
---

# FastAPI Advanced Patterns (2026)

Production-ready FastAPI patterns for modern Python backends.

## Lifespan Management (2026)

### Modern Lifespan Context Manager

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import redis.asyncio as redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with resource management."""
    # Startup
    app.state.db_engine = create_async_engine(
        settings.database_url,
        pool_size=5,
        max_overflow=10,
    )
    app.state.redis = redis.from_url(settings.redis_url)

    # Health check connections
    async with app.state.db_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    await app.state.redis.ping()

    yield  # Application runs

    # Shutdown
    await app.state.db_engine.dispose()
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)
```

### Lifespan with Services

```python
from app.services import EmbeddingsService, LLMService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize services
    app.state.embeddings = EmbeddingsService(
        model=settings.embedding_model,
        batch_size=100,
    )
    app.state.llm = LLMService(
        providers=["openai", "anthropic"],
        default="anthropic",
    )

    # Warm up models (optional)
    await app.state.embeddings.warmup()

    yield

    # Cleanup
    await app.state.embeddings.close()
    await app.state.llm.close()
```

## Dependency Injection Patterns

### Database Session

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request

async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Yield database session from app state."""
    async with AsyncSession(
        request.app.state.db_engine,
        expire_on_commit=False,
    ) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Service Dependencies

```python
from functools import lru_cache

class AnalysisService:
    def __init__(
        self,
        db: AsyncSession,
        embeddings: EmbeddingsService,
        llm: LLMService,
    ):
        self.db = db
        self.embeddings = embeddings
        self.llm = llm

def get_analysis_service(
    db: AsyncSession = Depends(get_db),
    request: Request = None,
) -> AnalysisService:
    return AnalysisService(
        db=db,
        embeddings=request.app.state.embeddings,
        llm=request.app.state.llm,
    )

@router.post("/analyses")
async def create_analysis(
    data: AnalysisCreate,
    service: AnalysisService = Depends(get_analysis_service),
):
    return await service.create(data)
```

### Cached Dependencies

```python
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    api_key: str

    model_config = {"env_file": ".env"}

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Usage in dependencies
def get_db_url(settings: Settings = Depends(get_settings)) -> str:
    return settings.database_url
```

### Authenticated User

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_jwt(token)

    user = await db.get(User, payload["sub"])
    if not user:
        raise HTTPException(401, "Invalid credentials")
    return user

async def get_admin_user(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_admin:
        raise HTTPException(403, "Admin access required")
    return user
```

## Middleware Patterns

### Request ID Middleware

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestIDMiddleware)
```

### Timing Middleware

```python
import time
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        return response
```

### Structured Logging Middleware

```python
import structlog
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log = logger.bind(
            request_id=getattr(request.state, "request_id", None),
            method=request.method,
            path=request.url.path,
        )

        try:
            response = await call_next(request)
            log.info(
                "request_completed",
                status_code=response.status_code,
            )
            return response
        except Exception as exc:
            log.exception("request_failed", error=str(exc))
            raise
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Response-Time"],
)
```

## Settings with Pydantic

```python
from pydantic import Field, field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: PostgresDsn
    db_pool_size: int = Field(default=5, ge=1, le=20)
    db_max_overflow: int = Field(default=10, ge=0, le=50)

    # Redis
    redis_url: str = "redis://localhost:6379"

    # API
    api_key: str = Field(min_length=32)
    debug: bool = False

    # LLM
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    @field_validator("database_url", mode="before")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if v and "+asyncpg" not in v:
            return v.replace("postgresql://", "postgresql+asyncpg://")
        return v

    @property
    def async_database_url(self) -> str:
        return str(self.database_url)
```

## Exception Handlers

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ProblemException

@app.exception_handler(ProblemException)
async def problem_exception_handler(request: Request, exc: ProblemException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_problem_detail(),
        media_type="application/problem+json",
    )

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={
            "type": "https://api.example.com/problems/conflict",
            "title": "Conflict",
            "status": 409,
            "detail": "Resource already exists or constraint violated",
        },
        media_type="application/problem+json",
    )
```

## Response Optimization

```python
from fastapi.responses import ORJSONResponse

# Use orjson for faster JSON serialization
app = FastAPI(default_response_class=ORJSONResponse)

# Streaming response
from fastapi.responses import StreamingResponse

@router.get("/export")
async def export_data():
    async def generate():
        async for chunk in fetch_large_dataset():
            yield json.dumps(chunk) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
    )
```

## Health Checks

```python
from fastapi import APIRouter

health_router = APIRouter(tags=["health"])

@health_router.get("/health")
async def health_check(request: Request):
    checks = {}

    # Database
    try:
        async with request.app.state.db_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {e}"

    # Redis
    try:
        await request.app.state.redis.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {e}"

    status = "healthy" if all(v == "healthy" for v in checks.values()) else "unhealthy"
    return {"status": status, "checks": checks}
```

## Anti-Patterns (FORBIDDEN)

```python
# NEVER use global state
db_session = None  # Global mutable state!

# NEVER block the event loop
def sync_db_query():  # Blocking in async context!
    return session.query(User).all()

# NEVER skip dependency injection
@router.get("/users")
async def get_users():
    db = create_session()  # Creating session in route!
    return db.query(User).all()

# NEVER ignore lifespan cleanup
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = create_pool()
    yield
    # Missing cleanup! Pool never closed
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Lifespan | Use `asynccontextmanager` (not events) |
| Dependencies | Class-based services with DI |
| Settings | Pydantic Settings with `.env` |
| Response | ORJSONResponse for performance |
| Middleware | Order: CORS → RequestID → Timing → Logging |
| Health | Check all critical dependencies |

## Related Skills

- `clean-architecture` - Service layer patterns
- `database-schema-designer` - SQLAlchemy models
- `observability-monitoring` - Logging and metrics

## Capability Details

### lifespan
**Keywords:** lifespan, startup, shutdown, asynccontextmanager
**Solves:**
- FastAPI startup/shutdown
- Resource management in FastAPI

### dependencies
**Keywords:** dependency injection, Depends, get_db, service dependency
**Solves:**
- FastAPI dependency injection patterns
- Reusable dependencies

### middleware
**Keywords:** middleware, request id, timing, cors, logging middleware
**Solves:**
- Custom FastAPI middleware
- Request/response interceptors

### settings
**Keywords:** settings, pydantic settings, env, configuration
**Solves:**
- FastAPI configuration management
- Environment variables

### health-checks
**Keywords:** health check, readiness, liveness, health endpoint
**Solves:**
- Kubernetes health checks
- Service health monitoring
