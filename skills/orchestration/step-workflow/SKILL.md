---
name: synapse-step-workflow
description: Explains step-based workflow system for Synapse plugin actions. Use when the user mentions "BaseStep", "StepRegistry", "Orchestrator", "StepResult", "BaseStepContext", "step-based workflow", "workflow steps", "rollback", "progress_weight", or needs help with multi-step action development.
---

# Step-based Workflow System

Synapse SDK provides a step-based workflow system for complex actions that need:
- Multi-phase execution with progress tracking
- Automatic rollback on failure
- State sharing between steps
- Conditional step execution

## Core Components

| Component | Purpose |
|-----------|---------|
| `BaseStep` | Abstract step definition |
| `StepResult` | Step execution result |
| `StepRegistry` | Ordered step registration |
| `Orchestrator` | Step execution with rollback |
| `BaseStepContext` | State sharing between steps |

## Quick Start

```python
from dataclasses import dataclass, field
from synapse_sdk.plugins.steps import (
    BaseStep,
    StepResult,
    StepRegistry,
    Orchestrator,
    BaseStepContext,
)
from synapse_sdk.plugins.context import RuntimeContext

# 1. Define context for state sharing
@dataclass
class ProcessContext(BaseStepContext):
    data: list = field(default_factory=list)
    processed: int = 0

# 2. Define steps
class LoadStep(BaseStep[ProcessContext]):
    @property
    def name(self) -> str:
        return 'load'

    @property
    def progress_weight(self) -> float:
        return 0.3

    def execute(self, ctx: ProcessContext) -> StepResult:
        ctx.data = load_data()
        return StepResult(success=True, data={'count': len(ctx.data)})

class ProcessStep(BaseStep[ProcessContext]):
    @property
    def name(self) -> str:
        return 'process'

    @property
    def progress_weight(self) -> float:
        return 0.7

    def execute(self, ctx: ProcessContext) -> StepResult:
        for item in ctx.data:
            process(item)
            ctx.processed += 1
            ctx.set_progress(ctx.processed, len(ctx.data))
        return StepResult(success=True)

# 3. Register and run
registry = StepRegistry[ProcessContext]()
registry.register(LoadStep())
registry.register(ProcessStep())

context = ProcessContext(runtime_ctx=runtime_ctx)
orchestrator = Orchestrator(registry, context)
result = orchestrator.execute()
```

## Using with Specialized Actions

Override `setup_steps()` in specialized actions:

```python
from synapse_sdk.plugins.actions.train import BaseTrainAction, TrainContext
from synapse_sdk.plugins.steps import StepRegistry

class MyTrainAction(BaseTrainAction[TrainParams]):
    def setup_steps(self, registry: StepRegistry[TrainContext]) -> None:
        registry.register(LoadDatasetStep())
        registry.register(TrainStep())
        registry.register(UploadModelStep())
```

## Workflow Features

### Automatic Progress Tracking

Progress is calculated based on step weights:

```python
# Total weight = 0.2 + 0.6 + 0.2 = 1.0
LoadStep()    # progress_weight = 0.2 -> 0-20%
TrainStep()   # progress_weight = 0.6 -> 20-80%
UploadStep()  # progress_weight = 0.2 -> 80-100%
```

### Automatic Rollback

On failure, executed steps are rolled back in reverse order:

```python
class UploadStep(BaseStep[UploadContext]):
    def execute(self, ctx: UploadContext) -> StepResult:
        ctx.uploaded_files = upload_files()
        return StepResult(success=True)

    def rollback(self, ctx: UploadContext, result: StepResult) -> None:
        for file in ctx.uploaded_files:
            delete_file(file)
```

### Conditional Execution

Skip steps based on context:

```python
class OptionalStep(BaseStep[MyContext]):
    def can_skip(self, ctx: MyContext) -> bool:
        return not ctx.params.get('enable_validation', True)
```

## Detailed References

- **[references/step-classes.md](references/step-classes.md)** - BaseStep, StepResult, StepRegistry
- **[references/orchestrator.md](references/orchestrator.md)** - Orchestrator usage
- **[references/contexts.md](references/contexts.md)** - BaseStepContext and specialized contexts
