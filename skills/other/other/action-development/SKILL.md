---
name: synapse-action-development
description: Explains how to create Synapse plugin actions. Use when the user asks to "create an action", "write an action", uses "@action decorator", "BaseAction class", "function-based action", "class-based action", "Pydantic params", "ActionPipeline", "DataType", "input_type", "output_type", "semantic types", "YOLODataset", "ModelWeights", "pipeline chaining", or needs help with synapse plugin action development.
---

# Synapse Action Development

Synapse SDK provides two patterns for plugin actions: **function-based** (simple, stateless) and **class-based** (complex, stateful).

## Quick Start: Function-Based Action

```python
from pydantic import BaseModel
from synapse_sdk.plugins.decorators import action
from synapse_sdk.plugins.context import RuntimeContext

class TrainParams(BaseModel):
    epochs: int = 10
    learning_rate: float = 0.001

@action(name='train', description='Train a model', params=TrainParams)
def train(params: TrainParams, ctx: RuntimeContext) -> dict:
    for epoch in range(params.epochs):
        ctx.set_progress(epoch + 1, params.epochs)
    return {'status': 'completed'}
```

## Quick Start: Class-Based Action

```python
from pydantic import BaseModel
from synapse_sdk.plugins.action import BaseAction

class InferParams(BaseModel):
    model_path: str
    threshold: float = 0.5

class InferAction(BaseAction[InferParams]):
    action_name = 'inference'

    def execute(self) -> dict:
        self.set_progress(0, 100)
        # Implementation here
        return {'predictions': []}
```

## When to Use Each Pattern

| Criteria | Function-Based | Class-Based |
|----------|----------------|-------------|
| Complexity | Simple, single-purpose | Complex, multi-step |
| State | Stateless | Can use helper methods |
| Semantic types | Limited | Full support |

**Recommendation**: Start with function-based. Use class-based when needing helper methods or semantic type declarations.

## @action Decorator Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | No | Action name (defaults to function name) |
| `description` | No | Human-readable description |
| `params` | No | Pydantic model for parameter validation |
| `result` | No | Pydantic model for result validation |
| `category` | No | PluginCategory for grouping |

### Category Parameter Examples

```python
from synapse_sdk.plugins.decorators import action
from synapse_sdk.plugins.constants import PluginCategory

# Training action
@action(
    name='train',
    category=PluginCategory.NEURAL_NET,
    description='Train object detection model'
)
def train(params, ctx):
    ...

# Export action
@action(
    name='export_coco',
    category=PluginCategory.EXPORT,
    description='Export to COCO format'
)
def export_coco(params, ctx):
    ...

# Smart tool (AI-assisted annotation)
@action(
    name='auto_segment',
    category=PluginCategory.SMART_TOOL,
    description='Auto-segmentation tool'
)
def auto_segment(params, ctx):
    ...

# Pre-annotation
@action(
    name='pre_label',
    category=PluginCategory.PRE_ANNOTATION,
    description='Pre-label with model predictions'
)
def pre_label(params, ctx):
    ...
```

**Available Categories**: `NEURAL_NET`, `EXPORT`, `UPLOAD`, `SMART_TOOL`, `PRE_ANNOTATION`, `POST_ANNOTATION`, `DATA_VALIDATION`, `CUSTOM`

## BaseAction Class Attributes

| Attribute | Description |
|-----------|-------------|
| `action_name` | Action name for invocation |
| `category` | PluginCategory |
| `input_type` | Semantic input type for pipelines |
| `output_type` | Semantic output type for pipelines |
| `params_model` | Auto-extracted from generic |
| `result_model` | Optional result schema |

## Available Methods in BaseAction

- `self.params` - Validated parameters
- `self.ctx` - RuntimeContext
- `self.logger` - Logger shortcut
- `self.set_progress(current, total, category)` - Progress tracking
- `self.set_metrics(value, category)` - Metrics recording
- `self.log(event, data, file)` - Event logging

## Additional Resources

For detailed patterns and advanced techniques:
- **[references/patterns.md](references/patterns.md)** - Parameter validation, semantic types
- **[references/categories.md](references/categories.md)** - Available PluginCategory values
- **[references/types-hierarchy.md](references/types-hierarchy.md)** - Semantic type system (DataType, Dataset, Model)
- **[references/pipelines.md](references/pipelines.md)** - ActionPipeline for chaining actions
