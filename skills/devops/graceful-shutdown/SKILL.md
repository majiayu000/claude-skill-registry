---
name: graceful-shutdown
description: Clean shutdown with in-flight job tracking, signal handlers, and buffer draining. Prevent data loss and corrupted state on process termination.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: resilience
  time: 3h
  source: drift-masterguide
---

# Graceful Shutdown

Clean shutdown without data loss.

## When to Use This Skill

- Running background workers
- Processing queues or streams
- Buffering data before persistence
- Any long-running process that handles state

## Core Concepts

1. **Signal handlers** - Catch SIGTERM/SIGINT
2. **In-flight tracking** - Know what's still running
3. **Buffer draining** - Flush before exit
4. **Cleanup callbacks** - Close connections properly

## Shutdown Flow

```
SIGTERM received
      │
      ▼
Stop accepting new work
      │
      ▼
Wait for in-flight jobs
      │
      ▼
Drain buffers
      │
      ▼
Run cleanup callbacks
      │
      ▼
Process exits
```

## TypeScript Implementation

```typescript
// graceful-shutdown.ts
type ShutdownCallback = () => Promise<void>;
type DrainCallback = () => Promise<{ flushed: number; dropped: number }>;

interface InFlightJob {
  id: string;
  workerName: string;
  startedAt: Date;
  timeoutMs: number;
}

class GracefulShutdown {
  private isShuttingDown = false;
  private shutdownPromise: Promise<void> | null = null;
  private callbacks: ShutdownCallback[] = [];
  private drainCallbacks: DrainCallback[] = [];
  private inFlightJobs = new Map<string, InFlightJob>();
  private shutdownTimeoutMs = 30000;

  registerSignals(): void {
    const handler = (signal: string) => {
      console.log(`[Shutdown] Received ${signal}`);
      this.shutdown(`Signal: ${signal}`);
    };

    process.on('SIGTERM', () => handler('SIGTERM'));
    process.on('SIGINT', () => handler('SIGINT'));
  }

  onShutdown(callback: ShutdownCallback): void {
    this.callbacks.push(callback);
  }

  onDrain(callback: DrainCallback): void {
    this.drainCallbacks.push(callback);
  }

  trackJob(id: string, workerName: string, timeoutMs = 60000): void {
    if (this.isShuttingDown) return;
    this.inFlightJobs.set(id, { id, workerName, startedAt: new Date(), timeoutMs });
  }

  completeJob(id: string): void {
    this.inFlightJobs.delete(id);
  }

  isShutdownInProgress(): boolean {
    return this.isShuttingDown;
  }

  async shutdown(reason: string): Promise<void> {
    if (this.shutdownPromise) return this.shutdownPromise;

    this.isShuttingDown = true;
    console.log(`[Shutdown] Starting: ${reason}`);

    this.shutdownPromise = this.performShutdown();
    return this.shutdownPromise;
  }

  private async performShutdown(): Promise<void> {
    const startTime = Date.now();

    // 1. Wait for in-flight jobs
    console.log(`[Shutdown] Waiting for ${this.inFlightJobs.size} jobs...`);
    
    while (this.inFlightJobs.size > 0) {
      if (Date.now() - startTime > this.shutdownTimeoutMs) {
        console.log(`[Shutdown] Timeout! ${this.inFlightJobs.size} jobs still running`);
        break;
      }

      // Force-complete stuck jobs
      const now = Date.now();
      for (const [id, job] of this.inFlightJobs) {
        if (now - job.startedAt.getTime() > job.timeoutMs) {
          console.log(`[Shutdown] Force-completing stuck job: ${id}`);
          this.inFlightJobs.delete(id);
        }
      }

      await this.sleep(100);
    }

    // 2. Drain buffers
    if (this.drainCallbacks.length > 0) {
      console.log(`[Shutdown] Draining ${this.drainCallbacks.length} buffers...`);
      
      let totalFlushed = 0, totalDropped = 0;
      
      for (const drain of this.drainCallbacks) {
        try {
          const result = await Promise.race([
            drain(),
            this.sleep(10000).then(() => ({ flushed: 0, dropped: 0 })),
          ]);
          totalFlushed += result.flushed;
          totalDropped += result.dropped;
        } catch (err) {
          console.error('[Shutdown] Drain error:', err);
        }
      }
      
      console.log(`[Shutdown] Drained: ${totalFlushed} flushed, ${totalDropped} dropped`);
    }

    // 3. Run cleanup callbacks
    console.log(`[Shutdown] Running ${this.callbacks.length} cleanup callbacks...`);
    
    for (const callback of this.callbacks) {
      try {
        await Promise.race([
          callback(),
          this.sleep(5000).then(() => { throw new Error('Callback timeout'); }),
        ]);
      } catch (err) {
        console.error('[Shutdown] Callback error:', err);
      }
    }

    console.log(`[Shutdown] Complete in ${Date.now() - startTime}ms`);
    process.exit(0);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Singleton
let instance: GracefulShutdown | null = null;

export function getShutdownHandler(): GracefulShutdown {
  if (!instance) instance = new GracefulShutdown();
  return instance;
}
```

