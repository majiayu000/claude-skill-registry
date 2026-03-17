---
name: zod-validation
description: Zod schema validation patterns. Input validation, type inference, transformations, error handling. Use when creating validation schemas or handling user input.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Zod Validation - Schema Design Patterns

## Purpose

Expert guidance for Zod validation:

- **Schema Design** - Create robust validation schemas
- **Type Inference** - Derive TypeScript types from schemas
- **Transformations** - Parse and transform data
- **Error Handling** - User-friendly error messages
- **Integration** - tRPC, forms, API routes

---

## Core Patterns

### Basic Schema

```typescript
import { z } from 'zod';

// Define schema
const userSchema = z.object({
	id: z.string().uuid(),
	email: z.string().email(),
	name: z.string().min(2).max(100),
	age: z.number().int().positive().optional(),
	role: z.enum(['admin', 'user', 'guest']),
	createdAt: z.date(),
});

// Infer TypeScript type
type User = z.infer<typeof userSchema>;
// { id: string; email: string; name: string; age?: number; role: 'admin' | 'user' | 'guest'; createdAt: Date }
```

### Input vs Output Types

```typescript
const createUserSchema = z.object({
	email: z.string().email(),
	name: z.string().min(2),
	password: z.string().min(8),
});

// Input type (what client sends)
type CreateUserInput = z.input<typeof createUserSchema>;

// Output type (after parsing)
type CreateUserOutput = z.output<typeof createUserSchema>;
```

---

## Common Validators

### Strings

```typescript
z.string().email(); // Email format
z.string().url(); // URL format
z.string().uuid(); // UUID format
z.string().cuid(); // CUID format
z.string().min(1); // Non-empty
z.string().max(255); // Max length
z.string().regex(/^[a-z]+$/); // Custom regex
z.string().trim(); // Trim whitespace
z.string().toLowerCase(); // Transform to lowercase
```

### Numbers

```typescript
z.number().int(); // Integer only
z.number().positive(); // > 0
z.number().nonnegative(); // >= 0
z.number().min(0).max(100); // Range
z.number().multipleOf(5); // Divisible by 5
z.number().finite(); // No Infinity
```

### Objects

```typescript
// Required & optional
z.object({
	required: z.string(),
	optional: z.string().optional(),
	nullable: z.string().nullable(),
	default: z.string().default('value'),
});

// Passthrough unknown keys
z.object({ name: z.string() }).passthrough();

// Strip unknown keys (default)
z.object({ name: z.string() }).strict();

// Extend schema
const baseSchema = z.object({ id: z.string() });
const extendedSchema = baseSchema.extend({ name: z.string() });

// Merge schemas
const merged = schemaA.merge(schemaB);

// Pick/omit fields
const partial = schema.pick({ name: true, email: true });
const omitted = schema.omit({ password: true });
```

### Arrays

```typescript
z.array(z.string()); // String array
z.array(z.number()).min(1); // Non-empty array
z.array(z.object({})).max(10); // Max 10 items
z.string().array(); // Alternative syntax
z.tuple([z.string(), z.number()]); // Fixed tuple
```

---

## Transformations

### Transform

```typescript
const slugSchema = z.string().transform((val) => val.toLowerCase().replace(/\s+/g, '-'));

slugSchema.parse('Hello World'); // 'hello-world'
```

### Coerce (Parse from string)

```typescript
// Useful for form data / URL params
z.coerce.number(); // "123" -> 123
z.coerce.boolean(); // "true" -> true
z.coerce.date(); // "2024-01-01" -> Date
```

### Preprocess

```typescript
const trimmedString = z.preprocess(
	(val) => (typeof val === 'string' ? val.trim() : val),
	z.string().min(1)
);
```

---

## Refinements

### Simple Refinement

```typescript
const passwordSchema = z
	.string()
	.min(8)
	.refine((val) => /[A-Z]/.test(val), {
		message: 'Must contain uppercase letter',
	})
	.refine((val) => /[0-9]/.test(val), {
		message: 'Must contain number',
	});
```

### Super Refine (Multiple Errors)

```typescript
const passwordSchema = z.string().superRefine((val, ctx) => {
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
			message: 'Must contain uppercase letter',
		});
	}
});
```

