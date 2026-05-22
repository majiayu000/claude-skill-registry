---
name: quality-gates
description: Python code quality gates script for linting, type checking, complexity analysis, and testing before commits. Use when enforcing consistent code quality across Python projects with fast (unit-tests) or comprehensive (all-tests) modes.
license: Complete terms in LICENSE.txt
metadata:
  author: eder
  version: "1.0"
---

# Quality Gates

## Overview

Project-agnostic bash script enforcing Python code quality gates using ruff, pyrefly, radon, hypothesis, pytest, and markdownlint. Three execution modes provide flexibility for different workflows: unit-tests for fast feedback, all-tests for comprehensive pre-merge validation, no-tests for static analysis only. Coverage runs are excluded by default; run coverage only when the user explicitly requests it.

## When to Use

Before committing Python code to enforce consistent quality checks across projects without directory structure assumptions.

## Modes

| Mode           | Gates Run                                                                            | Use Case                             |
|----------------|--------------------------------------------------------------------------------------|--------------------------------------|
| **unit-tests** | ruff, pyrefly, radon, hypothesis checks, pytest (unit/), markdownlint                | Fast feedback during development     |
| **all-tests**  | ruff, pyrefly, radon, hypothesis checks, pytest (unit/ + integration/), markdownlint | Pre-merge/deploy comprehensive check |
| **no-tests**   | ruff, pyrefly, radon, hypothesis checks, markdownlint                                | Static analysis only (time critical) |

## Quick Start

**Running quality gates:**

Make sure uv is installed.

```bash
# Fast feedback: lint + type check + unit tests
.claude/skills/quality-gates/scripts/quality-gates.sh unit-tests

# Pre-merge: everything including integration tests
.claude/skills/quality-gates/scripts/quality-gates.sh all-tests

# Quick static checks only
.claude/skills/quality-gates/scripts/quality-gates.sh no-tests
```

## Implementation Details

- **Script**: `scripts/quality-gates.sh` - Uses uv/uvx for tool management
- **Excluded directories**: tests, test, docs, doc, examples, scripts, build, dist, .venv, venv, .tox, .git, node_modules, **pycache**, *.egg-info
- **Graceful fallbacks**: Skips missing tools without failing

## Common Anti-Patterns

| Rationalization              | Reality                                                              |
|------------------------------|----------------------------------------------------------------------|
| "Time-critical, skip checks" | Use no-tests mode for fast static validation                         |
| "Already tested manually"    | Automation catches edge cases manual testing misses                  |
| "Partial checks sufficient"  | Modes provide full coverage options; incomplete coverage misses bugs |
| "Coverage by default"        | Coverage pollutes context; run it only when explicitly requested     |
| "Too slow"                   | Tools are fast; skipping misses complexity and type issues           |
| "Script not in project"      | Copy to project to .claude/; run locally                             |
| "Tools not installed"        | Install uv; graceful fallbacks skip missing tools                    |

## Red Flags

Stop and re-evaluate if you're:

- Skipping all checks
- "This time is different"
- "Good enough for now"
- Rationalizing under deadline pressure
- Adding coverage without an explicit request

All of these suggest running the script with the appropriate mode.
