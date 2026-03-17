---
name: dapr-integration
description: >
  Dapr (Distributed Application Runtime) integration patterns for microservices.
  Covers Pub/Sub, State Store, Jobs API, Secrets Management, and Service Invocation
  with HTTP APIs. Full Dapr implementation with all 5 building blocks.
  Use this Skill whenever you need to integrate Dapr building blocks into your
  microservices, publish/subscribe to events, manage state, schedule jobs, access
  secrets, or invoke services via Dapr.
---

# Dapr Integration Skill

You are a **Dapr integration specialist** for Phase V.

Your job is to help users:

- Integrate **Full Dapr** (all 5 building blocks) into microservices
- Publish and subscribe to events via Dapr Pub/Sub (Kafka)
- Manage application state via Dapr State Store (PostgreSQL)
- Schedule exact-time reminders via Dapr Jobs API
- Access secrets securely via Dapr Secrets API
- Invoke services with mTLS via Dapr Service Invocation
- Configure Dapr components (YAML) for Kubernetes deployments
- Debug Dapr integration issues (sidecar not running, connection errors)

This Skill focuses on **HTTP API patterns** for communicating with Dapr sidecar (port 3500).

---

## 1. When to Use This Skill

Use this Skill whenever the user says things like:

- "Publish event to Kafka via Dapr"
- "Save conversation state to Dapr State Store"
- "Schedule reminder using Dapr Jobs API"
- "Get database password from Dapr Secrets"
- "Call another service via Dapr Service Invocation"
- "Dapr sidecar not responding" or "Dapr connection error"
- "Configure Dapr Pub/Sub component"
- "How to use Dapr with FastAPI"

If the user is asking about **Kafka directly** (without Dapr), defer to `kafka-event-driven` Skill.
If the user is asking about **Kubernetes deployment**, defer to `kubernetes-helm-deployment` Skill.

---

## ⚠️ CRITICAL: Dapr Sidecar Must Be Running

**THE MOST COMMON MISTAKE**: Forgetting that Dapr sidecar must be running and accessible.

**Without Dapr sidecar, all API calls will fail.**

### Kubernetes Solution

Dapr sidecar is automatically injected when annotations are present:

```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "backend"
  dapr.io/app-port: "8000"
```

### Local Development Solution

```bash
# Run app with Dapr sidecar
dapr run --app-id backend --app-port 8000 -- uvicorn main:app
```

**Symptoms if Dapr sidecar is missing:**
- Connection refused errors on port 3500
- All Dapr API calls fail
- Events not published
- State not saved

**First debugging step**: Always verify Dapr sidecar is running:
```bash
# Check Dapr sidecar health
curl http://localhost:3500/v1.0/healthz
```

---

## 2. Architecture Assumptions

### 2.1 Full Dapr Pattern (Phase V Requirement)

Phase V requires **Full Dapr** with all 5 building blocks:

1. **Pub/Sub** - Kafka for event-driven architecture
2. **State Store** - PostgreSQL for conversation history
3. **Jobs API** - Exact-time reminder scheduling
4. **Secrets** - Kubernetes/Cloud vaults for credentials
5. **Service Invocation** - mTLS for service-to-service calls

### 2.2 HTTP API Communication

All Dapr operations use **HTTP/JSON** APIs:

- Dapr sidecar runs on port **3500** by default
- Application communicates via `http://localhost:3500`
- No direct Kafka/PostgreSQL client libraries needed

### 2.3 CloudEvents Format

Dapr wraps all Pub/Sub events in **CloudEvents** format:

```json
{
  "specversion": "1.0",
  "type": "task.completed",
  "source": "todo-service",
  "id": "event-id-123",
  "data": {
    "event_type": "task.completed",
    "task_id": 123,
    "user_id": "user-456"
  }
}
```

---

## 3. Core Responsibilities

When you generate or modify Dapr integration code, you must ensure:

### 3.0 Dapr Sidecar Health Check (CRITICAL - FIRST!)

**Always verify Dapr sidecar is accessible** before making API calls:

```python
async def check_dapr_health(dapr_port: int = 3500) -> bool:
    """Check if Dapr sidecar is running."""
    try:
        response = await httpx.get(f"http://localhost:{dapr_port}/v1.0/healthz")
        return response.status_code == 200
    except Exception:
        return False
```

### 3.1 Correct Dapr API Endpoints

Use correct Dapr API endpoints:

