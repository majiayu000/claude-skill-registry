---
name: web-realtime-socket-io
description: Socket.IO v4.x client patterns, connection lifecycle, reconnection, authentication, rooms, namespaces, acknowledgments, binary data, TypeScript integration
---

# Socket.IO Real-Time Communication Patterns

> **Quick Guide:** Use Socket.IO for real-time bidirectional communication when you need rooms, namespaces, automatic reconnection, acknowledgments, or transport fallback. Socket.IO is NOT a WebSocket implementation - it adds a protocol layer with additional features. Always define typed event interfaces, use the `auth` option for tokens (never query strings), and clean up listeners on unmount.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define typed interfaces for ALL Socket.IO events - ServerToClientEvents and ClientToServerEvents)**

**(You MUST use the `auth` option for authentication tokens - NEVER pass tokens in query strings)**

**(You MUST clean up event listeners on component unmount using socket.off())**

**(You MUST handle connection errors and implement proper reconnection state management)**

**(You MUST use named constants for all timeout values, retry limits, and intervals)**

</critical_requirements>

---

**Auto-detection:** Socket.IO, socket.io-client, io(), useSocket, socket.emit, socket.on, rooms, namespaces, acknowledgments, real-time

**When to use:**

- Building real-time features requiring rooms or namespaces (chat, multiplayer)
- Need automatic reconnection with connection state recovery
- Need acknowledgments/callbacks for message delivery confirmation
- Building applications that must work in restrictive network environments (fallback transports)
- Need server-side broadcasting patterns (emit to room, namespace, all clients)

**Key patterns covered:**

- TypeScript event interfaces (ServerToClientEvents, ClientToServerEvents)
- Client connection configuration and lifecycle
- Authentication via auth option and middleware
- Rooms and namespaces for logical grouping
- Acknowledgments and callbacks
- Connection state recovery (v4.6.0+)
- React integration hooks

**When NOT to use:**

- Simple WebSocket needs without rooms/namespaces (use native WebSocket)
- Need to connect to non-Socket.IO WebSocket servers (incompatible protocols)
- Minimal bundle size is critical (Socket.IO adds ~14.5KB gzipped overhead)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Socket factory, React hooks, event listeners, message queue, typing indicators, volatile events, namespace multiplexing
- [examples/authentication.md](examples/authentication.md) - Token auth, cookie auth, token refresh, namespace auth, auth state machine
- [examples/rooms.md](examples/rooms.md) - Room manager, room hooks, multi-room chat, namespace sockets, conditional namespace access
- [reference.md](reference.md) - Decision frameworks, client options reference, checklists

---

<philosophy>

## Philosophy

Socket.IO provides a layer on top of WebSocket with additional features: automatic reconnection, room-based broadcasting, acknowledgments, and transport fallback. **It is NOT a WebSocket implementation** - a plain WebSocket client cannot connect to a Socket.IO server and vice versa.

**Key Architectural Concepts:**

1. **Transport Abstraction:** Socket.IO uses WebSocket when available but falls back to HTTP long-polling for restrictive networks. Default order: polling first, then upgrade to WebSocket.

2. **Rooms:** Server-side grouping mechanism for targeted broadcasting. Clients don't know about rooms - they're purely a server concept for organizing sockets.

3. **Namespaces:** Separate communication channels on the same connection. Used to separate concerns (e.g., `/chat`, `/admin`, `/notifications`). Each can have its own middleware.

4. **Connection State Recovery (v4.6.0+):** Missed events can be automatically delivered after brief disconnections, reducing manual state sync. Server-configurable with 2-minute default window.

**Connection Lifecycle:**

```
CONNECTING -> CONNECTED <-> (events) -> DISCONNECTING -> DISCONNECTED
                 |                           |
             (error) <- reconnect <- (disconnect)
```

**Socket.IO vs Native WebSocket:**

