---
name: server-actions-patterns
description: Comprehensive patterns and best practices for Next.js 16 Server Actions including mutations, error handling, revalidation, type safety, and form handling. Use when user needs to create, modify, or debug server actions, handle form submissions, implement optimistic updates, or work with server-side data mutations.
---

# Server Actions Patterns Skill

Complete guide for implementing Next.js Server Actions with type safety, proper error handling, and optimal UX patterns in The Simpsons API project.

---

## ⚠️ PRAGMATIC PATTERN SELECTION

> **Not every operation needs full DDD architecture. Choose the right pattern for the job.**

### Quick Decision Guide

| Operation Type                   | Pattern                       | Example                |
| -------------------------------- | ----------------------------- | ---------------------- |
| **Read-only public data**        | Simple Repository             | `findAllCharacters()`  |
| **Simple mutation, no rules**    | Basic Server Action           | `incrementViewCount()` |
| **Mutation with business rules** | Server Action + UseCase       | `trackEpisode()`       |
| **User-owned data**              | Server Action + UseCase + RLS | `createDiaryEntry()`   |

### Pattern Comparison

#### 🟢 Simple Pattern (Read + Basic Mutations)

```typescript
// For operations WITHOUT business rules
// app/_lib/repositories.ts
export async function findAllCharacters(limit = 50) {
  return prisma.character.findMany({ take: limit });
}

// Page uses directly
const characters = await findAllCharacters();
```

#### 🟡 Standard Server Action (Light Mutations)

```typescript
// For mutations with Zod validation but no complex business logic
"use server";
import { z } from "zod";

const Schema = z.object({ name: z.string().min(1) });

export async function updateName(name: string) {
  const validated = Schema.parse({ name });
  await prisma.item.update({ data: { name: validated.name } });
  revalidatePath("/items");
  return { success: true };
}
```

#### 🔴 Full DDD Pattern (Complex Mutations)

```typescript
// For mutations WITH business rules, user ownership, RLS
"use server";
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";
import { UseCaseFactory } from "@/infrastructure/factories";

export async function createDiaryEntry(...) {
  return withAuthenticatedRLS(prisma, async (tx, user) => {
    const useCase = UseCaseFactory.createCreateDiaryEntryUseCase();
    // UseCase validates: character exists, location exists, description rules
    await useCase.execute(input, user.id);
    revalidatePath("/diary");
    return { success: true };
  });
}
```

### Reference

See [docs/ARCHITECTURE_DECISION_MATRIX.md](../../../docs/ARCHITECTURE_DECISION_MATRIX.md) for the complete decision guide.

---

## When to Use This Skill

Use this skill when the user requests:

✅ **Primary Use Cases**

- "Create a server action"
- "Handle form submission"
- "Implement data mutation"
- "Add optimistic updates"
- "Fix server action errors"
- "Revalidate cache after update"

✅ **Secondary Use Cases**

- "Validate form data"
- "Handle file uploads"
- "Implement progressive enhancement"
- "Debug action not working"
- "Type server action responses"
- "Handle concurrent mutations"

❌ **Do NOT use when**

- Reading data only (use repositories/queries)
- API route handlers needed (use app/api)
- Client-side only operations
- Static data generation

## Project Context

### Existing Server Actions Structure

```
app/_actions/
├── collections.ts    # Quote collections CRUD
├── diary.ts          # Diary entries management
├── episodes.ts       # Episode progress tracking
├── social.ts         # Comments, follows, favorites
├── sync.ts           # External API sync
└── trivia.ts         # Trivia facts management
```

### Key Imports

```typescript
// Required imports for all server actions
"use server";

import { revalidatePath, revalidateTag } from "next/cache";
import { execute, query, queryOne } from "@/app/_lib/db-utils";
import { TABLES } from "@/app/_lib/db-schema";
import { getCurrentUser } from "@/app/_lib/auth";
```

---

## Core Patterns

### Pattern 1: Basic Server Action

