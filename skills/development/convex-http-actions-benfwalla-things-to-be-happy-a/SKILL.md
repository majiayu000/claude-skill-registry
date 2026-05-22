---
name: convex-http-actions
displayName: Convex HTTP Actions
description: External API integration and webhook handling including HTTP endpoint routing, request/response handling, authentication, CORS configuration, and webhook signature validation
version: 1.0.0
author: Convex
tags: [convex, http, actions, webhooks, api, endpoints]
---

# Convex HTTP Actions

Build HTTP endpoints for webhooks, external API integrations, and custom routes in Convex applications.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/functions/http-actions
- Actions Overview: https://docs.convex.dev/functions/actions
- Authentication: https://docs.convex.dev/auth
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### HTTP Actions Overview

HTTP actions allow you to define HTTP endpoints in Convex that can:

- Receive webhooks from third-party services
- Create custom API routes
- Handle file uploads
- Integrate with external services
- Serve dynamic content

### Basic HTTP Router Setup

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

// Simple GET endpoint
http.route({
  path: "/health",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    return new Response(JSON.stringify({ status: "ok" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }),
});

export default http;
```

### Request Handling

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

// Handle JSON body
http.route({
  path: "/api/data",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    // Parse JSON body
    const body = await request.json();
    
    // Access headers
    const authHeader = request.headers.get("Authorization");
    
    // Access URL parameters
    const url = new URL(request.url);
    const queryParam = url.searchParams.get("filter");

    return new Response(
      JSON.stringify({ received: body, filter: queryParam }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  }),
});

// Handle form data
http.route({
  path: "/api/form",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const formData = await request.formData();
    const name = formData.get("name");
    const email = formData.get("email");

    return new Response(
      JSON.stringify({ name, email }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  }),
});

// Handle raw bytes
http.route({
  path: "/api/upload",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const bytes = await request.bytes();
    const contentType = request.headers.get("Content-Type") ?? "application/octet-stream";
    
    // Store in Convex storage
    const blob = new Blob([bytes], { type: contentType });
    const storageId = await ctx.storage.store(blob);

    return new Response(
      JSON.stringify({ storageId }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  }),
});

export default http;
```

### Path Parameters

Use path prefix matching for dynamic routes:

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

// Match /api/users/* with pathPrefix
http.route({
  pathPrefix: "/api/users/",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    // Extract user ID from path: /api/users/123 -> "123"
    const userId = url.pathname.replace("/api/users/", "");

    return new Response(
      JSON.stringify({ userId }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  }),
});

export default http;
```

### CORS Configuration

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

// CORS headers helper
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Access-Control-Max-Age": "86400",
};

// Handle preflight requests
http.route({
  path: "/api/data",
  method: "OPTIONS",
  handler: httpAction(async () => {
    return new Response(null, {
      status: 204,
      headers: corsHeaders,
    });
  }),
});

// Actual endpoint with CORS
http.route({
  path: "/api/data",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.json();

    return new Response(
      JSON.stringify({ success: true, data: body }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          ...corsHeaders,
        },
      }
    );
  }),
});

export default http;
```

### Webhook Handling

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { internal } from "./_generated/api";

const http = httpRouter();

// Stripe webhook
http.route({
  path: "/webhooks/stripe",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const signature = request.headers.get("stripe-signature");
    if (!signature) {
      return new Response("Missing signature", { status: 400 });
    }

    const body = await request.text();

    // Verify webhook signature (in action with Node.js)
    try {
      await ctx.runAction(internal.stripe.verifyAndProcessWebhook, {
        body,
        signature,
      });
      return new Response("OK", { status: 200 });
    } catch (error) {
      console.error("Webhook error:", error);
      return new Response("Webhook error", { status: 400 });
    }
  }),
});

// GitHub webhook
http.route({
  path: "/webhooks/github",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const event = request.headers.get("X-GitHub-Event");
    const signature = request.headers.get("X-Hub-Signature-256");
    
    if (!signature) {
      return new Response("Missing signature", { status: 400 });
    }

    const body = await request.text();

    await ctx.runAction(internal.github.processWebhook, {
      event: event ?? "unknown",
      body,
      signature,
    });

    return new Response("OK", { status: 200 });
  }),
});

export default http;
```

### Webhook Signature Verification

```typescript
// convex/stripe.ts
"use node";

