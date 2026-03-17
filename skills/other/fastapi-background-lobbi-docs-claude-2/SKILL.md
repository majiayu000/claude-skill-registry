---
name: FastAPI Background Tasks
description: This skill should be used when the user asks to "create background task", "add async job", "implement task queue", "schedule periodic task", "use Celery", "use ARQ", "process async", or mentions background processing, task queues, job scheduling, workers, or async jobs. Provides multiple task queue framework patterns.
version: 0.1.0
---

# FastAPI Background Task Processing

This skill provides patterns for background task processing with multiple frameworks: ARQ (recommended for async), Celery, and Dramatiq.

## ARQ (Async Redis Queue) - Recommended

### Installation

```bash
pip install arq
```

### Configuration

```python
# app/workers/config.py
from arq.connections import RedisSettings
from app.config import get_settings

settings = get_settings()

class WorkerSettings:
    redis_settings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        database=1  # Separate from cache
    )

    # Job settings
    max_jobs = 10
    job_timeout = 300  # 5 minutes
    keep_result = 3600  # 1 hour
    queue_name = "default"

    # Cron jobs
    cron_jobs = []
```

### Task Definitions

```python
# app/workers/tasks.py
from arq import cron
from typing import Dict, Any
import asyncio

async def send_email(ctx: Dict[str, Any], to: str, subject: str, body: str):
    """Send email asynchronously."""
    email_service = ctx.get("email_service")
    await email_service.send(to=to, subject=subject, body=body)
    return {"status": "sent", "to": to}

async def process_upload(ctx: Dict[str, Any], file_id: str, user_id: str):
    """Process uploaded file (resize, convert, etc.)."""
    storage = ctx.get("storage")
    file_data = await storage.get(file_id)

    # Process file
    processed = await process_file(file_data)

    # Save processed file
    await storage.put(f"processed/{file_id}", processed)

    return {"status": "processed", "file_id": file_id}

async def cleanup_expired(ctx: Dict[str, Any]):
    """Periodic cleanup of expired data."""
    db = ctx.get("db")
    result = await db.delete_expired()
    return {"deleted": result.deleted_count}

# Cron job example
@cron(hour=2, minute=0)  # Run at 2 AM daily
async def daily_report(ctx: Dict[str, Any]):
    """Generate daily report."""
    report_service = ctx.get("report_service")
    await report_service.generate_daily()
```

### Worker Entry Point

```python
# app/workers/main.py
from arq import create_pool
from arq.connections import RedisSettings
from app.workers.config import WorkerSettings
from app.workers.tasks import send_email, process_upload, cleanup_expired, daily_report
from app.infrastructure.database import init_database
from app.services.email import EmailService

async def startup(ctx: Dict[str, Any]):
    """Worker startup - initialize services."""
    await init_database()
    ctx["email_service"] = EmailService()
    ctx["db"] = get_db()

async def shutdown(ctx: Dict[str, Any]):
    """Worker shutdown - cleanup."""
    await close_database()

class WorkerSettings(WorkerSettings):
    functions = [send_email, process_upload, cleanup_expired]
    cron_jobs = [daily_report]
    on_startup = startup
    on_shutdown = shutdown

# Run with: arq app.workers.main.WorkerSettings
```

### Enqueueing Tasks from FastAPI

```python
# app/dependencies.py
from arq import ArqRedis, create_pool
from arq.connections import RedisSettings

async def get_task_queue() -> ArqRedis:
    return await create_pool(RedisSettings())

# app/routes/users.py
from fastapi import Depends
from arq import ArqRedis

@router.post("/users/{user_id}/welcome")
async def send_welcome_email(
    user_id: str,
    queue: ArqRedis = Depends(get_task_queue)
):
    user = await get_user(user_id)

    # Enqueue background task
    job = await queue.enqueue_job(
        "send_email",
        to=user.email,
        subject="Welcome!",
        body="Thanks for signing up."
    )

    return {"job_id": job.job_id, "status": "queued"}

@router.post("/uploads")
async def upload_file(
    file: UploadFile,
    user: User = Depends(get_current_user),
    queue: ArqRedis = Depends(get_task_queue)
):
    # Save file
    file_id = await save_file(file)

    # Enqueue processing
    await queue.enqueue_job(
        "process_upload",
        file_id=file_id,
        user_id=str(user.id),
        _defer_by=5  # Delay 5 seconds
    )

    return {"file_id": file_id, "status": "processing"}
```

## Celery (Battle-Tested)

### Configuration

```python
# app/workers/celery_app.py
from celery import Celery
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.workers.celery_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    worker_prefetch_multiplier=1,
)

# Periodic tasks (Celery Beat)
celery_app.conf.beat_schedule = {
    "cleanup-every-hour": {
        "task": "app.workers.celery_tasks.cleanup_expired",
        "schedule": 3600.0,
    },
    "daily-report": {
        "task": "app.workers.celery_tasks.generate_daily_report",
        "schedule": crontab(hour=2, minute=0),
    },
}
```

### Celery Tasks

```python
# app/workers/celery_tasks.py
from app.workers.celery_app import celery_app
import asyncio

def run_async(coro):
    """Helper to run async code in sync Celery tasks."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

@celery_app.task(bind=True, max_retries=3)
def send_email(self, to: str, subject: str, body: str):
    try:
        run_async(_send_email_async(to, subject, body))
        return {"status": "sent", "to": to}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

@celery_app.task
def process_upload(file_id: str, user_id: str):
    run_async(_process_upload_async(file_id, user_id))
    return {"status": "processed", "file_id": file_id}
```

## Dramatiq (Modern Celery Alternative)

### Configuration

```python
# app/workers/dramatiq_app.py
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

redis_broker = RedisBroker(url="redis://localhost:6379/0")
result_backend = RedisBackend(url="redis://localhost:6379/1")

redis_broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(redis_broker)
```

### Dramatiq Tasks

```python
# app/workers/dramatiq_tasks.py
import dramatiq

@dramatiq.actor(max_retries=3, min_backoff=1000)
def send_email(to: str, subject: str, body: str):
    # Sync implementation
    return {"status": "sent", "to": to}

@dramatiq.actor(time_limit=300000)  # 5 min timeout
def process_upload(file_id: str, user_id: str):
    return {"status": "processed", "file_id": file_id}
```

## FastAPI Built-in Background Tasks

For simple fire-and-forget tasks (no persistence):

```python
from fastapi import BackgroundTasks

async def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@router.post("/log")
async def create_log(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, message)
    return {"status": "logged"}
```

## Additional Resources

### Reference Files

For detailed patterns:
- **`references/arq-advanced.md`** - ARQ advanced patterns, retries, priorities
- **`references/celery-patterns.md`** - Celery best practices, chains, groups
- **`references/monitoring.md`** - Flower, task monitoring

### Example Files

Working examples in `examples/`:
- **`examples/arq_worker.py`** - Complete ARQ worker
- **`examples/celery_app.py`** - Celery configuration
- **`examples/task_service.py`** - Task enqueueing service
