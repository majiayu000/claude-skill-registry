---
name: synapse-result-schemas
description: Explains result schema classes for Synapse plugin actions. Use when the user mentions "TrainResult", "InferenceResult", "ExportResult", "UploadResult", "WeightsResult", "MetricsResult", "result_model", "result schema", or needs help with action return type validation.
---

# Result Schemas

Synapse SDK provides standardized result schema classes for common action outputs. These provide type-safe, validated return types for actions.

## Available Result Schemas

```python
from synapse_sdk.plugins.schemas import (
    TrainResult,
    InferenceResult,
    ExportResult,
    UploadResult,
    WeightsResult,
    MetricsResult,
)
```

| Schema | Purpose |
|--------|---------|
| `TrainResult` | Training output with weights and metrics |
| `InferenceResult` | Inference predictions |
| `ExportResult` | Data export output |
| `UploadResult` | File upload results |
| `WeightsResult` | Model weights only |
| `MetricsResult` | Evaluation metrics only |

## Quick Usage

### With Class-Based Actions

```python
from synapse_sdk.plugins.actions.train import BaseTrainAction
from synapse_sdk.plugins.schemas import TrainResult

class MyTrainAction(BaseTrainAction[TrainParams]):
    result_model = TrainResult  # Enable result validation

    def execute(self) -> TrainResult:
        # ... training ...
        return TrainResult(
            weights_path='/models/best.pt',
            final_epoch=100,
            train_metrics={'loss': 0.05},
            val_metrics={'mAP50': 0.85},
        )
```

### With Function-Based Actions

```python
from synapse_sdk.plugins.decorators import action
from synapse_sdk.plugins.schemas import InferenceResult

@action(name='infer', result=InferenceResult)
def infer(params: InferParams, ctx: RuntimeContext) -> InferenceResult:
    return InferenceResult(
        predictions=[{'class': 'dog', 'confidence': 0.95}],
        processed_count=100,
    )
```

## Schema Details

### TrainResult

```python
class TrainResult(BaseModel):
    weights_path: str            # Path to trained model
    final_epoch: int             # Last completed epoch
    best_epoch: int | None       # Best epoch by val metric
    train_metrics: dict = {}     # Final training metrics
    val_metrics: dict = {}       # Final validation metrics
```

### InferenceResult

```python
class InferenceResult(BaseModel):
    predictions: list[dict] = [] # Prediction results
    processed_count: int = 0     # Items processed
    output_path: str | None      # Output file path
```

### ExportResult

```python
class ExportResult(BaseModel):
    output_path: str             # Export path
    exported_count: int          # Items exported
    format: str                  # Export format
    file_size_bytes: int | None  # File size
```

### UploadResult

```python
class UploadResult(BaseModel):
    uploaded_count: int          # Items uploaded
    remote_path: str | None      # Remote URL/path
    status: str = 'completed'    # Upload status
```

### WeightsResult

```python
class WeightsResult(BaseModel):
    weights_path: str            # Best/final weights path
    checkpoint_paths: list = []  # Intermediate checkpoints
    format: str = 'pt'           # Weights format
```

### MetricsResult

```python
class MetricsResult(BaseModel):
    metrics: dict[str, float]    # Metric values
    category: str = 'default'    # Metrics category
```

## Detailed References

- **[references/train-result.md](references/train-result.md)** - TrainResult, WeightsResult
- **[references/inference-result.md](references/inference-result.md)** - InferenceResult
- **[references/other-results.md](references/other-results.md)** - ExportResult, UploadResult, MetricsResult
