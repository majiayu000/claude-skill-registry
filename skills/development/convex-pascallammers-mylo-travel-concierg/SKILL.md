---
name: convex
description: PROACTIVELY USED for Convex backend development. Auto-invokes when user mentions "Convex", "convex functions", "queries", "mutations", "actions", or working with Convex backend. Ensures correct patterns for queries, mutations, actions, schema design, and reactivity. Handles the complete development lifecycle from schema to deployment.
allowed-tools: Read, Bash, Edit, Grep, Glob, TodoWrite, WebFetch, mcp__exa__get_code_context_exa, mcp__Ref__ref_search_documentation
---

# Convex Development Expert Skill

You are the **Convex Development Expert**. You ensure correct usage of Convex for building reactive, real-time backends with TypeScript. You guide users through the complete development lifecycle while following Convex best practices and the "Zen of Convex."

## When You Activate

### Automatic Triggers
- User mentions "Convex", "convex functions", or "convex backend"
- User mentions "queries", "mutations", or "actions" in Convex context
- User asks about real-time database, reactive queries, or subscriptions
- User needs help with schema design, indexes, or validators
- User mentions "ctx.db", "useQuery", "useMutation", or Convex React hooks
- User asks about file storage, authentication, or scheduling in Convex
- User needs to implement HTTP endpoints or webhooks with Convex

### Complexity Indicators
```
✅ Use Convex when:
- Building real-time, reactive applications
- Need automatic data synchronization across clients
- Want type-safe backend functions with TypeScript
- Building collaborative apps, dashboards, or live feeds
- Need built-in authentication and file storage
- Want serverless backend without infrastructure management

❌ Don't use Convex when:
- Need complex SQL joins or analytics queries
- Require complete control over database infrastructure
- Building static sites with no real-time requirements
- Need specific database features (PostGIS, full-text search beyond basic)
```

## The Zen of Convex

### Core Principles

**1. Embrace Reactivity**
Convex's sync engine is the foundation. Queries automatically re-run when data changes. Design your application around this reactive model for best results.

**2. Query-First Pattern**
Use queries for nearly all data reads. They're:
- Automatically cached
- Reactive (re-run on data changes)
- Consistent (read from a single snapshot)
- Resilient (automatically retry)

**3. Keep Functions Lean**
- Queries and mutations should complete in < 100ms
- Process fewer than several hundred records per function
- Use pagination for large datasets
- Denormalize data when needed for performance

**4. Minimize Client State**
Let Convex handle data state. Use React `useState` only for:
- Form input values
- UI state (modals, dropdowns, toggles)
- Temporary local state

Don't use `useState` for:
- Data from database
- Loading/error states (Convex handles this)
- Data shared across components

**5. "Just Code" Composition**
Build abstractions using standard TypeScript patterns. Create helper functions, shared utilities, and composition layers with plain code.

**6. Actions as Workflows**
Think in effect chains: `action → mutation → action → mutation`
- Actions call external APIs
- Mutations write to database
- Chain them for complex workflows

## Function Types Deep Dive

### Queries: Reading Data

**Purpose:** Read data from the database reactively. Queries re-run automatically when underlying data changes.

**Characteristics:**
- Read-only (cannot write to database)
- Automatically cached
- Run in V8 isolate (no Node.js APIs)
- Transactional (consistent snapshot)
- Fast (< 100ms target)

**When to Use:**
- Fetching data for UI display
- Loading user profiles, posts, messages
- Filtering, sorting, aggregating data
- Any read operation that should react to changes

**Pattern:**
```typescript
import { query } from "./_generated/server";
import { v } from "convex/values";

export const listTasks = query({
  args: {
    userId: v.id("users"),
    status: v.optional(v.union(v.literal("pending"), v.literal("completed")))
  },
  returns: v.array(v.object({
    _id: v.id("tasks"),
    _creationTime: v.number(),
    title: v.string(),
    status: v.string(),
    userId: v.id("users")
  })),
  handler: async (ctx, args) => {
    let query = ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", args.userId));

    if (args.status) {
      query = query.filter((q) => q.eq(q.field("status"), args.status));
    }

    return await query.order("desc").collect();
  },
});
```

**Best Practices:**
- Always use `.withIndex()` instead of `.filter()` when possible
- Use `.take(n)` or pagination for large result sets
- Return only data needed by the client
- Use `.unique()` when expecting single result
- Add proper validators for args and returns

### Mutations: Writing Data

**Purpose:** Write data to the database. Mutations are transactional and atomic.

**Characteristics:**
- Can read and write to database
- Transactional (all-or-nothing)
- Run in V8 isolate (no Node.js APIs)
- Can schedule actions
- Fast (< 100ms target)

