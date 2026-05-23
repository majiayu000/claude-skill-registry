# 🔌 WebSocket Development Skill

---
name: websocket-development
description: Implement real-time communication using WebSockets and Socket.io
---

## 🎯 Purpose

พัฒนา real-time features โดยใช้ WebSockets และ Socket.io

## 📋 When to Use

- Chat applications
- Live notifications
- Real-time updates
- Collaborative editing
- Gaming
- Live dashboards

## 🔧 Implementation

### Server (Socket.io)
```typescript
import { Server } from 'socket.io';

const io = new Server(server, {
  cors: { origin: '*' }
});

io.on('connection', (socket) => {
  console.log('User connected:', socket.id);
  
  // Join room
  socket.on('join', (room) => {
    socket.join(room);
  });
  
  // Handle message
  socket.on('message', (data) => {
    io.to(data.room).emit('message', data);
  });
  
  // Disconnect
  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});
```

### Client (React)
```typescript
import { io, Socket } from 'socket.io-client';
import { useEffect, useState } from 'react';

function useSocket(url: string) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  
  useEffect(() => {
    const newSocket = io(url);
    setSocket(newSocket);
    
    newSocket.on('message', (msg) => {
      setMessages(prev => [...prev, msg]);
    });
    
    return () => { newSocket.disconnect(); };
  }, [url]);
  
  const sendMessage = (content: string) => {
    socket?.emit('message', { content, timestamp: Date.now() });
  };
  
  return { messages, sendMessage, connected: !!socket };
}
```

## 📊 Event Patterns

| Event | Direction | Use Case |
|-------|-----------|----------|
| `connect` | Server→Client | Connection established |
| `disconnect` | Server→Client | Connection lost |
| `message` | Bidirectional | Send/receive messages |
| `join` | Client→Server | Join a room |
| `leave` | Client→Server | Leave a room |
| `broadcast` | Server→All | Send to all clients |

## 🔒 Security

```typescript
// Authentication middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (validateToken(token)) {
    socket.data.user = decodeToken(token);
    next();
  } else {
    next(new Error('Unauthorized'));
  }
});
```

## ✅ Best Practices

- [ ] Handle reconnection
- [ ] Implement heartbeat
- [ ] Secure with auth
- [ ] Rate limiting
- [ ] Error handling
- [ ] Room management

## 🔗 Related Skills

- `socket-io` - Socket.io specifics
- `api-design` - API patterns
- `testing` - Test real-time
