---
name: "API Development"
description: "Build REST APIs with proper error handling, status codes, request validation, response formatting, and rate limiting. Apply when creating API routes, handling errors, validating input, or designing API responses."
allowed-tools: Read, Write, Edit, Bash
version: 1.1.0
compatibility: Claude Opus 4.5, Claude Code v2.x
updated: 2026-01-24
---

# API Development

Systematic REST API development with error handling, validation, and consistent response formats.

## Overview

This Skill enforces:
- HTTP status codes (appropriate, not overused)
- RFC 7807 Problem Details for errors
- Input validation and sanitization
- Consistent response formatting
- Request correlation IDs
- Rate limiting
- Security-first error messages
- Centralized error handling

Apply when building API routes, handling errors, or designing responses.

## HTTP Status Codes

### Status Code Categories

| Range | Purpose | Common Examples |
|-------|---------|-----------------|
| 200-299 | Success | 200 OK, 201 Created, 204 No Content |
| 300-399 | Redirection | 301 Moved Permanently, 302 Found |
| 400-499 | Client Errors | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| 500-599 | Server Errors | 500 Internal Error, 503 Service Unavailable |

### Correct Status Codes

```ts
// ✅ GOOD: Specific status codes
200  // GET: Resource retrieved
201  // POST: Resource created
204  // DELETE: Resource deleted (no content)
400  // Bad Request: Validation failed
401  // Unauthorized: Not authenticated
403  // Forbidden: Authenticated but no permission
404  // Not Found: Resource doesn't exist
409  // Conflict: Duplicate email
422  // Unprocessable Entity: Semantic error
429  // Too Many Requests: Rate limited
500  // Internal Server Error: Server bug

// ❌ BAD: Vague status codes
200  // Success response for everything
500  // Error response for everything
200  // Returned even when validation failed
```

## Error Response Format (RFC 7807)

### Problem Details Structure

```ts
// RFC 7807 Problem Details
type ProblemDetails = {
  type: string;        // URL to error type documentation
  title: string;       // Short error title
  status: number;      // HTTP status code
  detail: string;      // Specific error details
  instance?: string;   // Request ID for tracking
  errors?: Record<string, string[]>;  // Field-level errors
};
```

### Implementation

```ts
// lib/errors.ts
export class ApiError extends Error {
  constructor(
    public status: number,
    public title: string,
    public detail: string,
    public type: string = 'about:blank',
    public errors?: Record<string, string[]>
  ) {
    super(detail);
    this.name = 'ApiError';
  }

  toJSON() {
    return {
      type: this.type,
      title: this.title,
      status: this.status,
      detail: this.detail,
      instance: this.instance,
      ...(this.errors && { errors: this.errors })
    };
  }
}
```

### Error Responses

```ts
// ✅ GOOD: RFC 7807 format
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 400,
  "detail": "The request body contains invalid data",
  "instance": "req-12345",
  "errors": {
    "email": ["Invalid email format"],
    "age": ["Must be >= 18"]
  }
}

// ✅ GOOD: Unauthorized (no sensitive details)
{
  "type": "https://api.example.com/errors/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Authentication required",
  "instance": "req-12346"
}

// ❌ BAD: Leaks internal details
{
  "error": "User not found in database",
  "stack": "Error: query failed at line 42..."
}

// ❌ BAD: Not structured
{
  "message": "Something went wrong"
}
```

## Centralized Error Handler

```ts
// middleware/error-handler.ts
import { NextRequest, NextResponse } from 'next/server';
import { ApiError } from '@/lib/errors';

export function errorHandler(error: unknown) {
  const requestId = crypto.randomUUID();

  // Log error (internal, never exposed)
  console.error(`[${requestId}] Error:`, error);

  // ApiError (predictable)
  if (error instanceof ApiError) {
    return NextResponse.json(
      {
        type: error.type,
        title: error.title,
        status: error.status,
        detail: error.detail,
        instance: requestId,
        ...(error.errors && { errors: error.errors })
      },
      { status: error.status }
    );
  }

  // Validation error
  if (error instanceof ZodError) {
    return NextResponse.json(
      {
        type: 'https://api.example.com/errors/validation-failed',
        title: 'Validation Failed',
        status: 400,
        detail: 'The request body contains invalid data',
        instance: requestId,
        errors: error.flatten().fieldErrors
      },
      { status: 400 }
    );
  }

  // Unknown error (generic message)
  return NextResponse.json(
    {
      type: 'https://api.example.com/errors/internal-server-error',
      title: 'Internal Server Error',
      status: 500,
      detail: 'An unexpected error occurred',
      instance: requestId
    },
    { status: 500 }
  );
}
```

