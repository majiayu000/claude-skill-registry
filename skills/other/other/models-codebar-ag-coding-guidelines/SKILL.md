---
name: models
description: Eloquent model conventions covering mass assignment, casts, relationships, section headers, and activity logging. Every model must follow these structural rules.
---

**Name:** Models
**Description:** Eloquent model conventions covering mass assignment, casts, relationships, section headers, and activity logging. Every model must follow these structural rules.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Models/**/*.php, laravel, php, backend, eloquent, model, database

## Rules

- Use `$guarded = []` — never use `$fillable` arrays
- Define `casts()` as a **method**, not a property
- Cast enums, dates, decimals, and JSON in `casts()`
- Add the `LogsActivity` trait on all business models
- Configure `getActivitylogOptions()` with `logAll()`, `logOnlyDirty()`, `dontSubmitEmptyLogs()`
- Use typed return types on all relationship methods (`HasMany`, `BelongsTo`, etc.)
- Every new model must have a corresponding factory in `database/factories/`
- Group model code with section comment headers: `// --- Relationships ---`, `// --- Status Helpers ---`, etc.

## Examples

```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Spatie\Activitylog\LogOptions;
use Spatie\Activitylog\Traits\LogsActivity;

class Invoice extends Model
{
    use LogsActivity;

    protected $guarded = [];

    protected function casts(): array
    {
        return [
            'status'   => Status::class,
            'due_date' => 'date',
            'amount'   => 'decimal:2',
        ];
    }

    // --- Relationships ---

    public function lines(): HasMany
    {
        return $this->hasMany(InvoiceLine::class);
    }

    // --- Status Helpers ---

    public function isDraft(): bool
    {
        return $this->status === Status::Draft;
    }

    public function isPaid(): bool
    {
        return $this->status === Status::Paid;
    }

    // --- Activity Log ---

    public function getActivitylogOptions(): LogOptions
    {
        return LogOptions::defaults()
            ->logAll()
            ->logOnlyDirty()
            ->dontSubmitEmptyLogs();
    }
}
```

## Anti-Patterns

- Using `$fillable` arrays instead of `$guarded = []`
- Defining `$casts` as a property instead of a `casts()` method
- Not using the `LogsActivity` trait on business models
- Omitting return types on relationship methods
- Creating a model without a corresponding factory
- Putting business logic directly in the model — use Actions

## References

- [Laravel Eloquent Models](https://laravel.com/docs/eloquent)
- [Spatie Activity Log](https://spatie.be/docs/laravel-activitylog/)
- Related: `Enums/SKILL.md` — enums are cast in `casts()`
- Related: `Migrations/SKILL.md` — migrations define the model's schema