**When to Use:**
- Creating, updating, or deleting records
- Any operation that changes database state
- Scheduling background jobs
- Operations requiring atomicity

**Pattern:**
```typescript
import { mutation } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const createTask = mutation({
  args: {
    title: v.string(),
    description: v.optional(v.string()),
    userId: v.id("users"),
  },
  returns: v.id("tasks"),
  handler: async (ctx, args) => {
    // Verify user exists
    const user = await ctx.db.get(args.userId);
    if (!user) {
      throw new Error("User not found");
    }

    // Create task
    const taskId = await ctx.db.insert("tasks", {
      title: args.title,
      description: args.description ?? "",
      status: "pending" as const,
      userId: args.userId,
      createdAt: Date.now(),
    });

    // Schedule notification action
    await ctx.scheduler.runAfter(0, internal.notifications.sendTaskCreated, {
      taskId,
      userId: args.userId,
    });

    return taskId;
  },
});

export const updateTask = mutation({
  args: {
    taskId: v.id("tasks"),
    title: v.optional(v.string()),
    status: v.optional(v.union(v.literal("pending"), v.literal("completed"))),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const { taskId, ...updates } = args;

    // Verify task exists
    const task = await ctx.db.get(taskId);
    if (!task) {
      throw new Error("Task not found");
    }

    // Update task
    await ctx.db.patch(taskId, updates);

    return null;
  },
});

export const deleteTask = mutation({
  args: { taskId: v.id("tasks") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.delete(args.taskId);
    return null;
  },
});
```

**Best Practices:**
- Validate inputs thoroughly
- Check auth with `ctx.auth.getUserIdentity()`
- Verify related records exist before operations
- Use `ctx.db.patch()` for partial updates
- Use `ctx.db.replace()` for full replacement
- Return IDs or minimal data (queries handle display)
- Schedule actions for side effects

### Actions: External Operations

**Purpose:** Interact with external services, APIs, or perform Node.js operations.

**Characteristics:**
- Can call external APIs (fetch, OpenAI, etc.)
- Access to Node.js runtime
- Can call queries and mutations via `ctx.runQuery/Mutation`
- Non-transactional
- Can be long-running (up to 10 minutes)

**When to Use:**
- Calling external APIs (OpenAI, Stripe, Twilio)
- Sending emails or SMS
- Processing files or images
- Complex workflows with external dependencies
- Background jobs

**Pattern:**
```typescript
"use node";

import { action } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";
import OpenAI from "openai";

const openai = new OpenAI();

export const generateTaskSuggestions = action({
  args: {
    userId: v.id("users"),
    context: v.string(),
  },
  returns: v.array(v.string()),
  handler: async (ctx, args) => {
    // Load context from database via query
    const user = await ctx.runQuery(internal.users.getUser, {
      userId: args.userId,
    });

    if (!user) {
      throw new Error("User not found");
    }

    // Call external API
    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        {
          role: "system",
          content: "Generate task suggestions based on user context.",
        },
        {
          role: "user",
          content: `User: ${user.name}, Context: ${args.context}`,
        },
      ],
    });

    const suggestions = response.choices[0].message.content
      ?.split("\n")
      .filter(s => s.trim()) ?? [];

    // Store results via mutation
    await ctx.runMutation(internal.tasks.saveSuggestions, {
      userId: args.userId,
      suggestions,
    });

    return suggestions;
  },
});
```

**Best Practices:**
- Add `"use node";` at top of file for Node.js APIs
- Never access `ctx.db` directly in actions
- Use `ctx.runQuery` to read data
- Use `ctx.runMutation` to write data
- Minimize calls to queries/mutations (avoid N+1 patterns)
- Use plain TypeScript functions instead of `ctx.runAction` unless crossing runtimes
- Handle errors gracefully
- Consider retry logic for external APIs

### Internal Functions

**Purpose:** Private functions only callable by other Convex functions, not clients.

**When to Use:**
- Sensitive operations (admin functions)
- Helper functions called by other functions
- Scheduled jobs (cron)
- Functions triggered by actions

**Pattern:**
```typescript
import { internalQuery, internalMutation, internalAction } from "./_generated/server";
import { v } from "convex/values";

export const getUserByEmail = internalQuery({
  args: { email: v.string() },
  returns: v.union(
    v.object({
      _id: v.id("users"),
      name: v.string(),
      email: v.string(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("users")
      .withIndex("by_email", (q) => q.eq("email", args.email))
      .unique();
  },
});

export const sendTaskCreated = internalAction({
  args: {
    taskId: v.id("tasks"),
    userId: v.id("users"),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Send notification via external service
    // Implementation here
    return null;
  },
});
```

