---
name: WebSocket Bug Finder
description: Test WebSocket connections for reliability including reconnection logic, message ordering, heartbeat mechanisms, and connection state management under adverse conditions
version: 1.0.0
author: Pramod
license: MIT
tags: [websocket, real-time, connection-testing, reconnection, message-ordering, heartbeat, socket-testing, ws]
testingTypes: [integration, e2e]
frameworks: [playwright]
languages: [typescript, javascript]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# WebSocket Bug Finder Skill

You are an expert QA automation engineer specializing in WebSocket and real-time communication testing. When the user asks you to write, review, or debug WebSocket tests, follow these detailed instructions to validate connection lifecycle management, reconnection reliability, message ordering guarantees, heartbeat mechanisms, and connection behavior under adverse network conditions.

## Core Principles

1. **Connections are ephemeral** -- WebSocket connections will drop unexpectedly due to network changes, server restarts, load balancer timeouts, and mobile device sleep. Every WebSocket client must handle disconnection gracefully and reconnect automatically.
2. **Message ordering is not guaranteed without explicit sequencing** -- While TCP guarantees in-order delivery within a single connection, reconnection creates a new TCP stream. Messages sent during reconnection may arrive out of order. Test that applications handle sequence gaps correctly.
3. **Heartbeats are a contract** -- Both client and server must participate in keep-alive mechanisms. Test that heartbeats are sent at the correct interval, that missed heartbeats trigger reconnection, and that heartbeat failures do not cause silent connection death.
4. **Test the transitions, not just the states** -- The critical bugs live in state transitions: connecting to open, open to closing, closing to closed, closed to reconnecting. Test every transition path, especially the error paths.
5. **Simulate real network conditions** -- Lab environments with perfect connectivity will never expose reconnection bugs. Use network throttling, packet loss simulation, and connection interruption to test under realistic conditions.
6. **Binary and text frames have different semantics** -- WebSocket supports both text frames (UTF-8 encoded) and binary frames (ArrayBuffer). Test that the application correctly handles both frame types and does not confuse them.
7. **Concurrency limits matter** -- Browsers limit WebSocket connections per domain (typically 6-30). Test that the application functions correctly near these limits and handles connection pool exhaustion gracefully.

## Project Structure

Organize WebSocket testing projects with this structure:

```
tests/
  websocket/
    connection/
      lifecycle.spec.ts
      reconnection.spec.ts
      authentication.spec.ts
      concurrent-connections.spec.ts
    messaging/
      ordering.spec.ts
      delivery-guarantee.spec.ts
      binary-messages.spec.ts
      large-payloads.spec.ts
    heartbeat/
      ping-pong.spec.ts
      timeout-detection.spec.ts
      keep-alive.spec.ts
    resilience/
      network-disruption.spec.ts
      server-restart.spec.ts
      backpressure.spec.ts
    e2e/
      real-time-updates.spec.ts
      collaborative-editing.spec.ts
      chat-messaging.spec.ts
  helpers/
    ws-test-client.ts
    ws-message-recorder.ts
    network-simulator.ts
    ws-server-mock.ts
  fixtures/
    websocket.fixture.ts
  config/
    ws-test-config.ts
playwright.config.ts
```

## WebSocket Connection Lifecycle Testing

### Test Client Helper

