---
name: wix-backend-api
description: Creates Astro server endpoints (API routes) for Wix CLI applications. Generates backend API routes based on API specifications that handle HTTP requests, integrate with Wix Data collections, and provide server-side functionality. Use when building REST API endpoints, data APIs, server-side processing logic, APIs for frontend applications, form submissions, data mutations, or server-side validation. Triggers: API, endpoint, backend, server, route, HTTP, REST, GET, POST, PUT, DELETE, PATCH, server-side, backend logic, data API, CRUD API.
license: MIT
compatibility: Requires Wix CLI project with Astro server endpoint support
metadata:
  author: wix
  version: "1.0.0"
  category: wix-extensions
---

# Wix Backend API Builder

Creates Astro server endpoint extensions for Wix CLI applications. Backend APIs are server-side routes that handle HTTP requests, process data, and return responses. They are automatically discovered and don't require extension registration. Endpoints are generated based on API specifications and are designed to integrate well with frontend applications in fullstack applications.

## Non-Matching Intents

Do NOT use this skill for:

- **Dashboard admin interfaces** → Use `wix-dashboard-page`
- **Service plugins** (eCommerce SPIs) → Use `wix-service-plugin`
- **Embedded scripts** (client-side) → Use `wix-embedded-script`
- **Backend event handlers** (event-driven) → Use `wix-backend-event`
- **Site widgets** (client components) → Use `wix-site-widget`

## Architecture

Astro server endpoints are TypeScript files (`.ts` extension) in the `src/pages/api/` directory that export named functions for HTTP methods. They are automatically converted to API routes.

**Key characteristics:**

- Files use the `.ts` extension
- Files export named functions: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- Always import `APIRoute` type from 'astro' for proper typing
- Always return `Response` objects
- Use async/await for asynchronous operations
- No extension registration needed (auto-discovered)

## File Structure and Naming

### Basic Endpoint

File path determines the endpoint URL:

```
src/pages/api/users.ts → /api/users
```

### Dynamic Routes

Use square brackets for dynamic parameters:

```
src/pages/api/users/[id].ts → /api/users/:id
src/pages/api/posts/[slug].ts → /api/posts/:slug
src/pages/api/users/[userId]/posts/[postId].ts → /api/users/:userId/posts/:postId
```

## HTTP Methods

Export named functions for each HTTP method you want to support. **Always import the `APIRoute` type from 'astro'** for proper typing:

```typescript
import type { APIRoute } from "astro";

export async function GET({ params, request }) {
  // Handle GET request
}

export async function POST({ params, request }) {
  // Handle POST request
}

export async function PUT({ params, request }) {
  // Handle PUT request
}

export async function DELETE({ params, request }) {
  // Handle DELETE request
}

export async function PATCH({ params, request }) {
  // Handle PATCH request
}
```

## Request Handling

### Path Parameters

Extract dynamic route parameters from `params`:

```typescript
export async function GET({ params }) {
  const { id } = params; // From /api/users/[id]

  if (!id) {
    return new Response(JSON.stringify({ error: "ID required" }), {
      status: 400,
      statusText: "Bad Request",
      headers: { "Content-Type": "application/json" },
    });
  }

  // Use id to fetch data
}
```

### Query Parameters

Extract query string parameters from `request.url` using `new URL(request.url).searchParams`:

```typescript
export async function GET({ request }) {
  const url = new URL(request.url);
  const search = url.searchParams.get("search");
  const limit = parseInt(url.searchParams.get("limit") || "10", 10);
  const offset = parseInt(url.searchParams.get("offset") || "0", 10);

  // Use query parameters
}
```

**Note:** Use `request.url` to access the full URL, and `new URL(request.url).searchParams` for query parameters.

### Request Body

Parse JSON body from POST/PUT requests:

```typescript
export async function POST({ request }) {
  try {
    const body = await request.json();
    const { title, content } = body;

    // Validate required fields
    if (!title || !content) {
      return new Response(
        JSON.stringify({ error: "Title and content required" }),
        {
          status: 400,
          statusText: "Bad Request",
          headers: { "Content-Type": "application/json" },
        }
      );
    }

    // Process data
  } catch (error) {
    return new Response(JSON.stringify({ error: "Invalid JSON" }), {
      status: 400,
      statusText: "Bad Request",
      headers: { "Content-Type": "application/json" },
    });
  }
}
```

