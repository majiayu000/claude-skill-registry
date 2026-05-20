---
name: new-api-route
description: Creates a new Cloudflare Workers API route with typed context, JSON validation, and error handling. Use when adding a new API endpoint or server-side handler.
argument-hint: "<route-path>"
disable-model-invocation: true
---

Create a new API route in the `src/pages/api/` directory.

## Steps

1. Take the route path from the user's argument (e.g., "webhook", "media/upload"). If not provided, ask for one.
2. Determine the file path: `src/pages/api/<route-path>.ts`. Use kebab-case for filenames.
3. Ask the user:
   - What HTTP method(s) should it handle? (POST is most common)
   - What fields does the request body contain?
   - Should it require Cloudflare Access authentication?
4. Create the API route file using the project template:

```ts
import type { APIContext } from "astro";

export async function POST(context: APIContext) {
  const env = context.locals.runtime.env;

  let body: { /* typed fields */ };
  try {
    body = await context.request.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Validate required fields
  // Process request
  // Return JSON response with Content-Type header

  return new Response(JSON.stringify({ success: true }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}
```

5. If authentication is needed, add the auth guard at the top of the handler:

```ts
import { verifyAccessJwt } from "../../lib/access";

// Inside handler:
const user = await verifyAccessJwt(context.request, env);
if (!user) {
  return new Response(JSON.stringify({ error: "Unauthorized" }), {
    status: 403,
    headers: { "Content-Type": "application/json" },
  });
}
```

6. Follow these conventions:
   - Always wrap `context.request.json()` in try/catch
   - Always set `Content-Type: application/json` on responses
   - Access Cloudflare bindings via `context.locals.runtime.env`
   - API routes are SSR by default (no prerender export)
   - Type the request body explicitly

7. Suggest writing a test for the new route using `createMockContext()` from `tests/setup.ts`.