**Best Practices:**
- Use for all sensitive operations
- Use for cron jobs
- Use for scheduler callbacks
- Never expose sensitive data via public functions

## Schema Design

### Schema Structure

**Location:** Always define schema in `convex/schema.ts`

**Pattern:**
```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    avatarUrl: v.optional(v.string()),
    role: v.union(v.literal("user"), v.literal("admin")),
    settings: v.object({
      notifications: v.boolean(),
      theme: v.union(v.literal("light"), v.literal("dark")),
    }),
  })
    .index("by_email", ["email"])
    .index("by_role", ["role"]),

  tasks: defineTable({
    title: v.string(),
    description: v.string(),
    status: v.union(
      v.literal("pending"),
      v.literal("in_progress"),
      v.literal("completed")
    ),
    userId: v.id("users"),
    priority: v.number(),
    dueDate: v.optional(v.number()),
    tags: v.array(v.string()),
  })
    .index("by_user", ["userId"])
    .index("by_user_and_status", ["userId", "status"])
    .index("by_status_and_priority", ["status", "priority"])
    .searchIndex("search_title", {
      searchField: "title",
      filterFields: ["userId", "status"],
    }),

  comments: defineTable({
    taskId: v.id("tasks"),
    authorId: v.id("users"),
    content: v.string(),
    parentId: v.optional(v.id("comments")),
  })
    .index("by_task", ["taskId"])
    .index("by_task_and_parent", ["taskId", "parentId"]),
});
```

### Index Design

**Principles:**
- Always use indexes for queries (avoid `.filter()`)
- Index fields must be queried in order
- Name indexes descriptively: `by_field1_and_field2`
- Create composite indexes for common query patterns
- Avoid redundant indexes

**Examples:**
```typescript
// Good: Specific, useful index
.index("by_user_and_status", ["userId", "status"])

// Query usage (must query in order)
ctx.db
  .query("tasks")
  .withIndex("by_user_and_status", (q) =>
    q.eq("userId", userId).eq("status", "pending")
  )

// Can also query partial index
ctx.db
  .query("tasks")
  .withIndex("by_user_and_status", (q) => q.eq("userId", userId))

// Bad: Redundant indexes
.index("by_user", ["userId"])
.index("by_user_and_status", ["userId", "status"])
// First index is redundant - second can handle both cases
```

### Validators Reference

```typescript
// Primitives
v.null()           // null
v.number()         // Float64
v.int64()          // BigInt (-2^63 to 2^63-1)
v.boolean()        // boolean
v.string()         // string
v.bytes()          // ArrayBuffer

// IDs
v.id("tableName")  // Id<"tableName">

// Containers
v.array(v.string())                    // Array<string>
v.object({ name: v.string() })         // { name: string }
v.record(v.string(), v.number())       // Record<string, number>

// Optionals and Unions
v.optional(v.string())                 // string | undefined
v.union(v.string(), v.number())        // string | number
v.literal("pending")                   // "pending" (literal type)

// Complex types
v.union(
  v.object({
    kind: v.literal("error"),
    message: v.string(),
  }),
  v.object({
    kind: v.literal("success"),
    data: v.any(),
  })
)
```

### System Fields

Every document automatically has:
- `_id: Id<"tableName">` - Unique document ID
- `_creationTime: number` - Timestamp when created

```typescript
// No need to define these in schema
// They're automatically available

const doc = await ctx.db.get(id);
console.log(doc._id);           // Id<"tasks">
console.log(doc._creationTime); // number (milliseconds)
```

## Query Patterns

### Basic Query

```typescript
// Get all documents
const tasks = await ctx.db.query("tasks").collect();

// With index
const userTasks = await ctx.db
  .query("tasks")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .collect();

// With ordering
const recentTasks = await ctx.db
  .query("tasks")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .order("desc")  // or "asc"
  .take(10);

// Single document
const task = await ctx.db
  .query("tasks")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .unique();  // Throws if 0 or >1 results

// Single document (returns null if not found)
const task = await ctx.db
  .query("tasks")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .first();  // Returns null if no results
```

### Pagination

```typescript
import { paginationOptsValidator } from "convex/server";

export const listTasks = query({
  args: {
    userId: v.id("users"),
    paginationOpts: paginationOptsValidator,
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .paginate(args.paginationOpts);
  },
});

// Returns:
// {
//   page: Array<Doc<"tasks">>,
//   isDone: boolean,
//   continueCursor: string
// }
```

**Client usage:**
```typescript
const { results, status, loadMore } = usePaginatedQuery(
  api.tasks.listTasks,
  { userId: "..." },
  { initialNumItems: 20 }
);
```

### Full-Text Search

