---
name: code-organization
description: Enforce code organization principles - "Directory X contains ONLY class type X", DDD naming patterns, PHP best practices, type safety, and SOLID principles. Use when reviewing code structure, placing classes, or ensuring proper organization.
---

# Code Organization Skill

## Core Principle

> **Directory X contains ONLY class type X**

This is the fundamental rule for code organization in this codebase.

## Context (Input)

- Creating new classes and determining correct directory
- Moving classes to proper locations
- Reviewing code for organizational compliance
- Fixing organizational issues from code reviews
- Ensuring class names match their responsibilities

## Task (Function)

Enforce strict code organization principles: proper directory structure, DDD naming conventions, specific variable names, type safety, SOLID principles, and PHP best practices.

## Directory Type Classification

Classes MUST be in directories matching their type:

| Directory          | Contains ONLY                   | Example                            |
| ------------------ | ------------------------------- | ---------------------------------- |
| `Converter/`       | Type converters                 | `UlidTypeConverter`                |
| `Transformer/`     | Data transformers (DB/serial)   | `CustomerToArrayTransformer`       |
| `Validator/`       | Validation logic                | `UlidValidator`                    |
| `Builder/`         | Object builders                 | `QueryBuilder`                     |
| `Fixer/`           | Data fixers/modifiers           | `DataFixer`                        |
| `Cleaner/`         | Data cleaners/filters           | `DataCleaner`                      |
| `Factory/`         | Object factories                | `CustomerFactory`                  |
| `Resolver/`        | Value resolvers                 | `CustomerUpdateScalarResolver`     |
| `Serializer/`      | Serializers/normalizers         | `CustomerNormalizer`               |
| `Formatter/`       | Data formatters                 | `CustomerNameFormatter`            |
| `Mapper/`          | Data mappers                    | `PathsMapper`                      |
| `Provider/`        | Data/service providers          | `TimestampProvider`                |
| `Processor/`       | API Platform processors         | `CreateCustomerProcessor`          |
| `EventListener/`   | Event listeners (Symfony)       | `QueryParameterValidationListener` |
| `EventSubscriber/` | Event subscribers (Symfony/App) | `SendEmailOnCustomerCreated`       |

## DDD Naming Patterns

### By Layer and Type

| Layer              | Class Type         | Naming Pattern                       | Example                           |
| ------------------ | ------------------ | ------------------------------------ | --------------------------------- |
| **Domain**         | Entity             | `{EntityName}.php`                   | `Customer.php`                    |
|                    | Value Object       | `{ConceptName}.php`                  | `Email.php`, `Money.php`          |
|                    | Domain Event       | `{Entity}{PastTenseAction}.php`      | `CustomerCreated.php`             |
|                    | Repository Iface   | `{Entity}RepositoryInterface.php`    | `CustomerRepositoryInterface.php` |
|                    | Exception          | `{SpecificError}Exception.php`       | `InvalidEmailException.php`       |
| **Application**    | Command            | `{Action}{Entity}Command.php`        | `CreateCustomerCommand.php`       |
|                    | Command Handler    | `{Action}{Entity}Handler.php`        | `CreateCustomerHandler.php`       |
|                    | Event Subscriber   | `{Action}On{Event}.php`              | `SendEmailOnCustomerCreated.php`  |
|                    | DTO                | `{Entity}{Type}.php`                 | `CustomerInput.php`               |
|                    | Processor          | `{Action}{Entity}Processor.php`      | `CreateCustomerProcessor.php`     |
|                    | Transformer        | `{From}To{To}Transformer.php`        | `CustomerToArrayTransformer.php`  |
| **Infrastructure** | Repository         | `{Technology}{Entity}Repository.php` | `MySQLCustomerRepository.php`     |
|                    | Doctrine Type      | `{ConceptName}Type.php`              | `UlidType.php`                    |
|                    | Bus Implementation | `{Framework}{Type}Bus.php`           | `SymfonyCommandBus.php`           |

### Directory Structure by Layer

