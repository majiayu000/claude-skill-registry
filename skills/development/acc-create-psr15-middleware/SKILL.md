---
name: acc-create-psr15-middleware
description: Generates PSR-15 HTTP Middleware implementation for PHP 8.5. Creates MiddlewareInterface and RequestHandlerInterface with pipeline composition. Includes unit tests.
---

# PSR-15 HTTP Middleware Generator

## Overview

Generates PSR-15 compliant HTTP middleware and request handlers for building middleware pipelines.

## When to Use

- Building HTTP middleware pipeline
- Authentication/authorization middleware
- CORS, logging, error handling middleware
- Request/response transformation

## Generated Components

| Component | Description | Location |
|-----------|-------------|----------|
| Middleware | MiddlewareInterface impl | `src/Infrastructure/Http/Middleware/` |
| RequestHandler | Pipeline dispatcher | `src/Infrastructure/Http/` |
| Unit Tests | PHPUnit tests | `tests/Unit/Infrastructure/Http/` |

## Template: Middleware

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http\Middleware;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\MiddlewareInterface;
use Psr\Http\Server\RequestHandlerInterface;

final readonly class AuthenticationMiddleware implements MiddlewareInterface
{
    public function __construct(
        private TokenValidatorInterface $tokenValidator,
    ) {
    }

    public function process(
        ServerRequestInterface $request,
        RequestHandlerInterface $handler,
    ): ResponseInterface {
        $token = $this->extractToken($request);

        if ($token === null) {
            return $this->unauthorizedResponse();
        }

        $user = $this->tokenValidator->validate($token);

        if ($user === null) {
            return $this->unauthorizedResponse();
        }

        $request = $request->withAttribute('user', $user);

        return $handler->handle($request);
    }

    private function extractToken(ServerRequestInterface $request): ?string
    {
        $header = $request->getHeaderLine('Authorization');

        if (!str_starts_with($header, 'Bearer ')) {
            return null;
        }

        return substr($header, 7);
    }

    private function unauthorizedResponse(): ResponseInterface
    {
        return (new Response(401))
            ->withHeader('Content-Type', 'application/json')
            ->withBody(new Stream(json_encode(['error' => 'Unauthorized'])));
    }
}
```

## Template: Middleware Pipeline

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\MiddlewareInterface;
use Psr\Http\Server\RequestHandlerInterface;

final class MiddlewarePipeline implements RequestHandlerInterface
{
    /** @var MiddlewareInterface[] */
    private array $middleware = [];
    private int $index = 0;

    public function __construct(
        private readonly RequestHandlerInterface $fallbackHandler,
    ) {
    }

    public function pipe(MiddlewareInterface $middleware): self
    {
        $clone = clone $this;
        $clone->middleware[] = $middleware;

        return $clone;
    }

    public function handle(ServerRequestInterface $request): ResponseInterface
    {
        if (!isset($this->middleware[$this->index])) {
            return $this->fallbackHandler->handle($request);
        }

        $middleware = $this->middleware[$this->index];

        $next = clone $this;
        $next->index++;

        return $middleware->process($request, $next);
    }
}
```

## Template: Request Handler

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\RequestHandlerInterface;

