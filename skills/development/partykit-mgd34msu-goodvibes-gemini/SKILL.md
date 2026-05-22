---
name: partykit
description: Builds real-time multiplayer applications with PartyKit on Cloudflare's edge. Use when creating collaborative apps, games, AI agents, or stateful WebSocket servers with global low-latency deployment.
---

# PartyKit

Real-time infrastructure on Cloudflare's edge. Stateful WebSocket servers with on-demand rooms, global distribution, and Durable Objects backing.

## Quick Start

```bash
npm create partykit@latest my-app
cd my-app
npm run dev
```

### Server (party/index.ts)

```typescript
import type * as Party from "partykit/server";

export default class Server implements Party.Server {
  constructor(readonly room: Party.Room) {}

  onConnect(conn: Party.Connection) {
    // New WebSocket connection
    conn.send("Welcome to the party!");
  }

  onMessage(message: string, sender: Party.Connection) {
    // Broadcast to all connections
    this.room.broadcast(message, [sender.id]);
  }

  onClose(conn: Party.Connection) {
    console.log("Connection closed:", conn.id);
  }

  onRequest(req: Party.Request) {
    // Handle HTTP requests
    return new Response("Hello from HTTP!");
  }
}
```

### Client

```typescript
import PartySocket from "partysocket";

const socket = new PartySocket({
  host: "localhost:1999",  // or your-project.partykit.dev
  room: "my-room"
});

socket.addEventListener("message", (event) => {
  console.log("Received:", event.data);
});

socket.send("Hello, party!");
```

## Room Lifecycle

Each unique room ID creates a separate server instance.

```typescript
// Connecting to same room = same server instance
const socket1 = new PartySocket({ room: "room-123" });
const socket2 = new PartySocket({ room: "room-123" });  // Same server

// Different room = different server instance
const socket3 = new PartySocket({ room: "room-456" });  // Different server
```

## Server API

### Connection Handling

```typescript
export default class Server implements Party.Server {
  // Called when WebSocket connects
  onConnect(
    conn: Party.Connection,
    ctx: Party.ConnectionContext
  ) {
    console.log("Connected:", conn.id);
    console.log("Request:", ctx.request);  // Initial HTTP request
  }

  // Called when message received
  onMessage(
    message: string | ArrayBuffer,
    sender: Party.Connection
  ) {
    // Parse JSON messages
    const data = JSON.parse(message as string);

    // Reply to sender only
    sender.send(JSON.stringify({ type: "ack" }));

    // Broadcast to all except sender
    this.room.broadcast(message, [sender.id]);
  }

  // Called when connection closes
  onClose(conn: Party.Connection) {
    console.log("Disconnected:", conn.id);
  }

  // Called on connection error
  onError(conn: Party.Connection, error: Error) {
    console.error("Error:", error);
  }
}
```

### HTTP Requests

```typescript
export default class Server implements Party.Server {
  async onRequest(req: Party.Request) {
    const url = new URL(req.url);

    if (req.method === "GET") {
      return Response.json({
        connections: [...this.room.getConnections()].length
      });
    }

    if (req.method === "POST") {
      const body = await req.json();
      this.room.broadcast(JSON.stringify(body));
      return new Response("Broadcasted");
    }

    return new Response("Not found", { status: 404 });
  }
}
```

### Room State

Store state in the server instance - persists as long as room is active.

```typescript
export default class Server implements Party.Server {
  messages: string[] = [];
  users: Map<string, { name: string }> = new Map();

  constructor(readonly room: Party.Room) {}

  onConnect(conn: Party.Connection) {
    // Send history to new connections
    conn.send(JSON.stringify({
      type: "history",
      messages: this.messages
    }));
  }

  onMessage(message: string, sender: Party.Connection) {
    const data = JSON.parse(message);

    if (data.type === "message") {
      this.messages.push(data.text);
      this.room.broadcast(message);
    }

    if (data.type === "join") {
      this.users.set(sender.id, { name: data.name });
    }
  }

  onClose(conn: Party.Connection) {
    this.users.delete(conn.id);
  }
}
```

### Persistent Storage

