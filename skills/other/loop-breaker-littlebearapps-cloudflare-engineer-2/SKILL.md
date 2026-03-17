---
name: loop-breaker
description: Scaffold middleware to detect and block Worker self-recursion, infinite fetch chains, and runaway loops. Use this skill when designing Workers that call other Workers, implement webhooks, or handle events that might trigger themselves. Also use when encountering "recursion", "infinite loop", "self-call", "fetch chain", or "denial of wallet" scenarios.
---

# Loop Breaker Skill

Scaffold protective middleware to prevent infinite recursion, self-calling Workers, and runaway loops that cause "denial-of-wallet" attacks on your Cloudflare bill.

## Why This Matters

In serverless, a loop isn't just a frozen browser tab—it's a **direct billing multiplier**:

| Loop Type | Billing Impact | Example Cost |
|-----------|---------------|--------------|
| Worker → Worker fetch chain | Each hop = new Worker invocation | 1000 loops × $0.30/M = instant bill |
| D1 query in loop | Each iteration = row reads | 1M rows × $0.25/B = $0.25+ per loop |
| R2 write in loop | Each iteration = Class A op | 1000 writes × $4.50/M = $0.0045+ |
| DO kept alive | Duration billing continues | 1 hour idle = $0.045 |

## Recursion Depth Middleware

The most common and costly loop occurs when a Worker calls itself (or calls a second Worker that calls the first) via `fetch()`. This creates an infinite chain of HTTP requests.

### Pattern: X-Recursion-Depth Header

**Core Implementation**:

```typescript
// src/middleware/recursion-guard.ts
import { createMiddleware } from 'hono/factory';
import type { Bindings } from '../types';

const RECURSION_HEADER = 'X-Recursion-Depth';
const DEFAULT_DEPTH_LIMIT = 3;

interface RecursionGuardOptions {
  maxDepth?: number;
  onLimitExceeded?: (depth: number) => Response;
}

export const recursionGuard = (options: RecursionGuardOptions = {}) => {
  const maxDepth = options.maxDepth ?? DEFAULT_DEPTH_LIMIT;

  return createMiddleware<{ Bindings: Bindings }>(async (c, next) => {
    const currentDepth = parseInt(c.req.header(RECURSION_HEADER) || '0', 10);

    if (currentDepth > maxDepth) {
      console.error(`Recursion limit exceeded: depth=${currentDepth}, limit=${maxDepth}`);

      if (options.onLimitExceeded) {
        return options.onLimitExceeded(currentDepth);
      }

      // HTTP 508 Loop Detected (RFC 5842)
      return c.json({
        error: 'Loop Detected',
        message: `Recursion depth ${currentDepth} exceeds limit ${maxDepth}`,
        code: 'RECURSION_LIMIT_EXCEEDED'
      }, 508);
    }

    // Store for use in outgoing requests
    c.set('recursionDepth', currentDepth);

    await next();
  });
};

/**
 * Create headers for outgoing fetch requests that preserve recursion tracking
 */
export function createRecursionHeaders(
  currentHeaders: Headers,
  currentDepth: number
): Headers {
  const newHeaders = new Headers(currentHeaders);
  newHeaders.set(RECURSION_HEADER, (currentDepth + 1).toString());
  return newHeaders;
}
```

### Usage in Hono App

```typescript
// src/index.ts
import { Hono } from 'hono';
import { recursionGuard, createRecursionHeaders } from './middleware/recursion-guard';
import type { Bindings } from './types';

// Extend Hono context to include recursionDepth
type Variables = {
  recursionDepth: number;
};

const app = new Hono<{ Bindings: Bindings; Variables: Variables }>();

// Apply recursion guard to all routes
app.use('*', recursionGuard({ maxDepth: 3 }));

// Example: Worker that calls another Worker
app.post('/webhook', async (c) => {
  const currentDepth = c.get('recursionDepth');

  // When making outgoing requests, pass the incremented depth
  const response = await fetch('https://other-worker.example.com/process', {
    method: 'POST',
    headers: createRecursionHeaders(c.req.raw.headers, currentDepth),
    body: await c.req.text(),
  });

  return c.json({ processed: true, depth: currentDepth });
});

export default app;
```

### Types Extension

Add to `src/types.ts`:

```typescript
// Add to Hono Variables
declare module 'hono' {
  interface ContextVariableMap {
    recursionDepth: number;
  }
}
```

## Service Binding Recursion Guard

When using Service Bindings (RPC), you still need recursion protection but headers don't apply. Use a context-passing pattern:

