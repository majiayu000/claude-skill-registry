---
name: acc-create-mock-repository
description: Generates InMemory repository implementations for PHP 8.5 testing. Creates fake repositories with array storage, supporting CRUD operations and queries without database.
---

# Mock Repository Generator

Generates InMemory (Fake) repository implementations for testing.

## Characteristics

- **No database** — stores entities in memory
- **Fast** — no I/O operations
- **Isolated** — fresh state per test
- **Deterministic** — predictable behavior
- **Implements interface** — same contract as real repository

## Template

```php
<?php

declare(strict_types=1);

namespace Tests\Fake;

use {RepositoryInterface};
use {Entity};
use {EntityId};

final class InMemory{Entity}Repository implements {RepositoryInterface}
{
    /** @var array<string, {Entity}> */
    private array $entities = [];

    public function save({Entity} $entity): void
    {
        $this->entities[$entity->id()->toString()] = $entity;
    }

    public function findById({EntityId} $id): ?{Entity}
    {
        return $this->entities[$id->toString()] ?? null;
    }

    public function delete({Entity} $entity): void
    {
        unset($this->entities[$entity->id()->toString()]);
    }

    /** @return list<{Entity}> */
    public function findAll(): array
    {
        return array_values($this->entities);
    }

    public function clear(): void
    {
        $this->entities = [];
    }
}
```

## Complete Examples

### User Repository

```php
<?php

declare(strict_types=1);

namespace Tests\Fake;

use App\Domain\User\User;
use App\Domain\User\UserId;
use App\Domain\User\Email;
use App\Domain\User\UserRepositoryInterface;

final class InMemoryUserRepository implements UserRepositoryInterface
{
    /** @var array<string, User> */
    private array $users = [];

    public function save(User $user): void
    {
        $this->users[$user->id()->toString()] = $user;
    }

    public function findById(UserId $id): ?User
    {
        return $this->users[$id->toString()] ?? null;
    }

    public function findByEmail(Email $email): ?User
    {
        foreach ($this->users as $user) {
            if ($user->email()->equals($email)) {
                return $user;
            }
        }
        return null;
    }

    public function delete(User $user): void
    {
        unset($this->users[$user->id()->toString()]);
    }

    public function existsByEmail(Email $email): bool
    {
        return $this->findByEmail($email) !== null;
    }

    /** @return list<User> */
    public function findAll(): array
    {
        return array_values($this->users);
    }

    public function count(): int
    {
        return count($this->users);
    }

    public function clear(): void
    {
        $this->users = [];
    }
}
```

### Order Repository with Queries

```php
<?php

declare(strict_types=1);

namespace Tests\Fake;

use App\Domain\Order\Order;
use App\Domain\Order\OrderId;
use App\Domain\Order\OrderStatus;
use App\Domain\Order\OrderRepositoryInterface;
use App\Domain\Customer\CustomerId;
use DateTimeImmutable;

final class InMemoryOrderRepository implements OrderRepositoryInterface
{
    /** @var array<string, Order> */
    private array $orders = [];

    public function save(Order $order): void
    {
        $this->orders[$order->id()->toString()] = $order;
    }

    public function findById(OrderId $id): ?Order
    {
        return $this->orders[$id->toString()] ?? null;
    }

    public function delete(Order $order): void
    {
        unset($this->orders[$order->id()->toString()]);
    }

    /** @return list<Order> */
    public function findByCustomer(CustomerId $customerId): array
    {
        return array_values(array_filter(
            $this->orders,
            fn(Order $order) => $order->customerId()->equals($customerId)
        ));
    }

    /** @return list<Order> */
    public function findByStatus(OrderStatus $status): array
    {
        return array_values(array_filter(
            $this->orders,
            fn(Order $order) => $order->status() === $status
        ));
    }

    /** @return list<Order> */
    public function findPending(): array
    {
        return $this->findByStatus(OrderStatus::Pending);
    }

    /** @return list<Order> */
    public function findCreatedBefore(DateTimeImmutable $date): array
    {
        return array_values(array_filter(
            $this->orders,
            fn(Order $order) => $order->createdAt() < $date
        ));
    }

    /** @return list<Order> */
    public function findAll(int $limit = 100, int $offset = 0): array
    {
        return array_slice(array_values($this->orders), $offset, $limit);
    }

    public function count(): int
    {
        return count($this->orders);
    }

    public function countByStatus(OrderStatus $status): int
    {
        return count($this->findByStatus($status));
    }

    public function clear(): void
    {
        $this->orders = [];
    }

    // Test helpers
    public function getAll(): array
    {
        return $this->orders;
    }

    public function has(OrderId $id): bool
    {
        return isset($this->orders[$id->toString()]);
    }
}
```

### Repository with Specifications

