---
name: effect-ts-testing
description: Testing guidelines and patterns for Effect-based code.
---

# Effect-TS Testing Skill

Use this skill when writing or reviewing tests for Effect-based code.

## Effect testing rules (for `*.spec.*` files)

When testing a method that returns an `Effect` type, use the `@effect/vitest`
package.

- Use `import { it } from '@effect/vitest'` as opposed to importing `it` from
  regular vitest.
- Usage:
  ```typescript
  it.effect('test name', () => {
     return Effect.gen(...)
  })
  ```
- Use `it.layer()` to provide test dependencies when your Effect requires
  specific services:
  ```typescript
  it.layer(Layer.fresh(IncrementalIdGenerator))((it) => {
    it.effect('test name', () => {
      return Effect.gen(...)
    })
  })
  ```

## Testing for type-safety

Use `tsafe` package for compile-time type assertions to validate type safety in
tests.

- Import: `import { assert } from 'tsafe'` and `import type { Equals } from 'tsafe'`
- Usage: `assert<Equals<ActualType, ExpectedType>>()` - validates exact type
  equality at compile time

## Test time helpers

Never use `new Date()` in tests. Always use `yield* DateTime.now` and convert to
`Date` if needed.

```typescript
import { DateTime, Effect } from 'effect';

const nowDateTime = yield* DateTime.now;
const now = DateTime.toDateUtc(nowDateTime);
```

## Schema decoding with decodeUnknown

When decoding unknown values using Effect schemas, always use the
`decodeUnknown` function exported from `zerospin` instead of
`Schema.decodeUnknown` directly.

- Import: `import { decodeUnknown } from 'zerospin'`
- Always specify `onExcessProperty`: `'error'`, `'ignore'`, or `'preserve'`
  based on your needs
- Map errors to `ZerospinError` with code `'failed-to-decode-unknown'`

**In Effect.gen contexts:**
```typescript
import { decodeUnknown } from 'zerospin';
import { ZerospinError } from '@zerospin/error';
import { Effect } from 'effect';

const decoded = yield* decodeUnknown({
  onExcessProperty: 'error', // or 'ignore' or 'preserve'
  schema: MySchema,
  value: unknownValue,
}).pipe(
  Effect.mapError((error) => {
    return new ZerospinError({
      code: 'failed-to-decode-unknown',
      message: error.message,
      cause: error,
    });
  })
);
```

**In async/await contexts:**
```typescript
import { decodeUnknown } from 'zerospin';
import { ZerospinError } from '@zerospin/error';
import { Effect } from 'effect';

const decoded = await Effect.runPromise(
  decodeUnknown({
    onExcessProperty: 'error',
    schema: MySchema,
    value: unknownValue,
  }).pipe(
    Effect.mapError((error) => {
      return new ZerospinError({
        code: 'failed-to-decode-unknown',
        message: error.message,
        cause: error,
      });
    })
  )
);
```