```typescript
// app/_actions/example.ts
"use server";

import { revalidatePath } from "next/cache";
import { execute } from "@/app/_lib/db-utils";
import { TABLES } from "@/app/_lib/db-schema";
import { getCurrentUser } from "@/app/_lib/auth";

export async function createExample(data: { title: string; content: string }) {
  // 1. Authentication check
  const user = await getCurrentUser();
  if (!user) {
    return { success: false, error: "Not authenticated" };
  }

  // 2. Validation
  if (!data.title?.trim()) {
    return { success: false, error: "Title is required" };
  }

  // 3. Database operation
  try {
    await execute(
      `INSERT INTO ${TABLES.examples} (user_id, title, content, created_at)
       VALUES ($1, $2, $3, NOW())`,
      [user.id, data.title.trim(), data.content?.trim() || null],
    );

    // 4. Revalidate cache
    revalidatePath("/examples");

    return { success: true };
  } catch (error) {
    console.error("Failed to create example:", error);
    return { success: false, error: "Failed to create. Please try again." };
  }
}
```

### Pattern 2: FormData Handler

```typescript
// app/_actions/diary.ts
"use server";

import { revalidatePath } from "next/cache";
import { execute } from "@/app/_lib/db-utils";
import { TABLES } from "@/app/_lib/db-schema";
import { getCurrentUser } from "@/app/_lib/auth";

export async function addDiaryEntry(formData: FormData) {
  const user = await getCurrentUser();
  if (!user) {
    return { success: false, error: "Please log in to add diary entries" };
  }

  // Extract and validate form data
  const characterId = formData.get("characterId");
  const title = formData.get("title")?.toString().trim();
  const content = formData.get("content")?.toString().trim();
  const mood = formData.get("mood")?.toString() || "neutral";

  // Validation
  const errors: string[] = [];
  if (!characterId) errors.push("Character is required");
  if (!title) errors.push("Title is required");
  if (!content) errors.push("Content is required");

  if (errors.length > 0) {
    return { success: false, error: errors.join(", ") };
  }

  try {
    await execute(
      `INSERT INTO ${TABLES.diary_entries} 
       (user_id, character_id, title, content, mood, created_at)
       VALUES ($1, $2, $3, $4, $5, NOW())`,
      [user.id, characterId, title, content, mood],
    );

    revalidatePath("/diary");
    return { success: true, message: "Diary entry added!" };
  } catch (error) {
    console.error("Diary entry failed:", error);
    return { success: false, error: "Failed to save diary entry" };
  }
}
```

### Pattern 3: Return Type Definitions

```typescript
// app/_lib/types.ts
export type ActionResult<T = void> =
  | { success: true; data: T; message?: string }
  | { success: false; error: string; fieldErrors?: Record<string, string[]> };

// Usage in action
export async function updateProfile(
  formData: FormData,
): Promise<ActionResult<{ userId: string }>> {
  // ... validation

  if (!name) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: { name: ["Name is required"] },
    };
  }

  // ... operation

  return {
    success: true,
    data: { userId: user.id },
    message: "Profile updated successfully",
  };
}
```

### Pattern 4: Optimistic Updates

```typescript
// app/_components/FollowButton.tsx
"use client";

import { useOptimistic, useTransition } from "react";
import { toggleFollow } from "@/app/_actions/social";

interface FollowButtonProps {
  characterId: number;
  isFollowing: boolean;
  followerCount: number;
}

export function FollowButton({
  characterId,
  isFollowing,
  followerCount,
}: FollowButtonProps) {
  const [isPending, startTransition] = useTransition();

  const [optimisticState, setOptimisticState] = useOptimistic(
    { isFollowing, followerCount },
    (current, newFollowing: boolean) => ({
      isFollowing: newFollowing,
      followerCount: current.followerCount + (newFollowing ? 1 : -1),
    })
  );

  async function handleClick() {
    startTransition(async () => {
      // Optimistically update UI
      setOptimisticState(!optimisticState.isFollowing);

      // Perform actual action
      const result = await toggleFollow(characterId);

      if (!result.success) {
        // Revert on error (will happen automatically on revalidation)
        console.error(result.error);
      }
    });
  }

  return (
    <button
      onClick={handleClick}
      disabled={isPending}
      className={`px-4 py-2 rounded ${
        optimisticState.isFollowing
          ? "bg-red-500 hover:bg-red-600"
          : "bg-blue-500 hover:bg-blue-600"
      } text-white disabled:opacity-50`}
    >
      {isPending
        ? "..."
        : optimisticState.isFollowing
        ? "Unfollow"
        : "Follow"}
      <span className="ml-2">({optimisticState.followerCount})</span>
    </button>
  );
}
```

