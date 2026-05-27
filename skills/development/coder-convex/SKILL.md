---
name: coder-convex
description: Self-hosted Convex development in Coder workspaces with authentication, queries, mutations, React integration, and environment configuration
updated: 2026-01-16
---

# Coder-Convex: Self-Hosted Convex Development in Coder Workspace

You are an expert at working with **self-hosted Convex** in a **Coder development workspace**. You understand the unique constraints and capabilities of this environment and can help users build full-stack applications with Convex as the backend.

> **NOTE**: This skill is for **everyday Convex development** (queries, mutations, React integration, etc.). For **initial workspace setup**, use the `coder-convex-setup` skill instead.

## Environment Context

### Coder Workspace Characteristics

- **OS**: Linux (Ubuntu/Debian-based), x86_64 architecture
- **Runtime**: Docker-in-Docker capability
- **Networking**: Internal cluster networking with port forwarding
- **Package Manager**: Node.js package manager (pnpm/npm/yarn)

### Coder Convex Services

In a Coder workspace, Convex is exposed through multiple services:

| Slug | Display Name | Internal URL | Port | Hidden | Purpose |
|------|-------------|--------------|------|--------|---------|
| `convex-dashboard` | Convex Dashboard | `localhost:6791` | 6791 | No | Admin dashboard |
| `convex-api` | Convex API | `localhost:3210` | 3210 | **Yes** | Main API endpoints |
| `convex-site` | Convex Site | `localhost:3211` | 3211 | **Yes** | **Site Proxy (Auth)** |

### Self-Hosted Convex in Coder

This workspace uses a **self-hosted Convex deployment** (not the convex.dev cloud service). Key differences:

1. **Deployment URL**: Coder proxy URL (e.g., `https://convex-api--workspace--user.coder.hahomelabs.com`)
2. **Authentication**: Uses `@convex-dev/auth` with self-hosted configuration
3. **Dashboard**: Available at `localhost:6791` or via Coder proxy
4. **Admin Key**: Generated automatically by setup script
5. **Environment Variables**: Managed via `.env.convex.local` file

## Required Scripts

The following operations should be available through your project's package manager:

**Development:**
- `dev:backend` - Run Convex dev server (runs `npx convex dev`)
- `deploy:functions` - Deploy Convex functions (runs `npx convex deploy --yes`)

**Docker (Self-Hosted Backend):**
- `convex:start` - Start self-hosted Convex via Docker Compose
- `convex:stop` - Stop Docker services
- `convex:logs` - View Docker logs
- `convex:status` - Check service status

**Testing:**
- Run end-to-end tests
- Run framework type checking
- Run TypeScript compiler checking

## Project Structure

```
convex/
├── _generated/          # Auto-generated API definitions (DO NOT EDIT)
│   ├── api.d.ts         # Type-safe function references
│   ├── server.d.ts      # Server-side function types
│   └── dataModel.d.ts   # Database model types
├── schema.ts            # Database schema definition
├── auth.config.ts       # Auth configuration (required for Coder)
├── auth.ts              # Auth utilities
├── messages.ts          # Chat/messaging functions
├── rag.ts               # RAG (Retrieval Augmented Generation) functions
├── actions.ts           # Node.js actions (with "use node")
├── documents.ts         # Document management
├── tasks.ts             # Task management
└── lib/                 # Internal utilities
    └── ids.ts           # ID generation helpers

src/
├── components/          # React components
│   └── ChatWidget.tsx   # Example Convex React integration
└── pages/               # Astro pages

scripts/
├── setup-convex.sh      # Coder-specific setup script
└── start-convex-backend.sh  # Backend startup script

.env.convex.local        # Coder environment variables (auto-generated)
```

## Convex Development Guidelines

### Function Types

