---
name: acc-solid-knowledge
description: SOLID principles knowledge base for PHP 8.5 projects. Provides quick reference for SRP, OCP, LSP, ISP, DIP with detection patterns, PHP examples, and antipattern identification. Use for architecture audits and code quality reviews.
---

# SOLID Principles Knowledge Base

## Overview

SOLID is a set of five design principles for writing maintainable, extensible software.

| Principle | Name | Core Idea |
|-----------|------|-----------|
| **S** | Single Responsibility | One class = one reason to change |
| **O** | Open/Closed | Open for extension, closed for modification |
| **L** | Liskov Substitution | Subtypes must be substitutable for base types |
| **I** | Interface Segregation | Many specific interfaces > one general |
| **D** | Dependency Inversion | Depend on abstractions, not concretions |

## Quick Detection Patterns

### SRP Violations

```bash
# God classes (>500 lines)
find . -name "*.php" -exec wc -l {} \; | awk '$1 > 500 {print}'

# Classes with "And" in name
grep -rn "class.*And[A-Z]" --include="*.php"

# Classes with >7 dependencies
grep -rn "public function __construct" --include="*.php" -A 20 | grep -E "private|readonly" | wc -l

# Multiple responsibility indicators
grep -rn "class.*Manager\|class.*Handler\|class.*Processor" --include="*.php"
```

**Signs of SRP Violation:**
- Class has >500 lines
- Class has >7 dependencies
- Class name contains "And", "Or", "Manager", "Handler"
- Multiple unrelated public methods
- Changes for multiple business reasons

### OCP Violations

```bash
# Switch on type
grep -rn "switch.*instanceof\|switch.*::class" --include="*.php"

# Type checking conditionals
grep -rn "if.*instanceof\|elseif.*instanceof" --include="*.php"

# Hardcoded type maps
grep -rn "\[.*::class.*=>" --include="*.php"
```

**Signs of OCP Violation:**
- Switch statements on object types
- instanceof chains in conditionals
- Adding new types requires modifying existing code
- Hardcoded type-to-behavior mappings

### LSP Violations

```bash
# Exception in overridden methods
grep -rn "throw.*NotImplemented\|throw.*NotSupported" --include="*.php"

# Empty overrides
grep -rn "public function.*\{[\s]*\}" --include="*.php"

# Type checks in child classes
grep -rn "if.*parent::" --include="*.php"
```

**Signs of LSP Violation:**
- Child class throws NotImplementedException
- Child class has empty method overrides
- Parent type check in child class
- Preconditions strengthened in subtype
- Postconditions weakened in subtype

### ISP Violations

```bash
# Large interfaces (>5 methods)
grep -rn "interface\s" --include="*.php" -A 30 | grep -c "public function"

# Empty interface implementations
grep -rn "// TODO\|// not implemented\|// unused" --include="*.php"
```

**Signs of ISP Violation:**
- Interface has >5 methods
- Classes implement interfaces partially
- Unused methods return null/throw
- Interface name too generic ("Service", "Manager")

### DIP Violations

```bash
# Direct instantiation in constructors
grep -rn "new\s\+[A-Z]" --include="*.php" | grep -v "Exception\|DateTime\|stdClass"

# Static method calls
grep -rn "::[a-z].*(" --include="*.php" | grep -v "self::\|static::\|parent::"

# Concrete class type hints (not interfaces)
grep -rn "function.*([A-Z][a-z]*[A-Z]" --include="*.php"
```

**Signs of DIP Violation:**
- `new ConcreteClass()` inside methods
- Static calls to concrete classes
- Type hints to concrete classes (not interfaces)
- No constructor injection

## PHP 8.5 Patterns

### SRP Compliant

```php
<?php

declare(strict_types=1);

// BAD: Multiple responsibilities
final class UserService
{
    public function register(UserData $data): User { /* ... */ }
    public function sendEmail(User $user): void { /* ... */ }
    public function generateReport(User $user): Report { /* ... */ }
}

// GOOD: Single responsibility each
final readonly class RegisterUserHandler
{
    public function __construct(
        private UserRepository $users,
        private EventDispatcher $events,
    ) {}

    public function __invoke(RegisterUserCommand $command): UserId
    {
        $user = User::register($command->email, $command->password);
        $this->users->save($user);
        $this->events->dispatch($user->releaseEvents());

        return $user->id;
    }
}
```

### OCP Compliant

