---
name: implementing-realtime-sync
description: Real-time communication patterns for live updates, collaboration, and presence. Use when building chat applications, collaborative tools, live dashboards, or streaming interfaces (LLM responses, metrics). Covers SSE (server-sent events for one-way streams), WebSocket (bidirectional communication), WebRTC (peer-to-peer video/audio), CRDTs (Yjs, Automerge for conflict-free collaboration), presence patterns, offline sync, and scaling strategies. Supports Python, Rust, Go, and TypeScript.
---

# Real-Time Sync

Implement real-time communication for live updates, collaboration, and presence awareness across applications.

## When to Use

Use this skill when building:

- **LLM streaming interfaces** - Stream tokens progressively (ai-chat integration)
- **Live dashboards** - Push metrics and updates to clients
- **Collaborative editing** - Multi-user document/spreadsheet editing with CRDTs
- **Chat applications** - Real-time messaging with presence
- **Multiplayer features** - Cursor tracking, live updates, presence awareness
- **Offline-first apps** - Mobile/PWA with sync-on-reconnect

## Protocol Selection Framework

Choose the transport protocol based on communication pattern:

### Decision Tree

```
ONE-WAY (Server → Client only)
├─ LLM streaming, notifications, live feeds
└─ Use SSE (Server-Sent Events)
   ├─ Automatic reconnection (browser-native)
   ├─ Event IDs for resumption
   └─ Simple HTTP implementation

BIDIRECTIONAL (Client ↔ Server)
├─ Chat, games, collaborative editing
└─ Use WebSocket
   ├─ Manual reconnection required
   ├─ Binary + text support
   └─ Lower latency for two-way

COLLABORATIVE EDITING
├─ Multi-user documents/spreadsheets
└─ Use WebSocket + CRDT (Yjs or Automerge)
   ├─ CRDT handles conflict resolution
   ├─ WebSocket for transport
   └─ Offline-first with sync

PEER-TO-PEER MEDIA
├─ Video, screen sharing, voice calls
└─ Use WebRTC
   ├─ WebSocket for signaling
   ├─ Direct P2P connection
   └─ STUN/TURN for NAT traversal
```

### Protocol Comparison

| Protocol | Direction | Reconnection | Complexity | Best For |
|----------|-----------|--------------|------------|----------|
| SSE | Server → Client | Automatic | Low | Live feeds, LLM streaming |
| WebSocket | Bidirectional | Manual | Medium | Chat, games, collaboration |
| WebRTC | P2P | Complex | High | Video, screen share, voice |

## Implementation Patterns

### Pattern 1: LLM Streaming with SSE

Stream LLM tokens progressively to frontend (ai-chat integration).

**Python (FastAPI):**
```python
from sse_starlette.sse import EventSourceResponse

@app.post("/chat/stream")
async def stream_chat(prompt: str):
    async def generate():
        async for chunk in llm_stream:
            yield {"event": "token", "data": chunk.content}
        yield {"event": "done", "data": "[DONE]"}
    return EventSourceResponse(generate())
```

**Frontend:**
```typescript
const es = new EventSource('/chat/stream')
es.addEventListener('token', (e) => appendToken(e.data))
```

Reference `references/sse.md` for full implementations, reconnection, and event ID resumption.

### Pattern 2: WebSocket Chat

Bidirectional communication for chat applications.

**Python (FastAPI):**
```python
connections: set[WebSocket] = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for conn in connections:
                await conn.send_text(data)
    except WebSocketDisconnect:
        connections.remove(websocket)
```

Reference `references/websockets.md` for multi-language examples, authentication, heartbeats, and scaling.

### Pattern 3: Collaborative Editing with CRDTs

Conflict-free multi-user editing using Yjs.

**TypeScript (Yjs):**
```typescript
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'

const doc = new Y.Doc()
const provider = new WebsocketProvider('ws://localhost:1234', 'doc-id', doc)
const ytext = doc.getText('content')

ytext.observe(event => console.log('Changes:', event.changes))
ytext.insert(0, 'Hello collaborative world!')
```

Reference `references/crdts.md` for conflict resolution, Yjs vs Automerge, and advanced patterns.

### Pattern 4: Presence Awareness

Track online users, cursor positions, and typing indicators.

**Yjs Awareness API:**
```typescript
const awareness = provider.awareness
awareness.setLocalState({ user: { name: 'Alice' }, cursor: { x: 100, y: 200 } })
awareness.on('change', () => {
  awareness.getStates().forEach((state, clientId) => {
    renderCursor(state.cursor, state.user)
  })
})
```

Reference `references/presence-patterns.md` for cursor tracking, typing indicators, and online status.

