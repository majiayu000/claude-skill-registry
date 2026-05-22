---
name: websocket-management
description: Production-grade WebSocket connection management with connection limits, user-to-connection mapping, ping/pong health verification, and automatic stale connection cleanup.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: api
  time: 4h
  source: drift-masterguide
---

# WebSocket Connection Management

Production-grade WebSocket connection manager with health verification and capacity management.

## When to Use This Skill

- Building real-time features with WebSockets
- Need connection limits (global and per-room)
- Want to detect and clean up stale connections
- Require reliable user-to-connection mapping

## Core Concepts

WebSocket connections can appear connected but be stale (client crashed, network dropped). The solution:
- Track connections by lobby/room AND by user ID
- Enforce connection limits (global + per-lobby)
- Ping/pong health verification
- Automatic stale connection cleanup

## Implementation

### Python (FastAPI)

```python
import asyncio
import json
import time
import logging
from typing import Dict, Optional, Set, Tuple
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Production-grade WebSocket connection manager."""

    def __init__(
        self,
        max_connections: int = 500,
        max_per_lobby: int = 10,
    ):
        self.max_connections = max_connections
        self.max_per_lobby = max_per_lobby
        
        # lobby_code -> set of websockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        
        # websocket -> (lobby_code, user_id)
        self.connection_info: Dict[WebSocket, Tuple[str, str]] = {}
        
        # user_id -> websocket (for direct messaging)
        self.user_connections: Dict[str, WebSocket] = {}
        
        # Health monitoring
        self._pending_pings: Dict[str, asyncio.Event] = {}
        self._last_message_times: Dict[str, float] = {}
    
    def can_accept_connection(self, lobby_code: str) -> Tuple[bool, str]:
        """Check if we can accept a new connection."""
        total = sum(len(conns) for conns in self.active_connections.values())
        if total >= self.max_connections:
            return False, "server_full"
        
        lobby_count = len(self.active_connections.get(lobby_code, set()))
        if lobby_count >= self.max_per_lobby:
            return False, "lobby_full"
        
        return True, ""

    async def connect(
        self,
        websocket: WebSocket,
        lobby_code: str,
        user_id: str,
    ) -> None:
        """Accept and register a WebSocket connection."""
        await websocket.accept()
        
        if lobby_code not in self.active_connections:
            self.active_connections[lobby_code] = set()
        self.active_connections[lobby_code].add(websocket)
        
        self.connection_info[websocket] = (lobby_code, user_id)
        self.user_connections[user_id] = websocket
        self._last_message_times[user_id] = time.time()

    def disconnect(self, websocket: WebSocket) -> Optional[Tuple[str, str]]:
        """Remove a WebSocket connection."""
        info = self.connection_info.get(websocket)
        if not info:
            return None
        
        lobby_code, user_id = info
        
        if lobby_code in self.active_connections:
            self.active_connections[lobby_code].discard(websocket)
            if not self.active_connections[lobby_code]:
                del self.active_connections[lobby_code]
        
        del self.connection_info[websocket]
        self.user_connections.pop(user_id, None)
        self._last_message_times.pop(user_id, None)
        self._pending_pings.pop(user_id, None)
        
        return info

    async def broadcast_to_lobby(
        self,
        lobby_code: str,
        message: dict,
        exclude_user_id: Optional[str] = None,
    ) -> int:
        """Broadcast message to all connections in a lobby."""
        if lobby_code not in self.active_connections:
            return 0
        
        data = json.dumps(message)
        disconnected = []
        sent_count = 0
        
        for websocket in self.active_connections[lobby_code]:
            if exclude_user_id:
                info = self.connection_info.get(websocket)
                if info and info[1] == exclude_user_id:
                    continue
            
            try:
                await websocket.send_text(data)
                sent_count += 1
            except Exception:
                disconnected.append(websocket)
        
        for ws in disconnected:
            self.disconnect(ws)
        
        return sent_count

    async def send_to_user(self, user_id: str, message: dict) -> bool:
        """Send message to a specific user."""
        websocket = self.user_connections.get(user_id)
        if not websocket:
            return False
        
        try:
            await websocket.send_text(json.dumps(message))
            return True
        except Exception:
            self.disconnect(websocket)
            return False

    async def ping_user(self, user_id: str, timeout: float = 2.0) -> Tuple[bool, Optional[float]]:
        """Send health check ping and wait for pong."""
        websocket = self.user_connections.get(user_id)
        if not websocket:
            return False, None
        
        ping_event = asyncio.Event()
        self._pending_pings[user_id] = ping_event
        
        start_time = time.time()
        
        try:
            await websocket.send_text(json.dumps({
                "type": "health_ping",
                "timestamp": start_time
            }))
            
            try:
                await asyncio.wait_for(ping_event.wait(), timeout=timeout)
                latency_ms = (time.time() - start_time) * 1000
                return True, latency_ms
            except asyncio.TimeoutError:
                return False, None
        finally:
            self._pending_pings.pop(user_id, None)

    def record_pong(self, user_id: str) -> None:
        """Record pong response from user."""
        self._last_message_times[user_id] = time.time()
        ping_event = self._pending_pings.get(user_id)
        if ping_event:
            ping_event.set()

    def update_last_message(self, user_id: str) -> None:
        """Update last message timestamp."""
        self._last_message_times[user_id] = time.time()

    def is_user_connected(self, user_id: str) -> bool:
        return user_id in self.user_connections

    def get_lobby_users(self, lobby_code: str) -> Set[str]:
        users = set()
        for ws in self.active_connections.get(lobby_code, set()):
            info = self.connection_info.get(ws)
            if info:
                users.add(info[1])
        return users

    def get_stats(self) -> dict:
        total = sum(len(conns) for conns in self.active_connections.values())
        return {
            "total_connections": total,
            "max_connections": self.max_connections,
            "capacity_percent": round(total / self.max_connections * 100, 1),
            "active_lobbies": len(self.active_connections),
        }


manager = ConnectionManager()
```

