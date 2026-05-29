---
name: acc-saga-pattern-knowledge
description: Saga Pattern knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for saga orchestration, choreography, and distributed transaction audits.
---

# Saga Pattern Knowledge Base

Quick reference for Saga pattern and PHP implementation guidelines for distributed transactions.

## Core Principles

### Saga Pattern Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SAGA PATTERN                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   CHOREOGRAPHY (Event-driven)                                            │
│   ┌─────────┐    event    ┌─────────┐    event    ┌─────────┐           │
│   │ Service │───────────▶ │ Service │───────────▶ │ Service │           │
│   │    A    │             │    B    │             │    C    │           │
│   └─────────┘             └─────────┘             └─────────┘           │
│        │                       │                       │                │
│        └───────── compensate ──┴─── compensate ────────┘                │
│                                                                          │
│   ORCHESTRATION (Central coordinator)                                    │
│                    ┌───────────────┐                                    │
│                    │  Saga         │                                    │
│                    │  Orchestrator │                                    │
│                    └───────┬───────┘                                    │
│              ┌─────────────┼─────────────┐                              │
│              ▼             ▼             ▼                              │
│        ┌─────────┐   ┌─────────┐   ┌─────────┐                          │
│        │ Service │   │ Service │   │ Service │                          │
│        │    A    │   │    B    │   │    C    │                          │
│        └─────────┘   └─────────┘   └─────────┘                          │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Saga = Sequence of local transactions + compensating actions           │
│                                                                          │
│   T1 → T2 → T3 → ... → Tn                                               │
│    ↓    ↓    ↓          ↓                                               │
│   C1   C2   C3        Cn                                                │
│                                                                          │
│   If Ti fails: execute Ci-1, Ci-2, ..., C1 (reverse order)              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| Saga | Sequence of local transactions with compensations |
| Step | Single local transaction within saga |
| Compensating Action | Undoes the effect of a previous step |
| Orchestrator | Central coordinator managing saga execution |
| Choreography | Decentralized, event-driven saga coordination |
| Saga State | Current execution status (enum) |
| Idempotency | Steps can be retried safely |
| Semantic Lock | Prevents concurrent saga conflicts |

### Choreography vs Orchestration

| Aspect | Choreography | Orchestration |
|--------|--------------|---------------|
| Coordination | Decentralized (events) | Centralized (orchestrator) |
| Coupling | Loose | Tighter to orchestrator |
| Visibility | Distributed (hard to trace) | Centralized (easy to monitor) |
| Complexity | Simpler services | Simpler overall flow |
| Testing | Harder (distributed) | Easier (centralized logic) |
| Best for | Simple sagas (2-3 steps) | Complex sagas (4+ steps) |

## Quick Checklists

### Saga Design Checklist

- [ ] Each step is a local transaction
- [ ] Every step has compensating action
- [ ] Compensations are idempotent
- [ ] Forward actions are idempotent
- [ ] Saga state is persisted
- [ ] Failure handling defined for each step
- [ ] Timeout handling for long-running steps

### Orchestrator Checklist

- [ ] State machine for saga lifecycle
- [ ] Persistent saga state storage
- [ ] Step execution tracking
- [ ] Compensation ordering (reverse)
- [ ] Retry logic with limits
- [ ] Dead letter for failed sagas
- [ ] Correlation ID propagation

### Compensation Checklist

- [ ] Semantic undo (not rollback)
- [ ] Handles partial completion
- [ ] Idempotent (can run multiple times)
- [ ] Doesn't fail silently
- [ ] Logs compensation actions
- [ ] Eventual consistency acceptable

## PHP 8.5 Saga Patterns

### Saga State Enum

```php
<?php

declare(strict_types=1);

namespace Domain\Shared\Saga;

enum SagaState: string
{
    case Pending = 'pending';
    case Running = 'running';
    case Compensating = 'compensating';
    case Completed = 'completed';
    case Failed = 'failed';
    case CompensationFailed = 'compensation_failed';

    public function canTransitionTo(self $next): bool
    {
        return match ($this) {
            self::Pending => $next === self::Running,
            self::Running => in_array($next, [self::Completed, self::Compensating], true),
            self::Compensating => in_array($next, [self::Failed, self::CompensationFailed], true),
            self::Completed, self::Failed, self::CompensationFailed => false,
        };
    }

    public function isTerminal(): bool
    {
        return in_array($this, [self::Completed, self::Failed, self::CompensationFailed], true);
    }
}
```

### Saga Step Interface

```php
<?php

declare(strict_types=1);

namespace Domain\Shared\Saga;

interface SagaStepInterface
{
    public function name(): string;

    public function execute(SagaContext $context): StepResult;

    public function compensate(SagaContext $context): StepResult;

    public function isIdempotent(): bool;
}
```

### Saga Context

