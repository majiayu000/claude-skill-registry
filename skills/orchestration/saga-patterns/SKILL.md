---
name: saga-patterns
description: Saga patterns for distributed transactions with orchestration and choreography approaches. Use when implementing multi-service transactions, handling partial failures, or building systems requiring eventual consistency with compensation.
context: fork
agent: event-driven-architect
version: 1.0.0
tags: [saga, distributed-transactions, orchestration, choreography, compensation, microservices, 2026]
author: SkillForge
user-invocable: false
---

# Saga Patterns for Distributed Transactions

Maintain consistency across microservices without distributed locks.

## Overview

- Multi-service business transactions (order -> payment -> inventory -> shipping)
- Operations that must eventually succeed or roll back completely
- Long-running business processes (minutes to days)
- Microservices avoiding 2PC (two-phase commit)

## When NOT to Use

- Single database operations (use transactions)
- Real-time consistency requirements (use synchronous calls)
- When eventual consistency is unacceptable

## Orchestration vs Choreography

| Aspect | Orchestration | Choreography |
|--------|---------------|--------------|
| Control | Central orchestrator | Distributed events |
| Coupling | Services depend on orchestrator | Loosely coupled |
| Visibility | Single point of observation | Requires distributed tracing |
| Best for | Complex, ordered workflows | Simple, parallel flows |

## Orchestration Pattern

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Any
from datetime import datetime, timezone

class SagaStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"
    FAILED = "failed"

@dataclass
class SagaStep:
    name: str
    action: Callable
    compensation: Callable
    status: SagaStatus = SagaStatus.PENDING
    result: Any = None

@dataclass
class SagaContext:
    saga_id: str
    data: dict = field(default_factory=dict)
    steps: list[SagaStep] = field(default_factory=list)
    status: SagaStatus = SagaStatus.PENDING
    current_step: int = 0

class SagaOrchestrator:
    def __init__(self, saga_repository, event_publisher):
        self.repo = saga_repository
        self.publisher = event_publisher

    async def execute(self, saga: SagaContext) -> SagaContext:
        saga.status = SagaStatus.RUNNING
        await self.repo.save(saga)

        for i, step in enumerate(saga.steps):
            saga.current_step = i
            try:
                step.result = await step.action(saga.data)
                saga.data.update(step.result or {})
                step.status = SagaStatus.COMPLETED
            except Exception:
                step.status = SagaStatus.FAILED
                await self._compensate(saga, i)
                return saga

        saga.status = SagaStatus.COMPLETED
        await self.repo.save(saga)
        return saga

    async def _compensate(self, saga: SagaContext, failed_step: int):
        saga.status = SagaStatus.COMPENSATING
        for i in range(failed_step - 1, -1, -1):
            step = saga.steps[i]
            if step.status == SagaStatus.COMPLETED:
                try:
                    await step.compensation(saga.data)
                    step.status = SagaStatus.COMPENSATED
                except Exception as e:
                    step.error = f"Compensation failed: {e}"
        saga.status = SagaStatus.COMPENSATED
        await self.repo.save(saga)
```

### Order Saga Example

```python
class OrderSaga:
    def __init__(self, payment_service, inventory_service, shipping_service):
        self.payment = payment_service
        self.inventory = inventory_service
        self.shipping = shipping_service

    def create_saga(self, order: Order) -> SagaContext:
        return SagaContext(
            saga_id=f"order-{order.id}",
            data={"order": order.dict()},
            steps=[
                SagaStep("reserve_inventory", self._reserve_inventory, self._release_inventory),
                SagaStep("process_payment", self._process_payment, self._refund_payment),
                SagaStep("create_shipment", self._create_shipment, self._cancel_shipment),
            ],
        )

    async def _reserve_inventory(self, data: dict) -> dict:
        reservation = await self.inventory.reserve(items=data["order"]["items"])
        return {"reservation_id": reservation.id}

    async def _release_inventory(self, data: dict):
        await self.inventory.release(data["reservation_id"])

    async def _process_payment(self, data: dict) -> dict:
        payment = await self.payment.charge(amount=data["order"]["total"])
        return {"payment_id": payment.id}

    async def _refund_payment(self, data: dict):
        await self.payment.refund(data["payment_id"])

    async def _create_shipment(self, data: dict) -> dict:
        shipment = await self.shipping.create(order_id=data["order"]["id"])
        return {"shipment_id": shipment.id}

    async def _cancel_shipment(self, data: dict):
        if "shipment_id" in data:
            await self.shipping.cancel(data["shipment_id"])
