---
name: python-optional-dependencies
description: "Use when supporting multiple backends/providers without forcing all dependencies on users. pyproject.toml extras pattern."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-09"
---

# Python Optional Dependencies Pattern

**Extracted:** 2026-02-09
**Context:** Supporting multiple providers/backends without forcing all dependencies on all users

## Problem

You're building a library/CLI that supports multiple backends (e.g., multiple LLM providers, multiple databases, multiple cloud providers), but you don't want to force users to install all dependencies.

**Example Scenarios:**
- LLM application supporting both Anthropic and OpenAI
- Database library supporting PostgreSQL, MySQL, SQLite
- Cloud SDK supporting AWS, Azure, GCP
- Analytics tool supporting multiple data sources

**Naive Approach:**
```toml
dependencies = [
    "anthropic>=0.40.0",  # ← Forces everyone to install
    "openai>=1.0.0",      # ← Even if they only use one
    "google-generativeai>=0.3.0",
]
```

**Problem:** Users installing 50+ MB of unused SDKs, potential version conflicts, slower installation.

---

## Solution: Optional Dependencies

Use `[project.optional-dependencies]` in `pyproject.toml` to let users choose.

### Step 1: Define Optional Dependency Groups

```toml
[project]
name = "myapp"
dependencies = [
    # Only core dependencies here
    "pydantic>=2.0",
    "typer>=0.15.0",
]

[project.optional-dependencies]
# Individual provider groups
anthropic = ["anthropic>=0.40.0"]
openai = ["openai>=1.0.0"]
google = ["google-generativeai>=0.3.0"]

# Convenience groups
all = [
    "anthropic>=0.40.0",
    "openai>=1.0.0",
    "google-generativeai>=0.3.0",
]

# Dev dependencies
dev = [
    "pytest>=8.0",
    "mypy>=1.11",
]
```

### Step 2: Installation

```bash
# Install with specific provider
pip install myapp[anthropic]
pip install myapp[openai]

# Install with multiple providers
pip install myapp[anthropic,openai]

# Install everything
pip install myapp[all]

# Dev installation
pip install myapp[all,dev]
```

---

## Implementation Pattern

### Step 3: Runtime Availability Check

Create a module to check which optional dependencies are available:

```python
# myapp/providers/__init__.py
"""Provider availability checks."""

# Check Anthropic availability
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Check OpenAI availability
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Check at least one is available
if not (ANTHROPIC_AVAILABLE or OPENAI_AVAILABLE):
    raise ImportError(
        "No LLM provider installed. "
        "Install at least one:\n"
        "  pip install myapp[anthropic]\n"
        "  pip install myapp[openai]\n"
        "  pip install myapp[all]"
    )
```

### Step 4: Provider Factory with Runtime Check

```python
# myapp/providers/factory.py
from myapp.providers import ANTHROPIC_AVAILABLE, OPENAI_AVAILABLE

def create_provider(provider_name: str):
    """Create provider instance with availability check."""

    if provider_name == "anthropic":
        if not ANTHROPIC_AVAILABLE:
            raise RuntimeError(
                "Anthropic provider not installed.\n"
                "Install with: pip install myapp[anthropic]"
            )
        from myapp.providers.anthropic import AnthropicProvider
        return AnthropicProvider()

    elif provider_name == "openai":
        if not OPENAI_AVAILABLE:
            raise RuntimeError(
                "OpenAI provider not installed.\n"
                "Install with: pip install myapp[openai]"
            )
        from myapp.providers.openai import OpenAIProvider
        return OpenAIProvider()

    else:
        raise ValueError(f"Unknown provider: {provider_name}")
```

### Step 5: CLI Help with Availability Info

```python
# myapp/main.py
import typer
from myapp.providers import ANTHROPIC_AVAILABLE, OPENAI_AVAILABLE

app = typer.Typer()

@app.command()
def process(
    provider: str = typer.Option(
        ...,
        help="LLM provider (anthropic/openai)"
    ),
):
    """Process with specified provider."""

    # Show available providers
    available = []
    if ANTHROPIC_AVAILABLE:
        available.append("anthropic")
    if OPENAI_AVAILABLE:
        available.append("openai")

    typer.echo(f"Available providers: {', '.join(available)}")

    if provider not in available:
        typer.secho(
            f"Provider '{provider}' not installed.\n"
            f"Install with: pip install myapp[{provider}]",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # Continue with processing
    from myapp.providers.factory import create_provider
    llm = create_provider(provider)
    # ...
```

---

## Testing Strategy

### Test with Mocked Imports

