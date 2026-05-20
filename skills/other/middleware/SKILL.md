---
name: middleware
description: HTTP request/response pipeline handlers that inspect, modify, or reject requests before or after they reach a controller. Used for authentication, throttling, header manipulation, and logging.
---

**Name:** Middleware
**Description:** HTTP request/response pipeline handlers that inspect, modify, or reject requests before or after they reach a controller. Used for authentication, throttling, header manipulation, and logging.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Http/Middleware/**/*.php, laravel, php, backend, middleware, http, pipeline

## Rules

- Middleware classes live in `app/Http/Middleware/`
- Use a clear descriptive name that states what it does: `EnsureUserIsSubscribed`, `ForceJsonResponse`, `CheckMaintenanceWindow`
- Avoid vague names like `ApiMiddleware` or `CheckMiddleware`
- Middleware must call `$next($request)` to pass the request down the pipeline, or return early to reject it
- Register middleware in `bootstrap/app.php` using `->withMiddleware()`
- Apply middleware at the group level, not on individual routes, when possible
- Code before `$next($request)` runs before the controller; code after runs on the response
- Never put business logic in middleware — use Actions or Services
- Never put model-level authorization in middleware — use Policies
- Never put request body validation in middleware — use Form Requests

## Examples

```php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    public function handle(Request $request, Closure $next): Response
    {
        if (!$request->user()?->isSubscribed()) {
            return response()->json(['message' => 'Subscription required.'], 403);
        }

        return $next($request);
    }
}
```

```php
// Before and After middleware
public function handle(Request $request, Closure $next): Response
{
    // Runs BEFORE the controller
    $request->headers->set('X-Request-Id', Str::uuid());

    $response = $next($request);

    // Runs AFTER the controller
    $response->headers->set('X-Powered-By', 'MyApp');

    return $response;
}
```

```php
// Registration in bootstrap/app.php
->withMiddleware(function (Middleware $middleware) {
    $middleware->append(ForceJsonResponse::class);

    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class,
    ]);
})

// Applied to route group
Route::middleware('subscribed')->group(function () {
    Route::get('/dashboard', DashboardController::class);
});
```

## Anti-Patterns

- Putting business logic inside middleware (belongs in Actions or Services)
- Putting model-level authorization in middleware (belongs in Policies)
- Validating the request body in middleware (belongs in Form Requests)
- Accessing validated input inside middleware — middleware runs before validation
- Using middleware for things that only apply to a single route

## References

- [Laravel Middleware](https://laravel.com/docs/middleware)
- Related: `Policies/SKILL.md` — for model-level authorization
- Related: `FormRequests/SKILL.md` — for request body validation
