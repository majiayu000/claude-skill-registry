---
name: phpstan
description: Static analysis tool configured at Level 9. All code must pass PHPStan Level 9 with strict typing, no untyped signatures, and minimal suppression of errors.
---

**Name:** PHPStan
**Description:** Static analysis tool configured at Level 9. All code must pass PHPStan Level 9 with strict typing, no untyped signatures, and minimal suppression of errors.
**Compatible Agents:** general-purpose, testing, backend
**Tags:** app/**/*.php, tests/**/*.php, laravel, php, static-analysis, phpstan, types

## Rules

- All code must pass **PHPStan Level 9**
- Type hints on all parameters, return types, and properties — no untyped signatures
- No `@phpstan-ignore` unless documented with a justification comment
- Use `phpstan-assert`, `phpstan-param`, and `phpstan-return` PHPDoc tags when generics or complex types are needed
- Replace `mixed` with specific union types where possible
- Use `array<string, mixed>` instead of bare `array` in PHPDoc
- Add `@throws` annotations for methods that throw exceptions
- Use `assert()` or type narrowing instead of suppressing errors

## Examples

```php
// ✓ Specific types instead of mixed
public function process(Order $order): Invoice { ... }

// ✓ PHPDoc with typed arrays
/**
 * @return array<string, array<int, string|object>>
 */
public function rules(): array { ... }

// ✓ Union types instead of mixed
public function format(string|int|null $value): string { ... }

// ✓ Generics for collections
/**
 * @return Collection<int, Invoice>
 */
public function getInvoices(): Collection { ... }
```

```php
// ✓ @throws annotation
/**
 * @throws InvoiceAlreadyPaidException
 */
public function markAsPaid(Invoice $invoice): void
{
    if ($invoice->isPaid()) {
        throw InvoiceAlreadyPaidException::for($invoice);
    }
    // ...
}
```

```php
// ✓ Type narrowing with assert() instead of suppression
public function handle(mixed $model): void
{
    assert($model instanceof Invoice);
    $model->markAsPaid(); // PHPStan now knows it's an Invoice
}
```

```php
// ✓ Justified suppression with comment
/** @phpstan-ignore-next-line Property accessed via magic method — documented in IDE helper */
$user->custom_attribute;
```

## Anti-Patterns

- Using bare `mixed` types when a more specific type is possible
- Using bare `array` without a PHPDoc generic shape: `array<string, mixed>`
- Using `@phpstan-ignore` without a comment explaining why it is necessary
- Omitting `@throws` annotations on methods that throw
- Leaving parameters, return types, or properties untyped
- Using `(int)`, `(string)` casts as substitutes for proper type narrowing

## References

- [PHPStan Documentation](https://phpstan.org/user-guide/getting-started)
- [PHPStan Rule Levels](https://phpstan.org/user-guide/rule-levels)
- Related: `PHP/SKILL.md` — general PHP conventions including strict typing
