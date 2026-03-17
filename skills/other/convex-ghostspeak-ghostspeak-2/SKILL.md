---
name: convex-expert-2025
description: Expert Convex backend development for December 2025. Use when (1) Building Convex queries, mutations, or actions, (2) Defining schemas and validators, (3) Integrating Convex with React/Next.js, (4) Implementing authentication with Convex Auth or Clerk, (5) Building AI agents with persistent memory, (6) Using file storage, scheduling, or workflows, (7) Optimizing database queries with indexes, or any Convex backend architecture questions.
---

# Convex Expert Guide - December 2025

## What is Convex?

Convex is a full-stack TypeScript backend platform with:
- **Reactive database** - Real-time subscriptions, automatic cache invalidation
- **Serverless functions** - Queries, mutations, actions with TypeScript
- **ACID transactions** - Every mutation is a transaction, automatic conflict resolution
- **Type safety** - End-to-end types from schema to React hooks
- **Built-in features** - Auth, file storage, scheduling, vector search, workflows

## Function Types

| Type | Purpose | Database | External APIs | Deterministic |
|------|---------|----------|---------------|---------------|
| `query` | Read data | ✅ Read | ❌ | ✅ Required |
| `mutation` | Write data | ✅ Read/Write | ❌ | ✅ Required |
| `action` | Side effects | Via `runQuery`/`runMutation` | ✅ | ❌ |
| `httpAction` | HTTP endpoints | Via ctx | ✅ | ❌ |

## Quick Patterns

### Schema Definition
```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    role: v.union(v.literal("admin"), v.literal("user")),
    profileId: v.optional(v.id("profiles")),
  })
    .index("by_email", ["email"])
    .index("by_role", ["role"]),

  messages: defineTable({
    authorId: v.id("users"),
    body: v.string(),
    channel: v.string(),
  })
    .index("by_channel", ["channel"])
    .searchIndex("search_body", { searchField: "body" }),
});
```

### Query
```typescript
// convex/messages.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const list = query({
  args: { channel: v.string(), limit: v.optional(v.number()) },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channel", args.channel))
      .order("desc")
      .take(args.limit ?? 50);
  },
});
```

### Mutation
```typescript
// convex/messages.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const send = mutation({
  args: { body: v.string(), channel: v.string() },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    return await ctx.db.insert("messages", {
      authorId: identity.subject,
      body: args.body,
      channel: args.channel,
    });
  },
});
```

### Action
```typescript
// convex/ai.ts
import { action } from "./_generated/server";
import { v } from "convex/values";
import { api, internal } from "./_generated/api";

export const generateResponse = action({
  args: { prompt: v.string(), threadId: v.id("threads") },
  handler: async (ctx, args) => {
    // Call external API
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` },
      body: JSON.stringify({ model: "gpt-4", messages: [{ role: "user", content: args.prompt }] }),
    });
    const data = await response.json();
    
    // Write result via mutation
    await ctx.runMutation(internal.messages.saveAIResponse, {
      threadId: args.threadId,
      content: data.choices[0].message.content,
    });
  },
});
```

### React Integration
```typescript
// app/page.tsx
"use client";
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

