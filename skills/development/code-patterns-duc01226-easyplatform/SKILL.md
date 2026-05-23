---
name: code-patterns
description: Code implementation patterns and best practices learned from real mistakes. Covers file I/O safety (locking, atomic writes), data persistence, and validation. Use for file-based state, shared resources, concurrent access. NOT for auto-learning patterns (see learned-patterns skill).
version: 1.0.0
languages: all
---

# Code Patterns

Best practices distilled from implementation lessons. These patterns prevent common bugs in file I/O, data persistence, and validation.

## Core Principle

**LEARN FROM MISTAKES - DON'T REPEAT THEM**

Each pattern here was extracted from a real bug or issue. Apply these patterns proactively to prevent the same mistakes.

## When to Use

**Always use for:** File-based state, shared resources, data persistence, validation layers, concurrent access

**Especially when:** Multiple processes/hooks access same file, persisting JSON data, creating factory functions, implementing save/load logic

## The Patterns

### 1. File Locking (`references/file-io.md`)

Advisory file locking for shared state access.

**Problem:** Multiple processes writing to same file causes data corruption or race conditions.

**Solution:** Use `.lock` file pattern with timeout and stale lock detection.

**⚠️ MUST READ when:** Implementing file-based state accessed by multiple hooks/processes

### 2. Atomic Writes (`references/data-persistence.md`)

Safe file persistence that survives crashes.

**Problem:** `writeFileSync()` mid-write crash corrupts file.

**Solution:** Write to `.tmp`, rename to final path (atomic on POSIX), handle Windows with backup pattern.

**⚠️ MUST READ when:** Persisting any JSON/data file that must survive unexpected termination

### 3. Schema Validation (`references/data-validation.md`)

Validate before every persist operation.

**Problem:** Factory functions create invalid data that persists and causes downstream issues.

**Solution:** Validate at creation AND before every write. Never trust "it was validated earlier."

**⚠️ MUST READ when:** Creating factory functions, implementing create/update operations, building data pipelines

## Quick Reference

```
Shared file access → file-io.md (add locking)
JSON persistence → data-persistence.md (atomic writes)
Factory function → data-validation.md (validate output)
```

## Prevention Checklist

Before implementing file I/O:

- [ ] Will multiple processes access this file?
- [ ] What happens if write crashes mid-operation?
- [ ] Is data validated before every write?
- [ ] Are stale locks handled (dead process detection)?

## Origin

These patterns were extracted from ACE (Agentic Context Engineering) implementation review:

- Race condition in concurrent delta writes → file-io.md
- File corruption risk on crash → data-persistence.md
- Invalid deltas persisting → data-validation.md

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
