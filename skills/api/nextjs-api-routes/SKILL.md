---
name: nextjs-api-routes
description: Apply when building API endpoints in Next.js App Router using Route Handlers.
version: 1.0.0
tokens: ~650
confidence: high
sources:
  - https://nextjs.org/docs/app/building-your-application/routing/route-handlers
  - https://nextjs.org/docs/app/api-reference/functions/next-request
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [nextjs, api, routes, backend]
---

## When to Use

Apply when building API endpoints in Next.js App Router using Route Handlers.

## Patterns

### Pattern 1: Basic Route Handler
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/routing/route-handlers
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const users = await db.users.findMany();
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const user = await db.users.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

### Pattern 2: Dynamic Route Parameters
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/routing/route-handlers
// app/api/users/[id]/route.ts
interface RouteParams {
  params: Promise<{ id: string }>;
}

export async function GET(request: NextRequest, { params }: RouteParams) {
  const { id } = await params;
  const user = await db.users.findUnique({ where: { id } });

  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
  return NextResponse.json(user);
}

export async function DELETE(request: NextRequest, { params }: RouteParams) {
  const { id } = await params;
  await db.users.delete({ where: { id } });
  return new NextResponse(null, { status: 204 });
}
```

### Pattern 3: Query Parameters & Headers
```typescript
// Source: https://nextjs.org/docs/app/api-reference/functions/next-request
export async function GET(request: NextRequest) {
  // Query params
  const searchParams = request.nextUrl.searchParams;
  const page = parseInt(searchParams.get('page') || '1');
  const limit = parseInt(searchParams.get('limit') || '10');

  // Headers
  const authHeader = request.headers.get('authorization');
  if (!authHeader) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const data = await db.items.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });

  return NextResponse.json({ data, page, limit });
}
```

### Pattern 4: Error Handling Pattern
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/routing/route-handlers
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validation
    const result = schema.safeParse(body);
    if (!result.success) {
      return NextResponse.json(
        { error: 'Validation failed', details: result.error.flatten() },
        { status: 400 }
      );
    }

    const item = await db.items.create({ data: result.data });
    return NextResponse.json(item, { status: 201 });

  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### Pattern 5: CORS Headers
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/routing/route-handlers
export async function OPTIONS() {
  return new NextResponse(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
```

## Anti-Patterns

- **Business logic in route handlers** - Extract to service layer
- **No error handling** - Always wrap in try/catch
- **Returning errors as 200** - Use appropriate status codes
- **No input validation** - Always validate with Zod

## Verification Checklist

- [ ] All routes have error handling
- [ ] Input validated before processing
- [ ] Correct HTTP status codes used
- [ ] Auth checked where required
- [ ] CORS configured if needed
