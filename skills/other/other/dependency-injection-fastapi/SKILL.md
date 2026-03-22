---
name: dependency-injection-fastapi
description: >
  Implement FastAPI dependency injection with Depends(), security dependencies,
  database session management, request-scoped deps, and testing with overrides. Use
  when the user builds FastAPI endpoints, manages database connections, implements
  auth, or asks about dependency injection. Trigger when you see repeated setup
  logic in endpoint functions that should be extracted to dependencies.
---

# FastAPI Dependency Injection

Use FastAPI's `Depends()` system to inject shared logic into endpoints: database
sessions, authentication, authorization, pagination, and configuration. Dependencies
are composable, testable, and handle cleanup automatically.

## When to Use
- User creates FastAPI endpoints with shared setup/teardown logic
- User implements authentication or authorization
- User manages database connections or sessions
- User asks about dependency injection or testing FastAPI
- User has duplicated logic across multiple endpoints

## Core Patterns

### Basic Dependencies

```python
from fastapi import Depends, FastAPI, Query

app = FastAPI()

# Simple dependency -- function that returns a value
async def common_parameters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: str = Query("created_at"),
):
    return {"skip": skip, "limit": limit, "sort_by": sort_by}

@app.get("/items")
async def list_items(params: dict = Depends(common_parameters)):
    return await fetch_items(**params)

@app.get("/users")
async def list_users(params: dict = Depends(common_parameters)):
    return await fetch_users(**params)
```

### Database Session Dependencies

Use generator dependencies for automatic session cleanup.

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session, ensuring cleanup on exit."""
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Security Dependencies

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate the current user from JWT token."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=["HS256"],
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Role-based authorization as composable dependency
def require_role(required_role: str):
    async def check_role(user: User = Depends(get_current_user)) -> User:
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return check_role

@app.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    await db.execute(delete(User).where(User.id == user_id))
    return {"deleted": user_id}
```

### Dependency Chaining

Dependencies can depend on other dependencies. FastAPI resolves the entire graph.

```python
async def get_settings() -> Settings:
    return Settings()

async def get_cache(settings: Settings = Depends(get_settings)) -> RedisCache:
    return RedisCache(url=settings.redis_url)

async def get_user_service(
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_cache),
) -> UserService:
    return UserService(db=db, cache=cache)

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return await service.get_by_id(user_id)
```

### Request-Scoped Dependencies

FastAPI caches dependency results per request by default. The same dependency called
multiple times in the same request returns the same instance.

```python
# get_db() is called once per request, even if multiple dependencies use it
@app.post("/transfer")
async def transfer_funds(
    transfer: TransferRequest,
    sender_service: AccountService = Depends(get_sender_service),   # uses get_db
    receiver_service: AccountService = Depends(get_receiver_service), # uses get_db
    # Both services share the SAME db session within this request
):
    ...

# To force a fresh instance, use use_cache=False
@app.get("/data")
async def get_data(
    db1: AsyncSession = Depends(get_db),
    db2: AsyncSession = Depends(get_db, use_cache=False),  # Different session
):
    ...
```

### Router-Level Dependencies

Apply dependencies to all routes in a router or the entire app.

```python
from fastapi import APIRouter

# All routes in this router require authentication
authenticated_router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(get_current_user)],
)

@authenticated_router.get("/profile")
async def get_profile(user: User = Depends(get_current_user)):
    return user

# App-level dependencies
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

### Testing with Dependency Overrides

Replace dependencies in tests without modifying production code.

```python
import pytest
from httpx import AsyncClient, ASGITransport

# Create a test database session
async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    async with test_session_factory() as session:
        yield session

# Mock current user
async def get_mock_user() -> User:
    return User(id=1, name="Test User", email="test@example.com", role="admin")

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = get_test_db
    app.dependency_overrides[get_current_user] = get_mock_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

async def test_get_profile(client: AsyncClient):
    response = await client.get("/api/v1/profile")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
```

## Anti-Patterns

- **Instantiating services in endpoint bodies**: Extract to dependencies for reuse
  and testability. If you see `service = UserService(db)` in an endpoint, make it
  a dependency.
- **Not cleaning up resources**: Always use generator dependencies (`yield`) for
  resources that need cleanup (DB sessions, HTTP clients, file handles).
- **Hardcoding auth checks in endpoints**: Extract to reusable security dependencies.
  `Depends(require_role("admin"))` is clearer and more testable than inline checks.
- **Not using dependency overrides in tests**: Overriding is the standard way to mock
  dependencies. Avoid monkey-patching or modifying production code for tests.
- **Fat dependencies**: A dependency that does too much. Keep dependencies focused on
  one thing: one for DB session, one for auth, one for pagination.

## Quick Reference

| Pattern | Syntax |
|---|---|
| Simple dependency | `Depends(my_function)` |
| Generator (cleanup) | `yield` inside dependency function |
| Security | `Security(HTTPBearer())` |
| Parameterized | Function returning a dependency function |
| Router-level | `APIRouter(dependencies=[Depends(...)])` |
| Test override | `app.dependency_overrides[dep] = mock_dep` |
| Skip cache | `Depends(dep, use_cache=False)` |
| Class dependency | `class MyDep:` with `__call__` method |
