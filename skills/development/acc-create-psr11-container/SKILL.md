---
name: acc-create-psr11-container
description: Generates PSR-11 Container implementation for PHP 8.5. Creates ContainerInterface with service resolution, autowiring support, and exceptions. Includes unit tests.
---

# PSR-11 Container Generator

## Overview

Generates PSR-11 compliant dependency injection container implementations.

## When to Use

- Building lightweight DI container
- Creating service locator
- Simple service resolution needs
- Testing with mock containers

## Generated Components

| Component | Description | Location |
|-----------|-------------|----------|
| Container | Container implementation | `src/Infrastructure/Container/` |
| Exceptions | PSR-11 exceptions | `src/Infrastructure/Container/` |
| Unit Tests | PHPUnit tests | `tests/Unit/Infrastructure/Container/` |

## Template: Simple Container

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Container;

use Closure;
use Psr\Container\ContainerInterface;

final class Container implements ContainerInterface
{
    /** @var array<string, mixed> */
    private array $services = [];

    /** @var array<string, Closure> */
    private array $factories = [];

    public function get(string $id): mixed
    {
        if (isset($this->services[$id])) {
            return $this->services[$id];
        }

        if (isset($this->factories[$id])) {
            $this->services[$id] = ($this->factories[$id])($this);

            return $this->services[$id];
        }

        throw new NotFoundException("Service not found: {$id}");
    }

    public function has(string $id): bool
    {
        return isset($this->services[$id]) || isset($this->factories[$id]);
    }

    public function set(string $id, mixed $service): void
    {
        $this->services[$id] = $service;
    }

    public function factory(string $id, Closure $factory): void
    {
        $this->factories[$id] = $factory;
    }
}
```

## Template: Autowiring Container

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Container;

use Closure;
use Psr\Container\ContainerInterface;
use ReflectionClass;
use ReflectionNamedType;
use ReflectionParameter;

final class AutowiringContainer implements ContainerInterface
{
    /** @var array<string, mixed> */
    private array $services = [];

    /** @var array<string, Closure> */
    private array $factories = [];

    /** @var array<string, string> */
    private array $aliases = [];

    public function get(string $id): mixed
    {
        $id = $this->resolveAlias($id);

        if (isset($this->services[$id])) {
            return $this->services[$id];
        }

        if (isset($this->factories[$id])) {
            $this->services[$id] = ($this->factories[$id])($this);

            return $this->services[$id];
        }

        if (class_exists($id)) {
            $this->services[$id] = $this->autowire($id);

            return $this->services[$id];
        }

        throw new NotFoundException("Service not found: {$id}");
    }

    public function has(string $id): bool
    {
        $id = $this->resolveAlias($id);

        return isset($this->services[$id])
            || isset($this->factories[$id])
            || class_exists($id);
    }

    public function set(string $id, mixed $service): void
    {
        $this->services[$id] = $service;
    }

    public function factory(string $id, Closure $factory): void
    {
        $this->factories[$id] = $factory;
    }

    public function alias(string $alias, string $id): void
    {
        $this->aliases[$alias] = $id;
    }

    private function resolveAlias(string $id): string
    {
        return $this->aliases[$id] ?? $id;
    }

    private function autowire(string $class): object
    {
        $reflection = new ReflectionClass($class);

        if (!$reflection->isInstantiable()) {
            throw new ContainerException("Cannot instantiate: {$class}");
        }

        $constructor = $reflection->getConstructor();

        if ($constructor === null) {
            return new $class();
        }

        $parameters = $constructor->getParameters();
        $dependencies = array_map(
            fn(ReflectionParameter $param) => $this->resolveDependency($param),
            $parameters,
        );

        return new $class(...$dependencies);
    }

    private function resolveDependency(ReflectionParameter $parameter): mixed
    {
        $type = $parameter->getType();

        if ($type === null) {
            if ($parameter->isDefaultValueAvailable()) {
                return $parameter->getDefaultValue();
            }

            throw new ContainerException(
                "Cannot resolve parameter: {$parameter->getName()}",
            );
        }

        if (!$type instanceof ReflectionNamedType || $type->isBuiltin()) {
            if ($parameter->isDefaultValueAvailable()) {
                return $parameter->getDefaultValue();
            }

            throw new ContainerException(
                "Cannot resolve builtin type: {$parameter->getName()}",
            );
        }

        return $this->get($type->getName());
    }
}
```

## Template: Exceptions

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Container;

use Exception;
use Psr\Container\ContainerExceptionInterface;
use Psr\Container\NotFoundExceptionInterface;

final class ContainerException extends Exception implements ContainerExceptionInterface
{
}

final class NotFoundException extends Exception implements NotFoundExceptionInterface
{
}
```

## Template: Unit Test

```php
<?php

declare(strict_types=1);

namespace App\Tests\Unit\Infrastructure\Container;

use App\Infrastructure\Container\AutowiringContainer;
use App\Infrastructure\Container\NotFoundException;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

#[Group('unit')]
#[CoversClass(AutowiringContainer::class)]
final class AutowiringContainerTest extends TestCase
{
    private AutowiringContainer $container;

    protected function setUp(): void
    {
        $this->container = new AutowiringContainer();
    }

    #[Test]
    public function it_resolves_registered_service(): void
    {
        $service = new \stdClass();
        $this->container->set('service', $service);

        self::assertSame($service, $this->container->get('service'));
    }

    #[Test]
    public function it_resolves_factory(): void
    {
        $this->container->factory('service', fn() => new \stdClass());

        $service1 = $this->container->get('service');
        $service2 = $this->container->get('service');

        self::assertSame($service1, $service2);
    }

    #[Test]
    public function it_autowires_class(): void
    {
        $service = $this->container->get(SimpleService::class);

        self::assertInstanceOf(SimpleService::class, $service);
    }

    #[Test]
    public function it_throws_not_found_for_unknown_service(): void
    {
        $this->expectException(NotFoundException::class);

        $this->container->get('unknown');
    }

    #[Test]
    public function it_resolves_aliases(): void
    {
        $this->container->set('concrete', new \stdClass());
        $this->container->alias('alias', 'concrete');

        self::assertSame(
            $this->container->get('concrete'),
            $this->container->get('alias'),
        );
    }
}

class SimpleService
{
}
```

## Usage Example

```php
<?php

use App\Infrastructure\Container\AutowiringContainer;

$container = new AutowiringContainer();

// Register services
$container->set('config', ['db' => 'mysql://localhost/app']);

// Register factories
$container->factory(LoggerInterface::class, fn($c) => new FileLogger('/var/log/app.log'));

// Register aliases (interface to implementation)
$container->alias(UserRepositoryInterface::class, DoctrineUserRepository::class);

// Resolve services
$logger = $container->get(LoggerInterface::class);
$repository = $container->get(UserRepositoryInterface::class);
$handler = $container->get(CreateUserHandler::class); // Autowired
```

## Requirements

```json
{
    "require": {
        "psr/container": "^2.0"
    }
}
```

## See Also

- `references/templates.md` - Additional container patterns
- `references/examples.md` - Integration examples
