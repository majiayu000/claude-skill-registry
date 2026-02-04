---
name: api-route-creator
description: Creates Next.js 16 API routes with auth, validation, and tenant scoping. Use when creating API endpoints.
allowed-tools: Read, Write, Edit, Glob
context: fork
---

# API Route Creation Skill

## When to Use

Use this skill when creating:

- New API endpoints
- Route handlers
- Server actions

## Security Requirements (NEVER VIOLATE)

1. **Always authenticate** - Check session
2. **Always scope by tenant** - Use session.user.tenantId
3. **Always validate input** - Use Zod schemas
4. **Never trust user input** - Especially tenant_id
5. **Log sensitive ops** - Audit trail

## Template: API Route Handler

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth/config';
import { z } from 'zod';
import { db } from '@/lib/db';
import { eq, and } from 'drizzle-orm';
import { tableName } from '@/lib/db/schema';
import { auditLogger } from '@/lib/audit/logger';

// Input validation schema
const inputSchema = z.object({
  name: z.string().min(1).max(100).trim(),
  description: z.string().max(500).optional(),
});

// GET - Read (with tenant scoping)
export async function GET(request: NextRequest) {
  try {
    const session = await auth();

    // Authentication check
    if (!session?.user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Role check (if needed)
    if (!['teacher', 'tenant_admin'].includes(session.user.role)) {
      return NextResponse.json(
        { error: 'Forbidden' },
        { status: 403 }
      );
    }

    // ✅ CRITICAL: Always scope by tenant
    const data = await db.query.tableName.findMany({
      where: eq(tableName.tenantId, session.user.tenantId),
    });

    return NextResponse.json({ data });
  } catch (error) {
    console.error('[API] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// POST - Create
export async function POST(request: NextRequest) {
  try {
    const session = await auth();

    if (!session?.user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Parse and validate input
    const body = await request.json();
    const validatedInput = inputSchema.parse(body);

    // ✅ CRITICAL: Use session tenant, NEVER request body
    const [created] = await db.insert(tableName).values({
      ...validatedInput,
      tenantId: session.user.tenantId, // FROM SESSION ONLY
      createdBy: session.user.id,
    }).returning();

    // Audit log sensitive operations
    await auditLogger.log({
      action: 'CREATE',
      resourceType: 'RESOURCE_NAME',
      resourceId: created.id,
      userId: session.user.id,
      tenantId: session.user.tenantId,
    });

    return NextResponse.json({ data: created }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation error', details: error.errors },
        { status: 400 }
      );
    }
    console.error('[API] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Template: Dynamic Route ([id])

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth/config';
import { db } from '@/lib/db';
import { eq, and } from 'drizzle-orm';
import { tableName } from '@/lib/db/schema';

interface RouteContext {
  params: Promise<{ id: string }>;
}

export async function GET(
  request: NextRequest,
  context: RouteContext
) {
  try {
    const session = await auth();
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // ✅ Await params in Next.js 16
    const { id } = await context.params;

    // ✅ CRITICAL: Scope by BOTH id AND tenant
    const item = await db.query.tableName.findFirst({
      where: and(
        eq(tableName.id, id),
        eq(tableName.tenantId, session.user.tenantId)
      ),
    });

    if (!item) {
      return NextResponse.json({ error: 'Not found' }, { status: 404 });
    }

    return NextResponse.json({ data: item });
  } catch (error) {
    console.error('[API] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Error Response Format

```typescript
// Standard error responses (FERPA-safe - no data leakage)
{ error: 'Unauthorized' }           // 401 - Not authenticated
{ error: 'Forbidden' }              // 403 - Wrong role
{ error: 'Not found' }              // 404 - Doesn't exist or wrong tenant
{ error: 'Validation error', details: [...] }  // 400 - Bad input
{ error: 'Internal server error' }  // 500 - Something broke

// ❌ NEVER expose internal details
{ error: `Item ${id} not found in tenant ${tenantId}` }  // WRONG!
```

## Role Hierarchy

| Role           | Can Access                       |
| -------------- | -------------------------------- |
| student        | Own data, joined assistants      |
| teacher        | Own assistants, class students   |
| tenant_admin   | All tenant data, user management |
| platform_admin | Everything (cross-tenant)        |

## Checklist

- [ ] Session authentication
- [ ] Role-based authorization
- [ ] Tenant scoping on ALL queries
- [ ] Input validation with Zod
- [ ] Params awaited (Next.js 16)
- [ ] FERPA-safe error messages
- [ ] Audit logging for sensitive ops
- [ ] TypeScript types complete
