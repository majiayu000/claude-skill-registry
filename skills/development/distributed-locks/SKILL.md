---
name: distributed-locks
description: Distributed locking patterns with Redis and PostgreSQL for coordination across instances. Use when implementing exclusive access, preventing race conditions, or coordinating distributed resources.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [distributed, locks, redis, postgresql, concurrency, coordination, 2026]
author: SkillForge
user-invocable: false
---

# Distributed Locks

Coordinate exclusive access to resources across multiple service instances.

## Overview

- Preventing duplicate processing of jobs/events
- Coordinating singleton processes (cron, leaders)
- Protecting critical sections across instances
- Implementing leader election
- Rate limiting at distributed level

## Lock Types Comparison

| Lock Type | Durability | Latency | Use Case |
|-----------|-----------|---------|----------|
| Redis (single) | Low | ~1ms | Fast, non-critical |
| Redlock (multi) | High | ~5ms | Critical, HA required |
| PostgreSQL advisory | High | ~2ms | Already using PG, ACID |

## Quick Reference

### Redis Lock (Single Node)

```python
from uuid_utils import uuid7
import redis.asyncio as redis

class RedisLock:
    """Redis lock with Lua scripts for atomicity."""

    ACQUIRE = "if redis.call('set',KEYS[1],ARGV[1],'NX','PX',ARGV[2]) then return 1 end return 0"
    RELEASE = "if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) end return 0"

    def __init__(self, client: redis.Redis, name: str, ttl_ms: int = 30000):
        self._client = client
        self._name = f"lock:{name}"
        self._owner = str(uuid7())
        self._ttl = ttl_ms

    async def acquire(self) -> bool:
        return await self._client.eval(self.ACQUIRE, 1, self._name, self._owner, self._ttl) == 1

    async def release(self) -> bool:
        return await self._client.eval(self.RELEASE, 1, self._name, self._owner) == 1

    async def __aenter__(self):
        if not await self.acquire():
            raise LockError(f"Failed to acquire {self._name}")
        return self

    async def __aexit__(self, *_):
        await self.release()
```

See [redis-locks.md](references/redis-locks.md) for complete implementation with retry/extend.

### PostgreSQL Advisory Lock

```python
from sqlalchemy import text

async def with_advisory_lock(session, lock_id: int):
    """PostgreSQL advisory lock (session-level)."""
    await session.execute(text("SELECT pg_advisory_lock(:id)"), {"id": lock_id})
    try:
        yield
    finally:
        await session.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": lock_id})
```

See [postgres-advisory-locks.md](references/postgres-advisory-locks.md) for transaction-level and monitoring.

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Backend | Redis for speed, PG if already using it |
| TTL | 2-3x expected operation time |
| Retry | Exponential backoff with jitter |
| Fencing | Include owner ID for safety |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER forget TTL (causes deadlocks)
await redis.set(f"lock:{name}", "1")  # WRONG - no expiry!

# NEVER release without owner check
await redis.delete(f"lock:{name}")  # WRONG - might release others' lock

# NEVER use single Redis for critical operations
lock = RedisLock(single_redis, "payment")  # Use Redlock for HA

# NEVER hold locks across await points without heartbeat
async with lock:
    await slow_external_api()  # Lock may expire!
```

## Related Skills

- `idempotency-patterns` - Complement locks with idempotency
- `caching-strategies` - Redis patterns
- `background-jobs` - Job deduplication

## References

- [Redis Locks](references/redis-locks.md) - Lua scripts, retry, extend
- [Redlock Algorithm](references/redlock-algorithm.md) - Multi-node HA
- [PostgreSQL Advisory](references/postgres-advisory-locks.md) - Session/transaction

## Capability Details

### redis-locks
**Keywords:** Redis, Lua, SET NX, atomic, TTL
**Solves:** Fast distributed locks, atomic acquire/release, auto-expiry

### redlock
**Keywords:** Redlock, multi-node, quorum, HA, fault-tolerant
**Solves:** High-availability locking, survive node failures

### advisory-locks
**Keywords:** PostgreSQL, advisory, pg_advisory_lock, session, transaction
**Solves:** Lock with existing PG, ACID integration, no extra infra

### leader-election
**Keywords:** leader, election, singleton, coordinator
**Solves:** Single active instance, coordinator pattern
