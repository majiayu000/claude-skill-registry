---
name: rule-typescript
description: 'Rule mapping for typescript'
---

# Rule typescript

Apply this rule whenever work touches:
- `*.ts`
- `*.tsx`

This project uses TypeScript in strict mode with additional safety flags. Every file must compile cleanly under these settings.

### Strict compiler options

The tsconfig enables `strict: true` plus:

- **noUncheckedIndexedAccess** - array/object index access returns `T | undefined`. Always check the result before using it.
- **exactOptionalPropertyTypes** - optional properties do not accept `undefined` as an explicit value unless the type also includes `| undefined`.
- **noImplicitReturns** - every code path in a function must return a value if any path does.

### Imports and path aliases

Cross-library imports must use the path aliases defined in `tsconfig.paths.json`. For example:

```ts
// Correct
import { stubDocument } from '@carrot-fndn/shared/testing';

// Wrong - relative path crossing library boundary
import { stubDocument } from '../../../shared/testing/src';
```

Within the same library, relative imports are acceptable.

### Exports

All exported symbols must have explicit return types. This improves API readability and catches accidental return-type changes.

```ts
// Correct
export function computeScore(input: RuleInput): RuleOutput { ... }

// Wrong - implicit return type
export function computeScore(input: RuleInput) { ... }
```

Use named exports only. Default exports make refactoring harder and are inconsistent with the rest of the codebase.

### Type utilities

Prefer `type-fest` utilities over custom mapped types:

- `SetRequired<T, K>` instead of manual `Omit & Required` combinations
- `ReadonlyDeep<T>` for deeply immutable structures
- `JsonValue` / `JsonObject` for JSON-safe typing

### Zod integration

Define Zod schemas as the source of truth for shapes that require runtime validation. Derive the static TypeScript type from the schema:

```ts
const UserSchema = z.object({
  name: z.string(),
  age: z.number().int().positive(),
});

type User = z.infer<typeof UserSchema>;
```

Never maintain a hand-written interface alongside a Zod schema for the same shape.
