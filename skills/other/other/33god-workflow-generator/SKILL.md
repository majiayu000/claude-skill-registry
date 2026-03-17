---
name: 33god-workflow-generator
description: Generate complete workflow implementations from semantic descriptions for the 33GOD ecosystem. Use when (1) implementing new event-driven workflows, (2) creating services that span filesystem → API → Bloodbank → processing, (3) adding orchestration flows that combine Node-RED + Python services, (4) registering new services in the 33GOD registry, or (5) when the user provides a workflow description like "watch directory, process files, publish events."
---

# 33GOD Workflow Generator

Generates complete workflow implementations from semantic descriptions, following **33GOD event-driven architecture patterns**.

## Overview

This skill transforms high-level workflow descriptions into production-ready implementations including Node-RED flows, Python services, Bloodbank event definitions, and registry entries. It encodes the architectural patterns and best practices of the 33GOD event-driven ecosystem.

**The Event-Driven Architecture Flow:**

```
Holyfields (Definition) → Bloodbank (Transport) → Candystore (Persistence) → Holocene (Visibility) → Agents (Action)
```

Every workflow you generate must fit into this flow:
1. **Define events** in Holyfields (schema-first)
2. **Transport** via Bloodbank (RabbitMQ)
3. **Persist** to Candystore (automatic, wildcard binding)
4. **Visualize** in Holocene (automatic, API + WS)
5. **Act** via Agents (consumers, heartbeat-aware)

## Workflow Generation Process

### Step 1: Analyze Workflow Complexity

Given a semantic workflow description, determine the appropriate architecture:

**Decision Matrix:**

| Workflow Characteristics | Architecture | Components |
|--------------------------|-------------|------------|
| 1-2 steps, single protocol | Watchdog + Python | Python service only |
| 3-4 steps, minimal branching | FastAPI | Python service only |
| 5+ steps, multiple protocols | Hybrid | Node-RED + Python service |
| Heavy computation | Python service | FastStream consumer |

**Complexity Threshold:**
- **Simple (Python only):** File watch → publish event
- **Medium (Python only):** Webhook → validate → transform → publish
- **Complex (Hybrid):** File watch → extract audio → upload S3 → call API → webhook → process → publish

**Use Node-RED when:**
- 5+ steps with 3+ protocols (filesystem, HTTP, S3, RabbitMQ)
- Conditional branching based on file type or API responses
- Need visual debugging during development
- Runtime modification is valuable

### Step 2: Identify Components

For each workflow, identify:

1. **Trigger** - What starts the workflow?
   - Filesystem watch: Node-RED watch node
   - Webhook: Node-RED http in node or FastAPI endpoint
   - Scheduled: Node-RED cron or Python async task
   - Event: FastStream subscriber

2. **Processing Steps** - What happens?
   - Media processing: Python script via exec node
   - API calls: Node-RED http request or Python httpx
   - Data transformation: Python service with Pydantic models
   - File operations: Node-RED file nodes or Python pathlib

3. **Event Publishing** - What events are produced?
   - Node-RED: Build envelope → write file → `bb publish`
   - Python: `Publisher.publish()` with EventEnvelope

4. **Consumers** - What processes the events?
   - Python FastStream service with Pydantic models
   - Node-RED exec subscriber (for visualization only)

### Step 3: Generate Node-RED Flow (if needed)

See `references/node-red-patterns.md` for detailed patterns.

**Flow Structure:**

```json
[
  {
    "id": "tab_<workflow_name>",
    "type": "tab",
    "label": "<Descriptive Label>",
    "info": "<What this workflow does>"
  }
]
```

**Essential Patterns:**
1. File watching with media filtering
2. Delay nodes for file writes
3. Exec nodes for Python scripts
4. Function nodes for envelope building
5. File write → exec publish pattern
6. Debug nodes on all error paths

### Step 4: Generate Python Service (if needed)

**Service Types:**

**A. FastStream Consumer (processes events)**

