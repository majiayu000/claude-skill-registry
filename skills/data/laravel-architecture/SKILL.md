---
name: laravel-architecture
description: Design Laravel app architecture with services, repositories, actions, and clean code patterns. Use when structuring projects, creating services, implementing DI, or organizing code layers.
versions:
  laravel: "12.46"
  php: "8.5"
user-invocable: true
references: references/container.md, references/providers.md, references/facades.md, references/contracts.md, references/structure.md, references/lifecycle.md, references/configuration.md, references/installation.md, references/upgrade.md, references/releases.md, references/sail.md, references/valet.md, references/homestead.md, references/octane.md, references/artisan.md, references/helpers.md, references/filesystem.md, references/processes.md, references/context.md, references/pennant.md, references/mcp.md, references/concurrency.md, references/deployment.md, references/envoy.md, references/logging.md, references/errors.md, references/packages.md
related-skills: solid-php, laravel-api, laravel-eloquent
---

# Laravel Architecture Patterns

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing architecture
2. **fuse-ai-pilot:research-expert** - Verify Laravel patterns via Context7
3. **mcp__context7__query-docs** - Check service container and DI patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

Laravel architecture focuses on clean separation of concerns, dependency injection, and maintainable code organization. This skill covers everything from project structure to production deployment.

### When to Use

- Structuring new Laravel projects
- Implementing services, repositories, actions
- Setting up dependency injection
- Configuring development environments
- Deploying to production

---

## Critical Rules

1. **Thin controllers** - Delegate business logic to services
2. **Interfaces in app/Contracts/** - Never alongside implementations
3. **DI over facades** - Constructor injection for testability
4. **Files < 100 lines** - Split larger files per SOLID
5. **Environment separation** - .env never committed

---

## Architecture

```text
app/
├── Actions/              # Single-purpose action classes
├── Contracts/            # Interfaces (DI)
├── DTOs/                 # Data transfer objects
├── Enums/                # PHP 8.1+ enums
├── Events/               # Domain events
├── Http/
│   ├── Controllers/      # Thin controllers
│   ├── Middleware/       # Request filters
│   ├── Requests/         # Form validation
│   └── Resources/        # API transformations
├── Jobs/                 # Queued jobs
├── Listeners/            # Event handlers
├── Models/               # Eloquent models only
├── Policies/             # Authorization
├── Providers/            # Service registration
├── Repositories/         # Data access layer
└── Services/             # Business logic
```

---

## Reference Guide

### Core Architecture

| Reference | When to Use |
|-----------|-------------|
| [container.md](references/container.md) | Dependency injection, binding, resolution |
| [providers.md](references/providers.md) | Service registration, bootstrapping |
| [facades.md](references/facades.md) | Static proxies, real-time facades |
| [contracts.md](references/contracts.md) | Interfaces, loose coupling |
| [structure.md](references/structure.md) | Directory organization |
| [lifecycle.md](references/lifecycle.md) | Request handling flow |

### Configuration & Setup

| Reference | When to Use |
|-----------|-------------|
| [configuration.md](references/configuration.md) | Environment, config files |
| [installation.md](references/installation.md) | New project setup |
| [upgrade.md](references/upgrade.md) | Version upgrades, breaking changes |
| [releases.md](references/releases.md) | Release notes, versioning |

### Development Environments

| Reference | When to Use |
|-----------|-------------|
| [sail.md](references/sail.md) | Docker development |
| [valet.md](references/valet.md) | macOS native development |
| [homestead.md](references/homestead.md) | Vagrant (legacy) |
| [octane.md](references/octane.md) | High-performance servers |

### Utilities & Tools

| Reference | When to Use |
|-----------|-------------|
| [artisan.md](references/artisan.md) | CLI commands, custom commands |
| [helpers.md](references/helpers.md) | Global helper functions |
| [filesystem.md](references/filesystem.md) | File storage, S3, local |
| [processes.md](references/processes.md) | Shell command execution |
| [context.md](references/context.md) | Request-scoped data sharing |

### Advanced Features

| Reference | When to Use |
|-----------|-------------|
| [pennant.md](references/pennant.md) | Feature flags |
| [mcp.md](references/mcp.md) | Model Context Protocol |
| [concurrency.md](references/concurrency.md) | Parallel execution |

### Operations

| Reference | When to Use |
|-----------|-------------|
| [deployment.md](references/deployment.md) | Production deployment |
| [envoy.md](references/envoy.md) | SSH task automation |
| [logging.md](references/logging.md) | Log channels, formatting |
| [errors.md](references/errors.md) | Exception handling |
| [packages.md](references/packages.md) | Creating packages |

---

## Templates

| Template | Purpose |
|----------|---------|
| [UserService.php.md](references/templates/UserService.php.md) | Service + repository pattern |
| [AppServiceProvider.php.md](references/templates/AppServiceProvider.php.md) | DI bindings, bootstrapping |
| [ArtisanCommand.php.md](references/templates/ArtisanCommand.php.md) | CLI commands, signatures, I/O |
| [McpServer.php.md](references/templates/McpServer.php.md) | MCP servers, tools, resources, prompts |
| [PennantFeature.php.md](references/templates/PennantFeature.php.md) | Feature flags, A/B testing |
| [Envoy.blade.php.md](references/templates/Envoy.blade.php.md) | SSH deployment automation |
| [sail-config.md](references/templates/sail-config.md) | Docker Sail configuration |
| [octane-config.md](references/templates/octane-config.md) | FrankenPHP, Swoole, RoadRunner |

---

## Feature Matrix

| Feature | Reference | Priority |
|---------|-----------|----------|
| Service Container | container.md | High |
| Service Providers | providers.md | High |
| Directory Structure | structure.md | High |
| Configuration | configuration.md | High |
| Installation | installation.md | High |
| Octane (Performance) | octane.md | High |
| Sail (Docker) | sail.md | High |
| Artisan CLI | artisan.md | Medium |
| Deployment | deployment.md | Medium |
| Envoy (SSH) | envoy.md | Medium |
| Facades | facades.md | Medium |
| Contracts | contracts.md | Medium |
| Valet (macOS) | valet.md | Medium |
| Upgrade Guide | upgrade.md | Medium |
| Logging | logging.md | Medium |
| Errors | errors.md | Medium |
| Lifecycle | lifecycle.md | Medium |
| Filesystem | filesystem.md | Medium |
| Helpers | helpers.md | Low |
| Pennant (Flags) | pennant.md | Low |
| Context | context.md | Low |
| Processes | processes.md | Low |
| Concurrency | concurrency.md | Low |
| MCP | mcp.md | Low |
| Packages | packages.md | Low |
| Releases | releases.md | Low |
| Homestead | homestead.md | Low |

---

## Quick Reference

### Service Injection

```php
public function __construct(
    private readonly UserServiceInterface $userService,
) {}
```

### Service Provider Binding

```php
public function register(): void
{
    $this->app->bind(UserServiceInterface::class, UserService::class);
    $this->app->singleton(CacheService::class);
}
```

### Artisan Command

```shell
php artisan make:provider CustomServiceProvider
php artisan make:command ProcessOrders
```

### Environment Access

```php
$debug = env('APP_DEBUG', false);
$config = config('app.name');
```
