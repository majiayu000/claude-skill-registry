---
description: "Symfony API response standardization — JSON payload format, exception handling, controllers, REST endpoints, error responses, debug mode. Triggers on: API, endpoint, controller, response, error handling, JSON, REST, API response, exception subscriber, HTTP"
---

# Symfony API Response Standard

You are an expert in building standardized REST APIs within Symfony hexagonal architecture.

## When to Activate

- User creates API endpoints or controllers
- User asks about response format or error handling
- User needs exception handling for APIs
- User mentions REST, JSON, or API design

## Standard JSON Payload

ALL API responses use this format:

```json
{
    "result": null,
    "error": null,
    "extra": null,
    "status": 200
}
```

| Field | Type | Description |
|-------|------|-------------|
| `result` | `mixed` | Success data (null on error) |
| `error` | `?object` | Error details (null on success) |
| `extra` | `?object` | Metadata: pagination, debug info |
| `status` | `int` | HTTP status code |

### Success Response
```json
{
    "result": {"id": "uuid-123", "name": "John"},
    "error": null,
    "extra": null,
    "status": 200
}
```

### Error Response
```json
{
    "result": null,
    "error": {"code": "USER_NOT_FOUND", "message": "User not found"},
    "extra": null,
    "status": 404
}
```

### Debug Mode (APP_DEBUG=true)
```json
{
    "result": null,
    "error": {"code": "INTERNAL_ERROR", "message": "Something went wrong"},
    "extra": {"debug": {"exception": "...", "trace": "..."}},
    "status": 500
}
```

## Controller Pattern

Controllers are thin — dispatch to buses only:

```php
namespace App\Presentation\{Module}\API;

use App\Presentation\Shared\ApiResponseTrait;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route('/api/{module}')]
final class {Entity}Controller
{
    use ApiResponseTrait;

    public function __construct(
        private readonly MessageBusInterface $commandBus,
        private readonly MessageBusInterface $queryBus,
    ) {
    }

    #[Route('', methods: ['POST'])]
    #[IsGranted('ROLE_...')] // ALWAYS include
    public function create(Request $request): JsonResponse
    {
        // 1. Parse input
        // 2. Create command
        // 3. Dispatch to command bus
        // 4. Return success response
    }
}
```

## References

See `references/` for detailed guides:
- `payload-schema.md` — ApiResponseTrait, response helpers
- `exception-handling.md` — ExceptionSubscriber, error mapping