import { internalAction, internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export const verifyAndProcessWebhook = internalAction({
  args: {
    body: v.string(),
    signature: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

    // Verify signature
    const event = stripe.webhooks.constructEvent(
      args.body,
      args.signature,
      webhookSecret
    );

    // Process based on event type
    switch (event.type) {
      case "checkout.session.completed":
        await ctx.runMutation(internal.payments.handleCheckoutComplete, {
          sessionId: event.data.object.id,
          customerId: event.data.object.customer as string,
        });
        break;

      case "customer.subscription.updated":
        await ctx.runMutation(internal.subscriptions.handleUpdate, {
          subscriptionId: event.data.object.id,
          status: event.data.object.status,
        });
        break;
    }

    return null;
  },
});
```

### Authentication in HTTP Actions

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { internal } from "./_generated/api";

const http = httpRouter();

// API key authentication
http.route({
  path: "/api/protected",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const apiKey = request.headers.get("X-API-Key");
    
    if (!apiKey) {
      return new Response(
        JSON.stringify({ error: "Missing API key" }),
        { status: 401, headers: { "Content-Type": "application/json" } }
      );
    }

    // Validate API key
    const isValid = await ctx.runQuery(internal.auth.validateApiKey, {
      apiKey,
    });

    if (!isValid) {
      return new Response(
        JSON.stringify({ error: "Invalid API key" }),
        { status: 403, headers: { "Content-Type": "application/json" } }
      );
    }

    // Process authenticated request
    const data = await ctx.runQuery(internal.data.getProtectedData, {});

    return new Response(
      JSON.stringify(data),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  }),
});

// Bearer token authentication
http.route({
  path: "/api/user",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const authHeader = request.headers.get("Authorization");
    
    if (!authHeader?.startsWith("Bearer ")) {
      return new Response(
        JSON.stringify({ error: "Missing or invalid Authorization header" }),
        { status: 401, headers: { "Content-Type": "application/json" } }
      );
    }

    const token = authHeader.slice(7);

    // Validate token and get user
    const user = await ctx.runQuery(internal.auth.validateToken, { token });

    if (!user) {
      return new Response(
        JSON.stringify({ error: "Invalid token" }),
        { status: 403, headers: { "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify(user),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  }),
});

export default http;
```

### Calling Mutations and Queries

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { api, internal } from "./_generated/api";

const http = httpRouter();

http.route({
  path: "/api/items",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.json();

    // Call a mutation
    const itemId = await ctx.runMutation(internal.items.create, {
      name: body.name,
      description: body.description,
    });

    // Query the created item
    const item = await ctx.runQuery(internal.items.get, { id: itemId });

    return new Response(
      JSON.stringify(item),
      { status: 201, headers: { "Content-Type": "application/json" } }
    );
  }),
});

http.route({
  path: "/api/items",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const limit = parseInt(url.searchParams.get("limit") ?? "10");

    const items = await ctx.runQuery(internal.items.list, { limit });

    return new Response(
      JSON.stringify(items),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  }),
});

export default http;
```

### Error Handling

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

// Helper for JSON responses
function jsonResponse(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

// Helper for error responses
function errorResponse(message: string, status: number) {
  return jsonResponse({ error: message }, status);
}

http.route({
  path: "/api/process",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    try {
      // Validate content type
      const contentType = request.headers.get("Content-Type");
      if (!contentType?.includes("application/json")) {
        return errorResponse("Content-Type must be application/json", 415);
      }

      // Parse body
      let body;
      try {
        body = await request.json();
      } catch {
        return errorResponse("Invalid JSON body", 400);
      }

      // Validate required fields
      if (!body.data) {
        return errorResponse("Missing required field: data", 400);
      }

      // Process request
      const result = await ctx.runMutation(internal.process.handle, {
        data: body.data,
      });

      return jsonResponse({ success: true, result }, 200);
    } catch (error) {
      console.error("Processing error:", error);
      return errorResponse("Internal server error", 500);
    }
  }),
});

export default http;
```

### File Downloads

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { Id } from "./_generated/dataModel";

const http = httpRouter();