### Pattern 5: Form with useActionState (React 19)

```typescript
// app/_components/DiaryForm.tsx
"use client";

import { useActionState } from "react";
import { addDiaryEntry } from "@/app/_actions/diary";

const initialState = {
  success: false,
  error: null as string | null,
  message: null as string | null,
};

export function DiaryForm({ characterId }: { characterId: number }) {
  const [state, formAction, isPending] = useActionState(
    async (prevState: typeof initialState, formData: FormData) => {
      const result = await addDiaryEntry(formData);
      return {
        success: result.success,
        error: result.success ? null : result.error,
        message: result.success ? result.message || "Saved!" : null,
      };
    },
    initialState
  );

  return (
    <form action={formAction} className="space-y-4">
      <input type="hidden" name="characterId" value={characterId} />

      <div>
        <label htmlFor="title" className="block text-sm font-medium">
          Title
        </label>
        <input
          id="title"
          name="title"
          type="text"
          required
          className="mt-1 block w-full rounded border-gray-300"
        />
      </div>

      <div>
        <label htmlFor="content" className="block text-sm font-medium">
          Content
        </label>
        <textarea
          id="content"
          name="content"
          rows={4}
          required
          className="mt-1 block w-full rounded border-gray-300"
        />
      </div>

      <div>
        <label htmlFor="mood" className="block text-sm font-medium">
          Mood
        </label>
        <select id="mood" name="mood" className="mt-1 block w-full rounded">
          <option value="happy">Happy 😊</option>
          <option value="neutral">Neutral 😐</option>
          <option value="sad">Sad 😢</option>
          <option value="excited">Excited 🎉</option>
        </select>
      </div>

      {state.error && (
        <p className="text-red-600 text-sm">{state.error}</p>
      )}

      {state.message && (
        <p className="text-green-600 text-sm">{state.message}</p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {isPending ? "Saving..." : "Save Entry"}
      </button>
    </form>
  );
}
```

---

## Advanced Patterns

### Pattern 6: Zod Validation

```typescript
// app/_lib/validations.ts
import { z } from "zod";

export const diaryEntrySchema = z.object({
  characterId: z.coerce.number().positive("Character is required"),
  title: z.string().min(1, "Title is required").max(100, "Title too long"),
  content: z
    .string()
    .min(10, "Content must be at least 10 characters")
    .max(5000, "Content too long"),
  mood: z.enum(["happy", "neutral", "sad", "excited"]).default("neutral"),
});

export type DiaryEntryInput = z.infer<typeof diaryEntrySchema>;

// app/_actions/diary.ts
("use server");

import { diaryEntrySchema } from "@/app/_lib/validations";

export async function addDiaryEntry(formData: FormData) {
  const user = await getCurrentUser();
  if (!user) {
    return { success: false, error: "Not authenticated" };
  }

  // Parse and validate
  const rawData = {
    characterId: formData.get("characterId"),
    title: formData.get("title"),
    content: formData.get("content"),
    mood: formData.get("mood"),
  };

  const result = diaryEntrySchema.safeParse(rawData);

  if (!result.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: result.error.flatten().fieldErrors,
    };
  }

  const { characterId, title, content, mood } = result.data;

  // ... proceed with validated data
}
```

### Pattern 7: Transactions

