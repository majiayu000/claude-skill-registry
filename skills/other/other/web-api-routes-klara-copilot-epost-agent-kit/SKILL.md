---
name: web-api-routes
description: Use when working with route.ts files, API endpoints, server actions, or web backend logic in the monorepo
user-invokable: false

metadata:
  agent-affinity: [epost-implementer]
  keywords: [api, rest, fetchbuilder, caller, server-action, route, endpoint]
  platforms: [web]
  triggers: ["route.ts", "api/", "server action", "endpoint", "caller", "fetchbuilder"]
  connections:
    enhances: [web-frontend]
---

# Web API Routes — FetchBuilder & Caller Patterns

## Purpose

HTTP client patterns for Next.js apps. All API calls go through FetchBuilder. Server actions use the caller pattern. Route handlers proxy binary data or handle internal APIs.

## FetchBuilder

**Location**: `service/fetch-builder.ts`

Fluent builder for all HTTP calls. **Never throws** — returns `FetchResponse<T>` with `result` or `error`.

### Types

```typescript
export type ErrorResponse = { status: number; reason: string };

export interface FetchResponse<T> {
  result?: T;
  error?: ErrorResponse;
  tenantId?: string;
}

export const isErrorResponse = (response: unknown): response is ErrorResponse => {
  return typeof response === 'object' && response !== null
    && 'status' in response && 'reason' in response;
};
```

### Builder API

See `references/fetch-builder.md` for the full FetchBuilder API.

## Caller Pattern

**Location**: `caller/` — all files begin with `'use server'`.

See `references/caller-patterns.md` for caller implementation examples (Pattern A: explicit params, Pattern B: session auto-extracted).

## API URL Constants

**Location**: `libs/utils/src/lib/constants/API-urls.ts`

Namespaced objects with `:placeholder` convention:

```typescript
export const MY_SERVICE_API = {
  USER_PROFILE: SERVICE_BASE_URL + '/v2/:tenantId/profile',
  GET_ITEMS:    SERVICE_BASE_URL + '/:tenantId/items',
  UPDATE_USER:  SERVICE_BASE_URL + '/:tenantId/users/:username',
};

export const ANOTHER_SERVICE_API = {
  CONTACTS:    ANOTHER_SERVICE_URL + '/:tenantId/contacts',
  SETTINGS:    ANOTHER_SERVICE_URL + '/:tenantId/settings',
};
```

### Placeholder Convention

- `:tenantId` — first-class via `.withTenantId()` builder method
- `:username` — first-class via `.withUsername()` builder method
- `:workplaceId` — first-class via `.withWorkplaceId()` builder method
- Other (`:contactId`, `:documentId`, etc.) — manual `.replace()` before `.withUrl()`
- Query string placeholders also use `:name` syntax, substituted manually

## Route Handlers

**Location**: `app/api/` — used for binary data proxying and internal APIs.

Route handlers use raw `fetch()` (not FetchBuilder) since they proxy directly:

```typescript
// app/api/documents/thumbnail/route.ts
export async function GET(request: Request) {
  const session = await getServerSession(Options);
  const token = session?.accessToken;
  const requestUrl = MY_SERVICE_API.DOCUMENT_THUMBNAIL
    .replace(':tenantId', tenantId)
    .replace(':documentId', documentId);

  const response = await fetch(requestUrl, {
    headers: { Authorization: `Bearer ${token}` },
    cache: 'no-cache',
  });
  const arrayBuffer = await response.arrayBuffer();
  return new Response(arrayBuffer, { status: 200, headers: { ... } });
}
```

## Reference Files

| File | Purpose |
|------|---------|
| `references/fetch-builder.md` | Complete FetchBuilder API + waterfall prevention |
| `references/caller-patterns.md` | Detailed caller examples, both patterns |

## Rules

- **All app-level API calls through FetchBuilder** — never raw `fetch()` (except route.ts proxies)
- **Always check `response.error`** — FetchBuilder never throws
- **Use API constants** from your shared utils — never hardcode URLs
- **Use `:placeholder` convention** — substitute via builder methods or `.replace()`
- **Do NOT use**: Express, Hono, Prisma, Drizzle, SWR, React Query — none exist in this project
