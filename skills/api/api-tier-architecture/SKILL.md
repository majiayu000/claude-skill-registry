---
name: api-tier-architecture
description: 3-tier API architecture (Convex WebSocket, SSE, REST) for cross-platform data fetching. Platform detection, hybrid hooks, DAL layer patterns. Triggers on "API", "tier", "Convex", "REST", "SSE", "useConvexQuery", "useQuery", "withAuth", "DAL".
---

# API Tier Architecture

Three-tier API architecture for web (real-time) and mobile (battery-optimized) platforms.

## Architecture Overview

**Tier 1 (Web Desktop):** Convex WebSocket - Real-time bidirectional subscription
**Tier 2 (Mobile):** SSE - Server-Sent Events with polling (battery-optimized)
**Tier 3 (Mobile Fallback):** REST - Standard HTTP polling

All tiers authenticated via `withAuth` middleware, data accessed via DAL layer.

## Platform Detection

```typescript
// From apps/web/src/lib/utils/platform.ts
export function shouldUseConvex(): boolean {
  return getDataFetchingStrategy() === "convex";
}

export function shouldUseSSE(): boolean {
  return getDataFetchingStrategy() === "sse";
}

// Detection hierarchy:
// 1. User-agent (iPhone, Android, mobile browsers)
// 2. Viewport width (< 768px)
// 3. Touch capability
```

**Manual override for testing:**
```typescript
localStorage.setItem("blah_data_strategy", "convex"); // or "sse" or "polling"
```

## Hybrid Hook Pattern

All data hooks use hybrid pattern: Convex for web, React Query for mobile.

```typescript
// From apps/web/src/lib/hooks/queries/useConversations.ts
export function useConversations(options: UseConversationsOptions = {}) {
  const { page = 1, pageSize = 20, archived = false } = options;
  const useConvexMode = shouldUseConvex();
  const apiClient = useApiClient();

  // Tier 1: Convex WebSocket subscription (web desktop)
  const convexData = useConvexQuery(
    api.conversations.list,
    useConvexMode && !archived ? {} : "skip",
  );

  // Tier 2/3: REST API query (mobile)
  const restQuery = useQuery({
    queryKey: ["conversations", { page, pageSize, archived }],
    queryFn: async () => {
      const params = new URLSearchParams({
        page: String(page),
        pageSize: String(pageSize),
        archived: String(archived),
      });
      return apiClient.get(`/conversations?${params}`);
    },
    enabled: !useConvexMode,
    staleTime: 30_000, // 30s cache
  });

  // Return unified interface
  if (useConvexMode) {
    return {
      data: convexData ? { items: convexData, ... } : undefined,
      isLoading: convexData === undefined,
      error: null,
      refetch: () => Promise.resolve(),
    };
  }

  return {
    data: restQuery.data,
    isLoading: restQuery.isLoading,
    error: restQuery.error,
    refetch: restQuery.refetch,
  };
}
```

**Key conventions:**
- Import both `useQuery` from `@tanstack/react-query` and `useQuery as useConvexQuery` from `convex/react`
- Check `shouldUseConvex()` before rendering
- Pass `"skip"` to Convex query when disabled
- Return unified interface: `{ data, isLoading, error, refetch }`

## DAL Layer (Data Access Layer)

Server-only Convex client wrappers. Never import in client components.

```typescript
// From apps/web/src/lib/api/dal/conversations.ts
import "server-only";

export const conversationsDAL = {
  create: async (_userId: string, data: CreateInput) => {
    const validated = createConversationSchema.parse(data);
    const convex = getConvexClient();

    const conversationId = (await (convex.mutation as any)(
      // @ts-ignore - TypeScript recursion limit with 94+ Convex modules
      api.conversations.create,
      { ...validated },
    )) as any;

    const conversation = (await (convex.query as any)(
      // @ts-ignore - TypeScript recursion limit with 94+ Convex modules
      api.conversations.get,
      { conversationId },
    )) as any;

    return formatEntity(conversation, "conversation", conversation._id);
  },

  getById: async (userId: string, conversationId: string) => {
    const convex = getConvexClient();

    // Uses clerkId for server-side ownership verification
    const conversation = (await (convex.query as any)(
      // @ts-ignore - TypeScript recursion limit with 94+ Convex modules
      api.conversations.getWithClerkVerification,
      { conversationId: conversationId as Id<"conversations">, clerkId: userId },
    )) as any;

    if (!conversation) {
      throw new Error("Conversation not found or access denied");
    }

    return formatEntity(conversation, "conversation", conversation._id);
  },

  // Always verify ownership before mutations
  update: async (userId: string, conversationId: string, data: UpdateInput) => {
    await conversationsDAL.getById(userId, conversationId); // Ownership check
    // ... perform mutation
  },
};
```

