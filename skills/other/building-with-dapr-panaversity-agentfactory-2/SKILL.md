---
name: building-with-dapr
description: Use when building distributed microservices with Dapr sidecar architecture. Triggers include Dapr components, service invocation, state management, pub/sub, secrets, bindings, configuration, actors, and workflows. NOT for direct infrastructure clients (use building-with-kafka-strimzi instead).
---

# Building Distributed Systems with Dapr

Production-ready distributed microservices using Dapr's portable building blocks on Kubernetes. Includes stateful actors and durable workflow orchestration.

## Persona

You are a Dapr and distributed systems expert with production Kubernetes experience. You understand:
- Dapr sidecar architecture and building block APIs
- Service invocation with automatic service discovery and mTLS
- State management with pluggable stores (Redis, PostgreSQL, etc.)
- Pub/Sub messaging with CloudEvents and topic routing
- Bindings for external system integration
- Secrets management and configuration APIs
- **Virtual Actors** with turn-based concurrency, timers, and reminders
- **Durable Workflows** with fault-tolerant orchestration patterns
- Python SDKs: dapr-client, dapr-ext-fastapi, dapr-ext-workflow

## When to Use

- Abstracting infrastructure from application code
- Building portable microservices across cloud providers
- Service-to-service communication with built-in resilience
- State management without direct database code
- Pub/sub without broker-specific SDKs
- Secrets retrieval from multiple stores
- Deploying Dapr on Kubernetes with Helm
- **Stateful entities** with identity (actors for chat sessions, IoT devices, game entities)
- **Long-running orchestration** (workflows for order processing, approval flows, sagas)

## When NOT to Use

- Need direct Kafka access (use building-with-kafka-strimzi)
- Simple single-service applications without distributed needs

## Core Concepts

### Dapr Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  Application Container                                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  FastAPI Service (Your Code)                                │ │
│  │  - Calls localhost:3500 (Dapr HTTP) or localhost:50001     │ │
│  │  - Uses DaprClient from dapr-client SDK                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│                              ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Dapr Sidecar (daprd)                                       │ │
│  │  - HTTP API: :3500  │  gRPC API: :50001                     │ │
│  │  - Building Blocks: state, pubsub, invoke, secrets...       │ │
│  │  - Components: Redis, Kafka, Kubernetes secrets...          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                    │
└──────────────────────────────┼────────────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│  Dapr Control Plane (dapr-system namespace)                       │
│  - dapr-operator: Manages components and Kubernetes integration   │
│  - dapr-sidecar-injector: Auto-injects sidecars via annotations   │
│  - dapr-sentry: Certificate authority for mTLS                    │
│  - dapr-placement: Actor placement (Chapter 59)                   │
│  - dapr-scheduler: Job/workflow scheduling (Chapter 59)           │
└──────────────────────────────────────────────────────────────────┘
```

### Building Blocks (Ch53 Scope)

| Building Block | API Endpoint | Description |
|----------------|--------------|-------------|
| **Service Invocation** | `/v1.0/invoke/{app-id}/method/{method}` | Call other services with discovery + mTLS |
| **State Management** | `/v1.0/state/{store}` | Key-value store with consistency options |
| **Pub/Sub** | `/v1.0/publish/{pubsub}/{topic}` | Event messaging with CloudEvents |
| **Bindings** | `/v1.0/bindings/{binding}` | Input/output triggers for external systems |
| **Secrets** | `/v1.0/secrets/{store}/{key}` | Retrieve secrets from configured stores |
| **Configuration** | `/v1.0/configuration/{store}` | Dynamic configuration with subscriptions |

### Building Blocks: Actors & Workflows (Chapter 59)

| Building Block | API Endpoint | Description |
|----------------|--------------|-------------|
| **Actors** | `/v1.0/actors/{actorType}/{actorId}/method/{method}` | Virtual actors with turn-based concurrency |
| **Workflows** | `/v1.0/workflows/dapr/{workflowName}/start` | Durable orchestration with fault tolerance |

**See detailed reference files:**
- `references/actors.md` - Actor model, Python SDK, timers/reminders
- `references/workflows.md` - Workflow patterns (chaining, fan-out, saga, monitor)

## Decision Logic

| Situation | Pattern | Why |
|-----------|---------|-----|
| Service-to-service calls | Service Invocation | Built-in discovery, retries, mTLS |
| Persistent key-value data | State Management | Pluggable stores, concurrency control |
| Event-driven messaging | Pub/Sub | CloudEvents, at-least-once delivery |
| Cron triggers or webhooks | Input Bindings | Decouple trigger from processing |
| Send to external systems | Output Bindings | Abstracted destination |
| API keys, credentials | Secrets | Centralized, secure access |
| Feature flags, settings | Configuration | Dynamic updates, subscriptions |
| **Stateful entity with identity** | **Actors** | Turn-based concurrency, timers, reminders |
| **Long-running orchestration** | **Workflows** | Durable, fault-tolerant, retries |
| **Multi-step business process** | **Workflows** | Compensation (saga), external events |
| **Parallel task execution** | **Workflows** | Fan-out/fan-in pattern |
| **Scheduled recurring work** | **Actor Reminders** | Survives restarts, persistent |

## Dapr Deployment on Kubernetes

### Install Dapr Control Plane with Helm

```bash
# Add Dapr Helm repo
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Install Dapr 1.14+ in dapr-system namespace
helm upgrade --install dapr dapr/dapr \
  --version=1.14.0 \
  --namespace dapr-system \
  --create-namespace \
  --wait

