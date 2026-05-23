---
name: saga-pattern-skill
description: Implements saga pattern for distributed transactions with compensating actions and rollback coordination
version: 1.0.0
tags: [orchestration, saga, transactions, compensation, rollback, distributed-systems]
---

# Saga Pattern Skill

## Purpose

This skill implements the saga pattern for managing distributed transactions across multiple agents or services. It coordinates forward progress and automatic compensation (rollback) when failures occur, ensuring data consistency without distributed locks.

## When to Use This Skill

**Use this skill when:**
- ✅ Executing multi-step workflows where partial completion is unacceptable
- ✅ Need to rollback completed steps when later steps fail
- ✅ Coordinating distributed transactions across services/agents
- ✅ Want automatic compensation without manual intervention
- ✅ Implementing workflows with side effects (deployments, API calls, database changes)

**Don't use this skill for:**
- ❌ Read-only operations (no rollback needed)
- ❌ Single-step atomic operations (use transactions instead)
- ❌ Workflows where partial success is acceptable
- ❌ Operations that cannot be compensated/undone

## Core Concepts

### Forward Flow

The normal execution path through saga steps:
```
step1 → step2 → step3 → ... → stepN
```

### Compensation Flow

The rollback path when a step fails:
```
rollback_stepN → rollback_step(N-1) → ... → rollback_step1
```

### Saga Guarantees

1. **Atomicity**: Either all steps complete, or all are compensated
2. **Isolation**: Each step is isolated, but not globally isolated
3. **Durability**: Completed steps and compensations are durable

## Implementation

### 1. Saga Coordinator

```python
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Any, Optional
from enum import Enum

class SagaStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"
    FAILED = "failed"

@dataclass
class SagaStep:
    """A single step in a saga."""
    name: str
    forward_action: Callable
    compensation_action: Callable
    status: SagaStatus = SagaStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None

@dataclass
class Saga:
    """Saga coordinator managing forward and compensation flows."""
    name: str
    steps: List[SagaStep] = field(default_factory=list)
    status: SagaStatus = SagaStatus.PENDING
    completed_steps: List[str] = field(default_factory=list)
    compensated_steps: List[str] = field(default_factory=list)

    def add_step(self, name: str, forward_action: Callable, compensation_action: Callable) -> None:
        """Add a step to the saga."""
        step = SagaStep(
            name=name,
            forward_action=forward_action,
            compensation_action=compensation_action
        )
        self.steps.append(step)

    def execute(self) -> bool:
        """
        Execute the saga.

        Returns:
            True if saga completed successfully, False if compensated
        """
        self.status = SagaStatus.IN_PROGRESS

        # Forward execution
        for step in self.steps:
            try:
                print(f"Executing step: {step.name}")
                step.status = SagaStatus.IN_PROGRESS
                step.result = step.forward_action()
                step.status = SagaStatus.COMPLETED
                self.completed_steps.append(step.name)
                print(f"✓ Step completed: {step.name}")

            except Exception as e:
                print(f"✗ Step failed: {step.name} - {str(e)}")
                step.error = e
                step.status = SagaStatus.FAILED

                # Trigger compensation for all completed steps
                self._compensate()
                return False

        # All steps completed successfully
        self.status = SagaStatus.COMPLETED
        return True

    def _compensate(self) -> None:
        """Execute compensation actions in reverse order."""
        self.status = SagaStatus.COMPENSATING
        print("\n🔄 Starting compensation (rollback)...")

        # Compensate in reverse order
        for step_name in reversed(self.completed_steps):
            step = next(s for s in self.steps if s.name == step_name)

            try:
                print(f"Compensating: {step.name}")
                step.compensation_action()
                self.compensated_steps.append(step.name)
                print(f"✓ Compensated: {step.name}")

            except Exception as e:
                print(f"✗ Compensation failed: {step.name} - {str(e)}")
                # Log critical error but continue compensating
                # In production, alert operators
                self._alert_compensation_failure(step.name, e)

        self.status = SagaStatus.COMPENSATED
        print("Compensation complete.\n")

    def _alert_compensation_failure(self, step_name: str, error: Exception) -> None:
        """Alert operators of compensation failure (critical)."""
        print(f"🚨 CRITICAL: Compensation failed for {step_name}: {error}")
        # In production: Send alert to operators, create incident ticket
```

### 2. Saga Builder Pattern

```python
class SagaBuilder:
    """Fluent interface for building sagas."""

    def __init__(self, name: str):
        self.saga = Saga(name=name)

    def add_step(self, name: str, forward: Callable, compensation: Callable) -> 'SagaBuilder':
        """Add a step with forward and compensation actions."""
        self.saga.add_step(name, forward, compensation)
        return self

    def build(self) -> Saga:
        """Build and return the saga."""
        return self.saga
```

