---
name: laravel-api-resources
description: >-
  Develops API endpoints with Eloquent resources and versioning. Activates when creating API routes,
  Eloquent resources, resource collections, API controllers, or when user mentions API, resource,
  JSON response, REST, endpoint, or API versioning.
---

# Laravel API Resources Development

## When to Apply

Activate this skill when:

- Creating API endpoints and routes
- Building Eloquent API Resources
- Implementing resource collections
- Designing API response structures
- Working with API versioning

## Documentation

Use `search-docs` for detailed Laravel API Resource patterns and documentation.

## Basic Usage

### Creating Resources

```bash
php artisan make:resource UserResource
php artisan make:resource UserCollection
```

### Basic Resource

<code-snippet name="Basic Resource" lang="php">
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at->toISOString(),
        ];
    }
}
</code-snippet>

### Resource Collections

<code-snippet name="Resource Collection" lang="php">
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total' => $this->collection->count(),
            ],
        ];
    }
}
</code-snippet>

### Conditional Attributes

<code-snippet name="Conditional Attributes" lang="php">
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,

        // Include only when loaded
        'posts' => PostResource::collection($this->whenLoaded('posts')),

        // Include conditionally
        'secret' => $this->when($request->user()?->isAdmin(), $this->secret),

        // Include when not null
        'bio' => $this->whenNotNull($this->bio),
    ];
}
</code-snippet>

### Nested Resources

<code-snippet name="Nested Resources" lang="php">
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        'author' => new UserResource($this->whenLoaded('author')),
        'comments' => CommentResource::collection($this->whenLoaded('comments')),
    ];
}
</code-snippet>

### Using Resources in Controllers

<code-snippet name="API Controller" lang="php">
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\UserResource;
use App\Http\Resources\UserCollection;
use App\Models\User;

class UserController extends Controller
{
    public function index()
    {
        $users = User::with('posts')->paginate(15);

        return new UserCollection($users);
    }

    public function show(User $user)
    {
        $user->load('posts', 'profile');

        return new UserResource($user);
    }
}
</code-snippet>

### API Routes

<code-snippet name="API Routes" lang="php">
// routes/api.php
use App\Http\Controllers\Api\UserController;

Route::prefix('v1')->group(function () {
    Route::apiResource('users', UserController::class);
});
</code-snippet>

### API Versioning

<code-snippet name="API Versioning Structure" lang="text">
app/
├── Http/
│   ├── Controllers/
│   │   └── Api/
│   │       ├── V1/
│   │       │   └── UserController.php
│   │       └── V2/
│   │           └── UserController.php
│   └── Resources/
│       ├── V1/
│       │   └── UserResource.php
│       └── V2/
│           └── UserResource.php
</code-snippet>

### Response Wrapping

<code-snippet name="Custom Response Wrapper" lang="php">
// In AppServiceProvider boot()
JsonResource::withoutWrapping();

// Or customize the wrapper
public static $wrap = 'user';
</code-snippet>

### Pagination

<code-snippet name="Paginated Response" lang="php">
public function index()
{
    $users = User::paginate(15);

    // Automatically includes pagination meta
    return UserResource::collection($users);
}

// Response structure:
// {
//     "data": [...],
//     "links": { "first": "...", "last": "...", ... },
//     "meta": { "current_page": 1, "total": 100, ... }
// }
</code-snippet>

### Additional Meta Data

<code-snippet name="Additional Meta" lang="php">
return (new UserCollection($users))
    ->additional([
        'meta' => [
            'version' => 'v1',
            'generated_at' => now()->toISOString(),
        ],
    ]);
</code-snippet>

## Common Pitfalls

- Not using `whenLoaded()` for relationships (causes N+1 or null errors)
- Exposing sensitive data in resources (passwords, tokens)
- Not eager loading relationships before passing to resources
- Missing API versioning from the start
- Not using pagination for large collections
- Inconsistent response structures across endpoints