```typescript
// helpers/ws-test-client.ts
import WebSocket from 'ws';
import { EventEmitter } from 'events';

interface WSMessage {
  data: string | Buffer;
  timestamp: number;
  type: 'text' | 'binary';
  sequence?: number;
}

interface ConnectionEvent {
  type: 'open' | 'close' | 'error' | 'message' | 'reconnect';
  timestamp: number;
  details?: unknown;
}

export class WSTestClient extends EventEmitter {
  private ws: WebSocket | null = null;
  private url: string;
  private messages: WSMessage[] = [];
  private events: ConnectionEvent[] = [];
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private shouldReconnect = true;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private heartbeatTimeout: NodeJS.Timeout | null = null;
  private headers: Record<string, string>;

  constructor(
    url: string,
    options: {
      headers?: Record<string, string>;
      maxReconnectAttempts?: number;
      reconnectDelay?: number;
    } = {}
  ) {
    super();
    this.url = url;
    this.headers = options.headers || {};
    this.maxReconnectAttempts = options.maxReconnectAttempts ?? 5;
    this.reconnectDelay = options.reconnectDelay ?? 1000;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url, { headers: this.headers });

      this.ws.on('open', () => {
        this.reconnectAttempts = 0;
        this.recordEvent('open');
        this.emit('open');
        resolve();
      });

      this.ws.on('message', (data: WebSocket.Data) => {
        const message: WSMessage = {
          data: data instanceof Buffer ? data : data.toString(),
          timestamp: Date.now(),
          type: data instanceof Buffer ? 'binary' : 'text',
        };

        // Extract sequence number if present
        if (typeof message.data === 'string') {
          try {
            const parsed = JSON.parse(message.data);
            if (parsed.seq !== undefined) {
              message.sequence = parsed.seq;
            }
          } catch {
            // Not JSON, that is fine
          }
        }

        this.messages.push(message);
        this.recordEvent('message', message);
        this.emit('message', message);
      });

      this.ws.on('close', (code, reason) => {
        this.recordEvent('close', { code, reason: reason.toString() });
        this.emit('close', code, reason);
        this.stopHeartbeat();

        if (this.shouldReconnect && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.attemptReconnect();
        }
      });

      this.ws.on('error', (error) => {
        this.recordEvent('error', { message: error.message });
        this.emit('error', error);
        reject(error);
      });
    });
  }

  private async attemptReconnect(): Promise<void> {
    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    this.recordEvent('reconnect', { attempt: this.reconnectAttempts, delay });

    await new Promise((resolve) => setTimeout(resolve, delay));

    try {
      await this.connect();
    } catch {
      // Reconnect failed, will retry if under max attempts
    }
  }

  send(data: string | Buffer): void {
    if (this.ws?.readyState !== WebSocket.OPEN) {
      throw new Error(`Cannot send: WebSocket is ${this.getStateName()}`);
    }
    this.ws.send(data);
  }

  startHeartbeat(intervalMs: number = 30000, timeoutMs: number = 5000): void {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.ping();

        this.heartbeatTimeout = setTimeout(() => {
          // No pong received within timeout
          this.emit('heartbeat-timeout');
          this.ws?.terminate();
        }, timeoutMs);
      }
    }, intervalMs);

    this.ws?.on('pong', () => {
      if (this.heartbeatTimeout) {
        clearTimeout(this.heartbeatTimeout);
        this.heartbeatTimeout = null;
      }
      this.emit('pong');
    });
  }

  stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
    if (this.heartbeatTimeout) {
      clearTimeout(this.heartbeatTimeout);
      this.heartbeatTimeout = null;
    }
  }

  close(code: number = 1000, reason: string = 'Test complete'): void {
    this.shouldReconnect = false;
    this.stopHeartbeat();
    this.ws?.close(code, reason);
  }

  getMessages(): WSMessage[] {
    return [...this.messages];
  }

  getEvents(): ConnectionEvent[] {
    return [...this.events];
  }

  getState(): number {
    return this.ws?.readyState ?? WebSocket.CLOSED;
  }

  getStateName(): string {
    const states: Record<number, string> = {
      [WebSocket.CONNECTING]: 'CONNECTING',
      [WebSocket.OPEN]: 'OPEN',
      [WebSocket.CLOSING]: 'CLOSING',
      [WebSocket.CLOSED]: 'CLOSED',
    };
    return states[this.getState()] || 'UNKNOWN';
  }

  getReconnectAttempts(): number {
    return this.reconnectAttempts;
  }

  clearMessages(): void {
    this.messages = [];
  }

  private recordEvent(type: ConnectionEvent['type'], details?: unknown): void {
    this.events.push({ type, timestamp: Date.now(), details });
  }
}
```

### Connection Lifecycle Tests

```typescript
// tests/websocket/connection/lifecycle.spec.ts
import { describe, test, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { WSTestClient } from '../../helpers/ws-test-client';
import { WebSocketServer, WebSocket } from 'ws';

let wss: WebSocketServer;
const PORT = 8765;
const WS_URL = `ws://localhost:${PORT}`;

beforeAll(() => {
  wss = new WebSocketServer({ port: PORT });
  wss.on('connection', (ws) => {
    ws.on('message', (data) => {
      // Echo messages back
      ws.send(data);
    });
  });
});

afterAll(() => {
  wss.close();
});

describe('WebSocket Connection Lifecycle', () => {
  let client: WSTestClient;

  afterEach(() => {
    client?.close();
  });

  test('should establish connection and reach OPEN state', async () => {
    client = new WSTestClient(WS_URL);
    await client.connect();

    expect(client.getState()).toBe(WebSocket.OPEN);
    expect(client.getStateName()).toBe('OPEN');

    const events = client.getEvents();
    expect(events[0].type).toBe('open');
  });

  test('should perform clean close with code 1000', async () => {
    client = new WSTestClient(WS_URL);
    await client.connect();

    const closePromise = new Promise<{ code: number; reason: Buffer }>((resolve) => {
      client.on('close', (code, reason) => resolve({ code, reason }));
    });

    client.close(1000, 'Normal closure');
    const result = await closePromise;

    expect(result.code).toBe(1000);
    expect(client.getState()).toBe(WebSocket.CLOSED);
  });

  test('should record all lifecycle events in order', async () => {
    client = new WSTestClient(WS_URL);
    await client.connect();

    client.send('test message');

    // Wait for echo
    await new Promise<void>((resolve) => {
      client.on('message', () => resolve());
    });

    client.close();

    await new Promise<void>((resolve) => {
      client.on('close', () => resolve());
    });

    const events = client.getEvents();
    const eventTypes = events.map((e) => e.type);

    expect(eventTypes[0]).toBe('open');
    expect(eventTypes).toContain('message');
    expect(eventTypes[eventTypes.length - 1]).toBe('close');

    // Events should be in chronological order
    for (let i = 1; i < events.length; i++) {
      expect(events[i].timestamp).toBeGreaterThanOrEqual(events[i - 1].timestamp);
    }
  });

  test('should handle server-initiated close', async () => {
    client = new WSTestClient(WS_URL, { maxReconnectAttempts: 0 });
    await client.connect();

    const closePromise = new Promise<number>((resolve) => {
      client.on('close', (code) => resolve(code));
    });

    // Close from server side
    wss.clients.forEach((ws) => {
      ws.close(1001, 'Server going away');
    });

    const code = await closePromise;
    expect(code).toBe(1001);
  });

  test('should reject connection to invalid URL', async () => {
    client = new WSTestClient('ws://localhost:9999', { maxReconnectAttempts: 0 });

    await expect(client.connect()).rejects.toThrow();
    expect(client.getState()).toBe(WebSocket.CLOSED);
  });
});
```

## Reconnection Logic Verification

```typescript
// tests/websocket/connection/reconnection.spec.ts
import { describe, test, expect, afterEach } from 'vitest';
import { WSTestClient } from '../../helpers/ws-test-client';
import { WebSocketServer, WebSocket } from 'ws';

