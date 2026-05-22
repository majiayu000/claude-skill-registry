---
name: cloudflare-durable-objects
description: "Cloudflare Durable Objects stateful serverless playbook: DurableObjectState, Storage API (SQLite/KV), WebSocket hibernation, alarms, RPC, bindings, migrations, limits, pricing. Keywords: Durable Objects, DurableObjectState, DurableObjectStorage, SQLite, ctx.storage, WebSocket hibernation, acceptWebSocket, alarms, setAlarm, RPC, blockConcurrencyWhile."
---

# Cloudflare Durable Objects

Durable Objects combine compute with strongly consistent, transactional storage. Each object has a globally-unique name, enabling coordination across clients worldwide.

---

## Quick Start

### Durable Object Class

```typescript
// src/counter.ts
import { DurableObject } from "cloudflare:workers";

export class Counter extends DurableObject<Env> {
  async increment(): Promise<number> {
    let count = (await this.ctx.storage.get<number>("count")) ?? 0;
    count++;
    await this.ctx.storage.put("count", count);
    return count;
  }

  async getCount(): Promise<number> {
    return (await this.ctx.storage.get<number>("count")) ?? 0;
  }
}
```

### Worker Entry Point

```typescript
// src/index.ts
export { Counter } from "./counter";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const id = env.COUNTER.idFromName("global");
    const stub = env.COUNTER.get(id);
    const count = await stub.increment();
    return new Response(`Count: ${count}`);
  },
};
```

### wrangler.jsonc

```jsonc
{
  "name": "counter-worker",
  "main": "src/index.ts",
  "durable_objects": {
    "bindings": [
      {
        "name": "COUNTER",
        "class_name": "Counter"
      }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": ["Counter"]
    }
  ]
}
```

### Deploy

```bash
npx wrangler deploy
```

---

## Core Concepts

### DurableObjectState

Available as `this.ctx` in Durable Object class:

```typescript
interface DurableObjectState {
  readonly id: DurableObjectId;
  readonly storage: DurableObjectStorage;

  blockConcurrencyWhile<T>(callback: () => Promise<T>): Promise<T>;
  waitUntil(promise: Promise<any>): void; // No effect in DO

  // WebSocket Hibernation
  acceptWebSocket(ws: WebSocket, tags?: string[]): void;
  getWebSockets(tag?: string): WebSocket[];
  getTags(ws: WebSocket): string[];
  setWebSocketAutoResponse(pair?: WebSocketRequestResponsePair): void;
  getWebSocketAutoResponse(): WebSocketRequestResponsePair | null;

  abort(message?: string): void; // Force reset DO
}
```

### DurableObjectId

```typescript
const id = env.MY_DO.idFromName("user-123"); // Deterministic ID
const id = env.MY_DO.newUniqueId(); // Random unique ID
const stub = env.MY_DO.get(id); // Get stub for DO instance
```

See [api.md](references/api.md) for full type definitions.

---

## Storage API (SQLite-backed)

SQLite is the recommended storage backend for new Durable Objects.

### SQL API

```typescript
const cursor = this.ctx.storage.sql.exec("SELECT * FROM users WHERE id = ?", userId);

// Get single row (throws if not exactly one)
const user = cursor.one();

// Get all rows
const users = cursor.toArray();

// Iterate
for (const row of cursor) {
  console.log(row);
}
```

### SQL Cursor Properties

```typescript
cursor.columnNames; // string[]
cursor.rowsRead; // number
cursor.rowsWritten; // number
```

### Create Tables

```typescript
this.ctx.storage.sql.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at INTEGER DEFAULT (unixepoch())
  )
`);
```

### Insert/Update

```typescript
this.ctx.storage.sql.exec("INSERT INTO users (id, name) VALUES (?, ?)", id, name);