| Feature            | Socket.IO             | Native WebSocket     |
| ------------------ | --------------------- | -------------------- |
| Transport fallback | Automatic             | Manual               |
| Reconnection       | Built-in              | Manual               |
| Rooms              | Built-in              | Manual (server-side) |
| Namespaces         | Built-in              | Not available        |
| Acknowledgments    | Built-in              | Manual               |
| Protocol           | Custom (incompatible) | Standard WebSocket   |
| Bundle size        | ~14.5KB gzipped       | Native (0KB)         |

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: TypeScript Event Interfaces

Define separate interfaces for each communication direction. Socket.IO v4 enforces these at compile time.

```typescript
interface ServerToClientEvents {
  "message:received": (message: ChatMessage) => void;
  "user:joined": (user: User) => void;
  error: (error: SocketError) => void;
}

interface ClientToServerEvents {
  "message:send": (
    content: string,
    callback: (res: MessageResponse) => void,
  ) => void;
  "room:join": (roomId: string, callback: (result: JoinResult) => void) => void;
}

type TypedSocket = Socket<ServerToClientEvents, ClientToServerEvents>;
```

**Why this matters:** Without typed events, typos in event names fail silently at runtime. Typed interfaces catch `"mesage"` vs `"message"` at compile time.

See [examples/core.md](examples/core.md) Example 1 for complete type definitions.

---

### Pattern 2: Client Configuration

Token goes in `auth` object (never query string). Use named constants for all timing values. The `timeout` option controls the **connection** timeout (default 20000ms). For acknowledgment timeouts, use `ackTimeout` (v4.6.0+) or `socket.timeout(ms).emitWithAck()`.

```typescript
const RECONNECTION_DELAY_MS = 1000;
const MAX_RECONNECTION_ATTEMPTS = 10;
const CONNECTION_TIMEOUT_MS = 20000;

const socket: TypedSocket = io(url, {
  auth: { token }, // NOT in query string
  reconnectionAttempts: MAX_RECONNECTION_ATTEMPTS,
  reconnectionDelay: RECONNECTION_DELAY_MS,
  timeout: CONNECTION_TIMEOUT_MS, // Connection timeout
  transports: ["websocket", "polling"],
});
```

**Key distinction:** `timeout` = connection timeout. `ackTimeout` = per-emit acknowledgment timeout (requires `retries` option, v4.6.0+).

See [examples/core.md](examples/core.md) Example 1 for full factory implementation.

---

### Pattern 3: Connection Lifecycle

Socket-level events (`connect`, `disconnect`, `connect_error`) track the socket. Manager-level events (`reconnect_attempt`, `reconnect`, `reconnect_failed`) track the underlying connection. Always listen to both.

```typescript
socket.on("connect", () => {
  /* connected */
});
socket.on("disconnect", (reason) => {
  // socket.active === true means it will reconnect
});
socket.on("connect_error", (error) => {
  /* handle */
});

// Manager-level: socket.io is the Manager instance
socket.io.on("reconnect_attempt", (attempt) => {
  /* show UI */
});
socket.io.on("reconnect_failed", () => {
  /* all attempts exhausted */
});
```

**Critical:** Check `socket.recovered` (v4.6.0+) after `connect` to determine if missed events were automatically delivered or if you need a full state refresh.

See [examples/core.md](examples/core.md) Examples 2-3 for React hooks.

---

### Pattern 4: Acknowledgments

Two approaches: automatic retries (v4.6.0+) or manual `emitWithAck`. Both confirm message delivery.

```typescript
// Automatic retries (v4.6.0+)
const socket = io(url, { ackTimeout: 5000, retries: 3 });
socket.emit("message:send", content, (response) => {
  /* confirmed */
});

// Manual with emitWithAck
const response = await socket
  .timeout(5000)
  .emitWithAck("message:send", content);
```

**Gotcha:** When using automatic retries, server handlers must be **idempotent** since the same packet may arrive multiple times.

