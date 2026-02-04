---
name: laravel-migrations
description: Laravel 12 database migrations - Schema Builder, columns, indexes, foreign keys, seeders. Use when designing database schema or managing migrations.
versions:
  laravel: "12.x"
  php: "8.4"
user-invocable: true
references: references/schema.md, references/columns.md, references/indexes.md, references/foreign-keys.md, references/commands.md, references/seeding.md, references/testing.md, references/production.md, references/troubleshooting.md, references/templates/CreateTableMigration.php.md, references/templates/ModifyTableMigration.php.md, references/templates/PivotTableMigration.php.md, references/templates/Seeder.php.md, references/templates/MigrationTest.php.md
related-skills: laravel-eloquent, laravel-testing, laravel-architecture
---

# Laravel Migrations

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing migrations
2. **fuse-ai-pilot:research-expert** - Verify Laravel 12 patterns via Context7
3. **mcp__context7__query-docs** - Check specific Schema Builder features

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Schema Builder** | Create, modify, drop tables |
| **Columns** | 50+ column types with modifiers |
| **Indexes** | Primary, unique, fulltext, spatial |
| **Foreign Keys** | Constraints with cascade options |
| **Seeders** | Populate tables with data |

---

## Critical Rules

1. **Always define down()** - Reversible migrations
2. **Use foreignId()->constrained()** - Not raw unsignedBigInteger
3. **Add indexes on foreign keys** - Performance critical
4. **Test rollback before deploy** - Validate down() works
5. **Never modify deployed migrations** - Create new ones

---

## Decision Guide

### Migration Type

```
Need schema change?
├── New table → make:migration create_X_table
├── Add column → make:migration add_X_to_Y_table
├── Modify column → make:migration modify_X_in_Y_table
├── Add index → make:migration add_index_to_Y_table
└── Seed data → make:seeder XSeeder
```

### Column Type Selection

| Use Case | Type | Example |
|----------|------|---------|
| Primary Key | `id()` | Auto-increment BIGINT |
| Foreign Key | `foreignId()->constrained()` | References parent |
| UUID Primary | `uuid()->primary()` | UUIDs |
| Boolean | `boolean()` | is_active |
| Enum | `enum('status', [...])` | order_status |
| JSON | `json()` | preferences |
| Money | `decimal('price', 10, 2)` | 99999999.99 |
| Timestamps | `timestamps()` | created_at, updated_at |
| Soft Delete | `softDeletes()` | deleted_at |

### Foreign Key Cascade

| Scenario | onDelete | Use Case |
|----------|----------|----------|
| Strict integrity | `restrictOnDelete()` | Financial records |
| Auto-cleanup | `cascadeOnDelete()` | Post → Comments |
| Preserve with null | `nullOnDelete()` | Optional relations |
| No action | `noActionOnDelete()` | Audit logs |

---

## Reference Guide

### Core Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Schema** | [schema.md](references/schema.md) | Table operations |
| **Columns** | [columns.md](references/columns.md) | Column types |
| **Indexes** | [indexes.md](references/indexes.md) | Performance indexes |
| **Foreign Keys** | [foreign-keys.md](references/foreign-keys.md) | Constraints |
| **Commands** | [commands.md](references/commands.md) | Artisan commands |
| **Seeding** | [seeding.md](references/seeding.md) | Populate data |

### Advanced Topics

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Testing** | [testing.md](references/testing.md) | Test migrations |
| **Production** | [production.md](references/production.md) | Deploy safely |
| **Troubleshooting** | [troubleshooting.md](references/troubleshooting.md) | Fix errors |

### Templates

| Template | When to Use |
|----------|-------------|
| [CreateTableMigration.php.md](references/templates/CreateTableMigration.php.md) | New table |
| [ModifyTableMigration.php.md](references/templates/ModifyTableMigration.php.md) | Alter table |
| [PivotTableMigration.php.md](references/templates/PivotTableMigration.php.md) | Many-to-many |
| [Seeder.php.md](references/templates/Seeder.php.md) | Seed patterns |
| [MigrationTest.php.md](references/templates/MigrationTest.php.md) | Test migrations |

---

## Quick Reference

### Create Table

```php
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->cascadeOnDelete();
    $table->string('title');
    $table->text('content');
    $table->enum('status', ['draft', 'published'])->default('draft');
    $table->timestamps();
    $table->softDeletes();

    $table->index(['user_id', 'status']);
});
```

### Modify Table

```php
Schema::table('posts', function (Blueprint $table) {
    $table->string('slug')->after('title')->unique();
    $table->boolean('featured')->default(false);
});
```

### Commands

```bash
php artisan make:migration create_posts_table
php artisan migrate
php artisan migrate:rollback --step=1
php artisan migrate:fresh --seed
```

---

## Best Practices

### DO
- Use `foreignId()->constrained()` for foreign keys
- Add composite indexes for common queries
- Test down() method before deploying
- Use `--pretend` to preview SQL

### DON'T
- Modify already-deployed migrations
- Forget down() method
- Use raw SQL without Schema Builder
- Skip indexes on foreign keys
