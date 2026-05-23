---
name: rest-api-design
description: Design REST API endpoints with Zod validation and OpenAPI documentation. Use when creating new API routes, validating request/response schemas, or updating API documentation. Activates for endpoint design, schema validation, error handling, and API docs.
allowed-tools: Read,Write,Edit,Bash(npm:*,npx:*)
category: Code Quality & Testing
tags:
  - api
  - code
  - validation
  - documentation
---

# REST API Design

This skill helps you design and implement REST API endpoints following project patterns with Zod validation and OpenAPI documentation.

## When to Use

✅ **USE this skill for:**
- Creating new REST API endpoints with Next.js App Router
- Designing request/response schemas with Zod
- Implementing proper error handling and status codes
- Adding rate limiting and authentication
- Generating OpenAPI documentation

❌ **DO NOT use for:**
- GraphQL APIs → different paradigm entirely
- Cloudflare Workers → use `cloudflare-worker-dev` skill
- Supabase Edge Functions → use Supabase docs
- WebSocket/real-time APIs → different patterns

## API Route Structure

```
src/app/api/
├── auth/           # Authentication endpoints
├── check-in/       # Daily check-in CRUD
├── chat/           # AI coaching chat
├── journal/        # Journal entries
├── admin/          # Admin-only endpoints
└── health/         # Health check
```

## Standard Route Template

```typescript
// src/app/api/[feature]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { getSession } from '@/lib/auth';
import { createRateLimiter } from '@/lib/rate-limit';
import { logPHIAccess } from '@/lib/hipaa/audit';
import { db } from '@/db';

// 1. Define schemas
const RequestSchema = z.object({
  field: z.string().min(1).max(1000),
  optional: z.string().optional(),
  enumField: z.enum(['option1', 'option2']),
  number: z.number().int().positive(),
});

const ResponseSchema = z.object({
  id: z.string(),
  createdAt: z.string().datetime(),
});

// 2. Configure rate limiter
const rateLimiter = createRateLimiter({
  windowMs: 60000,    // 1 minute
  maxRequests: 30,    // 30 requests per window
  keyPrefix: 'api:feature',
});

// 3. Implement handlers
export async function GET(request: NextRequest) {
  // Auth check
  const session = await getSession();
  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  // Rate limit
  const rateLimitResult = await rateLimiter.check(session.userId);
  if (!rateLimitResult.allowed) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429, headers: rateLimitResult.headers }
    );
  }

  // Query data
  const data = await db.query.features.findMany({
    where: eq(features.userId, session.userId),
  });

  // Audit log (if PHI)
  await logPHIAccess(session.userId, 'feature', null, 'LIST');

  return NextResponse.json(data);
}

export async function POST(request: NextRequest) {
  // Auth check
  const session = await getSession();
  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  // Rate limit
  const rateLimitResult = await rateLimiter.check(session.userId);
  if (!rateLimitResult.allowed) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429, headers: rateLimitResult.headers }
    );
  }

  // Parse and validate body
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json(
      { error: 'Invalid JSON' },
      { status: 400 }
    );
  }

  const parsed = RequestSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      {
        error: 'Validation failed',
        details: parsed.error.issues.map(i => ({
          path: i.path.join('.'),
          message: i.message,
        })),
      },
      { status: 400 }
    );
  }

  // Create resource
  const [created] = await db.insert(features).values({
    id: generateId(),
    userId: session.userId,
    ...parsed.data,
    createdAt: new Date(),
  }).returning();

  // Audit log
  await logPHIAccess(session.userId, 'feature', created.id, 'CREATE');

  return NextResponse.json(created, { status: 201 });
}
```

## Zod Schema Patterns

### Basic Types

```typescript
import { z } from 'zod';

const Schema = z.object({
  // Strings
  name: z.string().min(1).max(100),
  email: z.string().email(),
  url: z.string().url(),
  uuid: z.string().uuid(),

  // Numbers
  count: z.number().int().positive(),
  rating: z.number().min(1).max(5),
  price: z.number().nonnegative(),

  // Booleans
  isActive: z.boolean(),

  // Dates
  date: z.string().datetime(),
  dateOnly: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),

  // Enums
  status: z.enum(['pending', 'approved', 'denied']),

  // Arrays
  tags: z.array(z.string()).min(1).max(10),

  // Optional fields
  notes: z.string().optional(),
  metadata: z.record(z.string()).optional(),

  // Nullable
  deletedAt: z.string().datetime().nullable(),
});
```

