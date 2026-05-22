---
name: tzurot-async-flow
description: BullMQ and async patterns for Tzurot v3. Use when working with jobs, Discord deferrals, or retry logic. Covers queue architecture, idempotency, and error handling.
lastUpdated: '2026-01-21'
---

# Tzurot v3 Async Flow & Job Queue

**Use this skill when:** Creating jobs, processing queue tasks, handling Discord interactions, implementing retry logic, or managing async operations.

## Quick Reference

```typescript
// Queue setup (api-gateway)
import { Queue } from 'bullmq';
const aiQueue = new Queue('ai-jobs', { connection });

// Worker setup (ai-worker)
import { Worker } from 'bullmq';
const worker = new Worker('ai-jobs', processJob, { connection, concurrency: 5 });

// Discord deferral (bot-client)
await interaction.deferReply();
const result = await fetch('/ai/generate');
await interaction.editReply({ content: result.content });
```

## Architecture Flow

```
Discord Interaction → bot-client defers (3s window)
  → api-gateway creates BullMQ job
  → ai-worker picks up job
  → ai-worker returns result
  → bot-client sends webhook reply
```

## 🚨 Discord Deferral (CRITICAL)

Discord requires response within 3 seconds. AI calls take longer.

```typescript
// MUST defer IMMEDIATELY, then process
await interaction.deferReply();

const response = await fetch(`${GATEWAY_URL}/ai/generate`, {
  method: 'POST',
  body: JSON.stringify(requestData),
});

await interaction.editReply({ content: result.content });
```

## Job Patterns

### Job Naming

```typescript
// Use prefixes from common-types
import { JOB_PREFIXES } from '@tzurot/common-types';
const jobId = `${JOB_PREFIXES.LLM_GENERATION}${requestId}`;
```

### Job Processor Structure

```typescript
export async function processLLMGeneration(
  job: Job<LLMGenerationJobData>
): Promise<AIGenerationResponse> {
  await job.updateProgress(10);
  const personality = await personalityService.getPersonality(job.data.personalityId);

  await job.updateProgress(50);
  const response = await aiProvider.generateResponse({
    /* ... */
  });

  await job.updateProgress(100);
  return { content: response.content };
}
```

### Queue Configuration

```typescript
const aiQueue = new Queue('ai-jobs', {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: { type: 'exponential', delay: 2000 },
    removeOnComplete: { count: 10, age: 24 * 3600 },
    removeOnFail: { count: 50, age: 7 * 24 * 3600 },
  },
});
```

## Idempotency

Prevent duplicate requests with Redis:

```typescript
async isDuplicate(requestId: string): Promise<boolean> {
  const result = await redis.set(`dedup:${requestId}`, '1', 'EX', 5, 'NX');
  return result === null; // null = key already existed
}
```

## Retry Strategy

**Retryable errors:** Network timeouts, rate limits (429), server errors (5xx)
**Non-retryable:** Validation errors (400), not found (404), auth (401)

```typescript
async function withRetry<T>(fn: () => Promise<T>, maxAttempts = 3): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts || !isRetryableError(error)) throw error;
      await new Promise(r => setTimeout(r, 2000 * Math.pow(2, attempt - 1)));
    }
  }
}
```

## Timer Patterns

### ✅ OK Patterns

```typescript
// Request timeouts
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 30000);

// One-time delays
await new Promise(resolve => setTimeout(resolve, delayMs));
```

### ❌ Scaling Blockers (avoid)

```typescript
// Persistent intervals prevent horizontal scaling
this.cleanupInterval = setInterval(() => this.cleanup(), 60000);
```

### ✅ Alternatives

Use BullMQ repeatable jobs instead:

```typescript
await queue.add('cleanup-cache', {}, { repeat: { every: 60000 } });
```

## Waiting for Job Completion

```typescript
async function waitForJobCompletion(jobId: string, timeoutMs: number): Promise<any> {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Timeout')), timeoutMs);

    const onCompleted = (args: { jobId: string; returnvalue: any }) => {
      if (args.jobId !== jobId) return;
      clearTimeout(timeout);
      queueEvents.off('completed', onCompleted);
      resolve(args.returnvalue);
    };

    queueEvents.on('completed', onCompleted);
  });
}
```

## Monitoring

```typescript
app.get('/metrics', async (req, res) => {
  const [waiting, active, failed] = await Promise.all([
    aiQueue.getWaitingCount(),
    aiQueue.getActiveCount(),
    aiQueue.getFailedCount(),
  ]);
  res.json({ queue: { waiting, active, failed } });
});
```

## Related Skills

- **tzurot-architecture** - Async workflow design
- **tzurot-observability** - Job logging and correlation IDs
- **tzurot-types** - Job data type definitions
- **tzurot-security** - Signed payloads for job verification

## References

- BullMQ docs: https://docs.bullmq.io/
- Queue constants: `packages/common-types/src/constants/queue.ts`
- Job processors: `services/ai-worker/src/jobs/`