```typescript
// Schema
tasks: defineTable({
  title: v.string(),
  userId: v.id("users"),
  status: v.string(),
}).searchIndex("search_title", {
  searchField: "title",
  filterFields: ["userId", "status"],
})

// Query
export const searchTasks = query({
  args: {
    query: v.string(),
    userId: v.id("users"),
    status: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    let searchQuery = ctx.db
      .query("tasks")
      .withSearchIndex("search_title", (q) =>
        q.search("title", args.query).eq("userId", args.userId)
      );

    if (args.status) {
      searchQuery = searchQuery.eq("status", args.status);
    }

    return await searchQuery.take(10);
  },
});
```

### Async Iteration

```typescript
// For processing large datasets
for await (const task of ctx.db
  .query("tasks")
  .withIndex("by_status", (q) => q.eq("status", "pending"))
) {
  // Process each task
  await ctx.db.patch(task._id, { status: "processing" });
}
```

### Deleting Query Results

```typescript
// Convex queries don't support .delete()
// Must collect and iterate

const tasksToDelete = await ctx.db
  .query("tasks")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .collect();

for (const task of tasksToDelete) {
  await ctx.db.delete(task._id);
}
```

## Database Operations

### Create (Insert)

```typescript
const taskId = await ctx.db.insert("tasks", {
  title: "New task",
  userId: userId,
  status: "pending" as const,
});
// Returns: Id<"tasks">
```

### Read (Get)

```typescript
const task = await ctx.db.get(taskId);
// Returns: Doc<"tasks"> | null
```

### Update (Patch)

```typescript
// Shallow merge
await ctx.db.patch(taskId, {
  status: "completed" as const,
  completedAt: Date.now(),
});

// Throws if document doesn't exist
```

### Replace

```typescript
// Full replacement (must include all fields)
await ctx.db.replace(taskId, {
  title: "Updated task",
  userId: userId,
  status: "pending" as const,
  // Must include all required fields
});

// Throws if document doesn't exist
```

### Delete

```typescript
await ctx.db.delete(taskId);
// Throws if document doesn't exist
```

## React Integration

### useQuery Hook

```typescript
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function TaskList({ userId }: { userId: Id<"users"> }) {
  const tasks = useQuery(api.tasks.listTasks, { userId });

  // tasks is undefined while loading
  if (tasks === undefined) {
    return <div>Loading...</div>;
  }

  // Automatically re-renders when data changes!
  return (
    <ul>
      {tasks.map(task => (
        <li key={task._id}>{task.title}</li>
      ))}
    </ul>
  );
}
```

### useMutation Hook

```typescript
import { useMutation } from "convex/react";
import { api } from "../convex/_generated/api";
import { useState } from "react";

function CreateTask({ userId }: { userId: Id<"users"> }) {
  const [title, setTitle] = useState("");
  const createTask = useMutation(api.tasks.createTask);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Fire and forget
    createTask({ title, userId });

    // OR wait for result
    const taskId = await createTask({ title, userId });
    console.log("Created task:", taskId);

    setTitle("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <button type="submit">Create Task</button>
    </form>
  );
}
```

### useAction Hook

```typescript
import { useAction } from "convex/react";
import { api } from "../convex/_generated/api";

function AITaskSuggestions({ userId }: { userId: Id<"users"> }) {
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const generateSuggestions = useAction(api.tasks.generateTaskSuggestions);

  const handleGenerate = async () => {
    const results = await generateSuggestions({
      userId,
      context: "work projects",
    });
    setSuggestions(results);
  };

  return (
    <div>
      <button onClick={handleGenerate}>Generate AI Suggestions</button>
      <ul>
        {suggestions.map((s, i) => <li key={i}>{s}</li>)}
      </ul>
    </div>
  );
}
```

## Authentication

### Setup

```typescript
// convex/auth.config.ts
export default {
  providers: [
    {
      domain: process.env.CLERK_DOMAIN,
      applicationID: "convex",
    },
  ],
};
```

### Checking Auth

```typescript
export const createTask = mutation({
  args: { title: v.string() },
  handler: async (ctx, args) => {
    // Get authenticated user
    const identity = await ctx.auth.getUserIdentity();

    if (!identity) {
      throw new Error("Unauthenticated");
    }

    // identity contains:
    // - tokenIdentifier: string
    // - subject: string
    // - email?: string
    // - name?: string

    // Look up user in your schema
    const user = await ctx.db
      .query("users")
      .withIndex("by_token", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier)
      )
      .unique();

    if (!user) {
      throw new Error("User not found");
    }

    // Use authenticated user ID
    return await ctx.db.insert("tasks", {
      title: args.title,
      userId: user._id,
    });
  },
});
```

### Helper Pattern

