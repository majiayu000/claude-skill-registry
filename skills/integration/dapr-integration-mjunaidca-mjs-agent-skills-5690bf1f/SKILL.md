---
name: dapr-integration
description: Integrate Dapr for pub/sub messaging and scheduled jobs. Use this skill when implementing event-driven architectures with Dapr, handling CloudEvent message formats, setting up pub/sub subscriptions, or scheduling jobs with Dapr Jobs API. Covers common pitfalls like CloudEvent unwrapping and callback URL patterns.
---

# Dapr Integration

Integrate Dapr sidecar for pub/sub messaging, state management, and scheduled jobs in Kubernetes environments.

## When to Use

- Setting up Dapr pub/sub for event-driven microservices
- Scheduling jobs with Dapr Jobs API (v1.0-alpha1)
- Handling CloudEvent message formats
- Implementing subscription handlers in FastAPI
- Debugging Dapr integration issues

## Quick Start

```bash
# Install Dapr CLI
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Initialize Dapr (local)
dapr init

# Run app with Dapr sidecar
dapr run --app-id myapp --app-port 8000 -- uvicorn main:app
```

## Core Patterns

### 1. Pub/Sub Subscription Handler (FastAPI)

```python
from fastapi import APIRouter, Request
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/dapr", tags=["Dapr"])

# Topics we subscribe to
SUBSCRIPTIONS = [
    {"pubsubname": "taskflow-pubsub", "topic": "task-events", "route": "/dapr/events/task-events"},
    {"pubsubname": "taskflow-pubsub", "topic": "reminders", "route": "/dapr/events/reminders"},
]

@router.get("/subscribe")
async def get_subscriptions() -> list[dict]:
    """Dapr calls this on startup to discover subscriptions."""
    return SUBSCRIPTIONS
```

### 2. CloudEvent Handling (CRITICAL)

Dapr wraps all pub/sub messages in CloudEvent format. **You MUST unwrap it.**

```python
@router.post("/events/task-events")
async def handle_task_events(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        # Step 1: Get raw CloudEvent
        raw_event = await request.json()

        # Step 2: ALWAYS unwrap CloudEvent "data" field
        # CloudEvent structure:
        # {
        #   "data": {              <-- Your payload is HERE
        #     "event_type": "task.created",
        #     "data": {...},
        #     "timestamp": "..."
        #   },
        #   "datacontenttype": "application/json",
        #   "id": "...",
        #   "pubsubname": "taskflow-pubsub",
        #   "source": "myapp",
        #   "topic": "task-events",
        #   ...
        # }
        event = raw_event.get("data", raw_event)  # Unwrap or use as-is

        # Step 3: Now access your payload
        event_type = event.get("event_type")  # "task.created"
        data = event.get("data", {})          # Your actual data

        # Process event...

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.exception("Error handling event: %s", e)
        # Return SUCCESS to prevent Dapr retries for bad events
        return {"status": "SUCCESS"}
```

### 3. Publishing Events

```python
import httpx

DAPR_HTTP_ENDPOINT = "http://localhost:3500"
PUBSUB_NAME = "taskflow-pubsub"

async def publish_event(
    topic: str,
    event_type: str,
    data: dict,
) -> bool:
    """Publish event to Dapr pub/sub."""
    url = f"{DAPR_HTTP_ENDPOINT}/v1.0/publish/{PUBSUB_NAME}/{topic}"

    payload = {
        "event_type": event_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=payload)
            return response.status_code == 204
    except Exception as e:
        logger.error("Failed to publish event: %s", e)
        return False
```

### 4. Dapr Jobs API (Scheduled Jobs)

**CRITICAL**: Dapr Jobs v1.0-alpha1 calls back to `/job/{job_name}` by default!

```python
# Scheduling a job
async def schedule_job(
    job_name: str,
    due_time: datetime,
    data: dict,
    dapr_http_endpoint: str = "http://localhost:3500",
) -> bool:
    """Schedule a one-time Dapr job."""
    url = f"{dapr_http_endpoint}/v1.0-alpha1/jobs/{job_name}"

    payload = {
        "dueTime": due_time.strftime("%Y-%m-%dT%H:%M:%SZ"),  # RFC3339
        "data": data,
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=payload)
            return response.status_code == 204
    except Exception as e:
        logger.error("Failed to schedule job: %s", e)
        return False
```

**Handling the callback** - Dapr calls `/job/{job_name}`, NOT a custom endpoint:

