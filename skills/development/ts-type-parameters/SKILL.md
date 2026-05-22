---
name: type-parameters
description: Type parameter naming conventions for personal TypeScript projects. Triggers on generic type/function creation, type-level code, or when asking about TypeScript generics.
---

# Type Parameter Naming

## Convention

* __Type aliases and interfaces__: Use `$` prefix
  * `type Transform<$Input> = $Input extends string ? number : boolean`
  * `interface Container<$T> { value: $T }`

* __Functions and methods__: Use `$` prefix matching the value parameter name
  * `function process<$value>(value: $value): $value`
  * `function map<$item, $result>(item: $item, fn: ($item) => $result): $result`

* __Type guard exception__: Add `_` suffix to avoid conflict with narrowed type
  * `function isString<$value_>(value: unknown): value is $value_`

* __Generic returns exception__: When type param is NOT mapped to value parameter
  * `function create<$T>(): $T`

* __Utility internals__: Parameters with `___` prefix are implementation details
  * `type Utility<$T, ___Internal = SomeDefault<$T>> = ...`

* __Mapped types__: Use specific single-letter iterators
  * Objects: `k` (key) - `{ [k in keyof $T]: $T[k] }`
  * Tuples/arrays: `i` (index) - `{ [i in keyof $T]: Transform<$T[i]> }`

* __Infer clauses__: Use `__lowercase__` pattern
  * `$T extends Array<infer __element__> ? __element__ : never`

## Type Parameter Defaults

Default type parameters to their widest possible variant:

```typescript
// GOOD - Defaults to widest
type ParserContext<
  $Schema = Schema | undefined,
  $SDDM = any,
  $TypeHooks = never
> = ...

// Usage with clean constraints
function parse<$Context extends ParserContext>(...) // Clean!

// BAD - Cluttered constraint
function parse<$Context extends ParserContext<any, any, any>>(...) // Ugly!
```
