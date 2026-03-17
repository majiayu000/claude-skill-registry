---
name: web-framework-nextjs-server-actions
description: Server Actions patterns for mutations, revalidation, and form handling in Next.js App Router
---

# Next.js Server Actions Patterns

> **Quick Guide:** Use Server Actions for mutations (create, update, delete) in Next.js App Router. Define with `'use server'` directive, invoke from forms or event handlers, revalidate cache after mutations.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST add `'use server'` directive at the top of the file OR at the top of the async function)**

**(You MUST revalidate the cache after mutations using `revalidatePath()` or `revalidateTag()`)**

**(You MUST validate all input data on the server - client-side validation is NOT sufficient for security)**

**(You MUST perform authorization checks inside EVERY Server Action - they are public HTTP endpoints)**

**(You MUST call `revalidatePath()` BEFORE `redirect()` to ensure fresh data)**

</critical_requirements>

---

**Auto-detection:** Server Actions, use server directive, revalidatePath, revalidateTag, formAction, useActionState, useFormStatus, useOptimistic, server mutation

**When to use:**

- Creating, updating, or deleting data from forms
- Performing server-side mutations triggered by user actions
- Invalidating cached data after state changes
- Progressive enhancement for forms that work without JavaScript

**Key patterns covered:**

- Server Action definition (`'use server'` directive)
- Form actions with progressive enhancement
- Cache revalidation patterns (revalidatePath, revalidateTag)
- Pending states (useActionState from React 19, useFormStatus from React 19)
- Optimistic updates (useOptimistic from React 19)
- Error handling and validation

**React 19 Integration:**

- `useActionState`, `useFormStatus`, and `useOptimistic` are React 19 hooks (not Next.js-specific)
- `useActionState` replaces the deprecated `ReactDOM.useFormState` from React Canary
- These hooks work with Server Actions for form state management

**When NOT to use:**

- Data fetching (use Server Components or your data fetching solution)
- Complex multi-step workflows requiring parallel operations (use Route Handlers)
- Real-time subscriptions (use WebSockets or SSE)

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Server Actions are asynchronous functions that execute on the server, invoked via network requests from the client. They integrate with Next.js caching and revalidation, enabling single-roundtrip updates where both UI and data refresh together.

**Core Principles:**

1. **Server-side execution**: Actions run on the server, enabling direct database access and secure operations
2. **Progressive enhancement**: Form-based actions work without JavaScript enabled
3. **Integrated caching**: Actions trigger cache revalidation, keeping UI in sync with data
4. **Security by default**: Encrypted action IDs and dead code elimination, but explicit auth checks required

**Server Actions vs API Routes:**

Server Actions are ideal for form submissions and mutations tightly coupled to UI. Use Route Handlers for external API consumers, webhooks, or complex multi-step operations requiring parallel execution.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Defining Server Actions

Define Server Actions using the `'use server'` directive. Place it at the file level (recommended for Client Component imports) or function level (for Server Components).

#### File-Level Directive (Recommended)

```typescript
// app/actions.ts
"use server";

import { revalidatePath } from "next/cache";

export async function createPost(formData: FormData) {
  const title = formData.get("title") as string;
  const content = formData.get("content") as string;

  // Mutation logic here (defer to your database solution)
  // ...

  revalidatePath("/posts");
}
```

**Why good:** File-level directive marks all exports as Server Actions, clear separation of server code, can be imported into Client Components

#### Function-Level Directive (Server Components Only)

```typescript
// app/page.tsx - Server Component
export default function Page() {
  async function createPost(formData: FormData) {
    'use server'
    // Server Action logic
  }

  return <form action={createPost}>...</form>
}
```

**Why good:** Inline definition when action is only used in one place, directive at function level keeps action close to usage

---

### Pattern 2: Form Actions with Progressive Enhancement

Invoke Server Actions via the `action` attribute on forms. This enables progressive enhancement - forms work even without JavaScript.

```typescript
// app/posts/new/page.tsx
import { createPost } from '@/app/actions'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input type="text" name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  )
}
```

**Why good:** Form works without JavaScript (progressive enhancement), FormData automatically passed to action, native browser form validation works

**When to use:** Any form that performs a mutation - this is the primary invocation pattern for Server Actions.

---

### Pattern 3: Cache Revalidation

After mutations, revalidate the cache to reflect changes in the UI. Use `revalidatePath()` for specific routes or `revalidateTag()` for tagged data.

#### revalidatePath - Refresh Specific Routes

```typescript
"use server";

import { revalidatePath } from "next/cache";

export async function updatePost(id: string, formData: FormData) {
  // Update in database...

  // Revalidate the posts list page
  revalidatePath("/posts");

  // Revalidate the specific post page
  revalidatePath(`/posts/${id}`);
}
```

**Why good:** Invalidates cached data for specific routes, UI shows fresh data after mutation

#### revalidateTag - Invalidate Tagged Cache

```typescript
"use server";

import { revalidateTag } from "next/cache";

export async function createPost(formData: FormData) {
  // Create in database...

  // Invalidate all data tagged with 'posts'
  revalidateTag("posts");
}
```

**Why good:** Invalidates all cached data with a specific tag, useful when multiple routes display the same data

**When to use:** Use `revalidatePath()` for route-specific invalidation, `revalidateTag()` for cross-route invalidation of tagged data.

