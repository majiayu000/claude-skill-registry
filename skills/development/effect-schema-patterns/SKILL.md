---
name: schema-patterns
description: Effect Schema conventions and patterns. Triggers on Schema class creation, tagged unions, enums, type guards, or test fixtures using Effect Schema.
---

# Effect Schema Patterns

## Class Instantiation

__ALWAYS use `Schema.make()` for creating instances:__

```typescript
// ✅ GOOD - Use Schema.make()
const user = Schema.make(User)({ name: 'Alice', age: 30 })

// ❌ BAD - Manual construction
const user = { _tag: 'User', name: 'Alice', age: 30 }
```

## Type Guards

__ALWAYS use `Schema.is()` or static `.is` method:__

```typescript
// ✅ GOOD
if (Standard.is(value)) { ... }
if (Schema.is(Standard)(value)) { ... }

// ❌ BAD - manual _tag check
if (value._tag === 'Standard') { ... }
```

## Enums

__ALWAYS inline enum values directly in `Schema.Enums()`:__

```typescript
// ✅ GOOD - inline values, use .enums for runtime access
export const Status = Schema.Enums({
  active: 'active',
  inactive: 'inactive',
})
export type Status = typeof Status.Type
// Runtime: Status.enums.active

// ❌ BAD - separate const object
export const StatusValues = {
  active: 'active',
  inactive: 'inactive',
} as const
export const Status = Schema.Enums(StatusValues)
```

## Key Points

* Use `Schema.make()` for type-safe instantiation
* Use `Schema.is()` for type predicates, never manual `_tag` checks
* Inline enum values directly in `Schema.Enums()`
* Access runtime enum values via `.enums` property