```typescript
// For operations that need atomicity
import { pool } from "@/app/_lib/db";
import { TABLES } from "@/app/_lib/db-schema";

export async function transferQuotes(
  fromCollectionId: number,
  toCollectionId: number,
  quoteIds: number[],
) {
  const user = await getCurrentUser();
  if (!user) return { success: false, error: "Not authenticated" };

  // Note: With HTTP mode, each query is independent
  // For true transactions, you'd need a different approach
  // This example shows the pattern for handling multi-step operations

  try {
    // Verify ownership of both collections
    const [fromCollection, toCollection] = await Promise.all([
      queryOne(
        `SELECT id FROM ${TABLES.quote_collections} WHERE id = $1 AND user_id = $2`,
        [fromCollectionId, user.id],
      ),
      queryOne(
        `SELECT id FROM ${TABLES.quote_collections} WHERE id = $1 AND user_id = $2`,
        [toCollectionId, user.id],
      ),
    ]);

    if (!fromCollection || !toCollection) {
      return { success: false, error: "Collection not found or not owned" };
    }

    // Update quotes
    await execute(
      `UPDATE ${TABLES.collection_quotes} 
       SET collection_id = $1 
       WHERE collection_id = $2 AND id = ANY($3)`,
      [toCollectionId, fromCollectionId, quoteIds],
    );

    revalidatePath("/collections");
    return { success: true };
  } catch (error) {
    console.error("Transfer failed:", error);
    return { success: false, error: "Transfer failed" };
  }
}
```

### Pattern 8: Rate Limiting

```typescript
// app/_lib/rate-limit.ts
const rateLimitMap = new Map<string, { count: number; resetTime: number }>();

export function checkRateLimit(
  userId: string,
  action: string,
  limit: number = 10,
  windowMs: number = 60000,
): boolean {
  const key = `${userId}:${action}`;
  const now = Date.now();
  const record = rateLimitMap.get(key);

  if (!record || now > record.resetTime) {
    rateLimitMap.set(key, { count: 1, resetTime: now + windowMs });
    return true;
  }

  if (record.count >= limit) {
    return false;
  }

  record.count++;
  return true;
}

// Usage in action
export async function addComment(formData: FormData) {
  const user = await getCurrentUser();
  if (!user) return { success: false, error: "Not authenticated" };

  if (!checkRateLimit(user.id, "addComment", 5, 60000)) {
    return {
      success: false,
      error: "Too many comments. Please wait a minute.",
    };
  }

  // ... proceed
}
```

### Pattern 9: File Upload

```typescript
// app/_actions/upload.ts
"use server";

import { writeFile } from "fs/promises";
import { join } from "path";

export async function uploadImage(formData: FormData) {
  const user = await getCurrentUser();
  if (!user) return { success: false, error: "Not authenticated" };

  const file = formData.get("file") as File;
  if (!file) {
    return { success: false, error: "No file provided" };
  }

  // Validate file type
  const allowedTypes = ["image/jpeg", "image/png", "image/webp"];
  if (!allowedTypes.includes(file.type)) {
    return {
      success: false,
      error: "Invalid file type. Use JPEG, PNG, or WebP.",
    };
  }

  // Validate size (5MB max)
  if (file.size > 5 * 1024 * 1024) {
    return { success: false, error: "File too large. Max 5MB." };
  }

  try {
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // Generate unique filename
    const ext = file.name.split(".").pop();
    const filename = `${user.id}-${Date.now()}.${ext}`;
    const path = join(process.cwd(), "public/uploads", filename);

    await writeFile(path, buffer);

    return { success: true, data: { url: `/uploads/${filename}` } };
  } catch (error) {
    console.error("Upload failed:", error);
    return { success: false, error: "Upload failed" };
  }
}
```

---

## Revalidation Strategies

### Path-based Revalidation

```typescript
// Revalidate specific page
revalidatePath("/characters");

// Revalidate dynamic route
revalidatePath(`/characters/${characterId}`);

// Revalidate layout and all children
revalidatePath("/", "layout");

// Revalidate everything
revalidatePath("/", "page");
```

