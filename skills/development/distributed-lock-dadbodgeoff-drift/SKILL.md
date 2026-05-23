---
name: distributed-lock
description: Prevent race conditions across multiple instances. Only one instance can hold a lock at a time. Automatic expiration prevents deadlocks.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: resilience
  time: 3h
  source: drift-masterguide
---

# Distributed Locking

Prevent race conditions across multiple instances.

## When to Use This Skill

- Multiple instances processing the same job
- Need to prevent duplicate operations
- Singleton cron jobs across instances
- Critical sections in distributed systems

## Core Concepts

1. **Atomic acquisition** - Only one holder at a time
2. **TTL expiration** - Prevents deadlocks if holder crashes
3. **Lock extension** - Renew for long-running operations
4. **Holder ID** - Track who owns the lock

## TypeScript Implementation

### Types

```typescript
// types.ts
export interface LockInfo {
  lockName: string;
  holderId: string;
  acquiredAt: Date;
  expiresAt: Date;
  metadata?: Record<string, unknown>;
}

export interface LockOptions {
  timeoutSeconds?: number;
  blocking?: boolean;
  blockingTimeoutSeconds?: number;
  metadata?: Record<string, unknown>;
}

export interface LockResult {
  acquired: boolean;
  lock?: LockInfo;
  error?: string;
}
```

### In-Memory Lock (Single Instance)

```typescript
// distributed-lock.ts
import { LockInfo, LockOptions, LockResult } from './types';

const lockStore = new Map<string, LockInfo>();

export class DistributedLock {
  private holderId: string;
  private heldLocks = new Map<string, LockInfo>();

  constructor() {
    this.holderId = `worker_${Date.now()}_${Math.random().toString(36).slice(2)}`;
  }

  async acquire(lockName: string, options: LockOptions = {}): Promise<LockResult> {
    const { timeoutSeconds = 30, blocking = false, blockingTimeoutSeconds = 10 } = options;

    const now = new Date();
    const expiresAt = new Date(now.getTime() + timeoutSeconds * 1000);

    // Clean expired locks
    for (const [name, lock] of lockStore) {
      if (lock.expiresAt <= now) lockStore.delete(name);
    }

    const existing = lockStore.get(lockName);
    
    if (existing && existing.expiresAt > now) {
      if (existing.holderId === this.holderId) {
        // Extend our own lock
        existing.expiresAt = expiresAt;
        return { acquired: true, lock: existing };
      }

      if (blocking) {
        return this.waitForLock(lockName, options);
      }

      return { acquired: false, error: `Lock held by ${existing.holderId}` };
    }

    const lock: LockInfo = {
      lockName,
      holderId: this.holderId,
      acquiredAt: now,
      expiresAt,
      metadata: options.metadata,
    };

    lockStore.set(lockName, lock);
    this.heldLocks.set(lockName, lock);

    return { acquired: true, lock };
  }

  async release(lockName: string): Promise<boolean> {
    const lock = lockStore.get(lockName);
    if (!lock || lock.holderId !== this.holderId) return false;

    lockStore.delete(lockName);
    this.heldLocks.delete(lockName);
    return true;
  }

  async extend(lockName: string, additionalSeconds: number): Promise<boolean> {
    const lock = lockStore.get(lockName);
    if (!lock || lock.holderId !== this.holderId) return false;

    lock.expiresAt = new Date(Date.now() + additionalSeconds * 1000);
    return true;
  }

  async withLock<T>(
    lockName: string,
    fn: () => Promise<T>,
    options: LockOptions = {}
  ): Promise<T> {
    const result = await this.acquire(lockName, options);
    if (!result.acquired) {
      throw new Error(`Failed to acquire lock: ${lockName}`);
    }

    try {
      return await fn();
    } finally {
      await this.release(lockName);
    }
  }

  private async waitForLock(lockName: string, options: LockOptions): Promise<LockResult> {
    const timeout = (options.blockingTimeoutSeconds || 10) * 1000;
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      await new Promise(r => setTimeout(r, 100));
      const result = await this.acquire(lockName, { ...options, blocking: false });
      if (result.acquired) return result;
    }

    return { acquired: false, error: 'Timeout waiting for lock' };
  }

  async releaseAll(): Promise<void> {
    for (const lockName of this.heldLocks.keys()) {
      await this.release(lockName);
    }
  }
}

// Singleton
let instance: DistributedLock | null = null;
export function getDistributedLock(): DistributedLock {
  if (!instance) instance = new DistributedLock();
  return instance;
}
```

### PostgreSQL Lock (Multi-Instance)

