---
name: observability-instrumentation
description: Add business metrics using AWS EMF (Embedded Metric Format) to API endpoints. Focus on domain-specific metrics only - AWS AppRunner provides default SLO/SLA metrics. Use when implementing new endpoints, adding command handlers, or instrumenting business events.
---

# Business Metrics with AWS EMF

Instrument API endpoints with **business metrics** using AWS CloudWatch Embedded Metric Format (EMF). This skill focuses exclusively on domain-specific metrics - AWS AppRunner already provides infrastructure SLO/SLA metrics automatically.

## What This Skill Covers

- **Business metrics** - Domain events (users created, orders placed, payments processed)
- **AWS EMF format** - Logs that automatically become CloudWatch metrics
- **Event subscribers** - Metrics emitted via domain event subscribers (not in handlers)
- **Type-safe metrics** - Concrete metric classes instead of arrays
- **SOLID principles** - Single Responsibility (subscribers) + Open/Closed (new metric classes)

## What This Skill Does NOT Cover

- **Infrastructure metrics** - Latency, error rates, RPS (AWS AppRunner provides these)
- **SLO/SLA metrics** - Availability, response times (AWS AppRunner provides these)
- **Distributed tracing** - Use AWS X-Ray integration instead

## When to Use This Skill

Use this skill when:

- Implementing new API endpoints that have business significance
- Adding domain events that should trigger metric emission
- Tracking domain events for analytics and business intelligence
- Building dashboards for business KPIs

> User Service defaults: use `Endpoint=User` with operations like `create` (registration), `update` (profile changes), and `request-password-reset`; run checks via `make <command>`; keep Domain entities free of framework/validation concerns.

---

## Architecture Overview

Business metrics follow these patterns:

1. **Metric classes** - Each metric type is a concrete class extending `BusinessMetric`
2. **Event subscribers** - Metrics are emitted via domain event subscribers (not hardcoded in handlers)
3. **Symfony logger** - EMF output goes through Monolog with a custom EMF formatter
4. **No arrays** - All metric configuration uses typed objects, not arrays
5. **Collections** - Multiple metrics use `MetricCollection`, not arrays

---

## SOLID Principles in Observability

### Single Responsibility Principle (SRP)

Each class has ONE responsibility:

| Class                          | Responsibility                           |
| ------------------------------ | ---------------------------------------- |
| `UsersCreatedMetric`           | Define metric name, value, dimensions    |
| `UserCreatedMetricsSubscriber` | Listen to event, emit metric             |
| `AwsEmfBusinessMetricsEmitter` | Format and write EMF logs                |
| `MetricCollection`             | Hold multiple metrics for batch emission |

**Anti-pattern**: Metrics emitted directly in command handlers (violates SRP - handler should only handle commands)

### Open/Closed Principle (OCP)

- **Open for extension**: Add new metrics via new classes
- **Closed for modification**: Don't change existing metric/emitter code

```php
// ✅ GOOD: Add new metric by creating new class
final readonly class OrdersPlacedMetric extends EndpointOperationBusinessMetric { ... }

// ❌ BAD: Modify existing emitter to handle new metric type
```

### Why Event Subscribers (Not Handler Injection)

```php
// ❌ BAD: Metrics in command handler (violates SRP)
final class CreateUserHandler
{
    public function __construct(
        private UserRepository $repository,
        private BusinessMetricsEmitterInterface $metrics  // Wrong!
    ) {}
}

// ✅ GOOD: Metrics in dedicated event subscriber
final class UserCreatedMetricsSubscriber implements DomainEventSubscriberInterface
{
    public function __invoke(UserCreatedEvent $event): void
    {
        $this->metricsEmitter->emit($this->metricFactory->create());
    }
}
```

**Benefits**:

- Handler focuses on domain logic only
- Metrics emission is decoupled and testable
- Easy to add/remove metrics without touching business logic
- Multiple subscribers can react to same event

---

## Type-Safe Metric Class Hierarchy

```text
BusinessMetric (abstract)
├── EndpointOperationBusinessMetric (abstract) - for metrics with Endpoint/Operation dimensions
│   ├── UsersCreatedMetric
│   ├── UsersUpdatedMetric
│   ├── UsersDeletedMetric
│   └── EndpointInvocationsMetric
└── (other base classes for different dimension patterns)

MetricDimensionsInterface
├── EndpointOperationMetricDimensions - Endpoint + Operation
└── (custom dimensions for specific metrics)

MetricDimensions - typed collection of MetricDimension objects
MetricDimension - key/value pair

MetricUnit (enum)
├── COUNT, NONE, SECONDS, MILLISECONDS, BYTES, PERCENT

MetricCollection - typed collection implementing IteratorAggregate, Countable
```