```php
<?php

declare(strict_types=1);

// BAD: Modification required for new types
final class PaymentProcessor
{
    public function process(Payment $payment): void
    {
        match ($payment->type) {
            'card' => $this->processCard($payment),
            'paypal' => $this->processPaypal($payment),
            // Must modify for new payment types
        };
    }
}

// GOOD: Extension without modification
interface PaymentGateway
{
    public function supports(Payment $payment): bool;
    public function process(Payment $payment): PaymentResult;
}

final readonly class PaymentProcessor
{
    /** @param iterable<PaymentGateway> $gateways */
    public function __construct(
        private iterable $gateways,
    ) {}

    public function process(Payment $payment): PaymentResult
    {
        foreach ($this->gateways as $gateway) {
            if ($gateway->supports($payment)) {
                return $gateway->process($payment);
            }
        }
        throw new UnsupportedPaymentException($payment->type);
    }
}
```

### LSP Compliant

```php
<?php

declare(strict_types=1);

// BAD: Violates substitutability
abstract class Bird
{
    abstract public function fly(): void;
}

final class Penguin extends Bird
{
    public function fly(): void
    {
        throw new CannotFlyException(); // LSP violation!
    }
}

// GOOD: Proper abstraction hierarchy
interface Bird
{
    public function move(): void;
}

interface FlyingBird extends Bird
{
    public function fly(): void;
}

final readonly class Penguin implements Bird
{
    public function move(): void
    {
        $this->swim();
    }

    private function swim(): void { /* ... */ }
}

final readonly class Eagle implements FlyingBird
{
    public function move(): void
    {
        $this->fly();
    }

    public function fly(): void { /* ... */ }
}
```

### ISP Compliant

```php
<?php

declare(strict_types=1);

// BAD: Fat interface
interface UserRepository
{
    public function find(UserId $id): ?User;
    public function findByEmail(Email $email): ?User;
    public function save(User $user): void;
    public function delete(User $user): void;
    public function findAll(): array;
    public function count(): int;
    public function export(): string;
    public function import(string $data): void;
}

// GOOD: Segregated interfaces
interface UserReader
{
    public function find(UserId $id): ?User;
    public function findByEmail(Email $email): ?User;
}

interface UserWriter
{
    public function save(User $user): void;
    public function delete(User $user): void;
}

interface UserExporter
{
    public function export(): string;
    public function import(string $data): void;
}

// Compose as needed
interface UserRepository extends UserReader, UserWriter {}
```

### DIP Compliant

```php
<?php

declare(strict_types=1);

// BAD: Depends on concretions
final class OrderService
{
    public function process(Order $order): void
    {
        $mailer = new SmtpMailer();           // Concrete dependency
        $logger = Logger::getInstance();       // Static dependency
        $validator = new OrderValidator();     // Hidden dependency

        // ...
    }
}

// GOOD: Depends on abstractions
final readonly class OrderService
{
    public function __construct(
        private OrderRepository $orders,
        private Mailer $mailer,
        private LoggerInterface $logger,
        private OrderValidator $validator,
    ) {}

    public function process(Order $order): void
    {
        $this->validator->validate($order);
        $this->orders->save($order);
        $this->mailer->send(new OrderConfirmation($order));
        $this->logger->info('Order processed', ['id' => $order->id->value]);
    }
}
```

## SOLID & DDD Integration

| SOLID | DDD Application |
|-------|-----------------|
| SRP | Aggregates have single consistency boundary |
| OCP | Domain Events enable extension without modification |
| LSP | Value Objects are substitutable (same type = same behavior) |
| ISP | Repository interfaces segregated (Reader/Writer) |
| DIP | Domain depends on Repository interfaces, not implementations |

## SOLID & Clean Architecture

| Layer | SOLID Focus |
|-------|-------------|
| Domain | SRP (Entities), LSP (Value Objects), ISP (Repository interfaces) |
| Application | SRP (Use Cases), DIP (Port interfaces) |
| Infrastructure | OCP (Adapters), DIP (Implements ports) |
| Presentation | SRP (Controllers), ISP (API contracts) |

## Severity Levels

| Level | Description | Example |
|-------|-------------|---------|
| CRITICAL | Fundamental violation affecting entire system | God class, no DI |
| WARNING | Localized violation, should be fixed | instanceof chains |
| INFO | Minor issue, consider refactoring | Interface with 6 methods |

## References

See detailed documentation in `references/`:
- `srp-patterns.md` - Single Responsibility patterns
- `ocp-patterns.md` - Open/Closed patterns
- `lsp-patterns.md` - Liskov Substitution patterns
- `isp-patterns.md` - Interface Segregation patterns
- `dip-patterns.md` - Dependency Inversion patterns
- `antipatterns.md` - Common SOLID violations

See `assets/report-template.md` for audit report format.
