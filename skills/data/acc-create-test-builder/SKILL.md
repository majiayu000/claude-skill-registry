---
name: acc-create-test-builder
description: Generates Test Data Builder and Object Mother patterns for PHP 8.5. Creates fluent builders with sensible defaults and factory methods for test data creation.
---

# Test Data Builder Generator

Generates Test Data Builder and Object Mother patterns for test data creation.

## Patterns

### Test Data Builder

Fluent interface for constructing test objects with customizable properties.

**When to use:**
- Complex objects with many properties
- Need to customize specific properties per test
- Want to express test intent clearly

### Object Mother

Factory methods returning pre-configured objects for common scenarios.

**When to use:**
- Standard test fixtures (default user, pending order)
- Shared across many tests
- Named scenarios (premium customer, expired subscription)

## Builder Template

```php
<?php

declare(strict_types=1);

namespace Tests\Builder;

use {FullyQualifiedClassName};

final class {ClassName}Builder
{
    private {IdType} $id;
    private {Property1Type} ${property1};
    private {Property2Type} ${property2};
    // ... other properties

    private function __construct()
    {
        // Sensible defaults
        $this->id = {IdType}::generate();
        $this->{property1} = {default1};
        $this->{property2} = {default2};
    }

    public static function a{ClassName}(): self
    {
        return new self();
    }

    public static function an{ClassName}(): self
    {
        return new self();
    }

    public function withId({IdType} $id): self
    {
        $clone = clone $this;
        $clone->id = $id;
        return $clone;
    }

    public function with{Property1}({Property1Type} ${property1}): self
    {
        $clone = clone $this;
        $clone->{property1} = ${property1};
        return $clone;
    }

    public function with{Property2}({Property2Type} ${property2}): self
    {
        $clone = clone $this;
        $clone->{property2} = ${property2};
        return $clone;
    }

    public function build(): {ClassName}
    {
        return new {ClassName}(
            $this->id,
            $this->{property1},
            $this->{property2}
        );
    }
}
```

## Object Mother Template

```php
<?php

declare(strict_types=1);

namespace Tests\Mother;

use {FullyQualifiedClassName};

final class {ClassName}Mother
{
    public static function default(): {ClassName}
    {
        return {ClassName}Builder::a{ClassName}()->build();
    }

    public static function {scenario1}(): {ClassName}
    {
        return {ClassName}Builder::a{ClassName}()
            ->with{Property}({value})
            ->build();
    }

    public static function {scenario2}(): {ClassName}
    {
        return {ClassName}Builder::a{ClassName}()
            ->with{Property1}({value1})
            ->with{Property2}({value2})
            ->build();
    }
}
```

## Complete Example: Order

### OrderBuilder

```php
<?php

declare(strict_types=1);

namespace Tests\Builder;

use App\Domain\Order\Order;
use App\Domain\Order\OrderId;
use App\Domain\Order\OrderItem;
use App\Domain\Order\OrderStatus;
use App\Domain\Customer\CustomerId;
use App\Domain\Shared\Money;
use DateTimeImmutable;

final class OrderBuilder
{
    private OrderId $id;
    private CustomerId $customerId;
    /** @var list<OrderItem> */
    private array $items = [];
    private OrderStatus $status;
    private DateTimeImmutable $createdAt;

    private function __construct()
    {
        $this->id = OrderId::generate();
        $this->customerId = CustomerId::generate();
        $this->status = OrderStatus::Pending;
        $this->createdAt = new DateTimeImmutable();
    }

    public static function anOrder(): self
    {
        return new self();
    }

    public function withId(OrderId $id): self
    {
        $clone = clone $this;
        $clone->id = $id;
        return $clone;
    }

    public function forCustomer(CustomerId $customerId): self
    {
        $clone = clone $this;
        $clone->customerId = $customerId;
        return $clone;
    }

    public function withItem(Product $product, int $quantity = 1): self
    {
        $clone = clone $this;
        $clone->items[] = new OrderItem($product, $quantity);
        return $clone;
    }

    public function withItems(array $items): self
    {
        $clone = clone $this;
        $clone->items = $items;
        return $clone;
    }

    public function withTotal(Money $total): self
    {
        $clone = clone $this;
        $clone->items = [
            new OrderItem(ProductMother::withPrice($total), 1),
        ];
        return $clone;
    }

    public function pending(): self
    {
        $clone = clone $this;
        $clone->status = OrderStatus::Pending;
        return $clone;
    }

    public function confirmed(): self
    {
        $clone = clone $this;
        $clone->status = OrderStatus::Confirmed;
        // Add item if empty (can't confirm empty order)
        if (empty($clone->items)) {
            $clone->items[] = new OrderItem(ProductMother::book(), 1);
        }
        return $clone;
    }

    public function shipped(): self
    {
        $clone = clone $this;
        $clone->status = OrderStatus::Shipped;
        if (empty($clone->items)) {
            $clone->items[] = new OrderItem(ProductMother::book(), 1);
        }
        return $clone;
    }

    public function cancelled(): self
    {
        $clone = clone $this;
        $clone->status = OrderStatus::Cancelled;
        return $clone;
    }

    public function createdAt(DateTimeImmutable $createdAt): self
    {
        $clone = clone $this;
        $clone->createdAt = $createdAt;
        return $clone;
    }

    public function createdDaysAgo(int $days): self
    {
        return $this->createdAt(
            new DateTimeImmutable("-{$days} days")
        );
    }

    public function build(): Order
    {
        $order = new Order($this->id, $this->customerId, $this->createdAt);

        foreach ($this->items as $item) {
            $order->addItem($item->product(), $item->quantity());
        }

        // Apply status transitions
        if ($this->status === OrderStatus::Confirmed) {
            $order->confirm();
        } elseif ($this->status === OrderStatus::Shipped) {
            $order->confirm();
            $order->ship();
        } elseif ($this->status === OrderStatus::Cancelled) {
            $order->cancel();
        }

        return $order;
    }
}
```

