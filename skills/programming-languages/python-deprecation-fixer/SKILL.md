---
name: python-deprecation-fixer
description: Automatically detect and fix Python deprecation warnings in codebases, including datetime.utcnow(), and other common deprecated patterns. Supports extensible pattern matching for future deprecations.
---

# Python Deprecation Fixer

## Overview

This skill automatically detects and fixes Python deprecation warnings across your codebase. It uses intelligent pattern matching to identify deprecated code patterns and applies the recommended modern alternatives. The skill is designed to be extensible, allowing easy addition of new deprecation patterns as Python evolves.

## When to Use This Skill

Use this skill when:
- You encounter Python deprecation warnings in your code
- Upgrading to a newer Python version (e.g., 3.12+)
- Modernizing a legacy Python codebase
- Running linters that flag deprecated APIs
- You see warnings like "DeprecationWarning: datetime.utcnow() is deprecated"

Common deprecation scenarios:
- `datetime.utcnow()` → `datetime.now(UTC)`
- `datetime.utcfromtimestamp()` → `datetime.fromtimestamp(UTC)`
- `asyncio.coroutine` decorator → `async def`
- `collections.Mapping` → `collections.abc.Mapping`
- Other deprecated stdlib patterns

## Quick Start

### Scan for Deprecations

Scan your codebase to find all deprecation issues:

```bash
python3 scripts/fix_deprecations.py /path/to/project --scan-only
```

This will report all deprecated patterns found without making changes.

### Fix All Deprecations

Automatically fix all detected deprecations:

```bash
python3 scripts/fix_deprecations.py /path/to/project --fix
```

### Preview Changes

See what would be changed before applying fixes:

```bash
python3 scripts/fix_deprecations.py /path/to/project --dry-run
```

## Usage Options

### Basic Commands

**Scan only (no changes):**
```bash
python3 scripts/fix_deprecations.py /path/to/project --scan-only
```

**Fix with automatic backup:**
```bash
python3 scripts/fix_deprecations.py /path/to/project --fix
```

**Dry run (show changes without applying):**
```bash
python3 scripts/fix_deprecations.py /path/to/project --dry-run
```

### Advanced Options

**Target specific files:**
```bash
python3 scripts/fix_deprecations.py /path/to/project --fix --files "*.py" --exclude "tests/*"
```

**Fix specific deprecation types:**
```bash
# Only fix datetime deprecations
python3 scripts/fix_deprecations.py /path/to/project --fix --pattern datetime

# Only fix asyncio deprecations
python3 scripts/fix_deprecations.py /path/to/project --fix --pattern asyncio
```

**Control output verbosity:**
```bash
# Verbose output with detailed changes
python3 scripts/fix_deprecations.py /path/to/project --fix --verbose

# JSON output for programmatic use
python3 scripts/fix_deprecations.py /path/to/project --scan-only --json
```

**Skip imports check:**
```bash
# Fix patterns without verifying imports exist
python3 scripts/fix_deprecations.py /path/to/project --fix --no-import-check
```

## Supported Deprecation Patterns

### datetime Module (Python 3.12+)

**Pattern:** `datetime.utcnow()`
**Replacement:** `datetime.now(UTC)`
**Import required:** `from datetime import UTC`

Example:
```python
# Before
from datetime import datetime
timestamp = datetime.utcnow()

# After
from datetime import datetime, UTC
timestamp = datetime.now(UTC)
```

**Pattern:** `datetime.utcfromtimestamp(ts)`
**Replacement:** `datetime.fromtimestamp(ts, UTC)`

Example:
```python
# Before
dt = datetime.utcfromtimestamp(1234567890)

# After
from datetime import UTC
dt = datetime.fromtimestamp(1234567890, UTC)
```

### asyncio Module

**Pattern:** `@asyncio.coroutine`
**Replacement:** `async def`

Example:
```python
# Before
@asyncio.coroutine
def my_func():
    yield from something()

# After
async def my_func():
    await something()
```

### collections Module

**Pattern:** `collections.Mapping`, `collections.Sequence`, etc.
**Replacement:** `collections.abc.Mapping`, `collections.abc.Sequence`

Example:
```python
# Before
from collections import Mapping

# After
from collections.abc import Mapping
```

## How It Works

The fixer uses a multi-step approach:

1. **Pattern Detection:** Searches Python files using AST (Abstract Syntax Tree) parsing
2. **Context Analysis:** Verifies the deprecation applies in context (e.g., checks imports)
3. **Smart Replacement:** Applies the recommended fix while preserving formatting
4. **Import Management:** Automatically adds required imports (e.g., `UTC`)
5. **Validation:** Optionally runs syntax checks after modifications

