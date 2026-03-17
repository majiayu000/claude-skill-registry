---
name: database-change-management
description: |
  Plan and implement safe database schema changes including migrations, indexes, and backfills. Use when creating
  tables, adding columns, optimizing queries, or managing Eloquent/SQLAlchemy relationships. EXCLUSIVE to database-admin agent.
allowed-tools: Read, Edit, Bash, Grep, Glob, Write, mcp_context7
---
# Database Change Management

**Exclusive to:** `database-admin` agent

## 📚 Context7 (Memory) — Up-to-Date Docs

Lookup latest ORM patterns before implementing:
```
mcp_context7_resolve-library-id(libraryName="laravel", query="eloquent relationships")
mcp_context7_query-docs(libraryId="/laravel/docs", query="migrations foreign keys")
```

## Validation Loop (MANDATORY)

Every migration MUST pass this verification sequence:
```bash
php artisan migrate        # Run migration
php artisan migrate:rollback   # Verify rollback works
php artisan migrate        # Re-run migration
composer test             # All tests still pass
```

**Do NOT complete until all steps succeed.**

## Instructions

1. Audit existing migrations and models for current schema
2. Design migration with reversible `down()` method
3. Run `migrate` and `rollback` to validate locally
4. Update Eloquent model ($fillable, $casts, relationships)
5. Document any required backfills or deployment order

## Safe Migration Patterns

### Adding Columns
```php
// ✅ Safe: nullable or with default
$table->string('field')->nullable();
$table->boolean('active')->default(true);

// ❌ Unsafe: NOT NULL without default
$table->string('field');
```

### Adding Indexes
```php
// Index for WHERE/ORDER BY columns
$table->index('user_id');
$table->index(['status', 'created_at']);
```

### Zero-Downtime Strategy
1. **Add** — Add nullable column
2. **Backfill** — Populate data in chunks
3. **Enforce** — Make column required

## Backfill Pattern
```php
Model::query()
    ->whereNull('new_field')
    ->chunkById(1000, function ($items) {
        foreach ($items as $item) {
            $item->update(['new_field' => $value]);
        }
    });
```

## Eloquent Relationships

### One-to-Many
```php
// User has many Posts
public function posts(): HasMany
{
    return $this->hasMany(Post::class);
}
```

### Many-to-Many
```php
public function tags(): BelongsToMany
{
    return $this->belongsToMany(Tag::class)
        ->withTimestamps();
}
```

## Query Optimization

### Eager Loading
```php
// ❌ N+1 Problem
foreach (Post::all() as $post) {
    echo $post->user->name;
}

// ✅ Eager Load
Post::with('user')->get();
```

### Index Strategy
| Query Pattern | Index |
|---------------|-------|
| `WHERE user_id = ?` | `index('user_id')` |
| `WHERE status = ? AND date > ?` | `index(['status', 'date'])` |

## Common Pitfalls
- ❌ NOT NULL without default on existing table
- ❌ Dropping columns without backup
- ❌ Missing indexes on foreign keys
- ❌ Missing `down()` method

## Verification
```bash
php artisan migrate
php artisan migrate:rollback
php artisan migrate
```

## Examples
- "Add an index to speed up dashboard query"
- "Add a nullable column then backfill safely"
