---
name: laravel-queues-jobs
description: >-
  Develops queued jobs and background processing. Activates when creating jobs, dispatching to queues,
  handling failed jobs, configuring queue workers, batching jobs, or when user mentions job, queue,
  dispatch, worker, background, async processing, or ShouldQueue.
---

# Laravel Queues & Jobs Development

## When to Apply

Activate this skill when:

- Creating queued jobs for background processing
- Dispatching jobs to queues
- Handling job failures and retries
- Configuring queue connections and workers
- Implementing job batching or chaining

## Documentation

Use `search-docs` for detailed Laravel queue patterns and documentation.

## Basic Usage

### Creating Jobs

Use Artisan to create jobs:

```bash
php artisan make:job ProcessPodcast
```

### Job Structure

<code-snippet name="Basic Job" lang="php">
<?php

namespace App\Jobs;

use App\Models\Podcast;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    public function __construct(
        public Podcast $podcast,
    ) {}

    public function handle(): void
    {
        // Process the podcast...
    }
}
</code-snippet>

### Dispatching Jobs

<code-snippet name="Dispatching Jobs" lang="php">
use App\Jobs\ProcessPodcast;

// Dispatch to default queue
ProcessPodcast::dispatch($podcast);

// Dispatch to specific queue
ProcessPodcast::dispatch($podcast)->onQueue('podcasts');

// Dispatch with delay
ProcessPodcast::dispatch($podcast)->delay(now()->addMinutes(10));

// Dispatch after response sent
ProcessPodcast::dispatchAfterResponse($podcast);

// Dispatch synchronously (for testing)
ProcessPodcast::dispatchSync($podcast);
</code-snippet>

### Job Configuration

<code-snippet name="Job Configuration" lang="php">
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    // Max attempts before failing
    public int $tries = 3;

    // Max exceptions before failing
    public int $maxExceptions = 3;

    // Timeout in seconds
    public int $timeout = 120;

    // Backoff between retries (seconds)
    public int $backoff = 60;

    // Or exponential backoff
    public array $backoff = [30, 60, 120];

    // Unique job (prevents duplicates)
    public function uniqueId(): string
    {
        return $this->podcast->id;
    }

    public int $uniqueFor = 3600; // Seconds
}
</code-snippet>

### Handling Failures

<code-snippet name="Failed Job Handling" lang="php">
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    public function handle(): void
    {
        // Process...
    }

    public function failed(?Throwable $exception): void
    {
        // Notify team, cleanup, etc.
        Log::error('Podcast processing failed', [
            'podcast_id' => $this->podcast->id,
            'error' => $exception->getMessage(),
        ]);
    }
}
</code-snippet>

### Job Batching

<code-snippet name="Job Batching" lang="php">
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

$batch = Bus::batch([
    new ProcessPodcast($podcast1),
    new ProcessPodcast($podcast2),
    new ProcessPodcast($podcast3),
])->then(function (Batch $batch) {
    // All jobs completed successfully
})->catch(function (Batch $batch, Throwable $e) {
    // First batch job failure detected
})->finally(function (Batch $batch) {
    // Batch finished (success or failure)
})->dispatch();
</code-snippet>

### Job Chaining

<code-snippet name="Job Chaining" lang="php">
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new ProcessPodcast($podcast),
    new OptimizePodcast($podcast),
    new ReleasePodcast($podcast),
])->dispatch();
</code-snippet>

### Rate Limiting

<code-snippet name="Rate Limited Jobs" lang="php">
use Illuminate\Support\Facades\Redis;

public function handle(): void
{
    Redis::throttle('podcast-processing')
        ->allow(10)
        ->every(60)
        ->then(function () {
            // Process podcast...
        }, function () {
            // Release back to queue
            return $this->release(30);
        });
}
</code-snippet>

## Queue Workers

```bash
# Start worker
php artisan queue:work

# Process specific queue
php artisan queue:work --queue=high,default

# Process single job
php artisan queue:work --once

# Restart workers after code deploy
php artisan queue:restart
```

## Failed Jobs

```bash
# View failed jobs
php artisan queue:failed

# Retry specific job
php artisan queue:retry <job-id>

# Retry all failed jobs
php artisan queue:retry all

# Delete failed job
php artisan queue:forget <job-id>

# Flush all failed jobs
php artisan queue:flush
```

## Common Pitfalls

- Not implementing `ShouldQueue` interface (job runs synchronously)
- Passing Eloquent models without serialization consideration
- Not handling job failures appropriately
- Missing `queue:restart` after deployments
- Not configuring appropriate timeouts for long-running jobs
- Forgetting to set up queue worker in production (Supervisor, Horizon)