```
src/{Context}/
├── Application/
│   ├── Command/          ← Commands
│   ├── CommandHandler/   ← Command Handlers
│   ├── EventSubscriber/  ← Event Subscribers
│   ├── DTO/              ← Data Transfer Objects
│   ├── Processor/        ← API Platform Processors
│   ├── Transformer/      ← Data Transformers
│   ├── Validator/        ← Validators
│   ├── Converter/        ← Type Converters
│   ├── Resolver/         ← Value Resolvers
│   ├── Factory/          ← Factories
│   ├── Builder/          ← Builders
│   ├── Formatter/        ← Formatters
│   └── MutationInput/    ← GraphQL Mutation Inputs
├── Domain/
│   ├── Entity/           ← Entities & Aggregates
│   ├── ValueObject/      ← Value Objects
│   ├── Event/            ← Domain Events
│   ├── Repository/       ← Repository Interfaces
│   └── Exception/        ← Domain Exceptions
└── Infrastructure/
    ├── Repository/       ← Repository Implementations
    ├── DoctrineType/     ← Custom Doctrine Types
    ├── EventSubscriber/  ← Infrastructure Event Subscribers
    ├── EventListener/    ← Symfony Event Listeners
    └── Bus/              ← Message Bus Implementations
```

## Verification Checklist

When creating or reviewing a class, verify:

1. ✅ **Class Type Matches Directory** (Directory X contains ONLY class type X)
   - Example: `UlidValidator` in `Validator/`, NOT `Transformer/`
2. ✅ **Class Name Follows DDD Pattern** for its type
3. ✅ **Namespace Matches Directory Structure** exactly
4. ✅ **Class Name Reflects Actual Functionality**
5. ✅ **Correct Layer** (Domain/Application/Infrastructure)
6. ✅ **Domain Layer Has NO Framework Imports** (Symfony/Doctrine/API Platform)
7. ✅ **Variable Names Are Specific** (not vague)
   - ✅ `$typeConverter`, `$scalarResolver` (specific)
   - ❌ `$converter`, `$resolver` (too vague)
8. ✅ **Parameter Names Match Actual Types**
   - ✅ `mixed $value` when accepts any type
   - ❌ `string $binary` when accepts mixed
9. ✅ **No "Helper" or "Util" Classes** (extract specific responsibilities)

## PHP Best Practices

### Required Patterns

- ✅ **Constructor property promotion**
- ✅ **Inject ALL dependencies** (no default instantiation)
- ✅ **Use `readonly`** when appropriate
- ✅ **Use `final`** for classes that shouldn't be extended
- ✅ **No static methods** (except named constructors like `create()`, `from()`)

### Anti-Patterns (Forbidden)

- ❌ **Helper/Util classes** - Extract specific responsibilities
- ❌ **Default instantiation in constructors** - Inject dependencies
- ❌ **Vague variable names** - Be specific
- ❌ **Namespace mismatches** - Must match directory structure

## Factory Pattern (Maintainability & Flexibility)

> **Use factories when creating typed classes with dependencies or configuration**

### When Factories Are REQUIRED (Production Code)

1. Objects with injected dependencies (timestamp providers, config, etc.)
2. Objects requiring complex construction logic
3. Objects needing different implementations per environment
4. Objects created from external input (DTOs, metrics, etc.)

### When Factories Are OPTIONAL (Tests)

- Tests can instantiate objects directly for simplicity
- Test-specific factories can be created for reusable fixtures

### Factory Benefits

- ✅ Centralized object creation logic
- ✅ Easy to inject different implementations
- ✅ Configuration changes don't affect consumers
- ✅ Single place for validation/transformation
- ✅ Enables dependency injection for complex objects

### Example: Bad vs Good

```php
// ❌ BAD: Direct instantiation with configuration
public function emit(BusinessMetric $metric): void
{
    $timestamp = (int)(microtime(true) * 1000);
    $payload = new EmfPayload(
        new EmfAwsMetadata($timestamp, new EmfCloudWatchMetricConfig(...)),
        new EmfDimensionValueCollection(...),
        new EmfMetricValueCollection(...)
    );
    $this->logger->info($payload);
}

// ✅ GOOD: Factory handles complexity
public function emit(BusinessMetric $metric): void
{
    $payload = $this->payloadFactory->createFromMetric($metric);
    $this->logger->info($payload);
}
```

