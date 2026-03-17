---
name: php-expert
version: 1.0.0
description: Expert-level PHP development with PHP 8+, Laravel, Composer, and modern best practices
category: languages
tags: [php, laravel, composer, symfony, phpunit, psr]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(php:*, composer:*, artisan:*)
---

# PHP Expert

Expert guidance for modern PHP development including PHP 8+ features, Laravel framework, Composer dependency management, and PHP best practices.

## Core Concepts

### PHP 8+ Features
- Union types and mixed type
- Named arguments
- Attributes (annotations)
- Constructor property promotion
- Match expressions
- Nullsafe operator
- JIT compiler
- Fibers (PHP 8.1+)
- Readonly properties and classes

### Object-Oriented PHP
- Classes and objects
- Interfaces and abstract classes
- Traits
- Namespaces
- Autoloading (PSR-4)
- Type declarations
- Visibility modifiers

### Modern PHP
- Strict types
- Return type declarations
- Property type declarations
- Enums (PHP 8.1+)
- First-class callable syntax

## Modern PHP 8+ Syntax

### Constructor Property Promotion
```php
<?php

// Before PHP 8
class User {
    private string $name;
    private string $email;
    private int $age;

    public function __construct(string $name, string $email, int $age) {
        $this->name = $name;
        $this->email = $email;
        $this->age = $age;
    }
}

// PHP 8+ (constructor property promotion)
class User {
    public function __construct(
        private string $name,
        private string $email,
        private int $age,
    ) {}

    public function getName(): string {
        return $this->name;
    }
}

$user = new User('Alice', 'alice@example.com', 30);
```

### Named Arguments
```php
<?php

function createUser(
    string $name,
    string $email,
    int $age = 18,
    bool $admin = false,
): User {
    return new User($name, $email, $age, $admin);
}

// Named arguments (PHP 8+)
$user = createUser(
    name: 'Alice',
    email: 'alice@example.com',
    age: 30,
    admin: true,
);

// Skip optional parameters
$user = createUser(
    name: 'Bob',
    email: 'bob@example.com',
);
```

### Union Types and Mixed
```php
<?php

// Union types (PHP 8+)
function processValue(int|float $number): int|float {
    return $number * 2;
}

function findUser(int|string $identifier): ?User {
    if (is_int($identifier)) {
        return User::find($identifier);
    }
    return User::where('email', $identifier)->first();
}

// Mixed type (accepts any type)
function debugValue(mixed $value): void {
    var_dump($value);
}
```

### Match Expression
```php
<?php

// Old switch
switch ($status) {
    case 'pending':
        $message = 'Order is pending';
        break;
    case 'processing':
        $message = 'Order is being processed';
        break;
    case 'completed':
        $message = 'Order completed';
        break;
    default:
        $message = 'Unknown status';
}

// Match expression (PHP 8+)
$message = match ($status) {
    'pending' => 'Order is pending',
    'processing' => 'Order is being processed',
    'completed' => 'Order completed',
    default => 'Unknown status',
};

// Multiple conditions
$result = match ($value) {
    0, 1, 2 => 'Small',
    3, 4, 5 => 'Medium',
    default => 'Large',
};

// With expressions
$discount = match (true) {
    $customer->isPremium() && $order->total() > 1000 => 0.20,
    $customer->isPremium() => 0.15,
    $order->total() > 500 => 0.10,
    default => 0,
};
```

### Nullsafe Operator
```php
<?php

// Before PHP 8
$country = null;
if ($user !== null) {
    $address = $user->getAddress();
    if ($address !== null) {
        $country = $address->getCountry();
    }
}

// PHP 8+ nullsafe operator
$country = $user?->getAddress()?->getCountry();

// With default
$country = $user?->getAddress()?->getCountry() ?? 'Unknown';
```

