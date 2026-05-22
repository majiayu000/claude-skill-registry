---
name: deslop
description: Remove low-quality AI-generated code patterns
argument-hint: "[--fix] [--report-only]"
tags: [quality, cleanup, deslop, refactoring]
user-invocable: true
---

# Deslop -- Remove AI Slop

Detect and fix common low-quality AI-generated code patterns.

## Patterns Detected

1. **Unnecessary comments**: `// Get the user` before `GetUser()`
2. **Over-abstraction**: Single-use interfaces, unnecessary factories
3. **Verbose null checks**: Where null-conditional (`?.`) suffices
4. **Redundant try-catch**: Catching only to rethrow
5. **Magic strings**: Hardcoded values that should be constants
6. **Dead parameters**: Parameters that are never used
7. **Excessive logging**: Logging at every method entry/exit
8. **Copy-paste patterns**: Near-identical code blocks

## What To Do
1. Scan files for slop patterns using Grep
2. Generate report with file:line references
3. If --fix: Apply automated fixes where safe
4. If --report-only: Just output the report

## Arguments
- `--fix`: Auto-fix safe patterns
- `--report-only`: Report without changes