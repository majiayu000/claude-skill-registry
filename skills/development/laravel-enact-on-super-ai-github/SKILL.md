---
name: laravel
description: Laravel and PHP development patterns and best practices
license: MIT
compatibility: opencode
---

# Laravel Skill

Comprehensive patterns and best practices for Laravel and PHP development.

## What I Know

### Project Structure

```
app/
├── Http/
│   ├── Controllers/     # Controllers
│   ├── Middleware/      # Middleware
│   ├── Requests/        # Form Requests (validation)
│   └── Resources/       # API Resources
├── Models/              # Eloquent models
├── Services/            # Business logic
├── Exceptions/          # Custom exceptions
└── Helpers/             # Helper functions
```

### Routing

**API Routes**
```php
// routes/api.php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('users', UserController::class);
    Route::prefix('admin')->group(function () {
        Route::apiResource('posts', PostController::class);
    });
});
```

**Web Routes**
```php
// routes/web.php
Route::get('/', [HomeController::class, 'index'])->name('home');
Route::resource('posts', PostController::class);
```

### Controllers

**Best Practice Controller**
```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\StorePostRequest;
use App\Http\Resources\PostResource;
use App\Models\Post;
use Illuminate\Http\JsonResponse;

class PostController extends Controller
{
    public function index()
    {
        $posts = Post::with(['author', 'tags'])
            ->latest()
            ->paginate(20);

        return PostResource::collection($posts);
    }

    public function store(StorePostRequest $request): JsonResponse
    {
        $post = $this->postService->create($request->validated());

        return response()->json([
            'data' => new PostResource($post),
        ], 201);
    }

    public function update(StorePostRequest $request, Post $post): JsonResponse
    {
        $post = $this->postService->update($post, $request->validated());

        return response()->json([
            'data' => new PostResource($post),
        ]);
    }

    public function destroy(Post $post): JsonResponse
    {
        $this->authorize('delete', $post);

        $post->delete();

        return response()->json(null, 204);
    }
}
```

### Services (Business Logic)

**Service Class**
```php
<?php

namespace App\Services;

use App\Models\Post;
use Illuminate\Database\Eloquent\Model;

class PostService
{
    public function create(array $data): Post
    {
        $post = Post::create($data);

        // Handle relationships
        if (isset($data['tags'])) {
            $post->tags()->sync($data['tags']);
        }

        return $post->load(['author', 'tags']);
    }

    public function update(Post $post, array $data): Post
    {
        $post->update($data);

        if (isset($data['tags'])) {
            $post->tags()->sync($data['tags']);
        }

        return $post->load(['author', 'tags']);
    }
}
```

### Models

**Eloquent Model**
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Post extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
        'content',
        'author_id',
        'published_at',
    ];

    protected $casts = [
        'published_at' => 'datetime',
    ];

    protected $hidden = [
        'deleted_at',
    ];

    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'author_id');
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class)
            ->withTimestamps();
    }

    public function scopePublished($query)
    {
        return $query->whereNotNull('published_at')
            ->where('published_at', '<=', now());
    }

    public function scopeWithTag($query, string $tag)
    {
        return $query->whereHas('tags', function ($q) use ($tag) {
            $q->where('name', $tag);
        });
    }
}
```

### Validation

**Form Request**
```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Contracts\Validation\ValidationRule;

class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Post::class);
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'content' => ['required', 'string'],
            'tags' => ['array'],
            'tags.*' => ['exists:tags,id'],
            'published_at' => ['nullable', 'date'],
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'A title is required',
            'content.required' => 'Content cannot be empty',
        ];
    }
}
```

### API Resources

**Resource**
```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class PostResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'excerpt' => Str::limit($this->content, 150),
            'author' => new UserResource($this->whenLoaded('author')),
            'tags' => TagResource::collection($this->whenLoaded('tags')),
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),
        ];
    }
}
```

### Migrations

**Migration**
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('author_id')->constrained('users')->cascadeOnDelete();
            $table->string('title');
            $table->text('content');
            $table->timestamp('published_at')->nullable();
            $table->softDeletes();
            $table->timestamps();

            $table->index(['author_id', 'published_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

### Jobs & Queues

**Job Class**
```php
<?php