```python
# tests/test_providers.py
import sys
from unittest.mock import MagicMock
import pytest

def test_anthropic_provider_unavailable():
    """Test error when Anthropic SDK not installed."""

    # Mock missing anthropic module
    anthropic_module = sys.modules.get('anthropic')
    sys.modules['anthropic'] = None

    try:
        # Reload to trigger ImportError
        import importlib
        import myapp.providers
        importlib.reload(myapp.providers)

        assert not myapp.providers.ANTHROPIC_AVAILABLE

        with pytest.raises(RuntimeError, match="not installed"):
            from myapp.providers.factory import create_provider
            create_provider("anthropic")
    finally:
        # Restore original module
        if anthropic_module:
            sys.modules['anthropic'] = anthropic_module
```

### Test Matrix with tox

```ini
# tox.ini
[tox]
envlist = py312-{anthropic,openai,all}

[testenv]
deps =
    pytest
    anthropic: anthropic>=0.40.0
    openai: openai>=1.0.0
    all: anthropic>=0.40.0
    all: openai>=1.0.0

commands =
    pytest tests/
```

---

## Real-World Examples

### FastAPI
```bash
pip install fastapi               # Minimal
pip install fastapi[standard]     # All recommended extras
```

### SQLAlchemy
```bash
pip install sqlalchemy            # Core only
pip install sqlalchemy[postgresql]
pip install sqlalchemy[mysql]
pip install sqlalchemy[asyncio]
```

### pytest
```bash
pip install pytest                # Core
pip install pytest[testing]       # Additional test tools
```

### Requests
```bash
pip install requests              # Core
pip install requests[security]    # Security extras
pip install requests[socks]       # SOCKS proxy support
```

---

## Advanced: Combining Extras

### Cross-Product Groups

```toml
[project.optional-dependencies]
# Providers
anthropic = ["anthropic>=0.40.0"]
openai = ["openai>=1.0.0"]

# Features
batch = ["aiofiles>=23.0"]
ocr = ["ocrmypdf>=16.0.0"]

# Combinations
anthropic-batch = ["anthropic>=0.40.0", "aiofiles>=23.0"]
openai-batch = ["openai>=1.0.0", "aiofiles>=23.0"]

# All combinations
all = [
    "anthropic>=0.40.0",
    "openai>=1.0.0",
    "aiofiles>=23.0",
    "ocrmypdf>=16.0.0",
]
```

### Recommendation Groups

```toml
[project.optional-dependencies]
# Minimal working setup
recommended = [
    "anthropic>=0.40.0",
    "rich>=13.0",  # Better CLI output
]

# Power user setup
complete = [
    "anthropic>=0.40.0",
    "openai>=1.0.0",
    "rich>=13.0",
    "aiofiles>=23.0",
    "ocrmypdf>=16.0.0",
]
```

---

## Benefits

### For Users
- ✅ **Minimal installation**: Only install what they need
- ✅ **Faster installation**: Fewer packages to download
- ✅ **Less disk space**: No unused dependencies
- ✅ **Fewer conflicts**: Smaller dependency tree
- ✅ **Clear choices**: Explicit opt-in for features

### For Developers
- ✅ **Flexibility**: Support many backends without forcing all
- ✅ **Testing**: Can test each backend independently
- ✅ **Maintenance**: Can deprecate backends gradually
- ✅ **Documentation**: Clear dependency requirements per feature

---

## Gotchas

### 1. Circular Imports

**Problem:** Checking availability in `__init__.py` can cause circular imports.

**Solution:** Use separate `_availability.py` module:

```python
# myapp/_availability.py
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# myapp/__init__.py
from myapp._availability import ANTHROPIC_AVAILABLE
```

### 2. Type Checking

**Problem:** `mypy` complains about imports that might not exist.

**Solution:** Use `TYPE_CHECKING` guard:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import anthropic
    import openai

def create_provider(name: str):
    if name == "anthropic":
        import anthropic  # Runtime import
        # ...
```

### 3. Documentation

**Problem:** Users don't know which extras to install.

**Solution:** Clear documentation in README:

```markdown
## Installation

Choose the provider(s) you need:

### Anthropic Claude only
\`\`\`bash
pip install myapp[anthropic]
\`\`\`

### OpenAI GPT only
\`\`\`bash
pip install myapp[openai]
\`\`\`

### Both (for comparison)
\`\`\`bash
pip install myapp[all]
\`\`\`
```

---

## When to Use This Pattern

**Use optional dependencies when:**
1. Supporting multiple backends/providers
2. Some dependencies are large (> 10 MB)
3. Users typically need only 1-2 of N options
4. Dependencies might conflict (e.g., different TensorFlow versions)

**Don't use optional dependencies when:**
1. All features are commonly used together
2. Dependencies are small (< 1 MB total)
3. Complexity outweighs benefits
4. Users expect "batteries included"

---

## Related Patterns

- `ai-era-architecture-principles.md` - When to minimize dependencies
- `cost-aware-llm-pipeline.md` - Provider abstraction for LLM costs
