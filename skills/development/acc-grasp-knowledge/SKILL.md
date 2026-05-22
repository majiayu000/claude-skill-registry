---
name: acc-grasp-knowledge
description: GRASP principles knowledge base for PHP 8.5 projects. Provides quick reference for 9 responsibility assignment patterns (Information Expert, Creator, Controller, Low Coupling, High Cohesion, Polymorphism, Pure Fabrication, Indirection, Protected Variations). Use for architecture audits and design decisions.
---

# GRASP Principles Knowledge Base

## Overview

GRASP (General Responsibility Assignment Software Patterns) provides guidelines for assigning responsibilities to classes and objects in object-oriented design.

| Principle | Core Question | Goal |
|-----------|---------------|------|
| **Information Expert** | Who has the data? | Assign to class with information |
| **Creator** | Who creates objects? | Assign creation responsibility |
| **Controller** | Who handles system events? | Coordinate use case flow |
| **Low Coupling** | How to reduce dependencies? | Minimize interconnections |
| **High Cohesion** | How to focus responsibilities? | Keep related things together |
| **Polymorphism** | How to handle type variations? | Use polymorphic operations |
| **Pure Fabrication** | What if no domain class fits? | Create artificial class |
| **Indirection** | How to decouple? | Add intermediate object |
| **Protected Variations** | How to handle change? | Hide variation points |

## Quick Detection Patterns

### Information Expert Violations

```bash
# Feature Envy: Class uses other class's data more
Grep: "->get.*->get.*->get" --glob "**/*.php"

# Train wreck calls
Grep: "->.*()->.*()->.*()->" --glob "**/*.php"
```

**Signs:** Method accesses other object's data extensively, data and behavior separated.

### Creator Violations

```bash
# Random creation locations
Grep: "new\s\+[A-Z][a-z]*[A-Z]" --glob "**/*.php"
```

**Signs:** Objects created in unexpected places, no clear creation ownership.

### Controller Violations

```bash
# Fat controllers (>100 lines)
find . -path "*/Controller/*.php" -exec wc -l {} \; | awk '$1 > 100'

# Business logic in controllers
Grep: "if.*&&.*||" --glob "*Controller.php"
```

**Signs:** Controller has >100 lines, business logic in controller.

### Low Coupling Violations

```bash
# High dependency count (>7)
Grep: "__construct" --glob "**/*.php" -A 15

# Concrete type dependencies
Grep: "function.*([A-Z][a-z]*[A-Z]" --glob "**/*.php"
```

**Signs:** Class has >7 dependencies, depends on concrete classes.

### High Cohesion Violations

```bash
# Unrelated method names
Grep: "public function" --glob "**/*.php" | grep -E "And[A-Z]|Or[A-Z]"

# Multiple responsibilities in class name
Grep: "class.*Manager|class.*Handler|class.*Processor" --glob "**/*.php"
```

**Signs:** Methods don't relate to each other, class does many unrelated things.

## Quick PHP 8.5 Examples

### Information Expert

```php
// BAD: Logic outside of object with data
final class OrderService
{
    public function calculateTotal(Order $order): Money
    {
        $total = Money::zero();
        foreach ($order->getLines() as $line) {
            $total = $total->add($line->getProduct()->getPrice()->multiply($line->getQuantity()));
        }
        return $total;
    }
}

// GOOD: Logic in class that has the data
final class Order
{
    public function total(): Money
    {
        return array_reduce(
            $this->lines,
            fn(Money $sum, OrderLine $line) => $sum->add($line->total()),
            Money::zero(),
        );
    }
}
```

### Low Coupling

```php
// BAD: Depends on concrete classes
final class ReportGenerator
{
    public function __construct(
        private DoctrineOrderRepository $orders,
        private SymfonyMailer $mailer,
    ) {}
}

// GOOD: Depends on abstractions
final readonly class ReportGenerator
{
    public function __construct(
        private OrderReader $orders,
        private Mailer $mailer,
    ) {}
}
```

### High Cohesion

```php
// BAD: Low cohesion - unrelated responsibilities
final class UserManager
{
    public function register(array $data): User { }
    public function sendEmail(User $user): void { }
    public function generateReport(): string { }
}

// GOOD: High cohesion - focused responsibilities
final readonly class UserRegistrationService
{
    public function register(RegistrationData $data): User { }
    public function confirmEmail(Token $token): void { }
}
```

## GRASP & DDD Integration

| GRASP | DDD Application |
|-------|-----------------|
| Information Expert | Entities contain their behavior |
| Creator | Aggregates create their entities |
| Controller | Application Services / Use Cases |
| Low Coupling | Bounded Context boundaries |
| High Cohesion | Aggregate consistency boundary |
| Polymorphism | Domain Services, Strategies |
| Pure Fabrication | Repositories, Factories, Specifications |
| Indirection | Anti-Corruption Layer, Adapters |
| Protected Variations | Ports & Adapters, Domain Events |

## References

For detailed patterns and examples, see `references/`:
- `information-expert.md` — Tell Don't Ask, calculations in owner
- `creator.md` — Factory patterns, aggregation rules
- `controller.md` — Use case handlers, thin controllers
- `low-coupling.md` — Dependency injection, abstractions
- `high-cohesion.md` — Focused responsibilities
- `polymorphism.md` — Strategy pattern, type variations
- `pure-fabrication.md` — Repositories, specifications
- `indirection.md` — Adapters, mediators
- `protected-variations.md` — Stable interfaces
- `antipatterns.md` — Common GRASP violations

## Assets

- `assets/report-template.md` — GRASP audit report format
