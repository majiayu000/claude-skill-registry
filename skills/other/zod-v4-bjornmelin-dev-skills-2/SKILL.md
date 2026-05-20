---
name: zod-v4
description: Expert guidance for Zod v4 schema validation in TypeScript. Use when designing schemas, migrating from Zod 3, handling validation errors, generating JSON Schema/OpenAPI, using codecs/transforms, or integrating with React Hook Form, tRPC, Hono, or Next.js. Covers all Zod v4 APIs including top-level string formats, strictObject/looseObject, metadata, registries, branded types, and recursive schemas.
---

# Zod v4 Schema Validation

## Quick Start

```bash
pnpm add zod@^4.3.5
```

```typescript
import { z } from 'zod';

// Define schema
const User = z.object({
  name: z.string().min(1),
  email: z.email(),
  age: z.number().positive(),
});

// Parse (throws on error)
const user = User.parse({ name: "Alice", email: "alice@example.com", age: 30 });

// Safe parse (returns result)
const result = User.safeParse(data);
if (result.success) {
  result.data; // validated
} else {
  console.log(z.prettifyError(result.error));
}

// Type inference
type User = z.infer<typeof User>;
```

## Versioning + Imports (v4.3.5)

- Use `import { z } from "zod"` for v4 (package root now exports v4).
- Use `import * as z from "zod/mini"` for Zod Mini.
- Use `import * as z from "zod/v3"` only if you must stay on v3.

## Workflow: Determine Task Type

**Designing new schemas?**
→ Read [API Reference](references/api-reference.md)

**Migrating from Zod 3?**
→ Read [Migration Guide](references/migration-guide.md)

**Working with codecs, errors, JSON Schema, or metadata?**
→ Read [Advanced Features](references/advanced-features.md)

**Integrating with frameworks (RHF, tRPC, Hono, Next.js)?**
→ Read [Ecosystem Patterns](references/ecosystem-patterns.md)

---

## Key v4 Concepts

### Top-Level String Formats

v4 moved string validators to top-level functions:

```typescript
// v4 style (preferred)
z.email()
z.uuid()
z.url()
z.ipv4()
z.ipv6()
z.iso.date()
z.iso.datetime()

// v3 style (deprecated but works)
z.string().email()
```

### Object Variants

```typescript
z.object({})        // Allows unknown keys (default)
z.strictObject({})  // Rejects unknown keys
z.looseObject({})   // Explicitly allows unknown keys
```

### Unified Error Parameter

```typescript
// String message
z.string().min(5, { error: "Too short" });

// Function for dynamic messages
z.string({
  error: (iss) => iss.input === undefined ? "Required" : "Invalid"
});
```

### Type Inference

```typescript
const Schema = z.object({ name: z.string() });
type Schema = z.infer<typeof Schema>;

// For transforms, get input/output separately
const Transformed = z.string().transform(s => s.length);
type Input = z.input<typeof Transformed>;   // string
type Output = z.output<typeof Transformed>; // number
```

---

## Common Patterns

### Discriminated Unions

```typescript
const Event = z.discriminatedUnion("type", [
  z.object({ type: z.literal("click"), x: z.number(), y: z.number() }),
  z.object({ type: z.literal("keypress"), key: z.string() }),
]);
```

### Exhaustive Records

```typescript
const Status = z.enum(["pending", "active", "done"]);

// All keys required
z.record(Status, z.number())  // { pending: number; active: number; done: number }

// Keys optional
z.partialRecord(Status, z.number())  // { pending?: number; active?: number; done?: number }
```

### Recursive Schemas

```typescript
const Category = z.object({
  name: z.string(),
  get subcategories() { return z.array(Category) }
});
```

### Branded Types

```typescript
const UserId = z.string().brand<"UserId">();
const PostId = z.string().brand<"PostId">();

type UserId = z.infer<typeof UserId>;
// Cannot assign UserId to PostId
```

### Transforms and Pipes

```typescript
// Transform
z.string().transform(s => s.toUpperCase())

// Pipe (chain schemas)
z.pipe(
  z.string(),
  z.coerce.number(),
  z.number().positive()
)
```

### Default Values

```typescript
// Output default (v4)
z.string().default("guest")

// Input default (pre-transform)
z.string().transform(s => s.toUpperCase()).prefault("hello")
// Missing => "HELLO"
```

---

## Error Handling

### Pretty Print

```typescript
const result = schema.safeParse(data);
if (!result.success) {
  console.log(z.prettifyError(result.error));
  // ✖ Invalid email
  //   → at email
}
```

### Flat Structure (Forms)

```typescript
const flat = z.flattenError(result.error);
// { formErrors: [], fieldErrors: { email: ["Invalid email"] } }
```

### Tree Structure (Nested)

```typescript
const tree = z.treeifyError(result.error);
// { properties: { email: { errors: ["Invalid email"] } } }
```

---

## JSON Schema / OpenAPI

```typescript
const schema = z.object({
  name: z.string(),
  email: z.email(),
}).meta({ id: "User", title: "User" });

// Generate JSON Schema
const jsonSchema = z.toJSONSchema(schema);

// For OpenAPI 3.0
z.toJSONSchema(schema, { target: "openapi-3.0" });

// Using registry for multiple schemas
z.globalRegistry.add(schema, schema.meta());
const allSchemas = z.toJSONSchema(z.globalRegistry);
```

---

## v3 to v4 Migration Quick Reference

| v3 | v4 |
|----|----|
| `z.string().email()` | `z.email()` |
| `z.nativeEnum(MyEnum)` | `z.enum(MyEnum)` |
| `{ message: "..." }` | `{ error: "..." }` |
| `.strict()` | `z.strictObject({})` |
| `.passthrough()` | `z.looseObject({})` |
| `.merge(other)` | `.extend(other.shape)` |
| `z.record(valueSchema)` | `z.record(z.string(), valueSchema)` |
| `.deepPartial()` | Nest `.partial()` manually |
| `error.format()` | `z.treeifyError(error)` |
| `error.flatten()` | `z.flattenError(error)` |

### Breaking Changes

- **Numbers**: No `Infinity`, stricter `.safe()` and `.int()`
- **UUID**: RFC 4122 compliant (use `z.guid()` for permissive)
- **Defaults in optional**: `z.string().default("x").optional()` now applies default
- **z.unknown()**: No longer implicitly optional
- **Error precedence**: Schema-level wins over global

Run codemod: `npx zod-v3-to-v4`

---

## Framework Integration Quick Start

### React Hook Form

```typescript
import { zodResolver } from '@hookform/resolvers/zod';

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema),
});
```

### tRPC

```typescript
publicProcedure
  .input(z.object({ id: z.string() }))
  .query(({ input }) => getById(input.id))
```

### Hono

```typescript
import { zValidator } from '@hono/zod-validator';

app.post('/users', zValidator('json', schema), (c) => {
  const data = c.req.valid('json');
});
```

### Next.js Server Actions

```typescript
'use server';

const result = schema.safeParse(Object.fromEntries(formData));
if (!result.success) {
  return { errors: z.flattenError(result.error).fieldErrors };
}
```

---

## Reference Files

- [API Reference](references/api-reference.md) - All schema types, methods, and validation APIs
- [Advanced Features](references/advanced-features.md) - Codecs, error handling, metadata, JSON Schema
- [Migration Guide](references/migration-guide.md) - Complete v3 to v4 migration reference
- [Ecosystem Patterns](references/ecosystem-patterns.md) - Framework integrations and organization patterns
