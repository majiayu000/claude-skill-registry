---
name: type-assertions
description: Type assertion patterns using @kitz/assert. Triggers on type-level tests, .test-d.ts files, or when asserting TypeScript types.
---

# Type Assertions

## Import

```typescript
import { Assert } from '@kitz/assert'
```

## Builder Pattern

Assertions use a fluent builder: `Assert.<relator>.<matcher>(expected).<setting>().on(actual)`

### Relators (Required First)

| Relator  | Meaning                     |
| -------- | --------------------------- |
| `.exact` | Types must be identical     |
| `.equiv` | Bidirectional assignability |
| `.sub`   | Actual extends expected     |

### Unary Matchers (No Expected Type)

```typescript
Assert.exact.any.on(value) // value is any
Assert.exact.unknown.on(value) // value is unknown
Assert.exact.never.on(value) // value is never
Assert.exact.empty.on(value) // value is {}
```

### Binary Matchers

```typescript
// Value-level (preferred)
Assert.exact.of(expected).on(actual)

// Type-level only
Assert.exact.ofAs<Expected>().onAs<Actual>()

// Shorthand matchers
Assert.exact.string.on(value)
Assert.exact.number.on(value)
Assert.exact.boolean.on(value)
Assert.exact.bigint.on(value)
Assert.exact.symbol.on(value)
Assert.exact.null.on(value)
Assert.exact.undefined.on(value)
Assert.exact.void.on(value)
Assert.exact.object.on(value)
Assert.exact.function.on(value)
```

### Settings (Optional)

```typescript
// Negate assertion
Assert.exact.of(string).not.on(value) // value is NOT string

// Control type inference
Assert.exact.of(expected).inferNarrow().on(actual) // narrow inference
Assert.exact.of(expected).inferWide().on(actual) // wide inference
Assert.exact.of(expected).inferAuto().on(actual) // default
```

### Extractors

```typescript
// Extract return type
Assert.exact.string.returned.on(fn) // ReturnType<fn> is string

// Extract awaited type
Assert.exact.string.awaited.on(promise) // Awaited<promise> is string

// Extract parameters
Assert.exact.of([string, number]).parameters.on(fn)

// Extract array element
Assert.exact.string.array.on(arr) // arr is string[]
```

## Preferred Pattern

__ALWAYS prefer value-level API__ - it reports ALL failures simultaneously:

```typescript
// In .test.ts files
test('types', () => {
  const value = getValue()
  Assert.exact.string.on(value)
  Assert.exact.of({ a: 1 }).on(obj)
})

// In .test-d.ts files (pure type-level)
Assert.exact.ofAs<string>().onAs<string>()
Assert.exact.ofAs<number>().onAs<number>()

// @ts-expect-error - type mismatch
Assert.exact.ofAs<string>().onAs<number>()
```

## Avoid

```typescript
// DON'T use type-level only assertions in test blocks
test('bad', () => {
  type _ = Assert.exact.of<string, number> // Short-circuits on first error
})
```