---

### Pattern 4: Post-Mutation Redirect

Redirect users after successful mutations. Call `revalidatePath()` BEFORE `redirect()` to ensure the destination shows fresh data.

```typescript
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

export async function createPost(formData: FormData) {
  // Create in database...

  // Revalidate BEFORE redirect
  revalidatePath("/posts");

  // Redirect to posts list
  redirect("/posts");
}
```

**Why good:** Ensures destination page shows updated data, `redirect()` throws internally so nothing runs after it

---

### Pattern 5: Passing Additional Arguments with bind()

Pass arguments beyond FormData using JavaScript's `bind()` method.

```typescript
// actions.ts
"use server";

export async function updateUser(userId: string, formData: FormData) {
  const name = formData.get("name") as string;
  // Update user with userId...
}
```

```typescript
// components/user-form.tsx
'use client'

import { updateUser } from '@/app/actions'

export function UserForm({ userId }: { userId: string }) {
  const updateUserWithId = updateUser.bind(null, userId)

  return (
    <form action={updateUserWithId}>
      <input type="text" name="name" />
      <button type="submit">Update</button>
    </form>
  )
}
```

**Why good:** Passes additional context (IDs, etc.) to Server Actions, works with progressive enhancement, type-safe with TypeScript

---

### Pattern 6: Event Handler Invocation

Invoke Server Actions from event handlers when not using forms.

```typescript
// components/like-button.tsx
'use client'

import { useState, useTransition } from 'react'
import { incrementLike } from '@/app/actions'

export function LikeButton({ initialLikes }: { initialLikes: number }) {
  const [likes, setLikes] = useState(initialLikes)
  const [isPending, startTransition] = useTransition()

  const handleClick = () => {
    startTransition(async () => {
      const updatedLikes = await incrementLike()
      setLikes(updatedLikes)
    })
  }

  return (
    <button onClick={handleClick} disabled={isPending}>
      {isPending ? 'Liking...' : `Likes: ${likes}`}
    </button>
  )
}
```

**Why good:** `startTransition` prevents UI blocking during action execution, pending state provides user feedback, works for non-form interactions

**When to use:** Toggle buttons, quick actions, any mutation not tied to a form submission.

---

### Pattern 7: Server-Side Validation

Validate all input data on the server. Use a validation library for type-safe parsing.

```typescript
// app/actions.ts
"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";

const CreatePostSchema = z.object({
  title: z.string().min(1, "Title is required").max(200),
  content: z.string().min(1, "Content is required"),
});

export async function createPost(formData: FormData) {
  const rawData = {
    title: formData.get("title"),
    content: formData.get("content"),
  };

  const validatedFields = CreatePostSchema.safeParse(rawData);

  if (!validatedFields.success) {
    return {
      success: false,
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  // Proceed with mutation using validatedFields.data
  // ...

  revalidatePath("/posts");
  return { success: true };
}
```

**Why good:** Server-side validation cannot be bypassed, type-safe data after validation, structured error response for UI feedback

---

### Pattern 8: Authorization in Server Actions

Server Actions are public HTTP endpoints. Perform authorization checks inside EVERY action.

```typescript
// app/actions.ts
"use server";

import { revalidatePath } from "next/cache";

export async function deletePost(postId: string) {
  // Defer to your authentication solution for user/session retrieval
  const user = await getCurrentUser();

  if (!user) {
    throw new Error("Unauthorized: Not authenticated");
  }

  // Defer to your database solution for fetching the post
  const post = await getPost(postId);

  if (!post) {
    throw new Error("Not found");
  }

  if (post.authorId !== user.id) {
    throw new Error("Forbidden: Not the author");
  }

  // Proceed with deletion
  // ...

  revalidatePath("/posts");
}
```

**Why good:** Every action verifies identity and permissions, prevents unauthorized access even if action ID is discovered, follows defense-in-depth principle

</patterns>

---

<integration>

## Integration Guide

**Server Actions are framework-agnostic for business logic.** They receive data, perform mutations, and revalidate cache. The actual database operations, authentication, and form UI are handled by other parts of your stack.

**Works with:**

- **Forms**: Native HTML forms with `action` attribute
- **React hooks**: `useActionState`, `useFormStatus`, `useOptimistic` for UI states
- **Cache**: Next.js cache system via `revalidatePath()` and `revalidateTag()`
- **Navigation**: `redirect()` for post-mutation navigation

**Defers to:**

- **Database operations**: Use your database/ORM solution for queries and mutations
- **Authentication**: Use your auth solution for user/session retrieval
- **Form UI components**: Use your component library for form elements
- **Validation libraries**: Use Zod, Valibot, or similar for schema validation

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST add `'use server'` directive at the top of the file OR at the top of the async function)**

**(You MUST revalidate the cache after mutations using `revalidatePath()` or `revalidateTag()`)**

**(You MUST validate all input data on the server - client-side validation is NOT sufficient for security)**

**(You MUST perform authorization checks inside EVERY Server Action - they are public HTTP endpoints)**

**(You MUST call `revalidatePath()` BEFORE `redirect()` to ensure fresh data)**

**Failure to follow these rules will cause stale UI, security vulnerabilities, or broken redirects.**

</critical_reminders>