Use Durable Object storage for data that survives room hibernation.

```typescript
export default class Server implements Party.Server {
  constructor(readonly room: Party.Room) {}

  async onStart() {
    // Called when room starts
    const stored = await this.room.storage.get<string[]>("messages");
    this.messages = stored ?? [];
  }

  async onMessage(message: string, sender: Party.Connection) {
    const data = JSON.parse(message);

    if (data.type === "message") {
      this.messages.push(data.text);

      // Persist to storage
      await this.room.storage.put("messages", this.messages);

      this.room.broadcast(message);
    }
  }

  messages: string[] = [];
}
```

## Client API (PartySocket)

### Basic Usage

```typescript
import PartySocket from "partysocket";

const socket = new PartySocket({
  host: "your-project.partykit.dev",
  room: "my-room",
  // Optional
  id: "custom-connection-id",
  query: { token: "abc123" }
});

// Event handlers
socket.addEventListener("open", () => {
  console.log("Connected!");
});

socket.addEventListener("message", (event) => {
  const data = JSON.parse(event.data);
  console.log("Received:", data);
});

socket.addEventListener("close", () => {
  console.log("Disconnected");
});

socket.addEventListener("error", (event) => {
  console.error("Error:", event);
});

// Send messages
socket.send(JSON.stringify({ type: "chat", text: "Hello!" }));

// Close connection
socket.close();
```

### Auto-Reconnect

PartySocket automatically reconnects on disconnect.

```typescript
const socket = new PartySocket({
  host: "your-project.partykit.dev",
  room: "my-room",
  // Reconnect options
  startClosed: false,
  maxRetries: 10,
  minReconnectionDelay: 1000,
  maxReconnectionDelay: 30000,
  reconnectionDelayGrowFactor: 1.3
});
```

## React Integration

```tsx
import usePartySocket from "partysocket/react";

function Chat({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<string[]>([]);

  const socket = usePartySocket({
    host: "your-project.partykit.dev",
    room: roomId,
    onMessage(event) {
      const data = JSON.parse(event.data);
      if (data.type === "message") {
        setMessages((prev) => [...prev, data.text]);
      }
    }
  });

  const sendMessage = (text: string) => {
    socket.send(JSON.stringify({ type: "message", text }));
  };

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}>{msg}</div>
      ))}
      <input
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            sendMessage(e.currentTarget.value);
            e.currentTarget.value = "";
          }
        }}
      />
    </div>
  );
}
```

### Connection State

```tsx
function ChatRoom() {
  const [status, setStatus] = useState<"connecting" | "open" | "closed">("connecting");

  const socket = usePartySocket({
    room: "chat",
    onOpen() {
      setStatus("open");
    },
    onClose() {
      setStatus("closed");
    },
    onMessage(event) {
      // Handle messages
    }
  });

  return (
    <div>
      <span>Status: {status}</span>
      {/* ... */}
    </div>
  );
}
```

## Multi-Party Architecture

Connect to different party types for different purposes.

```typescript
// partykit.json
{
  "name": "my-app",
  "main": "party/main.ts",
  "parties": {
    "game": "party/game.ts",
    "chat": "party/chat.ts"
  }
}
```

```typescript
// Client - connect to specific party
const gameSocket = new PartySocket({
  host: "your-project.partykit.dev",
  party: "game",
  room: "game-123"
});

const chatSocket = new PartySocket({
  host: "your-project.partykit.dev",
  party: "chat",
  room: "game-123-chat"
});
```

## AI Integration

```typescript
import { Ai } from "partykit-ai";

export default class Server implements Party.Server {
  ai: Ai;

  constructor(readonly room: Party.Room) {
    this.ai = new Ai(room.context.ai);
  }

  async onMessage(message: string, sender: Party.Connection) {
    const data = JSON.parse(message);

    if (data.type === "prompt") {
      // Generate AI response
      const response = await this.ai.run("@cf/meta/llama-3-8b-instruct", {
        prompt: data.text
      });

      sender.send(JSON.stringify({
        type: "ai-response",
        text: response.response
      }));
    }
  }
}
```

## Deployment

