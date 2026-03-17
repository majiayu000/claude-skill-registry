---
name: zod-v4-patterns
description: Ensures Zod v4 patterns are used correctly throughout the codebase. Apply when creating or modifying validation schemas, form schemas, or any Zod validators. Enforces v4 syntax and prevents deprecated v3 patterns.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Zod v4 Patterns for kove-webapp

This skill ensures consistent usage of Zod v4 patterns and prevents deprecated v3 syntax.

## When to Apply

Use these patterns when:
- Creating new validation schemas
- Defining form validation with React Hook Form
- Writing API request/response validators
- Updating existing Zod schemas from v3
- Adding custom error messages to validators

## Critical Pattern Changes from v3 to v4

### 1. Error Customization (Most Important)

**✅ v4: Use `error` parameter**
```typescript
z.string({ error: "Custom error message" })
z.number({ error: "Must be a number" })
z.boolean({ error: "Must be true or false" })
```

**❌ v3 patterns (AVOID):**
```typescript
z.string({ message: "..." })
z.string({ invalid_type_error: "..." })
z.string({ required_error: "..." })
```

### 2. String Format Validators

**✅ v4: Top-level functions**
```typescript
z.email()
z.email({ error: "Invalid email address" })

z.uuid()
z.uuid({ error: "Must be a valid UUID" })

z.url()
z.url({ error: "Must be a valid URL" })
```

**❌ v3: Chained methods (AVOID)**
```typescript
z.string().email()
z.string().uuid()
z.string().url()
```

### 3. Object Strictness

**✅ v4: Use constructors**
```typescript
// Strict: No unknown keys allowed
z.strictObject({
  name: z.string(),
  age: z.number()
})

// Loose: Allow unknown keys to pass through
z.looseObject({
  name: z.string(),
  age: z.number()
})

// Default object (strips unknown keys)
z.object({
  name: z.string(),
  age: z.number()
})
```

**❌ v3: Chained methods (AVOID)**
```typescript
z.object({ ... }).strict()
z.object({ ... }).passthrough()
```

### 4. Schema Composition

**✅ v4: Use `.extend()`**
```typescript
const baseSchema = z.object({
  name: z.string(),
  email: z.email()
});

const extendedSchema = baseSchema.extend({
  age: z.number(),
  phone: z.string()
});
```

**❌ v3: `.merge()` (AVOID)**
```typescript
const extendedSchema = baseSchema.merge(additionalSchema);
```

### 5. Default Values

**⚠️ Important: `.default()` applies AFTER validation**

The default value must match the **output type**, not the input type:

```typescript
// ✅ Correct: Default matches output type
z.string().transform(s => s.length).default(5)

// ❌ Wrong: Default doesn't match output (output is number)
z.string().transform(s => s.length).default("hello")
```

**Use `.prefault()` for pre-validation defaults:**
```typescript
// Applies default BEFORE validation
z.string().prefault("default value")
```

### 6. Error Handling

**✅ v4: Use `z.prettifyError()` or `z.treeifyError()`**
```typescript
const result = schema.safeParse(data);

if (!result.success) {
  // Pretty print errors for debugging
  console.error(z.prettifyError(result.error));

  // Or get tree structure
  const errorTree = z.treeifyError(result.error);
}
```

**❌ v3: Avoid old methods**
```typescript
result.error.format()    // Deprecated
result.error.flatten()   // Deprecated
result.error.formErrors  // Deprecated
```

## Common Validation Patterns

### Form Schema Example

```typescript
import { z } from 'zod';

const formSchema = z.object({
  // Basic string with custom error
  name: z.string({ error: "Name is required" }),

  // Email validation
  email: z.email({ error: "Invalid email address" }),

  // String with minimum length
  password: z.string({ error: "Password is required" })
    .min(8, { error: "Password must be at least 8 characters" }),

  // Optional field
  phone: z.string().optional(),

  // Number with range
  age: z.number({ error: "Age must be a number" })
    .min(18, { error: "Must be at least 18 years old" })
    .max(120, { error: "Invalid age" }),

  // Boolean with default
  terms: z.boolean({ error: "Must be true or false" })
    .refine(val => val === true, {
      message: "You must accept the terms and conditions"
    }),

  // Enum
  role: z.enum(['admin', 'user', 'guest'], {
    error: "Invalid role selected"
  }),

  // Array of strings
  tags: z.array(z.string({ error: "Each tag must be a string" }))
    .min(1, { error: "At least one tag is required" }),

  // Nested object
  address: z.object({
    street: z.string({ error: "Street is required" }),
    city: z.string({ error: "City is required" }),
    zip: z.string({ error: "ZIP code is required" })
  }),

  // UUID
  userId: z.uuid({ error: "Invalid user ID format" })
});

type FormData = z.infer<typeof formSchema>;
```

### API Request Schema

```typescript
const createLeaseSchema = z.strictObject({
  propertyId: z.uuid({ error: "Invalid property ID" }),
  tenantId: z.uuid({ error: "Invalid tenant ID" }),
  startDate: z.string({ error: "Start date is required" })
    .transform(str => new Date(str)),
  endDate: z.string({ error: "End date is required" })
    .transform(str => new Date(str)),
  monthlyRent: z.number({ error: "Monthly rent must be a number" })
    .positive({ error: "Monthly rent must be positive" }),
  deposit: z.number({ error: "Deposit must be a number" })
    .nonnegative({ error: "Deposit cannot be negative" })
}).refine(data => data.endDate > data.startDate, {
  message: "End date must be after start date",
  path: ["endDate"]
});
```

