---
name: temporal-python-pro
description: Master Temporal workflow orchestration using the Python SDK. Use PROACTIVELY for workflow design, microservice orchestration, long-running processes, saga pattern implementation, distributed transactions, or any durable execution patterns. Covers workflows, activities, determinism, testing strategies, and production deployment with Python-specific best practices and common pitfalls.
---

# Temporal Python Pro

Master durable workflow orchestration with Temporal's Python SDK. This skill provides comprehensive guidance for building reliable, scalable distributed systems using workflows and activities.

## When to Use This Skill

Use this skill proactively when:
- Designing or implementing Temporal workflows in Python
- Debugging workflow determinism issues or replay failures
- Implementing saga patterns for distributed transactions
- Setting up testing strategies for Temporal applications
- Deploying Temporal workers to production
- Optimizing workflow performance and resource utilization
- Troubleshooting common Temporal Python pitfalls
- Onboarding to Temporal Python SDK

## Core Concepts

### Workflows

Workflows define the orchestration logic. They MUST be deterministic - same inputs must produce same outputs.

```python
from datetime import timedelta
from temporalio import workflow

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        # Orchestrates activities
        await workflow.execute_activity(
            reserve_inventory,
            order_id,
            start_to_close_timeout=timedelta(seconds=30)
        )

        await workflow.execute_activity(
            process_payment,
            order_id,
            start_to_close_timeout=timedelta(seconds=30)
        )

        return f"Order {order_id} completed"
```

### Activities

Activities perform non-deterministic operations (I/O, API calls, database operations).

```python
from temporalio import activity

@activity.defn
async def reserve_inventory(order_id: str) -> None:
    # Business logic and I/O operations
    inventory_system.reserve(order_id)
```

### Determinism Rules

**CRITICAL**: Workflow code must be deterministic.

**Forbidden in workflows:**
- `datetime.now()`, `time.time()` → Use `workflow.now()`
- `random.choice()`, `random.random()` → Move to activity
- `uuid.uuid4()` → Use `workflow.uuid()` or activity
- `asyncio.wait()` with activities → Use `asyncio.gather()`
- File I/O, network calls → Move to activities
- Global mutable state → Use workflow instance variables

## Common Pitfalls

### AI-Generated Code Issues

AI often generates non-deterministic workflow code. Watch for:

1. **System time in workflows**
   ```python
   # ❌ WRONG (AI-generated)
   timestamp = datetime.now()

   # ✅ CORRECT
   timestamp = workflow.now()
   ```

2. **Random numbers in workflows**
   ```python
   # ❌ WRONG (AI-generated)
   choice = random.choice(options)

   # ✅ CORRECT
   choice = await workflow.execute_activity(
       random_choice, options
   )
   ```

3. **Business logic in workflows**
   ```python
   # ❌ WRONG
   processed = complex_transform(data)  # In workflow

   # ✅ CORRECT
   processed = await workflow.execute_activity(
       transform, data
   )
   ```

### Non-Idempotent Activities

Activities MUST be idempotent - retries should not cause side effects.

```python
# ❌ NOT IDEMPOTENT
@activity.defn
async def charge_card(amount: float):
    payment_gateway.charge(amount)  # Charges twice on retry!

# ✅ IDEMPOTENT
@activity.defn
async def charge_card(charge_id: str, amount: float):
    payment_gateway.charge_with_idempotency_key(charge_id, amount)
```

## Testing Strategy

### Unit Tests with Time Skipping

```python
import pytest
from temporalio.testing import WorkflowEnvironment

@pytest.mark.asyncio
async def test_order_workflow():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[OrderWorkflow],
            activities=[mock_activities]
        ):
            result = await env.client.execute_workflow(
                OrderWorkflow.run,
                "order-123",
                id="test-order",
                task_queue="test-queue"
            )

            assert result.success
```

### Replay Testing (Required Before Deploying)

Always test workflow replay with production history to catch non-determinism.

```python
async def test_replay_production():
    # Fetch history from production
    handle = prod_client.get_workflow_handle("prod-workflow-id")
    history = await handle.fetch_history()

    # Replay in test
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[MyWorkflow],  # NEW code
            activities=[mock_activities]
        ):
            # Fails if non-deterministic!
            await env.client.execute_workflow(
                MyWorkflow.run,
                args,
                id="replay-test",
                task_queue="test-queue",
                replay_history=history
            )
```

## Production Deployment

### Worker Configuration

```python
from temporalio.worker import Worker

worker = Worker(
    client,
    task_queue="production-queue",
    workflows=[MyWorkflows],
    activities=[MyActivities],
    max_concurrent_activities=50,
    max_concurrent_workflow_tasks=20
)
```

### Graceful Shutdown

```python
import signal

shutdown_event = asyncio.Event()

def handler(sig, frame):
    shutdown_event.set()

signal.signal(signal.SIGTERM, handler)

await worker.run_until(shutdown_event.is_set)
await worker.shutdown()  # Graceful shutdown
```

## Quick Reference

### When to Use Temporal

**Use Temporal for:**
- Long-running processes (minutes to months)
- Multi-step orchestrations with human approval
- Reliable retries and compensation
- Distributed transactions (saga pattern)
- Stateful workflows across failures

**Use regular async for:**
- Fast operations (< 10 seconds)
- Simple orchestration
- No durability required

### Key Resources

- [Core Concepts](references/core-concepts.md) - Workflows, activities, determinism, signals, queries
- [Best Practices](references/best-practices.md) - Workflow design, activity patterns, error handling
- [Common Pitfalls](references/common-pitfalls.md) - Determinism violations, AI mistakes, production issues
- [Testing Guide](references/testing.md) - Unit tests, integration tests, replay testing, time skipping
- [Production Deployment](references/production.md) - Worker config, monitoring, scaling, security

### Pre-Deployment Checklist

Before deploying workflow code:

- [ ] All time references use `workflow.now()`
- [ ] No `random`, `uuid`, `datetime` modules in workflows
- [ ] No `asyncio.wait()` with activities
- [ ] All activities are idempotent
- [ ] All activities have appropriate timeouts
- [ ] Business logic moved to activities
- [ ] Workflow replay tested with production history
- [ ] Search attributes configured for queries
- [ ] Unit tests pass with time skipping
- [ ] Integration tests with real activities pass
