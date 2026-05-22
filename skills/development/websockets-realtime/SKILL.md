---
name: websockets-realtime
description: Real-time communication with WebSockets, Server-Sent Events, and related technologies. Use when building chat, live updates, collaborative features, or any real-time functionality.
---

# WebSockets & Real-Time

Comprehensive guide for building real-time applications.

## Real-Time Technologies

### Comparison

| Technology             | Direction               | Use Case                    |
| ---------------------- | ----------------------- | --------------------------- |
| **WebSocket**          | Bidirectional           | Chat, gaming, collaboration |
| **Server-Sent Events** | Server → Client         | Live feeds, notifications   |
| **Long Polling**       | Simulated bidirectional | Fallback, simple updates    |
| **WebRTC**             | Peer-to-peer            | Video calls, file sharing   |

### When to Use What

```
WEBSOCKETS:
✓ Chat applications
✓ Real-time collaboration
✓ Gaming
✓ Financial trading
✓ IoT dashboards
✓ Any bidirectional communication

SERVER-SENT EVENTS (SSE):
✓ Live feeds (news, sports)
✓ Notifications
✓ Progress updates
✓ Server-initiated updates only

LONG POLLING:
✓ Fallback when WebSocket unavailable
✓ Simple, infrequent updates
✓ Behind strict firewalls

WEBRTC:
✓ Video/audio calls
✓ Screen sharing
✓ Peer-to-peer file transfer
```

---

## WebSocket Fundamentals

### How WebSockets Work

```
HTTP Upgrade Handshake:
┌──────┐                      ┌──────┐
│Client│  GET /ws HTTP/1.1    │Server│
│      │  Upgrade: websocket  │      │
│      │ ──────────────────>  │      │
│      │                      │      │
│      │  HTTP/1.1 101        │      │
│      │  Switching Protocols │      │
│      │ <──────────────────  │      │
└──────┘                      └──────┘

After handshake:
┌──────┐                      ┌──────┐
│Client│ <═══════════════════>│Server│
│      │  Full-duplex TCP     │      │
│      │  Binary or text      │      │
└──────┘                      └──────┘
```

### Client Implementation

```typescript
// Basic WebSocket client
const ws = new WebSocket("wss://api.example.com/ws");

ws.onopen = () => {
  console.log("Connected");
  ws.send(JSON.stringify({ type: "subscribe", channel: "updates" }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Received:", data);
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
};

ws.onclose = (event) => {
  console.log("Disconnected:", event.code, event.reason);
};

// Send message
ws.send(JSON.stringify({ type: "message", content: "Hello!" }));

// Close connection
ws.close(1000, "Normal closure");
```

### Reconnection Logic

```typescript
class ReconnectingWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private reconnectDelay = 1000;

  constructor(private url: string) {
    this.connect();
  }

  private connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log("Connected");
      this.reconnectAttempts = 0;
    };

    this.ws.onclose = (event) => {
      if (event.code !== 1000) {
        this.reconnect();
      }
    };

    this.ws.onerror = () => {
      this.ws?.close();
    };
  }

  private reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error("Max reconnection attempts reached");
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

    console.log(
      `Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`,
    );

    setTimeout(() => this.connect(), delay);
  }

  send(data: unknown) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
}
```

---

## Server Implementation (Node.js)

### ws Library

```typescript
import { WebSocketServer, WebSocket } from "ws";
import { createServer } from "http";

const server = createServer();
const wss = new WebSocketServer({ server });

// Track connected clients
const clients = new Set<WebSocket>();

wss.on("connection", (ws, request) => {
  console.log("Client connected");
  clients.add(ws);

  // Send welcome message
  ws.send(JSON.stringify({ type: "connected", clientCount: clients.size }));

  ws.on("message", (data) => {
    try {
      const message = JSON.parse(data.toString());
      handleMessage(ws, message);
    } catch (error) {
      ws.send(JSON.stringify({ type: "error", message: "Invalid JSON" }));
    }
  });

  ws.on("close", () => {
    clients.delete(ws);
    console.log("Client disconnected");
  });

  ws.on("error", (error) => {
    console.error("WebSocket error:", error);
  });

  // Heartbeat to detect stale connections
  ws.isAlive = true;
  ws.on("pong", () => {
    ws.isAlive = true;
  });
});

// Heartbeat interval
const heartbeatInterval = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) {
      return ws.terminate();
    }
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);

wss.on("close", () => {
  clearInterval(heartbeatInterval);
});

function handleMessage(ws: WebSocket, message: any) {
  switch (message.type) {
    case "broadcast":
      broadcast(message.content);
      break;
    case "private":
      // Handle private messages
      break;
    default:
      ws.send(
        JSON.stringify({ type: "error", message: "Unknown message type" }),
      );
  }
}

function broadcast(content: any) {
  const message = JSON.stringify({ type: "broadcast", content });
  clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

server.listen(3000);
```

### Socket.IO