**DAL conventions:**
- Always validate input with Zod schemas
- Use `(convex.mutation as any)` + `@ts-ignore` for type recursion workaround
- Always wrap responses with `formatEntity(data, "entityName", id)`
- Verify ownership before mutations (call `getById` first)
- For mutations requiring `ctx.auth`, use `getAuthenticatedConvexClient(sessionToken)`

## REST API Routes (Tier 3)

```typescript
// From apps/web/src/app/api/v1/conversations/route.ts
async function postHandler(req: NextRequest, { userId }: { userId: string }) {
  const startTime = performance.now();
  logger.info({ userId }, "POST /api/v1/conversations");

  const body = await parseBody(req, createSchema);
  const result = await conversationsDAL.create(userId, body);

  const duration = performance.now() - startTime;

  trackAPIPerformance({
    endpoint: "/api/v1/conversations",
    method: "POST",
    duration,
    status: 201,
    userId,
  });

  return NextResponse.json(result, { status: 201 });
}

async function getHandler(req: NextRequest, { userId }: { userId: string }) {
  const limit = Number.parseInt(getQueryParam(req, "limit") || "50", 10);
  const archived = getQueryParam(req, "archived") === "true";

  const conversations = await conversationsDAL.list(userId, limit, archived);

  return NextResponse.json(
    formatEntity({ items: conversations, total: conversations.length }, "list"),
    {
      headers: {
        "Cache-Control": getCacheControl(CachePresets.LIST), // 30s cache
      },
    },
  );
}

export const POST = withErrorHandling(withAuth(postHandler));
export const GET = withErrorHandling(withAuth(getHandler));
export const dynamic = "force-dynamic";
```

**REST conventions:**
- Wrap handlers with `withAuth` (requires authentication) or `withOptionalAuth`
- Wrap with `withErrorHandling` for consistent error responses
- Parse body with `parseBody(req, zodSchema)`
- Always call `trackAPIPerformance` for monitoring
- Use structured logging with `logger.info/warn/error`
- Return envelope-formatted responses via `formatEntity`
- Set `dynamic = "force-dynamic"` to prevent static optimization

## SSE Routes (Tier 2)

For medium-duration operations with real-time progress updates.

```typescript
// From apps/web/src/app/api/v1/conversations/stream/route.ts
async function getHandler(req: NextRequest, { userId }: { userId: string }) {
  const convex = getConvexClient();

  // Create SSE connection
  const { response, send, sendError, close, isClosed } = createSSEResponse();

  try {
    // Send initial snapshot
    const initialData = await convex.query(api.conversations.list, {});
    await send("snapshot", { conversations: initialData });

    // Poll for updates every 5s
    const pollInterval = createPollingLoop(
      async () => {
        if (isClosed()) return null;
        const conversations = await convex.query(api.conversations.list, {});
        return { conversations };
      },
      send,
      5000, // 5s polling
      "update",
    );

    // Heartbeat every 2min (prevents mobile carrier disconnection)
    const heartbeat = createHeartbeatLoop(send, 120_000);

    // Setup cleanup on disconnect
    setupSSECleanup(req.signal, close, [pollInterval, heartbeat]);

    return response;
  } catch (error) {
    await sendError(error instanceof Error ? error : new Error(String(error)));
    await close();
    return new Response("Internal server error", { status: 500 });
  }
}

export const GET = withErrorHandling(withAuth(getHandler));
```

