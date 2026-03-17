---
name: ast_injection
description: Use AST-aware edits to reduce syntax errors and maintain structure.
metadata:
  short-description: AST-aware edits
---

## Purpose
Apply structural code changes safely.

## Steps
1. Prefer AST insertion over raw text replacement.
2. Validate with tests or static checks.
3. Record assumptions when AST tooling is unavailable.
