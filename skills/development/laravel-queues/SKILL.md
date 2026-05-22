---
name: laravel-queues
description: Implement background jobs with queues, workers, batches, chains, events, broadcasting, and failure handling. Use when processing async tasks, sending emails, or handling long-running operations.
user-invocable: false
---

# Laravel Queues & Events

## Documentation

### Queues & Jobs
- [queues.md](docs/queues.md) - Queue system
- [horizon.md](docs/horizon.md) - Queue monitoring
- [scheduling.md](docs/scheduling.md) - Task scheduling

### Events & Broadcasting
- [events.md](docs/events.md) - Events & Listeners
- [broadcasting.md](docs/broadcasting.md) - WebSocket broadcasting
- [reverb.md](docs/reverb.md) - Laravel Reverb (WebSockets)

### Notifications & Mail
- [notifications.md](docs/notifications.md) - Notifications
- [mail.md](docs/mail.md) - Email sending

### Caching & Storage
- [cache.md](docs/cache.md) - Caching
- [redis.md](docs/redis.md) - Redis

### Monitoring
- [telescope.md](docs/telescope.md) - Debug assistant
- [pulse.md](docs/pulse.md) - Application monitoring

## Job Class

```php
<?php

declare(strict_types=1);

namespace App\Jobs;

final class SendWelcomeEmail implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;

    public function __construct(
        public readonly User $user,
    ) {}

    public function handle(EmailService $emailService): void
    {
        $emailService->sendWelcome($this->user);
    }

    public function failed(\Throwable $exception): void
    {
        Log::error('Welcome email failed', ['user_id' => $this->user->id]);
    }
}
```

## Events & Listeners

```php
// Event
class OrderShipped
{
    public function __construct(
        public readonly Order $order,
    ) {}
}

// Listener
class SendShipmentNotification
{
    public function handle(OrderShipped $event): void
    {
        $event->order->user->notify(new OrderShippedNotification($event->order));
    }
}

// Dispatch
OrderShipped::dispatch($order);
```

## Job Batches

```php
Bus::batch([
    new ProcessPodcast($podcast1),
    new ProcessPodcast($podcast2),
])
->then(fn (Batch $batch) => Log::info('All completed!'))
->catch(fn (Batch $batch, Throwable $e) => Log::error('Failed'))
->dispatch();
```
