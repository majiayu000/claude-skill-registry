---
name: laravel
description: |
  Laravel 11+ framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Laravel projects, or when the user mentions Laravel.
  Provides Eloquent ORM, Blade templates, routing, middleware, and queue guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: php
  extensions: ".php"
---

# Laravel Guide

> Applies to: Laravel 11+, PHP 8.2+, Full-Stack Web Applications, APIs, SaaS

## Core Principles

1. **Convention Over Configuration**: Follow Laravel's conventions for file placement, naming, and structure
2. **Service Layer**: Keep controllers thin, extract business logic into service classes
3. **Form Requests**: Validate all input through dedicated Form Request classes
4. **Eloquent Relationships**: Use eager loading to prevent N+1 queries
5. **Queue Everything Slow**: Offload email, notifications, and heavy processing to queues

## Guardrails

### Version & Dependencies

- Use Laravel 11+ with PHP 8.2+
- Run `composer install --no-dev` for production
- Use Laravel Pint for code formatting (ships with Laravel)
- Use PHPStan or Larastan for static analysis
- Lock dependency versions in `composer.lock`

### Code Style

- Always use `declare(strict_types=1);` at the top of every PHP file
- Use constructor property promotion for dependency injection
- Use typed properties and return types on all methods
- Follow PSR-12 coding standard (enforced by Pint)
- Use `readonly` properties where values should not change after construction

### Security

- Never use `DB::raw()` without parameter binding
- Always validate input through Form Requests, never in controllers
- Use Sanctum for API authentication, not plain tokens
- Never commit `.env` files; use `.env.example` as template
- Use `$fillable` (whitelist) on models, never `$guarded = []`
- Escape Blade output with `{{ }}` (not `{!! !!}` unless explicitly safe)
- Use CSRF protection on all web routes (enabled by default)

### Performance

- Always eager load relationships: `->with('relation')` or `->load('relation')`
- Use pagination for list endpoints: `->paginate(15)` or `->cursorPaginate(15)`
- Cache expensive queries with `Cache::remember()`
- Use database indexes on columns used in `WHERE`, `ORDER BY`, `JOIN`
- Queue emails, notifications, and any operation >200ms

## Project Structure

```
myapp/
├── app/
│   ├── Console/Commands/    # Artisan commands
│   ├── Enums/               # PHP enums (roles, statuses)
│   ├── Events/              # Domain events
│   ├── Http/
│   │   ├── Controllers/     # Thin controllers (delegate to services)
│   │   ├── Middleware/      # HTTP middleware
│   │   └── Requests/        # Form Request validation
│   ├── Jobs/                # Queued jobs
│   ├── Listeners/           # Event listeners
│   ├── Models/              # Eloquent models
│   ├── Policies/            # Authorization policies
│   ├── Providers/           # Service providers
│   └── Services/            # Business logic layer
├── config/                  # Configuration files
├── database/
│   ├── factories/           # Model factories for testing
│   ├── migrations/          # Always include down() for rollback
│   └── seeders/             # Database seeders
├── resources/views/         # Blade templates
├── routes/
│   ├── api.php              # API routes (versioned: /api/v1/)
│   └── web.php              # Web routes
├── tests/
│   ├── Feature/             # Integration/HTTP tests
│   └── Unit/                # Isolated unit tests
├── .env.example
├── composer.json
└── phpunit.xml
```

## Eloquent Models

### Defining Models

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'title',
        'slug',
        'body',
        'status',
        'user_id',
    ];

    protected $casts = [
        'published_at' => 'datetime',
        'is_featured' => 'boolean',
    ];

    // -- Relationships --

    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }

    // -- Scopes --

    public function scopePublished($query)
    {
        return $query->where('status', 'published')
            ->whereNotNull('published_at');
    }

    // -- Accessors (Laravel 11 attribute casting) --

    public function getExcerptAttribute(): string
    {
        return str()->limit($this->body, 150);
    }
}
```

### Key Eloquent Rules

- Always declare `$fillable` (whitelist) for mass assignment protection
- Use `$casts` for type casting (datetime, boolean, enum, array, json)
- Type-hint relationship return types (`HasMany`, `BelongsTo`, etc.)
- Use SoftDeletes when data should be recoverable
- Name scopes descriptively: `scopeActive`, `scopePublished`, `scopeByRole`

## Routing

### Web Routes

```php
<?php
// routes/web.php

use App\Http\Controllers\PostController;
use Illuminate\Support\Facades\Route;

Route::get('/', fn () => view('welcome'));

Route::middleware('auth')->group(function () {
    Route::resource('posts', PostController::class);
});
```

### API Routes

```php
<?php
// routes/api.php

use App\Http\Controllers\Api\PostController;
use Illuminate\Support\Facades\Route;

