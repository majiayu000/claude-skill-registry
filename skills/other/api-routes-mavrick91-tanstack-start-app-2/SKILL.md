---
name: api-routes
description: Generate secure TanStack Start API routes with authentication, rate limiting, validation, and proper error handling. Use when creating API endpoints, REST resources, or backend logic.
---

# API Route Generator

Create production-ready API endpoints following this project's security-first patterns.

## Quick Start Template

```typescript
import { createFileRoute } from '@tanstack/react-router'
import { eq } from 'drizzle-orm'
import { db } from '@/db'
import { tableName } from '@/db/schema'
import {
  errorResponse,
  requireAuth,
  simpleErrorResponse,
  successResponse,
} from '@/lib/api'
import { checkRateLimit } from '@/lib/rate-limit'

export const Route = createFileRoute('/api/resource')({
  server: {
    handlers: {
      GET: async ({ request }) => {
        try {
          // 1. Rate limiting
          const rateLimit = await checkRateLimit(request, 'api')
          if (!rateLimit.allowed) {
            return new Response(
              JSON.stringify({ error: 'Too many requests' }),
              {
                status: 429,
                headers: { 'Retry-After': String(rateLimit.retryAfter) },
              },
            )
          }

          // 2. Authentication
          const auth = await requireAuth(request)
          if (!auth.success) return auth.response

          // 3. Business logic
          const items = await db.select().from(tableName)

          // 4. Success response
          return successResponse({ items })
        } catch (error) {
          return errorResponse('Failed to fetch', error)
        }
      },
    },
  },
})
```

## Authentication Patterns

### User Authentication (any logged-in user)

```typescript
const auth = await requireAuth(request)
if (!auth.success) return auth.response
const user = auth.user // { id, email, role }
```

### Admin Authentication

```typescript
const auth = await requireAdmin(request)
if (!auth.success) return auth.response
// Only admins reach here
```

### Optional Authentication (public with user context)

```typescript
import { validateSession } from '@/lib/auth'

const session = await validateSession(request)
const userId = session.success ? session.user.id : null
// Proceed with or without user
```

## Response Helpers

```typescript
import { successResponse, simpleErrorResponse, errorResponse } from '@/lib/api'

// Success with data (200)
return successResponse({ items, total })

// Success with custom status
return successResponse({ item }, 201)

// Validation/client error (400)
return simpleErrorResponse('Email is required')
return simpleErrorResponse('Not found', 404)

// Server error (logs stack in dev)
return errorResponse('Database error', error, 500)
```

## Input Validation

### Required Fields

```typescript
const body = await request.json()
const { email, name, password } = body

if (!email?.trim()) {
  return simpleErrorResponse('Email is required')
}

if (!password || password.length < 8) {
  return simpleErrorResponse('Password must be at least 8 characters')
}
```

### Localized String Validation

```typescript
type LocalizedString = { en: string; fr?: string; id?: string }

if (!name || typeof name !== 'object' || !('en' in name) || !name.en?.trim()) {
  return simpleErrorResponse('Name must have a non-empty "en" property')
}
```

### URL Parameter Validation

```typescript
// For /api/resource/$resourceId routes
const { resourceId } = params

if (!resourceId || !isValidUUID(resourceId)) {
  return simpleErrorResponse('Invalid resource ID', 400)
}
```

## CRUD Operations

### List with Pagination, Filtering, Sorting

```typescript
import { and, asc, count, desc, eq, ilike, SQL } from 'drizzle-orm'

GET: async ({ request }) => {
  const auth = await requireAuth(request)
  if (!auth.success) return auth.response

  const url = new URL(request.url)

  // Pagination
  const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10))
  const limit = Math.min(
    100,
    Math.max(1, parseInt(url.searchParams.get('limit') || '10', 10)),
  )

  // Filtering
  const search = url.searchParams.get('q') || ''
  const status = url.searchParams.get('status') as 'active' | 'draft' | null

  // Sorting
  const sortKey = url.searchParams.get('sort') || 'createdAt'
  const sortOrder = url.searchParams.get('order') === 'asc' ? 'asc' : 'desc'

  // Build conditions
  const conditions: SQL[] = []
  if (search) {
    conditions.push(ilike(tableName.name, `%${search}%`) as SQL)
  }
  if (status) {
    conditions.push(eq(tableName.status, status))
  }
  const whereClause = conditions.length > 0 ? and(...conditions) : undefined

  // Get total count
  const [{ total }] = await db
    .select({ total: count() })
    .from(tableName)
    .where(whereClause)

  // Get paginated items
  const sortColumn =
    {
      name: tableName.name,
      status: tableName.status,
      createdAt: tableName.createdAt,
    }[sortKey] || tableName.createdAt

  const offset = (page - 1) * limit
  const items = await db
    .select()
    .from(tableName)
    .where(whereClause)
    .orderBy(sortOrder === 'asc' ? asc(sortColumn) : desc(sortColumn))
    .limit(limit)
    .offset(offset)

  return successResponse({
    items,
    total,
    page,
    limit,
    totalPages: Math.ceil(total / limit),
  })
}
```

### Create with Transaction

