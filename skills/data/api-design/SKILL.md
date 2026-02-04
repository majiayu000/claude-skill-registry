---
name: api-design
description: "REST and GraphQL API design patterns. Covers endpoint structure, versioning, authentication, error handling, rate limiting, and OpenAPI documentation."
version: 1.0.0
triggers:
  - api design
  - rest api
  - graphql
  - endpoint
  - api routes
  - openapi
---

# API Design Skill

Design robust, scalable APIs following industry best practices for REST and GraphQL.

## REST API Patterns

### Resource Naming

```
# Good - Nouns, plural, hierarchical
GET    /api/v1/users
GET    /api/v1/users/{id}
GET    /api/v1/users/{id}/posts
POST   /api/v1/users
PUT    /api/v1/users/{id}
PATCH  /api/v1/users/{id}
DELETE /api/v1/users/{id}

# Bad
GET /api/getUsers          # Verb in URL
GET /api/user              # Singular
POST /api/createUser       # Action in URL
```

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read | Yes | Yes |
| POST | Create | No | No |
| PUT | Replace | Yes | No |
| PATCH | Update | Yes | No |
| DELETE | Remove | Yes | No |

### Response Codes

```typescript
// Success
200 OK              // GET, PUT, PATCH success
201 Created         // POST success (include Location header)
204 No Content      // DELETE success

// Client Errors
400 Bad Request     // Invalid input
401 Unauthorized    // No/invalid auth
403 Forbidden       // Valid auth, no permission
404 Not Found       // Resource doesn't exist
409 Conflict        // State conflict (duplicate)
422 Unprocessable   // Validation error
429 Too Many Reqs   // Rate limited

// Server Errors
500 Internal Error  // Unexpected error
503 Unavailable     // Maintenance/overload
```

### Standard Response Format

```typescript
// Success response
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "name": "Frank",
      "email": "frank@frankx.ai"
    }
  },
  "meta": {
    "timestamp": "2026-01-23T12:00:00Z"
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      { "field": "email", "message": "Required field" }
    ]
  }
}

// Paginated response
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "perPage": 20,
    "totalPages": 5
  },
  "links": {
    "self": "/api/v1/users?page=1",
    "next": "/api/v1/users?page=2",
    "last": "/api/v1/users?page=5"
  }
}
```

## Next.js API Routes

### Route Handler Pattern

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get('page') ?? '1');
  const limit = parseInt(searchParams.get('limit') ?? '20');

  const users = await db.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });

  return NextResponse.json({
    data: users,
    meta: { page, limit },
  });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validated = CreateUserSchema.parse(body);

    const user = await db.user.create({ data: validated });

    return NextResponse.json(
      { data: user },
      { status: 201 }
    );
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: { code: 'VALIDATION_ERROR', details: error.errors } },
        { status: 422 }
      );
    }
    throw error;
  }
}
```

### Dynamic Route

```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

type Params = { params: Promise<{ id: string }> };

export async function GET(request: NextRequest, { params }: Params) {
  const { id } = await params;

  const user = await db.user.findUnique({ where: { id } });

  if (!user) {
    return NextResponse.json(
      { error: { code: 'NOT_FOUND', message: 'User not found' } },
      { status: 404 }
    );
  }

  return NextResponse.json({ data: user });
}
```

## Authentication Patterns

### JWT Middleware

```typescript
// lib/auth.ts
import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

export async function authMiddleware(request: NextRequest) {
  const token = request.headers.get('Authorization')?.replace('Bearer ', '');

  if (!token) {
    return NextResponse.json(
      { error: { code: 'UNAUTHORIZED', message: 'No token provided' } },
      { status: 401 }
    );
  }

  try {
    const { payload } = await jwtVerify(
      token,
      new TextEncoder().encode(process.env.JWT_SECRET)
    );
    return payload;
  } catch {
    return NextResponse.json(
      { error: { code: 'UNAUTHORIZED', message: 'Invalid token' } },
      { status: 401 }
    );
  }
}
```

## Rate Limiting

```typescript
// lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'), // 10 requests per 10 seconds
});

export async function rateLimitMiddleware(request: NextRequest) {
  const ip = request.ip ?? '127.0.0.1';
  const { success, limit, remaining, reset } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: { code: 'RATE_LIMITED', message: 'Too many requests' } },
      {
        status: 429,
        headers: {
          'X-RateLimit-Limit': limit.toString(),
          'X-RateLimit-Remaining': remaining.toString(),
          'X-RateLimit-Reset': reset.toString(),
        },
      }
    );
  }
}
```

## API Versioning

```
# URL versioning (recommended)
/api/v1/users
/api/v2/users

# Header versioning
Accept: application/vnd.frankx.v1+json

# Query parameter (avoid)
/api/users?version=1
```

## OpenAPI Documentation

```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: FrankX API
  version: 1.0.0
  description: API for FrankX creator platform

paths:
  /api/v1/users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
          format: email
```

## Anti-Patterns

❌ Verbs in URLs (`/getUser`, `/createPost`)
❌ Inconsistent naming (mix of snake_case and camelCase)
❌ Returning 200 for errors with error in body
❌ No pagination for list endpoints
❌ Exposing internal IDs/structure
❌ No rate limiting

✅ Noun-based resource URLs
✅ Consistent response format
✅ Proper HTTP status codes
✅ Pagination with cursors or pages
✅ UUIDs for public IDs
✅ Rate limiting on all endpoints
