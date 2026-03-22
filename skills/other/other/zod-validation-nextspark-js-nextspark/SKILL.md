---
name: zod-validation
description: |
  Zod validation patterns for this Next.js application.
  Covers schema definition, API validation, form integration, error formatting, and type inference.
  Use this skill when implementing validation for APIs, forms, or entity schemas.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Zod Validation Skill

Patterns for implementing type-safe validation with Zod across APIs, forms, and entity schemas.

## Architecture Overview

```
ZOD VALIDATION LAYERS:

API Layer:
├── Request body validation
├── Query parameter validation
└── Response type safety

Entity Layer:
├── Entity field validation
├── Create/Update schemas
└── Custom field validators

Form Layer:
├── React Hook Form integration
├── zodResolver for validation
└── Field-level error display

Block Layer:
├── baseBlockSchema extensions
├── Field definition schemas
└── Block-specific validations
```

## When to Use This Skill

- Validating API request bodies
- Creating entity schemas
- Implementing form validation
- Extending block schemas
- Type inference from schemas

## Common Schema Patterns

### Basic Schemas

```typescript
import { z } from 'zod'

// Simple object schema
const userSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email format'),
  age: z.number().int().min(18, 'Must be 18+').optional(),
})

// With enum validation
const statusSchema = z.enum(['active', 'inactive', 'pending'])

// With defaults
const settingsSchema = z.object({
  theme: z.enum(['light', 'dark']).default('light'),
  notifications: z.boolean().default(true),
  language: z.string().default('en'),
})

// Nullable vs Optional
const profileSchema = z.object({
  bio: z.string().optional(),           // undefined allowed
  avatar: z.string().nullable(),        // null allowed
  phone: z.string().nullish(),          // null or undefined
})
```

### Transformations

```typescript
// Transform input
const slugSchema = z.string()
  .transform(s => s.toLowerCase().replace(/\s+/g, '-'))

// Trim whitespace
const cleanStringSchema = z.string().trim()

// Parse JSON string
const jsonSchema = z.string().transform(s => JSON.parse(s))

// Coerce types
const numberFromString = z.coerce.number()  // "123" → 123
const dateFromString = z.coerce.date()      // "2024-01-01" → Date
```

### Refinements

```typescript
// Single refinement
const passwordSchema = z.string()
  .min(8, 'Minimum 8 characters')
  .refine(p => /[A-Z]/.test(p), 'Must contain uppercase')
  .refine(p => /[0-9]/.test(p), 'Must contain number')
  .refine(p => /[!@#$%^&*]/.test(p), 'Must contain special character')

// Cross-field validation
const signupSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],  // Error appears on this field
})

// Async refinement (DB check)
const uniqueEmailSchema = z.string().email().refine(
  async (email) => {
    const exists = await checkEmailExists(email)
    return !exists
  },
  { message: 'Email already registered' }
)
```

### Composition

```typescript
// Extend schema
const baseUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
})

const adminSchema = baseUserSchema.extend({
  role: z.literal('admin'),
  permissions: z.array(z.string()),
})

// Merge schemas
const fullSchema = schemaA.merge(schemaB)

// Pick/Omit fields
const loginSchema = userSchema.pick({ email: true, password: true })
const publicUserSchema = userSchema.omit({ password: true })

// Partial (all optional)
const updateUserSchema = userSchema.partial()

// Required (all required)
const strictSchema = partialSchema.required()
```

## Type Inference

```typescript
// Infer type from schema
const userSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  age: z.number().optional(),
})

type User = z.infer<typeof userSchema>
// Result: { name: string; email: string; age?: number }

// Input vs Output types (when using transform)
type UserInput = z.input<typeof userSchema>   // Before transform
type UserOutput = z.output<typeof userSchema>  // After transform

// Partial type
type UpdateUser = z.infer<typeof userSchema.partial()>
// Result: { name?: string; email?: string; age?: number }

// Pick specific fields
type UserName = z.infer<typeof userSchema.pick({ name: true })>
// Result: { name: string }
```

## API Validation Pattern