Route::prefix('v1')->group(function () {
    Route::middleware('auth:sanctum')->group(function () {
        Route::apiResource('posts', PostController::class);
    });
});
```

### Routing Rules

- Group routes with shared middleware using `Route::middleware()->group()`
- Use `apiResource` for API controllers (excludes `create`/`edit` views)
- Version API routes with prefix: `/api/v1/...`
- Use route model binding for automatic model resolution
- Name routes explicitly when needed: `->name('posts.publish')`

## Controllers

### Controller Pattern (Thin Controller)

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StorePostRequest;
use App\Http\Resources\PostResource;
use App\Models\Post;
use App\Services\PostService;
use Illuminate\Http\JsonResponse;

class PostController extends Controller
{
    public function __construct(
        private readonly PostService $postService,
    ) {}

    public function index(): PostResource
    {
        return PostResource::collection(
            Post::with('author')->published()->paginate(15)
        );
    }

    public function store(StorePostRequest $request): JsonResponse
    {
        $post = $this->postService->create($request->validated());
        return PostResource::make($post)->response()->setStatusCode(201);
    }

    public function show(Post $post): PostResource
    {
        return PostResource::make($post->load('author', 'comments'));
    }

    public function destroy(Post $post): JsonResponse
    {
        $this->authorize('delete', $post);
        $this->postService->delete($post);
        return response()->json(null, 204);
    }
}
```

### Controller Rules

- Delegate business logic to Service classes (thin controllers)
- Use constructor injection with `readonly` for dependencies
- Use Form Requests for validation, API Resources for responses
- Use `$this->authorize()` or Policy middleware for authorization
- One resource per controller; avoid custom methods beyond CRUD

## Blade Templates

### Component Pattern

```blade
{{-- resources/views/components/alert.blade.php --}}
@props(['type' => 'info', 'dismissible' => false])

<div {{ $attributes->merge(['class' => "alert alert-{$type}"]) }}>
    {{ $slot }}
    @if($dismissible)
        <button type="button" class="close">&times;</button>
    @endif
</div>
```

### Blade Rules

- Use `{{ }}` for escaped output (default); `{!! !!}` only for trusted HTML
- Use `@props` in components for typed attributes with defaults
- Use `@stack` / `@push` for page-specific CSS/JS
- Use `@include` for partials, `<x-component>` for reusable components
- Use `@vite()` for asset bundling (replaces Laravel Mix)
- Never put business logic in Blade templates

## Form Request Validation

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Post::class);
    }

    /** @return array<string, mixed> */
    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'slug' => ['required', 'string', 'max:255', Rule::unique('posts')],
            'body' => ['required', 'string', 'min:10'],
            'status' => ['required', Rule::in(['draft', 'published'])],
        ];
    }
}
```

## Middleware

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserHasRole
{
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if ($request->user()?->role !== $role) {
            abort(403, "Role '{$role}' is required.");
        }

        return $next($request);
    }
}
```

Register in `bootstrap/app.php` (Laravel 11+):

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'role' => \App\Http\Middleware\EnsureUserHasRole::class,
    ]);
})
```

## Artisan Commands

```bash
# Scaffolding
php artisan make:model Post -mfcs          # Model + migration + factory + controller + seeder
php artisan make:controller Api/PostController --api
php artisan make:request StorePostRequest
php artisan make:resource PostResource
php artisan make:event PostPublished
php artisan make:job ProcessReport
php artisan make:policy PostPolicy --model=Post

# Database
php artisan migrate                        # Run pending migrations
php artisan migrate:fresh --seed           # Reset DB and seed (dev only)

# Cache & Optimization
php artisan optimize                       # Cache config, routes, views
php artisan optimize:clear                 # Clear all caches (dev)

# Queue & Testing
php artisan queue:work                     # Start queue worker
php artisan test                           # Run PHPUnit
php artisan test --filter=PostTest         # Run specific test
php artisan test --coverage                # With coverage report
```

## Testing

### Feature Test Example

```php
<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_authenticated_user_can_create_post(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
            ->postJson('/api/v1/posts', [
                'title' => 'My Post',
                'slug' => 'my-post',
                'body' => 'Post content here.',
                'status' => 'draft',
            ]);

        $response->assertCreated()
            ->assertJsonPath('data.title', 'My Post');
        $this->assertDatabaseHas('posts', ['slug' => 'my-post']);
    }

    public function test_guest_cannot_create_post(): void
    {
        $this->postJson('/api/v1/posts', ['title' => 'My Post'])
            ->assertUnauthorized();
    }
}
```

### Testing Rules

- Use `RefreshDatabase` trait for database tests
- Use model factories for test data (never insert raw SQL)
- Test happy paths, validation failures, and authorization
- Name tests descriptively: `test_guest_cannot_delete_post`
- Use `actingAs()` for authenticated requests
- Assert both HTTP status and database state
- See [references/patterns.md](references/patterns.md) for factory patterns and advanced testing

## Migrations

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
            $table->text('body');
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

- Always include `down()` for rollback
- Use `foreignId()->constrained()` for foreign keys with cascading
- Add indexes on columns used in `WHERE`, `ORDER BY`
- Never modify a deployed migration; create a new one instead

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Eloquent patterns, jobs/queues, events, Livewire, API resources, deployment

## External References

- [Laravel Documentation](https://laravel.com/docs)
- [Laracasts](https://laracasts.com/)
- [Laravel News](https://laravel-news.com/)
- [Laravel Pint](https://laravel.com/docs/pint)
- [Laravel Sanctum](https://laravel.com/docs/sanctum)
- [Laravel Horizon](https://laravel.com/docs/horizon)
- [Larastan (PHPStan for Laravel)](https://github.com/larastan/larastan)
