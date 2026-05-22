---
name: Bun WebSocket Server
description: This skill should be used when the user asks about "WebSocket in Bun", "real-time communication", "Bun.serve websocket", "ws server", "socket connections", "pub/sub", "broadcasting messages", "WebSocket upgrade", or building real-time applications with Bun.
version: 1.0.0
---

# Bun WebSocket Server

Bun has built-in WebSocket support integrated with `Bun.serve()`.

## Quick Start

```typescript
const server = Bun.serve({
  fetch(req, server) {
    // Upgrade to WebSocket
    if (server.upgrade(req)) {
      return; // Upgraded successfully
    }
    return new Response("Not a WebSocket request", { status: 400 });
  },
  websocket: {
    open(ws) {
      console.log("Client connected");
    },
    message(ws, message) {
      console.log("Received:", message);
      ws.send(`Echo: ${message}`);
    },
    close(ws) {
      console.log("Client disconnected");
    },
  },
});

console.log(`WebSocket server running on ws://localhost:${server.port}`);
```

## WebSocket Handlers

```typescript
Bun.serve({
  fetch(req, server) {
    server.upgrade(req);
  },
  websocket: {
    // Client connected
    open(ws) {
      console.log("New connection");
    },

    // Message received
    message(ws, message) {
      // message is string | Buffer
      if (typeof message === "string") {
        console.log("Text:", message);
      } else {
        console.log("Binary:", message);
      }
    },

    // Connection closed
    close(ws, code, reason) {
      console.log(`Closed: ${code} - ${reason}`);
    },

    // Drain event (buffer flushed)
    drain(ws) {
      console.log("Buffer drained");
    },

    // Ping received
    ping(ws, data) {
      // Pong sent automatically
    },

    // Pong received
    pong(ws, data) {
      console.log("Pong received");
    },
  },
});
```

## Sending Messages

```typescript
websocket: {
  message(ws, message) {
    // Send text
    ws.send("Hello");

    // Send JSON
    ws.send(JSON.stringify({ type: "greeting", data: "Hello" }));

    // Send binary
    ws.send(new Uint8Array([1, 2, 3]));
    ws.send(Buffer.from("binary data"));

    // Send with compression
    ws.send("compressed message", true);

    // Check if buffer is full
    const bufferedAmount = ws.send("data");
    if (bufferedAmount > 1024 * 1024) {
      console.log("Buffer getting full");
    }
  },
}
```

## Attaching Data to Connections

```typescript
interface UserData {
  id: string;
  name: string;
  joinedAt: Date;
}

Bun.serve<UserData>({
  fetch(req, server) {
    const url = new URL(req.url);
    const userId = url.searchParams.get("userId");

    // Attach data during upgrade
    server.upgrade(req, {
      data: {
        id: userId,
        name: "User " + userId,
        joinedAt: new Date(),
      },
    });
  },
  websocket: {
    open(ws) {
      // Access attached data
      console.log(`${ws.data.name} connected`);
    },
    message(ws, message) {
      console.log(`${ws.data.name}: ${message}`);
    },
  },
});
```

## Pub/Sub (Topics)

```typescript
Bun.serve({
  fetch(req, server) {
    const url = new URL(req.url);
    const room = url.searchParams.get("room") || "general";

    server.upgrade(req, {
      data: { room },
    });
  },
  websocket: {
    open(ws) {
      // Subscribe to a topic
      ws.subscribe(ws.data.room);

      // Publish to topic (excludes sender)
      ws.publish(ws.data.room, `User joined ${ws.data.room}`);
    },
    message(ws, message) {
      // Broadcast to all in room (excludes sender)
      ws.publish(ws.data.room, message);
    },
    close(ws) {
      // Unsubscribe (automatic on close)
      ws.unsubscribe(ws.data.room);
      ws.publish(ws.data.room, "User left");
    },
  },
});
```

## Broadcasting to All Clients

```typescript
Bun.serve({
  fetch(req, server) {
    server.upgrade(req);
  },
  websocket: {
    open(ws) {
      // Subscribe to global topic
      ws.subscribe("global");
    },
    message(ws, message) {
      // Broadcast to ALL clients including sender
      server.publish("global", message);
    },
  },
});
```

## Server-Level Publish

```typescript
const server = Bun.serve({
  fetch(req, server) {
    const url = new URL(req.url);

    // HTTP endpoint to publish
    if (url.pathname === "/broadcast") {
      const message = url.searchParams.get("msg");
      server.publish("global", message);
      return new Response("Broadcasted");
    }

    server.upgrade(req);
  },
  websocket: {
    open(ws) {
      ws.subscribe("global");
    },
  },
});

// Can also publish from outside fetch
setInterval(() => {
  server.publish("global", `Server time: ${new Date().toISOString()}`);
}, 5000);
```

## WebSocket Options

```typescript
Bun.serve({
  websocket: {
    // Max message size (default 16MB)
    maxPayloadLength: 1024 * 1024, // 1MB

    // Idle timeout in seconds (default 120)
    idleTimeout: 60,

    // Backpressure limit
    backpressureLimit: 1024 * 1024,

    // Enable compression
    perMessageDeflate: true,
    // Or with options
    perMessageDeflate: {
      compress: "shared",
      decompress: "shared",
    },

    // Send/receive pings
    sendPings: true,

    // Handlers
    open(ws) {},
    message(ws, message) {},
    close(ws) {},
  },
});
```

## Client-Side Connection

```javascript
// Browser
const ws = new WebSocket("ws://localhost:3000");

ws.onopen = () => {
  ws.send("Hello Server!");
};

ws.onmessage = (event) => {
  console.log("Received:", event.data);
};

ws.onclose = () => {
  console.log("Disconnected");
};
```

## Authentication

```typescript
Bun.serve({
  fetch(req, server) {
    // Verify auth before upgrade
    const token = req.headers.get("Authorization");

    if (!verifyToken(token)) {
      return new Response("Unauthorized", { status: 401 });
    }

    const user = decodeToken(token);
    server.upgrade(req, {
      data: { userId: user.id },
    });
  },
  websocket: {
    open(ws) {
      console.log(`Authenticated user ${ws.data.userId} connected`);
    },
  },
});
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Upgrade failed` | Invalid request | Check upgrade headers |
| `Connection closed` | Client disconnect | Handle in close handler |
| `Message too large` | Exceeds maxPayloadLength | Increase limit or chunk data |
| `Backpressure` | Slow client | Check buffer, wait for drain |

## Common Patterns

### Chat Room

```typescript
Bun.serve({
  fetch(req, server) {
    const url = new URL(req.url);
    const username = url.searchParams.get("user") || "Anonymous";

    server.upgrade(req, {
      data: { username },
    });
  },
  websocket: {
    open(ws) {
      ws.subscribe("chat");
      ws.publish("chat", `${ws.data.username} joined`);
    },
    message(ws, message) {
      ws.publish("chat", `${ws.data.username}: ${message}`);
    },
    close(ws) {
      ws.publish("chat", `${ws.data.username} left`);
    },
  },
});
```

## When to Load References

Load `references/compression.md` when:
- perMessageDeflate configuration
- Compression tuning
- Binary message handling

Load `references/scaling.md` when:
- Multiple server instances
- Redis pub/sub integration
- Horizontal scaling
