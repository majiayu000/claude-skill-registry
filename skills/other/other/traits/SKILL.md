---
name: traits
description: Reusable behaviour shared across multiple unrelated classes. Traits provide shared Eloquent scopes, accessors, lifecycle hooks, and small stateless helper methods.
---

**Name:** Traits
**Description:** Reusable behaviour shared across multiple unrelated classes. Traits provide shared Eloquent scopes, accessors, lifecycle hooks, and small stateless helper methods.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Traits/**/*.php, laravel, php, backend, trait, reusable, eloquent

## Rules

- Trait classes live in `app/Traits/`
- Each trait should have a **single, clearly defined responsibility**
- Use descriptive names that reflect the behaviour they provide, not the classes that use them
- Suffix with `able` when the trait grants a capability: `Archivable`, `Taggable`, `Sluggable`
- Use a noun phrase when grouping related accessors/scopes: `HasTimestamps`, `HasAddress`
- Use a trait only when the **same behaviour is needed across multiple unrelated classes**
- Use `bootTraitName()` to hook into the model lifecycle without overriding `boot()` in the model
- Use `initializeTraitName()` to set default property values on instantiation
- Never put complex business logic in a trait — use an Action or Service

## Examples

```php
namespace App\Traits;

use Illuminate\Database\Eloquent\Builder;

trait Archivable
{
    public function archive(): void
    {
        $this->update(['archived_at' => now()]);
    }

    public function unarchive(): void
    {
        $this->update(['archived_at' => null]);
    }

    public function isArchived(): bool
    {
        return ! is_null($this->archived_at);
    }

    public function scopeArchived(Builder $query): Builder
    {
        return $query->whereNotNull('archived_at');
    }

    public function scopeNotArchived(Builder $query): Builder
    {
        return $query->whereNull('archived_at');
    }
}
```

```php
trait Sluggable
{
    public static function bootSluggable(): void
    {
        static::creating(function ($model) {
            $model->slug = str($model->name)->slug();
        });
    }

    public function scopeBySlug(Builder $query, string $slug): Builder
    {
        return $query->where('slug', $slug);
    }
}
```

```php
// Usage across unrelated models
class Post extends Model { use Archivable; }
class Supplier extends Model { use Archivable; }

$post->archive();
Post::archived()->get();
```

## Anti-Patterns

- Creating a trait for logic that only exists in one class (keep it inline)
- Putting complex business rules in a trait (use an Action or Service)
- Putting external service dependencies in a trait (use a Service class)
- Using a trait to avoid inheritance instead of reconsidering the architecture
- Creating catch-all traits that bundle unrelated behaviour

## References

- [PHP Traits](https://www.php.net/manual/en/language.oop5.traits.php)
- [Laravel Model Booting](https://laravel.com/docs/eloquent#boot-and-initialize-traits)
- Related: `Models/SKILL.md` — where traits are used on Eloquent models