### Factory Naming Convention

- `{ObjectName}Factory` - creates `{ObjectName}` instances
- Location: Same namespace as the object being created
- Example: `EmfPayloadFactory` creates `EmfPayload`

## Type Safety: Classes Over Arrays

> **Prefer typed classes and collections over arrays for structured data**

Arrays lack type safety and self-documentation. Use concrete classes instead.

### Array vs Class Comparison

| Pattern       | Bad (Array)                               | Good (Class)                                |
| ------------- | ----------------------------------------- | ------------------------------------------- |
| Configuration | `['endpoint' => 'X', 'operation' => 'Y']` | `new EndpointOperationDimensions('X', 'Y')` |
| Return data   | `return ['name' => $n, 'value' => $v]`    | `return new MetricData($n, $v)`             |
| Method params | `function emit(array $metrics)`           | `function emit(MetricCollection $metrics)`  |
| Events data   | `['type' => 'created', 'id' => $id]`      | `new CustomerCreatedEvent($id)`             |

### Benefits of Typed Classes

- ✅ IDE autocompletion and refactoring support
- ✅ Static analysis catches type errors
- ✅ Self-documenting code
- ✅ Encapsulation (validation in constructor)
- ✅ Single Responsibility
- ✅ Open/Closed principle (extend via new classes)

### Collection Pattern

```php
// ❌ BAD: Array of arrays
$metrics = [
    ['name' => 'OrdersPlaced', 'value' => 1],
    ['name' => 'OrderValue', 'value' => 99.99],
];

// ✅ GOOD: Typed collection of objects
$metrics = new MetricCollection(
    new OrdersPlacedMetric(value: 1),
    new OrderValueMetric(value: 99.99)
);
```

### When Arrays ARE Acceptable

- Simple key-value maps for serialization output (`toArray()` methods)
- Framework integration points requiring arrays
- Temporary internal data within a single method

## Cross-Cutting Concerns Pattern

> **Use event subscribers for cross-cutting concerns (metrics, logging), NOT direct injection into handlers**

### Anti-Pattern: Metrics in Command Handler

```php
// ❌ WRONG: Metrics in command handler
final class CreateCustomerHandler
{
    public function __construct(
        private CustomerRepository $repository,
        private BusinessMetricsEmitterInterface $metrics  // Wrong place!
    ) {}

    public function __invoke(CreateCustomerCommand $cmd): void
    {
        $customer = Customer::create(...);
        $this->repository->save($customer);
        $this->metrics->emit(new CustomersCreatedMetric());  // Violates SRP
    }
}
```

### Correct Pattern: Dedicated Event Subscriber

```php
// ✅ CORRECT: Clean command handler
final class CreateCustomerHandler
{
    public function __construct(
        private CustomerRepository $repository,
        private EventBusInterface $eventBus
    ) {}

    public function __invoke(CreateCustomerCommand $cmd): void
    {
        $customer = Customer::create(...);
        $this->repository->save($customer);
        $this->eventBus->publish(...$customer->pullDomainEvents());
        // Metrics subscriber handles emission
    }
}

// ✅ CORRECT: Metrics in dedicated subscriber
final class CustomerCreatedMetricsSubscriber implements DomainEventSubscriberInterface
{
    public function __invoke(CustomerCreatedEvent $event): void
    {
        // Error handling is automatic via DomainEventMessageHandler.
        // Subscribers are executed in async workers - failures are logged + emit metrics.
        // This ensures observability never breaks the main request (AP from CAP).
        $this->metricsEmitter->emit($this->metricFactory->create());
    }
}
```

## Common Issues and Fixes

### Issue 1: Class in Wrong Type Directory

