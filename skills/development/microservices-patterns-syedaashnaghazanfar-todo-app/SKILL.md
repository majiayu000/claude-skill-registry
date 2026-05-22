---
name: microservices-patterns
description: Microservices architecture patterns for event-driven systems. Covers service-to-service communication, idempotency, user isolation, event-driven design, and service discovery.
---

# Microservices Patterns Skill

Microservices architecture patterns for building scalable, resilient, event-driven systems.

## Core Principles

1. **Service Independence** - Each service can be developed, deployed, and scaled independently
2. **Event-Driven Communication** - Services communicate via events (Kafka) rather than direct calls
3. **User Isolation** - All operations are scoped to user_id
4. **Idempotency** - Operations can be safely retried
5. **Service Discovery** - Services discover each other via Dapr Service Invocation

## 1. Service-to-Service Communication

### Dapr Service Invocation

```python
import httpx

async def invoke_service(
    app_id: str,
    method: str,
    data: dict | None = None,
    dapr_port: int = 3500
) -> dict:
    """Invoke another microservice via Dapr."""
    url = f"http://localhost:{dapr_port}/v1.0/invoke/{app_id}/method/{method}"
    
    async with httpx.AsyncClient() as client:
        if data:
            response = await client.post(url, json=data)
        else:
            response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

### Example: Recurring Task Service Calls Backend

```python
# Recurring Task Service creates next occurrence
async def create_next_occurrence(parent_task_id: int, user_id: str):
    """Create next occurrence via backend service."""
    result = await invoke_service(
        app_id="backend",
        method="api/tasks",
        data={
            "title": "Daily standup",
            "user_id": user_id,  # Required for user isolation
            "recurring_pattern": "DAILY",
            "parent_task_id": parent_task_id
        }
    )
    return result
```

## 2. User Isolation

### Always Filter by user_id

```python
from sqlmodel import Session, select

def get_user_tasks(session: Session, user_id: str):
    """Get tasks for specific user only."""
    # ✅ Good: Filter by user_id
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()

# ❌ Bad: No user filter
def get_all_tasks(session: Session):
    statement = select(Task)  # Missing user_id filter!
    return session.exec(statement).all()
```

### User ID in Events

```python
# Always include user_id in events
event = {
    "user_id": user_id,  # Required
    "task_id": task_id,
    "event_type": "task.completed"
}

# Consumer validates user_id
async def handle_event(event: dict):
    user_id = event.get("user_id")
    if not user_id:
        raise ValueError("Missing user_id in event")
    
    # Process with user isolation
    await process_for_user(user_id, event)
```

## 3. Idempotency Patterns

### Idempotent Event Processing

```python
from dapr_integration import get_state, save_state
import uuid

