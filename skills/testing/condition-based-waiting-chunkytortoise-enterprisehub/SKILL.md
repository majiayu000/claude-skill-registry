---
name: Condition-Based Waiting
description: This skill should be used when dealing with "race conditions in tests", "Redis timing issues", "WebSocket connection timing", "async test failures", "flaky tests due to timing", "test synchronization problems", or when tests fail intermittently due to timing issues.
version: 1.0.0
---

# Condition-Based Waiting: Fixing Race Conditions in Tests

## Overview

This skill provides systematic approaches to fixing race conditions and timing issues in tests, particularly common with Redis connections, WebSocket interactions, database operations, and async workflows.

## When to Use This Skill

Use this skill when you encounter:
- **Intermittent test failures** that pass on retry
- **Redis connection timing issues** in async tests
- **WebSocket connection race conditions**
- **Database transaction timing problems**
- **API response timing inconsistencies**
- **File system operation delays**
- **Async/await synchronization issues**

## Core Principles

### 1. Replace Sleep with Condition Waiting
```python
# ❌ BAD: Fixed delays are unreliable
import time
time.sleep(2)  # Arbitrary delay

# ✅ GOOD: Wait for actual condition
import asyncio
from typing import Callable, Any

async def wait_for_condition(
    condition: Callable[[], bool],
    timeout: float = 10.0,
    poll_interval: float = 0.1,
    error_message: str = "Condition not met"
) -> None:
    """Wait for a condition to become true within timeout."""
    start_time = asyncio.get_event_loop().time()

    while True:
        if condition():
            return

        if asyncio.get_event_loop().time() - start_time > timeout:
            raise TimeoutError(error_message)

        await asyncio.sleep(poll_interval)
```

### 2. Redis Connection Readiness
```python
# ✅ GOOD: Proper Redis connection waiting
import redis.asyncio as redis
import pytest

@pytest.fixture
async def redis_client():
    client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    # Wait for Redis to be ready
    await wait_for_condition(
        condition=lambda: asyncio.create_task(ping_redis(client)),
        timeout=30.0,
        error_message="Redis not available within 30 seconds"
    )

    yield client
    await client.close()

async def ping_redis(client: redis.Redis) -> bool:
    """Check if Redis is responsive."""
    try:
        await client.ping()
        return True
    except Exception:
        return False
```

### 3. WebSocket Connection Synchronization
```python
# ✅ GOOD: WebSocket state verification
import websockets
import json

class WebSocketTestClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.websocket = None
        self.connected = False
        self.messages = []

    async def connect(self):
        """Connect and wait for readiness."""
        self.websocket = await websockets.connect(self.uri)
        self.connected = True

        # Wait for initial handshake/auth response
        await self.wait_for_message_count(1, timeout=5.0)

    async def wait_for_message_count(self, count: int, timeout: float = 10.0):
        """Wait for specific number of messages."""
        await wait_for_condition(
            condition=lambda: len(self.messages) >= count,
            timeout=timeout,
            error_message=f"Expected {count} messages, got {len(self.messages)}"
        )

    async def wait_for_message_containing(self, text: str, timeout: float = 10.0):
        """Wait for message containing specific text."""
        await wait_for_condition(
            condition=lambda: any(text in msg for msg in self.messages),
            timeout=timeout,
            error_message=f"No message containing '{text}' received"
        )
```

### 4. Database Transaction Consistency
```python
# ✅ GOOD: Database state verification
import asyncpg
from typing import Optional

class DatabaseTestHelper:
    def __init__(self, db_pool: asyncpg.Pool):
        self.pool = db_pool

    async def wait_for_record(
        self,
        table: str,
        conditions: dict,
        timeout: float = 10.0
    ) -> Optional[dict]:
        """Wait for a database record to appear."""
        async def check_record():
            async with self.pool.acquire() as conn:
                query = f"SELECT * FROM {table} WHERE " + " AND ".join(
                    f"{k} = ${i+1}" for i, k in enumerate(conditions.keys())
                )
                result = await conn.fetchrow(query, *conditions.values())
                return result is not None

        await wait_for_condition(
            condition=check_record,
            timeout=timeout,
            error_message=f"Record not found in {table} with {conditions}"
        )

        # Fetch the actual record
        async with self.pool.acquire() as conn:
            query = f"SELECT * FROM {table} WHERE " + " AND ".join(
                f"{k} = ${i+1}" for i, k in enumerate(conditions.keys())
            )
            return await conn.fetchrow(query, *conditions.values())
```

