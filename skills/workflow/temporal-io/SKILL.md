---
name: temporal-io
description: Temporal.io workflow orchestration for durable, fault-tolerant distributed applications. Use when implementing long-running workflows, saga patterns, microservice orchestration, or systems requiring exactly-once execution guarantees.
context: fork
agent: workflow-architect
version: 1.0.0
tags: [temporal, workflow, orchestration, durable-execution, saga, microservices, 2026]
author: SkillForge
user-invocable: false
---

# Temporal.io Workflow Orchestration

Durable execution engine for reliable distributed applications.

## Overview

- Long-running business processes (days/weeks/months)
- Saga patterns requiring compensation/rollback
- Microservice orchestration with retries
- Systems requiring exactly-once execution guarantees
- Complex state machines with human-in-the-loop
- Scheduled and recurring workflows

## Workflow Definition

```python
from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta

@workflow.defn
class OrderWorkflow:
    def __init__(self):
        self._status = "pending"
        self._order_id: str | None = None

    @workflow.run
    async def run(self, order_data: OrderInput) -> OrderResult:
        self._order_id = await workflow.execute_activity(
            create_order, order_data,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3, initial_interval=timedelta(seconds=1)),
        )
        self._status = "processing"

        # Parallel activities
        payment, inventory = await asyncio.gather(
            workflow.execute_activity(process_payment, PaymentInput(order_id=self._order_id), start_to_close_timeout=timedelta(minutes=5)),
            workflow.execute_activity(reserve_inventory, InventoryInput(order_id=self._order_id), start_to_close_timeout=timedelta(minutes=2)),
        )

        self._status = "completed"
        return OrderResult(order_id=self._order_id, payment_id=payment.id)

    @workflow.query
    def get_status(self) -> str:
        return self._status

    @workflow.signal
    async def cancel_order(self, reason: str):
        self._status = "cancelling"
        await workflow.execute_activity(cancel_order_activity, CancelInput(order_id=self._order_id), start_to_close_timeout=timedelta(seconds=30))
        self._status = "cancelled"
```

## Activity Definition

```python
from temporalio import activity
from temporalio.exceptions import ApplicationError

@activity.defn
async def process_payment(input: PaymentInput) -> PaymentResult:
    activity.logger.info(f"Processing payment for order {input.order_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("https://payments.example.com/charge", json={"order_id": input.order_id, "amount": input.amount})
            response.raise_for_status()
            return PaymentResult(**response.json())
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 402:
            raise ApplicationError("Payment declined", non_retryable=True, type="PaymentDeclined")
        raise

@activity.defn
async def send_notification(input: NotificationInput) -> None:
    for i, recipient in enumerate(input.recipients):
        activity.heartbeat(f"Sending {i+1}/{len(input.recipients)}")  # For long operations
        await send_email(recipient, input.subject, input.body)
```

## Worker and Client

```python
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="order-processing",
        workflows=[OrderWorkflow],
        activities=[create_order, process_payment, reserve_inventory, cancel_order_activity],
    )
    await worker.run()

async def start_order_workflow(order_data: OrderInput) -> str:
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        OrderWorkflow.run, order_data,
        id=f"order-{order_data.order_id}",
        task_queue="order-processing",
    )
    return handle.id

async def get_order_status(workflow_id: str) -> str:
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(workflow_id)
    return await handle.query(OrderWorkflow.get_status)
```

## Saga Pattern with Compensation

```python
@workflow.defn
class OrderSagaWorkflow:
    @workflow.run
    async def run(self, order: OrderInput) -> OrderResult:
        compensations: list[tuple[Callable, Any]] = []

        try:
            reservation = await workflow.execute_activity(reserve_inventory, order.items, start_to_close_timeout=timedelta(minutes=2))
            compensations.append((release_inventory, reservation.id))

            payment = await workflow.execute_activity(charge_payment, PaymentInput(order_id=order.id), start_to_close_timeout=timedelta(minutes=5))
            compensations.append((refund_payment, payment.id))

            shipment = await workflow.execute_activity(create_shipment, ShipmentInput(order_id=order.id), start_to_close_timeout=timedelta(minutes=3))
            return OrderResult(order_id=order.id, payment_id=payment.id, shipment_id=shipment.id)

        except Exception:
            workflow.logger.warning(f"Saga failed, running {len(compensations)} compensations")
            for compensate_fn, compensate_arg in reversed(compensations):
                try:
                    await workflow.execute_activity(compensate_fn, compensate_arg, start_to_close_timeout=timedelta(minutes=2))
                except Exception as e:
                    workflow.logger.error(f"Compensation failed: {e}")
            raise
```

## Timers and Scheduling

```python
@workflow.defn
class TimeoutWorkflow:
    @workflow.run
    async def run(self, input: TaskInput) -> TaskResult:
        try:
            await workflow.wait_condition(lambda: self._approved is not None, timeout=timedelta(hours=24))
        except asyncio.TimeoutError:
            return TaskResult(status="auto_rejected")
        return TaskResult(status="approved" if self._approved else "rejected")

    @workflow.signal
    async def approve(self, approved: bool):
        self._approved = approved
```

## Testing

```python
import pytest
from temporalio.testing import WorkflowEnvironment

@pytest.fixture
async def workflow_env():
    async with await WorkflowEnvironment.start_local() as env:
        yield env

@pytest.mark.asyncio
async def test_order_workflow(workflow_env):
    async with Worker(workflow_env.client, task_queue="test", workflows=[OrderWorkflow], activities=[create_order, process_payment]):
        result = await workflow_env.client.execute_workflow(
            OrderWorkflow.run, OrderInput(id="test-1", total=100),
            id="test-order-1", task_queue="test",
        )
        assert result.order_id == "test-1"
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Workflow ID | Business-meaningful, idempotent (e.g., `order-{order_id}`) |
| Task queue | Per-service or per-workflow-type |
| Activity timeout | `start_to_close` for most cases |
| Retry policy | 3 attempts default, exponential backoff |
| Heartbeating | Required for activities > 60s |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER do non-deterministic operations in workflows
if random.random() > 0.5:  # Different on replay!
if datetime.now() > deadline:  # Different on replay!

# CORRECT: Use workflow APIs
if await workflow.random() > 0.5:
if workflow.now() > deadline:

# NEVER make network calls directly in workflows
response = await httpx.get("https://api.example.com")  # WRONG!

# CORRECT: Use activities for I/O
response = await workflow.execute_activity(fetch_data, ...)

# NEVER ignore activity idempotency - use upsert with order_id as key
```

## Related Skills

- `saga-patterns` - Distributed transaction patterns
- `message-queues` - Event-driven integration
- `resilience-patterns` - Retry and circuit breaker patterns
