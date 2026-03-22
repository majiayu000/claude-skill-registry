---
name: celery-tasks
description: Celery background task patterns for Python apps. Use when implementing background jobs, scheduled tasks, email sending, image processing, or any async work that shouldn't block a web request.
---

# Celery Background Tasks

## Setup
```python
# celery_app.py
from celery import Celery
from kombu import Queue

celery = Celery(
    "myapp",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.email", "app.tasks.processing"],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    task_track_started=True,
    task_acks_late=True,          # Re-queue if worker crashes
    worker_prefetch_multiplier=1,  # Fair distribution
    task_queues=[
        Queue("high", routing_key="high"),
        Queue("default", routing_key="default"),
        Queue("low", routing_key="low"),
    ],
    task_default_queue="default",
    # Retry policy
    task_max_retries=3,
    task_soft_time_limit=300,   # 5 min warning
    task_time_limit=600,        # 10 min hard kill
)
```

## Task Patterns
```python
# tasks/email.py
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 1 min between retries
    queue="high",
)
def send_welcome_email(self, user_id: int, email: str, name: str):
    try:
        logger.info(f"Sending welcome email to {email}")
        result = email_service.send(
            to=email,
            template="welcome",
            context={"name": name},
        )
        logger.info(f"Email sent: {result.id}")
        return {"status": "sent", "message_id": result.id}
    except EmailServiceError as exc:
        logger.warning(f"Email failed (attempt {self.request.retries + 1}): {exc}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))  # exponential backoff

@shared_task(queue="low", rate_limit="10/m")
def generate_thumbnail(image_path: str, sizes: list[tuple[int, int]]):
    """Rate-limited to 10/min — heavy CPU task."""
    for w, h in sizes:
        img = Image.open(image_path)
        img.thumbnail((w, h))
        img.save(f"{image_path}_{w}x{h}.jpg", optimize=True, quality=85)
```

## Calling Tasks
```python
# Fire and forget
send_welcome_email.delay(user.id, user.email, user.name)

# With explicit queue
send_welcome_email.apply_async(
    args=[user.id, user.email, user.name],
    queue="high",
    countdown=5,         # delay 5 seconds
    expires=3600,        # discard if not run within 1h
)

# Chain: run tasks in sequence
from celery import chain
result = chain(
    resize_image.s(image_path),
    upload_to_s3.s(bucket="uploads"),
    notify_user.s(user_id=user.id),
).delay()

# Group: run tasks in parallel
from celery import group
job = group(
    send_welcome_email.s(u.id, u.email, u.name)
    for u in new_users
)
job.apply_async()
```

## Scheduled Tasks (Celery Beat)
```python
from celery.schedules import crontab

celery.conf.beat_schedule = {
    "cleanup-expired-sessions": {
        "task": "app.tasks.cleanup.remove_expired_sessions",
        "schedule": crontab(minute=0, hour=3),  # Daily at 3am
    },
    "send-digest-emails": {
        "task": "app.tasks.email.send_weekly_digest",
        "schedule": crontab(day_of_week="monday", hour=9, minute=0),
    },
}
```

## Docker Compose Setup
```yaml
worker:
  build: .
  command: celery -A app.celery_app worker --loglevel=info --concurrency=4 -Q high,default,low
  env_file: [.env]
  depends_on: [redis]

beat:
  build: .
  command: celery -A app.celery_app beat --loglevel=info
  env_file: [.env]
  depends_on: [redis]

flower:
  build: .
  command: celery -A app.celery_app flower --port=5555
  ports: ["5555:5555"]
```

## Rules
- Always use `bind=True` + `self.retry()` for retryable tasks (email, API calls)
- Never put database sessions in tasks — create fresh session inside task
- Use queues to prioritize: high (user-facing), default, low (batch)
- `task_acks_late=True` + `worker_prefetch_multiplier=1` for reliability
- Idempotent tasks: safe to run twice (check if already done before acting)
- Log task start, success, and failure with task ID for debugging
- Monitor with Flower (web dashboard) or Datadog/Grafana
