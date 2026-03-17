---
name: best-practices-python
description: >
  Repo-specific Python best practices for agentic coding: Loguru + Typer + uv + pyproject.toml,
  httpx over requests, functions-first, module docstrings, max 800 LOC per file, and non-mocked sanity tests.
triggers:
  - best practices python
  - python conventions
  - loguru
  - typer
  - httpx
  - python code review
license: MIT
metadata:
  language: python
  python_versions: ["3.11+", "3.12+"]
  defaults:
    logging: loguru
    cli: typer
    http: httpx
    packaging: uv + pyproject.toml
    style:
      max_lines_per_file: 800
      module_docstring: required
      functions_over_classes: true
    testing:
      include_sanity_tests: true

provides:
  - best-practices-python
composes:
  - task-monitor
---

# Python Best Practices (Project Skill)

This skill is a curated set of atomic rules for writing and refactoring Python in *this* repo.

## Project Defaults (apply unless explicitly overridden)

- **Logging:** Loguru (`from loguru import logger`)
- **CLI:** Typer (thin CLI; logic in functions)
- **HTTP:** httpx (not requests)
- **Packaging:** uv + pyproject.toml
- **Structure:** functions over classes unless state is required
- **Files:** no Python file over **800** lines
- **Docs:** every module begins with a **clear module docstring** describing purpose, inputs, outputs, and failure modes
- **Tests:** include **non-mocked sanity tests** in addition to unit tests

## When to Apply

Use this skill whenever you:
- create or refactor Python modules, CLIs, services, or pipelines
- add network calls, subprocess calls, or IO
- change packaging/tooling (uv, pyproject)
- add tests or fix bugs/flakiness

## Categories (priority order)

1. Correctness (CRITICAL/HIGH): `correctness-`
2. Security (CRITICAL/HIGH): `security-`
3. Conventions (HIGH): `conventions-`
4. Testing & Sanity (HIGH/MEDIUM): `testing-`
5. Async & Concurrency (HIGH/MEDIUM): `async-`
6. Performance (MEDIUM): `perf-`
7. Packaging (MEDIUM): `packaging-`
8. Logging & Observability (MEDIUM): `logging-`
9. Style & Maintainability (MEDIUM/LOW): `style-`

## Quick Reference (house rules)

- `style-max-800-lines`
- `style-module-docstring`
- `conventions-loguru`
- `conventions-typer-cli`
- `conventions-httpx`
- `conventions-uv-pyproject`
- `conventions-functions-over-classes`
- `conventions-pyproject-deps-complete`
- `testing-non-mocked-sanity`

## pyproject.toml Dependency Completeness (NON-NEGOTIABLE)

**Every `import` in a skill's `.py` files MUST have a corresponding entry in `pyproject.toml` `[project.dependencies]`.**

This is a hard gate. Missing dependencies cause `ModuleNotFoundError` at runtime after `uv sync` in a clean venv — a silent regression that only surfaces when the skill is invoked by another agent or in CI.

### Rule: `conventions-pyproject-deps-complete`

When creating or modifying a Python skill with a `pyproject.toml`:

1. **Scan all `.py` files** in the skill for `import` and `from X import` statements
2. **Cross-reference** each top-level import against `[project.dependencies]`
3. **Add any missing** third-party packages to dependencies
4. **Run `uv sync`** after adding to verify resolution

### Common offenders (imports that look stdlib but aren't)

| Import | Package needed in pyproject.toml |
|--------|----------------------------------|
| `from loguru import logger` | `loguru>=0.7.0` |
| `import typer` | `typer>=0.9.0` |
| `import httpx` | `httpx>=0.24.0` |
| `from rich import ...` | `rich>=13.0.0` |
| `import pydantic` | `pydantic>=2.0` |
| `from dotenv import ...` | `python-dotenv>=1.0.0` |
| `import pytz` | `pytz` |
| `import tenacity` | `tenacity>=8.0` |

### Verification pattern

```bash
# After any pyproject.toml change:
cd /path/to/skill && uv sync && uv run python -c "import <every_module>"
```

### Why this matters

The ops-chutes skill broke (Feb 2026) because `loguru` was imported by 3 files but
missing from `pyproject.toml`. After `uv sync` recreated the venv, `loguru` vanished
and every downstream skill that called ops-chutes got `ModuleNotFoundError`. This was
a silent regression — the skill worked in the shared system venv but failed in isolation.
