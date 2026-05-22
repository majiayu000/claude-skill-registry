---
name: socket-io
description: Builds real-time applications with Socket.IO including events, rooms, namespaces, and acknowledgements. Use when implementing real-time features, chat applications, live updates, or multiplayer functionality.
---

# Socket.IO

Real-time bidirectional event-based communication library.

## Quick Start

**Install Server:**
```bash
npm install socket.io
```

**Install Client:**
```bash
npm install socket.io-client
```

## Server Setup

### Basic Server (Node.js)

```typescript
// server.ts
import { createServer } from 'http';
import { Server } from 'socket.io';

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: {
    origin: 'http://localhost:3000',
    methods: ['GET', 'POST'],
  },
});

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

httpServer.listen(3001, () => {
  console.log('Socket.IO server running on port 3001');
});
```

### Express Integration

```typescript
import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: 'http://localhost:3000',
  },
});

app.get('/', (req, res) => {
  res.send('Hello World');
});

io.on('connection', (socket) => {
  console.log('Connected:', socket.id);
});

httpServer.listen(3001);
```

### Next.js API Route

```typescript
// pages/api/socket.ts (Pages Router)
import { Server } from 'socket.io';
import type { NextApiRequest, NextApiResponse } from 'next';
import type { Server as HTTPServer } from 'http';
import type { Socket as NetSocket } from 'net';

interface SocketServer extends HTTPServer {
  io?: Server;
}

interface SocketWithIO extends NetSocket {
  server: SocketServer;
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (!(res.socket as SocketWithIO).server.io) {
    const io = new Server((res.socket as SocketWithIO).server, {
      path: '/api/socket',
      addTrailingSlash: false,
    });

    io.on('connection', (socket) => {
      console.log('Connected:', socket.id);

      socket.on('message', (data) => {
        io.emit('message', data);
      });
    });

    (res.socket as SocketWithIO).server.io = io;
  }

  res.end();
}
```

## Client Setup

### Browser Client

```typescript
import { io } from 'socket.io-client';

const socket = io('http://localhost:3001');

socket.on('connect', () => {
  console.log('Connected:', socket.id);
});

socket.on('disconnect', () => {
  console.log('Disconnected');
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', error);
});
```

### React Hook

```tsx
// hooks/useSocket.ts
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export function useSocket(url: string) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socketInstance = io(url);

    socketInstance.on('connect', () => {
      setIsConnected(true);
    });

    socketInstance.on('disconnect', () => {
      setIsConnected(false);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.disconnect();
    };
  }, [url]);

  return { socket, isConnected };
}
```

```tsx
// components/Chat.tsx
function Chat() {
  const { socket, isConnected } = useSocket('http://localhost:3001');
  const [messages, setMessages] = useState<string[]>([]);

  useEffect(() => {
    if (!socket) return;

    socket.on('message', (data: string) => {
      setMessages((prev) => [...prev, data]);
    });

    return () => {
      socket.off('message');
    };
  }, [socket]);

  const sendMessage = (text: string) => {
    socket?.emit('message', text);
  };

  return (
    <div>
      <p>Status: {isConnected ? 'Connected' : 'Disconnected'}</p>
      <ul>
        {messages.map((msg, i) => (
          <li key={i}>{msg}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Events

### Emit and Listen

```typescript
// Server
io.on('connection', (socket) => {
  // Receive from client
  socket.on('chat:message', (data) => {
    console.log('Message:', data);
  });

  // Send to client
  socket.emit('chat:message', { text: 'Hello from server' });
});

// Client
socket.emit('chat:message', { text: 'Hello from client' });

socket.on('chat:message', (data) => {
  console.log('Message:', data);
});
```

### Acknowledgements

```typescript
// Client sends with callback
socket.emit('save:data', { id: 1, name: 'Test' }, (response) => {
  console.log('Server response:', response);
});

// Server handles with callback
socket.on('save:data', (data, callback) => {
  // Process data
  const result = saveToDatabase(data);
  callback({ success: true, id: result.id });
});
```

### With Timeout

```typescript
// Client with timeout
socket.timeout(5000).emit('request', data, (err, response) => {
  if (err) {
    console.error('Timeout or error');
  } else {
    console.log('Response:', response);
  }
});
```

## Broadcasting

### To All Clients

```typescript
// To all connected clients (including sender)
io.emit('announcement', 'Hello everyone!');

// To all except sender
socket.broadcast.emit('user:joined', { name: 'John' });
```

### To Specific Clients

```typescript
// To specific socket ID
io.to(socketId).emit('private:message', 'Hello');

// To multiple IDs
io.to(socketId1).to(socketId2).emit('message', 'Hello');
```

## Rooms

### Join and Leave

```typescript
// Server
socket.on('room:join', (roomId) => {
  socket.join(roomId);
  socket.to(roomId).emit('user:joined', { userId: socket.id });
});

socket.on('room:leave', (roomId) => {
  socket.leave(roomId);
  socket.to(roomId).emit('user:left', { userId: socket.id });
});

socket.on('disconnect', () => {
  // Automatically leaves all rooms
});
```

### Send to Room

```typescript
// To everyone in room (except sender)
socket.to('room-1').emit('chat:message', { text: 'Hello room!' });

