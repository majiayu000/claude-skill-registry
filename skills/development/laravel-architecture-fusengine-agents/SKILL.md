---
name: laravel-architecture
description: Design Laravel app architecture with services, repositories, actions, and clean code patterns. Use when structuring projects, creating services, implementing DI, or organizing code layers.
user-invocable: false
---

# Laravel Architecture Patterns

## Documentation

### Core
- [installation.md](docs/installation.md) - Installation and setup
- [configuration.md](docs/configuration.md) - Configuration
- [structure.md](docs/structure.md) - Directory structure
- [lifecycle.md](docs/lifecycle.md) - Request lifecycle
- [upgrade.md](docs/upgrade.md) - Upgrade guide
- [releases.md](docs/releases.md) - Release notes

### Service Container & Providers
- [container.md](docs/container.md) - Service container
- [providers.md](docs/providers.md) - Service providers
- [facades.md](docs/facades.md) - Facades
- [contracts.md](docs/contracts.md) - Contracts
- [context.md](docs/context.md) - Context

### CLI & Tools
- [artisan.md](docs/artisan.md) - Artisan CLI
- [packages.md](docs/packages.md) - Package development
- [helpers.md](docs/helpers.md) - Helper functions

### Development Environment
- [sail.md](docs/sail.md) - Docker development
- [valet.md](docs/valet.md) - macOS development
- [homestead.md](docs/homestead.md) - Vagrant development

### Performance & Deployment
- [octane.md](docs/octane.md) - High performance server
- [envoy.md](docs/envoy.md) - Deployment tasks
- [deployment.md](docs/deployment.md) - Deployment guide

### Advanced
- [processes.md](docs/processes.md) - Process management
- [concurrency.md](docs/concurrency.md) - Concurrency
- [filesystem.md](docs/filesystem.md) - File storage
- [pennant.md](docs/pennant.md) - Feature flags
- [mcp.md](docs/mcp.md) - Model Context Protocol

### Error Handling
- [errors.md](docs/errors.md) - Error handling
- [logging.md](docs/logging.md) - Logging

## Recommended Structure

```text
app/
├── Actions/              # Single-purpose action classes
├── Services/             # Business logic
├── Repositories/         # Data access layer
│   └── Contracts/
├── Http/
│   ├── Controllers/      # Thin controllers
│   ├── Requests/         # Form validation
│   └── Resources/        # API transformations
├── Models/               # Eloquent models only
├── Enums/                # PHP 8.1+ enums
├── Events/               # Domain events
├── Listeners/            # Event handlers
└── Policies/             # Authorization
```

## Service Pattern

```php
<?php

declare(strict_types=1);

namespace App\Services;

final readonly class UserService
{
    public function __construct(
        private UserRepositoryInterface $repository,
    ) {}

    public function create(CreateUserDTO $dto): User
    {
        return $this->repository->create($dto->toArray());
    }
}
```

## Dependency Injection

```php
// AppServiceProvider.php
public function register(): void
{
    $this->app->bind(
        UserRepositoryInterface::class,
        UserRepository::class
    );
}
```
