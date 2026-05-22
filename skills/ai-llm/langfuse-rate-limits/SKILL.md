---
name: langfuse-rate-limits
description: |
  Implement Langfuse rate limiting, batching, and backoff patterns.
  Use when handling rate limit errors, optimizing trace ingestion,
  or managing high-volume LLM observability workloads.
  Trigger with phrases like "langfuse rate limit", "langfuse throttling",
  "langfuse 429", "langfuse batching", "langfuse high volume".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Langfuse Rate Limits

## Overview
Handle Langfuse rate limits gracefully with batching and backoff strategies.

## Prerequisites
- Langfuse SDK installed
- Understanding of async/await patterns
- High-volume trace workload

## Rate Limit Tiers

| Tier | Events/min | Events/hour | Batch Size |
|------|------------|-------------|------------|
| Free | 1,000 | 10,000 | 15 |
| Pro | 10,000 | 100,000 | 50 |
| Enterprise | Custom | Custom | Custom |

## Instructions

### Step 1: Configure Optimal Batching

```typescript
import { Langfuse } from "langfuse";

// High-volume configuration
const langfuse = new Langfuse({
  publicKey: process.env.LANGFUSE_PUBLIC_KEY!,
  secretKey: process.env.LANGFUSE_SECRET_KEY!,
  // Batching settings
  flushAt: 50,           // Batch 50 events before sending
  flushInterval: 5000,   // Or flush every 5 seconds
  // Timeout settings
  requestTimeout: 30000, // 30 second timeout for large batches
});
```

### Step 2: Implement Exponential Backoff

```typescript
interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  jitterMs: number;
}

async function withBackoff<T>(
  operation: () => Promise<T>,
  config: RetryConfig = {
    maxRetries: 5,
    baseDelayMs: 1000,
    maxDelayMs: 30000,
    jitterMs: 500,
  }
): Promise<T> {
  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error: any) {
      if (attempt === config.maxRetries) throw error;

      // Only retry on rate limits (429) or server errors (5xx)
      const status = error.status || error.response?.status;
      if (status !== 429 && (status < 500 || status >= 600)) {
        throw error;
      }

      // Check for Retry-After header
      const retryAfter = error.headers?.get?.("Retry-After");
      let delay: number;

      if (retryAfter) {
        delay = parseInt(retryAfter) * 1000;
      } else {
        // Exponential backoff with jitter
        const exponentialDelay = config.baseDelayMs * Math.pow(2, attempt);
        const jitter = Math.random() * config.jitterMs;
        delay = Math.min(exponentialDelay + jitter, config.maxDelayMs);
      }

      console.warn(
        `Rate limited. Attempt ${attempt + 1}/${config.maxRetries}. ` +
        `Retrying in ${delay}ms...`
      );

      await new Promise((r) => setTimeout(r, delay));
    }
  }

  throw new Error("Unreachable");
}
```

### Step 3: Rate Limit-Aware Wrapper

```typescript
class RateLimitedLangfuse {
  private langfuse: Langfuse;
  private pendingEvents: number = 0;
  private maxConcurrent: number = 100;
  private queue: Array<() => void> = [];

  constructor(config?: ConstructorParameters<typeof Langfuse>[0]) {
    this.langfuse = new Langfuse({
      ...config,
      flushAt: 50,
      flushInterval: 5000,
    });
  }

  private async waitForCapacity(): Promise<void> {
    if (this.pendingEvents < this.maxConcurrent) {
      this.pendingEvents++;
      return;
    }

    return new Promise((resolve) => {
      this.queue.push(() => {
        this.pendingEvents++;
        resolve();
      });
    });
  }

  private releaseCapacity(): void {
    this.pendingEvents--;
    const next = this.queue.shift();
    if (next) next();
  }

  async trace(
    params: Parameters<typeof this.langfuse.trace>[0]
  ): Promise<ReturnType<typeof this.langfuse.trace>> {
    await this.waitForCapacity();
    try {
      return this.langfuse.trace(params);
    } finally {
      this.releaseCapacity();
    }
  }

  async flush(): Promise<void> {
    return this.langfuse.flushAsync();
  }

  async shutdown(): Promise<void> {
    return this.langfuse.shutdownAsync();
  }
}
```

