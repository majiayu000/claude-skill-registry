---
name: synapse-runtime-context-api
description: Explains how to use Synapse RuntimeContext API. Use when the user asks about "RuntimeContext", "ctx.", "logging", "progress tracking", "set_progress", "set_metrics", "log_message", "BaseStepContext", "TrainContext", "ExportContext", "UploadContext", "InferenceContext", "AddTaskDataContext", or needs help with synapse plugin context and logging.
---

# Synapse RuntimeContext API

RuntimeContext provides logging, progress tracking, and client access for plugin actions.

## Quick Reference

```python
from synapse_sdk.plugins.context import RuntimeContext

def train(params: TrainParams, ctx: RuntimeContext) -> dict:
    # Progress tracking
    ctx.set_progress(0, 100)

    # Metrics recording
    ctx.set_metrics({'loss': 0.05}, 'training')

    # User-facing message
    ctx.log_message('Training started', 'info')

    # Event logging
    ctx.log('checkpoint', {'epoch': 5}, '/path/to/file')

    # Debug logging
    ctx.log_dev_event('Debug info', {'data': 'value'})

    # Signal completion
    ctx.end_log()

    return {'status': 'completed'}
```

## Context Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `ctx.logger` | BaseLogger | Logger instance |
| `ctx.env` | PluginEnvironment | Environment variables |
| `ctx.job_id` | str \| None | Job tracking ID |
| `ctx.client` | BackendClient \| None | API client |
| `ctx.agent_client` | AgentClient \| None | Ray operations client |
| `ctx.checkpoint` | dict \| None | Pretrained model info |

## Progress Tracking

```python
# Basic progress
ctx.set_progress(current=50, total=100)

# Progress with category (multi-phase)
ctx.set_progress(5, 10, category='download')
ctx.set_progress(3, 100, category='training')
```

## Metrics Recording

```python
ctx.set_metrics(
    value={'loss': 0.05, 'accuracy': 0.95},
    category='training'
)
```

## Logging Methods

| Method | Description |
|--------|-------------|
| `log(event, data, file)` | Log event with data |
| `log_message(message, context)` | User-facing message |
| `log_dev_event(message, data)` | Debug/dev event |
| `end_log()` | Signal completion |

## Message Contexts

```python
ctx.log_message('Success!', 'success')   # Green
ctx.log_message('Warning', 'warning')    # Yellow
ctx.log_message('Error', 'danger')       # Red
ctx.log_message('Info', 'info')          # Blue (default)
```

## Environment Access

```python
# Get environment variable
api_key = ctx.env.get('API_KEY', '')
debug_mode = ctx.env.get('DEBUG', 'false') == 'true'
```

## Checkpoint Info

```python
if ctx.checkpoint:
    model_path = ctx.checkpoint.get('path')
    category = ctx.checkpoint.get('category')  # 'base' or fine-tuned
```

## Specialized Step Contexts

For step-based workflows, specialized contexts extend `BaseStepContext`:

```python
from synapse_sdk.plugins.actions.train import TrainContext
from synapse_sdk.plugins.actions.export import ExportContext
from synapse_sdk.plugins.actions.upload import UploadContext
from synapse_sdk.plugins.actions.inference import InferenceContext, DeploymentContext
from synapse_sdk.plugins.actions.add_task_data import AddTaskDataContext
```

| Context | Purpose | Key Attributes |
|---------|---------|----------------|
| `TrainContext` | Training workflows | `dataset`, `model_path`, `model` |
| `ExportContext` | Export workflows | `results`, `exported_count`, `output_path` |
| `UploadContext` | Upload workflows | `uploaded_files`, `data_units` |
| `InferenceContext` | Inference workflows | `model`, `results`, `processed_count` |
| `DeploymentContext` | Deployment workflows | `serve_app_id`, `deployed` |
| `AddTaskDataContext` | Pre-annotation workflows | `task_ids`, `success_count`, `failures` |

All step contexts include:
- `runtime_ctx` - Reference to RuntimeContext
- `set_progress()` / `set_metrics()` - Auto-uses step name as category
- `log()` - Event logging

See [step-workflow skill](../step-workflow/SKILL.md) for details.

## Additional Resources

For advanced patterns:
- **[references/logging-patterns.md](references/logging-patterns.md)** - Advanced logging
- **[references/specialized-contexts.md](references/specialized-contexts.md)** - Step context details
