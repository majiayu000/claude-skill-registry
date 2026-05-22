---
name: acc-create-responder
description: Generates ADR Responder classes for PHP 8.5. Creates HTTP response builders with PSR-7/PSR-17 support. Includes unit tests.
---

# Responder Generator

Generate ADR-compliant Responder classes for HTTP response building.

## Responder Characteristics

- **Response Building**: Creates complete HTTP Response (status, headers, body)
- **No Business Logic**: Only format and transform data
- **No Domain Access**: No repository or service calls
- **Error Mapping**: Maps domain errors to HTTP status codes
- **Content Type**: Sets appropriate Content-Type header
- **PSR Compliance**: Uses PSR-7 and PSR-17 interfaces

## Template

```php
<?php

declare(strict_types=1);

namespace Presentation\Api\{Context}\{Action};

use Application\{Context}\UseCase\{Action}\{Action}Result;
use Psr\Http\Message\ResponseFactoryInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\StreamFactoryInterface;

final readonly class {Action}Responder
{
    public function __construct(
        private ResponseFactoryInterface $responseFactory,
        private StreamFactoryInterface $streamFactory,
    ) {
    }

    public function respond({Action}Result $result): ResponseInterface
    {
        if ($result->isFailure()) {
            return $this->handleFailure($result);
        }

        return $this->success($result);
    }

    private function success({Action}Result $result): ResponseInterface
    {
        {successResponse}
    }

    private function handleFailure({Action}Result $result): ResponseInterface
    {
        return match ($result->failureReason()) {
            {errorMapping}
            default => $this->badRequest($result->errorMessage()),
        };
    }

    private function json(array $data, int $status = 200): ResponseInterface
    {
        $body = $this->streamFactory->createStream(
            json_encode($data, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE)
        );

        return $this->responseFactory->createResponse($status)
            ->withHeader('Content-Type', 'application/json; charset=utf-8')
            ->withBody($body);
    }

    {helperMethods}
}
```

## Test Template

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Presentation\Api\{Context}\{Action};

use Application\{Context}\UseCase\{Action}\{Action}Result;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\TestCase;
use Presentation\Api\{Context}\{Action}\{Action}Responder;
use Psr\Http\Message\ResponseFactoryInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\StreamFactoryInterface;
use Psr\Http\Message\StreamInterface;

#[Group('unit')]
#[CoversClass({Action}Responder::class)]
final class {Action}ResponderTest extends TestCase
{
    private ResponseFactoryInterface $responseFactory;
    private StreamFactoryInterface $streamFactory;
    private {Action}Responder $responder;

    protected function setUp(): void
    {
        $this->responseFactory = $this->createMock(ResponseFactoryInterface::class);
        $this->streamFactory = $this->createMock(StreamFactoryInterface::class);
        $this->responder = new {Action}Responder(
            $this->responseFactory,
            $this->streamFactory,
        );

        $this->setupMocks();
    }

    public function testSuccessReturns{ExpectedStatus}(): void
    {
        $result = {Action}Result::success({successData});

        $response = $this->responder->respond($result);

        self::assertSame({expectedStatusCode}, $response->getStatusCode());
    }

    {failureTests}

    private function setupMocks(): void
    {
        $stream = $this->createMock(StreamInterface::class);
        $this->streamFactory->method('createStream')->willReturn($stream);

        $response = $this->createMock(ResponseInterface::class);
        $response->method('withHeader')->willReturnSelf();
        $response->method('withBody')->willReturnSelf();
        $response->method('getStatusCode')->willReturnCallback(
            fn () => $this->responseFactory->lastStatus ?? 200
        );

        $this->responseFactory->method('createResponse')->willReturnCallback(
            function (int $status) use ($response) {
                $this->responseFactory->lastStatus = $status;
                $mock = clone $response;
                $mock->method('getStatusCode')->willReturn($status);
                return $mock;
            }
        );
    }
}
```

## Responder Patterns

### Create Responder (201)

```php
<?php

declare(strict_types=1);

namespace Presentation\Api\User\Create;

use Application\User\UseCase\CreateUser\CreateUserResult;
use Psr\Http\Message\ResponseFactoryInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\StreamFactoryInterface;

final readonly class CreateUserResponder
{
    public function __construct(
        private ResponseFactoryInterface $responseFactory,
        private StreamFactoryInterface $streamFactory,
    ) {
    }

    public function respond(CreateUserResult $result): ResponseInterface
    {
        if ($result->isFailure()) {
            return match ($result->failureReason()) {
                'email_exists' => $this->conflict('User with this email already exists'),
                'invalid_email' => $this->badRequest('Invalid email format'),
                default => $this->badRequest($result->errorMessage()),
            };
        }

        return $this->created([
            'id' => $result->userId(),
            'email' => $result->email(),
        ]);
    }

    private function created(array $data): ResponseInterface
    {
        return $this->json($data, 201);
    }

    private function conflict(string $message): ResponseInterface
    {
        return $this->json(['error' => $message], 409);
    }

    private function badRequest(string $message): ResponseInterface
    {
        return $this->json(['error' => $message], 400);
    }

    private function json(array $data, int $status): ResponseInterface
    {
        $body = $this->streamFactory->createStream(
            json_encode($data, JSON_THROW_ON_ERROR)
        );

        return $this->responseFactory->createResponse($status)
            ->withHeader('Content-Type', 'application/json')
            ->withBody($body);
    }
}
```

### Get Responder (200/404)

```php
<?php

declare(strict_types=1);

namespace Presentation\Api\User\GetById;

use Application\User\UseCase\GetUserById\GetUserByIdResult;
use Psr\Http\Message\ResponseFactoryInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\StreamFactoryInterface;