this.ctx.storage.sql.exec("UPDATE users SET name = ? WHERE id = ?", newName, id);
```

### Transactions

```typescript
// Synchronous transaction (SQLite only)
this.ctx.storage.transactionSync(() => {
  this.ctx.storage.sql.exec("INSERT INTO logs (msg) VALUES (?)", "start");
  this.ctx.storage.sql.exec("UPDATE counters SET value = value + 1");
});
```

### Database Size

```typescript
const sizeBytes = this.ctx.storage.sql.databaseSize;
```

See [storage.md](references/storage.md) for KV API and advanced usage.

---

## Storage API (KV)

### Synchronous KV (SQLite-backed)

```typescript
this.ctx.storage.kv.put("key", value);
const val = this.ctx.storage.kv.get("key");
const deleted = this.ctx.storage.kv.delete("key");

for (const [key, value] of this.ctx.storage.kv.list()) {
  console.log(key, value);
}
```

### Async KV (Both backends)

```typescript
await this.ctx.storage.put("key", value);
const val = await this.ctx.storage.get<MyType>("key");

// Batch operations (up to 128 keys)
const values = await this.ctx.storage.get(["key1", "key2", "key3"]);
await this.ctx.storage.put({ key1: val1, key2: val2 });
await this.ctx.storage.delete(["key1", "key2"]);

// List with options
const map = await this.ctx.storage.list({ prefix: "user:" });

// Delete all
await this.ctx.storage.deleteAll();
```

### Write Coalescing

Multiple writes without `await` are coalesced atomically:

```typescript
// These are batched into single transaction
this.ctx.storage.put("a", 1);
this.ctx.storage.put("b", 2);
this.ctx.storage.put("c", 3);
// All committed together
```

---

## Alarms

Schedule single alarm per Durable Object for background processing.

### Set Alarm

```typescript
// Schedule 1 hour from now
await this.ctx.storage.setAlarm(Date.now() + 60 * 60 * 1000);

// Schedule at specific time
await this.ctx.storage.setAlarm(new Date("2024-12-31T00:00:00Z"));
```

### Handle Alarm

```typescript
export class MyDO extends DurableObject<Env> {
  async alarm(info?: AlarmInfo): Promise<void> {
    console.log(`Alarm fired! Retry: ${info?.isRetry}, count: ${info?.retryCount}`);

    // Process scheduled work
    await this.processScheduledTasks();

    // Schedule next alarm if needed
    const nextRun = await this.getNextScheduledTime();
    if (nextRun) {
      await this.ctx.storage.setAlarm(nextRun);
    }
  }
}
```

### Alarm Methods

```typescript
await this.ctx.storage.setAlarm(timestamp); // Set/overwrite alarm
const time = await this.ctx.storage.getAlarm(); // Get scheduled time (ms) or null
await this.ctx.storage.deleteAlarm(); // Cancel alarm
```

**Retry behavior**: Alarms retry with exponential backoff (2s initial, up to 6 retries) on exceptions.

See [alarms.md](references/alarms.md) for patterns.

---

## WebSocket Hibernation

Keep WebSocket connections alive while Durable Object hibernates.

### Accept WebSocket

```typescript
export class ChatRoom extends DurableObject<Env> {
  async fetch(request: Request): Promise<Response> {
    const upgradeHeader = request.headers.get("Upgrade");
    if (upgradeHeader === "websocket") {
      const [client, server] = Object.values(new WebSocketPair());

      // Accept with hibernation support
      this.ctx.acceptWebSocket(server, ["user:123"]); // Optional tags

      return new Response(null, { status: 101, webSocket: client });
    }
    return new Response("Expected WebSocket", { status: 400 });
  }

  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer): Promise<void> {
    // Handle incoming message (DO wakes from hibernation)
    this.broadcast(message);
  }

  async webSocketClose(ws: WebSocket, code: number, reason: string): Promise<void> {
    // Handle disconnect
  }
}
```

### Broadcast to All

```typescript
broadcast(message: string) {
  for (const ws of this.ctx.getWebSockets()) {
    ws.send(message);
  }
}
```

### Per-Connection State

```typescript
// Save state that survives hibernation (max 2048 bytes)
ws.serializeAttachment({ userId: "123", role: "admin" });

