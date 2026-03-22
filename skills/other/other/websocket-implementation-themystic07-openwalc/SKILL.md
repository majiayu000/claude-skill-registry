---
name: websocket-implementation
description: Implement real-time bidirectional communication with WebSockets including connection management, message routing, and scaling. Use when building real-time features, chat systems, live notifications, or collaborative applications.
---

# WebSocket Implementation

## Overview

Build scalable WebSocket systems for real-time communication with proper connection management, message routing, error handling, and horizontal scaling support.

## When to Use

- Building real-time chat and messaging
- Implementing live notifications
- Creating collaborative editing tools
- Broadcasting live data updates
- Building real-time dashboards
- Streaming events to clients
- Live multiplayer games

## Instructions

### 1. **Node.js WebSocket Server (Socket.IO)**

```javascript
const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const redis = require("redis");

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: { origin: "*" },
  transports: ["websocket", "polling"],
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 5,
});

// Redis adapter for horizontal scaling
const redisClient = redis.createClient();
const { createAdapter } = require("@socket.io/redis-adapter");

io.adapter(createAdapter(redisClient, redisClient.duplicate()));

// Connection management
const connectedUsers = new Map();

io.on("connection", (socket) => {
  console.log(`User connected: ${socket.id}`);

  // Store user connection
  socket.on("auth", (userData) => {
    connectedUsers.set(socket.id, {
      userId: userData.id,
      username: userData.username,
      socketId: socket.id,
      connectedAt: new Date(),
    });

    // Join user-specific room
    socket.join(`user:${userData.id}`);
    socket.join("authenticated_users");

    // Notify others user is online
    io.to("authenticated_users").emit("user:online", {
      userId: userData.id,
      username: userData.username,
      timestamp: new Date(),
    });

    console.log(`User authenticated: ${userData.username}`);
  });

  // Chat messaging
  socket.on("chat:message", (message) => {
    const user = connectedUsers.get(socket.id);

    if (!user) {
      socket.emit("error", { message: "Not authenticated" });
      return;
    }

    const chatMessage = {
      id: `msg_${Date.now()}`,
      senderId: user.userId,
      senderName: user.username,
      text: message.text,
      roomId: message.roomId,
      timestamp: new Date(),
      status: "delivered",
    };

    // Save to database
    Message.create(chatMessage);

    // Broadcast to room
    io.to(`room:${message.roomId}`).emit("chat:message", chatMessage);

    // Update message status
    setTimeout(() => {
      socket.emit("chat:message:ack", {
        messageId: chatMessage.id,
        status: "read",
      });
    }, 100);
  });

  // Room management
  socket.on("room:join", (roomId) => {
    socket.join(`room:${roomId}`);

    const user = connectedUsers.get(socket.id);
    io.to(`room:${roomId}`).emit("room:user:joined", {
      userId: user.userId,
      username: user.username,
      timestamp: new Date(),
    });
  });

  socket.on("room:leave", (roomId) => {
    socket.leave(`room:${roomId}`);

    const user = connectedUsers.get(socket.id);
    io.to(`room:${roomId}`).emit("room:user:left", {
      userId: user.userId,
      timestamp: new Date(),
    });
  });

  // Typing indicator
  socket.on("typing:start", (roomId) => {
    const user = connectedUsers.get(socket.id);
    io.to(`room:${roomId}`).emit("typing:indicator", {
      userId: user.userId,
      username: user.username,
      isTyping: true,
    });
  });

  socket.on("typing:stop", (roomId) => {
    const user = connectedUsers.get(socket.id);
    io.to(`room:${roomId}`).emit("typing:indicator", {
      userId: user.userId,
      isTyping: false,
    });
  });

  // Handle disconnection
  socket.on("disconnect", () => {
    const user = connectedUsers.get(socket.id);

    if (user) {
      connectedUsers.delete(socket.id);
      io.to("authenticated_users").emit("user:offline", {
        userId: user.userId,
        timestamp: new Date(),
      });

      console.log(`User disconnected: ${user.username}`);
    }
  });

  // Error handling
  socket.on("error", (error) => {
    console.error(`Socket error: ${error}`);
    socket.emit("error", { message: "An error occurred" });
  });
});

// Server methods
const broadcastUserUpdate = (userId, data) => {
  io.to(`user:${userId}`).emit("user:update", data);
};

const notifyRoom = (roomId, event, data) => {
  io.to(`room:${roomId}`).emit(event, data);
};

const sendDirectMessage = (userId, event, data) => {
  io.to(`user:${userId}`).emit(event, data);
};

server.listen(3000, () => {
  console.log("WebSocket server listening on port 3000");
});
```

