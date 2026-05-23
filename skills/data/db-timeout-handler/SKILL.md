# Skill: Database Timeout Handler

**Purpose**: Automatically diagnose and resolve database connection timeout issues for Neon PostgreSQL.

## Trigger Conditions

Invoke this skill when:
- Error contains "connection timed out", "connection refused", or "timeout expired"
- User mentions "database not connecting" or "DB timeout"
- Neon cold start issues occur

## Capabilities

### 1. Diagnose Timeout Cause

Common causes and solutions:

| Error Pattern | Likely Cause | Solution |
|---------------|--------------|----------|
| `timeout expired` | Neon cold start | Add `pool_pre_ping=True` |
| `connection refused` | Wrong host/port | Verify DATABASE_URL |
| `SSL required` | Missing sslmode | Add `?sslmode=require` |
| `too many connections` | Pool exhausted | Reduce pool_size |

### 2. Fix Connection Configuration

Update `backend/app/database.py`:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from .config import settings

# Neon-optimized engine with timeout handling
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    # Cold start handling
    pool_pre_ping=True,
    # Connection timeout (30 seconds)
    connect_args={
        "timeout": 30,
        "command_timeout": 30,
        "server_settings": {
            "statement_timeout": "30000",  # 30 seconds
            "idle_in_transaction_session_timeout": "60000",  # 60 seconds
        }
    },
    # Pool configuration
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,  # Recycle connections after 1 hour
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

### 3. Add Retry Logic

Create `backend/app/utils/db_retry.py`:

```python
import asyncio
from functools import wraps
from typing import TypeVar, Callable
from sqlalchemy.exc import OperationalError, TimeoutError

T = TypeVar('T')

def with_db_retry(max_retries: int = 3, delay: float = 1.0):
    """Decorator for database operations with automatic retry on timeout."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_error = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except (OperationalError, TimeoutError) as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        wait_time = delay * (2 ** attempt)  # Exponential backoff
                        print(f"DB retry {attempt + 1}/{max_retries} in {wait_time}s: {e}")
                        await asyncio.sleep(wait_time)
            raise last_error
        return wrapper
    return decorator

# Usage:
# @with_db_retry(max_retries=3)
# async def get_tasks(session: AsyncSession, user_id: str):
#     result = await session.execute(select(Task).where(Task.user_id == user_id))
#     return result.scalars().all()
```

### 4. Health Check Endpoint

Add to `backend/app/main.py`:

```python
from sqlalchemy import text

@app.get("/health/db")
async def db_health_check():
    """Check database connectivity with timeout."""
    try:
        async with async_session() as session:
            result = await session.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
```

## Quick Diagnosis Commands

```bash
# Test Neon connection from CLI
python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test():
    engine = create_async_engine('$DATABASE_URL')
    async with engine.connect() as conn:
        result = await conn.execute(text('SELECT 1'))
        print('Connection OK:', result.scalar())

asyncio.run(test())
"
```

## Checklist

- [ ] Verify DATABASE_URL format (`postgresql+asyncpg://...?sslmode=require`)
- [ ] Add `pool_pre_ping=True` for cold start handling
- [ ] Configure connection timeout (30s recommended)
- [ ] Implement retry logic for critical operations
- [ ] Add /health/db endpoint for monitoring
- [ ] Test connection after Neon project wake-up