**Why no arrays?**

| Arrays              | Typed Classes             |
| ------------------- | ------------------------- |
| No type safety      | Full type checking        |
| No IDE autocomplete | IDE support               |
| Runtime errors      | Compile-time errors       |
| Hard to refactor    | Easy to refactor          |
| No encapsulation    | Validation in constructor |

---

## Current Implementation

### Metric Base Class (Application Layer)

```php
// src/Shared/Application/Observability/Metric/BusinessMetric.php
abstract readonly class BusinessMetric
{
    public function __construct(
        private float|int $value,
        private MetricUnit $unit
    ) {}

    abstract public function name(): string;
    abstract public function dimensions(): MetricDimensionsInterface;

    public function value(): float|int { return $this->value; }
    public function unit(): MetricUnit { return $this->unit; }
}
```

### Concrete Metric Example

```php
// src/User/Application/Metric/UsersCreatedMetric.php
final readonly class UsersCreatedMetric extends EndpointOperationBusinessMetric
{
    private const ENDPOINT = 'User';
    private const OPERATION = 'create';

    public function __construct(
        MetricDimensionsFactoryInterface $dimensionsFactory,
        float|int $value = 1
    ) {
        parent::__construct($dimensionsFactory, $value, MetricUnit::COUNT);
    }

    public function name(): string
    {
        return 'UsersCreated';
    }

    protected function endpoint(): string
    {
        return self::ENDPOINT;
    }

    protected function operation(): string
    {
        return self::OPERATION;
    }
}
```

### Emitter Interface (Application Layer)

```php
// src/Shared/Application/Observability/Emitter/BusinessMetricsEmitterInterface.php
interface BusinessMetricsEmitterInterface
{
    public function emit(BusinessMetric $metric): void;
    public function emitCollection(MetricCollection $metrics): void;
}
```

### Metrics Event Subscriber

```php
// src/User/Application/EventSubscriber/UserCreatedMetricsSubscriber.php
/**
 * Error handling is automatic via DomainEventMessageHandler in async workers.
 * Subscribers stay clean - failures are logged + emit metrics automatically.
 * This ensures observability never breaks the main request (AP from CAP theorem).
 */
final readonly class UserCreatedMetricsSubscriber implements DomainEventSubscriberInterface
{
    public function __construct(
        private BusinessMetricsEmitterInterface $metricsEmitter,
        private UsersCreatedMetricFactoryInterface $metricFactory
    ) {
    }

    public function __invoke(UserCreatedEvent $event): void
    {
        $this->metricsEmitter->emit($this->metricFactory->create());
    }

    public function subscribedTo(): array
    {
        return [UserCreatedEvent::class];
    }
}
```

---

## AWS EMF Format

AWS Embedded Metric Format allows you to embed custom metrics in structured log events. CloudWatch automatically extracts metrics from EMF-formatted logs.

### EMF Log Structure

```json
{
  "_aws": {
    "Timestamp": 1702425600000,
    "CloudWatchMetrics": [
      {
        "Namespace": "UserService/BusinessMetrics",
        "Dimensions": [["Endpoint", "Operation"]],
        "Metrics": [{ "Name": "UsersCreated", "Unit": "Count" }]
      }
    ]
  },
  "Endpoint": "User",
  "Operation": "create",
  "UsersCreated": 1
}
```

When this log is written to stdout via the EMF Monolog channel, CloudWatch automatically:

1. Extracts `UsersCreated` as a metric
2. Associates it with the `UserService/BusinessMetrics` namespace
3. Applies dimensions `Endpoint` and `Operation`

---

## Creating New Business Metrics

### Step 1: Create the Metric Class

```php
// src/Core/Order/Application/Metric/OrdersPlacedMetric.php
namespace App\Core\Order\Application\Metric;

use App\Shared\Application\Observability\Metric\BusinessMetric;
use App\Shared\Application\Observability\Metric\MetricDimension;
use App\Shared\Application\Observability\Metric\MetricDimensions;
use App\Shared\Application\Observability\Metric\MetricDimensionsFactoryInterface;
use App\Shared\Application\Observability\Metric\MetricDimensionsInterface;
use App\Shared\Application\Observability\Metric\MetricUnit;

final readonly class OrdersPlacedMetricDimensions implements MetricDimensionsInterface
{
    public function __construct(
        private MetricDimensionsFactoryInterface $dimensionsFactory,
        private string $paymentMethod
    ) {
    }

    public function values(): MetricDimensions
    {
        return $this->dimensionsFactory->endpointOperationWith(
            'Order',
            'create',
            new MetricDimension('PaymentMethod', $this->paymentMethod)
        );
    }
}

final readonly class OrdersPlacedMetric extends BusinessMetric
{
    public function __construct(
        private MetricDimensionsFactoryInterface $dimensionsFactory,
        private string $paymentMethod,
        float|int $value = 1
    ) {
        parent::__construct($value, MetricUnit::COUNT);
    }

    public function name(): string
    {
        return 'OrdersPlaced';
    }

    public function dimensions(): MetricDimensionsInterface
    {
        return new OrdersPlacedMetricDimensions(
            dimensionsFactory: $this->dimensionsFactory,
            paymentMethod: $this->paymentMethod
        );
    }
}
```

