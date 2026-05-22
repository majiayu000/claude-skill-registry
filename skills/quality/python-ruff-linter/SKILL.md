---
name: python-ruff-linter
description: Ensure Python code follows industry standards using Ruff linter with linting-workflow framework
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: code-quality
---

## What I do

I implement Python-specific Ruff linting by extending the `linting-workflow` framework:

1. **Detect Python Environment**: Identify Python project (Poetry or pip)
2. **Detect Ruff Linter**: Check if Ruff is installed and configured
3. **Delegate to Linting Workflow**: Use `linting-workflow` for core linting functionality
4. **Provide Python-Specific Guidance**: Help interpret Ruff error codes (F401, E501, etc.)
5. **Ensure PEP 8 Compliance**: Guide on Python style standards

## When to use me

Use this workflow when:
- Writing or modifying Python code that needs to follow industry standards
- Before committing Python changes to ensure code quality
- When you see Ruff linting errors and need help fixing them
- Setting up a new Python project with proper linting configuration
- You want to ensure code quality in automated workflows

**Framework**: This skill extends `linting-workflow` for generic linting, adding Python-specific Ruff guidance.

## Steps

### Step 1: Detect Python Environment

Verify this is a Python project:
```bash
# Check for Python files
ls *.py 2>/dev/null

# Check for Python project files
[ -f pyproject.toml ] || [ -f requirements.txt ] || [ -f setup.py ]
```

### Step 2: Detect Ruff Configuration

Check for Ruff in project:
```bash
# Check pyproject.toml for Ruff
grep -q "ruff" pyproject.toml || grep -q "ruff" requirements.txt
```

### Step 3: Detect Poetry

Check if Poetry is installed:
```bash
poetry --version 2>/dev/null
```

### Step 4: Delegate to Linting Workflow

Use `linting-workflow` framework for:
- Language detection (Python)
- Linter detection (Ruff)
- Package manager detection (Poetry or pip)
- Running linting with appropriate commands
- Auto-fix application
- Error resolution guidance
- Verification and re-running

### Step 5: Python-Specific Ruff Error Guidance

**Common Ruff Error Codes**:

| Error Code | Description | Common Fix |
|------------|-------------|-----------|
| F401 | Unused imports | Remove or use import |
| F841 | Unused variables | Remove or use variable |
| E501 | Line too long (>88) | Break into multiple lines |
| E722 | Missing docstring | Add function docstring |
| W291 | Trailing whitespace | Remove trailing spaces |
| E731 | Class name should use CapWords | Rename class |
| F821 | Redefined variable | Rename variable |
| E231 | Unexpected indentation | Fix indentation level |

**Error Resolution Template**:
```
For each Ruff error found:

1. **File**: <file>
   Line: <line>
   Error: <error message>
   Code: <F401 | E501 | etc.>

2. **Ruff Rule Explanation**:
   <Description of what Ruff is checking>

3. **Recommended Fix**:
   <Step-by-step fix instructions>

4. **Example**:
   ```python
   # Before (incorrect)
   <code>

   # After (corrected)
   <code>
   ```

5. **Apply Fix**:
   <Action to take>
```

## Best Practices

**Refer to `linting-workflow` for general linting best practices.**

Python-specific best practices:
- **PEP 8**: Follow Python Enhancement Proposal 8 style guide
- **Type Hints**: Use type hints for better code quality and IDE support
- **Docstrings**: Follow PEP 257 for docstring conventions
- **Import Order**: Use `ruff check --select I001` or configure `isort`
- **Code Organization**: Separate concerns into modules/packages
- **Virtual Environments**: Use Poetry for dependency management and isolation
- **Ruff Configuration**: Tailor Ruff settings for your project needs

## Common Ruff Issues

### Poetry Not Detected

**Issue**: Poetry is installed but `linting-workflow` doesn't detect it

**Solution**: Ensure Poetry is detected:
```bash
poetry --version
```

### Ruff Not Installed

**Issue**: Ruff is not available

**Solution**: Install Ruff:
```bash
# With Poetry
poetry add --group dev ruff

# With pip
pip install ruff
```

### Ruff Configuration Issues

**Issue**: Ruff doesn't follow project style

**Solution**: Update `pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W"]
ignore = []
```

## Troubleshooting Checklist

Before linting:
- [ ] Python project is identified
- [ ] Ruff is installed
- [ ] Poetry is detected (if applicable)
- [ ] Configuration files exist

After linting:
- [ ] Linting completed successfully
- [ ] Auto-fix applied (if errors found)
- [ ] Errors are categorized and displayed
- [ ] User receives Python-specific guidance
- [ ] Linting is re-run after fixes

## Related Commands

```bash
# Poetry + Ruff
poetry run ruff check .
poetry run ruff check . --fix
poetry add --group dev ruff

# Direct Ruff
ruff check .
ruff check . --fix

# Ruff checks
ruff check --select E,F,W .
ruff check --ignore E501 .
```

## Related Skills

- `linting-workflow`: Core linting framework
- `python-pytest-creator`: Python test generation