### Attributes (Annotations)
```php
<?php

// Define attribute
#[Attribute]
class Route {
    public function __construct(
        public string $path,
        public string $method = 'GET',
    ) {}
}

// Use attribute
class UserController {
    #[Route('/users', method: 'GET')]
    public function index(): array {
        return User::all();
    }

    #[Route('/users/{id}', method: 'GET')]
    public function show(int $id): User {
        return User::findOrFail($id);
    }

    #[Route('/users', method: 'POST')]
    public function store(Request $request): User {
        return User::create($request->all());
    }
}

// Read attributes
$reflection = new ReflectionClass(UserController::class);
foreach ($reflection->getMethods() as $method) {
    $attributes = $method->getAttributes(Route::class);
    foreach ($attributes as $attribute) {
        $route = $attribute->newInstance();
        echo "{$route->method} {$route->path}\n";
    }
}
```

### Enums (PHP 8.1+)
```php
<?php

// Basic enum
enum Status {
    case Pending;
    case Processing;
    case Completed;
    case Cancelled;
}

// Usage
$status = Status::Pending;

function updateOrder(Order $order, Status $status): void {
    $order->status = $status;
    $order->save();
}

// Backed enums
enum OrderStatus: string {
    case Pending = 'pending';
    case Processing = 'processing';
    case Completed = 'completed';
    case Cancelled = 'cancelled';

    public function label(): string {
        return match($this) {
            self::Pending => 'Pending',
            self::Processing => 'Being Processed',
            self::Completed => 'Completed',
            self::Cancelled => 'Cancelled',
        };
    }

    public function color(): string {
        return match($this) {
            self::Pending => 'yellow',
            self::Processing => 'blue',
            self::Completed => 'green',
            self::Cancelled => 'red',
        };
    }
}

$status = OrderStatus::from('pending');
echo $status->label(); // 'Pending'
echo $status->value;   // 'pending'
```

### Readonly Properties and Classes
```php
<?php

// Readonly property (PHP 8.1+)
class User {
    public function __construct(
        public readonly string $id,
        public readonly string $email,
        public string $name,
    ) {}
}

$user = new User('123', 'user@example.com', 'Alice');
$user->name = 'Bob'; // OK
// $user->email = 'new@example.com'; // Error: readonly property

// Readonly class (PHP 8.2+)
readonly class Point {
    public function __construct(
        public int $x,
        public int $y,
    ) {}
}
```

## Laravel Framework

### Models
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\SoftDeletes;

class User extends Model
{
    use SoftDeletes;

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'is_admin' => 'boolean',
        'settings' => 'array',
    ];

    // Relationships
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }

    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }

    // Accessors (Laravel 9+)
    protected function name(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
            set: fn (string $value) => strtolower($value),
        );
    }

    // Scopes
    public function scopeActive($query)
    {
        return $query->where('active', true);
    }

    public function scopeAdmins($query)
    {
        return $query->where('is_admin', true);
    }

    // Methods
    public function isAdmin(): bool
    {
        return $this->is_admin;
    }
}

// Usage
$users = User::active()->get();
$admins = User::admins()->get();
$user = User::with('posts', 'roles')->find(1);
```

### Controllers
```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StorePostRequest;
use App\Http\Requests\UpdatePostRequest;
use App\Http\Resources\PostResource;
use App\Models\Post;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class PostController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth:api')->except(['index', 'show']);
    }

    public function index(): AnonymousResourceCollection
    {
        $posts = Post::with('user')
            ->published()
            ->latest()
            ->paginate(20);

        return PostResource::collection($posts);
    }

    public function show(Post $post): PostResource
    {
        $post->load(['user', 'comments.user']);
        return new PostResource($post);
    }

    public function store(StorePostRequest $request): JsonResponse
    {
        $post = $request->user()->posts()->create(
            $request->validated()
        );

        return response()->json(
            new PostResource($post),
            201
        );
    }

    public function update(UpdatePostRequest $request, Post $post): PostResource
    {
        $this->authorize('update', $post);

        $post->update($request->validated());

        return new PostResource($post);
    }

    public function destroy(Post $post): JsonResponse
    {
        $this->authorize('delete', $post);

        $post->delete();

        return response()->json(null, 204);
    }
}
```

### Form Requests
```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user() !== null;
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:200'],
            'content' => ['required', 'string', 'min:100'],
            'published' => ['sometimes', 'boolean'],
            'tags' => ['sometimes', 'array'],
            'tags.*' => ['string', 'max:50'],
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'Please provide a title for your post',
            'content.min' => 'Post content must be at least 100 characters',
        ];
    }
}
```

### API Resources
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
            'slug' => $this->slug,
            'content' => $this->when(
                $request->routeIs('posts.show'),
                $this->content
            ),
            'excerpt' => $this->excerpt,
            'published' => $this->published,
            'published_at' => $this->published_at?->toIso8601String(),
            'author' => new UserResource($this->whenLoaded('user')),
            'comments' => CommentResource::collection(
                $this->whenLoaded('comments')
            ),
            'tags' => $this->tags,
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),
        ];
    }
}
```

