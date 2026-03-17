---
name: "Convex Backend Development"
description: "Build Convex backends with queries, mutations, actions, HTTP endpoints, and schemas. Comprehensive guide for all Convex patterns and workflows."
tools: Read, Grep, Glob, Write, Edit, Bash
model: inherit
---

# Skill: Convex Backend Development

Complete guide for implementing Convex backend functionality including queries, mutations, actions, HTTP endpoints, file storage, and database schemas.

## When to Use

- Implementing Convex backend functionality
- Creating database schemas with tables and indexes
- Adding HTTP endpoints for webhooks or external API access
- Implementing async actions and scheduled tasks
- Setting up authentication and authorization
- Debugging Convex-related issues
- Working with file storage and URLs

## Domain Knowledge

### Critical Patterns

#### Function Type Separation (CRITICAL)
Convex has three function types, each with specific purposes:

- **Queries**: Read data only, cannot modify database
  - Used for fetching data
  - Can be called from components
  - Cached and reactive

- **Mutations**: Write to database
  - Used for creating, updating, deleting data
  - Can schedule actions
  - Transactional

- **Actions**: External side effects
  - Call third-party APIs
  - Send emails
  - Interact with external services
  - Cannot directly access database (must call queries/mutations)

**Rule**: Schedule actions from mutations, never call actions directly from mutations.

```typescript
// ❌ Wrong - calling action directly
export const myMutation = mutation({
  handler: async (ctx) => {
    await ctx.runAction(api.actions.sendEmail); // Don't do this
  },
});

// ✅ Correct - schedule action
export const myMutation = mutation({
  handler: async (ctx, args) => {
    await ctx.scheduler.runAfter(0, api.actions.sendEmail, args);
  },
});
```

#### CORS Headers for HTTP Endpoints (CRITICAL)
All HTTP endpoints accessed from browsers MUST include CORS headers, or browsers will block requests.

**Required CORS headers constant:**
```typescript
const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS, GET, PUT, DELETE",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Vary": "Origin",
};
```

**Must include in:**
- All successful responses
- All error responses
- OPTIONS preflight responses

**Why this matters**: Without CORS headers, your HTTP endpoint will work in Postman/curl but fail in browser applications.

#### Storage URL Generation
Always use `ctx.storage.getUrl()` for storage URLs, never construct URLs manually.

```typescript
// ❌ Wrong - manual URL construction
const url = `https://your-deployment.convex.cloud/storage/${storageId}`;

// ✅ Correct - use ctx.storage.getUrl()
const url = await ctx.storage.getUrl(storageId);
```

**Why**: Manual URLs don't work and return null. The storage system requires proper URL generation through the API.

#### HTTP Endpoint Domains (CRITICAL)
Use `.convex.site` for HTTP endpoints, NOT `.convex.cloud`.

```typescript
// ❌ Wrong - .convex.cloud is for dashboard only
const url = `${process.env.NEXT_PUBLIC_CONVEX_URL}/uploadFile`;
// Results in 404 Not Found

// ✅ Correct - replace with .convex.site
const url = `${process.env.NEXT_PUBLIC_CONVEX_URL.replace('.convex.cloud', '.convex.site')}/uploadFile`;
```

**Why**: `.convex.cloud` is for the Convex dashboard, `.convex.site` is for HTTP endpoints.

### Key Files

- **convex/schema.ts** - Database schema definitions (tables, indexes, relationships)
- **convex/http.ts** - HTTP endpoint routes and handlers
- **convex/_generated/api.js** - Generated API types (auto-generated, don't edit)
- **convex/auth.config.ts** - Authentication configuration (Clerk JWT)

### Authentication Pattern

Convex integrates with Clerk via JWT tokens:

```typescript
// In HTTP action - get auth from header
const authHeader = request.headers.get("Authorization");
const token = authHeader?.replace("Bearer ", "");

// In query/mutation - get authenticated user
const identity = await ctx.auth.getUserIdentity();
if (!identity) {
  throw new Error("Unauthorized");
}
```

## Workflows

### Workflow 1: Create HTTP Endpoint

Step-by-step guide for creating HTTP endpoints with CORS, authentication, and error handling.

**Step 1: Define CORS Headers**

```typescript
// convex/http.ts
const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS, GET, PUT, DELETE",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Vary": "Origin",
};
```

**Step 2: Create HTTP Route**

```typescript
import { httpRouter, httpAction } from "convex/server";
import { api } from "./_generated/api";

const http = httpRouter();

http.route({
  path: "/your-endpoint",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    try {
      // Parse request body
      const body = await request.json();

      // Validate inputs
      if (!body.requiredField) {
        return new Response(
          JSON.stringify({ error: "Missing requiredField" }),
          { status: 400, headers: CORS_HEADERS }
        );
      }

      // Call mutation or action
      const result = await ctx.runMutation(api.mutations.yourMutation, body);

      // Return success with CORS
      return new Response(
        JSON.stringify({ success: true, data: result }),
        { status: 200, headers: CORS_HEADERS }
      );
    } catch (error) {
      // Return error with CORS
      return new Response(
        JSON.stringify({ error: error.message }),
        { status: 500, headers: CORS_HEADERS }
      );
    }
  }),
});

