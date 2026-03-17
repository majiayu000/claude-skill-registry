---
name: convex-security-check
displayName: Convex Security Check
description: Quick security audit checklist covering authentication, function exposure, argument validation, row-level access control, and environment variable handling
version: 1.0.0
author: Convex
tags: [convex, security, authentication, authorization, checklist]
---

# Convex Security Check

A quick security audit checklist for Convex applications covering authentication, function exposure, argument validation, row-level access control, and environment variable handling.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/auth
- Production Security: https://docs.convex.dev/production
- Functions Auth: https://docs.convex.dev/auth/functions-auth
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### Security Checklist

Use this checklist to quickly audit your Convex application's security:

#### 1. Authentication

- [ ] Authentication provider configured (Clerk, Auth0, etc.)
- [ ] All sensitive queries check `ctx.auth.getUserIdentity()`
- [ ] Unauthenticated access explicitly allowed where intended
- [ ] Session tokens properly validated

#### 2. Function Exposure

- [ ] Public functions (`query`, `mutation`, `action`) reviewed
- [ ] Internal functions use `internalQuery`, `internalMutation`, `internalAction`
- [ ] No sensitive operations exposed as public functions
- [ ] HTTP actions validate origin/authentication

#### 3. Argument Validation

- [ ] All functions have explicit `args` validators
- [ ] All functions have explicit `returns` validators
- [ ] No `v.any()` used for sensitive data
- [ ] ID validators use correct table names

#### 4. Row-Level Access Control

- [ ] Users can only access their own data
- [ ] Admin functions check user roles
- [ ] Shared resources have proper access checks
- [ ] Deletion functions verify ownership

#### 5. Environment Variables

- [ ] API keys stored in environment variables
- [ ] No secrets in code or schema
- [ ] Different keys for dev/prod environments
- [ ] Environment variables accessed only in actions

### Authentication Check

```typescript
// convex/auth.ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";
import { ConvexError } from "convex/values";

// Helper to require authentication
async function requireAuth(ctx: QueryCtx | MutationCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) {
    throw new ConvexError("Authentication required");
  }
  return identity;
}

// Secure query pattern
export const getMyProfile = query({
  args: {},
  returns: v.union(v.object({
    _id: v.id("users"),
    name: v.string(),
    email: v.string(),
  }), v.null()),
  handler: async (ctx) => {
    const identity = await requireAuth(ctx);
    
    return await ctx.db
      .query("users")
      .withIndex("by_tokenIdentifier", (q) => 
        q.eq("tokenIdentifier", identity.tokenIdentifier)
      )
      .unique();
  },
});
```

### Function Exposure Check

```typescript
// PUBLIC - Exposed to clients (review carefully!)
export const listPublicPosts = query({
  args: {},
  returns: v.array(v.object({ /* ... */ })),
  handler: async (ctx) => {
    // Anyone can call this - intentionally public
    return await ctx.db
      .query("posts")
      .withIndex("by_public", (q) => q.eq("isPublic", true))
      .collect();
  },
});

// INTERNAL - Only callable from other Convex functions
export const _updateUserCredits = internalMutation({
  args: { userId: v.id("users"), amount: v.number() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // This cannot be called directly from clients
    await ctx.db.patch(args.userId, {
      credits: args.amount,
    });
    return null;
  },
});
```

### Argument Validation Check

```typescript
// GOOD: Strict validation
export const createPost = mutation({
  args: {
    title: v.string(),
    content: v.string(),
    category: v.union(
      v.literal("tech"),
      v.literal("news"),
      v.literal("other")
    ),
  },
  returns: v.id("posts"),
  handler: async (ctx, args) => {
    const identity = await requireAuth(ctx);
    return await ctx.db.insert("posts", {
      ...args,
      authorId: identity.tokenIdentifier,
    });
  },
});

// BAD: Weak validation
export const createPostUnsafe = mutation({
  args: {
    data: v.any(), // DANGEROUS: Allows any data
  },
  returns: v.id("posts"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("posts", args.data);
  },
});
```

### Row-Level Access Control Check

