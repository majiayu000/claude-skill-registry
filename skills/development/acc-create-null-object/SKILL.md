---
name: acc-create-null-object
description: Generates Null Object pattern for PHP 8.5. Creates safe default implementations eliminating null checks. Includes unit tests.
---

# Null Object Pattern Generator

Creates Null Object pattern infrastructure for eliminating null checks.

## When to Use

| Scenario | Example |
|----------|---------|
| Optional dependencies | Logger, Cache, Notifier |
| Missing entities | Customer, User, Product |
| Feature toggles | Disabled feature returns null object |
| Default implementations | No-op defaults |

## Component Characteristics

### Interface
- Defines expected behavior
- Shared by real and null implementations
- Enables polymorphic usage

### Null Object
- Implements interface with no-op behavior
- Returns neutral values
- Never throws on calls

### Benefits
- Eliminates null checks
- Follows Liskov Substitution
- Simplifies client code

---

## Generation Process

### Step 1: Generate Interface

**Path:** `src/Domain/{BoundedContext}/`

1. `{Name}Interface.php` — Interface with `isNull()` method

### Step 2: Generate Null Object

**Path:** `src/Domain/{BoundedContext}/`

1. `Null{Name}.php` — Null implementation returning neutral values

### Step 3: Generate Real Implementation

**Path:** `src/Domain/{BoundedContext}/`

1. `{Name}.php` — Real implementation with business logic

### Step 4: Generate Tests

1. `Null{Name}Test.php` — Null object behavior tests

---

## File Placement

| Component | Path |
|-----------|------|
| Interface | `src/Domain/{BoundedContext}/` |
| Null Object | `src/Domain/{BoundedContext}/` |
| Real Implementation | `src/Domain/{BoundedContext}/` |
| Unit Tests | `tests/Unit/Domain/{BoundedContext}/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Interface | `{Name}Interface` | `CustomerInterface` |
| Real Implementation | `{Name}` | `Customer` |
| Null Object | `Null{Name}` | `NullCustomer` |
| Test | `{ClassName}Test` | `NullCustomerTest` |

---

## Neutral Return Values

| Type | Neutral Value |
|------|---------------|
| `string` | `''` (empty string) |
| `int` | `0` |
| `float` | `0.0` |
| `bool` | `false` |
| `array` | `[]` |
| `void` | No return |
| Object | Empty/default instance |
| Collection | Empty collection |

---

## Quick Template Reference

### Interface

```php
interface {Name}Interface
{
    public function {method1}(): {returnType1};
    public function {method2}({params}): {returnType2};
    public function isNull(): bool;
}
```

### Null Object

```php
final readonly class Null{Name} implements {Name}Interface
{
    public function {method1}(): {returnType1}
    {
        return {neutralValue1};
    }

    public function isNull(): bool
    {
        return true;
    }
}
```

### Real Implementation

```php
final readonly class {Name} implements {Name}Interface
{
    public function __construct({properties}) {}

    public function {method1}(): {returnType1}
    {
        return {realImplementation};
    }

    public function isNull(): bool
    {
        return false;
    }
}
```

---

## Usage Example

### Repository Returning Null Object

```php
final readonly class DoctrineCustomerRepository implements CustomerRepositoryInterface
{
    public function findById(CustomerId $id): CustomerInterface
    {
        $row = $this->connection->fetchAssociative(
            'SELECT * FROM customers WHERE id = :id',
            ['id' => $id->toString()]
        );

        if ($row === false) {
            return new NullCustomer();
        }

        return $this->hydrate($row);
    }
}
```

### Client Code Without Null Checks

```php
final readonly class CreateOrderUseCase
{
    public function execute(CreateOrderCommand $command): Order
    {
        $customer = $this->customers->findById($command->customerId);

        // No null check needed - NullCustomer returns 0.0
        $discount = $customer->getDiscount();

        $order = Order::create(
            customerId: $customer->id(),
            items: $command->items,
            discount: $discount
        );

        return $order;
    }
}
```

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Throwing in Null | Unexpected exceptions | Return neutral values |
| No `isNull()` | Can't detect null object | Add isNull method |
| Different Interface | LSP violation | Same interface as real |
| Side Effects | Unexpected behavior | Pure no-op methods |
| Complex Logic | Not a null object | Keep simple and neutral |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — Interface, NullObject, Real Implementation, NullLogger, NullCache templates
- `references/examples.md` — NullCustomer, NullNotifier, Repository integration examples and tests