See [examples/core.md](examples/core.md) Example 4 for the emit hook pattern.

---

### Pattern 5: Auth Token Handling

The `auth` option can be an object (evaluated once) or a **function** (called on every connection/reconnection). Use the function form to ensure fresh tokens on reconnect.

```typescript
// Static (stale on reconnect)
const socket = io(url, { auth: { token } });

// Dynamic (fresh on every connection attempt)
const socket = io(url, {
  auth: (cb) => {
    cb({ token: getToken() });
  },
});

// Or update before reconnection
socket.io.on("reconnect_attempt", () => {
  socket.auth = { token: getToken() };
});
```

See [examples/authentication.md](examples/authentication.md) for full auth patterns, token refresh, and auth state machine.

---

### Pattern 6: Rooms and Namespaces

**Rooms** are server-side only - clients request to join, server decides. **Namespaces** are protocol-level - clients connect explicitly. Multiple namespace sockets share one underlying connection via the Manager.

```typescript
// Namespaces: use Manager for connection sharing
const manager = new Manager(url, { autoConnect: false });
const chatSocket = manager.socket("/chat");
const adminSocket = manager.socket("/admin", {
  auth: { token: adminToken }, // Per-namespace auth
});
manager.connect();
```

See [examples/rooms.md](examples/rooms.md) for room manager, room hooks, and namespace patterns.

---

### Pattern 7: Listener Cleanup

Every `socket.on()` must have a corresponding `socket.off()`. In React, return cleanup from `useEffect`. Pass the exact same function reference to `off()`.

```typescript
useEffect(() => {
  const handler = (msg: Message) => setMessages((prev) => [...prev, msg]);
  socket.on("message", handler);
  return () => {
    socket.off("message", handler);
  }; // Same reference
}, [socket]);
```

**Why this matters:** Without cleanup, handlers accumulate on re-renders causing memory leaks and duplicate processing.

</patterns>

---

<red_flags>

## RED FLAGS

- **Token in query string** - Visible in server logs, browser history, proxy logs. Always use `auth` option.
- **No event type definitions** - Typos in event names fail silently. Define `ServerToClientEvents`/`ClientToServerEvents`.
- **Missing socket.off() cleanup** - Memory leaks and duplicate handlers accumulate.
- **No connection error handling** - Users see blank screens with no feedback on failures.
- **Using socket.id as user identifier** - Changes on every reconnection. Use server-provided user ID.
- **Sending without connected check** - `socket.emit()` on a disconnected socket fails silently. Check `socket.connected` or queue messages.
- **Confusing `timeout` with `ackTimeout`** - `timeout` is connection timeout (default 20000ms). `ackTimeout` is acknowledgment timeout (v4.6.0+, requires `retries`).
- **Static auth with long sessions** - Token expires, reconnection fails. Use `auth` as a function or update on `reconnect_attempt`.

**Gotchas:**

- Socket.IO protocol is **incompatible** with plain WebSocket - they cannot interoperate
- Default transport order is polling-first, then upgrade to WebSocket (not WebSocket-first)
- `socket.recovered` only works when server has connection state recovery enabled (v4.6.0+)
- Namespaces share one WebSocket connection - a transport failure affects all namespaces
- Rooms are purely server-side - the client never knows which rooms it belongs to
- `volatile.emit()` may silently drop messages - only use for expendable data (cursor positions)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST define typed interfaces for ALL Socket.IO events - ServerToClientEvents and ClientToServerEvents)**

**(You MUST use the `auth` option for authentication tokens - NEVER pass tokens in query strings)**

**(You MUST clean up event listeners on component unmount using socket.off())**

**(You MUST handle connection errors and implement proper reconnection state management)**

**(You MUST use named constants for all timeout values, retry limits, and intervals)**

**Failure to follow these rules will result in security vulnerabilities, memory leaks, and type-unsafe code.**

</critical_reminders>