```typescript
// convex/lib/auth.ts
export async function requireUser(ctx: QueryCtx | MutationCtx) {
  const identity = await ctx.auth.getUserIdentity();

  if (!identity) {
    throw new Error("Unauthenticated");
  }

  const user = await ctx.db
    .query("users")
    .withIndex("by_token", (q) =>
      q.eq("tokenIdentifier", identity.tokenIdentifier)
    )
    .unique();

  if (!user) {
    throw new Error("User not found");
  }

  return user;
}

// Usage
export const createTask = mutation({
  args: { title: v.string() },
  handler: async (ctx, args) => {
    const user = await requireUser(ctx);

    return await ctx.db.insert("tasks", {
      title: args.title,
      userId: user._id,
    });
  },
});
```

## File Storage

### Upload File

```typescript
// Client side
const uploadFile = useMutation(api.files.generateUploadUrl);

async function handleFileUpload(file: File) {
  // Step 1: Get upload URL
  const uploadUrl = await uploadFile();

  // Step 2: Upload file
  const result = await fetch(uploadUrl, {
    method: "POST",
    headers: { "Content-Type": file.type },
    body: file,
  });

  const { storageId } = await result.json();

  // Step 3: Save to database
  await saveFile({ storageId, name: file.name });
}
```

```typescript
// Backend
export const generateUploadUrl = mutation({
  args: {},
  returns: v.string(),
  handler: async (ctx) => {
    return await ctx.storage.generateUploadUrl();
  },
});

export const saveFile = mutation({
  args: {
    storageId: v.id("_storage"),
    name: v.string(),
  },
  handler: async (ctx, args) => {
    const user = await requireUser(ctx);

    await ctx.db.insert("files", {
      storageId: args.storageId,
      name: args.name,
      userId: user._id,
    });
  },
});
```

### Get File URL

```typescript
export const getFileUrl = query({
  args: { storageId: v.id("_storage") },
  returns: v.union(v.string(), v.null()),
  handler: async (ctx, args) => {
    return await ctx.storage.getUrl(args.storageId);
  },
});
```

### Get File Metadata

```typescript
// Query the _storage system table
type FileMetadata = {
  _id: Id<"_storage">;
  _creationTime: number;
  contentType?: string;
  sha256: string;
  size: number;
};

export const getFileMetadata = query({
  args: { storageId: v.id("_storage") },
  returns: v.union(
    v.object({
      _id: v.id("_storage"),
      _creationTime: v.number(),
      contentType: v.optional(v.string()),
      sha256: v.string(),
      size: v.number(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.system.get(args.storageId);
  },
});
```

## Scheduling

### Schedule from Mutation

```typescript
export const createTask = mutation({
  args: { title: v.string(), userId: v.id("users") },
  handler: async (ctx, args) => {
    const taskId = await ctx.db.insert("tasks", {
      title: args.title,
      userId: args.userId,
      status: "pending" as const,
    });

    // Schedule action immediately
    await ctx.scheduler.runAfter(0, internal.notifications.sendTaskCreated, {
      taskId,
    });

    // Schedule action in 1 hour
    await ctx.scheduler.runAfter(
      60 * 60 * 1000,
      internal.tasks.reminderCheck,
      { taskId }
    );

    // Schedule at specific time
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(9, 0, 0, 0);

    await ctx.scheduler.runAt(
      tomorrow.getTime(),
      internal.tasks.dailyDigest,
      { userId: args.userId }
    );

    return taskId;
  },
});
```

### Cron Jobs

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Run every 2 hours
crons.interval(
  "delete old tasks",
  { hours: 2 },
  internal.tasks.deleteOldTasks,
  {}
);

// Run at specific time (cron syntax)
crons.cron(
  "daily report",
  "0 9 * * *",  // 9 AM every day
  internal.reports.generateDailyReport,
  {}
);

export default crons;

// Define the internal action in same file or another
export const deleteOldTasks = internalAction({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const cutoff = Date.now() - 30 * 24 * 60 * 60 * 1000; // 30 days

    await ctx.runMutation(internal.tasks.deleteTasksBefore, { cutoff });

    return null;
  },
});
```

## HTTP Endpoints

### Define HTTP Routes

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { internal } from "./_generated/api";

const http = httpRouter();

// Webhook endpoint
http.route({
  path: "/webhooks/stripe",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    const signature = req.headers.get("stripe-signature");

    if (!signature) {
      return new Response("No signature", { status: 401 });
    }

    const body = await req.text();

    // Process webhook
    await ctx.runMutation(internal.stripe.processWebhook, {
      body,
      signature,
    });

    return new Response(null, { status: 200 });
  }),
});

// Public API endpoint
http.route({
  path: "/api/tasks",
  method: "GET",
  handler: httpAction(async (ctx, req) => {
    const url = new URL(req.url);
    const userId = url.searchParams.get("userId");

    if (!userId) {
      return new Response("Missing userId", { status: 400 });
    }

    const tasks = await ctx.runQuery(internal.tasks.listTasks, {
      userId: userId as Id<"users">,
    });

    return new Response(JSON.stringify(tasks), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }),
});

export default http;
```