### 2. **Browser WebSocket Client**

```javascript
class WebSocketClient {
  constructor(url, options = {}) {
    this.url = url;
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
    this.reconnectDelay = options.reconnectDelay || 1000;
    this.listeners = new Map();
    this.messageQueue = [];
    this.isAuthenticated = false;

    this.connect();
  }

  connect() {
    this.socket = io(this.url, {
      reconnection: true,
      reconnectionDelay: this.reconnectDelay,
      reconnectionAttempts: this.maxReconnectAttempts,
    });

    this.socket.on("connect", () => {
      console.log("Connected to server");
      this.reconnectAttempts = 0;
      this.processMessageQueue();
    });

    this.socket.on("disconnect", () => {
      console.log("Disconnected from server");
    });

    this.socket.on("error", (error) => {
      console.error("Socket error:", error);
      this.emit("error", error);
    });

    this.socket.on("connect_error", (error) => {
      console.error("Connection error:", error);
    });
  }

  authenticate(userData) {
    this.socket.emit("auth", userData, (response) => {
      if (response.success) {
        this.isAuthenticated = true;
        this.emit("authenticated");
      }
    });
  }

  on(event, callback) {
    this.socket.on(event, callback);

    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  emit(event, data, callback) {
    if (!this.socket.connected) {
      this.messageQueue.push({ event, data, callback });
      return;
    }

    this.socket.emit(event, data, callback);
  }

  processMessageQueue() {
    while (this.messageQueue.length > 0) {
      const { event, data, callback } = this.messageQueue.shift();
      this.socket.emit(event, data, callback);
    }
  }

  joinRoom(roomId) {
    this.emit("room:join", roomId);
  }

  leaveRoom(roomId) {
    this.emit("room:leave", roomId);
  }

  sendMessage(roomId, text) {
    this.emit("chat:message", { roomId, text });
  }

  setTypingIndicator(roomId, isTyping) {
    if (isTyping) {
      this.emit("typing:start", roomId);
    } else {
      this.emit("typing:stop", roomId);
    }
  }

  disconnect() {
    this.socket.disconnect();
  }
}

// Usage
const client = new WebSocketClient("http://localhost:3000");

client.on("chat:message", (message) => {
  console.log("Received message:", message);
  displayMessage(message);
});

client.on("typing:indicator", (data) => {
  updateTypingIndicator(data);
});

client.on("user:online", (user) => {
  updateUserStatus(user.userId, "online");
});

client.authenticate({ id: "user123", username: "john" });
client.joinRoom("room1");
client.sendMessage("room1", "Hello everyone!");
```

### 3. **Python WebSocket Server (aiohttp)**

