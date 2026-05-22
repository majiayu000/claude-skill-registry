---
name: acc-create-factory
description: Generates DDD Factory for PHP 8.5. Creates factories for complex domain object instantiation with validation and encapsulated creation logic. Includes unit tests.
---

# Factory Generator

Generate DDD-compliant Factories for complex domain object creation.

## Factory Characteristics

- **Encapsulates Creation**: Hides complex instantiation logic
- **Validates Input**: Ensures valid object creation
- **Named Constructors**: Provides semantic creation methods
- **Domain Layer**: Lives in Domain, no infrastructure dependencies
- **Returns Valid Objects**: Never creates invalid domain objects
- **Static or Instance**: Static for simple, instance for dependencies

## When to Use Factory

| Scenario | Example |
|----------|---------|
| Complex construction logic | `OrderFactory::createFromCart()` |
| Multiple creation paths | `User::register()`, `User::createAdmin()` |
| Aggregate creation | `PolicyFactory::createWithCoverage()` |
| Reconstruction from persistence | `OrderFactory::reconstitute()` |
| Creation with validation | `InvoiceFactory::create()` |

---

## Generation Process

### Step 1: Determine Factory Type

- **Static Factory**: No dependencies, simple validation
- **Instance Factory**: Needs domain services or repositories

### Step 2: Generate Factory

**Path:** `src/Domain/{BoundedContext}/Factory/`

1. `{Entity}Factory.php` — Main factory class

### Step 3: Define Creation Methods

1. `create()` — Primary creation with validation
2. `createFrom{Source}()` — Creation from other objects
3. `reconstitute()` — Reconstruction from persistence (no validation)

### Step 4: Generate Tests

**Path:** `tests/Unit/Domain/{BoundedContext}/Factory/`

---

## File Placement

| Component | Path |
|-----------|------|
| Factory | `src/Domain/{BoundedContext}/Factory/` |
| Unit Tests | `tests/Unit/Domain/{BoundedContext}/Factory/` |

---

## Naming Conventions

| Pattern | Example |
|---------|---------|
| Factory Class | `{EntityName}Factory` |
| Create Method | `create()`, `createFrom{Source}()` |
| Named Constructor | `create{Variant}()` |
| Reconstitute | `reconstitute()` |
| Validation | `validate{Aspect}()` |

---

## Quick Template Reference

### Static Factory

```php
final class {Entity}Factory
{
    public static function create({parameters}): {Entity}
    {
        self::validate({parameters});
        return new {Entity}({constructorArgs});
    }

    public static function createFrom{Source}({SourceType} $source): {Entity}
    {
        return new {Entity}({mappedArgs});
    }

    public static function reconstitute({allFields}): {Entity}
    {
        return new {Entity}({allArgs});
    }

    private static function validate({parameters}): void
    {
        {validationLogic}
    }
}
```

### Instance Factory

```php
final readonly class {Entity}Factory
{
    public function __construct(
        private {DomainService} $service,
        private {Repository} $repository
    ) {}

    public function create({parameters}): {Entity}
    {
        {creationLogicWithDependencies}
    }
}
```

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Infrastructure in Factory | DB calls in factory | Keep pure domain logic |
| No Validation | Creates invalid objects | Validate before creation |
| Too Many Parameters | Hard to use | Use Value Objects, Builder |
| Mutable Factory | Stateful creation | Make stateless or readonly |
| Missing Reconstitute | Can't hydrate from DB | Add reconstitute method |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — Static Factory, Instance Factory, Test templates
- `references/examples.md` — Order, User, Policy factory examples and tests