### 3. Common Compensation Patterns

```python
class CompensationPatterns:
    """Common compensation patterns for typical operations."""

    @staticmethod
    def database_insert_compensation(table: str, record_id: str, db):
        """Compensate database insert by deleting the record."""
        def compensate():
            db.delete(table, record_id)
        return compensate

    @staticmethod
    def file_create_compensation(file_path: str):
        """Compensate file creation by deleting the file."""
        def compensate():
            import os
            if os.path.exists(file_path):
                os.remove(file_path)
        return compensate

    @staticmethod
    def api_call_compensation(rollback_endpoint: str, rollback_data: dict):
        """Compensate API call by calling rollback endpoint."""
        def compensate():
            import requests
            response = requests.post(rollback_endpoint, json=rollback_data)
            response.raise_for_status()
        return compensate

    @staticmethod
    def state_change_compensation(previous_state: Any, state_setter: Callable):
        """Compensate state change by restoring previous state."""
        def compensate():
            state_setter(previous_state)
        return compensate
```

## Workflow

### Step 1: Define Saga Steps

```python
# Example: Multi-service deployment saga

def deploy_database():
    """Deploy database schema changes."""
    print("Deploying database schema...")
    # Execute database migration
    return {"db_version": "1.2.0"}

def rollback_database():
    """Rollback database schema changes."""
    print("Rolling back database schema...")
    # Execute rollback migration

def deploy_api_service():
    """Deploy API service."""
    print("Deploying API service...")
    # Deploy new API version
    return {"api_version": "2.0.0"}

def rollback_api_service():
    """Rollback API service."""
    print("Rolling back API service...")
    # Deploy previous API version

def deploy_frontend():
    """Deploy frontend application."""
    print("Deploying frontend...")
    # Deploy new frontend version
    return {"frontend_version": "3.1.0"}

def rollback_frontend():
    """Rollback frontend application."""
    print("Rolling back frontend...")
    # Deploy previous frontend version

def notify_users():
    """Send notification to users."""
    print("Notifying users of deployment...")
    # Send email/notification
    return {"notification_sent": True}

def compensate_notification():
    """Send rollback notification."""
    print("Notifying users of rollback...")
    # Send rollback notification
```

### Step 2: Build Saga

```python
saga = (
    SagaBuilder("deployment-saga")
    .add_step("deploy-database", deploy_database, rollback_database)
    .add_step("deploy-api", deploy_api_service, rollback_api_service)
    .add_step("deploy-frontend", deploy_frontend, rollback_frontend)
    .add_step("notify-users", notify_users, compensate_notification)
    .build()
)
```

### Step 3: Execute Saga

```python
success = saga.execute()

if success:
    print("✅ Saga completed successfully")
else:
    print("❌ Saga failed and was compensated")
```

### Step 4: Handle Results

```python
# Check saga status
if saga.status == SagaStatus.COMPLETED:
    # Extract results from each step
    results = {step.name: step.result for step in saga.steps}
    print(f"Deployment successful: {results}")

elif saga.status == SagaStatus.COMPENSATED:
    # Saga was rolled back
    print(f"Deployment failed. Rolled back {len(saga.compensated_steps)} steps.")

    # Find failed step
    failed_step = next((s for s in saga.steps if s.status == SagaStatus.FAILED), None)
    if failed_step:
        print(f"Failed at: {failed_step.name} - {failed_step.error}")
```

## Advanced Patterns

### 1. Saga with Conditional Steps

```python
def execute_with_conditions(saga: Saga, context: Dict) -> bool:
    """Execute saga with conditional step execution."""
    saga.status = SagaStatus.IN_PROGRESS

    for step in saga.steps:
        # Check if step should execute (based on context/previous results)
        if not should_execute_step(step, context):
            print(f"Skipping step: {step.name}")
            continue

        try:
            step.result = step.forward_action()
            step.status = SagaStatus.COMPLETED
            saga.completed_steps.append(step.name)

            # Update context for next steps
            context[step.name] = step.result

        except Exception as e:
            step.error = e
            saga._compensate()
            return False

    saga.status = SagaStatus.COMPLETED
    return True
```

### 2. Saga with Parallel Steps

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def execute_parallel_batch(steps: List[SagaStep]) -> List[SagaStep]:
    """Execute multiple independent steps in parallel."""
    failed_steps = []

    with ThreadPoolExecutor(max_workers=len(steps)) as executor:
        # Submit all steps
        future_to_step = {
            executor.submit(step.forward_action): step
            for step in steps
        }

        # Collect results
        for future in as_completed(future_to_step):
            step = future_to_step[future]
            try:
                step.result = future.result()
                step.status = SagaStatus.COMPLETED
            except Exception as e:
                step.error = e
                step.status = SagaStatus.FAILED
                failed_steps.append(step)

    return failed_steps