### 5. File System Operation Synchronization
```python
# ✅ GOOD: File system waiting
import os
import aiofiles
from pathlib import Path

async def wait_for_file(
    file_path: Path,
    timeout: float = 10.0,
    min_size: int = 0
) -> None:
    """Wait for file to exist and optionally reach minimum size."""
    await wait_for_condition(
        condition=lambda: (
            file_path.exists() and
            file_path.stat().st_size >= min_size
        ),
        timeout=timeout,
        error_message=f"File {file_path} not ready within {timeout}s"
    )

async def wait_for_file_content(
    file_path: Path,
    expected_content: str,
    timeout: float = 10.0
) -> None:
    """Wait for file to contain specific content."""
    async def check_content():
        try:
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
                return expected_content in content
        except (FileNotFoundError, PermissionError):
            return False

    await wait_for_condition(
        condition=check_content,
        timeout=timeout,
        error_message=f"File {file_path} doesn't contain expected content"
    )
```

## Integration Patterns

### 1. Test Fixture with Built-in Waiting
```python
@pytest.fixture
async def system_ready():
    """Comprehensive system readiness check."""
    # Wait for Redis
    redis_client = redis.Redis(decode_responses=True)
    await wait_for_condition(
        condition=lambda: asyncio.create_task(ping_redis(redis_client)),
        timeout=30.0
    )

    # Wait for Database
    db_pool = await asyncpg.create_pool("postgresql://localhost/testdb")
    await wait_for_condition(
        condition=lambda: asyncio.create_task(ping_database(db_pool)),
        timeout=30.0
    )

    # Wait for HTTP service
    await wait_for_condition(
        condition=lambda: asyncio.create_task(ping_http_service("http://localhost:8000/health")),
        timeout=60.0
    )

    yield {
        'redis': redis_client,
        'db': db_pool
    }

    # Cleanup
    await redis_client.close()
    await db_pool.close()
```

### 2. Smart Retry Mechanisms
```python
import functools
from typing import TypeVar, Callable, Any

T = TypeVar('T')

def retry_on_condition(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_multiplier: float = 2.0,
    retry_exceptions: tuple = (ConnectionError, TimeoutError)
):
    """Decorator for retrying with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            current_delay = delay

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except retry_exceptions as e:
                    if attempt == max_retries:
                        raise
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff_multiplier

        return wrapper
    return decorator

# Usage:
@retry_on_condition(max_retries=3, delay=0.5)
async def flaky_api_call():
    """API call that might fail due to timing."""
    async with aiohttp.ClientSession() as session:
        async with session.get("http://api.example.com/data") as response:
            return await response.json()
```

## Project-Specific Patterns

### For EnterpriseHub GHL Real Estate AI

#### 1. Streamlit Component Testing
```python
# ✅ Streamlit app readiness
async def wait_for_streamlit_app(
    port: int = 8501,
    timeout: float = 30.0
) -> None:
    """Wait for Streamlit app to be ready."""
    url = f"http://localhost:{port}"

    async def check_app():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return response.status == 200
        except aiohttp.ClientError:
            return False

    await wait_for_condition(
        condition=check_app,
        timeout=timeout,
        error_message=f"Streamlit app not ready on port {port}"
    )
```

#### 2. AI Model Loading Synchronization
```python
# ✅ Wait for AI model initialization
async def wait_for_model_ready(
    model_service,
    timeout: float = 120.0
) -> None:
    """Wait for AI model to be loaded and ready."""
    await wait_for_condition(
        condition=lambda: model_service.is_ready(),
        timeout=timeout,
        poll_interval=2.0,
        error_message="AI model not ready within timeout"
    )
```

