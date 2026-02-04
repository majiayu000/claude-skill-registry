---
name: acc-check-immutability
description: Analyzes PHP code for immutability violations. Checks Value Objects, Events, DTOs for readonly properties, no setters, final classes, and wither patterns. Ensures domain objects maintain invariants.
---

# Immutability Analyzer

## Overview

This skill analyzes PHP DDD projects for immutability violations in Value Objects, Domain Events, DTOs, and Read Models. Immutability is crucial for maintaining invariants, thread safety, and predictable behavior.

## Immutability Requirements by Type

| Type | Must Be Immutable | Key Checks |
|------|-------------------|------------|
| Value Object | ✅ Required | readonly, no setters, final |
| Domain Event | ✅ Required | readonly, no modification after creation |
| DTO | ✅ Recommended | readonly, no business logic |
| Read Model | ✅ Required | readonly, projection-only changes |
| Entity | ⚠️ Controlled | Setters via behavior methods only |
| Aggregate | ⚠️ Controlled | State changes via domain methods |

## Detection Patterns

### Phase 1: Identify Immutable Candidates

```bash
# Value Objects
Glob: **/ValueObject/**/*.php
Glob: **/Domain/**/*Value.php
Glob: **/Domain/**/*VO.php
Grep: "final.*class.*implements.*ValueObject" --glob "**/*.php"

# Domain Events
Glob: **/Event/**/*Event.php
Glob: **/Domain/**/*Event.php
Grep: "class.*Event\s*\{|final readonly class.*Event" --glob "**/*.php"

# DTOs
Glob: **/DTO/**/*.php
Glob: **/Application/**/*DTO.php
Glob: **/Application/**/*Request.php
Glob: **/Application/**/*Response.php

# Read Models
Glob: **/ReadModel/**/*.php
Glob: **/Projection/**/*.php
Grep: "class.*ReadModel|class.*View|class.*Projection" --glob "**/*.php"
```

### Phase 2: Readonly Class Check

```bash
# PHP 8.2+ readonly classes (best practice)
Grep: "readonly class|final readonly class" --glob "**/*.php"

# Missing readonly keyword
Grep: "final class.*ValueObject|final class.*Event|final class.*DTO" --glob "**/*.php"
# Should be: final readonly class
```

**PHP 8.2+ Recommended Pattern:**
```php
// Good
final readonly class Email
{
    public function __construct(
        public string $value,
    ) {}
}

// Bad (pre-8.2 style)
final class Email
{
    private string $value;

    public function __construct(string $value)
    {
        $this->value = $value;
    }
}
```

### Phase 3: Readonly Properties Check

```bash
# Properties without readonly
Grep: "private string|private int|private float|private bool|private array" --glob "**/ValueObject/**/*.php"
Grep: "private string|private int|private float" --glob "**/Event/**/*.php"

# Expected: private readonly string, or use readonly class

# Public non-readonly properties (critical)
Grep: "public string|public int|public float|public bool" --glob "**/Domain/**/*.php"
# Should be: public readonly or private with getter
```

### Phase 4: Setter Detection

```bash
# Explicit setters in immutable types
Grep: "public function set[A-Z]" --glob "**/ValueObject/**/*.php"
Grep: "public function set[A-Z]" --glob "**/Event/**/*.php"
Grep: "public function set[A-Z]" --glob "**/DTO/**/*.php"

# Property assignment outside constructor
Grep: "\$this->[a-z]+ =" --glob "**/ValueObject/**/*.php"
# Check if inside __construct or not

# ArrayAccess modifications
Grep: "implements.*ArrayAccess" --glob "**/ValueObject/**/*.php"
# offsetSet should throw or return new instance
```

### Phase 5: Final Class Check