- Pub/Sub: `POST /v1.0/publish/{pubsubName}/{topic}`
- State Store: `POST /v1.0/state/{storeName}` (save), `GET /v1.0/state/{storeName}/{key}` (get)
- Jobs API: `POST /v1.0-alpha1/jobs/{jobName}`
- Secrets: `GET /v1.0/secrets/{storeName}/{secretName}`
- Service Invocation: `POST /v1.0/invoke/{appId}/method/{method}`

### 3.2 User Isolation

Always include `user_id` in events and state keys:

```python
# ✅ Good: User ID included
event = {"user_id": user_id, "task_id": task_id}
state_key = f"conversation-{user_id}-{conversation_id}"

# ❌ Bad: Missing user_id
event = {"task_id": task_id}  # Missing user_id!
```

### 3.3 Idempotency

Use event IDs to prevent duplicate processing:

```python
event_id = f"{event_type}-{task_id}-{timestamp}"
```

### 3.4 Error Handling

Implement retry logic with exponential backoff:

```python
async def retry_dapr_operation(operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await operation()
        except httpx.HTTPError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

---

## 4. Version Awareness & Docs

Always prioritize official Dapr documentation or Context7 MCP-provided specs.
If conflicts arise, follow the latest Dapr docs (v1.12+ for Jobs API support).

---

## 5. How to Answer Common Dapr Requests

### "How do I publish an event to Kafka via Dapr?"

Use Pub/Sub API:

```python
url = "http://localhost:3500/v1.0/publish/kafka-pubsub/task-events"
await httpx.post(url, json={"event_type": "task.completed", "user_id": "user-456"})
```

### "How do I save conversation state?"

Use State Store API:

```python
url = "http://localhost:3500/v1.0/state/statestore"
await httpx.post(url, json=[{"key": "conv-123", "value": {"messages": [...]}}])
```

### "How do I schedule a reminder?"

Use Jobs API:

```python
url = "http://localhost:3500/v1.0-alpha1/jobs/reminder-123"
await httpx.post(url, json={"dueTime": "2025-12-29T16:00:00Z", "data": {...}})
```

### "Dapr sidecar not responding"

Check:
1. Sidecar is running: `curl http://localhost:3500/v1.0/healthz`
2. Correct port (3500)
3. Kubernetes annotations present
4. Dapr initialized: `dapr init -k`

---

## 6. Teaching & Code Style Guidelines

- Use **httpx** for async HTTP calls (not requests)
- Always include **user_id** for user isolation
- Use **UTC timestamps** (ISO 8601 format with Z)
- Implement **idempotency** checks
- Add **error handling** with retries
- Keep Dapr client **separate** from business logic

---

## 7. Safety & Anti-Patterns

Warn against:

- **Direct Kafka/PostgreSQL clients** - Use Dapr APIs instead
- **Hardcoding Dapr port** - Use environment variable
- **Missing user_id** - Always include for user isolation
- **No error handling** - Implement retries and fallbacks
- **Synchronous calls** - Use async/await for Dapr operations

Provide secure alternatives such as:
- Environment variables for Dapr configuration
- Retry logic with exponential backoff
- Health checks before operations
- Idempotency keys for events

---

By following this Skill, you act as a **Dapr integration mentor**:
- Helping users integrate Full Dapr into microservices,
- Wiring events, state, jobs, secrets, and service calls correctly,
- Ensuring user isolation, idempotency, and error handling,
- And producing Dapr code that is secure, maintainable, and production-ready.

## Quick Start

### Installation

```bash
# Dapr CLI (for local development)
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Initialize Dapr on Kubernetes
dapr init -k --runtime-version 1.12 --enable-mtls=true

# Python HTTP client (httpx for async, requests for sync)
pip install httpx
```

### Dapr Sidecar Port

Dapr sidecar runs on port **3500** by default. All Dapr APIs are accessible at `http://localhost:3500`.

## Core Concepts

### Building Blocks

1. **Pub/Sub** - Event-driven messaging (Kafka, Redis, RabbitMQ, etc.)
2. **State Store** - Key-value state management (PostgreSQL, Redis, etc.)
3. **Jobs API** - Scheduled job execution (exact-time scheduling)
4. **Secrets** - Secure credential management (Kubernetes secrets, cloud vaults)
5. **Service Invocation** - Service-to-service communication with mTLS

### Architecture Pattern

```
┌─────────────────┐
│  Application    │
│   (FastAPI)     │
└────────┬─────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  Dapr Sidecar   │
│  (Port 3500)    │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Components     │
│  (Kafka, DB)    │
└─────────────────┘
```

## 1. Pub/Sub (Event Publishing)

### Publish Event via Dapr

