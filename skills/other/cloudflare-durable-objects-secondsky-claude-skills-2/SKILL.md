---
name: cloudflare-durable-objects
description: Cloudflare Durable Objects for stateful coordination and real-time apps. Use for chat, multiplayer games, WebSocket hibernation, or encountering class export, migration, alarm errors.

  Keywords: durable objects, cloudflare do, DurableObject class, do bindings, websocket hibernation, do state api, ctx.storage.sql, ctx.acceptWebSocket, webSocketMessage, alarm() handler, storage.setAlarm, idFromName, newUniqueId, getByName, DurableObjectStub, serializeAttachment, real-time cloudflare, multiplayer cloudflare, chat room workers, coordination cloudflare, stateful workers, new_sqlite_classes, do migrations, location hints, RPC methods, blockConcurrencyWhile, "do class export", "new_sqlite_classes", "migrations required", "websocket hibernation", "alarm api error", "global uniqueness", "binding not found"
license: MIT
---

# Cloudflare Durable Objects

**Status**: Production Ready ✅
**Last Updated**: 2025-11-25
**Dependencies**: cloudflare-worker-base (recommended)
**Latest Versions**: wrangler@4.50.0+, @cloudflare/workers-types@4.20251125.0+
**Official Docs**: https://developers.cloudflare.com/durable-objects/

