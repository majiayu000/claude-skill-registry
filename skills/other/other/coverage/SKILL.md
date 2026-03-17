---
name: coverage
description: Check test coverage for unstaged changes. Use when user asks to "check coverage", "/coverage", or wants to see which unstaged changes lack test coverage.
---

# Coverage Check

## Context

Run in parallel:
- `git diff --name-only` - get unstaged files
- `git diff -U0 --no-color` - get changed line numbers

## Commands

Sequential:
1. `npm run test:ci` - vitest with coverage
2. `npm run coverage:report` - generate lcov/text reports

## Workflow

1. Get unstaged files and line ranges (parallel):
   - `git diff --name-only`
   - `git diff -U0 --no-color`
2. Run coverage:
   - `npm run test:ci`
   - `npm run coverage:report`
3. Parse `coverage/lcov.info` (see `lcov-format.md` for format details)
4. Map changed lines to coverage data
5. Report uncovered lines: `file.ts:42`
6. Summary: X/Y changed lines covered

## Rules

- Only analyze unstaged changes (`git diff`)
- Use sequential commands: `test:ci` then `coverage:report`
- Parse lcov.info for coverage data
- Report uncovered lines: `file.ts:42`
- Ignore files without coverage data (non-code files)
