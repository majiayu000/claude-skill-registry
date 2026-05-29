---
name: gptme-plugin-development
description: Guide to creating gptme plugins with tools, hooks, and commands.
version: "1.0.0"
category: development
allowed-tools: "Read, Write, Edit, Bash"
---

# gptme Plugin Development

**Description:** Guide to creating gptme plugins with tools, hooks, and commands.

## When to Use Plugins vs Skills/Lessons

| Need | Use | Why |
|------|-----|-----|
| Share knowledge/workflows | Skills/Lessons | Lightweight bundles, no runtime |
| Custom tools (new actions) | Plugins | Extend capabilities via Python |
| Runtime hooks (lifecycle) | Plugins | Deep integration with gptme |
| Custom commands (/cmd) | Plugins | Add CLI commands |

## Plugin Structure

```tree
my_plugin/
├── pyproject.toml           # Package metadata + dependencies
├── README.md                # Documentation
├── src/
│   └── gptme_my_plugin/    # Package name
│       ├── __init__.py      # Simple init (avoid heavy imports)
│       └── tools/
│           └── __init__.py  # ToolSpec definitions
└── tests/
    └── test_my_plugin.py    # Tests
```

## Step-by-Step: Creating a Tool Plugin

### 1. Create pyproject.toml

```toml
[project]
name = "gptme-my-plugin"
version = "0.1.0"
description = "My custom gptme plugin"
requires-python = ">=3.10"
dependencies = [
    "gptme>=0.27.0",  # Required for ToolSpec, etc.
]

[project.optional-dependencies]
test = [
    "pytest>=8.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/gptme_my_plugin"]
```

### 2. Create Simple __init__.py

Keep it simple to avoid import issues:

```python
# src/gptme_my_plugin/__init__.py
"""My gptme plugin description."""

__version__ = "0.1.0"
```

**Important**: Don't import hooks or complex gptme internals here - it can cause import errors in tests.

### 3. Create the Tool

```python
# src/gptme_my_plugin/tools/__init__.py
"""My plugin tools."""

from gptme.tools.base import ToolSpec, ToolUse


def my_function(arg1: str, arg2: int = 10) -> str:
    """
    Do something useful.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2 (default: 10)

    Returns:
        Result description
    """
    return f"Result: {arg1} x {arg2}"


def examples(tool_format):
    return f'''
### Example usage
User: Do the thing
Assistant: I'll use my_function.
{ToolUse("ipython", [], "my_function('test', 5)").to_output(tool_format)}
'''


tool = ToolSpec(
    name="my_plugin",
    desc="Short description for tool list",
    examples=examples,
    functions=[my_function],
)

__doc__ = tool.get_doc(__doc__)
```

### 4. Write Tests

```python
# tests/test_my_plugin.py
"""Tests for my plugin."""

from gptme_my_plugin.tools import my_function


def test_my_function():
    """Test the main function."""
    result = my_function("hello", 3)
    assert "hello" in result
    assert "3" in result
```

### 5. Run Tests

```bash
# From plugin directory
cd plugins/my_plugin

# Using uv in workspace
uv run pytest tests/ -v

# Or install and test
uv pip install -e ".[test]"
uv run pytest tests/ -v
```

## Adding Hooks

For lifecycle hooks (SESSION_START, TOOL_PRE_EXECUTE, etc.):

```python
# src/gptme_my_plugin/hooks/__init__.py
from gptme.hooks import HookType, register_hook
from gptme.message import Message


def on_session_start(logdir, workspace, initial_msgs):
    """Hook called at session start."""
    yield Message("system", f"Plugin loaded in: {workspace}")


def register():
    """Register all hooks from this module."""
    register_hook(
        "my_plugin.session_start",
        HookType.SESSION_START,
        on_session_start,
        priority=0,
    )
```

**Available Hook Types:**
- `SESSION_START`, `SESSION_END` - Session lifecycle
- `TOOL_PRE_EXECUTE`, `TOOL_POST_EXECUTE` - Tool execution
- `FILE_PRE_SAVE`, `FILE_POST_SAVE` - File operations
- `GENERATION_PRE`, `GENERATION_POST` - LLM generation

## Adding Commands

For custom `/command` handlers:

```python
# src/gptme_my_plugin/commands/__init__.py
from gptme.commands import register_command, CommandContext
from gptme.message import Message


def my_command_handler(ctx: CommandContext):
    """Handle the /mycommand command."""
    args = ctx.full_args or "default"
    yield Message("system", f"Command executed with: {args}")


def register():
    register_command("mycommand", my_command_handler, aliases=["mc"])
```

## Common Patterns

### Optional Dependencies

For provider-specific features:

```toml
[project.optional-dependencies]
gemini = ["google-genai>=1.0.0"]
openai = ["openai>=1.0.0"]
```

### Getting API Keys

```python
def _get_api_key(env_var: str) -> str | None:
    """Get API key from gptme config first, then environment."""
    try:
        from gptme.config import get_config
        return get_config().get_env(env_var)
    except ImportError:
        import os
        return os.environ.get(env_var)
```

### Fallback Imports

For standalone usage:

```python
def _get_logs_dir():
    try:
        from gptme.dirs import get_logs_dir
        return get_logs_dir()
    except ImportError:
        from pathlib import Path
        return Path.home() / ".local" / "share" / "gptme" / "logs"
```

### Testing with logs_dir Parameter

Make functions testable by adding optional parameters:

```python
def my_stats(year: int | None = None, logs_dir: Path | None = None):
    if logs_dir is None:
        logs_dir = _get_logs_dir()
    # Use logs_dir...
```

Then in tests:

```python
def test_my_stats(tmp_path):
    # Create test data in tmp_path
    result = my_stats(2025, logs_dir=tmp_path)
    assert result["year"] == 2025
```

## Installation & Configuration

Configure plugins in `gptme.toml` at user-level (`~/.config/gptme/config.toml`) or project-level (`gptme.toml` in workspace root):

```toml
[plugins]
paths = ["~/.config/gptme/plugins", "/path/to/plugins"]
enabled = ["my_plugin"]  # Optional: limit which plugins load
```

See [gptme Plugin Docs](https://gptme.org/docs/plugins.html#configuration) for full configuration details.

### For Development

```bash
# Install in editable mode
uv pip install -e .

# Or in workspace
uv sync
```

## Troubleshooting

### Module Not Found in Tests

**Problem**: `ModuleNotFoundError: No module named 'gptme_my_plugin'`

**Solution**: Ensure you're running tests from the workspace environment:
```bash
cd /path/to/gptme-contrib
uv run pytest plugins/my_plugin/tests/ -v
```

### Import Errors from __init__.py

**Problem**: Complex imports in `__init__.py` cause import failures

**Solution**: Keep `__init__.py` minimal:
```python
# Bad
from gptme.plugins import hookimpl, PluginMetadata  # May fail

# Good
__version__ = "0.1.0"
```

### Environment Mismatch

**Problem**: uv installs to different env than pytest runs from

**Solution**: Use `uv run` to ensure consistent environment:
```bash
uv run pytest tests/ -v
```

## Examples in gptme-contrib

- **wrapped**: Analytics tool with tests
- **imagen**: Multi-provider image generation
- **lsp**: Language server integration
- **consortium**: Multi-model consensus
- **example-hooks**: Hook registration patterns

## Related

- [gptme Plugin Docs](https://gptme.org/docs/plugins.html)
- [Custom Tools Guide](https://gptme.org/docs/custom_tool.html)
- [Hooks System](https://gptme.org/docs/hooks.html)