# Verify installation
kubectl get pods -n dapr-system
```

Expected pods:
- `dapr-operator-*`
- `dapr-sidecar-injector-*`
- `dapr-sentry-*`
- `dapr-placement-server-*`
- `dapr-scheduler-server-*`

### Install Dapr Dashboard (Optional)

```bash
helm install dapr-dashboard dapr/dapr-dashboard --namespace dapr-system

# Access dashboard
kubectl port-forward service/dapr-dashboard 8080:8080 -n dapr-system
# Visit http://localhost:8080
```

## Component Configuration

### Redis State Store

```yaml
# components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.redis
  version: v1
  metadata:
    - name: redisHost
      value: redis-master.default.svc.cluster.local:6379
    - name: redisPassword
      value: ""  # Use secretKeyRef for production
```

### Redis Pub/Sub

```yaml
# components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
  namespace: default
spec:
  type: pubsub.redis
  version: v1
  metadata:
    - name: redisHost
      value: redis-master.default.svc.cluster.local:6379
```

### Kafka Pub/Sub (Connects to Ch52)

```yaml
# components/kafka-pubsub.yaml
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
      value: task-events-kafka-bootstrap.kafka.svc.cluster.local:9092
    - name: consumerGroup
      value: dapr-consumer
    - name: authType
      value: none
```

### Kubernetes Secrets Store

```yaml
# components/secrets.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: default
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

### Declarative Subscription

```yaml
# subscriptions/task-subscription.yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-subscription
  namespace: default
spec:
  pubsubname: pubsub
  topic: task-events
  routes:
    default: /events/task
```

## Python SDK Patterns

### Installation

```bash
# Core client
pip install dapr-client

# FastAPI extension (for pub/sub subscriptions and actors)
pip install dapr-ext-fastapi
```

### DaprClient Initialization

```python
from dapr.clients import DaprClient

# Default: connects to localhost:50001 (gRPC)
with DaprClient() as client:
    # Use client for all building block operations
    pass

# Environment variables:
# DAPR_HTTP_PORT (default: 3500)
# DAPR_GRPC_PORT (default: 50001)
```

### Service Invocation

```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # GET request to another service
    response = client.invoke_method(
        app_id='notification-service',
        method_name='notifications',
        http_verb='GET'
    )

    # POST with data
    response = client.invoke_method(
        app_id='notification-service',
        method_name='notifications',
        data='{"user_id": "123", "message": "Task completed"}',
        http_verb='POST',
        content_type='application/json'
    )

    print(response.text())
```

### State Management

```python
from dapr.clients import DaprClient
import json

with DaprClient() as client:
    # Save state
    client.save_state(
        store_name='statestore',
        key='task-123',
        value=json.dumps({'title': 'Buy groceries', 'status': 'pending'})
    )

    # Get state
    state = client.get_state(
        store_name='statestore',
        key='task-123'
    )
    task = json.loads(state.data) if state.data else None

    # Delete state
    client.delete_state(
        store_name='statestore',
        key='task-123'
    )

    # Bulk state operations
    client.save_bulk_state(
        store_name='statestore',
        states=[
            {'key': 'task-1', 'value': json.dumps({'title': 'Task 1'})},
            {'key': 'task-2', 'value': json.dumps({'title': 'Task 2'})}
        ]
    )
```

