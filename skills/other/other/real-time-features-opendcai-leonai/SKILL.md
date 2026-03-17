---
name: real-time-features
description: Implement real-time functionality using WebSockets, Server-Sent Events (SSE), or long polling. Use when building chat applications, live dashboards, collaborative editing, notifications, or any feature requiring instant updates.
---

# Real-Time Features

## Overview

Implement real-time bidirectional communication between clients and servers for instant data synchronization and live updates.

## When to Use

- Chat and messaging applications
- Live dashboards and analytics
- Collaborative editing (Google Docs-style)
- Real-time notifications
- Live sports scores or stock tickers
- Multiplayer games
- Live auctions or bidding systems
- IoT device monitoring
- Real-time location tracking

## Technologies Comparison

| Technology | Direction | Use Case | Browser Support |
|------------|-----------|----------|-----------------|
| **WebSockets** | Bidirectional | Chat, gaming, collaboration | Excellent |
| **SSE** | Server → Client | Live updates, notifications | Good (no IE) |
| **Long Polling** | Request/Response | Fallback, simple updates | Universal |
| **WebRTC** | Peer-to-peer | Video/audio streaming | Good |

## Implementation Examples

### 1. **WebSocket Server (Node.js)**

```typescript
// server.ts
import WebSocket, { WebSocketServer } from 'ws';
import { createServer } from 'http';

interface Message {
  type: 'join' | 'message' | 'leave' | 'typing';
  userId: string;
  username: string;
  content?: string;
  timestamp: number;
}

interface Client {
  ws: WebSocket;
  userId: string;
  username: string;
  roomId: string;
}

class ChatServer {
  private wss: WebSocketServer;
  private clients: Map<string, Client> = new Map();
  private rooms: Map<string, Set<string>> = new Map();

  constructor(port: number) {
    const server = createServer();
    this.wss = new WebSocketServer({ server });

    this.wss.on('connection', this.handleConnection.bind(this));

    server.listen(port, () => {
      console.log(`WebSocket server running on port ${port}`);
    });

    // Heartbeat to detect disconnections
    this.startHeartbeat();
  }

  private handleConnection(ws: WebSocket): void {
    const clientId = this.generateId();

    console.log(`New connection: ${clientId}`);

    ws.on('message', (data: string) => {
      try {
        const message: Message = JSON.parse(data.toString());
        this.handleMessage(clientId, message, ws);
      } catch (error) {
        console.error('Invalid message format:', error);
      }
    });

    ws.on('close', () => {
      this.handleDisconnect(clientId);
    });

    ws.on('error', (error) => {
      console.error(`WebSocket error for ${clientId}:`, error);
    });

    // Keep connection alive
    (ws as any).isAlive = true;
    ws.on('pong', () => {
      (ws as any).isAlive = true;
    });
  }

  private handleMessage(
    clientId: string,
    message: Message,
    ws: WebSocket
  ): void {
    switch (message.type) {
      case 'join':
        this.handleJoin(clientId, message, ws);
        break;

      case 'message':
        this.broadcastToRoom(clientId, message);
        break;

      case 'typing':
        this.broadcastToRoom(clientId, message, [clientId]);
        break;

      case 'leave':
        this.handleDisconnect(clientId);
        break;
    }
  }

  private handleJoin(
    clientId: string,
    message: Message,
    ws: WebSocket
  ): void {
    const client: Client = {
      ws,
      userId: message.userId,
      username: message.username,
      roomId: 'general' // Could be dynamic
    };

    this.clients.set(clientId, client);

    // Add to room
    if (!this.rooms.has(client.roomId)) {
      this.rooms.set(client.roomId, new Set());
    }
    this.rooms.get(client.roomId)!.add(clientId);

    // Notify room
    this.broadcastToRoom(clientId, {
      type: 'join',
      userId: message.userId,
      username: message.username,
      timestamp: Date.now()
    });

    // Send room state to new user
    this.sendRoomState(clientId);
  }

  private broadcastToRoom(
    senderId: string,
    message: Message,
    exclude: string[] = []
  ): void {
    const sender = this.clients.get(senderId);
    if (!sender) return;

    const roomClients = this.rooms.get(sender.roomId);
    if (!roomClients) return;

    const payload = JSON.stringify(message);

    roomClients.forEach(clientId => {
      if (!exclude.includes(clientId)) {
        const client = this.clients.get(clientId);
        if (client && client.ws.readyState === WebSocket.OPEN) {
          client.ws.send(payload);
        }
      }
    });
  }

  private sendRoomState(clientId: string): void {
    const client = this.clients.get(clientId);
    if (!client) return;

    const roomClients = this.rooms.get(client.roomId);
    if (!roomClients) return;

    const users = Array.from(roomClients)
      .map(id => this.clients.get(id))
      .filter(c => c && c.userId !== client.userId)
      .map(c => ({ userId: c!.userId, username: c!.username }));

    client.ws.send(JSON.stringify({
      type: 'room_state',
      users,
      timestamp: Date.now()
    }));
  }

  private handleDisconnect(clientId: string): void {
    const client = this.clients.get(clientId);
    if (!client) return;

    // Remove from room
    const roomClients = this.rooms.get(client.roomId);
    if (roomClients) {
      roomClients.delete(clientId);

      // Notify others
      this.broadcastToRoom(clientId, {
        type: 'leave',
        userId: client.userId,
        username: client.username,
        timestamp: Date.now()
      });
    }

    this.clients.delete(clientId);
    console.log(`Client disconnected: ${clientId}`);
  }

  private startHeartbeat(): void {
    setInterval(() => {
      this.wss.clients.forEach((ws: any) => {
        if (ws.isAlive === false) {
          return ws.terminate();
        }
        ws.isAlive = false;
        ws.ping();
      });
    }, 30000);
  }

  private generateId(): string {
    return Math.random().toString(36).substr(2, 9);
  }
}

// Start server
new ChatServer(8080);
```

