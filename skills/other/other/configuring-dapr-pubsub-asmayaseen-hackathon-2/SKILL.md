---
name: configuring-dapr-pubsub
description: |
  Configures Dapr pub/sub components for event-driven microservices with Kafka or Redis.
  Use when wiring agent-to-agent communication, setting up event subscriptions, or integrating Dapr sidecars.
  Covers component configuration, subscription patterns, publishing events, and Kubernetes deployment.
  NOT when using direct Kafka clients or non-Dapr messaging patterns.
---

# Configuring Dapr Pub/Sub

Wire event-driven microservices using Dapr pub/sub with Kafka or Redis backends.

## Quick Start

```yaml
# components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
    - name: authType
      value: "none"
    - name: disableTls
      value: "true"
```

```bash
# Apply component
kubectl apply -f components/pubsub.yaml

# Test with Dapr CLI
dapr run --app-id publisher -- dapr publish --pubsub pubsub --topic test --data '{"msg":"hello"}'
```

## Component Configurations

### Kafka (Production)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    # Required
    - name: brokers
      value: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
    - name: authType
      value: "none"

    # Consumer settings
    - name: consumerGroup
      value: "{namespace}-{appId}"  # Templated per deployment
    - name: consumeRetryInterval
      value: "100ms"
    - name: heartbeatInterval
      value: "3s"
    - name: sessionTimeout
      value: "10s"

    # Performance
    - name: maxMessageBytes
      value: "1048576"  # 1MB
    - name: channelBufferSize
      value: "256"
```

### Kafka with SASL Authentication

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub-secure
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka.example.com:9093"
    - name: authType
      value: "password"
    - name: saslUsername
      value: "dapr-user"
    - name: saslPassword
      secretKeyRef:
        name: kafka-secrets
        key: password
    - name: saslMechanism
      value: "SCRAM-SHA-256"
```

### Redis (Development/Simple)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: redis-pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
    - name: redisHost
      value: "redis-master.redis.svc.cluster.local:6379"
    - name: redisPassword
      secretKeyRef:
        name: redis-secrets
        key: password
```

## Subscription Patterns

### Declarative Subscription (Recommended)

```yaml
# subscriptions/task-events.yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-created-subscription
spec:
  pubsubname: pubsub
  topic: task-created
  routes:
    default: /dapr/task-created
  scopes:
    - triage-agent
    - concepts-agent
```

### Programmatic Subscription (FastAPI)

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/dapr/subscribe")
async def subscribe():
    """Dapr calls this to discover subscriptions."""
    return [
        {
            "pubsubname": "pubsub",
            "topic": "task-created",
            "route": "/dapr/task-created"
        },
        {
            "pubsubname": "pubsub",
            "topic": "task-completed",
            "route": "/dapr/task-completed"
        }
    ]

@app.post("/dapr/task-created")
async def handle_task_created(request: Request):
    """Handle incoming CloudEvent."""
    event = await request.json()

    # CloudEvent wrapper - data is nested
    task_data = event.get("data", event)
    task_id = task_data.get("task_id")

    # Process event
    print(f"Task created: {task_id}")

    return {"status": "SUCCESS"}
```

## Publishing Events

### From FastAPI Service

```python
import httpx

DAPR_URL = "http://localhost:3500"

async def publish_event(topic: str, data: dict):
    """Publish event through Dapr sidecar."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DAPR_URL}/v1.0/publish/pubsub/{topic}",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

# Usage
await publish_event("task-created", {
    "task_id": "123",
    "title": "Learn Python",
    "user_id": "user-456"
})
```

### With CloudEvent Metadata

```python
async def publish_cloudevent(topic: str, data: dict, event_type: str):
    """Publish with explicit CloudEvent fields."""
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{DAPR_URL}/v1.0/publish/pubsub/{topic}",
            json=data,
            headers={
                "Content-Type": "application/cloudevents+json",
                "ce-specversion": "1.0",
                "ce-type": event_type,
                "ce-source": "triage-agent",
                "ce-id": str(uuid.uuid4())
            }
        )
```

## Kubernetes Deployment

### Component Scoping