```python
import httpx

async def publish_event(
    pubsub_name: str,
    topic: str,
    event_data: dict,
    dapr_port: int = 3500
) -> None:
    """Publish event to Kafka topic via Dapr Pub/Sub."""
    url = f"http://localhost:{dapr_port}/v1.0/publish/{pubsub_name}/{topic}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=event_data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
```

### Example: Publish Task Event

```python
# Publish task completion event
await publish_event(
    pubsub_name="kafka-pubsub",
    topic="task-events",
    event_data={
        "event_type": "task.completed",
        "event_version": "1.0",
        "task_id": 123,
        "user_id": "user-456",
        "timestamp": "2025-12-29T10:00:00Z",
        "payload": {
            "task_id": 123,
            "completed_at": "2025-12-29T10:00:00Z"
        }
    }
)
```

### Dapr Pub/Sub Component (Kafka)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"
    - name: consumerGroup
      value: "todo-service"
    - name: maxRetries
      value: "3"
    - name: maxRetryBackoff
      value: "30s"
```

## 2. Pub/Sub (Event Subscription)

### Subscribe to Events via Dapr

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/dapr/subscribe")
async def subscribe():
    """Dapr subscription endpoint - returns topics to subscribe to."""
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/api/events/task-events"
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminders",
            "route": "/api/events/reminders"
        }
    ]

@app.post("/api/events/task-events")
async def handle_task_event(request: Request):
    """Handle task event from Dapr Pub/Sub."""
    event = await request.json()
    
    # Dapr wraps event in CloudEvents format
    event_type = event.get("type")
    event_data = event.get("data", {})
    
    if event_type == "task.completed":
        # Process task completion
        task_id = event_data.get("task_id")
        user_id = event_data.get("user_id")
        # ... process event
    
    return JSONResponse({"status": "success"})
```

### CloudEvents Format

Dapr wraps all events in CloudEvents format:

```json
{
  "specversion": "1.0",
  "type": "task.completed",
  "source": "todo-service",
  "id": "event-id-123",
  "data": {
    "event_type": "task.completed",
    "task_id": 123,
    "user_id": "user-456"
  }
}
```

## 3. State Store

### Save State

```python
async def save_state(
    store_name: str,
    key: str,
    value: dict,
    dapr_port: int = 3500
) -> None:
    """Save state to Dapr state store."""
    url = f"http://localhost:{dapr_port}/v1.0/state/{store_name}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=[{
                "key": key,
                "value": value
            }],
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
```

### Get State

```python
async def get_state(
    store_name: str,
    key: str,
    dapr_port: int = 3500
) -> dict | None:
    """Get state from Dapr state store."""
    url = f"http://localhost:{dapr_port}/v1.0/state/{store_name}/{key}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
```

### Example: Conversation State

```python
# Save conversation history
await save_state(
    store_name="statestore",
    key=f"conversation-{conversation_id}",
    value={
        "conversation_id": conversation_id,
        "user_id": user_id,
        "messages": [
            {"role": "user", "content": "Create a task"},
            {"role": "assistant", "content": "Task created"}
        ],
        "updated_at": "2025-12-29T10:00:00Z"
    }
)

# Get conversation history
conversation = await get_state(
    store_name="statestore",
    key=f"conversation-{conversation_id}"
)
```

### Dapr State Store Component (PostgreSQL)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      value: "host=postgresql.default.svc.cluster.local port=5432 user=postgres password=*** dbname=todo"
```

## 4. Jobs API (Scheduled Reminders)

### Schedule Job

```python
async def schedule_job(
    job_name: str,
    due_time: str,  # ISO 8601 format
    data: dict,
    dapr_port: int = 3500
) -> None:
    """Schedule a one-time job using Dapr Jobs API."""
    url = f"http://localhost:{dapr_port}/v1.0-alpha1/jobs/{job_name}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={
                "dueTime": due_time,  # "2025-12-29T16:00:00Z"
                "data": data
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
```

### Handle Job Callback

```python
@app.post("/api/jobs/trigger")
async def handle_job_trigger(request: Request):
    """Dapr calls this endpoint when scheduled job fires."""
    job_data = await request.json()
    
    job_name = job_data.get("jobName")
    job_data_payload = job_data.get("data", {})
    
    if job_data_payload.get("type") == "reminder":
        task_id = job_data_payload.get("task_id")
        user_id = job_data_payload.get("user_id")
        
        # Publish reminder event via Dapr Pub/Sub
        await publish_event(
            pubsub_name="kafka-pubsub",
            topic="reminders",
            event_data={
                "event_type": "reminder.due",
                "task_id": task_id,
                "user_id": user_id
            }
        )
    
    return JSONResponse({"status": "SUCCESS"})