### Step 4: Sampling for High Volume

```typescript
interface SamplingConfig {
  rate: number; // 0.0 to 1.0
  alwaysSample: (trace: TraceParams) => boolean;
}

class SampledLangfuse {
  private langfuse: Langfuse;
  private config: SamplingConfig;

  constructor(
    langfuseConfig: ConstructorParameters<typeof Langfuse>[0],
    samplingConfig: SamplingConfig = { rate: 1.0, alwaysSample: () => false }
  ) {
    this.langfuse = new Langfuse(langfuseConfig);
    this.config = samplingConfig;
  }

  trace(params: Parameters<typeof this.langfuse.trace>[0]) {
    // Always sample errors and specific conditions
    if (this.config.alwaysSample(params)) {
      return this.langfuse.trace(params);
    }

    // Random sampling
    if (Math.random() > this.config.rate) {
      // Return no-op trace
      return createNoOpTrace();
    }

    return this.langfuse.trace({
      ...params,
      metadata: {
        ...params.metadata,
        sampled: true,
        sampleRate: this.config.rate,
      },
    });
  }
}

// Usage: Sample 10% of traces, but always sample errors
const sampledLangfuse = new SampledLangfuse(
  { publicKey: "...", secretKey: "..." },
  {
    rate: 0.1,
    alwaysSample: (params) =>
      params.tags?.includes("error") || params.level === "ERROR",
  }
);
```

## Output
- Optimized batching configuration
- Exponential backoff for rate limits
- Concurrent request limiting
- Sampling for ultra-high volume

## Error Handling
| Header/Error | Description | Action |
|--------------|-------------|--------|
| 429 Too Many Requests | Rate limited | Use exponential backoff |
| Retry-After | Seconds to wait | Honor this value exactly |
| X-RateLimit-Remaining | Requests left | Pre-emptive throttling |
| 503 Service Unavailable | Overloaded | Back off significantly |

## Examples

### Monitor Rate Limit Usage
```typescript
class RateLimitMonitor {
  private remaining: number = 1000;
  private resetAt: Date = new Date();

  updateFromResponse(headers: Headers) {
    const remaining = headers.get("X-RateLimit-Remaining");
    const reset = headers.get("X-RateLimit-Reset");

    if (remaining) this.remaining = parseInt(remaining);
    if (reset) this.resetAt = new Date(parseInt(reset) * 1000);
  }

  shouldThrottle(): boolean {
    return this.remaining < 10 && new Date() < this.resetAt;
  }

  getWaitTime(): number {
    return Math.max(0, this.resetAt.getTime() - Date.now());
  }

  getStatus() {
    return {
      remaining: this.remaining,
      resetAt: this.resetAt.toISOString(),
      shouldThrottle: this.shouldThrottle(),
    };
  }
}
```

### Batch Processing Pattern
```typescript
async function processBatchWithRateLimits(items: any[]) {
  const BATCH_SIZE = 50;
  const DELAY_BETWEEN_BATCHES = 1000; // 1 second

  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE);

    // Process batch
    const traces = batch.map((item) =>
      langfuse.trace({
        name: "batch-item",
        input: item,
      })
    );

    // Flush after each batch
    await langfuse.flushAsync();

    // Delay before next batch
    if (i + BATCH_SIZE < items.length) {
      await new Promise((r) => setTimeout(r, DELAY_BETWEEN_BATCHES));
    }
  }
}
```

### Queue-Based Rate Limiting
```typescript
import PQueue from "p-queue";

// Create rate-limited queue
const queue = new PQueue({
  concurrency: 10,      // Max 10 concurrent requests
  interval: 1000,       // Per second
  intervalCap: 50,      // Max 50 per interval
});

async function queuedTrace(params: TraceParams) {
  return queue.add(() => langfuse.trace(params));
}
```

## Resources
- [Langfuse Rate Limits](https://langfuse.com/docs/api-reference)
- [p-queue Documentation](https://github.com/sindresorhus/p-queue)
- [Langfuse SDK Configuration](https://langfuse.com/docs/sdk)

## Next Steps
For security configuration, see `langfuse-security-basics`.
