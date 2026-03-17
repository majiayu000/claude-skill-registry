---
name: web-realtime-socket-io
description: Socket.IO v4.x client patterns, connection lifecycle, reconnection, authentication, rooms, namespaces, acknowledgments, binary data, TypeScript integration
---

# Socket.IO Real-Time Communication Patterns

> **Quick Guide:** Use Socket.IO for real-time bidirectional communication when you need rooms, namespaces, automatic reconnection, acknowledgments, or transport fallback. Socket.IO is NOT a WebSocket implementation - it adds a protocol layer with additional features.

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
- Minimal bundle size is critical (Socket.IO adds overhead)

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Socket.IO provides a layer on top of WebSocket with additional features: automatic reconnection, room-based broadcasting, acknowledgments, and transport fallback. **It is NOT a WebSocket implementation** - a plain WebSocket client cannot connect to a Socket.IO server and vice versa.

**Key Architectural Concepts:**

1. **Transport Abstraction:** Socket.IO uses WebSocket when available but falls back to HTTP long-polling for restrictive networks. This happens automatically.

2. **Rooms:** Server-side grouping mechanism for targeted broadcasting. Clients don't know about rooms - they're purely a server concept for organizing sockets.

3. **Namespaces:** Separate communication channels on the same connection. Used to separate concerns (e.g., `/chat`, `/admin`, `/notifications`).

4. **Connection State Recovery (v4.6.0+):** Missed events can be automatically delivered after brief disconnections, reducing manual state sync.

**Connection Lifecycle:**

```
CONNECTING → CONNECTED ↔ (events) → DISCONNECTING → DISCONNECTED
                ↓                        ↓
            (error) ← reconnect ← (disconnect)
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

Socket.IO v4 has first-class TypeScript support. Define interfaces for type-safe bidirectional communication.

#### Event Type Definitions

```typescript
// types/socket-events.ts

// Events sent from server to client
interface ServerToClientEvents {
  "user:joined": (user: User) => void;
  "user:left": (userId: string) => void;
  "message:received": (message: ChatMessage) => void;
  "room:updated": (room: Room) => void;
  "typing:start": (data: { userId: string; username: string }) => void;
  "typing:stop": (data: { userId: string }) => void;
  error: (error: SocketError) => void;
  pong: () => void;
}

// Events sent from client to server
interface ClientToServerEvents {
  "message:send": (
    content: string,
    callback: (response: MessageResponse) => void,
  ) => void;
  "room:join": (roomId: string, callback: (result: JoinResult) => void) => void;
  "room:leave": (roomId: string) => void;
  "typing:start": (roomId: string) => void;
  "typing:stop": (roomId: string) => void;
  ping: () => void;
}

// Supporting types
interface User {
  id: string;
  username: string;
  avatar?: string;
}

interface ChatMessage {
  id: string;
  content: string;
  senderId: string;
  roomId: string;
  createdAt: Date;
}

interface Room {
  id: string;
  name: string;
  memberCount: number;
}

interface SocketError {
  code: string;
  message: string;
}

interface MessageResponse {
  success: boolean;
  messageId?: string;
  error?: string;
}

interface JoinResult {
  success: boolean;
  room?: Room;
  error?: string;
}

export type {
  ServerToClientEvents,
  ClientToServerEvents,
  User,
  ChatMessage,
  Room,
  SocketError,
  MessageResponse,
  JoinResult,
};
```

**Why good:** Discriminated event names enable type narrowing, callback types are enforced, separate interfaces for each direction, supporting types are explicit

---

### Pattern 2: Client Configuration

Configure Socket.IO client with proper authentication, reconnection settings, and transport options.

#### Constants

```typescript
const RECONNECTION_DELAY_MS = 1000;
const RECONNECTION_DELAY_MAX_MS = 5000;
const MAX_RECONNECTION_ATTEMPTS = 10;
const REQUEST_TIMEOUT_MS = 10000;
```

#### Implementation

```typescript
// lib/socket-client.ts
import { io, Socket } from "socket.io-client";
import type {
  ServerToClientEvents,
  ClientToServerEvents,
} from "../types/socket-events";

