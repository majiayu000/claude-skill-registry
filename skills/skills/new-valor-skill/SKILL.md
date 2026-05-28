---
name: new-valor-skill
description: Build a new Valor-specific tool following established patterns. Use when creating tools that integrate with Valor's Telegram bridge, use SOUL.md persona, or should be documented in CLAUDE.md. Guides through planning, implementation, testing, and documentation phases.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
hooks:
  Stop:
    - hooks:
        - type: command
          command: >-
            uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_tool_structure.py
            --tools-dir tools
        - type: command
          command: >-
            uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_claude_md_updated.py
            --tools-dir tools
---

# New Valor Skill

Build a new Valor-specific tool following established patterns with validation.

## When to Use

- Creating a tool unique to Valor (not shared across projects)
- Building capabilities that integrate with Valor's Telegram bridge
- Adding features that should be documented in CLAUDE.md
- User says "create a new tool", "add a command", "build a valor tool"

## Valor-Specific vs Shared

| Valor-Specific | Shared/Generic |
|----------------|----------------|
| Uses SOUL.md persona | Works in any Claude Code context |
| Integrates with Telegram bridge | Standalone utility |
| References `config/` files | No Valor dependencies |
| Uses SDK client patterns | Generic Python module |
| Documented in CLAUDE.md | Self-contained docs |

**Valor-specific examples:** `valor-image-gen`, `valor-calendar`, Telegram history tools
**Shared examples:** `agent-browser` (npm package), generic file utilities

---

## Process

### Phase 1: Planning (gather requirements first)

Before writing any code, establish:

1. **Define the capability**
   - What does this tool do?
   - Who is the user? (Valor via Telegram, developer via CLI, both?)
   - What's the expected input/output?

2. **Identify integration points**
   - Does it need Telegram? (file sending, message formatting)
   - Does it call external APIs? (which ones, auth required?)
   - Does it use AI models? (check `config/models.py` for available models)

3. **Check for existing patterns**
   - Look at similar tools in `tools/` directory
   - Check if there's a model constant in `config/models.py`
   - Review `bridge/telegram_bridge.py` for file detection patterns

4. **List dependencies**
   - External APIs and their keys
   - Python packages needed
   - Environment variables required

5. **Choose the interface**
   - Python library only (`from tools.my_tool import func`)
   - CLI command (`valor-my-tool`)
   - Both (recommended)

### Phase 2: Implementation

Create the tool directory structure:

```
tools/<tool_name>/
├── __init__.py       # Main implementation (REQUIRED)
├── README.md         # Documentation (REQUIRED)
├── manifest.json     # Tool metadata (recommended)
└── tests/
    ├── __init__.py
    └── test_<tool>.py
```

#### __init__.py Template

```python
"""
Tool Name - Brief description.

Usage:
    from tools.tool_name import main_function
    result = main_function(arg1, arg2)

CLI:
    valor-tool-name arg1 arg2
"""

import argparse
import sys
from pathlib import Path

# Import model constants if using AI
# from config.models import MODEL_FAST, MODEL_REASONING

def main_function(arg1: str, arg2: str | None = None) -> dict:
    """
    Main tool function.

    Args:
        arg1: Description
        arg2: Optional description

    Returns:
        dict with 'result' key on success, 'error' key on failure
    """
    try:
        # Implementation
        result = do_work(arg1, arg2)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument("arg1", help="First argument")
    parser.add_argument("arg2", nargs="?", help="Optional second argument")
    args = parser.parse_args()

    result = main_function(args.arg1, args.arg2)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(result["result"])


if __name__ == "__main__":
    main()
```

#### manifest.json Template

```json
{
  "name": "tool-name",
  "version": "1.0.0",
  "description": "What this tool does",
  "type": "library",
  "status": "beta",
  "source": {"type": "internal"},
  "capabilities": ["capability1", "capability2"],
  "requires": {
    "env": ["API_KEY_NAME"],
    "python": ">=3.11"
  }
}
```

#### Register CLI in pyproject.toml

Add to `[project.scripts]`:

```toml
valor-tool-name = "tools.tool_name:main"
```