### State with ETag (Optimistic Concurrency)

```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Get with ETag
    state = client.get_state('statestore', 'task-123')
    current_etag = state.etag

    # Update only if ETag matches (first-write-wins)
    client.save_state(
        store_name='statestore',
        key='task-123',
        value='{"status": "completed"}',
        etag=current_etag,
        state_metadata={'concurrency': 'first-write'}
    )
```

### Publish Events

```python
from dapr.clients import DaprClient
import json

with DaprClient() as client:
    # Simple publish
    client.publish_event(
        pubsub_name='pubsub',
        topic_name='task-events',
        data=json.dumps({
            'event_type': 'task.created',
            'task_id': 'task-123',
            'title': 'Buy groceries'
        }),
        data_content_type='application/json'
    )

    # With CloudEvents metadata
    client.publish_event(
        pubsub_name='pubsub',
        topic_name='task-events',
        data=json.dumps({'task_id': 'task-123'}),
        data_content_type='application/json',
        publish_metadata={
            'cloudevent.type': 'task.created',
            'cloudevent.source': 'task-api'
        }
    )
```

### Subscribe to Events (FastAPI Extension)

```python
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp
from pydantic import BaseModel

app = FastAPI()
dapr_app = DaprApp(app)

class TaskEvent(BaseModel):
    task_id: str
    event_type: str

# Declarative subscription via decorator
@dapr_app.subscribe(pubsub='pubsub', topic='task-events')
async def handle_task_event(event_data: dict):
    print(f"Received: {event_data}")
    return {"status": "SUCCESS"}

# With route rules
@dapr_app.subscribe(
    pubsub='pubsub',
    topic='task-events',
    route='/events/task-created'
)
async def handle_task_created(event_data: dict):
    print(f"Task created: {event_data}")
    return {"status": "SUCCESS"}
```

### Retrieve Secrets

```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Get single secret
    secret = client.get_secret(
        store_name='kubernetes-secrets',
        key='api-credentials'
    )
    api_key = secret.secret.get('api-key')

    # Get all secrets from store
    secrets = client.get_bulk_secret(store_name='kubernetes-secrets')
```

### Output Bindings

```python
from dapr.clients import DaprClient
import json

with DaprClient() as client:
    # Invoke output binding (e.g., send email, write to queue)
    client.invoke_binding(
        binding_name='email-binding',
        operation='create',
        data=json.dumps({
            'to': 'user@example.com',
            'subject': 'Task Completed',
            'body': 'Your task has been completed.'
        })
    )
```

### Configuration API

```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Get configuration items
    config = client.get_configuration(
        store_name='configstore',
        keys=['feature-flag-x', 'max-retry-count']
    )

    for item in config.items:
        print(f"{item.key}: {item.value}")
```

## FastAPI Integration Pattern

### Complete Task API with Dapr

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from dapr.clients import DaprClient
from dapr.ext.fastapi import DaprApp
from pydantic import BaseModel
import json
import uuid

class Task(BaseModel):
    id: str | None = None
    title: str
    status: str = "pending"

class TaskCreatedEvent(BaseModel):
    task_id: str
    title: str

# Lifespan for Dapr client
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dapr sidecar should be ready
    yield

app = FastAPI(lifespan=lifespan)
dapr_app = DaprApp(app)

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    task.id = str(uuid.uuid4())

    with DaprClient() as client:
        # Save state
        client.save_state(
            store_name='statestore',
            key=f'task-{task.id}',
            value=task.model_dump_json()
        )

        # Publish event
        client.publish_event(
            pubsub_name='pubsub',
            topic_name='task-events',
            data=json.dumps({
                'event_type': 'task.created',
                'task_id': task.id,
                'title': task.title
            }),
            data_content_type='application/json'
        )

    return task

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    with DaprClient() as client:
        state = client.get_state(
            store_name='statestore',
            key=f'task-{task_id}'
        )

        if not state.data:
            raise HTTPException(status_code=404, detail="Task not found")

        return Task.model_validate_json(state.data)

# Subscribe to events
@dapr_app.subscribe(pubsub='pubsub', topic='task-events')
async def handle_task_event(event_data: dict):
    print(f"Processing event: {event_data}")

    # Call notification service via Dapr
    with DaprClient() as client:
        client.invoke_method(
            app_id='notification-service',
            method_name='notify',
            data=json.dumps(event_data),
            http_verb='POST'
        )

    return {"status": "SUCCESS"}
