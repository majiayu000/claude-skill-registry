---
name: kafka-event-driven
description: Event-driven architecture patterns with Apache Kafka. Covers event schemas, producer/consumer patterns, partitioning strategies, dead letter queues, and retry mechanisms. Works with Dapr Pub/Sub abstraction.
---

# Kafka Event-Driven Architecture Skill

Event-driven architecture patterns using Apache Kafka for building scalable, decoupled microservices.

## Quick Start

### Installation

```bash
# kafka-python (if using direct Kafka client - NOT recommended with Dapr)
pip install kafka-python

# For Dapr integration, use httpx instead
pip install httpx
```

### Architecture Pattern

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Producer   │────▶│   Kafka     │────▶│  Consumer   │
│  Service    │     │   Topics    │     │  Service    │
└─────────────┘     └─────────────┘     └─────────────┘
```

**With Dapr**:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Producer   │────▶│   Dapr     │────▶│  Consumer   │
│  Service    │     │  Pub/Sub   │     │  Service    │
└─────────────┘     └─────────────┘     └─────────────┘
                    (Kafka backend)
```

## 1. Event Schema Design

### Versioned Event Schema

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class TaskEvent(BaseModel):
    """Versioned task event schema."""
    event_id: str = Field(..., description="Unique event identifier")
    event_type: Literal["task.created", "task.updated", "task.completed", "task.deleted"]
    event_version: str = Field(default="1.0", description="Schema version")
    task_id: int
    user_id: str = Field(..., description="Required for user isolation")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: dict = Field(..., description="Event-specific data")

class ReminderEvent(BaseModel):
    """Reminder event schema."""
    event_id: str
    event_type: Literal["reminder.scheduled", "reminder.due", "reminder.cancelled"]
    event_version: str = "1.0"
    task_id: int
    user_id: str
    timestamp: datetime
    payload: dict
```

### Event Schema Registry

```python
EVENT_SCHEMAS = {
    "task.created": TaskEvent,
    "task.updated": TaskEvent,
    "task.completed": TaskEvent,
    "task.deleted": TaskEvent,
    "reminder.scheduled": ReminderEvent,
    "reminder.due": ReminderEvent,
}

def validate_event(event_data: dict) -> BaseModel:
    """Validate event against schema registry."""
    event_type = event_data.get("event_type")
    schema_class = EVENT_SCHEMAS.get(event_type)
    
    if not schema_class:
        raise ValueError(f"Unknown event type: {event_type}")
    
    return schema_class(**event_data)
```

## 2. Event Publishing (via Dapr)

### Publisher Service

```python
import httpx
import uuid
from datetime import datetime
from typing import Literal

class EventPublisher:
    """Publish events to Kafka via Dapr Pub/Sub."""
    
    def __init__(
        self,
        pubsub_name: str = "kafka-pubsub",
        dapr_port: int = 3500
    ):
        self.pubsub_name = pubsub_name
        self.dapr_url = f"http://localhost:{dapr_port}"
    
    async def publish_task_event(
        self,
        event_type: Literal["task.created", "task.updated", "task.completed", "task.deleted"],
        task_id: int,
        user_id: str,
        payload: dict
    ) -> None:
        """Publish task event to task-events topic."""
        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "event_version": "1.0",
            "task_id": task_id,
            "user_id": user_id,  # Required for partitioning
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": payload
        }
        
        url = f"{self.dapr_url}/v1.0/publish/{self.pubsub_name}/task-events"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=event)
            response.raise_for_status()
    
    async def publish_reminder_event(
        self,
        event_type: Literal["reminder.scheduled", "reminder.due"],
        task_id: int,
        user_id: str,
        payload: dict
    ) -> None:
        """Publish reminder event to reminders topic."""
        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "event_version": "1.0",
            "task_id": task_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": payload
        }
        
        url = f"{self.dapr_url}/v1.0/publish/{self.pubsub_name}/reminders"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=event)
            response.raise_for_status()
```

### Example: Publish Task Completion

```python
publisher = EventPublisher()

# When task is marked complete
await publisher.publish_task_event(
    event_type="task.completed",
    task_id=123,
    user_id="user-456",
    payload={
        "task_id": 123,
        "completed_at": "2025-12-29T10:00:00Z",
        "recurring_pattern": "DAILY"
    }
)
```

## 3. Event Consumption (via Dapr)

### Consumer Service

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

@app.post("/dapr/subscribe")
async def subscribe():
    """Dapr subscription endpoint."""
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/api/events/task-events",
            "metadata": {
                "rawPayload": "false"  # Dapr wraps in CloudEvents
            }
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminders",
            "route": "/api/events/reminders"
        }
    ]

@app.post("/api/events/task-events")
async def handle_task_event(request: Request):
    """Handle task event from Kafka."""
    cloud_event = await request.json()
    
    # Extract event data from CloudEvents format
    event_data = cloud_event.get("data", {})
    event_type = event_data.get("event_type")
    user_id = event_data.get("user_id")
    task_id = event_data.get("task_id")
    
    # User isolation check
    if not user_id:
        return JSONResponse(
            {"status": "error", "message": "Missing user_id"},
            status_code=400
        )
    
    # Process event based on type
    if event_type == "task.completed":
        await handle_task_completed(event_data)
    elif event_type == "task.created":
        await handle_task_created(event_data)
    
    return JSONResponse({"status": "success"})

async def handle_task_completed(event_data: dict):
    """Process task completion event."""
    task_id = event_data.get("task_id")
    user_id = event_data.get("user_id")
    payload = event_data.get("payload", {})
    
    # Check if recurring task
    if payload.get("recurring_pattern"):
        # Trigger next occurrence creation
        await create_next_occurrence(task_id, user_id, payload)
```

