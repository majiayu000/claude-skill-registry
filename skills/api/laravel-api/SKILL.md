---
name: laravel-api
description: Build RESTful APIs with Laravel using API Resources, Sanctum authentication, rate limiting, and versioning. Use when creating API endpoints, transforming responses, or handling API authentication.
user-invocable: false
---

# Laravel API Development

## Documentation

### HTTP Layer
- [routing.md](docs/routing.md) - Routing
- [controllers.md](docs/controllers.md) - Controllers
- [middleware.md](docs/middleware.md) - Middleware
- [requests.md](docs/requests.md) - HTTP requests
- [responses.md](docs/responses.md) - HTTP responses
- [redirects.md](docs/redirects.md) - Redirects
- [urls.md](docs/urls.md) - URL generation

### API Features
- [rate-limiting.md](docs/rate-limiting.md) - Rate limiting
- [pagination.md](docs/pagination.md) - Pagination
- [http-client.md](docs/http-client.md) - HTTP client

### Validation & Helpers
- [validation.md](docs/validation.md) - Validation rules
- [strings.md](docs/strings.md) - String helpers

## API Controller

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Api\V1;

final class PostController extends Controller
{
    public function __construct(
        private readonly PostService $postService,
    ) {}

    public function index(): AnonymousResourceCollection
    {
        return PostResource::collection($this->postService->paginate(15));
    }

    public function store(StorePostRequest $request): JsonResponse
    {
        $post = $this->postService->create($request->validated());
        return PostResource::make($post)->response()->setStatusCode(201);
    }
}
```

## API Routes

```php
Route::prefix('v1')->group(function () {
    Route::get('posts', [PostController::class, 'index']);

    Route::middleware('auth:sanctum')->group(function () {
        Route::post('posts', [PostController::class, 'store']);
    });
});
```
