---
name: prisma-nextjs16
description: Best practices for using Prisma ORM with Next.js 16 App Router and Neon serverless database. Use this skill when writing database queries, mutations, or configuring Prisma client to ensure connection limits, caching, and serverless compatibility are handled correctly.
---

# Prisma ORM with Next.js 16 (App Router) & Neon

This skill defines the mandatory patterns for using Prisma implementation in this project.

## 1. Core Architecture

- **Client Location:** `app/_lib/prisma.ts` (Singleton pattern)
- **Database:** Neon Serverless PostgreSQL
- **Adapter:** `@prisma/adapter-neon` (HTTP-based for serverless)
- **Schema:** `prisma/schema.prisma`

## 2. Critical Rules regarding AI Implementation

### Connection Management (The Singleton Rule)

**NEVER** instantiate `new PrismaClient()` in standard files.
**ALWAYS** import the shared instance from `@/app/_lib/prisma`.

```typescript
// ✅ CORRECT
import { prisma } from "@/app/_lib/prisma";

// ❌ WRONG (Causes connection exhaustion)
const prisma = new PrismaClient();
```

### Server Components (Data Fetching)

- **Direct Access:** Fetch data directly in Server Components using `prisma`.
- **No API Routes:** Do not create `api/routes` for data needed in Server Components.
- **Select Fields:** Always use `select` to retrieve only necessary fields (reduces payload).
- **Memoization:** If the same query is needed in multiple components in the same render (e.g., Layout + Page), wrap the fetcher in React's `cache()`.

```typescript
// app/_lib/repositories.ts
import { cache } from "react";
import { prisma } from "@/app/_lib/prisma";

export const getUser = cache(async (id: string) => {
  return prisma.user.findUnique({
    where: { id },
    select: { id: true, name: true },
  });
});
```

### Server Actions (Mutations)

- **Location:** Place all mutations in `app/_actions/`.
- **Validation:** ALWAYS validate input with Zod before query execution.
- **Revalidation:** Always call `revalidatePath()` or `revalidateTag()` after successful mutation.
- **Error Handling:** Wrap in `try/catch` and return typed objects `{ success: boolean, error?: string }`.

```typescript
'use server'
import { prisma } from "@/app/_lib/prisma";
import { revalidatePath } from "next/cache";

export async function updateProfile(data: ProfileSchema) {
  try {
    await prisma.user.update({ ... });
    revalidatePath('/profile');
    return { success: true };
  } catch (error) {
    return { success: false, error: 'Update failed' };
  }
}
```

## 3. Performance & Serverless Best Practices

### The `search_path` Issue

Neon's HTTP adapter ignores connection pooling search paths on a per-request basis in some configurations. Ensure schema references are explicit or handled via the default search path in the connection string if not using the public schema.

---

## 6. Row Level Security (RLS) Integration with Prisma

Row Level Security provides database-level enforcement of access control. When combined with Prisma, RLS ensures data isolation even if application logic is bypassed.

### RLS with Prisma Pattern

**The Challenge:**
PostgreSQL RLS policies filter rows based on session-level context. Prisma needs to set this context before executing queries.

**The Solution:**
Use `prisma.$transaction()` with `$executeRawUnsafe()` to establish RLS context:

```typescript
// app/_lib/prisma-rls.ts
import { prisma } from "./prisma";
import { getCurrentUser } from "./auth";

/**
 * Execute queries with authenticated RLS context
 * Sets app.current_user_id for RLS policies
 */
export async function withAuthenticatedRLS<T>(
  callback: (tx: PrismaClient) => Promise<T>,
): Promise<T> {
  const user = await getCurrentUser();
  if (!user) throw new Error("User must be authenticated");

  return prisma.$transaction(async (tx) => {
    // Set RLS context: PostgreSQL can now filter based on current_user_id
    await tx.$executeRawUnsafe(
      `SELECT set_config('app.current_user_id', $1, true)`,
      user.id,
    );
    return callback(tx);
  });
}

/**
 * Execute queries with optional RLS (user may be null)
 */
export async function withOptionalRLS<T>(
  callback: (tx: PrismaClient, userId: string | null) => Promise<T>,
): Promise<T> {
  const user = await getCurrentUserOptional();
  const userId = user?.id ?? null;

  return prisma.$transaction(async (tx) => {
    if (userId) {
      await tx.$executeRawUnsafe(
        `SELECT set_config('app.current_user_id', $1, true)`,
        userId,
      );
    }
    return callback(tx, userId);
  });
}

/**
 * Execute queries with RLS disabled (admin/sync operations)
 * Use sparingly and only for trusted operations
 */
export async function withoutRLS<T>(
  callback: (tx: PrismaClient) => Promise<T>,
): Promise<T> {
  return prisma.$transaction(async (tx) => {
    // Execute without setting user context - RLS policies will not filter
    return callback(tx);
  });
}
```

