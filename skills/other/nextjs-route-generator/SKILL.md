---
name: nextjs-route-generator
description: Scaffold Next.js App Router API routes with Zod validation, error handling, and TypeScript types. Use when asked to create API routes, REST endpoints, CRUD operations, or scaffold a Next.js backend.
---

# Next.js Route Generator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Generation Process

1. Determine the route path and HTTP methods needed
2. Generate route handler with proper exports (GET, POST, PUT, PATCH, DELETE)
3. Add Zod schemas for request validation
4. Include structured error handling
5. Export TypeScript types for frontend consumption

## Route Structure

Place routes in `app/api/` following Next.js App Router conventions:
- `app/api/users/route.ts` → `/api/users`
- `app/api/users/[id]/route.ts` → `/api/users/:id`
- `app/api/posts/[postId]/comments/route.ts` → `/api/posts/:postId/comments`

## Standard Route Template

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

// ============ Schemas ============

const createSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
});

const updateSchema = createSchema.partial();

const querySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  search: z.string().optional(),
});

// ============ Types ============

export type CreateInput = z.infer<typeof createSchema>;
export type UpdateInput = z.infer<typeof updateSchema>;
export type QueryParams = z.infer<typeof querySchema>;

// ============ Helpers ============

function errorResponse(message: string, status: number, details?: unknown) {
  return NextResponse.json(
    { error: message, details },
    { status }
  );
}

function parseSearchParams(request: NextRequest, schema: z.ZodSchema) {
  const params = Object.fromEntries(request.nextUrl.searchParams);
  return schema.safeParse(params);
}

// ============ Handlers ============

export async function GET(request: NextRequest) {
  const parsed = parseSearchParams(request, querySchema);

  if (!parsed.success) {
    return errorResponse('Invalid query parameters', 400, parsed.error.flatten());
  }

  const { page, limit, search } = parsed.data;

  // TODO: Implement data fetching
  const items = [];
  const total = 0;

  return NextResponse.json({
    data: items,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  });
}

export async function POST(request: NextRequest) {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    return errorResponse('Invalid JSON body', 400);
  }

  const parsed = createSchema.safeParse(body);

  if (!parsed.success) {
    return errorResponse('Validation failed', 400, parsed.error.flatten());
  }

  // TODO: Implement creation logic
  const created = { id: 1, ...parsed.data };

  return NextResponse.json({ data: created }, { status: 201 });
}
```

## Dynamic Route Template

For `[id]` routes (`app/api/resource/[id]/route.ts`):

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const paramsSchema = z.object({
  id: z.coerce.number().int().positive(),
});

const updateSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  email: z.string().email().optional(),
});

type RouteContext = {
  params: Promise<{ id: string }>;
};

export async function GET(request: NextRequest, context: RouteContext) {
  const params = await context.params;
  const parsed = paramsSchema.safeParse(params);

  if (!parsed.success) {
    return NextResponse.json({ error: 'Invalid ID' }, { status: 400 });
  }

  // TODO: Fetch by ID
  const item = null;

  if (!item) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  return NextResponse.json({ data: item });
}

export async function PUT(request: NextRequest, context: RouteContext) {
  const params = await context.params;
  const parsedParams = paramsSchema.safeParse(params);

  if (!parsedParams.success) {
    return NextResponse.json({ error: 'Invalid ID' }, { status: 400 });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'Invalid JSON' }, { status: 400 });
  }

  const parsedBody = updateSchema.safeParse(body);

  if (!parsedBody.success) {
    return NextResponse.json(
      { error: 'Validation failed', details: parsedBody.error.flatten() },
      { status: 400 }
    );
  }

  // TODO: Update logic
  const updated = { id: parsedParams.data.id, ...parsedBody.data };

  return NextResponse.json({ data: updated });
}

export async function DELETE(request: NextRequest, context: RouteContext) {
  const params = await context.params;
  const parsed = paramsSchema.safeParse(params);

  if (!parsed.success) {
    return NextResponse.json({ error: 'Invalid ID' }, { status: 400 });
  }

  // TODO: Delete logic

  return new NextResponse(null, { status: 204 });
}
```

## Middleware Pattern

For routes requiring authentication:

```typescript
import { auth } from '@/lib/auth';

export async function GET(request: NextRequest) {
  const session = await auth();

  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Proceed with authenticated request
}
```

## Error Handling Patterns

### Database Errors
```typescript
import { Prisma } from '@prisma/client';

try {
  // Database operation
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.code === 'P2002') {
      return errorResponse('Resource already exists', 409);
    }
    if (error.code === 'P2025') {
      return errorResponse('Resource not found', 404);
    }
  }
  throw error; // Re-throw unexpected errors
}
```

### Global Error Boundary
Unexpected errors are caught by Next.js and return 500. Log them in production:
```typescript
console.error('Unhandled API error:', error);
```

## Response Conventions

- **200**: Successful GET/PUT/PATCH
- **201**: Successful POST (resource created)
- **204**: Successful DELETE (no content)
- **400**: Bad request / validation error
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not found
- **409**: Conflict (duplicate)
- **500**: Internal server error

## Integration Check

After generating a route, verify that: the Zod schema matches the expected request body, the response type is explicitly defined, error responses use consistent format across all generated routes, and the route handles all specified HTTP methods. If generating multiple routes, ensure shared types are extracted to a common types file.

## Asset

See `assets/route-template/route.ts` for a minimal starter template.