```typescript
import { Server } from "socket.io";
import { createServer } from "http";

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: {
    origin: "https://example.com",
    methods: ["GET", "POST"],
  },
});

// Namespace for chat
const chat = io.of("/chat");

chat.on("connection", (socket) => {
  console.log("User connected:", socket.id);

  // Join room
  socket.on("join", (room: string) => {
    socket.join(room);
    socket.to(room).emit("user_joined", { userId: socket.id });
  });

  // Handle message
  socket.on("message", (data: { room: string; content: string }) => {
    chat.to(data.room).emit("message", {
      from: socket.id,
      content: data.content,
      timestamp: Date.now(),
    });
  });

  // Leave room
  socket.on("leave", (room: string) => {
    socket.leave(room);
    socket.to(room).emit("user_left", { userId: socket.id });
  });

  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
  });
});

// Authentication middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (validateToken(token)) {
    socket.data.user = decodeToken(token);
    next();
  } else {
    next(new Error("Authentication error"));
  }
});

httpServer.listen(3000);
```

---

## Server-Sent Events (SSE)

### Server Implementation

```typescript
import express from "express";

const app = express();

app.get("/events", (req, res) => {
  // Set SSE headers
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  // Send initial event
  res.write("event: connected\n");
  res.write('data: {"status": "connected"}\n\n');

  // Send periodic updates
  const interval = setInterval(() => {
    const data = JSON.stringify({
      timestamp: Date.now(),
      value: Math.random(),
    });
    res.write(`data: ${data}\n\n`);
  }, 1000);

  // Cleanup on disconnect
  req.on("close", () => {
    clearInterval(interval);
    res.end();
  });
});

app.listen(3000);
```

### Client Implementation

```typescript
const eventSource = new EventSource("/events");

eventSource.onopen = () => {
  console.log("SSE connection opened");
};

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Received:", data);
};

eventSource.addEventListener("connected", (event) => {
  console.log("Connected event:", event.data);
});

eventSource.onerror = (error) => {
  console.error("SSE error:", error);
  if (eventSource.readyState === EventSource.CLOSED) {
    // Reconnect logic if needed
  }
};

// Close connection
eventSource.close();
```

---

## Message Protocols

### JSON Message Format

```typescript
// Define message types
interface BaseMessage {
  type: string;
  timestamp: number;
  id: string;
}

interface ChatMessage extends BaseMessage {
  type: "chat";
  room: string;
  content: string;
  sender: string;
}

interface PresenceMessage extends BaseMessage {
  type: "presence";
  status: "online" | "offline" | "away";
  userId: string;
}

interface ErrorMessage extends BaseMessage {
  type: "error";
  code: string;
  message: string;
}

type Message = ChatMessage | PresenceMessage | ErrorMessage;

// Type-safe message handling
function handleMessage(data: string) {
  const message: Message = JSON.parse(data);

  switch (message.type) {
    case "chat":
      displayChatMessage(message);
      break;
    case "presence":
      updateUserPresence(message);
      break;
    case "error":
      handleError(message);
      break;
  }
}
```

### Binary Protocols

```typescript
// For high-performance needs, use binary formats

// MessagePack
import { encode, decode } from "@msgpack/msgpack";

const encoded = encode({ type: "position", x: 100, y: 200 });
ws.send(encoded);

ws.onmessage = (event) => {
  const data = decode(event.data);
};

// Protocol Buffers
// Define schema in .proto file, generate types
// Smaller messages, faster serialization
```

---

## Scaling WebSockets

### Architecture

```
                    Load Balancer
                   (Sticky Sessions)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌─────────┐      ┌─────────┐      ┌─────────┐
   │ Server 1│      │ Server 2│      │ Server 3│
   │ (Node)  │      │ (Node)  │      │ (Node)  │
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                    ┌─────────┐
                    │  Redis  │
                    │ Pub/Sub │
                    └─────────┘
```

### Redis Pub/Sub for Cross-Server Messages

```typescript
import Redis from "ioredis";
import { WebSocketServer } from "ws";

const pub = new Redis();
const sub = new Redis();

const wss = new WebSocketServer({ port: 3000 });

// Subscribe to channel
sub.subscribe("broadcast");

// Forward Redis messages to local clients
sub.on("message", (channel, message) => {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
});

// Publish messages to Redis
function broadcast(message: object) {
  pub.publish("broadcast", JSON.stringify(message));
}

// Receive from WebSocket, publish to Redis
wss.on("connection", (ws) => {
  ws.on("message", (data) => {
    broadcast(JSON.parse(data.toString()));
  });
});
```

### Socket.IO with Redis Adapter

```typescript
import { Server } from "socket.io";
import { createAdapter } from "@socket.io/redis-adapter";
import { createClient } from "redis";

const pubClient = createClient({ url: "redis://localhost:6379" });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

const io = new Server();
io.adapter(createAdapter(pubClient, subClient));

// Now messages are automatically synchronized across servers
io.emit("notification", { message: "Hello all servers!" });
```

---

## React Integration

### Custom Hook