### Eloquent Queries
```php
<?php

// Basic queries
$users = User::all();
$user = User::find(1);
$user = User::where('email', 'user@example.com')->first();

// Complex queries
$posts = Post::where('published', true)
    ->where('created_at', '>', now()->subWeek())
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();

// Eager loading (avoid N+1)
$posts = Post::with(['user', 'comments.user'])->get();

// Lazy eager loading
$posts = Post::all();
$posts->load('user');

// Conditional loading
$posts = Post::with([
    'user' => function ($query) {
        $query->select('id', 'name', 'email');
    },
    'comments' => function ($query) {
        $query->latest()->limit(5);
    },
])->get();

// Aggregates
$count = Post::where('published', true)->count();
$sum = Order::where('status', 'completed')->sum('total');
$avg = Product::avg('price');

// Chunk processing
Post::chunk(100, function ($posts) {
    foreach ($posts as $post) {
        // Process post
    }
});

// Transactions
DB::transaction(function () use ($data) {
    $user = User::create($data['user']);
    $profile = $user->profile()->create($data['profile']);
    $user->roles()->attach($data['roles']);
});
```

### Migrations
```php
<?php

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
            $table->text('excerpt')->nullable();
            $table->boolean('published')->default(false);
            $table->timestamp('published_at')->nullable();
            $table->json('tags')->nullable();
            $table->timestamps();
            $table->softDeletes();

            $table->index('published');
            $table->index('published_at');
            $table->index(['user_id', 'published']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

### Jobs (Queues)
```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class SendWelcomeEmail implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public User $user,
    ) {}

    public function handle(): void
    {
        Mail::to($this->user->email)
            ->send(new WelcomeEmail($this->user));
    }

    public function failed(\Throwable $exception): void
    {
        // Handle job failure
        Log::error('Failed to send welcome email', [
            'user_id' => $this->user->id,
            'error' => $exception->getMessage(),
        ]);
    }
}

// Dispatch job
SendWelcomeEmail::dispatch($user);
SendWelcomeEmail::dispatch($user)->delay(now()->addMinutes(10));
SendWelcomeEmail::dispatch($user)->onQueue('emails');
```

### Events and Listeners
```php
<?php

// Event
namespace App\Events;

use App\Models\Post;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class PostPublished
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public Post $post,
    ) {}
}

// Listener
namespace App\Listeners;

use App\Events\PostPublished;
use App\Notifications\NewPostNotification;

class NotifyFollowers
{
    public function handle(PostPublished $event): void
    {
        $followers = $event->post->user->followers;

        foreach ($followers as $follower) {
            $follower->notify(new NewPostNotification($event->post));
        }
    }
}

// Register in EventServiceProvider
protected $listen = [
    PostPublished::class => [
        NotifyFollowers::class,
    ],
];

// Dispatch event
PostPublished::dispatch($post);
```

## Testing with PHPUnit

### Feature Tests
```php
<?php

namespace Tests\Feature;