### Tag-based Revalidation

```typescript
// In data fetching (page or component)
const characters = await fetch("/api/characters", {
  next: { tags: ["characters", "homepage"] },
});

// In server action
import { revalidateTag } from "next/cache";

export async function addCharacter(data: CharacterData) {
  // ... create character

  // Revalidate all caches with these tags
  revalidateTag("characters");
  revalidateTag("homepage");

  return { success: true };
}
```

### When to Use Which

| Scenario               | Strategy                        |
| ---------------------- | ------------------------------- |
| Single page update     | `revalidatePath('/page')`       |
| Related pages update   | `revalidateTag('tagname')`      |
| All pages need update  | `revalidatePath('/', 'layout')` |
| Specific dynamic route | `revalidatePath('/items/[id]')` |

---

## Error Handling Best Practices

### Structured Error Responses

```typescript
// Consistent error types
type ServerActionError =
  | { code: "UNAUTHORIZED"; message: string }
  | { code: "VALIDATION"; message: string; fields: Record<string, string[]> }
  | { code: "NOT_FOUND"; message: string }
  | { code: "CONFLICT"; message: string }
  | { code: "SERVER_ERROR"; message: string };

function createError(error: ServerActionError): {
  success: false;
  error: ServerActionError;
} {
  return { success: false, error };
}

// Usage
export async function updateCharacter(id: number, data: CharacterUpdate) {
  const user = await getCurrentUser();
  if (!user) {
    return createError({ code: "UNAUTHORIZED", message: "Please log in" });
  }

  const existing = await queryOne(
    `SELECT * FROM ${TABLES.characters} WHERE id = $1`,
    [id],
  );
  if (!existing) {
    return createError({ code: "NOT_FOUND", message: "Character not found" });
  }

  // ... update logic
}
```

### Client-Side Error Handling

```typescript
"use client";

import { useTransition } from "react";
import { toast } from "sonner";

function MyComponent() {
  const [isPending, startTransition] = useTransition();

  async function handleAction() {
    startTransition(async () => {
      const result = await myServerAction(data);

      if (result.success) {
        toast.success(result.message || "Success!");
      } else {
        // Handle different error types
        if (result.error.code === "UNAUTHORIZED") {
          toast.error("Please log in to continue");
          // Redirect to login
        } else if (result.error.code === "VALIDATION") {
          toast.error(result.error.message);
          // Show field errors
        } else {
          toast.error("Something went wrong. Please try again.");
        }
      }
    });
  }

  return (
    <button onClick={handleAction} disabled={isPending}>
      {isPending ? "Loading..." : "Submit"}
    </button>
  );
}
```

---

## Testing Server Actions

### Unit Testing Pattern

```typescript
// __tests__/actions/diary.test.ts
import { describe, it, expect, vi } from "vitest";
import { addDiaryEntry } from "@/app/_actions/diary";

// Mock dependencies
vi.mock("@/app/_lib/auth", () => ({
  getCurrentUser: vi.fn(),
}));

vi.mock("@/app/_lib/db-utils", () => ({
  execute: vi.fn(),
}));

describe("addDiaryEntry", () => {
  it("should return error when not authenticated", async () => {
    const { getCurrentUser } = await import("@/app/_lib/auth");
    (getCurrentUser as any).mockResolvedValue(null);

    const formData = new FormData();
    formData.set("title", "Test");
    formData.set("content", "Test content");

    const result = await addDiaryEntry(formData);

    expect(result.success).toBe(false);
    expect(result.error).toContain("log in");
  });

  it("should create entry when valid", async () => {
    const { getCurrentUser } = await import("@/app/_lib/auth");
    const { execute } = await import("@/app/_lib/db-utils");

    (getCurrentUser as any).mockResolvedValue({ id: "user123" });
    (execute as any).mockResolvedValue(1);

    const formData = new FormData();
    formData.set("characterId", "1");
    formData.set("title", "Test Entry");
    formData.set("content", "This is test content");

    const result = await addDiaryEntry(formData);

    expect(result.success).toBe(true);
    expect(execute).toHaveBeenCalled();
  });
});
```