### 2. **WebSocket Client (React)**

```typescript
// useWebSocket.ts
import { useEffect, useRef, useState, useCallback } from 'react';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
}

export const useWebSocket = (options: UseWebSocketOptions) => {
  const {
    url,
    onMessage,
    onOpen,
    onClose,
    onError,
    reconnectAttempts = 5,
    reconnectInterval = 3000
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<
    'connecting' | 'connected' | 'disconnected' | 'error'
  >('connecting');

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectCountRef = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();

  const connect = useCallback(() => {
    try {
      setConnectionStatus('connecting');
      const ws = new WebSocket(url);

      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        setConnectionStatus('connected');
        reconnectCountRef.current = 0;
        onOpen?.();
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          onMessage?.(data);
        } catch (error) {
          console.error('Failed to parse message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('error');
        onError?.(error);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        setConnectionStatus('disconnected');
        onClose?.();

        // Attempt reconnection
        if (reconnectCountRef.current < reconnectAttempts) {
          reconnectCountRef.current++;
          console.log(
            `Reconnecting... (${reconnectCountRef.current}/${reconnectAttempts})`
          );
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to connect:', error);
      setConnectionStatus('error');
    }
  }, [url, onMessage, onOpen, onClose, onError, reconnectAttempts, reconnectInterval]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    wsRef.current?.close();
    wsRef.current = null;
  }, []);

  const send = useCallback((data: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket is not connected');
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    connectionStatus,
    send,
    disconnect,
    reconnect: connect
  };
};

// Usage in component
const ChatComponent: React.FC = () => {
  const [messages, setMessages] = useState<any[]>([]);

  const { isConnected, send } = useWebSocket({
    url: 'ws://localhost:8080',
    onMessage: (data) => {
      if (data.type === 'message') {
        setMessages(prev => [...prev, data]);
      }
    },
    onOpen: () => {
      send({
        type: 'join',
        userId: 'user123',
        username: 'John Doe',
        timestamp: Date.now()
      });
    }
  });

  const sendMessage = (content: string) => {
    send({
      type: 'message',
      userId: 'user123',
      username: 'John Doe',
      content,
      timestamp: Date.now()
    });
  };

  return (
    <div>
      <div>Status: {isConnected ? 'Connected' : 'Disconnected'}</div>
      <div>
        {messages.map((msg, i) => (
          <div key={i}>{msg.username}: {msg.content}</div>
        ))}
      </div>
    </div>
  );
};
```

### 3. **Server-Sent Events (SSE)**

```typescript
// server.ts - SSE endpoint
import express from 'express';

const app = express();

interface Client {
  id: string;
  res: express.Response;
}

class SSEManager {
  private clients: Client[] = [];

  addClient(id: string, res: express.Response): void {
    // Set SSE headers
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');

    this.clients.push({ id, res });

    // Send initial connection event
    this.sendToClient(id, {
      type: 'connected',
      clientId: id,
      timestamp: Date.now()
    });

    console.log(`Client ${id} connected. Total: ${this.clients.length}`);
  }

  removeClient(id: string): void {
    this.clients = this.clients.filter(client => client.id !== id);
    console.log(`Client ${id} disconnected. Total: ${this.clients.length}`);
  }

  sendToClient(id: string, data: any): void {
    const client = this.clients.find(c => c.id === id);
    if (client) {
      client.res.write(`data: ${JSON.stringify(data)}\n\n`);
    }
  }

  broadcast(data: any, excludeId?: string): void {
    const message = `data: ${JSON.stringify(data)}\n\n`;
    this.clients.forEach(client => {
      if (client.id !== excludeId) {
        client.res.write(message);
      }
    });
  }

  sendEvent(event: string, data: any): void {
    const message = `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
    this.clients.forEach(client => {
      client.res.write(message);
    });
  }
}

