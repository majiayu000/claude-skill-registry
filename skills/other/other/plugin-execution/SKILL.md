---
name: synapse-plugin-execution
description: Explains how to execute Synapse plugins programmatically. Use when the user mentions "run_plugin", "ExecutionMode", "LocalExecutor", "RayActorExecutor", "RayJobExecutor", "PluginDiscovery", "from_path", "from_module", or needs help with running plugins programmatically.
---

# Plugin Execution

Synapse SDK provides multiple ways to execute plugin actions programmatically.

## run_plugin() Function

The simplest way to run a plugin action:

```python
from synapse_sdk.plugins.runner import run_plugin, ExecutionMode

# Local execution (in-process, good for dev)
result = run_plugin(
    plugin_code='/path/to/plugin',
    action='train',
    params={'epochs': 100},
    mode=ExecutionMode.LOCAL,
)

# Ray Actor execution (fast startup)
result = run_plugin(
    plugin_code='/path/to/plugin',
    action='train',
    params={'epochs': 100},
    mode=ExecutionMode.TASK,
)

# Ray Job execution (heavy workloads)
job_id = run_plugin(
    plugin_code='/path/to/plugin',
    action='train',
    params={'epochs': 100},
    mode=ExecutionMode.JOB,
)
```

## Execution Modes

| Mode | Class | Use Case | Returns |
|------|-------|----------|---------|
| `LOCAL` | `LocalExecutor` | Development, testing | Result dict |
| `TASK` | `RayActorExecutor` | Fast startup, medium work | Result dict |
| `JOB` | `RayJobExecutor` | Heavy workloads, isolation | Job ID string |

## Plugin Discovery

Discover and inspect plugins before execution:

```python
from synapse_sdk.plugins.discovery import PluginDiscovery

# From filesystem path
discovery = PluginDiscovery.from_path('/path/to/plugin')

# From Python module
import my_plugin
discovery = PluginDiscovery.from_module(my_plugin)

# List available actions
actions = discovery.list_actions()  # ['train', 'inference']

# Get action class
action_cls = discovery.get_action_class('train')

# Get action metadata
config = discovery.get_action_config('train')
params_model = discovery.get_action_params_model('train')
```

## Direct Executor Usage

For more control, use executors directly:

```python
from synapse_sdk.plugins.executors.local import LocalExecutor
from synapse_sdk.plugins.discovery import PluginDiscovery

discovery = PluginDiscovery.from_path('/path/to/plugin')
action_cls = discovery.get_action_class('train')

executor = LocalExecutor()
result = executor.execute(action_cls, {'epochs': 100})
```

## Detailed References

- **[references/run-plugin.md](references/run-plugin.md)** - run_plugin() function details
- **[references/executors.md](references/executors.md)** - Executor classes
- **[references/discovery.md](references/discovery.md)** - PluginDiscovery class