```python
# WRONG - Dapr won't call this!
@router.post("/api/jobs/trigger")
async def handle_trigger(...):
    pass

# CORRECT - This is what Dapr actually calls
@router.post("/job/{job_name}")
async def handle_dapr_job_callback(
    job_name: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Handle Dapr Jobs v1.0-alpha1 callback.

    Dapr calls POST /job/{job_name} when a scheduled job fires.
    """
    try:
        body = await request.json()
        job_data = body.get("data", body)  # Unwrap if needed

        task_id = job_data.get("task_id")
        job_type = job_data.get("type")

        logger.info("Job callback: job=%s, type=%s", job_name, job_type)

        if job_type == "reminder":
            return await handle_reminder(session, job_data)
        elif job_type == "spawn":
            return await handle_spawn(session, task_id)

        return {"status": "unknown_type"}

    except Exception as e:
        logger.exception("Error handling job %s: %s", job_name, e)
        return {"status": "error"}
```

### 5. Deleting Scheduled Jobs

```python
async def delete_job(
    job_name: str,
    dapr_http_endpoint: str = "http://localhost:3500",
) -> bool:
    """Cancel a scheduled Dapr job."""
    url = f"{dapr_http_endpoint}/v1.0-alpha1/jobs/{job_name}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.delete(url)
            # 204 = deleted, 500 = not found (both OK)
            return response.status_code in (204, 500)
    except Exception as e:
        logger.error("Failed to delete job: %s", e)
        return False
```

## Kubernetes/Helm Configuration

### Dapr Pub/Sub Component (Redis)

```yaml
# dapr-pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskflow-pubsub
  namespace: taskflow
spec:
  type: pubsub.redis
  version: v1
  metadata:
    - name: redisHost
      value: "redis:6379"
    - name: redisPassword
      secretKeyRef:
        name: redis-secret
        key: password
    - name: enableTLS
      value: "true"  # Required for Upstash
```

### Dapr Annotations for Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taskflow-api
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "taskflow-api"
        dapr.io/app-port: "8000"
        dapr.io/enable-api-logging: "true"
```

## Common Pitfalls

### 1. Not Unwrapping CloudEvent

```python
# WRONG - event_type will be None!
event = await request.json()
event_type = event.get("event_type")  # None - it's nested in "data"

# CORRECT
raw_event = await request.json()
event = raw_event.get("data", raw_event)  # Unwrap CloudEvent
event_type = event.get("event_type")  # "task.created"
```

### 2. Wrong Job Callback URL

```python
# WRONG - Dapr calls /job/{name}, not custom endpoints
@router.post("/api/jobs/trigger")  # Dapr won't call this!

# CORRECT
@router.post("/job/{job_name}")  # Dapr WILL call this
```

### 3. Forgetting to Return SUCCESS

```python
# WRONG - Dapr will retry on errors
@router.post("/events/task-events")
async def handle(request: Request):
    try:
        # process...
        return {"status": "SUCCESS"}
    except Exception:
        raise  # Dapr will retry!

# CORRECT - Always return SUCCESS to stop retries
@router.post("/events/task-events")
async def handle(request: Request):
    try:
        # process...
    except Exception as e:
        logger.exception("Error: %s", e)
    return {"status": "SUCCESS"}  # Always, even on error
```

### 4. Using Wrong Dapr HTTP Port

```python
# Local development
DAPR_HTTP_ENDPOINT = "http://localhost:3500"

# In Kubernetes (sidecar)
DAPR_HTTP_ENDPOINT = "http://localhost:3500"  # Same! Sidecar is localhost
```

## Debugging

### Check Dapr Sidecar Logs

```bash
# Kubernetes
kubectl logs deploy/myapp -c daprd -n mynamespace

# Look for:
# - "Scheduler stream connected" = Jobs API working
# - "HTTP API Called" = API calls to Dapr
```

### Verify Subscriptions

```bash
# Call your subscribe endpoint
curl http://localhost:8000/dapr/subscribe

# Should return your subscriptions list
```

### Test Pub/Sub Locally

```bash
# Publish test event
curl -X POST http://localhost:3500/v1.0/publish/taskflow-pubsub/task-events \
  -H "Content-Type: application/json" \
  -d '{"event_type": "test", "data": {}}'
```

## References

- [Dapr Pub/Sub](https://docs.dapr.io/developing-applications/building-blocks/pubsub/)
- [Dapr Jobs API](https://docs.dapr.io/developing-applications/building-blocks/jobs/)
- [CloudEvents Spec](https://cloudevents.io/)
