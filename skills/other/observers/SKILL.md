---
name: observers
description: Centralised classes that react to Eloquent model lifecycle events. Used for side effects that should always fire regardless of where a model is mutated — such as notifications, cache invalidation, and audit logging.
---

**Name:** Observers
**Description:** Centralised classes that react to Eloquent model lifecycle events. Used for side effects that should always fire regardless of where a model is mutated — such as notifications, cache invalidation, and audit logging.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Observers/**/*.php, laravel, php, backend, observer, eloquent, model-events

## Rules

- Observer classes live in `app/Observers/`
- Naming: `PascalCase` with an `Observer` suffix, named after the model they observe: `UserObserver`, `InvoiceObserver`
- Only define the event methods you actually need — do not scaffold empty methods
- Register observers in `AppServiceProvider` using the `observe()` method
- Use observers for side effects tied to model lifecycle events that should always fire
- Never put business logic that should be explicitly controlled in an observer — use an Action instead

## Examples

```php
namespace App\Observers;

use App\Models\User;
use App\Notifications\WelcomeNotification;
use Illuminate\Support\Facades\Cache;

class UserObserver
{
    public function created(User $user): void
    {
        $user->notify(new WelcomeNotification());
    }

    public function updated(User $user): void
    {
        Cache::forget("user:{$user->id}");
    }

    public function deleted(User $user): void
    {
        Cache::forget("user:{$user->id}");
    }
}
```

```php
// Registration in AppServiceProvider
use App\Models\User;
use App\Observers\UserObserver;

public function boot(): void
{
    User::observe(UserObserver::class);
}
```

**Available lifecycle events:**

| Method | Fires when... |
|---|---|
| `creating` | Before a model is first saved |
| `created` | After a model is first saved |
| `updating` | Before an existing model is saved |
| `updated` | After an existing model is saved |
| `saving` | Before creating or updating |
| `saved` | After creating or updating |
| `deleting` | Before a model is deleted |
| `deleted` | After a model is deleted |
| `restoring` | Before a soft-deleted model is restored |
| `restored` | After a soft-deleted model is restored |

## Anti-Patterns

- Using an observer for side effects specific to one particular action (use the Action directly instead)
- Scaffolding empty observer methods for all lifecycle events when only one is needed
- Putting complex orchestration inside an observer (use a Service)
- Using an observer for validation (use Form Requests)
- Using an observer for authorization (use Policies)
- Relying on observers when you need fine-grained control over when side effects fire

## References

- [Laravel Observers](https://laravel.com/docs/eloquent#observers)
- Related: `Models/SKILL.md` — Eloquent model conventions
- Related: `Events/SKILL.md` — alternative for decoupled side effects