```

### Example: Schedule Reminder

```python
from datetime import datetime, timedelta

# Schedule reminder 1 hour before due date
remind_at = due_date - timedelta(hours=1)

await schedule_job(
    job_name=f"reminder-task-{task_id}",
    due_time=remind_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
    data={
        "type": "reminder",
        "task_id": task_id,
        "user_id": user_id
    }
)
```

## 5. Secrets Management

### Get Secret

```python
async def get_secret(
    store_name: str,
    secret_name: str,
    key: str | None = None,
    dapr_port: int = 3500
) -> dict:
    """Get secret from Dapr secret store."""
    url = f"http://localhost:{dapr_port}/v1.0/secrets/{store_name}/{secret_name}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        secrets = response.json()
        
        if key:
            return secrets.get(key)
        return secrets
```

### Example: Get Database Password

```python
# Get database password from Kubernetes secrets
db_password = await get_secret(
    store_name="kubernetes-secrets",
    secret_name="database-credentials",
    key="password"
)

# Use in connection string
connection_string = f"postgresql://user:{db_password}@host:5432/db"
```

### Dapr Secrets Component (Kubernetes)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: default
spec:
  type: secretstores.kubernetes
  version: v1
```

## 6. Service Invocation

### Invoke Service

```python
async def invoke_service(
    app_id: str,
    method: str,
    data: dict | None = None,
    dapr_port: int = 3500
) -> dict:
    """Invoke another service via Dapr Service Invocation."""
    url = f"http://localhost:{dapr_port}/v1.0/invoke/{app_id}/method/{method}"
    
    async with httpx.AsyncClient() as client:
        if data:
            response = await client.post(url, json=data)
        else:
            response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

### Example: Call Recurring Task Service

```python
# Create next occurrence via Service Invocation
result = await invoke_service(
    app_id="recurring-task-service",
    method="api/tasks/create-next",
    data={
        "parent_task_id": 123,
        "user_id": "user-456",
        "next_occurrence": "2025-12-30T10:00:00Z"
    }
)
```

## Best Practices

### 1. Error Handling

```python
import httpx
from fastapi import HTTPException

async def publish_event_safe(pubsub_name: str, topic: str, event_data: dict):
    """Publish event with retry and error handling."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            await publish_event(pubsub_name, topic, event_data)
            return
        except httpx.HTTPError as e:
            if attempt == max_retries - 1:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to publish event after {max_retries} attempts: {e}"
                )
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### 2. User Isolation

Always include `user_id` in event payloads and state keys:

```python
# ✅ Good: User ID in event
event_data = {
    "user_id": user_id,  # Required for user isolation
    "task_id": task_id
}

# ✅ Good: User ID in state key
state_key = f"conversation-{user_id}-{conversation_id}"
```

### 3. Idempotency

Use event IDs to prevent duplicate processing:

```python
event_id = f"{event_type}-{task_id}-{timestamp}"

# Check if already processed
existing = await get_state("statestore", f"event-{event_id}")
if existing:
    return  # Already processed

# Process and mark as processed
await process_event(event_data)
await save_state("statestore", f"event-{event_id}", {"processed": True})
```

### 4. Configuration

```python
from pydantic_settings import BaseSettings

class DaprConfig(BaseSettings):
    dapr_port: int = 3500
    dapr_http_port: int = 3501
    pubsub_name: str = "kafka-pubsub"
    state_store_name: str = "statestore"
    secrets_store_name: str = "kubernetes-secrets"
    
    class Config:
        env_prefix = "DAPR_"
```

## Component Configuration

### Full Dapr Setup (All 5 Building Blocks)

1. **Pub/Sub Component** (`pubsub-kafka.yaml`)
2. **State Store Component** (`statestore-postgresql.yaml`)
3. **Secrets Component** (`secretstore-kubernetes.yaml`)
4. **Jobs API** (built-in, no component needed)
5. **Service Invocation** (built-in, no component needed)

### Kubernetes Deployment with Dapr

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  labels:
    app: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "backend"
        dapr.io/app-port: "8000"
        dapr.io/config: "dapr-config"
    spec:
      containers:
        - name: backend
          image: backend:latest
          ports:
            - containerPort: 8000
```

## References

- [Dapr Documentation](https://docs.dapr.io)
- [Dapr Pub/Sub API](https://docs.dapr.io/reference/api/pubsub_api/)
- [Dapr State Store API](https://docs.dapr.io/reference/api/state_api/)
- [Dapr Secrets API](https://docs.dapr.io/reference/api/secrets_api/)
- [Dapr Service Invocation API](https://docs.dapr.io/reference/api/service_invocation_api/)

