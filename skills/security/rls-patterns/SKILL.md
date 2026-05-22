---
name: rls-patterns
description: Row Level Security patterns for database operations. Use when writing Prisma/database code, creating API routes that access data, or implementing webhooks. Enforces withUserContext, withAdminContext, or withSystemContext helpers. NEVER use direct prisma calls.
---

# RLS Patterns Skill

## Purpose

Enforce Row Level Security (RLS) patterns for all database operations. This skill ensures data isolation and prevents cross-user data access at the database level.

## When This Skill Applies

Invoke this skill when:

- Writing any Prisma database query
- Creating or modifying API routes that access the database
- Implementing webhook handlers that write to the database
- Working with user data, payments, subscriptions, or enrollments
- Accessing admin-only tables (disputes, webhook_events)

## Critical Rules

### NEVER Do This

```typescript
// ❌ FORBIDDEN - Direct Prisma calls bypass RLS
const user = await prisma.user.findUnique({ where: { user_id } });

// ❌ FORBIDDEN - No context set
const payments = await prisma.payments.findMany();
```

**ESLint will block direct Prisma calls.** See `eslint.config.mjs` for enforcement rules.

### ALWAYS Do This

```typescript
import {
  withUserContext,
  withAdminContext,
  withSystemContext,
} from "@/lib/rls-context";

// ✅ CORRECT - User context for user operations
const user = await withUserContext(prisma, userId, async (client) => {
  return client.user.findUnique({ where: { user_id: userId } });
});

// ✅ CORRECT - Admin context for admin operations
const webhooks = await withAdminContext(prisma, userId, async (client) => {
  return client.webhook_events.findMany();
});

// ✅ CORRECT - System context for webhooks/background tasks
const event = await withSystemContext(prisma, "webhook", async (client) => {
  return client.webhook_events.create({ data: eventData });
});
```

## Context Helper Reference

### `withUserContext(prisma, userId, callback)`

**Use for**: All user-facing operations

- User profile access
- Payment history
- Subscription management
- Course enrollments

```typescript
const payments = await withUserContext(prisma, userId, async (client) => {
  return client.payments.findMany({ where: { user_id: userId } });
});
```

### `withAdminContext(prisma, userId, callback)`

**Use for**: Admin-only operations (requires admin role in `user_roles` table)

- Viewing all webhook events
- Managing disputes
- Accessing payment failures

```typescript
const disputes = await withAdminContext(prisma, adminUserId, async (client) => {
  return client.disputes.findMany();
});
```

### `withSystemContext(prisma, contextType, callback)`

**Use for**: Webhooks and background jobs

- Stripe webhook handlers
- Clerk webhook handlers
- Background job processing

```typescript
// Stripe webhook handler
await withSystemContext(prisma, "webhook", async (client) => {
  await client.payments.create({ data: paymentData });
});
```

## Admin Pages: Force Dynamic Rendering

**CRITICAL**: Admin pages using RLS queries MUST force runtime rendering:

```typescript
// app/admin/some-page/page.tsx
import { withAdminContext } from "@/lib/rls-context";
import { prisma } from "@/lib/prisma";

// REQUIRED - RLS context unavailable at build time
export const dynamic = "force-dynamic";

async function getAdminData() {
  return await withAdminContext(prisma, userId, async (client) => {
    return client.someTable.findMany();
  });
}
```

Without `export const dynamic = 'force-dynamic'`, Next.js will try to pre-render at build time, causing "permission denied" errors.

## Protected Tables

### User Data Tables (User Isolation)

| Table               | Policy Type    | Access                 |
| ------------------- | -------------- | ---------------------- |
| `user`              | User isolation | Own data only          |
| `payments`          | User isolation | Own payments only      |
| `subscriptions`     | User isolation | Own subscriptions only |
| `invoices`          | User isolation | Own invoices only      |
| `course_enrollment` | User isolation | Own enrollments only   |

### Admin/System Tables (Role-Based)

| Table                 | Policy Type  | Access                   |
| --------------------- | ------------ | ------------------------ |
| `webhook_events`      | Admin+System | Admins and webhooks only |
| `disputes`            | Admin only   | Admins only              |
| `payment_failures`    | Admin only   | Admins only              |
| `trial_notifications` | Admin+System | Admins and system only   |

## Testing Requirements

Always test with `{PROJECT}_app_user` role (not `{PROJECT}_user` superuser):

```bash
# Basic RLS functionality test
node scripts/test-rls-phase3-simple.js

# Comprehensive security validation
cat scripts/rls-phase4-final-validation.sql | \
  docker exec -i {PROJECT_NAME}-postgres-1 psql -U {PROJECT}_app_user -d {PROJECT}_dev
```

## Common Patterns

### API Route with User Context

```typescript
// app/api/user/payments/route.ts
import { NextResponse } from "next/server";
import { requireAuth } from "@/lib/auth";
import { withUserContext } from "@/lib/rls-context";
import { prisma } from "@/lib/prisma";

export async function GET() {
  const { userId } = await requireAuth();

  const payments = await withUserContext(prisma, userId, async (client) => {
    return client.payments.findMany({
      where: { user_id: userId },
      orderBy: { created_at: "desc" },
    });
  });

  return NextResponse.json(payments);
}
```

### Webhook Handler with System Context

```typescript
// app/api/webhooks/stripe/route.ts
import { withSystemContext } from "@/lib/rls-context";
import { prisma } from "@/lib/prisma";

export async function POST(req: Request) {
  // Verify webhook signature first...

  await withSystemContext(prisma, "webhook", async (client) => {
    await client.webhook_events.create({
      data: {
        event_type: event.type,
        payload: event.data,
        processed_at: new Date(),
      },
    });
  });

  return new Response("OK", { status: 200 });
}
```

## Authoritative References

- **Implementation Guide**: `docs/database/RLS_IMPLEMENTATION_GUIDE.md`
- **Policy Catalog**: `docs/database/RLS_POLICY_CATALOG.md`
- **Migration SOP**: `docs/database/RLS_DATABASE_MIGRATION_SOP.md`
- **ESLint Rules**: `eslint.config.mjs` (direct Prisma call enforcement)
- **RLS Context**: `lib/rls-context.ts`
