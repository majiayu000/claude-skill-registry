---
name: acc-create-mediator
description: Generates Mediator pattern for PHP 8.5. Creates coordination layer for complex component interactions with event dispatching, request/response handling, and colleague classes. Reduces coupling between interacting objects. Includes unit tests.
---

# Mediator Pattern Generator

## Overview

Generates Mediator pattern components for PHP 8.5 to coordinate complex interactions between multiple objects without them referencing each other directly.

## When to Use

- Complex communication between multiple objects
- Reducing coupling in event-driven systems
- Coordinating UI components or form elements
- Command bus / Query bus implementation
- Chat room / notification hub scenarios
- Workflow coordination

## Generated Components

| Component | Location | Purpose |
|-----------|----------|---------|
| MediatorInterface | `src/Application/{Context}/Mediator/` | Defines mediation contract |
| ConcreteMediator | `src/Application/{Context}/Mediator/` | Implements coordination logic |
| ColleagueInterface | `src/Application/{Context}/Mediator/Colleague/` | Participant contract |
| AbstractColleague | `src/Application/{Context}/Mediator/Colleague/` | Base with mediator access |
| ConcreteColleagues | `src/Application/{Context}/Mediator/Colleague/` | Participating components |
| Tests | `tests/{Context}/Application/Mediator/` | Unit tests |

## Input Requirements

1. **Name** - Mediator name (e.g., "OrderWorkflow", "ChatRoom")
2. **Context** - Bounded context (e.g., "Order", "Notification")
3. **Colleagues** - List of participating components
4. **Events** - Events to coordinate (optional)

## Template: Mediator Interface

```php
<?php

declare(strict_types=1);

namespace App\{Context}\Application\Mediator;

use App\{Context}\Application\Mediator\Colleague\ColleagueInterface;

interface {Name}Mediator
{
    public function notify(ColleagueInterface $sender, string $event, mixed $data = null): void;
    public function register(ColleagueInterface $colleague): void;
    public function send(string $request, mixed $data = null): mixed;
}
```

## Template: Colleague Interface

```php
<?php

declare(strict_types=1);

namespace App\{Context}\Application\Mediator\Colleague;

use App\{Context}\Application\Mediator\{Name}Mediator;

interface ColleagueInterface
{
    public function getName(): string;
    public function setMediator({Name}Mediator $mediator): void;
    public function handle(mixed $data): mixed;
}
```

## Template: Abstract Colleague

```php
<?php

declare(strict_types=1);

namespace App\{Context}\Application\Mediator\Colleague;

use App\{Context}\Application\Mediator\{Name}Mediator;

abstract class AbstractColleague implements ColleagueInterface
{
    protected ?{Name}Mediator $mediator = null;

    public function setMediator({Name}Mediator $mediator): void
    {
        $this->mediator = $mediator;
    }

    protected function notify(string $event, mixed $data = null): void
    {
        if ($this->mediator === null) {
            throw new MediatorNotSetException();
        }
        $this->mediator->notify($this, $event, $data);
    }

    protected function send(string $request, mixed $data = null): mixed
    {
        if ($this->mediator === null) {
            throw new MediatorNotSetException();
        }
        return $this->mediator->send($request, $data);
    }
}
```

## File Placement

```
src/
└── {Context}/
    └── Application/
        └── Mediator/
            ├── {Name}Mediator.php           # Interface
            ├── {Name}MediatorImpl.php       # Implementation
            └── Colleague/
                ├── ColleagueInterface.php   # Base interface
                ├── AbstractColleague.php    # Base class
                └── {Colleague}.php          # Participants

tests/
└── {Context}/
    └── Application/
        └── Mediator/
            └── {Name}MediatorTest.php       # Tests
```

## GRASP Compliance

| Principle | Implementation |
|-----------|----------------|
| Low Coupling | Colleagues don't know each other |
| Indirection | Mediator provides indirection layer |
| Controller | Mediator coordinates use case flow |
| Pure Fabrication | Mediator is artificial coordinating class |

## References

See `references/` for detailed documentation:
- `templates.md` - Full Mediator, Colleague, Command Bus, Event Mediator, Chat Room templates
- `examples.md` - Real-world examples