## 4. Partitioning Strategy

### User ID Partitioning

Kafka topics should be partitioned by `user_id` to ensure:
- Events for same user are processed in order
- Parallel processing across users
- User isolation

```python
# Dapr automatically partitions by key if provided
# Use user_id as partition key

event = {
    "user_id": user_id,  # Used for partitioning
    "task_id": task_id,
    # ... other fields
}

# Dapr Pub/Sub component configuration
# metadata:
#   - name: partitionKey
#     value: "user_id"  # Partition by user_id field
```

### Topic Configuration

```yaml
# Kafka topics with user_id partitioning
topics:
  - name: task-events
    partitions: 12
    replication_factor: 1
    config:
      retention.ms: 604800000  # 7 days (local)
      # retention.ms: 2592000000  # 30 days (cloud)
```

## 5. Dead Letter Queue (DLQ)

### Retry Strategy

```python
from enum import Enum
from typing import Dict, List

class EventType(str, Enum):
    TASK_COMPLETION = "task.completed"
    REMINDER = "reminder.due"
    TASK_UPDATE = "task.updated"

RETRY_STRATEGIES: Dict[EventType, List[int]] = {
    EventType.TASK_COMPLETION: [30, 300, 1800],  # 30s, 5min, 30min
    EventType.REMINDER: [1, 2, 4, 8, 16, 32, 64, 128, 256, 512],  # 1s to 512s
    EventType.TASK_UPDATE: [1, 2, 4, 8, 16],  # 1s to 16s
}

MAX_RETRIES: Dict[EventType, int] = {
    EventType.TASK_COMPLETION: 3,
    EventType.REMINDER: 10,
    EventType.TASK_UPDATE: 5,
}
```

### DLQ Handler

```python
import asyncio
from datetime import datetime

class DLQHandler:
    """Handle failed events and move to DLQ."""
    
    async def handle_failed_event(
        self,
        event: dict,
        error: Exception,
        retry_count: int
    ) -> None:
        """Move failed event to DLQ after max retries."""
        event_type = event.get("event_type")
        max_retries = MAX_RETRIES.get(EventType(event_type), 3)
        
        if retry_count >= max_retries:
            # Move to DLQ
            await self.publish_to_dlq(event, error, retry_count)
            
            # Alert operations team
            await self.alert_ops_team(event, error)
            
            # Alert user if reminder failed
            if event_type.startswith("reminder"):
                await self.alert_user(event, error)
        else:
            # Retry with exponential backoff
            delay = RETRY_STRATEGIES[EventType(event_type)][retry_count]
            await asyncio.sleep(delay)
            await self.retry_event(event, retry_count + 1)
    
    async def publish_to_dlq(self, event: dict, error: Exception, retry_count: int):
        """Publish failed event to DLQ topic."""
        dlq_event = {
            **event,
            "dlq_metadata": {
                "failed_at": datetime.utcnow().isoformat() + "Z",
                "error": str(error),
                "retry_count": retry_count
            }
        }
        
        # Publish to DLQ topic
        publisher = EventPublisher()
        await publisher.publish_task_event(
            event_type="dlq.failed",
            task_id=event.get("task_id", 0),
            user_id=event.get("user_id", "unknown"),
            payload=dlq_event
        )
```

## 6. Idempotency

### Idempotent Consumer

```python
import httpx
from dapr_integration import get_state, save_state

async def process_event_idempotent(event: dict) -> bool:
    """Process event with idempotency check."""
    event_id = event.get("event_id")
    
    # Check if already processed
    processed = await get_state(
        store_name="statestore",
        key=f"event-{event_id}"
    )
    
    if processed:
        return False  # Already processed
    
    # Process event
    try:
        await handle_event(event)
        
        # Mark as processed
        await save_state(
            store_name="statestore",
            key=f"event-{event_id}",
            value={
                "processed": True,
                "processed_at": datetime.utcnow().isoformat() + "Z"
            }
        )
        return True
    except Exception as e:
        # Don't mark as processed on error
        raise
```

## 7. Event Schema Evolution

### Version Compatibility

```python
def migrate_event(event: dict, target_version: str) -> dict:
    """Migrate event to target schema version."""
    current_version = event.get("event_version", "1.0")
    
    if current_version == target_version:
        return event
    
    # Migration logic
    if current_version == "1.0" and target_version == "1.1":
        # Add new fields, transform data
        event["payload"]["new_field"] = None
    
    return event
```

## Best Practices

### 1. Always Include user_id

```python
# ✅ Good
event = {
    "user_id": user_id,  # Required
    "task_id": task_id
}

# ❌ Bad
event = {
    "task_id": task_id  # Missing user_id
}
```

### 2. Use Event IDs for Idempotency

```python
event_id = f"{event_type}-{task_id}-{timestamp}"
```

### 3. Version Your Events

```python
event = {
    "event_version": "1.0",  # Schema version
    # ... other fields
}
```

### 4. Handle CloudEvents Format

Dapr wraps events in CloudEvents format:

```python
# Extract from CloudEvents
cloud_event = await request.json()
event_data = cloud_event.get("data", {})
```

## References

- [Kafka Python Client](https://kafka-python.readthedocs.io/)
- [Dapr Pub/Sub](https://docs.dapr.io/reference/api/pubsub_api/)
- [CloudEvents Specification](https://cloudevents.io/)