export default http;
```

**Step 3: Add OPTIONS Handler (Required for CORS)**

```typescript
http.route({
  path: "/your-endpoint",
  method: "OPTIONS",
  handler: httpAction(async () => {
    return new Response(null, {
      status: 200,
      headers: CORS_HEADERS,
    });
  }),
});
```

**Step 4: Add Authentication (Optional)**

```typescript
http.route({
  path: "/authenticated-endpoint",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    // Get and validate auth token
    const authHeader = request.headers.get("Authorization");
    if (!authHeader?.startsWith("Bearer ")) {
      return new Response(
        JSON.stringify({ error: "Missing or invalid Authorization header" }),
        { status: 401, headers: CORS_HEADERS }
      );
    }

    // Verify with Clerk (if using Clerk auth)
    const token = authHeader.replace("Bearer ", "");

    // Your authentication logic here
    // ...

    // Continue with authenticated logic
    const body = await request.json();
    const result = await ctx.runMutation(api.mutations.secureAction, body);

    return new Response(
      JSON.stringify({ success: true, data: result }),
      { status: 200, headers: CORS_HEADERS }
    );
  }),
});
```

**Step 5: Use Endpoint from Frontend**

```typescript
// In your Next.js app
const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL!.replace('.convex.cloud', '.convex.site');

const response = await fetch(`${convexUrl}/your-endpoint`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`, // if authenticated
  },
  body: JSON.stringify({ requiredField: "value" }),
});

const data = await response.json();
```

### Workflow 2: Design Database Schema

**Step 1: Define Tables in schema.ts**

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    clerkId: v.string(),
    email: v.string(),
    name: v.optional(v.string()),
    createdAt: v.number(),
  })
    .index("by_clerkId", ["clerkId"])
    .index("by_email", ["email"]),

  posts: defineTable({
    title: v.string(),
    content: v.string(),
    authorId: v.id("users"),
    published: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_author", ["authorId"])
    .index("by_published", ["published"])
    .index("by_author_and_published", ["authorId", "published"]),
});
```

**Step 2: Add Indexes for Queries**

Add indexes for fields you'll frequently query:
- Single field indexes: `.index("by_field", ["field"])`
- Compound indexes: `.index("by_field1_field2", ["field1", "field2"])`

**Rule**: If you query by a field, add an index for it.

**Step 3: Create Queries Using Schema**

```typescript
// convex/posts.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getByAuthor = query({
  args: { authorId: v.id("users") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("posts")
      .withIndex("by_author", (q) => q.eq("authorId", args.authorId))
      .collect();
  },
});
```

**Step 4: Deploy Schema Changes**

Schema changes deploy automatically with `npx convex dev` or when you push to production.

### Workflow 3: Implement Scheduled Action Pattern

Use this pattern for async operations like API calls, emails, or background jobs.

**Step 1: Create Action for Side Effect**

```typescript
// convex/actions.ts
import { action } from "./_generated/server";
import { v } from "convex/values";

export const sendWelcomeEmail = action({
  args: {
    email: v.string(),
    name: v.string()
  },
  handler: async (ctx, args) => {
    // Call external email API
    await fetch("https://api.emailservice.com/send", {
      method: "POST",
      headers: { "Authorization": `Bearer ${process.env.EMAIL_API_KEY}` },
      body: JSON.stringify({
        to: args.email,
        subject: "Welcome!",
        body: `Hello ${args.name}, welcome to our app!`,
      }),
    });

    // Optionally update database via mutation
    await ctx.runMutation(api.mutations.markEmailSent, {
      email: args.email,
    });
  },
});
```

**Step 2: Schedule Action from Mutation**

```typescript
// convex/mutations.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const createUser = mutation({
  args: {
    clerkId: v.string(),
    email: v.string(),
    name: v.string()
  },
  handler: async (ctx, args) => {
    // Create user in database
    const userId = await ctx.db.insert("users", {
      clerkId: args.clerkId,
      email: args.email,
      name: args.name,
      createdAt: Date.now(),
    });

    // Schedule welcome email (async)
    await ctx.scheduler.runAfter(0, api.actions.sendWelcomeEmail, {
      email: args.email,
      name: args.name,
    });

    return userId;
  },
});
```

**Timing Options:**
- `runAfter(0, ...)` - Run immediately (async)
- `runAfter(60000, ...)` - Run after 1 minute
- `runAt(timestamp, ...)` - Run at specific time

### Workflow 4: File Storage with Progress

**Step 1: Generate Upload URL**

```typescript
// convex/storage.ts
import { mutation } from "./_generated/server";

