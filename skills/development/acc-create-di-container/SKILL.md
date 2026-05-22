---
name: acc-create-di-container
description: Generates DI Container configuration for PHP 8.5. Creates module classes, service providers, container configuration, and autowiring setup. Supports Symfony, Laravel, and PHP-DI patterns. Includes unit tests.
---

# DI Container Generator

## Overview

Generates Dependency Injection container configuration components for PHP 8.5 following DDD and Clean Architecture principles.

## When to Use

- Setting up new bounded context DI configuration
- Creating service provider/module for feature
- Configuring autowiring and interface bindings
- Registering tagged services (handlers, strategies)
- Setting up factory-based service creation

## Generated Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Module | `src/Infrastructure/DependencyInjection/{Context}Module.php` | Service registration |
| ServiceProvider | `src/Infrastructure/DependencyInjection/{Context}ServiceProvider.php` | Laravel-style provider |
| Extension | `src/Infrastructure/DependencyInjection/{Context}Extension.php` | Symfony bundle extension |
| Configuration | `config/services/{context}.yaml` | YAML configuration |
| CompilerPass | `src/Infrastructure/DependencyInjection/Compiler/{Name}Pass.php` | Service manipulation |

## Input Requirements

1. **Context name** - Bounded context (e.g., "Order", "Payment")
2. **Framework** - Symfony, Laravel, or PHP-DI
3. **Services to register** - Interfaces and implementations
4. **Tagged services** - Handlers, strategies, listeners

## File Placement

```
src/
└── Infrastructure/
    └── DependencyInjection/
        ├── {Context}Module.php           # Pure PHP registration
        ├── {Context}ServiceProvider.php  # Laravel
        ├── {Context}Extension.php        # Symfony
        └── Compiler/
            └── {Handler}Pass.php         # Compiler passes

config/
└── services/
    └── {context}.yaml                    # YAML config
```

## Template: Module Class (Framework-agnostic)

```php
<?php

declare(strict_types=1);

namespace App\{Context}\Infrastructure\DependencyInjection;

use App\{Context}\Application\Command\CreateOrderHandler;
use App\{Context}\Application\Query\GetOrderHandler;
use App\{Context}\Domain\Repository\OrderRepository;
use App\{Context}\Infrastructure\Persistence\DoctrineOrderRepository;

/**
 * Dependency injection module for {Context} bounded context.
 */
final readonly class {Context}Module
{
    /**
     * @return array<string, array{class: class-string, arguments: array<string>}>
     */
    public function getDefinitions(): array
    {
        return [
            // Repository bindings
            OrderRepository::class => [
                'class' => DoctrineOrderRepository::class,
                'arguments' => ['@doctrine.entity_manager'],
            ],

            // Command handlers
            CreateOrderHandler::class => [
                'class' => CreateOrderHandler::class,
                'arguments' => [
                    '@' . OrderRepository::class,
                    '@event_dispatcher',
                ],
                'tags' => ['command_handler'],
            ],

            // Query handlers
            GetOrderHandler::class => [
                'class' => GetOrderHandler::class,
                'arguments' => ['@order_read_repository'],
                'tags' => ['query_handler'],
            ],
        ];
    }

    /**
     * @return array<string, class-string>
     */
    public function getInterfaceBindings(): array
    {
        return [
            OrderRepository::class => DoctrineOrderRepository::class,
            PaymentGateway::class => StripePaymentGateway::class,
        ];
    }

    /**
     * @return array<string, array<class-string>>
     */
    public function getTaggedServices(): array
    {
        return [
            'command_handler' => [
                CreateOrderHandler::class,
                CancelOrderHandler::class,
                ShipOrderHandler::class,
            ],
            'query_handler' => [
                GetOrderHandler::class,
                ListOrdersHandler::class,
            ],
            'payment_gateway' => [
                StripePaymentGateway::class,
                PayPalPaymentGateway::class,
            ],
        ];
    }
}
```

## Template: Symfony Service Provider

