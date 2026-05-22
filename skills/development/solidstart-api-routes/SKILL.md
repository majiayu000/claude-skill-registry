---
name: solidstart-api-routes
description: "SolidStart API routes: export GET/POST/PATCH/DELETE functions, handle APIEvent with request/params/fetch, GraphQL and tRPC integration, session management."
metadata:
  globs:
    - "src/routes/api/**/*"
    - "**/api/**/*.ts"
    - "**/api/**/*.tsx"
---

# SolidStart API Routes

API routes export HTTP method functions instead of components. API routes take priority over UI routes.

## Basic API Routes

```tsx
// routes/api/users.ts
import type { APIEvent } from "@solidjs/start/server";

export async function GET({ request, params, fetch }: APIEvent) {
  const users = await db.getUsers();
  return { users };
}

export async function POST({ request }: APIEvent) {
  const body = await request.json();
  const user = await db.createUser(body);
  return new Response(JSON.stringify(user), {
    status: 201,
    headers: { "Content-Type": "application/json" }
  });
}

export async function PATCH({ request }: APIEvent) {
  // Handle PATCH
}

export async function DELETE({ request }: APIEvent) {
  // Handle DELETE
}
```

## APIEvent Object

`APIEvent` contains:
- `request`: Request object
- `params`: Dynamic route parameters
- `fetch`: Internal fetch for same-origin requests

```tsx
// routes/api/users/[id].ts
export async function GET({ params }: APIEvent) {
  const user = await db.getUser(params.id);
  if (!user) {
    return new Response("Not Found", { status: 404 });
  }
  return { user };
}

export async function DELETE({ params }: APIEvent) {
  await db.deleteUser(params.id);
  return new Response(null, { status: 204 });
}
```

## Session Management

```tsx
import { getCookie } from "vinxi/http";

export async function GET(event: APIEvent) {
  const userId = getCookie("userId");
  if (!userId) {
    return new Response("Unauthorized", { status: 401 });
  }
  
  const user = await db.getUser(userId);
  return { user };
}
```

## Multiple Methods Handler

```tsx
// routes/api/handler.ts
async function handler(event: APIEvent) {
  const method = event.request.method;
  if (method === "GET") {
    return { data: "get" };
  } else if (method === "POST") {
    const body = await event.request.json();
    return { data: "post", body };
  }
}

export const GET = handler;
export const POST = handler;
```

## GraphQL API

```tsx
// routes/graphql.ts
import { buildSchema, graphql } from "graphql";
import type { APIEvent } from "@solidjs/start/server";

const schema = buildSchema(`
  type Query {
    hello: String
  }
`);

const rootValue = {
  hello: () => "Hello World"
};

const handler = async (event: APIEvent) => {
  const body = await event.request.json();
  const result = await graphql({
    schema,
    source: body.query,
    rootValue
  });
  return result;
};

export const GET = handler;
export const POST = handler;
```

## tRPC API

```tsx
// routes/api/trpc/[trpc].ts
import type { APIEvent } from "@solidjs/start/server";
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "~/lib/router";

const handler = (event: APIEvent) =>
  fetchRequestHandler({
    endpoint: "/api/trpc",
    req: event.request,
    router: appRouter,
    createContext: () => ({})
  });

export const GET = handler;
export const POST = handler;
```

## Best Practices

1. API routes for external APIs (GraphQL, tRPC, webhooks, public REST APIs)
2. Return proper status codes (200, 201, 404, 401, etc.)
3. Use `fetch` from APIEvent for internal requests (same-origin)
4. Handle errors with proper error responses
5. Use sessions for authentication in API routes
