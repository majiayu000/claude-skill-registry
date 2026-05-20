---
name: real-time-systems
description: Build real-time features with WebSockets, SSE, pub/sub, and CRDTs
---

# Real-Time Systems

## Approach Selection

| Requirement | WebSocket | SSE | Long Polling | WebTransport |
|-------------|-----------|-----|--------------|--------------|
| **Bidirectional** | Yes | No (client->server via fetch) | No | Yes |
| **Browser support** | All modern | All modern | All | Chrome 97+ |
| **Through CDN/proxy** | Needs upgrade | Works natively | Works natively | UDP-based, limited |
| **Reconnect built-in** | No (manual) | Yes (EventSource) | No | No |
| **Binary data** | Yes | No (text only) | Yes | Yes |
| **Best for** | Chat, collab editing | Notifications, feeds | Legacy fallback | Gaming, low-latency |

**Default:** WebSocket for bidirectional, SSE for server-push. Add Redis pub/sub when >1 server instance.

## Scaling Backend Selection

| Backend | Throughput | Persistence | Use When |
|---------|-----------|-------------|----------|
| **Redis Pub/Sub** | ~1M msg/s | None | Ephemeral broadcast, presence |
| **Redis Streams** | ~500K msg/s | Yes | Need replay, consumer groups |
| **NATS** | ~10M msg/s | No (core) | Microservices, low-latency |
| **NATS JetStream** | ~5M msg/s | Yes | Durable delivery, exactly-once |
| **Kafka** | ~1M msg/s | Yes | Event sourcing, audit trail |

## WebSocket Server with FastAPI

```python
import asyncio, json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dataclasses import dataclass, field

@dataclass
class ConnectionManager:
    rooms: dict[str, set[WebSocket]] = field(default_factory=dict)      # room -> connections
    connections: dict[WebSocket, dict] = field(default_factory=dict)     # ws -> metadata

    async def connect(self, ws: WebSocket, user_id: str, room_id: str):
        await ws.accept()
        self.connections[ws] = {"user_id": user_id, "room_id": room_id}
        self.rooms.setdefault(room_id, set()).add(ws)
        await self.broadcast(room_id, {"type": "user_joined", "user_id": user_id}, exclude=ws)

    def disconnect(self, ws: WebSocket):
        meta = self.connections.pop(ws, None)
        if meta and meta["room_id"] in self.rooms:
            self.rooms[meta["room_id"]].discard(ws)
            if not self.rooms[meta["room_id"]]:
                del self.rooms[meta["room_id"]]
        return meta

    async def broadcast(self, room_id: str, message: dict, exclude: WebSocket | None = None):
        dead: list[WebSocket] = []
        for ws in self.rooms.get(room_id, set()):
            if ws is exclude:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(ws: WebSocket, room_id: str, user_id: str):
    await manager.connect(ws, user_id, room_id)
    try:
        while True:
            data = await ws.receive_json()
            if data["type"] == "chat":
                await manager.broadcast(room_id, {
                    "type": "chat", "user_id": user_id, "text": data["text"],
                })
            elif data["type"] == "typing":
                await manager.broadcast(room_id, {"type": "typing", "user_id": user_id}, exclude=ws)
    except WebSocketDisconnect:
        meta = manager.disconnect(ws)
        if meta:
            await manager.broadcast(room_id, {"type": "user_left", "user_id": user_id})
```

## Server-Sent Events Streaming

```python
from fastapi import Request
from fastapi.responses import StreamingResponse

async def event_generator(request: Request, channel: str):
    """Yields SSE-formatted events; stops when client disconnects."""
    import redis.asyncio as aioredis
    r = aioredis.from_url("redis://localhost")
    pubsub = r.pubsub()
    await pubsub.subscribe(channel)
    try:
        async for message in pubsub.listen():
            if await request.is_disconnected():
                break
            if message["type"] == "message":
                payload = json.loads(message["data"])
                yield f"event: {payload['event']}\ndata: {json.dumps(payload['data'])}\n\n"
    finally:
        await pubsub.unsubscribe(channel)
        await r.aclose()

@app.get("/events/{channel}")
async def sse_endpoint(request: Request, channel: str):
    return StreamingResponse(
        event_generator(request, channel),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

## Redis Pub/Sub for Horizontal Scaling

```python
import redis.asyncio as aioredis

