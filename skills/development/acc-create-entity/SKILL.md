---
name: acc-create-entity
description: Generates DDD Entities for PHP 8.5. Creates identity-based objects with behavior, state transitions, and invariant protection. Includes unit tests.
---

# Entity Generator

Generate DDD-compliant Entities with identity, behavior, and tests.

## Entity Characteristics

- **Identity**: Has unique identifier (ID)
- **Lifecycle**: Created, modified, potentially deleted
- **Behavior**: Contains domain logic (not just data)
- **Invariants**: Protects business rules
- **State transitions**: Controlled mutations
- **No public setters**: State changed via behavior methods

## Template

```php
<?php

declare(strict_types=1);

namespace Domain\{BoundedContext}\Entity;

use Domain\{BoundedContext}\ValueObject\{Name}Id;
use Domain\{BoundedContext}\Enum\{Name}Status;
use Domain\{BoundedContext}\Exception\{Exceptions};

final class {Name}
{
    private {Name}Status $status;
    private DateTimeImmutable $createdAt;
    private ?DateTimeImmutable $updatedAt = null;

    public function __construct(
        private readonly {Name}Id $id,
        {constructorProperties}
    ) {
        {constructorValidation}
        $this->status = {Name}Status::default();
        $this->createdAt = new DateTimeImmutable();
    }

    public function id(): {Name}Id
    {
        return $this->id;
    }

    public function status(): {Name}Status
    {
        return $this->status;
    }

    {behaviorMethods}

    private function touch(): void
    {
        $this->updatedAt = new DateTimeImmutable();
    }
}
```

## Test Template

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Domain\{BoundedContext}\Entity;

use Domain\{BoundedContext}\Entity\{Name};
use Domain\{BoundedContext}\ValueObject\{Name}Id;
use Domain\{BoundedContext}\Enum\{Name}Status;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\TestCase;

#[Group('unit')]
#[CoversClass({Name}::class)]
final class {Name}Test extends TestCase
{
    public function testCreatesWithValidData(): void
    {
        $entity = $this->createEntity();

        self::assertInstanceOf({Name}Id::class, $entity->id());
        self::assertSame({Name}Status::default(), $entity->status());
    }

    {behaviorTests}

    private function createEntity(): {Name}
    {
        return new {Name}(
            id: {Name}Id::generate(),
            {testConstructorArgs}
        );
    }
}
```

## Common Entity Patterns

### Order Entity

```php
<?php

declare(strict_types=1);

namespace Domain\Order\Entity;

use Domain\Order\ValueObject\OrderId;
use Domain\Order\ValueObject\CustomerId;
use Domain\Order\ValueObject\Money;
use Domain\Order\Enum\OrderStatus;
use Domain\Order\Exception\CannotModifyConfirmedOrderException;
use Domain\Order\Exception\CannotConfirmEmptyOrderException;
use Domain\Order\Exception\InvalidStateTransitionException;

final class Order
{
    private OrderStatus $status;
    /** @var array<OrderLine> */
    private array $lines = [];
    private DateTimeImmutable $createdAt;
    private ?DateTimeImmutable $confirmedAt = null;

    public function __construct(
        private readonly OrderId $id,
        private readonly CustomerId $customerId
    ) {
        $this->status = OrderStatus::Draft;
        $this->createdAt = new DateTimeImmutable();
    }

    public function id(): OrderId
    {
        return $this->id;
    }

    public function customerId(): CustomerId
    {
        return $this->customerId;
    }

    public function status(): OrderStatus
    {
        return $this->status;
    }

    public function addLine(Product $product, int $quantity): void
    {
        if ($this->status !== OrderStatus::Draft) {
            throw new CannotModifyConfirmedOrderException($this->id);
        }

        $this->lines[] = new OrderLine(
            product: $product,
            quantity: $quantity,
            unitPrice: $product->price()
        );
    }

    public function removeLine(int $index): void
    {
        if ($this->status !== OrderStatus::Draft) {
            throw new CannotModifyConfirmedOrderException($this->id);
        }

        if (!isset($this->lines[$index])) {
            return;
        }

        unset($this->lines[$index]);
        $this->lines = array_values($this->lines);
    }

    public function confirm(): void
    {
        if ($this->status !== OrderStatus::Draft) {
            throw new InvalidStateTransitionException(
                $this->status,
                OrderStatus::Confirmed
            );
        }

        if (empty($this->lines)) {
            throw new CannotConfirmEmptyOrderException($this->id);
        }

        $this->status = OrderStatus::Confirmed;
        $this->confirmedAt = new DateTimeImmutable();
    }

    public function cancel(): void
    {
        if (!$this->status->canBeCancelled()) {
            throw new InvalidStateTransitionException(
                $this->status,
                OrderStatus::Cancelled
            );
        }

        $this->status = OrderStatus::Cancelled;
    }

    public function total(): Money
    {
        return array_reduce(
            $this->lines,
            fn (Money $carry, OrderLine $line) => $carry->add($line->total()),
            Money::zero('USD')
        );
    }

    /**
     * @return array<OrderLine>
     */
    public function lines(): array
    {
        return $this->lines;
    }

    public function lineCount(): int
    {
        return count($this->lines);
    }

    public function isEmpty(): bool
    {
        return empty($this->lines);
    }

    public function createdAt(): DateTimeImmutable
    {
        return $this->createdAt;
    }

