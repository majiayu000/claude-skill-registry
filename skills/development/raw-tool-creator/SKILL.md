---
name: raw-tool-creator
description: Create reusable RAW tools that workflows can import. Use when the user asks to create a tool, extract reusable functionality, or build a new capability for workflows.
---

# RAW Tool Creator Skill

Create reusable RAW tools for workflows.

## When to Use This Skill

Use this skill when:
- A workflow needs functionality that should be reusable
- The user asks to create a tool for a specific task
- You identify repeated logic that should be extracted

## Key Directives

1. **ALWAYS search existing tools first** - Run `raw search "<capability>"` (checks local and remote registry)
2. **PREFER installation** - If a remote tool exists, use `raw install <url>` instead of creating a new one
3. **ALWAYS use `raw create --tool`** to scaffold - do not manually create directories
4. **ALWAYS implement `tool.py`** with the actual logic - scaffolds without code are useless
5. **ALWAYS write tests** in `test.py` - untested tools are unreliable
6. **Single responsibility** - One tool does one thing well
7. **Use underscores in names** - Tool names become Python modules (`web_scraper`, not `web-scraper`)

## Prerequisites Checklist

Before creating a tool:
- [ ] RAW is initialized (`.raw/` directory exists)
- [ ] Searched `raw search` and found NO suitable local or remote tool
- [ ] Clear understanding of inputs and outputs

## Requirements Validation (Ask Before Building)

**Before implementing, ask clarifying questions when:**

| Ambiguity | Example Question |
|-----------|------------------|
| Input format unclear | "Should the function accept a file path or file contents?" |
| Output structure unspecified | "Should this return a dict, list, or a custom object?" |
| Error handling unclear | "Should errors raise exceptions or return error objects?" |
| API/provider choice | "Should I use requests or httpx for HTTP calls?" |
| Scope ambiguous | "Should this tool also handle pagination, or just single requests?" |

If only one reasonable approach exists, proceed without asking.

## Tool Creation Process

### Step 1: Search Existing Tools

```bash
raw search "stock data"           # Semantic search (PREFERRED)
raw search "fetch prices"         # Try different phrasings
raw list tools                    # Browse local tools
```

**If a remote tool is found:**
```bash
raw install <git-url>
# Done! No need to create a new tool.
```

**If NO tool exists:** Proceed to Step 2.

### Step 2: Create Tool Scaffold

```bash
raw create <name> --tool -d "<what it does>"
```

**Naming conventions:**
- Use underscores: `fetch_stock`, `parse_csv`, `generate_pdf`
- Be specific: `fetch_stock` not `data_fetcher`
- Names are sanitized: `web-scraper` → `web_scraper` automatically

**Writing searchable descriptions:**

Descriptions are indexed for semantic search (`raw search`). Write them for discoverability.

Structure: `[Action verb] [what] [from/to where] [key capabilities]`

Good examples:
```
Fetch real-time stock prices, historical data, and dividends from Yahoo Finance API
Parse CSV files with automatic type detection, header handling, and encoding support
Generate PDF reports from structured data with charts, tables, and custom styling
```

Rules:
- Start with action verb: Fetch, Send, Generate, Convert, Parse, Validate, Scrape
- Include domain keywords that users might search for
- Mention data sources/destinations: from Yahoo Finance, to S3, via SMTP
- List key capabilities: retry logic, caching, pagination, HTML support
- Avoid: "This tool...", "A utility for...", "Used to..."

### Step 3: Implement tool.py

**Write the implementation** at `tools/<name>/tool.py`:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   # ADD REQUIRED DEPENDENCIES
# ]
# ///
"""<Tool description>"""

from typing import Any


def tool_name(
    required_param: str,
    optional_param: int = 10,
) -> dict:
    """<Tool description>

    Args:
        required_param: What this parameter is for
        optional_param: What this does (default: 10)

    Returns:
        Dictionary with results

    Raises:
        ValueError: If inputs are invalid
    """
    # === Input Validation ===
    if not required_param:
        raise ValueError("required_param cannot be empty")

    # === Main Logic ===
    # IMPLEMENT THE TOOL'S CORE FUNCTIONALITY

    result = {"processed": True}

    # === Return Results ===
    return result


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--required-param", required=True)
    parser.add_argument("--optional-param", type=int, default=10)
    args = parser.parse_args()

    result = tool_name(args.required_param, args.optional_param)
    print(json.dumps(result, indent=2, default=str))
```

### Step 4: Update __init__.py

The scaffold creates an `__init__.py` with a placeholder import. **You must update it** to export your actual functions:

```python
"""<Tool description>."""