### Using Error Handler

```ts
// app/api/users/route.ts
import { errorHandler } from '@/middleware/error-handler';

export async function POST(request: Request) {
  try {
    const body = await request.json();

    // Validate
    const validated = CreateUserSchema.parse(body);

    // Check duplicate
    const existing = await db.user.findUnique({
      where: { email: validated.email }
    });

    if (existing) {
      throw new ApiError(
        409,
        'Conflict',
        'A user with this email already exists',
        'https://api.example.com/errors/duplicate-email'
      );
    }

    // Create
    const user = await db.user.create({ data: validated });

    return new Response(JSON.stringify(user), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return errorHandler(error);
  }
}
```

## Input Validation

### Schema Validation

```ts
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  name: z.string().min(1, 'Name required').max(255),
  age: z.number().int().min(0).max(150),
  role: z.enum(['admin', 'user', 'guest']).default('user')
});

// Validate request
const validated = CreateUserSchema.parse(body);
```

### Sanitization

```ts
import DOMPurify from 'isomorphic-dompurify';

const sanitized = {
  ...validated,
  name: DOMPurify.sanitize(validated.name)
};
```

## Rate Limiting

```ts
import rateLimit from 'express-rate-limit';

// General rate limiter
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                   // 100 requests per window
  message: 'Too many requests, please try again later',
  standardHeaders: true,      // Return rate limit info in headers
  legacyHeaders: false
});

// Auth rate limiter (stricter)
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,                      // 5 attempts
  skipSuccessfulRequests: true // Don't count successful logins
});

app.post('/login', authLimiter, loginHandler);
app.use('/api/', limiter);
```

## Response Formatting

### Success Response

```ts
// ✅ GOOD: Consistent response
export async function GET(request: Request) {
  const users = await db.user.findMany();

  return NextResponse.json({
    status: 'success',
    data: users,
    meta: {
      count: users.length,
      timestamp: new Date().toISOString()
    }
  });
}

// ✅ GOOD: Paginated response
export async function GET(request: Request) {
  const page = parseInt(request.nextUrl.searchParams.get('page') || '1');
  const limit = parseInt(request.nextUrl.searchParams.get('limit') || '20');
  const offset = (page - 1) * limit;

  const [users, total] = await Promise.all([
    db.user.findMany({ skip: offset, take: limit }),
    db.user.count()
  ]);

  return NextResponse.json({
    status: 'success',
    data: users,
    meta: {
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    }
  });
}
```

## Request Correlation

```ts
// middleware/correlation-id.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const correlationId = 
    request.headers.get('x-correlation-id') || 
    crypto.randomUUID();

  const response = NextResponse.next();
  response.headers.set('x-correlation-id', correlationId);

  return response;
}

// Include in logs
console.log(`[${correlationId}] User created:`, user);

// Client can track requests
fetch('/api/users', {
  headers: { 'x-correlation-id': myRequestId }
});
```

## Anti-Patterns

```ts
// ❌ BAD: Leaking stack traces
{
  "error": "Cannot read property 'id' of undefined at getUserData (line 42)",
  "stack": "Error: ...\nat app.js:42..."
}

// ❌ BAD: Generic error message
{
  "error": "Something went wrong"
}

// ❌ BAD: No rate limiting
// Anyone can hammer API endpoint

// ❌ BAD: Overusing 500
// Always return 500 for any error

// ❌ BAD: No validation
const user = await db.user.create(request.body);
// Raw user input!
```

## Verification Before Production

- [ ] HTTP status codes specific and appropriate
- [ ] Error responses RFC 7807 compliant
- [ ] No stack traces or sensitive data exposed
- [ ] Input validated on server side
- [ ] Input sanitized before storage
- [ ] Rate limiting configured
- [ ] Correlation IDs for request tracking
- [ ] Error messages user-friendly (not technical)
- [ ] Centralized error handler
- [ ] Response format consistent

## Integration with Project Standards

Enforces security and usability:
- S-1: No sensitive data in errors
- C-10: Input validated
- AP-8: Validation on server side

## Resources

- RFC 7807 Problem Details: https://tools.ietf.org/html/rfc7807
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- Express Rate Limiting: https://github.com/nfriedly/express-rate-limit
---

**Last Updated:** January 24, 2026
**Compatibility:** Claude Opus 4.5, Claude Code v2.x
**Status:** Production Ready

> **January 2026 Update:** This skill is compatible with Claude Opus 4.5 and Claude Code v2.x. For complex tasks, use the `effort: high` parameter for thorough analysis.
