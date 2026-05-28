---
name: web-realtime-sse
description: Server-Sent Events for unidirectional server-to-client streaming, EventSource API, fetch streaming, reconnection patterns, message parsing
---

# Server-Sent Events (SSE) Patterns

> **Quick Guide:** Use SSE for unidirectional server-to-client real-time updates over HTTP. Use the native EventSource API for automatic reconnection and message parsing. Use fetch streaming when you need custom headers or POST requests.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use named constants for ALL timing values - reconnect intervals, keep-alive periods, timeouts)**

**(You MUST implement proper cleanup by calling `eventSource.close()` when connections are no longer needed)**

**(You MUST use event IDs (`id:` field) to enable message recovery on reconnection)**

**(You MUST handle the `onerror` event and check `readyState` to distinguish reconnection from permanent failure)**

**(You MUST set `Content-Type: text/event-stream` and `Cache-Control: no-cache` on SSE responses — do NOT set `Connection: keep-alive` on HTTP/2+)**

</critical_requirements>

---

**Auto-detection:** SSE, Server-Sent Events, EventSource, text/event-stream, onmessage, server push, one-way streaming, real-time updates

**When to use:**

- Server-to-client real-time updates (notifications, feeds, dashboards)
- LLM/AI response streaming (token-by-token output)
- Live data feeds (stock prices, sports scores, news)
- Server push notifications without client responses needed
- Long-polling replacement with better browser support

**Key patterns covered:**

- EventSource API connection lifecycle
- Custom event types with addEventListener
- Fetch-based streaming for custom headers/POST
- SSE message parsing (data, event, id, retry fields)
- Reconnection with Last-Event-ID recovery
- Keep-alive comments to prevent proxy timeouts
- Custom React hooks (useEventSource, useSSE)

**When NOT to use:**

- Bidirectional communication needed (use WebSocket)
- Binary data transmission required (use WebSocket)
- Client needs to send frequent messages (use WebSocket)
- Sub-millisecond latency required (use WebSocket)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - React hooks (useEventSource, useSSE), shared context, conditional connection
- [examples/fetch-streaming.md](examples/fetch-streaming.md) - Fetch-based SSE, message parser, auth, POST streaming, LLM pattern
- [examples/reconnection.md](examples/reconnection.md) - Last-Event-ID recovery, exponential backoff, health checks, visibility-aware
- [reference.md](reference.md) - Decision frameworks, anti-patterns, message format reference

---

<philosophy>

## Philosophy

Server-Sent Events (SSE) provide a simple, HTTP-based protocol for servers to push real-time updates to clients. Unlike WebSockets, SSE is **unidirectional** (server to client only), built on standard HTTP, and includes automatic reconnection.

**Why SSE exists:**

1. **Simplicity:** Standard HTTP protocol - works through firewalls, proxies, and load balancers without special configuration.

2. **Built-in Reconnection:** The EventSource API automatically reconnects when connections drop, with configurable retry intervals.

3. **Message Recovery:** The `Last-Event-ID` header enables servers to replay missed messages after reconnection.

4. **Text-Based Protocol:** Human-readable format makes debugging straightforward.

**Connection Lifecycle:**

```
CONNECTING (0) → OPEN (1) → messages... → CLOSED (2)
                    ↓                         ↓
                (error) ← auto-reconnect ← (connection lost)
```

**When to Choose SSE over WebSocket:**

- Server sends updates, client only listens
- Working with HTTP/2 (multiplexing multiple SSE streams)
- Need automatic reconnection without custom logic
- Proxies/firewalls block WebSocket but allow HTTP
- Building LLM streaming interfaces

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic EventSource Connection

The native EventSource API provides automatic connection management, message parsing, and reconnection.

#### Constants

```typescript
const SSE_URL = "/api/events";
```

#### Implementation

```typescript
// ✅ Good Example - Complete lifecycle handling
const SSE_URL = "/api/events";

const eventSource = new EventSource(SSE_URL);

eventSource.onopen = () => {
  console.log("SSE connection opened");
  // Connection is ready - server can now push events
};

eventSource.onmessage = (event: MessageEvent) => {
  console.log("Received:", event.data);
  console.log("Event ID:", event.lastEventId);
};

eventSource.onerror = (error: Event) => {
  console.error("SSE error:", error);

  // Check connection state to determine action
  if (eventSource.readyState === EventSource.CLOSED) {
    console.log("Connection closed permanently");
  } else if (eventSource.readyState === EventSource.CONNECTING) {
    console.log("Reconnecting...");
  }
};

// Cleanup when done
// eventSource.close();
```

**Why good:** All three lifecycle events handled, readyState check distinguishes reconnection from permanent failure, named constant for URL, cleanup shown

