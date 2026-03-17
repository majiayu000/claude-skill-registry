---
name: synapse-config-yaml-guide
description: Explains how to write Synapse plugin config.yaml files. Use when the user asks about "config.yaml", "plugin configuration", "action definition", "execution method", "runtime environment", or needs help with synapse plugin settings.
---

# Synapse Plugin config.yaml Guide

The `config.yaml` file (or `synapse.yaml`) defines your plugin's metadata, actions, and runtime configuration.

## Minimal Example

```yaml
name: "My Plugin"
code: my-plugin
version: 1.0.0
category: custom

actions:
  train:
    entrypoint: plugin.train:TrainAction
    method: job
    description: "Train a model"
```

## Complete Structure

```yaml
# Basic metadata
name: "YOLOv8 Object Detection"
code: yolov8
version: 1.0.0
category: neural_net
description: "Train and run YOLOv8 models"
readme: README.md

# Package management
package_manager: pip  # or 'uv'
package_manager_options: []
wheels_dir: wheels

# Environment variables
env:
  DEBUG: "false"
  BATCH_SIZE: "32"

# Runtime environment (Ray)
runtime_env: {}

# Data type configuration
data_type: image
tasks:
  - image.object_detection
  - image.segmentation

# Actions
actions:
  train:
    entrypoint: plugin.train:TrainAction
    method: job
    description: "Train YOLO model"
  inference:
    entrypoint: plugin.inference:run
    method: task
    description: "Run inference"
```

## Action Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `entrypoint` | Yes | Module path (`module.path:ClassName` or `module.path.function`) |
| `method` | No | Execution method: `job`, `task`, or `serve` (default: `task`) |
| `description` | No | Human-readable description |

**Config Sync (Recommended)**

Sync entrypoints, input/output types, and hyperparameters from code:

```bash
synapse plugin update-config
```

## Execution Methods

| Method | Use Case | Characteristics |
|--------|----------|-----------------|
| `job` | Training, batch processing | Async, isolated, long-running (100s+) |
| `task` | Interactive operations | Sync, fast startup (<1s), serial per actor |
| `serve` | Model serving, inference | REST API endpoint, auto-scaling |

## Entrypoint Formats

Both formats are supported:
- **Colon notation**: `plugin.train:TrainAction`
- **Dot notation**: `plugin.train.TrainAction`

## Additional Resources

For detailed configuration options:
- **[references/fields.md](references/fields.md)** - All config.yaml fields
- **[references/smart-tool.md](references/smart-tool.md)** - Smart tool configuration
