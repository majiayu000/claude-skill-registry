---
name: websockets-realtime
description: WebSocket and real-time patterns. Use when implementing live chat, notifications, dashboards, collaborative features, or any real-time communication with WebSockets or SSE.
---

# WebSockets & Real-Time Patterns

## FastAPI WebSocket
```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set

class ConnectionManager:
    def __init__(self):
        # room_id → set of connected websockets
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, ws: WebSocket, room: str):
        await ws.accept()
        self.rooms.setdefault(room, set()).add(ws)

    def disconnect(self, ws: WebSocket, room: str):
        if room in self.rooms:
            self.rooms[room].discard(ws)

    async def broadcast(self, room: str, message: dict):
        dead = set()
        for ws in self.rooms.get(room, set()):
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.disconnect(ws, room)

    async def send_personal(self, ws: WebSocket, message: dict):
        await ws.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(ws: WebSocket, room_id: str, token: str = Query(...)):
    # Auth
    user = await verify_token(token)
    if not user:
        await ws.close(code=4001, reason="Unauthorized")
        return

    await manager.connect(ws, room_id)
    await manager.broadcast(room_id, {"type": "user_joined", "user": user.name})
    try:
        while True:
            data = await ws.receive_json()
            # Validate message
            if data.get("type") == "message":
                msg = {"type": "message", "user": user.name, "text": data["text"][:1000]}
                await manager.broadcast(room_id, msg)
    except WebSocketDisconnect:
        manager.disconnect(ws, room_id)
        await manager.broadcast(room_id, {"type": "user_left", "user": user.name})
```

## Server-Sent Events (SSE) — simpler than WS for server→client
```python
from fastapi.responses import StreamingResponse
import asyncio

@app.get("/events/{channel}")
async def event_stream(channel: str, request: Request):
    async def generator():
        queue: asyncio.Queue = asyncio.Queue()
        subscribers[channel].add(queue)
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"  # Keep connection alive
        finally:
            subscribers[channel].discard(queue)

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )
```

## React WebSocket Hook
```tsx
function useWebSocket(url: string) {
  const [messages, setMessages] = useState<Message[]>([])
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimer = useRef<NodeJS.Timeout>()

  const connect = useCallback(() => {
    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data)
      setMessages(prev => [...prev, msg])
    }

    ws.onclose = () => {
      // Reconnect after 3s
      reconnectTimer.current = setTimeout(connect, 3000)
    }

    ws.onerror = (e) => console.error('WS error:', e)
  }, [url])

  useEffect(() => {
    connect()
    return () => {
      clearTimeout(reconnectTimer.current)
      wsRef.current?.close()
    }
  }, [connect])

  const send = useCallback((data: object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    }
  }, [])

  return { messages, send }
}
```

## Redis Pub/Sub for Multi-Server Broadcasting
```python
# When you have multiple server instances, use Redis to broadcast
async def broadcast_via_redis(channel: str, message: dict):
    async with redis.client() as r:
        await r.publish(f"ws:{channel}", json.dumps(message))

async def redis_subscriber():
    """Run this as a background task on startup."""
    async with redis.client() as r:
        async with r.pubsub() as pubsub:
            await pubsub.psubscribe("ws:*")  # Subscribe to all ws: channels
            async for msg in pubsub.listen():
                if msg["type"] == "pmessage":
                    channel = msg["channel"].replace("ws:", "")
                    data = json.loads(msg["data"])
                    # Broadcast to all local WebSocket connections in this room
                    await manager.broadcast(channel, data)
```

## Rules
- Always authenticate WebSocket connections (token in query param or first message)
- Handle WebSocketDisconnect — cleanup room membership on disconnect
- Heartbeat/ping: send `: heartbeat` every 30s to keep connection alive through proxies
- For multi-server: use Redis Pub/Sub (not just in-memory dict)
- Use SSE for server→client only (simpler, works through HTTP/2, auto-reconnect)
- Use WebSocket for bidirectional (chat, collaborative editing, games)
- Message size limit: reject messages > 64KB
- Rate limit messages per connection (not just per IP)
