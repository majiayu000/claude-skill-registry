---
name: celery-advanced
description: Advanced Celery patterns including canvas workflows, priority queues, rate limiting, multi-queue routing, and production monitoring. Use when implementing complex task orchestration, task prioritization, or enterprise-grade background processing.
context: fork
agent: python-performance-engineer
version: 1.0.0
tags: [celery, canvas, workflow, priority-queue, rate-limiting, task-routing, flower, 2026]
author: SkillForge
user-invocable: false
---

# Advanced Celery Patterns

Enterprise-grade task orchestration beyond basic background jobs.

## When to Use

- Complex multi-step task workflows (ETL pipelines, order processing)
- Priority-based task processing (premium vs standard users)
- Rate-limited external API calls (API quotas, throttling)
- Multi-queue routing (dedicated workers per task type)
- Production monitoring and observability
- Task result aggregation and fan-out patterns

## Canvas Workflows

### Signatures (Task Invocation)

```python
from celery import signature, chain, group, chord

# Create a reusable task signature
sig = signature("tasks.process_order", args=[order_id], kwargs={"priority": "high"})

# Immutable signature (won't receive results from previous task)
sig = process_order.si(order_id)

# Partial signature (curry arguments)
partial_sig = send_email.s(subject="Order Update")
# Later: partial_sig.delay(to="user@example.com", body="...")
```

### Chains (Sequential Execution)

```python
from celery import chain

# Tasks execute sequentially, passing results
workflow = chain(
    extract_data.s(source_id),      # Returns raw_data
    transform_data.s(),              # Receives raw_data, returns clean_data
    load_data.s(destination_id),     # Receives clean_data
)
result = workflow.apply_async()

# Access intermediate results
chain_result = result.get()  # Final result
parent_result = result.parent.get()  # Previous task result

# Error handling in chains
@celery_app.task(bind=True)
def transform_data(self, raw_data):
    try:
        return do_transform(raw_data)
    except TransformError as exc:
        # Chain stops here, no subsequent tasks run
        raise self.retry(exc=exc, countdown=60)
```

### Groups (Parallel Execution)

```python
from celery import group

# Execute tasks in parallel
parallel = group(
    process_chunk.s(chunk) for chunk in chunks
)
group_result = parallel.apply_async()

# Wait for all to complete
results = group_result.get()  # List of results

# Check completion status
group_result.ready()      # All completed?
group_result.successful() # All succeeded?
group_result.failed()     # Any failed?

# Iterate as they complete
for result in group_result:
    if result.ready():
        print(f"Completed: {result.get()}")
```

### Chords (Parallel + Callback)

```python
from celery import chord

# Parallel execution with callback when all complete
workflow = chord(
    [process_chunk.s(chunk) for chunk in chunks],
    aggregate_results.s()  # Receives list of all results
)
result = workflow.apply_async()

# Chord with header and body
header = group(fetch_data.s(url) for url in urls)
body = combine_data.s()
workflow = chord(header, body)

# Error handling: if any header task fails, body won't run
@celery_app.task(bind=True)
def aggregate_results(self, results):
    # results = [result1, result2, ...]
    return sum(results)
```

### Map and Starmap

```python
# Map: apply same task to each item
workflow = process_item.map([item1, item2, item3])

# Starmap: unpack args for each call
workflow = send_email.starmap([
    ("user1@example.com", "Subject 1"),
    ("user2@example.com", "Subject 2"),
])

# Chunks: split large list into batches
workflow = process_item.chunks(items, batch_size=100)
```

## Priority Queues

### Queue Configuration

```python
# celery_config.py
from kombu import Queue

celery_app.conf.task_queues = (
    Queue("high", routing_key="high"),
    Queue("default", routing_key="default"),
    Queue("low", routing_key="low"),
)

celery_app.conf.task_default_queue = "default"
celery_app.conf.task_default_routing_key = "default"

# Priority within queue (requires Redis 5+)
celery_app.conf.broker_transport_options = {
    "priority_steps": list(range(10)),  # 0-9 priority levels
    "sep": ":",
    "queue_order_strategy": "priority",
}
```

### Task Routing

