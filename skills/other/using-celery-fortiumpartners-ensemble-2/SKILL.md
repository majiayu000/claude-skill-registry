---
name: using-celery
description: Celery 5.3+ distributed task queue with Beat scheduler, Redis/RabbitMQ brokers, workflow patterns, and FastAPI integration. Use for background jobs, periodic tasks, and async processing.
---

# Celery & Beat Development Skill

## Quick Reference

Celery 5.3+ distributed task queue with Beat scheduler for Python applications. Background job processing, periodic scheduling, workflow patterns, and FastAPI integration.

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [When to Use](#when-to-use)
3. [Project Structure](#project-structure)
4. [Celery Application Setup](#celery-application-setup)
5. [Task Definitions](#task-definitions)
6. [Queue Routing](#queue-routing)
7. [Beat Scheduler](#beat-scheduler)
8. [Workflow Patterns](#workflow-patterns)
9. [FastAPI Integration](#fastapi-integration)
10. [Testing](#testing)
11. [CLI Commands](#cli-commands)
12. [Essential Configuration](#essential-configuration)
13. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
14. [Integration Checklist](#integration-checklist)
15. [See Also](#see-also)

---

## When to Use

This skill is loaded by `backend-developer` when:
- `celery` or `celery[redis]` in dependencies
- `celeryconfig.py` or `celery.py` present
- Beat schedule configuration detected
- User mentions "background tasks", "job queue", or "periodic tasks"
- Task decorator patterns (`@app.task`) found

**Minimum Detection Confidence**: 0.8 (80%)

**Prerequisite**: Python skill should be loaded for core patterns.

---

## Project Structure

```
my_project/
├── src/my_app/
│   ├── celery_app.py        # Celery application
│   ├── config.py            # Settings
│   ├── tasks/               # Task modules
│   │   ├── email.py
│   │   ├── reports.py
│   │   └── cleanup.py
│   └── workers/queues.py    # Queue definitions
├── tests/
│   ├── conftest.py          # Celery fixtures
│   └── tasks/
├── docker-compose.yml       # Redis + workers
└── pyproject.toml
```

---

## Celery Application Setup

```python
from celery import Celery
from kombu import Queue
from .config import settings

app = Celery(
    "my_app",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["my_app.tasks.email", "my_app.tasks.reports"],
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    task_soft_time_limit=240,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# Queue routing
app.conf.task_queues = (
    Queue("default", routing_key="default"),
    Queue("high_priority", routing_key="high"),
    Queue("low_priority", routing_key="low"),
)
```

---

## Task Definitions

### Basic Task

```python
from celery import shared_task
from my_app.celery_app import app

@shared_task(name="tasks.add")
def add(x: int, y: int) -> int:
    return x + y

@app.task(bind=True, name="tasks.send_email")
def send_email(self, to: str, subject: str, body: str) -> dict:
    task_id = self.request.id
    return {"task_id": task_id, "status": "sent"}
```

### Task with Retry Logic

```python
@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(httpx.TimeoutException, httpx.ConnectError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def call_external_api(self, endpoint: str, payload: dict) -> dict:
    with httpx.Client(timeout=30) as client:
        response = client.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
```

### Task with Rate Limiting

```python
@shared_task(bind=True, rate_limit="10/m", name="tasks.send_sms")
def send_sms(self, phone: str, message: str) -> dict:
    return sms_service.send(phone, message)
```

### Task with Time Limits

```python
from celery.exceptions import SoftTimeLimitExceeded

@shared_task(bind=True, soft_time_limit=300, time_limit=360)
def generate_report(self, report_id: int) -> dict:
    try:
        return build_report(report_id)
    except SoftTimeLimitExceeded:
        partial_save(report_id)
        raise
```

> **See [REFERENCE.md](./REFERENCE.md#task-patterns)** for manual retry, progress tracking, and custom retry backoff patterns.

---

## Queue Routing

### Route by Task

```python
app.conf.task_routes = {
    "tasks.send_email": {"queue": "high_priority"},
    "tasks.generate_report": {"queue": "low_priority"},
    "tasks.process_payment": {"queue": "payments"},
    "tasks.*": {"queue": "default"},
}
```

### Route Dynamically

```python
process_order.apply_async(args=[123], queue="high_priority")
process_order.apply_async(args=[456], routing_key="payments")
```

### Worker Queue Assignment

```bash
# High priority only
celery -A my_app.celery_app worker -Q high_priority -c 4

# Multiple queues
celery -A my_app.celery_app worker -Q default,low_priority -c 2
```

---

## Beat Scheduler

### Basic Schedule

```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    "health-check": {
        "task": "tasks.health_check",
        "schedule": 30.0,  # Every 30 seconds
    },
    "daily-report": {
        "task": "tasks.generate_daily_report",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    "weekly-summary": {
        "task": "tasks.send_weekly_summary",
        "schedule": crontab(hour=9, minute=0, day_of_week=1),  # Monday 9 AM
    },
}
```

### Crontab Quick Reference

| Pattern | Expression |
|---------|------------|
| Every minute | `crontab()` |
| Every 15 min | `crontab(minute="*/15")` |
| Daily midnight | `crontab(hour=0, minute=0)` |
| Weekdays 9 AM | `crontab(hour=9, minute=0, day_of_week="1-5")` |
| Monthly 1st | `crontab(hour=0, minute=0, day_of_month=1)` |

### Running Beat

```bash
# Standalone
celery -A my_app.celery_app beat --loglevel=info

# With worker (dev only)
celery -A my_app.celery_app worker --beat --loglevel=info
```

> **See [REFERENCE.md](./REFERENCE.md#beat-scheduler)** for dynamic database schedules and advanced crontab patterns.

---

## Workflow Patterns

### Chain (Sequential)

```python
from celery import chain

workflow = chain(
    fetch_data.s(url),
    process_data.s(),
    save_results.s(destination),
)
result = workflow.apply_async()
```

### Group (Parallel)

```python
from celery import group

workflow = group(process_image.s(id) for id in image_ids)
result = workflow.apply_async()
all_results = result.get()
```

### Chord (Parallel + Callback)

```python
from celery import chord

workflow = chord(
    (process_chunk.s(chunk) for chunk in chunks),
    aggregate_results.s()
)
result = workflow.apply_async()
```

> **See [REFERENCE.md](./REFERENCE.md#workflow-patterns)** for complex multi-step workflows and error handling in chains.

---

## FastAPI Integration

### Triggering Tasks

```python
from fastapi import APIRouter
from celery.result import AsyncResult
from .celery_app import celery_app
from .tasks.email import send_email

router = APIRouter()

@router.post("/emails/send")
async def queue_email(to: str, subject: str, body: str) -> dict:
    task = send_email.delay(to, subject, body)
    return {"task_id": task.id, "status": "queued"}

@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str) -> dict:
    result = AsyncResult(task_id, app=celery_app)
    response = {"task_id": task_id, "status": result.status, "ready": result.ready()}
    if result.ready():
        response["result"] = result.get() if result.successful() else str(result.result)
    return response
```

### Progress Tracking

```python
@shared_task(bind=True)
def process_large_file(self, file_id: int) -> dict:
    file_data = load_file(file_id)
    for i, chunk in enumerate(file_data):
        process_chunk(chunk)
        self.update_state(state="PROGRESS", meta={"current": i + 1, "total": len(file_data)})
    return {"processed": len(file_data)}
```

> **See [REFERENCE.md](./REFERENCE.md#fastapi-integration)** for polling patterns, revocation, and lifespan management.

---

## Testing

### pytest Configuration

```python
import pytest

@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "memory://",
        "result_backend": "cache+memory://",
        "task_always_eager": True,
        "task_eager_propagates": True,
    }
```

### Unit Testing (Eager Mode)

```python
def test_send_email_success(celery_app):
    with patch("my_app.tasks.email.email_client") as mock:
        mock.send.return_value = {"id": "msg_123"}
        result = send_email.delay("user@example.com", "Test", "Hello")
        assert result.successful()
        assert result.get()["status"] == "sent"
```

> **See [REFERENCE.md](./REFERENCE.md#testing)** for integration tests with real workers and Beat schedule testing.

---

## CLI Commands

### Worker Management

```bash
celery -A my_app.celery_app worker --loglevel=info
celery -A my_app.celery_app worker -c 4 -Q high,default
celery -A my_app.celery_app worker --pool=gevent -c 100
celery -A my_app.celery_app worker --autoscale=10,3
```

### Inspection

```bash
celery -A my_app.celery_app inspect active
celery -A my_app.celery_app inspect registered
celery -A my_app.celery_app inspect scheduled
celery -A my_app.celery_app inspect ping
```

### Control

```bash
celery -A my_app.celery_app control shutdown
celery -A my_app.celery_app purge
celery -A my_app.celery_app control revoke <task_id>
celery -A my_app.celery_app control rate_limit tasks.send_email 10/m
```

---

## Essential Configuration

```python
# Broker & backend
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
result_expires = 3600

# Serialization
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

# Execution
task_time_limit = 300
task_soft_time_limit = 240
task_acks_late = True
task_reject_on_worker_lost = True

# Worker
worker_prefetch_multiplier = 1
worker_concurrency = 4
```

> **See [REFERENCE.md](./REFERENCE.md#configuration)** for full configuration reference and environment-based settings.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Blocking in tasks | `time.sleep()` blocks worker | Use `countdown` or async |
| Large arguments | Megabytes through broker | Pass ID, fetch in task |
| Not idempotent | Duplicate charges on retry | Use idempotency keys |
| Ignoring results | Memory leaks in backend | Set `ignore_result=True` or configure `result_expires` |
| DB in task module | Import-time connections | Import inside task function |

> **See [REFERENCE.md](./REFERENCE.md#anti-patterns)** for detailed examples and solutions.

---

## Integration Checklist

- [ ] Celery app configured with broker/backend
- [ ] Tasks defined with proper retry logic
- [ ] Queues defined and routed appropriately
- [ ] Beat schedule configured for periodic tasks
- [ ] Tests use eager mode with memory broker
- [ ] Health check endpoint monitors workers
- [ ] Docker Compose includes Redis + workers

---

## See Also

- **[REFERENCE.md](./REFERENCE.md)** - Complete patterns, advanced configuration, monitoring setup
- **[examples/](./examples/)** - Working code examples
- **[templates/](./templates/)** - Starter templates
- [Celery Documentation](https://docs.celeryq.dev/)
- [Flower Monitoring](https://flower.readthedocs.io/)
