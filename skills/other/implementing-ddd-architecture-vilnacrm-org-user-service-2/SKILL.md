---
name: implementing-ddd-architecture
description: Design and implement DDD patterns (entities, value objects, aggregates, CQRS). Use when creating new domain objects, implementing bounded contexts, designing repository interfaces, or learning proper layer separation. For fixing existing Deptrac violations, use the deptrac-fixer skill instead.
---

# Implementing DDD Architecture

## Context (Input)

- Creating new entities, value objects, or aggregates
- Implementing bounded contexts or modules
- Designing repository interfaces and implementations
- Learning proper layer separation (Domain/Application/Infrastructure)
- Need to understand CQRS pattern (Commands, Handlers, Events)
- Code review for architectural compliance

## Task (Function)

Design and implement rich domain models following DDD, hexagonal architecture, and CQRS patterns.

**Success Criteria**:

- Domain entities remain framework-agnostic (no framework imports)
- Business logic in Domain layer, not in Application handlers
- `make deptrac` shows zero violations
- Repository interfaces in Domain, implementations in Infrastructure

---

## Core Principle

**Rich Domain Models, Not Anemic**

Business logic belongs in the Domain layer. Application layer orchestrates, Domain executes.

---

## Layer Dependency Rules

```
Domain ─────────────────> (NO dependencies - pure PHP)
           │
           │
Application ──────────> Domain + Infrastructure
           │
           │
Infrastructure ───────> Domain + Application
```

**Allowed Dependencies**:

| Layer              | Can Import                                                 |
| ------------------ | ---------------------------------------------------------- |
| **Domain**         | ❌ Nothing (pure PHP, SPL, domain-specific libraries only) |
| **Application**    | ✅ Domain, Infrastructure, Symfony, API Platform           |
| **Infrastructure** | ✅ Domain, Application, Symfony, Doctrine ORM              |

> Template examples may show Doctrine ODM/MongoDB constructs. In this service, use Doctrine ORM with MySQL (`EntityManagerInterface`, `.orm.xml` mappings).

**See**: [DIRECTORY-STRUCTURE.md](DIRECTORY-STRUCTURE.md) for complete file placement guide.

---

## Critical Rules

### 1. Domain Layer Purity

❌ **FORBIDDEN in Domain**:

- Symfony components (`use Symfony\...`)
- Doctrine annotations/attributes
- API Platform attributes
- Any framework-specific code

✅ **ALLOWED in Domain**:

- Pure PHP
- SPL (Standard PHP Library)
- Domain-specific value objects
- Domain interfaces

### 2. Rich Domain Models

❌ **BAD (Anemic)**:

```php
class Customer {
    public function setName(string $name): void {
        $this->name = $name;  // No validation!
    }
}
```

✅ **GOOD (Rich)**:

```php
class Customer {
    public function changeName(CustomerName $name): void {
        // Business rules enforced
        $this->record(new CustomerNameChanged($this->id, $name));
        $this->name = $name;
    }
}
```

### 3. Validation Pattern

❌ **BAD**: Validation in Domain with Symfony

```php
use Symfony\Component\Validator\Constraints as Assert;

class Customer {
    #[Assert\NotBlank]  // ❌ Framework in Domain!
    private string $name;
}
```

✅ **GOOD**: Validation in YAML config (Preferred)

```yaml
# config/validator/Customer.yaml
App\Application\DTO\CustomerCreate:
  properties:
    name:
      - NotBlank: ~
      - Length:
          min: 2
          max: 100
```

**Framework validators should always be used when possible.** They provide:

- Centralized configuration
- Easy maintenance
- Standard error messages
- Built-in constraints (NotBlank, Email, Length, etc.)
- Custom validators for business rules

**Value Objects** should only be used when:

- Framework validators cannot express the business rule
- Complex domain logic requires encapsulation
- The validation is part of domain invariants

**See**: [REFERENCE.md](REFERENCE.md) for complete validation patterns.