### Standard Pattern (safeParse)

```typescript
import { z } from 'zod'
import { NextRequest } from 'next/server'
import { createApiError, createApiResponse } from '@/core/lib/api/helpers'

// Define schema
const createCustomerSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email format'),
  phone: z.string().optional(),
  notes: z.string().max(500).optional(),
})

export async function POST(request: NextRequest) {
  // 1. Parse request body
  const body = await request.json()

  // 2. Validate with safeParse (no exceptions)
  const result = createCustomerSchema.safeParse(body)

  // 3. Handle validation error
  if (!result.success) {
    return createApiError(
      'Validation error',
      400,
      result.error.issues,  // Array of ZodIssue
      'VALIDATION_ERROR'
    )
  }

  // 4. Use validated, type-safe data
  const validatedData = result.data  // Fully typed!

  // 5. Process
  const customer = await CustomerService.create(
    userId,
    teamId,
    validatedData
  )

  return createApiResponse(customer, 201)
}
```

### Query Parameters

```typescript
const listQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['createdAt', 'name', 'updatedAt']).default('createdAt'),
  order: z.enum(['asc', 'desc']).default('desc'),
  search: z.string().optional(),
  status: z.enum(['active', 'inactive', 'all']).default('all'),
})

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const queryObject = Object.fromEntries(searchParams)

  const result = listQuerySchema.safeParse(queryObject)
  if (!result.success) {
    return createApiError('Invalid query parameters', 400, result.error.issues)
  }

  const { page, limit, sort, order, search, status } = result.data
  // ... use validated params
}
```

## Form Integration (React Hook Form)

### Basic Setup

```typescript
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

// 1. Define schema
const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(6, 'Minimum 6 characters'),
})

// 2. Infer type
type LoginFormData = z.infer<typeof loginSchema>

// 3. Use in component
function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    mode: 'onSubmit',
    reValidateMode: 'onChange',
    defaultValues: {
      email: '',
      password: '',
    },
  })

  const onSubmit = async (data: LoginFormData) => {
    // data is fully typed and validated
    await signIn(data.email, data.password)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && (
        <p className="text-sm text-destructive">{errors.email.message}</p>
      )}

      <input type="password" {...register('password')} />
      {errors.password && (
        <p className="text-sm text-destructive">{errors.password.message}</p>
      )}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  )
}
```

### With shadcn/ui Form Components

```typescript
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/core/components/ui/form'
import { Input } from '@/core/components/ui/input'
import { Button } from '@/core/components/ui/button'

function CustomerForm() {
  const form = useForm<CustomerFormData>({
    resolver: zodResolver(customerSchema),
    defaultValues: { name: '', email: '' },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />  {/* Auto-displays error */}
            </FormItem>
          )}
        />
        <Button type="submit">Save</Button>
      </form>
    </Form>
  )
}
```

## Error Formatting

### ZodError Structure

```typescript
// When safeParse fails:
result.error  // ZodError instance
result.error.issues  // Array<ZodIssue>

// ZodIssue structure:
interface ZodIssue {
  code: string           // "too_small", "invalid_type", "custom"
  message: string        // Error message
  path: (string|number)[] // Field path: ["user", "email"]
  minimum?: number       // For min validations
  maximum?: number       // For max validations
  type?: string          // Expected type
}
```

### Flatten for API Responses

```typescript
const result = schema.safeParse(data)

if (!result.success) {
  // Flatten for cleaner API response
  const flattened = result.error.flatten()
  // {
  //   formErrors: [],  // Root-level errors
  //   fieldErrors: {
  //     email: ['Invalid email'],
  //     name: ['Required']
  //   }
  // }

  return createApiError('Validation error', 400, flattened.fieldErrors)
}
```

### Format for Display

```typescript
const formatted = result.error.format()
// {
//   _errors: [],  // Root errors
//   email: { _errors: ['Invalid email'] },
//   name: { _errors: ['Required'] }
// }
```

## Block Schema Extension

### Using baseBlockSchema