class RedisBridge:
    """Bridges local ConnectionManager with Redis for multi-instance broadcast."""
    def __init__(self, manager: ConnectionManager, redis_url: str = "redis://localhost"):
        self.manager = manager
        self.redis = aioredis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()

    async def start(self):
        await self.pubsub.psubscribe("room:*")       # Pattern subscribe
        asyncio.create_task(self._listen())

    async def _listen(self):
        async for message in self.pubsub.listen():
            if message["type"] != "pmessage":
                continue
            room_id = message["channel"].decode().split(":", 1)[1]
            data = json.loads(message["data"])
            if data.get("_origin") != id(self):       # Skip echo
                await self.manager.broadcast(room_id, data)

    async def publish(self, room_id: str, message: dict):
        message["_origin"] = id(self)
        await self.redis.publish(f"room:{room_id}", json.dumps(message))
```

## NATS JetStream Patterns

```python
import nats
from nats.js.api import StreamConfig, RetentionPolicy, ConsumerConfig, DeliverPolicy

async def setup_nats_stream():
    nc = await nats.connect("nats://localhost:4222")
    js = nc.jetstream()
    await js.add_stream(StreamConfig(
        name="EVENTS", subjects=["events.>"],
        retention=RetentionPolicy.LIMITS,
        max_bytes=1_073_741_824, max_age=86400 * 7,  # 1GB, 7 days
        duplicate_window=120,                          # 2min dedup
    ))
    return nc, js

async def durable_consumer(js, handler):
    sub = await js.pull_subscribe("events.chat.>", durable="chat-processor",
        config=ConsumerConfig(ack_wait=30, max_deliver=3, deliver_policy=DeliverPolicy.ALL))
    while True:
        for msg in await sub.fetch(batch=10, timeout=5):
            try:
                await handler(msg.data)
                await msg.ack()
            except Exception:
                await msg.nak(delay=5)                 # Negative ack with backoff
```

## Presence and Typing Indicators

```python
import time

class PresenceTracker:
    """Redis-backed presence with TTL-based expiry."""
    def __init__(self, redis, ttl: int = 30):
        self.redis = redis
        self.ttl = ttl

    async def heartbeat(self, room_id: str, user_id: str):
        await self.redis.zadd(f"presence:{room_id}", {user_id: time.time()})

    async def get_online(self, room_id: str) -> list[str]:
        cutoff = time.time() - self.ttl
        key = f"presence:{room_id}"
        await self.redis.zremrangebyscore(key, "-inf", cutoff)
        return [m.decode() for m in await self.redis.zrangebyscore(key, cutoff, "+inf")]

    async def set_typing(self, room_id: str, user_id: str):
        await self.redis.setex(f"typing:{room_id}:{user_id}", 3, "1")
```

## CRDTs for Collaborative State

```python
class GCounter:
    """Grow-only counter: each node increments its own slot; merge takes max per slot."""
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.counts: dict[str, int] = {}

    def increment(self, amount: int = 1):
        self.counts[self.node_id] = self.counts.get(self.node_id, 0) + amount

    def value(self) -> int:
        return sum(self.counts.values())

    def merge(self, other: "GCounter"):
        for node, count in other.counts.items():
            self.counts[node] = max(self.counts.get(node, 0), count)

class LWWRegister:
    """Last-Writer-Wins register: highest timestamp wins; tie-break on node_id."""
    def __init__(self):
        self.value, self.timestamp, self.node_id = None, 0.0, ""

    def set(self, value, timestamp: float, node_id: str):
        if timestamp > self.timestamp or (timestamp == self.timestamp and node_id > self.node_id):
            self.value, self.timestamp, self.node_id = value, timestamp, node_id

    def merge(self, other: "LWWRegister"):
        self.set(other.value, other.timestamp, other.node_id)
```

## Gotchas

- **WebSocket ping/pong**: Browsers don't expose ping frames; implement application-level heartbeats (30s interval, 10s timeout)
- **SSE reconnection ID**: Use `id:` field so `Last-Event-ID` header enables gap-free reconnection
- **Redis pub/sub is fire-and-forget**: No persistence; if subscriber is down, message is lost -- use Streams for durability
- **Connection limits**: Each WebSocket holds a file descriptor; set `ulimit -n`; 10K connections per instance is a reasonable ceiling
- **CRDT clock skew**: LWW-Register depends on synchronized clocks; use hybrid logical clocks (HLC) in distributed setups
- **Thundering herd on reconnect**: After restart, all clients reconnect at once -- add jittered backoff (random 0-5s delay)
- **JSON serialization overhead**: For >10K msg/s, switch to MessagePack or Protobuf
- **NATS subject naming**: Use dots for hierarchy (`events.chat.room1`), stars for wildcard -- avoid >5 levels deep
