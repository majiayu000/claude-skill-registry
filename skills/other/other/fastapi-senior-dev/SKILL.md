---
name: fastapi-senior-dev
description: Senior Python Backend Engineer skill for FastAPI. Use when scaffolding production-ready APIs, enforcing clean architecture, optimizing async patterns, or auditing FastAPI codebases.
author: George Khananaev
---

# FastAPI Senior Developer

Transform into a Senior Python Backend Engineer for production-ready FastAPI applications.

## When to Use

- Scaffolding new FastAPI projects
- Implementing clean architecture patterns
- Database integration (PostgreSQL, MongoDB)
- Authentication (OAuth2, JWT, OIDC)
- Microservices & event-driven patterns
- Performance optimization & async patterns
- Security hardening (OWASP compliance)

## Triggers

- `/fastapi-init` - Scaffold new project with clean architecture
- `/fastapi-structure` - Analyze & restructure existing project
- `/fastapi-audit` - Code review for patterns, performance, security

## Reference Files

Load appropriate references based on task context:

| Category | Reference | When to Load |
|----------|-----------|--------------|
| Database | `references/database-sqlalchemy.md` | PostgreSQL, async ORM, migrations |
| Database | `references/database-mongodb.md` | MongoDB with Beanie/Motor |
| Caching | `references/caching-redis.md` | Redis caching, sessions, pub/sub |
| Security | `references/security-auth.md` | OAuth2, JWT, OIDC, RBAC |
| Security | `references/security-owasp.md` | OWASP compliance, hardening |
| Observability | `references/observability.md` | Logging, metrics, tracing |
| Microservices | `references/microservices.md` | Celery, Kafka, event-driven |
| API Design | `references/api-lifecycle.md` | Versioning, deprecation, docs |
| Operations | `references/production-ops.md` | Health checks, K8s, deployment |

## Core Tenets

### 1. Thin Routes, Fat Services

Routes handle HTTP concerns only. Business logic lives in services.

```python
# WRONG: Logic in route
@router.post("/orders")
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    if not await db.get(Product, order.product_id):
        raise HTTPException(404, "Product not found")
    # ... 50 more lines of business logic
    return order

# RIGHT: Thin route, fat service
@router.post("/orders", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    service: OrderService = Depends(get_order_service)
) -> OrderResponse:
    return await service.create(order)
```

### 2. Configuration First

Use pydantic-settings as foundational concern. Split by domain.

```python
# core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    host: str = "localhost"
    port: int = 5432
    name: str
    user: str
    password: str
    pool_size: int = 10
    max_overflow: int = 20

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AUTH_")

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

class Settings(BaseSettings):
    debug: bool = False
    db: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()

settings = Settings()
```

### 3. Project Organization

Choose architecture based on project size. Be consistent.

**Vertical Slice (Recommended for most projects)**
```
src/
├── users/
│   ├── router.py
│   ├── service.py
│   ├── schemas.py
│   ├── models.py
│   └── dependencies.py
├── orders/
│   ├── router.py
│   ├── service.py
│   └── ...
└── core/
    ├── config.py
    ├── database.py
    └── security.py
```

**Layered Architecture (Large teams, strict boundaries)**
```
src/
├── api/
│   ├── routes/
│   ├── deps/
│   └── schemas/
├── services/
├── repositories/
├── models/
│   ├── domain/
│   └── db/
└── core/
```

### 4. Service Layer Pattern (Not Repository)

Use services with direct ORM access. Avoid unnecessary repository abstraction.

```python
# services/user_service.py
class UserService:
    def __init__(self, db: AsyncSession, cache: Redis):
        self.db = db
        self.cache = cache

    async def get_by_id(self, user_id: int) -> User | None:
        # Check cache first
        cached = await self.cache.get(f"user:{user_id}")
        if cached:
            return User.model_validate_json(cached)

        # Direct ORM query - no repository needed
        result = await self.db.execute(
            select(UserModel)
            .options(selectinload(UserModel.profile))
            .where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()

        if user_model:
            user = User.model_validate(user_model)
            await self.cache.setex(f"user:{user_id}", 300, user.model_dump_json())
            return user
        return None
```

### 5. Advanced Dependency Injection

Chain dependencies for validation and composition.

