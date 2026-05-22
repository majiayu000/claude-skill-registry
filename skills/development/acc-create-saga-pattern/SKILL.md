---
name: acc-create-saga-pattern
description: Generates Saga pattern components for PHP 8.5. Creates Saga interfaces, steps, orchestrator, state management, and compensation logic with unit tests.
---

# Saga Pattern Generator

Creates Saga pattern infrastructure for distributed transaction coordination.

## When to Use

- Distributed transactions across multiple services
- Long-running business processes
- Operations requiring compensation on failure
- Multi-step workflows with rollback capability

## Component Characteristics

### SagaState Enum
- Domain layer enum
- Defines saga lifecycle states: Pending, Running, Compensating, Completed, Failed, CompensationFailed
- Includes state transition validation
- Terminal states detection

### SagaStep Interface
- Domain layer interface
- Execute and compensate methods
- Idempotency declaration
- Timeout configuration

### SagaContext
- Carries saga execution data
- Serializable for persistence
- Supports data accumulation across steps

### SagaOrchestrator
- Application layer coordinator
- Manages step execution
- Handles compensation flow (reverse order)
- Persists state after each step

### SagaPersistence
- Stores saga state for recovery
- Supports finding incomplete sagas
- Dead letter handling

---

## Generation Process

### Step 1: Analyze Request

Determine:
- Context name (Order, Payment, Shipping)
- Required saga steps
- Compensation logic for each step

### Step 2: Generate Core Components

Create in this order:

1. **Domain Layer** (`src/Domain/Shared/Saga/`)
   - `SagaState.php` — State enum with transitions
   - `StepResult.php` — Step result value object
   - `SagaStepInterface.php` — Step contract
   - `SagaContext.php` — Execution context
   - `SagaResult.php` — Saga result
   - Exception classes

2. **Application Layer** (`src/Application/Shared/Saga/`)
   - `SagaPersistenceInterface.php` — Persistence port
   - `SagaRecord.php` — Persisted record
   - `AbstractSagaStep.php` — Base step class
   - `SagaOrchestrator.php` — Orchestrator

3. **Infrastructure Layer**
   - `DoctrineSagaPersistence.php` — Doctrine implementation
   - Database migration

4. **Tests**
   - `SagaStateTest.php`
   - `SagaOrchestratorTest.php`

### Step 3: Generate Context-Specific Steps

For each saga step (e.g., Order saga):

```
src/Application/{Context}/Saga/Step/
├── ReserveInventoryStep.php
├── ChargePaymentStep.php
└── CreateShipmentStep.php

src/Application/{Context}/Saga/
└── {Context}SagaFactory.php
```

---

## File Placement

| Layer | Path |
|-------|------|
| Domain Types | `src/Domain/Shared/Saga/` |
| Application Saga | `src/Application/Shared/Saga/` |
| Context Steps | `src/Application/{Context}/Saga/Step/` |
| Saga Factory | `src/Application/{Context}/Saga/` |
| Infrastructure | `src/Infrastructure/Persistence/Doctrine/Repository/` |
| Unit Tests | `tests/Unit/{Layer}/{Path}/` |

---

## Key Principles

### Compensation Rules
1. Compensate in **reverse order** of execution
2. Compensations must be **idempotent**
3. Handle "already compensated" gracefully
4. Log all compensation attempts

### Idempotency
1. Use idempotency keys for each step
2. Check for existing results before executing
3. Return existing result if found

### State Transitions
```
Pending → Running → Completed
              ↓
         Compensating → Failed
              ↓
         CompensationFailed
```

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| State Enum | `SagaState` | `SagaState` |
| Step Interface | `SagaStepInterface` | `SagaStepInterface` |
| Abstract Step | `AbstractSagaStep` | `AbstractSagaStep` |
| Concrete Step | `{Action}Step` | `ReserveInventoryStep` |
| Orchestrator | `SagaOrchestrator` | `SagaOrchestrator` |
| Factory | `{Name}SagaFactory` | `OrderSagaFactory` |
| Test | `{ClassName}Test` | `SagaOrchestratorTest` |

---

## Quick Template Reference

### SagaStepInterface

```php
interface SagaStepInterface
{
    public function name(): string;
    public function execute(SagaContext $context): StepResult;
    public function compensate(SagaContext $context): StepResult;
    public function isIdempotent(): bool;
    public function timeout(): int;
}
```

### StepResult

```php
final readonly class StepResult
{
    public static function success(array $data = []): self;
    public static function failure(string $error): self;
    public function isSuccess(): bool;
    public function isFailure(): bool;
}
```

### Concrete Step Pattern

```php
final readonly class {Action}Step extends AbstractSagaStep
{
    public function name(): string
    {
        return '{action_name}';
    }

    public function execute(SagaContext $context): StepResult
    {
        $idempotencyKey = $this->idempotencyKey($context);

        // Check for existing result (idempotency)
        // Execute action
        // Return StepResult::success([...data...]) or failure
    }

    public function compensate(SagaContext $context): StepResult
    {
        // Get data from context
        // Undo action
        // Handle "already undone" gracefully
        return StepResult::success();
    }
}
```

---

## Usage Example

```php
// Create saga
$saga = $orderSagaFactory->create($command);

// Execute
$result = $saga->execute();

if ($result->isCompleted()) {
    // Success
} elseif ($result->isFailed()) {
    // Failed but compensated
    $error = $result->error;
} elseif ($result->isCompensationFailed()) {
    // Needs manual intervention
    $originalError = $result->error;
    $compensationError = $result->compensationError;
}
```

---

## DI Configuration

```yaml
# Symfony services.yaml
Domain\Shared\Saga\SagaStepInterface:
    tags: ['saga.step']

Application\Shared\Saga\SagaPersistenceInterface:
    alias: Infrastructure\Persistence\Doctrine\Repository\DoctrineSagaPersistence

Application\Order\Saga\OrderSagaFactory:
    arguments:
        $reserveStep: '@Application\Order\Saga\Step\ReserveInventoryStep'
        $chargeStep: '@Application\Order\Saga\Step\ChargePaymentStep'
        $shipStep: '@Application\Order\Saga\Step\CreateShipmentStep'
```

---

## Database Schema

```sql
CREATE TABLE sagas (
    id VARCHAR(255) PRIMARY KEY,
    type VARCHAR(255) NOT NULL,
    state VARCHAR(50) NOT NULL,
    completed_steps JSONB NOT NULL DEFAULT '[]',
    context JSONB NOT NULL,
    error TEXT,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    completed_at TIMESTAMP(6)
);

CREATE INDEX idx_sagas_state ON sagas (state);
CREATE INDEX idx_sagas_type_state ON sagas (type, state);
```

---

## References

For complete PHP templates and test examples, see:
- `references/templates.md` — All component templates
- `references/examples.md` — Order saga example and unit tests