use App\Models\User;
use App\Models\Post;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_can_list_posts(): void
    {
        Post::factory()->count(3)->create(['published' => true]);
        Post::factory()->create(['published' => false]);

        $response = $this->getJson('/api/posts');

        $response->assertOk()
            ->assertJsonCount(3, 'data');
    }

    public function test_can_create_post_when_authenticated(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user, 'api')
            ->postJson('/api/posts', [
                'title' => 'Test Post',
                'content' => 'Test content with enough characters to pass validation.',
            ]);

        $response->assertCreated()
            ->assertJsonPath('data.title', 'Test Post');

        $this->assertDatabaseHas('posts', [
            'title' => 'Test Post',
            'user_id' => $user->id,
        ]);
    }

    public function test_cannot_create_post_when_not_authenticated(): void
    {
        $response = $this->postJson('/api/posts', [
            'title' => 'Test Post',
            'content' => 'Test content',
        ]);

        $response->assertUnauthorized();
    }

    public function test_validates_post_creation(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user, 'api')
            ->postJson('/api/posts', [
                'title' => '', // Invalid
                'content' => 'Short', // Too short
            ]);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['title', 'content']);
    }

    public function test_can_update_own_post(): void
    {
        $user = User::factory()->create();
        $post = Post::factory()->create(['user_id' => $user->id]);

        $response = $this->actingAs($user, 'api')
            ->putJson("/api/posts/{$post->id}", [
                'title' => 'Updated Title',
                'content' => 'Updated content with enough characters.',
            ]);

        $response->assertOk();
        $this->assertDatabaseHas('posts', [
            'id' => $post->id,
            'title' => 'Updated Title',
        ]);
    }

    public function test_cannot_update_other_user_post(): void
    {
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $post = Post::factory()->create(['user_id' => $otherUser->id]);

        $response = $this->actingAs($user, 'api')
            ->putJson("/api/posts/{$post->id}", [
                'title' => 'Updated Title',
            ]);

        $response->assertForbidden();
    }
}
```

### Unit Tests
```php
<?php

namespace Tests\Unit;

use App\Models\User;
use App\Models\Post;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_has_posts(): void
    {
        $user = User::factory()->create();
        $posts = Post::factory()->count(3)->create(['user_id' => $user->id]);

        $this->assertCount(3, $user->posts);
        $this->assertTrue($user->posts->contains($posts->first()));
    }

    public function test_is_admin_returns_true_for_admin_users(): void
    {
        $admin = User::factory()->create(['is_admin' => true]);
        $user = User::factory()->create(['is_admin' => false]);

        $this->assertTrue($admin->isAdmin());
        $this->assertFalse($user->isAdmin());
    }
}
```

### Factories
```php
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class PostFactory extends Factory
{
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'title' => fake()->sentence(),
            'slug' => fake()->slug(),
            'content' => fake()->paragraphs(5, true),
            'excerpt' => fake()->paragraph(),
            'published' => false,
            'published_at' => null,
            'tags' => fake()->words(3),
        ];
    }

    public function published(): static
    {
        return $this->state(fn (array $attributes) => [
            'published' => true,
            'published_at' => now(),
        ]);
    }

    public function withUser(User $user): static
    {
        return $this->state(fn (array $attributes) => [
            'user_id' => $user->id,
        ]);
    }
}
```

## Best Practices

### Type Safety
```php
<?php
declare(strict_types=1);

// Always use strict types
// Use type declarations for parameters and return types
// Use property types where possible
```

### Dependency Injection
```php
<?php

// Use constructor injection
class UserService
{
    public function __construct(
        private UserRepository $repository,
        private EventDispatcher $dispatcher,
    ) {}

    public function createUser(array $data): User
    {
        $user = $this->repository->create($data);
        $this->dispatcher->dispatch(new UserCreated($user));
        return $user;
    }
}
```

### PSR Standards
- PSR-1: Basic Coding Standard
- PSR-4: Autoloading Standard
- PSR-12: Extended Coding Style
- PSR-7: HTTP Message Interface

## Anti-Patterns to Avoid

❌ **Not using strict types**: Always declare(strict_types=1)
❌ **Fat controllers**: Extract logic to services
❌ **N+1 queries**: Use eager loading
❌ **No type declarations**: Use types everywhere
❌ **Ignoring PSR standards**: Follow PSR-4, PSR-12
❌ **Direct DB queries in controllers**: Use repositories
❌ **Missing validation**: Always validate input
❌ **No tests**: Write tests for critical code

## Resources

- PHP Documentation: https://www.php.net/docs.php
- Laravel Documentation: https://laravel.com/docs
- Composer: https://getcomposer.org/
- PSR Standards: https://www.php-fig.org/psr/
- PHPUnit: https://phpunit.de/