// Restore in message handler
const state = ws.deserializeAttachment();
```

### Auto-Response (No Wake)

```typescript
// Respond to pings without waking DO
this.ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair("ping", "pong"));
```

See [websockets.md](references/websockets.md) for details.

---

## RPC Methods

Call Durable Object methods directly (compatibility date >= 2024-04-03):

```typescript
const stub = env.USER_SERVICE.get(id);
const user = await stub.getUser("123"); // Direct RPC call
await stub.updateUser("123", { name: "New Name" });
```

**Note**: Each RPC method call = one RPC session for billing.

---

## Initialization

Use `blockConcurrencyWhile` in constructor for migrations:

```typescript
constructor(ctx: DurableObjectState, env: Env) {
  super(ctx, env);
  ctx.blockConcurrencyWhile(async () => {
    this.ctx.storage.sql.exec(`CREATE TABLE IF NOT EXISTS data (key TEXT PRIMARY KEY, value TEXT)`);
  });
}
```

**Timeout**: 30 seconds.

---

## Hibernation

### Conditions for Hibernation

All must be true:

- No pending `setTimeout`/`setInterval`
- No in-progress `await fetch()`
- Using Hibernation WebSocket API (not standard WebSocket)
- No active request processing

### Lifecycle

1. **Active**: Processing requests
2. **Idle hibernateable**: ~10 seconds → may hibernate
3. **Hibernated**: Removed from memory, WebSockets stay connected
4. **Wake**: On message/event, constructor runs, handler invoked

**Important**: In-memory state is lost on hibernation. Restore from storage or attachments.

---

## Bindings & Migrations

```jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "MY_DO", "class_name": "MyDO" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyDO"] }]
}
```

**Note**: Cannot enable SQLite on existing deployed classes.

---

## Wrangler Commands

```bash
npx wrangler deploy   # Deploy with migrations
wrangler tail         # Tail logs
```

---

## Limits

| Feature               | Free     | Paid               |
| --------------------- | -------- | ------------------ |
| DO classes            | 100      | 500                |
| Storage per DO        | 10 GB    | 10 GB              |
| Storage per account   | 5 GB     | Unlimited          |
| CPU per request       | 30 sec   | 30 sec (max 5 min) |
| WebSocket connections | 32,768   | 32,768             |
| SQL row/value size    | 2 MB     | 2 MB               |
| KV value size         | 128 KiB  | 128 KiB            |
| Batch size            | 128 keys | 128 keys           |

---

## Pricing

| Metric              | Free         | Paid                           |
| ------------------- | ------------ | ------------------------------ |
| Requests            | 100K/day     | 1M/mo included, +$0.15/M       |
| Duration            | 13K GB-s/day | 400K GB-s/mo, +$12.50/M GB-s   |
| SQLite rows read    | 5M/day       | 25B/mo included, +$0.001/M     |
| SQLite rows written | 100K/day     | 50M/mo included, +$1.00/M      |
| Storage             | 5 GB         | 5 GB/mo included, +$0.20/GB-mo |

**WebSocket**: 20:1 billing ratio (1M messages = 50K requests).

See [pricing.md](references/pricing.md) for details.

---

## Prohibitions

- ❌ Do not store state outside storage (lost on hibernation)
- ❌ Do not use standard WebSocket API for hibernation
- ❌ Do not exceed 2 MB per row/value in SQLite
- ❌ Do not call `sql.exec()` with transaction control statements
- ❌ Do not expect `waitUntil` to work (no effect in DO)

---

## References

- [api.md](references/api.md) — Full API reference
- [storage.md](references/storage.md) — Storage API details
- [websockets.md](references/websockets.md) — WebSocket hibernation
- [alarms.md](references/alarms.md) — Alarm patterns
- [pricing.md](references/pricing.md) — Billing details

## Related Skills

- `cloudflare-workers` — Worker development
- `cloudflare-d1` — D1 database
- `cloudflare-kv` — Global KV
- `cloudflare-workflows` — Durable execution
