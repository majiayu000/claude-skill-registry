---
name: background-job-guardian
description: Prevents background job failures in Bull/Redis queue systems. Use when implementing async workers, debugging stuck jobs, optimizing queue performance, or handling job failures. Covers job retry strategies, dead letter queues, concurrency limits, progress tracking, error handling, and queue monitoring.
---

# Background Job Guardian

**Mission:** Ensure background jobs are reliable, performant, and observable. Prevent stuck jobs, infinite retries, memory leaks, and silent failures.

## Activation Triggers

- Implementing new Bull queues/jobs
- Jobs stuck in processing state
- Queue backing up (thousands of pending jobs)
- Jobs failing silently
- Memory leaks in workers
- Slow job processing
- Dead letter queue filling up
- Need job progress tracking

## Framework Awareness

This skill understands:
- **Bull** - Redis-based queue system for Node.js
- **Redis** - In-memory data store for job queues
- **Job Patterns** - Fire-and-forget, request-response, delayed jobs
- **Worker Patterns** - Concurrency, rate limiting, batching

## Common Job Patterns in PDFLab

```
1. Conversion Job (Long-running, 30s-5min)
   Upload → Queue → Process (CloudConvert) → Download → Cleanup

2. Batch Job (Parent job with multiple children)
   Upload Files → Create Batch → Spawn N Conversion Jobs → ZIP Results

3. Cleanup Job (Delayed, 1 hour)
   Job Completes → Schedule Cleanup → Delete Files

4. Email Job (Fast, <5s)
   User Action → Queue Email → Send via SMTP
```

## Scan Methodology

### 1. Critical Job Configuration

#### 🔴 CRITICAL: Retry Strategy

**Historical Failure:** Infinite retries overwhelmed CloudConvert API, account suspended

**Scan for:**
- [ ] Maximum retry attempts defined (3-5 for most jobs)
- [ ] Exponential backoff configured
- [ ] Different retry strategies for different error types
- [ ] Dead letter queue for permanently failed jobs
- [ ] No retry for non-retryable errors (400 Bad Request)

**Red flags:**
```typescript
// ❌ DANGEROUS - Infinite retries
conversionQueue.add(data, {
  attempts: Infinity  // Never stops retrying
})

// ❌ DANGEROUS - No backoff, hammers API
conversionQueue.add(data, {
  attempts: 10,
  backoff: 1000  // Fixed 1s delay, no exponential backoff
})

// ❌ DANGEROUS - Retries non-retryable errors
conversionQueue.process(async (job) => {
  try {
    await cloudConvert.convert(file)
  } catch (error) {
    throw error  // Retries even for 400 Bad Request
  }
})
```

**Optimization:**
```typescript
// ✅ SAFE - Smart retry strategy
conversionQueue.add(data, {
  attempts: 5,  // Max 5 retries
  backoff: {
    type: 'exponential',
    delay: 2000  // 2s, 4s, 8s, 16s, 32s
  },
  removeOnComplete: true,  // Save memory
  removeOnFail: 100  // Keep last 100 failed jobs for debugging
})

// ✅ SAFE - Error-specific retry logic
conversionQueue.process(async (job) => {
  try {
    await cloudConvert.convert(job.data.file)
  } catch (error) {
    // Don't retry client errors
    if (error.statusCode >= 400 && error.statusCode < 500) {
      job.moveToFailed({ message: 'Client error, not retrying' }, false)
      return
    }

    // Retry server errors
    if (error.statusCode >= 500) {
      throw error  // Will retry with exponential backoff
    }

    // Don't retry quota exceeded
    if (error.code === 'QUOTA_EXCEEDED') {
      job.moveToFailed({ message: 'Quota exceeded' }, false)
      return
    }

    // Retry other errors
    throw error
  }
})
```

#### 🔴 CRITICAL: Job Timeout

**Historical Failure:** Job stuck for 24 hours, blocked queue

**Scan for:**
- [ ] Timeout defined for all jobs
- [ ] Timeout appropriate for job type (30s for fast, 10min for slow)
- [ ] Timeout handling (cleanup resources)
- [ ] Progress updates prevent timeout

