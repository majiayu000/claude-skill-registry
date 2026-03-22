---
name: typescript
description: Esposter TypeScript conventions — banned patterns (any, Omit, !, forEach, parameter properties), error handling with InvalidOperationError, control flow guard clauses, and enum ref defaults. Apply when writing any TypeScript in this project.
---

# TypeScript Conventions

## Core Rules

- TypeScript compiler: `strict` mode enabled. ESLint: `tseslint.configs.strictTypeChecked`. `any` is **BANNED**.
- **Always use strict equality** — `===` and `!==` only. Never `==` or `!=`, including null checks: use `=== null || === undefined` (or optional chaining) instead of `== null`.
- `Omit` is **BANNED** — use `Except` from `type-fest` (`import type { Except } from "type-fest"`). Note: `Except` is not re-exported from `@esposter/shared` — always import directly from `type-fest`.
- **No parameter properties** — never use `constructor(private readonly foo: T)`. Always declare class properties explicitly and assign in the constructor body: `private readonly foo: T; constructor(foo: T) { super(); this.foo = foo; }`.
- Non-null assertions (`!`) are **BANNED** — use optional chaining or guard clauses.
- `.forEach()` is **BANNED** — use `for...of`.
- `type` aliases for object shapes are **BANNED** — always use `interface` for object type declarations.
- `Array#sort()` is **BANNED** — use `Array#toSorted()` instead. This returns a new array without mutating the original, so replace `[...arr].sort(fn)` with `arr.toSorted(fn)`.
- Always use named imports from libraries — only when not already auto-imported by Nuxt or Nuxt modules (e.g. `ref`, `computed`, `watch` from Vue; `storeToRefs` from Pinia; VueUse composables are all auto-imported and must not be manually imported).
- Explicitly type variables with proper types.
- **No `current*` variable caching of `.value`** — don't assign `const currentX = x.value` just to use it once. If TypeScript narrowing is needed after a guard, assign with a descriptive name (`const selectedFile = file.value`). Prefer plain `const` over `computed()` when the source value is already non-reactive (e.g. a `readonly` prop field).
- **Cloning objects** — use `structuredClone(obj)` for deep clones; use `Object.assign(structuredClone(obj), { ...updates })` to clone and override fields. Never use `{ ...spread }` to clone a class instance — spread creates a plain object losing the prototype. **Exception**: `structuredClone(new ClassName(...))` is intentional when a plain object is explicitly required (e.g. Vjsf does not accept class instances — must use `structuredClone` to strip the prototype). Always add a comment explaining why.
- **Boolean casting** — never use `!!` to cast to boolean. Always use `Boolean(value)`.

## Promise Style

- **Always use `async`/`await`** — never use `.then()` or `.catch()` promise chains. Use `try`/`catch` blocks for error handling.
- When fire-and-forgetting an async operation, extract to a named `async` function and call it without `await`.

## Error Handling

- **Never use `new Error(...)`** — always throw `new InvalidOperationError(operation, name, message)` from `@esposter/shared`.
- Pick the appropriate `Operation` enum value (`Operation.Read`, `Operation.Create`, `Operation.Update`, `Operation.Delete`, etc.).
- Use the resource name (e.g. `file.name`, entity ID) as the `name` argument — fall back to the calling function's name (e.g. `deserializeJson.name`) if no better resource name is available.
- For user-supplied JSON (file uploads, external input): use Zod `safeParse` and throw `InvalidOperationError` on failure — never use bare `JSON.parse` with a type cast.
- For validated endpoint data: `jsonDateParse` from `@esposter/shared` is acceptable.

## Control Flow

- **Guard clauses first**: always use `if (!condition) return` to exit early instead of wrapping the main body in an `if` block. Reduce nesting aggressively — if the body of an `if` is the rest of the function, invert the condition and return early instead.
- **Always use `if/else if/else` from the very first branch** when a function has multiple conditional returns — no standalone `if` followed by `else if`.

## Return Type Annotations

- **Prefer inferred return types** — don't annotate a function's return type when TypeScript can infer it correctly. Only add explicit return type annotations when: (a) the inferred type is too broad and you want to enforce a narrower contract (e.g. `ComputedRef<ValidationRule>` instead of `ComputedRef<(value: string) => string | true>`), or (b) the function is part of a public API boundary. Never add redundant annotations just for documentation.

## Helper Functions

- **Don't extract helpers that add no value** — if a helper function just wraps an inline object literal or a single expression without reuse or meaningful abstraction, return/use the value directly. Three lines of inline code is better than a named wrapper used once.
- **Function naming prefixes** — use `get*` for functions that derive or compute a display value (e.g. `getVisibilityTooltip`, `getRowTitle`). Use CRUD prefixes (`create*`, `update*`, `delete*`) for heavier operations that interact with data or stores.

## Enum Refs

- **Never use `ref<EnumType | null>(null)`** — always default to a sensible first enum value: `ref(DataSourceType.Csv)`, `ref(ColumnType.String)`, etc.
- **Never write `ref<EnumType>(EnumValue)`** — TypeScript infers the enum type from the value. Write `ref(ColumnType.String)`, not `ref<ColumnType>(ColumnType.String)`.

## Stable Identifiers for Selections

- **Track selections by stable ID, not by name or index** — column names change, indices shift on delete/reorder. Always use `entity.id` (UUID) as the key when storing which items are selected/active. A stale ID in a selection is harmless; a stale name or index is a bug.

## Generic Definition Arrays — `as const` Without `satisfies`

When a definition array has entries typed as `Definition<T>` where the generic `T` controls a **contravariant** position (e.g. a callback parameter like `format: (value: ColumnStats[T]) => string`), using `satisfies readonly Definition[]` widens each entry to `Definition<KeyUnion>`, which fails due to contravariance.

**Fix**: drop `satisfies` and use `as const` alone. Each entry retains its specific `Definition<"specificKey">` type, inferred by the `define*` helper.

```ts
// ColumnStatDefinition<T> has format: (value: ColumnStats[T]) => string  — contravariant in T
// satisfies readonly ColumnStatDefinition[] FAILS (widens T → ColumnStatKey → function param too broad)
// as const alone PASSES — preserves ColumnStatDefinition<"nullCount">, etc.
export const ColumnStatDefinitions = [
  defineColumnStat({ key: "nullCount", format: (value) => String(value), ... }),
  ...
] as const;  // NOT "satisfies readonly ColumnStatDefinition[]"
```

At call sites where the entry is destructured from the array (losing key↔format correlation), cast the value with `as never`:

```ts
// key and format are destructured — TypeScript loses their correlation
format(item[key] as never); // safe: key and format always come from the same definition entry
```

## Filter-Based Type Narrowing

- **No redundant type guards after a filtering condition** — if a `.filter()` predicate already narrows the type (e.g. `filter((v) => typeof v === "number")`), the resulting array is already typed `number[]`. Do NOT add a separate type guard (`: v is number`) or cast inside the callback — the filter itself is sufficient.
  ```ts
  // WRONG — redundant guard
  values.filter((v): v is number => typeof v === "number");
  // CORRECT — filter condition narrows the type
  values.filter((v) => typeof v === "number");
  ```
  Exception: when the predicate is a function reference (e.g. `filter(Boolean)`) that TypeScript cannot narrow automatically, a type predicate is still needed.