```php
<?php

declare(strict_types=1);

namespace App\{Context}\Infrastructure\DependencyInjection;

use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\DependencyInjection\Extension\Extension;
use Symfony\Component\DependencyInjection\Loader\YamlFileLoader;
use Symfony\Component\Config\FileLocator;

final class {Context}Extension extends Extension
{
    public function load(array $configs, ContainerBuilder $container): void
    {
        $loader = new YamlFileLoader(
            $container,
            new FileLocator(__DIR__ . '/../../config'),
        );

        $loader->load('services.yaml');

        $this->registerRepositories($container);
        $this->registerHandlers($container);
        $this->registerAdapters($container);
    }

    private function registerRepositories(ContainerBuilder $container): void
    {
        $container->setAlias(
            OrderRepository::class,
            DoctrineOrderRepository::class,
        );
    }

    private function registerHandlers(ContainerBuilder $container): void
    {
        $container->registerForAutoconfiguration(CommandHandler::class)
            ->addTag('messenger.message_handler');

        $container->registerForAutoconfiguration(QueryHandler::class)
            ->addTag('messenger.message_handler');
    }

    private function registerAdapters(ContainerBuilder $container): void
    {
        $container->setAlias(
            PaymentGateway::class,
            StripePaymentGateway::class,
        );
    }

    public function getAlias(): string
    {
        return '{context}';
    }
}
```

## Template: Symfony YAML Configuration

```yaml
# config/services/{context}.yaml

services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  # Repositories
  App\{Context}\Domain\Repository\OrderRepository:
    class: App\{Context}\Infrastructure\Persistence\DoctrineOrderRepository

  # Command Handlers (auto-tagged by messenger)
  App\{Context}\Application\Command\:
    resource: '../../../src/{Context}/Application/Command/*Handler.php'
    tags:
      - { name: messenger.message_handler }

  # Query Handlers
  App\{Context}\Application\Query\:
    resource: '../../../src/{Context}/Application/Query/*Handler.php'
    tags:
      - { name: messenger.message_handler }

  # Domain Services
  App\{Context}\Domain\Service\:
    resource: '../../../src/{Context}/Domain/Service/*.php'

  # Adapters (Payment Gateways as tagged services)
  App\{Context}\Infrastructure\Adapter\PaymentGateway\:
    resource: '../../../src/{Context}/Infrastructure/Adapter/PaymentGateway/*.php'
    tags:
      - { name: app.payment_gateway }

  # Payment Gateway Registry
  App\{Context}\Infrastructure\PaymentGatewayRegistry:
    arguments:
      $gateways: !tagged_iterator app.payment_gateway
```

## Template: Laravel Service Provider

```php
<?php

declare(strict_types=1);

namespace App\{Context}\Infrastructure\DependencyInjection;

use App\{Context}\Application\Command\CreateOrderHandler;
use App\{Context}\Domain\Repository\OrderRepository;
use App\{Context}\Infrastructure\Persistence\DoctrineOrderRepository;
use Illuminate\Support\ServiceProvider;

final class {Context}ServiceProvider extends ServiceProvider
{
    /**
     * @var array<class-string, class-string>
     */
    public array $bindings = [
        OrderRepository::class => DoctrineOrderRepository::class,
        PaymentGateway::class => StripePaymentGateway::class,
    ];

    /**
     * @var array<class-string>
     */
    public array $singletons = [
        PaymentGatewayRegistry::class,
        OrderReadRepository::class,
    ];

    public function register(): void
    {
        $this->registerRepositories();
        $this->registerHandlers();
        $this->registerAdapters();
    }

    public function boot(): void
    {
        $this->registerTaggedServices();
    }

    private function registerRepositories(): void
    {
        $this->app->bind(
            OrderRepository::class,
            DoctrineOrderRepository::class,
        );
    }

    private function registerHandlers(): void
    {
        $this->app->bind(CreateOrderHandler::class, function ($app) {
            return new CreateOrderHandler(
                $app->make(OrderRepository::class),
                $app->make(EventDispatcher::class),
            );
        });
    }

    private function registerAdapters(): void
    {
        $this->app->when(PaymentService::class)
            ->needs(PaymentGateway::class)
            ->give(function ($app) {
                $gateway = config('payment.gateway', 'stripe');

                return match ($gateway) {
                    'stripe' => $app->make(StripePaymentGateway::class),
                    'paypal' => $app->make(PayPalPaymentGateway::class),
                    default => throw new InvalidConfigurationException(),
                };
            });
    }

    private function registerTaggedServices(): void
    {
        $this->app->tag([
            StripePaymentGateway::class,
            PayPalPaymentGateway::class,
        ], 'payment_gateways');

        $this->app->bind(PaymentGatewayRegistry::class, function ($app) {
            return new PaymentGatewayRegistry(
                $app->tagged('payment_gateways'),
            );
        });
    }
}
```

