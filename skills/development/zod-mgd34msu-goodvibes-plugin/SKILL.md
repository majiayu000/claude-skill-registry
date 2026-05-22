---
name: zod
description: Validates data with Zod schemas including type inference, transformations, error handling, and form integration. Use when validating API inputs, form data, environment variables, or any runtime data validation.
---

# Zod

TypeScript-first schema validation with static type inference.

## Quick Start

**Install:**
```bash
npm install zod
```

**Basic usage:**
```typescript
import { z } from 'zod';

// Define schema
const UserSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  age: z.number().min(18),
});

// Infer TypeScript type
type User = z.infer<typeof UserSchema>;

// Validate data
const result = UserSchema.safeParse(data);
if (result.success) {
  console.log(result.data); // Typed as User
} else {
  console.log(result.error.issues);
}
```

## Primitive Types

```typescript
// Strings
const name = z.string();
const email = z.string().email();
const url = z.string().url();
const uuid = z.string().uuid();
const cuid = z.string().cuid();
const regex = z.string().regex(/^[a-z]+$/);
const minMax = z.string().min(1).max(100);
const length = z.string().length(10);
const nonempty = z.string().min(1, 'Required');

// Numbers
const age = z.number();
const positive = z.number().positive();
const negative = z.number().negative();
const integer = z.number().int();
const range = z.number().min(0).max(100);
const finite = z.number().finite();

// BigInt
const bigint = z.bigint();

// Boolean
const active = z.boolean();

// Date
const date = z.date();
const minDate = z.date().min(new Date('2024-01-01'));
const maxDate = z.date().max(new Date());

// Undefined/Null
const undef = z.undefined();
const nul = z.null();
const nullable = z.string().nullable(); // string | null
const optional = z.string().optional(); // string | undefined
const nullish = z.string().nullish();   // string | null | undefined
```

## Objects

### Basic Objects

```typescript
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().optional(),
});

type User = z.infer<typeof UserSchema>;
// { id: string; name: string; email: string; age?: number }
```

### Modifiers

```typescript
const schema = z.object({
  name: z.string(),
  email: z.string(),
  age: z.number(),
});

// All properties optional
const PartialSchema = schema.partial();
// { name?: string; email?: string; age?: number }

// All properties required
const RequiredSchema = schema.required();

// Pick specific properties
const NameEmail = schema.pick({ name: true, email: true });
// { name: string; email: string }

// Omit specific properties
const NoAge = schema.omit({ age: true });
// { name: string; email: string }

// Extend with new properties
const ExtendedSchema = schema.extend({
  role: z.enum(['admin', 'user']),
});

// Merge schemas
const merged = schema.merge(z.object({ role: z.string() }));

// Make specific properties optional
const PartialAge = schema.partial({ age: true });
// { name: string; email: string; age?: number }
```

### Strict and Passthrough

```typescript
// Strict: fail if unknown keys present
const StrictSchema = z.object({ name: z.string() }).strict();

// Passthrough: allow and preserve unknown keys
const PassthroughSchema = z.object({ name: z.string() }).passthrough();

// Strip: remove unknown keys (default)
const StripSchema = z.object({ name: z.string() }).strip();
```

## Arrays and Tuples

```typescript
// Arrays
const strings = z.array(z.string());
const numbers = z.number().array(); // Alternative syntax
const nonEmpty = z.array(z.string()).nonempty();
const lengthRange = z.array(z.string()).min(1).max(10);
const exactLength = z.array(z.string()).length(5);

// Tuples (fixed length, specific types)
const tuple = z.tuple([z.string(), z.number(), z.boolean()]);
// [string, number, boolean]

// Tuple with rest
const tupleWithRest = z.tuple([z.string()]).rest(z.number());
// [string, ...number[]]
```

## Unions and Enums

### Unions

```typescript
// Union types
const StringOrNumber = z.union([z.string(), z.number()]);
// string | number

// Shorthand
const StringOrNumber2 = z.string().or(z.number());

// Discriminated unions (better performance, error messages)
const Result = z.discriminatedUnion('status', [
  z.object({ status: z.literal('success'), data: z.string() }),
  z.object({ status: z.literal('error'), error: z.string() }),
]);
```

### Enums

```typescript
// Zod enum
const RoleSchema = z.enum(['admin', 'user', 'guest']);
type Role = z.infer<typeof RoleSchema>; // 'admin' | 'user' | 'guest'

// Get enum values
RoleSchema.options; // ['admin', 'user', 'guest']

// Native enum
enum Status {
  Active = 'active',
  Inactive = 'inactive',
}
const StatusSchema = z.nativeEnum(Status);
```

### Literals

```typescript
const admin = z.literal('admin');
const fortyTwo = z.literal(42);
const trueLiteral = z.literal(true);
```

## Transformations

### Transform

```typescript
// Transform string to number
const StringToNumber = z.string().transform((val) => parseInt(val, 10));

// Parse and transform
const DateString = z.string().transform((val) => new Date(val));

// With validation after transform
const PositiveNumber = z.string()
  .transform((val) => parseInt(val, 10))
  .pipe(z.number().positive());
```

### Coercion

