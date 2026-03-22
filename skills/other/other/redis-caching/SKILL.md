---
name: redis-caching
description: Redis caching and queue patterns. Use when implementing caching, rate limiting, session storage, pub/sub, or background job queues with Redis.
---

# Redis Patterns

## Connection (Python)
```python
import redis.asyncio as redis

# Create pool once at startup
redis_pool = redis.ConnectionPool.from_url(
    settings.REDIS_URL,
    max_connections=10,
    decode_responses=True
)

async def get_redis() -> redis.Redis:
    return redis.Redis(connection_pool=redis_pool)
```

## Caching Pattern
```python
async def get_user(user_id: int, db: AsyncSession, r: redis.Redis) -> User:
    cache_key = f"user:{user_id}"

    # Try cache first
    cached = await r.get(cache_key)
    if cached:
        return User.model_validate_json(cached)

    # Cache miss — fetch from DB
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Cache for 5 minutes
    await r.setex(cache_key, 300, user.model_dump_json())
    return user

async def invalidate_user_cache(user_id: int, r: redis.Redis):
    await r.delete(f"user:{user_id}")
```

## Rate Limiting
```python
async def check_rate_limit(identifier: str, limit: int, window: int, r: redis.Redis):
    """Sliding window rate limit. Raises 429 if over limit."""
    key = f"ratelimit:{identifier}"
    pipe = r.pipeline()
    now = time.time()

    pipe.zremrangebyscore(key, 0, now - window)  # Remove old entries
    pipe.zadd(key, {str(now): now})               # Add current request
    pipe.zcard(key)                               # Count requests in window
    pipe.expire(key, window)
    results = await pipe.execute()

    if results[2] > limit:
        raise HTTPException(429, f"Rate limit exceeded. Try again in {window}s.")
```

## Session Storage
```python
import secrets

async def create_session(user_id: int, r: redis.Redis) -> str:
    session_id = secrets.token_urlsafe(32)
    await r.setex(
        f"session:{session_id}",
        3600 * 24 * 7,  # 7 days
        json.dumps({"user_id": user_id, "created_at": time.time()})
    )
    return session_id

async def get_session(session_id: str, r: redis.Redis) -> dict | None:
    data = await r.get(f"session:{session_id}")
    return json.loads(data) if data else None

async def delete_session(session_id: str, r: redis.Redis):
    await r.delete(f"session:{session_id}")
```

## Pub/Sub (Real-time)
```python
# Publisher
async def publish_event(channel: str, data: dict, r: redis.Redis):
    await r.publish(channel, json.dumps(data))

# Subscriber
async def subscribe_loop(channel: str, r: redis.Redis):
    async with r.pubsub() as pubsub:
        await pubsub.subscribe(channel)
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await handle_event(data)
```

## Key Naming Convention
```
user:{id}              # User cache
session:{token}        # User session
ratelimit:{ip}:{route} # Rate limit counter
lock:{resource}        # Distributed lock
queue:{name}           # Task queue
```

## Rules
- Always set TTL (SETEX not SET) — never let keys grow forever
- Use pipelines for multiple operations (reduces round trips)
- Key names must be namespaced: `user:123`, not just `123`
- Use SCAN not KEYS in production (KEYS blocks Redis)
- Monitor memory: set maxmemory and maxmemory-policy in redis.conf
- For distributed locks: use Redlock algorithm, not simple SET NX