**Timeout Strategy:**
```typescript
// ❌ NO TIMEOUT - Can hang forever
conversionQueue.process(async (job) => {
  await processFile(job.data.file)  // Could hang forever
})

// ✅ JOB-LEVEL TIMEOUT
conversionQueue.add(data, {
  timeout: 300000  // 5 minutes (5 * 60 * 1000)
})

// ✅ OPERATION-LEVEL TIMEOUT with cleanup
import pTimeout from 'p-timeout'

conversionQueue.process(async (job) => {
  try {
    await pTimeout(
      processFile(job.data.file),
      { milliseconds: 300000 }
    )
  } catch (error) {
    if (error.name === 'TimeoutError') {
      // Cleanup resources
      await cleanupPartialFiles(job.data.file)
      throw new Error('Job timed out after 5 minutes')
    }
    throw error
  }
})

// ✅ PREVENT TIMEOUT with progress updates
conversionQueue.process(async (job) => {
  // Update progress every 10s to keep job alive
  const progressInterval = setInterval(() => {
    job.progress(job.data.currentProgress)
  }, 10000)

  try {
    await processFile(job.data.file)
  } finally {
    clearInterval(progressInterval)
  }
})
```

#### 🟡 HIGH: Concurrency Limits

**Historical Issue:** 100 concurrent jobs overwhelmed server, OOM crash

**Scan for:**
- [ ] Concurrency defined per queue
- [ ] Concurrency appropriate for resource usage
- [ ] Rate limiting for external API calls
- [ ] Memory monitoring

**Concurrency Patterns:**
```typescript
// ❌ UNLIMITED CONCURRENCY - OOM risk
conversionQueue.process(async (job) => {
  // Processes all queued jobs at once
})

// ✅ LIMITED CONCURRENCY
conversionQueue.process(5, async (job) => {
  // Max 5 jobs processing at once
})

// ✅ DYNAMIC CONCURRENCY based on plan
const getConcurrency = (plan: string) => {
  switch (plan) {
    case 'free': return 1      // 1 concurrent conversion
    case 'starter': return 2   // 2 concurrent
    case 'pro': return 5       // 5 concurrent
    case 'enterprise': return 10  // 10 concurrent
  }
}

// ✅ RESOURCE-AWARE CONCURRENCY
const MEMORY_THRESHOLD = 0.8  // 80% memory usage

conversionQueue.process(async (job) => {
  // Check memory before processing
  const memoryUsage = process.memoryUsage().heapUsed / process.memoryUsage().heapTotal

  if (memoryUsage > MEMORY_THRESHOLD) {
    // Delay job if low on memory
    await job.moveToDelayed(Date.now() + 60000)  // Retry in 1 minute
    return
  }

  await processFile(job.data.file)
})
```

#### 🟡 HIGH: Progress Tracking

**Historical Issue:** Users had no idea if job was stuck or progressing

**Scan for:**
- [ ] Progress updates during long jobs
- [ ] Progress stored in job data
- [ ] Frontend can poll for progress
- [ ] Stages/milestones communicated

**Progress Patterns:**
```typescript
// ❌ NO PROGRESS - User has no feedback
conversionQueue.process(async (job) => {
  await step1()
  await step2()
  await step3()
  // User sees 0% until complete
})

// ✅ STAGE-BASED PROGRESS
conversionQueue.process(async (job) => {
  job.progress(0)
  job.data.stage = 'Uploading to CloudConvert'
  await uploadFile(job.data.file)

  job.progress(33)
  job.data.stage = 'Converting PDF'
  await convertFile()

  job.progress(66)
  job.data.stage = 'Downloading result'
  await downloadResult()

  job.progress(100)
  job.data.stage = 'Complete'
})

// ✅ PERCENTAGE-BASED PROGRESS (for batch jobs)
conversionQueue.process(async (job) => {
  const totalFiles = job.data.files.length
  let completedFiles = 0

  for (const file of job.data.files) {
    await processFile(file)
    completedFiles++

    const progress = Math.round((completedFiles / totalFiles) * 100)
    job.progress(progress)
    job.data.completed = completedFiles
  }
})

// ✅ NESTED PROGRESS (batch with sub-jobs)
batchQueue.process(async (batchJob) => {
  const conversionJobs = await ConversionJob.findAll({
    where: { id: batchJob.data.conversion_job_ids }
  })

  // Update batch progress based on child jobs
  const completed = conversionJobs.filter(j => j.status === 'completed').length
  const progress = Math.round((completed / conversionJobs.length) * 100)

  batchJob.progress(progress)
})
```

#### 🟠 MEDIUM: Job Data Size

**Historical Issue:** 10MB job data in Redis caused memory issues

**Scan for:**
- [ ] Job data is minimal (IDs, not full objects)
- [ ] Large files not stored in job data
- [ ] Use file paths/URLs, not file contents
- [ ] Clean up job data on completion

