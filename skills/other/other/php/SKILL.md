---
name: php
description: General PHP coding standards covering strict typing, formatting, control flow, and error handling. Applies to all PHP files in the application.
---

**Name:** PHP Conventions
**Description:** General PHP coding standards covering strict typing, formatting, control flow, and error handling. Applies to all PHP files in the application.
**Compatible Agents:** general-purpose, backend
**Tags:** app/**/*.php, laravel, php, backend, typing, formatting, conventions

## Rules

- Type hints on **all** parameters, return types, and properties — no untyped signatures
- Use union types or nullable (`?Type`) where needed
- Target **PHPStan Level 9** compliance
- All code in **English**: variable names, comments, docblocks
- Foreign-language domain terms from external APIs are acceptable in DTOs where they match the API
- Run **Laravel Pint** before committing
- Avoid `try-catch` blocks — let exceptions bubble up to the framework's handler
- Only catch exceptions when you **must** react locally (retry logic, API fallback)
- Use **early returns** (guard clauses) to handle edge cases at the top of a method
- Never use `else`, `elseif`, or nested `if` blocks — invert the condition and return early
- Prefer immutability — use `readonly` properties where possible
- One class per file

## Examples

```php
// ✓ Early returns — guard clauses
public function process(Order $order): void
{
    if (! $order->isPaid()) {
        throw new UnpaidOrderException();
    }

    if (! $order->hasItems()) {
        throw new EmptyOrderException();
    }

    // Happy-path logic here
}
```

```php
// ✗ Nested if/else — never do this
public function process(Order $order): void
{
    if ($order->isPaid()) {
        if ($order->hasItems()) {
            // deep logic
        } else {
            throw new EmptyOrderException();
        }
    } else {
        throw new UnpaidOrderException();
    }
}
```

```php
// ✓ Fully typed class
class CreateInvoice
{
    public function __construct(
        private readonly GenerateInvoicePdf $generatePdf,
    ) {}

    public function execute(Order $order): Invoice
    {
        // implementation
    }
}
```

```php
// ✓ Structured logging when catching
try {
    $this->externalService->call($data);
} catch (ServiceException $e) {
    Log::error('External service failed.', [
        'message' => $e->getMessage(),
        'data'    => $data,
    ]);
    throw $e;
}
```

## Anti-Patterns

- Untyped function parameters or return types
- Using `else` or `elseif` — invert and return early instead
- Silently swallowing exceptions with empty catch blocks
- Using `env()` directly in application code (only in config files)
- Non-English variable names, comments, or method names
- Multiple classes in a single file

## References

- [PHPStan](https://phpstan.org/)
- [Laravel Pint](https://laravel.com/docs/pint)
- Related: `PHPStan/SKILL.md` — static analysis compliance
