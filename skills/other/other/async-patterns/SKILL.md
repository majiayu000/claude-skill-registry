---
name: async-patterns
description: Asynchronous programming patterns for Python, JavaScript/TypeScript, and other languages. Auto-triggers when implementing concurrent code, handling promises, or optimizing I/O operations.
---

# Async Programming Patterns

## Core Concepts

### Event Loop
- Single-threaded execution model
- Non-blocking I/O operations
- Cooperative multitasking via yield points

### When to Use Async
- I/O-bound operations (network, disk, database)
- High concurrency requirements
- Real-time applications (WebSockets)

### When NOT to Use Async
- CPU-bound computation (use multiprocessing)
- Simple sequential scripts
- When overhead outweighs benefit

## Python Async Patterns

### Basic Pattern
```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Run concurrent requests
async def main():
    urls = ["url1", "url2", "url3"]
    results = await asyncio.gather(*[fetch_data(u) for u in urls])
```

### Producer-Consumer Queue
```python
async def producer(queue: asyncio.Queue):
    for item in items:
        await queue.put(item)
    await queue.put(None)  # Sentinel

async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        await process(item)
        queue.task_done()
```

### Rate Limiting with Semaphore
```python
semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

async def rate_limited_request(url):
    async with semaphore:
        return await fetch(url)
```

### Timeout Handling
```python
try:
    result = await asyncio.wait_for(slow_operation(), timeout=5.0)
except asyncio.TimeoutError:
    handle_timeout()
```

## JavaScript/TypeScript Patterns

### Promise Patterns
```typescript
// Parallel execution
const results = await Promise.all([fetch1(), fetch2(), fetch3()]);

// First to complete
const fastest = await Promise.race([fetch1(), fetch2()]);

// All settled (includes failures)
const outcomes = await Promise.allSettled([fetch1(), fetch2()]);
```

### Async Iterator
```typescript
async function* paginate(url: string) {
  let cursor: string | null = null;
  do {
    const { data, nextCursor } = await fetchPage(url, cursor);
    yield* data;
    cursor = nextCursor;
  } while (cursor);
}

for await (const item of paginate('/api/items')) {
  process(item);
}
```

### Error Handling
```typescript
// Good: Specific error handling
try {
  const data = await fetchData();
} catch (error) {
  if (error instanceof NetworkError) {
    await retry();
  } else if (error instanceof ValidationError) {
    logValidationError(error);
  } else {
    throw error;  // Re-throw unknown errors
  }
}
```

### Cancellation
```typescript
const controller = new AbortController();
const { signal } = controller;

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch(url, { signal });
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Request cancelled');
  }
}
```

## Common Anti-Patterns

### Sequential Awaits (Bad)
```javascript
// BAD: Sequential execution
const a = await fetchA();
const b = await fetchB();
const c = await fetchC();

// GOOD: Parallel execution
const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()]);
```

### Unhandled Promise Rejection
```javascript
// BAD: Silent failure
fetchData().then(process);

// GOOD: Handle errors
fetchData().then(process).catch(handleError);
// OR
try {
  const data = await fetchData();
  process(data);
} catch (error) {
  handleError(error);
}
```

### Blocking Event Loop
```python
# BAD: Blocks event loop
def sync_heavy_computation():
    # CPU-bound work
    pass

# GOOD: Run in executor
result = await asyncio.get_event_loop().run_in_executor(
    None, sync_heavy_computation
)
```

## Performance Tips

1. **Connection pooling**: Reuse connections
2. **Batch operations**: Group small requests
3. **Backpressure**: Limit queue sizes
4. **Graceful shutdown**: Cancel pending tasks on exit