```python
# deps/common.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# deps/users.py
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = verify_token(token)
    user = await db.get(UserModel, payload["sub"])
    if not user:
        raise HTTPException(401, "User not found")
    return user

async def get_current_active_user(
    user: User = Depends(get_current_user)
) -> User:
    if not user.is_active:
        raise HTTPException(403, "Inactive user")
    return user

# deps/resources.py
async def valid_post_id(
    post_id: int,
    db: AsyncSession = Depends(get_db)
) -> Post:
    post = await db.get(PostModel, post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    return post

async def valid_owned_post(
    post: Post = Depends(valid_post_id),
    user: User = Depends(get_current_user)
) -> Post:
    if post.owner_id != user.id:
        raise HTTPException(403, "Not your post")
    return post

# Usage in routes
@router.put("/posts/{post_id}")
async def update_post(
    data: PostUpdate,
    post: Post = Depends(valid_owned_post)  # Validates existence + ownership
) -> PostResponse:
    ...
```

## Async Patterns

### Do

```python
# Async DB with proper session handling
async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# Concurrent independent calls
async def get_dashboard_data(user_id: int) -> DashboardData:
    user, orders, notifications = await asyncio.gather(
        user_service.get(user_id),
        order_service.list_recent(user_id),
        notification_service.get_unread(user_id),
        return_exceptions=True
    )
    return DashboardData(user=user, orders=orders, notifications=notifications)

# Background tasks for non-blocking operations
@router.post("/users")
async def create_user(user: UserCreate, background: BackgroundTasks):
    db_user = await user_service.create(user)
    background.add_task(send_welcome_email, db_user.email)
    background.add_task(analytics.track, "user_created", db_user.id)
    return db_user
```

### Don't

```python
# WRONG: Blocking calls in async context
time.sleep(5)           # Use: await asyncio.sleep(5)
requests.get(url)       # Use: async with httpx.AsyncClient() as client
open("file").read()     # Use: aiofiles.open()

# WRONG: Sequential when parallel is possible
user = await get_user(id)
orders = await get_orders(id)  # Use asyncio.gather()

# WRONG: Sync dependencies in async routes
def get_db():  # Should be: async def get_db()
    return SessionLocal()
```

## Pydantic V2 Patterns

```python
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

class BaseSchema(BaseModel):
    """Base for all schemas with common config."""
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

class UserCreate(BaseSchema):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()

class UserUpdate(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    avatar_url: str | None = None

class UserResponse(BaseSchema):
    id: int
    email: str
    name: str | None
    created_at: datetime
    # Never expose: password, is_admin, internal fields

class UserInDB(UserResponse):
    hashed_password: str  # Internal use only
```

## Error Handling

```python
# core/exceptions.py
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code

class NotFoundError(AppException):
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} with id '{identifier}' not found",
            code="NOT_FOUND",
            status_code=404
        )

class AuthorizationError(AppException):
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message=message, code="FORBIDDEN", status_code=403)

# Register handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        }
    )

# Production: Hide stack traces
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}}
    )
```

## Security Essentials

See `references/security-auth.md` and `references/security-owasp.md` for complete patterns.

### Quick Checklist

- [ ] Use **PyJWT** (not python-jose) for JWT handling
- [ ] **Auth Code + PKCE** for SPAs/Mobile (not password flow)
- [ ] Short-lived access tokens (15-30 min)
- [ ] Refresh tokens in HttpOnly cookies
- [ ] Rate limiting on auth endpoints
- [ ] Request body size limits
- [ ] pydantic-settings for secrets (never hardcode)
- [ ] Log sanitization (filter password, token, authorization)

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Business logic in routes | Move to services |
| DB queries in routes | Use service layer |
| `requests` in async code | Use `httpx.AsyncClient` |
| `time.sleep()` | Use `asyncio.sleep()` |
| Hardcoded config | Use pydantic-settings |
| Return dict from routes | Return Pydantic models |
| Skip type hints | Type everything |
| Global scoped_session | Request-scoped via Depends |
| Repository pattern overkill | Service + direct ORM |
| python-jose for JWT | Use PyJWT |

## Scripts

- `scripts/scaffold_structure.py` - Generate clean architecture folders
- `scripts/generate_migration.py` - Alembic wrapper for async migrations

## Assets

- `assets/docker-compose.yml` - Postgres + Redis + API stack
- `assets/Dockerfile` - Multi-stage production build

## Audit Checklist

When running `/fastapi-audit`, check:

1. **Architecture**
   - [ ] Thin routes, fat services
   - [ ] Consistent project structure
   - [ ] No circular imports

2. **Async**
   - [ ] No blocking calls in async code
   - [ ] Proper session handling
   - [ ] Concurrent calls where possible

3. **Security** (load `references/security-owasp.md`)
   - [ ] Auth patterns correct
   - [ ] Input validation complete
   - [ ] No hardcoded secrets

4. **Database** (load `references/database-sqlalchemy.md`)
   - [ ] Connection pooling configured
   - [ ] N+1 queries prevented
   - [ ] Migrations reversible

5. **Observability** (load `references/observability.md`)
   - [ ] Structured logging
   - [ ] Health checks present
   - [ ] Metrics exposed