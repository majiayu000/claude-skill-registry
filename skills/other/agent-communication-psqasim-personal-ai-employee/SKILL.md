---
name: agent-communication
description: Expert guidance on multi-agent communication patterns. Use when designing or implementing: (1) Message protocols (AgentMessage, AgentResponse), (2) Request-response patterns between agents, (3) Action-based routing logic, (4) Correlation IDs for distributed tracing, (5) Error handling across agent boundaries, (6) Async message passing with queues. Invoke when building orchestrators, agent systems, or inter-service communication.
---

# Agent Communication

Expert guidance for designing robust multi-agent communication systems.

## Core Message Types

### AgentMessage (Request)

```python
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

class AgentMessage(BaseModel):
    """Immutable message sent to an agent."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    action: str  # e.g., "task_add", "storage_get"
    payload: dict[str, Any] = Field(default_factory=dict)
    correlation_id: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_agent: str | None = None

    model_config = {"frozen": True}
```

### AgentResponse (Reply)

```python
class AgentResponse(BaseModel):
    """Response from an agent."""

    success: bool
    data: dict[str, Any] | None = None
    error_code: str | None = None
    error_message: str | None = None
    correlation_id: str | None = None
    source_agent: str | None = None

    @classmethod
    def ok(cls, data: dict[str, Any], **kwargs) -> "AgentResponse":
        return cls(success=True, data=data, **kwargs)

    @classmethod
    def error(cls, code: str, message: str, **kwargs) -> "AgentResponse":
        return cls(success=False, error_code=code, error_message=message, **kwargs)
```

## Quick Routing Pattern

```python
class OrchestratorAgent:
    """Routes messages to appropriate agents."""

    def __init__(self, agents: dict[str, BaseAgent]) -> None:
        self._agents = agents
        self._routes = {
            "task_": "task_manager",
            "storage_": "storage",
            "ui_": "ui_controller",
        }

    def handle_message(self, message: AgentMessage) -> AgentResponse:
        agent_name = self._resolve_route(message.action)
        if not agent_name:
            return AgentResponse.error("ROUTING_ERROR", f"Unknown action: {message.action}")

        agent = self._agents.get(agent_name)
        return agent.handle_message(message)

    def _resolve_route(self, action: str) -> str | None:
        for prefix, agent_name in self._routes.items():
            if action.startswith(prefix):
                return agent_name
        return None
```

## Request-Response Flow

```
┌──────────┐    AgentMessage     ┌─────────────┐    AgentMessage     ┌─────────┐
│  Client  │───────────────────▶│ Orchestrator │───────────────────▶│  Agent  │
│          │                     │              │                     │         │
│          │◀───────────────────│              │◀───────────────────│         │
└──────────┘   AgentResponse     └─────────────┘   AgentResponse     └─────────┘
```

1. Client creates `AgentMessage` with action and payload
2. Orchestrator routes based on action prefix
3. Target agent processes and returns `AgentResponse`
4. Response propagates back through orchestrator

## Reference Guides

For detailed patterns, see:

- **Message Protocol**: See [references/message-protocol.md](references/message-protocol.md) for complete message design, validation, and serialization
- **Routing Patterns**: See [references/routing-patterns.md](references/routing-patterns.md) for prefix routing, registry patterns, and dynamic routing
- **Error Handling**: See [references/error-handling.md](references/error-handling.md) for error propagation, error codes, and recovery patterns
- **Async Messaging**: See [references/async-messaging.md](references/async-messaging.md) for queue-based communication and async patterns
- **Tracing Patterns**: See [references/tracing-patterns.md](references/tracing-patterns.md) for correlation IDs, distributed tracing, and observability
