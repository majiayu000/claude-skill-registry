---
name: helpers
description: Stateless utility classes providing shared formatting, conversion, or calculation logic needed across multiple parts of the application.
---

**Name:** Helpers
**Description:** Stateless utility classes providing shared formatting, conversion, or calculation logic needed across multiple parts of the application.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Helpers/**/*.php, laravel, php, backend, helper, utility

## Rules

- Helper classes live in `app/Helpers/`
- Naming: `PascalCase` with a `Helper` suffix → `StringHelper`, `MoneyHelper`, `DateHelper`
- Helpers are for utilities needed in **multiple places** across the project
- For testability, static methods are acceptable but not enforced — use your judgement
- Never put business logic in helpers — use Actions or Services
- Never put database queries in helpers — use Model Scopes
- Never put HTTP requests in helpers — use Services

## Examples

```php
namespace App\Helpers;

use Carbon\Carbon;

class DateHelper
{
    public static function format(mixed $date, string $format = 'd M Y'): ?string
    {
        if (is_null($date)) {
            return null;
        }

        return Carbon::parse($date)->format($format);
    }
}
```

```php
namespace App\Helpers;

class MoneyHelper
{
    public static function format(int $amountInCents, string $currency = 'CHF'): string
    {
        return number_format($amountInCents / 100, 2) . ' ' . $currency;
    }
}
```

```php
// Usage in a Resource
'created_at' => DateHelper::format($this->created_at),
'amount'     => MoneyHelper::format($this->amount_in_cents),
```

## Anti-Patterns

- Putting business logic in a helper (belongs in an Action or Service)
- Putting database queries in a helper (use Model scopes instead)
- Using a helper for logic only needed in one place (keep it inline)
- Creating a catch-all `AppHelper` or `Utils` class — keep helpers domain-specific

## References

- [Carbon Documentation](https://carbon.nesbot.com/)
- Related: `Actions/SKILL.md` — for business logic
- Related: `Resources/SKILL.md` — helpers are commonly used for formatting in API resources
