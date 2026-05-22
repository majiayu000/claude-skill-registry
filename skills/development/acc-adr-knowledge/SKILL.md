---
name: acc-adr-knowledge
description: Action-Domain-Responder pattern knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for ADR (web-specific MVC alternative) audits.
---

# ADR Knowledge Base

Quick reference for Action-Domain-Responder pattern and PHP implementation guidelines.

## Core Principles

### ADR Components

```
HTTP Request → Action (collects input)
                 ↓
              Domain (executes business logic)
                 ↓
             Responder (builds HTTP Response)
                 ↓
           HTTP Response
```

**Rule:** One action = one HTTP endpoint. Responder builds the COMPLETE response.

### Component Responsibilities

| Component | Responsibility | Contains |
|-----------|----------------|----------|
| **Action** | Collects input, invokes Domain, passes to Responder | Request parsing, DTO creation, UseCase invocation |
| **Domain** | Business logic (same as DDD Domain/Application) | Entities, Value Objects, UseCases, Services |
| **Responder** | Builds HTTP Response (status, headers, body) | Response building, template rendering, content negotiation |

## ADR vs MVC Comparison

| Aspect | MVC Controller | ADR Action |
|--------|----------------|------------|
| Granularity | Multiple actions | Single action per class |
| Response building | Mixed in controller | Separate Responder class |
| HTTP concerns | Scattered | Isolated in Responder |
| Testability | Lower (many concerns) | Higher (single responsibility) |
| File structure | Few large files | Many focused files |

## Quick Checklists

### Action Checklist

- [ ] Single `__invoke()` method
- [ ] No `new Response()` or response building
- [ ] No business logic (if/switch on domain state)
- [ ] Only input parsing and domain invocation
- [ ] Returns Responder result

### Responder Checklist

- [ ] Receives domain result only
- [ ] Builds complete HTTP Response
- [ ] Handles content negotiation
- [ ] Sets status codes based on result
- [ ] No domain/business logic
- [ ] No database/repository access

### Domain Checklist

- [ ] Same as DDD Domain/Application layers
- [ ] No HTTP/Response concerns
- [ ] Returns domain objects (not HTTP responses)
- [ ] Pure business logic

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| `new Response()` in Action | *Action.php | Critical |
| `->withStatus()` in Action | *Action.php | Critical |
| `if ($result->isError())` in Action | *Action.php | Warning |
| `$repository->` in Responder | *Responder.php | Critical |
| `$service->` in Responder | *Responder.php | Critical |
| Multiple public methods in Action | *Action.php | Warning |
| Template logic in Action | *Action.php | Warning |

## PHP 8.5 ADR Patterns

### Action Pattern

```php
<?php

declare(strict_types=1);

namespace Presentation\Api\User\Create;

use Application\User\UseCase\CreateUser\CreateUserUseCase;
use Application\User\UseCase\CreateUser\CreateUserInput;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;

final readonly class CreateUserAction
{
    public function __construct(
        private CreateUserUseCase $useCase,
        private CreateUserResponder $responder,
    ) {
    }

    public function __invoke(ServerRequestInterface $request): ResponseInterface
    {
        $input = $this->parseInput($request);
        $result = $this->useCase->execute($input);

        return $this->responder->respond($result);
    }

    private function parseInput(ServerRequestInterface $request): CreateUserInput
    {
        $body = (array) $request->getParsedBody();

        return new CreateUserInput(
            email: $body['email'] ?? '',
            name: $body['name'] ?? '',
        );
    }
}
```

### Responder Pattern

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
            return $this->error($result->error());
        }

        return $this->success($result->userId());
    }

    private function success(string $userId): ResponseInterface
    {
        return $this->json(['id' => $userId], 201);
    }

    private function error(string $message): ResponseInterface
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

## Detection Patterns

### Action Detection

```bash
# Find Action classes
Glob: **/*Action.php
Glob: **/Action/**/*.php
Grep: "implements.*ActionInterface|extends.*Action" --glob "**/*.php"

# Detect Action pattern usage
Grep: "public function __invoke.*Request" --glob "**/*Action.php"
```

### Responder Detection