export const generateUploadUrl = mutation(async (ctx) => {
  return await ctx.storage.generateUploadUrl();
});
```

**Step 2: Upload File from Frontend**

```typescript
// In your Next.js component
const uploadFile = async (file: File) => {
  // Get upload URL
  const uploadUrl = await convex.mutation(api.storage.generateUploadUrl);

  // Upload file
  const result = await fetch(uploadUrl, {
    method: "POST",
    headers: { "Content-Type": file.type },
    body: file,
  });

  const { storageId } = await result.json();

  // Save storage ID to database
  await convex.mutation(api.mutations.saveFile, {
    storageId,
    filename: file.name,
    contentType: file.type,
  });
};
```

**Step 3: Get File URL**

```typescript
// convex/queries.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getFileUrl = query({
  args: { storageId: v.string() },
  handler: async (ctx, args) => {
    // ALWAYS use ctx.storage.getUrl()
    const url = await ctx.storage.getUrl(args.storageId);
    return url;
  },
});
```

## Troubleshooting

### Issue: CORS Policy Blocked in Browser

**Symptoms:**
- Endpoint works in Postman/curl
- Browser console shows CORS error
- Request fails with no response

**Cause:** Missing CORS headers in HTTP endpoint responses

**Solution:**

1. Add CORS headers constant:
```typescript
const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS, GET, PUT, DELETE",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Vary": "Origin",
};
```

2. Include CORS headers in ALL responses (success, error, OPTIONS):
```typescript
return new Response(
  JSON.stringify({ data }),
  { status: 200, headers: CORS_HEADERS }
);
```

3. Add OPTIONS handler for preflight:
```typescript
http.route({
  path: "/your-endpoint",
  method: "OPTIONS",
  handler: httpAction(async () => {
    return new Response(null, { status: 200, headers: CORS_HEADERS });
  }),
});
```

**Frequency:** High (very common mistake)

### Issue: 404 Not Found on HTTP Endpoints

**Symptoms:**
- Endpoint configured in convex/http.ts
- Dashboard shows endpoint exists
- Frontend gets 404 error

**Cause:** Using `.convex.cloud` domain instead of `.convex.site`

**Solution:**

```typescript
// ❌ Wrong
const url = `${process.env.NEXT_PUBLIC_CONVEX_URL}/endpoint`;

// ✅ Correct
const url = `${process.env.NEXT_PUBLIC_CONVEX_URL.replace('.convex.cloud', '.convex.site')}/endpoint`;
```

**Why:** `.convex.cloud` is for the Convex dashboard UI, `.convex.site` is for HTTP endpoints.

**Frequency:** High (common mistake)

### Issue: Storage URL Returns Null

**Symptoms:**
- File uploaded successfully
- Storage ID exists
- getUrl() returns null

**Cause:** Manual URL construction instead of using ctx.storage.getUrl()

**Solution:**

```typescript
// ❌ Wrong - manual construction
const url = `https://deployment.convex.cloud/storage/${storageId}`;

// ✅ Correct - use API
const url = await ctx.storage.getUrl(storageId);
```

**Frequency:** Medium

### Issue: 401 Unauthorized on HTTP Endpoints

**Symptoms:**
- Authentication configured
- Token present in request
- Getting 401 error

**Possible Causes & Solutions:**

1. **Missing Bearer prefix:**
```typescript
// ❌ Wrong
headers: { "Authorization": token }

// ✅ Correct
headers: { "Authorization": `Bearer ${token}` }
```

2. **Clerk JWT misconfiguration:**
- Check `CLERK_JWT_ISSUER_DOMAIN` in Convex dashboard
- Verify `convex/auth.config.ts` has correct issuer domain
- Ensure Clerk JWT template is set up correctly

3. **Token expired:**
- Check token expiration
- Refresh token if needed

**Frequency:** Medium

## Validation Checklist

Before considering Convex implementation complete:

- [ ] Functions use correct type (query for reads, mutation for writes, action for side effects)
- [ ] HTTP endpoints include CORS headers in all responses
- [ ] HTTP endpoints have OPTIONS handler for preflight
- [ ] Schema includes indexes for all queried fields
- [ ] Async operations use scheduled actions (ctx.scheduler.runAfter)
- [ ] Actions are scheduled from mutations, not called directly
- [ ] Frontend uses .convex.site domain for HTTP endpoints
- [ ] Storage URLs use ctx.storage.getUrl(), not manual construction
- [ ] Authentication is properly validated where required
- [ ] Error responses include appropriate status codes and CORS headers

## Best Practices

1. **Keep functions focused** - Each query/mutation/action should do one thing well
2. **Use TypeScript strictly** - Leverage generated types from convex/values
3. **Index strategically** - Add indexes for fields you query, but don't over-index
4. **Handle errors gracefully** - Always return proper status codes and error messages
5. **Test locally first** - Use `npx convex dev` to test before deploying
6. **Secure sensitive operations** - Always validate authentication for protected endpoints
7. **Use environment variables** - Never hardcode API keys or secrets

## References

- **Previous expertise**: `.claude/experts/convex-expert/expertise.yaml`
- **Agent integration**: `.claude/agents/agent-convex.md`
- **Official docs**: https://docs.convex.dev