```typescript
import { useEffect, useRef, useState, useCallback } from 'react';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  reconnect?: boolean;
}

export function useWebSocket(options: UseWebSocketOptions) {
  const { url, onMessage, reconnect = true } = options;
  const wsRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);

  const connect = useCallback(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => setIsConnected(true);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLastMessage(data);
      onMessage?.(data);
    };

    ws.onclose = () => {
      setIsConnected(false);
      if (reconnect) {
        setTimeout(connect, 3000);
      }
    };

    wsRef.current = ws;
  }, [url, onMessage, reconnect]);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
    };
  }, [connect]);

  const send = useCallback((data: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  return { isConnected, lastMessage, send };
}

// Usage
function ChatComponent() {
  const { isConnected, lastMessage, send } = useWebSocket({
    url: 'wss://api.example.com/chat',
    onMessage: (data) => {
      console.log('New message:', data);
    },
  });

  return (
    <div>
      <span>Status: {isConnected ? 'Connected' : 'Disconnected'}</span>
      <button onClick={() => send({ type: 'message', content: 'Hello!' })}>
        Send
      </button>
    </div>
  );
}
```

### Socket.IO Client

```typescript
import { io, Socket } from 'socket.io-client';
import { createContext, useContext, useEffect, useState } from 'react';

const SocketContext = createContext<Socket | null>(null);

export function SocketProvider({ children }: { children: React.ReactNode }) {
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    const newSocket = io('https://api.example.com', {
      auth: { token: getAuthToken() },
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  return (
    <SocketContext.Provider value={socket}>{children}</SocketContext.Provider>
  );
}

export function useSocket() {
  const socket = useContext(SocketContext);
  if (!socket) {
    throw new Error('useSocket must be used within SocketProvider');
  }
  return socket;
}

// Usage
function ChatRoom({ roomId }: { roomId: string }) {
  const socket = useSocket();
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    socket.emit('join', roomId);

    socket.on('message', (message: Message) => {
      setMessages((prev) => [...prev, message]);
    });

    return () => {
      socket.emit('leave', roomId);
      socket.off('message');
    };
  }, [socket, roomId]);

  const sendMessage = (content: string) => {
    socket.emit('message', { room: roomId, content });
  };

  return (/* render messages */);
}
```

---

## Security

### Authentication

```typescript
// Token-based authentication
const ws = new WebSocket("wss://api.example.com/ws");

ws.onopen = () => {
  // Send auth message immediately
  ws.send(
    JSON.stringify({
      type: "auth",
      token: localStorage.getItem("token"),
    }),
  );
};

// Server-side validation
wss.on("connection", (ws, request) => {
  let authenticated = false;
  const authTimeout = setTimeout(() => {
    if (!authenticated) {
      ws.close(4001, "Authentication timeout");
    }
  }, 5000);

  ws.on("message", (data) => {
    const message = JSON.parse(data.toString());

    if (message.type === "auth") {
      if (validateToken(message.token)) {
        authenticated = true;
        clearTimeout(authTimeout);
        ws.send(JSON.stringify({ type: "auth_success" }));
      } else {
        ws.close(4002, "Invalid token");
      }
    } else if (!authenticated) {
      ws.close(4003, "Not authenticated");
    }
  });
});
```

### Rate Limiting

```typescript
const rateLimits = new Map<WebSocket, { count: number; timestamp: number }>();

function checkRateLimit(ws: WebSocket): boolean {
  const now = Date.now();
  const limit = rateLimits.get(ws);

  if (!limit || now - limit.timestamp > 1000) {
    rateLimits.set(ws, { count: 1, timestamp: now });
    return true;
  }

  if (limit.count >= 10) {
    // 10 messages per second
    return false;
  }

  limit.count++;
  return true;
}

ws.on("message", (data) => {
  if (!checkRateLimit(ws)) {
    ws.send(JSON.stringify({ type: "error", message: "Rate limit exceeded" }));
    return;
  }
  // Process message
});
```

---

## Best Practices

### DO:

- Use WSS (WebSocket Secure) in production
- Implement heartbeat/ping-pong
- Handle reconnection gracefully
- Authenticate connections
- Validate all incoming messages
- Use message IDs for acknowledgment
- Implement backpressure handling
- Monitor connection health

### DON'T:

- Trust client data without validation
- Send sensitive data without encryption
- Keep connections open indefinitely
- Ignore disconnection handling
- Block the message handler
- Send unbounded data
- Forget about horizontal scaling

---

## Troubleshooting

### Common Issues

| Problem              | Cause                | Solution               |
| -------------------- | -------------------- | ---------------------- |
| Connection drops     | Idle timeout         | Implement heartbeat    |
| Messages lost        | No acknowledgment    | Add message IDs + acks |
| High latency         | Large messages       | Use binary, compress   |
| Memory leak          | Unclosed connections | Proper cleanup         |
| Cross-origin blocked | Missing CORS         | Configure server CORS  |

### Debug Logging

```typescript
// Development logging
if (process.env.NODE_ENV === "development") {
  ws.on("message", (data) => {
    console.log("← Received:", JSON.parse(data.toString()));
  });

  const originalSend = ws.send.bind(ws);
  ws.send = (data: string) => {
    console.log("→ Sending:", JSON.parse(data));
    originalSend(data);
  };
}
```
