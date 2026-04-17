---
name: typescript-patterns
description: TypeScript best practices and patterns. Use when writing TypeScript, fixing type errors, or working with generics.
---

# TypeScript Patterns

## Type vs Interface

| Use Case | Prefer |
|----------|--------|
| Object shape | interface |
| Union types | type |
| Extending shapes | interface |
| Intersection | type |
| Tuple/primitives | type |

## Key Patterns

**Discriminated Unions** — model state with tagged types:
```typescript
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };
```

**Type Guards** — narrow at runtime:
```typescript
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}
```

**Generic Constraints:**
```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] { return obj[key]; }
```

## Utility Types

| Type | Purpose |
|------|---------|
| Partial\<T\> | All optional |
| Required\<T\> | All required |
| Pick\<T,K\> | Select properties |
| Omit\<T,K\> | Remove properties |
| Record\<K,V\> | Key-value map |
| ReturnType\<T\> | Function return type |

## Avoid

- `any` — use `unknown` and narrow
- Type assertions (`as`) — use type guards
- `!` operator — handle null properly
- Missing return types on complex functions
