---
name: valibot
description: Validates data with Valibot's modular, tree-shakable schema library for minimal bundle size. Use when bundle size matters, building form validation, or needing lightweight TypeScript validation.
---

# Valibot

Modular schema validation library with best-in-class bundle size (~1KB for basic forms).

## Quick Start

```bash
npm install valibot
```

```typescript
import * as v from 'valibot';

const schema = v.object({
  name: v.pipe(v.string(), v.minLength(2)),
  email: v.pipe(v.string(), v.email()),
  age: v.pipe(v.number(), v.minValue(0)),
});

// Validate
const result = v.safeParse(schema, data);

if (result.success) {
  console.log(result.output);
} else {
  console.log(result.issues);
}
```

## Schema Types

### Primitives

```typescript
import * as v from 'valibot';

// String
v.string()
v.pipe(v.string(), v.minLength(1), v.maxLength(100))

// Number
v.number()
v.pipe(v.number(), v.minValue(0), v.maxValue(100))

// Boolean
v.boolean()

// Null/Undefined
v.null_()
v.undefined_()

// BigInt
v.bigint()

// Symbol
v.symbol()

// Date
v.date()
v.pipe(v.date(), v.minValue(new Date()))
```

### String Validations

```typescript
v.pipe(
  v.string(),
  v.minLength(1, 'Required'),
  v.maxLength(100, 'Too long'),
  v.email('Invalid email'),
  v.url('Invalid URL'),
  v.uuid('Invalid UUID'),
  v.regex(/^[a-z]+$/, 'Only lowercase'),
  v.startsWith('https://'),
  v.endsWith('.com'),
  v.includes('@'),
  v.trim(),
  v.toLowerCase(),
  v.toUpperCase(),
)
```

### Number Validations

```typescript
v.pipe(
  v.number(),
  v.minValue(0, 'Must be positive'),
  v.maxValue(100, 'Max 100'),
  v.integer('Must be integer'),
  v.multipleOf(5, 'Must be multiple of 5'),
  v.finite('Must be finite'),
  v.safeInteger('Must be safe integer'),
)
```

### Object

```typescript
const userSchema = v.object({
  name: v.string(),
  email: v.pipe(v.string(), v.email()),
  age: v.optional(v.number()),
});

// Strict (no extra keys)
const strictSchema = v.strictObject({
  id: v.number(),
  name: v.string(),
});

// Loose (allow extra keys)
const looseSchema = v.looseObject({
  id: v.number(),
});
```

### Array

```typescript
v.array(v.string())
v.pipe(
  v.array(v.string()),
  v.minLength(1, 'At least one item'),
  v.maxLength(10, 'Max 10 items'),
)

// Tuple
v.tuple([v.string(), v.number()])
```

### Union & Intersection

```typescript
// Union (OR)
const statusSchema = v.union([
  v.literal('active'),
  v.literal('inactive'),
  v.literal('pending'),
]);

// Variant (discriminated union)
const eventSchema = v.variant('type', [
  v.object({ type: v.literal('click'), x: v.number(), y: v.number() }),
  v.object({ type: v.literal('scroll'), offset: v.number() }),
]);

// Intersection (AND)
const combined = v.intersect([
  v.object({ id: v.number() }),
  v.object({ name: v.string() }),
]);
```

### Optional & Nullable

```typescript
// Optional (undefined allowed)
v.optional(v.string())

// Nullable (null allowed)
v.nullable(v.string())

// Nullish (null or undefined)
v.nullish(v.string())

// With default
v.optional(v.string(), 'default value')
v.nullable(v.number(), 0)
```

## Pipe System

Valibot uses `pipe()` to chain validations and transformations:

```typescript
const schema = v.pipe(
  v.string(),
  v.trim(),              // Transform
  v.minLength(1),        // Validate
  v.toLowerCase(),       // Transform
  v.email(),             // Validate
);

// Order matters!
const result = v.parse(schema, '  John@Example.COM  ');
// Output: 'john@example.com'
```

