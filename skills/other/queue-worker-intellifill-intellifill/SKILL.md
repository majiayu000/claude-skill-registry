---
name: queue-worker
description: Bull queue setup, worker processes, job lifecycle, error handling, retries, progress reporting, Redis connection management, and queue patterns for OCR and knowledge processing
version: 1.0.0
lastUpdated: 2025-12-12
---

# Queue Worker Skill - IntelliFill

This skill covers Bull queue implementation patterns, worker processes, job lifecycle management, error handling, retries, progress reporting, and Redis connection management in the IntelliFill project.

---

## Table of Contents

1. [Overview](#overview)
2. [Queue Architecture](#queue-architecture)
3. [Bull Queue Setup](#bull-queue-setup)
4. [Worker Process Patterns](#worker-process-patterns)
5. [Job Lifecycle Management](#job-lifecycle-management)
6. [Error Handling and Retries](#error-handling-and-retries)
7. [Progress Reporting](#progress-reporting)
8. [Redis Connection Management](#redis-connection-management)
9. [OCR Processing Queue](#ocr-processing-queue)
10. [Knowledge Processing Queue](#knowledge-processing-queue)
11. [Document Processing Queue](#document-processing-queue)
12. [Queue Health Monitoring](#queue-health-monitoring)
13. [Graceful Shutdown](#graceful-shutdown)
14. [Best Practices](#best-practices)
15. [Testing Queues](#testing-queues)
16. [Troubleshooting](#troubleshooting)

---

## Overview

IntelliFill uses **Bull** (a Redis-based queue system) for asynchronous job processing. The project has three main queue types:

1. **Knowledge Processing Queue** (`knowledgeQueue`) - Document extraction, chunking, embedding, and vector storage
2. **OCR Processing Queue** (`ocrQueue`) - OCR text extraction from scanned documents
3. **Document Processing Queue** (`documentQueue`) - General document parsing and data extraction

### Key Files

```
quikadmin/src/
├── queues/
│   ├── knowledgeQueue.ts      # Knowledge base document processing
│   ├── ocrQueue.ts            # OCR processing for scanned PDFs
│   └── documentQueue.ts       # General document processing
├── workers/
│   ├── knowledgeProcessor.ts  # Knowledge processing worker
│   └── queue-processor.ts     # Generic queue processor wrapper
└── config/
    └── index.ts               # Redis configuration
```

---

## Queue Architecture

### Queue vs Worker Separation

**Queues** (in `src/queues/`) define:
- Job data types
- Job submission functions
- Event handlers
- Progress reporting utilities
- Queue configuration

**Workers** (in `src/workers/`) define:
- Job processing logic
- Service initialization
- Error handling
- Result generation

### Queue Types Comparison

| Feature | Knowledge Queue | OCR Queue | Document Queue |
|---------|----------------|-----------|----------------|
| **Purpose** | Vector search knowledge base | OCR text extraction | Form data extraction |
| **Timeout** | 10 minutes | 10 minutes | Default (30s) |
| **Retries** | 3 (exponential backoff) | 3 (exponential backoff) | 3 (exponential backoff) |
| **Concurrency** | 2 jobs | 1 job (default) | 1 job (default) |
| **Checkpointing** | Yes (Postgres) | No | No |
| **Progress Stages** | 5 (extraction, chunking, embedding, storage, complete) | 3 (processing, extraction, complete) | 4 (parse, extract, map, complete) |

---

## Bull Queue Setup

### Basic Queue Configuration

```typescript
import Bull, { Queue, JobOptions } from 'bull';
import { logger } from '../utils/logger';
import { config } from '../config';

// Define job data type
export interface MyJob {
  id: string;
  userId: string;
  data: any;
  options?: {
    priority?: 'high' | 'normal' | 'low';
  };
}

// Redis configuration
const redisConfig = {
  host: config.redis.host,
  port: config.redis.port,
  password: config.redis.password,
  maxRetriesPerRequest: 3,
};

// Create queue
export const myQueue: Queue<MyJob> = new Bull<MyJob>(
  'my-queue-name',
  {
    redis: redisConfig,
    defaultJobOptions: {
      removeOnComplete: 100,    // Keep last 100 completed jobs
      removeOnFail: 50,         // Keep last 50 failed jobs
      attempts: 3,              // Retry up to 3 times
      timeout: 300000,          // 5 minute timeout
      backoff: {
        type: 'exponential',
        delay: 5000,            // Start with 5s delay
      },
    },
    settings: {
      stalledInterval: 60000,   // Check for stalled jobs every minute
      maxStalledCount: 2,       // Jobs can be stalled twice before failing
      lockDuration: 300000,     // Lock jobs for 5 minutes
      lockRenewTime: 150000,    // Renew lock every 2.5 minutes
    },
    limiter: {
      max: 2,                   // Max 2 concurrent jobs
      duration: 1000,           // Per second
    },
  }
);
```

### Queue Event Handlers

```typescript
// Error handling
myQueue.on('error', (error) => {
  logger.error('Queue error', { error: error.message });
});

// Job lifecycle events
myQueue.on('waiting', (jobId) => {
  logger.debug('Job waiting', { jobId });
});

myQueue.on('active', (job) => {
  logger.info('Job started', {
    jobId: job.id,
    type: job.data.type,
    userId: job.data.userId,
  });
});

myQueue.on('completed', (job, result) => {
  logger.info('Job completed', {
    jobId: job.id,
    processingTimeMs: result.processingTimeMs,
    success: result.success,
  });
});

myQueue.on('failed', (job, error) => {
  logger.error('Job failed', {
    jobId: job.id,
    error: error.message,
    attemptsMade: job.attemptsMade,
  });
});

myQueue.on('stalled', (job) => {
  logger.warn('Job stalled', {
    jobId: job.id,
    type: job.data.type,
  });
});

myQueue.on('progress', (job, progress) => {
  logger.debug('Job progress', {
    jobId: job.id,
    percentage: progress.percentage,
    stage: progress.stage,
  });
});
```

### Priority-Based Job Submission

```typescript
const PRIORITY_MAP: Record<string, number> = {
  high: 1,    // Lower number = higher priority
  normal: 5,
  low: 10,
};

export async function addJob(
  data: Omit<MyJob, 'type'>,
  options?: Partial<JobOptions>
): Promise<Job<MyJob>> {
  const jobData: MyJob = {
    ...data,
    type: 'process',
  };

  const jobOptions: JobOptions = {
    priority: PRIORITY_MAP[data.priority || 'normal'],
    ...options,
  };

  const job = await myQueue.add(jobData, jobOptions);

  logger.info('Job queued', {
    jobId: job.id,
    userId: data.userId,
    priority: data.priority || 'normal',
  });

  return job;
}
```

---

## Worker Process Patterns

### Basic Worker Setup

```typescript
import { Job } from 'bull';
import { myQueue, MyJob } from '../queues/myQueue';

// Define result type
interface JobResult {
  success: boolean;
  data: any;
  processingTimeMs: number;
  error?: string;
}

// Main processor function
async function processJob(job: Job<MyJob>): Promise<JobResult> {
  const startTime = Date.now();

  try {
    logger.info('Processing job', { jobId: job.id });

    // Update progress
    await job.progress({ percentage: 10, stage: 'starting' });

    // Do work here
    const result = await doWork(job.data);

    await job.progress({ percentage: 100, stage: 'complete' });

    return {
      success: true,
      data: result,
      processingTimeMs: Date.now() - startTime,
    };
  } catch (error) {
    logger.error('Job failed', { jobId: job.id, error });
    throw error;
  }
}

// Register processor with concurrency
export function startWorker(): void {
  const CONCURRENCY = 2; // Process 2 jobs at once

  logger.info('Starting worker', { concurrency: CONCURRENCY });

  myQueue.process(CONCURRENCY, processJob);

  logger.info('Worker started');
}

// Graceful shutdown
export async function stopWorker(): Promise<void> {
  logger.info('Stopping worker...');
  await myQueue.close();
  logger.info('Worker stopped');
}
```

### Dependency Injection Pattern

```typescript
// Define dependencies interface
interface WorkerDependencies {
  service1: Service1;
  service2: Service2;
  database: DatabaseClient;
}

let dependencies: WorkerDependencies | null = null;

// Initialize dependencies once
async function initializeDependencies(): Promise<WorkerDependencies> {
  if (dependencies) {
    return dependencies;
  }

  logger.info('Initializing worker dependencies...');

  dependencies = {
    service1: new Service1(),
    service2: new Service2(),
    database: await createDatabaseClient(),
  };

  logger.info('Worker dependencies initialized');
  return dependencies;
}

// Use in processor
async function processJob(job: Job<MyJob>): Promise<JobResult> {
  const deps = await initializeDependencies();

  // Use deps.service1, deps.service2, etc.
  const result = await deps.service1.process(job.data);

  return {
    success: true,
    data: result,
    processingTimeMs: 0,
  };
}
```

### Standalone Worker Script

```typescript
// src/workers/myWorker.ts

import { startWorker, stopWorker } from './myProcessor';

// Check if running as standalone script
if (require.main === module) {
  (async () => {
    try {
      await startWorker();

      logger.info('Worker running. Press Ctrl+C to stop.');

      // Graceful shutdown handlers
      process.on('SIGINT', async () => {
        logger.info('Received SIGINT, shutting down...');
        await stopWorker();
        process.exit(0);
      });

      process.on('SIGTERM', async () => {
        logger.info('Received SIGTERM, shutting down...');
        await stopWorker();
        process.exit(0);
      });
    } catch (error) {
      logger.error('Failed to start worker', { error });
      process.exit(1);
    }
  })();
}

export default { startWorker, stopWorker };
```

**Run standalone worker:**
```bash
# Development
npx ts-node src/workers/myWorker.ts

# Production
node dist/workers/myWorker.js
```

---

## Job Lifecycle Management

### Job States

Bull jobs progress through these states:

1. **waiting** - Job queued, waiting to be processed
2. **active** - Job is currently being processed
3. **completed** - Job finished successfully
4. **failed** - Job failed after all retry attempts
5. **delayed** - Job scheduled for future processing
6. **paused** - Queue paused, job not processing

### Job Status Tracking

```typescript
export async function getJobStatus(
  jobId: string
): Promise<{
  id: string;
  status: string;
  progress: any;
  attemptsMade: number;
  processedOn?: Date;
  finishedOn?: Date;
  failedReason?: string;
} | null> {
  const job = await myQueue.getJob(jobId);

  if (!job) {
    return null;
  }

  const state = await job.getState();

  return {
    id: String(job.id),
    status: state,
    progress: job.progress(),
    attemptsMade: job.attemptsMade,
    processedOn: job.processedOn ? new Date(job.processedOn) : undefined,
    finishedOn: job.finishedOn ? new Date(job.finishedOn) : undefined,
    failedReason: job.failedReason,
  };
}
```

### Job Cancellation

```typescript
export async function cancelJob(jobId: string): Promise<boolean> {
  const job = await myQueue.getJob(jobId);

  if (!job) {
    return false;
  }

  const state = await job.getState();

  if (state === 'active') {
    // Cannot cancel active jobs
    logger.warn('Cannot cancel active job', { jobId });
    return false;
  }

  await job.remove();
  logger.info('Job cancelled', { jobId });
  return true;
}
```

### Job Retry

```typescript
export async function retryJob(jobId: string): Promise<boolean> {
  const job = await myQueue.getJob(jobId);

  if (!job) {
    return false;
  }

  const state = await job.getState();

  if (state !== 'failed') {
    logger.warn('Cannot retry non-failed job', { jobId, state });
    return false;
  }

  await job.retry();
  logger.info('Job retried', { jobId });
  return true;
}
```

### Get Jobs by Organization

```typescript
export async function getOrganizationJobs(
  organizationId: string,
  status?: 'waiting' | 'active' | 'completed' | 'failed'
): Promise<Job<MyJob>[]> {
  let jobs: Job<MyJob>[];

  switch (status) {
    case 'waiting':
      jobs = await myQueue.getWaiting();
      break;
    case 'active':
      jobs = await myQueue.getActive();
      break;
    case 'completed':
      jobs = await myQueue.getCompleted(0, 50); // Last 50
      break;
    case 'failed':
      jobs = await myQueue.getFailed(0, 50); // Last 50
      break;
    default:
      const [waiting, active] = await Promise.all([
        myQueue.getWaiting(),
        myQueue.getActive(),
      ]);
      jobs = [...waiting, ...active];
  }

  // Filter by organization
  return jobs.filter((job) => job.data.organizationId === organizationId);
}
```

---

## Error Handling and Retries

### Exponential Backoff Configuration

```typescript
export const myQueue = new Bull<MyJob>('my-queue', {
  redis: redisConfig,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 5000, // First retry after 5s, then 25s, then 125s
    },
  },
});
```

### Custom Retry Logic

```typescript
async function processJob(job: Job<MyJob>): Promise<JobResult> {
  try {
    // Attempt processing
    const result = await doWork(job.data);
    return { success: true, data: result };
  } catch (error) {
    const isRetryable = error instanceof RetryableError;
    const hasRetriesLeft = job.attemptsMade < job.opts.attempts!;

    if (isRetryable && hasRetriesLeft) {
      logger.warn('Retryable error, will retry', {
        jobId: job.id,
        attemptsMade: job.attemptsMade,
        attemptsTotal: job.opts.attempts,
        error: error.message,
      });
      throw error; // Throw to trigger Bull's retry mechanism
    } else {
      logger.error('Non-retryable error or max retries reached', {
        jobId: job.id,
        error: error.message,
      });

      // Update database status to permanent failure
      await updateJobStatus(job.data.id, 'failed', error.message);

      throw error; // Still throw to mark job as failed
    }
  }
}
```

### Retry Strategy by Error Type

```typescript
class RetryableError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RetryableError';
  }
}

class PermanentError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'PermanentError';
  }
}

async function processWithErrorHandling(job: Job<MyJob>): Promise<JobResult> {
  try {
    return await doWork(job.data);
  } catch (error) {
    // Network errors - retry
    if (error instanceof NetworkError) {
      throw new RetryableError(`Network error: ${error.message}`);
    }

    // Rate limit - retry with longer delay
    if (error instanceof RateLimitError) {
      await job.moveToDelayed(Date.now() + 60000); // Delay 1 minute
      throw new RetryableError(`Rate limited: ${error.message}`);
    }

    // Validation errors - don't retry
    if (error instanceof ValidationError) {
      throw new PermanentError(`Validation failed: ${error.message}`);
    }

    // Unknown errors - retry
    throw new RetryableError(`Unknown error: ${error.message}`);
  }
}
```

### Job Failure Handling

```typescript
myQueue.on('failed', async (job, error) => {
  logger.error('Job failed', {
    jobId: job.id,
    attemptsMade: job.attemptsMade,
    attemptsTotal: job.opts.attempts,
    error: error.message,
  });

  // Check if all retries exhausted
  if (job.attemptsMade >= job.opts.attempts!) {
    logger.error('Job failed after all retries', { jobId: job.id });

    // Update database to reflect permanent failure
    await prisma.document.update({
      where: { id: job.data.documentId },
      data: {
        status: 'FAILED',
        errorMessage: error.message,
      },
    });

    // Send notification to user
    await sendFailureNotification(job.data.userId, job.data.documentId);
  }
});
```

---

## Progress Reporting

### Basic Progress Updates

```typescript
async function processJob(job: Job<MyJob>): Promise<JobResult> {
  // Stage 1: Initialization
  await job.progress({ percentage: 10, stage: 'initializing' });
  await initialize();

  // Stage 2: Processing
  await job.progress({ percentage: 50, stage: 'processing' });
  const result = await process(job.data);

  // Stage 3: Complete
  await job.progress({ percentage: 100, stage: 'complete' });

  return { success: true, data: result };
}
```

### Structured Progress Interface

```typescript
export interface JobProgress {
  stage: 'extraction' | 'chunking' | 'embedding' | 'storage' | 'complete' | 'failed';
  percentage: number;
  currentStep: string;
  details?: {
    itemsProcessed?: number;
    totalItems?: number;
    errorMessage?: string;
  };
}

export async function reportProgress(
  job: Job<MyJob>,
  progress: JobProgress
): Promise<void> {
  await job.progress(progress);

  logger.debug('Job progress updated', {
    jobId: job.id,
    stage: progress.stage,
    percentage: progress.percentage,
    currentStep: progress.currentStep,
  });
}
```

### Progress Reporter Helper

```typescript
export function createProgressReporter(job: Job<MyJob>) {
  return {
    async extraction(percentage: number, processed: number, total: number) {
      return reportProgress(job, {
        stage: 'extraction',
        percentage: Math.min(25, percentage * 0.25),
        currentStep: `Extracting: ${processed}/${total}`,
        details: { itemsProcessed: processed, totalItems: total },
      });
    },

    async processing(percentage: number, processed: number, total: number) {
      return reportProgress(job, {
        stage: 'processing',
        percentage: 25 + Math.min(50, percentage * 0.5),
        currentStep: `Processing: ${processed}/${total}`,
        details: { itemsProcessed: processed, totalItems: total },
      });
    },

    async complete(stats: any) {
      return reportProgress(job, {
        stage: 'complete',
        percentage: 100,
        currentStep: 'Processing complete',
        details: stats,
      });
    },

    async failed(errorMessage: string) {
      return reportProgress(job, {
        stage: 'failed',
        percentage: job.progress()?.percentage || 0,
        currentStep: 'Processing failed',
        details: { errorMessage },
      });
    },
  };
}

// Usage
async function processJob(job: Job<MyJob>): Promise<JobResult> {
  const reporter = createProgressReporter(job);

  try {
    await reporter.extraction(0, 0, 10);
    // Do extraction...
    await reporter.extraction(100, 10, 10);

    await reporter.processing(0, 0, 100);
    // Do processing...
    await reporter.processing(100, 100, 100);

    await reporter.complete({ itemsProcessed: 100 });

    return { success: true };
  } catch (error) {
    await reporter.failed(error.message);
    throw error;
  }
}
```

### Real-time Progress Streaming

```typescript
// API endpoint to stream progress
import { EventEmitter } from 'events';

const progressEmitter = new EventEmitter();

// Worker emits progress events
myQueue.on('progress', (job, progress) => {
  progressEmitter.emit(`job:${job.id}:progress`, progress);
});

// API endpoint
app.get('/api/jobs/:id/progress', async (req, res) => {
  const { id } = req.params;

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  const listener = (progress: JobProgress) => {
    res.write(`data: ${JSON.stringify(progress)}\n\n`);
  };

  progressEmitter.on(`job:${id}:progress`, listener);

  req.on('close', () => {
    progressEmitter.off(`job:${id}:progress`, listener);
  });
});
```

---

## Redis Connection Management

### Redis Configuration from Environment

```typescript
// src/config/index.ts
export interface RedisConfig {
  url: string;
  host: string;
  port: number;
  password?: string;
  maxMemory: string;
  sentinel: {
    enabled: boolean;
    hosts?: string[];
    masterName?: string;
  };
}

export const config = {
  redis: {
    url: process.env.REDIS_URL || 'redis://localhost:6379',
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD,
    maxMemory: process.env.REDIS_MAX_MEMORY || '256mb',
    sentinel: {
      enabled: process.env.REDIS_SENTINEL_ENABLED === 'true',
      hosts: process.env.REDIS_SENTINEL_HOSTS?.split(','),
      masterName: process.env.REDIS_SENTINEL_MASTER_NAME,
    },
  },
};
```

### Standard Redis Connection

```typescript
import { config } from '../config';

const redisConfig = {
  host: config.redis.host,
  port: config.redis.port,
  password: config.redis.password,
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  connectTimeout: 10000,
};

export const myQueue = new Bull('my-queue', {
  redis: redisConfig,
});
```

### Redis Sentinel Configuration

```typescript
import { config } from '../config';

const redisConfig = config.redis.sentinel.enabled
  ? {
      sentinels: config.redis.sentinel.hosts?.map((host) => {
        const [hostname, port] = host.split(':');
        return { host: hostname, port: parseInt(port || '26379') };
      }),
      name: config.redis.sentinel.masterName,
      password: config.redis.password,
    }
  : {
      host: config.redis.host,
      port: config.redis.port,
      password: config.redis.password,
    };

export const myQueue = new Bull('my-queue', {
  redis: redisConfig,
});
```

### Connection Error Handling

```typescript
const redisConfig = {
  host: config.redis.host,
  port: config.redis.port,
  password: config.redis.password,
  maxRetriesPerRequest: 3,
  retryStrategy: (times: number) => {
    const delay = Math.min(times * 1000, 30000); // Max 30s
    logger.warn(`Redis reconnection attempt ${times}, delay: ${delay}ms`);

    if (times > 10) {
      logger.error('Redis max reconnection attempts reached');
      return new Error('Redis reconnection failed');
    }

    return delay;
  },
  reconnectOnError: (err: Error) => {
    logger.warn('Redis connection error, attempting reconnect', { error: err.message });
    return true; // Always try to reconnect
  },
};

export const myQueue = new Bull('my-queue', {
  redis: redisConfig,
});

// Monitor Redis connection
myQueue.on('error', (error) => {
  logger.error('Queue error (likely Redis)', { error: error.message });
});
```

### In-Memory Fallback Pattern

Some services (like rate limiting) support fallback to in-memory when Redis is unavailable:

```typescript
import { createClient } from 'redis';
import { logger } from '../utils/logger';

let redisClient: any = null;
let useMemoryFallback = false;

try {
  redisClient = createClient({
    host: config.redis.host,
    port: config.redis.port,
    password: config.redis.password,
    retryStrategy: (times: number) => {
      if (times > 5) {
        logger.warn('Redis unavailable, falling back to in-memory storage');
        useMemoryFallback = true;
        return undefined; // Stop retrying
      }
      return Math.min(times * 1000, 5000);
    },
  });

  await redisClient.connect();
  logger.info('Redis connected for rate limiting');
} catch (error) {
  logger.warn('Redis connection failed, using in-memory fallback', { error });
  useMemoryFallback = true;
}

// Use in-memory Map if Redis unavailable
const memoryStore = new Map<string, number>();

export async function incrementKey(key: string): Promise<number> {
  if (useMemoryFallback) {
    const current = memoryStore.get(key) || 0;
    const next = current + 1;
    memoryStore.set(key, next);
    return next;
  } else {
    return await redisClient.incr(key);
  }
}
```

---

## OCR Processing Queue

### OCR Queue Configuration

```typescript
// quikadmin/src/queues/ocrQueue.ts

export interface OCRProcessingJob {
  documentId: string;
  userId: string;
  filePath: string;
  isReprocessing?: boolean;
  reprocessReason?: string;
  options?: {
    language?: string;
    dpi?: number;
    enhancedPreprocessing?: boolean;
  };
}

export const ocrQueue = new Bull<OCRProcessingJob>('ocr-processing', {
  redis: redisConfig,
  defaultJobOptions: {
    removeOnComplete: 100,
    removeOnFail: 50,
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 3000, // 3s, 9s, 27s
    },
    timeout: 600000, // 10 minute timeout
  },
});
```

### Enqueuing OCR Jobs

```typescript
export async function enqueueDocumentForOCR(
  documentId: string,
  userId: string,
  filePath: string,
  forceOCR: boolean = false
): Promise<Bull.Job<OCRProcessingJob> | null> {
  try {
    // Check if PDF needs OCR
    if (!forceOCR) {
      const detectionService = new DocumentDetectionService();
      const isScanned = await detectionService.isScannedPDF(filePath);

      if (!isScanned) {
        logger.info(`Document ${documentId} is text-based, skipping OCR`);
        return null; // No OCR needed
      }
    }

    logger.info(`Enqueueing document ${documentId} for OCR processing`);

    const job = await ocrQueue.add({
      documentId,
      userId,
      filePath,
      options: {},
    });

    return job;
  } catch (error) {
    logger.error(`Failed to enqueue document ${documentId} for OCR:`, error);
    throw error;
  }
}
```

### OCR Job Processing

```typescript
ocrQueue.process(async (job) => {
  const { documentId, filePath, options } = job.data;
  const startTime = Date.now();

  try {
    // Update document status
    await prisma.document.update({
      where: { id: documentId },
      data: { status: 'PROCESSING' },
    });

    await job.progress(5);

    // Initialize OCR service
    const ocrService = new OCRService();
    await ocrService.initialize();
    await job.progress(10);

    // Process PDF with OCR and track progress
    const ocrResult = await ocrService.processPDF(filePath, (progress) => {
      // Map OCR progress (0-100) to job progress (10-90)
      const progressPercent = 10 + (progress.progress * 0.8);
      job.progress(progressPercent);
    });

    await job.progress(90);

    // Extract structured data
    const structuredData = await ocrService.extractStructuredData(ocrResult.text);
    await job.progress(95);

    // Update document with results
    await prisma.document.update({
      where: { id: documentId },
      data: {
        status: 'COMPLETED',
        extractedText: ocrResult.text,
        extractedData: {
          ...structuredData,
          ocrMetadata: ocrResult.metadata,
        },
        confidence: ocrResult.confidence / 100,
        processedAt: new Date(),
      },
    });

    await ocrService.cleanup();
    await job.progress(100);

    const processingTime = Date.now() - startTime;

    return {
      documentId,
      status: 'completed',
      confidence: ocrResult.confidence,
      pageCount: ocrResult.metadata.pageCount,
      processingTime,
    };
  } catch (error) {
    logger.error(`OCR processing failed for document ${documentId}:`, error);

    await prisma.document.update({
      where: { id: documentId },
      data: {
        status: 'FAILED',
        extractedText: `OCR Error: ${error.message}`,
      },
    });

    throw error;
  }
});
```

### OCR Reprocessing

```typescript
export async function enqueueDocumentForReprocessing(
  documentId: string,
  userId: string,
  filePath: string,
  reason?: string
): Promise<Bull.Job<OCRProcessingJob>> {
  const document = await prisma.document.findUnique({
    where: { id: documentId },
    select: { reprocessCount: true },
  });

  if (document && document.reprocessCount >= 3) {
    throw new Error('Maximum reprocessing attempts (3) reached');
  }

  logger.info('Enqueueing document for reprocessing', {
    documentId,
    attempt: (document?.reprocessCount || 0) + 1,
  });

  const job = await ocrQueue.add(
    {
      documentId,
      userId,
      filePath,
      isReprocessing: true,
      reprocessReason: reason,
      options: {
        dpi: 600, // Higher DPI for reprocessing
        enhancedPreprocessing: true,
      },
    },
    {
      priority: 1, // High priority
      timeout: 600000,
    }
  );

  return job;
}
```

---

## Knowledge Processing Queue

### Knowledge Queue Types

```typescript
// quikadmin/src/queues/knowledgeQueue.ts

export type KnowledgeJobType =
  | 'processDocument'
  | 'generateEmbeddings'
  | 'reprocessChunks';

export interface ProcessDocumentJob {
  type: 'processDocument';
  sourceId: string;
  organizationId: string;
  userId: string;
  filePath: string;
  filename: string;
  mimeType: string;
  fileSize: number;
  options?: {
    chunkingStrategy?: 'semantic' | 'fixed' | 'hybrid';
    targetChunkSize?: number;
    ocrEnabled?: boolean;
    language?: string;
    skipEmbeddings?: boolean;
  };
}

export interface JobProgress {
  stage: 'extraction' | 'chunking' | 'embedding' | 'storage' | 'complete' | 'failed';
  percentage: number;
  currentStep: string;
  details?: {
    pagesProcessed?: number;
    totalPages?: number;
    chunksProcessed?: number;
    totalChunks?: number;
    embeddingsGenerated?: number;
    chunksStored?: number;
    errorMessage?: string;
  };
}
```

### Knowledge Queue Configuration

```typescript
const QUEUE_NAME = 'knowledge-processing';
const DEFAULT_JOB_TIMEOUT = 10 * 60 * 1000; // 10 minutes
const MAX_CONCURRENT_JOBS = 2;

export const knowledgeQueue: Queue<KnowledgeJob> = new Bull<KnowledgeJob>(
  QUEUE_NAME,
  {
    redis: redisConfig,
    defaultJobOptions: {
      removeOnComplete: 100,
      removeOnFail: 50,
      attempts: 3,
      timeout: DEFAULT_JOB_TIMEOUT,
      backoff: {
        type: 'exponential',
        delay: 5000,
      },
    },
    settings: {
      stalledInterval: 60000,
      maxStalledCount: 2,
      lockDuration: 300000,
      lockRenewTime: 150000,
    },
    limiter: {
      max: MAX_CONCURRENT_JOBS,
      duration: 1000,
    },
  }
);
```

### Adding Knowledge Jobs

```typescript
export async function addProcessDocumentJob(
  data: Omit<ProcessDocumentJob, 'type'>,
  options?: Partial<JobOptions>
): Promise<Job<ProcessDocumentJob>> {
  const PRIORITY_MAP = { high: 1, normal: 5, low: 10 };

  const jobData: ProcessDocumentJob = {
    ...data,
    type: 'processDocument',
  };

  const jobOptions: JobOptions = {
    priority: PRIORITY_MAP[data.priority || 'normal'],
    ...options,
  };

  const job = await knowledgeQueue.add(jobData, jobOptions);

  logger.info('Document processing job queued', {
    jobId: job.id,
    sourceId: data.sourceId,
    filename: data.filename,
  });

  return job as Job<ProcessDocumentJob>;
}
```

### Knowledge Processing Worker

```typescript
// quikadmin/src/workers/knowledgeProcessor.ts

const PAGE_BATCH_SIZE = 5;       // Process 5 pages at a time
const EMBEDDING_BATCH_SIZE = 50;  // Generate 50 embeddings at once
const STORAGE_BATCH_SIZE = 100;   // Store 100 chunks at once

async function processDocumentJob(
  job: Job<ProcessDocumentJob>,
  deps: ProcessorDependencies
): Promise<KnowledgeJobResult> {
  const { sourceId, filePath, filename, options = {} } = job.data;
  const reporter = createProgressReporter(job);

  // Update source status
  await updateSourceStatus(sourceId, 'processing');

  // Check for checkpoint (resume from failure)
  const checkpoint = await getCheckpoint(sourceId);

  try {
    // =============================================
    // Stage 1: Text Extraction
    // =============================================
    let extractionResult;

    if (checkpoint?.extractedText) {
      logger.info('Resuming from extraction checkpoint', { sourceId });
      extractionResult = JSON.parse(checkpoint.extractedText);
    } else {
      await reporter.extraction(0, 0, 1);

      extractionResult = await deps.extractionService.extractFromFile(filePath, {
        mimeType: options.mimeType,
        ocrEnabled: options.ocrEnabled ?? true,
        language: options.language,
      });

      await reporter.extraction(100, extractionResult.metadata.pageCount, extractionResult.metadata.pageCount);

      // Save checkpoint
      await saveCheckpoint({
        sourceId,
        stage: 'extraction',
        extractedText: JSON.stringify(extractionResult),
        startedAt: new Date(),
      });
    }

    // =============================================
    // Stage 2: Chunking
    // =============================================
    let chunks: DocumentChunk[];

    if (checkpoint?.chunksJson) {
      chunks = JSON.parse(checkpoint.chunksJson);
    } else {
      await reporter.chunking(0, 0);

      const documentType = detectDocumentType(filename);
      const chunkingResult = deps.chunkingService.chunkDocument(
        extractionResult,
        documentType
      );
      chunks = chunkingResult.chunks;

      await reporter.chunking(100, chunks.length);

      await saveCheckpoint({
        sourceId,
        stage: 'chunking',
        chunksJson: JSON.stringify(chunks),
        totalChunks: chunks.length,
      });
    }

    // =============================================
    // Stage 3: Embedding Generation
    // =============================================
    const startChunkIndex = checkpoint?.lastCompletedChunkIndex || 0;
    const chunksWithEmbeddings: ChunkWithEmbedding[] = [];
    let embeddingsGenerated = 0;

    for (let i = startChunkIndex; i < chunks.length; i += EMBEDDING_BATCH_SIZE) {
      // Check memory before each batch
      await deps.memoryManager.checkMemory();

      const batchChunks = chunks.slice(i, i + EMBEDDING_BATCH_SIZE);
      const batchTexts = batchChunks.map((c) => c.text);

      if (!options.skipEmbeddings) {
        const batchResult = await deps.embeddingService.generateBatch(
          batchTexts,
          job.data.organizationId
        );

        for (let j = 0; j < batchChunks.length; j++) {
          if (batchResult.embeddings[j]) {
            chunksWithEmbeddings.push({
              ...batchChunks[j],
              embedding: batchResult.embeddings[j],
            });
            embeddingsGenerated++;
          }
        }
      }

      await reporter.embedding(
        ((i + batchChunks.length) / chunks.length) * 100,
        embeddingsGenerated,
        chunks.length
      );

      // Update checkpoint after each batch
      await saveCheckpoint({
        sourceId,
        stage: 'embedding',
        lastCompletedChunkIndex: i + batchChunks.length,
      });

      // Allow GC between batches
      await new Promise((resolve) => setImmediate(resolve));
    }

    // =============================================
    // Stage 4: Vector Storage
    // =============================================
    let chunksStored = 0;
    let duplicatesSkipped = 0;

    for (let i = 0; i < chunksWithEmbeddings.length; i += STORAGE_BATCH_SIZE) {
      const batchChunks = chunksWithEmbeddings.slice(i, i + STORAGE_BATCH_SIZE);

      for (const chunk of batchChunks) {
        // Check for duplicates
        const isDuplicate = await deps.vectorStorage.checkDuplicate(
          chunk.textHash,
          sourceId,
          job.data.organizationId
        );

        if (isDuplicate) {
          duplicatesSkipped++;
          continue;
        }

        await deps.vectorStorage.insertChunk({
          sourceId,
          organizationId: job.data.organizationId,
          text: chunk.text,
          tokenCount: chunk.tokenCount,
          chunkIndex: chunk.chunkIndex,
          embedding: chunk.embedding,
        });

        chunksStored++;
      }

      await reporter.storage(
        ((i + batchChunks.length) / chunksWithEmbeddings.length) * 100,
        chunksStored,
        chunksWithEmbeddings.length
      );
    }

    // =============================================
    // Completion
    // =============================================
    const stats = {
      pagesProcessed: extractionResult.metadata.pageCount,
      chunksCreated: chunks.length,
      embeddingsGenerated,
      chunksStored,
      duplicatesSkipped,
    };

    await reporter.complete(stats);
    await updateSourceStatus(sourceId, 'completed', { chunkCount: chunksStored });
    await deleteCheckpoint(sourceId);

    return {
      success: true,
      sourceId,
      organizationId: job.data.organizationId,
      processingTimeMs: 0,
      stats,
    };
  } catch (error) {
    await updateSourceStatus(sourceId, 'error', {
      errorMessage: error.message,
    });
    throw error;
  }
}
```

### Checkpointing for Resume

```typescript
export interface ProcessingCheckpoint {
  sourceId: string;
  stage: JobProgress['stage'];
  lastCompletedChunkIndex: number;
  totalChunks: number;
  extractedText?: string;
  chunksJson?: string;
  startedAt: Date;
  lastUpdatedAt: Date;
}

async function saveCheckpoint(checkpoint: ProcessingCheckpoint): Promise<void> {
  await prisma.$executeRaw`
    INSERT INTO processing_checkpoints (
      source_id, stage, last_completed_chunk_index, total_chunks,
      extracted_text, chunks_json, started_at, last_updated_at
    ) VALUES (
      ${checkpoint.sourceId}::uuid,
      ${checkpoint.stage},
      ${checkpoint.lastCompletedChunkIndex},
      ${checkpoint.totalChunks},
      ${checkpoint.extractedText ?? null},
      ${checkpoint.chunksJson ?? null},
      ${checkpoint.startedAt},
      ${checkpoint.lastUpdatedAt}
    )
    ON CONFLICT (source_id) DO UPDATE SET
      stage = EXCLUDED.stage,
      last_completed_chunk_index = EXCLUDED.last_completed_chunk_index,
      extracted_text = EXCLUDED.extracted_text,
      chunks_json = EXCLUDED.chunks_json,
      last_updated_at = EXCLUDED.last_updated_at
  `;
}

async function getCheckpoint(sourceId: string): Promise<ProcessingCheckpoint | null> {
  const results = await prisma.$queryRaw<ProcessingCheckpoint[]>`
    SELECT * FROM processing_checkpoints
    WHERE source_id = ${sourceId}::uuid
    LIMIT 1
  `;
  return results[0] || null;
}
```

---

## Document Processing Queue

### Document Queue Configuration

```typescript
// quikadmin/src/queues/documentQueue.ts

export interface DocumentProcessingJob {
  documentId: string;
  userId: string;
  filePath: string;
  options?: {
    extractTables?: boolean;
    ocrEnabled?: boolean;
    language?: string;
    confidenceThreshold?: number;
  };
}

export const documentQueue = new Bull<DocumentProcessingJob>('document-processing', {
  redis: redisConfig,
  defaultJobOptions: {
    removeOnComplete: 100,
    removeOnFail: 50,
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
  },
});
```

### Document Processing Job

```typescript
documentQueue.process(async (job) => {
  const { documentId, filePath, options } = job.data;

  try {
    await job.progress(10);

    // Initialize services
    const parser = new DocumentParser();
    const extractor = new DataExtractor();
    const mapper = new FieldMapper();

    // Parse document
    await job.progress(30);
    const parsedContent = await parser.parse(filePath);

    // Extract data
    await job.progress(50);
    const extractedData = await extractor.extract(parsedContent);

    // Map fields
    await job.progress(70);
    const mappedFields = await mapper.mapFields(extractedData, []);

    await job.progress(100);

    return {
      documentId,
      status: 'completed',
      extractedData,
      mappedFields,
      processingTime: Date.now() - job.timestamp,
    };
  } catch (error) {
    logger.error(`Failed to process document ${documentId}:`, error);
    throw error;
  }
});
```

### Batch Processing Queue

```typescript
export interface BatchProcessingJob {
  documentIds: string[];
  userId: string;
  targetFormId?: string;
  options?: {
    parallel?: boolean;
    stopOnError?: boolean;
  };
}

export const batchQueue = new Bull<BatchProcessingJob>('batch-processing', {
  redis: redisConfig,
  defaultJobOptions: {
    removeOnComplete: 50,
    removeOnFail: 25,
    attempts: 2,
  },
});

batchQueue.process(async (job) => {
  const { documentIds, options } = job.data;
  const results = [];

  for (let i = 0; i < documentIds.length; i++) {
    const progress = Math.round((i / documentIds.length) * 100);
    await job.progress(progress);

    // Add individual document to processing queue
    const childJob = await documentQueue.add({
      documentId: documentIds[i],
      userId: job.data.userId,
      filePath: `pending`,
      options: {},
    });

    // Wait for completion if not parallel
    if (!options?.parallel) {
      const result = await childJob.finished();
      results.push(result);

      if (options?.stopOnError && result.status === 'failed') {
        break;
      }
    } else {
      results.push({ documentId: documentIds[i], jobId: childJob.id });
    }
  }

  await job.progress(100);

  return {
    batchId: job.id,
    documentsProcessed: results.length,
    results,
  };
});
```

---

## Queue Health Monitoring

### Basic Queue Health Check

```typescript
export async function getQueueHealth() {
  const [waiting, active, completed, failed] = await Promise.all([
    myQueue.getWaitingCount(),
    myQueue.getActiveCount(),
    myQueue.getCompletedCount(),
    myQueue.getFailedCount(),
  ]);

  const isHealthy = active < 100 && waiting < 1000;

  return {
    queue: 'my-queue',
    waiting,
    active,
    completed,
    failed,
    isHealthy,
  };
}
```

### Comprehensive Queue Metrics

```typescript
export async function getQueueMetrics() {
  const [
    waiting,
    active,
    completed,
    failed,
    delayed,
    paused,
    jobs,
  ] = await Promise.all([
    myQueue.getWaitingCount(),
    myQueue.getActiveCount(),
    myQueue.getCompletedCount(),
    myQueue.getFailedCount(),
    myQueue.getDelayedCount(),
    myQueue.isPaused(),
    myQueue.getJobs(['waiting', 'active'], 0, 10), // Last 10 jobs
  ]);

  // Calculate average processing time
  const completedJobs = await myQueue.getCompleted(0, 100);
  const processingTimes = completedJobs
    .filter((job) => job.finishedOn && job.processedOn)
    .map((job) => job.finishedOn! - job.processedOn!);

  const avgProcessingTime =
    processingTimes.length > 0
      ? processingTimes.reduce((a, b) => a + b, 0) / processingTimes.length
      : 0;

  // Calculate failure rate
  const total = completed + failed;
  const failureRate = total > 0 ? (failed / total) * 100 : 0;

  return {
    queue: 'my-queue',
    counts: { waiting, active, completed, failed, delayed },
    paused,
    avgProcessingTimeMs: Math.round(avgProcessingTime),
    failureRate: failureRate.toFixed(2) + '%',
    isHealthy: active < 100 && waiting < 1000 && failureRate < 5,
    recentJobs: jobs.map((job) => ({
      id: job.id,
      status: job.getState(),
      progress: job.progress(),
    })),
  };
}
```

### Health Check Endpoint

```typescript
// Express route
app.get('/api/health/queues', async (req, res) => {
  try {
    const [knowledgeHealth, ocrHealth, documentHealth] = await Promise.all([
      getKnowledgeQueueHealth(),
      getOCRQueueHealth(),
      getDocumentQueueHealth(),
    ]);

    const allHealthy =
      knowledgeHealth.isHealthy &&
      ocrHealth.isHealthy &&
      documentHealth.isHealthy;

    res.status(allHealthy ? 200 : 503).json({
      status: allHealthy ? 'healthy' : 'degraded',
      queues: {
        knowledge: knowledgeHealth,
        ocr: ocrHealth,
        document: documentHealth,
      },
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error('Failed to get queue health', { error });
    res.status(500).json({ error: 'Failed to get queue health' });
  }
});
```

### Automated Alerting

```typescript
async function monitorQueueHealth() {
  setInterval(async () => {
    try {
      const health = await getQueueHealth();

      if (!health.isHealthy) {
        logger.warn('Queue unhealthy', health);

        // Send alert
        await sendAlert({
          level: 'warning',
          message: `Queue ${health.queue} unhealthy`,
          details: health,
        });
      }

      // Check for stuck jobs (active for > 30 minutes)
      const activeJobs = await myQueue.getActive();
      const now = Date.now();

      for (const job of activeJobs) {
        const activeTime = now - (job.processedOn || job.timestamp);

        if (activeTime > 30 * 60 * 1000) {
          logger.error('Job stuck', {
            jobId: job.id,
            activeTimeMs: activeTime,
          });

          await sendAlert({
            level: 'error',
            message: `Job ${job.id} stuck for ${Math.round(activeTime / 60000)} minutes`,
          });
        }
      }
    } catch (error) {
      logger.error('Queue monitoring failed', { error });
    }
  }, 60000); // Check every minute
}

// Start monitoring
monitorQueueHealth();
```

---

## Graceful Shutdown

### Basic Shutdown

```typescript
let isShuttingDown = false;

export async function closeQueue(): Promise<void> {
  if (isShuttingDown) {
    return;
  }

  isShuttingDown = true;
  logger.info('Closing queue...');

  try {
    await myQueue.close();
    logger.info('Queue closed');
  } catch (error) {
    logger.error('Error closing queue', { error });
  }
}

// Register shutdown handlers
process.on('SIGTERM', closeQueue);
process.on('SIGINT', closeQueue);
```

### Graceful Shutdown with Timeout

```typescript
export async function closeQueueGracefully(timeoutMs: number = 30000): Promise<void> {
  logger.info('Starting graceful shutdown...');

  // Stop accepting new jobs
  await myQueue.pause();

  // Wait for active jobs to complete (with timeout)
  const startTime = Date.now();

  while (true) {
    const activeCount = await myQueue.getActiveCount();

    if (activeCount === 0) {
      logger.info('All active jobs completed');
      break;
    }

    const elapsed = Date.now() - startTime;

    if (elapsed > timeoutMs) {
      logger.warn('Shutdown timeout reached, forcing close', {
        activeJobs: activeCount,
      });
      break;
    }

    logger.info('Waiting for active jobs to complete', {
      activeJobs: activeCount,
      elapsedMs: elapsed,
    });

    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  // Close queue
  await myQueue.close();
  logger.info('Queue closed gracefully');
}

process.on('SIGTERM', () => closeQueueGracefully(30000));
```

### Multi-Queue Shutdown

```typescript
import { knowledgeQueue, closeQueue as closeKnowledgeQueue } from './queues/knowledgeQueue';
import { ocrQueue, closeQueue as closeOCRQueue } from './queues/ocrQueue';
import { documentQueue, closeQueue as closeDocumentQueue } from './queues/documentQueue';

export async function closeAllQueues(): Promise<void> {
  logger.info('Closing all queues...');

  try {
    await Promise.all([
      closeKnowledgeQueue(),
      closeOCRQueue(),
      closeDocumentQueue(),
    ]);

    logger.info('All queues closed');
  } catch (error) {
    logger.error('Error closing queues', { error });
    throw error;
  }
}

// Express server shutdown
const server = app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});

process.on('SIGTERM', async () => {
  logger.info('SIGTERM received, shutting down...');

  // Close HTTP server
  server.close(async () => {
    logger.info('HTTP server closed');

    // Close queues
    await closeAllQueues();

    // Close database
    await prisma.$disconnect();

    logger.info('Shutdown complete');
    process.exit(0);
  });
});
```

---

## Best Practices

### 1. Job Data Design

**DO:**
- Keep job data small and JSON-serializable
- Store large files on disk/S3, pass file paths
- Use UUIDs for referencing database records
- Include organizationId/userId for multi-tenancy

**DON'T:**
- Store large binary data in job payload
- Include sensitive credentials in job data
- Use circular references in job objects

```typescript
// ✅ GOOD
interface MyJob {
  documentId: string;      // Reference, not full document
  filePath: string;        // Path, not file contents
  userId: string;          // For tracking
  options: { language: string };
}

// ❌ BAD
interface MyJob {
  documentBuffer: Buffer;  // Too large for Redis
  password: string;        // Sensitive data exposed
  circularRef: MyJob;      // Not JSON-serializable
}
```

### 2. Concurrency Configuration

```typescript
// CPU-intensive tasks: low concurrency
const CPU_INTENSIVE_CONCURRENCY = 2;

// I/O-bound tasks: higher concurrency
const IO_BOUND_CONCURRENCY = 10;

// Memory-intensive tasks: very low concurrency
const MEMORY_INTENSIVE_CONCURRENCY = 1;

ocrQueue.process(CPU_INTENSIVE_CONCURRENCY, processOCR);
apiQueue.process(IO_BOUND_CONCURRENCY, callAPI);
mlQueue.process(MEMORY_INTENSIVE_CONCURRENCY, trainModel);
```

### 3. Memory Management

```typescript
// Check memory before processing
async function processJob(job: Job<MyJob>): Promise<JobResult> {
  const memoryManager = getMemoryManager();

  // Check before starting
  await memoryManager.checkMemory();

  // Process in batches
  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE);

    // Check memory before each batch
    await memoryManager.checkMemory();

    await processBatch(batch);

    // Allow GC between batches
    await new Promise((resolve) => setImmediate(resolve));
  }

  return { success: true };
}
```

### 4. Error Classification

```typescript
class RetryableError extends Error {
  constructor(message: string, public retryAfterMs?: number) {
    super(message);
    this.name = 'RetryableError';
  }
}

class PermanentError extends Error {
  constructor(message: string, public code?: string) {
    super(message);
    this.name = 'PermanentError';
  }
}

async function processWithClassification(job: Job<MyJob>): Promise<JobResult> {
  try {
    return await doWork(job.data);
  } catch (error) {
    // Network/timeout errors - retry
    if (error instanceof NetworkError || error instanceof TimeoutError) {
      throw new RetryableError(error.message);
    }

    // Rate limit - retry with delay
    if (error instanceof RateLimitError) {
      throw new RetryableError(error.message, 60000); // Retry after 1 minute
    }

    // Validation errors - don't retry
    if (error instanceof ValidationError) {
      throw new PermanentError(error.message, 'VALIDATION_FAILED');
    }

    // Unknown errors - retry (cautiously)
    throw new RetryableError(`Unknown error: ${error.message}`);
  }
}
```

### 5. Logging Standards

```typescript
// At job start
logger.info('Job started', {
  jobId: job.id,
  type: job.data.type,
  userId: job.data.userId,
  organizationId: job.data.organizationId,
});

// At key stages
logger.info('Job stage completed', {
  jobId: job.id,
  stage: 'extraction',
  itemsProcessed: 100,
});

// On error
logger.error('Job failed', {
  jobId: job.id,
  error: error.message,
  stack: error.stack,
  attemptsMade: job.attemptsMade,
  attemptsTotal: job.opts.attempts,
});

// On completion
logger.info('Job completed', {
  jobId: job.id,
  processingTimeMs: Date.now() - startTime,
  stats: { itemsProcessed: 100, errors: 0 },
});
```

### 6. Testing Queue Jobs

```typescript
// Test job processing logic directly (without Bull)
describe('processJob', () => {
  it('should process job successfully', async () => {
    const mockJob = {
      id: '123',
      data: { documentId: 'doc-1', userId: 'user-1' },
      progress: jest.fn(),
      attemptsMade: 0,
      opts: { attempts: 3 },
    } as any;

    const result = await processJob(mockJob);

    expect(result.success).toBe(true);
    expect(mockJob.progress).toHaveBeenCalledWith({ percentage: 100 });
  });

  it('should handle errors gracefully', async () => {
    const mockJob = {
      id: '123',
      data: { documentId: 'invalid' },
    } as any;

    await expect(processJob(mockJob)).rejects.toThrow();
  });
});
```

---

## Testing Queues

### Unit Testing Job Processors

```typescript
import { Job } from 'bull';
import { processJob } from '../workers/myWorker';

describe('processJob', () => {
  let mockJob: Partial<Job>;

  beforeEach(() => {
    mockJob = {
      id: '123',
      data: {
        documentId: 'doc-1',
        userId: 'user-1',
        filePath: '/path/to/file.pdf',
      },
      progress: jest.fn(),
      attemptsMade: 0,
      opts: { attempts: 3 },
      timestamp: Date.now(),
    };
  });

  it('should process job successfully', async () => {
    const result = await processJob(mockJob as Job);

    expect(result.success).toBe(true);
    expect(result.processingTimeMs).toBeGreaterThan(0);
    expect(mockJob.progress).toHaveBeenCalled();
  });

  it('should report progress at each stage', async () => {
    await processJob(mockJob as Job);

    expect(mockJob.progress).toHaveBeenCalledWith(
      expect.objectContaining({ percentage: 10 })
    );
    expect(mockJob.progress).toHaveBeenCalledWith(
      expect.objectContaining({ percentage: 100 })
    );
  });

  it('should handle errors and throw', async () => {
    mockJob.data!.documentId = 'invalid';

    await expect(processJob(mockJob as Job)).rejects.toThrow();
  });
});
```

### Integration Testing with Bull

```typescript
import Bull from 'bull';
import { myQueue } from '../queues/myQueue';

describe('myQueue integration', () => {
  let testQueue: Bull.Queue;

  beforeAll(async () => {
    // Use test Redis database
    testQueue = new Bull('test-queue', {
      redis: {
        host: 'localhost',
        port: 6379,
        db: 15, // Use separate DB for tests
      },
    });

    // Start processor
    testQueue.process(async (job) => {
      return { success: true, data: job.data };
    });
  });

  afterAll(async () => {
    await testQueue.close();
  });

  afterEach(async () => {
    // Clean up jobs after each test
    await testQueue.empty();
  });

  it('should process a job end-to-end', async () => {
    const job = await testQueue.add({ test: 'data' });

    const result = await job.finished();

    expect(result.success).toBe(true);
    expect(result.data.test).toBe('data');
  });

  it('should retry failed jobs', async () => {
    let attempts = 0;

    testQueue.process(async (job) => {
      attempts++;
      if (attempts < 3) {
        throw new Error('Simulated failure');
      }
      return { success: true, attempts };
    });

    const job = await testQueue.add(
      { test: 'retry' },
      { attempts: 3, backoff: { type: 'fixed', delay: 100 } }
    );

    const result = await job.finished();

    expect(result.attempts).toBe(3);
  });
});
```

### Testing Queue Health

```typescript
import { getQueueHealth } from '../queues/myQueue';

describe('getQueueHealth', () => {
  it('should return queue metrics', async () => {
    const health = await getQueueHealth();

    expect(health).toHaveProperty('queue');
    expect(health).toHaveProperty('waiting');
    expect(health).toHaveProperty('active');
    expect(health).toHaveProperty('completed');
    expect(health).toHaveProperty('failed');
    expect(health).toHaveProperty('isHealthy');
  });

  it('should mark queue as unhealthy when overloaded', async () => {
    // Add 200 jobs to simulate overload
    for (let i = 0; i < 200; i++) {
      await myQueue.add({ test: i });
    }

    const health = await getQueueHealth();

    expect(health.isHealthy).toBe(false);
  });
});
```

---

## Troubleshooting

### Redis Connection Issues

**Symptom:** Jobs not processing, "Connection refused" errors

**Diagnosis:**
```bash
# Check Redis is running
redis-cli ping
# Should return: PONG

# Check Redis connection from Node.js
node -e "const redis = require('redis'); const client = redis.createClient(); client.on('connect', () => console.log('Connected')); client.on('error', (err) => console.error(err));"
```

**Solutions:**
1. Start Redis: `redis-server`
2. Check `REDIS_URL` environment variable
3. Verify Redis password (if configured)
4. Check firewall/network settings

### Jobs Stuck in "Active" State

**Symptom:** Jobs show as active but never complete

**Diagnosis:**
```typescript
// Check for stalled jobs
const stalledJobs = await myQueue.getActive();
console.log('Active jobs:', stalledJobs.length);

for (const job of stalledJobs) {
  const activeTime = Date.now() - (job.processedOn || job.timestamp);
  console.log(`Job ${job.id}: active for ${activeTime}ms`);
}
```

**Solutions:**
1. Increase `lockDuration` and `lockRenewTime`
2. Check for worker crashes (logs)
3. Manually clean stalled jobs:
```typescript
await myQueue.clean(5000, 'active'); // Clean jobs active > 5s
```

### Memory Leaks in Workers

**Symptom:** Worker memory usage grows over time

**Diagnosis:**
```typescript
// Monitor memory in worker
setInterval(() => {
  const usage = process.memoryUsage();
  console.log('Memory:', {
    rss: `${Math.round(usage.rss / 1024 / 1024)}MB`,
    heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)}MB`,
  });
}, 60000);
```

**Solutions:**
1. Process items in batches with `setImmediate()` breaks
2. Close/cleanup services after each job
3. Restart worker periodically (PM2 max_memory_restart)
4. Use `--max-old-space-size` Node.js flag

### Queue Growing Too Fast

**Symptom:** Waiting job count increases rapidly

**Diagnosis:**
```typescript
const health = await getQueueHealth();
console.log('Waiting:', health.waiting);
console.log('Active:', health.active);

// Calculate processing rate
const completedCount = await myQueue.getCompletedCount();
// Wait 1 minute
await new Promise((resolve) => setTimeout(resolve, 60000));
const newCompletedCount = await myQueue.getCompletedCount();
const jobsPerMinute = newCompletedCount - completedCount;
console.log('Processing rate:', jobsPerMinute, 'jobs/minute');
```

**Solutions:**
1. Increase worker concurrency
2. Scale horizontally (more worker instances)
3. Optimize job processing time
4. Add job prioritization
5. Implement rate limiting on job creation

### Failed Jobs Not Retrying

**Symptom:** Jobs fail but don't retry

**Diagnosis:**
```typescript
const failedJobs = await myQueue.getFailed();
for (const job of failedJobs) {
  console.log(`Job ${job.id}:`, {
    attemptsMade: job.attemptsMade,
    attemptsTotal: job.opts.attempts,
    failedReason: job.failedReason,
  });
}
```

**Solutions:**
1. Check `attempts` configuration in `defaultJobOptions`
2. Ensure error is thrown (not caught and silenced)
3. Check for PermanentError vs RetryableError
4. Manually retry: `await job.retry()`

---

## Related Documentation

- [Redis Configuration](../../quikadmin/src/config/index.ts)
- [Knowledge Queue](../../quikadmin/src/queues/knowledgeQueue.ts)
- [Knowledge Processor Worker](../../quikadmin/src/workers/knowledgeProcessor.ts)
- [OCR Queue](../../quikadmin/src/queues/ocrQueue.ts)
- [Document Queue](../../quikadmin/src/queues/documentQueue.ts)

---

**Last Updated:** 2025-12-12
**Skill Version:** 1.0.0
**Maintained By:** IntelliFill Team
