---
name: event-sourcing
description: Event sourcing patterns for storing state as a sequence of events. Use when implementing event-driven architectures, CQRS, audit trails, or building systems requiring full history reconstruction.
context: fork
agent: event-driven-architect
version: 2.0.0
tags: [event-sourcing, cqrs, events, audit-trail, domain-events, 2026]
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
author: SkillForge
user-invocable: false
---

# Event Sourcing Patterns

Store application state as immutable events rather than current state snapshots.

## Overview

- Full audit trail requirements (compliance, finance)
- Temporal queries ("what was state at time X?")
- CQRS implementations with separate read/write models
- Systems requiring event replay and debugging
- Microservices with eventual consistency

## Quick Reference

### Domain Event Base

```python
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4

class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    aggregate_id: UUID
    event_type: str
    version: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    class Config:
        frozen = True  # Events are immutable
```

### Event-Sourced Aggregate

```python
class Account:
    def __init__(self):
        self._changes, self._version, self.balance = [], 0, 0.0

    def deposit(self, amount: float):
        self._raise_event(MoneyDeposited(aggregate_id=self.id, amount=amount, version=self._version + 1))

    def _apply(self, event):
        match event:
            case MoneyDeposited(): self.balance += event.amount
            case MoneyWithdrawn(): self.balance -= event.amount

    def load_from_history(self, events):
        for e in events: self._apply(e); self._version = e.version
```

### Event Store Append

```python
async def append_events(self, aggregate_id: UUID, events: list, expected_version: int):
    current = await self.get_version(aggregate_id)
    if current != expected_version:
        raise ConcurrencyError(f"Expected {expected_version}, got {current}")
    for event in events:
        await self.session.execute(insert(event_store).values(
            event_id=event.event_id, aggregate_id=aggregate_id,
            event_type=event.event_type, version=event.version, data=event.model_dump()
        ))
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Event naming | Past tense (`OrderPlaced`, not `PlaceOrder`) |
| Concurrency | Optimistic locking with version check |
| Snapshots | Every 100-500 events for large aggregates |
| Event schema | Version events, support upcasting |
| Projections | Async handlers, idempotent updates |
| Storage | PostgreSQL + JSONB or dedicated event store |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER modify stored events
await event_store.update(event_id, new_data)  # Destroys audit trail

# NEVER include computed data in events
class OrderPlaced(DomainEvent):
    total: float  # WRONG - compute from line items

# NEVER ignore event ordering
async for event in events:  # May arrive out of order
    await handle(event)  # Must check version/sequence

# ALWAYS use immutable events
class Event(BaseModel):
    class Config:
        frozen = True  # Correct

# ALWAYS version your events
event_schema_version: int = 1  # Support schema evolution
```

## Related Skills

- `message-queues` - Distributed event delivery
- `database-schema-designer` - Event store schema design
- `integration-testing` - Testing event-sourced systems

## Capability Details

### event-store
**Keywords:** event store, append-only, event persistence, event log
**Solves:**
- Store events with optimistic concurrency
- Query events by aggregate ID
- Implement event versioning

### aggregate-pattern
**Keywords:** aggregate, domain model, event sourcing aggregate, DDD
**Solves:**
- Model aggregates with event sourcing
- Apply events to rebuild state
- Handle commands and raise events

### projections
**Keywords:** projection, read model, CQRS read side, denormalization
**Solves:**
- Create optimized read models from events
- Implement async event handlers
- Build materialized views

### snapshots
**Keywords:** snapshot, performance, aggregate loading, checkpoint
**Solves:**
- Speed up aggregate loading with snapshots
- Implement snapshot strategies
- Balance snapshot frequency vs storage
