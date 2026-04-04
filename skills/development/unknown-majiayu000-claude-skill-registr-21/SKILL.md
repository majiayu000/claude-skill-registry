---
name: dapr-integration
description: Integrate Dapr building blocks for event-driven microservices - Pub/Sub, State Management, Secrets, Service Invocation, and Jobs API. Use when implementing event-driven architecture for Phase 5. (project)
allowed-tools: Bash, Write, Read, Glob, Edit, Grep
---

# Dapr Integration Skill

## Quick Start

1. **Read Phase 5 Constitution** - `constitution-prompt-phase-5.md`
2. **Check Dapr installation** - `dapr --version`
3. **Initialize Dapr** - `dapr init` or `dapr init -k` for Kubernetes
4. **Create component files** - In `dapr-components/` directory
5. **Configure sidecar** - Annotations for Kubernetes deployments
6. **Test locally** - `dapr run` commands

## Dapr Building Blocks Overview

| Building Block | Purpose | Phase 5 Usage |
|----------------|---------|---------------|
| **Pub/Sub** | Event messaging | Task events, reminders, audit logs |
| **State** | Key-value storage | Cache, session state |
| **Secrets** | Secret management | API keys, DB credentials |
| **Service Invocation** | Service-to-service calls | Microservice communication |
| **Jobs API** | Scheduled tasks | Recurring task scheduling |

## Component Configuration

### Pub/Sub Component (Kafka)

Create `dapr-components/pubsub.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskpubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"
    - name: consumerGroup
      value: "todo-consumer-group"
    - name: authType
      value: "none"
    - name: disableTls
      value: "true"
scopes:
  - backend
  - notification-service
  - recurring-service
  - audit-service
```

### State Store Component

Create `dapr-components/statestore.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: todo-app
spec:
  type: state.redis
  version: v1
  metadata:
    - name: redisHost
      value: "redis:6379"
    - name: redisPassword
      value: ""
    - name: actorStateStore
      value: "true"
scopes:
  - backend
```

### Secrets Component

Create `dapr-components/secrets.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: todo-app
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

## Python SDK Integration

### Installation

```bash
uv add dapr dapr-ext-fastapi
```

### Pub/Sub Publisher

```python
from dapr.clients import DaprClient

async def publish_task_event(event_type: str, task_data: dict):
    """Publish task event to Kafka via Dapr."""
    with DaprClient() as client:
        client.publish_event(
            pubsub_name="taskpubsub",
            topic_name="task-events",
            data=json.dumps({
                "event_type": event_type,
                "task": task_data,
                "timestamp": datetime.utcnow().isoformat()
            }),
            data_content_type="application/json"
        )
```

### Pub/Sub Subscriber (FastAPI)

```python
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI

app = FastAPI()
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub="taskpubsub", topic="task-events")
async def handle_task_event(event: dict):
    """Handle incoming task events."""
    event_type = event.get("event_type")
    task_data = event.get("task")

    if event_type == "task.created":
        await process_new_task(task_data)
    elif event_type == "task.completed":
        await process_completed_task(task_data)
```

### State Management

```python
from dapr.clients import DaprClient

async def save_state(key: str, value: dict):
    """Save state to Dapr state store."""
    with DaprClient() as client:
        client.save_state(
            store_name="statestore",
            key=key,
            value=json.dumps(value)
        )

async def get_state(key: str) -> dict | None:
    """Get state from Dapr state store."""
    with DaprClient() as client:
        state = client.get_state(store_name="statestore", key=key)
        return json.loads(state.data) if state.data else None
```

### Service Invocation

```python
from dapr.clients import DaprClient

async def invoke_notification_service(user_id: str, message: str):
    """Invoke notification service via Dapr."""
    with DaprClient() as client:
        response = client.invoke_method(
            app_id="notification-service",
            method_name="send",
            data=json.dumps({
                "user_id": user_id,
                "message": message
            }),
            http_verb="POST"
        )
        return response.json()
```

### Jobs API (Scheduled Tasks)

```python
from dapr.clients import DaprClient

async def schedule_reminder(reminder_id: str, due_at: datetime):
    """Schedule a reminder using Dapr Jobs API."""
    with DaprClient() as client:
        # Create a scheduled job
        client.start_workflow(
            workflow_component="dapr",
            workflow_name="reminder-workflow",
            input={
                "reminder_id": reminder_id,
                "scheduled_time": due_at.isoformat()
            }
        )
```

## Kubernetes Deployment Annotations

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "backend"
        dapr.io/app-port: "8000"
        dapr.io/enable-api-logging: "true"
        dapr.io/log-level: "info"
        dapr.io/config: "dapr-config"
    spec:
      containers:
        - name: backend
          image: evolution-todo/backend:latest
```

## Local Development with Dapr

### Run with Dapr Sidecar

```bash
# Run backend with Dapr
dapr run --app-id backend \
         --app-port 8000 \
         --dapr-http-port 3500 \
         --components-path ./dapr-components \
         -- uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

# Run notification service with Dapr
dapr run --app-id notification-service \
         --app-port 8002 \
         --dapr-http-port 3502 \
         --components-path ./dapr-components \
         -- uv run uvicorn services.notification.main:app --host 0.0.0.0 --port 8002
```

### Test Pub/Sub

```bash
# Publish test event
dapr publish --publish-app-id backend \
             --pubsub taskpubsub \
             --topic task-events \
             --data '{"event_type":"task.created","task":{"id":"123","title":"Test"}}'
```

## Verification Checklist

- [ ] Dapr CLI installed (`dapr --version`)
- [ ] Dapr initialized (`dapr init` or `dapr init -k`)
- [ ] Component files created in `dapr-components/`
- [ ] Python SDK installed (`dapr`, `dapr-ext-fastapi`)
- [ ] Pub/Sub working (publish → subscribe)
- [ ] State store working (save → get)
- [ ] Service invocation working
- [ ] Kubernetes annotations configured
- [ ] All services have Dapr sidecars

## Event Topics

| Topic | Publisher | Subscribers | Purpose |
|-------|-----------|-------------|---------|
| `task-events` | Backend | Notification, Audit, WebSocket | Task CRUD events |
| `reminder-events` | Recurring Service | Notification, Backend | Reminder triggers |
| `audit-events` | All Services | Audit Service | Audit logging |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Sidecar not starting | Missing annotations | Add `dapr.io/enabled: "true"` |
| Pub/Sub not working | Component not loaded | Check component scope |
| Connection refused | Wrong port | Verify `app-port` matches app |
| State not persisting | Redis not running | Start Redis container |

## References

- [Dapr Documentation](https://docs.dapr.io/)
- [Dapr Python SDK](https://github.com/dapr/python-sdk)
- [Dapr Pub/Sub](https://docs.dapr.io/developing-applications/building-blocks/pubsub/)
- [Dapr State Management](https://docs.dapr.io/developing-applications/building-blocks/state-management/)
- [Phase 5 Constitution](../../../constitution-prompt-phase-5.md)