final readonly class GetUserByIdResponder
{
    public function __construct(
        private ResponseFactoryInterface $responseFactory,
        private StreamFactoryInterface $streamFactory,
    ) {
    }

    public function respond(GetUserByIdResult $result): ResponseInterface
    {
        if ($result->isNotFound()) {
            return $this->notFound('User not found');
        }

        $user = $result->user();

        return $this->json([
            'id' => $user->id()->toString(),
            'email' => $user->email()->value(),
            'name' => $user->name(),
            'created_at' => $user->createdAt()->format('c'),
        ]);
    }

    private function notFound(string $message): ResponseInterface
    {
        return $this->json(['error' => $message], 404);
    }

    private function json(array $data, int $status = 200): ResponseInterface
    {
        $body = $this->streamFactory->createStream(
            json_encode($data, JSON_THROW_ON_ERROR)
        );

        return $this->responseFactory->createResponse($status)
            ->withHeader('Content-Type', 'application/json')
            ->withBody($body);
    }
}
```

### List Responder with Pagination

```php
<?php

declare(strict_types=1);

namespace Presentation\Api\User\ListAll;

use Application\User\UseCase\ListUsers\ListUsersResult;
use Psr\Http\Message\ResponseFactoryInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\StreamFactoryInterface;

final readonly class ListUsersResponder
{
    public function __construct(
        private ResponseFactoryInterface $responseFactory,
        private StreamFactoryInterface $streamFactory,
    ) {
    }

    public function respond(ListUsersResult $result): ResponseInterface
    {
        $users = array_map(
            fn ($user) => [
                'id' => $user->id()->toString(),
                'email' => $user->email()->value(),
                'name' => $user->name(),
            ],
            $result->users()
        );

        return $this->json([
            'data' => $users,
            'meta' => [
                'total' => $result->total(),
                'page' => $result->page(),
                'per_page' => $result->perPage(),
                'total_pages' => $result->totalPages(),
            ],
        ]);
    }

    private function json(array $data, int $status = 200): ResponseInterface
    {
        $body = $this->streamFactory->createStream(
            json_encode($data, JSON_THROW_ON_ERROR)
        );

        return $this->responseFactory->createResponse($status)
            ->withHeader('Content-Type', 'application/json')
            ->withBody($body);
    }
}
```

### Delete Responder (204)

```php
<?php

declare(strict_types=1);

namespace Presentation\Api\User\Delete;

use Application\User\UseCase\DeleteUser\DeleteUserResult;
use Psr\Http\Message\ResponseFactoryInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\StreamFactoryInterface;

final readonly class DeleteUserResponder
{
    public function __construct(
        private ResponseFactoryInterface $responseFactory,
        private StreamFactoryInterface $streamFactory,
    ) {
    }

    public function respond(DeleteUserResult $result): ResponseInterface
    {
        if ($result->isNotFound()) {
            return $this->notFound('User not found');
        }

        if ($result->isFailure()) {
            return $this->badRequest($result->errorMessage());
        }

        return $this->noContent();
    }

    private function noContent(): ResponseInterface
    {
        return $this->responseFactory->createResponse(204);
    }

    private function notFound(string $message): ResponseInterface
    {
        return $this->json(['error' => $message], 404);
    }

    private function badRequest(string $message): ResponseInterface
    {
        return $this->json(['error' => $message], 400);
    }

    private function json(array $data, int $status): ResponseInterface
    {
        $body = $this->streamFactory->createStream(
            json_encode($data, JSON_THROW_ON_ERROR)
        );

        return $this->responseFactory->createResponse($status)
            ->withHeader('Content-Type', 'application/json')
            ->withBody($body);
    }
}
```

## HTTP Status Mapping

| Domain Condition | HTTP Status | Method |
|------------------|-------------|--------|
| Success (create) | 201 | `created()` |
| Success (read) | 200 | `json()` |
| Success (update) | 200 | `json()` |
| Success (delete) | 204 | `noContent()` |
| Not found | 404 | `notFound()` |
| Already exists | 409 | `conflict()` |
| Validation error | 422 | `unprocessableEntity()` |
| Invalid input | 400 | `badRequest()` |
| Unauthorized | 401 | `unauthorized()` |
| Forbidden | 403 | `forbidden()` |

## File Placement

| Component | Path |
|-----------|------|
| Responder | `src/Presentation/Api/{Context}/{Action}/{Action}Responder.php` |
| Interface | `src/Presentation/Shared/Responder/ResponderInterface.php` |
| Abstract | `src/Presentation/Shared/Responder/AbstractJsonResponder.php` |
| Test | `tests/Unit/Presentation/Api/{Context}/{Action}/{Action}ResponderTest.php` |

## Generation Instructions

When asked to create a Responder:

1. **Identify operation type** (create, read, update, delete)
2. **Determine success status** (201, 200, 204)
3. **List possible failures** and their HTTP codes
4. **Define response structure** (what data to return)
5. **Generate Responder class** with proper namespace
6. **Generate test** for each status code path

## Naming Conventions

| HTTP Method | Responder Name | Success Status |
|-------------|----------------|----------------|
| GET (single) | Get{Resource}ByIdResponder | 200 |
| GET (list) | List{Resource}sResponder | 200 |
| POST | Create{Resource}Responder | 201 |
| PUT | Update{Resource}Responder | 200 |
| PATCH | Patch{Resource}Responder | 200 |
| DELETE | Delete{Resource}Responder | 204 |

## References

For detailed patterns and examples:

- `references/templates.md` — Additional Responder templates
- `references/examples.md` — Real-world Responder examples