type TypedSocket = Socket<ServerToClientEvents, ClientToServerEvents>;

interface SocketConfig {
  url: string;
  token?: string;
  autoConnect?: boolean;
}

export function createSocket(config: SocketConfig): TypedSocket {
  const socket: TypedSocket = io(config.url, {
    // Authentication - token in auth object, NOT query string
    auth: config.token ? { token: config.token } : undefined,

    // Connection settings
    autoConnect: config.autoConnect ?? false,

    // Reconnection settings
    reconnection: true,
    reconnectionAttempts: MAX_RECONNECTION_ATTEMPTS,
    reconnectionDelay: RECONNECTION_DELAY_MS,
    reconnectionDelayMax: RECONNECTION_DELAY_MAX_MS,

    // Transport settings
    transports: ["websocket", "polling"],
    upgrade: true,

    // Request timeout for emitWithAck
    timeout: REQUEST_TIMEOUT_MS,
  });

  return socket;
}

// Singleton pattern for app-wide socket
let socketInstance: TypedSocket | null = null;

export function initializeSocket(token: string): TypedSocket {
  if (socketInstance) {
    socketInstance.disconnect();
  }

  const url = process.env.NEXT_PUBLIC_SOCKET_URL ?? "http://localhost:3000";

  socketInstance = createSocket({
    url,
    token,
    autoConnect: true,
  });

  return socketInstance;
}

export function getSocket(): TypedSocket {
  if (!socketInstance) {
    throw new Error("Socket not initialized. Call initializeSocket first.");
  }
  return socketInstance;
}

export function disconnectSocket(): void {
  if (socketInstance) {
    socketInstance.disconnect();
    socketInstance = null;
  }
}
```

**Why good:** Token in auth object (not query string), named constants for all timing values, typed socket with generics, singleton pattern prevents multiple connections, explicit error for uninitialized access

```typescript
// WRONG - Token in query string (visible in logs)
const socket = io(`http://localhost:3000?token=${token}`);

// WRONG - Magic numbers
const socket = io(url, {
  reconnectionDelay: 1000,
  reconnectionAttempts: 10,
});
```

**Why bad:** Query string tokens appear in server logs and may be cached by proxies, magic numbers make configuration unclear and hard to maintain

---

### Pattern 3: Connection Lifecycle Management

Track connection state and handle reconnection events properly.

#### Constants

```typescript
const INITIAL_RECONNECT_ATTEMPTS = 0;
```

#### Implementation

```typescript
// lib/socket-lifecycle.ts
import type { Socket } from "socket.io-client";

interface ConnectionState {
  isConnected: boolean;
  isReconnecting: boolean;
  reconnectAttempts: number;
  lastError: Error | null;
  recovered: boolean;
}

type StateChangeCallback = (state: ConnectionState) => void;

