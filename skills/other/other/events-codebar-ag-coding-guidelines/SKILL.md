---
name: events
description: Decoupled communication between application layers. Events are plain data objects describing what happened; listeners react to those events with a single, specific side effect.
---

**Name:** Events & Listeners
**Description:** Decoupled communication between application layers. Events are plain data objects describing what happened; listeners react to those events with a single, specific side effect.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Events/**/*.php, app/Listeners/**/*.php, laravel, php, backend, event, listener, observer-pattern

## Rules

- Event classes live in `app/Events/`; listener classes live in `app/Listeners/`
- Events are plain data containers — no logic inside events
- Listeners handle one specific reaction each — never bundle multiple side effects
- Events: past-tense noun phrase → `InvoicePaid`, `UserRegistered`, `OrderShipped`
- Listeners: verb phrase describing the reaction → `SendInvoicePaidNotification`, `UpdateInventory`
- Dispatch events from inside an **Action** after the operation completes — never from a controller or model directly
- Register events and listeners in `EventServiceProvider`
- Implement `ShouldQueue` on listeners for side effects that can be deferred
- Define a `failed()` method on queued listeners
- Use events when one action triggers multiple independent side effects

## Examples

```php
// Event — data container only
namespace App\Events;

use App\Models\Invoice;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class InvoicePaid
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public readonly Invoice $invoice,
    ) {}
}
```

```php
// Listener — one reaction
namespace App\Listeners;

use App\Events\InvoicePaid;
use App\Notifications\InvoicePaidNotification;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendInvoicePaidNotification implements ShouldQueue
{
    public function handle(InvoicePaid $event): void
    {
        $event->invoice->user->notify(new InvoicePaidNotification($event->invoice));
    }

    public function failed(InvoicePaid $event, \Throwable $exception): void
    {
        // Handle failure
    }
}
```

```php
// Dispatching — from inside an Action
class MarkInvoiceAsPaid
{
    public function execute(Invoice $invoice): void
    {
        $invoice->update(['paid_at' => now()]);
        InvoicePaid::dispatch($invoice);
    }
}
```

```php
// Registration — one event, many listeners
protected $listen = [
    InvoicePaid::class => [
        SendInvoicePaidNotification::class,
        UpdateAccountingRecords::class,
        NotifyAccountManager::class,
    ],
];
```

## Anti-Patterns

- Adding business logic inside an Event class
- Bundling multiple reactions in a single Listener (one listener, one reaction)
- Dispatching events from controllers or models directly — dispatch from Actions
- Using events for simple, single side effects that can be triggered directly
- Not implementing `failed()` on queued listeners for critical side effects
- Creating event chains that obscure control flow and make debugging hard

## References

- [Laravel Events](https://laravel.com/docs/events)
- Related: `Actions/SKILL.md` — events should be dispatched from Actions
- Related: `Observers/SKILL.md` — for model lifecycle reactions