### TypeScript (Client)

```typescript
class WebSocketClient {
  private ws: WebSocket | null = null;
  
  connect(url: string) {
    this.ws = new WebSocket(url);
    
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      // Respond to health pings immediately
      if (message.type === 'health_ping') {
        this.ws?.send(JSON.stringify({
          type: 'health_pong',
          timestamp: message.timestamp
        }));
        return;
      }
      
      this.handleMessage(message);
    };
  }
  
  private handleMessage(message: any) {
    // Your message handling logic
  }
}
```

## Usage Examples

### FastAPI Endpoint

```python
@app.websocket("/ws/{lobby_code}")
async def websocket_endpoint(
    websocket: WebSocket,
    lobby_code: str,
    token: str = Query(...),
):
    user_id = await authenticate_token(token)
    if not user_id:
        await websocket.close(code=4001, reason="unauthorized")
        return
    
    can_accept, reason = manager.can_accept_connection(lobby_code)
    if not can_accept:
        await websocket.close(code=4002, reason=reason)
        return
    
    await manager.connect(websocket, lobby_code, user_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            manager.update_last_message(user_id)
            
            if data.get("type") == "health_pong":
                manager.record_pong(user_id)
                continue
            
            await handle_message(lobby_code, user_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

## Best Practices

1. Check capacity before accepting - Reject early with clear reason
2. Track by user ID - Enable direct messaging and presence queries
3. Ping/pong health checks - Detect stale connections (every 15-30s)
4. Clean up on send failure - Remove connections that fail to receive
5. Log connection events - Track connects, disconnects, and capacity

## Common Mistakes

- Not checking capacity before accepting connections
- Missing user-to-connection mapping (can't send direct messages)
- No health verification (stale connections accumulate)
- Not cleaning up failed sends (resource leaks)
- Forgetting to handle WebSocketDisconnect exception

## Related Patterns

- sse-streaming - Server-Sent Events alternative
- graceful-shutdown - Drain connections on shutdown
- rate-limiting - Rate limit WebSocket messages
