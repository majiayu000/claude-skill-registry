---
name: enums
description: PHP backed string enums used instead of constants or magic strings. Enums include `label()` and `color()` helper methods and are cast on Eloquent models.
---

**Name:** Enums
**Description:** PHP backed string enums used instead of constants or magic strings. Enums include `label()` and `color()` helper methods and are cast on Eloquent models.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Enums/**/*.php, laravel, php, backend, enum, status

## Rules

- Use **backed string enums** — never use plain constants or magic strings for finite sets of values
- Include `label(): string` and `color(): string` helper methods on every enum
- Place all enums in `app/Enums/`
- Always cast enum columns in model `casts()` methods
- Use enum string values in migrations: `$table->string('status')->default('draft')`
- Reference enum cases in code, never raw strings: `Status::Draft` not `'draft'`
- Use `match` expressions in `label()` and `color()` — never if/else chains

## Examples

```php
enum Status: string
{
    case Draft    = 'draft';
    case Active   = 'active';
    case Archived = 'archived';

    public function label(): string
    {
        return match ($this) {
            self::Draft    => 'Draft',
            self::Active   => 'Active',
            self::Archived => 'Archived',
        };
    }

    public function color(): string
    {
        return match ($this) {
            self::Draft    => 'gray',
            self::Active   => 'green',
            self::Archived => 'red',
        };
    }
}
```

```php
// Model cast
protected function casts(): array
{
    return [
        'status' => Status::class,
    ];
}

// Usage
if ($invoice->status === Status::Draft) { ... }
echo $invoice->status->label(); // 'Draft'
```

## Anti-Patterns

- Using raw strings instead of enum cases: `'draft'` instead of `Status::Draft`
- Using integer-backed enums when string enums are more readable
- Forgetting to cast enum columns in the model's `casts()` method
- Using if/else chains instead of `match` expressions in `label()` or `color()`
- Putting business logic inside enum methods (beyond label/color presentation helpers)

## References

- [PHP Enums](https://www.php.net/manual/en/language.enumerations.php)
- [Laravel Enum Casting](https://laravel.com/docs/eloquent-mutators#enum-casting)
- Related: `Models/SKILL.md` — for how enums are cast in Eloquent models