Limit component access to specific apps:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"
scopes:
  - triage-agent
  - concepts-agent
  - debug-agent
```

### App Deployment with Dapr Sidecar

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: triage-agent
spec:
  replicas: 2
  selector:
    matchLabels:
      app: triage-agent
  template:
    metadata:
      labels:
        app: triage-agent
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "triage-agent"
        dapr.io/app-port: "8000"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
        - name: triage-agent
          image: myapp/triage-agent:latest
          ports:
            - containerPort: 8000
          env:
            - name: DAPR_HTTP_PORT
              value: "3500"
```

## Multi-Agent Routing Pattern

### Triage Agent → Specialist Agents

```python
# triage_agent.py
from fastapi import FastAPI, Request
import httpx

app = FastAPI()
DAPR_URL = "http://localhost:3500"

@app.post("/api/question")
async def handle_question(request: Request):
    data = await request.json()
    question = data["question"]

    # Route based on content
    if "python" in question.lower() or "code" in question.lower():
        topic = "concepts-request"
    elif "error" in question.lower() or "bug" in question.lower():
        topic = "debug-request"
    else:
        topic = "concepts-request"  # Default

    # Publish to appropriate agent
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{DAPR_URL}/v1.0/publish/pubsub/{topic}",
            json={
                "question": question,
                "user_id": data["user_id"],
                "session_id": data["session_id"]
            }
        )

    return {"status": "routed", "topic": topic}
```

### Specialist Agent Handler

```python
# concepts_agent.py
from fastapi import FastAPI, Request
import httpx

app = FastAPI()
DAPR_URL = "http://localhost:3500"

@app.get("/dapr/subscribe")
async def subscribe():
    return [{"pubsubname": "pubsub", "topic": "concepts-request", "route": "/dapr/handle"}]

@app.post("/dapr/handle")
async def handle_concepts_request(request: Request):
    event = await request.json()
    data = event.get("data", event)

    # Process with LLM
    response = await process_with_llm(data["question"])

    # Publish response
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{DAPR_URL}/v1.0/publish/pubsub/response-ready",
            json={
                "session_id": data["session_id"],
                "response": response,
                "agent": "concepts"
            }
        )

    return {"status": "SUCCESS"}
```

## Local Development

### Run with Dapr CLI

```bash
# Start subscriber first
dapr run --app-id concepts-agent --app-port 8001 --dapr-http-port 3501 \
  --resources-path ./components -- uvicorn concepts:app --port 8001

# Start publisher
dapr run --app-id triage-agent --app-port 8000 --dapr-http-port 3500 \
  --resources-path ./components -- uvicorn triage:app --port 8000
```

### Docker Compose with Dapr

```yaml
version: "3.8"
services:
  triage-agent:
    build: ./services/triage
    ports:
      - "8000:8000"

  triage-agent-dapr:
    image: daprio/daprd:latest
    command: ["./daprd",
      "--app-id", "triage-agent",
      "--app-port", "8000",
      "--dapr-http-port", "3500",
      "--resources-path", "/components"
    ]
    volumes:
      - ./components:/components
    network_mode: "service:triage-agent"
    depends_on:
      - triage-agent

  kafka:
    image: confluentinc/cp-kafka:latest
    # ... kafka config
```

## Troubleshooting

### Check Dapr Sidecar

```bash
# View sidecar logs
kubectl logs deploy/triage-agent -c daprd

# Check component registration
curl http://localhost:3500/v1.0/metadata
```

### Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `component not found` | Component not loaded | Check `--resources-path` or K8s namespace |
| `connection refused` | Kafka not reachable | Verify broker address in component |
| `consumer group rebalance` | Multiple instances | Use unique `consumerGroup` per app |
| `event not received` | Wrong topic/route | Check subscription config |

### Debug Event Flow

```bash
# Publish test event
dapr publish --pubsub pubsub --topic test --data '{"test": true}'

# Check consumer logs
kubectl logs deploy/my-app -c daprd | grep -i subscribe
```

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `deploying-kafka-k8s` - Kafka cluster setup with Strimzi
- `scaffolding-fastapi-dapr` - FastAPI services with Dapr
- `scaffolding-openai-agents` - Agent orchestration patterns