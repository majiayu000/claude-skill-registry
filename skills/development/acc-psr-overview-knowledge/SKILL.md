---
name: acc-psr-overview-knowledge
description: PHP Standards Recommendations (PSR) overview knowledge base. Provides comprehensive reference for all accepted PSRs including PSR-1,3,4,6,7,11,12,13,14,15,16,17,18,20. Use for PSR selection decisions and compliance audits.
---

# PSR Overview Knowledge

## What is PSR?

PSR (PHP Standards Recommendations) are specifications published by the PHP Framework Interoperability Group (PHP-FIG). They establish common standards for PHP code to ensure interoperability between frameworks and libraries.

## Accepted PSRs Summary

| PSR | Name | Category | Status |
|-----|------|----------|--------|
| PSR-1 | Basic Coding Standard | Coding Style | Accepted |
| PSR-3 | Logger Interface | Logging | Accepted |
| PSR-4 | Autoloader | Autoloading | Accepted |
| PSR-6 | Caching Interface | Caching | Accepted |
| PSR-7 | HTTP Message Interface | HTTP | Accepted |
| PSR-11 | Container Interface | DI Container | Accepted |
| PSR-12 | Extended Coding Style | Coding Style | Accepted |
| PSR-13 | Hypermedia Links | Hypermedia | Accepted |
| PSR-14 | Event Dispatcher | Events | Accepted |
| PSR-15 | HTTP Handlers | HTTP | Accepted |
| PSR-16 | Simple Cache | Caching | Accepted |
| PSR-17 | HTTP Factories | HTTP | Accepted |
| PSR-18 | HTTP Client | HTTP | Accepted |
| PSR-20 | Clock | Time | Accepted |

## PSR Categories

### Coding Style (PSR-1, PSR-12)

Standards for writing clean, consistent PHP code.

| Aspect | PSR-1 | PSR-12 |
|--------|-------|--------|
| Scope | Basic rules | Extended formatting |
| File encoding | UTF-8 without BOM | Inherits PSR-1 |
| Class names | StudlyCaps | Inherits PSR-1 |
| Method names | camelCase | Inherits PSR-1 |
| Indentation | - | 4 spaces |
| Line length | - | 120 chars soft limit |
| Keywords | - | Lowercase |

### Autoloading (PSR-4)

Standard for autoloading classes from file paths.

```
Namespace Prefix → Base Directory
App\             → src/

FQCN                          → File Path
App\Domain\User\Entity\User   → src/Domain/User/Entity/User.php
```

### HTTP (PSR-7, PSR-15, PSR-17, PSR-18)

Standards for HTTP messages, handlers, factories, and clients.

| PSR | Purpose | Key Interfaces |
|-----|---------|----------------|
| PSR-7 | HTTP Messages | `RequestInterface`, `ResponseInterface`, `StreamInterface` |
| PSR-15 | HTTP Handlers | `MiddlewareInterface`, `RequestHandlerInterface` |
| PSR-17 | HTTP Factories | `RequestFactoryInterface`, `ResponseFactoryInterface` |
| PSR-18 | HTTP Client | `ClientInterface` |

```
PSR-17 (Factory) → PSR-7 (Message) → PSR-15 (Handler) → PSR-7 (Response)
                                          ↓
                                   PSR-18 (Client)
```

### Caching (PSR-6, PSR-16)

Standards for caching implementations.

| Aspect | PSR-6 | PSR-16 |
|--------|-------|--------|
| Complexity | Full-featured | Simple |
| Key interfaces | `CacheItemPoolInterface`, `CacheItemInterface` | `CacheInterface` |
| Deferred saves | Yes | No |
| Use case | Complex caching needs | Simple get/set |

### Logging (PSR-3)

Standard for logging libraries.

```php
interface LoggerInterface {
    public function emergency(string|\Stringable $message, array $context = []): void;
    public function alert(string|\Stringable $message, array $context = []): void;
    public function critical(string|\Stringable $message, array $context = []): void;
    public function error(string|\Stringable $message, array $context = []): void;
    public function warning(string|\Stringable $message, array $context = []): void;
    public function notice(string|\Stringable $message, array $context = []): void;
    public function info(string|\Stringable $message, array $context = []): void;
    public function debug(string|\Stringable $message, array $context = []): void;
    public function log(mixed $level, string|\Stringable $message, array $context = []): void;
}
```

### DI Container (PSR-11)

Standard for dependency injection containers.

```php
interface ContainerInterface {
    public function get(string $id): mixed;
    public function has(string $id): bool;
}
```

### Events (PSR-14)

Standard for event dispatching.

```php
interface EventDispatcherInterface {
    public function dispatch(object $event): object;
}

interface ListenerProviderInterface {
    public function getListenersForEvent(object $event): iterable;
}

interface StoppableEventInterface {
    public function isPropagationStopped(): bool;
}
```

### Hypermedia (PSR-13)

Standard for hypermedia links (HATEOAS).

```php
interface LinkInterface {
    public function getHref(): string;
    public function isTemplated(): bool;
    public function getRels(): array;
    public function getAttributes(): array;
}
```

### Time (PSR-20)

Standard for clock abstraction.

```php
interface ClockInterface {
    public function now(): DateTimeImmutable;
}
```

## When to Use Each PSR

### Decision Matrix

| Need | PSR |
|------|-----|
| Code formatting | PSR-1, PSR-12 |
| Class autoloading | PSR-4 |
| Logging | PSR-3 |
| Simple caching (get/set) | PSR-16 |
| Complex caching (pools, tags) | PSR-6 |
| HTTP requests/responses | PSR-7 |
| HTTP middleware | PSR-15 |
| Creating HTTP objects | PSR-17 |
| HTTP client for external APIs | PSR-18 |
| Dependency injection | PSR-11 |
| Event system | PSR-14 |
| REST API with links | PSR-13 |
| Testing with time | PSR-20 |

