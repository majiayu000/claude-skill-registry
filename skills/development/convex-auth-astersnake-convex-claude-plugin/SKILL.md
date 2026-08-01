---
name: convex-auth
description: Convex Auth - authentication, user management, protected functions, and
  session handling
---

---
name: convex-auth
description: Convex Auth - authentication, user management, protected functions, and session handling
globs:
  - "convex/**/*.ts"
  - "convex/auth.ts"
  - "**/*auth*.ts"
  - "**/*auth*.tsx"
triggers:
  - getAuthUserId
  - authentication
  - authenticated
  - login
  - logout
  - protected
  - authTables
  - @convex-dev/auth
  - loggedInUser
  - currentUser
  - session
  - user permission
---

# Convex Auth Server Guidelines

## Getting the Authenticated User ID

When writing Convex handlers, use the `getAuthUserId` function to get the logged in user's ID. You can then pass this to `ctx.db.get` in queries or mutations to get the user's data.

**IMPORTANT:** You can only use this within the `convex/` directory.

```typescript
// convex/users.ts
import { getAuthUserId } from "@convex-dev/auth/server";
import { query } from "./_generated/server";

export const currentLoggedInUser = query({
  args: {},
  returns: v.union(v.null(), v.object({
    _id: v.id("users"),
    name: v.optional(v.string()),
    email: v.optional(v.string()),
    image: v.optional(v.string()),
  })),
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return null;
    }
    const user = await ctx.db.get(userId);
    if (!user) {
      return null;
    }
    console.log("User", user.name, user.image, user.email);
    return user;
  }
});
```

---

# Logged In User Query

If you want to get the current logged in user's data on the frontend, use this function defined in `convex/auth.ts`:

```typescript
// convex/auth.ts
import { getAuthUserId } from "@convex-dev/auth/server";
import { query } from "./_generated/server";

export const loggedInUser = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return null;
    }
    const user = await ctx.db.get(userId);
    if (!user) {
      return null;
    }
    return user;
  },
});
```

Then use the `loggedInUser` query in your React component:

```tsx
// src/App.tsx
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function App() {
  const user = useQuery(api.auth.loggedInUser);

  if (user === undefined) {
    return <div>Loading...</div>;
  }

  if (user === null) {
    return <div>Not logged in</div>;
  }

  return <div>Welcome, {user.name}!</div>;
}
```

---

# Users Table Schema

The "users" table within `authTables` has this schema:

```typescript
const users = defineTable({
  name: v.optional(v.string()),
  image: v.optional(v.string()),
  email: v.optional(v.string()),
  emailVerificationTime: v.optional(v.number()),
  phone: v.optional(v.string()),
  phoneVerificationTime: v.optional(v.number()),
  isAnonymous: v.optional(v.boolean()),
})
  .index("email", ["email"])
  .index("phone", ["phone"]);
```

---

# Schema with Auth Tables

When defining your schema with authentication, always spread `authTables`:

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";
import { authTables } from "@convex-dev/auth/server";

const applicationTables = {
  // Your application tables here
  posts: defineTable({
    authorId: v.id("users"),
    title: v.string(),
    content: v.string(),
  }).index("by_author", ["authorId"]),
};

export default defineSchema({
  ...authTables,
  ...applicationTables,
});
```

---

# Protected Mutations and Queries

## Pattern for Protected Functions

Create a helper function to get the logged-in user and throw if not authenticated:

```typescript
// convex/utils.ts
import { getAuthUserId } from "@convex-dev/auth/server";
import { QueryCtx, MutationCtx } from "./_generated/server";
import { Doc } from "./_generated/dataModel";

export async function getLoggedInUser(ctx: QueryCtx | MutationCtx): Promise<Doc<"users">> {
  const userId = await getAuthUserId(ctx);
  if (!userId) {
    throw new Error("Not authenticated");
  }
  const user = await ctx.db.get(userId);
  if (!user) {
    throw new Error("User not found");
  }
  return user;
}

export async function getLoggedInUserOrNull(ctx: QueryCtx | MutationCtx): Promise<Doc<"users"> | null> {
  const userId = await getAuthUserId(ctx);
  if (!userId) {
    return null;
  }
  return await ctx.db.get(userId);
}
```

## Using the Helper

```typescript
// convex/posts.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { getLoggedInUser } from "./utils";

export const createPost = mutation({
  args: {
    title: v.string(),
    content: v.string(),
  },
  returns: v.id("posts"),
  handler: async (ctx, args) => {
    const user = await getLoggedInUser(ctx);

    return await ctx.db.insert("posts", {
      authorId: user._id,
      title: args.title,
      content: args.content,
    });
  },
});

