---
name: rbac-security
description: Role-based access control (RBAC) patterns, authentication wrappers, authorization checks, input validation with Zod schemas, security boundaries, server action security, real-time message validation, preventing common vulnerabilities like XSS and SQL injection, and security best practices for ree-board project
model: opus
---

# RBAC Security Patterns

## When to Use This Skill

**CRITICAL:** This skill is MANDATORY for all server actions and database operations.

Activate this skill when:

- Creating or modifying server actions
- Implementing authentication flows
- Adding authorization checks
- Validating user input
- Working with real-time messages
- Reviewing code for security vulnerabilities
- Implementing role-based access control

## Core Patterns

### Authentication Wrappers (MANDATORY)

**Rule:** ALL server actions MUST use `actionWithAuth` or `rbacWithAuth`

#### actionWithAuth - Simple Authentication

**Use when:** Only user authentication is needed (no board-specific permissions)

```typescript
// lib/actions/user/updateProfile.ts
"use server";

import { actionWithAuth } from "@/lib/actions/actionWithAuth";

export const updateProfile = async (name: string) =>
  actionWithAuth(async (userId) => {
    // userId is guaranteed to exist
    await db.update(userTable).set({ name }).where(eq(userTable.id, userId));

    return { success: true };
  });
```

#### rbacWithAuth - Role-Based Access Control

**Use when:** Board-specific permissions are required

```typescript
// lib/actions/post/deletePost.ts
"use server";

import { rbacWithAuth } from "@/lib/actions/actionWithAuth";

export const deletePost = async (postId: string, boardId: string) =>
  rbacWithAuth(boardId, async (userId) => {
    // User's role is checked against board
    // Only owner/member can proceed
    await db.delete(postTable).where(eq(postTable.id, postId));

    return { success: true };
  });
```

### Role Hierarchy

**Three Roles with Decreasing Permissions:**

```typescript
enum Role {
  owner = "owner", // Full control (delete board, manage members)
  member = "member", // Create/edit/delete own posts, vote
  guest = "guest", // Read-only access
}
```

**Role Permissions:**

| Action          | Owner | Member | Guest |
| --------------- | ----- | ------ | ----- |
| View board      | ✅    | ✅     | ✅    |
| Create post     | ✅    | ✅     | ❌    |
| Edit own post   | ✅    | ✅     | ❌    |
| Delete own post | ✅    | ✅     | ❌    |
| Vote            | ✅    | ✅     | ❌    |
| Manage members  | ✅    | ❌     | ❌    |
| Delete board    | ✅    | ❌     | ❌    |

**Implementation:**

```typescript
// lib/actions/actionWithAuth.ts
export const rbacWithAuth = async <T>(
  boardId: string,
  callback: (userId: string, role: Role) => Promise<T>
): Promise<T> => {
  // Verify session using Supabase
  const session = await verifySession();

  if (!session?.userId) {
    throw new Error("Unauthorized");
  }

  // Check user's role for this board
  const member = await db.query.memberTable.findFirst({
    where: and(
      eq(memberTable.boardId, boardId),
      eq(memberTable.userId, session.userId)
    ),
  });

  if (!member) {
    throw new Error("Access denied");
  }

  // Guest role has read-only access
  if (member.role === "guest") {
    throw new Error("Insufficient permissions");
  }

  return callback(session.userId, member.role);
};
```

### Input Validation with Zod

**Use Zod for Complex Validation:**

```typescript
import { z } from "zod";

const CreatePostSchema = z.object({
  boardId: z.string().min(1, "Board ID is required"),
  content: z
    .string()
    .min(1, "Content cannot be empty")
    .max(1000, "Content too long"),
  type: z.enum(["went_well", "to_improve", "action_items"]),
});

export const createPost = async (data: unknown) => {
  // ✅ Validate input
  const validated = CreatePostSchema.parse(data);
  return rbacWithAuth(validated.boardId, async (userId) => {
    const post = await db
      .insert(postTable)
      .values({
        id: nanoid(),
        userId,
        ...validated,
        createdAt: new Date(),
      })
      .returning();

    return post[0];
  });
};
```

### Real-Time Message Validation

**Critical for Ably Messages:**

```typescript
// lib/realtime/messageProcessors.ts
import { z } from "zod";

const PostUpdateSchema = z.object({
  postId: z.string(),
  content: z.string().min(1).max(1000),
  timestamp: z.number(),
});

export const processPostUpdate = (data: unknown) => {
  try {
    // ✅ Validate message data
    const validated = PostUpdateSchema.parse(data);

    // ✅ Check message staleness (30s threshold)
    const now = Date.now();
    if (now - validated.timestamp > 30000) {
      console.warn("Stale message discarded", {
        age: now - validated.timestamp,
      });
      return;
    }

    // Process validated message
    updatePostSignal(validated.postId, validated.content);
  } catch (error) {
    console.error("Invalid message data", { error, data });
  }
};
```

### Security Boundaries

**Never Trust Client Input:**

```typescript
// ❌ BAD - Trusts client completely
export const deletePost = async (postId: string) => {
  await db.delete(postTable).where(eq(postTable.id, postId));
};

// ✅ GOOD - Validates ownership
export const deletePost = async (postId: string, boardId: string) =>
  rbacWithAuth(boardId, async (userId) => {
    const post = await db.query.postTable.findFirst({
      where: eq(postTable.id, postId),
    });

    // Verify post exists and user owns it
    if (!post) {
      throw new Error("Post not found");
    }

    if (post.userId !== userId) {
      throw new Error("Cannot delete another user's post");
    }

    await db.delete(postTable).where(eq(postTable.id, postId));
  });
```