### Common Combinations

| Use Case | PSRs |
|----------|------|
| HTTP API | PSR-7 + PSR-15 + PSR-17 |
| HTTP Client | PSR-7 + PSR-17 + PSR-18 |
| Web Application | PSR-1 + PSR-4 + PSR-12 + PSR-3 + PSR-11 |
| CQRS/Event-Driven | PSR-14 + PSR-3 + PSR-11 |
| Microservice | All of the above |

## PHP Package Implementations

### PSR-3: Logger

| Package | Description |
|---------|-------------|
| `monolog/monolog` | De facto standard logger |
| `psr/log` | Interface only |

### PSR-4: Autoloader

| Package | Description |
|---------|-------------|
| Composer | Built-in autoloader |

### PSR-6: Cache

| Package | Description |
|---------|-------------|
| `symfony/cache` | Full-featured cache |
| `cache/filesystem-adapter` | File-based cache |

### PSR-7/PSR-17: HTTP

| Package | Description |
|---------|-------------|
| `guzzlehttp/psr7` | Guzzle implementation |
| `nyholm/psr7` | Lightweight implementation |
| `laminas/laminas-diactoros` | Laminas implementation |

### PSR-11: Container

| Package | Description |
|---------|-------------|
| `php-di/php-di` | Autowiring DI container |
| `league/container` | Flexible container |
| `pimple/pimple` | Simple container |

### PSR-14: Event Dispatcher

| Package | Description |
|---------|-------------|
| `symfony/event-dispatcher` | Symfony implementation |
| `league/event` | League implementation |

### PSR-15: HTTP Handlers

| Package | Description |
|---------|-------------|
| `middlewares/utils` | Middleware utilities |
| `relay/relay` | Simple dispatcher |

### PSR-18: HTTP Client

| Package | Description |
|---------|-------------|
| `guzzlehttp/guzzle` | Full HTTP client |
| `symfony/http-client` | Symfony HTTP client |

### PSR-20: Clock

| Package | Description |
|---------|-------------|
| `psr/clock` | Interface only |
| `symfony/clock` | Symfony implementation |
| `lcobucci/clock` | Simple implementation |

## Composer Requirements

```json
{
    "require": {
        "psr/log": "^3.0",
        "psr/cache": "^3.0",
        "psr/http-message": "^2.0",
        "psr/http-factory": "^1.0",
        "psr/http-client": "^1.0",
        "psr/container": "^2.0",
        "psr/event-dispatcher": "^1.0",
        "psr/link": "^2.0",
        "psr/clock": "^1.0",
        "psr/simple-cache": "^3.0"
    }
}
```

## Integration with DDD

### Layer Mapping

| DDD Layer | Relevant PSRs |
|-----------|---------------|
| Domain | PSR-14 (Domain Events) |
| Application | PSR-3, PSR-11, PSR-14, PSR-20 |
| Infrastructure | PSR-6, PSR-16, PSR-18 |
| Presentation | PSR-7, PSR-15, PSR-17 |

### Example: CQRS Application

```php
<?php

declare(strict_types=1);

namespace App\Application\User\Handler;

use App\Application\User\Command\CreateUserCommand;
use App\Domain\User\Entity\User;
use App\Domain\User\Repository\UserRepositoryInterface;
use Psr\EventDispatcher\EventDispatcherInterface;  // PSR-14
use Psr\Log\LoggerInterface;                       // PSR-3
use Psr\Clock\ClockInterface;                      // PSR-20

final readonly class CreateUserHandler
{
    public function __construct(
        private UserRepositoryInterface $repository,
        private EventDispatcherInterface $eventDispatcher,
        private LoggerInterface $logger,
        private ClockInterface $clock,
    ) {
    }

    public function __invoke(CreateUserCommand $command): void
    {
        $this->logger->info('Creating user', ['email' => $command->email]);

        $user = User::create(
            $command->email,
            $command->name,
            $this->clock->now(),
        );

        $this->repository->save($user);

        foreach ($user->pullEvents() as $event) {
            $this->eventDispatcher->dispatch($event);
        }
    }
}
```

## Compliance Checklist

| PSR | Required For | Check |
|-----|--------------|-------|
| PSR-1 | All PHP projects | `phpcs --standard=PSR1` |
| PSR-12 | All PHP projects | `phpcs --standard=PSR12` |
| PSR-4 | All PHP projects | `composer dump-autoload --strict` |
| PSR-3 | Projects with logging | Implement `LoggerInterface` |
| PSR-6/16 | Projects with caching | Implement `CacheInterface` |
| PSR-7 | HTTP APIs | Use PSR-7 implementations |
| PSR-11 | Projects with DI | Implement `ContainerInterface` |
| PSR-14 | Event-driven projects | Implement `EventDispatcherInterface` |
| PSR-15 | HTTP middleware | Implement `MiddlewareInterface` |
| PSR-17 | HTTP object creation | Use factory interfaces |
| PSR-18 | External API calls | Implement `ClientInterface` |
| PSR-20 | Time-sensitive code | Implement `ClockInterface` |

## See Also

- `references/accepted-psrs.md` - Detailed PSR descriptions
- `references/when-to-use.md` - Decision matrix for PSR selection
- `references/compatibility.md` - Inter-PSR relationships
- `references/php-fig-process.md` - How PSRs are created
- `assets/psr-selection-guide.md` - Selection guide template