---

## Common Mistakes

### ❌ Wrong: Missing "use server" Directive

```typescript
// This won't work as a server action
export async function myAction() {
  // ...
}
```

### ✅ Correct: Include Directive

```typescript
"use server";

export async function myAction() {
  // ...
}
```

### ❌ Wrong: Returning Non-Serializable Data

```typescript
export async function getUser() {
  const user = await queryOne(...);
  return user; // Date objects, etc. may cause issues
}
```

### ✅ Correct: Return Serializable Data

```typescript
export async function getUser() {
  const user = await queryOne(...);
  return {
    ...user,
    createdAt: user.created_at.toISOString(),
  };
}
```

### ❌ Wrong: Not Handling Errors

```typescript
export async function deleteItem(id: number) {
  await execute(`DELETE FROM ${TABLES.items} WHERE id = $1`, [id]);
  return { success: true };
}
```

### ✅ Correct: Wrap in Try-Catch

```typescript
export async function deleteItem(id: number) {
  try {
    await execute(`DELETE FROM ${TABLES.items} WHERE id = $1`, [id]);
    revalidatePath("/items");
    return { success: true };
  } catch (error) {
    console.error("Delete failed:", error);
    return { success: false, error: "Failed to delete item" };
  }
}
```

---

## Related Skills

- [neon-database-management](../neon-database-management/SKILL.md) - Database queries
- [component-development](../component-development/SKILL.md) - Client components using actions
- [webapp-testing](../webapp-testing/SKILL.md) - Testing action flows

---

---

## Error Handling Best Practices (SonarLint Validated)

### ✅ DO: Preserve Domain Exception Types

**Critical Pattern:** When using DDD architecture, preserve domain exceptions instead of wrapping them in generic `Error`.

```typescript
// app/_actions/episodes.ts
"use server";
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";
import { UseCaseFactory } from "@/infrastructure/factories";
import {
  ValidationException,
  NotFoundException,
  DomainException,
} from "@/core/domain/exceptions";
import { revalidatePath } from "next/cache";

export async function trackEpisode(episodeId: number, rating: number) {
  return withAuthenticatedRLS(prisma, async (tx, user) => {
    try {
      const useCase = UseCaseFactory.createTrackEpisodeUseCase();
      await useCase.execute({ episodeId, rating }, user.id);

      revalidatePath(`/episodes/${episodeId}`);
      return { success: true };
    } catch (error) {
      // ✅ CORRECT: Preserve domain exceptions
      if (error instanceof ValidationException) {
        throw error; // Client can catch specific type + access field, code
      }
      if (error instanceof NotFoundException) {
        throw error; // Client can access entityType, entityId
      }
      if (error instanceof DomainException) {
        throw error; // All domain exceptions preserved
      }
      if (error instanceof Error) {
        throw error; // Preserve stack trace
      }

      throw new Error("Failed to track episode");
    }
  });
}
```

### ❌ DON'T: Wrap Domain Exceptions

**Anti-Pattern:**

```typescript
// ❌ BAD - Loses exception type and metadata
catch (error) {
  if (error instanceof ValidationException) {
    throw new Error(error.message); // Lost field, code, metadata!
  }
  throw new Error("Failed");
}

// Client cannot catch specific types
try {
  await trackEpisode(123, 5);
} catch (error) {
  // ❌ Can only check error.message (string matching = fragile)
  if (error.message.includes("validation")) {
    // No access to error.field, error.code
  }
}
```

### Why This Matters

**1. Type-Safe Error Handling**

```typescript
// Client code with preserved exceptions
try {
  await trackEpisode(episodeId, rating);
  toast.success("Episode tracked!");
} catch (error) {
  if (error instanceof ValidationException) {
    // ✅ Access to field-specific data
    toast.error(`${error.field}: ${error.message}`);
  } else if (error instanceof NotFoundException) {
    // ✅ Access to entity information
    toast.error(`${error.entityType} not found`);
  } else {
    toast.error("Something went wrong");
  }
}
```

