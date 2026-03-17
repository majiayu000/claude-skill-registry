---
name: clean-typescript
description: Write clean, efficient TypeScript code that follows common best practices
---

# Clean TypeScript

We use **TypeScript as a correctness and clarity tool**, not as ceremony.
Types should reduce bugs and cognitive load.

## Type Philosophy

- **PREFER** explicit, readable types over clever or overly generic ones
- **AVOID** `any` and unsafe type assertions
- Use `unknown` instead of `any` when necessary
- Let TypeScript infer types when inference is clear and stable

## Types & Interfaces

- **PREFER** `type` aliases for most use cases
- Use `interface` primarily for public, extendable object shapes
- Keep types small, composable, and well-named

## Functions & APIs

- **PREFER** explicit return types for public functions
- Avoid function overloads unless they meaningfully improve the API
- Keep function signatures simple and predictable

## Nullability & Safety

- Handle `null` and `undefined` explicitly
- **DO NOT** rely on non-null assertions (`!`) except as a last resort
- Prefer narrowing via control flow and guards

## Enums & Constants

- **AVOID** `enum`
- **PREFER** union types or `as const` objects
- Keep runtime output predictable and minimal

## Error Handling

- Type errors and error states explicitly
- Prefer result objects or typed errors over throwing where appropriate
- Do not hide failure modes behind broad types

## General Principles

- Types should explain intent
- If a type is hard to understand, it’s probably wrong
- Favor maintainability over theoretical completeness