```bash
# Non-final Value Objects
Grep: "^class [A-Z].*ValueObject|^abstract class.*ValueObject" --glob "**/ValueObject/**/*.php"
# Should be final

# Non-final Events
Grep: "^class [A-Z].*Event\s*\{" --glob "**/Event/**/*.php"
# Should be final

# Non-final DTOs
Grep: "^class [A-Z].*DTO|^class [A-Z].*Request|^class [A-Z].*Response" --glob "**/DTO/**/*.php"
```

### Phase 6: Wither Pattern Check

```bash
# Methods returning new instances (wither pattern)
Grep: "return new self\(|return new static\(" --glob "**/ValueObject/**/*.php"

# Methods that should use wither but mutate
Grep: "public function with[A-Z]" --glob "**/ValueObject/**/*.php" -A 5
# Check if returns new instance or mutates

# Missing wither methods
Grep: "public function update|public function change|public function modify" --glob "**/ValueObject/**/*.php"
# These should be wither methods returning new instance
```

**Wither Pattern Example:**
```php
// Good (wither pattern)
final readonly class Money
{
    public function __construct(
        public int $amount,
        public Currency $currency,
    ) {}

    public function withAmount(int $amount): self
    {
        return new self($amount, $this->currency);
    }
}

// Bad (mutation)
final class Money
{
    public function setAmount(int $amount): void
    {
        $this->amount = $amount; // Mutation!
    }
}
```

### Phase 7: Collection Immutability

```bash
# Mutable array properties
Grep: "private array" --glob "**/ValueObject/**/*.php"
# Check for array_push, unset, etc.

# Collection modifications
Grep: "array_push|unset\(|\\$this->items\[\]" --glob "**/ValueObject/**/*.php"

# Missing array return by value
Grep: "return \$this->[a-z]+;" --glob "**/ValueObject/**/*.php"
# Arrays should be returned as copies or immutable iterators
```

### Phase 8: DateTimeImmutable Check

```bash
# Using DateTime instead of DateTimeImmutable
Grep: "DateTime[^I]|\\\\DateTime " --glob "**/Domain/**/*.php"
Grep: "new DateTime\(" --glob "**/Domain/**/*.php"

# Expected: DateTimeImmutable
Grep: "DateTimeImmutable" --glob "**/Domain/**/*.php"
```

## Report Format