## Validation

### parse() - Throws on Error

```typescript
try {
  const data = v.parse(schema, input);
} catch (error) {
  if (error instanceof v.ValiError) {
    console.log(error.issues);
  }
}
```

### safeParse() - Returns Result

```typescript
const result = v.safeParse(schema, input);

if (result.success) {
  console.log(result.output);
} else {
  console.log(result.issues);
}
```

### is() - Type Guard

```typescript
if (v.is(schema, input)) {
  // input is typed
}
```

## Type Inference

```typescript
import * as v from 'valibot';

const userSchema = v.object({
  id: v.number(),
  name: v.string(),
  email: v.pipe(v.string(), v.email()),
  roles: v.array(v.string()),
});

// Infer TypeScript type
type User = v.InferOutput<typeof userSchema>;
// { id: number; name: string; email: string; roles: string[] }

// Infer input type (before transforms)
type UserInput = v.InferInput<typeof userSchema>;
```

## Custom Validation

### check() - Custom Predicate

```typescript
const schema = v.pipe(
  v.string(),
  v.check((value) => value.includes('@'), 'Must contain @'),
);
```

### transform() - Custom Transform

```typescript
const schema = v.pipe(
  v.string(),
  v.transform((value) => value.split(',').map((s) => s.trim())),
);
```

### Custom Schema

```typescript
const passwordSchema = v.pipe(
  v.string(),
  v.minLength(8, 'At least 8 characters'),
  v.regex(/[A-Z]/, 'Need uppercase'),
  v.regex(/[a-z]/, 'Need lowercase'),
  v.regex(/[0-9]/, 'Need number'),
);
```

## Common Patterns

### User Registration

```typescript
const registrationSchema = v.object({
  email: v.pipe(
    v.string(),
    v.email('Invalid email'),
  ),
  password: v.pipe(
    v.string(),
    v.minLength(8, 'At least 8 characters'),
    v.regex(/[A-Z]/, 'Need uppercase'),
    v.regex(/[0-9]/, 'Need number'),
  ),
  confirmPassword: v.string(),
  age: v.pipe(
    v.number(),
    v.minValue(18, 'Must be 18+'),
  ),
  terms: v.pipe(
    v.boolean(),
    v.value(true, 'Must accept terms'),
  ),
});

// Add cross-field validation
const fullSchema = v.pipe(
  registrationSchema,
  v.forward(
    v.partialCheck(
      [['password'], ['confirmPassword']],
      (input) => input.password === input.confirmPassword,
      'Passwords must match',
    ),
    ['confirmPassword'],
  ),
);
```

### API Response

```typescript
const apiResponseSchema = v.object({
  success: v.boolean(),
  data: v.optional(v.object({
    users: v.array(v.object({
      id: v.number(),
      name: v.string(),
    })),
  })),
  error: v.optional(v.string()),
});
```

### Environment Variables

```typescript
const envSchema = v.object({
  NODE_ENV: v.picklist(['development', 'production', 'test']),
  PORT: v.pipe(v.string(), v.transform(Number), v.integer()),
  DATABASE_URL: v.pipe(v.string(), v.url()),
  API_KEY: v.pipe(v.string(), v.minLength(32)),
});

const env = v.parse(envSchema, process.env);
```

## React Hook Form Integration

```typescript
import { useForm } from 'react-hook-form';
import { valibotResolver } from '@hookform/resolvers/valibot';
import * as v from 'valibot';

const schema = v.object({
  email: v.pipe(v.string(), v.email()),
  password: v.pipe(v.string(), v.minLength(8)),
});

type FormData = v.InferOutput<typeof schema>;

function Form() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: valibotResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

## Bundle Size Comparison

| Library | Basic Form |
|---------|------------|
| Valibot | ~1.4 KB |
| Zod | ~12 KB |
| Yup | ~15 KB |

Valibot achieves this through modular imports - only used functions are bundled.

See [references/methods.md](references/methods.md) for complete method reference.
