---
name: async-await-checker
description: Automatically applies when writing Python functions that call async operations. Ensures proper async/await pattern usage (not asyncio.run) to prevent event loop errors.
---

# Async/Await Pattern Enforcer

When you are writing or modifying Python functions that:
- Call any function with `async def`
- Work with async I/O operations (database, HTTP, file I/O)
- Need to run in an async context (FastAPI, async frameworks)

**Always apply these patterns:**

## ✅ Correct Pattern

```python
# Helper function
async def fetch_user_data(user_id: str) -> dict:
    """Fetch user data from database."""
    result = await db.query(user_id)  # ✅ Use await
    return result

# API endpoint (FastAPI)
@app.get("/users/{user_id}")
async def get_user(user_id: str) -> dict:  # ✅ async def
    data = await fetch_user_data(user_id)  # ✅ await
    return data

# Multiple async calls
async def process_order(order_id: str) -> dict:
    # ✅ Run sequentially
    user = await fetch_user(order_id)
    payment = await process_payment(user.id)

    # ✅ Run in parallel with asyncio.gather
    results = await asyncio.gather(
        send_email(user.email),
        update_inventory(order_id),
        log_transaction(payment.id)
    )

    return {"status": "success"}
```

## ❌ Incorrect Pattern (Causes Runtime Errors)

```python
# ❌ Don't do this
def fetch_user_data(user_id: str):
    result = asyncio.run(db.query(user_id))  # ❌ asyncio.run in event loop = error!
    return result

# ❌ Missing async
@app.get("/users/{user_id}")
def get_user(user_id: str):  # ❌ Should be async def
    data = fetch_user_data(user_id)  # ❌ Not awaiting
    return data

# ❌ Blocking in async function
async def process_order(order_id: str):
    time.sleep(5)  # ❌ Blocks event loop! Use asyncio.sleep(5)
    return await fetch_data()
```

## Why This Matters

**Runtime Error:** `asyncio.run()` fails when called from within an already-running event loop.

**Solution:** Always use `async def` + `await` pattern.

**Performance:** Blocking operations in async functions defeat the purpose of async code.

## Common Async Operations

**Database queries:**
```python
async def get_records():
    async with db.session() as session:
        result = await session.execute(query)
        return result.fetchall()
```

**HTTP requests:**
```python
import httpx

async def fetch_api_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

**File I/O:**
```python
import aiofiles

async def read_file(path: str):
    async with aiofiles.open(path, 'r') as f:
        content = await f.read()
        return content
```

## Error Handling in Async

```python
async def safe_api_call(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise TimeoutError(f"Request to {url} timed out")
    except httpx.HTTPStatusError as e:
        raise APIError(f"API error: {e.response.status_code}")
```

## Testing Async Code

```python
import pytest

@pytest.mark.asyncio
async def test_fetch_user_data():
    """Test async function"""
    result = await fetch_user_data("user_123")
    assert result["id"] == "user_123"

@pytest.mark.asyncio
async def test_with_mock():
    """Test with mocked async dependency"""
    with patch('module.db.query') as mock_query:
        mock_query.return_value = {"id": "test"}
        result = await fetch_user_data("test")
        assert result["id"] == "test"
```

## ❌ Anti-Patterns

```python
# ❌ Mixing sync and async incorrectly
def sync_function():
    return asyncio.run(async_function())  # Only OK at top level!

# ❌ Not using asyncio.gather for parallel operations
async def slow_version():
    result1 = await operation1()  # Waits
    result2 = await operation2()  # Waits
    result3 = await operation3()  # Waits
    return [result1, result2, result3]

# ✅ Better: parallel execution
async def fast_version():
    results = await asyncio.gather(
        operation1(),
        operation2(),
        operation3()
    )
    return results

# ❌ Forgetting error handling in gather
async def unsafe():
    await asyncio.gather(op1(), op2())  # If op1 fails, op2 continues

# ✅ Better: return exceptions
async def safe():
    results = await asyncio.gather(
        op1(), op2(),
        return_exceptions=True
    )
    for result in results:
        if isinstance(result, Exception):
            handle_error(result)
```

## Best Practices Checklist

- ✅ Use `async def` for any function that awaits
- ✅ Use `await` for all async calls
- ✅ Use `asyncio.gather()` for parallel operations
- ✅ Use `async with` for async context managers
- ✅ Use `asyncio.sleep()` instead of `time.sleep()`
- ✅ Add proper error handling with try/except
- ✅ Use `@pytest.mark.asyncio` for async tests
- ✅ Consider timeouts for external operations
- ✅ Use `return_exceptions=True` in gather when appropriate

## Auto-Apply

When you see code calling async functions, automatically:
1. Make the calling function `async def`
2. Use `await` for async calls
3. Update callers to also be async (chain up)
4. Add `@pytest.mark.asyncio` to tests
5. Replace blocking calls with async equivalents

## Related Skills

- pytest-patterns - For testing async code
- structured-errors - For async error handling
- tool-design-pattern - For async tools
