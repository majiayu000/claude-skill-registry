---
name: websocket
description: Production-grade WebSocket patterns for Python (FastAPI/Starlette) with connection management, rooms, and message protocols
---

# WebSocket Skill

Production-grade WebSocket patterns for real-time communication in Python applications.

## When to Use This Skill

Use this skill when:
- Building real-time features (chat, notifications, live updates)
- Implementing bidirectional client-server communication
- Creating collaborative features (multi-user editing, presence)
- Building dashboards with live data feeds
- Implementing game servers or real-time applications

## Core Mental Model

A WebSocket connection is fundamentally different from HTTP:

```
HTTP:     Request → Response → Done
WebSocket: Connect → Accept → [Receive Loop] → Disconnect → Cleanup
```

The **receive loop** is unavoidable because:
1. The connection is long-lived - something must continuously listen
2. Messages arrive asynchronously from the client
3. The loop defines the connection's lifetime boundary
4. Even when frameworks abstract it, a loop exists underneath

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     WebSocket System                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────────────────────────┐  │
│  │   Client 1   │───▶│                                  │  │
│  └──────────────┘    │                                  │  │
│                      │     Connection Manager           │  │
│  ┌──────────────┐    │  ┌─────────────────────────────┐ │  │
│  │   Client 2   │───▶│  │ connections: Set[WebSocket] │ │  │
│  └──────────────┘    │  │ rooms: Dict[str, Set[WS]]   │ │  │
│                      │  └─────────────────────────────┘ │  │
│  ┌──────────────┐    │                                  │  │
│  │   Client N   │───▶│  connect() → track              │  │
│  └──────────────┘    │  disconnect() → remove          │  │
│                      │  broadcast() → fan-out          │  │
│                      │  send_to_room() → targeted      │  │
│                      └──────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
app/
├── websocket/
│   ├── __init__.py
│   ├── manager.py          # ConnectionManager class
│   ├── handlers.py         # Message handlers by type
│   ├── models.py           # Message schemas (Pydantic)
│   └── router.py           # WebSocket endpoint
└── main.py                 # Mount WebSocket router
```

## Core Principles

### 1. Explicit Connection Lifecycle

Connections must be:
- **Accepted explicitly** - Never assume connection success
- **Tracked centrally** - Single source of truth
- **Removed on disconnect** - Eager cleanup prevents leaks
- **Silent failures are worse than explicit disconnects**

### 2. Centralized Connection Management

```python
# Connection state lives in ONE place
class ConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)
```

Business logic must NEVER handle socket tracking directly.

### 3. Receive Loop Responsibility

The receive loop:
- Defines connection lifetime
- Is the only entry point for client messages
- Must handle disconnection gracefully

```python
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:  # THE LOOP
            data = await websocket.receive_text()
            # validate → dispatch → respond
    except WebSocketDisconnect:
        pass  # Expected, not exceptional
    finally:
        manager.disconnect(websocket)  # Always cleanup
```

### 4. Message Contract Discipline

Every message must be:
- **Structured**: JSON, not raw strings
- **Typed**: `{"type": "chat", "payload": {...}}`
- **Intent-declaring**: The `type` field routes to handlers

```python
class WebSocketMessage(BaseModel):
    type: str
    payload: dict = {}
```

### 5. Defensive Failure Handling

- Disconnections happen constantly (normal, not exceptional)
- Writes can fail even after reads succeed
- Dead connections must be cleaned eagerly
- One failure must not cascade to others

## Extended Concepts

### Rooms / Channels

A room is a **logical routing layer**, not a socket feature:

```python
class ConnectionManager:
    def __init__(self):
        self.connections: set[WebSocket] = set()
        self.rooms: dict[str, set[WebSocket]] = defaultdict(set)

    def join_room(self, websocket: WebSocket, room_id: str) -> None:
        self.rooms[room_id].add(websocket)

    def leave_room(self, websocket: WebSocket, room_id: str) -> None:
        self.rooms[room_id].discard(websocket)

    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        for connection in self.rooms[room_id]:
            await connection.send_text(message)
```

Key insights:
- Connection belongs to exactly 1 manager, but 0+ rooms
- Room membership is explicit (join/leave operations)
- Leaving a room ≠ disconnecting (orthogonal concerns)

### Performance Mental Model

Performance is about **control**, not speed:

| Cost Center | Why It Matters |
|-------------|----------------|
| Fan-out O(n) | Broadcast to 1000 clients = 1000 sends |
| Serialization | JSON encoding per message adds up |
| Slow clients | One blocked send() can stall others |

Safety principles:
1. Never block the receive loop with slow operations
2. Writes must not delay reads
3. One slow client must not affect others

## Generation Order

When implementing WebSocket features:

1. **Define message types** - What messages will be exchanged?
2. **Create ConnectionManager** - Central state management
3. **Implement receive loop** - WebSocket endpoint
4. **Add message handlers** - Route by message type
5. **Add rooms (if needed)** - Logical grouping
6. **Add error handling** - Defensive cleanup

## Quick Reference

```python
# Accept connection
await websocket.accept()

# Receive message
data = await websocket.receive_text()
data = await websocket.receive_json()

# Send message
await websocket.send_text(message)
await websocket.send_json(data)

# Close connection
await websocket.close(code=1000)

# Handle disconnection
from starlette.websockets import WebSocketDisconnect
```

## What "Production-Grade" Means

**Not:**
- Feature-rich
- Horizontally scalable (yet)
- Prematurely optimized

**Yes:**
- Predictable behavior under all conditions
- Clear separation: connection management | business logic | routing
- Safe defaults (cleanup on failure, structured messages)
- Clear upgrade paths to rooms, scaling, tuning

## Explicit Non-Goals

These are intentionally excluded to keep the core pattern clean:
- Authentication / authorization (handle before WebSocket upgrade)
- Persistence (message history is a separate concern)
- Distributed state (requires Redis/pubsub, out of scope)
- Message ordering guarantees across processes

## References

See the `references/` directory for:
- `connection-manager-pattern.md` - Centralized connection tracking
- `receive-loop-pattern.md` - Message loop structure and lifetime
- `message-protocol-pattern.md` - JSON message contracts
- `rooms-pattern.md` - Logical routing and channels
- `error-handling-pattern.md` - Defensive failure handling