```python
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue, ExchangeType
from event_producers.config import settings
from event_producers.events.base import EventEnvelope, create_envelope, Source, TriggerType
from event_producers.rabbit import Publisher

# Models
class PayloadModel(BaseModel):
    field: str

# Broker
broker = RabbitBroker(settings.rabbit_url)
app = FastStream(broker)
publisher = Publisher()

@app.after_startup
async def startup():
    await publisher.start()

@app.after_shutdown
async def shutdown():
    await publisher.stop()

@broker.subscriber(
    queue=RabbitQueue(
        name="services.domain.queue_name",
        routing_key="domain.resource.action",
        durable=True
    ),
    exchange=RabbitExchange(
        name=settings.exchange_name,
        type=ExchangeType.TOPIC,
        durable=True
    )
)
async def handle_event(message_dict: Dict[str, Any]):
    envelope = EventEnvelope(**message_dict)
    payload = PayloadModel.model_validate(envelope.payload)
    result = await process(payload)
    await publisher.publish(
        routing_key="domain.resource.result",
        body=create_envelope(
            event_type="domain.resource.result",
            payload=result,
            source=Source(
                host="service-name",
                type=TriggerType.AGENT,
                app="service-name"
            )
        ).model_dump(mode="json")
    )
```

**Service Directory Structure:**

```
service-name/
├── src/
│   ├── __init__.py
│   ├── consumer.py
│   ├── models.py
│   └── config.py
├── tests/
├── Dockerfile
├── pyproject.toml
└── README.md
```

### Step 5: Update Registry

See `references/registry-schema.md` for complete schema.

**Add service definition:**

```yaml
services:
  service-name:
    name: "service-name"
    description: "What this service does and why"
    type: "event-consumer | event-producer | orchestrator"
    queue_name: "services.domain.queue_name"
    routing_keys:
      - "domain.resource.action"
    produces:
      - "domain.resource.result"
    status: "active"
    owner: "33GOD"
    tags:
      - "domain"
```

**Add event subscriptions:**

```yaml
event_subscriptions:
  domain.resource.action:
    - "service-name"
```

**Add to topology:**

```yaml
topology:
  processors:
    - "service-name"
```

### Step 6: Generate Documentation

Create implementation documentation with architecture, workflow steps, event flow, testing instructions, and configuration.

## Reference Files

Load these as needed for detailed patterns:

- **[architecture-patterns.md](references/architecture-patterns.md)** - Service separation, Node-RED vs Python decisions
- **[bloodbank-events.md](references/bloodbank-events.md)** - Event envelope structure, publishing, consuming
- **[node-red-patterns.md](references/node-red-patterns.md)** - Node types, flow structure, complete examples
- **[registry-schema.md](references/registry-schema.md)** - Service definition schema, event subscriptions

## Common Workflow Patterns

### Pattern 1: File Watch → Process → Publish
Node-RED: Watch → Filter → Process → Publish
Python: Event consumer for downstream processing

### Pattern 2: Webhook → API → Event → Process
Node-RED: Webhook receiver → API calls → Event publish
Python: Event consumer for data processing

### Pattern 3: Scheduled → Query → Transform → Publish
Python: Async scheduled task → Query → Transform → Publish

## Anti-Patterns to Avoid

❌ **Domain logic in Node-RED function nodes**
✅ **Domain logic in Python services with Pydantic models**

❌ **Node-RED consuming events for processing**
✅ **Node-RED consuming events for visualization only**

❌ **Hardcoded paths and secrets**
✅ **Environment variables for all configuration**

## Workflow Checklist

- [ ] Architecture decision documented (event-driven vs request/response)
- [ ] Holyfields schema defined (if new events)
- [ ] Node-RED flow JSON generated (if needed)
- [ ] Python service created (if needed)
- [ ] Registry.yaml updated
- [ ] Environment variables documented
- [ ] Testing instructions provided
- [ ] Event flow diagram created
- [ ] Error handling implemented
- [ ] Heartbeat consumption considered (for long-running services)