| Type               | Runtime | Use Case                         | Import From           |
| ------------------ | ------- | -------------------------------- | --------------------- |
| `query`            | V8      | Read data, no side effects       | `./_generated/server` |
| `mutation`         | V8      | Write data, transactional        | `./_generated/server` |
| `action`           | Node.js | External API calls, long-running | `./_generated/server` |
| `internalQuery`    | V8      | Private read functions           | `./_generated/server` |
| `internalMutation` | V8      | Private write functions          | `./_generated/server` |
| `internalAction`   | Node.js | Private Node.js operations       | `./_generated/server` |

### Function Syntax (Modern)

```typescript
import { query, mutation, action } from "./_generated/server";
import { v } from "convex/values";

// Public query
export const listTasks = query({
  args: { status: v.optional(v.string()) },
  handler: async (ctx, args) => {
    const tasks = await ctx.db.query("tasks").collect();
    return tasks;
  },
});

// Public mutation
export const createTask = mutation({
  args: {
    title: v.string(),
    description: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const taskId = await ctx.db.insert("tasks", {
      title: args.title,
      description: args.description,
      status: "pending",
    });
    return taskId;
  },
});

// Internal action (Node.js runtime)
("use node"); // Required at top of file for Node.js features

import { internalAction } from "./_generated/server";
import OpenAI from "openai";

export const generateEmbedding = internalAction({
  args: { text: v.string() },
  handler: async (_ctx, args) => {
    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
    const response = await openai.embeddings.create({
      model: "text-embedding-3-small",
      input: args.text,
    });
    return response.data[0].embedding;
  },
});
```

### Schema Definition

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";
import { authTables } from "@convex-dev/auth/server";

// Your application tables
const applicationTables = {
  tasks: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    status: v.string(),
    priority: v.optional(v.number()),
    userId: v.id("users"), // Reference to auth users table
  })
    .index("by_status", ["status"])
    .index("by_priority", ["priority"])
    .index("by_user", ["userId"]),
};

export default defineSchema({
  ...authTables,  // Always include auth tables
  ...applicationTables,
});
```

### Key Schema Rules

1. **Always include `...authTables`** from `@convex-dev/auth/server` for Coder workspaces
2. **Never manually add `_creationTime`** - it's automatic
3. **Never use `.index("by_creation_time", ["_creationTime"])`** - it's built-in
4. **Index names should be descriptive**: `by_fieldName` or `by_field1_and_field2`
5. **All indexes include `_creationTime` automatically as the last field**
6. **Indexes must be non-empty**: define at least one field

### Common Validators

```typescript
v.id("tableName"); // Reference to a document
v.string(); // String value
v.number(); // Number (float/int)
v.boolean(); // Boolean
v.null(); // Null value
v.array(v.string()); // Array of strings
v.object({
  // Object with defined shape
  name: v.string(),
  age: v.number(),
});
v.optional(v.string()); // Optional field
v.union(
  // Union of types
  v.literal("active"),
  v.literal("inactive")
);
```

### Query Patterns

```typescript
// Get all documents
const all = await ctx.db.query("tasks").collect();

// Get with index filter
const active = await ctx.db
  .query("tasks")
  .withIndex("by_status", (q) => q.eq("status", "active"))
  .collect();

// Get single document
const task = await ctx.db.get(taskId);

// Unique result (throws if multiple)
const task = await ctx.db
  .query("tasks")
  .filter((q) => q.eq(q.field("title"), "My Task"))
  .unique();

// Order and limit
const recent = await ctx.db.query("tasks").order("desc").take(10);

// Pagination
const page = await ctx.db
  .query("tasks")
  .paginate({ numItems: 20, cursor: null });
```

### Mutation Patterns

```typescript
// Insert new document
const id = await ctx.db.insert("tasks", {
  title: "New Task",
  status: "pending",
});

// Patch (merge update)
await ctx.db.patch(taskId, {
  status: "completed",
});

// Replace (full replacement)
await ctx.db.replace(taskId, {
  title: "Updated Title",
  status: "completed",
  description: "New description",
});

// Delete
await ctx.db.delete(taskId);
```

### Calling Functions from Functions

```typescript
import { api } from "./_generated/api";
import { internal } from "./_generated/api";

