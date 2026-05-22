---
name: developing-with-laravel
description: Laravel framework patterns for PHP applications including Eloquent ORM, migrations, routing, queues, and Blade templates. Use when building Laravel applications or working with Laravel projects.
---

# Laravel Skill - Quick Reference

Laravel framework patterns for modern PHP applications. For PHP language fundamentals, see the PHP skill. For advanced patterns, see [REFERENCE.md](./REFERENCE.md).

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Routing & Controllers](#routing--controllers)
3. [Eloquent ORM](#eloquent-orm)
4. [Validation](#validation)
5. [Middleware](#middleware)
6. [Authentication](#authentication)
7. [Artisan CLI](#artisan-cli)
8. [Queues & Jobs](#queues--jobs)
9. [Events & Listeners](#events--listeners)
10. [Testing](#testing)
11. [Service Providers](#service-providers)
12. [Task Scheduling](#task-scheduling)

---

## Project Structure

```
app/
├── Console/Commands/       # Artisan commands
├── Http/
│   ├── Controllers/        # Request handlers
│   ├── Middleware/         # Request/response filters
│   └── Requests/           # Form validation
├── Jobs/                   # Queueable jobs
├── Models/                 # Eloquent models
├── Providers/              # Service providers
└── Services/               # Business logic

config/                     # Configuration files
database/
├── factories/              # Model factories
├── migrations/             # Database migrations
└── seeders/                # Database seeders
routes/
├── api.php                 # API routes
└── web.php                 # Web routes
tests/
├── Feature/                # Integration tests
└── Unit/                   # Unit tests
```

---

## Routing & Controllers

### Route Definitions

```php
// Basic routes
Route::get('/users', [UserController::class, 'index']);
Route::post('/users', [UserController::class, 'store']);

// Resource routes (all CRUD)
Route::resource('posts', PostController::class);
Route::apiResource('comments', CommentController::class);

// Route groups with middleware
Route::prefix('api/v1')->middleware(['auth:sanctum'])->group(function () {
    Route::get('/profile', [ProfileController::class, 'show']);
});
```

### Controllers

```php
class UserController extends Controller
{
    public function index()
    {
        return UserResource::collection(
            User::with(['profile', 'roles'])->paginate(20)
        );
    }

    public function store(StoreUserRequest $request)
    {
        return new UserResource(User::create($request->validated()));
    }

    public function show(User $user)  // Route model binding
    {
        return new UserResource($user->load('profile'));
    }
}
```

---

## Eloquent ORM

### Model Definition

```php
class Post extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = ['title', 'slug', 'content', 'status', 'author_id'];
    protected $casts = ['status' => PostStatus::class, 'published_at' => 'datetime'];
    protected $with = ['author'];  // Always eager load

    // Relationships
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'author_id');
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class)->withTimestamps();
    }

    // Scopes
    public function scopePublished(Builder $query): void
    {
        $query->where('status', PostStatus::Published)
              ->where('published_at', '<=', now());
    }

    // Accessors (Laravel 9+)
    protected function excerpt(): Attribute
    {
        return Attribute::make(
            get: fn () => Str::limit(strip_tags($this->content), 150),
        );
    }
}
```

### Relationships Quick Reference

| Method | Relationship | Example |
|--------|--------------|---------|
| `hasOne` | 1:1 | User has one Profile |
| `belongsTo` | 1:1 inverse | Profile belongs to User |
| `hasMany` | 1:n | User has many Posts |
| `belongsToMany` | n:n | Post has many Tags |
| `morphMany` | 1:n polymorphic | Post has many Comments |

> **Advanced**: For hasOneThrough, hasManyThrough, polymorphic relationships, see [REFERENCE.md](./REFERENCE.md#2-eloquent-advanced-patterns)

### Query Builder

```php
// Filtering
$posts = Post::where('status', 'published')
    ->whereHas('tags', fn($q) => $q->where('name', 'laravel'))
    ->with(['author', 'comments'])
    ->latest('published_at')
    ->paginate(10);

// Aggregates
$count = Post::where('status', 'published')->count();
$avg = Order::avg('total');

// Chunking for large datasets
Post::chunk(100, fn($posts) => $posts->each->process());
```

### Transactions

```php
// Closure-based (auto commit/rollback)
$order = DB::transaction(function () use ($data) {
    $order = Order::create($data['order']);
    foreach ($data['items'] as $item) {
        $order->items()->create($item);
    }
    return $order;
});
```

---

## Validation

### Form Requests

```php
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
            'slug' => ['required', Rule::unique('posts')->ignore($this->post)],
            'content' => ['required', 'string', 'min:100'],
            'status' => ['required', Rule::enum(PostStatus::class)],
            'category_id' => ['required', 'exists:categories,id'],
            'tags' => ['array'],
            'tags.*' => ['exists:tags,id'],
        ];
    }

    public function messages(): array
    {
        return ['title.required' => 'A post title is required.'];
    }
}
```

### Common Validation Rules

| Rule | Description |
|------|-------------|
| `required` | Must be present and not empty |
| `nullable` | Can be null |
| `string`, `integer`, `boolean` | Type validation |
| `email` | Valid email format |
| `unique:table,column` | Unique in database |
| `exists:table,column` | Must exist in database |
| `in:a,b,c` | Must be one of values |
| `min:n`, `max:n` | Size constraints |

> **Advanced**: For custom validation rules and complex conditional validation, see [REFERENCE.md](./REFERENCE.md#4-validation-advanced)

---

## Middleware

```php
class EnsureUserIsActive
{
    public function handle(Request $request, Closure $next): Response
    {
        if (!$request->user()?->isActive()) {
            return response()->json(['message' => 'Account inactive.'], 403);
        }
        return $next($request);
    }
}

// With parameters
class CheckRole
{
    public function handle(Request $request, Closure $next, string ...$roles): Response
    {
        if (!$request->user()?->hasAnyRole($roles)) {
            abort(403);
        }
        return $next($request);
    }
}
// Usage: Route::middleware('role:admin,moderator')
```

> **Advanced**: For tenant-scoping middleware and session management, see [REFERENCE.md](./REFERENCE.md#7-multi-tenancy-patterns)

---

## Authentication

### Sanctum (API Tokens)

```php
// Login and issue token
public function login(LoginRequest $request)
{
    $user = User::where('email', $request->email)->first();

    if (!$user || !Hash::check($request->password, $user->password)) {
        throw ValidationException::withMessages([
            'email' => ['Invalid credentials.'],
        ]);
    }

    $user->tokens()->delete();  // Revoke existing
    $token = $user->createToken('api-token', ['read', 'write'])->plainTextToken;

    return response()->json(['user' => new UserResource($user), 'token' => $token]);
}

// Protected routes
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', fn(Request $request) => $request->user());
});
```

> **Advanced**: For Passport OAuth, spatie/permission RBAC, see [REFERENCE.md](./REFERENCE.md#8-authentication-advanced)

---

## Artisan CLI

### Custom Command

```php
class ProcessContacts extends Command
{
    protected $signature = 'contacts:process
                            {--status=active : Filter by status}
                            {--limit=100 : Maximum to process}
                            {--dry-run : Simulate without changes}';

    protected $description = 'Process contacts based on criteria';

    public function handle(): int
    {
        $query = Contact::where('status', $this->option('status'))
            ->limit((int) $this->option('limit'));

        if (!$this->confirm("Process {$query->count()} contacts?")) {
            return Command::SUCCESS;
        }

        $this->withProgressBar($query->cursor(), fn($c) => $this->process($c));
        $this->newLine();
        $this->info('Done.');

        return Command::SUCCESS;
    }
}
```

### Common Artisan Commands

| Command | Description |
|---------|-------------|
| `php artisan make:model -mfc` | Model + migration + factory + controller |
| `php artisan make:controller --api` | API resource controller |
| `php artisan make:request` | Form request validation |
| `php artisan make:job` | Queueable job |
| `php artisan queue:work` | Process queue jobs |
| `php artisan schedule:run` | Run scheduled tasks |

> **Advanced**: For long-running consumers and graceful shutdown, see [REFERENCE.md](./REFERENCE.md#6-artisan-cli-advanced)

---

## Queues & Jobs

### Job Definition

```php
class SendWelcomeEmail implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $timeout = 60;
    public array $backoff = [30, 60, 120];

    public function __construct(public User $user) {}

    public function handle(Mailer $mailer): void
    {
        $mailer->to($this->user->email)->send(new WelcomeMail($this->user));
    }

    public function failed(\Throwable $e): void
    {
        Log::error('Welcome email failed', ['user' => $this->user->id, 'error' => $e->getMessage()]);
    }
}
```

### Dispatching Jobs

```php
// Basic dispatch
SendWelcomeEmail::dispatch($user);

// With options
SendWelcomeEmail::dispatch($user)
    ->onQueue('emails')
    ->delay(now()->addMinutes(10));

// Conditional
SendWelcomeEmail::dispatchIf($user->wantsEmails(), $user);
```

> **Advanced**: For job batching, chaining, and rate limiting, see [REFERENCE.md](./REFERENCE.md#4-queue-system-advanced)

---

## Events & Listeners

```php
class PostPublished implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(public Post $post) {}

    public function broadcastOn(): array
    {
        return [new PrivateChannel("user.{$this->post->author_id}")];
    }
}

// Dispatch: event(new PostPublished($post));
```

---

## Testing

### Feature Test

```php
class PostControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_post(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->postJson('/api/posts', [
            'title' => 'Test Post',
            'content' => 'Test content for the post.',
        ]);

        $response->assertStatus(201)
            ->assertJson(['data' => ['title' => 'Test Post']]);

        $this->assertDatabaseHas('posts', [
            'title' => 'Test Post',
            'author_id' => $user->id,
        ]);
    }
}
```

### Mocking

```php
public function test_order_processing(): void
{
    Queue::fake();
    $gateway = $this->mock(PaymentGateway::class);
    $gateway->shouldReceive('charge')->once()->andReturn(['id' => 'ch_123']);

    $this->postJson('/api/orders', [...]);

    Queue::assertPushed(ProcessOrder::class);
}
```

> **Advanced**: For testing commands, complex mocking, see [REFERENCE.md](./REFERENCE.md#11-testing-advanced)

---

## Service Providers

```php
class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // Bind interfaces to implementations
        $this->app->bind(UserRepositoryInterface::class, UserRepository::class);

        // Singleton binding
        $this->app->singleton(PaymentGateway::class, fn($app) =>
            new StripeGateway(config('services.stripe.key'))
        );
    }

    public function boot(): void
    {
        Model::preventLazyLoading(!app()->isProduction());
    }
}
```

> **Advanced**: For contextual binding and deferred providers, see [REFERENCE.md](./REFERENCE.md#1-service-container--dependency-injection)

---

## Task Scheduling

```php
// app/Console/Kernel.php
protected function schedule(Schedule $schedule): void
{
    $schedule->command('queue:work --stop-when-empty')
        ->everyMinute()
        ->withoutOverlapping();

    $schedule->command('reports:generate')
        ->dailyAt('00:00')
        ->onOneServer()
        ->emailOutputOnFailure('admin@example.com');

    $schedule->job(new ProcessPendingOrders)
        ->hourly()
        ->between('08:00', '22:00');
}
```

---

**For advanced patterns including multi-tenancy, repository pattern, performance optimization, and debugging, see [REFERENCE.md](./REFERENCE.md)**
