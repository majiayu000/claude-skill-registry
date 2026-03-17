---
name: service-layer-extraction
description: "Use when a Typer/Click CLI module exceeds 300 LOC with mixed concerns. Extract business logic into a testable service layer."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-11"
---
# Service Layer Extraction from CLI

**Extracted:** 2026-02-11
**Context:** Refactoring a Typer/Click CLI module to separate business logic into a testable service layer

## Problem

CLI modules (e.g., `main.py` with Typer) accumulate business logic alongside CLI concerns. This makes the logic untestable without CLI runners and blocks reuse from other interfaces (Web UI, SDK).

## Solution

Extract business logic into `service.py` with these translation rules:

| CLI Layer (main.py) | Service Layer (service.py) |
|---------------------|---------------------------|
| `typer.BadParameter` | `ValueError` |
| CLI enums (`OutputFormat`) | Plain strings (`"tsv"`, `"off"`) |
| `console.print()` (Rich) | `logger.info()` (logging) |
| Private names (`_collect_files`) | Public names (`collect_files`) |

### Conversion at the boundary (main.py):

```python
# Catch service ValueError, convert to CLI output
try:
    files = collect_files(path)
except ValueError as e:
    console.print(f"[red]Error:[/red] {e}")
    raise typer.Exit(code=1) from e

# Pass enum .value to service layer
result = process_file(quality=quality.value, fmt=fmt.value)
```

## When to Use

- CLI module exceeds ~300 LOC with mixed concerns
- Business logic needs testing without CliRunner
- Planning a second interface (Web UI, API, SDK)