namespace App\Jobs;

use App\Models\Post;
use App\Services\NotificationService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class PublishPostJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public $tries = 3;
    public $timeout = 120;

    public function __construct(
        public Post $post
    ) {}

    public function handle(NotificationService $notification): void
    {
        $this->post->update(['published_at' => now()]);
        $notification->notifyPostPublished($this->post);
    }

    public function failed(\Throwable $exception): void
    {
        \Log::error('Failed to publish post: ' . $exception->getMessage());
    }
}
```

### Events & Listeners

**Event**
```php
<?php

namespace App\Events;

use App\Models\Post;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class PostPublished
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public Post $post
    ) {}
}
```

**Listener**
```php
<?php

namespace App\Listeners;

use App\Events\PostPublished;
use App\Services\SubscriptionService;

class NotifySubscribers
{
    public function __construct(
        private SubscriptionService $subscription
    ) {}

    public function handle(PostPublished $event): void
    {
        $this->subscription->notifyAbout($event->post);
    }
}
```

### Middleware

**Custom Middleware**
```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserHasRole
{
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if (!$request->user()?->hasRole($role)) {
            return response()->json(['error' => 'Forbidden'], 403);
        }

        return $next($request);
    }
}
```

### Config

**Service Provider**
```php
<?php

namespace App\Providers;

use App\Services\PostService;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(PostService::class);
    }

    public function boot(): void
    {
        // Blade directives, macros, etc.
    }
}
```

### Testing

**Feature Test**
```php
<?php

namespace Tests\Feature;

use App\Models\Post;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostManagementTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_post(): void
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        $response = $this->postJson('/api/posts', [
            'title' => 'Test Post',
            'content' => 'Test content',
        ]);

        $response->assertStatus(201)
            ->assertJsonPath('data.title', 'Test Post');

        $this->assertDatabaseHas('posts', [
            'title' => 'Test Post',
            'author_id' => $user->id,
        ]);
    }
}
```

### Common Patterns

**Repository Pattern (Optional)**
```php
<?php

namespace App\Repositories;

use App\Models\Post;
use Illuminate\Pagination\LengthAwarePaginator;

interface PostRepositoryInterface
{
    public function all(): LengthAwarePaginator;
    public function find(int $id): ?Post;
    public function create(array $data): Post;
    public function update(Post $post, array $data): Post;
    public function delete(Post $post): bool;
}

class EloquentPostRepository implements PostRepositoryInterface
{
    public function all(): LengthAwarePaginator
    {
        return Post::with(['author', 'tags'])
            ->latest()
            ->paginate(20);
    }
    // ... other methods
}
```

### Best Practices

1. **Use Form Requests** for validation (not in controllers)
2. **Use Services** for business logic (not in controllers)
3. **Use API Resources** for consistent responses
4. **Use Route Model Binding** for type-hinted models
5. **Use Eloquent relationships** instead of manual joins
6. **Use migrations** for all schema changes
7. **Use queues** for long-running tasks
8. **Use config** for environment-specific settings
9. **Implement rate limiting** for API endpoints
10. **Use database transactions** for multi-step operations
11. **Cache frequently accessed data** with Redis
12. **Sanitize user input** to prevent XSS attacks

### Common Pitfalls

1. **N+1 queries** → Use eager loading (`with()`)
2. **Fat controllers** → Move logic to services
3. **Direct env() calls** → Use config instead
4. **Mass assignment vulnerabilities** → Use `$fillable` or guarded
5. **Missing foreign key constraints** → Use database constraints
6. **Not using transactions** → Wrap multi-step operations in transactions
7. **Forgetting to cache** → Use Redis caching for expensive queries
8. **SQL injection** → Use parameterized queries (Eloquent handles this)

### API Design Patterns

**RESTful Resource Controller**
```php
// routes/api.php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('users', UserController::class);
    Route::apiResource('posts', PostController::class);
});

