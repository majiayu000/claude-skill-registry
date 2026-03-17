---
name: synapse-specialized-actions
description: Explains specialized Synapse action classes for specific workflows. Use when the user mentions "BaseTrainAction", "BaseExportAction", "BaseUploadAction", "BaseInferenceAction", "BaseDeploymentAction", "AddTaskDataAction", "train action", "export action", "upload action", "inference action", "deployment action", "pre-annotation", "add_task_data", "autolog", "get_dataset", "create_model", or needs workflow-specific action development help.
---

# Specialized Action Classes

Synapse SDK provides specialized base classes for common ML workflows. Each extends `BaseAction` with workflow-specific helper methods and default settings.

## Available Specialized Actions

| Class | Category | Purpose |
|-------|----------|---------|
| `BaseTrainAction` | `NEURAL_NET` | Training models |
| `BaseExportAction` | `EXPORT` | Exporting data |
| `BaseUploadAction` | `UPLOAD` | Uploading files |
| `BaseInferenceAction` | `NEURAL_NET` | Running inference |
| `BaseDeploymentAction` | - | Ray Serve deployment |
| `AddTaskDataAction` | `PRE_ANNOTATION` | Pre-annotation workflows |

## Quick Comparison

```python
# Training - autolog, get_dataset, create_model
class TrainAction(BaseTrainAction[TrainParams]):
    def execute(self) -> dict:
        self.autolog('ultralytics')  # Auto-log metrics
        dataset = self.get_dataset()
        # ... train ...
        return self.create_model('./model.pt')

# Export - get_filtered_results
class ExportAction(BaseExportAction[ExportParams]):
    def get_filtered_results(self, filters: dict) -> tuple[Any, int]:
        return self.client.get_assignments(filters)

# Upload - step-based workflow required
class UploadAction(BaseUploadAction[UploadParams]):
    def setup_steps(self, registry: StepRegistry[UploadContext]) -> None:
        registry.register(InitStep())
        registry.register(UploadFilesStep())

# Inference - download_model, load_model, infer
class InferAction(BaseInferenceAction[InferParams]):
    def execute(self) -> dict:
        model = self.load_model(self.params.model_id)
        return {'predictions': self.infer(model, self.params.inputs)}

# Pre-annotation - convert_data_from_file, convert_data_from_inference
class PreAnnotateAction(AddTaskDataAction):
    def convert_data_from_file(self, primary_url, ...) -> dict:
        return {'annotations': [...]}
```

## Execution Modes

All specialized actions (except Deployment) support two modes:

1. **Simple Execute**: Override `execute()` for straightforward workflows
2. **Step-based**: Override `setup_steps()` for complex multi-step workflows with rollback

```python
# Simple mode
class SimpleTrainAction(BaseTrainAction[Params]):
    def execute(self) -> dict:
        return {'weights_path': '/model.pt'}

# Step-based mode
class StepTrainAction(BaseTrainAction[Params]):
    def setup_steps(self, registry: StepRegistry[TrainContext]) -> None:
        registry.register(LoadDatasetStep())
        registry.register(TrainStep())
        registry.register(UploadModelStep())
```

## Detailed References

- **[references/train-action.md](references/train-action.md)** - Training workflows with autolog, checkpoints
- **[references/export-action.md](references/export-action.md)** - Data export workflows
- **[references/upload-action.md](references/upload-action.md)** - File upload with step workflow
- **[references/inference-action.md](references/inference-action.md)** - Model inference and deployment
- **[references/add-task-data-action.md](references/add-task-data-action.md)** - Pre-annotation workflows
- **[references/progress-categories.md](references/progress-categories.md)** - Progress category constants