```

### 3. Saga with Timeout

```python
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds: int):
    """Context manager for timeout."""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {seconds} seconds")

    original_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)

def execute_with_timeout(saga: Saga, step_timeout: int = 300) -> bool:
    """Execute saga with per-step timeout."""
    saga.status = SagaStatus.IN_PROGRESS

    for step in saga.steps:
        try:
            with timeout(step_timeout):
                step.result = step.forward_action()
                step.status = SagaStatus.COMPLETED
                saga.completed_steps.append(step.name)

        except TimeoutError as e:
            step.error = e
            step.status = SagaStatus.FAILED
            saga._compensate()
            return False

        except Exception as e:
            step.error = e
            step.status = SagaStatus.FAILED
            saga._compensate()
            return False

    saga.status = SagaStatus.COMPLETED
    return True
```

### 4. Saga with State Persistence

```python
import json
from typing import IO

class PersistentSaga(Saga):
    """Saga that persists state for recovery after failures."""

    def __init__(self, name: str, state_file: str):
        super().__init__(name)
        self.state_file = state_file
        self._load_state()

    def _save_state(self) -> None:
        """Persist saga state to disk."""
        state = {
            "name": self.name,
            "status": self.status.value,
            "completed_steps": self.completed_steps,
            "compensated_steps": self.compensated_steps
        }

        with open(self.state_file, 'w') as f:
            json.dump(state, f)

    def _load_state(self) -> None:
        """Load saga state from disk (if exists)."""
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                self.status = SagaStatus(state["status"])
                self.completed_steps = state["completed_steps"]
                self.compensated_steps = state["compensated_steps"]
        except FileNotFoundError:
            pass  # No previous state

    def execute(self) -> bool:
        """Execute saga with state persistence."""
        result = super().execute()
        self._save_state()
        return result
```

## Integration Patterns

### With Resilience Orchestrator

```python
# Resilience Orchestrator uses saga for multi-step workflows
from skills.orchestration.saga_pattern import Saga, SagaBuilder

class ResilientWorkflow:
    def __init__(self):
        self.saga = None

    def execute_deployment(self):
        """Execute deployment with automatic rollback on failure."""

        # Build deployment saga
        self.saga = (
            SagaBuilder("deployment")
            .add_step("backup", self.backup_database, self.restore_database)
            .add_step("deploy", self.deploy_services, self.rollback_services)
            .add_step("verify", self.verify_deployment, self.noop)
            .add_step("notify", self.notify_completion, self.notify_rollback)
            .build()
        )

        # Execute with automatic compensation on failure
        success = self.saga.execute()

        return success
```

### With DAG Orchestrator

```python
# Each DAG task can be part of a saga
def create_dag_with_saga(tasks: List[Task]) -> Saga:
    """Create saga from DAG tasks."""

    saga_builder = SagaBuilder("dag-execution")

    for task in tasks:
        saga_builder.add_step(
            name=task.id,
            forward=lambda: execute_task(task),
            compensation=lambda: rollback_task(task)
        )

    return saga_builder.build()
```

## Examples

### Example 1: E-Commerce Order Saga

```python
# Saga for order processing with multiple services

class OrderSaga:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.reservation_id = None
        self.payment_id = None

    def reserve_inventory(self):
        """Reserve items in inventory."""
        self.reservation_id = inventory_service.reserve(self.order_id)
        return self.reservation_id

    def cancel_reservation(self):
        """Cancel inventory reservation."""
        inventory_service.cancel(self.reservation_id)

    def process_payment(self):
        """Process customer payment."""
        self.payment_id = payment_service.charge(self.order_id)
        return self.payment_id

    def refund_payment(self):
        """Refund customer payment."""
        payment_service.refund(self.payment_id)

    def ship_order(self):
        """Ship the order."""
        tracking_id = shipping_service.ship(self.order_id)
        return tracking_id

    def cancel_shipment(self):
        """Cancel shipment."""
        # Note: May not be possible if already shipped
        shipping_service.cancel(self.order_id)

    def execute(self):
        """Execute order saga."""
        saga = (
            SagaBuilder(f"order-{self.order_id}")
            .add_step("reserve-inventory", self.reserve_inventory, self.cancel_reservation)
            .add_step("process-payment", self.process_payment, self.refund_payment)
            .add_step("ship-order", self.ship_order, self.cancel_shipment)
            .build()
        )

        return saga.execute()

# Usage
order_saga = OrderSaga(order_id="ORD-12345")
success = order_saga.execute()
# If any step fails, all completed steps are automatically compensated
```

### Example 2: Multi-Agent Workflow Saga

```python
# Saga for multi-agent feature implementation