describe('WebSocket Reconnection', () => {
  let wss: WebSocketServer;
  let client: WSTestClient;
  const PORT = 8766;

  afterEach(() => {
    client?.close();
    wss?.close();
  });

  test('should automatically reconnect after server disconnect', async () => {
    wss = new WebSocketServer({ port: PORT });

    client = new WSTestClient(`ws://localhost:${PORT}`, {
      maxReconnectAttempts: 3,
      reconnectDelay: 100,
    });

    await client.connect();
    expect(client.getState()).toBe(WebSocket.OPEN);

    // Track reconnection
    const reconnectPromise = new Promise<void>((resolve) => {
      client.on('open', () => resolve());
    });

    // Force disconnect from server side
    wss.clients.forEach((ws) => ws.terminate());

    // Wait for reconnection
    await reconnectPromise;
    expect(client.getState()).toBe(WebSocket.OPEN);
    expect(client.getReconnectAttempts()).toBeGreaterThanOrEqual(1);
  });

  test('should use exponential backoff for reconnection attempts', async () => {
    // Start server, connect, then stop server to force reconnect failures
    wss = new WebSocketServer({ port: PORT });

    client = new WSTestClient(`ws://localhost:${PORT}`, {
      maxReconnectAttempts: 4,
      reconnectDelay: 100,
    });

    await client.connect();

    // Close server to prevent reconnection
    wss.close();

    // Force disconnect
    client['ws']?.terminate();

    // Wait for all reconnection attempts to fail
    await new Promise((resolve) => setTimeout(resolve, 5000));

    const events = client.getEvents().filter((e) => e.type === 'reconnect');

    // Verify exponential backoff pattern
    for (let i = 1; i < events.length; i++) {
      const prevDelay = (events[i - 1].details as { delay: number }).delay;
      const currDelay = (events[i].details as { delay: number }).delay;
      expect(currDelay).toBeGreaterThanOrEqual(prevDelay);
    }
  });

  test('should stop reconnecting after max attempts', async () => {
    const maxAttempts = 3;

    wss = new WebSocketServer({ port: PORT });
    client = new WSTestClient(`ws://localhost:${PORT}`, {
      maxReconnectAttempts: maxAttempts,
      reconnectDelay: 50,
    });

    await client.connect();
    wss.close();
    client['ws']?.terminate();

    // Wait for all attempts to exhaust
    await new Promise((resolve) => setTimeout(resolve, 3000));

    const reconnectEvents = client.getEvents().filter((e) => e.type === 'reconnect');
    expect(reconnectEvents.length).toBeLessThanOrEqual(maxAttempts);
  });

  test('should reset reconnect counter after successful connection', async () => {
    wss = new WebSocketServer({ port: PORT });
    client = new WSTestClient(`ws://localhost:${PORT}`, {
      maxReconnectAttempts: 5,
      reconnectDelay: 100,
    });

    await client.connect();

    // First disconnect and reconnect
    const firstReconnect = new Promise<void>((resolve) => {
      client.once('open', () => resolve());
    });
    wss.clients.forEach((ws) => ws.terminate());
    await firstReconnect;

    // After successful reconnect, counter should reset
    expect(client.getReconnectAttempts()).toBe(0);

    // Second disconnect and reconnect should also work
    const secondReconnect = new Promise<void>((resolve) => {
      client.once('open', () => resolve());
    });
    wss.clients.forEach((ws) => ws.terminate());
    await secondReconnect;

    expect(client.getState()).toBe(WebSocket.OPEN);
  });
});
```

## Message Ordering and Delivery Guarantees

```typescript
// tests/websocket/messaging/ordering.spec.ts
import { describe, test, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { WSTestClient } from '../../helpers/ws-test-client';
import { WebSocketServer } from 'ws';

describe('Message Ordering', () => {
  let wss: WebSocketServer;
  let client: WSTestClient;
  const PORT = 8767;

  beforeAll(() => {
    wss = new WebSocketServer({ port: PORT });
    wss.on('connection', (ws) => {
      ws.on('message', (data) => {
        // Echo with server timestamp
        const msg = JSON.parse(data.toString());
        ws.send(
          JSON.stringify({
            ...msg,
            serverTimestamp: Date.now(),
          })
        );
      });
    });
  });

  afterAll(() => wss.close());
  afterEach(() => client?.close());

  test('messages should arrive in order within a single connection', async () => {
    client = new WSTestClient(`ws://localhost:${PORT}`);
    await client.connect();

    const messageCount = 100;
    const receivedPromise = new Promise<void>((resolve) => {
      let count = 0;
      client.on('message', () => {
        count++;
        if (count === messageCount) resolve();
      });
    });

    // Send 100 messages with sequence numbers
    for (let i = 0; i < messageCount; i++) {
      client.send(JSON.stringify({ seq: i, data: `message-${i}` }));
    }

    await receivedPromise;

    const messages = client.getMessages();
    expect(messages).toHaveLength(messageCount);

    // Verify ordering
    for (let i = 0; i < messages.length; i++) {
      const parsed = JSON.parse(messages[i].data as string);
      expect(parsed.seq).toBe(i);
    }
  });

  test('should detect out-of-order messages', async () => {
    client = new WSTestClient(`ws://localhost:${PORT}`);
    await client.connect();

    // Create a server that deliberately reorders messages
    const reorderWss = new WebSocketServer({ port: PORT + 1 });
    const reorderClient = new WSTestClient(`ws://localhost:${PORT + 1}`);

    reorderWss.on('connection', (ws) => {
      const buffer: string[] = [];
      ws.on('message', (data) => {
        buffer.push(data.toString());
        // Every 3 messages, send them in reverse order
        if (buffer.length === 3) {
          buffer.reverse().forEach((msg) => ws.send(msg));
          buffer.length = 0;
        }
      });
    });

    await reorderClient.connect();

    const receivedPromise = new Promise<void>((resolve) => {
      let count = 0;
      reorderClient.on('message', () => {
        count++;
        if (count === 9) resolve();
      });
    });

    for (let i = 0; i < 9; i++) {
      reorderClient.send(JSON.stringify({ seq: i }));
    }

    await receivedPromise;

    const messages = reorderClient.getMessages();
    const sequences = messages.map((m) => JSON.parse(m.data as string).seq);

    // Detect ordering violations
    let outOfOrderCount = 0;
    for (let i = 1; i < sequences.length; i++) {
      if (sequences[i] < sequences[i - 1]) {
        outOfOrderCount++;
      }
    }

    expect(outOfOrderCount).toBeGreaterThan(0); // Confirms reordering occurred

    reorderClient.close();
    reorderWss.close();
  });

  test('should handle duplicate message detection', async () => {
    client = new WSTestClient(`ws://localhost:${PORT}`);
    await client.connect();

    // Server that sends duplicates
    const dupWss = new WebSocketServer({ port: PORT + 2 });
    const dupClient = new WSTestClient(`ws://localhost:${PORT + 2}`);

    dupWss.on('connection', (ws) => {
      ws.on('message', (data) => {
        // Send each message twice to simulate duplicates
        ws.send(data);
        ws.send(data);
      });
    });

    await dupClient.connect();

    const receivedPromise = new Promise<void>((resolve) => {
      let count = 0;
      dupClient.on('message', () => {
        count++;
        if (count === 6) resolve(); // 3 messages x 2 duplicates
      });
    });

    for (let i = 0; i < 3; i++) {
      dupClient.send(JSON.stringify({ id: `msg-${i}`, seq: i }));
    }

    await receivedPromise;

    const messages = dupClient.getMessages();
    const uniqueIds = new Set(messages.map((m) => JSON.parse(m.data as string).id));

    // Should detect duplicates
    expect(messages.length).toBe(6); // All messages received
    expect(uniqueIds.size).toBe(3);  // But only 3 unique

    dupClient.close();
    dupWss.close();
  });
});
```

## Heartbeat and Ping-Pong Testing

```typescript
// tests/websocket/heartbeat/ping-pong.spec.ts
import { describe, test, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { WSTestClient } from '../../helpers/ws-test-client';
import { WebSocketServer } from 'ws';

describe('Heartbeat / Ping-Pong', () => {
  let wss: WebSocketServer;
  let client: WSTestClient;
  const PORT = 8768;

  beforeAll(() => {
    wss = new WebSocketServer({ port: PORT });
    wss.on('connection', (ws) => {
      // Server responds to pings automatically (ws library default behavior)
      ws.on('message', (data) => ws.send(data));
    });
  });

  afterAll(() => wss.close());
  afterEach(() => client?.close());

  test('client should send periodic heartbeat pings', async () => {
    client = new WSTestClient(`ws://localhost:${PORT}`);
    await client.connect();

    let pongCount = 0;
    client.on('pong', () => pongCount++);

    // Start heartbeat with 200ms interval for fast testing
    client.startHeartbeat(200, 100);

    // Wait for several heartbeat cycles
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Should have received multiple pong responses
    expect(pongCount).toBeGreaterThanOrEqual(3);
  });

  test('should detect heartbeat timeout when server stops responding', async () => {
    // Create a server that does not respond to pings
    const silentWss = new WebSocketServer({ port: PORT + 1 });
    silentWss.on('connection', (ws) => {
      // Override the automatic pong response
      ws.on('ping', () => {
        // Deliberately do not send pong
      });
    });

    client = new WSTestClient(`ws://localhost:${PORT + 1}`, {
      maxReconnectAttempts: 0,
    });
    await client.connect();

    const timeoutPromise = new Promise<void>((resolve) => {
      client.on('heartbeat-timeout', () => resolve());
    });

    client.startHeartbeat(200, 100);

    // Should detect timeout
    await timeoutPromise;

    // Connection should be terminated
    await new Promise((resolve) => setTimeout(resolve, 200));
    expect(client.getState()).not.toBe(1); // Not OPEN

    silentWss.close();
  });

  test('heartbeat should reset timeout on each successful pong', async () => {
    client = new WSTestClient(`ws://localhost:${PORT}`);
    await client.connect();

    let timeoutOccurred = false;
    client.on('heartbeat-timeout', () => {
      timeoutOccurred = true;
    });

    // Start heartbeat
    client.startHeartbeat(100, 500);

    // Let it run for multiple cycles
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // No timeout should occur because server responds to pings
    expect(timeoutOccurred).toBe(false);
    expect(client.getState()).toBe(1); // Still OPEN
  });
});
```

## Connection Drop Simulation

### Simulating Network Disruptions in E2E Tests

```typescript
// tests/websocket/resilience/network-disruption.spec.ts
import { test, expect, Page } from '@playwright/test';

test.describe('WebSocket Network Disruption', () => {
  test('should reconnect after network interruption', async ({ page, context }) => {
    await page.goto('/chat');
    await page.waitForLoadState('networkidle');

    // Verify WebSocket is connected
    await expect(page.locator('[data-testid="connection-status"]')).toHaveText('Connected');

    // Send a message to confirm connectivity
    await page.fill('[data-testid="message-input"]', 'Hello before disconnect');
    await page.click('[data-testid="send-button"]');
    await expect(page.locator('[data-testid="messages"] >> text=Hello before disconnect')).toBeVisible();

    // Simulate network going offline
    await context.setOffline(true);

    // Wait for the connection to be detected as lost
    await expect(page.locator('[data-testid="connection-status"]')).toHaveText(
      /disconnected|reconnecting/i,
      { timeout: 10000 }
    );

    // Restore network
    await context.setOffline(false);

    // Should auto-reconnect
    await expect(page.locator('[data-testid="connection-status"]')).toHaveText(
      'Connected',
      { timeout: 15000 }
    );

    // Verify messaging works after reconnection
    await page.fill('[data-testid="message-input"]', 'Hello after reconnect');
    await page.click('[data-testid="send-button"]');
    await expect(
      page.locator('[data-testid="messages"] >> text=Hello after reconnect')
    ).toBeVisible();
  });

  test('should queue messages sent during disconnection', async ({ page, context }) => {
    await page.goto('/chat');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('[data-testid="connection-status"]')).toHaveText('Connected');

    // Go offline
    await context.setOffline(true);
    await expect(page.locator('[data-testid="connection-status"]')).toHaveText(
      /disconnected|reconnecting/i,
      { timeout: 10000 }
    );

    // Try to send messages while disconnected
    await page.fill('[data-testid="message-input"]', 'Queued message 1');
    await page.click('[data-testid="send-button"]');
    await page.fill('[data-testid="message-input"]', 'Queued message 2');
    await page.click('[data-testid="send-button"]');

    // Messages should show as pending
    await expect(page.locator('[data-testid="pending-indicator"]').first()).toBeVisible();

    // Restore network
    await context.setOffline(false);
    await expect(page.locator('[data-testid="connection-status"]')).toHaveText(
      'Connected',
      { timeout: 15000 }
    );

    // Queued messages should be delivered
    await expect(page.locator('[data-testid="pending-indicator"]')).toHaveCount(0, {
      timeout: 10000,
    });
    await expect(page.locator('text=Queued message 1')).toBeVisible();
    await expect(page.locator('text=Queued message 2')).toBeVisible();
  });

  test('should handle slow network gracefully', async ({ page }) => {
    // Throttle the network to simulate a poor connection
    const cdpSession = await page.context().newCDPSession(page);
    await cdpSession.send('Network.emulateNetworkConditions', {
      offline: false,
      downloadThroughput: 5000,   // 5 KB/s
      uploadThroughput: 5000,     // 5 KB/s
      latency: 2000,              // 2 seconds
    });

    await page.goto('/chat');

    // Connection should eventually establish even under slow conditions
    await expect(page.locator('[data-testid="connection-status"]')).toHaveText(
      'Connected',
      { timeout: 30000 }
    );

    // Messages should still work (possibly with delay)
    await page.fill('[data-testid="message-input"]', 'Slow network message');
    await page.click('[data-testid="send-button"]');

    await expect(page.locator('text=Slow network message')).toBeVisible({
      timeout: 15000,
    });

    // Reset network conditions
    await cdpSession.send('Network.emulateNetworkConditions', {
      offline: false,
      downloadThroughput: -1,
      uploadThroughput: -1,
      latency: 0,
    });
  });
});
```

## Authentication Token Refresh During WebSocket Sessions

```typescript
// tests/websocket/connection/authentication.spec.ts
import { describe, test, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { WSTestClient } from '../../helpers/ws-test-client';
import { WebSocketServer, WebSocket } from 'ws';
import { IncomingMessage } from 'http';

describe('WebSocket Authentication', () => {
  let wss: WebSocketServer;
  let client: WSTestClient;
  const PORT = 8769;

  beforeAll(() => {
    wss = new WebSocketServer({
      port: PORT,
      verifyClient: (info: { req: IncomingMessage }) => {
        const token = info.req.headers['authorization'];
        // Accept connections with valid tokens
        return token === 'Bearer valid-token' || token === 'Bearer refreshed-token';
      },
    });

    wss.on('connection', (ws) => {
      ws.send(JSON.stringify({ type: 'auth_success' }));
      ws.on('message', (data) => ws.send(data));
    });
  });

  afterAll(() => wss.close());
  afterEach(() => client?.close());

  test('should connect with valid authentication token', async () => {
    client = new WSTestClient(`ws://localhost:${PORT}`, {
      headers: { Authorization: 'Bearer valid-token' },
    });

    await client.connect();
    expect(client.getState()).toBe(WebSocket.OPEN);

    // Wait for auth success message
    await new Promise<void>((resolve) => {
      client.on('message', (msg) => {
        const parsed = JSON.parse(msg.data as string);
        if (parsed.type === 'auth_success') resolve();
      });
    });
  });

  test('should reject connection with invalid token', async () => {
    client = new WSTestClient(`ws://localhost:${PORT}`, {
      headers: { Authorization: 'Bearer invalid-token' },
      maxReconnectAttempts: 0,
    });

    await expect(client.connect()).rejects.toThrow();
  });

  test('should reconnect with refreshed token after auth expiry', async () => {
    let connectionCount = 0;

    const authWss = new WebSocketServer({
      port: PORT + 1,
      verifyClient: (info: { req: IncomingMessage }) => {
        connectionCount++;
        if (connectionCount === 1) return true;  // First connection succeeds
        if (connectionCount === 2) return false;  // Simulate token expiry
        return true;  // Third attempt with refreshed token succeeds
      },
    });

    authWss.on('connection', (ws) => {
      ws.on('message', (data) => ws.send(data));
    });

    client = new WSTestClient(`ws://localhost:${PORT + 1}`, {
      maxReconnectAttempts: 3,
      reconnectDelay: 100,
    });

    await client.connect();
    expect(client.getState()).toBe(WebSocket.OPEN);

    // Simulate server-side token expiry by closing connection
    authWss.clients.forEach((ws) => ws.close(4001, 'Token expired'));

    // Wait for reconnection attempts
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Client should have attempted to reconnect
    expect(connectionCount).toBeGreaterThanOrEqual(2);

    authWss.close();
  });
});
```

## Backpressure Testing

```typescript
// tests/websocket/resilience/backpressure.spec.ts
import { describe, test, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { WSTestClient } from '../../helpers/ws-test-client';
import { WebSocketServer, WebSocket } from 'ws';

describe('WebSocket Backpressure', () => {
  let wss: WebSocketServer;
  let client: WSTestClient;
  const PORT = 8770;

  beforeAll(() => {
    wss = new WebSocketServer({ port: PORT });
    wss.on('connection', (ws) => {
      ws.on('message', (data) => {
        // Simulate slow processing
        setTimeout(() => ws.send(data), 10);
      });
    });
  });

  afterAll(() => wss.close());
  afterEach(() => client?.close());

  test('should handle burst of messages without dropping', async () => {
    client = new WSTestClient(`ws://localhost:${PORT}`);
    await client.connect();

    const messageCount = 500;
    let received = 0;

    const allReceived = new Promise<void>((resolve) => {
      client.on('message', () => {
        received++;
        if (received === messageCount) resolve();
      });
    });

    // Send burst of messages
    for (let i = 0; i < messageCount; i++) {
      client.send(JSON.stringify({ seq: i, data: 'x'.repeat(100) }));
    }

    await allReceived;

    expect(received).toBe(messageCount);

    // Verify no messages were dropped
    const messages = client.getMessages();
    const sequences = messages.map((m) => JSON.parse(m.data as string).seq);
    const uniqueSequences = new Set(sequences);
    expect(uniqueSequences.size).toBe(messageCount);
  });

  test('should handle large payloads', async () => {
    client = new WSTestClient(`ws://localhost:${PORT}`);
    await client.connect();

    // Send increasingly large messages
    const sizes = [1024, 10240, 102400, 1048576]; // 1KB, 10KB, 100KB, 1MB

    for (const size of sizes) {
      const payload = JSON.stringify({
        size,
        data: 'x'.repeat(size),
      });

      const responsePromise = new Promise<void>((resolve) => {
        client.once('message', () => resolve());
      });

      client.send(payload);
      await responsePromise;

      const lastMessage = client.getMessages().at(-1);
      expect(lastMessage).toBeDefined();

      const parsed = JSON.parse(lastMessage!.data as string);
      expect(parsed.data.length).toBe(size);
    }
  });
});
```

## Concurrent Connection Limits

```typescript
// tests/websocket/connection/concurrent-connections.spec.ts
import { describe, test, expect, beforeAll, afterAll } from 'vitest';
import { WSTestClient } from '../../helpers/ws-test-client';
import { WebSocketServer } from 'ws';

describe('Concurrent WebSocket Connections', () => {
  let wss: WebSocketServer;
  const PORT = 8771;
  const MAX_CONNECTIONS = 10;

  beforeAll(() => {
    wss = new WebSocketServer({ port: PORT });
    let connectionCount = 0;

    wss.on('connection', (ws) => {
      connectionCount++;

      if (connectionCount > MAX_CONNECTIONS) {
        ws.close(4029, 'Too many connections');
        return;
      }

      ws.on('message', (data) => ws.send(data));
      ws.on('close', () => connectionCount--);
    });
  });

  afterAll(() => wss.close());

  test('should handle multiple concurrent connections', async () => {
    const clients: WSTestClient[] = [];
    const count = 5;

    for (let i = 0; i < count; i++) {
      const client = new WSTestClient(`ws://localhost:${PORT}`, {
        maxReconnectAttempts: 0,
      });
      await client.connect();
      clients.push(client);
    }

    // All clients should be connected
    for (const client of clients) {
      expect(client.getStateName()).toBe('OPEN');
    }

    // All clients should be able to send and receive
    for (let i = 0; i < clients.length; i++) {
      const responsePromise = new Promise<void>((resolve) => {
        clients[i].once('message', () => resolve());
      });
      clients[i].send(JSON.stringify({ client: i }));
      await responsePromise;
    }

    // Clean up
    clients.forEach((c) => c.close());
  });

  test('should reject connections beyond the limit', async () => {
    const clients: WSTestClient[] = [];

    // Fill up to the limit
    for (let i = 0; i < MAX_CONNECTIONS; i++) {
      const client = new WSTestClient(`ws://localhost:${PORT}`, {
        maxReconnectAttempts: 0,
      });
      await client.connect();
      clients.push(client);
    }

    // The next connection should be rejected
    const extraClient = new WSTestClient(`ws://localhost:${PORT}`, {
      maxReconnectAttempts: 0,
    });

    await extraClient.connect();

    // Should receive a close frame with the rejection code
    const closePromise = new Promise<number>((resolve) => {
      extraClient.on('close', (code) => resolve(code));
    });

    const code = await closePromise;
    expect(code).toBe(4029);

    // Clean up
    clients.forEach((c) => c.close());
    extraClient.close();
  });
});
```

## Configuration

### Playwright Configuration for WebSocket E2E Tests

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/websocket/e2e',
  fullyParallel: false, // WebSocket tests may share server state
  retries: 2,
  timeout: 30000,
  reporter: [
    ['html', { open: 'never' }],
    ['json', { outputFile: 'ws-test-results.json' }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'ws-chrome',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'ws-firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'ws-mobile',
      use: { ...devices['iPhone 14'] },
    },
  ],
});
```

### WebSocket Test Configuration

```typescript
// config/ws-test-config.ts
export const WS_TEST_CONFIG = {
  // Server configuration
  serverUrl: process.env.WS_SERVER_URL || 'ws://localhost:8080',
  serverPort: parseInt(process.env.WS_TEST_PORT || '8080', 10),

  // Connection settings
  connectTimeout: 5000,
  maxReconnectAttempts: 5,
  reconnectBaseDelay: 1000,
  reconnectMaxDelay: 30000,

  // Heartbeat settings
  heartbeatInterval: 30000,
  heartbeatTimeout: 5000,

  // Message settings
  maxMessageSize: 1048576,  // 1MB
  messageTimeout: 10000,

  // Test data
  burstMessageCount: 500,
  concurrentClientCount: 10,
  largePayloadSizes: [1024, 10240, 102400, 1048576],
};
```

## Best Practices

1. **Always implement exponential backoff with jitter for reconnection** -- A fixed reconnect interval causes all disconnected clients to reconnect simultaneously, creating a "thundering herd" that can overwhelm the server. Add random jitter to spread reconnection attempts.

2. **Use connection state machines** -- Model the WebSocket lifecycle as a state machine with explicit states (DISCONNECTED, CONNECTING, CONNECTED, RECONNECTING) and valid transitions. This prevents impossible state combinations like sending messages while disconnected.

3. **Implement message acknowledgment for critical operations** -- For messages that must not be lost (e.g., financial transactions, chat messages), implement application-level acknowledgments. Do not rely solely on TCP delivery guarantees.

4. **Test with real-world disconnect scenarios** -- Lab-perfect connections hide bugs. Test with WiFi-to-cellular transitions, VPN disconnects, laptop lid close/open, and browser tab backgrounding.

5. **Add sequence numbers to messages** -- Every message should include a monotonically increasing sequence number. This enables detection of gaps, duplicates, and reordering on the receiving end.

6. **Handle the "half-open" connection state** -- A TCP connection can appear open on one side while closed on the other. Heartbeats detect this condition. Without heartbeats, a client may believe it is connected while the server has already dropped the connection.

7. **Buffer messages during reconnection** -- Messages sent while the WebSocket is reconnecting should be queued and delivered once the connection is re-established, not silently dropped.

8. **Test binary message handling separately from text** -- Binary frames (ArrayBuffer, Blob) and text frames have different serialization paths. Test both frame types to ensure the application handles each correctly.

9. **Implement connection pooling for multiple channels** -- Applications that need multiple logical channels should multiplex over a single WebSocket connection rather than opening separate connections per channel.

10. **Set appropriate close codes** -- Use RFC 6455 close codes correctly: 1000 (normal), 1001 (going away), 1008 (policy violation), 1011 (unexpected condition). Custom codes should be in the 4000-4999 range.

11. **Test WebSocket behavior across browser tabs** -- Browsers may throttle or suspend WebSocket connections in background tabs. Test that reconnection works correctly when a user returns to a backgrounded tab.

12. **Monitor WebSocket connection metrics in production** -- Track connection duration, reconnection frequency, message latency, and error rates. These metrics reveal reliability issues that tests alone cannot catch.

## Anti-Patterns to Avoid

1. **Reconnecting immediately without backoff** -- Instant reconnection creates a retry storm that wastes bandwidth and can trigger rate limiting or server overload. Always use exponential backoff.

2. **Silently dropping messages during disconnection** -- When a user sends a chat message during a brief disconnect and the message disappears, it erodes trust. Queue messages and deliver them after reconnection.

3. **Using WebSocket as the only data channel** -- WebSocket connections are not guaranteed to stay open. Critical operations should have an HTTP fallback. Do not build flows that are impossible to complete without a persistent WebSocket.

4. **Ignoring close frames and codes** -- Different close codes have different meanings. Code 1001 (going away) suggests the server is restarting and reconnection will likely succeed. Code 1008 (policy violation) suggests the client should not reconnect.

5. **Opening a new WebSocket per request** -- WebSocket's advantage is persistent connections. Opening and closing a WebSocket for each message negates the protocol's benefits and adds significant overhead.

6. **Trusting message order across reconnections** -- A new WebSocket connection is a new TCP stream. Messages in transit during reconnection may be lost or arrive on the new connection out of order. Always use sequence numbers.

7. **Not testing concurrent connection limits** -- Browsers enforce per-domain WebSocket limits. Applications that open too many connections will silently fail to connect, causing features to break with no visible error.

## Debugging Tips

1. **Use Chrome DevTools WebSocket inspector** -- The Network tab in Chrome DevTools shows individual WebSocket frames (both sent and received). Filter by "WS" to see only WebSocket traffic. Click on a connection to inspect individual frames.

2. **Log connection state transitions** -- Add logging for every state change: CONNECTING, OPEN, CLOSING, CLOSED, and any custom states like RECONNECTING. This trace is invaluable for debugging intermittent connection issues.

3. **Check for load balancer idle timeout** -- Many load balancers (AWS ALB, nginx) close idle WebSocket connections after 60 seconds. If connections drop without heartbeat activity, the load balancer timeout is the likely culprit.

4. **Verify WebSocket upgrade headers** -- Use `curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket"` to verify the server responds with a 101 Switching Protocols response. A 200 OK indicates the upgrade failed.

5. **Test with `wscat` for quick manual verification** -- The `wscat` command-line tool (`npx wscat -c ws://localhost:8080`) provides a simple way to interactively test WebSocket endpoints without building a test client.

6. **Monitor `readyState` before sending** -- Always check `ws.readyState === WebSocket.OPEN` before calling `ws.send()`. Sending on a non-OPEN socket throws an error that may not be caught by error boundaries.

7. **Check for CORS issues on WebSocket upgrade** -- While the WebSocket protocol itself does not enforce CORS, some reverse proxies and CDNs may block WebSocket upgrade requests based on Origin headers. Check server logs for rejected upgrade requests.

8. **Use Wireshark to inspect WebSocket frames at the protocol level** -- When high-level debugging is insufficient, Wireshark can decode WebSocket frames and show the raw binary content, opcode, masking, and frame boundaries.

9. **Verify that ping/pong frames are not confused with application messages** -- WebSocket control frames (ping, pong, close) are distinct from data frames. Ensure your message handler does not process control frames as application messages.

10. **Test reconnection with server-side logging** -- Log connection and disconnection events on the server with client identifiers. Compare server-side logs with client-side reconnection logs to identify mismatches where the client believes it is connected but the server does not have a matching connection.