```bash
# Deploy to PartyKit cloud
npx partykit deploy

# Deploy to your Cloudflare account
npx partykit deploy --with-vars
```

### Environment Variables

```bash
# Set secrets
npx partykit env add MY_SECRET

# Use in server
export default class Server implements Party.Server {
  constructor(readonly room: Party.Room) {
    const secret = room.env.MY_SECRET;
  }
}
```

## Common Patterns

### Chat Room

```typescript
// Server
type Message = {
  id: string;
  user: string;
  text: string;
  timestamp: number;
};

export default class ChatServer implements Party.Server {
  messages: Message[] = [];

  async onStart() {
    this.messages = await this.room.storage.get("messages") ?? [];
  }

  onConnect(conn: Party.Connection) {
    // Send history
    conn.send(JSON.stringify({
      type: "sync",
      messages: this.messages.slice(-100)
    }));
  }

  async onMessage(message: string, sender: Party.Connection) {
    const data = JSON.parse(message);

    if (data.type === "message") {
      const msg: Message = {
        id: crypto.randomUUID(),
        user: data.user,
        text: data.text,
        timestamp: Date.now()
      };

      this.messages.push(msg);
      await this.room.storage.put("messages", this.messages);

      this.room.broadcast(JSON.stringify({
        type: "message",
        message: msg
      }));
    }
  }
}
```

### Multiplayer Game State

```typescript
type Player = {
  id: string;
  x: number;
  y: number;
  name: string;
};

export default class GameServer implements Party.Server {
  players: Map<string, Player> = new Map();

  onConnect(conn: Party.Connection, ctx: Party.ConnectionContext) {
    const name = new URL(ctx.request.url).searchParams.get("name") || "Player";

    this.players.set(conn.id, {
      id: conn.id,
      x: Math.random() * 800,
      y: Math.random() * 600,
      name
    });

    // Send all players to new connection
    conn.send(JSON.stringify({
      type: "init",
      players: Object.fromEntries(this.players)
    }));

    // Notify others
    this.room.broadcast(JSON.stringify({
      type: "player-join",
      player: this.players.get(conn.id)
    }), [conn.id]);
  }

  onMessage(message: string, sender: Party.Connection) {
    const data = JSON.parse(message);

    if (data.type === "move") {
      const player = this.players.get(sender.id);
      if (player) {
        player.x = data.x;
        player.y = data.y;

        this.room.broadcast(JSON.stringify({
          type: "player-move",
          id: sender.id,
          x: data.x,
          y: data.y
        }), [sender.id]);
      }
    }
  }

  onClose(conn: Party.Connection) {
    this.players.delete(conn.id);

    this.room.broadcast(JSON.stringify({
      type: "player-leave",
      id: conn.id
    }));
  }
}
```

### Presence / Who's Online

```typescript
export default class PresenceServer implements Party.Server {
  users: Map<string, { name: string; status: string }> = new Map();

  onConnect(conn: Party.Connection, ctx: Party.ConnectionContext) {
    const url = new URL(ctx.request.url);
    const name = url.searchParams.get("name") || "Anonymous";

    this.users.set(conn.id, { name, status: "online" });
    this.broadcastPresence();
  }

  onMessage(message: string, sender: Party.Connection) {
    const data = JSON.parse(message);

    if (data.type === "status") {
      const user = this.users.get(sender.id);
      if (user) {
        user.status = data.status;
        this.broadcastPresence();
      }
    }
  }

  onClose(conn: Party.Connection) {
    this.users.delete(conn.id);
    this.broadcastPresence();
  }

  broadcastPresence() {
    this.room.broadcast(JSON.stringify({
      type: "presence",
      users: Object.fromEntries(this.users)
    }));
  }
}
```

## Best Practices

1. **Use room storage** for data that should survive hibernation
2. **Broadcast with exclusions** to avoid echo: `this.room.broadcast(msg, [sender.id])`
3. **Parse messages safely** with try/catch
4. **Clean up on disconnect** to prevent memory leaks
5. **Use connection IDs** as stable identifiers
6. **Debounce frequent updates** (e.g., cursor movements)
