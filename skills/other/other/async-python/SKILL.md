---
name: async-python
description: Python asyncio patterns for high-performance async code. Use when writing async functions, managing concurrency, working with aiohttp, asyncpg, or any async I/O in Python.
---

# Async Python Patterns

## Core Concepts
```python
import asyncio

# Basic async function
async def fetch_user(user_id: int) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/users/{user_id}") as resp:
            return await resp.json()

# Run from sync context
user = asyncio.run(fetch_user(123))
```

## Concurrency Patterns

### Run tasks in parallel (gather)
```python
# All run at the same time — total time = slowest task
users, posts, comments = await asyncio.gather(
    fetch_user(user_id),
    fetch_posts(user_id),
    fetch_comments(user_id),
)

# With error handling — return exceptions instead of raising
results = await asyncio.gather(
    fetch_user(user_id),
    fetch_posts(user_id),
    return_exceptions=True,
)
for result in results:
    if isinstance(result, Exception):
        logger.error(f"Task failed: {result}")
```

### Limit concurrency (Semaphore)
```python
# Process 100 items but max 10 at a time
sem = asyncio.Semaphore(10)

async def process_with_limit(item):
    async with sem:
        return await process(item)

results = await asyncio.gather(*[process_with_limit(i) for i in items])
```

### Timeout
```python
try:
    result = await asyncio.wait_for(fetch_data(), timeout=10.0)
except asyncio.TimeoutError:
    logger.warning("Fetch timed out after 10s")
    result = None
```

### Background tasks (fire and forget)
```python
async def main():
    # Don't await — runs in background
    task = asyncio.create_task(send_notification(user_id))

    # But keep reference so GC doesn't kill it
    background_tasks = set()
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
```

### Async context manager
```python
class DatabasePool:
    async def __aenter__(self):
        self.pool = await asyncpg.create_pool(dsn)
        return self

    async def __aexit__(self, *args):
        await self.pool.close()

async with DatabasePool() as db:
    await db.pool.fetchrow("SELECT * FROM users WHERE id = $1", 1)
```

### Async generator
```python
async def stream_records(table: str):
    async with db.pool.acquire() as conn:
        async for record in conn.cursor(f"SELECT * FROM {table}"):
            yield dict(record)

async for record in stream_records("large_table"):
    await process(record)  # Never loads all into memory
```

## Event Loop Management
```python
# FastAPI: use lifespan for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    app.state.db = await create_pool()
    app.state.redis = await aioredis.from_url(REDIS_URL)
    yield
    # shutdown
    await app.state.db.close()
    await app.state.redis.close()
```

## Common Mistakes to Avoid
```python
# ❌ WRONG: blocking call in async function kills concurrency
async def bad():
    time.sleep(1)         # Blocks entire event loop!
    requests.get(url)     # Blocking HTTP call

# ✅ RIGHT: use async equivalents
async def good():
    await asyncio.sleep(1)
    async with aiohttp.ClientSession() as s:
        await s.get(url)

# ❌ WRONG: creating event loop manually in library code
loop = asyncio.get_event_loop()
loop.run_until_complete(coro())

# ✅ RIGHT
asyncio.run(coro())  # Creates and closes loop properly
```

## Rules
- NEVER use time.sleep, requests, or any blocking I/O in async functions
- Use asyncio.gather() for parallel work — sequential awaits waste time
- Use Semaphore to limit concurrency for rate-limited APIs or DB pools
- Always await asyncio.wait_for() for external calls (never hang forever)
- Keep strong references to background tasks (set pattern above)
- Use asyncpg for PostgreSQL, aioredis for Redis, aiohttp for HTTP
- asyncio.run() at the top level only — never inside async functions
