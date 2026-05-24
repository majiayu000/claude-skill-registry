---
name: python-uv
description: Run Python scripts with automatic dependency management using uv. Use this skill when you need to (1) run Python scripts with external dependencies without polluting system Python, (2) create standalone Python scripts with inline dependencies (PEP 723), (3) convert existing scripts to use uv with inline metadata, (4) handle ModuleNotFoundError by running scripts with uv run --with, or (5) create CLI tools, data processing scripts, or API clients that are self-contained and portable.
---

# Python uv Script Management

## Overview

This skill helps create and run Python scripts with automatic dependency management using `uv` tool. It provides two approaches: inline dependencies (PEP 723) for new/converted scripts, and `uv run --with` for running existing scripts without modification.

## Quick Decision Guide

**When to use each approach:**

- **Inline Dependencies (PEP 723)** → Creating new scripts or converting scripts for distribution
- **`uv run --with`** → Running existing third-party scripts or quick one-off execution

## Approach 1: Inline Dependencies (Recommended)

### When to Use

- Creating new standalone scripts
- Scripts that will be shared or distributed
- Long-term maintainable scripts
- Scripts with known, stable dependencies

### Basic Template

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "package-name>=version",
# ]
# requires-python = ">=3.11"
# ///

import package_name

# Your code here
```

### Creating New Scripts

Use the template assets based on your use case:

1. **CLI tool** → `assets/template-cli.py` - Command-line tools with argument parsing
2. **Data processing** → `assets/template-data.py` - Pandas-based data analysis
3. **API client** → `assets/template-api.py` - REST API integration with auth

Copy the appropriate template and customize for your needs.

**Run with:** `./script.py` or `uv run script.py`

### Converting Existing Scripts

Use the utility script to add inline dependencies:

```bash
scripts/add_inline_dependencies.py <script.py> <dep1> [dep2] ...
```

Example:
```bash
scripts/add_inline_dependencies.py myscript.py "requests>=2.31.0" "pyyaml>=6.0"
```

This will:
- Add PEP 723 metadata block with dependencies
- Update shebang to `#!/usr/bin/env -S uv run --script`
- Make the script executable
- Preserve original code

## Approach 2: `uv run --with` for Old-Style Scripts

### When to Use

- Running existing scripts without modifying them
- Third-party scripts you can't or don't want to modify
- Quick testing with different dependency versions
- When encountering `ModuleNotFoundError` for unmaintained scripts

### Pattern

When you see import errors:

```
ModuleNotFoundError: No module named 'yaml'
```

Solution:
```bash
uv run --with pyyaml script.py
```

Multiple dependencies:
```bash
uv run --with pyyaml --with requests --with pandas script.py
```

### Common Import-to-Package Mappings

| Import Statement | Package Name |
|-----------------|--------------|
| `import yaml` | `pyyaml` |
| `import PIL` | `pillow` |
| `import bs4` | `beautifulsoup4` |
| `import dotenv` | `python-dotenv` |

**For complete mapping table and more details, see `references/uvx-guide.md`**

## Example Workflows

### Workflow 1: Create New CLI Tool

1. Copy template: `cp assets/template-cli.py mytool.py`
2. Customize the script for your use case
3. Make executable: `chmod +x mytool.py`
4. Run: `./mytool.py` or `uv run mytool.py`

### Workflow 2: Convert Existing Script

1. Identify missing dependencies from imports
2. Run: `scripts/add_inline_dependencies.py oldscript.py "dep1>=1.0" "dep2>=2.0"`
3. Test: `./oldscript.py`

### Workflow 3: Quick Fix for Module Errors

1. Encounter: `ModuleNotFoundError: No module named 'requests'`
2. Run: `uv run --with requests script.py`
3. If recurring, consider converting to inline dependencies

## Best Practices

1. **Always specify version constraints** (e.g., `"requests>=2.31.0"`) for reproducibility
2. **Pin Python version** if using newer language features
3. **Use `--script` flag** in shebang to enable inline dependency support
4. **Test after conversion** to ensure all dependencies are captured
5. **Prefer inline dependencies** for scripts you maintain or distribute
6. **Use `uv run --with`** for quick experiments or external scripts

## Resources

### scripts/
- `add_inline_dependencies.py` - Add PEP 723 metadata to existing Python scripts

### references/
- `uvx-guide.md` - Comprehensive guide with examples, troubleshooting, and detailed explanations

### assets/
- `template-cli.py` - CLI tool template with Click
- `template-data.py` - Data processing template with Pandas
- `template-api.py` - API client template with Requests

## Troubleshooting

**Script not found:** Install uv with `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Module not found during execution:** Use `uv run --with package-name script.py` for quick fix, or add to inline dependencies for permanent solution

**Permission denied:** Run `chmod +x script.py` to make executable

For more detailed troubleshooting, see `references/uvx-guide.md`.
