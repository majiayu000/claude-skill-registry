---
name: laravel-eloquent
description: Complete Eloquent ORM - models, relationships, queries, casts, observers, factories. Use when working with database models.
versions:
  laravel: "12.x"
  php: "8.4"
user-invocable: true
references: references/models.md, references/relationships-basic.md, references/relationships-many-to-many.md, references/relationships-advanced.md, references/relationships-polymorphic.md, references/eager-loading.md, references/scopes.md, references/casts.md, references/accessors-mutators.md, references/events-observers.md, references/soft-deletes.md, references/collections.md, references/serialization.md, references/factories.md, references/performance.md, references/resources.md, references/transactions.md, references/pagination.md, references/aggregates.md, references/batch-operations.md, references/query-debugging.md, references/templates/ModelBasic.php.md, references/templates/ModelRelationships.php.md, references/templates/ModelCasts.php.md, references/templates/Observer.php.md, references/templates/Factory.php.md, references/templates/Resource.php.md, references/templates/EagerLoadingExamples.php.md
related-skills: laravel-migrations, laravel-api, laravel-testing
---

# Laravel Eloquent ORM

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing models, relationships
2. **fuse-ai-pilot:research-expert** - Verify latest Eloquent docs via Context7
3. **mcp__context7__query-docs** - Query specific patterns (casts, scopes)

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

Eloquent is Laravel's ActiveRecord ORM implementation. Models represent database tables and provide a fluent interface for queries.

| Feature | Purpose |
|---------|---------|
| **Models** | Table representation with attributes |
| **Relationships** | Define connections between models |
| **Query Scopes** | Reusable query constraints |
| **Casts** | Attribute type conversion |
| **Events/Observers** | React to model lifecycle |
| **Factories** | Generate test data |

---

## Critical Rules

1. **Always eager load relationships** - Prevent N+1 queries
2. **Use scopes for reusable queries** - Don't repeat WHERE clauses
3. **Cast attributes properly** - Type safety for dates, arrays, enums
4. **No business logic in models** - Keep models slim
5. **Use factories for testing** - Never hardcode test data

---

## Decision Guide

### Relationship Type

```
What's the cardinality?
├── One-to-One → hasOne / belongsTo
├── One-to-Many → hasMany / belongsTo
├── Many-to-Many → belongsToMany (pivot table)
├── Through another → hasOneThrough / hasManyThrough
└── Polymorphic?
    ├── One-to-One → morphOne / morphTo
    ├── One-to-Many → morphMany / morphTo
    └── Many-to-Many → morphToMany / morphedByMany
```

### Performance Issue

```
What's the problem?
├── Too many queries → Eager loading (with)
├── Memory exhaustion → chunk() or cursor()
├── Slow queries → Add indexes, select columns
├── Repeated queries → Cache results
└── Large inserts → Batch operations
```

---

## Reference Guide

### Concepts (WHY & Architecture)

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Models** | [models.md](references/models.md) | Model config, fillable, conventions |
| **Basic Relations** | [relationships-basic.md](references/relationships-basic.md) | HasOne, HasMany, BelongsTo |
| **Many-to-Many** | [relationships-many-to-many.md](references/relationships-many-to-many.md) | Pivot tables, attach/sync |
| **Advanced Relations** | [relationships-advanced.md](references/relationships-advanced.md) | Through, dynamic relations |
| **Polymorphic** | [relationships-polymorphic.md](references/relationships-polymorphic.md) | MorphTo, MorphMany |
| **Eager Loading** | [eager-loading.md](references/eager-loading.md) | N+1 prevention, with() |
| **Scopes** | [scopes.md](references/scopes.md) | Local, global, dynamic |
| **Casts** | [casts.md](references/casts.md) | Type casting, custom casts |
| **Accessors/Mutators** | [accessors-mutators.md](references/accessors-mutators.md) | Attribute transformation |
| **Events/Observers** | [events-observers.md](references/events-observers.md) | Lifecycle hooks |
| **Soft Deletes** | [soft-deletes.md](references/soft-deletes.md) | Recoverable deletion |
| **Collections** | [collections.md](references/collections.md) | Eloquent collection methods |
| **Serialization** | [serialization.md](references/serialization.md) | toArray, toJson, hidden |
| **Factories** | [factories.md](references/factories.md) | Test data generation |
| **Performance** | [performance.md](references/performance.md) | Optimization techniques |
| **API Resources** | [resources.md](references/resources.md) | JSON transformation |
| **Transactions** | [transactions.md](references/transactions.md) | Atomic operations, rollback |
| **Pagination** | [pagination.md](references/pagination.md) | paginate, cursor, simplePaginate |
| **Aggregates** | [aggregates.md](references/aggregates.md) | count, sum, withCount, exists |
| **Batch Operations** | [batch-operations.md](references/batch-operations.md) | insert, upsert, mass update |
| **Query Debugging** | [query-debugging.md](references/query-debugging.md) | toSql, dd, DB::listen |

### Templates (Complete Code)

| Template | When to Use |
|----------|-------------|
| [ModelBasic.php.md](references/templates/ModelBasic.php.md) | Standard model with scopes |
| [ModelRelationships.php.md](references/templates/ModelRelationships.php.md) | All relationship types |
| [ModelCasts.php.md](references/templates/ModelCasts.php.md) | Casts and accessors |
| [Observer.php.md](references/templates/Observer.php.md) | Complete observer |
| [Factory.php.md](references/templates/Factory.php.md) | Factory with states |
| [Resource.php.md](references/templates/Resource.php.md) | API resource |
| [EagerLoadingExamples.php.md](references/templates/EagerLoadingExamples.php.md) | N+1 prevention |

---

## Quick Reference

### Basic Model

```php
class Post extends Model
{
    protected $fillable = ['title', 'content', 'author_id'];

    protected function casts(): array
    {
        return [
            'published_at' => 'datetime',
            'metadata' => 'array',
        ];
    }

    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

### Eager Loading

```php
// ✅ Good - 2 queries
$posts = Post::with('author')->get();

// ❌ Bad - N+1 queries
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->author->name;
}
```

### Query Scopes

```php
#[Scope]
protected function published(Builder $query): void
{
    $query->whereNotNull('published_at');
}

// Usage: Post::published()->get();
```

---

## Best Practices

### DO
- Use `$fillable` for mass assignment protection
- Eager load relationships with `with()`
- Use scopes for reusable query logic
- Cast dates, arrays, and enums
- Use factories in tests

### DON'T
- Put business logic in models
- Lazy load in loops (N+1)
- Use `$guarded = []` in production
- Query in accessors/mutators
- Forget foreign keys in `with()` columns