**Data Optimization:**
```typescript
// ❌ HUGE JOB DATA - Stores 10MB file in Redis
conversionQueue.add({
  file: fileBuffer,  // 10MB buffer in Redis!
  user: userObject   // Full user object
})

// ✅ MINIMAL JOB DATA - Only IDs and paths
conversionQueue.add({
  job_id: jobId,           // UUID
  user_id: userId,         // UUID
  input_file: '/path/to/file.pdf',  // File path, not contents
  output_format: 'pptx'
})

// ✅ CLEANUP ON COMPLETION
conversionQueue.on('completed', (job) => {
  job.remove()  // Remove job data from Redis
})

conversionQueue.add(data, {
  removeOnComplete: true,  // Auto-remove on success
  removeOnFail: 100        // Keep last 100 failures for debugging
})
```

#### 🟠 MEDIUM: Job Priority

**Scan for:**
- [ ] Priority levels defined (paid users > free users)
- [ ] LIFO/FIFO strategy appropriate
- [ ] Priority queue for urgent jobs

**Priority Patterns:**
```typescript
// ✅ PAID USERS GET PRIORITY
const getPriority = (user: User) => {
  switch (user.plan) {
    case 'enterprise': return 1  // Highest priority
    case 'pro': return 2
    case 'starter': return 3
    case 'free': return 4        // Lowest priority
  }
}

conversionQueue.add(data, {
  priority: getPriority(user)
})

// ✅ URGENT JOBS
conversionQueue.add(data, {
  priority: 1,        // Highest
  lifo: true          // Last In, First Out (process immediately)
})

// ✅ BATCH JOBS (lower priority)
conversionQueue.add(data, {
  priority: 5,        // Lower priority
  lifo: false         // FIFO (wait in line)
})
```

### 2. Queue Monitoring

#### Metrics to Track

```typescript
// Queue health metrics
const getQueueMetrics = async () => {
  const [waiting, active, completed, failed, delayed] = await Promise.all([
    conversionQueue.getWaitingCount(),
    conversionQueue.getActiveCount(),
    conversionQueue.getCompletedCount(),
    conversionQueue.getFailedCount(),
    conversionQueue.getDelayedCount()
  ])

  return {
    waiting,    // Jobs in queue
    active,     // Jobs being processed
    completed,  // Successfully completed
    failed,     // Failed (check these!)
    delayed,    // Scheduled for future
    total: waiting + active + delayed
  }
}

// Expose metrics endpoint
app.get('/admin/queue-metrics', async (req, res) => {
  const metrics = await getQueueMetrics()

  // Alert if queue backing up
  if (metrics.waiting > 100) {
    logger.warn('Queue backing up', { waiting: metrics.waiting })
  }

  res.json(metrics)
})
```

#### Queue Events to Monitor

```typescript
// Job lifecycle events
conversionQueue.on('waiting', (jobId) => {
  logger.debug('Job waiting', { jobId })
})

conversionQueue.on('active', (job) => {
  logger.info('Job started', {
    jobId: job.id,
    userId: job.data.user_id,
    type: job.data.conversion_type
  })
})

conversionQueue.on('completed', (job, result) => {
  logger.info('Job completed', {
    jobId: job.id,
    duration: Date.now() - job.processedOn,
    result
  })

  // Track metrics
  metrics.increment('conversion.success', {
    type: job.data.conversion_type
  })
})

conversionQueue.on('failed', (job, err) => {
  logger.error('Job failed', {
    jobId: job.id,
    error: err.message,
    stack: err.stack,
    attempts: job.attemptsMade,
    data: job.data
  })

  // Alert on repeated failures
  if (job.attemptsMade >= job.opts.attempts) {
    // Send alert (Sentry, Slack, etc.)
    Sentry.captureException(err, {
      tags: { job_id: job.id },
      extra: { job_data: job.data }
    })
  }

  metrics.increment('conversion.failed', {
    type: job.data.conversion_type,
    error_type: err.code || 'unknown'
  })
})

conversionQueue.on('stalled', (job) => {
  logger.warn('Job stalled (likely worker crashed)', {
    jobId: job.id
  })

  // Stalled jobs are automatically retried by Bull
})
```

### 3. Dead Letter Queue Pattern

**For permanently failed jobs:**