```

## Kubernetes Deployment with Dapr

### Deployment with Sidecar Injection

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-api
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: task-api
  template:
    metadata:
      labels:
        app: task-api
      annotations:
        # Enable Dapr sidecar injection
        dapr.io/enabled: "true"
        # Unique app identifier for service discovery
        dapr.io/app-id: "task-api"
        # Port your app listens on
        dapr.io/app-port: "8000"
        # Enable API logging for debugging
        dapr.io/enable-api-logging: "true"
        # Optional: configure sidecar resources
        dapr.io/sidecar-cpu-limit: "500m"
        dapr.io/sidecar-memory-limit: "256Mi"
    spec:
      containers:
        - name: task-api
          image: task-api:latest
          ports:
            - containerPort: 8000
          env:
            - name: DAPR_HTTP_PORT
              value: "3500"
```

### Service

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: task-api
  namespace: default
spec:
  selector:
    app: task-api
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
```

## HTTP API Patterns (No SDK)

For simple use cases, call Dapr directly via HTTP:

### State via HTTP

```python
import httpx
import os

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
STATE_URL = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/statestore"

async def save_state(key: str, value: dict):
    async with httpx.AsyncClient() as client:
        await client.post(
            STATE_URL,
            json=[{"key": key, "value": value}]
        )

async def get_state(key: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STATE_URL}/{key}")
        return response.json() if response.status_code == 200 else None
```

### Publish via HTTP

```python
PUBSUB_URL = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/pubsub/task-events"

async def publish_event(event: dict):
    async with httpx.AsyncClient() as client:
        await client.post(PUBSUB_URL, json=event)
```

## Safety & Guardrails

### NEVER

- Call Dapr before sidecar is ready (use health checks)
- Hardcode component names (use configuration)
- Skip error handling for Dapr API calls
- Store sensitive data in state without encryption
- Expose Dapr HTTP/gRPC ports externally
- Use `dapr.io/app-port` for gRPC apps without specifying protocol

### ALWAYS

- Wait for sidecar readiness: `/v1.0/healthz`
- Use secrets component for credentials (not environment variables)
- Enable mTLS in production (default with Sentry)
- Configure appropriate retry policies
- Set resource limits on sidecar
- Use CloudEvents for pub/sub interoperability

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ERR_STATE_STORE_NOT_FOUND` | State component not configured | Apply component YAML |
| `ERR_PUBSUB_NOT_FOUND` | Pub/sub component not configured | Apply component YAML |
| `connection refused :3500` | Sidecar not ready | Add startup probe, wait for health |
| `ERR_DIRECT_INVOKE` | Target app not found | Check app-id annotation |
| `DEADLINE_EXCEEDED` | Request timeout | Increase timeout or check target |
| `sidecar not found` | Injection not enabled | Check annotations and namespace |

## Dapr vs Direct Infrastructure

| Aspect | Direct (e.g., Redis SDK) | Dapr |
|--------|--------------------------|------|
| **Portability** | Locked to specific store | Swap via YAML config |
| **Code changes** | New SDK per backend | Same API always |
| **Discovery** | Manual configuration | Automatic via app-id |
| **Security** | Self-managed TLS | Auto mTLS via Sentry |
| **Observability** | Custom instrumentation | Built-in tracing |
| **Resilience** | Manual retry logic | Configured policies |

## References

**Official Documentation:**
- [Dapr Documentation](https://docs.dapr.io/)
- [Dapr Python SDK](https://github.com/dapr/python-sdk)
- [Dapr Building Blocks](https://docs.dapr.io/concepts/building-blocks-concept/)
- [Dapr Components](https://docs.dapr.io/reference/components-reference/)
- [Dapr on Kubernetes](https://docs.dapr.io/operations/hosting/kubernetes/)

**Actors & Workflows:**
- [Dapr Actors Overview](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-overview/)
- [Dapr Workflow Overview](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/)
- [Workflow Patterns](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-patterns/)
- [Python SDK Workflow Examples](https://github.com/dapr/python-sdk/tree/master/examples/demo_workflow)

**Skill Reference Files:**
- `references/actors.md` - Actor model, Python SDK patterns, timers/reminders
- `references/workflows.md` - Workflow patterns, determinism rules, management CLI