export const myPosts = query({
  args: {},
  handler: async (ctx) => {
    const user = await getLoggedInUser(ctx);

    return await ctx.db
      .query("posts")
      .withIndex("by_author", (q) => q.eq("authorId", user._id))
      .collect();
  },
});
```

---

# Auth in Scheduled Jobs

**CRITICAL:** Auth state does NOT propagate to scheduled jobs. `getAuthUserId()` and `ctx.getUserIdentity()` will ALWAYS return `null` from within a scheduled job.

## Solution: Pass User ID Explicitly

```typescript
// convex/tasks.ts
import { mutation, internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";
import { getAuthUserId } from "@convex-dev/auth/server";

export const scheduleTask = mutation({
  args: { taskData: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }

    // Pass the userId to the scheduled function
    await ctx.scheduler.runAfter(0, internal.tasks.processTask, {
      userId,
      taskData: args.taskData,
    });

    return null;
  },
});

export const processTask = internalMutation({
  args: {
    userId: v.id("users"),
    taskData: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Use the passed userId instead of getAuthUserId
    const user = await ctx.db.get(args.userId);
    if (!user) {
      throw new Error("User not found");
    }

    // Process the task with user context
    console.log(`Processing task for user: ${user.name}`);

    return null;
  },
});
```

---

# HTTP Endpoints with Auth

## Auth Handler Setup

The auth handler should be in `convex/http.ts`:

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { auth } from "./auth";

const http = httpRouter();

auth.addHttpRoutes(http);

export default http;
```

## Custom HTTP Endpoints (in convex/router.ts)

Define new HTTP endpoints in a separate file to avoid modifying the auth handler:

```typescript
// convex/router.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const router = httpRouter();

router.route({
  path: "/api/webhook",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    // Handle webhook
    const body = await req.json();
    return new Response(JSON.stringify({ received: true }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }),
});

export default router;
```

---

# Anonymous Users

Always make sure your UIs work well with anonymous users:

```tsx
// src/components/UserProfile.tsx
import { useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";

export function UserProfile() {
  const user = useQuery(api.auth.loggedInUser);

  // Loading state
  if (user === undefined) {
    return <div className="animate-pulse">Loading...</div>;
  }

  // Anonymous / not logged in
  if (user === null) {
    return (
      <div>
        <p>Welcome, Guest!</p>
        <button>Sign In</button>
      </div>
    );
  }

  // Logged in user
  return (
    <div>
      {user.image && <img src={user.image} alt={user.name || "User"} />}
      <p>Welcome, {user.name || user.email || "User"}!</p>
    </div>
  );
}
```

---

# Extending the Users Table

If you need to add more fields to the users table, you can extend it in your schema:

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";
import { authTables } from "@convex-dev/auth/server";

// Extend the users table with additional fields
const extendedAuthTables = {
  ...authTables,
  users: defineTable({
    // Original auth fields
    name: v.optional(v.string()),
    image: v.optional(v.string()),
    email: v.optional(v.string()),
    emailVerificationTime: v.optional(v.number()),
    phone: v.optional(v.string()),
    phoneVerificationTime: v.optional(v.number()),
    isAnonymous: v.optional(v.boolean()),
    // Your custom fields
    role: v.optional(v.union(v.literal("admin"), v.literal("user"))),
    bio: v.optional(v.string()),
    preferences: v.optional(v.object({
      theme: v.union(v.literal("light"), v.literal("dark")),
      notifications: v.boolean(),
    })),
  })
    .index("email", ["email"])
    .index("phone", ["phone"])
    .index("by_role", ["role"]),
};

export default defineSchema({
  ...extendedAuthTables,
  // Your other tables
});
```

---

# Best Practices

## 1. Always Check Authentication First

```typescript
export const sensitiveQuery = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Authentication required");
    }
    // Continue with authenticated logic
  },
});
```

## 2. Use Internal Functions for Privileged Operations

```typescript
// Public mutation that checks auth
export const deleteAccount = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }

    // Call internal function for the actual deletion
    await ctx.runMutation(internal.users.deleteUserData, { userId });
    return null;
  },
});

// Internal mutation that doesn't check auth (already verified)
export const deleteUserData = internalMutation({
  args: { userId: v.id("users") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Delete user's data
    const posts = await ctx.db
      .query("posts")
      .withIndex("by_author", (q) => q.eq("authorId", args.userId))
      .collect();

    for (const post of posts) {
      await ctx.db.delete(post._id);
    }

    return null;
  },
});
```

## 3. Handle Loading States Properly

```tsx
function ProtectedComponent() {
  const user = useQuery(api.auth.loggedInUser);

  // IMPORTANT: Check for undefined (loading) before null (not authenticated)
  if (user === undefined) {
    return <LoadingSpinner />;
  }

  if (user === null) {
    return <Navigate to="/login" />;
  }

  return <Dashboard user={user} />;
}
```