## Template: Symfony Compiler Pass

```php
<?php

declare(strict_types=1);

namespace App\{Context}\Infrastructure\DependencyInjection\Compiler;

use Symfony\Component\DependencyInjection\Compiler\CompilerPassInterface;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\DependencyInjection\Reference;

final class PaymentGatewayPass implements CompilerPassInterface
{
    public function process(ContainerBuilder $container): void
    {
        if (!$container->has(PaymentGatewayRegistry::class)) {
            return;
        }

        $definition = $container->findDefinition(PaymentGatewayRegistry::class);
        $taggedServices = $container->findTaggedServiceIds('app.payment_gateway');

        $gateways = [];
        foreach ($taggedServices as $id => $tags) {
            $gateways[] = new Reference($id);
        }

        $definition->setArgument('$gateways', $gateways);
    }
}
```

## Template: PHP-DI Configuration

```php
<?php

declare(strict_types=1);

use App\{Context}\Domain\Repository\OrderRepository;
use App\{Context}\Infrastructure\Persistence\DoctrineOrderRepository;
use DI\ContainerBuilder;

return function (ContainerBuilder $containerBuilder): void {
    $containerBuilder->addDefinitions([
        // Interface bindings
        OrderRepository::class => \DI\autowire(DoctrineOrderRepository::class),
        PaymentGateway::class => \DI\autowire(StripePaymentGateway::class),

        // Factory-based creation
        OrderFactory::class => \DI\factory(function ($container) {
            return new OrderFactory(
                $container->get(IdGenerator::class),
                $container->get(Clock::class),
            );
        }),

        // Decorated service
        LoggingOrderRepository::class => \DI\decorate(function ($previous, $container) {
            return new LoggingOrderRepository(
                $previous,
                $container->get(LoggerInterface::class),
            );
        }),

        // Tagged services collection
        'payment_gateways' => \DI\factory(function ($container) {
            return [
                $container->get(StripePaymentGateway::class),
                $container->get(PayPalPaymentGateway::class),
            ];
        }),
    ]);
};
```

## Unit Test Template

```php
<?php

declare(strict_types=1);

namespace Tests\{Context}\Infrastructure\DependencyInjection;

use App\{Context}\Domain\Repository\OrderRepository;
use App\{Context}\Infrastructure\DependencyInjection\{Context}Module;
use App\{Context}\Infrastructure\Persistence\DoctrineOrderRepository;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\TestCase;

#[Group('unit')]
#[CoversClass({Context}Module::class)]
final class {Context}ModuleTest extends TestCase
{
    private {Context}Module $module;

    protected function setUp(): void
    {
        $this->module = new {Context}Module();
    }

    public function testProvidesRepositoryBindings(): void
    {
        $bindings = $this->module->getInterfaceBindings();

        $this->assertArrayHasKey(OrderRepository::class, $bindings);
        $this->assertSame(DoctrineOrderRepository::class, $bindings[OrderRepository::class]);
    }

    public function testProvidesTaggedServices(): void
    {
        $tagged = $this->module->getTaggedServices();

        $this->assertArrayHasKey('command_handler', $tagged);
        $this->assertNotEmpty($tagged['command_handler']);
    }

    public function testProvidesServiceDefinitions(): void
    {
        $definitions = $this->module->getDefinitions();

        $this->assertArrayHasKey(CreateOrderHandler::class, $definitions);
        $this->assertArrayHasKey('arguments', $definitions[CreateOrderHandler::class]);
    }
}
```

## SOLID Compliance

| Principle | Implementation |
|-----------|----------------|
| SRP | Module only handles DI registration |
| OCP | Tagged services enable extension without modification |
| DIP | Interface-to-implementation bindings |
| ISP | Small focused modules per context |

## References

See `references/` for detailed documentation:
- `templates.md` - Additional templates
- `examples.md` - Real-world examples
