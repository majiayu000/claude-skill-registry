---
name: websocket-realtime
description: Auto-activates when user mentions WebSocket, Socket.io, real-time, SSE, Server-Sent Events, or live updates. Expert in implementing real-time bidirectional communication.
category: backend
---

# WebSocket & Real-Time Communication

Implements production-ready real-time features using WebSockets, Socket.io, and Server-Sent Events.

## When This Activates

- User says: "add real-time updates", "implement WebSocket", "live notifications"
- User mentions: "Socket.io", "WebSocket", "SSE", "Server-Sent Events", "real-time", "live chat"
- Features: chat, live updates, notifications, collaborative editing
- Files: websocket server, Socket.io configuration

## WebSocket vs Socket.io vs SSE

### When to Use Each

**WebSocket (Native):**
- Need low-level control
- Binary data (gaming, video)
- Minimal overhead
- Custom protocol

**Socket.io:**
- Auto-reconnection needed
- Room/namespace support
- Browser compatibility
- Event-based messaging

**Server-Sent Events (SSE):**
- One-way server→client
- Simple notifications
- Automatic reconnection
- Works through proxies

## Socket.io Implementation

### Server Setup

```typescript
// server.ts
import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const app = express();
const httpServer = createServer(app);

const io = new Server(httpServer, {
  cors: {
    origin: process.env.CLIENT_URL,
    credentials: true,
  },
  transports: ['websocket', 'polling'],
  pingTimeout: 60000,
  pingInterval: 25000,
});

// Redis adapter for multi-server scaling
const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);
io.adapter(createAdapter(pubClient, subClient));

// Middleware
io.use(async (socket, next) => {
  try {
    const token = socket.handshake.auth.token;
    const user = await verifyToken(token);
    socket.data.user = user;
    next();
  } catch (err) {
    next(new Error('Authentication failed'));
  }
});

// Connection handling
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.data.user.id}`);

  // Join user-specific room
  socket.join(`user:${socket.data.user.id}`);

  // Handle events
  socket.on('message:send', async (data) => {
    const message = await saveMessage(data);
    
    // Emit to specific room
    io.to(`chat:${data.chatId}`).emit('message:new', message);
  });

  socket.on('typing:start', ({ chatId }) => {
    socket.to(`chat:${chatId}`).emit('typing:user', {
      userId: socket.data.user.id,
      name: socket.data.user.name,
    });
  });

  socket.on('typing:stop', ({ chatId }) => {
    socket.to(`chat:${chatId}`).emit('typing:stop', {
      userId: socket.data.user.id,
    });
  });

  socket.on('disconnect', () => {
    console.log(`User disconnected: ${socket.data.user.id}`);
  });
});

httpServer.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### Client Setup (React)

```typescript
// hooks/useSocket.ts
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export function useSocket() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    
    const socketInstance = io(process.env.NEXT_PUBLIC_WS_URL, {
      auth: { token },
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5,
    });

    socketInstance.on('connect', () => {
      console.log('Connected to server');
      setConnected(true);
    });

    socketInstance.on('disconnect', () => {
      console.log('Disconnected from server');
      setConnected(false);
    });

    socketInstance.on('connect_error', (error) => {
      console.error('Connection error:', error);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.close();
    };
  }, []);

  return { socket, connected };
}

// components/Chat.tsx
import { useEffect, useState } from 'react';
import { useSocket } from '../hooks/useSocket';

export function Chat({ chatId }: { chatId: string }) {
  const { socket, connected } = useSocket();
  const [messages, setMessages] = useState([]);
  const [typingUsers, setTypingUsers] = useState<string[]>([]);

  useEffect(() => {
    if (!socket) return;

    // Join chat room
    socket.emit('chat:join', { chatId });

    // Listen for new messages
    socket.on('message:new', (message) => {
      setMessages(prev => [...prev, message]);
    });

    // Listen for typing indicators
    socket.on('typing:user', ({ userId, name }) => {
      setTypingUsers(prev => [...prev, name]);
    });

    socket.on('typing:stop', ({ userId }) => {
      setTypingUsers(prev => prev.filter(id => id !== userId));
    });

    return () => {
      socket.emit('chat:leave', { chatId });
      socket.off('message:new');
      socket.off('typing:user');
      socket.off('typing:stop');
    };
  }, [socket, chatId]);

  const sendMessage = (content: string) => {
    socket?.emit('message:send', { chatId, content });
  };

  const handleTyping = () => {
    socket?.emit('typing:start', { chatId });
    
    // Debounce typing stop
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
      socket?.emit('typing:stop', { chatId });
    }, 2000);
  };

  return (
    <div>
      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id}>{msg.content}</div>
        ))}
      </div>
      {typingUsers.length > 0 && (
        <div>{typingUsers.join(', ')} typing...</div>
      )}
      <input
        onChange={handleTyping}
        onKeyPress={(e) => {
          if (e.key === 'Enter') sendMessage(e.target.value);
        }}
      />
      <div>Status: {connected ? 'Connected' : 'Disconnected'}</div>
    </div>
  );
}
```