```php
<?php

declare(strict_types=1);

namespace Domain\Shared\Saga;

final class SagaContext
{
    /** @var array<string, mixed> */
    private array $data = [];

    public function __construct(
        public readonly string $sagaId,
        public readonly string $correlationId,
        public readonly \DateTimeImmutable $startedAt
    ) {}

    public function set(string $key, mixed $value): void
    {
        $this->data[$key] = $value;
    }

    public function get(string $key, mixed $default = null): mixed
    {
        return $this->data[$key] ?? $default;
    }

    public function has(string $key): bool
    {
        return array_key_exists($key, $this->data);
    }

    public function all(): array
    {
        return $this->data;
    }
}
```

### Saga Orchestrator

```php
<?php

declare(strict_types=1);

namespace Application\Shared\Saga;

use Domain\Shared\Saga\SagaContext;
use Domain\Shared\Saga\SagaState;
use Domain\Shared\Saga\SagaStepInterface;
use Domain\Shared\Saga\StepResult;

final class SagaOrchestrator
{
    /** @var array<SagaStepInterface> */
    private array $steps = [];

    /** @var array<string> */
    private array $completedSteps = [];

    private SagaState $state = SagaState::Pending;

    public function __construct(
        private readonly SagaContext $context,
        private readonly SagaPersistenceInterface $persistence
    ) {}

    public function addStep(SagaStepInterface $step): self
    {
        $this->steps[] = $step;
        return $this;
    }

    public function execute(): SagaResult
    {
        $this->state = SagaState::Running;
        $this->persistence->save($this->context->sagaId, $this->state, []);

        foreach ($this->steps as $step) {
            $result = $step->execute($this->context);

            if ($result->isFailure()) {
                return $this->compensate($step->name(), $result->error());
            }

            $this->completedSteps[] = $step->name();
            $this->persistence->save(
                $this->context->sagaId,
                $this->state,
                $this->completedSteps
            );
        }

        $this->state = SagaState::Completed;
        $this->persistence->save($this->context->sagaId, $this->state, $this->completedSteps);

        return SagaResult::completed($this->context);
    }

    private function compensate(string $failedStep, string $error): SagaResult
    {
        $this->state = SagaState::Compensating;
        $this->persistence->save($this->context->sagaId, $this->state, $this->completedSteps);

        $stepsToCompensate = array_reverse($this->completedSteps);

        foreach ($stepsToCompensate as $stepName) {
            $step = $this->findStep($stepName);
            $result = $step->compensate($this->context);

            if ($result->isFailure()) {
                $this->state = SagaState::CompensationFailed;
                $this->persistence->save($this->context->sagaId, $this->state, $this->completedSteps);

                return SagaResult::compensationFailed($this->context, $error, $result->error());
            }
        }

        $this->state = SagaState::Failed;
        $this->persistence->save($this->context->sagaId, $this->state, $this->completedSteps);

        return SagaResult::failed($this->context, $error);
    }

    private function findStep(string $name): SagaStepInterface
    {
        foreach ($this->steps as $step) {
            if ($step->name() === $name) {
                return $step;
            }
        }
        throw new \RuntimeException("Step not found: {$name}");
    }
}
```

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| Missing compensation | Saga step without compensate() | Critical |
| Non-idempotent steps | Retry causes duplicate effects | Critical |
| No saga state persistence | State lost on crash | Critical |
| Synchronous distributed tx | Two-phase commit attempt | Critical |
| Forward-only saga | No compensation at all | Warning |
| Missing correlation ID | Can't trace saga execution | Warning |
| No timeout handling | Saga hangs forever | Warning |
| Compensation order wrong | Not reversed | Warning |

## Detection Patterns

```bash
# Find saga implementations
Glob: **/Saga/**/*.php
Glob: **/*Saga.php
Grep: "SagaStep|SagaOrchestrator|Saga.*Interface" --glob "**/*.php"

# Check for saga state management
Grep: "SagaState|saga_state|enum.*Saga" --glob "**/*.php"

# Find compensating actions
Grep: "compensate|compensation|rollback.*step" --glob "**/Saga/**/*.php"

# Detect missing compensations
Grep: "implements.*SagaStep" --glob "**/*.php"
# Then check each for compensate() method

# Find choreography events
Grep: "SagaEvent|SagaCompleted|SagaFailed" --glob "**/Event/**/*.php"

# Check for saga persistence
Grep: "SagaPersistence|SagaRepository|saga.*save" --glob "**/*.php"

# Find potential issues
Grep: "Transaction.*begin.*Transaction" --glob "**/*.php"  # Distributed tx attempt
```

## Example: Order Saga

```
Order Saga: Reserve Inventory → Charge Payment → Ship Order

Step 1: Reserve Inventory
  - Action: Decrement stock
  - Compensation: Release stock (increment)

Step 2: Charge Payment
  - Action: Charge credit card
  - Compensation: Refund charge

Step 3: Ship Order
  - Action: Create shipment
  - Compensation: Cancel shipment

If Step 2 fails:
  1. Compensate Step 1 (release inventory)
  2. Mark saga as Failed
```

## References

For detailed information, load these reference files:

- `references/saga-patterns.md` — Choreography and orchestration patterns
- `references/compensation.md` — Compensating transaction strategies
- `references/antipatterns.md` — Common violations with detection patterns
- `references/php-specific.md` — PHP 8.5 specific implementations

## Assets

- `assets/report-template.md` — Structured audit report template