## Python Implementation

```python
# graceful_shutdown.py
import asyncio
import signal
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Awaitable, Dict, List

@dataclass
class InFlightJob:
    id: str
    worker_name: str
    started_at: datetime
    timeout_seconds: float

ShutdownCallback = Callable[[], Awaitable[None]]
DrainCallback = Callable[[], Awaitable[Dict[str, int]]]

class GracefulShutdown:
    def __init__(self, timeout_seconds: float = 30.0):
        self._is_shutting_down = False
        self._shutdown_task: asyncio.Task | None = None
        self._callbacks: List[ShutdownCallback] = []
        self._drain_callbacks: List[DrainCallback] = []
        self._in_flight: Dict[str, InFlightJob] = {}
        self._timeout = timeout_seconds

    def register_signals(self):
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(self.shutdown(f"Signal: {s.name}"))
            )

    def on_shutdown(self, callback: ShutdownCallback):
        self._callbacks.append(callback)

    def on_drain(self, callback: DrainCallback):
        self._drain_callbacks.append(callback)

    def track_job(self, job_id: str, worker_name: str, timeout_seconds: float = 60.0):
        if self._is_shutting_down:
            return
        self._in_flight[job_id] = InFlightJob(
            id=job_id,
            worker_name=worker_name,
            started_at=datetime.now(),
            timeout_seconds=timeout_seconds,
        )

    def complete_job(self, job_id: str):
        self._in_flight.pop(job_id, None)

    @property
    def is_shutting_down(self) -> bool:
        return self._is_shutting_down

    async def shutdown(self, reason: str):
        if self._shutdown_task:
            return await self._shutdown_task

        self._is_shutting_down = True
        print(f"[Shutdown] Starting: {reason}")
        
        self._shutdown_task = asyncio.create_task(self._perform_shutdown())
        return await self._shutdown_task

    async def _perform_shutdown(self):
        start_time = datetime.now()

        # Wait for in-flight jobs
        print(f"[Shutdown] Waiting for {len(self._in_flight)} jobs...")
        
        while self._in_flight:
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > self._timeout:
                print(f"[Shutdown] Timeout! {len(self._in_flight)} jobs still running")
                break

            # Force-complete stuck jobs
            now = datetime.now()
            stuck = [
                job_id for job_id, job in self._in_flight.items()
                if (now - job.started_at).total_seconds() > job.timeout_seconds
            ]
            for job_id in stuck:
                print(f"[Shutdown] Force-completing stuck job: {job_id}")
                self._in_flight.pop(job_id)

            await asyncio.sleep(0.1)

        # Drain buffers
        for drain in self._drain_callbacks:
            try:
                result = await asyncio.wait_for(drain(), timeout=10.0)
                print(f"[Shutdown] Drained: {result}")
            except Exception as e:
                print(f"[Shutdown] Drain error: {e}")

        # Run cleanup callbacks
        for callback in self._callbacks:
            try:
                await asyncio.wait_for(callback(), timeout=5.0)
            except Exception as e:
                print(f"[Shutdown] Callback error: {e}")

        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"[Shutdown] Complete in {elapsed:.1f}s")


# Singleton
_instance: GracefulShutdown | None = None

def get_shutdown_handler() -> GracefulShutdown:
    global _instance
    if _instance is None:
        _instance = GracefulShutdown()
    return _instance
```

## Usage Examples

### Basic Setup

```typescript
const shutdown = getShutdownHandler();
shutdown.registerSignals();

// Register cleanup
shutdown.onShutdown(async () => {
  await database.close();
  await redis.quit();
});

// Register buffer drain
shutdown.onDrain(async () => {
  return backpressureBuffer.flush();
});
```

### Job Tracking

```typescript
async function processJob(jobId: string) {
  const shutdown = getShutdownHandler();
  
  // Don't start new work during shutdown
  if (shutdown.isShutdownInProgress()) {
    return;
  }
  
  shutdown.trackJob(jobId, 'my-worker', 30000);
  
  try {
    await doWork(jobId);
  } finally {
    shutdown.completeJob(jobId);
  }
}
```

### With Express/Fastify

```typescript
const shutdown = getShutdownHandler();
shutdown.registerSignals();

// Stop accepting new requests
shutdown.onShutdown(async () => {
  await new Promise<void>((resolve) => {
    server.close(() => resolve());
  });
});

// Close database connections
shutdown.onShutdown(async () => {
  await prisma.$disconnect();
});
```

## Best Practices

1. **Register signals early** - First thing in app startup
2. **Track all in-flight work** - With appropriate timeouts
3. **Drain before cleanup** - Buffers first, connections last
4. **Set reasonable timeouts** - Don't hang forever
5. **Check before new work** - Don't start during shutdown

## Common Mistakes

- Not registering signal handlers
- Starting new work during shutdown
- No timeout on cleanup callbacks
- Forgetting to track in-flight jobs
- Closing connections before draining buffers

## Related Skills

- [Background Jobs](../background-jobs/)
- [Backpressure](../backpressure/)
- [Health Checks](../health-checks/)
