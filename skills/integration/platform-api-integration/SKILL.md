---
name: platform-api-integration
description: Guide for discovering and integrating with Rubin Science Platform (RSP) APIs using OpenAPI specifications. Use this skill when working with Gafaelfawr authentication APIs (/auth/*), Times Square notebook APIs (/times-square/api/*), or other RSP services. Covers finding OpenAPI specs, using WebFetch to download specifications, creating TypeScript types from schemas, implementing SWR-based hooks, handling authentication patterns (CSRF tokens, credentials), and creating mock APIs for development.
---

# Platform API Integration

This skill covers discovering, exploring, and integrating with Rubin Science Platform (RSP) APIs using their OpenAPI specifications.

## Quick Reference: OpenAPI Specifications

See [api-registry.md](reference/api-registry.md) for a complete list of RSP APIs and their OpenAPI specification URLs.

**Primary APIs:**
- **Gafaelfawr** (Authentication): https://gafaelfawr.lsst.io/_static/openapi.json
- **Times Square** (Notebooks): https://times-square.lsst.io/_static/openapi.json

## When to Use This Skill

Use this skill when you need to:
- Find API documentation for RSP services
- Discover available endpoints and their parameters
- Understand request/response schemas
- Implement new API integrations
- Create TypeScript types from API schemas
- Set up authentication for API calls
- Create mock APIs for local development

## Discovering API Endpoints

### Using WebFetch to Download OpenAPI Specs

When you need to explore an API, use the WebFetch tool to download the OpenAPI specification:

```typescript
// Example: Get Gafaelfawr API documentation
WebFetch({
  url: 'https://gafaelfawr.lsst.io/_static/openapi.json',
  prompt: 'Show me the available endpoints and their descriptions'
})
```

**What to ask for:**
- "Show me all endpoints for user token management"
- "What are the parameters for the create token endpoint?"
- "What does the user-info response schema look like?"
- "What authentication is required for this endpoint?"

### Navigating OpenAPI Structure

OpenAPI specs are organized into these main sections:

**Paths** (`/paths`):
- Contains all available endpoints
- HTTP methods (GET, POST, DELETE, etc.)
- Path parameters (e.g., `{username}`, `{token_key}`)
- Query parameters
- Request bodies
- Response schemas

**Schemas** (`/components/schemas`):
- Type definitions for request/response bodies
- Reusable data models
- Validation rules

**Security** (`/components/securitySchemes`):
- Authentication requirements
- OAuth scopes
- API keys

### Finding Endpoint Details

To find information about a specific endpoint:

1. **Use WebFetch** to download the OpenAPI spec
2. **Search for the path** (e.g., `/api/v1/user-info`)
3. **Check the method** (GET, POST, DELETE, etc.)
4. **Review parameters** (path, query, body)
5. **Examine responses** (200, 400, 401, etc.)
6. **Note authentication** requirements

## API-Specific Patterns

### Gafaelfawr APIs (Authentication & Token Management)

**Path Prefix:** `/auth/api/v1/`

**Common Endpoints:**
- `GET /auth/api/v1/user-info` - User profile and authentication status
- `GET /auth/api/v1/login` - CSRF token and available scopes
- `GET /auth/api/v1/users/{username}/tokens` - List user's tokens
- `POST /auth/api/v1/users/{username}/tokens` - Create new token
- `DELETE /auth/api/v1/users/{username}/tokens/{key}` - Delete token
- `GET /auth/api/v1/users/{username}/token-change-history` - Token history with pagination

**Authentication Pattern:**

Gafaelfawr APIs use **CSRF tokens** for mutation operations (POST, DELETE):

1. First, get the CSRF token from `/auth/api/v1/login`
2. Include it in mutation requests via `X-CSRF-Token` header (DELETE) or `x-csrf-token` header (POST)
3. Credentials are handled automatically via cookies

**Example Implementations:**

See existing hooks in the codebase:
- `apps/squareone/src/hooks/useUserInfo.ts` - User profile fetching
- `apps/squareone/src/hooks/useLoginInfo.ts` - CSRF token retrieval
- `apps/squareone/src/hooks/useUserTokens.ts` - Token listing
- `apps/squareone/src/hooks/useTokenCreation.ts` - Token creation with CSRF
- `apps/squareone/src/hooks/useDeleteToken.ts` - Token deletion with CSRF
- `apps/squareone/src/hooks/useTokenChangeHistory.ts` - Pagination example

**Pagination Pattern:**

Gafaelfawr uses **cursor-based pagination** with Link headers:

```typescript
// Parse RFC 5988 Link headers for next cursor
const linkHeader = response.headers.get('Link');
const totalCount = response.headers.get('X-Total-Count');

// Use useSWRInfinite for infinite scroll
const { data, size, setSize, isValidating } = useSWRInfinite(
  (pageIndex, previousPageData) => {
    // Extract cursor from previous page
    const cursor = previousPageData?.nextCursor;
    return cursor ? `/api/endpoint?cursor=${cursor}` : '/api/endpoint';
  }
);
```

### Times Square APIs (Notebook Execution)

**Path Prefix:** `/times-square/api/v1/`

**Common Endpoints:**
- `GET /times-square/api/v1/pages` - List all pages
- `GET /times-square/api/v1/pages/{page}` - Get page metadata
- `GET /times-square/api/v1/pages/{page}/html` - Get rendered HTML
- `GET /times-square/api/v1/pages/{page}/htmlstatus` - Check rendering status
- `GET /times-square/api/v1/pages/{page}/htmlevents` - SSE stream for real-time updates

**Authentication Pattern:**

Times Square APIs use **cookie-based authentication** (via Gafaelfawr):
- No explicit token needed in requests
- Credentials handled automatically
- No CSRF tokens required for GET requests

**Parameter-based URLs:**

Times Square APIs accept notebook parameters as URL query parameters:

```typescript
function parameterizeUrl(
  baseUrl: string,
  parameters: Record<string, any>,
  displaySettings: Record<string, any>
): string {
  const url = new URL(baseUrl);

  // Add notebook parameters
  Object.entries(parameters).forEach(([key, value]) => {
    url.searchParams.set(key, String(value));
  });

  // Add display settings
  Object.entries(displaySettings).forEach(([key, value]) => {
    url.searchParams.set(key, String(value));
  });

  return url.toString();
}
```

**Polling Pattern:**

For checking notebook rendering status, use **polling with SWR**:

```typescript
const { data, error } = useSWR<HtmlStatusData>(
  htmlStatusUrl,
  fetcher,
  {
    refreshInterval: 1000, // Poll every 1 second
    revalidateOnFocus: false, // Don't revalidate on window focus during polling
  }
);
```

**Server-Sent Events (SSE):**

For real-time updates, Times Square provides SSE endpoints:
- Connect to `/pages/{page}/htmlevents`
- Receive `status` events as notebook executes
- Context provider: `TimesSquareHtmlEventsContext`

**Example Implementations:**

See existing implementations:
- `apps/squareone/src/hooks/useTimesSquarePage.ts` - Page metadata
- `apps/squareone/src/components/TimesSquareNotebookViewer/useHtmlStatus.ts` - Status polling
- `apps/squareone/src/contexts/TimesSquareUrlParametersContext.tsx` - URL parameters
- `apps/squareone/src/contexts/TimesSquareHtmlEventsContext.tsx` - SSE integration

## Standard Integration Pattern

### Step-by-Step: Adding a New API Endpoint

**1. Find the Endpoint in OpenAPI Spec**

Use WebFetch to download the OpenAPI spec and find:
- Endpoint path
- HTTP method
- Request parameters
- Response schema
- Authentication requirements

**2. Create TypeScript Types**

Extract the response schema from OpenAPI and create TypeScript types:

```typescript
// Based on OpenAPI schema
type UserInfo = {
  username: string;
  name?: string;
  email?: string;
  uid?: number;
  gid?: number;
  groups?: Group[];
};

type Group = {
  id: number;
  name: string;
};
```

**3. Create a Custom Hook**

Follow the SWR-based hook pattern. See [hook-template.tsx](examples/hook-template.tsx) for a complete template.

**Basic pattern:**

```typescript
import useSWR from 'swr';

type UseApiHookResult = {
  data: ResponseType | undefined;
  isLoading: boolean;
  error: Error | undefined;
  mutate: () => void;
};

export function useApiHook(): UseApiHookResult {
  const { data, error, isLoading, mutate } = useSWR<ResponseType>(
    '/api/endpoint',
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      dedupingInterval: 10000, // 10 second cache
    }
  );

  return {
    data,
    isLoading,
    error,
    mutate,
  };
}
```

**4. Handle Authentication**

For Gafaelfawr mutations:

```typescript
// Get CSRF token first
const { data: loginData } = useLoginInfo();
const csrfToken = loginData?.csrf;

// Use in mutation
const response = await fetch('/auth/api/v1/endpoint', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-csrf-token': csrfToken,
  },
  body: JSON.stringify(payload),
});
```

**5. Implement Error Handling**

Parse API errors and provide user-friendly messages:

```typescript
type ApiError = {
  detail?: string | Array<{ loc: string[]; msg: string; type: string }>;
  message?: string;
};

function parseError(response: Response, data: ApiError): Error {
  // Handle Pydantic validation errors
  if (Array.isArray(data.detail)) {
    const errors = data.detail.map(err => err.msg).join(', ');
    return new Error(errors);
  }

  // Handle simple error messages
  if (data.detail) {
    return new Error(data.detail);
  }

  // Fallback to HTTP status
  return new Error(`HTTP ${response.status}: ${response.statusText}`);
}
```

**6. Create Mock API for Development**

Create a mock endpoint in `/pages/api/dev/`:

```typescript
// pages/api/dev/endpoint.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Return mock data matching OpenAPI schema
  res.status(200).json({
    username: 'testuser',
    name: 'Test User',
    email: 'test@example.com',
  });
}
```

**7. Set Up Development Rewrites**

Add to `next.config.js`:

```javascript
async rewrites() {
  return [
    {
      source: '/api/endpoint',
      destination: '/api/dev/endpoint',
    },
  ];
}
```

## Development Workflow

### Local Development with Mocks

For local development without backend services:

1. **Create mock endpoints** in `/pages/api/dev/` matching OpenAPI schemas
2. **Set up Next.js rewrites** to redirect API calls to mocks
3. **Use environment variables** to toggle between real and mock APIs

**Example rewrite configuration:**

```javascript
// next.config.js
async rewrites() {
  if (process.env.NODE_ENV === 'development') {
    return [
      // Gafaelfawr mocks
      {
        source: '/auth/api/v1/user-info',
        destination: '/api/dev/user-info',
      },
      // Times Square mocks
      {
        source: '/times-square/api/v1/pages/:page',
        destination: '/api/dev/times-square/v1/pages/:page',
      },
    ];
  }
  return [];
}
```

### Mock Data Best Practices

1. **Match OpenAPI schemas exactly** - Use the same field names and types
2. **Include realistic data** - Mimic production responses
3. **Test error cases** - Create mock endpoints that return errors
4. **Use query parameters** - Support filtering and pagination in mocks
5. **Maintain mock data files** - Store mock data in `/src/lib/mocks/`

**Example mock data organization:**

```
src/lib/mocks/
├── gafaelfawr/
│   ├── user-info.ts
│   ├── tokens.ts
│   └── token-history.ts
└── times-square/
    ├── pages.ts
    └── page-metadata.ts
```

## Common Patterns

### SWR Configuration

**Standard configuration for most endpoints:**

```typescript
{
  revalidateOnFocus: true,      // Refresh when window gains focus
  revalidateOnReconnect: true,  // Refresh on network recovery
  dedupingInterval: 10000,      // Cache for 10 seconds
}
```

**For polling status endpoints:**

```typescript
{
  refreshInterval: 1000,        // Poll every 1 second
  revalidateOnFocus: false,     // Don't revalidate during polling
}
```

**For static/rarely-changing data:**

```typescript
{
  revalidateOnFocus: false,
  revalidateOnReconnect: false,
  revalidateIfStale: false,
}
```

### Fetcher Function

**Standard fetcher with error handling:**

```typescript
const fetcher = async (...args: Parameters<typeof fetch>) => {
  const response = await fetch(...args);

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw parseError(response, data);
  }

  return response.json();
};
```

### Hook Return Pattern

**Consistent return types across all hooks:**

```typescript
return {
  data,           // Response data (undefined while loading)
  isLoading,      // True during initial fetch
  error,          // Error object if request failed
  mutate,         // Function to manually revalidate
};
```

## TypeScript Best Practices

### Type Definitions

**Extract types from OpenAPI schemas:**

```typescript
// User types
type GafaelfawrUser = {
  username: string;
  name?: string;
  email?: string;
  uid?: number;
  gid?: number;
  groups?: GafaelfawrGroup[];
  quota?: GafaelfawrQuota | null;
};

type GafaelfawrGroup = {
  id: number;
  name: string;
};

// Export for reuse
export type { GafaelfawrUser, GafaelfawrGroup };
```

**Use discriminated unions for token types:**

```typescript
type TokenType =
  | 'session'
  | 'user'
  | 'notebook'
  | 'internal'
  | 'service'
  | 'oidc';

type TokenInfo = {
  token_type: TokenType;
  token: string;
  username: string;
  // ... other fields
};
```

### Error Types

**Create specific error types for better error handling:**

```typescript
type TokenCreationError = {
  type: 'validation' | 'network' | 'server';
  message: string;
  statusCode?: number;
  details?: unknown;
};
```

## Troubleshooting

### OpenAPI Spec Not Loading

**Problem:** WebFetch cannot retrieve the OpenAPI specification.

**Solutions:**
- Verify the URL is correct (check [api-registry.md](reference/api-registry.md))
- Check if the service is accessible
- Try accessing the URL directly in a browser
- Some services may require authentication to access OpenAPI specs

### Type Mismatches

**Problem:** TypeScript types don't match actual API responses.

**Solutions:**
- Download the latest OpenAPI spec
- Check for API version differences
- Verify the endpoint path is correct
- Log actual responses during development

### CSRF Token Errors

**Problem:** Gafaelfawr mutations fail with 403 errors.

**Solutions:**
- Ensure you're calling `useLoginInfo()` to get the CSRF token
- Verify the CSRF token is included in request headers
- Check header name: `X-CSRF-Token` for DELETE, `x-csrf-token` for POST
- Ensure cookies are being sent with requests

### Mock API Not Being Used

**Problem:** Real API is called instead of mock in development.

**Solutions:**
- Check `next.config.js` rewrites configuration
- Verify `NODE_ENV === 'development'`
- Ensure mock endpoint path matches the rewrite destination
- Restart the dev server after config changes

## Related Skills

- **data-fetching-patterns** - SWR patterns, custom hooks, error handling
- **times-square-integration** - Times Square specific patterns and contexts
- **testing-infrastructure** - Testing API hooks and mocks

## Related Files

- `/pages/api/dev/` - Mock API endpoints for development
- `apps/squareone/src/hooks/` - Existing API hook implementations
- `apps/squareone/next.config.js` - Next.js rewrite configuration
- `packages/squared/src/hooks/` - Shared API hooks

## Additional Resources

**OpenAPI Specifications:**
- Gafaelfawr documentation: https://gafaelfawr.lsst.io
- Times Square documentation: https://times-square.lsst.io
- OpenAPI specification: https://spec.openapis.org/oas/latest.html

**Related Documentation:**
- SWR documentation: https://swr.vercel.app
- Next.js API routes: https://nextjs.org/docs/api-routes/introduction