```typescript
// ❌ Bad Example - Missing error handling and cleanup
const eventSource = new EventSource("/api/events");

eventSource.onmessage = (event) => {
  console.log(event.data);
};
// No onerror handler - connection failures are silent
// No cleanup - connection stays open forever
```

**Why bad:** Missing onerror means failures are silent, missing cleanup causes memory leaks and zombie connections, hardcoded URL string

---

### Pattern 2: Custom Event Types

SSE supports named events via the `event:` field. Use `addEventListener` to handle specific event types.

```typescript
// ✅ Good Example - Multiple event type handling
const SSE_URL = "/api/notifications";

const eventSource = new EventSource(SSE_URL);

// Default message event (no event: field in server response)
eventSource.onmessage = (event: MessageEvent) => {
  console.log("Generic message:", event.data);
};

// Named custom events
eventSource.addEventListener("notification", (event: MessageEvent) => {
  const notification = JSON.parse(event.data);
  showNotification(notification.title, notification.body);
});

eventSource.addEventListener("user-joined", (event: MessageEvent) => {
  const user = JSON.parse(event.data);
  updateUserList(user);
});

eventSource.addEventListener("heartbeat", (event: MessageEvent) => {
  // Keep-alive event - connection is healthy
  console.log("Heartbeat received at:", event.data);
});
```

**Why good:** Separate handlers for different event types, typed MessageEvent parameters, JSON parsing for structured data, heartbeat handling for connection health

**When to use:** When server sends multiple types of events with different handling requirements.

---

### Pattern 3: Credentials and Cross-Origin

For cross-origin requests or when cookies are required, configure `withCredentials`.

```typescript
// ✅ Good Example - Cross-origin with credentials
const SSE_URL = "https://api.example.com/events";

const eventSource = new EventSource(SSE_URL, {
  withCredentials: true, // Include cookies for cross-origin
});

eventSource.onopen = () => {
  console.log("Connected with credentials");
};

eventSource.onerror = (error) => {
  // CORS errors will trigger onerror
  console.error("Connection error - check CORS configuration");
};
```

**Why good:** withCredentials enables cookie-based authentication, CORS error handling noted

**When to use:** Cross-origin SSE connections that require authentication cookies.

---

### Pattern 4: Connection State Management

Track connection state for UI feedback and smart reconnection decisions.

#### Constants

```typescript
type SSEStatus = "connecting" | "open" | "closed" | "error";

const READY_STATE_MAP: Record<number, SSEStatus> = {
  [EventSource.CONNECTING]: "connecting",
  [EventSource.OPEN]: "open",
  [EventSource.CLOSED]: "closed",
};
```

#### Implementation

```typescript
// ✅ Good Example - State tracking class
const MAX_MANUAL_RETRIES = 5;
const RETRY_DELAY_MS = 3000;

class SSEConnection {
  private eventSource: EventSource | null = null;
  private status: SSEStatus = "closed";
  private manualRetryCount = 0;
  private onStatusChange?: (status: SSEStatus) => void;
  private onMessage?: (data: string, eventType: string) => void;

  constructor(
    private url: string,
    options?: {
      onStatusChange?: (status: SSEStatus) => void;
      onMessage?: (data: string, eventType: string) => void;
    },
  ) {
    this.onStatusChange = options?.onStatusChange;
    this.onMessage = options?.onMessage;
  }

  connect(): void {
    if (this.eventSource) {
      this.disconnect();
    }

    this.setStatus("connecting");
    this.eventSource = new EventSource(this.url);

    this.eventSource.onopen = () => {
      this.setStatus("open");
      this.manualRetryCount = 0; // Reset on successful connection
    };

    this.eventSource.onmessage = (event: MessageEvent) => {
      this.onMessage?.(event.data, "message");
    };

    this.eventSource.onerror = () => {
      if (this.eventSource?.readyState === EventSource.CLOSED) {
        this.setStatus("closed");
        // EventSource won't auto-reconnect if server sent HTTP error
        this.attemptManualReconnect();
      } else {
        this.setStatus("error");
        // EventSource is auto-reconnecting
      }
    };
  }

  private attemptManualReconnect(): void {
    if (this.manualRetryCount < MAX_MANUAL_RETRIES) {
      this.manualRetryCount++;
      console.log(`Manual reconnect attempt ${this.manualRetryCount}`);
      setTimeout(() => this.connect(), RETRY_DELAY_MS);
    }
  }

  disconnect(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
      this.setStatus("closed");
    }
  }

  private setStatus(status: SSEStatus): void {
    this.status = status;
    this.onStatusChange?.(status);
  }

  getStatus(): SSEStatus {
    return this.status;
  }
}

export { SSEConnection };
```