## Server-Sent Events (SSE)

### Server Implementation

```typescript
// routes/events.ts
import express from 'express';

const router = express.Router();

router.get('/events', async (req, res) => {
  // Set SSE headers
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Send initial connection message
  res.write('data: {"type":"connected"}\n\n');

  // Authenticate user
  const user = await authenticateRequest(req);
  if (!user) {
    res.write('event: error\ndata: {"message":"Unauthorized"}\n\n');
    res.end();
    return;
  }

  // Subscribe to notifications
  const subscription = await subscribeToNotifications(user.id, (notification) => {
    res.write(`event: notification\n`);
    res.write(`data: ${JSON.stringify(notification)}\n\n`);
  });

  // Heartbeat to keep connection alive
  const heartbeat = setInterval(() => {
    res.write(': heartbeat\n\n');
  }, 30000);

  // Cleanup on disconnect
  req.on('close', () => {
    clearInterval(heartbeat);
    subscription.unsubscribe();
    res.end();
  });
});

export default router;
```

### Client Implementation

```typescript
// hooks/useSSE.ts
import { useEffect, useState } from 'react';

export function useSSE<T>(url: string) {
  const [data, setData] = useState<T[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const eventSource = new EventSource(url, {
      withCredentials: true,
    });

    eventSource.onopen = () => {
      console.log('SSE Connected');
      setConnected(true);
    };

    eventSource.onmessage = (event) => {
      const newData = JSON.parse(event.data);
      setData(prev => [...prev, newData]);
    };

    eventSource.addEventListener('notification', (event) => {
      const notification = JSON.parse(event.data);
      setData(prev => [...prev, notification]);
    });

    eventSource.onerror = () => {
      console.error('SSE Error');
      setConnected(false);
    };

    return () => {
      eventSource.close();
    };
  }, [url]);

  return { data, connected };
}

// Usage
function Notifications() {
  const { data: notifications, connected } = useSSE('/api/events');

  return (
    <div>
      <div>Status: {connected ? 'Connected' : 'Disconnected'}</div>
      {notifications.map(notification => (
        <div key={notification.id}>{notification.message}</div>
      ))}
    </div>
  );
}
```

## Native WebSocket Implementation

```typescript
// server.ts
import { WebSocketServer } from 'ws';
import { createServer } from 'http';

const server = createServer();
const wss = new WebSocketServer({ server });

wss.on('connection', (ws, req) => {
  console.log('Client connected');

  ws.on('message', (data) => {
    const message = JSON.parse(data.toString());
    
    // Broadcast to all clients
    wss.clients.forEach(client => {
      if (client.readyState === ws.OPEN) {
        client.send(JSON.stringify(message));
      }
    });
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });

  // Send heartbeat
  const interval = setInterval(() => {
    if (ws.readyState === ws.OPEN) {
      ws.ping();
    } else {
      clearInterval(interval);
    }
  }, 30000);
});

server.listen(3000);
```