```typescript
import { z } from 'zod'
import { baseBlockSchema } from '@/core/types/blocks'

// baseBlockSchema provides:
// - title: z.string().optional()
// - content: z.string().optional()
// - cta: z.object({ text, link, target }).optional()
// - backgroundColor: z.enum([...]).optional()
// - className: z.string().optional()
// - id: z.string().optional()

// Extend with custom fields
export const schema = baseBlockSchema.merge(z.object({
  // Custom fields only - base fields inherited
  features: z.array(z.object({
    icon: z.string().optional(),
    title: z.string().min(1, 'Title required'),
    description: z.string().optional(),
  })).min(1).max(12),
  columns: z.enum(['2', '3', '4']).default('3'),
  showIcons: z.boolean().default(true),
}))

export type FeaturesGridProps = z.infer<typeof schema>
```

## i18n Error Messages

### Dynamic Schema with Translations

```typescript
// Function that returns schema with translated messages
export function createLoginSchema(t: (key: string) => string) {
  return z.object({
    email: z.string()
      .min(1, t('validation.email.required'))
      .email(t('validation.email.invalid')),
    password: z.string()
      .min(1, t('validation.password.required'))
      .min(6, t('validation.password.minLength')),
  })
}

// Usage in component
const { t } = useTranslations('auth')
const schema = createLoginSchema(t)
```

## Existing Schemas

| Schema | Location | Purpose |
|--------|----------|---------|
| `baseBlockSchema` | `core/types/blocks.ts` | Base for all blocks |
| `ctaSchema` | `core/types/blocks.ts` | CTA button definition |
| `teamSchema` | `core/lib/teams/schema.ts` | Team CRUD validation |
| `teamRoleSchema` | `core/lib/teams/schema.ts` | Role validation |
| `subscriptionStatusSchema` | `core/lib/billing/schema.ts` | Subscription states |
| `createPlanSchema` | `core/lib/billing/schema.ts` | Plan creation |
| `loginSchema` | `core/lib/validation-schemas.ts` | Login form |
| `signupSchema` | `core/lib/validation-schemas.ts` | Signup form |

## Anti-Patterns

```typescript
// NEVER: Use parse() in APIs (throws exceptions)
const data = schema.parse(body)  // Throws on error!

// CORRECT: Use safeParse (returns result object)
const result = schema.safeParse(body)
if (!result.success) { /* handle error */ }

// NEVER: Catch and ignore validation errors
try {
  const data = schema.parse(body)
} catch (e) {
  // Don't swallow errors!
}

// CORRECT: Handle errors explicitly
const result = schema.safeParse(body)
if (!result.success) {
  return createApiError('Validation error', 400, result.error.issues)
}

// NEVER: Duplicate base schema fields
const blockSchema = z.object({
  title: z.string(),  // Already in baseBlockSchema!
  content: z.string(),
  // ...custom fields
})

// CORRECT: Extend baseBlockSchema
const blockSchema = baseBlockSchema.merge(z.object({
  // Only custom fields
  customField: z.string(),
}))

// NEVER: Hardcode error messages without i18n support
const schema = z.string().min(1, 'Este campo es requerido')

// CORRECT: Use translation function
const schema = z.string().min(1, t('validation.required'))

// NEVER: Skip type inference
const handleSubmit = (data: any) => { ... }

// CORRECT: Use inferred types
type FormData = z.infer<typeof schema>
const handleSubmit = (data: FormData) => { ... }
```

## Checklist

Before finalizing validation implementation:

- [ ] Using `safeParse` instead of `parse` in APIs
- [ ] Type inference with `z.infer<typeof schema>`
- [ ] Error messages support i18n
- [ ] Block schemas extend `baseBlockSchema`
- [ ] Form uses `zodResolver` with React Hook Form
- [ ] API returns `error.issues` in response
- [ ] Cross-field validations use `.refine()` with proper `path`
- [ ] Optional vs nullable used correctly

## Related Skills

- `entity-api` - API endpoint patterns with validation
- `shadcn-components` - Form component patterns
- `page-builder-blocks` - Block schema patterns
