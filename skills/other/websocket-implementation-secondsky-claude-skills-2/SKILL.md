---
name: websocket-implementation
description: Implements real-time WebSocket communication with connection management, room-based messaging, and horizontal scaling. Use when building chat systems, live notifications, collaborative tools, or real-time dashboards.
---

# WebSocket Implementation

Build scalable real-time communication systems with proper connection management.

## Server Implementation (Socket.IO)

```javascript
const { Server } = require('socket.io');
const { createAdapter } = require('@socket.io/redis-adapter');
const { createClient } = require('redis');

const io = new Server(server, {
  cors: { origin: process.env.CLIENT_URL, credentials: true }
});

// Redis adapter for horizontal scaling
const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();
Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  io.adapter(createAdapter(pubClient, subClient));
});

// Connection management
const users = new Map();

io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    socket.user = verifyToken(token);
    next();
  } catch (err) {
    next(new Error('Authentication failed'));
  }
});

io.on('connection', (socket) => {
  users.set(socket.user.id, socket.id);
  console.log(`User ${socket.user.id} connected`);

  socket.on('join-room', (roomId) => {
    socket.join(roomId);
    socket.to(roomId).emit('user-joined', socket.user);
  });

  socket.on('message', ({ roomId, content }) => {
    io.to(roomId).emit('message', {
      userId: socket.user.id,
      content,
      timestamp: Date.now()
    });
  });

  socket.on('disconnect', () => {
    users.delete(socket.user.id);
  });
});

// Utility methods for message distribution
function broadcastUserUpdate(userId, data) {
  io.to(`user:${userId}`).emit('user-update', data);
}

function notifyRoom(roomId, event, data) {
  io.to(`room:${roomId}`).emit(event, data);
}

function sendDirectMessage(userId, message) {
  const socketId = users.get(userId);
  if (socketId) {
    io.to(socketId).emit('direct-message', message);
  }
}
```

## Client Implementation

```javascript
import { io } from 'socket.io-client';

class WebSocketClient {
  constructor(url, token) {
    this.socket = io(url, {
      auth: { token },
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    });

    this.messageQueue = [];
    this.setupListeners();
  }

  setupListeners() {
    this.socket.on('connect', () => {
      console.log('Connected');
      this.flushQueue();
    });

    this.socket.on('disconnect', (reason) => {
      console.log('Disconnected:', reason);
    });

    this.socket.on('message', (msg) => {
      this.onMessage?.(msg);
    });
  }

  joinRoom(roomId) {
    this.socket.emit('join-room', roomId);
  }

  send(roomId, content) {
    if (this.socket.connected) {
      this.socket.emit('message', { roomId, content });
    } else {
      this.messageQueue.push({ roomId, content });
    }
  }

  flushQueue() {
    while (this.messageQueue.length > 0) {
      const msg = this.messageQueue.shift();
      this.socket.emit('message', msg);
    }
  }
}
```

## React Hook

```javascript
function useWebSocket(url) {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // getToken() is a user-supplied helper that returns the current auth token
    // Example implementations:
    // - From localStorage: () => localStorage.getItem('authToken')
    // - From context: () => authContext.token
    // - From cookie: () => document.cookie.split('token=')[1]
    const ws = io(url, { auth: { token: getToken() } });

    ws.on('connect', () => setConnected(true));
    ws.on('disconnect', () => setConnected(false));
    ws.on('message', (msg) => {
      setMessages(prev => [...prev, msg]);
    });

    setSocket(ws);
    return () => ws.disconnect();
  }, [url]);

  const send = useCallback((roomId, content) => {
    socket?.emit('message', { roomId, content });
  }, [socket]);

  return { connected, messages, send };
}
```

## Message Protocol

```typescript
interface Message {
  type: 'message' | 'typing' | 'presence';
  roomId: string;
  userId: string;
  content?: string;
  timestamp: number;
}

// Acknowledge delivery
socket.emit('message', data, (ack) => {
  if (ack.success) console.log('Delivered');
});
```

## Additional Implementations

See [references/python-websocket.md](references/python-websocket.md) for:
- Python aiohttp WebSocket server
- FastAPI WebSocket endpoints
- Async connection handling

## Scaling Considerations

| Connections | Architecture |
|-------------|--------------|
| <10K | Single server |
| 10K-100K | Redis pub/sub |
| >100K | Sharded Redis + load balancer |

## Monitoring Endpoints

```javascript
// Express endpoints for operational visibility
app.get('/api/ws/stats', (req, res) => {
  res.json({
    activeConnections: io.sockets.sockets.size,
    rooms: [...io.sockets.adapter.rooms.keys()],
    users: users.size
  });
});

app.get('/api/ws/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    memoryUsage: process.memoryUsage()
  });
});
```

## Best Practices

- Authenticate before allowing operations
- Implement reconnection with exponential backoff
- Use rooms and channels for targeted broadcasting
- Add heartbeat/ping for connection health
- Persist important messages to database
- Monitor active connection counts
- Display user presence/availability status
- Implement rate limiting on incoming messages
- Use acknowledgments to confirm message delivery
- Leverage Redis for distributed deployments
- Implement comprehensive error handling

## Never Do

- Send sensitive data unencrypted
- Store unlimited messages in memory
- Skip authorization on room joins
- Ignore connection error handling
- Allow unbounded room subscriptions
- Neglect cleanup of disconnected user data
- Send frequent oversized message payloads
- Include authentication credentials in message bodies
- Deploy without security validation
- Allow uncontrolled connection accumulation
- Build without scalability consideration
