---
name: exceptions
description: Named, meaningful failure states in your domain. Custom exceptions communicate precise failure reasons to callers and optionally carry domain-specific data.
---

**Name:** Exceptions
**Description:** Named, meaningful failure states in your domain. Custom exceptions communicate precise failure reasons to callers and optionally carry domain-specific data.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Exceptions/**/*.php, laravel, php, backend, exception, error-handling

## Rules

- Exception classes live in `app/Exceptions/`
- Custom exceptions represent **named, meaningful failure states** — not generic error wrappers
- Use a clear noun phrase describing what went wrong: `InvoiceAlreadyPaid`, `InsufficientFunds`, `PaymentGatewayUnavailable`
- Always suffix with `Exception`: `InvoiceAlreadyPaidException`
- Use named static constructors (`static for()`) to make throw sites readable
- Set the message via `parent::__construct()` inside the constructor
- Expose domain-specific context data as `public readonly` properties
- Implement `render()` directly on exceptions that always map to the same HTTP response
- Register exception rendering in `bootstrap/app.php` using `withExceptions()`
- Avoid `try-catch` blocks — let exceptions bubble up to the framework handler unless you must react locally

## Examples

```php
namespace App\Exceptions;

use App\Models\Invoice;
use RuntimeException;

class InvoiceAlreadyPaidException extends RuntimeException
{
    public function __construct(
        public readonly Invoice $invoice,
    ) {
        parent::__construct(
            "Invoice #{$invoice->id} has already been paid and cannot be modified."
        );
    }

    public static function for(Invoice $invoice): static
    {
        return new static($invoice);
    }
}
```

```php
// Throwing — from inside an Action
class MarkInvoiceAsPaid
{
    public function execute(Invoice $invoice): void
    {
        if ($invoice->isPaid()) {
            throw InvoiceAlreadyPaidException::for($invoice);
        }

        $invoice->update(['paid_at' => now()]);
    }
}
```

```php
// Registering in bootstrap/app.php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvoiceAlreadyPaidException $e, Request $request) {
        return response()->json(['message' => $e->getMessage()], 422);
    });

    $exceptions->dontReport([
        InvoiceAlreadyPaidException::class,
    ]);
})
```

## Anti-Patterns

- Creating generic exception wrappers instead of named domain exceptions
- Not using a named static constructor — verbose `new InvoiceAlreadyPaidException($invoice)` at every throw site
- Putting business logic or recovery logic inside an exception class
- Silently swallowing exceptions without logging or re-throwing
- Using built-in exceptions where a domain-specific exception would communicate intent better
- Creating an exception for cases already handled cleanly by validation or early returns

## References

- [Laravel Error Handling](https://laravel.com/docs/errors)
- Related: `Actions/SKILL.md` — the typical place where domain exceptions are thrown
- Related: `PHP/SKILL.md` — for error handling philosophy (avoid try-catch, let bubble)
