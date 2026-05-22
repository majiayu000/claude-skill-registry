---
name: coding-conventions
description: Provides coding style rules for Python and PowerShell. Apply when writing, editing, reviewing, or debugging code.
---

# Coding Conventions

This skill contains language-specific coding convention files.

## Verb Mapping

This skill implements:
- [IMPLEMENT] - Apply coding style during implementation
- [REFACTOR] - Apply coding style during refactoring

**Phases**: IMPLEMENT, REFINE

## Available Convention Files

- `PYTHON-RULES.md` - Python coding conventions (formatting, imports, logging, etc.)
- `JSON-RULES.md` - JSON coding conventions (field naming, 2-space indent, 2D table formatting)
- `WORKFLOW-RULES.md` - Workflow document conventions (structure, formatting)
- `AGENT-SKILL-RULES.md` - Agent skill folder structure and SKILL.md conventions

## Tools

- `reindent.py` - Convert Python file indentation to target spaces

## Usage

Read the appropriate convention file for the language you are working with.

### reindent.py

Convert Python indentation to target spaces. Auto-detects source indentation and skips files already at target. Excludes itself from processing.

```powershell
# Convert folder to 2-space indentation
python reindent.py folder/ --to 2 --recursive

# Dry-run (preview only)
python reindent.py folder/ --to 2 --recursive --dry-run

# Single file
python reindent.py script.py --to 2
```