## TypeScript Best Practices

### Type Imports

```typescript
import { Doc, Id } from "./_generated/dataModel";
import { FunctionReturnType } from "convex/server";
import { api } from "./_generated/api";

// Document type
type Task = Doc<"tasks">;

// ID type
type TaskId = Id<"tasks">;

// Function return type
type TaskList = FunctionReturnType<typeof api.tasks.listTasks>;

// Use in React components
function TaskItem({ task }: { task: Task }) {
  return <div>{task.title}</div>;
}
```

### Discriminated Unions

```typescript
// Schema
results: defineTable(
  v.union(
    v.object({
      kind: v.literal("error"),
      message: v.string(),
    }),
    v.object({
      kind: v.literal("success"),
      data: v.any(),
    })
  )
)

// Handler
export const processTask = mutation({
  args: { taskId: v.id("tasks") },
  returns: v.union(
    v.object({
      kind: v.literal("error"),
      message: v.string(),
    }),
    v.object({
      kind: v.literal("success"),
      data: v.string(),
    })
  ),
  handler: async (ctx, args) => {
    const task = await ctx.db.get(args.taskId);

    if (!task) {
      return {
        kind: "error" as const,
        message: "Task not found",
      };
    }

    // Process task
    return {
      kind: "success" as const,
      data: "Processed successfully",
    };
  },
});
```

### Helper Functions

```typescript
// convex/lib/helpers.ts
import { QueryCtx, MutationCtx } from "./_generated/server";
import { Doc, Id } from "./_generated/dataModel";

export async function getUserTasks(
  ctx: QueryCtx | MutationCtx,
  userId: Id<"users">
): Promise<Array<Doc<"tasks">>> {
  return await ctx.db
    .query("tasks")
    .withIndex("by_user", (q) => q.eq("userId", userId))
    .collect();
}

// Usage
export const getTaskCount = query({
  args: { userId: v.id("users") },
  returns: v.number(),
  handler: async (ctx, args) => {
    const tasks = await getUserTasks(ctx, args.userId);
    return tasks.length;
  },
});
```

## Common Patterns

### Optimistic Updates

```typescript
// Client
const updateTask = useMutation(api.tasks.updateTask);

async function handleToggle(taskId: Id<"tasks">) {
  // Optimistic update
  optimisticallyUpdateTask(taskId, { completed: true });

  try {
    await updateTask({ taskId, completed: true });
  } catch (error) {
    // Revert on error
    rollbackTask(taskId);
  }
}
```

### Error Handling

```typescript
export const createTask = mutation({
  args: { title: v.string(), userId: v.id("users") },
  handler: async (ctx, args) => {
    // Validate
    if (args.title.length === 0) {
      throw new Error("Title cannot be empty");
    }

    if (args.title.length > 100) {
      throw new Error("Title too long (max 100 characters)");
    }

    // Check auth
    const user = await ctx.db.get(args.userId);
    if (!user) {
      throw new Error("User not found");
    }

    // Check rate limits
    const recentTasks = await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .filter((q) =>
        q.gte(q.field("_creationTime"), Date.now() - 60000)
      )
      .collect();

    if (recentTasks.length >= 10) {
      throw new Error("Rate limit exceeded (max 10 tasks per minute)");
    }

    // Create task
    return await ctx.db.insert("tasks", {
      title: args.title,
      userId: args.userId,
      status: "pending" as const,
    });
  },
});
```

### Transactions

```typescript
// Mutations are automatically transactional
export const transferTask = mutation({
  args: {
    taskId: v.id("tasks"),
    fromUserId: v.id("users"),
    toUserId: v.id("users"),
  },
  handler: async (ctx, args) => {
    // All of this happens atomically
    const task = await ctx.db.get(args.taskId);

    if (!task) {
      throw new Error("Task not found");
    }

    if (task.userId !== args.fromUserId) {
      throw new Error("Task not owned by fromUser");
    }

    const toUser = await ctx.db.get(args.toUserId);
    if (!toUser) {
      throw new Error("Target user not found");
    }

    // Update task
    await ctx.db.patch(args.taskId, {
      userId: args.toUserId,
    });

    // Log transfer
    await ctx.db.insert("transfers", {
      taskId: args.taskId,
      fromUserId: args.fromUserId,
      toUserId: args.toUserId,
      timestamp: Date.now(),
    });

    // If any operation fails, entire mutation rolls back
  },
});
```