### OrderMother

```php
<?php

declare(strict_types=1);

namespace Tests\Mother;

use App\Domain\Order\Order;
use App\Domain\Customer\CustomerId;
use App\Domain\Shared\Money;
use Tests\Builder\OrderBuilder;

final class OrderMother
{
    public static function pending(): Order
    {
        return OrderBuilder::anOrder()->pending()->build();
    }

    public static function confirmed(): Order
    {
        return OrderBuilder::anOrder()->confirmed()->build();
    }

    public static function shipped(): Order
    {
        return OrderBuilder::anOrder()->shipped()->build();
    }

    public static function cancelled(): Order
    {
        return OrderBuilder::anOrder()->cancelled()->build();
    }

    public static function forCustomer(CustomerId $customerId): Order
    {
        return OrderBuilder::anOrder()
            ->forCustomer($customerId)
            ->build();
    }

    public static function withTotal(Money $total): Order
    {
        return OrderBuilder::anOrder()
            ->withTotal($total)
            ->build();
    }

    public static function empty(): Order
    {
        return OrderBuilder::anOrder()->build();
    }

    public static function withItems(array $items): Order
    {
        return OrderBuilder::anOrder()
            ->withItems($items)
            ->build();
    }

    public static function expired(): Order
    {
        return OrderBuilder::anOrder()
            ->pending()
            ->createdDaysAgo(31)
            ->build();
    }
}
```

## Value Object Builders

```php
<?php

declare(strict_types=1);

namespace Tests\Builder;

use App\Domain\Shared\Money;

final class MoneyBuilder
{
    private int $amount;
    private string $currency;

    private function __construct()
    {
        $this->amount = 1000;
        $this->currency = 'EUR';
    }

    public static function money(): self
    {
        return new self();
    }

    public function withAmount(int $amount): self
    {
        $clone = clone $this;
        $clone->amount = $amount;
        return $clone;
    }

    public function inEUR(): self
    {
        $clone = clone $this;
        $clone->currency = 'EUR';
        return $clone;
    }

    public function inUSD(): self
    {
        $clone = clone $this;
        $clone->currency = 'USD';
        return $clone;
    }

    public function zero(): self
    {
        return $this->withAmount(0);
    }

    public function build(): Money
    {
        return new Money($this->amount, $this->currency);
    }
}

final class MoneyMother
{
    public static function eur(int $amount): Money
    {
        return Money::EUR($amount);
    }

    public static function usd(int $amount): Money
    {
        return Money::USD($amount);
    }

    public static function zero(): Money
    {
        return Money::EUR(0);
    }

    public static function oneHundred(): Money
    {
        return Money::EUR(10000); // cents
    }
}
```

## Usage in Tests

```php
// Builder - custom configuration
$order = OrderBuilder::anOrder()
    ->forCustomer($customerId)
    ->withItem($book, 2)
    ->withItem($pen, 5)
    ->confirmed()
    ->createdDaysAgo(7)
    ->build();

// Mother - common scenarios
$pendingOrder = OrderMother::pending();
$confirmedOrder = OrderMother::confirmed();
$expiredOrder = OrderMother::expired();
$customerOrder = OrderMother::forCustomer($customerId);
```

## Generation Instructions

1. **Analyze the target class:**
   - Constructor parameters
   - Required vs optional properties
   - Value objects used
   - State transitions (for entities)

2. **Determine sensible defaults:**
   - Generate IDs automatically
   - Use common/valid values
   - Consider relationships

3. **Create Builder with:**
   - Private constructor with defaults
   - Static factory method (`aOrder`, `anEmail`)
   - `with*` methods for each property
   - Immutable (clone in each method)
   - `build()` method

4. **Create Mother with:**
   - `default()` method
   - Named scenarios (`pending`, `confirmed`, `premium`)
   - Parameterized methods (`forCustomer`, `withTotal`)

5. **File placement:**
   - Builders: `tests/Builder/{ClassName}Builder.php`
   - Mothers: `tests/Mother/{ClassName}Mother.php`

## Best Practices

1. **Sensible defaults** — Tests should work without customization
2. **Fluent interface** — Chain method calls
3. **Immutable builders** — Clone in each `with*` method
4. **Expressive names** — `pending()` not `withStatus(pending)`
5. **Composition** — Builders can use other Mothers/Builders
6. **Single Responsibility** — One builder per aggregate/entity
