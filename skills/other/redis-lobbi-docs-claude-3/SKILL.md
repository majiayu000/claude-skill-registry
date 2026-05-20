---
name: redis
description: Redis caching, pub/sub, and data structures. Activate for Redis operations, caching strategies, session management, and message queuing.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Redis Skill

Provides comprehensive Redis capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Caching implementation
- Session management
- Pub/Sub messaging
- Rate limiting
- Distributed locks

## Redis CLI Quick Reference

### Connection
\`\`\`bash
# Connect
redis-cli -h localhost -p 6379
redis-cli -h localhost -p 6379 -a password

# Test connection
redis-cli ping
\`\`\`

### Basic Operations
\`\`\`bash
# Strings
SET key "value"
SET key "value" EX 3600          # With TTL
GET key
DEL key
EXISTS key
TTL key
EXPIRE key 3600

# Hashes
HSET user:1 name "John" age "30"
HGET user:1 name
HGETALL user:1
HDEL user:1 age

# Lists
LPUSH queue "item1"
RPUSH queue "item2"
LPOP queue
RPOP queue
LRANGE queue 0 -1

# Sets
SADD tags "python" "redis"
SMEMBERS tags
SISMEMBER tags "python"
SREM tags "python"

# Sorted Sets
ZADD leaderboard 100 "player1" 200 "player2"
ZRANGE leaderboard 0 -1 WITHSCORES
ZRANK leaderboard "player1"
ZINCRBY leaderboard 50 "player1"
\`\`\`

## Python Redis Client

\`\`\`python
import redis
from redis import asyncio as aioredis

# Synchronous client
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Async client
async_redis = aioredis.from_url("redis://localhost:6379", decode_responses=True)

# Basic operations
r.set('key', 'value', ex=3600)
value = r.get('key')
r.delete('key')

# Hash operations
r.hset('user:1', mapping={'name': 'John', 'age': '30'})
user = r.hgetall('user:1')

# List operations
r.lpush('queue', 'item1', 'item2')
items = r.lrange('queue', 0, -1)
item = r.rpop('queue')

# Async operations
async def cache_get(key: str):
    async with aioredis.from_url("redis://localhost") as redis:
        return await redis.get(key)
\`\`\`

## Caching Patterns

### Cache-Aside Pattern
\`\`\`python
async def get_agent(agent_id: str) -> dict:
    # Try cache first
    cache_key = f"agent:{agent_id}"
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss - fetch from database
    agent = await db.get_agent(agent_id)
    if agent:
        await redis.set(cache_key, json.dumps(agent), ex=3600)

    return agent

async def update_agent(agent_id: str, data: dict) -> dict:
    # Update database
    agent = await db.update_agent(agent_id, data)

    # Invalidate cache
    cache_key = f"agent:{agent_id}"
    await redis.delete(cache_key)

    return agent
\`\`\`

### Rate Limiting
\`\`\`python
async def rate_limit(key: str, limit: int, window: int) -> bool:
    """
    Sliding window rate limiter.
    Returns True if request is allowed.
    """
    current = int(time.time())
    window_key = f"rate:{key}:{current // window}"

    async with redis.pipeline() as pipe:
        pipe.incr(window_key)
        pipe.expire(window_key, window * 2)
        results = await pipe.execute()

    count = results[0]
    return count <= limit

# Usage
if not await rate_limit(f"user:{user_id}", limit=100, window=60):
    raise HTTPException(status_code=429, detail="Rate limit exceeded")
\`\`\`

### Distributed Lock
\`\`\`python
import uuid

class DistributedLock:
    def __init__(self, redis_client, key: str, timeout: int = 10):
        self.redis = redis_client
        self.key = f"lock:{key}"
        self.timeout = timeout
        self.token = str(uuid.uuid4())

    async def __aenter__(self):
        while True:
            acquired = await self.redis.set(
                self.key, self.token, nx=True, ex=self.timeout
            )
            if acquired:
                return self
            await asyncio.sleep(0.1)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Only release if we own the lock
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        await self.redis.eval(script, 1, self.key, self.token)

# Usage
async with DistributedLock(redis, "resource:123"):
    await do_critical_work()
\`\`\`

## Pub/Sub

\`\`\`python
# Publisher
async def publish_event(channel: str, message: dict):
    await redis.publish(channel, json.dumps(message))

# Subscriber
async def subscribe_events():
    pubsub = redis.pubsub()
    await pubsub.subscribe("agent:events")

    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            await handle_event(data)
\`\`\`

## Session Management

\`\`\`python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import secrets

security = HTTPBearer()

async def create_session(user_id: str) -> str:
    session_id = secrets.token_urlsafe(32)
    session_key = f"session:{session_id}"

    await redis.hset(session_key, mapping={
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat()
    })
    await redis.expire(session_key, 86400)  # 24 hours

    return session_id

async def get_session(token: str = Depends(security)) -> dict:
    session_key = f"session:{token.credentials}"
    session = await redis.hgetall(session_key)

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    # Refresh TTL
    await redis.expire(session_key, 86400)
    return session
\`\`\`

## Best Practices

1. **Use connection pooling** for production
2. **Set TTL on all keys** to prevent memory bloat
3. **Use pipelining** for batch operations
4. **Implement proper error handling** for connection issues
5. **Monitor memory usage** with `INFO memory`
6. **Use Lua scripts** for atomic operations