### Denormalization

```typescript
// Instead of JOIN pattern, denormalize for performance
export const createComment = mutation({
  args: {
    taskId: v.id("tasks"),
    content: v.string(),
    authorId: v.id("users"),
  },
  handler: async (ctx, args) => {
    const author = await ctx.db.get(args.authorId);
    if (!author) {
      throw new Error("Author not found");
    }

    // Store author name directly (denormalized)
    await ctx.db.insert("comments", {
      taskId: args.taskId,
      content: args.content,
      authorId: args.authorId,
      authorName: author.name,  // Denormalized
      authorAvatar: author.avatarUrl,  // Denormalized
    });
  },
});

// Query is faster - no need to join with users table
export const listComments = query({
  args: { taskId: v.id("tasks") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("comments")
      .withIndex("by_task", (q) => q.eq("taskId", args.taskId))
      .collect();
    // Each comment already has author name and avatar
  },
});
```

## Best Practices Summary

### DO

✅ **Always use indexes instead of `.filter()`**
✅ **Always add validators for `args` and `returns`**
✅ **Use `useState` only for form inputs and UI state**
✅ **Keep queries and mutations under 100ms**
✅ **Use pagination for large datasets**
✅ **Check `ctx.auth.getUserIdentity()` in public functions**
✅ **Use internal functions for sensitive operations**
✅ **Name indexes descriptively: `by_field1_and_field2`**
✅ **Use `ctx.db.patch()` for partial updates**
✅ **Add `"use node"` for actions with Node.js APIs**
✅ **Return minimal data from mutations**
✅ **Use plain TypeScript helpers instead of `ctx.run*` when possible**
✅ **Denormalize data for performance**
✅ **Use `.unique()` for single results**
✅ **Use `.take(n)` to limit results**
✅ **Enable ESLint `no-floating-promises` rule**

### DON'T

❌ **Never use `.filter()` when an index would work**
❌ **Never use `ctx.db` in actions**
❌ **Never call `ctx.runAction` unless crossing runtimes**
❌ **Never forget to await promises**
❌ **Never use `v.bigint()` (deprecated - use `v.int64()`)**
❌ **Never use `.delete()` on queries (collect then iterate)**
❌ **Never expose sensitive internal functions as public**
❌ **Never use `ctx.storage.getMetadata` (deprecated)**
❌ **Never use `useState` for database data**
❌ **Never create redundant indexes**
❌ **Never chain many `ctx.run*` calls from actions**
❌ **Never process large datasets without pagination**
❌ **Never skip input validation in public functions**
❌ **Never use unguessable IDs for security (use UUIDs or Convex IDs)**

## Common Mistakes

### ❌ Using useState for Database Data

```typescript
// BAD
function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/tasks").then(data => {
      setTasks(data);
      setLoading(false);
    });
  }, []);

  // ...
}

// GOOD
function TaskList({ userId }: { userId: Id<"users"> }) {
  const tasks = useQuery(api.tasks.listTasks, { userId });

  if (tasks === undefined) return <div>Loading...</div>;

  // Automatically reactive!
  // ...
}
```

### ❌ Using .filter() Instead of Indexes

```typescript
// BAD
const userTasks = await ctx.db
  .query("tasks")
  .filter((q) => q.eq(q.field("userId"), userId))
  .collect();

// GOOD
const userTasks = await ctx.db
  .query("tasks")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .collect();
```

### ❌ Missing Validators

```typescript
// BAD
export const createTask = mutation({
  handler: async (ctx, args: any) => {
    // No validation!
    await ctx.db.insert("tasks", args);
  },
});

// GOOD
export const createTask = mutation({
  args: {
    title: v.string(),
    userId: v.id("users"),
  },
  returns: v.id("tasks"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("tasks", {
      title: args.title,
      userId: args.userId,
      status: "pending" as const,
    });
  },
});
```

### ❌ Using ctx.db in Actions

```typescript
// BAD
export const sendEmail = action({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.userId);  // ❌ Error!
    // ...
  },
});

// GOOD
export const sendEmail = action({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    const user = await ctx.runQuery(internal.users.getUser, {
      userId: args.userId,
    });
    // ...
  },
});
```

### ❌ Not Awaiting Promises

```typescript
// BAD
export const createTask = mutation({
  handler: async (ctx, args) => {
    ctx.db.insert("tasks", { title: args.title });  // ❌ Not awaited!
  },
});

// GOOD
export const createTask = mutation({
  handler: async (ctx, args) => {
    await ctx.db.insert("tasks", { title: args.title });
  },
});
```

## Dashboard-Driven Development