**Why good:** Named constants for retry values, status tracking enables UI updates, manual retry for HTTP errors (EventSource only auto-retries network errors), cleanup resets state properly

---

### Pattern 5: SSE Message Format

Messages are `\n`-separated fields terminated by `\n\n`. Five field types: `data:` (payload), `event:` (named type), `id:` (recovery ID), `retry:` (reconnect ms), `:` (comment/keep-alive).

```
event: notification
data: {"title": "New message"}
id: msg-002

: keep-alive comment (ignored by client)
```

**Key behaviors:** multiple `data:` lines concatenate with `\n`; `id:` persists until changed; `retry:` is remembered for future reconnections; comments (`:`) keep connection alive but are not delivered.

See [reference.md](reference.md) for the full field reference and behavior table.

---

### Pattern 6: Discriminated Unions for Message Types

Use TypeScript discriminated unions for type-safe message handling.

```typescript
// ✅ Good Example - Type-safe SSE message handling

// Server message types
type SSEMessage =
  | {
      type: "notification";
      title: string;
      body: string;
      priority: "low" | "high";
    }
  | { type: "user-update"; userId: string; action: "joined" | "left" }
  | { type: "data-sync"; payload: unknown; timestamp: number }
  | { type: "heartbeat"; serverTime: number };

function parseSSEMessage(data: string): SSEMessage | null {
  try {
    return JSON.parse(data) as SSEMessage;
  } catch {
    console.error("Failed to parse SSE message:", data);
    return null;
  }
}

function handleSSEMessage(message: SSEMessage): void {
  switch (message.type) {
    case "notification":
      showNotification(message.title, message.body, message.priority);
      break;
    case "user-update":
      updateUserPresence(message.userId, message.action);
      break;
    case "data-sync":
      syncData(message.payload, message.timestamp);
      break;
    case "heartbeat":
      updateServerTime(message.serverTime);
      break;
    default:
      // Exhaustiveness check
      const exhaustive: never = message;
      console.warn("Unknown message type:", exhaustive);
  }
}

// Usage with EventSource
eventSource.onmessage = (event: MessageEvent) => {
  const message = parseSSEMessage(event.data);
  if (message) {
    handleSSEMessage(message);
  }
};
```

**Why good:** Discriminated union enables type narrowing, exhaustiveness check catches missing cases at compile time, separate parse and handle functions, error handling for malformed messages

</patterns>

---

<integration>

## Integration Guide

**SSE is a transport mechanism.** This skill covers the EventSource API and fetch streaming patterns only.

- Components receive SSE data via callbacks/hooks and pass it to your UI layer via props or state
- Authentication integrates via cookies (`withCredentials: true`) or fetch streaming with custom headers
- For bidirectional communication, SSE is not the right tool — evaluate WebSocket instead

</integration>

---

<red_flags>

## RED FLAGS

- **No cleanup on unmount** - EventSource stays open, memory leaks, zombie connections
- **Ignoring onerror event** - Connection failures are silent, users see stale data
- **Not checking readyState in onerror** - Cannot distinguish reconnection from permanent failure
- **Token in URL query string** - Security risk: visible in server logs, browser history
- **Missing keep-alive comments** - Proxies may close "idle" connections after 60-120 seconds
- **JSON.parse without try-catch** - Malformed messages crash the entire handler
- **Creating new EventSource without closing old one** - Duplicate connections, duplicate messages
- **Not handling buffer boundaries in fetch streaming** - Messages split across chunks are missed

**Gotchas & Edge Cases:**

- EventSource has no timeout - dead connections may not fire onerror for minutes
- HTTP/1.1 browsers limit 6 connections per domain (SSE counts against this)
- `retry:` field is in milliseconds, not seconds
- Empty `data:\n\n` sends empty string, not undefined
- `Connection: keep-alive` header is prohibited in HTTP/2+ (Safari rejects it)

See [reference.md](reference.md) for full anti-pattern examples with code.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use named constants for ALL timing values - reconnect intervals, keep-alive periods, timeouts)**

**(You MUST implement proper cleanup by calling `eventSource.close()` when connections are no longer needed)**

**(You MUST use event IDs (`id:` field) to enable message recovery on reconnection)**

**(You MUST handle the `onerror` event and check `readyState` to distinguish reconnection from permanent failure)**

**(You MUST set `Content-Type: text/event-stream` and `Cache-Control: no-cache` on SSE responses — do NOT set `Connection: keep-alive` on HTTP/2+)**

**Failure to follow these rules will result in memory leaks, missed messages, and silent connection failures.**

</critical_reminders>