export default function Chat() {
  const messages = useQuery(api.messages.list, { channel: "general" });
  const sendMessage = useMutation(api.messages.send);

  if (messages === undefined) return <div>Loading...</div>;

  return (
    <div>
      {messages.map((msg) => <p key={msg._id}>{msg.body}</p>)}
      <button onClick={() => sendMessage({ body: "Hello!", channel: "general" })}>
        Send
      </button>
    </div>
  );
}
```

## Reference Files

Load based on task:

- **Functions, schema, validators**: See [functions-and-schema.md](references/functions-and-schema.md)
- **Database queries, indexes, pagination**: See [database-patterns.md](references/database-patterns.md)
- **React hooks, Next.js, TanStack Query**: See [client-integration.md](references/client-integration.md)
- **Convex Auth, Clerk, Auth0**: See [authentication.md](references/authentication.md)
- **File storage, cron, scheduling**: See [file-storage-scheduling.md](references/file-storage-scheduling.md)
- **AI agents, vector search, workflows**: See [ai-agents-workflows.md](references/ai-agents-workflows.md)
- **Components, security, optimization**: See [components-best-practices.md](references/components-best-practices.md)

## Core Concepts

### Reactivity
- `useQuery` creates a WebSocket subscription
- UI updates automatically when data changes
- No manual cache invalidation needed
- All subscriptions update atomically

### Determinism
- Queries and mutations must be deterministic
- No `Math.random()`, `Date.now()`, or `fetch` allowed
- Use `_creationTime` instead of `Date.now()`
- Actions are the escape hatch for non-deterministic work

### Transactions
- Every mutation is an ACID transaction
- Automatic optimistic concurrency control
- Retries on conflicts
- No BEGIN/COMMIT needed

### Type Safety
- Schema generates TypeScript types
- `Doc<"tableName">` for document types
- `Id<"tableName">` for ID types
- End-to-end type checking from schema to React

## Validator Reference

| Validator | TypeScript Type | Example |
|-----------|-----------------|---------|
| `v.string()` | `string` | `"hello"` |
| `v.number()` | `number` | `42` |
| `v.boolean()` | `boolean` | `true` |
| `v.null()` | `null` | `null` |
| `v.id("table")` | `Id<"table">` | Document ID |
| `v.array(v.string())` | `string[]` | `["a", "b"]` |
| `v.object({...})` | `{...}` | `{ name: "x" }` |
| `v.optional(v.X())` | `X \| undefined` | Optional field |
| `v.union(v.X(), v.Y())` | `X \| Y` | Union type |
| `v.literal("x")` | `"x"` | Exact value |
| `v.any()` | `any` | Any value |
| `v.bytes()` | `ArrayBuffer` | Binary data |
| `v.record(k, v)` | `Record<K, V>` | Key-value map |

## Decision Framework

### When to Use Each Function Type

```
Need to read data?
├─ Yes → query
│   └─ Need real-time updates? → useQuery (React)
│   └─ One-time fetch? → fetchQuery (Server)
└─ No
    └─ Need to write data?
        ├─ Yes → mutation
        │   └─ Also need external API? → mutation + scheduler.runAfter(0, action)
        └─ No
            └─ Need external API? → action
                └─ Need durability? → Workflow component
```

### Internal vs Public Functions

| Use Case | Function Type |
|----------|---------------|
| Client can call | `query`, `mutation`, `action` |
| Backend only | `internalQuery`, `internalMutation`, `internalAction` |
| Scheduled work | Internal functions |
| Security-sensitive | Internal functions |

## Project Structure

```
my-app/
├── convex/
│   ├── _generated/           # Auto-generated (don't edit)
│   │   ├── api.d.ts
│   │   ├── api.js
│   │   ├── dataModel.d.ts
│   │   └── server.d.ts
│   ├── schema.ts             # Database schema
│   ├── auth.ts               # Auth configuration
│   ├── users.ts              # User functions
│   ├── messages.ts           # Message functions
│   ├── crons.ts              # Scheduled jobs
│   ├── http.ts               # HTTP endpoints
│   └── model/                # Business logic (recommended)
│       ├── users.ts
│       └── messages.ts
├── app/                      # Next.js app
│   ├── ConvexClientProvider.tsx
│   └── page.tsx
└── .env.local
    └── NEXT_PUBLIC_CONVEX_URL=...
```

## CLI Commands

```bash
# Initialize Convex in project
npx convex init

# Start development server (watches for changes)
npx convex dev

# Deploy to production
npx convex deploy

# Open dashboard
npx convex dashboard

# Run a function manually
npx convex run messages:list '{"channel": "general"}'

# Import data
npx convex import --table messages data.json

# Export data
npx convex export --path ./backup
```

## Environment Variables

```bash
# .env.local (development)
NEXT_PUBLIC_CONVEX_URL=https://your-project.convex.cloud

# Set in Convex dashboard for production
OPENAI_API_KEY=sk-...
CLERK_SECRET_KEY=sk_...
```

Access in functions:
```typescript
const apiKey = process.env.OPENAI_API_KEY;
```