```typescript
// Setup dead letter queue
const deadLetterQueue = new Bull('dead-letter', {
  redis: redisConfig
})

// Move permanently failed jobs
conversionQueue.on('failed', async (job, err) => {
  // If all retries exhausted
  if (job.attemptsMade >= job.opts.attempts) {
    // Move to dead letter queue for manual review
    await deadLetterQueue.add({
      original_job: job.data,
      failed_at: new Date(),
      error: err.message,
      stack: err.stack,
      attempts: job.attemptsMade
    })

    // Notify admin
    await sendAdminAlert({
      subject: 'Job permanently failed',
      body: `Job ${job.id} failed after ${job.attemptsMade} attempts`
    })
  }
})

// Admin endpoint to retry dead letter jobs
app.post('/admin/retry-dead-letter/:jobId', async (req, res) => {
  const deadJob = await deadLetterQueue.getJob(req.params.jobId)

  // Retry with fresh attempt count
  await conversionQueue.add(deadJob.data.original_job, {
    attempts: 5
  })

  await deadJob.remove()
  res.json({ message: 'Job requeued' })
})
```

### 4. Worker Health Checks

```typescript
// Worker heartbeat
let lastHeartbeat = Date.now()

conversionQueue.on('active', () => {
  lastHeartbeat = Date.now()
})

// Health check endpoint
app.get('/worker/health', (req, res) => {
  const timeSinceLastJob = Date.now() - lastHeartbeat

  // Worker should process jobs regularly
  if (timeSinceLastJob > 300000) {  // 5 minutes
    return res.status(503).json({
      status: 'unhealthy',
      reason: 'No jobs processed in 5 minutes',
      last_job: lastHeartbeat
    })
  }

  res.json({
    status: 'healthy',
    last_job: lastHeartbeat,
    uptime: process.uptime()
  })
})
```

### 5. Memory Leak Prevention

```typescript
// Monitor memory usage
setInterval(() => {
  const used = process.memoryUsage()

  logger.info('Memory usage', {
    rss_mb: Math.round(used.rss / 1024 / 1024),
    heap_used_mb: Math.round(used.heapUsed / 1024 / 1024),
    heap_total_mb: Math.round(used.heapTotal / 1024 / 1024)
  })

  // Alert if memory usage high
  if (used.heapUsed / used.heapTotal > 0.9) {
    logger.warn('High memory usage', {
      usage_percent: Math.round((used.heapUsed / used.heapTotal) * 100)
    })
  }

  // Force GC if needed (requires --expose-gc flag)
  if (global.gc && used.heapUsed / used.heapTotal > 0.8) {
    global.gc()
  }
}, 60000)  // Every minute

// Restart worker after N jobs to prevent memory leaks
let jobsProcessed = 0
const MAX_JOBS_BEFORE_RESTART = 1000

conversionQueue.on('completed', async () => {
  jobsProcessed++

  if (jobsProcessed >= MAX_JOBS_BEFORE_RESTART) {
    logger.info('Processed 1000 jobs, restarting worker to prevent memory leaks')
    await conversionQueue.close()
    process.exit(0)  // PM2/Docker will restart
  }
})
```

## Quick Reference: Bull Job Lifecycle

```
1. WAITING → Job added to queue, waiting for worker
2. ACTIVE → Worker picked up job, processing
3. COMPLETED → Job finished successfully
4. FAILED → Job failed, will retry if attempts remaining
5. DELAYED → Job scheduled for future processing
6. STUCK → Job didn't update progress, considered stalled
```

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Job stalled" | Worker crashed mid-job | Bull auto-retries, improve error handling |
| "ECONNREFUSED" | Redis not running | Start Redis, check connection |
| "Memory limit exceeded" | Too many concurrent jobs | Reduce concurrency, add cleanup |
| "Job timeout" | Job took too long | Increase timeout or optimize code |
| "Too many retries" | Job keeps failing | Fix root cause, don't just retry |

## Production Checklist

- [ ] Retry strategy configured (max 3-5 attempts, exponential backoff)
- [ ] Timeout defined for all jobs (appropriate for job type)
- [ ] Concurrency limited (5-10 max for heavy jobs)
- [ ] Progress tracking implemented
- [ ] Job data minimal (<1KB per job)
- [ ] Cleanup on completion (removeOnComplete: true)
- [ ] Dead letter queue for permanent failures
- [ ] Monitoring/alerting on queue metrics
- [ ] Worker health checks
- [ ] Memory leak prevention

## Key Principles

1. **Retry intelligently** - Not all errors are retryable
2. **Fail fast** - Don't retry forever
3. **Track progress** - Users need feedback
4. **Limit concurrency** - Prevent resource exhaustion
5. **Monitor queues** - Alert on backup
6. **Clean up data** - Redis is not permanent storage
7. **Handle worker crashes** - Jobs should be idempotent

## When to Escalate

- Complex job orchestration (Temporal, Airflow)
- Multi-queue coordination
- Job scheduling (cron patterns)
- Distributed workers across servers
- Custom retry logic per error type