## Output Format

### Scan Results

```
🔍 Scanning for Python deprecations in: /path/to/project

Found 3 deprecation issues:

📄 src/models.py
  Line 42: datetime.utcnow() → datetime.now(UTC)
  Line 127: datetime.utcfromtimestamp(ts) → datetime.fromtimestamp(ts, UTC)

📄 src/utils.py
  Line 15: datetime.utcnow() → datetime.now(UTC)

Summary:
  - datetime deprecations: 3
  - Files affected: 2
```

### Fix Results

```
🔧 Fixing Python deprecations in: /path/to/project

✅ src/models.py
  ✓ Line 42: Fixed datetime.utcnow() → datetime.now(UTC)
  ✓ Line 127: Fixed datetime.utcfromtimestamp() → datetime.fromtimestamp(UTC)
  ✓ Added import: from datetime import UTC

✅ src/utils.py
  ✓ Line 15: Fixed datetime.utcnow() → datetime.now(UTC)
  ✓ Added import: from datetime import UTC

Summary:
  - Files modified: 2
  - Total fixes applied: 3
  - Backup created: /path/to/project/.deprecation-backups/2025-10-26-09-02/
```

## Adding New Deprecation Patterns

To add support for new deprecation patterns, edit `scripts/deprecation_patterns.json`:

```json
{
  "patterns": [
    {
      "name": "datetime_utcnow",
      "category": "datetime",
      "deprecated": "datetime.utcnow()",
      "replacement": "datetime.now(UTC)",
      "regex": "datetime\\.utcnow\\(\\)",
      "replacement_template": "datetime.now(UTC)",
      "required_imports": ["from datetime import UTC"],
      "python_version": "3.12+",
      "description": "datetime.utcnow() is deprecated in favor of timezone-aware datetime.now(UTC)"
    }
  ]
}
```

## Best Practices

1. **Always backup before fixing:** The script creates automatic backups, but consider using version control
2. **Run tests after fixing:** Ensure your test suite passes after applying fixes
3. **Review changes:** Use `--dry-run` first to review what will change
4. **Fix incrementally:** For large codebases, fix one pattern at a time
5. **Check imports:** Verify all required imports are added correctly

## Integration with Development Workflow

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python3 ~/.claude/skills/python-deprecation-fixer/scripts/fix_deprecations.py . --scan-only
if [ $? -ne 0 ]; then
    echo "⚠️  Deprecation warnings found. Run fix_deprecations.py --fix"
    exit 1
fi
```

### CI/CD Integration

Add to your CI pipeline:
```yaml
- name: Check for Python deprecations
  run: |
    python3 scripts/fix_deprecations.py . --scan-only --json > deprecations.json
    if [ $(jq '.total_issues' deprecations.json) -gt 0 ]; then
      echo "Found deprecated code patterns"
      exit 1
    fi
```

## Troubleshooting

### Script doesn't find deprecations

- Ensure you're scanning `.py` files
- Check that the pattern is defined in `deprecation_patterns.json`
- Try `--verbose` to see detailed scanning info

### Fixes break syntax

- The script validates syntax after changes
- If issues occur, restore from the automatic backup in `.deprecation-backups/`
- Report the issue with `--verbose` output

### Import errors after fixing

- Check that all required imports were added
- Some patterns require specific Python versions
- Verify your Python version supports the replacement (e.g., `UTC` requires 3.11+)

## Resources

### scripts/

- **fix_deprecations.py**: Main script that detects and fixes deprecated Python patterns using AST parsing and intelligent replacement
- **deprecation_patterns.json**: Configuration file defining all supported deprecation patterns - easily extensible for new patterns
- **test_deprecations.py**: Test suite to verify the fixer works correctly on various code patterns

## Example Workflow

```bash
# 1. Scan your project
cd ~/my-python-project
python3 ~/.claude/skills/python-deprecation-fixer/scripts/fix_deprecations.py . --scan-only

# 2. Review what would change
python3 ~/.claude/skills/python-deprecation-fixer/scripts/fix_deprecations.py . --dry-run

# 3. Apply fixes
python3 ~/.claude/skills/python-deprecation-fixer/scripts/fix_deprecations.py . --fix

# 4. Run tests
pytest

# 5. Review changes and commit
git diff
git add -A
git commit -m "fix: update deprecated datetime.utcnow() calls"
```