// With additional routes
Route::prefix('posts')->group(function () {
    Route::apiResource('posts', PostController::class);
    Route::get('posts/{post}/comments', [PostCommentController::class, 'index']);
    Route::post('posts/{post}/comments', [PostCommentController::class, 'store']);
});
```

**API Versioning**
```php
// routes/api.php
Route::prefix('v1')->group(function () {
    Route::apiResource('users', UserV1Controller::class);
});

Route::prefix('v2')->group(function () {
    Route::apiResource('users', UserV2Controller::class);
});
```

**Standardized Response**
```php
// app/Http/Responses/ApiResponse.php
<?php

namespace App\Http\Responses;

class ApiResponse
{
    public static function success(
        $data = null,
        string $message = 'Success',
        int $statusCode = 200
    ) {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data' => $data,
        ], $statusCode);
    }

    public static function error(
        string $message = 'Error',
        int $statusCode = 400,
        $errors = null
    ) {
        return response()->json([
            'success' => false,
            'message' => $message,
            'errors' => $errors,
        ], $statusCode);
    }

    public static function paginated(
        $data,
        int $statusCode = 200
    ) {
        return response()->json([
            'success' => true,
            'data' => $data->items(),
            'meta' => [
                'current_page' => $data->currentPage(),
                'last_page' => $data->lastPage(),
                'per_page' => $data->perPage(),
                'total' => $data->total(),
            ],
        ], $statusCode);
    }
}
```

**Rate Limiting**
```php
// routes/api.php
use Illuminate\Support\Facades\RateLimiter;

// Global API rate limit
RateLimiter::for('api', function (Request $request) {
    return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
});

// Apply to routes
Route::middleware(['throttle:api'])->group(function () {
    Route::apiResource('posts', PostController::class);
});

// Stricter for auth endpoints
RateLimiter::for('auth', function (Request $request) {
    return Limit::perMinute(5)->by($request->ip());
});

Route::middleware(['throttle:auth'])->group(function () {
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/register', [AuthController::class, 'register']);
});
```

### Database Patterns

**Query Scopes**
```php
// app/Models/Post.php
class Post extends Model
{
    public function scopePublished($query)
    {
        return $query->whereNotNull('published_at')
            ->where('published_at', '<=', now());
    }

    public function scopeWithTag($query, string $tag)
    {
        return $query->whereHas('tags', function ($q) use ($tag) {
            $q->where('name', $tag);
        });
    }

    public function scopeSearch($query, string $search)
    {
        return $query->where('title', 'like', "%{$search}%")
            ->orWhere('content', 'like', "%{$search}%");
    }
}

// Usage
$posts = Post::published()->withTag('laravel')->search('tutorial')->get();
```

**Eager Loading Strategies**
```php
// Prevent N+1 queries
$posts = Post::with(['author', 'tags', 'comments'])->paginate(20);

// Nested eager loading
$users = User::with(['posts.tags', 'posts.comments'])->get();

// Conditional eager loading
$posts = Post::when(request()->include('author'), function ($q) {
    return $q->with('author');
})->get();

// Lazy eager loading
$posts = Post::all();
$posts->load(['author', 'tags']);
```

**Database Transactions**
```php
// app/Services/OrderService.php
class OrderService
{
    public function createOrder(array $data): Order
    {
        return DB::transaction(function () use ($data) {
            // Create order
            $order = Order::create([
                'user_id' => $data['user_id'],
                'total' => $data['total'],
            ]);

            // Create order items
            foreach ($data['items'] as $item) {
                OrderItem::create([
                    'order_id' => $order->id,
                    'product_id' => $item['product_id'],
                    'quantity' => $item['quantity'],
                    'price' => $item['price'],
                ]);

                // Update inventory
                Product::where('id', $item['product_id'])
                    ->decrement('stock', $item['quantity']);
            }

            // Process payment
            $this->paymentService->charge($order);

            return $order;
        });
    }
}
```

**Query Optimization**
```php
// Select only needed columns
$users = User::select(['id', 'name', 'email'])->get();

