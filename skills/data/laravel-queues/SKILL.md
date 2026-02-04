---
name: laravel-queues
description: Implement background jobs with queues, workers, batches, chains, middleware, and failure handling. Use when processing async tasks or handling long-running operations.
versions:
  laravel: "12.46"
  horizon: "5.43"
  php: "8.5"
user-invocable: false
references: references/jobs.md, references/dispatching.md, references/workers.md, references/batching.md, references/chaining.md, references/middleware.md, references/failed-jobs.md, references/horizon.md, references/testing.md, references/troubleshooting.md, references/templates/QueueableJob.php.md, references/templates/BatchJob.php.md, references/templates/ChainedJobs.php.md, references/templates/JobMiddleware.php.md, references/templates/JobTest.php.md
related-skills: laravel-architecture, laravel-eloquent
---

# Laravel Queues

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing job patterns
2. **fuse-ai-pilot:research-expert** - Verify Queue docs via Context7
3. **mcp__context7__query-docs** - Check job and worker patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Component | Purpose |
|-----------|---------|
| **Jobs** | Background tasks with retries, timeouts |
| **Workers** | Process jobs from queues |
| **Batches** | Group jobs with progress tracking |
| **Chains** | Sequential job execution |
| **Middleware** | Rate limiting, deduplication |
| **Horizon** | Redis queue monitoring dashboard |

---

## Decision Guide: Queue Driver

```
Which driver?
├── Development → sync (instant execution)
├── Small app → database (simple, no Redis)
├── Production → redis (fast, Horizon support)
├── AWS → sqs (managed, scalable)
└── High volume → redis + Horizon (monitoring)
```

---

## Decision Guide: Job Design

```
Job type?
├── Simple async → Standard Job
├── Group processing → Batch (progress, cancel)
├── Sequential steps → Chain (A → B → C)
├── Rate limited → Middleware + RateLimiter
├── Unique execution → UniqueJob / WithoutOverlapping
└── Long running → Timeout + Retry settings
```

---

## Critical Rules

1. **Use ShouldQueue** for async processing
2. **Set tries and backoff** for resilience
3. **Implement failed()** method for error handling
4. **Use database transactions** carefully with jobs
5. **Monitor with Horizon** in production

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Jobs** | [jobs.md](references/jobs.md) | Creating job classes |
| **Dispatching** | [dispatching.md](references/dispatching.md) | Sending jobs to queues |
| **Workers** | [workers.md](references/workers.md) | Running queue workers |
| **Batching** | [batching.md](references/batching.md) | Grouping jobs |
| **Chaining** | [chaining.md](references/chaining.md) | Sequential jobs |
| **Middleware** | [middleware.md](references/middleware.md) | Rate limiting, dedup |
| **Failed Jobs** | [failed-jobs.md](references/failed-jobs.md) | Error handling |
| **Horizon** | [horizon.md](references/horizon.md) | Monitoring dashboard |
| **Testing** | [testing.md](references/testing.md) | Job testing |
| **Troubleshooting** | [troubleshooting.md](references/troubleshooting.md) | Common issues |

### Templates

| Template | When to Use |
|----------|-------------|
| [QueueableJob.php.md](references/templates/QueueableJob.php.md) | Standard job with retries |
| [BatchJob.php.md](references/templates/BatchJob.php.md) | Batchable job |
| [ChainedJobs.php.md](references/templates/ChainedJobs.php.md) | Job chain implementation |
| [JobMiddleware.php.md](references/templates/JobMiddleware.php.md) | Custom middleware |
| [JobTest.php.md](references/templates/JobTest.php.md) | Testing jobs |

---

## Quick Reference

### Basic Job

```php
final class ProcessOrder implements ShouldQueue
{
    use Queueable;

    public int $tries = 3;
    public int $backoff = 60;
    public int $timeout = 120;

    public function __construct(
        public readonly Order $order,
    ) {}

    public function handle(OrderService $service): void
    {
        $service->process($this->order);
    }

    public function failed(\Throwable $e): void
    {
        Log::error('Order failed', ['id' => $this->order->id]);
    }
}
```

### Dispatch

```php
// Immediate
ProcessOrder::dispatch($order);

// Delayed
ProcessOrder::dispatch($order)->delay(now()->addMinutes(5));

// On specific queue
ProcessOrder::dispatch($order)->onQueue('orders');
```

---

## Best Practices

### DO
- Use `final` for job classes
- Implement `failed()` method
- Set appropriate `timeout` values
- Use `Unique` for one-at-a-time jobs
- Monitor with Horizon in production

### DON'T
- Dispatch inside database transactions (use `afterCommit`)
- Store large objects in job properties
- Forget to handle failures
- Use sync driver in production
