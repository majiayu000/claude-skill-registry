---
name: dead-letter-queue
description: Store failed jobs for replay or manual inspection. Track failure patterns, enable manual intervention, and prevent data loss from processing errors.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: workers
  time: 3h
  source: drift-masterguide
---

# Dead Letter Queue

Store failed jobs for replay and debugging.

## When to Use This Skill

- Jobs fail after max retries
- Need visibility into failure patterns
- Want to replay failed jobs manually
- Can't afford to lose failed work

## Core Concepts

1. **Capture context** - Store enough info to replay
2. **Track attempts** - Record all error messages
3. **Enable replay** - Allow manual re-processing
4. **Enforce limits** - Prevent unbounded growth

## TypeScript Implementation

```typescript
// dead-letter-queue.ts
interface DeadLetterJob {
  id: string;
  workerName: string;
  payload: Record<string, unknown>;
  errorMessage: string;
  errorType: string;
  stackTrace?: string;
  attempts: number;
  attemptErrors: string[];
  firstAttemptAt: Date;
  lastAttemptAt: Date;
  createdAt: Date;
  resolvedAt?: Date;
  resolution?: string;
}

class DeadLetterQueue {
  private jobs = new Map<string, DeadLetterJob>();
  private maxSize = 1000;
  private counter = 0;

  add(
    workerName: string,
    payload: Record<string, unknown>,
    errorMessage: string,
    errorType: string,
    attempts: number,
    stackTrace?: string
  ): DeadLetterJob {
    const id = `dlq_${++this.counter}_${Date.now()}`;
    const now = new Date();

    const job: DeadLetterJob = {
      id,
      workerName,
      payload,
      errorMessage,
      errorType,
      stackTrace,
      attempts,
      attemptErrors: [errorMessage],
      firstAttemptAt: now,
      lastAttemptAt: now,
      createdAt: now,
    };

    this.jobs.set(id, job);
    this.enforceMaxSize();
    
    console.log(`[DLQ] Added: ${id} (${workerName})`);
    return job;
  }

  recordAttempt(jobId: string, errorMessage: string): boolean {
    const job = this.jobs.get(jobId);
    if (!job) return false;

    job.attempts++;
    job.lastAttemptAt = new Date();
    job.attemptErrors.push(errorMessage);
    job.errorMessage = errorMessage;
    return true;
  }

  resolve(jobId: string, resolution: string): boolean {
    const job = this.jobs.get(jobId);
    if (!job) return false;

    job.resolvedAt = new Date();
    job.resolution = resolution;
    return true;
  }

  discard(jobId: string): boolean {
    return this.jobs.delete(jobId);
  }

  getUnresolved(): DeadLetterJob[] {
    return Array.from(this.jobs.values())
      .filter(j => !j.resolvedAt)
      .sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
  }

  getReplayable(maxAttempts = 5): DeadLetterJob[] {
    return this.getUnresolved().filter(j => j.attempts < maxAttempts);
  }

  getByWorker(workerName: string): DeadLetterJob[] {
    return this.getUnresolved().filter(j => j.workerName === workerName);
  }

  getStats() {
    const jobs = Array.from(this.jobs.values());
    const unresolved = jobs.filter(j => !j.resolvedAt);
    
    const byWorker: Record<string, number> = {};
    const byErrorType: Record<string, number> = {};
    
    for (const job of unresolved) {
      byWorker[job.workerName] = (byWorker[job.workerName] || 0) + 1;
      byErrorType[job.errorType] = (byErrorType[job.errorType] || 0) + 1;
    }

    return { total: jobs.length, unresolved: unresolved.length, byWorker, byErrorType };
  }

  cleanupResolved(olderThanHours = 24): number {
    const cutoff = Date.now() - olderThanHours * 60 * 60 * 1000;
    let deleted = 0;

    for (const [id, job] of this.jobs) {
      if (job.resolvedAt && job.resolvedAt.getTime() < cutoff) {
        this.jobs.delete(id);
        deleted++;
      }
    }
    return deleted;
  }

  private enforceMaxSize(): void {
    if (this.jobs.size <= this.maxSize) return;

    // Remove oldest resolved first, then oldest unresolved
    const sorted = Array.from(this.jobs.entries())
      .sort((a, b) => {
        if (a[1].resolvedAt && !b[1].resolvedAt) return -1;
        return a[1].createdAt.getTime() - b[1].createdAt.getTime();
      });

    while (sorted.length > this.maxSize) {
      const [id] = sorted.shift()!;
      this.jobs.delete(id);
    }
  }
}

// Singleton
let dlq: DeadLetterQueue | null = null;
export function getDeadLetterQueue(): DeadLetterQueue {
  if (!dlq) dlq = new DeadLetterQueue();
  return dlq;
}
```

## Python Implementation