```markdown
# Immutability Analysis Report

## Summary

| Type | Total | Fully Immutable | Issues |
|------|-------|-----------------|--------|
| Value Objects | 15 | 12 | 3 |
| Domain Events | 8 | 6 | 2 |
| DTOs | 10 | 8 | 2 |
| Read Models | 4 | 4 | 0 |

**Overall Immutability Score: 86%**

## Critical Issues

### IMM-001: Mutable Value Object
- **File:** `src/Domain/Order/ValueObject/Money.php`
- **Issue:** Public setter method found
- **Code:**
  ```php
  public function setAmount(int $amount): void
  {
      $this->amount = $amount;
  }
  ```
- **Expected:** Use wither pattern
  ```php
  public function withAmount(int $amount): self
  {
      return new self($amount, $this->currency);
  }
  ```
- **Skills:** `acc-create-value-object`

### IMM-002: Non-readonly Event
- **File:** `src/Domain/Order/Event/OrderCreatedEvent.php`
- **Issue:** Class not marked as `readonly`, properties mutable
- **Code:**
  ```php
  final class OrderCreatedEvent
  {
      private string $orderId;
  ```
- **Expected:**
  ```php
  final readonly class OrderCreatedEvent
  {
      public function __construct(
          public string $orderId,
  ```
- **Skills:** `acc-create-domain-event`

### IMM-003: DateTime Instead of DateTimeImmutable
- **File:** `src/Domain/User/Entity/User.php:45`
- **Issue:** Using mutable DateTime
- **Code:** `private DateTime $createdAt`
- **Expected:** `private DateTimeImmutable $createdAt`
- **Impact:** Date can be accidentally modified

## Warning Issues

### IMM-004: Non-final Value Object
- **File:** `src/Domain/Shared/ValueObject/Address.php`
- **Issue:** Class not marked as `final`
- **Impact:** Subclasses could break immutability contract

### IMM-005: Array Mutation
- **File:** `src/Domain/Order/ValueObject/OrderItems.php:34`
- **Issue:** Array property modified after construction
- **Code:** `$this->items[] = $item;`
- **Refactoring:** Return new collection instance

### IMM-006: Missing Readonly Properties
- **File:** `src/Application/DTO/CreateOrderDTO.php`
- **Issue:** Properties not readonly
- **Code:**
  ```php
  public string $customerId;
  public array $items;
  ```
- **Expected:**
  ```php
  public readonly string $customerId,
  public readonly array $items,
  ```

## Compliance by Layer

| Layer | Compliance | Notes |
|-------|------------|-------|
| Domain/ValueObject | 80% | 3 VOs need refactoring |
| Domain/Event | 75% | 2 events need readonly |
| Application/DTO | 80% | 2 DTOs need readonly |
| Infrastructure/ReadModel | 100% | All compliant |

## Refactoring Recommendations

### Immediate Actions
1. Add `readonly` keyword to all Value Objects
2. Replace `DateTime` with `DateTimeImmutable`
3. Remove setters from Events and DTOs

### Wither Method Additions
4. Add `withAmount()` to Money
5. Add `withItems()` to OrderItems

### Class Modifiers
6. Add `final` to all Value Objects
7. Consider `readonly class` for PHP 8.2+
```

## Immutability Patterns

### Fully Immutable Class (PHP 8.2+)

```php
final readonly class Email
{
    public function __construct(
        public string $value,
    ) {
        $this->validate($value);
    }

    private function validate(string $value): void
    {
        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidArgumentException('Invalid email');
        }
    }

    public function equals(self $other): bool
    {
        return $this->value === $other->value;
    }
}
```

### Wither Pattern for Modifications

```php
final readonly class Money
{
    public function __construct(
        public int $amount,
        public Currency $currency,
    ) {}

    public function add(self $other): self
    {
        if (!$this->currency->equals($other->currency)) {
            throw new CurrencyMismatchException();
        }
        return new self($this->amount + $other->amount, $this->currency);
    }

    public function withAmount(int $amount): self
    {
        return new self($amount, $this->currency);
    }
}
```

### Immutable Collection

```php
final readonly class OrderItems
{
    /** @param array<OrderItem> $items */
    public function __construct(
        private array $items,
    ) {}

    public function add(OrderItem $item): self
    {
        return new self([...$this->items, $item]);
    }

    public function remove(OrderItem $item): self
    {
        return new self(
            array_filter($this->items, fn($i) => !$i->equals($item))
        );
    }

    /** @return array<OrderItem> */
    public function toArray(): array
    {
        return $this->items;
    }
}
```

## Quick Analysis Commands

```bash
# Check immutability
echo "=== Non-readonly Value Objects ===" && \
grep -rn "final class" --include="*.php" src/Domain/*/ValueObject/ | grep -v "readonly" && \
echo "=== Setters in Immutable Types ===" && \
grep -rn "public function set[A-Z]" --include="*.php" src/Domain/*/ValueObject/ src/Domain/*/Event/ && \
echo "=== Mutable DateTime ===" && \
grep -rn "DateTime[^I]" --include="*.php" src/Domain/ | grep -v "DateTimeImmutable" && \
echo "=== Array Mutations ===" && \
grep -rn "\$this->[a-z]*\[\]" --include="*.php" src/Domain/*/ValueObject/
```

## Integration

Works with:
- `acc-create-value-object` — Generate immutable VOs
- `acc-create-domain-event` — Generate immutable events
- `acc-create-dto` — Generate immutable DTOs
- `acc-structural-auditor` — Architectural compliance
- `acc-behavioral-auditor` — Event Sourcing compliance

## References

- PHP 8.2 readonly classes RFC
- "Domain-Driven Design" (Eric Evans) — Value Objects chapter
- "Implementing DDD" (Vaughn Vernon) — Immutability patterns