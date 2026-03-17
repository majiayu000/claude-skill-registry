---
name: typescript-refactoring-patterns
description: Expert TypeScript refactoring patterns for cleaner, type-safe code
license: MIT
compatibility: typescript 5.0+
allowed-tools: read_file write_file apply_patch search_with_context
---

# TypeScript Refactoring Patterns

## Core Principles

1. **Type Narrowing Over Type Assertions** - Use type guards and discriminated unions instead of `as` casts
2. **Const Assertions for Literals** - Use `as const` for immutable literal types
3. **Generic Constraints** - Prefer `extends` constraints over `any`
4. **Branded Types** - Use branded types for domain-specific validation

## Refactoring Patterns

### Extract Discriminated Union
When you see multiple boolean flags, refactor to discriminated union:

```typescript
// Before
interface User {
  isAdmin: boolean;
  isGuest: boolean;
  permissions?: string[];
}

// After
type User =
  | { role: 'admin'; permissions: string[] }
  | { role: 'guest' }
  | { role: 'member'; permissions: string[] };
```

### Replace Conditional with Polymorphism
When you see switch statements on type, use the strategy pattern:

```typescript
// Before
function process(item: Item) {
  switch (item.type) {
    case 'a': return processA(item);
    case 'b': return processB(item);
  }
}

// After
const processors: Record<ItemType, (item: Item) => Result> = {
  a: processA,
  b: processB,
};
const process = (item: Item) => processors[item.type](item);
```

### Extract Type Guard
When narrowing types, create reusable type guards:

```typescript
function isNonNullable<T>(value: T): value is NonNullable<T> {
  return value !== null && value !== undefined;
}

// Usage
const items = array.filter(isNonNullable);
```

### Use Branded Types for Validation
Prevent primitive obsession with branded types:

```typescript
type UserId = string & { readonly brand: unique symbol };
type Email = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId {
  if (!isValidUuid(id)) throw new Error('Invalid user ID');
  return id as UserId;
}
```

## Code Smell Detectors

Watch for these patterns and refactor:
- `any` types (replace with `unknown` + type guards)
- Non-null assertions `!` (add proper checks)
- Type assertions `as` (use type guards)
- Optional chaining abuse `?.?.?.` (restructure data)
- Index signatures without validation

## Quick Wins

1. Enable `strict: true` in tsconfig
2. Use `satisfies` for type checking without widening
3. Prefer `readonly` arrays and objects
4. Use `unknown` for external data, validate at boundaries