    public function confirmedAt(): ?DateTimeImmutable
    {
        return $this->confirmedAt;
    }
}
```

### User Entity

```php
<?php

declare(strict_types=1);

namespace Domain\User\Entity;

use Domain\User\ValueObject\UserId;
use Domain\User\ValueObject\Email;
use Domain\User\ValueObject\HashedPassword;
use Domain\User\Enum\UserStatus;
use Domain\User\Exception\UserAlreadyActivatedException;
use Domain\User\Exception\UserDeactivatedException;

final class User
{
    private UserStatus $status;
    private DateTimeImmutable $createdAt;
    private ?DateTimeImmutable $lastLoginAt = null;

    public function __construct(
        private readonly UserId $id,
        private Email $email,
        private HashedPassword $password,
        private string $name
    ) {
        if (empty(trim($name))) {
            throw new InvalidUserNameException();
        }

        $this->status = UserStatus::Pending;
        $this->createdAt = new DateTimeImmutable();
    }

    public function id(): UserId
    {
        return $this->id;
    }

    public function email(): Email
    {
        return $this->email;
    }

    public function name(): string
    {
        return $this->name;
    }

    public function status(): UserStatus
    {
        return $this->status;
    }

    public function activate(): void
    {
        if ($this->status === UserStatus::Active) {
            throw new UserAlreadyActivatedException($this->id);
        }

        $this->status = UserStatus::Active;
    }

    public function deactivate(): void
    {
        $this->status = UserStatus::Deactivated;
    }

    public function changeEmail(Email $newEmail): void
    {
        $this->ensureActive();
        $this->email = $newEmail;
    }

    public function changePassword(HashedPassword $newPassword): void
    {
        $this->ensureActive();
        $this->password = $newPassword;
    }

    public function changeName(string $newName): void
    {
        $this->ensureActive();

        if (empty(trim($newName))) {
            throw new InvalidUserNameException();
        }

        $this->name = $newName;
    }

    public function recordLogin(): void
    {
        $this->ensureActive();
        $this->lastLoginAt = new DateTimeImmutable();
    }

    public function verifyPassword(string $plainPassword, PasswordHasherInterface $hasher): bool
    {
        return $hasher->verify($this->password, $plainPassword);
    }

    public function isActive(): bool
    {
        return $this->status === UserStatus::Active;
    }

    private function ensureActive(): void
    {
        if ($this->status === UserStatus::Deactivated) {
            throw new UserDeactivatedException($this->id);
        }
    }
}
```

## Entity Design Principles

### 1. Behavior Over Data

```php
// BAD: Anemic entity
class Order
{
    public function setStatus(string $status): void
    {
        $this->status = $status;
    }
}

// GOOD: Rich entity with behavior
class Order
{
    public function confirm(): void
    {
        if (!$this->canBeConfirmed()) {
            throw new InvalidStateTransitionException();
        }
        $this->status = OrderStatus::Confirmed;
        $this->confirmedAt = new DateTimeImmutable();
    }

    private function canBeConfirmed(): bool
    {
        return $this->status === OrderStatus::Draft && !empty($this->lines);
    }
}
```

### 2. Invariant Protection

```php
// Protect invariants in every method
public function addLine(Product $product, int $quantity): void
{
    // Invariant: Can only modify draft orders
    if ($this->status !== OrderStatus::Draft) {
        throw new CannotModifyConfirmedOrderException();
    }

    // Invariant: Quantity must be positive
    if ($quantity <= 0) {
        throw new InvalidQuantityException();
    }

    $this->lines[] = new OrderLine($product, $quantity);
}
```

### 3. State Transitions

```php
enum OrderStatus: string
{
    case Draft = 'draft';
    case Confirmed = 'confirmed';
    case Paid = 'paid';
    case Shipped = 'shipped';
    case Cancelled = 'cancelled';

    public function canTransitionTo(self $target): bool
    {
        return match($this) {
            self::Draft => in_array($target, [self::Confirmed, self::Cancelled]),
            self::Confirmed => in_array($target, [self::Paid, self::Cancelled]),
            self::Paid => in_array($target, [self::Shipped, self::Cancelled]),
            self::Shipped => false,
            self::Cancelled => false,
        };
    }

    public function canBeCancelled(): bool
    {
        return $this->canTransitionTo(self::Cancelled);
    }
}
```

## Generation Instructions

When asked to create an Entity:

1. **Identify the identity** (what makes it unique)
2. **Define the lifecycle** (statuses/states)
3. **List invariants** (business rules to protect)
4. **Design behavior methods** (what it can do)
5. **Generate tests** for behavior and invariants

## Naming Conventions

| Concept | Method Pattern | Exception |
|---------|----------------|-----------|
| State change | `confirm()`, `activate()`, `cancel()` | `InvalidStateTransitionException` |
| Add relation | `addLine()`, `addItem()` | `CannotModifyException` |
| Update property | `changeEmail()`, `updateName()` | `InvalidValueException` |
| Query state | `isActive()`, `canBeConfirmed()` | N/A (boolean return) |

## Usage

To generate an Entity, provide:
- Name (e.g., "Order", "User")
- Bounded Context (e.g., "Order", "User")
- Identity type (e.g., "OrderId")
- States/Statuses
- Key behaviors needed
- Invariants to protect