```typescript
POST: async ({ request }) => {
  const auth = await requireAdmin(request)
  if (!auth.success) return auth.response

  const body = await request.json()

  // Validate
  if (!body.name?.en?.trim()) {
    return simpleErrorResponse('Name is required')
  }

  try {
    const result = await db.transaction(async (tx) => {
      // Create main record
      const [item] = await tx
        .insert(tableName)
        .values({
          name: body.name,
          status: body.status || 'draft',
        })
        .returning()

      // Create related records
      if (body.variants?.length) {
        await tx.insert(variants).values(
          body.variants.map((v, i) => ({
            itemId: item.id,
            title: v.title,
            position: i,
          })),
        )
      }

      return item
    })

    return successResponse({ item: result }, 201)
  } catch (error) {
    return errorResponse('Failed to create', error)
  }
}
```

### Update (PATCH)

```typescript
PATCH: async ({ request, params }) => {
  const auth = await requireAdmin(request)
  if (!auth.success) return auth.response

  const { resourceId } = params
  const body = await request.json()

  // Check exists
  const [existing] = await db
    .select()
    .from(tableName)
    .where(eq(tableName.id, resourceId))
    .limit(1)

  if (!existing) {
    return simpleErrorResponse('Not found', 404)
  }

  // Update
  const [updated] = await db
    .update(tableName)
    .set({
      ...body,
      updatedAt: new Date(),
    })
    .where(eq(tableName.id, resourceId))
    .returning()

  return successResponse({ item: updated })
}
```

### Delete

```typescript
DELETE: async ({ request, params }) => {
  const auth = await requireAdmin(request)
  if (!auth.success) return auth.response

  const { resourceId } = params

  await db.delete(tableName).where(eq(tableName.id, resourceId))

  return successResponse({ deleted: true })
}
```

## Avoiding N+1 Queries

```typescript
// BAD: N+1 queries
const items = await db.select().from(orders)
for (const item of items) {
  const orderItems = await db
    .select()
    .from(orderItems)
    .where(eq(orderItems.orderId, item.id))
  item.items = orderItems
}

// GOOD: Batch with Map
const items = await db.select().from(orders)
const itemIds = items.map((i) => i.id)

// Single query for all related data
const allOrderItems = await db.select().from(orderItems)

// Build lookup map
const itemsByOrderId = new Map<string, typeof allOrderItems>()
for (const oi of allOrderItems) {
  const existing = itemsByOrderId.get(oi.orderId) || []
  existing.push(oi)
  itemsByOrderId.set(oi.orderId, existing)
}

// Use map
const itemsWithData = items.map((item) => ({
  ...item,
  orderItems: itemsByOrderId.get(item.id) || [],
}))
```

## Rate Limiting

```typescript
import { checkRateLimit } from '@/lib/rate-limit'

// Available tiers:
// 'auth': 5 requests per 15 minutes (login attempts)
// 'api': 100 requests per minute (general API)
// 'webhook': 50 requests per minute (payment webhooks)

const rateLimit = await checkRateLimit(request, 'api')
if (!rateLimit.allowed) {
  return new Response(JSON.stringify({ error: 'Too many requests' }), {
    status: 429,
    headers: { 'Retry-After': String(rateLimit.retryAfter) },
  })
}
```

## Webhook Handlers

```typescript
// src/routes/api/webhooks/stripe.ts
POST: async ({ request }) => {
  // Rate limit webhooks
  const rateLimit = await checkRateLimit(request, 'webhook')
  if (!rateLimit.allowed) {
    return new Response('Rate limited', { status: 429 })
  }

  // Verify signature
  const sig = request.headers.get('stripe-signature')
  if (!sig) {
    return new Response('Missing signature', { status: 400 })
  }

  const body = await request.text()

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!,
    )

    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSuccess(event.data.object)
        break
      case 'payment_intent.payment_failed':
        await handlePaymentFailed(event.data.object)
        break
    }

    return new Response('OK', { status: 200 })
  } catch (error) {
    console.error('Webhook error:', error)
    return new Response('Webhook error', { status: 400 })
  }
}
```

## Security Checklist

- [ ] Rate limiting applied
- [ ] Authentication checked
- [ ] Input validated
- [ ] SQL injection prevented (using Drizzle parameterized queries)
- [ ] Sensitive data not exposed in responses
- [ ] Error messages don't leak internals
- [ ] CSRF protection for state-changing operations

## File Naming

| Route                           | File                                           |
| ------------------------------- | ---------------------------------------------- |
| `GET /api/products`             | `src/routes/api/products/index.ts`             |
| `GET /api/products/:id`         | `src/routes/api/products/$productId.ts`        |
| `POST /api/products/:id/images` | `src/routes/api/products/$productId/images.ts` |
| `POST /api/webhooks/stripe`     | `src/routes/api/webhooks/stripe.ts`            |

## See Also

- `src/routes/api/products/index.ts` - Full CRUD example
- `src/routes/api/orders/$orderId.ts` - Single resource
- `src/routes/api/checkout/` - Complex flow
- `src/lib/api.ts` - Response helpers
- `src/lib/rate-limit.ts` - Rate limiting