## Table of Contents
[What are Durable Objects?](#what-are-durable-objects) • [Quick Start](#quick-start-10-minutes) • [When to Load References](#when-to-load-references) • [Class Structure](#durable-object-class-structure) • [State API](#state-api---persistent-storage) • [WebSocket Hibernation](#websocket-hibernation-api) • [Alarms](#alarms-api---scheduled-tasks) • [RPC vs HTTP](#rpc-vs-http-fetch) • [Stubs & Routing](#creating-durable-object-stubs-and-routing) • [Migrations](#migrations---managing-do-classes) • [Common Patterns](#common-patterns) • [Critical Rules](#critical-rules) • [Known Issues](#known-issues-prevention)
## What are Durable Objects?

**Globally unique, stateful objects** with single-point coordination, strong consistency (ACID), WebSocket Hibernation (thousands of connections), SQLite storage (1GB), and alarms API.

**Use for:** Chat rooms, multiplayer games, rate limiting, session management, leader election, stateful workflows
---
## Quick Start (10 Minutes)

### Option 1: Scaffold New DO Project

```bash
npm create cloudflare@latest my-durable-app -- \
  --template=cloudflare/durable-objects-template --ts --git --deploy false
cd my-durable-app && bun install && npm run dev
```

### Option 2: Add to Existing Worker

**1. Install types:**
```bash
bun add -d @cloudflare/workers-types
```

**2. Create DO class** (`src/counter.ts`):
```typescript
import { DurableObject } from 'cloudflare:workers';

export class Counter extends DurableObject {
  async increment(): Promise<number> {
    let value: number = (await this.ctx.storage.get('value')) || 0;
    await this.ctx.storage.put('value', ++value);
    return value;
  }
}

export default Counter;  // CRITICAL
```

**3. Configure** (`wrangler.jsonc`):
```jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "COUNTER", "class_name": "Counter" }]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["Counter"] }
  ]
}
```

**4. Call from Worker** (`src/index.ts`):
```typescript
import { Counter } from './counter';

interface Env {
  COUNTER: DurableObjectNamespace<Counter>;
}

export { Counter };

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const stub = env.COUNTER.getByName('global-counter');
    return new Response(`Count: ${await stub.increment()}`);
  },
};
```

**Deploy:**

```bash
bunx wrangler deploy
```

---

## Available Commands

Use these interactive commands for guided workflows:

- **`/do-setup`** - Initialize new DO project with interactive setup wizard
  - Choose storage backend (SQL, KV, both)
  - Select use case pattern (WebSocket, Sessions, Rate Limiting, etc.)
  - Optional Vitest testing setup
  - Generates complete DO implementation

- **`/do-migrate`** - Interactive migration assistant
  - New class creation (new_sqlite_classes, new_classes)
  - Rename existing classes (renamed_classes)
  - Delete classes with safety confirmations (deleted_classes)
  - Transfer classes between scripts (transferred_classes)
  - Auto-increments migration tags (v1, v2, v3...)

- **`/do-debug`** - Step-by-step debugging workflow
  - Detects error categories (deployment, runtime, performance, etc.)
  - Runs diagnostic checks on configuration and code
  - Provides specific fixes with code examples
  - Guides local testing and production verification

- **`/do-patterns`** - Pattern selection wizard
  - Recommends DO pattern based on use case
  - Supports WebSocket, Rate Limiting, Sessions, Analytics, Leader Election
  - Generates complete pattern implementation
  - Provides best practices and optimization tips

- **`/do-optimize`** - Performance optimization assistant
  - Analyzes existing DO code for bottlenecks
  - Provides targeted optimization recommendations
  - Covers constructor, queries, WebSocket, memory, alarms
  - Measures performance improvements

## Autonomous Agents

These agents work autonomously without user interaction:

- **`do-debugger`** - Automatic error detection and fixing
  - Validates wrangler.jsonc configuration
  - Detects 16+ common DO errors
  - Applies fixes automatically with backups
  - Tests fixes before reporting

- **`do-setup-assistant`** - Automatic project scaffolding
  - Analyzes user requirements from natural language
  - Generates complete DO implementation
  - Creates tests, documentation, validation
  - Supports all use case patterns

- **`do-pattern-implementer`** - Production pattern implementation
  - Analyzes existing DO code
  - Recommends patterns by priority
  - Implements TTL cleanup, RPC metadata, SQL indexes, etc.
  - Generates pattern-specific tests

---

## When to Load References

**Load immediately when user mentions:**
- **`state-api-reference.md`** → "storage", "sql", "database", "query", "get/put", "KV", "1GB limit"
- **`websocket-hibernation.md`** → "websocket", "real-time", "chat", "hibernation", "serializeAttachment"
- **`alarms-api.md`** → "alarms", "scheduled tasks", "cron", "periodic", "batch processing"
- **`rpc-patterns.md`** → "RPC", "fetch", "HTTP", "methods", "routing"
- **`rpc-metadata.md`** → "RpcTarget", "metadata", "DO name", "idFromName access"
- **`stubs-routing.md`** → "stubs", "idFromName", "newUniqueId", "location hints", "jurisdiction"
- **`migrations-guide.md`** → "migrations", "rename", "delete", "transfer", "schema changes"
- **`migration-cheatsheet.md`** → "migration quick reference", "migration types", "common migrations"
- **`common-patterns.md`** → "patterns", "examples", "rate limiting", "sessions", "leader election"
- **`vitest-testing.md`** → "test", "testing", "vitest", "unit test", "@cloudflare/vitest-pool-workers"
- **`gradual-deployments.md`** → "gradual", "deployment", "traffic split", "rollout", "canary"
- **`typescript-config.md`** → "TypeScript", "types", "tsconfig", "wrangler.jsonc", "bindings"
- **`advanced-sql-patterns.md`** → "CTE", "window functions", "FTS5", "full-text search", "JSON functions", "complex SQL"
- **`security-best-practices.md`** → "security", "authentication", "authorization", "SQL injection", "CORS", "encryption", "rate limiting"
- **`error-codes.md`** → "error codes", "error catalog", "specific error", "E001", "troubleshooting"
- **`top-errors.md`** → errors, "not working", debugging, "binding not found"

**Load proactively when:**
- Building new feature → Load relevant pattern from `common-patterns.md`
- Debugging issue → Load `error-codes.md` for specific errors, then `top-errors.md`
- Implementing WebSocket → Load `websocket-hibernation.md` before coding
- Setting up storage → Load `state-api-reference.md` for SQL/KV APIs
- Complex SQL queries → Load `advanced-sql-patterns.md` for CTEs, window functions, FTS5
- Security review → Load `security-best-practices.md` for authentication, authorization, SQL injection prevention
- Creating first DO → Load `stubs-routing.md` for ID methods
- Writing tests → Load `vitest-testing.md` for testing patterns
- Planning deployment → Load `gradual-deployments.md` for rollout strategy
- Migration needed → Load `migration-cheatsheet.md` for quick reference
- Using DO name inside DO → Load `rpc-metadata.md` for RpcTarget pattern
- TypeScript configuration → Load `typescript-config.md` for setup

---

## Durable Object Class Structure

All DOs extend `DurableObject` and **MUST be exported**:

```typescript
import { DurableObject } from 'cloudflare:workers';

export class MyDO extends DurableObject {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);  // Required first line
    // Keep minimal - heavy work blocks hibernation
    ctx.blockConcurrencyWhile(async () => {
      // Load from storage before handling requests
    });
  }

  async myMethod(): Promise<string> {  // RPC method (recommended)
    return 'Hello!';
  }
}

export default MyDO;  // CRITICAL: Must export
```

**`this.ctx` provides:** `storage` (SQL/KV), `id` (unique ID), `waitUntil()`, `acceptWebSocket()`

---

## State API - Persistent Storage

Durable Objects provide two storage options:

**SQL API** (SQLite backend, **recommended**):
- Access via `ctx.storage.sql`
- Up to 1GB storage per instance
- SQL queries with transactions, indexes, cursors
- Atomic operations (deleteAll is all-or-nothing)
- Use `new_sqlite_classes` in migrations

**Key-Value API** (available on both backends):
- Access via `ctx.storage` (get/put/delete/list)
- Simple key-value operations
- Async transactions supported
- 128MB limit on KV backend, 1GB on SQLite

**Quick example**:
```typescript
export class Counter extends DurableObject {
  sql: SqlStorage;

  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.sql.exec('CREATE TABLE IF NOT EXISTS counts (key TEXT PRIMARY KEY, value INTEGER)');
  }

  async increment(): Promise<number> {
    this.sql.exec('INSERT OR REPLACE INTO counts (key, value) VALUES (?, ?)', 'count', 1);
    return this.sql.exec('SELECT value FROM counts WHERE key = ?', 'count').one<{value: number}>().value;
  }
}
```

**Load `references/state-api-reference.md` for complete SQL and KV API documentation, cursor operations, transactions, parameterized queries, storage limits, and migration patterns.**

---

## WebSocket Hibernation API

Handle **thousands of WebSocket connections** per DO instance with automatic hibernation when idle (~10s no activity), saving duration costs. Connections stay open at the edge while DO sleeps.

**CRITICAL Rules**:
- ✅ Use `ctx.acceptWebSocket(server)` (enables hibernation)
- ✅ Use `ws.serializeAttachment(data)` to persist metadata across hibernation
- ✅ Restore connections in constructor with `ctx.getWebSockets()`
- ❌ Don't use `ws.accept()` (standard API, no hibernation)
- ❌ Don't use `setTimeout`/`setInterval` (prevents hibernation)

**Handler methods**: `webSocketMessage()`, `webSocketClose()`, `webSocketError()`

**Quick pattern**:
```typescript
export class ChatRoom extends DurableObject {
  sessions: Map<WebSocket, any>;

  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    this.sessions = new Map();
    // Restore connections after hibernation
    ctx.getWebSockets().forEach(ws => {
      this.sessions.set(ws, ws.deserializeAttachment());
    });
  }

  async fetch(request: Request): Promise<Response> {
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    this.ctx.acceptWebSocket(server);  // ← Enables hibernation
    server.serializeAttachment({ userId: 'alice' });  // ← Persists across hibernation
    this.sessions.set(server, { userId: 'alice' });

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws: WebSocket, message: string): Promise<void> {
    const session = this.sessions.get(ws);
    // Broadcast to all
    this.sessions.forEach((_, w) => w.send(message));
  }
}
```

**Load `references/websocket-hibernation.md` for complete handler patterns, hibernation lifecycle, serializeAttachment API, connection management, broadcasting patterns, and hibernation troubleshooting.**

---

## Alarms API - Scheduled Tasks

Schedule DO to wake up at a future time for batching, cleanup, reminders, or periodic tasks.

**Core API**:
- `await ctx.storage.setAlarm(timestamp)` - Schedule alarm
- `await ctx.storage.getAlarm()` - Get current alarm time (null if not set)
- `await ctx.storage.deleteAlarm()` - Cancel alarm
- `async alarm(info)` - Handler called when alarm fires

**Key Features**:
- ✅ Guaranteed at-least-once execution with automatic retries (up to 6)
- ✅ Survives hibernation and eviction
- ✅ Deleted automatically after successful execution
- ⚠️ Only ONE alarm per DO (setting new one overwrites previous)

**Quick pattern**:
```typescript
export class Batcher extends DurableObject {
  async addItem(item: string): Promise<void> {
    await this.ctx.storage.put('items', [...existingItems, item]);

    // Schedule batch processing if not already scheduled
    if (await this.ctx.storage.getAlarm() === null) {
      await this.ctx.storage.setAlarm(Date.now() + 10000);  // 10 seconds
    }
  }

  async alarm(info: { retryCount: number; isRetry: boolean }): Promise<void> {
    const items = await this.ctx.storage.get('items');
    await this.processBatch(items);  // Send to API, write to DB, etc.
    await this.ctx.storage.put('items', []);  // Clear buffer
  }
}
```

**Load `references/alarms-api.md` for periodic alarms pattern, retry handling, error scenarios, cleanup jobs, and batching strategies.**

---

## RPC vs HTTP Fetch

**RPC (Recommended)**: Call DO methods directly like `await stub.increment()`. Type-safe, simple, auto-serialization. Requires `compatibility_date >= 2024-04-03`.

**HTTP Fetch**: Traditional HTTP request/response with `async fetch(request)` handler. Required for WebSocket upgrades.

**Quick comparison**:
```typescript
// RPC Pattern (simpler)
export class Counter extends DurableObject {
  async increment(): Promise<number> {  // ← Direct method
    let value = await this.ctx.storage.get<number>('count') || 0;
    return ++value;
  }
}
const count = await stub.increment();  // ← Direct call

// HTTP Fetch Pattern
export class Counter extends DurableObject {
  async fetch(request: Request): Promise<Response> {  // ← HTTP handler
    const url = new URL(request.url);
    if (url.pathname === '/increment') { /* ... */ }
  }
}
const response = await stub.fetch('/increment', { method: 'POST' });
```

**Use RPC for**: New projects, type safety, simple method calls
**Use HTTP Fetch for**: WebSocket upgrades, complex routing, legacy code

**Load `references/rpc-patterns.md` for complete RPC vs Fetch comparison, migration guide, error handling patterns, and method visibility control.**

---

## Creating Durable Object Stubs and Routing

To interact with a Durable Object from a Worker: **get an ID** → **create a stub** → **call methods**.

**Three ID creation methods:**

1. **`idFromName(name)`** - Named DOs (most common): Deterministic routing to same instance globally
2. **`newUniqueId()`** - Random IDs: New unique instance, must store ID for future access
3. **`idFromString(idString)`** - Recreate from saved ID string

**Getting stubs:**

```typescript
// Method 1: From ID
const id = env.CHAT_ROOM.idFromName('room-123');
const stub = env.CHAT_ROOM.get(id);

// Method 2: Shortcut for named DOs (recommended)
const stub = env.CHAT_ROOM.getByName('room-123');

await stub.myMethod();
```

**Geographic routing with location hints:**
- Set `locationHint` option when creating stub: `{ locationHint: 'enam' }`
- 9 regions: wnam, enam, sam, weur, eeur, apac, oc, afr, me
- Best-effort (not guaranteed), only affects first creation

**Data residency with jurisdiction restrictions:**
- Use `newUniqueId({ jurisdiction: 'eu' })` or `{ jurisdiction: 'fedramp' }`
- Strictly enforced (DO never leaves jurisdiction)
- Cannot combine with location hints
- Required for GDPR/FedRAMP compliance

**Load `references/stubs-routing.md` for complete guide to ID methods, stub management, location hints, jurisdiction restrictions, use cases, best practices, and error handling patterns.**

---

## Migrations - Managing DO Classes

**Migrations are REQUIRED** when creating, renaming, deleting, or transferring DO classes between Workers.

**Four migration types:**

1. **Create New DO**: Use `new_sqlite_classes` (recommended, 1GB) or `new_classes` (legacy KV, 128MB)
2. **Rename DO**: Use `renamed_classes` with `from`/`to` mapping (data preserved, bindings forward)
3. **Delete DO**: Use `deleted_classes` (⚠️ immediate deletion, cannot undo, all storage lost)
4. **Transfer DO**: Use `transferred_classes` with `from_script` (moves instances to new Worker)

**Quick example - Create new DO with SQLite:**

```jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "COUNTER", "class_name": "Counter" }]
  },
  "migrations": [
    {
      "tag": "v1",                    // Unique identifier (append-only)
      "new_sqlite_classes": ["Counter"]
    }
  ]
}
```

**CRITICAL rules:**
- ❌ Migrations are ATOMIC (all instances migrate at once, no gradual rollout)
- ❌ Cannot enable SQLite on existing KV-backed DOs (must create new class)
- ❌ Migration tags must be unique (cannot reuse, append-only)
- ✅ Code changes don't need migrations (only schema changes do)
- ✅ DO class names are unique per account (across all Workers)

**Load `references/migrations-guide.md` for complete migration patterns, rename/delete/transfer procedures, rollback strategies, and migration gotchas.**

---

## Common Patterns

**Four production-ready patterns for Cloudflare Durable Objects:**

1. **Rate Limiting** - Per-user rate limiting with sliding window, KV storage for request tracking
2. **Session Management** - User sessions with TTL, SQL storage, automatic cleanup via alarms
3. **Leader Election** - Single leader guarantee using SQL constraints, heartbeat mechanism
4. **Multi-DO Coordination** - Game coordinator + game rooms pattern, parent-child DO relationships

**Quick example - Rate limiter:**

```typescript
export class RateLimiter extends DurableObject {
  async checkLimit(userId: string, limit: number, window: number): Promise<boolean> {
    const requests = await this.ctx.storage.get<number[]>(`rate:${userId}`) || [];
    const validRequests = requests.filter(t => Date.now() - t < window);

    if (validRequests.length >= limit) return false;

    validRequests.push(Date.now());
    await this.ctx.storage.put(`rate:${userId}`, validRequests);
    return true;
  }
}
```

**Load `references/common-patterns.md` for complete implementations of all 4 patterns with full code examples, SQL schemas, alarm usage, error handling, and best practices.**

---

## Critical Rules

**✅ Always:**
- Export DO class: `export default MyDO`
- Call `super(ctx, env)` first in constructor
- Use `new_sqlite_classes` in migrations (1GB vs 128MB KV)
- Use `ctx.acceptWebSocket()` for hibernation (not `ws.accept()`)
- Persist state to storage (not just memory)
- Use alarms instead of setTimeout/setInterval
- Use parameterized SQL: `sql.exec('... WHERE id = ?', id)`
- Minimize constructor work, use `blockConcurrencyWhile()`

**❌ Never:**
- Create DO without migration (error)
- Forget to export class (binding not found)
- Use setTimeout/setInterval (prevents hibernation)
- Rely only on in-memory state for WebSockets (use serializeAttachment)
- Deploy migrations gradually (migrations are atomic)
- Enable SQLite on existing KV-backed DO (must create new class)
- Assume location hints are guaranteed (best-effort only)

---

## Known Issues Prevention

This skill prevents **15+ documented issues**. Top 3 most critical:

### Issue #1: Class Not Exported
**Error**: `"binding not found"` | **Why**: DO class not exported
**Fix**: `export default MyDO;`

### Issue #2: Missing Migration
**Error**: `"migrations required"` | **Why**: Created DO without migration entry
**Fix**: Add `{ "tag": "v1", "new_sqlite_classes": ["MyDO"] }` to migrations

### Issue #3: setTimeout Breaks Hibernation
**Error**: DO never hibernates, high charges | **Why**: `setTimeout` prevents hibernation
**Fix**: Use `await ctx.storage.setAlarm(Date.now() + 1000)` instead

**12 more issues covered**: Wrong migration type, constructor overhead, in-memory state lost, outgoing WebSocket no hibernation, global uniqueness confusion, partial deleteAll, binding mismatch, state size exceeded, migration not atomic, location hint ignored, alarm retry failures, fetch blocks hibernation.

**Load `references/top-errors.md` for complete error catalog with all 15+ issues, detailed prevention strategies, debugging steps, and resolution patterns.**

---

## Configuration & TypeScript

Configure wrangler.jsonc with DO bindings and migrations, set up TypeScript types with proper exports.

**Load `references/typescript-config.md` for**: wrangler.jsonc structure, TypeScript types, Env interface, tsconfig.json, common type issues

---

**Official Docs**: https://developers.cloudflare.com/durable-objects/
- **State API (SQL)**: https://developers.cloudflare.com/durable-objects/api/sqlite-storage-api/
- **WebSocket Hibernation**: https://developers.cloudflare.com/durable-objects/best-practices/websockets/
- **Alarms API**: https://developers.cloudflare.com/durable-objects/api/alarms/
- **Migrations**: https://developers.cloudflare.com/durable-objects/reference/durable-objects-migrations/
- **Best Practices**: https://developers.cloudflare.com/durable-objects/best-practices/ 
**Questions?** Load `references/top-errors.md` for common problems or check `templates/` for working examples