```python
from aiohttp import web
import aiohttp
import json
from datetime import datetime
from typing import Set

class WebSocketServer:
    def __init__(self):
        self.app = web.Application()
        self.rooms = {}
        self.users = {}
        self.setup_routes()

    def setup_routes(self):
        self.app.router.add_get('/ws', self.websocket_handler)
        self.app.router.add_post('/api/message', self.send_message_api)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        user_id = None
        room_id = None

        async for msg in ws.iter_any():
            if isinstance(msg, aiohttp.WSMessage):
                data = json.loads(msg.data)
                event_type = data.get('type')

                try:
                    if event_type == 'auth':
                        user_id = data.get('userId')
                        self.users[user_id] = ws
                        await ws.send_json({
                            'type': 'authenticated',
                            'timestamp': datetime.now().isoformat()
                        })

                    elif event_type == 'join_room':
                        room_id = data.get('roomId')
                        if room_id not in self.rooms:
                            self.rooms[room_id] = set()
                        self.rooms[room_id].add(user_id)

                        # Notify others
                        await self.broadcast_to_room(room_id, {
                            'type': 'user_joined',
                            'userId': user_id,
                            'timestamp': datetime.now().isoformat()
                        }, exclude=user_id)

                    elif event_type == 'message':
                        message = {
                            'id': f'msg_{datetime.now().timestamp()}',
                            'userId': user_id,
                            'text': data.get('text'),
                            'roomId': room_id,
                            'timestamp': datetime.now().isoformat()
                        }

                        # Save to database
                        await self.save_message(message)

                        # Broadcast to room
                        await self.broadcast_to_room(room_id, message)

                    elif event_type == 'leave_room':
                        if room_id in self.rooms:
                            self.rooms[room_id].discard(user_id)

                except Exception as error:
                    await ws.send_json({
                        'type': 'error',
                        'message': str(error)
                    })

        # Cleanup on disconnect
        if user_id:
            del self.users[user_id]
        if room_id and user_id:
            if room_id in self.rooms:
                self.rooms[room_id].discard(user_id)

        return ws

    async def broadcast_to_room(self, room_id, message, exclude=None):
        if room_id not in self.rooms:
            return

        for user_id in self.rooms[room_id]:
            if user_id != exclude and user_id in self.users:
                try:
                    await self.users[user_id].send_json(message)
                except Exception as error:
                    print(f'Error sending message: {error}')

    async def save_message(self, message):
        # Save to database
        pass

    async def send_message_api(self, request):
        data = await request.json()
        room_id = data.get('roomId')

        await self.broadcast_to_room(room_id, {
            'type': 'message',
            'text': data.get('text'),
            'timestamp': datetime.now().isoformat()
        })

        return web.json_response({'sent': True})

def create_app():
    server = WebSocketServer()
    return server.app

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, port=3000)
```

### 4. **Message Types and Protocols**

```json
// Authentication
{
  "type": "auth",
  "userId": "user123",
  "token": "jwt_token_here"
}

// Chat Message
{
  "type": "message",
  "roomId": "room123",
  "text": "Hello everyone!",
  "timestamp": "2025-01-15T10:30:00Z"
}

// Typing Indicator
{
  "type": "typing",
  "roomId": "room123",
  "isTyping": true
}

// Presence
{
  "type": "presence",
  "status": "online|away|offline"
}

// Notification
{
  "type": "notification",
  "title": "New message",
  "body": "You have a new message",
  "data": {}
}
```

### 5. **Scaling with Redis**

```javascript
const redis = require("redis");
const { createAdapter } = require("@socket.io/redis-adapter");
const { createClient } = require("redis");

const pubClient = createClient({ host: "redis", port: 6379 });
const subClient = pubClient.duplicate();

io.adapter(createAdapter(pubClient, subClient));

// Publish to multiple servers
io.emit("user:action", { userId: 123, action: "login" });

// Subscribe to events from other servers
redisClient.subscribe("notifications", (message) => {
  const notification = JSON.parse(message);
  io.to(`user:${notification.userId}`).emit("notification", notification);
});
```

## Best Practices

### ✅ DO

- Implement proper authentication
- Handle reconnection gracefully
- Manage rooms/channels effectively
- Persist messages appropriately
- Monitor active connections
- Implement presence features
- Use Redis for scaling
- Add message acknowledgment
- Implement rate limiting
- Handle errors properly

### ❌ DON'T

- Send unencrypted sensitive data
- Keep unlimited message history in memory
- Allow arbitrary room/channel creation
- Forget to clean up disconnected connections
- Send large messages frequently
- Ignore network failures
- Store passwords in messages
- Skip authentication/authorization
- Create unbounded growth of connections
- Ignore scalability from day one

## Monitoring

```javascript
// Track active connections
io.engine.on("connection_error", (err) => {
  console.log(err.req); // the request object
  console.log(err.code); // the error code, e.g. 1
  console.log(err.message); // the error message
  console.log(err.context); // some additional error context
});

app.get("/metrics/websocket", (req, res) => {
  res.json({
    activeConnections: io.engine.clientsCount,
    connectedSockets: io.sockets.sockets.size,
    rooms: Object.keys(io.sockets.adapter.rooms),
  });
});
```