Then run:

```bash
pip install -e .
```

### Phase 3: Integration

#### Update CLAUDE.md

Add to the "Local Python Tools" or "Image Tools" section:

```markdown
- **Tool Name** (`valor-tool-name`): Brief description
  ```bash
  valor-tool-name arg1 arg2    # Example usage
  valor-tool-name --help       # Show options
  ```
```

#### Bridge Integration (if tool outputs files)

Files are auto-detected by `extract_files_from_response()` in the bridge.

For explicit file sending, use the marker:
```
<<FILE:/path/to/file>>
```

Check `ABSOLUTE_PATH_PATTERN` in `bridge/telegram_bridge.py` covers your file types.

#### Model Configuration (if using AI)

Import from `config/models.py`:
- `MODEL_FAST` - Quick responses (haiku-class)
- `MODEL_REASONING` - Complex tasks (sonnet-class)
- `MODEL_IMAGE_GEN` - Image generation
- `MODEL_VISION` - Image analysis

Add new constants if needed for specialized models.

### Phase 4: Testing

Create test file at `tools/<tool_name>/tests/test_<tool>.py`:

```python
"""Tests for tool_name."""

import os
import pytest
from tools.tool_name import main_function


class TestToolName:
    """Test suite for tool_name."""

    def test_basic_functionality(self):
        """Test happy path."""
        result = main_function("test_input")
        assert "error" not in result
        assert "result" in result

    @pytest.mark.skipif(
        not os.environ.get("REQUIRED_API_KEY"),
        reason="API key not set"
    )
    def test_real_api_call(self):
        """Test with real API (requires key)."""
        result = main_function("real_input")
        assert "error" not in result

    def test_error_handling(self):
        """Test error cases."""
        result = main_function("")
        # Should handle gracefully
        assert isinstance(result, dict)
```

Run tests:

```bash
pytest tools/<tool_name>/tests/ -v
```

Test CLI:

```bash
valor-tool-name --help
valor-tool-name test_arg
```

### Phase 5: Documentation

Ensure README.md contains:

1. **Overview** - What the tool does
2. **Installation** - Any extra dependencies
3. **Usage** - Python and CLI examples
4. **API Reference** - Main functions with parameters
5. **Environment Variables** - Required keys

### Phase 6: Deployment

```bash
# Format and lint
black tools/<tool_name>/
ruff check tools/<tool_name>/

# Commit
git add tools/<tool_name>/ pyproject.toml CLAUDE.md
git commit -m "Add valor-<name> tool for <purpose>"
git push

# Reinstall to register CLI
pip install -e .

# Restart bridge if bridge-integrated
pkill -f telegram_bridge.py
./scripts/start_bridge.sh

# Test in production
# Send test message via Telegram
```

---

## Validation

This skill has automatic validation hooks that check:

1. **Tool structure** - Directory exists with `__init__.py` and `README.md`
2. **CLAUDE.md updated** - Tool is documented for agent awareness

If validation fails, you'll receive specific instructions on what's missing.

---

## Reference Implementations

Look at these tools for patterns:

| Tool | Pattern | Key Features |
|------|---------|--------------|
| `tools/image_gen/` | API + file output | Gemini API, saves to `generated_images/` |
| `tools/image_analysis/` | Vision + multi-mode | Claude vision, multiple analysis types |
| `tools/sms_reader/` | System access | macOS database, CLI subcommands |
| `tools/telegram_history/` | Database query | SQLite, search patterns |

---

## Checklist

Use this to track progress:

- [ ] **Planning**: Defined capability, integration points, dependencies
- [ ] **Structure**: Created `tools/<name>/` with `__init__.py`, `README.md`
- [ ] **Implementation**: Main function with error handling, CLI entry point
- [ ] **CLI Registration**: Added to `pyproject.toml`, ran `pip install -e .`
- [ ] **CLAUDE.md**: Added documentation in appropriate section
- [ ] **Tests**: Created test file, tests pass
- [ ] **Lint**: `black` and `ruff` pass
- [ ] **Committed**: Changes pushed to git
- [ ] **Verified**: CLI works, tool functions correctly
