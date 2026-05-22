---
name: type-safety-audit
description: Audits TypeScript code for type safety best practices - no any usage, branded types for IDs, runtime validation, proper type narrowing. Use before committing TypeScript code or during type system reviews.
version: 1.0.0
---

# TypeScript Type Safety Audit Skill

## Purpose

Audit TypeScript code for type safety best practices. This skill ensures the type system is leveraged correctly to catch bugs at compile-time, prevent runtime type errors, and maintain type safety across API boundaries.

## What This Skill Checks

### Critical Violations (Block Commit)

1. **Any Type Usage** - Zero tolerance policy
2. **Missing Branded Types** - IDs must be branded
3. **Missing Runtime Validation** - API boundaries need validation
4. **Type Assertions** - Prefer type guards
5. **Unsafe Null Handling** - Check for null/undefined
6. **Weak Generic Constraints** - Generics need constraints
7. **Non-Strict tsconfig** - Must have strict mode

**For detailed checks with code examples and rationale, see `references/CHECKS-REFERENCE.md`.**

- Hermes Code Reviewer: Type Safety Patterns
