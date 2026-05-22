---
name: convex-actions-general
description: This skill should be used when working with Convex actions, HTTP endpoints, validators, schemas, environment variables, scheduling, file storage, and TypeScript patterns. It provides comprehensive guidelines for function definitions, API design, database limits, and advanced Convex features.
---

# Convex Actions and General Guidelines Skill

This skill provides comprehensive guidance for Convex actions, HTTP endpoints, validators, schema design, file storage, environment variables, scheduling, and TypeScript best practices.

## When to Use This Skill

Use this skill when:
- Implementing action functions for external API calls and long-running tasks
- Creating HTTP endpoints for webhooks or public APIs
- Defining validators for function arguments and database schemas
- Designing database schemas with tables, indexes, and search capabilities
- Setting up environment variables for secrets and configuration
- Implementing cron jobs and scheduled tasks
- Working with file storage for uploads and downloads
- Using Convex-specific TypeScript patterns and types
- Understanding Convex limits and performance constraints

## Skill Resources

This skill includes comprehensive reference documentation in `references/actions-and-general.md` that covers:

### Actions and HTTP
- **Actions**: Defining actions with `"use node"` for Node.js modules
  - V8 vs Node runtime differences
  - Action limitations (10-minute timeout, no database access)
  - Calling external APIs and services
- **HTTP Endpoints**: Setting up `convex/http.ts` with httpRouter
  - Path registration and exact matching
  - Request/response handling
  - Method definitions (POST, GET, etc.)

### Validators and Types
- Complete validator reference for all Convex types
- Common validators: `v.object()`, `v.array()`, `v.string()`, `v.number()`, `v.id()`, `v.boolean()`, `v.null()`
- Discriminated union types with `v.union()` and `v.literal()`
- ASCII field name requirements for objects
- Size and element count limits

### Function Development
- New function syntax for all function types
- Function registration patterns (`query`, `mutation`, `action`, `internalQuery`, `internalMutation`, `internalAction`)
- Function calling patterns across runtimes
- Function references via `api` and `internal` objects
- File-based routing conventions

### API Design
- Organizing public and private functions
- Thoughtful file structure within `convex/` directory
- Public vs. internal function visibility
- API surface consistency

### Database and Schema
- **Schema Definition**: `convex/schema.ts` structure
  - System fields (`_id`, `_creationTime`)
  - Table definitions with validators
- **Indexes**: Creating efficient indexes
  - Built-in indexes (by_id, by_creation_time)
  - Custom index naming and field ordering
  - Multiple field indexes for complex queries
- **Full Text Search**: Search index definitions
  - Search fields and filter fields
  - Nested field paths with dot notation

### Environment and Configuration
- **Environment Variables**: Using `process.env`
  - Storing secrets (API keys, credentials)
  - Per-deployment configuration
  - Access from any function type
- **Scheduling**:
  - **Crons**: Using `crons.interval()` and `crons.cron()`
  - **Scheduler**: Using `ctx.scheduler.runAfter()` from mutations/actions
  - Auth state propagation (doesn't propagate to scheduled jobs)
  - Timing constraints and best practices

### File Storage
- Upload URL generation with `ctx.storage.generateUploadUrl()`
- Signed URL retrieval with `ctx.storage.getUrl()`
- File metadata from `_storage` system table
- Blob conversion for storage operations
- Complete example: image upload in chat application

### Limits and Performance
- Function arguments and return values: 8 MiB maximum
- Database operations: 8192 document writes per mutation, 16384 reads per query
- Execution timeouts: 1 second for queries/mutations, 10 minutes for actions
- Array element limits: 8192 maximum
- Object/Record field limits: 1024 maximum
- Nesting depth: 16 maximum
- Record size: 1 MiB maximum
- HTTP streaming: 20 MiB maximum output

### TypeScript
- `Id<'tableName'>` types for strict document IDs
- `Doc<'tableName'>` types for document type safety
- `Record<KeyType, ValueType>` with proper typing
- `as const` for discriminated unions
- Type annotations for same-file function calls
- `@types/node` for Node.js modules

## How to Use This Skill

1. **Read the reference documentation** at `references/actions-and-general.md` for comprehensive patterns
2. **Follow the syntax** for defining actions with proper Node.js module handling
3. **Use validators** correctly for all function arguments and schema fields
4. **Design schemas** with appropriate indexes for your access patterns
5. **Set up environment variables** for secrets and configuration
6. **Implement scheduling** for background tasks using crons or the scheduler
7. **Handle file storage** with proper URL generation and metadata lookup
8. **Understand limits** and design applications to respect them
9. **Use TypeScript strictly** with `Id` types and proper generics

## Key General Guidelines

- ALWAYS use argument validators for all functions (queries, mutations, actions)
- Do NOT store file URLs in the database; store file IDs instead
- Remapping non-ASCII characters (emoji) to ASCII codes before storing in objects
- Auth state does NOT propagate to scheduled jobs; use internal functions
- Scheduled functions should not run more than once every 10 seconds
- Never call actions from other actions unless crossing runtimes (V8 to Node)
- Objects in Convex must have ASCII-only field names
- Be strict with TypeScript types, especially for document IDs

## Example: Complete Action with HTTP Endpoint

```ts
// convex/ai.ts
"use node";
import { action } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const generateResponse = action({
  args: {
    channelId: v.id("channels"),
  },
  handler: async (ctx, args) => {
    // Actions can't access ctx.db, but can call mutations
    const context = await ctx.runQuery(internal.functions.loadContext, {
      channelId: args.channelId,
    });

    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: context,
    });

    const content = response.choices[0].message.content;
    if (!content) throw new Error("No content in response");

    await ctx.runMutation(internal.functions.writeAgentResponse, {
      channelId: args.channelId,
      content,
    });

    return null;
  },
});
```

## Example: HTTP Endpoint

```ts
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

http.route({
  path: "/webhook",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    const body = await req.json();
    // Process webhook payload
    return new Response(JSON.stringify({ success: true }), { status: 200 });
  }),
});

export default http;
```

For more detailed information and additional patterns, refer to the complete reference documentation.
