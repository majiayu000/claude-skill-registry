---
name: laravel-migrations
description: Create database migrations with schema builder, indexes, foreign keys, and seeders. Use when designing database schema, creating tables, or modifying columns.
user-invocable: false
---

# Laravel Migrations

## Documentation

### Database
- [database.md](docs/database.md) - Database basics
- [migrations.md](docs/migrations.md) - Migrations
- [seeding.md](docs/seeding.md) - Database seeding
- [queries.md](docs/queries.md) - Query builder
- [mongodb.md](docs/mongodb.md) - MongoDB integration

## Migration Template

```php
<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('title');
            $table->string('slug')->unique();
            $table->text('content');
            $table->string('status')->default('draft');
            $table->timestamp('published_at')->nullable();
            $table->timestamps();
            $table->softDeletes();

            $table->index(['status', 'published_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

## Column Types

```php
$table->string('name', 100);           // VARCHAR(100)
$table->text('description');           // TEXT
$table->integer('count');              // INT
$table->decimal('price', 8, 2);        // DECIMAL(8,2)
$table->boolean('is_active');          // BOOLEAN
$table->json('metadata');              // JSON
$table->timestamps();                  // created_at, updated_at
$table->softDeletes();                 // deleted_at
```

## Foreign Keys

```php
$table->foreignId('user_id')->constrained()->cascadeOnDelete();
$table->foreignId('author_id')->constrained('users')->nullOnDelete();
```

## Seeder

```php
<?php

declare(strict_types=1);

namespace Database\Seeders;

final class PostSeeder extends Seeder
{
    public function run(): void
    {
        User::factory()->count(10)->create()->each(function (User $user) {
            Post::factory()->count(5)->for($user)->create();
        });
    }
}
```

## Commands

```bash
php artisan make:migration create_posts_table
php artisan migrate
php artisan migrate:fresh --seed
php artisan migrate:rollback --step=3
```