// Use chunk for large datasets
User::chunk(1000, function ($users) {
    foreach ($users as $user) {
        // Process user
    }
});

// Use lazy collection for memory efficiency
User::lazy()->each(function ($user) {
    // Process user
});

// Use indexes in migration
$table->index(['user_id', 'created_at']);
$table->unique('email');

// Use count instead of getCollection->count()
$count = User::where('active', true)->count();
```

**Database Indexes**
```php
// database/migrations/xxxx_create_posts_table.php
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('author_id')->constrained()->cascadeOnDelete();
    $table->string('slug')->unique();
    $table->string('title');
    $table->text('content');
    $table->timestamp('published_at')->nullable();
    $table->timestamps();

    // Indexes for common queries
    $table->index(['author_id', 'published_at']);
    $table->index('published_at');
});

// Composite index for sorting
$table->index(['status', 'created_at']);
```

### Security Patterns

**Authentication with Laravel Sanctum**
```php
// config/sanctum.php
'expiration' => 60, // Token expires in 60 minutes

// Controller
use Illuminate\Http\Request;
use Laravel\Sanctum\PersonalAccessToken;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        if (!Auth::attempt($request->only('email', 'password'))) {
            return response()->json(['error' => 'Invalid credentials'], 401);
        }

        $token = $request->user()->createToken('auth-token')->plainTextToken;

        return response()->json(['token' => $token]);
    }

    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();
        return response()->json(['message' => 'Logged out']);
    }
}
```

**Authorization with Policies**
```php
// app/Policies/PostPolicy.php
class PostPolicy
{
    public function view(User $user, Post $post)
    {
        return $post->published_at !== null || $user->id === $post->author_id;
    }

    public function update(User $user, Post $post)
    {
        return $user->id === $post->author_id;
    }

    public function delete(User $user, Post $post)
    {
        return $user->id === $post->author_id || $user->isAdmin();
    }
}

// In Controller
public function update(Post $post)
{
    $this->authorize('update', $post);

    $post->update(request()->validated());
    return new PostResource($post);
}
```

**CSRF Protection**
```php
// Handle API routes that don't need CSRF
// app/Http/Middleware/VerifyCsrfToken.php
class VerifyCsrfToken extends Middleware
{
    protected $except = [
        'api/*', // Exclude all API routes
        'stripe/*', // Exclude webhook endpoints
    ];
}
```

**Input Validation and Sanitization**
```php
// app/Http/Requests/StorePostRequest.php
class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'content' => ['required', 'string'],
            'tags' => ['array', 'max:5'],
            'tags.*' => ['exists:tags,id'],
            'excerpt' => ['nullable', 'string', 'max:500'],
        ];
    }

    public function prepareForValidation()
    {
        $this->merge([
            'title' => strip_tags($this->title),
            'excerpt' => strip_tags($this->excerpt),
        ]);
    }
}
```

**SQL Injection Prevention**
```php
// Laravel's query builder and Eloquent automatically prevent SQL injection

// Good - Using parameterized queries
DB::table('users')->where('email', $email)->first();
User::where('email', $email)->first();

// Bad - Never do this
DB::select("SELECT * FROM users WHERE email = '$email'");

// For raw queries, use bindings
DB::select('SELECT * FROM users WHERE email = :email', ['email' => $email]);
```

**Mass Assignment Protection**
```php
// app/Models/User.php
class User extends Model
{
    protected $fillable = ['name', 'email', 'password'];

    // OR use guarded
    protected $guarded = ['id', 'is_admin'];
}
```

### Performance Patterns

**Caching with Redis**
```php
// Cache query results
$users = Cache::remember('users.all', 3600, function () {
    return User::with(['posts', 'roles'])->get();
});

// Cache with tags
Cache::tags(['posts', 'user:' . $userId])->remember("user.{$userId}.posts", 3600, function () use ($userId) {
    return Post::where('user_id', $userId)->get();
});

