---
name: backpressure
description: Manage data flow when producers outpace consumers. Bounded buffers, adaptive flushing, and graceful degradation prevent OOM crashes and data loss.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: resilience
  time: 4h
  source: drift-masterguide
---

# Backpressure Management

Prevent OOM crashes when producers outpace consumers.

## When to Use This Skill

- Database writes slower than event ingestion
- Memory filling up with queued items
- Need to handle traffic spikes gracefully
- Want to drop low-priority data under load

## Core Concepts

1. **Bounded buffer** - Fixed-size queue prevents unbounded growth
2. **Watermarks** - Thresholds trigger state changes
3. **Strategies** - Block, drop oldest, drop newest, or sample
4. **Adaptive flushing** - Adjust rate based on downstream health

## State Machine

```
NORMAL (< 50%) → ELEVATED (50-80%) → CRITICAL (80-100%) → BLOCKED (100%)
     ↑                                                          │
     └──────────────────────────────────────────────────────────┘
                        (buffer drains)
```

## TypeScript Implementation

### Types

```typescript
// types.ts
export enum BackpressureState {
  NORMAL = 'normal',
  ELEVATED = 'elevated',
  CRITICAL = 'critical',
  BLOCKED = 'blocked',
  DRAINING = 'draining',
}

export enum BackpressureStrategy {
  BLOCK = 'block',
  DROP_OLDEST = 'drop_oldest',
  DROP_NEWEST = 'drop_newest',
  SAMPLE = 'sample',
}

export interface BackpressureConfig {
  maxBufferSize: number;
  highWatermark: number;     // 0-1
  lowWatermark: number;      // 0-1
  strategy: BackpressureStrategy;
  sampleRate?: number;
  maxBlockTimeMs?: number;
  batchSize: number;
  minFlushIntervalMs: number;
  maxFlushIntervalMs: number;
  targetLatencyMs: number;
}

export interface FlushResult {
  success: number;
  failed: number;
  errors: Error[];
}

export type FlushFunction<T> = (items: T[]) => Promise<FlushResult>;
```

### Bounded Buffer

```typescript
// buffer.ts
export class BoundedBuffer<T> {
  private items: T[] = [];
  
  constructor(private readonly maxSize: number) {}

  get size(): number { return this.items.length; }
  get capacity(): number { return this.maxSize; }
  get utilization(): number { return this.items.length / this.maxSize; }
  
  isFull(): boolean { return this.items.length >= this.maxSize; }
  isEmpty(): boolean { return this.items.length === 0; }

  push(item: T): boolean {
    if (this.isFull()) return false;
    this.items.push(item);
    return true;
  }

  pushWithEviction(item: T): T | null {
    const evicted = this.isFull() ? this.items.shift() ?? null : null;
    this.items.push(item);
    return evicted;
  }

  take(count: number): T[] {
    return this.items.splice(0, Math.min(count, this.items.length));
  }

  clear(): T[] {
    const all = this.items;
    this.items = [];
    return all;
  }
}
```

### Backpressure Controller