async def process_event_idempotent(event: dict) -> bool:
    """Process event exactly once using idempotency key."""
    event_id = event.get("event_id")
    
    if not event_id:
        # Generate idempotency key
        event_id = f"{event.get('event_type')}-{event.get('task_id')}-{uuid.uuid4()}"
        event["event_id"] = event_id
    
    # Check if already processed
    processed = await get_state(
        store_name="statestore",
        key=f"event-processed-{event_id}"
    )
    
    if processed:
        return False  # Already processed, skip
    
    # Process event
    try:
        await handle_event(event)
        
        # Mark as processed
        await save_state(
            store_name="statestore",
            key=f"event-processed-{event_id}",
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

### Idempotent Task Creation

```python
async def create_task_idempotent(
    session: Session,
    task_data: dict,
    idempotency_key: str
) -> Task:
    """Create task with idempotency check."""
    # Check if task already exists with this key
    existing = session.exec(
        select(Task).where(Task.idempotency_key == idempotency_key)
    ).first()
    
    if existing:
        return existing  # Return existing task
    
    # Create new task
    task = Task(
        **task_data,
        idempotency_key=idempotency_key
    )
    session.add(task)
    session.commit()
    return task
```

## 4. Event-Driven Service Design

### Recurring Task Service

```python
from fastapi import FastAPI, Request
from kafka_event_driven import EventPublisher, validate_event

app = FastAPI()

class RecurringTaskService:
    """Microservice for handling recurring task logic."""
    
    def __init__(self):
        self.publisher = EventPublisher()
    
    async def handle_task_completed(self, event: dict):
        """Handle task.completed event and create next occurrence."""
        task_id = event.get("task_id")
        user_id = event.get("user_id")
        payload = event.get("payload", {})
        
        # Check if recurring task
        recurring_pattern = payload.get("recurring_pattern")
        if not recurring_pattern:
            return  # Not a recurring task
        
        # Calculate next occurrence
        next_occurrence = calculate_next_occurrence(
            recurring_pattern,
            payload.get("completed_at")
        )
        
        # Create next occurrence via backend service
        await invoke_service(
            app_id="backend",
            method="api/tasks",
            data={
                "title": payload.get("title"),
                "user_id": user_id,
                "recurring_pattern": recurring_pattern,
                "next_occurrence": next_occurrence.isoformat(),
                "parent_task_id": task_id
            }
        )
        
        # Publish event for next occurrence
        await self.publisher.publish_task_event(
            event_type="task.created",
            task_id=task_id + 1,  # New task ID
            user_id=user_id,
            payload={"parent_task_id": task_id}
        )

@app.post("/api/events/task-events")
async def handle_task_event(request: Request):
    """Handle task events from Kafka."""
    cloud_event = await request.json()
    event_data = cloud_event.get("data", {})
    
    service = RecurringTaskService()
    
    if event_data.get("event_type") == "task.completed":
        await service.handle_task_completed(event_data)
    
    return {"status": "success"}
```

### Notification Service

```python
class NotificationService:
    """Microservice for sending notifications."""
    
    async def handle_reminder_due(self, event: dict):
        """Handle reminder.due event and send notification."""
        task_id = event.get("task_id")
        user_id = event.get("user_id")
        payload = event.get("payload", {})
        
        # Get user email from user service
        user = await invoke_service(
            app_id="backend",
            method=f"api/users/{user_id}"
        )
        
        # Send email notification
        await send_email(
            to=user["email"],
            subject=f"Reminder: {payload.get('title')}",
            body=f"Task '{payload.get('title')}' is due at {payload.get('due_at')}"
        )
        
        # Update reminder_sent flag
        await invoke_service(
            app_id="backend",
            method=f"api/tasks/{task_id}/reminder-sent",
            data={"reminder_sent": True}
        )
```

## 5. Service Health Checks

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    """Service health check endpoint."""
    return {
        "status": "healthy",
        "service": "recurring-task-service",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/health/ready")
async def readiness_check():
    """Readiness probe - check dependencies."""
    # Check database connection
    try:
        # ... database check
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}, 503

@app.get("/health/live")
async def liveness_check():
    """Liveness probe - service is running."""
    return {"status": "alive"}
```

## 6. Error Handling and Retries

### Retry with Exponential Backoff

```python
import asyncio
from typing import Callable, Any

async def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
) -> Any:
    """Retry function with exponential backoff."""
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Last attempt, raise exception
            
            await asyncio.sleep(delay)
            delay *= backoff_factor
    
    raise Exception("Max retries exceeded")

# Usage
result = await retry_with_backoff(
    lambda: invoke_service("backend", "api/tasks"),
    max_retries=3,
    initial_delay=1.0
)
```

## 7. Service Configuration

### Environment-Based Configuration

```python
from pydantic_settings import BaseSettings

class ServiceConfig(BaseSettings):
    service_name: str = "recurring-task-service"
    dapr_port: int = 3500
    database_url: str
    kafka_brokers: str = "kafka:9092"
    
    # Service discovery
    backend_service_id: str = "backend"
    notification_service_id: str = "notification-service"
    
    class Config:
        env_prefix = "SERVICE_"
```

## Best Practices

### 1. Stateless Services

Services should be stateless - store state in database or Dapr State Store:

```python
# ✅ Good: Stateless service
class RecurringTaskService:
    async def process_event(self, event: dict):
        # No instance state, all data from event/DB
        pass

# ❌ Bad: Stateful service
class RecurringTaskService:
    def __init__(self):
        self.processed_events = []  # Don't store state in service
```

### 2. User Context Propagation

Always propagate user_id through service calls:

```python
# ✅ Good: User ID in all calls
await invoke_service(
    app_id="backend",
    method="api/tasks",
    data={"user_id": user_id, ...}  # User ID included
)
```

### 3. Circuit Breaker Pattern

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
async def call_backend_service(method: str, data: dict):
    """Call backend service with circuit breaker."""
    return await invoke_service("backend", method, data)
```

## References

- [Dapr Service Invocation](https://docs.dapr.io/reference/api/service_invocation_api/)
- [Microservices Patterns](https://microservices.io/patterns/)

