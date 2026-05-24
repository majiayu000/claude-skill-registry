---
name: a2a-protocol
description: Comprehensive guide and utilities for building AI agents using the Agent2Agent (A2A) Protocol. Use when implementing agent-to-agent communication, creating A2A servers/clients, or working with JSON-RPC based agent systems.
argument-hint: "[agent-type: server|client]"
---

# A2A Protocol Implementation Guide

This skill provides comprehensive knowledge for building, deploying, and interacting with agents using the **Agent2Agent (A2A) Protocol v0.3.0**.

> **Reference**: https://a2a-protocol.org/latest/definitions/

---

## Protocol Overview

A2A is a standard protocol enabling AI agents to communicate and collaborate. It operates across three layers:

| Layer | Description |
|-------|-------------|
| **Data Model** | Core structures (Task, Message, AgentCard, Part, Artifact) |
| **Abstract Operations** | Protocol-agnostic capabilities (SendMessage, GetTask, etc.) |
| **Protocol Bindings** | Concrete implementations (JSON-RPC 2.0, gRPC, HTTP/REST) |

---

## Core Data Structures

### 1. AgentCard

Self-describing manifest hosted at `/.well-known/agent-card.json`:

```json
{
  "name": "my_agent",
  "description": "Agent description",
  "url": "http://localhost:8080/",
  "version": "1.0.0",
  "protocolVersion": "0.3.0",
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "extendedAgentCard": false
  },
  "skills": [
    {
      "id": "skill_id",
      "name": "Skill Name",
      "description": "What this skill does",
      "examples": ["Example query 1", "Example query 2"],
      "tags": []
    }
  ],
  "securitySchemes": {},
  "security": []
}
```

### 2. Task

The core unit of work with lifecycle management:

```json
{
  "id": "task_123",
  "contextId": "context_456",
  "status": {
    "state": "working",
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "artifacts": [],
  "history": [],
  "metadata": {}
}
```

**Task States:**

| State | Description |
|-------|-------------|
| `submitted` | Task received, not yet processing |
| `working` | Active processing |
| `input-required` | Awaiting client response |
| `auth-required` | Awaiting authentication |
| `completed` | Successfully finished |
| `failed` | Terminated with error |
| `cancelled` | Client-requested cancellation |
| `rejected` | Agent refused processing |

### 3. Message

Communication unit between client and server:

```json
{
  "messageId": "msg_789",
  "role": "user",
  "parts": [
    {
      "type": "text",
      "text": "Hello, agent!"
    }
  ],
  "contextId": "context_456",
  "taskId": "task_123",
  "metadata": {}
}
```

**Roles:** `user` | `agent`

### 4. Part

Content container supporting multiple types:

| Type | Structure | Description |
|------|-----------|-------------|
| **Text** | `{"type": "text", "text": "..."}` | Plain text, markdown, HTML |
| **File** | `{"type": "file", "uri": "...", "mimeType": "..."}` | File reference |
| **Data** | `{"type": "data", "data": {...}}` | Structured JSON |

### 5. Artifact

Task output representation:

```json
{
  "id": "artifact_001",
  "name": "Result",
  "description": "Calculation result",
  "parts": [
    {"type": "text", "text": "42"}
  ],
  "metadata": {}
}
```

---

## JSON-RPC 2.0 Operations

### Method List

| Method | Description |
|--------|-------------|
| `message/send` | Send message, returns Task or Message |
| `message/stream` | Streaming variant with SSE |
| `tasks/get` | Retrieve task state by ID |
| `tasks/list` | List tasks with filtering/pagination |
| `tasks/cancel` | Cancel an active task |
| `tasks/subscribe` | Stream updates for existing task |
| `tasks/pushNotificationConfig/create` | Create webhook config |
| `tasks/pushNotificationConfig/get` | Get webhook config |
| `tasks/pushNotificationConfig/list` | List webhook configs |
| `tasks/pushNotificationConfig/delete` | Delete webhook config |
| `agent/getExtendedCard` | Get authenticated agent card |

### Request Format

```json
{
  "jsonrpc": "2.0",
  "id": "request_id",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"type": "text", "text": "Hello"}],
      "messageId": "msg_001"
    }
  }
}
```

### Response Format

**Success:**
```json
{
  "jsonrpc": "2.0",
  "id": "request_id",
  "result": {
    "task": { ... }
  }
}
```