#### 3. GHL API Synchronization
```python
# ✅ Wait for GHL webhook processing
async def wait_for_webhook_processed(
    webhook_id: str,
    webhook_service,
    timeout: float = 30.0
) -> None:
    """Wait for GHL webhook to be processed."""
    await wait_for_condition(
        condition=lambda: webhook_service.is_processed(webhook_id),
        timeout=timeout,
        error_message=f"Webhook {webhook_id} not processed"
    )
```

## Best Practices

### 1. Proper Timeout Configuration
```python
# Environment-specific timeouts
TIMEOUTS = {
    'test': {
        'redis_connection': 5.0,
        'db_transaction': 10.0,
        'api_response': 15.0,
        'websocket_connect': 5.0
    },
    'ci': {
        'redis_connection': 30.0,
        'db_transaction': 60.0,
        'api_response': 45.0,
        'websocket_connect': 30.0
    },
    'local': {
        'redis_connection': 10.0,
        'db_transaction': 30.0,
        'api_response': 30.0,
        'websocket_connect': 10.0
    }
}

def get_timeout(operation: str) -> float:
    """Get environment-appropriate timeout."""
    env = os.getenv('TEST_ENV', 'local')
    return TIMEOUTS.get(env, TIMEOUTS['local']).get(operation, 30.0)
```

### 2. Comprehensive Logging
```python
import logging

async def wait_for_condition_with_logging(
    condition: Callable[[], bool],
    timeout: float,
    operation_name: str,
    poll_interval: float = 0.1
) -> None:
    """Wait for condition with detailed logging."""
    logger = logging.getLogger(__name__)
    logger.info(f"Starting wait for: {operation_name}")

    start_time = asyncio.get_event_loop().time()
    attempt = 0

    while True:
        attempt += 1

        if condition():
            elapsed = asyncio.get_event_loop().time() - start_time
            logger.info(f"Condition met for {operation_name} after {elapsed:.2f}s ({attempt} attempts)")
            return

        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > timeout:
            logger.error(f"Timeout waiting for {operation_name} after {elapsed:.2f}s ({attempt} attempts)")
            raise TimeoutError(f"{operation_name} not ready within {timeout}s")

        if attempt % 50 == 0:  # Log every 5 seconds with 0.1s poll interval
            logger.debug(f"Still waiting for {operation_name} ({elapsed:.1f}s elapsed)")

        await asyncio.sleep(poll_interval)
```

### 3. Health Check Patterns
```python
class HealthChecker:
    """Centralized health checking for all services."""

    def __init__(self):
        self.checks = {}

    def register_check(self, name: str, check_func: Callable[[], bool]):
        """Register a health check."""
        self.checks[name] = check_func

    async def wait_for_all_healthy(self, timeout: float = 60.0):
        """Wait for all registered services to be healthy."""
        for name, check_func in self.checks.items():
            await wait_for_condition(
                condition=check_func,
                timeout=timeout,
                error_message=f"Service {name} not healthy"
            )

    async def get_health_status(self) -> dict:
        """Get current health status of all services."""
        status = {}
        for name, check_func in self.checks.items():
            try:
                status[name] = check_func()
            except Exception as e:
                status[name] = False
                logging.warning(f"Health check failed for {name}: {e}")
        return status

# Usage in tests:
@pytest.fixture(scope="session")
async def healthy_system():
    health_checker = HealthChecker()

    # Register all service health checks
    health_checker.register_check("redis", lambda: ping_redis())
    health_checker.register_check("database", lambda: ping_database())
    health_checker.register_check("api", lambda: ping_api())

    # Wait for everything to be ready
    await health_checker.wait_for_all_healthy(timeout=120.0)

    yield health_checker
```

## Common Pitfalls to Avoid

1. **Don't use fixed sleep() calls** - Always wait for actual conditions
2. **Don't ignore cleanup** - Always close connections after tests
3. **Don't use infinite loops** - Always include timeouts
4. **Don't ignore logging** - Log wait operations for debugging
5. **Don't assume instant readiness** - Services need time to initialize

## Integration with Existing Tests

This skill works seamlessly with the existing test-driven-development skill and enhances the verification-before-completion quality gates by providing robust timing synchronization patterns.