```python
# Route by task name
celery_app.conf.task_routes = {
    "tasks.critical_task": {"queue": "high"},
    "tasks.bulk_*": {"queue": "low"},
    "tasks.default_*": {"queue": "default"},
}

# Route dynamically at call time
critical_task.apply_async(args=[data], queue="high", priority=9)
bulk_task.apply_async(args=[data], queue="low", priority=1)

# Route by task attribute
@celery_app.task(queue="high", priority=8)
def premium_user_task(user_id):
    pass
```

### Worker Configuration

```bash
# Start workers for specific queues
celery -A app worker -Q high -c 4 --prefetch-multiplier=1
celery -A app worker -Q default -c 8
celery -A app worker -Q low -c 2 --prefetch-multiplier=4
```

## Rate Limiting

### Per-Task Rate Limits

```python
@celery_app.task(rate_limit="100/m")  # 100 per minute
def call_external_api(endpoint):
    return requests.get(endpoint)

@celery_app.task(rate_limit="10/s")   # 10 per second
def send_notification(user_id):
    pass

@celery_app.task(rate_limit="1000/h") # 1000 per hour
def bulk_email(batch):
    pass
```

### Dynamic Rate Limiting

```python
from celery import current_app

# Change rate limit at runtime
current_app.control.rate_limit(
    "tasks.call_external_api",
    "50/m",  # Reduce during high load
    destination=["worker1@hostname"],
)

# Custom rate limiter with token bucket
from celery.utils.time import rate
from celery_singleton import Singleton

class RateLimitedTask(celery_app.Task):
    _rate_limit_key = "api:rate_limit"

    def __call__(self, *args, **kwargs):
        if not self._acquire_token():
            self.retry(countdown=self._get_backoff())
        return super().__call__(*args, **kwargs)

    def _acquire_token(self):
        return redis_client.set(
            self._rate_limit_key,
            "1",
            nx=True,
            ex=1  # 1 second window
        )
```

## Multi-Queue Routing

### Router Classes

```python
class TaskRouter:
    def route_for_task(self, task, args=None, kwargs=None):
        if task.startswith("tasks.premium"):
            return {"queue": "premium", "priority": 8}
        elif task.startswith("tasks.analytics"):
            return {"queue": "analytics"}
        elif kwargs and kwargs.get("urgent"):
            return {"queue": "high"}
        return {"queue": "default"}

celery_app.conf.task_routes = (TaskRouter(),)
```

### Content-Based Routing

```python
@celery_app.task(bind=True)
def process_order(self, order):
    # Route based on order value
    if order["total"] > 1000:
        self.update_state(state="ROUTING", meta={"queue": "premium"})
        return chain(
            verify_inventory.s(order).set(queue="high"),
            process_payment.s().set(queue="high"),
            notify_customer.s().set(queue="notifications"),
        ).apply_async()
    else:
        return standard_workflow(order)
```

## Production Monitoring

### Flower Dashboard

```bash
# Install and run Flower
pip install flower
celery -A app flower --port=5555 --basic_auth=admin:password

# With persistent storage
celery -A app flower --persistent=True --db=flower.db
```

### Custom Events

```python
from celery import signals

@signals.task_prerun.connect
def on_task_start(sender, task_id, task, args, kwargs, **_):
    metrics.counter("task_started", tags={"task": task.name})

@signals.task_postrun.connect
def on_task_complete(sender, task_id, task, args, kwargs, retval, state, **_):
    metrics.counter("task_completed", tags={"task": task.name, "state": state})

@signals.task_failure.connect
def on_task_failure(sender, task_id, exception, args, kwargs, traceback, einfo, **_):
    alerting.send_alert(
        f"Task {sender.name} failed: {exception}",
        severity="error"
    )
```

### Health Checks

```python
from celery import current_app

def celery_health_check():
    try:
        # Check broker connection
        conn = current_app.connection()
        conn.ensure_connection(max_retries=3)

        # Check workers responding
        inspector = current_app.control.inspect()
        active_workers = inspector.active()

        if not active_workers:
            return {"status": "unhealthy", "reason": "No active workers"}

        return {
            "status": "healthy",
            "workers": list(active_workers.keys()),
            "active_tasks": sum(len(tasks) for tasks in active_workers.values()),
        }
    except Exception as e:
        return {"status": "unhealthy", "reason": str(e)}
```

## Custom Task States

