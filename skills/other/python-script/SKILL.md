---
name: python-script
description: Create robust Python automation with full logging and safety checks. Use when tasks need complex data processing, authenticated API work, conditional file operations, or error handling beyond simple shell commands.
---

# Python Scripter

## Overview

Design and run Python scripts with clear requirements, safety checks, and reproducible logging.

## Workflow

1. Confirm inputs, outputs, constraints, and preferred libraries.
2. Identify risky operations and secure explicit approval.
3. Scaffold a script with PEP 723 metadata and structured logging.
4. Lint with `uvx ruff check --fix .agents/scripts/{script_name}.py`.
5. Run with `uv run --script .agents/scripts/{script_name}.py` and monitor logs.
6. Report results, risks encountered, and any follow-up steps.

## Logging requirements

- Log to `.agents/logs/{script_name}.log` and stream to console
- Capture start/end timestamps, parameters, file operations, and errors
- Add `RotatingFileHandler` if logs may grow large

## Template

Read `references/script-template.md` for the full script template.

## Safety practices

- Provide dry-run or rollback paths
- Validate external inputs and API responses
- Use temporary directories for intermediates
- Never run destructive steps without confirmation