```bash
# Find Responder classes
Glob: **/*Responder.php
Glob: **/Responder/**/*.php
Grep: "implements.*ResponderInterface" --glob "**/*.php"

# Detect Responder pattern usage
Grep: "public function respond" --glob "**/*Responder.php"
```

### Violation Detection

```bash
# Response building in Action (Critical)
Grep: "new Response|->withStatus|->withHeader|->withBody" --glob "**/*Action.php"

# Business logic in Action (Warning)
Grep: "if \(.*->status|switch \(|->isValid\(\)" --glob "**/*Action.php"

# Domain calls in Responder (Critical)
Grep: "Repository|Service|UseCase" --glob "**/*Responder.php"

# Multiple public methods in Action (Warning)
Grep: "public function [^_]" --glob "**/*Action.php" | wc -l
```

## File Structure

### Recommended Structure

```
src/
├── Presentation/
│   ├── Api/
│   │   └── {Context}/
│   │       └── {Action}/
│   │           ├── {Action}Action.php
│   │           ├── {Action}Responder.php
│   │           └── {Action}Request.php (optional DTO)
│   ├── Web/
│   │   └── {Context}/
│   │       └── {Action}/
│   │           ├── {Action}Action.php
│   │           ├── {Action}Responder.php
│   │           └── templates/ (for HTML)
│   └── Shared/
│       ├── Action/
│       │   └── ActionInterface.php
│       └── Responder/
│           └── ResponderInterface.php
├── Application/
│   └── {Context}/
│       └── UseCase/
│           └── {Action}/
│               ├── {Action}UseCase.php
│               ├── {Action}Input.php
│               └── {Action}Result.php
└── Domain/
    └── ...
```

### Alternative Structure (Feature-Based)

```
src/
├── User/
│   ├── Presentation/
│   │   ├── CreateUser/
│   │   │   ├── CreateUserAction.php
│   │   │   └── CreateUserResponder.php
│   │   └── GetUser/
│   │       ├── GetUserAction.php
│   │       └── GetUserResponder.php
│   ├── Application/
│   │   └── ...
│   └── Domain/
│       └── ...
```

## Integration with DDD

ADR fits naturally with DDD layering:

| ADR | DDD Layer | Notes |
|-----|-----------|-------|
| Action | Presentation | Entry point for HTTP |
| Responder | Presentation | Exit point for HTTP |
| Domain | Domain + Application | Business logic via UseCases |

## PSR Integration

ADR works with PSR-7/PSR-15:

| PSR | Usage |
|-----|-------|
| PSR-7 | Request/Response interfaces |
| PSR-15 | Middleware for cross-cutting concerns |
| PSR-17 | Response/Stream factories in Responder |

## Antipatterns

### 1. Fat Action (Critical)

```php
// BAD: Action doing too much
class CreateUserAction
{
    public function __invoke(Request $request): Response
    {
        $data = $request->getParsedBody();

        // Validation in Action
        if (empty($data['email'])) {
            return new Response(400, [], 'Email required');
        }

        // Business logic in Action
        $user = new User($data['email']);
        $this->repository->save($user);

        // Response building in Action
        return new Response(201, [], json_encode(['id' => $user->id()]));
    }
}
```

### 2. Anemic Responder (Warning)

```php
// BAD: Responder not doing its job
class CreateUserResponder
{
    public function respond($data): Response
    {
        return new Response(200, [], json_encode($data));
    }
}
```

### 3. Smart Responder (Critical)

```php
// BAD: Responder with business logic
class CreateUserResponder
{
    public function respond(User $user): Response
    {
        // Domain logic in Responder!
        if ($user->isAdmin()) {
            $this->notificationService->notifyAdmins();
        }

        return $this->json(['id' => $user->id()], 201);
    }
}
```

## References

For detailed information, load these reference files:

- `references/action-patterns.md` — Action class patterns and best practices
- `references/responder-patterns.md` — Responder class patterns
- `references/domain-integration.md` — Integration with DDD Domain layer
- `references/mvc-comparison.md` — Detailed MVC vs ADR comparison
- `references/antipatterns.md` — Common ADR violations with examples

## Assets

- `assets/report-template.md` — ADR audit report template
