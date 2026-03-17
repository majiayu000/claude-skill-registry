---
name: amplifier-modulebuilder-skill
description: Build amplifier-foundation modules using "bricks and studs" architecture. Covers tool, hook, provider, context, and orchestrator modules with testing, publishing, and best practices.
compatibility: Requires Python 3.11+, uv package manager, git. Designed for Claude Code and similar Agent Skills-compatible products.
license: MIT
metadata:
  author: Michael Jabbour
  version: "1.0"
  repository: https://github.com/michaeljabbour/amplifier-modulebuilder-skill
  related-skills:
    - amplifier-cli-skill
---

# Amplifier Module Builder Skill

> Build production-ready amplifier-foundation modules using "bricks and studs" architecture

This skill teaches you how to create well-designed, tested, and maintainable modules for the amplifier-foundation ecosystem. Whether you're extending agent capabilities with tools, observing lifecycle events with hooks, or managing conversation state with context modules, this guide will show you the patterns and practices that lead to successful modules.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Module Types Overview](#2-module-types-overview)
3. [Quick Start](#3-quick-start)
4. [Core Development Workflow](#4-core-development-workflow)
5. [Module Structure Pattern](#5-module-structure-pattern)
6. [Testing Requirements](#6-testing-requirements)
7. [Repository Awareness Rules](#7-repository-awareness-rules)
8. [Common Patterns](#8-common-patterns)
9. [Using modular-builder Agent](#9-using-modular-builder-agent)
10. [Deep Dive References](#10-deep-dive-references)
11. [Complete Example Walkthrough](#11-complete-example-walkthrough)
12. [Common Pitfalls](#12-common-pitfalls)
13. [External Resources](#13-external-resources)

---

## 1. Introduction

### What is a Module?

A module in amplifier-foundation is a **self-contained, regeneratable unit** that extends the capabilities of AI agents. Each module:

- Has a **single, well-defined responsibility**
- Exposes a **clean public interface** (the "studs")
- Hides implementation details (the "bricks")
- Can be **composed with other modules**
- Is **independently testable**
- Can be **published and reused** across applications

Think of modules as LEGO bricks: each piece has a specific purpose, clear connection points (studs), and can be combined with other pieces to build something larger.

### "Bricks and Studs" Philosophy

The amplifier-foundation architecture is built on the principle of **"bricks and studs"**:

**Bricks** (Internal Implementation):
- Private functions and classes
- Implementation details
- Internal state management
- File system structure

**Studs** (Public Interface):
- The `mount(coordinator, config)` function
- Public functions exposed to the coordinator
- Configuration schema
- README.md documentation
- Type signatures in `__init__.py`

Just as LEGO bricks hide their internal structure while exposing uniform studs for connection, modules should:

1. **Self-contained**: All implementation details stay inside the module
2. **Regeneratable**: Can be rebuilt from scratch using just the public interface documentation
3. **Composable**: Connect cleanly with other modules through well-defined interfaces
4. **Predictable**: Same inputs always produce same outputs

### Why Build Modules?

Building modules provides several benefits:

**Reusability**: Write once, use across many agent applications
- A file system tool can be used by CLI apps, web apps, or batch processors

**Testability**: Small, focused units are easier to test thoroughly
- Test a tool module without spinning up a full agent

**Maintainability**: Clear boundaries make updates safer
- Change hook implementation without affecting tools

**Composability**: Mix and match capabilities
- Combine memory context + search tools + approval hooks

**Community**: Share your modules, use modules from others
- Publish to GitHub, reference with git URLs

### Link to the Amplifier Ecosystem

Modules are part of the broader amplifier ecosystem:

- **amplifier-core**: The kernel that coordinates agent execution
- **amplifier-foundation**: Core modules (tools, hooks, providers, contexts, orchestrators)
- **Your modules**: Extensions that add new capabilities
- **Applications**: CLI apps, web services, batch processors that compose modules

When you build a module, you're contributing to a growing ecosystem of composable AI capabilities.

---

## 2. Module Types Overview

Amplifier-foundation supports five module types, each serving a distinct purpose in the agent architecture:

### Module Types Table

| Type | Purpose | Entry Point | Example Use Cases |
|------|---------|-------------|-------------------|
| **Orchestrator** | Controls agent execution loop | `amplifier.orchestrators` | Basic loop, streaming responses, event-driven |
| **Provider** | Connects to AI model APIs | `amplifier.providers` | Anthropic, OpenAI, Azure, local models |
| **Tool** | Extends agent capabilities | `amplifier.tools` | File system, web search, bash, database |
| **Context** | Manages conversation state | `amplifier.contexts` | Simple memory, persistent storage, summaries |
| **Hook** | Observes lifecycle events | `amplifier.hooks` | Logging, approval gates, metrics, redaction |

### Orchestrator Modules

**Purpose**: Control how the agent executes turns, manages tool calls, and handles streaming responses.

**Key Characteristics**:
- Implements the main execution loop
- Manages turn-taking between user and agent
- Handles tool call execution and results
- Controls streaming or batch response delivery

**When to Build**: You need custom execution logic (e.g., parallel tool calls, custom retry logic, specialized streaming)

**Examples**: `loop-basic`, `loop-streaming`, `loop-events`

### Provider Modules

**Purpose**: Connect to AI model APIs and abstract away vendor-specific details.

**Key Characteristics**:
- Implements completion and streaming
- Handles authentication and rate limiting
- Provides token counting
- Maps vendor formats to common protocol

**When to Build**: You want to support a new AI model API or custom model deployment

**Examples**: `anthropic`, `openai`, `azure`, `bedrock`

### Tool Modules

**Purpose**: Extend what the agent can do by providing callable functions.

**Key Characteristics**:
- Exposes functions agent can call
- Provides JSON schema for function signatures
- Validates inputs and handles errors
- Performs actual work (file I/O, API calls, etc.)

**When to Build**: You want the agent to interact with external systems or perform specific operations

**Examples**: `tool-filesystem`, `tool-bash`, `tool-search`, `tool-database`

### Context Modules

**Purpose**: Manage conversation state and inject relevant information into prompts.

**Key Characteristics**:
- Maintains conversation history
- Injects context into prompts
- Handles memory persistence
- Manages context windows

**When to Build**: You need specialized memory management or context injection logic

**Examples**: `context-simple`, `context-persistent`, `context-memory`

### Hook Modules

**Purpose**: Observe and react to lifecycle events without blocking execution.

**Key Characteristics**:
- Listens to events (turn start/end, tool calls, errors)
- Performs side effects (logging, metrics, notifications)
- Does not modify agent behavior
- Runs asynchronously

**When to Build**: You want to observe, log, or react to agent events

**Examples**: `hooks-logging`, `hooks-approval`, `hooks-metrics`, `hooks-redaction`

---

## 3. Quick Start

### Prerequisites

Before building modules, ensure you have:

- **Python 3.11 or higher** (3.12+ recommended)
- **uv** package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **git** for version control
- **amplifier-foundation** installed (`uv pip install amplifier-foundation`)

### Create Your First Tool Module in 5 Steps

Let's build a simple tool that converts text to uppercase.

#### Step 1: Create Directory Structure

```bash
mkdir -p amplifier-module-tool-uppercase
cd amplifier-module-tool-uppercase
mkdir -p amplifier_module_tool_uppercase tests
```

#### Step 2: Write pyproject.toml

```toml
[project]
name = "amplifier-module-tool-uppercase"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["amplifier-foundation"]

[project.entry-points."amplifier.tools"]
uppercase = "amplifier_module_tool_uppercase:mount"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

#### Step 3: Implement the Module

```python
# amplifier_module_tool_uppercase/__init__.py
from typing import Any

async def mount(coordinator: Any, config: dict) -> dict[str, Any]:
    """Mount the uppercase tool."""

    async def uppercase(text: str) -> str:
        """Convert text to uppercase.

        Args:
            text: The text to convert

        Returns:
            The text in uppercase
        """
        return text.upper()

    return {
        "uppercase": uppercase
    }

def get_schema() -> dict:
    """Return JSON schema for tool functions."""
    return {
        "uppercase": {
            "description": "Convert text to uppercase",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to convert"
                    }
                },
                "required": ["text"]
            }
        }
    }
```

#### Step 4: Write Tests

```python
# tests/test_uppercase.py
import pytest
from amplifier_module_tool_uppercase import mount, get_schema

@pytest.mark.asyncio
async def test_uppercase_basic():
    """Test basic uppercase conversion."""
    tools = await mount(coordinator=None, config={})
    result = await tools["uppercase"]("hello")
    assert result == "HELLO"

@pytest.mark.asyncio
async def test_uppercase_empty():
    """Test empty string."""
    tools = await mount(coordinator=None, config={})
    result = await tools["uppercase"]("")
    assert result == ""

def test_get_schema():
    """Test schema is valid."""
    schema = get_schema()
    assert "uppercase" in schema
    assert "description" in schema["uppercase"]
    assert "parameters" in schema["uppercase"]
```

#### Step 5: Test Locally

```bash
# Quick test with environment variable
export AMPLIFIER_MODULE_TOOL_UPPERCASE=$(pwd)
python -c "from amplifier_foundation import load_bundle; import asyncio; asyncio.run(load_bundle('./profile.md'))"

# Or run tests
uv pip install pytest pytest-asyncio
uv run pytest tests/
```

### Publishing to GitHub

```bash
git init
git add .
git commit -m "feat: initial uppercase tool module"
gh repo create amplifier-module-tool-uppercase --public
git push -u origin main
git tag v0.1.0
git push origin v0.1.0
```

### Using Your Module

Reference it in a profile:

```yaml
tools:
  - git+https://github.com/yourusername/amplifier-module-tool-uppercase.git@v0.1.0
```

---

## 4. Core Development Workflow

Follow this workflow for all module development:

### 1. Define Single Responsibility

Ask: "What is the ONE thing this module does?"

**Good examples**:
- "Convert files between formats"
- "Send notifications to Slack"
- "Track token usage metrics"

**Bad examples** (too broad):
- "Handle all file operations" (split into read, write, search)
- "Manage the entire conversation" (split responsibilities)

### 2. Write Contract (README.md First)

Document the public interface BEFORE writing code:

```markdown
# amplifier-module-tool-myfeature

Converts X to Y using Z algorithm.

## Installation

\`\`\`bash
uv pip install git+https://github.com/you/amplifier-module-tool-myfeature.git
\`\`\`

## API

### mount(coordinator, config) -> dict

Returns dict with these functions:

- `my_function(arg1: str, arg2: int) -> str`: Does X and returns Y

## Configuration

\`\`\`yaml
config:
  option1: value1
  option2: value2
\`\`\`

## Testing

\`\`\`bash
pytest tests/
\`\`\`
```

### 3. Create Module Structure

```
amplifier-module-{type}-{name}/
├── amplifier_module_{type}_{name}/
│   ├── __init__.py           # mount() and public functions
│   ├── _internal.py          # Private implementation
│   └── py.typed              # Type hints marker
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── test_unit.py         # Unit tests (60%)
│   ├── test_integration.py  # Integration tests (30%)
│   └── test_e2e.py          # End-to-end tests (10%)
├── pyproject.toml            # Dependencies and entry point
├── README.md                 # Public contract
└── .github/
    └── workflows/
        └── test.yml         # CI/CD

```

### 4. Implement Protocol

All modules implement the `mount()` protocol:

```python
async def mount(coordinator: Any, config: dict) -> dict[str, Any]:
    """Mount the module and return its public interface.

    Args:
        coordinator: The amplifier coordinator instance
        config: Configuration dict from profile/bundle

    Returns:
        Dict mapping names to functions/objects
    """
    # Setup (load resources, connect to services, etc.)

    # Define public functions
    async def my_function(arg: str) -> str:
        # Implementation
        pass

    # Return public interface
    return {
        "my_function": my_function
    }
```

For tool modules, also implement `get_schema()`:

```python
def get_schema() -> dict:
    """Return JSON schema for tool functions.

    Returns:
        Dict mapping function names to schemas
    """
    return {
        "my_function": {
            "description": "Does something useful",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg": {"type": "string", "description": "Input value"}
                },
                "required": ["arg"]
            }
        }
    }
```

### 5. Write Tests (60% unit, 30% integration, 10% e2e)

**Unit tests** (60%): Test individual functions in isolation

```python
@pytest.mark.asyncio
async def test_my_function_basic():
    tools = await mount(coordinator=None, config={})
    result = await tools["my_function"]("input")
    assert result == "expected"
```

**Integration tests** (30%): Test module with real dependencies

```python
@pytest.mark.asyncio
async def test_with_real_coordinator():
    from amplifier_foundation import Coordinator
    coordinator = Coordinator()
    tools = await mount(coordinator=coordinator, config={})
    # Test with real coordinator
```

**End-to-end tests** (10%): Test full workflows

```python
@pytest.mark.asyncio
async def test_full_agent_workflow():
    # Load bundle, create session, execute turn
    pass
```

### 6. Publish to GitHub

```bash
git init
git add .
git commit -m "feat: initial module implementation"
gh repo create amplifier-module-{type}-{name} --public
git push -u origin main
git tag v0.1.0
git push origin v0.1.0
```

### 7. Reference in Profiles with Git URL

```yaml
# profile.md or bundle.md
tools:
  - git+https://github.com/yourusername/amplifier-module-tool-myfeature.git@v0.1.0
```

---

## 5. Module Structure Pattern

### Required Directory Layout

```
amplifier-module-{type}-{name}/
├── amplifier_module_{type}_{name}/    # Package (underscores)
│   ├── __init__.py                    # Public interface (mount, get_schema)
│   ├── _internal.py                   # Private implementation
│   ├── _types.py                      # Private type definitions
│   └── py.typed                       # Type hints marker file
├── tests/                             # Test package
│   ├── __init__.py
│   ├── conftest.py                    # Pytest fixtures
│   ├── test_unit.py                   # Unit tests
│   ├── test_integration.py            # Integration tests
│   └── test_e2e.py                    # End-to-end tests
├── .github/
│   └── workflows/
│       └── test.yml                   # CI/CD workflow
├── pyproject.toml                     # Project metadata
├── README.md                          # Public contract
├── LICENSE                            # MIT recommended
├── .gitignore
└── .python-version                    # Python version (3.11+)
```

### pyproject.toml with Entry Points

The `pyproject.toml` file declares dependencies and registers the module:

```toml
[project]
name = "amplifier-module-{type}-{name}"
version = "0.1.0"
description = "One sentence description"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
dependencies = [
    "amplifier-foundation>=0.1.0",
]

# Entry point registration - CRITICAL
[project.entry-points."amplifier.{type}s"]  # Note plural
{name} = "amplifier_module_{type}_{name}:mount"

# Optional: Additional entry points for get_schema (tools only)
[project.entry-points."amplifier.tool_schemas"]
{name} = "amplifier_module_{type}_{name}:get_schema"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
asyncio_mode = "auto"

[tool.coverage.run]
source = ["amplifier_module_{type}_{name}"]
omit = ["tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

### Public vs Private Interfaces

**Public Interface** (in `__init__.py`):
- `mount()` function - REQUIRED
- `get_schema()` function - REQUIRED for tools
- Type definitions used in public signatures
- Constants that users should know about

```python
# amplifier_module_tool_myfeature/__init__.py
from typing import Any

async def mount(coordinator: Any, config: dict) -> dict[str, Any]:
    """Public mount function - this is a STUD."""
    from ._internal import MyFeatureImpl
    impl = MyFeatureImpl(config)
    return {"my_function": impl.execute}

def get_schema() -> dict:
    """Public schema function - this is a STUD."""
    return {"my_function": {...}}

# Public constants
DEFAULT_TIMEOUT = 30
```

**Private Implementation** (in `_internal.py`):
- Classes and functions prefixed with `_`
- Implementation details
- Helper functions
- Internal state

```python
# amplifier_module_tool_myfeature/_internal.py
class MyFeatureImpl:
    """Private implementation - this is a BRICK."""

    def __init__(self, config: dict):
        self._config = config
        self._cache = {}

    async def execute(self, input: str) -> str:
        # Implementation details hidden
        return self._process(input)

    def _process(self, input: str) -> str:
        # Private helper
        pass
```

### Testing Organization

```python
# tests/conftest.py - Shared fixtures
import pytest

@pytest.fixture
async def mounted_module():
    """Fixture that mounts the module."""
    from amplifier_module_tool_myfeature import mount
    return await mount(coordinator=None, config={})

@pytest.fixture
def sample_config():
    """Fixture for test configuration."""
    return {"option1": "value1"}
```

```python
# tests/test_unit.py - Unit tests (60%)
import pytest

@pytest.mark.asyncio
async def test_basic_function(mounted_module):
    """Test basic functionality."""
    result = await mounted_module["my_function"]("input")
    assert result == "expected"

@pytest.mark.asyncio
async def test_error_handling(mounted_module):
    """Test error cases."""
    with pytest.raises(ValueError):
        await mounted_module["my_function"]("")
```

```python
# tests/test_integration.py - Integration tests (30%)
import pytest

@pytest.mark.asyncio
async def test_with_coordinator():
    """Test with real coordinator."""
    from amplifier_foundation import Coordinator
    from amplifier_module_tool_myfeature import mount

    coordinator = Coordinator()
    tools = await mount(coordinator, config={})
    # Test integration
```

```python
# tests/test_e2e.py - End-to-end tests (10%)
import pytest

@pytest.mark.asyncio
async def test_full_workflow():
    """Test complete agent workflow."""
    from amplifier_foundation import load_bundle, create_session
    # Test end-to-end
```

### Documentation Requirements

Every module MUST include:

**README.md** with:
- One-sentence description
- Installation instructions
- API documentation (mount signature, returned functions)
- Configuration options
- Usage examples
- Testing instructions
- License information

**Inline docstrings**:
- All public functions must have docstrings
- Use Google or NumPy style
- Include Args, Returns, Raises sections
- Examples for complex functions

```python
async def mount(coordinator: Any, config: dict) -> dict[str, Any]:
    """Mount the uppercase tool.

    Args:
        coordinator: The amplifier coordinator instance
        config: Configuration dictionary (unused for this tool)

    Returns:
        Dictionary mapping "uppercase" to the uppercase function

    Examples:
        >>> tools = await mount(coordinator, {})
        >>> result = await tools["uppercase"]("hello")
        >>> print(result)
        HELLO
    """
```

---

## 6. Testing Requirements

### Test Pyramid (60/30/10)

Amplifier modules follow the test pyramid:

```
        /\
       /  \
      / E2E \    10% - Full workflows
     /------\
    /        \
   / Integrn  \  30% - Module + dependencies
  /------------\
 /              \
/   Unit Tests   \ 60% - Individual functions
------------------
```

**60% Unit Tests**: Fast, isolated, test individual functions

**30% Integration Tests**: Test module with real dependencies

**10% End-to-End Tests**: Test full agent workflows

### Coverage Targets

| Coverage Level | Target | Applies To |
|---------------|--------|------------|
| Minimum | 70% | All modules before publishing |
| Target | 85% | Production modules |
| Critical Paths | 100% | Error handling, security, data loss |

**Measuring coverage**:

```bash
uv pip install pytest-cov
uv run pytest --cov=amplifier_module_tool_myfeature --cov-report=html
open htmlcov/index.html
```

### Async Testing with Pytest

All amplifier modules are async, so use pytest-asyncio:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test an async function."""
    result = await my_async_function()
    assert result == expected
```

Or configure pytest to auto-detect async tests:

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # Automatically handle async tests
```

Then write tests without `@pytest.mark.asyncio`:

```python
async def test_async_function():
    """Automatically recognized as async test."""
    result = await my_async_function()
    assert result == expected
```

### Mocking External Dependencies

Use `pytest-mock` or `unittest.mock` to mock external services:

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mocked_api():
    """Test with mocked external API."""
    mock_response = {"data": "value"}

    with patch('my_module._internal.external_api_call', new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response

        result = await my_function()
        assert result == expected
        mock_api.assert_called_once()
```

### CI/CD Integration

Add GitHub Actions workflow:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv pip install -e ".[dev]"

      - name: Run tests with coverage
        run: uv run pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## 7. Repository Awareness Rules

### The Golden Rule

**"Only reference declared dependencies"**

Modules can ONLY import and use:
- Python standard library
- Dependencies declared in `pyproject.toml`
- The amplifier coordinator passed to `mount()`
- Their own internal modules

Modules CANNOT:
- Import other amplifier modules directly
- Reference peer modules
- Assume other modules exist
- Share state outside the coordinator

### Module Awareness Constraints

```python
# ❌ WRONG - Direct import of peer module
from amplifier_module_tool_filesystem import read_file

# ✅ CORRECT - Use tool through coordinator
async def mount(coordinator, config):
    async def my_function():
        # Request tool from coordinator
        filesystem = await coordinator.get_tool("filesystem")
        content = await filesystem["read_file"]("path.txt")
        return content
```

### Naming Conventions

**Repository names** (kebab-case):
```
amplifier-module-tool-filesystem
amplifier-module-hook-logging
amplifier-module-provider-openai
amplifier-module-context-memory
amplifier-module-loop-streaming
```

**Python packages** (snake_case):
```python
amplifier_module_tool_filesystem
amplifier_module_hook_logging
amplifier_module_provider_openai
```

**Entry point names** (kebab-case or snake_case):
```toml
[project.entry-points."amplifier.tools"]
filesystem = "amplifier_module_tool_filesystem:mount"
my-tool = "amplifier_module_tool_mytool:mount"
```

### Documentation as Contract

The README.md is a **contract**:
- It defines the public interface
- It specifies configuration options
- It documents expected behavior
- It should be sufficient to regenerate the module

**If it's not in the README, it's not public API.**

---

## 8. Common Patterns

### Pattern 1: Simple Input/Output Transformation

For stateless transformations:

```python
async def mount(coordinator, config):
    """Mount a simple transformation tool."""

    async def transform(input: str) -> str:
        """Transform input to output."""
        # Pure function - no state
        return input.upper()

    return {"transform": transform}
```

### Pattern 2: Service Module (Class-Based)

For stateful services:

```python
class MyService:
    """Internal service with state."""

    def __init__(self, config: dict):
        self.api_key = config.get("api_key")
        self._cache = {}

    async def call_api(self, query: str) -> dict:
        """Make API call with caching."""
        if query in self._cache:
            return self._cache[query]

        result = await self._make_request(query)
        self._cache[query] = result
        return result

    async def _make_request(self, query: str) -> dict:
        # Private implementation
        pass

async def mount(coordinator, config):
    """Mount service with state."""
    service = MyService(config)

    return {
        "call_api": service.call_api
    }
```

### Pattern 3: Pipeline Stage (Async Batch Processing)

For processing streams of data:

```python
async def mount(coordinator, config):
    """Mount batch processing tool."""
    batch_size = config.get("batch_size", 10)

    async def process_batch(items: list[str]) -> list[str]:
        """Process items in batches."""
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = await _process_items(batch)
            results.extend(batch_results)
        return results

    async def _process_items(items: list[str]) -> list[str]:
        # Process batch concurrently
        import asyncio
        tasks = [_process_one(item) for item in items]
        return await asyncio.gather(*tasks)

    async def _process_one(item: str) -> str:
        # Process single item
        return item.upper()

    return {"process_batch": process_batch}
```

### Pattern 4: Error Handling Standards

All modules should handle errors consistently:

```python
class ModuleError(Exception):
    """Base exception for module errors."""
    pass

class ConfigurationError(ModuleError):
    """Invalid configuration."""
    pass

class ExecutionError(ModuleError):
    """Error during execution."""
    pass

async def mount(coordinator, config):
    """Mount with proper error handling."""

    # Validate config at mount time
    if "required_key" not in config:
        raise ConfigurationError("Missing required_key in config")

    async def my_function(input: str) -> str:
        """Function with error handling."""
        if not input:
            raise ValueError("Input cannot be empty")

        try:
            result = await _do_work(input)
            return result
        except Exception as e:
            # Wrap external errors
            raise ExecutionError(f"Failed to process: {e}") from e

    return {"my_function": my_function}
```

---

## 9. Using modular-builder Agent

### What is modular-builder?

The `modular-builder` is an AI agent that generates module scaffold code based on specifications. It helps you:

- Generate initial module structure
- Create pyproject.toml with correct entry points
- Scaffold test files
- Generate basic README documentation

**Important**: modular-builder generates starting points, not production code. Always review and test generated code.

### When to Use Agent vs Manual Development

**Use modular-builder when**:
- Starting a new module from scratch
- Unsure about entry point configuration
- Want to quickly prototype an idea
- Need boilerplate for a standard pattern

**Write manually when**:
- Complex custom logic required
- Integrating with existing code
- Performance-critical implementation
- Specialized error handling needed

### Invoking modular-builder

Create a specification file:

```yaml
# module-spec.yaml
name: uppercase
type: tool
description: Convert text to uppercase
functions:
  - name: uppercase
    description: Convert text to uppercase
    parameters:
      text:
        type: string
        description: The text to convert
    returns:
      type: string
      description: The uppercased text
dependencies:
  - amplifier-foundation
test_coverage: 85
```

Invoke the agent:

```bash
modular-builder generate --spec module-spec.yaml --output ./amplifier-module-tool-uppercase
```

### Validating Generated Code

After generation, always:

1. **Review the code**: Check logic, error handling, edge cases
2. **Run tests**: `pytest tests/`
3. **Check coverage**: `pytest --cov`
4. **Test locally**: Export path and test with a profile
5. **Read documentation**: Ensure README matches implementation

### Iterating on Specifications

If generated code isn't quite right:

1. Update the specification file
2. Regenerate with `--force` flag
3. Review changes with `git diff`
4. Merge manually if needed

---

## 10. Deep Dive References

For detailed information on specific topics, see the `references/` directory:

### Building Your First Module?

→ **[references/MODULE_TYPES.md](references/MODULE_TYPES.md)**
- Deep dive on all 5 module types
- Protocol interfaces and required methods
- Type-specific testing strategies
- Common pitfalls for each type

### Setting Up Your Development Workflow?

→ **[references/DEVELOPMENT_WORKFLOW.md](references/DEVELOPMENT_WORKFLOW.md)**
- Complete step-by-step development process
- Local testing strategies
- Workspace configuration patterns
- Publishing and versioning

### Need Testing Guidance?

→ **[references/TESTING_GUIDE.md](references/TESTING_GUIDE.md)**
- Test pyramid breakdown (60/30/10)
- Coverage targets and rationale
- Async testing patterns with pytest
- Mocking strategies
- Module-specific testing approaches

### Understanding Module Constraints?

→ **[references/REPOSITORY_RULES.md](references/REPOSITORY_RULES.md)**
- Repository hierarchy
- The Golden Rule explained
- Module awareness constraints
- Naming conventions
- Documentation as contract

### Looking for Examples?

→ **[references/EXAMPLES.md](references/EXAMPLES.md)**
- 4 complete working examples:
  - Tool module (uppercase)
  - Hook module (metrics)
  - Provider module (mock)
  - Context module (memory)
- Full directory trees
- Complete pyproject.toml files
- Documented implementation code
- Test examples

### Need API Implementation Patterns?

→ **[references/API_PATTERNS.md](references/API_PATTERNS.md)**
- mount(coordinator, config) signatures
- get_schema() for tools
- execute() patterns
- Error handling conventions
- Async/await patterns
- Type annotations
- Validation patterns

### Using the modular-builder Agent?

→ **[references/MODULAR_BUILDER.md](references/MODULAR_BUILDER.md)**
- What is modular-builder?
- When to use vs manual coding
- Specification format
- Invoking the agent
- Validating generated code
- Best practices for AI-generated modules

### Contributing Modules to the Ecosystem?

→ **[references/CONTRIBUTING.md](references/CONTRIBUTING.md)**
- Repository structure expectations
- Coding style
- Documentation requirements
- Testing requirements
- Review process
- Publishing checklist

---

## 11. Complete Example Walkthrough

Let's build a complete tool module from scratch that searches text files for patterns.

### Step 1: Define Responsibility

"Search text files in a directory for regex patterns and return matching lines with line numbers."

### Step 2: Write Contract (README.md)

```markdown
# amplifier-module-tool-textsearch

Search text files for regex patterns with line number reporting.

## Installation

\`\`\`bash
uv pip install git+https://github.com/yourusername/amplifier-module-tool-textsearch.git
\`\`\`

## API

### mount(coordinator, config) -> dict

Returns dict with:

- `search_files(directory: str, pattern: str, file_ext: str = ".txt") -> list[dict]`
  - Search files in directory for regex pattern
  - Returns list of matches with file, line number, and content

## Configuration

\`\`\`yaml
config:
  max_file_size: 1048576  # 1MB default
  encoding: utf-8
\`\`\`

## Example

\`\`\`python
tools = await mount(coordinator, config={"max_file_size": 2097152})
results = await tools["search_files"](
    directory="./logs",
    pattern="ERROR.*authentication",
    file_ext=".log"
)
\`\`\`
```

### Step 3: Create Structure

```bash
mkdir -p amplifier-module-tool-textsearch
cd amplifier-module-tool-textsearch
mkdir -p amplifier_module_tool_textsearch tests
```

### Step 4: Implement Module

```python
# amplifier_module_tool_textsearch/__init__.py
"""Text search tool module."""
from typing import Any
import re
from pathlib import Path

class SearchError(Exception):
    """Base exception for search errors."""
    pass

async def mount(coordinator: Any, config: dict) -> dict[str, Any]:
    """Mount the text search tool.

    Args:
        coordinator: The amplifier coordinator
        config: Configuration with optional max_file_size and encoding

    Returns:
        Dict with search_files function
    """
    max_size = config.get("max_file_size", 1048576)  # 1MB default
    encoding = config.get("encoding", "utf-8")

    async def search_files(
        directory: str,
        pattern: str,
        file_ext: str = ".txt"
    ) -> list[dict]:
        """Search files for regex pattern.

        Args:
            directory: Directory path to search
            pattern: Regex pattern to match
            file_ext: File extension filter (default .txt)

        Returns:
            List of dicts with {file, line_num, line, match}

        Raises:
            SearchError: If directory doesn't exist or pattern is invalid
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            raise SearchError(f"Directory not found: {directory}")
        if not dir_path.is_dir():
            raise SearchError(f"Not a directory: {directory}")

        try:
            regex = re.compile(pattern)
        except re.error as e:
            raise SearchError(f"Invalid regex pattern: {e}")

        results = []
        for file_path in dir_path.rglob(f"*{file_ext}"):
            if file_path.is_file() and file_path.stat().st_size <= max_size:
                results.extend(await _search_file(file_path, regex, encoding))

        return results

    async def _search_file(
        file_path: Path,
        regex: re.Pattern,
        encoding: str
    ) -> list[dict]:
        """Search a single file."""
        results = []
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                for line_num, line in enumerate(f, start=1):
                    match = regex.search(line)
                    if match:
                        results.append({
                            "file": str(file_path),
                            "line_num": line_num,
                            "line": line.rstrip(),
                            "match": match.group(0)
                        })
        except Exception as e:
            # Skip files that can't be read
            pass

        return results

    return {
        "search_files": search_files
    }

def get_schema() -> dict:
    """Return JSON schema for tool functions."""
    return {
        "search_files": {
            "description": "Search text files for regex patterns",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path to search"
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Regex pattern to match"
                    },
                    "file_ext": {
                        "type": "string",
                        "description": "File extension filter (default .txt)",
                        "default": ".txt"
                    }
                },
                "required": ["directory", "pattern"]
            }
        }
    }
```

### Step 5: Write Tests

```python
# tests/conftest.py
import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
async def mounted_search():
    """Mount the search module."""
    from amplifier_module_tool_textsearch import mount
    return await mount(coordinator=None, config={})

@pytest.fixture
def temp_dir():
    """Create temporary directory with test files."""
    tmpdir = tempfile.mkdtemp()

    # Create test files
    (Path(tmpdir) / "file1.txt").write_text("line 1: ERROR\nline 2: OK\nline 3: ERROR")
    (Path(tmpdir) / "file2.txt").write_text("line 1: WARNING\nline 2: ERROR")
    (Path(tmpdir) / "subdir").mkdir()
    (Path(tmpdir) / "subdir" / "file3.txt").write_text("line 1: ERROR in subdirectory")

    yield tmpdir
    shutil.rmtree(tmpdir)
```

```python
# tests/test_unit.py
import pytest
from amplifier_module_tool_textsearch import mount, SearchError

@pytest.mark.asyncio
async def test_search_basic(mounted_search, temp_dir):
    """Test basic search functionality."""
    results = await mounted_search["search_files"](
        directory=temp_dir,
        pattern="ERROR"
    )
    assert len(results) == 4  # 3 in file1, 1 in file2, 0 in file3 (different ext)
    assert all(r["match"] == "ERROR" for r in results)

@pytest.mark.asyncio
async def test_search_subdirectories(mounted_search, temp_dir):
    """Test recursive search in subdirectories."""
    results = await mounted_search["search_files"](
        directory=temp_dir,
        pattern="ERROR"
    )
    # Should find matches in subdirectories too
    assert any("subdir" in r["file"] for r in results)

@pytest.mark.asyncio
async def test_invalid_directory(mounted_search):
    """Test error handling for invalid directory."""
    with pytest.raises(SearchError, match="Directory not found"):
        await mounted_search["search_files"](
            directory="/nonexistent",
            pattern="ERROR"
        )

@pytest.mark.asyncio
async def test_invalid_regex(mounted_search, temp_dir):
    """Test error handling for invalid regex."""
    with pytest.raises(SearchError, match="Invalid regex pattern"):
        await mounted_search["search_files"](
            directory=temp_dir,
            pattern="[invalid"
        )

@pytest.mark.asyncio
async def test_file_extension_filter(mounted_search, temp_dir):
    """Test file extension filtering."""
    # Create .log file
    from pathlib import Path
    (Path(temp_dir) / "test.log").write_text("ERROR in log file")

    # Search only .log files
    results = await mounted_search["search_files"](
        directory=temp_dir,
        pattern="ERROR",
        file_ext=".log"
    )
    assert len(results) == 1
    assert results[0]["file"].endswith(".log")
```

### Step 6: Test Locally

```bash
# Run tests
uv pip install pytest pytest-asyncio
uv run pytest tests/ -v

# Check coverage
uv run pytest --cov=amplifier_module_tool_textsearch --cov-report=term
```

### Step 7: Publish Module

```bash
# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "amplifier-module-tool-textsearch"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["amplifier-foundation"]

[project.entry-points."amplifier.tools"]
textsearch = "amplifier_module_tool_textsearch:mount"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
EOF

# Initialize git and publish
git init
git add .
git commit -m "feat: initial text search tool module"
gh repo create amplifier-module-tool-textsearch --public
git push -u origin main
git tag v0.1.0
git push origin v0.1.0
```

### Step 8: Use in Profile

```yaml
# profile.md
---
tools:
  - git+https://github.com/yourusername/amplifier-module-tool-textsearch.git@v0.1.0
---

# Profile with Text Search

This profile includes the text search tool.
```

---

## 12. Common Pitfalls

### Anti-Patterns Table

| Anti-Pattern | Why It's Bad | Correct Pattern |
|-------------|--------------|-----------------|
| **Importing peer modules** | Creates hidden dependencies, breaks isolation | Use coordinator to get other modules |
| **Storing state in module globals** | Not thread-safe, breaks on reload | Store state in class instances |
| **Returning classes from mount()** | Exposes implementation details | Return dict of functions |
| **No error handling** | Crashes agent on bad input | Validate inputs, raise clear errors |
| **Testing implementation** | Tests break on refactor | Test behavior through public API |
| **Undocumented config options** | Users can't configure module | Document all config in README |
| **Blocking I/O** | Hangs async loop | Use async I/O or run_in_executor |
| **Large mount() functions** | Hard to test and maintain | Extract to _internal.py |

### Module Coupling

**Bad**: Direct import creates coupling

```python
# ❌ WRONG
from amplifier_module_tool_filesystem import read_file

async def mount(coordinator, config):
    async def process_file(path: str):
        content = read_file(path)  # Tightly coupled
        return content.upper()
    return {"process_file": process_file}
```

**Good**: Use coordinator for loose coupling

```python
# ✅ CORRECT
async def mount(coordinator, config):
    async def process_file(path: str):
        # Loose coupling through coordinator
        fs = await coordinator.get_tool("filesystem")
        content = await fs["read_file"](path)
        return content.upper()
    return {"process_file": process_file}
```

### Leaky Abstractions

**Bad**: Exposing implementation details

```python
# ❌ WRONG - Exposes internal class
class SearchService:
    def __init__(self):
        self.cache = {}

async def mount(coordinator, config):
    service = SearchService()
    return {"search_service": service}  # Leaks internals
```

**Good**: Hide implementation behind functions

```python
# ✅ CORRECT - Hide implementation
class _SearchService:  # Private class
    def __init__(self):
        self._cache = {}

    async def search(self, query: str) -> list:
        # Implementation

async def mount(coordinator, config):
    service = _SearchService()
    return {"search": service.search}  # Only expose function
```

### Documentation Drift

**Bad**: Code and docs don't match

```python
# README.md says: uppercase(text: str) -> str
# But code has:
async def uppercase(text: str, mode: str = "upper") -> str:
    # Undocumented parameter!
```

**Good**: Docs match implementation exactly

```python
# README.md: uppercase(text: str, mode: str = "upper") -> str
# Code:
async def uppercase(text: str, mode: str = "upper") -> str:
    """Convert text case.

    Args:
        text: Input text
        mode: "upper" or "lower" (default: "upper")
    """
```

### Testing Implementation vs Behavior

**Bad**: Testing internal details

```python
# ❌ WRONG - Tests implementation
def test_internal_cache():
    service = SearchService()
    service._cache["key"] = "value"  # Testing private state
    assert service._cache["key"] == "value"
```

**Good**: Test behavior through public API

```python
# ✅ CORRECT - Tests behavior
@pytest.mark.asyncio
async def test_search_returns_results():
    tools = await mount(coordinator=None, config={})
    results = await tools["search"]("query")
    assert isinstance(results, list)
```

---

## 13. External Resources

### Official Documentation

- **[amplifier-foundation GitHub](https://github.com/microsoft/amplifier-foundation)** - Core modules and framework
- **[amplifier-core Documentation](https://github.com/microsoft/amplifier-core)** - Kernel and coordinator
- **[Agent Skills Specification](https://agentskills.io/specification)** - Format for this skill

### Module Registry

- **[Community Modules](https://github.com/topics/amplifier-module)** - Browse modules on GitHub
- **[Module Templates](https://github.com/microsoft/amplifier-foundation/tree/main/templates)** - Starter templates

### Related Skills

- **[amplifier-cli-skill](../amplifier-cli-skill)** - Build CLI applications with amplifier-foundation

### Development Tools

- **[uv Package Manager](https://astral.sh/uv)** - Fast Python package installer
- **[pytest](https://docs.pytest.org/)** - Testing framework
- **[pytest-asyncio](https://pytest-asyncio.readthedocs.io/)** - Async test support

### Community

- **[GitHub Discussions](https://github.com/microsoft/amplifier-foundation/discussions)** - Ask questions
- **[Issue Tracker](https://github.com/microsoft/amplifier-foundation/issues)** - Report bugs

---

## Summary

Building amplifier-foundation modules is about creating **self-contained, regeneratable units** with clear public interfaces and hidden implementation details.

**Key Takeaways**:

1. **"Bricks and Studs"**: Hide implementation (bricks), expose clean interface (studs)
2. **Single Responsibility**: One module does one thing well
3. **Testing Matters**: 60/30/10 pyramid, 85% coverage target
4. **Documentation is Contract**: README defines the public API
5. **Awareness Rules**: Only reference declared dependencies
6. **Async Everything**: Use async/await for all I/O
7. **Progressive Disclosure**: Start simple, provide deep references

**Next Steps**:

1. Read [references/MODULE_TYPES.md](references/MODULE_TYPES.md) for your module type
2. Follow [references/DEVELOPMENT_WORKFLOW.md](references/DEVELOPMENT_WORKFLOW.md) step-by-step
3. Study [references/EXAMPLES.md](references/EXAMPLES.md) for working code
4. Build your first module!
5. Share with the community

Happy building! 🔧
