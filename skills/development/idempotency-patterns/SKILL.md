---
name: idempotency-patterns
description: Idempotency patterns for APIs and event handlers. Use when implementing exactly-once semantics, deduplicating requests, or building reliable distributed systems.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [idempotency, deduplication, exactly-once, distributed-systems, api, 2026]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
author: SkillForge
user-invocable: false
---

# Idempotency Patterns (2026)

Patterns for ensuring operations can be safely retried without unintended side effects.

## Overview

- Building payment or financial APIs
- Implementing webhook handlers
- Processing messages from queues
- Creating mutation endpoints (POST, PUT, DELETE)
- Building distributed systems with at-least-once delivery

## Quick Reference

### Idempotency Key Generation

```python
import hashlib
import json
from typing import Any

def generate_idempotency_key(
    *,
    entity_id: str,
    action: str,
    params: dict[str, Any] | None = None,
) -> str:
    """
    Generate deterministic idempotency key.

    Args:
        entity_id: Unique identifier of the entity
        action: The action being performed
        params: Optional parameters that affect the result

    Returns:
        32-character hex string
    """
    content = f"{entity_id}:{action}"
    if params:
        # Sort keys for deterministic output
        content += f":{json.dumps(params, sort_keys=True)}"

    return hashlib.sha256(content.encode()).hexdigest()[:32]


# Examples
key1 = generate_idempotency_key(
    entity_id="order-123",
    action="create",
    params={"amount": 100, "currency": "USD"},
)

key2 = generate_idempotency_key(
    entity_id="payment-456",
    action="refund",
)
```

### FastAPI Idempotency Middleware

```python
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis
import json

class IdempotencyMiddleware(BaseHTTPMiddleware):
    """Handle Idempotency-Key header for POST/PUT/PATCH."""

    def __init__(self, app, redis_client: redis.Redis, ttl: int = 86400):
        super().__init__(app)
        self.redis = redis_client
        self.ttl = ttl

    async def dispatch(self, request: Request, call_next):
        # Only apply to mutation methods
        if request.method not in ("POST", "PUT", "PATCH"):
            return await call_next(request)

        # Check for idempotency key
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            return await call_next(request)

        cache_key = f"idem:{request.url.path}:{idempotency_key}"

        # Check for cached response
        cached = await self.redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            return Response(
                content=data["body"],
                status_code=data["status"],
                media_type="application/json",
                headers={"X-Idempotent-Replayed": "true"},
            )

        # Process request
        response = await call_next(request)

        # Cache successful responses
        if 200 <= response.status_code < 300:
            body = b"".join([chunk async for chunk in response.body_iterator])
            await self.redis.setex(
                cache_key,
                self.ttl,
                json.dumps({
                    "body": body.decode(),
                    "status": response.status_code,
                }),
            )
            return Response(
                content=body,
                status_code=response.status_code,
                media_type=response.media_type,
            )

        return response
```

### Database-Backed Idempotency

```python
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, insert
from datetime import UTC, datetime, timedelta

class ProcessedRequest(Base):
    """Track processed requests for idempotency."""
    __tablename__ = "processed_requests"

    idempotency_key = Column(String(64), primary_key=True)
    endpoint = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_body = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    expires_at = Column(DateTime)


async def idempotent_execute(
    db: AsyncSession,
    idempotency_key: str,
    endpoint: str,
    operation,
    ttl_hours: int = 24,
) -> tuple[Any, int, bool]:
    """
    Execute operation idempotently.

    Returns: (response, status_code, was_replayed)
    """
    # Check for existing
    existing = await db.get(ProcessedRequest, idempotency_key)
    if existing and existing.expires_at > datetime.now(UTC):
        return json.loads(existing.response_body), existing.status_code, True

    # Execute operation
    result, status_code = await operation()

    # Store result (upsert to handle races)
    stmt = insert(ProcessedRequest).values(
        idempotency_key=idempotency_key,
        endpoint=endpoint,
        status_code=status_code,
        response_body=json.dumps(result),
        expires_at=datetime.now(UTC) + timedelta(hours=ttl_hours),
    ).on_conflict_do_nothing()

    await db.execute(stmt)
    return result, status_code, False
```

### Event Consumer Idempotency

```python
class IdempotentConsumer:
    """Process events exactly once using idempotency keys."""

    def __init__(self, db: AsyncSession, redis: redis.Redis):
        self.db = db
        self.redis = redis

    async def process(
        self,
        event: dict,
        handler,
    ) -> tuple[Any, bool]:
        """
        Process event idempotently.

        Returns: (result, was_duplicate)
        """
        idempotency_key = event.get("idempotency_key")
        if not idempotency_key:
            # No key = always process (risky)
            return await handler(event), False

        # Fast path: check Redis cache
        cache_key = f"processed:{idempotency_key}"
        if await self.redis.exists(cache_key):
            return None, True

        # Slow path: check database
        existing = await self.db.execute(
            select(ProcessedEvent)
            .where(ProcessedEvent.idempotency_key == idempotency_key)
        )
        if existing.scalar_one_or_none():
            # Backfill cache
            await self.redis.setex(cache_key, 86400, "1")
            return None, True

        # Process with database lock to prevent races
        try:
            async with self.db.begin_nested():
                # Insert first to claim the key
                self.db.add(ProcessedEvent(idempotency_key=idempotency_key))
                await self.db.flush()

                # Then process
                result = await handler(event)

            # Cache for fast future lookups
            await self.redis.setex(cache_key, 86400, "1")
            return result, False

        except IntegrityError:
            # Another process claimed it
            return None, True
```

## Key Decisions

| Aspect | Recommendation | Rationale |
|--------|----------------|-----------|
| Key generation | Deterministic hash | Same input = same key always |
| Storage | Redis + DB | Redis for speed, DB for durability |
| TTL | 24-72 hours | Balance storage vs replay window |
| Lock strategy | DB unique constraint | Handles race conditions |
| Response caching | Status 2xx only | Don't cache errors |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER use non-deterministic keys
def bad_key():
    return str(uuid.uuid4())  # Different every time!

# NEVER include timestamps in keys
def bad_key(event):
    return f"{event.id}:{datetime.now(UTC)}"  # Timestamp varies!

# NEVER check-then-act without locking
async def bad_process(key):
    if not await exists(key):  # Race condition!
        await process()
        await mark_processed(key)

# NEVER skip idempotency for financial operations
@router.post("/payments")
async def create_payment(data: PaymentCreate):
    return await process_payment(data)  # No idempotency!

# NEVER cache error responses
if response.status_code >= 400:
    await cache_response(key, response)  # WRONG - errors should retry
```

## Related Skills

- `outbox-pattern` - Reliable event publishing
- `message-queues` - At-least-once message delivery
- `caching-strategies` - Redis caching patterns
- `auth-patterns` - API key management

## Capability Details

### key-generation
**Keywords:** idempotency key, hash, deterministic, deduplication key
**Solves:**
- How do I generate idempotency keys?
- Deterministic key generation
- Key format best practices

### api-idempotency
**Keywords:** idempotency header, POST idempotent, retry safe, middleware
**Solves:**
- How do I make POST endpoints idempotent?
- Implement Idempotency-Key header
- Cache and replay responses

### consumer-idempotency
**Keywords:** exactly-once, event deduplication, message idempotency
**Solves:**
- How do I process events exactly once?
- Deduplicate queue messages
- Handle at-least-once delivery