```sql
-- migrations/distributed_locks.sql

CREATE TABLE distributed_locks (
    lock_name VARCHAR(255) PRIMARY KEY,
    holder_id VARCHAR(255) NOT NULL,
    acquired_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_locks_expires ON distributed_locks(expires_at);

-- Atomic lock acquisition
CREATE OR REPLACE FUNCTION acquire_lock(
    p_lock_name VARCHAR(255),
    p_holder_id VARCHAR(255),
    p_ttl_seconds INTEGER DEFAULT 30,
    p_metadata JSONB DEFAULT '{}'
) RETURNS BOOLEAN AS $$
DECLARE
    v_now TIMESTAMPTZ := NOW();
    v_expires_at TIMESTAMPTZ := v_now + (p_ttl_seconds || ' seconds')::INTERVAL;
BEGIN
    -- Clean expired
    DELETE FROM distributed_locks 
    WHERE lock_name = p_lock_name AND expires_at < v_now;
    
    -- Try to acquire
    INSERT INTO distributed_locks (lock_name, holder_id, acquired_at, expires_at, metadata)
    VALUES (p_lock_name, p_holder_id, v_now, v_expires_at, p_metadata)
    ON CONFLICT (lock_name) DO UPDATE
    SET holder_id = EXCLUDED.holder_id,
        acquired_at = EXCLUDED.acquired_at,
        expires_at = EXCLUDED.expires_at
    WHERE distributed_locks.holder_id = p_holder_id
       OR distributed_locks.expires_at < v_now;
    
    RETURN EXISTS (
        SELECT 1 FROM distributed_locks 
        WHERE lock_name = p_lock_name AND holder_id = p_holder_id
    );
END;
$$ LANGUAGE plpgsql;

-- Release lock
CREATE OR REPLACE FUNCTION release_lock(
    p_lock_name VARCHAR(255),
    p_holder_id VARCHAR(255)
) RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM distributed_locks 
    WHERE lock_name = p_lock_name AND holder_id = p_holder_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;
```

## Python Implementation

```python
# distributed_lock.py
import time
import uuid
from dataclasses import dataclass
from typing import Optional, Callable, TypeVar
from contextlib import asynccontextmanager

T = TypeVar('T')

@dataclass
class LockInfo:
    lock_name: str
    holder_id: str
    acquired_at: float
    expires_at: float

class DistributedLock:
    def __init__(self, db):
        self.db = db
        self.holder_id = f"worker_{uuid.uuid4().hex[:8]}"
    
    async def acquire(
        self,
        lock_name: str,
        timeout_seconds: int = 30
    ) -> bool:
        result = await self.db.execute(
            "SELECT acquire_lock($1, $2, $3)",
            lock_name, self.holder_id, timeout_seconds
        )
        return result[0][0]
    
    async def release(self, lock_name: str) -> bool:
        result = await self.db.execute(
            "SELECT release_lock($1, $2)",
            lock_name, self.holder_id
        )
        return result[0][0]
    
    @asynccontextmanager
    async def lock(self, lock_name: str, timeout_seconds: int = 30):
        acquired = await self.acquire(lock_name, timeout_seconds)
        if not acquired:
            raise Exception(f"Failed to acquire lock: {lock_name}")
        try:
            yield
        finally:
            await self.release(lock_name)

# Usage
async with lock.lock("job:123"):
    await process_job("123")
```

## Usage Examples

### Basic Lock

```typescript
const lock = getDistributedLock();

const result = await lock.acquire('process-payment:order-123');

if (result.acquired) {
  try {
    await processPayment('order-123');
  } finally {
    await lock.release('process-payment:order-123');
  }
} else {
  console.log('Another instance is processing this order');
}
```

### With Context Manager

```typescript
await lock.withLock('daily-report', async () => {
  await generateDailyReport();
}, { timeoutSeconds: 300 });
```

### Long-Running Job with Extension

```typescript
async function processJob(jobId: string) {
  const lock = getDistributedLock();
  
  const result = await lock.acquire(`job:${jobId}`, { timeoutSeconds: 60 });
  if (!result.acquired) return;

  try {
    // Extend lock periodically for long jobs
    const extendInterval = setInterval(async () => {
      await lock.extend(`job:${jobId}`, 60);
    }, 30000);

    await doExpensiveWork(jobId);

    clearInterval(extendInterval);
  } finally {
    await lock.release(`job:${jobId}`);
  }
}
```

### Singleton Cron Job

```typescript
async function runScheduledTask() {
  const lock = getDistributedLock();
  
  const result = await lock.acquire('cron:daily-cleanup', {
    timeoutSeconds: 3600,
  });

  if (!result.acquired) {
    console.log('Another instance is running daily cleanup');
    return;
  }

  try {
    await performDailyCleanup();
  } finally {
    await lock.release('cron:daily-cleanup');
  }
}
```

## Lock Naming Conventions

```typescript
// Resource-based
`lock:user:${userId}:profile-update`
`lock:order:${orderId}:process`

// Job-based
`job:${jobType}:${jobId}`

// Singleton operations
`cron:${taskName}`
`singleton:cache-refresh`
```

## Best Practices

1. **Set appropriate TTL** - Match operation duration
2. **Extend for long ops** - Don't let locks expire mid-operation
3. **Unique holder IDs** - Per instance, not per request
4. **Release in finally** - Always release, even on error
5. **Use withLock** - Automatic acquire/release

## Common Mistakes

- TTL too short for operation
- Not extending long-running locks
- Forgetting to release on error
- Same holder ID across instances
- Not handling acquisition failure

## Related Skills

- [Background Jobs](../background-jobs/)
- [Circuit Breaker](../circuit-breaker/)
- [Idempotency](../idempotency/)
