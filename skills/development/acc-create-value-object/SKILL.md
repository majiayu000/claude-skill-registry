---
name: acc-create-value-object
description: Generates DDD Value Objects for PHP 8.5. Creates immutable, self-validating objects with equality comparison. Includes unit tests.
---

# Value Object Generator

Generate DDD-compliant Value Objects with validation, equality, and tests.

## Value Object Characteristics

- **Immutable**: `final readonly class`
- **Self-validating**: Validates in constructor
- **Equality by value**: `equals()` method compares values
- **No identity**: No ID, compared by content
- **Encapsulates concept**: Represents domain concept

## Template

```php
<?php

declare(strict_types=1);

namespace Domain\{BoundedContext}\ValueObject;

use Domain\{BoundedContext}\Exception\Invalid{Name}Exception;

final readonly class {Name}
{
    public function __construct(
        public {type} $value
    ) {
        {validation}
    }

    public function equals(self $other): bool
    {
        return $this->value === $other->value;
    }

    public function __toString(): string
    {
        return (string) $this->value;
    }
}
```

## Test Template

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Domain\{BoundedContext}\ValueObject;

use Domain\{BoundedContext}\ValueObject\{Name};
use Domain\{BoundedContext}\Exception\Invalid{Name}Exception;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\TestCase;

#[Group('unit')]
#[CoversClass({Name}::class)]
final class {Name}Test extends TestCase
{
    public function testCreatesWithValidValue(): void
    {
        $vo = new {Name}({validValue});

        self::assertSame({validValue}, $vo->value);
    }

    public function testThrowsExceptionForInvalidValue(): void
    {
        $this->expectException(Invalid{Name}Exception::class);

        new {Name}({invalidValue});
    }

    public function testEquality(): void
    {
        $vo1 = new {Name}({validValue});
        $vo2 = new {Name}({validValue});
        $vo3 = new {Name}({differentValue});

        self::assertTrue($vo1->equals($vo2));
        self::assertFalse($vo1->equals($vo3));
    }

    public function testToString(): void
    {
        $vo = new {Name}({validValue});

        self::assertSame({expectedString}, (string) $vo);
    }
}
```

## Common Value Objects

### Email

```php
final readonly class Email
{
    public function __construct(
        public string $value
    ) {
        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidEmailException($value);
        }
    }

    public function equals(self $other): bool
    {
        return strtolower($this->value) === strtolower($other->value);
    }

    public function domain(): string
    {
        return substr($this->value, strpos($this->value, '@') + 1);
    }

    public function __toString(): string
    {
        return $this->value;
    }
}
```

### Money

```php
final readonly class Money
{
    public function __construct(
        public int $cents,
        public string $currency
    ) {
        if ($cents < 0) {
            throw new InvalidMoneyException('Amount cannot be negative');
        }
        if (strlen($currency) !== 3) {
            throw new InvalidMoneyException('Currency must be 3 characters');
        }
    }

    public static function zero(string $currency): self
    {
        return new self(0, $currency);
    }

    public static function fromFloat(float $amount, string $currency): self
    {
        return new self((int) round($amount * 100), $currency);
    }

    public function add(self $other): self
    {
        $this->assertSameCurrency($other);
        return new self($this->cents + $other->cents, $this->currency);
    }

    public function subtract(self $other): self
    {
        $this->assertSameCurrency($other);
        return new self($this->cents - $other->cents, $this->currency);
    }

    public function multiply(int $factor): self
    {
        return new self($this->cents * $factor, $this->currency);
    }

    public function isGreaterThan(self $other): bool
    {
        $this->assertSameCurrency($other);
        return $this->cents > $other->cents;
    }

    public function isZero(): bool
    {
        return $this->cents === 0;
    }

    public function isPositive(): bool
    {
        return $this->cents > 0;
    }

    public function equals(self $other): bool
    {
        return $this->cents === $other->cents && $this->currency === $other->currency;
    }

    public function format(): string
    {
        return number_format($this->cents / 100, 2) . ' ' . $this->currency;
    }

    private function assertSameCurrency(self $other): void
    {
        if ($this->currency !== $other->currency) {
            throw new CurrencyMismatchException($this->currency, $other->currency);
        }
    }
}
```

### UUID-based ID

```php
final readonly class OrderId
{
    public function __construct(
        public string $value
    ) {
        if (!preg_match('/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i', $value)) {
            throw new InvalidOrderIdException($value);
        }
    }

    public static function generate(): self
    {
        return new self(self::uuid4());
    }

    public function equals(self $other): bool
    {
        return $this->value === $other->value;
    }

    public function __toString(): string
    {
        return $this->value;
    }

    private static function uuid4(): string
    {
        $data = random_bytes(16);
        $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
        $data[8] = chr(ord($data[8]) & 0x3f | 0x80);

        return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
    }
}
```

### Address (Composite)

```php
final readonly class Address
{
    public function __construct(
        public string $street,
        public string $city,
        public string $postalCode,
        public string $country
    ) {
        if (empty(trim($street))) {
            throw new InvalidAddressException('Street cannot be empty');
        }
        if (empty(trim($city))) {
            throw new InvalidAddressException('City cannot be empty');
        }
        if (strlen($country) !== 2) {
            throw new InvalidAddressException('Country must be ISO 3166-1 alpha-2');
        }
    }

    public function equals(self $other): bool
    {
        return $this->street === $other->street
            && $this->city === $other->city
            && $this->postalCode === $other->postalCode
            && $this->country === $other->country;
    }

    public function format(): string
    {
        return "{$this->street}\n{$this->postalCode} {$this->city}\n{$this->country}";
    }
}
```

### DateRange

```php
final readonly class DateRange
{
    public function __construct(
        public DateTimeImmutable $start,
        public DateTimeImmutable $end
    ) {
        if ($end < $start) {
            throw new InvalidDateRangeException('End date must be after start date');
        }
    }

    public function contains(DateTimeImmutable $date): bool
    {
        return $date >= $this->start && $date <= $this->end;
    }

    public function overlaps(self $other): bool
    {
        return $this->start <= $other->end && $this->end >= $other->start;
    }

    public function days(): int
    {
        return (int) $this->start->diff($this->end)->days;
    }

    public function equals(self $other): bool
    {
        return $this->start == $other->start && $this->end == $other->end;
    }
}
```

## Generation Instructions

When asked to create a Value Object:

1. **Identify the concept** being modeled
2. **Determine validation rules** from domain requirements
3. **Choose appropriate type** (string, int, composite)
4. **Add domain-specific methods** if needed
5. **Generate corresponding test** with valid/invalid cases

## Naming Conventions

| Concept | Class Name | Exception |
|---------|------------|-----------|
| Email address | `Email` | `InvalidEmailException` |
| Money amount | `Money` | `InvalidMoneyException` |
| Order identifier | `OrderId` | `InvalidOrderIdException` |
| Physical address | `Address` | `InvalidAddressException` |
| Phone number | `Phone` | `InvalidPhoneException` |
| Date range | `DateRange` | `InvalidDateRangeException` |

## Usage

To generate a Value Object, provide:
- Name (e.g., "Email", "CustomerId")
- Bounded Context (e.g., "Order", "Customer")
- Validation rules
- Any special methods needed