```typescript
// controller.ts
import { BoundedBuffer } from './buffer';
import {
  BackpressureState,
  BackpressureStrategy,
  BackpressureConfig,
  FlushFunction,
} from './types';

const DEFAULT_CONFIG: BackpressureConfig = {
  maxBufferSize: 10000,
  highWatermark: 0.8,
  lowWatermark: 0.5,
  strategy: BackpressureStrategy.DROP_OLDEST,
  batchSize: 100,
  minFlushIntervalMs: 100,
  maxFlushIntervalMs: 30000,
  targetLatencyMs: 500,
};

export class BackpressureController<T> {
  private buffer: BoundedBuffer<T>;
  private state: BackpressureState = BackpressureState.NORMAL;
  private config: BackpressureConfig;
  private flushFn: FlushFunction<T>;
  private flushInterval: NodeJS.Timeout | null = null;
  private currentFlushIntervalMs: number;
  private running = false;

  // Metrics
  private eventsAccepted = 0;
  private eventsDropped = 0;
  private eventsFlushed = 0;
  private lastFlushLatencyMs = 0;

  constructor(flushFn: FlushFunction<T>, config: Partial<BackpressureConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.buffer = new BoundedBuffer(this.config.maxBufferSize);
    this.flushFn = flushFn;
    this.currentFlushIntervalMs = this.config.minFlushIntervalMs;
  }

  start(): void {
    if (this.running) return;
    this.running = true;
    this.scheduleFlush();
  }

  stop(): void {
    this.running = false;
    if (this.flushInterval) {
      clearTimeout(this.flushInterval);
      this.flushInterval = null;
    }
  }

  async push(item: T): Promise<boolean> {
    switch (this.config.strategy) {
      case BackpressureStrategy.BLOCK:
        if (this.state === BackpressureState.BLOCKED) {
          const waited = await this.waitForSpace();
          if (!waited) {
            this.eventsDropped++;
            return false;
          }
        }
        break;

      case BackpressureStrategy.DROP_NEWEST:
        if (this.buffer.isFull()) {
          this.eventsDropped++;
          return false;
        }
        break;

      case BackpressureStrategy.DROP_OLDEST:
        if (this.buffer.isFull()) {
          this.buffer.pushWithEviction(item);
          this.eventsDropped++;
          this.eventsAccepted++;
          this.updateState();
          return true;
        }
        break;

      case BackpressureStrategy.SAMPLE:
        if (this.state !== BackpressureState.NORMAL) {
          const sampleRate = this.config.sampleRate || 10;
          if (this.eventsAccepted % sampleRate !== 0) {
            this.eventsDropped++;
            return false;
          }
        }
        break;
    }

    const accepted = this.buffer.push(item);
    if (accepted) {
      this.eventsAccepted++;
    } else {
      this.eventsDropped++;
    }

    this.updateState();
    return accepted;
  }

  async drain(): Promise<void> {
    this.state = BackpressureState.DRAINING;
    while (!this.buffer.isEmpty()) {
      await this.flush();
    }
  }

  getMetrics() {
    return {
      state: this.state,
      bufferSize: this.buffer.size,
      bufferUtilization: this.buffer.utilization,
      eventsAccepted: this.eventsAccepted,
      eventsDropped: this.eventsDropped,
      eventsFlushed: this.eventsFlushed,
      lastFlushLatencyMs: this.lastFlushLatencyMs,
    };
  }

  private async flush(): Promise<void> {
    if (this.buffer.isEmpty()) return;

    const batch = this.buffer.take(this.config.batchSize);
    const startTime = Date.now();

    try {
      const result = await this.flushFn(batch);
      this.eventsFlushed += result.success;
      this.lastFlushLatencyMs = Date.now() - startTime;
      this.adaptFlushInterval();
    } catch (error) {
      console.error('[Backpressure] Flush error:', error);
    }

    this.updateState();
  }

  private scheduleFlush(): void {
    if (!this.running) return;
    this.flushInterval = setTimeout(async () => {
      await this.flush();
      this.scheduleFlush();
    }, this.currentFlushIntervalMs);
  }

  private adaptFlushInterval(): void {
    const { targetLatencyMs, minFlushIntervalMs, maxFlushIntervalMs } = this.config;

    if (this.lastFlushLatencyMs > targetLatencyMs * 1.5) {
      this.currentFlushIntervalMs = Math.min(
        this.currentFlushIntervalMs * 1.5,
        maxFlushIntervalMs
      );
    } else if (this.lastFlushLatencyMs < targetLatencyMs * 0.5) {
      this.currentFlushIntervalMs = Math.max(
        this.currentFlushIntervalMs * 0.8,
        minFlushIntervalMs
      );
    }
  }

  private updateState(): void {
    const util = this.buffer.utilization;
    
    if (this.state === BackpressureState.DRAINING) return;
    
    if (util >= 1.0) {
      this.state = BackpressureState.BLOCKED;
    } else if (util >= this.config.highWatermark) {
      this.state = BackpressureState.CRITICAL;
    } else if (util >= this.config.lowWatermark) {
      this.state = BackpressureState.ELEVATED;
    } else {
      this.state = BackpressureState.NORMAL;
    }
  }

  private async waitForSpace(): Promise<boolean> {
    const maxWait = this.config.maxBlockTimeMs || 5000;
    const startTime = Date.now();

    while (Date.now() - startTime < maxWait) {
      if (!this.buffer.isFull()) return true;
      await new Promise(r => setTimeout(r, 50));
    }
    return false;
  }
}
```

## Usage Examples

```typescript
// Create controller
const controller = new BackpressureController(
  async (items) => {
    const result = await db.batchInsert('events', items);
    return { success: result.inserted, failed: 0, errors: [] };
  },
  {
    strategy: BackpressureStrategy.DROP_OLDEST,
    maxBufferSize: 10000,
    batchSize: 100,
  }
);

// Start processing
controller.start();

// Push events
await controller.push(event);

// On shutdown
await controller.drain();
controller.stop();
```

## Strategy Selection

| Strategy | Use Case | Trade-off |
|----------|----------|-----------|
| BLOCK | Critical data | Producers slow down |
| DROP_OLDEST | Time-series | Lose historical data |
| DROP_NEWEST | Batch jobs | Reject new work |
| SAMPLE | Telemetry | Statistical accuracy |

## Best Practices

1. **Size buffers for memory** - Don't exceed available RAM
2. **Match strategy to data** - Critical data = BLOCK
3. **Monitor drop rates** - Alert on high drops
4. **Drain on shutdown** - Don't lose buffered data
5. **Combine with circuit breaker** - Protect flush function

## Common Mistakes

- Unbounded queues (OOM crash)
- No metrics on drops
- Not draining on shutdown
- Wrong strategy for data criticality
- No adaptive rate adjustment

## Related Skills

- [Circuit Breaker](../circuit-breaker/)
- [Background Jobs](../background-jobs/)
- [Health Checks](../health-checks/)