const sseManager = new SSEManager();

app.get('/events', (req, res) => {
  const clientId = Math.random().toString(36).substr(2, 9);

  sseManager.addClient(clientId, res);

  req.on('close', () => {
    sseManager.removeClient(clientId);
  });
});

// Simulate real-time updates
setInterval(() => {
  sseManager.broadcast({
    type: 'update',
    value: Math.random() * 100,
    timestamp: Date.now()
  });
}, 5000);

app.listen(3000, () => {
  console.log('SSE server running on port 3000');
});
```

```typescript
// client.ts - SSE client
class SSEClient {
  private eventSource: EventSource | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect(url: string, handlers: {
    onMessage?: (data: any) => void;
    onError?: (error: Event) => void;
    onOpen?: () => void;
  }): void {
    this.eventSource = new EventSource(url);

    this.eventSource.onopen = () => {
      console.log('SSE connected');
      this.reconnectAttempts = 0;
      handlers.onOpen?.();
    };

    this.eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handlers.onMessage?.(data);
      } catch (error) {
        console.error('Failed to parse SSE data:', error);
      }
    };

    this.eventSource.onerror = (error) => {
      console.error('SSE error:', error);
      handlers.onError?.(error);

      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        setTimeout(() => {
          console.log('Reconnecting to SSE...');
          this.connect(url, handlers);
        }, 3000);
      }
    };

    // Custom event listeners
    this.eventSource.addEventListener('custom-event', (event: any) => {
      console.log('Custom event:', JSON.parse(event.data));
    });
  }

  disconnect(): void {
    this.eventSource?.close();
    this.eventSource = null;
  }
}

// Usage
const client = new SSEClient();
client.connect('http://localhost:3000/events', {
  onMessage: (data) => {
    console.log('Received:', data);
  },
  onOpen: () => {
    console.log('Connected to server');
  }
});
```

### 4. **Socket.IO (Production-Ready)**

```typescript
// server.ts
import { Server } from 'socket.io';
import { createServer } from 'http';

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: {
    origin: process.env.CLIENT_URL || 'http://localhost:3000',
    methods: ['GET', 'POST']
  },
  pingTimeout: 60000,
  pingInterval: 25000
});

// Middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (isValidToken(token)) {
    next();
  } else {
    next(new Error('Authentication error'));
  }
});

io.on('connection', (socket) => {
  console.log(`User connected: ${socket.id}`);

  // Join room
  socket.on('join-room', (roomId: string) => {
    socket.join(roomId);
    socket.to(roomId).emit('user-joined', {
      userId: socket.id,
      timestamp: Date.now()
    });
  });

  // Handle messages
  socket.on('message', (data) => {
    const roomId = Array.from(socket.rooms)[1]; // First is own ID
    io.to(roomId).emit('message', {
      ...data,
      userId: socket.id,
      timestamp: Date.now()
    });
  });

  // Typing indicator
  socket.on('typing', (isTyping: boolean) => {
    const roomId = Array.from(socket.rooms)[1];
    socket.to(roomId).emit('user-typing', {
      userId: socket.id,
      isTyping
    });
  });

  socket.on('disconnect', () => {
    console.log(`User disconnected: ${socket.id}`);
  });
});

httpServer.listen(3001);

function isValidToken(token: string): boolean {
  // Implement token validation
  return true;
}
```

## Best Practices

### ✅ DO
- Implement reconnection logic with exponential backoff
- Use heartbeat/ping-pong to detect dead connections
- Validate and sanitize all messages
- Implement authentication and authorization
- Handle connection limits and rate limiting
- Use compression for large payloads
- Implement proper error handling
- Monitor connection health
- Use rooms/channels for targeted messaging
- Implement graceful shutdown

### ❌ DON'T
- Send sensitive data without encryption
- Keep connections open indefinitely without cleanup
- Broadcast to all users when targeted messaging suffices
- Ignore connection state management
- Send large payloads frequently
- Skip message validation
- Forget about mobile/unstable connections
- Ignore scaling considerations

## Performance Optimization

```typescript
// Message batching
class MessageBatcher {
  private queue: any[] = [];
  private timer: NodeJS.Timeout | null = null;
  private batchSize = 10;
  private batchDelay = 100;

  constructor(
    private sendFn: (messages: any[]) => void
  ) {}

  add(message: any): void {
    this.queue.push(message);

    if (this.queue.length >= this.batchSize) {
      this.flush();
    } else if (!this.timer) {
      this.timer = setTimeout(() => this.flush(), this.batchDelay);
    }
  }

  private flush(): void {
    if (this.queue.length > 0) {
      this.sendFn(this.queue.splice(0));
    }
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
  }
}
```

## Resources

- [WebSocket API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Socket.IO Documentation](https://socket.io/docs/)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [ws - WebSocket Library](https://github.com/websockets/ws)
