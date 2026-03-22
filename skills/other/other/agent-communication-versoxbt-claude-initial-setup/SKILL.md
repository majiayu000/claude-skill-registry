---
name: agent-communication
description: >
  Patterns for inter-agent communication including message passing, shared state,
  event-driven architectures, pub/sub, inbox/outbox, and structured vs freeform messages.
  Use when the user is building systems where multiple agents need to communicate,
  share information, coordinate work, or pass data between processing stages.
---

# Agent Communication

Patterns for communication between AI agents. Covers message passing, shared state,
event-driven design, pub/sub, inbox/outbox, and structured message formats.

## When to Use
- User is building multi-agent systems that need inter-agent communication
- User needs shared state between agents
- User wants event-driven agent coordination
- User is designing message formats for agent-to-agent data exchange
- User asks about pub/sub or inbox/outbox patterns for agents

## Core Patterns

### Direct Message Passing

Agents communicate through explicit function calls with typed messages.

```python
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class AgentMessage:
    sender: str
    recipient: str
    msg_type: str  # "request", "response", "notification"
    payload: dict
    correlation_id: str  # Links requests to responses

class MessageBus:
    def __init__(self):
        self._handlers: dict[str, list] = {}
        self._inbox: dict[str, list[AgentMessage]] = {}

    def register(self, agent_id: str, handler):
        self._handlers[agent_id] = handler
        self._inbox[agent_id] = []

    def send(self, message: AgentMessage):
        self._inbox[message.recipient].append(message)

    async def deliver(self, agent_id: str) -> list[AgentMessage]:
        messages = self._inbox[agent_id]
        self._inbox[agent_id] = []
        return messages

# Usage
bus = MessageBus()
bus.send(AgentMessage(
    sender="orchestrator",
    recipient="researcher",
    msg_type="request",
    payload={"task": "Find recent papers on RAG optimization"},
    correlation_id="task-001"
))
```

### Shared State Store

Agents read and write to a shared state store for coordination.

```python
import asyncio
from dataclasses import dataclass, field

@dataclass(frozen=True)
class StateEntry:
    value: Any
    updated_by: str
    version: int

class SharedState:
    def __init__(self):
        self._state: dict[str, StateEntry] = {}
        self._lock = asyncio.Lock()
        self._watchers: dict[str, list] = {}

    async def get(self, key: str) -> StateEntry | None:
        return self._state.get(key)

    async def put(self, key: str, value: Any, agent_id: str) -> StateEntry:
        async with self._lock:
            current = self._state.get(key)
            version = (current.version + 1) if current else 1
            entry = StateEntry(value=value, updated_by=agent_id, version=version)
            self._state = {**self._state, key: entry}  # Immutable update

            # Notify watchers
            for callback in self._watchers.get(key, []):
                await callback(key, entry)
            return entry

    def watch(self, key: str, callback):
        watchers = self._watchers.get(key, [])
        self._watchers = {**self._watchers, key: [*watchers, callback]}

# Usage
state = SharedState()
await state.put("research_findings", {"papers": [...]}, agent_id="researcher")
await state.put("code_review", {"issues": [...]}, agent_id="reviewer")

# Another agent reads the state
findings = await state.get("research_findings")
```

### Event-Driven Architecture

Agents react to events rather than being explicitly called.

```python
@dataclass(frozen=True)
class Event:
    event_type: str
    source: str
    data: dict
    timestamp: float

class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Event], Awaitable[None]]):
        handlers = self._subscribers.get(event_type, [])
        self._subscribers = {**self._subscribers, event_type: [*handlers, handler]}

    async def publish(self, event: Event):
        await asyncio.gather(*[h(event) for h in self._subscribers.get(event.event_type, [])])

# Agents subscribe to event types they care about
event_bus = EventBus()
event_bus.subscribe("code_submitted", code_analyzer)    # Triggers analysis
event_bus.subscribe("analysis_complete", test_generator) # Triggers test gen
```

### Pub/Sub with Topics

Agents subscribe to topics and receive relevant messages without tight coupling.

```python
class PubSub:
    def __init__(self):
        self._topics: dict[str, list[str]] = {}
        self._queues: dict[str, asyncio.Queue] = {}

    def subscribe(self, agent_id: str, topic: str):
        subscribers = self._topics.get(topic, [])
        self._topics = {**self._topics, topic: [*subscribers, agent_id]}
        if agent_id not in self._queues:
            self._queues[agent_id] = asyncio.Queue()

    async def publish(self, topic: str, message: dict, sender: str):
        for agent_id in self._topics.get(topic, []):
            if agent_id != sender:
                await self._queues[agent_id].put({"topic": topic, "sender": sender, "message": message})

    async def receive(self, agent_id: str, timeout: float = 30.0) -> dict | None:
        try:
            return await asyncio.wait_for(self._queues[agent_id].get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

# Usage
pubsub = PubSub()
pubsub.subscribe("security_agent", "code_changes")
pubsub.subscribe("test_agent", "code_changes")
await pubsub.publish("code_changes", {"file": "auth.py", "diff": "..."}, sender="developer")
```

### Structured Message Formats

Define typed schemas for agent-to-agent communication instead of free-form text.

```python
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass(frozen=True)
class TaskRequest:
    task_id: str
    task_type: str       # "research", "code", "review", "test"
    instruction: str
    context: dict
    priority: int        # 1 (highest) to 5 (lowest)

@dataclass(frozen=True)
class TaskResponse:
    task_id: str
    status: TaskStatus
    result: dict | None = None
    error: str | None = None
    tokens_used: int = 0
```

## Anti-Patterns
- Using unstructured free-form text between agents (hard to parse, error-prone)
- Polling shared state in tight loops instead of using watchers or events
- Not including correlation IDs to link requests with responses
- Agents modifying each other's state directly instead of through messages
- Missing error handling in message delivery (lost messages, silent failures)
- Circular event chains without termination conditions (infinite loops)
- Mutable shared state without locking (race conditions in concurrent agents)

## Quick Reference

| Pattern | Best For | Coupling |
|---------|----------|----------|
| Direct message | Point-to-point requests | High |
| Shared state | Configuration, results store | Medium |
| Event-driven | Reactive pipelines | Low |
| Pub/sub | Broadcasting to interested agents | Low |

Key guidelines: use structured messages over free-form text, include correlation IDs,
prefer immutable message objects, log all inter-agent messages, set timeouts on receives.