### Step 2: Create the Event Subscriber

```php
// src/Core/Order/Application/EventSubscriber/OrderPlacedMetricsSubscriber.php
namespace App\Core\Order\Application\EventSubscriber;

use App\Core\Order\Application\Factory\OrdersPlacedMetricFactoryInterface;
use App\Core\Order\Domain\Event\OrderPlacedEvent;
use App\Shared\Application\Observability\Emitter\BusinessMetricsEmitterInterface;
use App\Shared\Domain\Bus\Event\DomainEventSubscriberInterface;

final readonly class OrderPlacedMetricsSubscriber implements DomainEventSubscriberInterface
{
    public function __construct(
        private BusinessMetricsEmitterInterface $metricsEmitter,
        private OrdersPlacedMetricFactoryInterface $metricFactory
    ) {}

    public function __invoke(OrderPlacedEvent $event): void
    {
        $this->metricsEmitter->emit($this->metricFactory->create($event->paymentMethod()));
    }

    /**
     * @return array<class-string>
     */
    public function subscribedTo(): array
    {
        return [OrderPlacedEvent::class];
    }
}
```

### Step 3: For Multiple Metrics - Use MetricCollection

```php
// Emit multiple metrics together (dimensionsFactory injected via constructor)
$this->metricsEmitter->emitCollection(new MetricCollection(
    $this->ordersPlacedMetricFactory->create($event->paymentMethod()),
    $this->orderValueMetricFactory->create($event->totalAmount())
));
```

---

## Dimension Best Practices

### Recommended Dimensions

| Dimension       | Description       | Cardinality |
| --------------- | ----------------- | ----------- |
| `Endpoint`      | API resource name | Low         |
| `Operation`     | CRUD action       | Very Low    |
| `PaymentMethod` | Payment type      | Low         |
| `UserType`      | User segment      | Low         |

### Avoid High-Cardinality Dimensions

**Don't use:**

- User IDs
- Order IDs
- Session IDs
- Timestamps

These create too many unique metric streams and increase CloudWatch costs.

---

## Metric Naming Conventions

### Format

```text
{Entity}{Action}   # PascalCase
```

### Examples

| Good                | Bad                   |
| ------------------- | --------------------- |
| `UsersCreated`      | `user_created`        |
| `OrdersPlaced`      | `orders.placed.count` |
| `PaymentsProcessed` | `payment-processed`   |

### Guidelines

- Use PascalCase for metric names
- Use plural nouns for counters (UsersCreated not UserCreated)
- Use past tense for completed actions

---

## Testing Business Metrics

### Use the Spy in Tests

```php
use App\Shared\Application\Observability\Metric\MetricDimension;
use App\Shared\Infrastructure\Observability\Factory\MetricDimensionsFactory;
use App\Tests\Unit\Shared\Infrastructure\Observability\BusinessMetricsEmitterSpy;

final class UserCreatedMetricsSubscriberTest extends TestCase
{
    public function testEmitsMetricOnUserCreated(): void
    {
        $metricsSpy = new BusinessMetricsEmitterSpy();
        $dimensionsFactory = new MetricDimensionsFactory();
        $metricFactory = new UsersCreatedMetricFactory($dimensionsFactory);
        $logger = $this->createMock(LoggerInterface::class);

        $subscriber = new UserCreatedMetricsSubscriber(
            $metricsSpy,
            $metricFactory,
            $logger
        );

        $event = new UserCreatedEvent($userId, $email);
        ($subscriber)($event);

        self::assertSame(1, $metricsSpy->count());

        foreach ($metricsSpy->emitted() as $metric) {
            self::assertSame('UsersCreated', $metric->name());
            self::assertSame(1, $metric->value());
            self::assertSame('User', $metric->dimensions()->values()->get('Endpoint'));
            self::assertSame('create', $metric->dimensions()->values()->get('Operation'));
        }

        // Or use the assertion helper
        $metricsSpy->assertEmittedWithDimensions(
            'UsersCreated',
            new MetricDimension('Endpoint', 'User'),
            new MetricDimension('Operation', 'create')
        );
    }
}
```