```python
from celery import states

# Define custom states
VALIDATING = "VALIDATING"
PROCESSING = "PROCESSING"
UPLOADING = "UPLOADING"

@celery_app.task(bind=True)
def long_running_task(self, data):
    self.update_state(state=VALIDATING, meta={"step": 1, "total": 3})
    validate(data)

    self.update_state(state=PROCESSING, meta={"step": 2, "total": 3})
    result = process(data)

    self.update_state(state=UPLOADING, meta={"step": 3, "total": 3})
    upload(result)

    return {"status": "complete", "url": result.url}

# Query task progress
from celery.result import AsyncResult

result = AsyncResult(task_id)
if result.state == PROCESSING:
    print(f"Step {result.info['step']}/{result.info['total']}")
```

## Base Tasks and Inheritance

```python
from celery import Task

class DatabaseTask(Task):
    """Base task with database session management."""
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = create_session()
        return self._db

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self._db:
            self._db.close()
            self._db = None

class RetryableTask(Task):
    """Base task with exponential backoff retry."""
    autoretry_for = (ConnectionError, TimeoutError)
    max_retries = 5
    retry_backoff = True
    retry_backoff_max = 600
    retry_jitter = True

@celery_app.task(base=DatabaseTask)
def query_database(query):
    return query_database.db.execute(query)

@celery_app.task(base=RetryableTask)
def call_flaky_api(endpoint):
    return requests.get(endpoint, timeout=30)
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Workflow type | Chain for sequential, Group for parallel, Chord for fan-in |
| Priority queues | 3 queues (high/default/low) for most use cases |
| Rate limiting | Per-task `rate_limit` for simple, token bucket for complex |
| Monitoring | Flower + custom signals for production |
| Task routing | Content-based router for dynamic routing needs |
| Worker scaling | Separate workers per queue, autoscale with HPA |
| Error handling | Base task with retry + dead letter queue |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER block on results in tasks
@celery_app.task
def bad_task():
    result = other_task.delay()
    return result.get()  # Blocks worker, causes deadlock!

# NEVER use synchronous I/O without timeout
requests.get(url)  # Can hang forever

# NEVER ignore task acknowledgment
celery_app.conf.task_acks_late = False  # Default loses tasks on crash

# NEVER skip idempotency for retried tasks
@celery_app.task(max_retries=3)
def create_order(order):
    Order.create(order)  # Creates duplicates on retry!

# ALWAYS use immutable signatures in chords
chord([task.s(x) for x in items], callback.si())  # si() prevents arg pollution
```

## References

For detailed implementation patterns, see:

- `references/canvas-workflows.md` - Deep dive on chain/group/chord with error handling
- `references/priority-queue-setup.md` - Redis priority queue configuration
- `references/rate-limiting-patterns.md` - Per-task and dynamic rate limiting
- `references/celery-beat-scheduling.md` - Periodic task configuration

## Templates

Production-ready code templates:

- `templates/celery-config-template.py` - Complete production Celery configuration
- `templates/canvas-workflow-template.py` - ETL pipeline using canvas patterns
- `templates/priority-worker-template.py` - Multi-queue worker with per-user rate limiting

## Checklists

- `checklists/celery-production-checklist.md` - Production deployment verification

## Examples

- `examples/order-processing-pipeline.md` - Real-world e-commerce order processing

## Related Skills

- `background-jobs` - Basic Celery and ARQ patterns
- `message-queues` - RabbitMQ/Kafka integration
- `resilience-patterns` - Circuit breakers, retries
- `observability-monitoring` - Metrics and alerting

## Capability Details

### canvas-workflows
**Keywords:** chain, group, chord, signature, canvas, workflow
**Solves:**
- Complex multi-step task pipelines
- Parallel task execution with aggregation
- Sequential task dependencies

### priority-queues
**Keywords:** priority, queue, routing, high priority, low priority
**Solves:**
- Premium user task prioritization
- Urgent vs batch task handling
- Multi-queue worker deployment

### rate-limiting
**Keywords:** rate limit, throttle, quota, api limit
**Solves:**
- External API rate limiting
- Per-task execution limits
- Dynamic rate adjustment

### task-monitoring
**Keywords:** flower, monitoring, health check, task state
**Solves:**
- Production task monitoring
- Worker health checks
- Custom task state tracking