**SSE patterns:**
1. `createSSEResponse()` - Returns `{ response, send, sendError, close, isClosed }`
2. Send initial snapshot with `await send("snapshot", data)`
3. `createPollingLoop(pollFn, send, interval, eventName)` - Poll for updates
4. `createHeartbeatLoop(send, 120_000)` - Keep-alive every 2min
5. `setupSSECleanup(req.signal, close, [intervals])` - Auto-cleanup on disconnect

**Event types:**
- `snapshot` - Initial data payload
- `update` - Incremental updates
- `heartbeat` - Keep-alive ping (2min interval prevents mobile carrier timeout)
- `error` - Error event

## withAuth Middleware

```typescript
// From apps/web/src/lib/api/middleware/auth.ts
export function withAuth(handler: AuthenticatedHandler) {
  return async (req: NextRequest, context: RouteContext) => {
    const { userId, getToken } = await auth();

    if (!userId) {
      return NextResponse.json(formatErrorEntity("Authentication required"), {
        status: 401,
      });
    }

    // Get session token for Convex authentication
    const sessionToken = await getToken({ template: "convex" });
    if (!sessionToken) {
      return NextResponse.json(
        formatErrorEntity("Session token unavailable"),
        { status: 401 },
      );
    }

    return await handler(req, { ...context, userId, sessionToken });
  };
}
```

**Usage:**
- `withAuth(handler)` - Requires authentication, provides `userId` and `sessionToken`
- `withOptionalAuth(handler)` - Provides `userId?: string` if authenticated
- Always use `formatErrorEntity` for error responses
- Session token needed for `getAuthenticatedConvexClient(sessionToken)`

## Tier Selection Criteria

| Criteria | Tier 1 (Convex) | Tier 2 (SSE) | Tier 3 (REST) |
|----------|----------------|--------------|---------------|
| Platform | Web desktop | Mobile | Mobile fallback |
| Latency | <100ms real-time | ~5s updates | 30s cache |
| Duration | Unlimited | 5-30min | <30s |
| Battery | High (WebSocket) | Medium (SSE) | Low (polling) |
| Use cases | Chat messages, live lists | Progress updates, streaming | Standard CRUD |

## Key Files

- `apps/web/src/lib/utils/platform.ts` - Platform detection logic
- `apps/web/src/lib/hooks/queries/` - Hybrid data hooks
- `apps/web/src/lib/api/dal/` - DAL layer (server-only)
- `apps/web/src/app/api/v1/` - REST/SSE routes
- `apps/web/src/lib/api/sse/utils.ts` - SSE utilities
- `apps/web/src/lib/api/middleware/auth.ts` - Auth middleware

## Common Patterns

**Creating new hybrid hook:**
1. Import both React Query and Convex query hooks
2. Call `shouldUseConvex()` for platform detection
3. Conditionally enable queries with `"skip"` or `enabled: false`
4. Return unified interface

**Creating new REST endpoint:**
1. Create route in `apps/web/src/app/api/v1/{resource}/route.ts`
2. Wrap handlers with `withAuth` and `withErrorHandling`
3. Call DAL layer (never call Convex directly from routes)
4. Return `formatEntity` responses
5. Set `dynamic = "force-dynamic"`

**Creating new SSE endpoint:**
1. Create route with `/stream` suffix
2. Use `createSSEResponse()` for connection
3. Send `snapshot` event immediately
4. Setup `createPollingLoop` for updates
5. Setup `createHeartbeatLoop` (2min interval)
6. Call `setupSSECleanup` with intervals

**Adding DAL method:**
1. Create in `apps/web/src/lib/api/dal/{resource}.ts`
2. Add `import "server-only"` at top
3. Validate input with Zod schemas
4. Use `(convex.mutation as any)` + `@ts-ignore` pattern
5. Always `formatEntity` responses
6. Verify ownership before mutations

## Avoid

- Never call Convex directly from client components on mobile (use hooks)
- Never skip ownership verification in DAL mutations
- Never return raw Convex data (always use `formatEntity`)
- Don't forget `dynamic = "force-dynamic"` on API routes
- Don't skip heartbeat in SSE (mobile carriers timeout idle connections)
- Never use SSE for long operations (>30min) - use Convex actions instead