### Test Service Configuration

In `config/services_test.yaml`, the spy is configured:

```yaml
App\Shared\Application\Observability\Emitter\BusinessMetricsEmitterInterface: '@App\Tests\Unit\Shared\Infrastructure\Observability\BusinessMetricsEmitterSpy'

App\Tests\Unit\Shared\Infrastructure\Observability\BusinessMetricsEmitterSpy:
  public: true
```

---

## CloudWatch Queries

After deploying, query your business metrics:

```sql
-- Total endpoint invocations by resource
SELECT SUM(EndpointInvocations)
FROM "UserService/BusinessMetrics"
GROUP BY Endpoint

-- Users created over time
SELECT SUM(UsersCreated)
FROM "UserService/BusinessMetrics"
WHERE Endpoint = 'User'
```

---

## What NOT to Track

Remember: AWS AppRunner already provides infrastructure metrics.

**Don't track:**

- Request latency
- Error rates
- Response times
- HTTP status codes
- Memory usage
- CPU usage

**Do track:**

- Business events (orders placed, users created)
- Business values (order amounts, payment totals)
- Domain-specific actions (logins, uploads, exports)

---

## Success Criteria

After implementing business metrics:

- Each domain event that needs tracking has a corresponding metric subscriber
- Metrics use typed classes (not arrays)
- Metrics are emitted via event subscribers (not hardcoded in handlers)
- Dimensions provide meaningful segmentation
- Unit tests verify metric emission
- No infrastructure metrics (AppRunner handles those)

### SOLID Compliance Checklist

- [ ] **SRP**: Each metric class has single purpose (define one metric type)
- [ ] **SRP**: Event subscriber only emits metrics (no business logic)
- [ ] **OCP**: New metrics added via new classes (no modification to emitter)
- [ ] **OCP**: New event subscribers added without changing existing code
- [ ] **LSP**: All metrics properly extend `BusinessMetric` base class
- [ ] **ISP**: `MetricDimensionsInterface` is minimal (only `values()`)
- [ ] **DIP**: Handlers depend on `EventBusInterface`, not concrete metrics

### Type Safety Checklist

- [ ] NO arrays for metric configuration - use typed classes
- [ ] NO arrays for metric collections - use `MetricCollection`
- [ ] All dimensions via `MetricDimensionsInterface` implementations
- [ ] Arrays are allowed only at infrastructure boundaries (JSON serialization, PSR-3 log context)
- [ ] Unit enum `MetricUnit` used for all units

---

## Files Reference

### Metric Classes

- `src/Shared/Application/Observability/Metric/BusinessMetric.php` - Base class
- `src/Shared/Application/Observability/Metric/MetricUnit.php` - Unit enum
- `src/Shared/Application/Observability/Metric/MetricDimension.php` - Dimension key/value
- `src/Shared/Application/Observability/Metric/MetricDimensions.php` - Dimension collection
- `src/Shared/Application/Observability/Metric/MetricCollection.php` - Metrics collection
- `src/Shared/Application/Observability/Metric/EndpointInvocationsMetric.php` - Endpoint metric
- `src/User/Application/Metric/UsersCreatedMetric.php` - User create metric
- `src/User/Application/Metric/UsersUpdatedMetric.php` - User update metric
- `src/User/Application/Metric/UsersDeletedMetric.php` - User delete metric

### Infrastructure

- `src/Shared/Application/Observability/Emitter/BusinessMetricsEmitterInterface.php` - Interface
- `src/Shared/Infrastructure/Observability/AwsEmfBusinessMetricsEmitter.php` - EMF implementation
- `src/Shared/Infrastructure/Observability/EmfLogFormatter.php` - Monolog formatter

### Event Subscribers

- `src/Shared/Infrastructure/Observability/ApiEndpointBusinessMetricsSubscriber.php` - HTTP metrics
- `src/User/Application/EventSubscriber/UserCreatedMetricsSubscriber.php`
- `src/User/Application/EventSubscriber/UserUpdatedMetricsSubscriber.php`
- `src/User/Application/EventSubscriber/UserDeletedMetricsSubscriber.php`

### Configuration

- `config/packages/monolog.yaml` - EMF channel configuration
- `config/services.yaml` - Production wiring
- `config/services_test.yaml` - Test spy wiring

---

## AWS Documentation

- [CloudWatch Embedded Metric Format](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html)
- [AWS App Runner Metrics](https://docs.aws.amazon.com/apprunner/latest/dg/monitor-cw.html)