### Real-World Example: Diary Entries

```typescript
// Before RLS: Manual filtering (error-prone)
export async function getDiaryEntries() {
  const user = await getCurrentUser();
  // ⚠️ If this check is bypassed, user sees all entries!
  return prisma.diaryEntry.findMany({
    where: { userId: user.id },
  });
}

// After RLS: Database-enforced filtering
export async function getDiaryEntries() {
  return withAuthenticatedRLS(async (tx) => {
    // RLS policy automatically filters to current_user_id
    // Cannot be bypassed, even if application logic is compromised
    return tx.diaryEntry.findMany();
  });
}
```

### Key Benefits

1. **Defense in Depth:** RLS provides security layer independent of application code
2. **Performance:** Filtering happens at database level, not in application memory
3. **Multi-tenant:** Naturally isolates data between users without complex query logic
4. **Audit Trail:** Database logs show what data each user accessed

### RLS Policy Example (PostgreSQL)

```sql
-- Enable RLS on the table
ALTER TABLE diary_entries ENABLE ROW LEVEL SECURITY;

-- Create policy: users can only see their own entries
CREATE POLICY diary_user_isolation ON diary_entries
  USING (user_id = current_setting('app.current_user_id')::uuid)
  WITH CHECK (user_id = current_setting('app.current_user_id')::uuid);
```

### Testing RLS with Prisma

```typescript
// __tests__/rls-isolation.test.ts
import { describe, it, expect } from "vitest";
import { prisma } from "@/app/_lib/prisma";
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";

describe("RLS Isolation", () => {
  it("prevents cross-user access", async () => {
    const userA = { id: "user-a-uuid", email: "a@test.com" };
    const userB = { id: "user-b-uuid", email: "b@test.com" };

    // User A creates entry
    await prisma.$transaction(async (tx) => {
      await tx.$executeRawUnsafe(
        `SELECT set_config('app.current_user_id', $1, true)`,
        userA.id,
      );
      await tx.diaryEntry.create({
        data: {
          userId: userA.id,
          characterId: 1,
          locationId: 1,
          activityDescription: "A's private entry",
        },
      });
    });

    // User B cannot see User A's entry
    await prisma.$transaction(async (tx) => {
      await tx.$executeRawUnsafe(
        `SELECT set_config('app.current_user_id', $1, true)`,
        userB.id,
      );
      const entriesB = await tx.diaryEntry.findMany();
      expect(entriesB).toHaveLength(0); // ✅ RLS enforced
    });
  });
});
```

### Lessons Learned

**Performance:** RLS filtering at database level is 10-100x faster than application-level filtering
**Complexity:** Setting up RLS policies requires PostgreSQL knowledge, but payoff is significant
**Testing:** Use integration tests to verify RLS policies work (unit test mocks cannot verify DB enforcement)
**Debugging:** Use `SELECT current_setting('app.current_user_id')` in queries to verify context is set

### Client Components Integration

**NEVER** import `prisma` in a Client Component (`"use client"`).

- Pass data as props from Server Components.
- Use Server Actions for interactivity.
- Data passed to Client Components must be serializable (Date objects must be converted to strings or numbers).

### Caching Strategy

- **Static (Default):** Prisma queries in Server Components are not cached by Next.js Data Cache automatically unless using `unstable_cache`.
- **Dynamic:** Queries relying on headers/cookies opt the page into dynamic rendering.

## 4. Common Patterns

### Repository Pattern

Centralize complex queries in `app/_lib/repositories.ts` to keep UI components clean and testable.

### Atomic Operations

Use `prisma.$transaction([])` for dependent writes (e.g., creating a User and an initial Post together).

## 5. Troubleshooting Reference

- **"Too many connections":** Check for extraneous `new PrismaClient()` calls.
- **"Module not found":** Ensure usage of `import { prisma }` path is correct.
- **Serialization Error:** You are passing a Date object to a Client Component. Convert it: `createdAt: user.createdAt.toISOString()`.
