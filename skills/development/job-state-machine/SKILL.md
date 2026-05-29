---
name: job-state-machine
description: Async job processing with validated state transitions, progress tracking, and asset linking. Ensure jobs always reach terminal states with proper error handling.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: workers
  time: 4h
  source: drift-masterguide
---

# Job State Machine

Validated state transitions for async jobs.

## When to Use This Skill

- Processing async jobs (image generation, exports, etc.)
- Need progress tracking for long operations
- Want to link created assets to jobs
- Need reliable state management

## Core Concepts

1. **Defined states** - QUEUED → PROCESSING → COMPLETED/FAILED/PARTIAL
2. **Valid transitions** - Only allowed state changes
3. **Terminal states** - Jobs must reach an end state
4. **Asset linking** - Track outputs created by jobs

## State Machine

```
         QUEUED
            │
            ▼
       PROCESSING
       /    |    \
      ▼     ▼     ▼
COMPLETED PARTIAL FAILED
   (terminal states)
```

## TypeScript Implementation

### Types

```typescript
// types.ts
export enum JobStatus {
  QUEUED = 'queued',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  PARTIAL = 'partial',
}

export const VALID_TRANSITIONS: Record<JobStatus, JobStatus[]> = {
  [JobStatus.QUEUED]: [JobStatus.PROCESSING],
  [JobStatus.PROCESSING]: [JobStatus.COMPLETED, JobStatus.PARTIAL, JobStatus.FAILED],
  [JobStatus.COMPLETED]: [],
  [JobStatus.FAILED]: [],
  [JobStatus.PARTIAL]: [],
};

export function isTerminalState(status: JobStatus): boolean {
  return VALID_TRANSITIONS[status].length === 0;
}

export interface Job {
  id: string;
  userId: string;
  jobType: string;
  status: JobStatus;
  progress: number;
  errorMessage?: string;
  parameters?: Record<string, unknown>;
  result?: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
  completedAt?: Date;
}

export interface Asset {
  id: string;
  jobId: string;
  userId: string;
  assetType: string;
  url: string;
  storagePath: string;
  fileSize: number;
  createdAt: Date;
}
```

### Job Service

```typescript
// job-service.ts
import { Job, JobStatus, Asset, VALID_TRANSITIONS, isTerminalState } from './types';

export class InvalidStateTransitionError extends Error {
  constructor(public currentStatus: JobStatus, public targetStatus: JobStatus) {
    super(`Cannot transition from '${currentStatus}' to '${targetStatus}'`);
    this.name = 'InvalidStateTransitionError';
  }
}

export class JobService {
  constructor(private db: Database) {}

  async createJob(
    userId: string,
    jobType: string,
    parameters?: Record<string, unknown>
  ): Promise<Job> {
    const job: Job = {
      id: crypto.randomUUID(),
      userId,
      jobType,
      status: JobStatus.QUEUED,
      progress: 0,
      parameters,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    await this.db.jobs.insert(job);
    return job;
  }

  async getJob(jobId: string, userId: string): Promise<Job> {
    const job = await this.db.jobs.findOne({ id: jobId });
    if (!job) throw new Error('Job not found');
    if (job.userId !== userId) throw new Error('Unauthorized');
    return job;
  }

  async transitionStatus(
    jobId: string,
    targetStatus: JobStatus,
    options: {
      progress?: number;
      errorMessage?: string;
      result?: Record<string, unknown>;
    } = {}
  ): Promise<Job> {
    const job = await this.db.jobs.findOne({ id: jobId });
    if (!job) throw new Error('Job not found');

    // Allow same-state for progress updates
    if (job.status !== targetStatus) {
      if (!VALID_TRANSITIONS[job.status].includes(targetStatus)) {
        throw new InvalidStateTransitionError(job.status, targetStatus);
      }
    }

    const updates: Partial<Job> = {
      status: targetStatus,
      progress: options.progress ?? job.progress,
      updatedAt: new Date(),
    };

    if (options.errorMessage !== undefined) {
      updates.errorMessage = options.errorMessage;
    }

    if (options.result !== undefined) {
      updates.result = options.result;
    }

    if (isTerminalState(targetStatus)) {
      updates.completedAt = new Date();
    }

    await this.db.jobs.update({ id: jobId }, updates);
    return { ...job, ...updates };
  }

  async updateProgress(jobId: string, progress: number): Promise<Job> {
    const job = await this.db.jobs.findOne({ id: jobId });
    if (!job) throw new Error('Job not found');

    if (job.status !== JobStatus.PROCESSING) {
      console.warn(`Ignoring progress update for job ${jobId} in ${job.status} state`);
      return job;
    }

    return this.transitionStatus(jobId, JobStatus.PROCESSING, { progress });
  }

  async markCompleted(jobId: string, result?: Record<string, unknown>): Promise<Job> {
    return this.transitionStatus(jobId, JobStatus.COMPLETED, { progress: 100, result });
  }

  async markFailed(jobId: string, errorMessage: string): Promise<Job> {
    return this.transitionStatus(jobId, JobStatus.FAILED, { errorMessage });
  }

  async markPartial(
    jobId: string,
    result?: Record<string, unknown>,
    errorMessage?: string
  ): Promise<Job> {
    return this.transitionStatus(jobId, JobStatus.PARTIAL, {
      progress: 100,
      result,
      errorMessage,
    });
  }

  async createAsset(
    jobId: string,
    userId: string,
    assetType: string,
    url: string,
    storagePath: string,
    fileSize: number
  ): Promise<Asset> {
    const asset: Asset = {
      id: crypto.randomUUID(),
      jobId,
      userId,
      assetType,
      url,
      storagePath,
      fileSize,
      createdAt: new Date(),
    };

    await this.db.assets.insert(asset);
    return asset;
  }

  async getJobAssets(jobId: string, userId: string): Promise<Asset[]> {
    await this.getJob(jobId, userId); // Verify ownership
    return this.db.assets.find({ jobId });
  }
}
```

