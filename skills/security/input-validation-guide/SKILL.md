---
name: input-validation-guide
description: >
  Validate and sanitize all user input using schema validation libraries. Activate whenever
  the user writes form handlers, API endpoints, request parsers, data processing functions,
  or any code that accepts external input. Also activate when the user asks about validation
  libraries like Zod, Joi, or Pydantic, or discusses input sanitization.
---

# Input Validation Guide

Validate all external input at system boundaries using schema validation libraries.
Reject invalid data early with clear error messages. Never trust client-side validation
as the sole defense.

## When to Use
- Writing API endpoint handlers that accept request bodies, query params, or path params
- Building form validation logic (server-side)
- Processing data from external APIs or file uploads
- Parsing configuration files or environment variables
- Any function that receives data from outside the trust boundary

## Core Patterns

### Zod (TypeScript)

The standard for TypeScript schema validation. Parse, don't validate.

```typescript
import { z } from 'zod';

// Define schemas as the source of truth
const CreateUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  name: z.string().min(1, 'Name required').max(100),
  age: z.number().int().min(13, 'Must be 13 or older').max(150),
  role: z.enum(['user', 'admin', 'moderator']).default('user'),
  website: z.string().url().optional(),
});

// Infer TypeScript types from schemas
type CreateUserInput = z.infer<typeof CreateUserSchema>;

// Parse at the boundary, use typed data internally
app.post('/api/users', async (req, res) => {
  const result = CreateUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({
      error: 'Validation failed',
      issues: result.error.issues.map(i => ({
        field: i.path.join('.'),
        message: i.message,
      })),
    });
  }
  // result.data is fully typed as CreateUserInput
  const user = await createUser(result.data);
  res.json(user);
});
```

Advanced Zod patterns for complex validation:

```typescript
// Transform and refine
const SearchParamsSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['name', 'date', 'relevance']).default('relevance'),
  q: z.string().trim().min(1).max(200).optional(),
});

// Discriminated unions for type-safe variants
const PaymentSchema = z.discriminatedUnion('method', [
  z.object({
    method: z.literal('card'),
    cardNumber: z.string().regex(/^\d{16}$/),
    expiry: z.string().regex(/^\d{2}\/\d{2}$/),
    cvv: z.string().regex(/^\d{3,4}$/),
  }),
  z.object({
    method: z.literal('bank_transfer'),
    accountNumber: z.string().min(8).max(20),
    routingNumber: z.string().length(9),
  }),
]);

// Custom refinements with cross-field validation
const DateRangeSchema = z.object({
  startDate: z.coerce.date(),
  endDate: z.coerce.date(),
}).refine(
  data => data.endDate > data.startDate,
  { message: 'End date must be after start date', path: ['endDate'] }
);
```

### Pydantic (Python)

The standard for Python data validation using type annotations.

```python
from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import date
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=13, le=150)
    role: UserRole = UserRole.USER
    website: str | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Name cannot be blank")
        return stripped

# FastAPI integration - validation is automatic
@app.post("/api/users")
async def create_user(data: CreateUserRequest):
    # data is already validated and typed
    return await save_user(data)
```

### Allowlists vs Denylists

Always prefer allowlists. Denylists are inherently incomplete.

```typescript
// WRONG: Denylist approach - always has gaps
function sanitizeFilename(name: string): string {
  return name.replace(/[<>:"/\\|?*]/g, ''); // What about null bytes? Unicode tricks?
}

// CORRECT: Allowlist approach - only permit known-good characters
function sanitizeFilename(name: string): string {
  const sanitized = name.replace(/[^a-zA-Z0-9._-]/g, '');
  if (!sanitized || sanitized.startsWith('.')) {
    throw new Error('Invalid filename');
  }
  return sanitized;
}

// CORRECT: Allowlist for content types
const ALLOWED_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp', 'application/pdf']);
function validateContentType(type: string): boolean {
  return ALLOWED_TYPES.has(type);
}
```

### Type Coercion Attack Prevention

Prevent attacks that exploit JavaScript's loose type coercion.

```typescript
// WRONG: Vulnerable to type coercion
app.get('/api/users', (req, res) => {
  // req.query.admin could be "true" (string), true (if parsed), or ["true"] (array)
  if (req.query.admin == true) { // Loose equality - dangerous
    return getAdminData();
  }
});

// CORRECT: Strict parsing with Zod
const QuerySchema = z.object({
  admin: z.enum(['true', 'false']).transform(v => v === 'true').optional(),
  id: z.coerce.number().int().positive(), // Explicit coercion
});

app.get('/api/users', (req, res) => {
  const query = QuerySchema.parse(req.query);
  // query.admin is boolean | undefined, query.id is number
});

// WRONG: JSON.parse without validation
const config = JSON.parse(userInput); // Could be any type

// CORRECT: Parse then validate
const rawData = JSON.parse(userInput);
const config = ConfigSchema.parse(rawData);
```

### Sanitization for Specific Contexts

Apply context-appropriate sanitization after validation.

```typescript
import DOMPurify from 'dompurify';
import sqlstring from 'sqlstring';

// HTML content: strip dangerous tags
function sanitizeHtml(input: string): string {
  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br', 'ul', 'li'],
    ALLOWED_ATTR: [],
  });
}

// Path traversal prevention
function safePath(basedir: string, userPath: string): string {
  const resolved = path.resolve(basedir, userPath);
  if (!resolved.startsWith(basedir)) {
    throw new Error('Path traversal detected');
  }
  return resolved;
}
```

## Anti-Patterns
- Relying solely on client-side validation (easily bypassed)
- Using denylists instead of allowlists for filtering
- Validating deep inside business logic instead of at the boundary
- Using loose equality (`==`) instead of strict equality (`===`) in JavaScript
- Trusting `Content-Type` headers without verifying actual content
- Silently coercing invalid data instead of rejecting it
- Writing custom regex for email, URL, or date validation instead of using library validators
- Catching validation errors and returning generic "Bad Request" without field-level detail

## Quick Reference

| Language | Library | Key Pattern |
|----------|---------|-------------|
| TypeScript | Zod | `schema.safeParse(input)` returns `{ success, data, error }` |
| TypeScript | Joi | `schema.validate(input)` returns `{ value, error }` |
| Python | Pydantic | Class-based models with type annotations |
| Go | validator | Struct tags: `validate:"required,email"` |

| Principle | Rule |
|-----------|------|
| Validate early | At system boundaries, not deep in business logic |
| Allowlist | Permit known-good, reject everything else |
| Parse, don't validate | Transform raw input into typed domain objects |
| Fail loudly | Return specific field-level error messages |
| Never trust client | Server-side validation is mandatory |