### Pattern 5: Offline Sync (Mobile/PWA)

Queue mutations locally and sync when connection restored.

**TypeScript (Yjs + IndexedDB):**
```typescript
import { IndexeddbPersistence } from 'y-indexeddb'
import { WebsocketProvider } from 'y-websocket'

const doc = new Y.Doc()
const indexeddbProvider = new IndexeddbPersistence('my-doc', doc)
const wsProvider = new WebsocketProvider('wss://api.example.com/sync', 'my-doc', doc)

wsProvider.on('status', (e) => {
  console.log(e.status === 'connected' ? 'Online' : 'Offline')
})
```

Reference `references/offline-sync.md` for conflict resolution and sync strategies.

## Library Recommendations

### Python

**WebSocket:**
- `websockets 13.x` - AsyncIO-based, production-ready
- `FastAPI WebSocket` - Built-in, dependency injection
- `Flask-SocketIO` - Socket.IO protocol with fallbacks

**SSE:**
- `sse-starlette` - FastAPI/Starlette, async, generator-based
- `Flask-SSE` - Redis backend for pub/sub

### Rust

**WebSocket:**
- `tokio-tungstenite 0.23` - Tokio integration, production-ready
- `axum WebSocket` - Built-in extractors, tower middleware

**SSE:**
- `axum SSE` - Native support, async streams

### Go

**WebSocket:**
- `gorilla/websocket` - Battle-tested, compression support
- `nhooyr/websocket` - Modern API, context support

**SSE:**
- `net/http` (native) - Flusher interface, no dependencies

### TypeScript

**WebSocket:**
- `ws` - Native WebSocket server, lightweight
- `Socket.io 4.x` - Auto-reconnect, fallbacks, rooms
- `Hono WebSocket` - Edge runtime (Cloudflare Workers, Deno)

**SSE:**
- `EventSource` (native) - Browser-native, automatic retry
- Node.js `http` (native) - Server-side, no dependencies

**CRDT:**
- `Yjs` - Mature, TypeScript/Rust, rich text editing
- `Automerge` - Rust/JS, JSON-like data, time-travel

## Reconnection Strategies

**SSE:** Browser's EventSource handles reconnection automatically with exponential backoff.
**WebSocket:** Implement manual exponential backoff with jitter to prevent thundering herd.

Reference `references/sse.md` and `references/websockets.md` for complete implementation patterns.

## Security Patterns

**Authentication:** Use cookie-based (same-origin) or token in Sec-WebSocket-Protocol header.
**Rate Limiting:** Implement per-user message throttling with sliding window.

Reference `references/websockets.md` for authentication and rate limiting implementations.

## Scaling with Redis Pub/Sub

For horizontal scaling, use Redis pub/sub to broadcast messages across multiple backend servers.

Reference `references/websockets.md` for complete Redis scaling implementation.

## Frontend Integration

### React Hooks Pattern

**SSE for LLM Streaming (ai-chat):**
```typescript
useEffect(() => {
  const es = new EventSource(`/api/chat/stream?prompt=${prompt}`)
  es.addEventListener('token', (e) => setContent(prev => prev + e.data))
  return () => es.close()
}, [prompt])
```

**WebSocket for Live Metrics (dashboards):**
```typescript
useEffect(() => {
  const ws = new WebSocket('ws://localhost:8000/metrics')
  ws.onmessage = (e) => setMetrics(JSON.parse(e.data))
  return () => ws.close()
}, [])
```

**Yjs for Collaborative Tables:**
```typescript
useEffect(() => {
  const doc = new Y.Doc()
  const provider = new WebsocketProvider('ws://localhost:1234', docId, doc)
  const yarray = doc.getArray('rows')
  yarray.observe(() => setRows(yarray.toArray()))
  return () => provider.destroy()
}, [docId])
```

## Reference Documentation

For detailed implementation patterns, consult:

- `references/sse.md` - SSE protocol, reconnection, event IDs
- `references/websockets.md` - WebSocket auth, heartbeats, scaling
- `references/crdts.md` - Yjs vs Automerge, conflict resolution
- `references/presence-patterns.md` - Cursor tracking, typing indicators
- `references/offline-sync.md` - Mobile patterns, conflict strategies

## Example Projects

Working implementations available in:

- `examples/llm-streaming-sse/` - FastAPI SSE for LLM streaming (RUNNABLE)
- `examples/chat-websocket/` - Python FastAPI + TypeScript chat
- `examples/collaborative-yjs/` - Yjs collaborative editor

## Testing Tools

Use scripts to validate implementations:

- `scripts/test_websocket_connection.py` - WebSocket connection testing
