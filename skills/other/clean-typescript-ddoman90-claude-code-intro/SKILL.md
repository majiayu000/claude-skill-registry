---
name: clean-typescript
description: Write clean, practical TypeScript focused on correctness over ceremony
---

# Clean TypeScript Style Guide

Use TypeScript as a correctness and clarity tool, not as ceremony. Prioritize readable types that genuinely reduce bugs.

## Type Declaration

- **PREFER** `type` aliases for most situations
- **USE** `interface` for public, extensible object shapes
- Keep types small and composable

## Function Design

- **PREFER** explicit return types for public functions
- Use function overloads sparingly, only when they meaningfully enhance the API

## Nullability

- Handle `null` and `undefined` explicitly through control flow and guards
- **AVOID** non-null assertions (`!`) as regular practice

## Avoid Anti-patterns

- **AVOID** `enum` - use union types or `as const` objects instead
- **AVOID** `any` - use `unknown` as the safer alternative

## Error Handling

- Type errors explicitly
- Consider result objects or typed errors over broad exception throwing

## Philosophy

If a type is hard to understand, it's probably wrong. Prioritize maintainability and clear intent over theoretical type system completeness.