# Update this to match your implemented functions in tool.py
from .tool import my_function  # Replace with your function names

__all__ = ["my_function"]
```

This enables imports like `from tools.fetch_stock import fetch_stock`.

### Step 5: Write Tests

**Create tests** at `tools/<name>/test.py`:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pytest>=8.0",
#   # SAME DEPS AS tool.py
# ]
# ///
"""Tests for <tool-name>."""

import pytest
from tool import tool_name


class TestToolName:
    def test_basic_usage(self) -> None:
        """Test normal usage."""
        result = tool_name("test_value")
        assert "processed" in result
        assert result["processed"] is True

    def test_with_options(self) -> None:
        """Test with optional parameters."""
        result = tool_name("test", optional_param=20)
        assert result is not None

    def test_invalid_input(self) -> None:
        """Test error handling."""
        with pytest.raises(ValueError):
            tool_name("")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Step 6: Run Tests

```bash
cd tools/<name>
uv run pytest test.py -v
```

**ONLY tell the user the tool is ready if tests pass.**

### Step 7: Update config.yaml

Edit `tools/<name>/config.yaml` with accurate:
- inputs (name, type, required, description)
- outputs (name, type, description)
- dependencies

### Step 8: Report to User

After tests pass:
```
Tool created and tested:
- Name: <tool_name>
- Location: tools/<name>/
- Usage: from tools.<name> import <function_name>
```

## Decision Tree

```
User needs tool
    │
    ├─► Search existing: `raw search "<capability>"`
    │       EXISTS → Use or extend existing
    │       NOT EXISTS → Continue
    │
    ├─► Create scaffold: `raw create <name> --tool -d "..."`
    │
    ├─► Implement tool.py
    │       - Input validation
    │       - Core logic
    │       - CLI support
    │
    ├─► Update __init__.py
    │       - Export your implemented functions
    │
    ├─► Write test.py
    │       - Basic usage
    │       - Edge cases
    │       - Error handling
    │
    ├─► Run tests: `uv run pytest test.py -v`
    │       FAIL → Fix and retry
    │       PASS → Continue
    │
    └─► Report success to user
```

See [references/best_practices.md](references/best_practices.md) for input validation, error handling, and output patterns.

See [references/examples.md](references/examples.md) for data fetcher, processor, and file generator examples.

## Validation checklist

Before reporting success:
- [ ] `tool.py` exists and runs standalone
- [ ] `__init__.py` exports public functions
- [ ] `test.py` exists with tests
- [ ] All tests pass
- [ ] config.yaml has accurate inputs/outputs
- [ ] Function has docstring with Args/Returns

## Error Recovery

When things go wrong during tool creation:

### Import Errors
```
ModuleNotFoundError: No module named 'requests'
```
**Fix:** Add to PEP 723 header in both `tool.py` and `test.py`:
```python
# /// script
# dependencies = ["requests>=2.28"]
# ///
```

### Test Failures
1. Read the assertion error carefully
2. Check if expected vs actual values make sense
3. Verify mock data matches real API format
4. Fix the code or update the test

### Type Errors
```
TypeError: expected str, got NoneType
```
**Fix:** Add input validation at function start:
```python
def fetch_data(url: str) -> dict:
    if not url:
        raise ValueError("url cannot be empty")
    # ...
```

### When Stuck
If you cannot resolve an error after 2 attempts:
1. Explain what's failing clearly
2. Show the error and your attempted fixes
3. Ask the user how they'd like to proceed

See [references/best_practices.md](references/best_practices.md) for common pitfalls and testing guidance.

## Progress communication

Keep the user informed during tool creation:

### During Implementation
```
Creating fetch_stock tool...
  ✓ Created tool scaffold
  ✓ Implementing main function
  ✓ Adding input validation
  ✓ Updating __init__.py with exports
  ✓ Writing tests
  ⏳ Running tests...
```

### After Completion
```
✓ Tool created and tested successfully!

  Name: fetch_stock
  Location: tools/fetch_stock/

  Usage:
    from tools.fetch_stock import fetch_stock
    data = fetch_stock("TSLA", period="3mo")

  3 tests passed ✓
```

### On Test Failure
```
✗ Tool tests failed

  FAILED test.py::TestFetchStock::test_invalid_ticker
    AssertionError: Expected ValueError for empty ticker

  The test expects the function to raise ValueError for invalid input,
  but currently it doesn't validate the ticker parameter.

  Would you like me to add input validation?
```

## Security

See [references/security.md](references/security.md) for security checklist and secure coding patterns.

## References

- [Tool Structure](references/tool_structure.md)
- [Best Practices](references/best_practices.md)