---

## CQRS Pattern Quick Start

### Commands (Write Operations)

```php
// src/Core/{Context}/Application/Command/{Action}{Entity}Command.php
final readonly class CreateCustomerCommand implements CommandInterface
{
    public function __construct(
        public string $id,
        public string $name,
        public string $email
    ) {}
}
```

### Command Handlers

```php
// src/Core/{Context}/Application/CommandHandler/{Action}{Entity}CommandHandler.php
final readonly class CreateCustomerCommandHandler implements CommandHandlerInterface
{
    public function __invoke(CreateCustomerCommand $command): Customer
    {
        // Minimal orchestration only
        $customer = Customer::create(
            Ulid::fromString($command->id),
            new CustomerName($command->name),
            new Email($command->email)
        );

        $this->repository->save($customer);
        $this->eventBus->publish(...$customer->pullDomainEvents());

        return $customer;
    }
}
```

**See**: [REFERENCE.md](REFERENCE.md) for complete CQRS patterns.

---

## Repository Pattern

### Interface (Domain Layer)

```php
// src/Core/{Context}/Domain/Repository/{Entity}RepositoryInterface.php
interface CustomerRepositoryInterface
{
    public function save(Customer $customer): void;
    public function findById(string $id): ?Customer;
}
```

### Implementation (Infrastructure Layer)

```php
// src/Core/{Context}/Infrastructure/Repository/{Entity}Repository.php
final class CustomerRepository implements CustomerRepositoryInterface
{
    public function __construct(
        private readonly DocumentManager $documentManager
    ) {}

    public function save(Customer $customer): void
    {
        $this->documentManager->persist($customer);
        $this->documentManager->flush();
    }
}
```

**Register in `config/services.yaml`**:

```yaml
App\Core\Customer\Domain\Repository\CustomerRepositoryInterface:
  alias: App\Core\Customer\Infrastructure\Repository\CustomerRepository
```

---

## Domain Events Pattern

### Recording Events in Aggregates

```php
class Customer extends AggregateRoot  // Provides event recording
{
    public function changeName(CustomerName $name): void
    {
        $this->name = $name;
        $this->record(new CustomerNameChanged($this->id, $name));
    }
}
```

### Event Subscribers

```php
// src/Core/{Context}/Application/EventSubscriber/{Event}Subscriber.php
final readonly class CustomerNameChangedSubscriber implements DomainEventSubscriberInterface
{
    public function __invoke(CustomerNameChanged $event): void
    {
        // React to event (e.g., send notification)
    }
}
```

**See**: [REFERENCE.md](REFERENCE.md) for complete event-driven patterns.

---

## Quick Start Workflows

### Creating a New Entity

1. **Create Entity** in `Domain/Entity/`
2. **Create Value Objects** in `Domain/ValueObject/`
3. **Create Repository Interface** in `Domain/Repository/`
4. **Create Repository Implementation** in `Infrastructure/Repository/`
5. **Create Commands** in `Application/Command/`
6. **Create Handlers** in `Application/CommandHandler/`
7. **Verify**: `make deptrac` shows zero violations

**See**: [examples/](examples/) for complete working examples.

### Fixing Deptrac Violations

**If** `make deptrac` shows violations:

**Use**: [deptrac-fixer](../deptrac-fixer/SKILL.md) skill for step-by-step fix patterns.

---

## Constraints (Parameters)

### NEVER

- Add framework imports to Domain layer
- Put business logic in Application handlers
- Create anemic domain models (getters/setters only)
- Modify `deptrac.yaml` to allow violations
- Skip validation (either in Value Objects or YAML config)
- Use public setters in entities

### ALWAYS

- Keep Domain layer pure (no framework dependencies)
- Put business logic in Domain entities/aggregates
- Use Value Objects for validation and invariants
- Create repository interfaces in Domain layer
- Implement repositories in Infrastructure layer
- Use Command Bus for write operations
- Record Domain Events for state changes
- Verify with `make deptrac` after changes