```php
<?php

declare(strict_types=1);

namespace Tests\Fake;

use App\Domain\Product\Product;
use App\Domain\Product\ProductId;
use App\Domain\Product\ProductRepositoryInterface;
use App\Domain\Shared\Specification\SpecificationInterface;

final class InMemoryProductRepository implements ProductRepositoryInterface
{
    /** @var array<string, Product> */
    private array $products = [];

    public function save(Product $product): void
    {
        $this->products[$product->id()->toString()] = $product;
    }

    public function findById(ProductId $id): ?Product
    {
        return $this->products[$id->toString()] ?? null;
    }

    public function delete(Product $product): void
    {
        unset($this->products[$product->id()->toString()]);
    }

    /** @return list<Product> */
    public function findBySpecification(SpecificationInterface $spec): array
    {
        return array_values(array_filter(
            $this->products,
            fn(Product $product) => $spec->isSatisfiedBy($product)
        ));
    }

    /** @return list<Product> */
    public function findAll(): array
    {
        return array_values($this->products);
    }

    public function clear(): void
    {
        $this->products = [];
    }
}
```

## Other Fake Implementations

### Collecting Event Dispatcher

```php
<?php

declare(strict_types=1);

namespace Tests\Fake;

use Psr\EventDispatcher\EventDispatcherInterface;

final class CollectingEventDispatcher implements EventDispatcherInterface
{
    /** @var list<object> */
    private array $events = [];

    public function dispatch(object $event): object
    {
        $this->events[] = $event;
        return $event;
    }

    /** @return list<object> */
    public function dispatchedEvents(): array
    {
        return $this->events;
    }

    /** @return list<object> */
    public function dispatchedEventsOf(string $eventClass): array
    {
        return array_values(array_filter(
            $this->events,
            fn(object $event) => $event instanceof $eventClass
        ));
    }

    public function hasDispatched(string $eventClass): bool
    {
        return count($this->dispatchedEventsOf($eventClass)) > 0;
    }

    public function clear(): void
    {
        $this->events = [];
    }
}
```

### Collecting Mailer

```php
<?php

declare(strict_types=1);

namespace Tests\Fake;

use App\Infrastructure\Email\MailerInterface;
use App\Infrastructure\Email\EmailMessage;

final class InMemoryMailer implements MailerInterface
{
    /** @var list<EmailMessage> */
    private array $sent = [];

    public function send(EmailMessage $message): void
    {
        $this->sent[] = $message;
    }

    /** @return list<EmailMessage> */
    public function sentMessages(): array
    {
        return $this->sent;
    }

    /** @return list<EmailMessage> */
    public function sentTo(string $email): array
    {
        return array_values(array_filter(
            $this->sent,
            fn(EmailMessage $msg) => $msg->to === $email
        ));
    }

    public function hasNotSentAny(): bool
    {
        return empty($this->sent);
    }

    public function clear(): void
    {
        $this->sent = [];
    }
}
```

### Frozen Clock

```php
<?php

declare(strict_types=1);

namespace Tests\Fake;

use Psr\Clock\ClockInterface;
use DateTimeImmutable;

final class FrozenClock implements ClockInterface
{
    public function __construct(
        private DateTimeImmutable $now
    ) {}

    public function now(): DateTimeImmutable
    {
        return $this->now;
    }

    public static function at(string $datetime): self
    {
        return new self(new DateTimeImmutable($datetime));
    }

    public static function now(): self
    {
        return new self(new DateTimeImmutable());
    }

    public function advance(string $interval): self
    {
        return new self($this->now->modify($interval));
    }
}
```

## Usage in Tests

```php
final class PlaceOrderHandlerTest extends TestCase
{
    private PlaceOrderHandler $handler;
    private InMemoryOrderRepository $orderRepository;
    private InMemoryProductRepository $productRepository;
    private CollectingEventDispatcher $eventDispatcher;

    protected function setUp(): void
    {
        $this->orderRepository = new InMemoryOrderRepository();
        $this->productRepository = new InMemoryProductRepository();
        $this->eventDispatcher = new CollectingEventDispatcher();

        $this->handler = new PlaceOrderHandler(
            $this->orderRepository,
            $this->productRepository,
            $this->eventDispatcher
        );
    }

    public function test_places_order(): void
    {
        // Arrange
        $product = ProductMother::book();
        $this->productRepository->save($product);

        // Act
        $orderId = $this->handler->handle(new PlaceOrderCommand(
            customerId: 'customer-123',
            items: [['productId' => $product->id()->toString(), 'quantity' => 2]]
        ));

        // Assert - check repository
        $order = $this->orderRepository->findById(OrderId::fromString($orderId));
        self::assertNotNull($order);

        // Assert - check events
        self::assertTrue($this->eventDispatcher->hasDispatched(OrderPlacedEvent::class));
    }
}
```

## Generation Instructions

1. **Read the repository interface:**
   - Extract all method signatures
   - Identify entity type
   - Identify ID type

2. **Generate InMemory implementation:**
   - Array storage keyed by ID
   - Implement all interface methods
   - Add `clear()` for test cleanup

3. **Handle complex queries:**
   - Use `array_filter` for criteria
   - Support specifications if used
   - Implement pagination with `array_slice`

4. **Add test helpers (optional):**
   - `getAll()` — access internal state
   - `has(Id $id)` — check existence
   - `count()` — entity count

5. **File placement:**
   - `tests/Fake/InMemory{Entity}Repository.php`
   - Or `tests/Double/` directory

## Best Practices

1. **Match interface exactly** — same method signatures
2. **Isolate per test** — use `clear()` in tearDown
3. **Avoid complexity** — simple in-memory logic
4. **Document deviations** — if behavior differs from real impl
5. **Consider thread safety** — for parallel tests (usually not needed)