**2. Better Debugging**

- Full stack traces preserved
- Exception metadata available in error logs
- Clearer error origins in production monitoring

**3. Consistent Error API**

```typescript
// All domain exceptions have consistent structure
interface DomainException {
  message: string;
  code: string;
  timestamp: Date;
  // Specific exceptions add more fields
}

interface ValidationException extends DomainException {
  field: string;
  value?: unknown;
}

interface NotFoundException extends DomainException {
  entityType: string;
  entityId: string | number;
}
```

### Pattern: Error Handling in DDD Server Actions

```typescript
"use server";
import {
  ValidationException,
  NotFoundException,
  DomainException
} from "@/core/domain/exceptions";

export async function complexMutation(...) {
  return withAuthenticatedRLS(prisma, async (tx, user) => {
    try {
      const useCase = UseCaseFactory.createUseCase();
      await useCase.execute(input, user.id);

      revalidatePath("/path");
      return { success: true };
    } catch (error) {
      // ✅ Order matters: Most specific first
      if (error instanceof ValidationException) {
        throw error;
      }
      if (error instanceof NotFoundException) {
        throw error;
      }
      if (error instanceof DomainException) {
        throw error; // Catches any other domain exceptions
      }
      if (error instanceof Error) {
        throw error; // Preserve standard errors
      }

      // Truly unexpected errors
      throw new Error("An unexpected error occurred");
    }
  });
}
```

### Lessons Learned (PR #14 SonarLint Analysis)

**Fixed Files:**

- [app/\_actions/collections.ts](../../../app/_actions/collections.ts) - 2 error handling fixes
- [app/\_actions/episodes.ts](../../../app/_actions/episodes.ts) - 1 fix
- [app/\_actions/diary.ts](../../../app/_actions/diary.ts) - 2 fixes
- [app/\_actions/social.ts](../../../app/_actions/social.ts) - 1 fix

**Impact:**

- Zero SonarLint blockers/critical issues
- Type-safe error handling throughout app
- Improved client-side error UX
- Better debugging in production

**Reference:** See [.traces/05-sonarlint-pr14-cleanup.md](../../../.traces/05-sonarlint-pr14-cleanup.md) for complete analysis.

---

## Server Actions with Row Level Security

Row Level Security (RLS) provides database-level data isolation. Server Actions are the ideal place to enforce RLS in Next.js applications.

### The RLS Pattern in Server Actions

**Pattern: Always use RLS helpers, never manual filtering**

```typescript
// ❌ BEFORE: Manual filtering (can be bypassed)
"use server";
import { prisma } from "@/app/_lib/prisma";

export async function getDiaryEntries() {
  const user = await getCurrentUser();
  // If this check is forgotten or bypassed, user sees everyone's data!
  return prisma.diaryEntry.findMany({
    where: { userId: user.id },
  });
}

// ✅ AFTER: RLS enforced at database level
("use server");
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";

export async function getDiaryEntries() {
  // RLS automatically filters by current_user_id
  // Database guarantees: cannot be bypassed
  return withAuthenticatedRLS(async (tx) => {
    return tx.diaryEntry.findMany();
  });
}
```

### Migration Path: Manual Filtering → RLS

**Step 1: Identify all manual filtering patterns**

```typescript
// Find all places that do: where: { userId: user.id }
// These are candidates for RLS enforcement
```

**Step 2: Wrap in RLS helper**

```typescript
"use server";
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";

export async function getUserData(id: string) {
  return withAuthenticatedRLS(async (tx) => {
    // RLS automatically validates ownership
    return tx.userData.findUnique({ where: { id } });
  });
}
```

**Step 3: Remove manual validation**

```typescript
// ❌ No longer needed
const user = await getCurrentUser();
if (user.id !== data.userId) throw new Error("Unauthorized");

// ✅ RLS handles it
```

### RLS + Zod Validation Pattern