**Error:**
```json
{
  "jsonrpc": "2.0",
  "id": "request_id",
  "error": {
    "code": -32000,
    "message": "Task not found",
    "data": { "taskId": "invalid_id" }
  }
}
```

### Error Codes

| Code | Name | Description |
|------|------|-------------|
| `-32700` | Parse Error | Invalid JSON |
| `-32600` | Invalid Request | Invalid JSON-RPC structure |
| `-32601` | Method Not Found | Unknown method |
| `-32602` | Invalid Params | Invalid method parameters |
| `-32603` | Internal Error | Server error |
| `-32000` | TaskNotFoundError | Task does not exist |
| `-32001` | PushNotificationNotSupportedError | Webhooks not supported |
| `-32002` | UnsupportedOperationError | Feature not available |
| `-32003` | ContentTypeNotSupportedError | Unsupported media type |
| `-32004` | VersionNotSupportedError | Protocol version mismatch |

---

## Streaming (Server-Sent Events)

### Stream Response Format

```
event: message
data: {"task": {...}}

event: message
data: {"statusUpdate": {"taskId": "...", "state": "working"}}

event: message
data: {"artifactUpdate": {"taskId": "...", "artifact": {...}}}

event: done
data: {"status": "complete"}
```

### Event Types

| Event | Description |
|-------|-------------|
| `task` | Initial task state |
| `message` | Direct response message |
| `statusUpdate` | Task state change |
| `artifactUpdate` | New or updated artifact |

**Ordering Guarantee:** Events MUST be delivered in generation order.

---

## Security Schemes

### Supported Authentication

| Scheme | Description |
|--------|-------------|
| **API Key** | Header, query, or cookie |
| **HTTP Auth** | Bearer, Basic, Digest |
| **OAuth 2.0** | Authorization Code, Client Credentials, Device Code |
| **OpenID Connect** | Identity layer on OAuth 2.0 |
| **Mutual TLS** | Certificate-based auth |

### Example Security Declaration

```json
{
  "securitySchemes": {
    "apiKey": {
      "type": "apiKey",
      "in": "header",
      "name": "X-API-Key"
    },
    "oauth2": {
      "type": "oauth2",
      "flows": {
        "clientCredentials": {
          "tokenUrl": "https://auth.example.com/token",
          "scopes": {
            "agent:read": "Read agent data",
            "agent:write": "Execute tasks"
          }
        }
      }
    }
  },
  "security": [{"apiKey": []}, {"oauth2": ["agent:read"]}]
}
```

---

## Implementation Guide

### Dependencies

```bash
pip install a2a-sdk uvicorn python-dotenv
```

### Server Implementation (3-File Pattern)

#### 1. agent.py - Agent Definition

```python
from a2a.types import AgentCapabilities, AgentSkill, AgentCard, ContentTypes

def create_agent_card(url: str) -> AgentCard:
    return AgentCard(
        name="my_agent",
        description="Agent description",
        url=url,
        version="1.0.0",
        protocolVersion="0.3.0",
        defaultInputModes=[ContentTypes.TEXT],
        defaultOutputModes=[ContentTypes.TEXT],
        capabilities=AgentCapabilities(
            streaming=True,
            pushNotifications=False,
        ),
        skills=[
            AgentSkill(
                id="main_skill",
                name="Main Skill",
                description="What this agent does",
                examples=["Example query"],
                tags=["category"],
            )
        ],
    )
```

#### 2. agent_executor.py - Business Logic

```python
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import Part, TextPart, Task, TaskState, TaskStatus
from a2a.utils import completed_task, new_artifact, working_task

class MyAgentExecutor(AgentExecutor):
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ) -> None:
        user_input = context.get_user_input()

        # Signal working state (optional, for long tasks)
        await event_queue.enqueue_event(
            working_task(context.task_id, context.context_id)
        )

        # --- YOUR AGENT LOGIC HERE ---
        result = await self.process(user_input)
        # ------------------------------

        # Create response parts
        parts = [Part(root=TextPart(text=result))]

        # Complete task with artifact
        await event_queue.enqueue_event(
            completed_task(
                context.task_id,
                context.context_id,
                artifacts=[new_artifact(parts, f"result_{context.task_id}")],
                history=[context.message],
            )
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ) -> Task | None:
        # Handle cancellation request
        return None

    async def process(self, input_text: str) -> str:
        # Implement your logic
        return f"Processed: {input_text}"
```

