---
name: FastAPI Caching
description: This skill should be used when the user asks to "add caching", "implement Redis cache", "cache API response", "invalidate cache", "add cache layer", "optimize with caching", or mentions Redis, caching strategies, cache invalidation, or performance optimization. Provides Redis caching patterns for FastAPI.
version: 0.1.0
---

# FastAPI Caching with Redis

This skill provides production-ready caching patterns using Redis for FastAPI applications.

## Redis Client Setup

### Connection Configuration

```python
# app/infrastructure/cache.py
import redis.asyncio as redis
from typing import Optional, Any
import json
from app.config import get_settings

settings = get_settings()

class RedisCache:
    def __init__(self):
        self._pool: Optional[redis.ConnectionPool] = None
        self._client: Optional[redis.Redis] = None

    async def connect(self):
        self._pool = redis.ConnectionPool.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20
        )
        self._client = redis.Redis(connection_pool=self._pool)

    async def disconnect(self):
        if self._pool:
            await self._pool.disconnect()

    @property
    def client(self) -> redis.Redis:
        if not self._client:
            raise RuntimeError("Redis not connected")
        return self._client

    async def get(self, key: str) -> Optional[Any]:
        value = await self.client.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: int = 3600
    ):
        await self.client.setex(
            key,
            expire,
            json.dumps(value, default=str)
        )

    async def delete(self, key: str):
        await self.client.delete(key)

    async def delete_pattern(self, pattern: str):
        """Delete all keys matching pattern."""
        keys = []
        async for key in self.client.scan_iter(match=pattern):
            keys.append(key)
        if keys:
            await self.client.delete(*keys)

    async def exists(self, key: str) -> bool:
        return await self.client.exists(key) > 0

cache = RedisCache()
```

### Lifespan Integration

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache.connect()
    yield
    await cache.disconnect()

app = FastAPI(lifespan=lifespan)
```

## Cache Decorator

```python
# app/core/cache.py
from functools import wraps
from typing import Callable, Optional
import hashlib
import json

def cached(
    prefix: str,
    expire: int = 3600,
    key_builder: Optional[Callable] = None
):
    """
    Cache decorator for async functions.

    Args:
        prefix: Cache key prefix
        expire: TTL in seconds
        key_builder: Custom function to build cache key
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key = f"{prefix}:{key_builder(*args, **kwargs)}"
            else:
                # Default: hash all arguments
                key_data = json.dumps(
                    {"args": args[1:], "kwargs": kwargs},
                    sort_keys=True,
                    default=str
                )
                key_hash = hashlib.md5(key_data.encode()).hexdigest()
                cache_key = f"{prefix}:{key_hash}"

            # Try cache
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute and cache
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, expire)

            return result
        return wrapper
    return decorator
```

### Usage Examples

```python
class UserService:
    @cached(prefix="user", expire=300)
    async def get_by_id(self, user_id: str) -> Optional[dict]:
        user = await User.get(user_id)
        return user.model_dump() if user else None

    @cached(
        prefix="users_list",
        expire=60,
        key_builder=lambda self, skip, limit, **kw: f"{skip}:{limit}"
    )
    async def get_all(self, skip: int = 0, limit: int = 100) -> list:
        users = await User.find_all().skip(skip).limit(limit).to_list()
        return [u.model_dump() for u in users]

    async def create(self, data: UserCreate) -> User:
        user = await User(**data.model_dump()).insert()
        # Invalidate list cache
        await cache.delete_pattern("users_list:*")
        return user

    async def update(self, user_id: str, data: UserUpdate) -> User:
        user = await self.get_by_id_uncached(user_id)
        await user.set(data.model_dump(exclude_unset=True))
        # Invalidate caches
        await cache.delete(f"user:{user_id}")
        await cache.delete_pattern("users_list:*")
        return user
```

## Response Caching Middleware

```python
# app/middleware/cache.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import hashlib

class ResponseCacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, cache_ttl: int = 60, cache_methods: list = None):
        super().__init__(app)
        self.cache_ttl = cache_ttl
        self.cache_methods = cache_methods or ["GET"]

    async def dispatch(self, request: Request, call_next):
        # Only cache specified methods
        if request.method not in self.cache_methods:
            return await call_next(request)

        # Skip if cache-control: no-cache
        if request.headers.get("cache-control") == "no-cache":
            return await call_next(request)

        # Build cache key
        cache_key = self._build_key(request)

        # Try cache
        cached = await cache.get(cache_key)
        if cached:
            return Response(
                content=cached["body"],
                status_code=cached["status"],
                headers={**cached["headers"], "X-Cache": "HIT"}
            )

        # Execute request
        response = await call_next(request)

        # Cache successful responses
        if 200 <= response.status_code < 300:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            await cache.set(cache_key, {
                "body": body.decode(),
                "status": response.status_code,
                "headers": dict(response.headers)
            }, self.cache_ttl)

            return Response(
                content=body,
                status_code=response.status_code,
                headers={**response.headers, "X-Cache": "MISS"}
            )

        return response

    def _build_key(self, request: Request) -> str:
        key_data = f"{request.method}:{request.url.path}:{request.query_params}"
        return f"response:{hashlib.md5(key_data.encode()).hexdigest()}"
```

## Cache-Aside Pattern

```python
class CachedUserRepository:
    def __init__(self, cache: RedisCache, db: Database):
        self.cache = cache
        self.db = db

    async def get(self, user_id: str) -> Optional[User]:
        # 1. Check cache
        cache_key = f"user:{user_id}"
        cached = await self.cache.get(cache_key)
        if cached:
            return User(**cached)

        # 2. Query database
        user = await self.db.users.find_one({"_id": user_id})
        if not user:
            return None

        # 3. Store in cache
        await self.cache.set(cache_key, user.model_dump(), expire=300)

        return user

    async def save(self, user: User) -> User:
        # 1. Save to database
        await self.db.users.update_one(
            {"_id": user.id},
            {"$set": user.model_dump()},
            upsert=True
        )

        # 2. Invalidate cache
        await self.cache.delete(f"user:{user.id}")

        return user
```

## Write-Through Pattern

```python
class WriteThroughUserRepository:
    async def save(self, user: User) -> User:
        # 1. Write to database
        await self.db.users.update_one(
            {"_id": user.id},
            {"$set": user.model_dump()},
            upsert=True
        )

        # 2. Update cache immediately
        await self.cache.set(
            f"user:{user.id}",
            user.model_dump(),
            expire=300
        )

        return user
```

## Cache Invalidation Patterns

```python
# Event-based invalidation
class CacheInvalidator:
    def __init__(self, cache: RedisCache):
        self.cache = cache

    async def on_user_updated(self, user_id: str):
        await self.cache.delete(f"user:{user_id}")
        await self.cache.delete_pattern("users_list:*")
        await self.cache.delete_pattern(f"user_orders:{user_id}:*")

    async def on_product_updated(self, product_id: str):
        await self.cache.delete(f"product:{product_id}")
        await self.cache.delete_pattern("products_list:*")
        await self.cache.delete_pattern("category_products:*")
```

## Additional Resources

### Reference Files

For detailed patterns:
- **`references/patterns.md`** - Cache patterns (write-behind, read-through)
- **`references/distributed.md`** - Distributed caching, cache stampede
- **`references/monitoring.md`** - Cache hit rates, memory usage

### Example Files

Working examples in `examples/`:
- **`examples/cache_service.py`** - Complete cache service
- **`examples/cached_repository.py`** - Repository with caching
- **`examples/cache_middleware.py`** - Response caching middleware