def create_feature_saga(feature_spec):
    """Create saga for feature implementation across agents."""

    # Agent outputs
    design_doc = None
    implementation = None
    tests = None

    def architect_design():
        nonlocal design_doc
        design_doc = architect_agent.design(feature_spec)
        return design_doc

    def delete_design():
        file_system.delete(design_doc.path)

    def builder_implement():
        nonlocal implementation
        implementation = builder_agent.implement(design_doc)
        return implementation

    def delete_implementation():
        file_system.delete(implementation.path)

    def validator_test():
        nonlocal tests
        tests = validator_agent.create_tests(implementation)
        return tests

    def delete_tests():
        file_system.delete(tests.path)

    def scribe_document():
        docs = scribe_agent.document(implementation)
        return docs

    def delete_documentation():
        # Compensation for documentation (if needed)
        pass

    saga = (
        SagaBuilder("feature-implementation")
        .add_step("design", architect_design, delete_design)
        .add_step("implement", builder_implement, delete_implementation)
        .add_step("test", validator_test, delete_tests)
        .add_step("document", scribe_document, delete_documentation)
        .build()
    )

    return saga.execute()
```

## Error Handling

### Compensation Failure

```python
# Critical scenario: Compensation itself fails

def handle_compensation_failure(saga: Saga):
    """Handle scenario where compensation fails."""

    failed_compensations = []

    for step_name in saga.compensated_steps:
        step = next(s for s in saga.steps if s.name == step_name)
        if step.error:
            failed_compensations.append(step)

    if failed_compensations:
        # Generate manual intervention report
        report = generate_intervention_report(saga, failed_compensations)

        # Alert operators
        alert_operators(
            severity="critical",
            title=f"Compensation failed for saga: {saga.name}",
            body=report
        )

        # Create incident ticket
        create_incident(
            title=f"Manual intervention required: {saga.name}",
            description=report,
            priority="P0"
        )
```

### Partial Compensation

```python
def analyze_partial_compensation(saga: Saga):
    """Analyze saga that partially compensated."""

    completed = set(saga.completed_steps)
    compensated = set(saga.compensated_steps)

    partially_compensated = completed - compensated

    if partially_compensated:
        print("⚠️ WARNING: Partial compensation")
        print(f"Completed steps: {completed}")
        print(f"Compensated steps: {compensated}")
        print(f"NOT compensated: {partially_compensated}")

        # Manual intervention needed
        return {
            "status": "partial_compensation",
            "manual_steps": list(partially_compensated)
        }
```

## Best Practices

1. **Make Compensations Idempotent**
   ```python
   def idempotent_compensation():
       """Compensation that can be called multiple times safely."""
       if resource_exists():
           delete_resource()
       # No error if resource already deleted
   ```

2. **Log All Saga Operations**
   ```python
   def execute_with_logging(saga: Saga):
       logger.info(f"Starting saga: {saga.name}")

       for step in saga.steps:
           logger.info(f"Executing step: {step.name}")
           # ... execute step
           logger.info(f"Step result: {step.result}")

       logger.info(f"Saga final status: {saga.status}")
   ```

3. **Test Compensation Paths**
   ```python
   def test_compensation():
       """Test that compensation works correctly."""
       saga = build_test_saga()

       # Force failure at step 3
       saga.steps[2].forward_action = lambda: (_ for _ in ()).throw(Exception("Test failure"))

       success = saga.execute()

       assert not success
       assert saga.status == SagaStatus.COMPENSATED
       assert len(saga.compensated_steps) == 2  # Steps 1 and 2 compensated
   ```

4. **Handle Uncompensatable Operations**
   ```python
   # Some operations cannot be compensated (e.g., sending email)
   def uncompensatable_step():
       send_email()  # Cannot un-send email

   def compensate_uncompensatable():
       # Best effort: Send corrective email
       send_correction_email("Previous email was sent in error")
   ```

5. **Use Timeouts**
   ```python
   saga_with_timeout = execute_with_timeout(saga, step_timeout=300)
   # Prevents saga from hanging indefinitely
   ```

## Related Skills

- `resilience-orchestrator-skill`: Uses saga for fault-tolerant workflows
- `dag-orchestrator-skill`: Each DAG can be wrapped in saga
- `circuit-breaker-skill`: Combined with saga for enhanced resilience

## References

- [Saga Pattern (Microsoft)](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga)
- Document 15, Section 5: Advanced Error Handling
- Command: `/fault-tolerant-orchestrator`

---

**Version**: 1.0.0
**Status**: Production Ready
**Complexity**: High (distributed transaction management)
**Token Cost**: Low (coordination overhead only)