```typescript
"use server";
import { z } from "zod";
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";
import { revalidatePath } from "next/cache";

const AddDiaryEntrySchema = z.object({
  characterId: z.number().int().positive(),
  locationId: z.number().int().positive(),
  description: z.string().min(10).max(1000),
});

export async function addDiaryEntry(data: z.infer<typeof AddDiaryEntrySchema>) {
  try {
    // 1. Validate input
    const validated = AddDiaryEntrySchema.parse(data);

    // 2. Execute with RLS context
    const result = await withAuthenticatedRLS(async (tx, user) => {
      return tx.diaryEntry.create({
        data: {
          userId: user.id, // Set by RLS context
          ...validated,
        },
      });
    });

    // 3. Revalidate cache
    revalidatePath("/diary");

    return { success: true, data: result };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        error: "Validation failed",
        details: error.errors,
      };
    }
    return { success: false, error: "Failed to add entry" };
  }
}
```

### Error Handling with RLS

```typescript
"use server";
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";

export async function deleteEntry(entryId: string) {
  try {
    await withAuthenticatedRLS(async (tx) => {
      const entry = await tx.diaryEntry.findUnique({
        where: { id: entryId },
      });

      // ✅ RLS ensures entry belongs to current user
      // If RLS policy returns null, entry belongs to different user
      if (!entry) {
        throw new Error("Entry not found or access denied");
      }

      await tx.diaryEntry.delete({ where: { id: entryId } });
    });

    return { success: true };
  } catch (error) {
    if (error instanceof PrismaClientKnownRequestError) {
      if (error.code === "P2025") {
        // Record not found - could be RLS filtered
        return { success: false, error: "Entry not found" };
      }
    }
    return { success: false, error: "Failed to delete entry" };
  }
}
```

### Testing Server Actions with RLS

```typescript
// app/_actions/diary.test.ts
import { describe, it, expect, vi } from "vitest";
import { addDiaryEntry } from "./diary";

vi.mock("@/app/_lib/prisma-rls", () => ({
  withAuthenticatedRLS: vi.fn(async (callback) => {
    // Mock user context
    const mockPrisma = {
      diaryEntry: {
        create: vi.fn().mockResolvedValue({
          id: "entry-1",
          userId: "test-user",
          characterId: 1,
          createdAt: new Date(),
        }),
      },
    };
    const mockUser = { id: "test-user", email: "test@test.com" };
    return callback(mockPrisma, mockUser);
  }),
}));

vi.mock("next/cache", () => ({
  revalidatePath: vi.fn(),
}));

describe("addDiaryEntry Server Action with RLS", () => {
  it("creates entry with user context", async () => {
    const result = await addDiaryEntry({
      characterId: 1,
      locationId: 1,
      description: "A day in Springfield",
    });

    expect(result.success).toBe(true);
    // ✅ Entry automatically assigned to current user via RLS context
  });

  it("validates input before executing", async () => {
    const result = await addDiaryEntry({
      characterId: 1,
      locationId: 1,
      description: "Too short", // Fails min(10) validation
    });

    expect(result.success).toBe(false);
    expect(result.error).toContain("Validation failed");
  });
});
```

### Lessons Learned from RLS Implementation

1. **Default to RLS:** New Server Actions should use RLS helpers by default
2. **Performance:** RLS filtering at DB level is faster than application filtering
3. **Security:** RLS provides defense-in-depth protection against logic bugs
4. **Testing:** Mock RLS helpers in unit tests, verify policies in integration tests
5. **Consistency:** All Server Actions mutating user data should use `withAuthenticatedRLS`

## References

- [Next.js Server Actions Documentation](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [React 19 Actions](https://react.dev/reference/react/use-server)
- [Zod Validation Library](https://zod.dev/)
- [prisma-nextjs16 Skill](../prisma-nextjs16/SKILL.md) - RLS with Prisma patterns

---

**Last Updated:** January 19, 2026  
**Maintained By:** Development Team  
**Status:** ✅ Production Ready with RLS Support