```typescript
// client.ts
const ws = new WebSocket('ws://localhost:3000');

ws.onopen = () => {
  console.log('Connected');
  ws.send(JSON.stringify({ type: 'message', content: 'Hello' }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected');
  // Reconnect logic
  setTimeout(() => connectWebSocket(), 5000);
};
```

## Real-Time Features

### Presence System

```typescript
// Track online users
const onlineUsers = new Map();

io.on('connection', (socket) => {
  const userId = socket.data.user.id;
  
  onlineUsers.set(userId, {
    socketId: socket.id,
    lastSeen: Date.now(),
  });

  io.emit('presence:update', {
    userId,
    status: 'online',
  });

  socket.on('disconnect', () => {
    onlineUsers.delete(userId);
    io.emit('presence:update', {
      userId,
      status: 'offline',
    });
  });
});
```

### Rate Limiting

```typescript
import { RateLimiterMemory } from 'rate-limiter-flexible';

const rateLimiter = new RateLimiterMemory({
  points: 10, // Number of points
  duration: 1, // Per second
});

io.use(async (socket, next) => {
  try {
    await rateLimiter.consume(socket.handshake.address);
    next();
  } catch {
    next(new Error('Rate limit exceeded'));
  }
});
```

### Message Acknowledgment

```typescript
// Server
socket.on('message:send', async (data, callback) => {
  try {
    const message = await saveMessage(data);
    io.to(data.chatId).emit('message:new', message);
    callback({ success: true, messageId: message.id });
  } catch (error) {
    callback({ success: false, error: error.message });
  }
});

// Client
socket.emit('message:send', messageData, (response) => {
  if (response.success) {
    console.log('Message sent:', response.messageId);
  } else {
    console.error('Failed to send:', response.error);
  }
});
```

## Best Practices

### 1. Reconnection Strategy

```typescript
function createSocketWithReconnect() {
  let reconnectAttempts = 0;
  const maxAttempts = 5;
  
  function connect() {
    const socket = io(url, {
      reconnection: true,
      reconnectionDelay: Math.min(1000 * 2 ** reconnectAttempts, 30000),
      reconnectionAttempts: maxAttempts,
    });

    socket.on('connect', () => {
      reconnectAttempts = 0;
    });

    socket.on('disconnect', () => {
      reconnectAttempts++;
      if (reconnectAttempts >= maxAttempts) {
        console.error('Max reconnection attempts reached');
      }
    });

    return socket;
  }

  return connect();
}
```

### 2. Message Queue for Offline

```typescript
const offlineQueue: Message[] = [];

socket.on('connect', () => {
  // Send queued messages
  while (offlineQueue.length > 0) {
    const message = offlineQueue.shift();
    socket.emit('message:send', message);
  }
});

socket.on('disconnect', () => {
  // Queue messages while offline
  sendMessage = (message) => {
    offlineQueue.push(message);
  };
});
```

### 3. Namespace Organization

```typescript
const chatIO = io.of('/chat');
const notificationIO = io.of('/notifications');

chatIO.on('connection', (socket) => {
  // Chat-specific logic
});

notificationIO.on('connection', (socket) => {
  // Notification-specific logic
});
```

## Checklist

- [ ] Authentication on connection
- [ ] Reconnection logic with exponential backoff
- [ ] Heartbeat/ping-pong for connection health
- [ ] Rate limiting to prevent abuse
- [ ] Message acknowledgment for critical data
- [ ] Offline message queue
- [ ] Room-based messaging for targeted updates
- [ ] Graceful error handling
- [ ] Cleanup on disconnect
- [ ] Redis adapter for multi-server scaling
- [ ] Monitoring connection metrics

**Implement real-time features, present complete WebSocket/SSE solution.**