### Cross-field Validation

```typescript
const registerSchema = z
	.object({
		password: z.string().min(8),
		confirmPassword: z.string(),
	})
	.refine((data) => data.password === data.confirmPassword, {
		message: "Passwords don't match",
		path: ['confirmPassword'],
	});
```

---

## Error Handling

### Safe Parse

```typescript
const result = userSchema.safeParse(input);

if (result.success) {
	// result.data is typed as User
	console.log(result.data);
} else {
	// result.error is ZodError
	console.log(result.error.issues);
}
```

### Custom Error Messages

```typescript
const schema = z.object({
	email: z
		.string({
			required_error: 'Email is required',
			invalid_type_error: 'Email must be a string',
		})
		.email({ message: 'Invalid email format' }),

	age: z
		.number({
			required_error: 'Age is required',
		})
		.min(18, { message: 'Must be 18 or older' }),
});
```

### Format Errors

```typescript
import { z } from 'zod';

function formatZodErrors(error: z.ZodError): Record<string, string[]> {
	const formatted: Record<string, string[]> = {};

	for (const issue of error.issues) {
		const path = issue.path.join('.');
		if (!formatted[path]) {
			formatted[path] = [];
		}
		formatted[path].push(issue.message);
	}

	return formatted;
}

// Usage
const result = schema.safeParse(input);
if (!result.success) {
	const errors = formatZodErrors(result.error);
	// { email: ['Invalid email format'], password: ['Too short'] }
}
```

---

## Integration Patterns

### tRPC Procedures

```typescript
import { z } from 'zod';
import { publicProcedure, protectedProcedure } from '../trpc';

export const userRouter = {
	getById: publicProcedure.input(z.object({ id: z.string().uuid() })).query(async ({ input }) => {
		return db.user.findUnique({ where: { id: input.id } });
	}),

	create: protectedProcedure.input(createUserSchema).mutation(async ({ input, ctx }) => {
		return db.user.create({ data: { ...input, createdBy: ctx.user.id } });
	}),
};
```

### Server Actions (Next.js)

```typescript
'use server';

import { z } from 'zod';

const formSchema = z.object({
	name: z.string().min(2),
	email: z.string().email(),
});

export async function submitForm(formData: FormData) {
	const parsed = formSchema.safeParse({
		name: formData.get('name'),
		email: formData.get('email'),
	});

	if (!parsed.success) {
		return { error: parsed.error.flatten() };
	}

	// Process valid data
	await saveToDatabase(parsed.data);
	return { success: true };
}
```

### API Route Validation

```typescript
import { z } from 'zod';
import { NextResponse } from 'next/server';

const bodySchema = z.object({
	title: z.string().min(1),
	content: z.string(),
});

export async function POST(request: Request) {
	const body = await request.json();
	const parsed = bodySchema.safeParse(body);

	if (!parsed.success) {
		return NextResponse.json({ errors: parsed.error.flatten() }, { status: 400 });
	}

	// Use parsed.data
	const result = await createPost(parsed.data);
	return NextResponse.json(result, { status: 201 });
}
```

---

## Schema Organization

### Structure

```
types/
├── schemas/
│   ├── user.schema.ts
│   ├── post.schema.ts
│   └── common.schema.ts
└── index.ts
```

### Reusable Schemas

```typescript
// types/schemas/common.schema.ts
export const idSchema = z.string().uuid();
export const emailSchema = z.string().email().toLowerCase();
export const timestampSchema = z.date().or(z.string().datetime());

export const paginationSchema = z.object({
	page: z.coerce.number().int().positive().default(1),
	limit: z.coerce.number().int().positive().max(100).default(20),
});
```

---

## Agent Integration

This skill is used by:

- **zod-schema-designer** agent
- **zod-validator** agent
- **input-sanitizer** agent
- **security-auditor** for validation checks

---

## FORBIDDEN

1. **`parse()` without try/catch** - Use `safeParse()` instead
2. **Missing validation on API inputs** - ALWAYS validate
3. **Inline schemas** - Define in types/ folder
4. **Generic error messages** - Be specific
5. **Skipping coercion for form data** - Use `z.coerce`

---

## Version

- **v1.0.0** - Initial implementation based on Zod 3.x patterns