```

## Choreography Pattern

```python
class OrderChoreography:
    """Event handlers for order saga choreography."""

    def __init__(self, event_bus, order_repo):
        self.bus = event_bus
        self.repo = order_repo

    async def handle_order_created(self, event):
        await self.bus.publish("inventory.reserve.requested", {
            "saga_id": event.saga_id,
            "items": event.payload["order"]["items"],
        })

    async def handle_inventory_reserved(self, event):
        await self.bus.publish("payment.charge.requested", {
            "saga_id": event.saga_id,
            "amount": event.payload["amount"],
        })

    async def handle_payment_failed(self, event):
        # Compensation: release inventory
        await self.bus.publish("inventory.release.requested", {
            "saga_id": event.saga_id,
            "reservation_id": event.payload["reservation_id"],
        })

    async def handle_shipment_created(self, event):
        order = await self.repo.get(event.payload["order_id"])
        order.status = "shipped"
        await self.repo.save(order)
```

## Timeout and Recovery

```python
from datetime import timedelta
import asyncio

class SagaRecovery:
    def __init__(self, saga_repo, orchestrator):
        self.repo = saga_repo
        self.orchestrator = orchestrator

    async def recover_stuck_sagas(self, timeout: timedelta = timedelta(hours=1)):
        cutoff = datetime.now(timezone.utc) - timeout
        stuck_sagas = await self.repo.find_by_status_and_age(SagaStatus.RUNNING, cutoff)

        for saga in stuck_sagas:
            try:
                await self.orchestrator.resume(saga)
            except Exception:
                await self.orchestrator._compensate(saga, saga.current_step)

    async def retry_failed_step(self, saga_id: str, max_retries: int = 3):
        saga = await self.repo.get(saga_id)
        failed_step = saga.steps[saga.current_step]

        for attempt in range(max_retries):
            try:
                failed_step.result = await failed_step.action(saga.data)
                failed_step.status = SagaStatus.COMPLETED
                await self.orchestrator.resume(saga, from_step=saga.current_step + 1)
                return
            except Exception:
                await asyncio.sleep(2 ** attempt)

        await self.orchestrator._compensate(saga, saga.current_step)
```

## Idempotency

```python
class IdempotentSagaStep:
    def __init__(self, step_name: str, idempotency_store):
        self.step_name = step_name
        self.store = idempotency_store

    async def execute(self, saga_id: str, action: Callable, *args, **kwargs):
        idempotency_key = f"{saga_id}:{self.step_name}"
        existing = await self.store.get(idempotency_key)
        if existing:
            return existing["result"]

        result = await action(*args, **kwargs)
        await self.store.set(idempotency_key, {"result": result}, ttl=timedelta(days=7))
        return result
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Pattern choice | Orchestration for complex flows, Choreography for simple |
| State storage | Persistent store (PostgreSQL) for saga state |
| Idempotency | Required for all saga steps |
| Timeouts | Per-step timeouts with recovery |
| Compensation | Always implement, test thoroughly |
| Observability | Trace saga ID across all services |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER skip compensation logic
async def _process_payment(self, data: dict):
    return await self.payment.charge(data)  # Missing compensation!

# NEVER rely on synchronous calls across services
async def _reserve_and_pay(self, data: dict):
    await self.inventory.reserve(data)
    await self.payment.charge(data)  # If fails, inventory stuck!

# NEVER ignore idempotency
async def _create_order(self, data: dict):
    return await self.db.insert(Order(**data))  # Duplicate on retry!

# NEVER use in-memory saga state
sagas = {}  # Lost on restart!

# ALWAYS persist saga state and test compensation paths
```

## Related Skills

- `temporal-io` - Durable workflow execution
- `event-sourcing` - Event-driven state management
- `idempotency-patterns` - Idempotent operations
