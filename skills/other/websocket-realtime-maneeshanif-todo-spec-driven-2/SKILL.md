---
name: websocket-realtime
description: Implement WebSocket service for real-time task synchronization across clients. Use when building real-time updates for Phase 5. (project)
allowed-tools: Bash, Write, Read, Glob, Edit, Grep
---

# WebSocket Real-time Skill

## Quick Start

1. **Read Phase 5 Constitution** - `constitution-prompt-phase-5.md`
2. **Create WebSocket service** - New microservice on port 8005
3. **Subscribe to Kafka events** - Via Dapr pub/sub
4. **Broadcast to clients** - WebSocket connections per user
5. **Update frontend** - Connect to WebSocket service
6. **Handle reconnection** - Automatic reconnect logic

## Architecture

```
┌─────────────┐     ┌───────────────┐     ┌─────────────────┐
│   Backend   │────▶│    Kafka      │────▶│ WebSocket Svc   │
│  (Events)   │     │  task-updates │     │   (Port 8005)   │
└─────────────┘     └───────────────┘     └────────┬────────┘
                                                   │
                           WebSocket Connections   │
                    ┌──────────────────────────────┼──────────────────────────────┐
                    │                              │                              │
              ┌─────▼─────┐                 ┌──────▼──────┐                ┌──────▼──────┐
              │  Client 1 │                 │  Client 2   │                │  Client 3   │
              │  (User A) │                 │  (User A)   │                │  (User B)   │
              └───────────┘                 └─────────────┘                └─────────────┘
```

## WebSocket Service Implementation

### Project Structure

```
services/websocket/
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI app with WebSocket
│   ├── connection.py     # Connection manager
│   ├── events.py         # Event handlers
│   └── auth.py           # Token validation
├── pyproject.toml
└── Dockerfile
```

### Main Application

```python
# services/websocket/src/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from dapr.ext.fastapi import DaprApp
import json

from .connection import ConnectionManager
from .auth import verify_token

app = FastAPI(title="WebSocket Service")
dapr_app = DaprApp(app)
manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    """WebSocket endpoint for real-time updates."""
    # Verify JWT token
    user_id = await verify_token(token)
    if not user_id:
        await websocket.close(code=4001)
        return

    await manager.connect(websocket, user_id)
    try:
        while True:
            # Keep connection alive, handle client messages
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

# Dapr subscription for task events
@dapr_app.subscribe(pubsub="taskpubsub", topic="task-updates")
async def handle_task_update(event: dict):
    """Handle task update events from Kafka."""
    user_id = event.get("user_id")
    event_type = event.get("event_type")
    task_data = event.get("task")

    # Broadcast to all connections for this user
    await manager.broadcast_to_user(user_id, {
        "type": "task_update",
        "event": event_type,
        "task": task_data
    })

@app.get("/health")
async def health_check():
    return {"status": "healthy", "connections": manager.active_connections_count}
```

### Connection Manager

```python
# services/websocket/src/connection.py
from fastapi import WebSocket
from collections import defaultdict
import asyncio
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manage WebSocket connections per user."""

    def __init__(self):
        # user_id -> list of WebSocket connections
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        async with self._lock:
            self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected. Total connections: {self.active_connections_count}")

    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove a WebSocket connection."""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"User {user_id} disconnected. Total connections: {self.active_connections_count}")

    async def broadcast_to_user(self, user_id: str, message: dict):
        """Send message to all connections for a specific user."""
        if user_id not in self.active_connections:
            return

        disconnected = []
        for connection in self.active_connections[user_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send to user {user_id}: {e}")
                disconnected.append(connection)

        # Clean up disconnected
        for conn in disconnected:
            self.disconnect(conn, user_id)

    async def broadcast_to_all(self, message: dict):
        """Send message to all connected users."""
        for user_id in list(self.active_connections.keys()):
            await self.broadcast_to_user(user_id, message)

    @property
    def active_connections_count(self) -> int:
        """Total number of active connections."""
        return sum(len(conns) for conns in self.active_connections.values())
```

### Token Verification

```python
# services/websocket/src/auth.py
import jwt
import os
from typing import Optional

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "")
ALGORITHM = "HS256"

async def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return user_id."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # user_id
    except jwt.InvalidTokenError:
        return None
```

## Frontend WebSocket Client

### WebSocket Hook

