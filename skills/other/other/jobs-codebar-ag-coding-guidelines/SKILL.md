---
name: jobs
description: Queueable units of work for background processing. Jobs handle queue configuration and failure handling — they delegate business logic to Actions or Services.
---

**Name:** Jobs
**Description:** Queueable units of work for background processing. Jobs handle queue configuration and failure handling — they delegate business logic to Actions or Services.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Jobs/**/*.php, laravel, php, backend, queue, job, background

## Rules

- Job classes live in `app/Jobs/`
- Jobs are **queueable units of work** that execute a single task in the background
- Use a clear verb-noun naming pattern: `ProcessInvoicePayment`, `SendWeeklyReport`, `ImportProductCsv`
- The name should describe what the job does, not when it runs
- Jobs delegate their work to an **Action** or **Service** — they own queue configuration and failure handling, not business logic
- Always declare queue configuration explicitly on the job class rather than relying on defaults
- Implement `ShouldQueue` for all jobs that should run asynchronously
- Always use the `Dispatchable`, `InteractsWithQueue`, `Queueable`, `SerializesModels` traits
- Define a `failed(Throwable $exception)` method for permanent failure handling

## Examples

```php
namespace App\Jobs;

use App\Actions\ProcessInvoicePayment;
use App\Models\Invoice;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Throwable;

class ProcessInvoicePaymentJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;
    public int $timeout = 120;
    public string $queue = 'invoices';

    public function __construct(
        private readonly Invoice $invoice,
    ) {}

    public function handle(ProcessInvoicePayment $action): void
    {
        $action->execute($this->invoice);
    }

    public function failed(Throwable $exception): void
    {
        // Notify, log, or alert on permanent failure after all retries
    }
}
```

```php
// Dispatch immediately to the queue
ProcessInvoicePaymentJob::dispatch($invoice);

// Dispatch with a delay
ProcessInvoicePaymentJob::dispatch($invoice)->delay(now()->addMinutes(5));

// Dispatch synchronously (bypasses queue — useful in tests)
ProcessInvoicePaymentJob::dispatchSync($invoice);
```

## Anti-Patterns

- Putting business logic directly in a job's `handle()` method instead of delegating to an Action or Service
- Omitting `$tries`, `$backoff`, or `$timeout` and relying on global queue defaults
- Not implementing a `failed()` method for jobs that process critical data
- Using jobs for work that must complete synchronously before returning a response
- Using jobs for simple, fast operations that don't justify queue overhead

## References

- [Laravel Queues](https://laravel.com/docs/queues)
- Related: `Actions/SKILL.md` — for the business logic jobs delegate to
- Related: `Services/SKILL.md` — for complex orchestration delegated from jobs
