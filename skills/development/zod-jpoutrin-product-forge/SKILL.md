---
name: zod
description: Zod schema validation patterns and type inference. Auto-loads when validating schemas, parsing data, validating forms, checking types at runtime, or using z.object/z.string/z.infer in TypeScript.
user-invocable: false
---

# Zod Schema Validation

TypeScript-first schema declaration and validation library with static type inference.

## Why Zod

- Zero dependencies, 2kb gzipped
- Works in Node.js and browsers
- Immutable API - methods return new instances
- Static type inference - no redundant type declarations
- JSON Schema conversion built-in

## Requirements

- TypeScript v5.5+
- Enable `strict` mode in tsconfig.json

## Core Concepts

### Schema Definition

Always define schemas before validation:

```typescript
import { z } from "zod";

// Object schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().positive(),
  role: z.enum(["admin", "user", "guest"]),
});

// Infer TypeScript type from schema
type User = z.infer<typeof UserSchema>;
```

### Parsing Methods

**`.parse()`** - Throws `ZodError` on failure:

```typescript
try {
  const user = UserSchema.parse(data);
  // user is typed as User
} catch (e) {
  if (e instanceof z.ZodError) {
    console.error(e.issues);
  }
}
```

**`.safeParse()`** - Returns discriminated union (preferred):

```typescript
const result = UserSchema.safeParse(data);

if (result.success) {
  console.log(result.data); // typed User
} else {
  console.error(result.error.issues);
}
```

**Async variants** - Required for async refinements/transforms:

```typescript
await UserSchema.parseAsync(data);
await UserSchema.safeParseAsync(data);
```

## Primitive Types

```typescript
// Basic primitives
z.string()
z.number()
z.bigint()
z.boolean()
z.date()
z.symbol()
z.undefined()
z.null()
z.void()
z.any()
z.unknown()
z.never()

// Coercion - converts input to target type
z.coerce.string()   // String(input)
z.coerce.number()   // Number(input)
z.coerce.boolean()  // Boolean(input)
z.coerce.bigint()   // BigInt(input)
z.coerce.date()     // new Date(input)
```

## String Validations

```typescript
z.string()
  .min(1)              // Minimum length
  .max(255)            // Maximum length
  .length(10)          // Exact length
  .email()             // Email format
  .url()               // URL format
  .uuid()              // UUID format
  .cuid()              // CUID format
  .regex(/pattern/)    // Custom regex
  .startsWith("prefix")
  .endsWith("suffix")
  .includes("substring")
  .trim()              // Transform: trim whitespace
  .toLowerCase()       // Transform: lowercase
  .toUpperCase()       // Transform: uppercase
```

## Number Validations

```typescript
z.number()
  .int()               // Integer only
  .positive()          // > 0
  .nonnegative()       // >= 0
  .negative()          // < 0
  .nonpositive()       // <= 0
  .gt(5)               // > 5
  .gte(5)              // >= 5 (alias: .min())
  .lt(10)              // < 10
  .lte(10)             // <= 10 (alias: .max())
  .multipleOf(5)       // Divisible by 5
  .finite()            // Excludes Infinity
  .safe()              // Safe integer range
```

## Object Schemas

```typescript
const PersonSchema = z.object({
  name: z.string(),
  age: z.number(),
});

// Make all properties optional
PersonSchema.partial();

// Make specific properties optional
PersonSchema.partial({ age: true });

// Make all properties required
PersonSchema.required();

// Pick specific properties
PersonSchema.pick({ name: true });

// Omit specific properties
PersonSchema.omit({ age: true });

// Extend with new properties
PersonSchema.extend({
  email: z.string().email(),
});

// Strict mode - reject unknown keys
PersonSchema.strict();

// Passthrough - preserve unknown keys
PersonSchema.passthrough();

// Strip unknown keys (default behavior)
PersonSchema.strip();
```

## Arrays and Tuples

```typescript
// Array of strings
z.array(z.string())
  .min(1)              // At least 1 element
  .max(10)             // At most 10 elements
  .length(5)           // Exactly 5 elements
  .nonempty();         // At least 1 element (typed)

// Alternative syntax
z.string().array();

// Tuple with fixed positions
z.tuple([
  z.string(),          // First element: string
  z.number(),          // Second element: number
]);

// Tuple with rest elements
z.tuple([z.string(), z.number()]).rest(z.boolean());
```

## Unions and Enums