#### 3. __main__.py - Server Entry Point

```python
import uvicorn
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.apps import A2AStarletteApplication
from a2a.server.tasks import InMemoryTaskStore
from .agent import create_agent_card
from .agent_executor import MyAgentExecutor

def main():
    host = "0.0.0.0"
    port = 8080
    url = f"http://{host}:{port}/"

    agent_card = create_agent_card(url)

    handler = DefaultRequestHandler(
        agent_executor=MyAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=handler,
    )

    print(f"A2A Agent running at {url}")
    print(f"Agent Card: {url}.well-known/agent-card.json")

    uvicorn.run(app.build(), host=host, port=port)

if __name__ == "__main__":
    main()
```

### Client Implementation

```python
import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    SendMessageRequest,
    MessageSendParams,
    Message,
    Part,
    TextPart,
)

async def call_agent(agent_url: str, query: str):
    async with httpx.AsyncClient(timeout=60.0) as http:
        # 1. Discover agent
        resolver = A2ACardResolver(
            base_url=agent_url,
            httpx_client=http
        )
        card = await resolver.get_agent_card()
        print(f"Connected to: {card.name} v{card.version}")

        # 2. Create client
        client = A2AClient(http, card, url=agent_url)

        # 3. Build message
        message = Message(
            role="user",
            parts=[Part(root=TextPart(text=query))],
        )

        # 4. Send request
        request = SendMessageRequest(
            params=MessageSendParams(message=message)
        )

        response = await client.send_message(request)
        return response

# Streaming client
async def call_agent_streaming(agent_url: str, query: str):
    async with httpx.AsyncClient(timeout=None) as http:
        resolver = A2ACardResolver(base_url=agent_url, httpx_client=http)
        card = await resolver.get_agent_card()
        client = A2AClient(http, card, url=agent_url)

        message = Message(
            role="user",
            parts=[Part(root=TextPart(text=query))],
        )
        request = SendMessageRequest(
            params=MessageSendParams(message=message)
        )

        async for event in client.send_message_streaming(request):
            if hasattr(event, 'task'):
                print(f"Task: {event.task.status.state}")
            elif hasattr(event, 'artifact'):
                print(f"Artifact: {event.artifact}")
```

---

## Best Practices

### 1. Agent Discovery
Always fetch `AgentCard` before interaction to adapt to capability changes.

### 2. Streaming
Use SSE for long-running tasks to provide real-time updates.

### 3. Artifacts vs Messages
- **Artifacts**: Final deliverables (files, structured data)
- **Messages**: Conversational updates, status information

### 4. Error Handling
```python
try:
    response = await client.send_message(request)
except A2AError as e:
    if e.code == -32000:
        print("Task not found")
    elif e.code == -32602:
        print("Invalid parameters")
```

### 5. Pagination
```python
# List tasks with pagination
params = TaskQueryParams(
    contextId="ctx_123",
    status=["completed", "failed"],
    pageSize=50,
    pageToken=None,  # For first page
)
response = await client.list_tasks(params)
next_page_token = response.nextPageToken
```

### 6. Push Notifications
```python
# Configure webhook for async updates
config = PushNotificationConfig(
    url="https://myserver.com/webhook",
    authentication={
        "type": "bearer",
        "token": "secret_token"
    }
)
await client.create_push_notification_config(task_id, config)
```

---

## Quick Reference

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/.well-known/agent-card.json` | GET | Public agent card |
| `/` | POST | JSON-RPC endpoint |

### Headers

| Header | Description |
|--------|-------------|
| `Content-Type` | `application/json` |
| `Accept` | `application/json` or `text/event-stream` |
| `A2A-Version` | Protocol version (e.g., `0.3.0`) |

### SDK Utilities

```python
from a2a.utils import (
    completed_task,    # Create completed task event
    failed_task,       # Create failed task event
    working_task,      # Create working status event
    input_required,    # Request user input
    new_artifact,      # Create new artifact
    new_message,       # Create new message
)
```

---

## References

- **Official Spec**: https://a2a-protocol.org/latest/specification/
- **Definitions**: https://a2a-protocol.org/latest/definitions/
- **Python SDK**: https://pypi.org/project/a2a-sdk/
- **GitHub**: https://github.com/a2a-protocol/a2a-python