```tsx
// frontend/lib/websocket/use-websocket.ts
import { useEffect, useRef, useCallback, useState } from "react";
import { useAuthStore } from "@/stores/auth-store";
import { useTaskStore } from "@/stores/task-store";

interface WebSocketMessage {
  type: string;
  event?: string;
  task?: Task;
}

export function useWebSocket() {
  const { token } = useAuthStore();
  const { updateTask, addTask, removeTask } = useTaskStore();
  const ws = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;

  const connect = useCallback(() => {
    if (!token) return;

    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/ws?token=${token}`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      console.log("WebSocket connected");
      setIsConnected(true);
      reconnectAttempts.current = 0;
    };

    ws.current.onmessage = (event) => {
      const message: WebSocketMessage = JSON.parse(event.data);
      handleMessage(message);
    };

    ws.current.onclose = () => {
      console.log("WebSocket disconnected");
      setIsConnected(false);

      // Attempt reconnection with exponential backoff
      if (reconnectAttempts.current < maxReconnectAttempts) {
        const delay = Math.pow(2, reconnectAttempts.current) * 1000;
        reconnectAttempts.current++;
        setTimeout(connect, delay);
      }
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }, [token]);

  const handleMessage = (message: WebSocketMessage) => {
    if (message.type === "task_update" && message.task) {
      switch (message.event) {
        case "task.created":
          addTask(message.task);
          break;
        case "task.updated":
          updateTask(message.task);
          break;
        case "task.deleted":
          removeTask(message.task.id);
          break;
        case "task.completed":
          updateTask({ ...message.task, status: "completed" });
          break;
      }
    }
  };

  // Heartbeat to keep connection alive
  useEffect(() => {
    if (!isConnected) return;

    const interval = setInterval(() => {
      if (ws.current?.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ type: "ping" }));
      }
    }, 30000); // Every 30 seconds

    return () => clearInterval(interval);
  }, [isConnected]);

  // Connect on mount
  useEffect(() => {
    connect();
    return () => {
      ws.current?.close();
    };
  }, [connect]);

  return { isConnected };
}
```

### WebSocket Provider

```tsx
// frontend/providers/websocket-provider.tsx
"use client";

import { createContext, useContext, ReactNode } from "react";
import { useWebSocket } from "@/lib/websocket/use-websocket";

interface WebSocketContextType {
  isConnected: boolean;
}

const WebSocketContext = createContext<WebSocketContextType>({
  isConnected: false,
});

export function WebSocketProvider({ children }: { children: ReactNode }) {
  const { isConnected } = useWebSocket();

  return (
    <WebSocketContext.Provider value={{ isConnected }}>
      {children}
    </WebSocketContext.Provider>
  );
}

export function useWebSocketStatus() {
  return useContext(WebSocketContext);
}
```

### Connection Status Indicator

```tsx
// frontend/components/websocket/connection-status.tsx
"use client";

import { useWebSocketStatus } from "@/providers/websocket-provider";
import { Wifi, WifiOff } from "lucide-react";

export function ConnectionStatus() {
  const { isConnected } = useWebSocketStatus();

  return (
    <div className="flex items-center gap-2">
      {isConnected ? (
        <>
          <Wifi className="h-4 w-4 text-green-500" />
          <span className="text-sm text-green-500">Connected</span>
        </>
      ) : (
        <>
          <WifiOff className="h-4 w-4 text-red-500" />
          <span className="text-sm text-red-500">Disconnected</span>
        </>
      )}
    </div>
  );
}
```

## Backend Event Publishing

```python
# backend/src/services/task_service.py
from dapr.clients import DaprClient

async def publish_task_update(event_type: str, task: Task):
    """Publish task update for real-time sync."""
    with DaprClient() as client:
        client.publish_event(
            pubsub_name="taskpubsub",
            topic_name="task-updates",
            data={
                "event_type": event_type,
                "user_id": str(task.user_id),
                "task": task.model_dump(mode="json")
            }
        )
```

## Kubernetes Deployment

```yaml
# k8s/websocket-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: websocket-service
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: websocket-service
  template:
    metadata:
      labels:
        app: websocket-service
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "websocket-service"
        dapr.io/app-port: "8005"
    spec:
      containers:
        - name: websocket-service
          image: evolution-todo/websocket-service:latest
          ports:
            - containerPort: 8005
          env:
            - name: BETTER_AUTH_SECRET
              valueFrom:
                secretKeyRef:
                  name: todo-secrets
                  key: better-auth-secret
---
apiVersion: v1
kind: Service
metadata:
  name: websocket-service
  namespace: todo-app
spec:
  selector:
    app: websocket-service
  ports:
    - port: 8005
      targetPort: 8005
```

## Dapr Configuration

```yaml
# dapr-components/subscription.yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-updates-subscription
spec:
  pubsubname: taskpubsub
  topic: task-updates
  routes:
    default: /task-updates
  scopes:
    - websocket-service
```

## Verification Checklist

- [ ] WebSocket service created on port 8005
- [ ] Connection manager handles multiple users
- [ ] Token verification working
- [ ] Dapr subscription configured
- [ ] Frontend WebSocket hook created
- [ ] Automatic reconnection working
- [ ] Heartbeat/ping-pong implemented
- [ ] Connection status indicator displayed
- [ ] Real-time updates propagate to all clients
- [ ] Service deployed to Kubernetes

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | Wrong URL | Check WS_URL env var |
| Auth failed | Invalid token | Verify token format |
| No updates received | Dapr not connected | Check dapr sidecar logs |
| Connection drops | No heartbeat | Implement ping/pong |
| High latency | Too many connections | Scale horizontally |

## References

- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [Dapr Pub/Sub](https://docs.dapr.io/developing-applications/building-blocks/pubsub/)
- [WebSocket API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Phase 5 Constitution](../../../constitution-prompt-phase-5.md)