### Headers

Access request headers:

```typescript
export async function GET({ request }) {
  const authHeader = request.headers.get("Authorization");
  const contentType = request.headers.get("Content-Type");

  // Use headers
}
```

## Response Patterns

Always return a `Response` object with appropriate status codes and headers. Use `JSON.stringify()` for JSON responses:

### Success Response

```typescript
return new Response(JSON.stringify({ data: result }), {
  status: 200,
  headers: {
    "Content-Type": "application/json",
  },
});
```

### Created Response

```typescript
return new Response(JSON.stringify({ id: newId, ...data }), {
  status: 201,
  headers: {
    "Content-Type": "application/json",
  },
});
```

### Error Responses

```typescript
// Bad Request (400)
return new Response(JSON.stringify({ error: "Invalid input" }), {
  status: 400,
  statusText: "Bad Request",
  headers: { "Content-Type": "application/json" },
});

// Not Found (404)
return new Response(JSON.stringify({ error: "Resource not found" }), {
  status: 404,
  statusText: "Not Found",
  headers: { "Content-Type": "application/json" },
});

// Internal Server Error (500)
return new Response(JSON.stringify({ error: "Internal server error" }), {
  status: 500,
  statusText: "Internal Server Error",
  headers: { "Content-Type": "application/json" },
});
```

## Wix Data Integration

Use `@wix/data` SDK to interact with Wix Data collections:

```typescript
import { items } from "@wix/data";

export async function GET({ params }) {
  const { id } = params;

  try {
    if (id) {
      // Get single item
      const item = await items.get("collectionId", id);
      return new Response(JSON.stringify(item), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    } else {
      // Get all items
      const results = await items.query("collectionId").limit(50).find();

      return new Response(JSON.stringify(results.items), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }
  } catch (error) {
    return new Response(JSON.stringify({ error: "Failed to fetch data" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}

export async function POST({ request }) {
  try {
    const body = await request.json();

    const newItem = await items.insert("collectionId", body);

    return new Response(JSON.stringify(newItem), {
      status: 201,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: "Failed to create item" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}

export async function PUT({ params, request }) {
  const { id } = params;

  if (!id) {
    return new Response(JSON.stringify({ error: "ID required" }), {
      status: 400,
      statusText: "Bad Request",
      headers: { "Content-Type": "application/json" },
    });
  }

  try {
    const body = await request.json();

    const updatedItem = await items.update("collectionId", {
      _id: id,
      ...body,
    });

    return new Response(JSON.stringify(updatedItem), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: "Failed to update item" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}

export async function DELETE({ params }) {
  const { id } = params;

  if (!id) {
    return new Response(JSON.stringify({ error: "ID required" }), {
      status: 400,
      statusText: "Bad Request",
      headers: { "Content-Type": "application/json" },
    });
  }

  try {
    await items.remove("collectionId", id);

    return new Response(null, {
      status: 204,
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: "Failed to delete item" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
```

**Query methods:** `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `between`, `contains`, `startsWith`, `endsWith`, `hasSome`, `hasAll`, `isEmpty`, `isNotEmpty`, `and`, `or`, `not`, `ascending`, `descending`, `limit`, `skip`, `include`

## Output Structure

```
src/pages/api/
├── users.ts              # /api/users endpoint
├── users/
│   └── [id].ts          # /api/users/:id endpoint
└── posts.ts             # /api/posts endpoint
```

## Examples

For additional examples, see [references/backend-api-examples.md](references/backend-api-examples.md).

## Extension Registration

**Backend API endpoints do NOT require extension registration.** They are automatically discovered from the `src/pages/api/` directory structure.

## Code Quality Requirements

- Strict TypeScript (no `any`, explicit return types)
- Import `APIRoute` type from 'astro' for proper typing
- Always return `Response` objects
- Use `JSON.stringify()` for JSON responses
- Use proper HTTP status codes (200, 201, 400, 404, 500, etc.)
- Include proper headers (`Content-Type: application/json`)
- Include `statusText` in error responses for clarity
- Handle errors gracefully with try/catch blocks
- Validate input parameters and request bodies
- Use async/await for asynchronous operations
- Keep endpoints focused and single-purpose
- No `@ts-ignore` comments