```typescript
// src/services/with-recursion-context.ts

interface RecursionContext {
  depth: number;
  maxDepth: number;
  callChain: string[];
}

export function createRecursionContext(
  workerName: string,
  existingContext?: RecursionContext
): RecursionContext {
  const ctx = existingContext ?? { depth: 0, maxDepth: 5, callChain: [] };

  return {
    depth: ctx.depth + 1,
    maxDepth: ctx.maxDepth,
    callChain: [...ctx.callChain, workerName],
  };
}

export function checkRecursionLimit(ctx: RecursionContext): void {
  if (ctx.depth > ctx.maxDepth) {
    throw new RecursionLimitError(ctx);
  }

  // Detect cycles in call chain
  const seen = new Set<string>();
  for (const worker of ctx.callChain) {
    if (seen.has(worker)) {
      throw new RecursionCycleError(worker, ctx.callChain);
    }
    seen.add(worker);
  }
}

class RecursionLimitError extends Error {
  constructor(ctx: RecursionContext) {
    super(`Recursion limit exceeded: ${ctx.depth} > ${ctx.maxDepth}`);
    this.name = 'RecursionLimitError';
  }
}

class RecursionCycleError extends Error {
  constructor(worker: string, chain: string[]) {
    super(`Recursion cycle detected: ${worker} in chain [${chain.join(' -> ')}]`);
    this.name = 'RecursionCycleError';
  }
}
```

### Service Binding Usage

```typescript
// When calling another Worker via Service Binding
const ctx = createRecursionContext('api-gateway', incomingContext);
checkRecursionLimit(ctx);

const result = await c.env.DATA_SERVICE.fetchUser(userId, ctx);
```

## Queue Idempotency Guard

Cloudflare Queues can create "Retry Loops" when a Worker fails to process a message due to a persistent bug. This burns CPU and D1 writes on every retry.

```typescript
// src/middleware/idempotency-guard.ts

interface IdempotencyOptions {
  kv: KVNamespace;
  ttlSeconds?: number;
  keyPrefix?: string;
}

export async function ensureIdempotent(
  messageId: string,
  options: IdempotencyOptions
): Promise<{ alreadyProcessed: boolean; markProcessed: () => Promise<void> }> {
  const { kv, ttlSeconds = 86400, keyPrefix = 'processed:' } = options;
  const key = `${keyPrefix}${messageId}`;

  const existing = await kv.get(key);
  if (existing) {
    return {
      alreadyProcessed: true,
      markProcessed: async () => {},
    };
  }

  return {
    alreadyProcessed: false,
    markProcessed: async () => {
      await kv.put(key, Date.now().toString(), { expirationTtl: ttlSeconds });
    },
  };
}

// Queue consumer usage
export default {
  async queue(batch: MessageBatch<QueueMessage>, env: Bindings): Promise<void> {
    for (const msg of batch.messages) {
      const { alreadyProcessed, markProcessed } = await ensureIdempotent(
        msg.id,
        { kv: env.IDEMPOTENCY_KV }
      );

      if (alreadyProcessed) {
        console.log(`Skipping duplicate message: ${msg.id}`);
        msg.ack();
        continue;
      }

      try {
        await processMessage(msg.body, env);
        await markProcessed();
        msg.ack();
      } catch (error) {
        console.error(`Failed to process message ${msg.id}:`, error);
        msg.retry(); // Will go to DLQ after max_retries
      }
    }
  },
};
```

## Durable Object Loop Protection

Durable Objects billing includes duration (wall time). A `setInterval` without clear termination keeps the DO active and billing.

### Pattern: Hibernation-Aware Intervals

```typescript
// DO with safe interval handling
export class SafeTimerDO implements DurableObject {
  private intervalId: ReturnType<typeof setInterval> | null = null;
  private state: DurableObjectState;

  constructor(state: DurableObjectState) {
    this.state = state;
  }

  // BAD: This keeps DO alive forever
  // startBadTimer() {
  //   setInterval(() => this.doWork(), 1000);
  // }

  // GOOD: Alarm-based timing (hibernation compatible)
  async startSafeTimer(intervalMs: number): Promise<void> {
    await this.state.storage.setAlarm(Date.now() + intervalMs);
  }

  async alarm(): Promise<void> {
    await this.doWork();
    // Reschedule only if still needed
    const shouldContinue = await this.checkShouldContinue();
    if (shouldContinue) {
      await this.state.storage.setAlarm(Date.now() + 1000);
    }
    // Otherwise, DO hibernates and stops billing
  }

  private async checkShouldContinue(): Promise<boolean> {
    // Check if there's a reason to keep running
    const activeConnections = await this.state.storage.get('activeConnections');
    return (activeConnections as number) > 0;
  }

  private async doWork(): Promise<void> {
    // Periodic work here
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/start-timer') {
      await this.startSafeTimer(1000);
      return new Response('Timer started with hibernation support');
    }

    return new Response('OK');
  }
}
```