final readonly class ControllerHandler implements RequestHandlerInterface
{
    public function __construct(
        private object $controller,
        private string $method,
    ) {
    }

    public function handle(ServerRequestInterface $request): ResponseInterface
    {
        return $this->controller->{$this->method}($request);
    }
}
```

## Template: Common Middleware

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http\Middleware;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\MiddlewareInterface;
use Psr\Http\Server\RequestHandlerInterface;
use Psr\Log\LoggerInterface;

final readonly class LoggingMiddleware implements MiddlewareInterface
{
    public function __construct(
        private LoggerInterface $logger,
    ) {
    }

    public function process(
        ServerRequestInterface $request,
        RequestHandlerInterface $handler,
    ): ResponseInterface {
        $startTime = microtime(true);

        $this->logger->info('Request started', [
            'method' => $request->getMethod(),
            'uri' => (string) $request->getUri(),
        ]);

        $response = $handler->handle($request);

        $duration = microtime(true) - $startTime;

        $this->logger->info('Request completed', [
            'method' => $request->getMethod(),
            'uri' => (string) $request->getUri(),
            'status' => $response->getStatusCode(),
            'duration_ms' => round($duration * 1000, 2),
        ]);

        return $response;
    }
}

final readonly class CorsMiddleware implements MiddlewareInterface
{
    public function __construct(
        private array $allowedOrigins = ['*'],
        private array $allowedMethods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        private array $allowedHeaders = ['Content-Type', 'Authorization'],
    ) {
    }

    public function process(
        ServerRequestInterface $request,
        RequestHandlerInterface $handler,
    ): ResponseInterface {
        if ($request->getMethod() === 'OPTIONS') {
            return $this->handlePreflight($request);
        }

        $response = $handler->handle($request);

        return $this->addCorsHeaders($response, $request);
    }

    private function handlePreflight(ServerRequestInterface $request): ResponseInterface
    {
        $response = new Response(204);

        return $this->addCorsHeaders($response, $request);
    }

    private function addCorsHeaders(
        ResponseInterface $response,
        ServerRequestInterface $request,
    ): ResponseInterface {
        $origin = $request->getHeaderLine('Origin');

        if ($this->isOriginAllowed($origin)) {
            $response = $response
                ->withHeader('Access-Control-Allow-Origin', $origin)
                ->withHeader('Access-Control-Allow-Methods', implode(', ', $this->allowedMethods))
                ->withHeader('Access-Control-Allow-Headers', implode(', ', $this->allowedHeaders));
        }

        return $response;
    }

    private function isOriginAllowed(string $origin): bool
    {
        return in_array('*', $this->allowedOrigins, true)
            || in_array($origin, $this->allowedOrigins, true);
    }
}

final readonly class ErrorHandlingMiddleware implements MiddlewareInterface
{
    public function __construct(
        private LoggerInterface $logger,
        private bool $debug = false,
    ) {
    }

    public function process(
        ServerRequestInterface $request,
        RequestHandlerInterface $handler,
    ): ResponseInterface {
        try {
            return $handler->handle($request);
        } catch (\Throwable $e) {
            $this->logger->error('Unhandled exception', [
                'exception' => $e::class,
                'message' => $e->getMessage(),
                'trace' => $e->getTraceAsString(),
            ]);

            $body = ['error' => 'Internal Server Error'];

            if ($this->debug) {
                $body['message'] = $e->getMessage();
                $body['trace'] = $e->getTrace();
            }

            return (new Response(500))
                ->withHeader('Content-Type', 'application/json')
                ->withBody(new Stream(json_encode($body)));
        }
    }
}
```

## Template: Unit Test

```php
<?php

declare(strict_types=1);

namespace App\Tests\Unit\Infrastructure\Http\Middleware;

use App\Infrastructure\Http\Middleware\AuthenticationMiddleware;
use App\Infrastructure\Http\Message\Response;
use App\Infrastructure\Http\Message\ServerRequest;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;
use Psr\Http\Server\RequestHandlerInterface;

#[Group('unit')]
#[CoversClass(AuthenticationMiddleware::class)]
final class AuthenticationMiddlewareTest extends TestCase
{
    #[Test]
    public function it_returns_401_without_token(): void
    {
        $middleware = new AuthenticationMiddleware(
            $this->createMock(TokenValidatorInterface::class),
        );

        $request = new ServerRequest('GET', '/api/users');
        $handler = $this->createMock(RequestHandlerInterface::class);
        $handler->expects($this->never())->method('handle');

        $response = $middleware->process($request, $handler);

        self::assertSame(401, $response->getStatusCode());
    }

    #[Test]
    public function it_passes_request_with_valid_token(): void
    {
        $validator = $this->createMock(TokenValidatorInterface::class);
        $validator->method('validate')->willReturn(new User('123'));

        $middleware = new AuthenticationMiddleware($validator);

        $request = (new ServerRequest('GET', '/api/users'))
            ->withHeader('Authorization', 'Bearer valid-token');

        $expectedResponse = new Response(200);
        $handler = $this->createMock(RequestHandlerInterface::class);
        $handler->expects($this->once())
            ->method('handle')
            ->willReturn($expectedResponse);

        $response = $middleware->process($request, $handler);

        self::assertSame(200, $response->getStatusCode());
    }
}
```

## Usage Example

```php
<?php

use App\Infrastructure\Http\MiddlewarePipeline;
use App\Infrastructure\Http\ControllerHandler;

// Build pipeline
$pipeline = (new MiddlewarePipeline(new NotFoundHandler()))
    ->pipe(new ErrorHandlingMiddleware($logger))
    ->pipe(new CorsMiddleware())
    ->pipe(new LoggingMiddleware($logger))
    ->pipe(new AuthenticationMiddleware($tokenValidator));

// Handle request
$response = $pipeline->handle($request);
```

## Requirements

```json
{
    "require": {
        "psr/http-server-handler": "^1.0",
        "psr/http-server-middleware": "^1.0"
    }
}
```