http.route({
  pathPrefix: "/files/",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const fileId = url.pathname.replace("/files/", "") as Id<"_storage">;

    // Get file URL from storage
    const fileUrl = await ctx.storage.getUrl(fileId);

    if (!fileUrl) {
      return new Response("File not found", { status: 404 });
    }

    // Redirect to the file URL
    return Response.redirect(fileUrl, 302);
  }),
});

export default http;
```

## Examples

### Complete Webhook Integration

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { internal } from "./_generated/api";

const http = httpRouter();

// Clerk webhook for user sync
http.route({
  path: "/webhooks/clerk",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const svixId = request.headers.get("svix-id");
    const svixTimestamp = request.headers.get("svix-timestamp");
    const svixSignature = request.headers.get("svix-signature");

    if (!svixId || !svixTimestamp || !svixSignature) {
      return new Response("Missing Svix headers", { status: 400 });
    }

    const body = await request.text();

    try {
      await ctx.runAction(internal.clerk.verifyAndProcess, {
        body,
        svixId,
        svixTimestamp,
        svixSignature,
      });
      return new Response("OK", { status: 200 });
    } catch (error) {
      console.error("Clerk webhook error:", error);
      return new Response("Webhook verification failed", { status: 400 });
    }
  }),
});

export default http;
```

```typescript
// convex/clerk.ts
"use node";

import { internalAction, internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";
import { Webhook } from "svix";

export const verifyAndProcess = internalAction({
  args: {
    body: v.string(),
    svixId: v.string(),
    svixTimestamp: v.string(),
    svixSignature: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const webhookSecret = process.env.CLERK_WEBHOOK_SECRET!;
    const wh = new Webhook(webhookSecret);

    const event = wh.verify(args.body, {
      "svix-id": args.svixId,
      "svix-timestamp": args.svixTimestamp,
      "svix-signature": args.svixSignature,
    }) as { type: string; data: Record<string, unknown> };

    switch (event.type) {
      case "user.created":
        await ctx.runMutation(internal.users.create, {
          clerkId: event.data.id as string,
          email: (event.data.email_addresses as Array<{ email_address: string }>)[0]?.email_address,
          name: `${event.data.first_name} ${event.data.last_name}`,
        });
        break;

      case "user.updated":
        await ctx.runMutation(internal.users.update, {
          clerkId: event.data.id as string,
          email: (event.data.email_addresses as Array<{ email_address: string }>)[0]?.email_address,
          name: `${event.data.first_name} ${event.data.last_name}`,
        });
        break;

      case "user.deleted":
        await ctx.runMutation(internal.users.remove, {
          clerkId: event.data.id as string,
        });
        break;
    }

    return null;
  },
});
```

### Schema for HTTP API

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  apiKeys: defineTable({
    key: v.string(),
    userId: v.id("users"),
    name: v.string(),
    createdAt: v.number(),
    lastUsedAt: v.optional(v.number()),
    revokedAt: v.optional(v.number()),
  })
    .index("by_key", ["key"])
    .index("by_user", ["userId"]),

  webhookEvents: defineTable({
    source: v.string(),
    eventType: v.string(),
    payload: v.any(),
    processedAt: v.number(),
    status: v.union(
      v.literal("success"),
      v.literal("failed")
    ),
    error: v.optional(v.string()),
  })
    .index("by_source", ["source"])
    .index("by_status", ["status"]),

  users: defineTable({
    clerkId: v.string(),
    email: v.string(),
    name: v.string(),
  }).index("by_clerk_id", ["clerkId"]),
});
```

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Always validate and sanitize incoming request data
- Use internal functions for database operations
- Implement proper error handling with appropriate status codes
- Add CORS headers for browser-accessible endpoints
- Verify webhook signatures before processing
- Log webhook events for debugging
- Use environment variables for secrets
- Handle timeouts gracefully

## Common Pitfalls

1. **Missing CORS preflight handler** - Browsers send OPTIONS requests first
2. **Not validating webhook signatures** - Security vulnerability
3. **Exposing internal functions** - Use internal functions from HTTP actions
4. **Forgetting Content-Type headers** - Clients may not parse responses correctly
5. **Not handling request body errors** - Invalid JSON will throw
6. **Blocking on long operations** - Use scheduled functions for heavy processing

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- HTTP Actions: https://docs.convex.dev/functions/http-actions
- Actions: https://docs.convex.dev/functions/actions
- Authentication: https://docs.convex.dev/auth