```typescript
// Union types
z.union([z.string(), z.number()]);
// Shorthand
z.string().or(z.number());

// Discriminated unions (better error messages)
z.discriminatedUnion("type", [
  z.object({ type: z.literal("email"), email: z.string() }),
  z.object({ type: z.literal("phone"), phone: z.string() }),
]);

// Enum from array
z.enum(["admin", "user", "guest"]);

// Native enum
enum Role { Admin, User }
z.nativeEnum(Role);
```

## Optional and Nullable

```typescript
// Optional - allows undefined
z.string().optional();  // string | undefined

// Nullable - allows null
z.string().nullable();  // string | null

// Both
z.string().nullish();   // string | null | undefined

// Default values
z.string().default("anonymous");
z.string().optional().default("anonymous");

// Catch - use default on parse failure
z.string().catch("fallback");
```

## Transforms

```typescript
// Transform output type
const StringToNumber = z.string().transform((val) => parseInt(val, 10));
type Output = z.output<typeof StringToNumber>; // number

// Chain transforms
z.string()
  .trim()
  .toLowerCase()
  .transform((val) => val.split(","));

// Preprocess input before validation
z.preprocess(
  (val) => String(val),
  z.string().min(1)
);
```

## Refinements

```typescript
// Custom validation
z.string().refine(
  (val) => val.length <= 255,
  { message: "String must be 255 chars or less" }
);

// Async refinement
z.string().refine(
  async (val) => await checkUnique(val),
  { message: "Value must be unique" }
);

// Super refine for complex validations
z.object({
  password: z.string(),
  confirm: z.string(),
}).superRefine((data, ctx) => {
  if (data.password !== data.confirm) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Passwords don't match",
      path: ["confirm"],
    });
  }
});
```

## Error Handling

```typescript
const result = schema.safeParse(data);

if (!result.success) {
  // Access all issues
  result.error.issues.forEach((issue) => {
    console.log(issue.path);    // Field path
    console.log(issue.message); // Error message
    console.log(issue.code);    // Error code
  });

  // Flatten for form errors
  const flat = result.error.flatten();
  // { formErrors: string[], fieldErrors: { [key]: string[] } }

  // Format for display
  const formatted = result.error.format();
  // { _errors: string[], field: { _errors: string[] } }
}
```

## Common Patterns

### API Request Validation

```typescript
const CreateUserRequest = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(1).max(100),
});

// In Express/Fastify handler
const body = CreateUserRequest.parse(req.body);
```

### Environment Variables

```typescript
const EnvSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
});

export const env = EnvSchema.parse(process.env);
```

### Form Data

```typescript
const ContactForm = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email address"),
  message: z.string().min(10, "Message must be at least 10 characters"),
});

// With React Hook Form
const { register, handleSubmit } = useForm({
  resolver: zodResolver(ContactForm),
});
```

### API Response

```typescript
const ApiResponse = z.object({
  data: z.array(UserSchema),
  pagination: z.object({
    page: z.number(),
    total: z.number(),
  }),
});

const response = await fetch("/api/users");
const json = await response.json();
const validated = ApiResponse.parse(json);
```

## JSON Schema Conversion

```typescript
import { z } from "zod";

// Zod to JSON Schema
const jsonSchema = z.toJSONSchema(UserSchema);

// JSON Schema to Zod
const zodSchema = z.fromJSONSchema(jsonSchema);
```

## Anti-Patterns

### Avoid redundant type declarations

```typescript
// Bad - duplicates schema
interface User {
  name: string;
  age: number;
}
const UserSchema = z.object({
  name: z.string(),
  age: z.number(),
});

// Good - infer from schema
const UserSchema = z.object({
  name: z.string(),
  age: z.number(),
});
type User = z.infer<typeof UserSchema>;
```

### Use safeParse for user input

```typescript
// Bad - throws on invalid input
const user = UserSchema.parse(userInput);

// Good - handle errors gracefully
const result = UserSchema.safeParse(userInput);
if (!result.success) {
  return { errors: result.error.flatten().fieldErrors };
}
```

### Prefer discriminated unions

```typescript
// Bad - ambiguous errors
z.union([
  z.object({ email: z.string() }),
  z.object({ phone: z.string() }),
]);

// Good - clear error messages
z.discriminatedUnion("contactType", [
  z.object({ contactType: z.literal("email"), email: z.string() }),
  z.object({ contactType: z.literal("phone"), phone: z.string() }),
]);
```

## References

- [Zod Documentation](https://zod.dev)
- [Zod API Reference](https://zod.dev/api)
- [Zod GitHub](https://github.com/colinhacks/zod)
