---
name: kiss-dry-yagni
description: Principes KISS, DRY, YAGNI. Use when reviewing code quality or refactoring.
triggers:
  files: ["*.cs"]
  keywords: ["simple", "simplify", "duplicate", "duplication", "refactor", "KISS", "DRY", "YAGNI"]
auto_suggest: true
---

# Principes KISS, DRY, YAGNI

This skill provides simplicity and code quality guidelines.

See @REFERENCE.md for detailed documentation.

## Quick Reference

- **KISS**: Methods < 20 lines, complexity < 10, indent < 3 levels
- **DRY**: Abstract after 3 occurrences, single source of truth
- **YAGNI**: Only build what's explicitly required NOW
- **Early returns**: Prefer guard clauses over nested else
- **Composition**: Prefer over inheritance
