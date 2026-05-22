---
name: input-validation
description: Input validation and sanitization patterns. Use when validating user input, preventing injection attacks, implementing allowlists, or sanitizing HTML/SQL/command inputs.
context: fork
agent: security-auditor
version: 2.0.0
tags: [security, validation, zod, pydantic, 2026]
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
author: SkillForge
user-invocable: false
---

# Input Validation

Validate and sanitize all untrusted input using Zod v4 and Pydantic.

## Overview

- Processing user input
- Query parameters
- Form submissions
- API request bodies
- File uploads
- URL validation

## Core Principles

1. **Never trust user input**
2. **Validate on server-side** (client-side is UX only)
3. **Use allowlists** (not blocklists)
4. **Validate type, length, format, range**

## Quick Reference

### Zod v4 Schema

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.coerce.number().int().min(0).max(150),
  role: z.enum(['user', 'admin']).default('user'),
});

const result = UserSchema.safeParse(req.body);
if (!result.success) {
  return res.status(400).json({ errors: result.error.flatten() });
}
```

### Type Coercion (v4)

```typescript
// Query params come as strings - coerce to proper types
z.coerce.number()  // "123" → 123
z.coerce.boolean() // "true" → true
z.coerce.date()    // "2024-01-01" → Date
```

### Discriminated Unions

```typescript
const ShapeSchema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('circle'), radius: z.number() }),
  z.object({ type: z.literal('rectangle'), width: z.number(), height: z.number() }),
]);
```

### Pydantic (Python)

```python
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=150)
```

## Anti-Patterns (FORBIDDEN)

```typescript
// ❌ NEVER rely on client-side validation only
if (formIsValid) submit();  // No server validation

// ❌ NEVER use blocklists
const blocked = ['password', 'secret'];  // Easy to miss fields

// ❌ NEVER trust Content-Type header
if (file.type === 'image/png') {...}  // Can be spoofed

// ❌ NEVER build queries with string concat
"SELECT * FROM users WHERE name = '" + name + "'"  // SQL injection

// ✅ ALWAYS validate server-side
const result = schema.safeParse(req.body);

// ✅ ALWAYS use allowlists
const allowed = ['name', 'email', 'createdAt'];

// ✅ ALWAYS validate file magic bytes
const isPng = buffer[0] === 0x89 && buffer[1] === 0x50;

// ✅ ALWAYS use parameterized queries
db.query('SELECT * FROM users WHERE name = ?', [name]);
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Validation library | Zod (TS), Pydantic (Python) |
| Strategy | Allowlist over blocklist |
| Location | Server-side always |
| Error messages | Generic (don't leak info) |
| File validation | Check magic bytes, not just extension |

## Detailed Documentation

| Resource | Description |
|----------|-------------|
| [references/zod-v4-api.md](references/zod-v4-api.md) | Zod v4 API with coercion, transforms |
| [examples/validation-patterns.md](examples/validation-patterns.md) | Complete validation examples |
| [checklists/validation-checklist.md](checklists/validation-checklist.md) | Implementation checklist |
| [templates/validation-schemas.ts](templates/validation-schemas.ts) | Ready-to-use schema templates |

## Related Skills

- `owasp-top-10` - Injection prevention
- `auth-patterns` - User input in auth
- `type-safety-validation` - TypeScript patterns

## Capability Details

### schema-validation
**Keywords:** schema, validate, Zod, Pydantic, validation
**Solves:**
- Validate input against schemas
- Define validation rules declaratively
- Handle validation errors gracefully

### type-coercion
**Keywords:** coerce, coercion, type conversion, parse
**Solves:**
- Automatically convert input types
- Parse strings to numbers/dates
- Handle type mismatches

### allowlist-validation
**Keywords:** allowlist, whitelist, enum, literal, allowed values
**Solves:**
- Validate against allowed values
- Prevent injection attacks
- Restrict input to safe options

### html-sanitization
**Keywords:** sanitize, HTML, XSS, escape, DOMPurify
**Solves:**
- Sanitize HTML input safely
- Prevent XSS attacks
- Allow safe HTML subset

### file-validation
**Keywords:** file, upload, MIME type, file size, file type
**Solves:**
- Validate file uploads securely
- Check file content not just extension
- Enforce size limits

### error-formatting
**Keywords:** error, error message, validation error, user-friendly
**Solves:**
- Format validation errors for users
- Avoid exposing internal details
- Provide actionable error messages