## D1 Loop Protection

Detect and prevent N+1 query patterns that multiply costs.

```typescript
// src/utils/query-batcher.ts

/**
 * Prevents N+1 queries by batching related lookups
 */
export class QueryBatcher<K, V> {
  private pending: Map<K, { resolve: (v: V | null) => void; reject: (e: Error) => void }[]> = new Map();
  private scheduled = false;

  constructor(
    private batchFn: (keys: K[]) => Promise<Map<K, V>>,
    private maxBatchSize = 100,
    private delayMs = 0
  ) {}

  async load(key: K): Promise<V | null> {
    return new Promise((resolve, reject) => {
      const callbacks = this.pending.get(key) ?? [];
      callbacks.push({ resolve, reject });
      this.pending.set(key, callbacks);

      if (!this.scheduled) {
        this.scheduled = true;
        if (this.delayMs > 0) {
          setTimeout(() => this.dispatch(), this.delayMs);
        } else {
          queueMicrotask(() => this.dispatch());
        }
      }
    });
  }

  private async dispatch(): Promise<void> {
    const batch = new Map(this.pending);
    this.pending.clear();
    this.scheduled = false;

    const keys = Array.from(batch.keys()).slice(0, this.maxBatchSize);

    try {
      const results = await this.batchFn(keys);

      for (const [key, callbacks] of batch) {
        const value = results.get(key) ?? null;
        for (const { resolve } of callbacks) {
          resolve(value);
        }
      }
    } catch (error) {
      for (const [, callbacks] of batch) {
        for (const { reject } of callbacks) {
          reject(error as Error);
        }
      }
    }
  }
}

// Usage example - prevents N+1 when fetching user data
const userBatcher = new QueryBatcher<string, User>(async (userIds) => {
  const placeholders = userIds.map(() => '?').join(',');
  const results = await db
    .prepare(`SELECT * FROM users WHERE id IN (${placeholders})`)
    .bind(...userIds)
    .all<User>();

  return new Map(results.results.map(u => [u.id, u]));
});

// Instead of: for (const id of userIds) { await getUser(id); } // N queries
// Use: await Promise.all(userIds.map(id => userBatcher.load(id))); // 1 query
```

## Configuration Templates

### wrangler.jsonc with Loop Protection

```jsonc
{
  "name": "loop-protected-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",

  // Billing Safety: Kill runaway loops fast
  "limits": {
    "cpu_ms": 100
  },

  // Use Service Bindings instead of fetch() chains
  "services": [
    { "binding": "AUTH_SERVICE", "service": "auth-worker" }
  ],

  // Queue with DLQ to break retry loops
  "queues": {
    "consumers": [{
      "queue": "events",
      "max_retries": 1,
      "dead_letter_queue": "events-dlq",
      "max_concurrency": 10
    }]
  },

  // KV for idempotency tracking
  "kv_namespaces": [
    { "binding": "IDEMPOTENCY_KV", "id": "..." }
  ]
}
```

## Detection Checklist

Use this checklist when reviewing code for loop vulnerabilities:

### Static Analysis

- [ ] Search for `fetch(` calls that might hit the same Worker
- [ ] Check for `while(true)` or `for(;;)` without break conditions
- [ ] Look for recursive function calls without depth limits
- [ ] Verify `setInterval` in Durable Objects has termination logic
- [ ] Check D1 queries inside iteration blocks
- [ ] Verify R2 writes are not inside high-frequency loops

### Runtime Protection

- [ ] `limits.cpu_ms` set in wrangler config
- [ ] Recursion depth header middleware applied
- [ ] Queue consumers have idempotency checks
- [ ] DLQ configured for all queues
- [ ] Alarm API used instead of setInterval in DOs

## Anti-Patterns

| Pattern | Risk | Solution |
|---------|------|----------|
| `fetch(request.url)` | Infinite self-call | Use recursion depth header |
| `while (!success)` retry | Unbounded retries | Add max attempts + backoff |
| `setInterval` in DO | Billing never stops | Use alarm API |
| D1 query in `forEach` | N+1 cost explosion | Use QueryBatcher |
| Webhook → same Worker | Recursive billing | Add depth limit |

## Related Skills

- **architect**: Billing Safety Limits section
- **guardian**: Loop-Sensitive Resource Auditing
- **implement**: Queue Consumer with Idempotency
- **patterns/circuit-breaker**: External API loop protection
