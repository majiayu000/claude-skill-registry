---
name: laravel-api
description: Build RESTful APIs with Laravel using API Resources, Sanctum authentication, rate limiting, and versioning. Use when creating API endpoints, transforming responses, or handling API authentication.
versions:
  laravel: "12.46"
  php: "8.5"
user-invocable: true
references: references/routing.md, references/controllers.md, references/middleware.md, references/requests.md, references/responses.md, references/validation.md, references/pagination.md, references/http-client.md, references/rate-limiting.md, references/redirects.md, references/urls.md, references/strings.md
related-skills: laravel-auth, laravel-eloquent, laravel-testing
---

# Laravel API Development

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing API patterns
2. **fuse-ai-pilot:research-expert** - Verify Laravel API docs via Context7
3. **mcp__context7__query-docs** - Check API Resources and Sanctum patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

Build RESTful APIs with Laravel using API Resources for response transformation and Sanctum for authentication.

| Component | Purpose |
|-----------|---------|
| **Controllers** | Handle requests, delegate to services |
| **Form Requests** | Validate input, authorize actions |
| **API Resources** | Transform models to JSON |
| **Middleware** | Auth, rate limiting, CORS |
| **Routes** | Versioned endpoints with groups |
| **Pagination** | Offset/cursor pagination |
| **HTTP Client** | Consume external APIs |

---

## Critical Rules

1. **Always use API Resources** - Never return Eloquent models directly
2. **Versioned routes** - Prefix with `/v1/`, `/v2/`
3. **Validate all input** - Use Form Requests, not inline validation
4. **Rate limiting** - Configure per-route limits
5. **Consistent responses** - Same structure, proper status codes
6. **Use services** - Keep controllers thin
7. **Eager load** - Prevent N+1 with `with()` before pagination

---

## Reference Guide

### Core Concepts

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **Routing** | [routing.md](references/routing.md) | Defining versioned API routes |
| **Controllers** | [controllers.md](references/controllers.md) | Controller patterns, resource methods |
| **Middleware** | [middleware.md](references/middleware.md) | Route protection, request filtering |
| **Validation** | [validation.md](references/validation.md) | Form Requests, validation rules |

### Request/Response

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **Requests** | [requests.md](references/requests.md) | Accessing input, files, headers |
| **Responses** | [responses.md](references/responses.md) | API Resources, status codes |
| **Pagination** | [pagination.md](references/pagination.md) | Offset/cursor pagination |

### Advanced

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **Rate Limiting** | [rate-limiting.md](references/rate-limiting.md) | Throttle configuration |
| **HTTP Client** | [http-client.md](references/http-client.md) | Consuming external APIs |
| **URLs** | [urls.md](references/urls.md) | URL generation, signed URLs |
| **Strings** | [strings.md](references/strings.md) | String helpers, UUIDs, slugs |
| **Redirects** | [redirects.md](references/redirects.md) | Redirect responses |

---

### Templates (Code Examples)

#### Controllers & Routes

| Template | Purpose |
|----------|---------|
| [ApiController.php.md](references/templates/ApiController.php.md) | Complete CRUD controller with service |
| [api-routes.md](references/templates/api-routes.md) | Versioned routes with middleware |
| [routing-examples.md](references/templates/routing-examples.md) | Detailed routing patterns |

#### Validation & Resources

| Template | Purpose |
|----------|---------|
| [FormRequest.php.md](references/templates/FormRequest.php.md) | Store/Update Form Requests |
| [validation-rules.md](references/templates/validation-rules.md) | All validation rules reference |
| [ApiResource.php.md](references/templates/ApiResource.php.md) | Resource with relationships |

#### External APIs

| Template | Purpose |
|----------|---------|
| [HttpClientService.php.md](references/templates/HttpClientService.php.md) | Reusable HTTP client service |

---

## Quick Reference

### Resource Response

```php
return PostResource::collection($posts);
return PostResource::make($post);
```

### Status Codes

```php
return PostResource::make($post)->response()->setStatusCode(201);
return response()->json(null, 204);
```

### Form Request

```php
public function store(StorePostRequest $request): JsonResponse
{
    $post = $this->service->create($request->validated());
    return PostResource::make($post)->response()->setStatusCode(201);
}
```

### Rate Limiting

```php
Route::middleware('throttle:60,1')->group(fn () => ...);
```

### Versioned Routes

```php
Route::prefix('v1')->group(function () {
    Route::apiResource('posts', PostController::class);
});
```

### Pagination

```php
return PostResource::collection(Post::paginate(15));
```

---

## Feature Matrix

| Feature | Status | Reference |
|---------|--------|-----------|
| RESTful Controllers | ✅ | controllers.md |
| API Resources | ✅ | responses.md |
| Form Request Validation | ✅ | validation.md |
| Route Versioning | ✅ | routing.md |
| Route Model Binding | ✅ | routing.md |
| Middleware | ✅ | middleware.md |
| Rate Limiting | ✅ | rate-limiting.md |
| Pagination | ✅ | pagination.md |
| Cursor Pagination | ✅ | pagination.md |
| HTTP Client | ✅ | http-client.md |
| Signed URLs | ✅ | urls.md |
| JSON Responses | ✅ | responses.md |
