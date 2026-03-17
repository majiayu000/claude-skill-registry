---
name: vitest-react-ts-coverage-enforce
description: Configure and enforce 100% coverage in Vitest for a React-TS project (include uncovered files, set thresholds=100 globally and per-file, choose provider v8/istanbul, add HTML report and CI-friendly scripts).
argument-hint: "[provider: v8|istanbul] [reporters] [ci]"
allowed-tools: Read, Write, Grep, Glob
---

# Enforce 100% Coverage (Vitest)

You are ensuring coverage enforcement is strict and fails builds when anything drops below 100%.

## Non-negotiables

1) Include source files in coverage even if not imported by tests.
2) Set thresholds to 100 for lines/functions/branches/statements.
3) Enable per-file thresholds to prevent a single file being under-tested.
4) Keep exclusions minimal and justified (types, stories, test utilities, entrypoints).

Use template.md as the default structure.
