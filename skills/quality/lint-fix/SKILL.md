---
name: lint-fix
description: Iteratively run linters, apply auto-fixes, and resolve remaining issues using Trunk.
---

# Lint & Fix with Trunk

## Purpose

This skill provides an autonomous loop for identifying, fixing, and verifying linting and formatting issues using `trunk`. Use this when you need to ensure the codebase adheres to project standards or when fixing specific lint errors.

## Loop Logic

1.  **Auto-Format**: Run `trunk fmt` (or `trunk fmt -a`) to apply automatic formatting fixes.
2.  **Discovery**: Run `trunk check -y` (or `trunk check -a -y` for all files) to list current linting issues.
3.  **Analyze**: For any remaining issues from Step 2:
    - Examine the error message and the failing code.
    - Identify the specific rule being violated (e.g., Ruff `E501`, Shellcheck `SC2086`).
4.  **Fix**: Apply the minimum necessary change to resolve the manual fix required.
5.  **Verify**: Re-run `trunk check -y` on the affected file(s).
    - If passed: Move to next issue.
    - If failed: Analyze the new failure and repeat the loop.

## Termination Criteria

- No more errors reported by `trunk check -y`.
- Reached max iteration limit (default: 5).

## Common Commands

| Task                 | Command                 |
| :------------------- | :---------------------- |
| Check changed files  | `trunk check -y`        |
| Check all files      | `trunk check -a -y`     |
| Format changed files | `trunk fmt`             |
| Format all files     | `trunk fmt -a`          |
| Check specific file  | `trunk check -y <path>` |
| Format specific file | `trunk fmt <path>`      |

## Examples

### Scenario: Fixing Python Lint Errors

1.  `trunk check -y` reports `ruff: D103` (missing docstring) in `scripts/utils.py` (after auto-fixing unused imports).
2.  Agent adds the missing docstring in `scripts/utils.py`.
3.  `trunk check -y scripts/utils.py` passes.
