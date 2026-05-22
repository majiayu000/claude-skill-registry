---
name: laravel-eloquent
description: >-
  Develops Eloquent models, relationships, scopes, and query optimization. Activates when creating models,
  defining relationships (hasMany, belongsTo, morphTo), writing scopes, eager loading, query building,
  accessors/mutators, model events, or when user mentions model, relationship, query, N+1, eager load,
  scope, or database optimization.
---

# Laravel Eloquent Development

## When to Apply

Activate this skill when:

- Creating or modifying Eloquent models
- Defining model relationships
- Writing query scopes (local or global)
- Optimizing queries or fixing N+1 problems
- Working with accessors, mutators, or casts
- Implementing model events or observers

## Documentation

Use `search-docs` for detailed Eloquent patterns and documentation.

## Basic Usage

### Creating Models

Use Artisan to create models with related files:

```bash
php artisan make:model Post --migration --factory --seeder
```

### Relationships

Always use explicit return types on relationship methods:

<code-snippet name="Eloquent Relationships" lang="php">
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

public function posts(): HasMany
{
    return $this->hasMany(Post::class);
}

public function author(): BelongsTo
{
    return $this->belongsTo(User::class, 'author_id');
}
</code-snippet>

### Eager Loading

Prevent N+1 queries by eager loading relationships:

<code-snippet name="Eager Loading" lang="php">
// Good - eager loads in 2 queries
$posts = Post::with(['author', 'comments'])->get();

// Bad - causes N+1 queries
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->author->name; // Query per post
}
</code-snippet>

### Constraining Eager Loads

<code-snippet name="Constrained Eager Loading" lang="php">
$users = User::with(['posts' => function ($query) {
    $query->where('published', true)
          ->latest()
          ->limit(10);
}])->get();
</code-snippet>

### Local Scopes

<code-snippet name="Local Scopes" lang="php">
use Illuminate\Database\Eloquent\Builder;

public function scopePublished(Builder $query): Builder
{
    return $query->where('published_at', '<=', now());
}

public function scopeByAuthor(Builder $query, User $author): Builder
{
    return $query->where('author_id', $author->id);
}

// Usage
Post::published()->byAuthor($user)->get();
</code-snippet>

### Casts

Define casts in the `casts()` method (Laravel 11+):

<code-snippet name="Model Casts" lang="php">
protected function casts(): array
{
    return [
        'published_at' => 'datetime',
        'metadata' => 'array',
        'is_featured' => 'boolean',
        'status' => PostStatus::class,
    ];
}
</code-snippet>

### Accessors and Mutators

Use attribute casting for simple transformations:

<code-snippet name="Accessors and Mutators" lang="php">
use Illuminate\Database\Eloquent\Casts\Attribute;

protected function fullName(): Attribute
{
    return Attribute::make(
        get: fn () => "{$this->first_name} {$this->last_name}",
    );
}

protected function email(): Attribute
{
    return Attribute::make(
        set: fn (string $value) => strtolower($value),
    );
}
</code-snippet>

## Query Building

Prefer `Model::query()` over `DB::` facade:

<code-snippet name="Query Building" lang="php">
// Good
$posts = Post::query()
    ->where('status', 'published')
    ->whereHas('author', fn ($q) => $q->where('active', true))
    ->orderByDesc('created_at')
    ->paginate(15);

// Avoid
$posts = DB::table('posts')->where(...)->get();
</code-snippet>

## Model Events and Observers

<code-snippet name="Model Observer" lang="php">
// app/Observers/PostObserver.php
class PostObserver
{
    public function creating(Post $post): void
    {
        $post->slug = Str::slug($post->title);
    }

    public function deleted(Post $post): void
    {
        Storage::delete($post->featured_image);
    }
}
</code-snippet>

## Common Pitfalls

- Not using eager loading, causing N+1 queries
- Using `DB::` instead of Eloquent models
- Missing return types on relationship methods
- Forgetting to create factories and seeders with new models
- Using `$casts` property instead of `casts()` method in Laravel 11+
- Not constraining eager loads when only subset of data is needed