export function setupConnectionLifecycle(
  socket: Socket,
  onStateChange: StateChangeCallback,
): () => void {
  const state: ConnectionState = {
    isConnected: socket.connected,
    isReconnecting: false,
    reconnectAttempts: INITIAL_RECONNECT_ATTEMPTS,
    lastError: null,
    recovered: false,
  };

  const updateState = (updates: Partial<ConnectionState>): void => {
    Object.assign(state, updates);
    onStateChange({ ...state });
  };

  // Connection established
  const handleConnect = (): void => {
    updateState({
      isConnected: true,
      isReconnecting: false,
      reconnectAttempts: INITIAL_RECONNECT_ATTEMPTS,
      lastError: null,
      recovered: socket.recovered ?? false,
    });
  };

  // Connection lost
  const handleDisconnect = (reason: string): void => {
    const willReconnect = socket.active;
    updateState({
      isConnected: false,
      isReconnecting: willReconnect,
      recovered: false,
    });

    // Log for debugging
    if (!willReconnect) {
      console.log("Connection closed permanently:", reason);
    }
  };

  // Connection error
  const handleConnectError = (error: Error): void => {
    updateState({
      isConnected: false,
      lastError: error,
    });
  };

  // Manager-level events for reconnection tracking
  const handleReconnectAttempt = (attempt: number): void => {
    updateState({
      isReconnecting: true,
      reconnectAttempts: attempt,
    });
  };

  const handleReconnect = (): void => {
    updateState({
      isConnected: true,
      isReconnecting: false,
      reconnectAttempts: INITIAL_RECONNECT_ATTEMPTS,
    });
  };

  const handleReconnectFailed = (): void => {
    updateState({
      isReconnecting: false,
      lastError: new Error("Max reconnection attempts reached"),
    });
  };

  // Socket-level events
  socket.on("connect", handleConnect);
  socket.on("disconnect", handleDisconnect);
  socket.on("connect_error", handleConnectError);

  // Manager-level events (socket.io property is the Manager)
  socket.io.on("reconnect_attempt", handleReconnectAttempt);
  socket.io.on("reconnect", handleReconnect);
  socket.io.on("reconnect_failed", handleReconnectFailed);

  // Return cleanup function
  return () => {
    socket.off("connect", handleConnect);
    socket.off("disconnect", handleDisconnect);
    socket.off("connect_error", handleConnectError);
    socket.io.off("reconnect_attempt", handleReconnectAttempt);
    socket.io.off("reconnect", handleReconnect);
    socket.io.off("reconnect_failed", handleReconnectFailed);
  };
}
```

**Why good:** Distinguishes socket-level vs manager-level events, tracks recovery state for v4.6.0+, returns cleanup function for React integration, state updates are immutable

---

### Pattern 4: Acknowledgments with Timeout and Retries

Use acknowledgments to confirm message delivery with timeout handling. Socket.IO v4.6.0+ adds automatic retry support.

#### Constants

```typescript
const ACK_TIMEOUT_MS = 5000;
const DEFAULT_TIMEOUT_MS = 10000;
const MAX_RETRIES = 3;
```

#### Automatic Retries (v4.6.0+)

```typescript
// Configure socket with automatic retries
const socket = io(url, {
  ackTimeout: ACK_TIMEOUT_MS, // Timeout per attempt
  retries: MAX_RETRIES, // Max retry attempts
});

// Events are automatically retried on timeout
socket.emit("message:send", content, (response) => {
  // Will be retried up to MAX_RETRIES times if no ack received
  console.log("Message confirmed:", response);
});
```

**Why good:** Automatic retry handling reduces boilerplate, consistent timeout behavior across all emits, server must be idempotent for retried packets

#### Manual Implementation

```typescript
// lib/socket-utils.ts
import type { Socket } from "socket.io-client";

// Callback-based acknowledgment
export function emitWithCallback<T>(
  socket: Socket,
  event: string,
  data: unknown,
  callback: (response: T) => void,
): void {
  socket.emit(event, data, callback);
}

// Promise-based acknowledgment with timeout
export async function emitWithTimeout<T>(
  socket: Socket,
  event: string,
  data: unknown,
  timeoutMs: number = DEFAULT_TIMEOUT_MS,
): Promise<T> {
  try {
    const response = await socket.timeout(timeoutMs).emitWithAck(event, data);
    return response as T;
  } catch (error) {
    if ((error as Error).message?.includes("timeout")) {
      throw new Error(`Request timed out after ${timeoutMs}ms`);
    }
    throw error;
  }
}