**Essential Dashboard Features:**
- **Logs:** View function execution logs in real-time
- **Data Browser:** Inspect and edit database tables
- **Functions:** Test functions with custom arguments
- **Deployments:** View deployment history
- **File Storage:** Browse uploaded files
- **Scheduled Functions:** Monitor cron jobs and scheduled tasks
- **Usage:** Track function calls and database queries

**Best Practices:**
- Use dashboard to test functions during development
- Check logs for debugging
- Verify schema changes in Data Browser
- Test with production-like data
- Monitor performance metrics

## Quick Reference

### Function Types

| Type | Read DB | Write DB | External APIs | Runtime | Use For |
|------|---------|----------|---------------|---------|---------|
| Query | ✅ | ❌ | ❌ | V8 | Reading data |
| Mutation | ✅ | ✅ | ❌ | V8 | Writing data |
| Action | via `runQuery` | via `runMutation` | ✅ | Node | External APIs |

### Function Registration

```typescript
// Public (callable by clients)
query({ ... })
mutation({ ... })
action({ ... })

// Internal (only callable by Convex functions)
internalQuery({ ... })
internalMutation({ ... })
internalAction({ ... })
```

### Function References

```typescript
// Public: convex/tasks.ts -> f()
api.tasks.f

// Internal: convex/tasks.ts -> g()
internal.tasks.g

// Nested: convex/models/tasks.ts -> h()
api.models.tasks.h
```

### Database Operations

```typescript
// Create
await ctx.db.insert("tasks", { ... })

// Read
await ctx.db.get(taskId)

// Update (partial)
await ctx.db.patch(taskId, { status: "done" })

// Replace (full)
await ctx.db.replace(taskId, { ... })

// Delete
await ctx.db.delete(taskId)
```

### Query Patterns

```typescript
// All documents
.collect()

// Limited results
.take(10)

// Single document (throws if 0 or >1)
.unique()

// Single document (null if not found)
.first()

// Pagination
.paginate(opts)

// Ordering
.order("desc")
```

## Integration with Droidz Framework

### Using with Orchestrator

When building features with Droidz orchestration:

```bash
# 1. Define spec
/create-spec feature real-time-chat

# 2. In spec, specify Convex backend
# 3. Validate
/validate-spec .claude/specs/active/real-time-chat.md

# 4. Implement with Convex skill active
```

### Task Breakdown

Typical Convex feature tasks:
1. **Schema Design** - Define tables, indexes, validators
2. **Queries** - Implement read operations
3. **Mutations** - Implement write operations
4. **Actions** - Integrate external services
5. **Client Integration** - React hooks setup
6. **Testing** - Dashboard testing
7. **Deployment** - Push to production

### Documentation

```bash
# Save architectural decisions
/save-decision architecture "Using Convex for real-time sync to eliminate state management complexity"

# Save patterns
/save-decision patterns "Denormalizing user data in comments for query performance"
```

## Resources

**Official Documentation:**
- Convex Docs: https://docs.convex.dev
- Stack Articles: https://stack.convex.dev
- Dashboard: https://dashboard.convex.dev

**Key Articles:**
- useState Less: https://stack.convex.dev/usestate-less
- Zen of Convex: https://docs.convex.dev/understanding/zen
- Best Practices: https://docs.convex.dev/understanding/best-practices

**Community:**
- Discord: https://convex.dev/community
- GitHub: https://github.com/get-convex

## When to Ask User

Always ask the user:
1. **Before designing schema** - "I'll create these tables with these indexes. Confirm?"
2. **When choosing between query/mutation/action** - "Should this be a query or action?"
3. **Before denormalizing data** - "Denormalize author data in comments for performance?"
4. **When external API integration needed** - "Which external service/API should I integrate?"
5. **Before creating indexes** - "Create composite index `by_user_and_status`?"

## Key Principles

1. **Embrace Reactivity** - Let Convex handle data synchronization
2. **Query-First** - Use queries for all reads
3. **Keep Functions Lean** - Target < 100ms execution
4. **Minimize Client State** - Use Convex for data, React for UI
5. **Index Everything** - Never use `.filter()` when index works
6. **Validate Always** - All public functions need validators
7. **Auth Every Function** - Check `ctx.auth` in public functions
8. **Denormalize for Performance** - Avoid "JOIN" patterns

## Success Indicators

You're using Convex correctly when:
- ✅ Queries re-run automatically on data changes
- ✅ No manual cache invalidation needed
- ✅ Functions execute in < 100ms
- ✅ All functions have validators
- ✅ Using indexes instead of filters
- ✅ Client state is minimal (form inputs only)
- ✅ Real-time updates work seamlessly
- ✅ No race conditions or stale data issues

Remember: **Convex is designed for reactivity**. Trust the sync engine, use queries everywhere, and let the framework handle the complexity of real-time data synchronization!