### Advanced Patterns

```typescript
// Discriminated unions
const EventSchema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('click'), x: z.number(), y: z.number() }),
  z.object({ type: z.literal('keypress'), key: z.string() }),
]);

// Refinements
const PasswordSchema = z.string()
  .min(12, 'Password must be at least 12 characters')
  .regex(/[A-Z]/, 'Must contain uppercase')
  .regex(/[a-z]/, 'Must contain lowercase')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character');

// Transform
const DateSchema = z.string()
  .datetime()
  .transform(str => new Date(str));

// Preprocess (coerce types)
const NumberFromString = z.preprocess(
  val => typeof val === 'string' ? parseInt(val, 10) : val,
  z.number()
);
```

### Query Parameter Validation

```typescript
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);

  const QuerySchema = z.object({
    page: z.coerce.number().int().positive().default(1),
    limit: z.coerce.number().int().min(1).max(100).default(20),
    sort: z.enum(['asc', 'desc']).default('desc'),
    status: z.enum(['all', 'active', 'archived']).optional(),
  });

  const query = QuerySchema.safeParse({
    page: searchParams.get('page'),
    limit: searchParams.get('limit'),
    sort: searchParams.get('sort'),
    status: searchParams.get('status'),
  });

  if (!query.success) {
    return NextResponse.json(
      { error: 'Invalid query parameters', details: query.error.issues },
      { status: 400 }
    );
  }

  const { page, limit, sort, status } = query.data;
  // Use validated params...
}
```

## Error Response Format

```typescript
// Standard error response
interface APIError {
  error: string;           // Human-readable message
  code?: string;           // Machine-readable code
  details?: ErrorDetail[]; // Validation details
}

interface ErrorDetail {
  path: string;
  message: string;
}

// Error responses
return NextResponse.json(
  { error: 'Not found', code: 'NOT_FOUND' },
  { status: 404 }
);

return NextResponse.json(
  {
    error: 'Validation failed',
    code: 'VALIDATION_ERROR',
    details: [
      { path: 'email', message: 'Invalid email format' },
    ],
  },
  { status: 400 }
);
```

## HTTP Status Codes

| Code | Use Case |
|------|----------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (created) |
| 204 | Successful DELETE (no content) |
| 400 | Invalid request/validation error |
| 401 | Not authenticated |
| 403 | Not authorized (authenticated but forbidden) |
| 404 | Resource not found |
| 409 | Conflict (duplicate, etc.) |
| 429 | Rate limit exceeded |
| 500 | Server error |

## OpenAPI Documentation

Update `docs/openapi.yaml` when adding endpoints:

```yaml
paths:
  /api/feature:
    get:
      summary: List features
      tags: [Features]
      security:
        - cookieAuth: []
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Feature'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create feature
      tags: [Features]
      security:
        - cookieAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateFeatureRequest'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Feature'
        '400':
          $ref: '#/components/responses/ValidationError'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  schemas:
    Feature:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        createdAt:
          type: string
          format: date-time
      required: [id, name, createdAt]

    CreateFeatureRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
      required: [name]

  responses:
    Unauthorized:
      description: Not authenticated
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: Unauthorized

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
              details:
                type: array
                items:
                  type: object
                  properties:
                    path:
                      type: string
                    message:
                      type: string
```

## Route Handler Patterns

### Dynamic Routes

```typescript
// src/app/api/feature/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;

  // Validate ID format
  if (!isValidUUID(id)) {
    return NextResponse.json(
      { error: 'Invalid ID format' },
      { status: 400 }
    );
  }

  const item = await db.query.features.findFirst({
    where: eq(features.id, id),
  });

  if (!item) {
    return NextResponse.json(
      { error: 'Not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(item);
}
```

### Pagination

```typescript
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

async function getPaginated(page: number, limit: number) {
  const offset = (page - 1) * limit;

  const [data, [{ count }]] = await Promise.all([
    db.query.features.findMany({
      limit,
      offset,
      orderBy: desc(features.createdAt),
    }),
    db.select({ count: count() }).from(features),
  ]);

  return {
    data,
    pagination: {
      page,
      limit,
      total: count,
      totalPages: Math.ceil(count / limit),
    },
  };
}
```

## References

- [Zod Documentation](https://zod.dev)
- [Next.js Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Dub.co Zod Validation](https://dub.co/blog/zod-api-validation)