// Clear cache on update
class PostObserver
{
    public function updated(Post $post)
    {
        Cache::forget("post.{$post->id}");
        Cache::tags(['posts'])->flush();
    }
}
```

**Query Optimization**
```php
// Use eager loading
$posts = Post::with(['author', 'tags', 'comments'])->get();

// Select specific columns
$users = User::select(['id', 'name', 'email'])->get();

// Use pagination
$posts = Post::with(['author'])->paginate(20);

// Chunk large results
DB::table('users')->orderBy('id')->chunk(1000, function ($users) {
    foreach ($users as $user) {
        // Process user
    }
});

// Use lazy collections
User::lazy()->each(function ($user) {
    // Process user without loading all into memory
});
```

**Queue for Long-Running Tasks**
```php
// jobs/SendWelcomeEmail.php
class SendWelcomeEmail implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public $tries = 3;
    public $timeout = 120;

    public function __construct(public User $user) {}

    public function handle(MailService $mail): void
    {
        $mail->sendWelcomeEmail($this->user);
    }
}

// Dispatch job
SendWelcomeEmail::dispatch($user);
```

**Route Caching**
```bash
# Cache routes for production
php artisan route:cache

# Clear cache when routes change
php artisan route:clear
```

**Config Caching**
```bash
# Cache config for production
php artisan config:cache

# Clear cache
php artisan config:clear
```

**Artisan Commands for Maintenance**
```bash
# Clear all caches
php artisan optimize:clear

# Optimize for production
php artisan optimize

# Compile views
php artisan view:cache
```

## Version Notes

### Supported Versions
- **Recommended:** Laravel 12.x (latest stable)
- **Minimum:** Laravel 10+ (PHP 8.1+)

### Version Summary

| Version | Status | PHP Required | Key Features |
|---------|--------|--------------|--------------|
| 12.x | Latest (Feb 2025) | 8.2+ | Queue batches 2.0, typed properties, health checks, streamlined structure |
| 11.x | Stable (Mar 2024) | 8.2+ | Slimmed application structure, per-second rate limiting, improved health |
| 10.x | Stable (Feb 2023) | 8.1+ | Native types, process helpers, Horizon & Scout improvements |

### Recent Breaking Changes

#### Laravel 11 → 12
<!-- 🆕 v12: Queue batches 2.0 with improved API -->
```php
// v12: New batch API
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

$batch = Bus::batch([
    new Job1(),
    new Job2(),
])->then(function (Batch $batch) {
    // All jobs complete
})->catch(function (Batch $batch, Throwable $e) {
    // First failure
})->finally(function (Batch $batch) {
    // All jobs complete
})->name('Process Order')->dispatch();
```

<!-- 🆕 v12: Typed model properties default -->
```php
// v12+: Models have typed properties by default
class User extends Model
{
    public string $name;
    public string $email;
    protected $fillable = ['name', 'email'];
}
```

<!-- 🆕 v12: Improved health checks -->
```php
// routes/web.php - v12 health endpoint
use Illuminate\Support\Facades\Health;

Health::check('database', fn () => DB::connection()->getPdo());
Health::check('redis', fn () => Redis::connection()->ping());
Health::check('storage', fn () => is_writable(storage_path()));

// Automatic /health endpoint registered
```

<!-- 🔄 v12: Application structure changes -->
```bash
# v12: Even slimmer structure
# - No bootstrap/app.php (config handled automatically)
# - routes/ consolidated
# - Simplified configuration
```

#### Laravel 10 → 11
<!-- 🔄 v11: Slimmed application structure -->
```bash
# v11: Reduced default files
# - No HTTP/Kernel.php, Console/Kernel.php
# - Merged exceptions handling
# - Fewer config files
```

<!-- 🆕 v11: Per-second rate limiting -->
```php
// v11+: Per-second rate limiting
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('api', function (Request $request) {
    return Limit::perSecond(10)->by($request->user()?->id ?: $request->ip());
});
```

<!-- 🆕 v11: Once helper for lazy evaluation -->
```php
// v11+: Once helper for expensive operations
use function Illuminate\Support\once;

