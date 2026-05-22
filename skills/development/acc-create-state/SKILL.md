---
name: acc-create-state
description: Generates State pattern for PHP 8.5. Creates state machines with context, state interface, and concrete states for behavior changes. Includes unit tests.
---

# State Pattern Generator

Creates State pattern infrastructure for objects that change behavior based on internal state.

## When to Use

| Scenario | Example |
|----------|---------|
| Object behavior varies by state | Order (pending, paid, shipped) |
| Many conditionals based on state | Document workflow |
| State-specific transitions | Subscription lifecycle |
| Finite state machines | Payment processing |

## Component Characteristics

### StateInterface
- Defines available actions
- Returns new state after transition
- Encapsulates state-specific behavior

### Context
- Holds current state
- Delegates actions to state
- Manages state transitions

### Concrete States
- Implement behavior for each state
- Handle valid/invalid transitions
- Return appropriate next state

---

## Generation Process

### Step 1: Analyze State Machine

Determine:
- All possible states
- Actions/transitions between states
- Which actions are valid per state
- Terminal states (no outgoing transitions)

### Step 2: Generate State Components

**Path:** `src/Domain/{BoundedContext}/State/`

1. `{Name}StateInterface.php` — State contract with all actions
2. `Abstract{Name}State.php` — Base class with default (invalid) implementations
3. `{StateName}State.php` — Concrete state for each state (PendingState, PaidState, etc.)
4. `{Name}StateFactory.php` — Factory for reconstitution from storage

**Path:** `src/Domain/{BoundedContext}/Exception/`

5. `InvalidStateTransitionException.php` — Exception for invalid transitions

### Step 3: Update Entity

**Path:** `src/Domain/{BoundedContext}/Entity/`

Update entity to use state pattern with delegation methods.

### Step 4: Generate Tests

**Path:** `tests/Unit/Domain/{BoundedContext}/State/`

1. `{StateName}StateTest.php` — Test each concrete state
2. `{Entity}StateTransitionTest.php` — Test full state machine

---

## File Placement

| Component | Path |
|-----------|------|
| State Interface | `src/Domain/{BoundedContext}/State/` |
| Concrete States | `src/Domain/{BoundedContext}/State/` |
| State Factory | `src/Domain/{BoundedContext}/State/` |
| Entity with State | `src/Domain/{BoundedContext}/Entity/` |
| Exception | `src/Domain/{BoundedContext}/Exception/` |
| Unit Tests | `tests/Unit/Domain/{BoundedContext}/State/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Interface | `{Name}StateInterface` | `OrderStateInterface` |
| Abstract State | `Abstract{Name}State` | `AbstractOrderState` |
| Concrete State | `{StateName}State` | `PendingState`, `PaidState` |
| Factory | `{Name}StateFactory` | `OrderStateFactory` |
| Exception | `InvalidStateTransitionException` | `InvalidStateTransitionException` |
| Test | `{ClassName}Test` | `PendingStateTest` |

---

## Quick Template Reference

### State Interface

```php
interface {Name}StateInterface
{
    public function getName(): string;
    public function {action1}({Context} $context): self;
    public function {action2}({Context} $context): self;
    public function canTransitionTo(self $state): bool;
    /** @return array<string> */
    public function allowedTransitions(): array;
}
```

### Abstract State

```php
abstract readonly class Abstract{Name}State implements {Name}StateInterface
{
    public function {action1}({Context} $context): {Name}StateInterface
    {
        throw InvalidStateTransitionException::actionNotAllowed('{action1}', $this->getName());
    }

    public function canTransitionTo({Name}StateInterface $state): bool
    {
        return in_array($state->getName(), $this->allowedTransitions(), true);
    }
}
```

### Concrete State

```php
final readonly class {StateName}State extends Abstract{Name}State
{
    public function getName(): string
    {
        return '{state_name}';
    }

    public function {action1}({Context} $context): {Name}StateInterface
    {
        $context->recordEvent(new {Event}($context->id()));
        return new {NextState}State();
    }

    public function allowedTransitions(): array
    {
        return ['{next_state_1}', '{next_state_2}'];
    }
}
```

### State Factory

```php
final class {Name}StateFactory
{
    public static function fromName(string $name): {Name}StateInterface
    {
        return match ($name) {
            'pending' => new PendingState(),
            'confirmed' => new ConfirmedState(),
            default => throw new \InvalidArgumentException("Unknown state: $name"),
        };
    }
}
```

---

## Usage Example

```php
// Entity with state
$order = new Order($id, $customerId, $items);
$order->confirm();  // Pending -> Confirmed
$order->pay();      // Confirmed -> Paid
$order->ship();     // Paid -> Shipped
$order->deliver();  // Shipped -> Delivered

// Check state
if ($order->isInState('delivered')) {
    // ...
}

// Reconstitute from storage
$state = OrderStateFactory::fromName($row['state']);
$order = new Order($id, $customerId, $items, $state);
```

---

## State Diagram Template

```
┌──────────┐  action1   ┌──────────┐  action2   ┌──────────┐
│  State1  │───────────▶│  State2  │───────────▶│  State3  │
└────┬─────┘            └────┬─────┘            └──────────┘
     │                       │
     │ cancel                │ cancel
     │                       │
     ▼                       ▼
┌──────────┐            ┌──────────┐
│Cancelled │            │Cancelled │
└──────────┘            └──────────┘
```

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Mutable States | Shared state pollution | Make states readonly |
| God State | One state handles all | Split into specific states |
| Missing Transitions | Silent failures | Throw on invalid action |
| State in Entity | Mixed concerns | Extract to State classes |
| No Factory | Hard to reconstitute | Add StateFactory |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — State interface, abstract, concrete templates
- `references/examples.md` — Order state machine example and tests
