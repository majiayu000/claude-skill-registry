---
name: dapr-code-generator
description: Generate Python boilerplate code for DAPR microservices, workflows, and actors. Creates properly structured services with DAPR SDK integration, health endpoints, logging, and best practices. Use when creating new services, adding DAPR features, or scaffolding projects.
allowed-tools: Read, Write, Glob
---

# DAPR Code Generator

This skill generates production-ready Python code for DAPR applications following best practices.

## When to Use

Claude automatically uses this skill when:
- User creates a new DAPR service
- Adding DAPR features to existing code
- Scaffolding microservice projects
- Creating workflows or actors

## Code Templates

### FastAPI Microservice

```python
"""
{service_name} - DAPR-enabled FastAPI microservice
"""
import json
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dapr.clients import DaprClient
from dapr.ext.fastapi import DaprApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DAPR_STORE_NAME = "statestore"
DAPR_PUBSUB_NAME = "pubsub"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting {service_name}")
    yield
    logger.info("Shutting down {service_name}")


app = FastAPI(
    title="{service_name}",
    lifespan=lifespan
)
dapr_app = DaprApp(app)


# Health endpoints
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    """Readiness check endpoint."""
    return {"status": "ready"}


# DAPR State Management
async def save_state(key: str, value: Any) -> None:
    """Save state to DAPR state store."""
    async with DaprClient() as client:
        await client.save_state(
            store_name=DAPR_STORE_NAME,
            key=key,
            value=json.dumps(value)
        )
        logger.info(f"State saved: {key}")


async def get_state(key: str) -> Any:
    """Get state from DAPR state store."""
    async with DaprClient() as client:
        state = await client.get_state(
            store_name=DAPR_STORE_NAME,
            key=key
        )
        if state.data:
            return json.loads(state.data)
        return None


# DAPR Pub/Sub
async def publish_event(topic: str, data: Any) -> None:
    """Publish event to DAPR pub/sub."""
    async with DaprClient() as client:
        await client.publish_event(
            pubsub_name=DAPR_PUBSUB_NAME,
            topic_name=topic,
            data=json.dumps(data),
            data_content_type="application/json"
        )
        logger.info(f"Event published to {topic}")


# DAPR Service Invocation
async def invoke_service(app_id: str, method: str, data: Any = None) -> Any:
    """Invoke another DAPR service."""
    async with DaprClient() as client:
        response = await client.invoke_method(
            app_id=app_id,
            method_name=method,
            data=json.dumps(data) if data else None,
            content_type="application/json"
        )
        return response.json() if response.data else None


# Example API endpoints - customize as needed
class ItemModel(BaseModel):
    id: str
    name: str
    data: dict = {}


@app.post("/items")
async def create_item(item: ItemModel):
    """Create a new item."""
    await save_state(f"item-{item.id}", item.model_dump())
    await publish_event("items", {"action": "created", "item": item.model_dump()})
    return {"status": "created", "id": item.id}


@app.get("/items/{item_id}")
async def get_item(item_id: str):
    """Get an item by ID."""
    item = await get_state(f"item-{item_id}")
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# DAPR Pub/Sub subscription
@dapr_app.subscribe(pubsub=DAPR_PUBSUB_NAME, topic="items")
async def handle_item_event(event: dict):
    """Handle item events from pub/sub."""
    logger.info(f"Received event: {event}")
    return {"status": "SUCCESS"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Workflow Service

```python
"""
{workflow_name} - DAPR Workflow Service
"""
import logging
from datetime import timedelta
from dapr.ext.workflow import (
    WorkflowRuntime,
    DaprWorkflowClient,
    DaprWorkflowContext,
    WorkflowActivityContext,
    RetryPolicy
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize workflow runtime
wf_runtime = WorkflowRuntime()

# Retry policy for activities
default_retry = RetryPolicy(
    max_number_of_attempts=3,
    first_retry_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    max_retry_interval=timedelta(seconds=30)
)


# Workflow definition
@wf_runtime.workflow(name="{workflow_name}")
def {workflow_name}_workflow(ctx: DaprWorkflowContext, input_data: dict):
    """
    Main workflow definition.

    Args:
        ctx: Workflow context
        input_data: Input data for the workflow

    Returns:
        Workflow result
    """
    logger.info(f"Starting workflow with input: {input_data}")

    # Step 1: First activity
    step1_result = yield ctx.call_activity(
        activity=step1_activity,
        input=input_data
    )
    logger.info(f"Step 1 completed: {step1_result}")

    # Step 2: Second activity
    step2_result = yield ctx.call_activity(
        activity=step2_activity,
        input=step1_result
    )
    logger.info(f"Step 2 completed: {step2_result}")

    # Step 3: Final activity
    final_result = yield ctx.call_activity(
        activity=step3_activity,
        input=step2_result
    )

    return {"status": "completed", "result": final_result}


# Activity definitions
@wf_runtime.activity(name="step1_activity")
def step1_activity(ctx: WorkflowActivityContext, data: dict) -> dict:
    """First step of the workflow."""
    logger.info(f"Executing step 1 with: {data}")
    # Your logic here
    return {"step": 1, "data": data}


@wf_runtime.activity(name="step2_activity")
def step2_activity(ctx: WorkflowActivityContext, data: dict) -> dict:
    """Second step of the workflow."""
    logger.info(f"Executing step 2 with: {data}")
    # Your logic here
    return {"step": 2, "data": data}


@wf_runtime.activity(name="step3_activity")
def step3_activity(ctx: WorkflowActivityContext, data: dict) -> dict:
    """Third step of the workflow."""
    logger.info(f"Executing step 3 with: {data}")
    # Your logic here
    return {"step": 3, "data": data}


# Start workflow runtime
if __name__ == "__main__":
    logger.info("Starting workflow runtime...")
    wf_runtime.start()

    # Keep the runtime running
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down workflow runtime...")
        wf_runtime.shutdown()
```

### Actor Service

```python
"""
{actor_name} - DAPR Virtual Actor
"""
import logging
from abc import abstractmethod
from dapr.actor import Actor, ActorInterface, ActorProxy, Remindable, actormethod
from dapr.actor.runtime.config import ActorRuntimeConfig, ActorTypeConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Actor interface
class {actor_name}Interface(ActorInterface):
    """Interface for {actor_name} actor."""

    @abstractmethod
    async def get_state(self) -> dict:
        """Get the current state of the actor."""
        ...

    @abstractmethod
    async def set_state(self, data: dict) -> None:
        """Set the state of the actor."""
        ...

    @abstractmethod
    async def process(self, input_data: dict) -> dict:
        """Process input data and return result."""
        ...


# Actor implementation
class {actor_name}(Actor, {actor_name}Interface, Remindable):
    """
    {actor_name} virtual actor implementation.

    This actor maintains state and can process requests.
    """

    def __init__(self, ctx, actor_id):
        super().__init__(ctx, actor_id)
        self._state = {}

    async def _on_activate(self) -> None:
        """Called when actor is activated."""
        logger.info(f"Actor {self.id} activated")
        # Load state if exists
        has_state, state = await self._state_manager.try_get_state("actor_state")
        if has_state:
            self._state = state

    async def _on_deactivate(self) -> None:
        """Called when actor is deactivated."""
        logger.info(f"Actor {self.id} deactivated")

    @actormethod(name="GetState")
    async def get_state(self) -> dict:
        """Get the current state of the actor."""
        return self._state

    @actormethod(name="SetState")
    async def set_state(self, data: dict) -> None:
        """Set the state of the actor."""
        self._state = data
        await self._state_manager.set_state("actor_state", self._state)
        await self._state_manager.save_state()

    @actormethod(name="Process")
    async def process(self, input_data: dict) -> dict:
        """Process input data and return result."""
        logger.info(f"Processing: {input_data}")
        # Your processing logic here
        result = {"processed": True, "input": input_data}
        return result

    async def receive_reminder(self, name: str, state: bytes, due_time, period) -> None:
        """Handle reminder callback."""
        logger.info(f"Reminder received: {name}")
        # Handle the reminder


# Actor runtime configuration
actor_runtime_config = ActorRuntimeConfig()
actor_runtime_config.register_actor({actor_name})


# FastAPI integration
from fastapi import FastAPI
from dapr.ext.fastapi import DaprActor

app = FastAPI(title="{actor_name} Service")
actor = DaprActor(app)


@app.on_event("startup")
async def startup():
    await actor.register_actor({actor_name})


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Generated File Structure

When generating a new service, create:

```
{service_name}/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application
│   ├── models.py            # Pydantic models
│   ├── services.py          # Business logic
│   └── config.py            # Configuration
├── components/
│   ├── statestore.yaml      # State store component
│   ├── pubsub.yaml          # Pub/sub component
│   └── secrets.yaml         # Secrets component
├── tests/
│   ├── __init__.py
│   └── test_main.py         # Unit tests
├── dapr.yaml                # DAPR configuration
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container image
└── README.md                # Documentation
```

## Requirements Template

```txt
# DAPR SDK
dapr>=1.12.0
dapr-ext-fastapi>=1.12.0
dapr-ext-workflow>=0.4.0

# Web framework
fastapi>=0.104.0
uvicorn>=0.24.0

# Utilities
pydantic>=2.0.0
python-dotenv>=1.0.0

# Observability
opentelemetry-api>=1.20.0
opentelemetry-sdk>=1.20.0
opentelemetry-instrumentation-fastapi>=0.41b0
```

## Dockerfile Template

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/

# Run application
EXPOSE 8000
CMD ["python", "src/main.py"]
```