// To everyone in room (including sender)
io.in('room-1').emit('announcement', 'Room announcement');

// To everyone in multiple rooms
io.to('room-1').to('room-2').emit('message', 'Hello rooms!');
```

### Get Room Info

```typescript
// Get sockets in room
const sockets = await io.in('room-1').fetchSockets();
console.log('Users in room:', sockets.length);

// Get rooms a socket is in
const rooms = socket.rooms;
console.log('Socket rooms:', [...rooms]);
```

## Namespaces

### Create Namespace

```typescript
// Server
const chatNamespace = io.of('/chat');
const adminNamespace = io.of('/admin');

chatNamespace.on('connection', (socket) => {
  console.log('Chat connected:', socket.id);
});

adminNamespace.on('connection', (socket) => {
  console.log('Admin connected:', socket.id);
});

// Client
const chatSocket = io('http://localhost:3001/chat');
const adminSocket = io('http://localhost:3001/admin');
```

### Namespace Middleware

```typescript
adminNamespace.use((socket, next) => {
  const token = socket.handshake.auth.token;

  if (isValidAdminToken(token)) {
    next();
  } else {
    next(new Error('Unauthorized'));
  }
});
```

## Middleware

### Server Middleware

```typescript
// Global middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  if (isValidToken(token)) {
    socket.data.user = decodeToken(token);
    next();
  } else {
    next(new Error('Authentication error'));
  }
});

// Access user data
io.on('connection', (socket) => {
  console.log('User:', socket.data.user);
});
```

### Error Handling

```typescript
// Client handles errors
socket.on('connect_error', (error) => {
  if (error.message === 'Authentication error') {
    // Redirect to login
  }
});
```

## Chat Application Example

### Server

```typescript
interface User {
  id: string;
  name: string;
}

interface Message {
  id: string;
  userId: string;
  userName: string;
  text: string;
  timestamp: Date;
}

const users = new Map<string, User>();

io.on('connection', (socket) => {
  socket.on('user:join', (name: string) => {
    const user = { id: socket.id, name };
    users.set(socket.id, user);

    socket.broadcast.emit('user:joined', user);
    io.emit('users:list', Array.from(users.values()));
  });

  socket.on('message:send', (text: string) => {
    const user = users.get(socket.id);
    if (!user) return;

    const message: Message = {
      id: crypto.randomUUID(),
      userId: user.id,
      userName: user.name,
      text,
      timestamp: new Date(),
    };

    io.emit('message:new', message);
  });

  socket.on('typing:start', () => {
    const user = users.get(socket.id);
    if (user) {
      socket.broadcast.emit('user:typing', user);
    }
  });

  socket.on('typing:stop', () => {
    socket.broadcast.emit('user:stopped-typing', socket.id);
  });

  socket.on('disconnect', () => {
    const user = users.get(socket.id);
    if (user) {
      users.delete(socket.id);
      io.emit('user:left', user);
      io.emit('users:list', Array.from(users.values()));
    }
  });
});
```

### Client

```tsx
function ChatApp() {
  const { socket, isConnected } = useSocket('http://localhost:3001');
  const [messages, setMessages] = useState<Message[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [typingUsers, setTypingUsers] = useState<User[]>([]);

  useEffect(() => {
    if (!socket) return;

    socket.on('message:new', (message: Message) => {
      setMessages((prev) => [...prev, message]);
    });

    socket.on('users:list', (userList: User[]) => {
      setUsers(userList);
    });

    socket.on('user:typing', (user: User) => {
      setTypingUsers((prev) => [...prev, user]);
    });

    socket.on('user:stopped-typing', (userId: string) => {
      setTypingUsers((prev) => prev.filter((u) => u.id !== userId));
    });

    return () => {
      socket.off('message:new');
      socket.off('users:list');
      socket.off('user:typing');
      socket.off('user:stopped-typing');
    };
  }, [socket]);

  const sendMessage = (text: string) => {
    socket?.emit('message:send', text);
  };

  return (
    <div>
      <UserList users={users} />
      <MessageList messages={messages} />
      {typingUsers.length > 0 && (
        <p>{typingUsers.map((u) => u.name).join(', ')} typing...</p>
      )}
      <MessageInput
        onSend={sendMessage}
        onTyping={() => socket?.emit('typing:start')}
        onStopTyping={() => socket?.emit('typing:stop')}
      />
    </div>
  );
}
```

## Best Practices

1. **Use namespaces** - Separate concerns (chat, notifications, etc.)
2. **Use rooms for groups** - Efficient broadcasting
3. **Implement reconnection** - Handle connection drops
4. **Add authentication** - Use middleware
5. **Handle errors** - Catch and log errors

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing CORS config | Add cors option to server |
| Not cleaning up listeners | Remove listeners in cleanup |
| Blocking event loop | Use async handlers |
| Missing error handling | Add connect_error listener |
| Memory leaks | Clean up on disconnect |

## Reference Files

- [references/events.md](references/events.md) - Event patterns
- [references/scaling.md](references/scaling.md) - Redis adapter
- [references/security.md](references/security.md) - Authentication
