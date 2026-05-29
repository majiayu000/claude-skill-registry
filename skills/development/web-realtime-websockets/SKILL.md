---
name: web-realtime-websockets
description: Native WebSocket API patterns, connection lifecycle, reconnection strategies, heartbeat, message typing, binary data, custom hooks
---

# WebSocket Real-Time Communication Patterns

> **Quick Guide:** Use native WebSocket API for real-time bidirectional communication. Implement exponential backoff with jitter for reconnection. Use discriminated unions for type-safe message handling. Queue messages during disconnection for delivery on reconnect.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST implement exponential backoff with jitter for ALL reconnection logic)**

**(You MUST use discriminated unions with a `type` field for ALL WebSocket message types)**

**(You MUST queue messages during disconnection and flush on reconnect)**

**(You MUST implement heartbeat/ping-pong to detect dead connections)**

**(You MUST set `binaryType` to 'arraybuffer' when handling binary data for synchronous processing)**

**(You MUST use wss:// for secure origins - modern browsers block ws:// on HTTPS pages except localhost)**

**(You MUST handle bfcache compatibility with pagehide/pageshow events for better navigation performance)**

</critical_requirements>

---

**Auto-detection:** WebSocket, ws://, wss://, onmessage, onopen, onclose, onerror, reconnect, heartbeat, ping, pong, real-time, bidirectional

**When to use:**

- Building real-time features (chat, notifications, live updates)
- Implementing bidirectional communication between client and server
- Creating live dashboards or collaborative editing features
- Streaming data updates with low latency requirements

**Key patterns covered:**

- WebSocket connection lifecycle management
- Reconnection with exponential backoff and jitter
- Heartbeat/ping-pong for connection health
- Message queuing during disconnection
- Type-safe message handling with discriminated unions
- Binary data handling (ArrayBuffer, Blob)
- Custom React hooks (useWebSocket)
- Authentication patterns

**When NOT to use:**

- One-way server-to-client streaming only (use SSE instead)
- Simple request-response patterns (use HTTP/REST instead)
- When library abstractions are required (use Socket.IO or similar)
- When automatic backpressure handling is critical (consider WebSocketStream when widely supported)

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

WebSockets provide full-duplex communication channels over a single TCP connection, enabling real-time bidirectional data flow between client and server. Unlike HTTP, WebSocket connections remain open, eliminating the overhead of repeated handshakes.

**The native WebSocket API is simple but requires careful handling:**

1. **Connection Resilience:** Networks are unreliable. Always implement reconnection with exponential backoff and jitter to prevent thundering herd problems.

2. **Connection Health:** Intermediate proxies and firewalls can silently drop idle connections. Heartbeats detect dead connections and keep connections alive.

3. **Message Integrity:** Messages sent during disconnection are lost. Queue them and flush on reconnect for reliable delivery.

4. **Type Safety:** WebSocket messages are untyped strings. Use discriminated unions with a shared `type` field for compile-time safety.

**Connection Lifecycle:**

```
CONNECTING → OPEN ↔ (messages) → CLOSING → CLOSED
                ↓                    ↓
            (error) ← reconnect ← (close)
```

5. **bfcache Compatibility:** Open WebSocket connections can prevent pages from using the browser's back/forward cache, degrading navigation performance. Close connections on `pagehide` and reconnect on `pageshow` when persisted.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic WebSocket Connection

The native WebSocket API provides four lifecycle events: `onopen`, `onmessage`, `onerror`, and `onclose`.

```typescript
// ✅ Good Example - Complete lifecycle handling
const WS_URL = "wss://api.example.com/ws";

const socket = new WebSocket(WS_URL);

socket.onopen = (event: Event) => {
  console.log("Connected to WebSocket server");
  // Connection is ready - safe to send messages
};

socket.onmessage = (event: MessageEvent) => {
  const data = JSON.parse(event.data);
  console.log("Received:", data);
};

socket.onerror = (event: Event) => {
  console.error("WebSocket error:", event);
  // Note: onerror is always followed by onclose
};

socket.onclose = (event: CloseEvent) => {
  console.log(`Connection closed: code=${event.code}, reason=${event.reason}`);
  // Implement reconnection logic here
};
```

**Why good:** All four lifecycle events handled, typed event parameters, named constant for URL, comments explain behavior

```typescript
// ❌ Bad Example - Missing error and close handling
const socket = new WebSocket("wss://api.example.com/ws");

socket.onmessage = (event) => {
  console.log(event.data);
};
```

**Why bad:** Missing onopen means messages could be sent before ready, missing onerror/onclose means connection failures are silent, hardcoded URL string

---

### Pattern 2: Exponential Backoff with Jitter

Reconnection attempts should use exponential backoff with jitter to prevent all clients from reconnecting simultaneously (thundering herd problem).

#### Constants

```typescript
const INITIAL_BACKOFF_MS = 1000;
const MAX_BACKOFF_MS = 30000;
const BACKOFF_MULTIPLIER = 2;
const MAX_RETRY_ATTEMPTS = 10;
const JITTER_FACTOR = 0.5; // 50% randomness
```

#### Implementation

```typescript
// ✅ Good Example - Exponential backoff with jitter
function calculateBackoff(attempt: number): number {
  const exponentialDelay = Math.min(
    INITIAL_BACKOFF_MS * Math.pow(BACKOFF_MULTIPLIER, attempt),
    MAX_BACKOFF_MS,
  );

  // Add jitter: random value between 50% and 150% of delay
  const jitter = exponentialDelay * JITTER_FACTOR * (Math.random() * 2 - 1);

  return Math.floor(exponentialDelay + jitter);
}

class ReconnectingWebSocket {
  private socket: WebSocket | null = null;
  private url: string;
  private retryCount = 0;
  private reconnectTimeoutId: ReturnType<typeof setTimeout> | null = null;

  constructor(url: string) {
    this.url = url;
    this.connect();
  }

  private connect(): void {
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      this.retryCount = 0; // Reset on successful connection
    };

    this.socket.onclose = (event: CloseEvent) => {
      // Don't reconnect on intentional close (code 1000)
      if (event.code !== 1000 && this.retryCount < MAX_RETRY_ATTEMPTS) {
        this.scheduleReconnect();
      }
    };
  }

  private scheduleReconnect(): void {
    const delay = calculateBackoff(this.retryCount);
    this.retryCount++;

    console.log(`Reconnecting in ${delay}ms (attempt ${this.retryCount})`);

    this.reconnectTimeoutId = setTimeout(() => {
      this.connect();
    }, delay);
  }

  public close(): void {
    if (this.reconnectTimeoutId) {
      clearTimeout(this.reconnectTimeoutId);
    }
    this.socket?.close(1000, "Client closed"); // Normal closure
  }
}
```

**Why good:** Jitter prevents thundering herd, capped maximum delay prevents excessive waits, retry limit prevents infinite loops, intentional close (code 1000) skips reconnect, timeout cleaned up on close

```typescript
// ❌ Bad Example - No backoff, no jitter
socket.onclose = () => {
  // Immediately reconnect - causes thundering herd
  new WebSocket(url);
};
```

**Why bad:** Immediate reconnection overwhelms server during outages, all clients reconnect at exact same time, no retry limit causes infinite loops

---

### Pattern 3: Heartbeat/Ping-Pong

Heartbeats detect dead connections and prevent intermediate infrastructure from closing idle connections.

```typescript
// ✅ Good Example - Client-side heartbeat implementation
const HEARTBEAT_INTERVAL_MS = 30000;
const HEARTBEAT_TIMEOUT_MS = 10000;

class HeartbeatWebSocket {
  private socket: WebSocket;
  private heartbeatIntervalId: ReturnType<typeof setInterval> | null = null;
  private heartbeatTimeoutId: ReturnType<typeof setTimeout> | null = null;
  private onConnectionLost: () => void;

  constructor(url: string, onConnectionLost: () => void) {
    this.socket = new WebSocket(url);
    this.onConnectionLost = onConnectionLost;

    this.socket.onopen = () => {
      this.startHeartbeat();
    };

    this.socket.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data);

      if (data.type === "pong") {
        this.clearHeartbeatTimeout();
        return;
      }

      // Handle other messages...
    };

    this.socket.onclose = () => {
      this.stopHeartbeat();
    };
  }

  private startHeartbeat(): void {
    this.heartbeatIntervalId = setInterval(() => {
      this.sendPing();
    }, HEARTBEAT_INTERVAL_MS);
  }

  private sendPing(): void {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type: "ping" }));

      // Set timeout for pong response
      this.heartbeatTimeoutId = setTimeout(() => {
        console.error("Heartbeat timeout - connection lost");
        this.socket.close();
        this.onConnectionLost();
      }, HEARTBEAT_TIMEOUT_MS);
    }
  }

  private clearHeartbeatTimeout(): void {
    if (this.heartbeatTimeoutId) {
      clearTimeout(this.heartbeatTimeoutId);
      this.heartbeatTimeoutId = null;
    }
  }

  private stopHeartbeat(): void {
    if (this.heartbeatIntervalId) {
      clearInterval(this.heartbeatIntervalId);
    }
    this.clearHeartbeatTimeout();
  }
}
```

**Why good:** Named constants for intervals, timeout detects dead connections, cleanup prevents memory leaks, pong handler clears timeout, readyState check prevents sending on closed socket

**When to use:** All WebSocket connections, especially those that may be idle for extended periods or pass through NATs/proxies.

---

### Pattern 4: Message Queuing During Disconnection

Messages sent during disconnection are lost. Queue them and flush when connection is restored.

```typescript
// ✅ Good Example - Message queue with flush on reconnect
const MAX_QUEUE_SIZE = 100;

interface QueuedMessage {
  data: unknown;
  timestamp: number;
}

class QueuedWebSocket {
  private socket: WebSocket | null = null;
  private messageQueue: QueuedMessage[] = [];
  private url: string;

  constructor(url: string) {
    this.url = url;
    this.connect();
  }

  private connect(): void {
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      this.flushQueue();
    };

    // ... other handlers
  }

  public send(data: unknown): void {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(data));
    } else {
      this.queueMessage(data);
    }
  }

  private queueMessage(data: unknown): void {
    if (this.messageQueue.length >= MAX_QUEUE_SIZE) {
      // Remove oldest message to make room
      this.messageQueue.shift();
      console.warn("Message queue full - dropping oldest message");
    }

    this.messageQueue.push({
      data,
      timestamp: Date.now(),
    });
  }

  private flushQueue(): void {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      if (message && this.socket?.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify(message.data));
      }
    }
  }
}
```

**Why good:** Queue has size limit to prevent memory issues, oldest messages dropped when full, flush happens on successful reconnect, readyState check before sending, timestamp allows message expiration if needed

---

### Pattern 5: Type-Safe Messages with Discriminated Unions

Use discriminated unions with a shared `type` field for compile-time type safety and exhaustive handling.

```typescript
// ✅ Good Example - Discriminated unions for message types

// Outgoing messages (client to server)
type ClientMessage =
  | { type: "subscribe"; channel: string }
  | { type: "unsubscribe"; channel: string }
  | { type: "message"; channel: string; content: string }
  | { type: "ping" };

// Incoming messages (server to client)
type ServerMessage =
  | { type: "subscribed"; channel: string; members: string[] }
  | { type: "unsubscribed"; channel: string }
  | { type: "message"; channel: string; content: string; sender: string }
  | { type: "pong" }
  | { type: "error"; code: number; message: string };

function handleServerMessage(message: ServerMessage): void {
  // TypeScript narrows the type based on the `type` field
  switch (message.type) {
    case "subscribed":
      console.log(
        `Joined ${message.channel} with ${message.members.length} members`,
      );
      break;
    case "unsubscribed":
      console.log(`Left ${message.channel}`);
      break;
    case "message":
      console.log(`${message.sender}: ${message.content}`);
      break;
    case "pong":
      // Heartbeat response - handled elsewhere
      break;
    case "error":
      console.error(`Error ${message.code}: ${message.message}`);
      break;
    default:
      // Exhaustiveness check - TypeScript error if case missing
      const exhaustiveCheck: never = message;
      console.warn("Unknown message type:", exhaustiveCheck);
  }
}

function sendMessage(socket: WebSocket, message: ClientMessage): void {
  socket.send(JSON.stringify(message));
}

// Usage - TypeScript enforces correct structure
sendMessage(socket, { type: "subscribe", channel: "general" });
sendMessage(socket, { type: "message", channel: "general", content: "Hello!" });
```

**Why good:** Discriminated union enables type narrowing in switch, exhaustiveness check catches missing cases at compile time, separate types for client/server messages, type-safe send function

```typescript
// ❌ Bad Example - Untyped message handling
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "message") {
    // No type safety - data.content could be anything
    console.log(data.content);
  }
};
```

**Why bad:** No compile-time type checking, typos in type strings not caught, missing fields cause runtime errors

---

### Pattern 6: Binary Data Handling

WebSockets support binary data via ArrayBuffer or Blob. Use ArrayBuffer for synchronous processing.

```typescript
// ✅ Good Example - Binary data with ArrayBuffer

const BINARY_HEADER_SIZE = 8; // 4 bytes type + 4 bytes length

type BinaryMessageType = 0x01 | 0x02 | 0x03;

const BinaryMessageTypes = {
  IMAGE: 0x01 as BinaryMessageType,
  AUDIO: 0x02 as BinaryMessageType,
  FILE: 0x03 as BinaryMessageType,
} as const;

class BinaryWebSocket {
  private socket: WebSocket;

  constructor(url: string) {
    this.socket = new WebSocket(url);

    // Set binaryType to arraybuffer for synchronous processing
    this.socket.binaryType = "arraybuffer";

    this.socket.onmessage = (event: MessageEvent) => {
      if (event.data instanceof ArrayBuffer) {
        this.handleBinaryMessage(event.data);
      } else {
        this.handleTextMessage(event.data);
      }
    };
  }

  private handleBinaryMessage(buffer: ArrayBuffer): void {
    const view = new DataView(buffer);

    // Read header (big-endian by default)
    const messageType = view.getUint32(0);
    const payloadLength = view.getUint32(4);

    // Extract payload
    const payload = buffer.slice(
      BINARY_HEADER_SIZE,
      BINARY_HEADER_SIZE + payloadLength,
    );

    switch (messageType) {
      case BinaryMessageTypes.IMAGE:
        this.handleImage(payload);
        break;
      case BinaryMessageTypes.AUDIO:
        this.handleAudio(payload);
        break;
      case BinaryMessageTypes.FILE:
        this.handleFile(payload);
        break;
    }
  }

  public sendBinary(type: BinaryMessageType, data: ArrayBuffer): void {
    const header = new ArrayBuffer(BINARY_HEADER_SIZE);
    const headerView = new DataView(header);

    headerView.setUint32(0, type);
    headerView.setUint32(4, data.byteLength);

    // Combine header and payload
    const message = new Uint8Array(BINARY_HEADER_SIZE + data.byteLength);
    message.set(new Uint8Array(header), 0);
    message.set(new Uint8Array(data), BINARY_HEADER_SIZE);

    this.socket.send(message);
  }

  private handleTextMessage(data: string): void {
    // Handle JSON messages
    const message = JSON.parse(data);
    // ...
  }

  private handleImage(payload: ArrayBuffer): void {
    /* ... */
  }
  private handleAudio(payload: ArrayBuffer): void {
    /* ... */
  }
  private handleFile(payload: ArrayBuffer): void {
    /* ... */
  }
}
```

**Why good:** binaryType set to arraybuffer for synchronous DataView access, header with type and length for protocol parsing, typed message types, instanceof check distinguishes binary from text

```typescript
// ❌ Bad Example - Using Blob (async only)
socket.binaryType = "blob"; // Default, but forces async handling

socket.onmessage = async (event) => {
  if (event.data instanceof Blob) {
    // Must use async API - less performant
    const buffer = await event.data.arrayBuffer();
    // Process buffer...
  }
};
```

**Why bad:** Blob requires async processing, adds latency to message handling, ArrayBuffer is synchronous and faster

---

### Pattern 7: Authentication Over WebSocket

WebSocket doesn't support custom HTTP headers. Authenticate via query string or first message after connection.

```typescript
// ✅ Good Example - Token authentication via first message

interface AuthMessage {
  type: "auth";
  token: string;
}

interface AuthResponse {
  type: "auth_result";
  success: boolean;
  error?: string;
}

class AuthenticatedWebSocket {
  private socket: WebSocket;
  private authenticated = false;
  private pendingMessages: unknown[] = [];
  private onAuthenticated: () => void;
  private onAuthError: (error: string) => void;

  constructor(
    url: string,
    token: string,
    onAuthenticated: () => void,
    onAuthError: (error: string) => void,
  ) {
    this.socket = new WebSocket(url);
    this.onAuthenticated = onAuthenticated;
    this.onAuthError = onAuthError;

    this.socket.onopen = () => {
      // Send auth token as first message
      const authMessage: AuthMessage = { type: "auth", token };
      this.socket.send(JSON.stringify(authMessage));
    };

    this.socket.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data);

      if (data.type === "auth_result") {
        this.handleAuthResult(data as AuthResponse);
        return;
      }

      if (!this.authenticated) {
        console.warn("Received message before authentication");
        return;
      }

      // Handle authenticated messages...
    };
  }

  private handleAuthResult(response: AuthResponse): void {
    if (response.success) {
      this.authenticated = true;
      this.flushPendingMessages();
      this.onAuthenticated();
    } else {
      this.onAuthError(response.error || "Authentication failed");
      this.socket.close();
    }
  }

  public send(data: unknown): void {
    if (!this.authenticated) {
      this.pendingMessages.push(data);
      return;
    }

    this.socket.send(JSON.stringify(data));
  }

  private flushPendingMessages(): void {
    while (this.pendingMessages.length > 0) {
      const message = this.pendingMessages.shift();
      this.socket.send(JSON.stringify(message));
    }
  }
}
```

**Why good:** Token sent as first message (not in URL - avoids server logs), messages queued until authenticated, auth response handled before other messages, explicit authenticated state, callbacks for success/error

```typescript
// ❌ Bad Example - Token in query string
const socket = new WebSocket(`wss://api.example.com/ws?token=${token}`);
```

**Why bad:** Token visible in server access logs, may be cached by proxies, URL length limits, harder to refresh token

---

### Pattern 8: Room/Channel Pattern

Organize connections into logical channels for targeted message delivery.

```typescript
// ✅ Good Example - Room subscription pattern

interface RoomState {
  id: string;
  members: Set<string>;
  joined: boolean;
}

class RoomWebSocket {
  private socket: WebSocket;
  private rooms: Map<string, RoomState> = new Map();
  private onRoomMessage: (roomId: string, message: unknown) => void;

  constructor(
    url: string,
    onRoomMessage: (roomId: string, message: unknown) => void,
  ) {
    this.socket = new WebSocket(url);
    this.onRoomMessage = onRoomMessage;

    this.socket.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };
  }

  public joinRoom(roomId: string): void {
    if (this.rooms.has(roomId)) {
      return; // Already in room
    }

    this.rooms.set(roomId, {
      id: roomId,
      members: new Set(),
      joined: false,
    });

    this.socket.send(
      JSON.stringify({
        type: "join_room",
        roomId,
      }),
    );
  }

  public leaveRoom(roomId: string): void {
    if (!this.rooms.has(roomId)) {
      return;
    }

    this.socket.send(
      JSON.stringify({
        type: "leave_room",
        roomId,
      }),
    );

    this.rooms.delete(roomId);
  }

  public sendToRoom(roomId: string, message: unknown): void {
    const room = this.rooms.get(roomId);
    if (!room?.joined) {
      console.warn(`Cannot send to room ${roomId} - not joined`);
      return;
    }

    this.socket.send(
      JSON.stringify({
        type: "room_message",
        roomId,
        payload: message,
      }),
    );
  }

  private handleMessage(data: unknown): void {
    const message = data as {
      type: string;
      roomId?: string;
      [key: string]: unknown;
    };

    switch (message.type) {
      case "room_joined": {
        const room = this.rooms.get(message.roomId!);
        if (room) {
          room.joined = true;
          room.members = new Set(message.members as string[]);
        }
        break;
      }
      case "room_message": {
        this.onRoomMessage(message.roomId!, message.payload);
        break;
      }
      case "member_joined": {
        const room = this.rooms.get(message.roomId!);
        room?.members.add(message.memberId as string);
        break;
      }
      case "member_left": {
        const room = this.rooms.get(message.roomId!);
        room?.members.delete(message.memberId as string);
        break;
      }
    }
  }
}
```

**Why good:** Local room state tracks membership, guards against sending to unjoined rooms, member tracking for presence, clean subscription API

</patterns>

---

<integration>

## Integration Guide

**WebSocket is transport-agnostic.** This skill covers the native WebSocket API only. Integration with specific frameworks or libraries is handled by their respective skills.

**Works with:**

- Your React framework via custom hooks (see Pattern 9 in examples/)
- Your state management solution for connection state
- Your authentication system for token management

**Defers to:**

- Backend WebSocket server implementation (backend skills)
- Socket.IO library patterns (socket-io skill if exists)
- Server-Sent Events for one-way streams (SSE skill if exists)
- State management for storing received data (state management skills)

**Alternative APIs (Future):**

- **WebSocketStream** (experimental) - Promise-based API with automatic backpressure handling via Streams API. Not widely supported yet - check browser compatibility before use.

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST implement exponential backoff with jitter for ALL reconnection logic)**

**(You MUST use discriminated unions with a `type` field for ALL WebSocket message types)**

**(You MUST queue messages during disconnection and flush on reconnect)**

**(You MUST implement heartbeat/ping-pong to detect dead connections)**

**(You MUST set `binaryType` to 'arraybuffer' when handling binary data for synchronous processing)**

**(You MUST use wss:// for secure origins - modern browsers block ws:// on HTTPS pages except localhost)**

**(You MUST close WebSocket on `pagehide` and reconnect on `pageshow` when `event.persisted` to allow bfcache)**

**Failure to follow these rules will result in connection storms, lost messages, blocked connections, and degraded navigation performance.**

</critical_reminders>
