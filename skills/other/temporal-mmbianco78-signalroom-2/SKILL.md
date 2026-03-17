---
name: temporal
description: Temporal.io workflow orchestration for SignalRoom. Use when designing workflows, debugging activities, managing schedules, or troubleshooting stuck workflows.
---

# Temporal Workflow Orchestration

## Architecture

```
Temporal Cloud (signalroom-713.nzg5u)
    │
    ├── Schedules (cron triggers)
    │
    └── Workflows (orchestration)
            │
            └── Activities (actual work)
                    │
                    └── dlt Pipelines / Reports / Notifications
```

## Key Concepts

| Concept | Purpose | Location |
|---------|---------|----------|
| **Workflow** | Orchestration logic (no I/O) | `temporal/workflows.py` |
| **Activity** | Retryable unit of work | `temporal/activities.py` |
| **Worker** | Process that executes workflows/activities | `workers/main.py` |
| **Schedule** | Cron-like trigger | Temporal Cloud UI |

## Workflows vs Activities

**Workflows** (pure orchestration):
- No I/O, no network calls, no file access
- Must be deterministic (same input = same output)
- Can call activities and wait for results

**Activities** (actual work):
- API calls, database writes, file operations
- Retried automatically on failure
- Can be long-running

## SignalRoom Workflows

```python
# Sync a single source
SyncSourceWorkflow(source_name, resources, notify_on_success, notify_on_failure)

# Sync multiple sources sequentially
ScheduledSyncWorkflow(sources)

# Run and send a report
RunReportWorkflow(report_name, channel, send)
```

## Triggering Workflows

```bash
# Via script (recommended)
python scripts/trigger_workflow.py everflow -w

# Programmatically
from signalroom.temporal.config import get_temporal_client

client = await get_temporal_client()
await client.start_workflow(
    SyncSourceWorkflow.run,
    args=[...],
    id="sync-everflow-manual",
    task_queue="api-tasks"
)
```

## Schedules

### Active Schedules

| Schedule ID | Cron | Workflow |
|-------------|------|----------|
| `hourly-sync-everflow-redtrack` | `0 12-23 * * *` (7am-11pm ET) | ScheduledSyncWorkflow |
| `daily-sync-s3` | `0 11 * * *` (6am ET) | SyncSourceWorkflow |

### Managing Schedules

```bash
# Setup/update schedules
python scripts/setup_schedules.py

# Delete all schedules
python scripts/setup_schedules.py --delete
```

### Temporal Cloud UI

https://cloud.temporal.io/namespaces/signalroom-713.nzg5u/schedules

## Retry Policy

Defined in `temporal/config.py`:

```python
RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    maximum_interval=timedelta(minutes=5),
    backoff_coefficient=2.0,
    maximum_attempts=5,
    non_retryable_error_types=["ValueError", "KeyError"],
)
```

## Debugging Stuck Workflows

### 1. Check Temporal UI

https://cloud.temporal.io/namespaces/signalroom-713.nzg5u/workflows

Look for:
- Workflow status (Running, Completed, Failed)
- Pending activities
- Event history

### 2. Check Worker Logs

```bash
# Local
make logs-worker

# Fly.io
fly logs
```

### 3. Common Issues

**"Activity timed out"**
- Pipeline took > 30 minutes
- Worker crashed mid-activity

**"No worker available"**
- Worker not running
- Wrong task queue

**"Workflow stuck in Running"**
- Activity repeatedly failing and retrying
- Check activity error in event history

## UnsandboxedWorkflowRunner

Temporal sandboxes workflows by default. If you get `RestrictedWorkflowAccessError` from imports like `structlog`:

```python
from temporalio.worker import UnsandboxedWorkflowRunner

worker = Worker(
    client,
    task_queue=settings.temporal_task_queue,
    workflows=[...],
    activities=[...],
    workflow_runner=UnsandboxedWorkflowRunner(),  # Add this
)
```

## Activity Patterns

### Async Context

Activities run in async context. Don't use `asyncio.run()` inside:

```python
# WRONG - nested event loop
@activity.defn
async def my_activity():
    result = some_sync_function_that_uses_asyncio_run()  # Fails!

# RIGHT - await directly
@activity.defn
async def my_activity():
    result = await some_async_function()
```

### Heartbeats (Long-Running)

For activities > 1 minute:

```python
@activity.defn
async def long_activity():
    for batch in batches:
        activity.heartbeat()  # Prevent timeout
        await process(batch)
```

## Resources

- [Temporal Cloud UI](https://cloud.temporal.io/namespaces/signalroom-713.nzg5u)
- [Temporal Python SDK](https://docs.temporal.io/develop/python)
- [Workflow Patterns](https://docs.temporal.io/develop/python/core-application)