### Preventing Common Vulnerabilities

#### XSS Prevention

**Already Handled by React:** React escapes content by default

**For Markdown Content:**

```typescript
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";

// ✅ Sanitize user-generated markdown
<ReactMarkdown rehypePlugins={[rehypeSanitize]}>{userContent}</ReactMarkdown>;
```

#### SQL Injection Prevention

**Drizzle ORM Prevents This:**

```typescript
// ✅ Parameterized queries (safe)
await db.select().from(postTable).where(eq(postTable.id, postId));

// ❌ Raw SQL (avoid unless necessary)
await db.execute(sql`SELECT * FROM post WHERE id = ${postId}`);
```

## Anti-Patterns

### ❌ Server Actions Without Authentication

**CRITICAL VULNERABILITY:**

```typescript
"use server";

// ❌ NEVER DO THIS
export async function deleteBoard(id: string) {
  await db.delete(boardTable).where(eq(boardTable.id, id));
}
```

**Correct:**

```typescript
"use server";

// ✅ ALWAYS USE AUTHENTICATION
export const deleteBoard = async (id: string) =>
  rbacWithAuth(id, async (userId, role) => {
    if (role !== "owner") {
      throw new Error("Only board owner can delete");
    }
    await db.delete(boardTable).where(eq(boardTable.id, id));
  });
```

### ❌ Trusting Client-Side Role Checks

**Bad:**

```typescript
"use client";

function DeleteButton({ userRole, boardId }) {
  // ❌ Client-side check can be bypassed
  if (userRole === "owner") {
    return <button onClick={() => deleteBoard(boardId)}>Delete</button>;
  }
}
```

**Good:**

```typescript
"use client";

function DeleteButton({ boardId }) {
  // ✅ UI check for UX, server validates
  return <button onClick={() => deleteBoard(boardId)}>Delete</button>;
}

// Server action validates role
export const deleteBoard = async (id: string) =>
  rbacWithAuth(id, async (userId, role) => {
    if (role !== "owner") {
      throw new Error("Unauthorized");
    }
    // ...
  });
```

### ❌ Exposing Sensitive Data in Client Components

**Bad:**

```typescript
// ❌ API keys in client component
"use client";

const API_KEY = "secret-key"; // Exposed in bundle!
```

**Good:**

```typescript
// ✅ API keys in server actions/environment
"use server";

export async function callExternalAPI() {
  const apiKey = process.env.API_KEY; // Server-side only
  // ...
}
```

### ❌ Not Validating Real-Time Messages

**Bad:**

```typescript
// ❌ Trusts message data completely
channel.subscribe("post:update", (message) => {
  updatePost(message.data.postId, message.data.content);
});
```

**Good:**

```typescript
// ✅ Validates before processing
channel.subscribe("post:update", (message) => {
  const validated = PostUpdateSchema.safeParse(message.data);
  if (!validated.success) {
    console.error("Invalid message", validated.error);
    return;
  }
  updatePost(validated.data.postId, validated.data.content);
});
```

## Integration with Other Skills

- **[nextjs-app-router](../nextjs-app-router/SKILL.md):** Server actions must use authentication wrappers
- **[drizzle-patterns](../drizzle-patterns/SKILL.md):** Database operations require auth checks
- **[ably-realtime](../ably-realtime/SKILL.md):** Real-time messages need validation
- **[testing-patterns](../testing-patterns/SKILL.md):** Mock authentication in tests

## Project-Specific Context

### Key Files

- `lib/actions/actionWithAuth.ts` - Authentication wrapper implementations
- `lib/realtime/messageProcessors.ts` - Real-time message validation
- `proxy.ts` - Supabase authentication proxy (Next.js 16)
- `CLAUDE.md` (Security section) - Comprehensive security guidelines

### Project Security Checklist

When creating/modifying features:

- [ ] All server actions use `actionWithAuth` or `rbacWithAuth`
- [ ] Input validation with Zod where applicable
- [ ] No direct database access without RBAC checks
- [ ] Real-time messages validated before processing
- [ ] No secrets in client-side code
- [ ] Role checks enforced server-side
- [ ] Error messages don't leak sensitive info

### Authentication Flow

1. User authenticates via Supabase Auth
2. Middleware validates session
3. Server action checks user ID via `verifySession()`
4. For board operations, verify role via `memberTable`
5. Execute operation if authorized
6. Return serializable data to client

### Common Patterns

**Check Board Ownership:**

```typescript
const isOwner = await db.query.memberTable.findFirst({
  where: and(
    eq(memberTable.boardId, boardId),
    eq(memberTable.userId, userId),
    eq(memberTable.role, "owner")
  ),
});

if (!isOwner) throw new Error("Unauthorized");
```

**Verify Post Ownership:**

```typescript
const post = await db.query.postTable.findFirst({
  where: eq(postTable.id, postId),
});

if (!post) {
  throw new Error("Post not found");
}

if (post.userId !== userId) {
  throw new Error("Not your post");
}
```

---

**Last Updated:** 2026-01-10
