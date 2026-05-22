---
name: api-handler
description: StepLeague API route pattern using withApiHandler wrapper. Use when creating or modifying any API route in the /api directory. Keywords: API, route, endpoint, handler, auth, POST, GET, PUT, DELETE, validation.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.1"
  project: "stepleague"
---

# API Handler Skill

## Overview

Use `withApiHandler` for all API routes. It eliminates boilerplate and ensures consistent auth, validation, and error handling.

---

## Basic Usage

```typescript
import { withApiHandler } from "@/lib/api/handler";
import { z } from "zod";

const mySchema = z.object({
  name: z.string(),
  count: z.number().optional(),
});

export const POST = withApiHandler({
  auth: 'required',
  schema: mySchema,
}, async ({ user, body, adminClient }) => {
  const { data } = await adminClient
    .from("table")
    .insert({ ...body, user_id: user.id })
    .select()
    .single();
  
  return { success: true, data };
});
```

---

## Auth Levels

| Level | Description | Context Provided |
|-------|-------------|------------------|
| `'none'` | No auth required | `user` may be null |
| `'required'` | Must be logged in | `user` guaranteed |
| `'superadmin'` | Site-wide superadmin | `user` guaranteed, verified superadmin |
| `'league_member'` | Must be league member | `user`, `membership` |
| `'league_admin'` | Must be admin or owner | `user`, `membership` (admin/owner role) |
| `'league_owner'` | Must be owner | `user`, `membership` (owner role) |

### League Auth Examples

```typescript
// Any league member can access
export const GET = withApiHandler({
  auth: 'league_member',
}, async ({ user, membership }) => {
  // membership.role is 'owner', 'admin', or 'member'
  return { role: membership?.role };
});

// Only admins and owners
export const PUT = withApiHandler({
  auth: 'league_admin',
  schema: updateSchema,
}, async ({ user, body, adminClient, membership }) => {
  // membership.role is guaranteed 'admin' or 'owner'
  return { updated: true };
});
```

### League ID Resolution

For league auth, the handler looks for `league_id` in this order:
1. Request body (`{ league_id: "..." }`)
2. URL params (`/api/leagues/[id]`)
3. Query params (`?league_id=...`)

---

## Handler Context

The handler function receives:

```typescript
interface HandlerContext<T> {
  user: User | null;           // Authenticated user
  body: T;                     // Parsed & validated request body
  adminClient: SupabaseClient; // Admin client (bypasses RLS)
  request: Request;            // Original request
  params: Record<string, string>; // URL params (e.g., { id: 'xxx' })
  membership: Membership | null;  // For league_* auth levels
}
```

---

## Schema Validation

Use Zod for request validation:

```typescript
const createSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  is_active: z.boolean().default(true),
  league_id: z.string().uuid(),
});

export const POST = withApiHandler({
  auth: 'required',
  schema: createSchema,
}, async ({ body }) => {
  // body is fully typed and validated
  console.log(body.name); // string
  console.log(body.is_active); // boolean (defaulted to true if not provided)
});
```

### Validation Errors

If validation fails, the handler automatically returns:

```json
{
  "error": "Validation failed: name: Required, league_id: Invalid uuid"
}
```

---

## Returning Responses

### Return Object (Auto-wrapped)

```typescript
return { success: true, data };
// Becomes: Response with JSON { success: true, data }
```

### Return Response Directly

```typescript
import { json, badRequest, forbidden } from "@/lib/api";

// Custom status or headers
return json({ data }, { status: 201 });

// Error responses
return badRequest("Invalid input");
return forbidden("Not allowed");
```

---

## Error Handling

Errors thrown in the handler are caught and logged:

```typescript
export const POST = withApiHandler({
  auth: 'required',
}, async ({ adminClient }) => {
  const { data, error } = await adminClient.from("table").insert({});
  
  if (error) {
    // Use AppError for typed errors
    throw new AppError({
      code: ErrorCode.DB_INSERT_FAILED,
      message: error.message,
      context: { table: 'table' },
    });
  }
  
  return { success: true };
});
```

Reference the `error-handling` skill for more on AppError.

---

## Complete Example

```typescript
// src/app/api/leagues/[id]/members/route.ts

import { withApiHandler } from "@/lib/api/handler";
import { z } from "zod";
import { AppError, ErrorCode } from "@/lib/errors";

const addMemberSchema = z.object({
  user_id: z.string().uuid(),
  role: z.enum(['member', 'admin']).default('member'),
});

// GET - List members (any league member can view)
export const GET = withApiHandler({
  auth: 'league_member',
}, async ({ params, adminClient }) => {
  const { data } = await adminClient
    .from("memberships")
    .select("*, users(*)")
    .eq("league_id", params.id);
  
  return { members: data };
});

// POST - Add member (only admins/owners)
export const POST = withApiHandler({
  auth: 'league_admin',
  schema: addMemberSchema,
}, async ({ params, body, adminClient }) => {
  const { data, error } = await adminClient
    .from("memberships")
    .insert({
      league_id: params.id,
      user_id: body.user_id,
      role: body.role,
    })
    .select()
    .single();
  
  if (error) {
    throw new AppError({
      code: ErrorCode.DB_INSERT_FAILED,
      message: "Failed to add member",
      context: { error: error.message },
    });
  }
  
  return { success: true, member: data };
});
```

---

## Legacy Pattern

For existing routes not yet migrated:

```typescript
import { createServerSupabaseClient, createAdminClient } from "@/lib/supabase/server";
import { json, badRequest, unauthorized } from "@/lib/api";

export async function GET(request: Request) {
  const supabase = await createServerSupabaseClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return unauthorized();

  const adminClient = createAdminClient();
  const { data } = await adminClient.from("table").select("*");
  return json({ data });
}
```

**Rule:** Use `withApiHandler` for all NEW routes. Migrate legacy routes only when modifying them for other reasons.

---

## Reference Files

| File | Purpose |
|------|---------|
| `src/lib/api/handler.ts` | The withApiHandler implementation |
| `src/lib/api.ts` | Response helpers (json, badRequest, etc.) |

---

## Related Skills

- `supabase-patterns` - Database operations with adminClient
- `error-handling` - Error codes and AppError usage
- `architecture-philosophy` - Why we use this pattern
