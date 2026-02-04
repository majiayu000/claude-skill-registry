---
name: lint-and-fix
description: Run make format and make lint, then fix linter violations. Use when formatting code or fixing trunk/lint issues.
compatibility: Requires trunk (make format, make lint).
---

# Lint-and-Fix

## Purpose

An autonomous loop to format the codebase, run linters, and fix any remaining violations until the project passes format and lint checks.

## Loop Logic

1. **Format**: Run `make format` (trunk fmt).
2. **Identify**: Run `make lint` to list current failures.
3. **Analyze**: Read the linter output and the affected code.
4. **Fix**: Apply the minimum necessary change to resolve each issue.
5. **Verify**: Re-run `make format` and `make lint`.
   - If both pass: Done.
   - If failures remain: Repeat from step 2 (or move to the next issue).

## Termination Criteria

- No failures from `make lint` after fixes.
- Optional: Cap iterations (e.g. 5) to avoid unbounded loops.

## Reference

Format and lint commands are defined in the project Makefile: `make format` runs `trunk fmt -a`; `make lint` runs `trunk check -a -y`.