// Usage example
async function sendMessage(
  socket: Socket,
  content: string,
): Promise<MessageResponse> {
  return emitWithTimeout<MessageResponse>(
    socket,
    "message:send",
    content,
    ACK_TIMEOUT_MS,
  );
}
```

**Why good:** Two patterns for different use cases (callback vs Promise), explicit timeout handling, named constants for timeout values, typed response generic

---

### Pattern 5: Connection State Recovery

Leverage Socket.IO v4.6.0+ connection state recovery to handle brief disconnections gracefully.

```typescript
// lib/socket-recovery.ts
import type { Socket } from "socket.io-client";

interface RecoveryHandler {
  onRecovered: () => void;
  onNewSession: () => void;
}

export function setupRecoveryHandler(
  socket: Socket,
  handlers: RecoveryHandler,
): () => void {
  const handleConnect = (): void => {
    if (socket.recovered) {
      // Connection recovered - missed events will be delivered automatically
      // No need to re-fetch initial state
      console.log("Connection recovered, state restored");
      handlers.onRecovered();
    } else {
      // New session or recovery failed
      // Need to re-sync state from server
      console.log("New session, fetching initial state...");
      handlers.onNewSession();
    }
  };

  socket.on("connect", handleConnect);

  return () => {
    socket.off("connect", handleConnect);
  };
}

// Usage with initial data fetch
function setupWithRecovery(
  socket: Socket,
  fetchInitialState: () => void,
): void {
  setupRecoveryHandler(socket, {
    onRecovered: () => {
      // Missed events delivered automatically - just update UI
      console.log("Session recovered, no refetch needed");
    },
    onNewSession: () => {
      // Need full state sync
      fetchInitialState();
    },
  });
}
```

**Why good:** Differentiates recovered vs new sessions, prevents unnecessary refetches after brief disconnections, cleanup function for React

---

### Pattern 6: Sending and Receiving Binary Data

Socket.IO automatically handles binary data including Buffer, ArrayBuffer, and Blob.

#### Constants

```typescript
const BINARY_CHUNK_SIZE = 64 * 1024; // 64KB chunks
```

#### Implementation

```typescript
// lib/binary-transfer.ts

interface FileMetadata {
  name: string;
  type: string;
  size: number;
}

interface UploadResponse {
  success: boolean;
  fileId?: string;
  error?: string;
}

// Sending binary data
export function sendFile(
  socket: Socket,
  file: File,
  onProgress?: (percent: number) => void,
): Promise<UploadResponse> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = () => {
      const arrayBuffer = reader.result as ArrayBuffer;
      const metadata: FileMetadata = {
        name: file.name,
        type: file.type,
        size: file.size,
      };

      // Socket.IO handles ArrayBuffer automatically
      socket.emit(
        "file:upload",
        arrayBuffer,
        metadata,
        (response: UploadResponse) => {
          if (response.success) {
            resolve(response);
          } else {
            reject(new Error(response.error ?? "Upload failed"));
          }
        },
      );
    };

    reader.onerror = () => reject(reader.error);
    reader.readAsArrayBuffer(file);
  });
}

// Receiving binary data
export function setupBinaryReceiver(
  socket: Socket,
  onFileReceived: (data: ArrayBuffer, metadata: FileMetadata) => void,
): () => void {
  const handler = (data: ArrayBuffer, metadata: FileMetadata): void => {
    onFileReceived(data, metadata);
  };

  socket.on("file:received", handler);

  return () => {
    socket.off("file:received", handler);
  };
}
```

**Why good:** Socket.IO handles binary serialization automatically, metadata travels with file data, callback confirms delivery, cleanup function returned

</patterns>

---

<integration>

## Integration Guide

**Socket.IO is a transport solution.** This skill covers Socket.IO client patterns only.

**Works with:**

- Your React framework via custom hooks (see examples/core.md)
- Your state management solution for connection state tracking
- Your authentication system for token management

**Defers to:**

- Backend Socket.IO server implementation (backend skills)
- Native WebSocket patterns (websockets skill)
- State management for storing received data (state management skills)

</integration>

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