$user = once(fn () => User::firstWhere('email', 'user@example.com'));
```

<!-- 🆕 v11: Improved health checks -->
```php
// v11+: Health checks built-in
php artisan make:command HealthCheckCommand

// Built-in health endpoint available
GET /up
```

#### Laravel 9 → 10
<!-- 🆕 v10: Native type declarations -->
```php
// v10+: All framework code has native type hints
// Application code should also use types
public function store(StorePostRequest $request): JsonResponse
{
    return response()->json(['data' => $post], 201);
}
```

<!-- 🔄 v10: Process helpers -->
```php
// v10+: New process helpers
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

if ($result->successful()) {
    echo $result->output();
}
```

<!-- 🚫 v10: PHP 8.0 minimum required -->
<!-- 🚫 v10: Several deprecated features removed -->

### Version Callouts by Feature

**Routing**
<!-- ✅ v10+: All routing patterns stable -->
```php
// Stable across v10, v11, v12
Route::apiResource('posts', PostController::class);
Route::middleware('auth:sanctum')->group(function () {
    // Routes
});
```

**Eloquent Models**
<!-- ✅ v10+: All model patterns stable -->
<!-- 🆕 v12: Typed properties encouraged -->
```php
// v12+: Use typed properties
class Post extends Model
{
    public string $title;
    public string $content;
    protected $fillable = ['title', 'content'];

    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

**Migrations**
<!-- ✅ v10+: All migration patterns stable -->
```php
// Stable across versions
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('author_id')->constrained()->cascadeOnDelete();
    $table->string('title');
    $table->timestamps();
});
```

**Queues**
<!-- ✅ v10+: Job patterns stable -->
<!-- 🆕 v12: Improved batch API -->
```php
// v12+: Better batch API
$batch = Bus::batch([
    new ProcessOrder($order),
    new SendNotification($order),
])->allowFailures()->dispatch();
```

**Validation**
<!-- ✅ v10+: Form Request patterns stable -->
```php
// Stable across versions
class StorePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'content' => ['required', 'string'],
        ];
    }
}
```

**Sanctum Authentication**
<!-- ✅ v10+: Sanctum API stable -->
```php
// Stable across versions
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('users', UserController::class);
});
```

**Application Structure**
<!-- 🔄 v11: Slimmed structure -->
<!-- 🔄 v12: Further simplification -->
```bash
# v10: Traditional structure
app/
├── Http/
│   ├── Controllers/
│   ├── Middleware/
│   └── Kernel.php

# v11+: No Kernel.php, merged middleware
# v12+: Even simpler bootstrap, fewer config files
```

**Testing**
<!-- ✅ v10+: All testing patterns stable -->
```php
// Stable across versions
class PostTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_post(): void
    {
        $response = $this->postJson('/api/posts', [
            'title' => 'Test',
        ]);

        $response->assertStatus(201);
    }
}
```

### Upgrade Recommendations

**From 10 to 11:**
1. Run `composer require laravel/framework:^11.0`
2. Review application structure changes
3. Remove unused config files
4. Update custom middleware to remove constructor dependencies
5. Test per-second rate limiting implementation

**From 11 to 12:**
1. Run `composer require laravel/framework:^12.0`
2. Add typed properties to models
3. Review batch API updates
4. Implement new health checks
5. Test queue batches thoroughly

### Minimum Requirements by Version

| Version | PHP | Release Date | Support Until |
|---------|-----|--------------|---------------|
| 12.x | 8.2+ | Feb 2025 | Aug 2026 |
| 11.x | 8.2+ | Mar 2024 | Aug 2025 |
| 10.x | 8.1+ | Feb 2023 | Feb 2025 |

### Annual Release Cycle

Laravel follows an annual release cycle with major releases in February:
- **Laravel 12**: February 2025
- **Laravel 11**: February 2024
- **Laravel 10**: February 2023

Each version receives bug fixes for 18 months and security fixes for 2 years.

---

*Part of SuperAI GitHub - Centralized OpenCode Configuration*
