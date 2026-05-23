---
name: resilience-engineering
description: Strategies for handling Shopify API Rate Limits (429), retry policies, and circuit breakers. Essential for high-traffic apps.
---

# Resilience Engineering for Shopify Apps

Shopify's API limit is a "Leaky Bucket". If you pour too much too fast, it overflows (429 Too Many Requests). Your app must handle this gracefully.

## 1. Handling Rate Limits (429)

### The "Retry-After" Header
When Shopify returns a 429, they include a `Retry-After` header (seconds to wait).

**Implementation (using `bottleneck` or custom delay)**:
```typescript
async function fetchWithRetry(url, options, retries = 3) {
  try {
    const res = await fetch(url, options);
    if (res.status === 429) {
      const wait = parseFloat(res.headers.get("Retry-After") || "1.0");
      if (retries > 0) {
        await new Promise(r => setTimeout(r, wait * 1000));
        return fetchWithRetry(url, options, retries - 1);
      }
    }
    return res;
  } catch (err) {
    // network error handling
  }
}
```
*Note: The official `@shopify/shopify-api` client handles retries automatically if configured.*

## 2. Queues & Throttling
For bulk operations (e.g., syncing 10,000 products), you cannot just loop and await.

### Using `bottleneck`
```bash
npm install bottleneck
```

```typescript
import Bottleneck from "bottleneck";

const limiter = new Bottleneck({
  minTime: 500, // wait 500ms between requests (2 req/sec)
  maxConcurrent: 5,
});

const products = await limiter.schedule(() => shopify.rest.Product.list({ ... }));
```

### Background Jobs (BullMQ)
Move heavy lifting to a background worker. (See `redis-bullmq` skill - *to be added if needed, but conceptually here*).

## 3. Circuit Breaker
If an external service (e.g., your own backend API or a shipping carrier) goes down, stop calling it to prevent cascading failures.

### Using `cockatiel`
```bash
npm install cockatiel
```

```typescript
import { CircuitBreaker, handleAll, retry } from 'cockatiel';

// Create a Retry Policy
const retryPolicy = retry(handleAll, { maxAttempts: 3, backoff: new ExponentialBackoff() });

// Create a Circuit Breaker (open after 5 failures, reset after 10s)
const circuitBreaker = new CircuitBreaker(handleAll, {
  halfOpenAfter: 10 * 1000,
  breaker: new ConsecutiveBreaker(5),
});

// Execute
const result = await retryPolicy.execute(() => 
  circuitBreaker.execute(() => fetchMyService())
);
```

## 4. Webhook Idempotency
Shopify guarantees "at least once" delivery. You might receive the same `orders/create` webhook twice.
**Fix**: Store `X-Shopify-Webhook-Id` in Redis/DB with a short TTL (e.g., 24h). If it exists, ignore the request.