```bash
❌ WRONG:
src/Shared/Infrastructure/Transformer/UlidValidator.php

✅ CORRECT:
src/Shared/Infrastructure/Validator/UlidValidator.php

# Fix:
mv src/Shared/Infrastructure/Transformer/UlidValidator.php \
   src/Shared/Infrastructure/Validator/UlidValidator.php
# Update namespace and all imports
```

### Issue 2: Vague Variable Names

```php
❌ WRONG:
private UlidTypeConverter $converter;  // Converter of what?

✅ CORRECT:
private UlidTypeConverter $typeConverter;  // Specific!
```

### Issue 3: Misleading Parameter Names

```php
❌ WRONG:
public function fromBinary(mixed $binary): Ulid  // Accepts mixed, not just binary

✅ CORRECT:
public function fromBinary(mixed $value): Ulid  // Accurate!
```

### Issue 4: Helper/Util Classes

```php
❌ WRONG:
class CustomerHelper {
    public function validateEmail() {}
    public function formatName() {}
    public function convertData() {}
}

✅ CORRECT: Extract specific responsibilities
- CustomerEmailValidator (Validator/)
- CustomerNameFormatter (Formatter/)
- CustomerDataConverter (Converter/)
```

### Issue 5: Namespace Mismatch

```php
❌ WRONG:
// File: src/Shared/Infrastructure/Validator/UlidValidator.php
namespace App\Shared\Infrastructure\Transformer;  // Mismatch!

✅ CORRECT:
// File: src/Shared/Infrastructure/Validator/UlidValidator.php
namespace App\Shared\Infrastructure\Validator;  // Matches directory!
```

## Decision Tree: Where Does It Belong?

```text
What does the class DO?

├─ Converts between types (string ↔ object)? → Converter/
├─ Transforms for DB/serialization? → Transformer/
├─ Validates values? → Validator/
├─ Builds/constructs objects? → Builder/
├─ Fixes/modifies data? → Fixer/
├─ Cleans/filters data? → Cleaner/
├─ Creates complex objects? → Factory/
├─ Resolves/determines values? → Resolver/
├─ Normalizes/serializes? → Serializer/
├─ Formats data for display? → Formatter/
├─ Maps data between structures? → Mapper/
└─ Something else? → Define specific responsibility!
```

## Verification Commands

```bash
# Check namespace consistency
make phpcsfixer
make psalm

# Find organizational issues
grep -r "class.*Helper" src/      # Find Helper classes
grep -r "class.*Util" src/        # Find Util classes
grep -r "private.*\$converter;" src/  # Find vague names

# Verify architecture compliance
make deptrac  # Must show 0 violations
```

## Constraints (Never Do This)

**NEVER**:

- Place class in wrong type directory (violates "Directory X contains ONLY class type X")
- Allow Domain layer to import framework code (Symfony/Doctrine/API Platform)
- Use vague variable names (`$converter`, `$resolver` - be specific!)
- Create "Helper" or "Util" classes (extract specific responsibilities)
- Allow namespace to mismatch directory structure
- Use arrays for structured data when typed classes would be appropriate
- Inject cross-cutting concerns (metrics, logging) into command handlers
- Create complex objects directly without factories in production code

**ALWAYS**:

- Verify "Directory X contains ONLY class type X" principle
- Use specific variable names (`$typeConverter`, not `$converter`)
- Use accurate parameter names (match actual types)
- Ensure namespace matches directory structure exactly
- Extract specific responsibilities from Helper/Util classes
- Prefer typed classes over arrays for structured data
- Use collections instead of arrays of objects
- Use event subscribers for cross-cutting concerns
- Use factories for complex object creation in production code

## Related Skills

- **code-review**: References this skill for organization verification during PR reviews
- **implementing-ddd-architecture**: DDD patterns and layer structure
- **deptrac-fixer**: Fixes architectural boundary violations
- **quality-standards**: Maintains overall code quality metrics

## Related Documentation

See `reference/troubleshooting.md` for detailed troubleshooting and `examples/organization-fixes.md` for real-world examples.