### Server Action Validation

```typescript
'use server';

import { z } from 'zod';

const inputSchema = z.object({
  organizationId: z.uuid({ error: "Invalid organization ID" }),
  name: z.string({ error: "Name is required" })
    .min(1, { error: "Name cannot be empty" }),
  email: z.email({ error: "Invalid email address" })
});

export async function createTenant(input: unknown) {
  // Validate input
  const result = inputSchema.safeParse(input);

  if (!result.success) {
    return {
      error: z.prettifyError(result.error)
    };
  }

  const validatedData = result.data;

  // Use validatedData (fully typed)
  // ...
}
```

## React Hook Form Integration

```typescript
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const formSchema = z.object({
  email: z.email({ error: "Invalid email address" }),
  password: z.string({ error: "Password is required" })
    .min(8, { error: "Password must be at least 8 characters" })
});

type FormValues = z.infer<typeof formSchema>;

export function LoginForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      password: ''
    }
  });

  const onSubmit = async (data: FormValues) => {
    // data is fully typed and validated
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* form fields */}
    </form>
  );
}
```

## Migration Checklist

When updating schemas from v3 to v4:

- [ ] Replace `{ message: "..." }` with `{ error: "..." }`
- [ ] Replace `{ invalid_type_error: "..." }` with `{ error: "..." }`
- [ ] Replace `{ required_error: "..." }` with `{ error: "..." }`
- [ ] Replace `z.string().email()` with `z.email()`
- [ ] Replace `z.string().uuid()` with `z.uuid()`
- [ ] Replace `z.string().url()` with `z.url()`
- [ ] Replace `.strict()` with `z.strictObject()`
- [ ] Replace `.passthrough()` with `z.looseObject()`
- [ ] Replace `.merge()` with `.extend()`
- [ ] Replace `.format()` with `z.prettifyError()`
- [ ] Replace `.flatten()` with `z.prettifyError()` or `z.treeifyError()`
- [ ] Verify `.default()` values match output types
- [ ] Consider using `.prefault()` for pre-validation defaults

## Common Mistakes to Avoid

### ❌ Using v3 error syntax
```typescript
// Wrong
z.string({ message: "Required" })
z.string({ invalid_type_error: "Must be string" })

// Correct
z.string({ error: "Required" })
```

### ❌ Using chained format validators
```typescript
// Wrong
z.string().email()
z.string().url()

// Correct
z.email()
z.url()
```

### ❌ Using .merge() for composition
```typescript
// Wrong
const extended = baseSchema.merge(additionalSchema);

// Correct
const extended = baseSchema.extend({ ...additionalFields });
```

### ❌ Wrong default type
```typescript
// Wrong: default doesn't match output type (number)
z.string().transform(s => parseInt(s)).default("0")

// Correct: default matches output type
z.string().transform(s => parseInt(s)).default(0)
```

### ❌ Using deprecated error methods
```typescript
// Wrong
if (!result.success) {
  const errors = result.error.flatten();
}

// Correct
if (!result.success) {
  console.error(z.prettifyError(result.error));
}
```

## Advanced Patterns

### Custom Refinements
```typescript
const passwordSchema = z.string({ error: "Password is required" })
  .min(8, { error: "Password must be at least 8 characters" })
  .refine(val => /[A-Z]/.test(val), {
    message: "Password must contain at least one uppercase letter"
  })
  .refine(val => /[0-9]/.test(val), {
    message: "Password must contain at least one number"
  });
```

### Conditional Validation
```typescript
const schema = z.object({
  type: z.enum(['individual', 'company']),
  name: z.string({ error: "Name is required" }),
  companyName: z.string().optional()
}).refine(data => {
  if (data.type === 'company') {
    return !!data.companyName;
  }
  return true;
}, {
  message: "Company name is required for company type",
  path: ["companyName"]
});
```

### Discriminated Unions
```typescript
const eventSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('click'),
    x: z.number(),
    y: z.number()
  }),
  z.object({
    type: z.literal('keypress'),
    key: z.string()
  })
]);
```

### Transform with Validation
```typescript
const dateSchema = z.string({ error: "Date is required" })
  .refine(val => !isNaN(Date.parse(val)), {
    message: "Invalid date format"
  })
  .transform(val => new Date(val));
```

## What to Check

When reviewing Zod schemas:

1. ✅ Are error messages using `{ error: "..." }` syntax?
2. ✅ Are email/uuid/url validators using top-level functions?
3. ✅ Are object strictness patterns using constructors?
4. ✅ Is schema composition using `.extend()`?
5. ✅ Do `.default()` values match output types?
6. ✅ Is error handling using `z.prettifyError()` or `z.treeifyError()`?
7. ✅ Are there any deprecated v3 patterns?
8. ✅ Are refinements used for complex validation logic?
9. ✅ Are TypeScript types inferred with `z.infer<typeof schema>`?

## Resources

- Zod v4 Documentation: Check official docs for latest patterns
- Location: All schema definitions throughout the codebase
- Integration: React Hook Form uses `zodResolver` for form validation
