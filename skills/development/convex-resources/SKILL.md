---
name: convex-resources
description: "Use Convex for reactive web app backends. Default for project types C (Web) and F (AI Web). Use when user says 'convex', 'reactive database', 'real-time backend', or building web apps."
allowed-tools: Bash, Read, Write, Edit
---

# Convex Resources

You are an expert at using Convex as a reactive backend for web applications.

## When To Use

- Building web app (project type C or F) - **this is the default**
- User says "convex", "reactive database", "real-time backend"
- Need real-time sync, built-in auth, or TypeScript-first backend
- User says "set up convex", "add convex"
- Migrating from SQLite/Supabase to Convex

## Credentials

```bash
# Decrypt Convex credentials
sops --decrypt ~/github/oneshot/secrets/convex.env.encrypted > .env
source .env
# CONVEX_TEAM_ACCESS_TOKEN and CONVEX_TEAM_ID now available
```

## Quick Setup

### New Project

```bash
npm create convex@latest
# or
npx create-next-app@latest my-app --typescript
cd my-app
npm install convex
npx convex dev
```

### Add to Existing Next.js

```bash
npm install convex
npx convex dev
```

## Provider Setup

Create `app/ConvexClientProvider.tsx`:

```typescript
"use client";

import { ConvexProvider, ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
}
```

Update `app/layout.tsx`:

```typescript
import { ConvexClientProvider } from "./ConvexClientProvider";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ConvexClientProvider>{children}</ConvexClientProvider>
      </body>
    </html>
  );
}
```

---

## Schema Definition

Create `convex/schema.ts`:

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  tasks: defineTable({
    text: v.string(),
    isCompleted: v.boolean(),
    userId: v.optional(v.string()),
  }).index("by_user", ["userId"]),

  messages: defineTable({
    body: v.string(),
    author: v.string(),
    createdAt: v.number(),
  }).index("by_time", ["createdAt"]),
});
```

---

## Query & Mutation Patterns

Create `convex/tasks.ts`:

```typescript
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

// Query - auto-subscribes in React
export const list = query({
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});

// Mutation - transactional write
export const create = mutation({
  args: { text: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("tasks", {
      text: args.text,
      isCompleted: false,
    });
  },
});

export const toggle = mutation({
  args: { id: v.id("tasks") },
  handler: async (ctx, args) => {
    const task = await ctx.db.get(args.id);
    if (!task) throw new Error("Task not found");
    await ctx.db.patch(args.id, { isCompleted: !task.isCompleted });
  },
});
```

---

## React Usage

```typescript
"use client";

import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

export function TaskList() {
  const tasks = useQuery(api.tasks.list);
  const createTask = useMutation(api.tasks.create);
  const toggleTask = useMutation(api.tasks.toggle);

  if (!tasks) return <div>Loading...</div>;

  return (
    <div>
      {tasks.map((task) => (
        <div key={task._id} onClick={() => toggleTask({ id: task._id })}>
          {task.isCompleted ? "✓" : "○"} {task.text}
        </div>
      ))}
      <button onClick={() => createTask({ text: "New task" })}>Add</button>
    </div>
  );
}
```

---

## Authentication

### Clerk Integration (Recommended)

```bash
npm install @clerk/nextjs
```

Create `convex/auth.config.ts`:

```typescript
export default {
  providers: [
    {
      domain: process.env.CLERK_ISSUER_URL,
      applicationID: "convex",
    },
  ],
};
```

Update provider:

```typescript
import { ClerkProvider, useAuth } from "@clerk/nextjs";
import { ConvexProviderWithClerk } from "convex/react-clerk";

export function Providers({ children }) {
  return (
    <ClerkProvider>
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        {children}
      </ConvexProviderWithClerk>
    </ClerkProvider>
  );
}
```

Protected query:

```typescript
export const myData = query({
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthenticated");

    return await ctx.db
      .query("tasks")
      .filter((q) => q.eq(q.field("userId"), identity.subject))
      .collect();
  },
});
```

---

## Actions (External APIs)

```typescript
import { action } from "./_generated/server";
import { v } from "convex/values";

export const callOpenAI = action({
  args: { prompt: v.string() },
  handler: async (ctx, args) => {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-4",
        messages: [{ role: "user", content: args.prompt }],
      }),
    });
    return await response.json();
  },
});
```

---

## File Storage

```typescript
// Generate upload URL
export const generateUploadUrl = mutation(async (ctx) => {
  return await ctx.storage.generateUploadUrl();
});

// Store file reference
export const saveFile = mutation({
  args: { storageId: v.id("_storage"), name: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("files", {
      storageId: args.storageId,
      name: args.name,
    });
  },
});

// Get file URL
export const getFileUrl = query({
  args: { storageId: v.id("_storage") },
  handler: async (ctx, args) => {
    return await ctx.storage.getUrl(args.storageId);
  },
});
```

---

## Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Connect to Vercel
3. Add env: `NEXT_PUBLIC_CONVEX_URL`
4. Deploy - Convex syncs automatically

### Manual

```bash
npx convex deploy
```

---

## Decision Matrix

| Scenario | Convex | SQLite | Supabase |
|----------|--------|--------|----------|
| Web app (type C/F) | **Default** | OK | OK |
| Real-time features | Best | No | OK |
| TypeScript-first | Best | N/A | OK |
| Built-in auth | Yes | No | Yes |
| CLI/library | No | Best | No |
| Self-hosting required | No | Yes | Yes |
| Complex SQL/joins | No | OK | Best |
| Offline-first | Best | OK | No |

## Free Tier Limits

- 500K function calls/month
- 16M queries/month
- 1GB storage
- Built-in auth included
- Unlimited projects

---

## Verification

```bash
# Check Convex CLI
npx convex --version

# Start dev server
npx convex dev

# Open dashboard
npx convex dashboard
```

---

## Anti-Patterns

- Using Convex for CLI tools (use SQLite)
- Storing API keys in client code (use Actions with server env)
- Not using TypeScript (loses type safety)
- Polling instead of subscriptions (Convex is reactive)
- Complex SQL-style joins (use denormalization)

---

## Related Skills

- `oneshot-core`: Project creation (defaults to Convex for web apps)
- `secrets-vault-manager`: Decrypt Convex credentials
- `push-to-cloud`: Deploy Convex apps to OCI/Vercel

## Keywords

convex, reactive, real-time, typescript, backend, database, web app, next.js, react, clerk, auth, subscriptions
