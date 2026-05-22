---
name: solidstart-websocket
description: "SolidStart WebSocket: experimental WebSocket endpoints, connection handling, message events, real-time communication, bidirectional data flow."
metadata:
  globs:
    - "**/ws.ts"
    - "**/*websocket*"
    - "**/*socket*"
---

# SolidStart WebSocket

Complete guide to WebSocket endpoints in SolidStart. Enable real-time bidirectional communication for chat, notifications, and live updates.

## Setup

**Note:** WebSocket support is experimental and may change in future releases.

### Enable in Config

```tsx
// app.config.ts
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({
  server: {
    experimental: {
      websocket: true,
    },
  },
}).addRouter({
  name: "ws",
  type: "http",
  handler: "./src/ws.ts",
  target: "server",
  base: "/ws",
});
```

### WebSocket Handler

```tsx
// src/ws.ts
import { eventHandler } from "vinxi/http";

export default eventHandler({
  handler() {},
  websocket: {
    async open(peer) {
      console.log("Connection opened:", peer.id, peer.url);
    },
    async message(peer, msg) {
      const message = msg.text();
      console.log("Message received:", peer.id, message);
    },
    async close(peer, details) {
      console.log("Connection closed:", peer.id);
    },
    async error(peer, error) {
      console.error("WebSocket error:", peer.id, error);
    },
  },
});
```

## Connection Lifecycle

### Open Event

Called when client connects:

```tsx
websocket: {
  async open(peer) {
    // Store connection
    connections.set(peer.id, peer);
    
    // Send welcome message
    peer.send("Welcome!");
    
    // Broadcast to others
    broadcast("User connected", peer.id);
  },
}
```

### Message Event

Handle incoming messages:

```tsx
websocket: {
  async message(peer, msg) {
    const data = msg.text(); // or msg.json() for JSON
    
    // Handle different message types
    if (data.startsWith("/")) {
      handleCommand(peer, data);
    } else {
      broadcast(data, peer.id);
    }
  },
}
```

### Close Event

Clean up on disconnect:

```tsx
websocket: {
  async close(peer, details) {
    // Remove from connections
    connections.delete(peer.id);
    
    // Broadcast disconnect
    broadcast("User disconnected", peer.id);
  },
}
```

### Error Event

Handle errors:

```tsx
websocket: {
  async error(peer, error) {
    console.error("Error for peer:", peer.id, error);
    // Handle error, possibly close connection
  },
}
```

## Client Connection

### Basic Client

```tsx
function useWebSocket(url: string) {
  const [socket, setSocket] = createSignal<WebSocket | null>(null);
  const [messages, setMessages] = createSignal<string[]>([]);

  onMount(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      setSocket(ws);
    };

    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    ws.onclose = () => {
      setSocket(null);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    onCleanup(() => {
      ws.close();
    });
  });

  const send = (message: string) => {
    socket()?.send(message);
  };

  return { socket, messages, send };
}
```

### Usage in Component

```tsx
function Chat() {
  const { messages, send } = useWebSocket("ws://localhost:3000/ws");
  const [input, setInput] = createSignal("");

  const handleSend = () => {
    send(input());
    setInput("");
  };

  return (
    <div>
      <For each={messages()}>
        {(msg) => <div>{msg}</div>}
      </For>
      <input
        value={input()}
        onInput={(e) => setInput(e.target.value)}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
```

## Message Handling

### Text Messages

```tsx
websocket: {
  async message(peer, msg) {
    const text = msg.text();
    // Handle text message
  },
}
```

### JSON Messages

```tsx
websocket: {
  async message(peer, msg) {
    const data = msg.json();
    // Handle JSON message
    if (data.type === "chat") {
      broadcast(data, peer.id);
    }
  },
}
```

### Binary Messages

```tsx
websocket: {
  async message(peer, msg) {
    const buffer = msg.arrayBuffer();
    // Handle binary data
  },
}
```

## Broadcasting

### Broadcast to All

```tsx
const connections = new Map<string, any>();

websocket: {
  async message(peer, msg) {
    const message = msg.text();
    
    // Broadcast to all connected peers
    for (const [id, conn] of connections) {
      if (id !== peer.id) {
        conn.send(message);
      }
    }
  },
}
```

### Broadcast to Room

```tsx
const rooms = new Map<string, Set<string>>();

function joinRoom(peerId: string, roomId: string) {
  if (!rooms.has(roomId)) {
    rooms.set(roomId, new Set());
  }
  rooms.get(roomId)!.add(peerId);
}

function broadcastToRoom(roomId: string, message: string, excludeId?: string) {
  const room = rooms.get(roomId);
  if (room) {
    for (const peerId of room) {
      if (peerId !== excludeId) {
        const peer = connections.get(peerId);
        peer?.send(message);
      }
    }
  }
}
```

## Common Patterns

### Chat Application

```tsx
// src/ws.ts
const connections = new Map();
const messages: string[] = [];

export default eventHandler({
  handler() {},
  websocket: {
    async open(peer) {
      connections.set(peer.id, peer);
      // Send message history
      peer.send(JSON.stringify({ type: "history", messages }));
    },
    async message(peer, msg) {
      const data = JSON.parse(msg.text());
      
      if (data.type === "message") {
        messages.push(data.text);
        // Broadcast to all
        for (const [id, conn] of connections) {
          conn.send(JSON.stringify({ type: "message", text: data.text }));
        }
      }
    },
    async close(peer) {
      connections.delete(peer.id);
    },
  },
});
```

### Real-Time Notifications

```tsx
websocket: {
  async message(peer, msg) {
    const { userId, notification } = JSON.parse(msg.text());
    
    // Send to specific user
    const userPeer = findPeerByUserId(userId);
    if (userPeer) {
      userPeer.send(JSON.stringify({ type: "notification", data: notification }));
    }
  },
}
```

### Live Updates

```tsx
// Server-side data updates
function notifyClients(data: any) {
  for (const [id, peer] of connections) {
    peer.send(JSON.stringify({ type: "update", data }));
  }
}
```

## Best Practices

1. **Handle reconnection:**
   - Implement reconnection logic on client
   - Handle connection drops gracefully

2. **Manage connections:**
   - Track active connections
   - Clean up on disconnect
   - Limit connection count if needed

3. **Validate messages:**
   - Validate incoming messages
   - Sanitize user input
   - Handle malformed data

4. **Error handling:**
   - Handle errors gracefully
   - Log errors for debugging
   - Close connections on critical errors

5. **Rate limiting:**
   - Limit message frequency
   - Prevent abuse
   - Implement throttling

## Limitations

- **Experimental**: API may change
- **Nitro dependency**: Requires Nitro server support
- **Scaling**: Consider message queue for multiple servers

## Summary

- **Experimental feature**: Enable in config
- **Event handlers**: open, message, close, error
- **Client connection**: Use WebSocket API
- **Broadcasting**: Send to multiple peers
- **Real-time**: Perfect for chat, notifications, live updates

