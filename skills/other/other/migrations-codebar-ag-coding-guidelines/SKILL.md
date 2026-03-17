---
name: migrations
description: Database schema change files. Always create new files for changes — never modify existing migrations. Use descriptive names, proper foreign key constraints, and reversible `down()` methods.
---

**Name:** Migrations
**Description:** Database schema change files. Always create new files for changes — never modify existing migrations. Use descriptive names, proper foreign key constraints, and reversible `down()` methods.
**Compatible Agents:** general-purpose, backend
**Tags:** database/migrations/**/*.php, laravel, php, backend, database, migration, schema

## Rules

- Always create **new** migration files for database changes — **never** modify existing migration files
- Use descriptive names: `create_invoices_table`, `add_status_to_invoices_table`
- Implement both `up()` and `down()` methods — `down()` must fully reverse `up()`
- Group related columns logically: IDs first, then data, then timestamps
- Use enum string values for status columns: `$table->string('status')->default('draft')`
- Add indexes on columns used in WHERE clauses and foreign keys
- Use `foreignId()->constrained()->cascadeOnDelete()` for foreign keys
- Keep migrations focused — one concern per migration

## Examples

```php
public function up(): void
{
    Schema::create('invoices', function (Blueprint $table) {
        $table->id();
        $table->foreignId('order_id')->constrained()->cascadeOnDelete();
        $table->foreignId('user_id')->constrained()->cascadeOnDelete();
        $table->string('status')->default('draft');
        $table->decimal('amount', 10, 2);
        $table->date('due_date');
        $table->timestamp('paid_at')->nullable();
        $table->timestamps();

        $table->index('status');
    });
}

public function down(): void
{
    Schema::dropIfExists('invoices');
}
```

```php
// Adding a column to an existing table
public function up(): void
{
    Schema::table('invoices', function (Blueprint $table) {
        $table->string('reference')->nullable()->after('status');
    });
}

public function down(): void
{
    Schema::table('invoices', function (Blueprint $table) {
        $table->dropColumn('reference');
    });
}
```

## Anti-Patterns

- Modifying existing migration files instead of creating new ones
- Using an integer default for status columns instead of a string enum value
- Omitting the `down()` method or leaving it empty
- Not adding indexes on foreign key columns and frequently queried columns
- Creating a single migration that makes multiple unrelated schema changes
- Using `$table->integer('status')` instead of `$table->string('status')->default('...')`

## References

- [Laravel Migrations](https://laravel.com/docs/migrations)
- Related: `Models/SKILL.md` — models reflect the schema defined in migrations
- Related: `Enums/SKILL.md` — enum string values used as migration defaults