```python
# dead_letter_queue.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any

@dataclass
class DeadLetterJob:
    id: str
    worker_name: str
    payload: Dict[str, Any]
    error_message: str
    error_type: str
    attempts: int
    attempt_errors: List[str]
    first_attempt_at: datetime
    last_attempt_at: datetime
    created_at: datetime
    stack_trace: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None

class DeadLetterQueue:
    def __init__(self, max_size: int = 1000):
        self._jobs: Dict[str, DeadLetterJob] = {}
        self._max_size = max_size
        self._counter = 0

    def add(
        self,
        worker_name: str,
        payload: Dict[str, Any],
        error_message: str,
        error_type: str,
        attempts: int,
        stack_trace: Optional[str] = None,
    ) -> DeadLetterJob:
        self._counter += 1
        job_id = f"dlq_{self._counter}_{int(datetime.now().timestamp())}"
        now = datetime.now()

        job = DeadLetterJob(
            id=job_id,
            worker_name=worker_name,
            payload=payload,
            error_message=error_message,
            error_type=error_type,
            stack_trace=stack_trace,
            attempts=attempts,
            attempt_errors=[error_message],
            first_attempt_at=now,
            last_attempt_at=now,
            created_at=now,
        )

        self._jobs[job_id] = job
        self._enforce_max_size()
        return job

    def record_attempt(self, job_id: str, error_message: str) -> bool:
        job = self._jobs.get(job_id)
        if not job:
            return False

        job.attempts += 1
        job.last_attempt_at = datetime.now()
        job.attempt_errors.append(error_message)
        job.error_message = error_message
        return True

    def resolve(self, job_id: str, resolution: str) -> bool:
        job = self._jobs.get(job_id)
        if not job:
            return False

        job.resolved_at = datetime.now()
        job.resolution = resolution
        return True

    def get_unresolved(self) -> List[DeadLetterJob]:
        return sorted(
            [j for j in self._jobs.values() if not j.resolved_at],
            key=lambda j: j.created_at,
            reverse=True,
        )

    def get_replayable(self, max_attempts: int = 5) -> List[DeadLetterJob]:
        return [j for j in self.get_unresolved() if j.attempts < max_attempts]

    def get_stats(self) -> Dict[str, Any]:
        unresolved = self.get_unresolved()
        by_worker: Dict[str, int] = {}
        by_error: Dict[str, int] = {}

        for job in unresolved:
            by_worker[job.worker_name] = by_worker.get(job.worker_name, 0) + 1
            by_error[job.error_type] = by_error.get(job.error_type, 0) + 1

        return {
            "total": len(self._jobs),
            "unresolved": len(unresolved),
            "by_worker": by_worker,
            "by_error_type": by_error,
        }

    def _enforce_max_size(self):
        if len(self._jobs) <= self._max_size:
            return

        # Sort: resolved first, then by age
        sorted_jobs = sorted(
            self._jobs.items(),
            key=lambda x: (x[1].resolved_at is None, x[1].created_at),
        )

        while len(sorted_jobs) > self._max_size:
            job_id, _ = sorted_jobs.pop(0)
            del self._jobs[job_id]


# Singleton
_dlq: Optional[DeadLetterQueue] = None

def get_dead_letter_queue() -> DeadLetterQueue:
    global _dlq
    if _dlq is None:
        _dlq = DeadLetterQueue()
    return _dlq
```

## Usage Examples

### Worker Integration

```typescript
const dlq = getDeadLetterQueue();
const MAX_RETRIES = 3;

async function processJob(job: Job) {
  try {
    await doWork(job.payload);
  } catch (error) {
    if (job.attempts >= MAX_RETRIES) {
      dlq.add(
        'my-worker',
        job.payload,
        error.message,
        error.name,
        job.attempts,
        error.stack
      );
    } else {
      throw error; // Let retry mechanism handle it
    }
  }
}
```

### Admin Replay

```typescript
async function replayFailedJobs() {
  const dlq = getDeadLetterQueue();
  const replayable = dlq.getReplayable();
  
  for (const job of replayable) {
    try {
      await processJob({ payload: job.payload, attempts: 0 });
      dlq.resolve(job.id, 'Replayed successfully');
    } catch (e) {
      dlq.recordAttempt(job.id, e.message);
    }
  }
}
```

### Monitoring Endpoint

```typescript
app.get('/admin/dlq/stats', (req, res) => {
  const dlq = getDeadLetterQueue();
  res.json(dlq.getStats());
});

app.get('/admin/dlq/jobs', (req, res) => {
  const dlq = getDeadLetterQueue();
  res.json(dlq.getUnresolved());
});

app.post('/admin/dlq/jobs/:id/replay', async (req, res) => {
  const dlq = getDeadLetterQueue();
  const job = dlq.getUnresolved().find(j => j.id === req.params.id);
  
  if (!job) {
    return res.status(404).json({ error: 'Job not found' });
  }
  
  // Replay logic...
});
```

## Best Practices

1. **Store full context** - Include everything needed to replay
2. **Track all errors** - Keep history of attempt failures
3. **Enforce size limits** - Prevent memory exhaustion
4. **Expose stats** - Monitor failure patterns
5. **Cleanup resolved** - Don't keep forever

## Common Mistakes

- Not storing enough context to replay
- Unbounded queue growth
- No visibility into failure patterns
- Forgetting to cleanup old resolved jobs
- Not tracking attempt history

## Related Skills

- [Background Jobs](../background-jobs/)
- [Error Handling](../error-handling/)
- [Graceful Shutdown](../graceful-shutdown/)