## Python Implementation

```python
# job_service.py
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import uuid4

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"

VALID_TRANSITIONS = {
    JobStatus.QUEUED: [JobStatus.PROCESSING],
    JobStatus.PROCESSING: [JobStatus.COMPLETED, JobStatus.PARTIAL, JobStatus.FAILED],
    JobStatus.COMPLETED: [],
    JobStatus.FAILED: [],
    JobStatus.PARTIAL: [],
}

def is_terminal_state(status: JobStatus) -> bool:
    return len(VALID_TRANSITIONS.get(status, [])) == 0

@dataclass
class Job:
    id: str
    user_id: str
    job_type: str
    status: JobStatus
    progress: int
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    completed_at: Optional[datetime] = None

class InvalidStateTransitionError(Exception):
    def __init__(self, current: JobStatus, target: JobStatus):
        self.current = current
        self.target = target
        super().__init__(f"Cannot transition from '{current}' to '{target}'")

class JobService:
    def __init__(self, db):
        self.db = db

    async def create_job(
        self,
        user_id: str,
        job_type: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Job:
        now = datetime.utcnow()
        job = Job(
            id=str(uuid4()),
            user_id=user_id,
            job_type=job_type,
            status=JobStatus.QUEUED,
            progress=0,
            parameters=parameters,
            created_at=now,
            updated_at=now,
        )
        await self.db.jobs.insert(job)
        return job

    async def transition_status(
        self,
        job_id: str,
        target_status: JobStatus,
        progress: Optional[int] = None,
        error_message: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None,
    ) -> Job:
        job = await self.db.jobs.find_one(id=job_id)
        if not job:
            raise ValueError("Job not found")

        if job.status != target_status:
            if target_status not in VALID_TRANSITIONS.get(job.status, []):
                raise InvalidStateTransitionError(job.status, target_status)

        job.status = target_status
        job.updated_at = datetime.utcnow()
        
        if progress is not None:
            job.progress = progress
        if error_message is not None:
            job.error_message = error_message
        if result is not None:
            job.result = result
        if is_terminal_state(target_status):
            job.completed_at = datetime.utcnow()

        await self.db.jobs.update(job)
        return job

    async def mark_completed(self, job_id: str, result: Optional[Dict] = None) -> Job:
        return await self.transition_status(
            job_id, JobStatus.COMPLETED, progress=100, result=result
        )

    async def mark_failed(self, job_id: str, error_message: str) -> Job:
        return await self.transition_status(
            job_id, JobStatus.FAILED, error_message=error_message
        )
```

## Worker Integration

```typescript
async function processJob(jobId: string) {
  const jobService = getJobService();

  try {
    // Transition to PROCESSING
    await jobService.transitionStatus(jobId, JobStatus.PROCESSING, { progress: 0 });

    const job = await jobService.getJobInternal(jobId);

    // Process with progress updates
    await jobService.updateProgress(jobId, 25);
    const result1 = await doStep1(job.parameters);

    await jobService.updateProgress(jobId, 50);
    const result2 = await doStep2(result1);

    await jobService.updateProgress(jobId, 75);
    const assetUrl = await uploadResult(result2);

    // Create asset
    await jobService.createAsset(
      jobId,
      job.userId,
      job.jobType,
      assetUrl,
      `${job.userId}/${jobId}/result.png`,
      result2.length
    );

    // Mark completed
    await jobService.markCompleted(jobId, { assetCount: 1 });

  } catch (error) {
    console.error(`Job ${jobId} failed:`, error);
    await jobService.markFailed(jobId, error.message);
  }
}
```

## Database Schema

```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'queued',
    progress INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    parameters JSONB,
    result JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    
    CONSTRAINT valid_status CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'partial')),
    CONSTRAINT valid_progress CHECK (progress >= 0 AND progress <= 100)
);

CREATE INDEX idx_jobs_user_status ON jobs(user_id, status);

CREATE TABLE assets (
    id UUID PRIMARY KEY,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    asset_type VARCHAR(50) NOT NULL,
    url TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_assets_job_id ON assets(job_id);
```

## Best Practices

1. **Validate all transitions** - Never skip state machine validation
2. **Always reach terminal** - Jobs must complete, fail, or partial
3. **Track progress** - Provide feedback for long operations
4. **Link assets** - Maintain relationship for cleanup
5. **Log transitions** - Essential for debugging

## Common Mistakes

- Allowing invalid state transitions
- Jobs stuck in non-terminal states
- Not tracking progress for long jobs
- Orphaned assets without job links
- Missing error messages on failure

## Related Skills

- [Background Jobs](../background-jobs/)
- [Dead Letter Queue](../dead-letter-queue/)
- [Graceful Shutdown](../graceful-shutdown/)