---

## Format (Output)

### Expected Directory Structure

```
src/Core/{Context}/
├── Domain/
│   ├── Entity/
│   │   └── {Entity}.php          # Pure PHP, no attributes
│   ├── ValueObject/
│   │   └── {ValueObject}.php     # Validation logic here
│   ├── Repository/
│   │   └── {Entity}RepositoryInterface.php
│   ├── Event/
│   │   └── {Event}.php
│   └── Exception/
│       └── {Exception}.php
├── Application/
│   ├── Command/
│   │   └── {Action}{Entity}Command.php
│   ├── CommandHandler/
│   │   └── {Action}{Entity}CommandHandler.php
│   └── EventSubscriber/
│       └── {Event}Subscriber.php
└── Infrastructure/
    └── Repository/
        └── {Entity}Repository.php
```

### Expected Deptrac Output

```
✅ No violations found
```

---

## Verification Checklist

After implementing DDD patterns:

- [ ] Domain entities have no framework imports
- [ ] Business logic in Domain layer, not Application
- [ ] Value Objects used for validation and invariants
- [ ] Repository interfaces in Domain layer
- [ ] Repository implementations in Infrastructure layer
- [ ] Commands implement `CommandInterface`
- [ ] Handlers implement `CommandHandlerInterface`
- [ ] Domain Events recorded in aggregates
- [ ] Event Subscribers implement `DomainEventSubscriberInterface`
- [ ] `make deptrac` shows zero violations
- [ ] All tests pass
- [ ] `make ci` passes

---

## Related Skills

- [deptrac-fixer](../deptrac-fixer/SKILL.md) - Fix architectural violations
- [api-platform-crud](../api-platform-crud/SKILL.md) - YAML-based API Platform with DDD
- [database-migrations](../database-migrations/SKILL.md) - XML-based Doctrine mappings
- [complexity-management](../complexity-management/SKILL.md) - Keep domain logic maintainable

---

## Reference Documentation

For detailed patterns, workflows, and examples:

- **[REFERENCE.md](REFERENCE.md)** - Complete DDD workflows and patterns
- **[DIRECTORY-STRUCTURE.md](DIRECTORY-STRUCTURE.md)** - File placement guide (CodelyTV style)
- **[examples/](examples/)** - Complete working examples:
  - Entity examples
  - Value Object examples
  - CQRS examples
  - Event-driven examples

---

## Anti-Patterns to Avoid

### ❌ Business Logic in Handlers

```php
// ❌ BAD: Logic in handler
class CreateCustomerHandler {
    public function __invoke($command) {
        if (strlen($command->name) < 2) {  // ❌ Validation in handler!
            throw new Exception();
        }
        // ...
    }
}
```

### ❌ Framework Dependencies in Domain

```php
// ❌ BAD: Symfony in Domain
use Symfony\Component\Validator\Constraints as Assert;

class Customer {
    #[Assert\NotBlank]  // ❌ Framework coupling!
    private string $name;
}
```

### ❌ Anemic Domain Models

```php
// ❌ BAD: Just getters/setters
class Customer {
    public function setName(string $name): void {
        $this->name = $name;  // No business rules!
    }
}
```

### ✅ GOOD Patterns

- Value Objects enforce invariants
- Domain methods express business operations
- Handlers orchestrate, Domain executes
- Configuration externalized to YAML/XML

---

## CodelyTV Architecture Pattern

This project follows CodelyTV's hexagonal architecture patterns:

- **Directory structure**: Bounded Context → Layer → Component Type
- **Naming conventions**: Explicit suffixes (Command, Handler, Repository, etc.)
- **Layer isolation**: Deptrac enforces boundaries
- **CQRS**: Commands for writes, Queries for reads
- **Event-driven**: Domain Events for decoupling

**See**: [DIRECTORY-STRUCTURE.md](DIRECTORY-STRUCTURE.md) for complete hierarchy.