```typescript
// Automatic coercion
const coercedString = z.coerce.string();   // Any -> string
const coercedNumber = z.coerce.number();   // Any -> number
const coercedBoolean = z.coerce.boolean(); // Any -> boolean
const coercedDate = z.coerce.date();       // Any -> Date

// Common use: form data
const FormSchema = z.object({
  age: z.coerce.number().min(0).max(120),
  active: z.coerce.boolean(),
  date: z.coerce.date(),
});
```

### Preprocess

```typescript
// Run function before validation
const TrimmedString = z.preprocess(
  (val) => (typeof val === 'string' ? val.trim() : val),
  z.string()
);

// Handle null/undefined
const NullableToDefault = z.preprocess(
  (val) => val ?? 'default',
  z.string()
);
```

### Default Values

```typescript
const WithDefault = z.string().default('default value');
const WithDefaultFn = z.string().default(() => generateId());

// Catch: use default on parse failure
const SafeNumber = z.number().catch(0);
const SafeString = z.string().catch('');
```

## Refinements

### Custom Validation

```typescript
// Simple refinement
const PasswordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .refine((val) => /[A-Z]/.test(val), {
    message: 'Password must contain uppercase letter',
  })
  .refine((val) => /[0-9]/.test(val), {
    message: 'Password must contain number',
  });

// Superrefine (multiple issues)
const PasswordSchema2 = z.string().superRefine((val, ctx) => {
  if (val.length < 8) {
    ctx.addIssue({
      code: z.ZodIssueCode.too_small,
      minimum: 8,
      type: 'string',
      inclusive: true,
      message: 'Password must be at least 8 characters',
    });
  }

  if (!/[A-Z]/.test(val)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Password must contain uppercase letter',
    });
  }
});
```

### Cross-Field Validation

```typescript
const SignupSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'], // Error on specific field
});
```

## Error Handling

### Safe Parse

```typescript
const result = UserSchema.safeParse(data);

if (result.success) {
  // result.data is typed
  console.log(result.data);
} else {
  // result.error is ZodError
  console.log(result.error.issues);
}
```

### Parse (throws)

```typescript
try {
  const user = UserSchema.parse(data);
  // user is typed
} catch (error) {
  if (error instanceof z.ZodError) {
    console.log(error.issues);
  }
}
```

### Format Errors

```typescript
const result = UserSchema.safeParse(data);

if (!result.success) {
  // Flat format
  const flat = result.error.flatten();
  // { formErrors: string[], fieldErrors: { [key]: string[] } }

  // Formatted
  const formatted = result.error.format();
  // { _errors: string[], field: { _errors: string[] } }

  // Custom format
  const issues = result.error.issues.map((issue) => ({
    path: issue.path.join('.'),
    message: issue.message,
  }));
}
```

### Custom Error Messages

```typescript
const UserSchema = z.object({
  name: z.string({
    required_error: 'Name is required',
    invalid_type_error: 'Name must be a string',
  }).min(1, 'Name cannot be empty'),

  email: z.string()
    .email({ message: 'Invalid email format' }),

  age: z.number()
    .min(18, { message: 'Must be 18 or older' })
    .max(120, { message: 'Invalid age' }),
});
```

## Common Patterns

### API Request Validation

```typescript
const CreatePostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(1),
  tags: z.array(z.string()).default([]),
  published: z.boolean().default(false),
});

// In API handler
export async function POST(request: Request) {
  const body = await request.json();
  const result = CreatePostSchema.safeParse(body);

  if (!result.success) {
    return Response.json(
      { error: result.error.flatten().fieldErrors },
      { status: 400 }
    );
  }

  const post = await createPost(result.data);
  return Response.json(post);
}
```

### Environment Variables

```typescript
const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
});

export const env = EnvSchema.parse(process.env);
```

### Form Data

```typescript
const ContactFormSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email'),
  message: z.string().min(10, 'Message too short').max(1000),
  subscribe: z.coerce.boolean().default(false),
});

// Parse FormData
function parseFormData(formData: FormData) {
  return ContactFormSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
    subscribe: formData.get('subscribe'),
  });
}
```

### React Hook Form Integration

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const FormSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type FormData = z.infer<typeof FormSchema>;

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(FormSchema),
  });

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Login</button>
    </form>
  );
}
```

### Server Actions (Next.js)

```typescript
'use server';

import { z } from 'zod';

const CreatePostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(1),
});

export async function createPost(formData: FormData) {
  const result = CreatePostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!result.success) {
    return { error: result.error.flatten().fieldErrors };
  }

  const post = await db.posts.create({ data: result.data });
  return { data: post };
}
```

## Type Inference

```typescript
const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

// Infer type from schema
type User = z.infer<typeof UserSchema>;

// Input type (before transforms)
type UserInput = z.input<typeof UserSchema>;

// Output type (after transforms)
type UserOutput = z.output<typeof UserSchema>;
```

## Best Practices

1. **Define schemas once** - Reuse across validation points
2. **Use safeParse** - Handle errors gracefully
3. **Infer types** - Don't duplicate type definitions
4. **Use coercion for forms** - Handle string inputs
5. **Custom error messages** - User-friendly validation

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using parse without try/catch | Use safeParse instead |
| Not handling errors | Check result.success |
| Duplicating types | Use z.infer<typeof Schema> |
| Ignoring transforms | Remember input vs output types |
| Over-complex schemas | Break into smaller schemas |

## Reference Files

- [references/advanced.md](references/advanced.md) - Advanced patterns
- [references/integration.md](references/integration.md) - Framework integrations