```typescript
// Verify ownership before update
export const updateTask = mutation({
  args: {
    taskId: v.id("tasks"),
    title: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const identity = await requireAuth(ctx);
    
    const task = await ctx.db.get(args.taskId);
    
    // Check ownership
    if (!task || task.userId !== identity.tokenIdentifier) {
      throw new ConvexError("Not authorized to update this task");
    }
    
    await ctx.db.patch(args.taskId, { title: args.title });
    return null;
  },
});

// Verify ownership before delete
export const deleteTask = mutation({
  args: { taskId: v.id("tasks") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const identity = await requireAuth(ctx);
    
    const task = await ctx.db.get(args.taskId);
    
    if (!task || task.userId !== identity.tokenIdentifier) {
      throw new ConvexError("Not authorized to delete this task");
    }
    
    await ctx.db.delete(args.taskId);
    return null;
  },
});
```

### Environment Variables Check

```typescript
// convex/actions.ts
"use node";

import { action } from "./_generated/server";
import { v } from "convex/values";

export const sendEmail = action({
  args: {
    to: v.string(),
    subject: v.string(),
    body: v.string(),
  },
  returns: v.object({ success: v.boolean() }),
  handler: async (ctx, args) => {
    // Access API key from environment
    const apiKey = process.env.RESEND_API_KEY;
    
    if (!apiKey) {
      throw new Error("RESEND_API_KEY not configured");
    }
    
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: "noreply@example.com",
        to: args.to,
        subject: args.subject,
        html: args.body,
      }),
    });
    
    return { success: response.ok };
  },
});
```

## Examples

### Complete Security Pattern

```typescript
// convex/secure.ts
import { query, mutation, internalMutation } from "./_generated/server";
import { v } from "convex/values";
import { ConvexError } from "convex/values";

// Authentication helper
async function getAuthenticatedUser(ctx: QueryCtx | MutationCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) {
    throw new ConvexError({
      code: "UNAUTHENTICATED",
      message: "You must be logged in",
    });
  }
  
  const user = await ctx.db
    .query("users")
    .withIndex("by_tokenIdentifier", (q) => 
      q.eq("tokenIdentifier", identity.tokenIdentifier)
    )
    .unique();
    
  if (!user) {
    throw new ConvexError({
      code: "USER_NOT_FOUND",
      message: "User profile not found",
    });
  }
  
  return user;
}

// Check admin role
async function requireAdmin(ctx: QueryCtx | MutationCtx) {
  const user = await getAuthenticatedUser(ctx);
  
  if (user.role !== "admin") {
    throw new ConvexError({
      code: "FORBIDDEN",
      message: "Admin access required",
    });
  }
  
  return user;
}

// Public: List own tasks
export const listMyTasks = query({
  args: {},
  returns: v.array(v.object({
    _id: v.id("tasks"),
    title: v.string(),
    completed: v.boolean(),
  })),
  handler: async (ctx) => {
    const user = await getAuthenticatedUser(ctx);
    
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", user._id))
      .collect();
  },
});

// Admin only: List all users
export const listAllUsers = query({
  args: {},
  returns: v.array(v.object({
    _id: v.id("users"),
    name: v.string(),
    role: v.string(),
  })),
  handler: async (ctx) => {
    await requireAdmin(ctx);
    
    return await ctx.db.query("users").collect();
  },
});

// Internal: Update user role (never exposed)
export const _setUserRole = internalMutation({
  args: {
    userId: v.id("users"),
    role: v.union(v.literal("user"), v.literal("admin")),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(args.userId, { role: args.role });
    return null;
  },
});
```

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Always verify user identity before returning sensitive data
- Use internal functions for sensitive operations
- Validate all arguments with strict validators
- Check ownership before update/delete operations
- Store API keys in environment variables
- Review all public functions for security implications

## Common Pitfalls

1. **Missing authentication checks** - Always verify identity
2. **Exposing internal operations** - Use internalMutation/Query
3. **Trusting client-provided IDs** - Verify ownership
4. **Using v.any() for arguments** - Use specific validators
5. **Hardcoding secrets** - Use environment variables

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- Authentication: https://docs.convex.dev/auth
- Production Security: https://docs.convex.dev/production
- Functions Auth: https://docs.convex.dev/auth/functions-auth