// From a mutation or action
export const myMutation = mutation({
  args: {},
  handler: async (ctx) => {
    // Call another query
    const tasks: Array<Doc<"tasks">> = await ctx.runQuery(api.tasks.list, {});

    // Call another mutation
    await ctx.runMutation(api.tasks.create, { title: "From mutation" });

    // Call internal function
    await ctx.runMutation(internal.tasks.processTask, { taskId: "abc123" });
  },
});
```

## Authentication in Coder Workspaces

### Auth Configuration

The `convex/auth.config.ts` file is critical for authentication in Coder workspaces:

```typescript
// convex/auth.config.ts
export default {
  providers: [
    {
      domain: process.env.CONVEX_SITE_URL,  // Points to API URL (port 3210)
      applicationID: "convex",
    },
  ],
};
```

**Critical:** The `domain` uses `CONVEX_SITE_URL` which points to the **API URL**, not the site proxy URL. This is because auth endpoints are served at `/api/auth/*` on the API.

### Using Auth in Functions

```typescript
import { query } from "./_generated/server";
import { getAuthUserId } from "@convex-dev/auth/server";

export const getCurrentUser = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return null;
    }
    return await ctx.db.get(userId);
  },
});

// Query that requires authentication
export const getUserTasks = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .collect();
  },
});
```

### React Auth Integration

```typescript
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";
import { SignInButton, SignOutButton, useAuth } from "@convex-dev/auth/react";

export default function App() {
  const { isAuthenticated, user } = useAuth();
  const tasks = useQuery(api.tasks.getUserTasks) || [];

  if (!isAuthenticated) {
    return (
      <main>
        <h1>My App</h1>
        <SignInButton />
      </main>
    );
  }

  return (
    <main>
      <h1>Welcome, {user?.name || 'User'}!</h1>
      <SignOutButton />
      <ul>
        {tasks.map(task => (
          <li key={task._id}>{task.title}</li>
        ))}
      </ul>
    </main>
  );
}
```

## React Integration

```typescript
import { useQuery, useMutation, useAction } from "convex/react";
import { api } from "../../convex/_generated/api";

function TaskList() {
  // Query with automatic reactivity
  const tasks = useQuery(api.tasks.list) || [];

  // Mutation
  const createTask = useMutation(api.tasks.create);

  // Action
  const generateEmbedding = useAction(api.rag.generateQueryEmbedding);

  return (
    <div>
      {tasks.map(task => (
        <div key={task._id}>{task.title}</div>
      ))}
      <button onClick={() => createTask({ title: "New" })}>
        Add Task
      </button>
    </div>
  );
}
```

### React Best Practices

1. **NEVER call hooks conditionally**:

   ```typescript
   // WRONG
   const data = user ? useQuery(api.getUser, { userId: user.id }) : null;

   // RIGHT
   const data = useQuery(api.getUser, user ? { userId: user.id } : "skip");
   ```

2. **Use "skip" sentinel for conditional queries**:
   ```typescript
   import { skipToken } from "convex/react";
   const data = useQuery(api.tasks.get, taskId ? { id: taskId } : skipToken());
   ```

3. **Always use ConvexProviderWithAuth** for authentication:
   ```typescript
   import { ConvexReactClient } from "convex/react";
   import { ConvexProviderWithAuth } from "@convex-dev/auth/react";

   const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

   ReactDOM.createRoot(document.getElementById("root")!).render(
     <ConvexProviderWithAuth client={convex}>
       <App />
     </ConvexProviderWithAuth>
   );
   ```

## Environment Variables

> **NOTE**: For initial environment setup (creating `.env.convex.local`, generating admin keys, Docker configuration), use the `coder-convex-setup` skill.

### Available Environment Variables (Coder)

```bash
# Coder Workspace URLs (auto-generated by setup script)
CONVEX_CLOUD_ORIGIN=<convex-api URL>       # e.g., https://convex-api--...coder.hahomelabs.com
CONVEX_SITE_ORIGIN=<convex-site URL>       # e.g., https://convex-site--...coder.hahomelabs.com
CONVEX_SITE_URL=<convex-api URL>           # Same as CONVEX_CLOUD_ORIGIN (used by auth.config.ts)
CONVEX_DEPLOYMENT_URL=<convex-api URL>     # Same as CONVEX_CLOUD_ORIGIN

# Frontend Configuration
VITE_CONVEX_URL=<convex-api URL>           # Same as CONVEX_CLOUD_ORIGIN

# Admin Key
CONVEX_SELF_HOSTED_ADMIN_KEY=<admin-key>   # Auto-generated

# JWT Configuration (for auth)
JWT_ISSUER=<convex-site URL>               # Same as CONVEX_SITE_ORIGIN
JWT_PRIVATE_KEY_BASE64=<base64-key>        # Auto-generated

# Database (if using PostgreSQL)
POSTGRES_URL=<postgres-connection-string>  # e.g., postgresql://convex:convex@localhost:5432/convex

# AI Services (if using)
LITELLM_APP_API_KEY=<api-key>              # For LiteLLM proxy
LITELLM_BASE_URL=<proxy-url>               # e.g., https://llm-gateway.hahomelabs.com
OPENAI_API_KEY=<openai-key>                # For embeddings/RAG

# Feature Flags
ENABLE_RAG=true/false                      # Enable RAG functionality
```

### Critical Variable Relationships

```
CONVEX_CLOUD_ORIGIN = CONVEX_SITE_URL = CONVEX_DEPLOYMENT_URL = VITE_CONVEX_URL (all point to convex-api)
CONVEX_SITE_ORIGIN = JWT_ISSUER (both point to convex-site)
```

**Why this works:**
- All Convex client communication goes through the API (port 3210)
- Auth endpoints are `/api/auth/*` on the API
- The site proxy (port 3211) is for HTTP routes and internal Convex communication
- The `domain` in `auth.config.ts` uses `CONVEX_SITE_URL` (API URL) because auth endpoints are on the API

### Accessing Environment Variables in Functions

```typescript
export const checkEnv = query({
  args: {},
  handler: async (_ctx) => {
    return {
      convexCloudOrigin: process.env.CONVEX_CLOUD_ORIGIN,
      convexSiteOrigin: process.env.CONVEX_SITE_ORIGIN,
      convexSiteUrl: process.env.CONVEX_SITE_URL,
      jwtIssuer: process.env.JWT_ISSUER,
      apiKeyPresent: !!process.env.LITELLM_APP_API_KEY,
    };
  },
});
```

## Self-Hosted Convex Specifics

> **NOTE**: For initial deployment workflow and Docker setup, use the `coder-convex-setup` skill.

### Docker Services Status

The self-hosted Convex runs via Docker Compose. Check status:

```bash
[package-manager] run convex:status    # Check container status
docker ps                               # List running containers
[package-manager] run convex:logs      # View backend logs
```

### Common Runtime Issues

| Issue                              | Solution                                          |
| ---------------------------------- | ------------------------------------------------- |
| Functions not updating             | Run `[package-manager] run deploy:functions]`      |
| Type errors after schema change    | Run `[package-manager] run dev:backend]`           |
| Module not found: `_generated/api` | Run `[package-manager] run deploy:functions]`      |
| Authentication not working         | Check `CONVEX_SITE_URL` points to API URL         |
| Port 3211 not accessible           | Verify Docker is running with site proxy enabled  |

## Development Workflow

### Step 1: Define Schema

Edit [convex/schema.ts](convex/schema.ts):

```typescript
import { authTables } from "@convex-dev/auth/server";

const applicationTables = {
  tasks: defineTable({
    title: v.string(),
    status: v.string(),
    userId: v.id("users"),
  }).index("by_user", ["userId"]),
};

export default defineSchema({
  ...authTables,
  ...applicationTables,
});
```

### Step 2: Write Functions

Edit or create files in [convex/](convex/):

```typescript
// convex/tasks.ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";
import { getAuthUserId } from "@convex-dev/auth/server";

export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});

export const getUserTasks = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return [];
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .collect();
  },
});

export const create = mutation({
  args: { title: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }
    await ctx.db.insert("tasks", {
      title: args.title,
      status: "pending",
      userId,
    });
  },
});
```

### Step 3: Deploy Functions

Deploy the Convex functions to your backend:

```bash
[package-manager] run deploy:functions
```

This regenerates [convex/\_generated/api.d.ts](convex/_generated/api.d.ts) with type-safe references.

### Step 4: Use in React

```typescript
import { useQuery, useMutation } from "convex/react";
import { api } from "../../convex/_generated/api";
import { SignInButton, SignOutButton, useAuth } from "@convex-dev/auth/react";

export default function Tasks() {
  const { isAuthenticated } = useAuth();
  const tasks = useQuery(api.tasks.getUserTasks) || [];
  const create = useMutation(api.tasks.create);

  if (!isAuthenticated) {
    return <SignInButton />;
  }

  return (
    <div>
      <SignOutButton />
      <ul>
        {tasks.map((t) => (
          <div key={t._id}>{t.title}</div>
        ))}
      </ul>
      <button onClick={() => create({ title: "New" })}>Add</button>
    </div>
  );
}
```

### Step 5: Quality Gates

Run appropriate quality gates based on the changes made. Consider what regressions are possible and what new functionality was added, then conduct relevant checks:

- **Type checking** (for TypeScript changes)
- **Linting** (for code style consistency)
- **Build verification** (to catch integration issues)
- **Targeted tests** (for new or modified functionality)

Run only the quality gates that are relevant to the changes made.

## Testing Convex Functions

### Unit Tests

```typescript
// tests/convex-function.test.ts
import { test } from "node:test";
import assert from "node:assert";

test("tasks.create creates a task", async () => {
  // Test your function logic
});
```

### Integration Tests (Playwright)

See [tests/convex-chat-api.test.ts](tests/convex-chat-api.test.ts) for examples.

## Type Safety

### Using Generated Types

```typescript
import type { Doc, Id } from "./_generated/dataModel";

type Task = Doc<"tasks">; // Task document type
type TaskId = Id<"tasks">; // Task ID type
type UserId = Id<"users">; // User ID type (from auth tables)

function processTask(taskId: TaskId) {
  // Type-safe!
}
```

### Function Reference Types

```typescript
import type { FunctionReference } from "convex/server";

// Function references are fully typed
const fn: FunctionReference<"query", "public", args, Doc<"tasks">> = api.tasks.get;
```

## Best Practices

### DO

- Use `internal*` functions for sensitive operations
- Always validate arguments with `v.*()` validators
- Use indexes for efficient queries
- Always include `...authTables` in schema for Coder workspaces
- Check authentication in mutations that modify user data
- Keep functions under 100 lines
- Use TypeScript strict mode
- Test in dev before deploying

### DON'T

- Don't use `.filter()` in queries - use indexes instead
- Don't manually add `_id` or `_creationTime` to schemas
- Don't use `undefined` - use `null` instead
- Don't make files longer than 300 lines
- Don't call hooks conditionally in React
- Don't manually edit `_generated/` files
- Don't forget to deploy functions after changes

## Coder Workspace URL Patterns

### Internal (Localhost)

| Service | URL |
|---------|-----|
| Convex API | `http://localhost:3210` |
| Site Proxy (Auth) | `http://localhost:3211` |
| Dashboard | `http://localhost:6791` |

### External (Coder Proxy)

| Service | URL Pattern | Example |
|---------|-------------|---------|
| Convex API | `https://convex-api--<workspace>--<user>.<domain>` | `https://convex-api--myproject--johndoe.coder.hahomelabs.com` |
| Convex Site | `https://convex-site--<workspace>--<user>.<domain>` | `https://convex-site--myproject--johndoe.coder.hahomelabs.com` |
| Convex Dashboard | `https://convex--<workspace>--<user>.<domain>` | `https://convex--myproject--johndoe.coder.hahomelabs.com` |

## Self-Hosted Convex vs Convex Cloud

| Feature               | Coder Self-Hosted                              | Convex Cloud                |
| --------------------- | ---------------------------------------------- | --------------------------- |
| Dashboard             | Local at `localhost:6791` or Coder proxy URL  | Web dashboard at convex.dev |
| Deployment URL        | Coder proxy URL                                | `*.convex.cloud`            |
| Environment Variables | `.env.convex.local` file                      | Dashboard UI                |
| Auth Configuration    | Points to `CONVEX_SITE_URL` (API URL)         | Auto-configured             |
| Site Proxy Port       | 3211 (auth/site proxy)                        | Not applicable              |
| Initial Setup         | Manual (use `coder-convex-setup`)             | Guided in dashboard         |
| Pricing               | Self-managed infrastructure                    | Usage-based pricing         |

## RAG (Retrieval Augmented Generation)

This project includes RAG capabilities for AI-powered document search.

### Generating Embeddings

Run the embeddings generation script to process documents for RAG search.

### Using RAG in Queries

```typescript
import { internal } from "./_generated/api";

export const searchWithRAG = action({
  args: { query: v.string() },
  handler: async (ctx, args) => {
    // Generate query embedding
    const embedding = await ctx.runAction(internal.rag.generateQueryEmbedding, {
      query: args.query,
    });

    // Search documents
    const results = await ctx.runQuery(internal.rag.searchDocuments, {
      queryEmbedding: embedding,
      threshold: 0.6,
      maxResults: 3,
    });

    return results;
  },
});
```

## Troubleshooting

> **NOTE**: For setup-related issues (missing deployment URL, invalid admin key, Docker problems), use the `coder-convex-setup` skill.

### Common Runtime Errors

```
Type error: Property 'xxx' does not exist on type
```

**Fix**: Run `[package-manager] run dev:backend]` to regenerate types after schema changes.

```
Error: Module not found: Can't resolve './_generated/api'
```

**Fix**: Run `[package-manager] run deploy:functions]` to generate API files.

```
Error: Cannot read property 'xxx' of undefined
```

**Fix**: Check your query/mutation logic - document may not exist or field may be optional.

```
Authentication failing with "Invalid issuer"
```

**Fix**: Verify environment variables:
```bash
grep "CONVEX_SITE" .env.convex.local
# CONVEX_SITE_ORIGIN should point to convex-site URL
# CONVEX_SITE_URL should point to convex-api URL
# JWT_ISSUER should match CONVEX_SITE_ORIGIN
```

### Debug Queries

```typescript
// Check database state
export const debugDb = query({
  args: {},
  handler: async (ctx) => {
    const tasks = await ctx.db.query("tasks").collect();
    return { count: tasks.length, tasks };
  },
});

// Check function execution
export const debugFunction = query({
  args: {},
  handler: async (_ctx) => {
    return {
      timestamp: Date.now(),
      envKeys: Object.keys(process.env),
      convexCloudOrigin: process.env.CONVEX_CLOUD_ORIGIN,
      convexSiteOrigin: process.env.CONVEX_SITE_ORIGIN,
      convexSiteUrl: process.env.CONVEX_SITE_URL,
    };
  },
});
```

## Quick Reference

| Operation                        | Purpose                             |
| -------------------------------- | ----------------------------------- |
| `dev:backend`                    | Development mode with type sync     |
| `deploy:functions`                | Update backend functions            |
| `convex:start`                   | Launch Docker services              |
| `convex:stop`                    | Stop Docker services                |
| `convex:logs`                    | View backend logs                   |
| `convex:status`                  | Check service status                |
| Type checking                    | Verify TypeScript correctness       |
| Run tests                        | Execute test suite                  |

## Summary

This workspace uses **self-hosted Convex in Coder** with:

- Docker-based deployment with Coder proxy URLs
- `@convex-dev/auth` for authentication
- Port 3211 for site proxy (auth)
- Port 3210 for API endpoints
- Dashboard at `localhost:6791`
- Environment variables in `.env.convex.local`

Remember: Always deploy Convex functions after changing Convex code, and run appropriate quality gates before committing.
