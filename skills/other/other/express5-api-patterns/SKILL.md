---
name: express5-api-patterns
description: Express 5 patterns for peek-stash-browser — TypeScript backend serving a React SPA with HLS video proxying, multi-instance Stash server routing, JWT auth via HTTP-only cookies, and SQLite via Prisma. Use when writing or modifying Express route handlers, middleware, proxy controllers, or streaming endpoints in the peek project.
---

# Express 5 API Patterns (peek-stash-browser)

Express 5.x patterns extracted from peek-stash-browser. This project uses Express ^5.1.0 with TypeScript strict mode, Prisma/SQLite, and JWT auth.

## 1. Express 5 Breaking Changes from v4

### Async Error Handling (the big one)
Express 5 automatically catches rejected promises from async route handlers and forwards them to the error handler. No need for `asyncHandler` wrappers or try/catch in every handler.

```typescript
// Express 4 — needed wrapper or manual try/catch
app.get("/api/thing", asyncHandler(async (req, res) => { ... }));

// Express 5 — just throw, it gets caught automatically
app.get("/api/thing", async (req, res) => {
  const data = await db.find(req.params.id); // rejection auto-forwarded
  if (!data) throw new NotFoundError("Not found"); // caught by error middleware
  res.json(data);
});
```

### Path-to-regexp v8 Changes
- **Wildcards must be named**: `/*` becomes `/*splat` (or `/{*splat}` to also match root)
- **Optional params use braces**: `/:file.:ext?` becomes `/:file{.:ext}`
- **No regex in path strings**: `app.get('/[discussion|page]/:slug')` must use array: `app.get(['/discussion/:slug', '/page/:slug'])`
- **Reserved chars must be escaped**: `()[]?+!` need backslash escaping in paths
- **Unmatched optional params are omitted** from `req.params` (not set to `undefined`)
- **Wildcard params are arrays**: `req.params.splat` returns `['foo', 'bar']` for `/foo/bar`

### req.query Is Read-Only
`req.query` is a getter in Express 5 — cannot be reassigned. Default parser changed from "extended" to "simple".

### req.host Includes Port
`req.host` now returns `example.com:8080` instead of just `example.com`.

### req.body Is undefined When Not Parsed
Without body-parsing middleware, `req.body` is `undefined` (was `{}` in v4).

### Removed APIs
- `app.del()` — use `app.delete()`
- `req.param(name)` — use `req.params.id`, `req.body.field`, or `req.query.key` explicitly
- `res.redirect('back')` — use `res.redirect(req.get('Referrer') || '/')`
- `res.send(status)` with a number — use `res.sendStatus(200)` or `res.status(200).send()`
- `express.static.mime` — use the `mime-types` package directly

### Changed Signatures
- `res.redirect(url, status)` arg order reversed: `res.redirect(301, '/new-url')`
- `res.json(obj, status)` removed: use `res.status(201).json(obj)`
- `res.status()` only accepts integers 100-999 (no strings, no values < 100)

### Other Behavioral Changes
- `express.urlencoded` defaults to `extended: false` (was `true`)
- `express.static` defaults to `dotfiles: 'ignore'` (dot-prefixed files return 404)
- `res.clearCookie()` ignores `maxAge` and `expires` options
- `res.vary()` throws when field argument is missing (was silent warning)

## 2. Async Error Handling

Express 5 catches rejected promises automatically. The project uses explicit try/catch only when it needs custom error responses or cleanup.

### Simple Throws vs Explicit Try/Catch
```typescript
// Let Express 5 catch it — for simple handlers
export const getScene = async (req: Request, res: Response) => {
  const scene = await prisma.stashScene.findFirst({ where: { id: req.params.id } });
  if (!scene) throw new NotFoundError("Scene not found");
  res.json(scene);
};

// Explicit catch — when you need custom error shapes or cleanup
export const proxyScenePreview = async (req: Request, res: Response) => {
  if (!req.params.id) return res.status(400).json({ error: "Missing scene ID" });
  try {
    const creds = getInstanceCredentials(scene.stashInstanceId ?? undefined);
    // ... proxy logic with concurrency slot cleanup
  } catch (error) {
    logger.error("Failed to get credentials", { error });
    return res.status(500).json({ error: "Stash configuration missing" });
  }
};
```

### Error Middleware (must have 4 params for Express to recognize it)
```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) return res.status(err.statusCode).json({ error: err.message });
  logger.error("Unhandled error", { error: err.message, stack: err.stack });
  res.status(500).json({ error: "Internal server error" });
});

class AppError extends Error {
  constructor(public message: string, public statusCode: number = 500) { super(message); }
}
class NotFoundError extends AppError { constructor(msg = "Not found") { super(msg, 404); } }
class ValidationError extends AppError { constructor(msg: string) { super(msg, 400); } }
```

## 3. TypeScript Patterns

### Typed Request/Response Helpers (`server/types/api/express.ts`)
```typescript
// Generic typed request — TBody, TParams, TQuery
interface TypedRequest<
  TBody = unknown,
  TParams extends Record<string, string> = Record<string, string>,
  TQuery extends Record<string, string | string[] | undefined> = Record<string, string | undefined>
> extends Request { body: TBody; params: TParams; query: TQuery; user?: RequestUser; }

// Authenticated variant — user guaranteed to exist (post-auth middleware)
interface TypedAuthRequest<TBody, TParams, TQuery> extends TypedRequest<TBody, TParams, TQuery> {
  user: RequestUser;
}
type TypedResponse<T> = Response<T>;
```

### Using Typed Handlers
```typescript
interface UpdateRatingRequest { rating?: number | null; favorite?: boolean; instanceId?: string; }
interface UpdateSceneRatingParams { sceneId: string; }

export async function updateSceneRating(
  req: TypedAuthRequest<UpdateRatingRequest, UpdateSceneRatingParams>,
  res: TypedResponse<UpdateRatingResponse | ApiErrorResponse>
) {
  const userId = req.user.id;          // guaranteed by TypedAuthRequest
  const { sceneId } = req.params;      // typed as { sceneId: string }
  const { rating, favorite } = req.body;
}
```

### Type Bridge for Router Registration
Express's `RequestHandler` doesn't match custom typed handlers. Bridge with cast:
```typescript
// server/utils/routeHelpers.ts
export function authenticated(handler: (...args: any[]) => any): RequestHandler {
  return handler as unknown as RequestHandler;
}
// In route files:
router.put("/scene/:sceneId", authenticated(updateSceneRating));
```

### AuthenticatedRequest for Middleware
```typescript
interface AuthenticatedRequest extends Request { user: RequestUser; }
// In middleware: (req as AuthenticatedRequest).user = user;
// In controllers: use TypedAuthRequest instead of manual casting
```

## 4. Proxy Middleware

Based on `server/controllers/proxy.ts`. All media requests to upstream Stash servers go through Peek's proxy to hide API keys from clients.

### Connection Pooling
```typescript
const httpAgent = new http.Agent({
  keepAlive: true,
  maxSockets: 6,
  keepAliveMsecs: 30000,
});
const httpsAgent = new https.Agent({
  keepAlive: true,
  maxSockets: 6,
  keepAliveMsecs: 30000,
});
```

### Concurrency Limiting
Queue-based limiter prevents overwhelming upstream servers:
```typescript
const MAX_CONCURRENT_REQUESTS = 6;
let activeRequests = 0;
const requestQueue: Array<() => void> = [];

function acquireConcurrencySlot(): Promise<void> {
  return new Promise((resolve) => {
    if (activeRequests < MAX_CONCURRENT_REQUESTS) {
      activeRequests++;
      resolve();
    } else {
      requestQueue.push(() => { activeRequests++; resolve(); });
    }
  });
}

function releaseConcurrencySlot(): void {
  activeRequests--;
  const next = requestQueue.shift();
  if (next) next();
}
```

### Shared Proxy Helper with Cleanup
Key patterns: double-release guard, client disconnect cleanup, timeout handling.
```typescript
function proxyHttpRequest({ fullUrl, res, label, defaultCacheControl, timeoutMs }: ProxyOptions): void {
  let slotReleased = false;
  const releaseOnce = () => {
    if (!slotReleased) { slotReleased = true; releaseConcurrencySlot(); }
  };

  const proxyReq = httpModule.get(fullUrl, { agent }, (proxyRes) => {
    // Forward select headers, set status, pipe response
    if (proxyRes.headers["content-type"]) res.setHeader("Content-Type", proxyRes.headers["content-type"]);
    res.status(proxyRes.statusCode || 200);
    proxyRes.pipe(res);
    proxyRes.on("end", releaseOnce);
    proxyRes.on("error", releaseOnce);
  });

  // Destroy upstream request when client disconnects
  res.on("close", () => {
    if (!proxyReq.destroyed) proxyReq.destroy();
    releaseOnce();
  });

  proxyReq.on("error", (error) => {
    releaseOnce();
    if ((error as NodeJS.ErrnoException).code === "ECONNRESET") return; // expected on client disconnect
    if (!res.headersSent) res.status(500).json({ error: "Proxy request failed" });
  });

  proxyReq.setTimeout(timeoutMs, () => {
    releaseOnce();
    proxyReq.destroy();
    if (!res.headersSent) res.status(504).json({ error: "Proxy request timeout" });
  });
}
```

### API Key Injection
API keys are appended as query params to upstream URLs, never exposed to the client:
```typescript
const fullUrl = `${stashUrl}/scene/${id}/preview?apikey=${apiKey}`;
// Log with key redacted
logger.debug("Proxying", { url: fullUrl.replace(apiKey, "***") });
```

## 5. HLS Video Streaming

Based on `server/controllers/video.ts`. Peek proxies Stash's HLS streams and rewrites playlist URLs.

### Stream Proxy with Fetch + AbortController
```typescript
export const proxyStashStream = async (req: Request, res: Response) => {
  const { sceneId, streamPath, subPath } = req.params;
  const instanceId = req.query.instanceId as string | undefined;
  const fullStreamPath = subPath ? `${streamPath}/${subPath}` : streamPath;

  // Abort upstream fetch when client disconnects
  const abortController = new AbortController();
  res.on('close', () => abortController.abort());

  const headers: Record<string, string> = { 'ApiKey': apiKey };
  if (req.headers.range) headers['Range'] = req.headers.range;

  const response = await fetch(stashUrl, { headers, signal: abortController.signal });
  // ...
};
```

### HLS Playlist Rewriting
Strip API keys from segment URLs and route through Peek's proxy:
```typescript
function rewriteHlsPlaylist(content: string, sceneId: string, stashBaseUrl: string, instanceId?: string): string {
  return content.split('\n').map(line => {
    if (!line.trim() || line.startsWith('#')) return line; // skip tags and empty lines
    // Parse URL (absolute, absolute path, or relative)
    // Strip apikey param, add instanceId for routing
    queryParams.delete('apikey');
    if (instanceId) queryParams.set('instanceId', instanceId);
    return `/api/scene/${sceneId}/proxy-stream/${streamPath}${queryString}`;
  }).join('\n');
}
```

### HLS Content-Type Detection
```typescript
const isHlsPlaylist = fullStreamPath.endsWith('.m3u8') ||
                      contentType.includes('mpegurl') ||
                      contentType.includes('x-mpegURL');
```

### Stream Piping with Backpressure (`server/utils/streamProxy.ts`)
Uses `Readable.fromWeb()` + `stream.pipeline()` for proper backpressure. Silently swallows `AbortError` and `ERR_STREAM_PREMATURE_CLOSE` since they are expected when client disconnects (seek, refresh, navigate away).
```typescript
const nodeStream = Readable.fromWeb(fetchResponse.body as import("stream/web").ReadableStream);
try {
  await pipeline(nodeStream, res);
} catch (err: unknown) {
  if (err instanceof Error && (err.name === "AbortError" ||
      (err as NodeJS.ErrnoException).code === "ERR_STREAM_PREMATURE_CLOSE")) return;
  logger.error(`${label} Stream pipeline error`, { error: (err as Error).message });
}
```

### Route Registration for Multi-Segment Paths
Two routes handle both single-segment and nested HLS paths:
```typescript
router.get("/scene/:sceneId/proxy-stream/:streamPath/:subPath", proxyStashStream);
router.get("/scene/:sceneId/proxy-stream/:streamPath", proxyStashStream);
```

## 6. Multi-Instance Routing

Peek routes requests to different Stash servers based on `instanceId`.

### Instance Credential Resolution
```typescript
function getInstanceCredentials(instanceId?: string): { baseUrl: string; apiKey: string } {
  if (instanceId && instanceId !== "default") {
    const instance = stashInstanceManager.get(instanceId);
    if (!instance) throw new Error(`Stash instance not found: ${instanceId}`);
    return {
      baseUrl: stashInstanceManager.getBaseUrl(instanceId),
      apiKey: stashInstanceManager.getApiKey(instanceId),
    };
  }
  return {
    baseUrl: stashInstanceManager.getBaseUrl(),
    apiKey: stashInstanceManager.getApiKey(),
  };
}
```

### Per-Entity Instance Lookup
Entities store their `stashInstanceId` in the database. Controllers look it up before proxying:
```typescript
const scene = await prisma.stashScene.findFirst({
  where: { id, deletedAt: null },
  select: { stashInstanceId: true },
});
const creds = getInstanceCredentials(scene.stashInstanceId ?? undefined);
```

### instanceId in Query Params
For stream proxying, `instanceId` travels as a query param and is stripped before forwarding:
```typescript
const instanceId = req.query.instanceId as string | undefined;
const urlParams = new URLSearchParams(req.url.split('?')[1] || '');
urlParams.delete('instanceId'); // don't send to Stash
```

## 7. Authentication Middleware

Based on `server/middleware/auth.ts`. JWT tokens stored in HTTP-only cookies.

### Token Cookie Configuration
```typescript
res.cookie("token", token, {
  httpOnly: true,
  secure: process.env.SECURE_COOKIES === "true",
  sameSite: "strict",
  maxAge: TOKEN_EXPIRY_HOURS * 60 * 60 * 1000, // 2 hours
});
```

### Dual Auth: Cookie + Bearer Token
```typescript
const token = req.cookies?.token || req.header("Authorization")?.replace("Bearer ", "");
```

### Silent Token Refresh
Tokens older than 1 hour are automatically refreshed for cookie-based auth (not Bearer tokens):
```typescript
if (req.cookies?.token && decoded.iat) {
  const tokenAgeHours = (Date.now() / 1000 - decoded.iat) / 3600;
  if (tokenAgeHours > TOKEN_REFRESH_THRESHOLD_HOURS) {
    const newToken = generateToken({ id: user.id, username: user.username, role: user.role });
    setTokenCookie(res, newToken);
  }
}
```

### Reverse Proxy Auth Header Support
Check for a configurable header before falling back to JWT:
```typescript
export const authenticate = async (req: Request, res: Response, next: NextFunction) => {
  const proxyAuthHeader = process.env.PROXY_AUTH_HEADER;
  if (proxyAuthHeader) {
    const username = req.header(proxyAuthHeader);
    if (username) return await authenticateUser(username, req, res, next);
  }
  return await authenticateToken(req, res, next);
};
```

### Role-Based Middleware
```typescript
export const requireAdmin = (req: Request, res: Response, next: NextFunction) => {
  const authReq = req as AuthenticatedRequest;
  if (!authReq.user || authReq.user.role !== "ADMIN") {
    return res.status(403).json({ error: "Admin access required." });
  }
  next();
};
```

### Middleware Chaining on Routes
```typescript
// Admin-only endpoint: authenticate -> requireAdmin -> handler
app.get("/api/stats", authenticate, requireAdmin, statsController.getStats);

// User endpoint with cache guard: authenticate -> requireCacheReady -> handler
app.get("/api/scenes/:id/clips", authenticate, requireCacheReady, getClipsForScene);

// Router-level auth applied to all routes in the router
const router = express.Router();
router.use(authenticate);
router.put("/scene/:sceneId", authenticated(updateSceneRating));
```

## 8. HTTP Caching

### Cache-Control Headers by Content Type
```typescript
// Immutable static assets (images, sprites) — cache forever
res.setHeader("Cache-Control", "public, max-age=31536000, immutable");

// Stable media (scene previews) — cache 24 hours
res.setHeader("Cache-Control", "public, max-age=86400");

// HLS playlists — never cache (segments change between requests)
res.setHeader("Cache-Control", "no-cache");

// Dynamic API responses — default no cache header (let browser decide)
```

### Forwarding Upstream Cache Headers
When proxying, prefer upstream's Cache-Control but provide a default:
```typescript
if (proxyRes.headers["cache-control"]) {
  res.setHeader("Cache-Control", proxyRes.headers["cache-control"]);
} else {
  res.setHeader("Cache-Control", defaultCacheControl);
}
```

### Headers Forwarded for Streaming
```typescript
const headersToForward = [
  'content-type', 'content-length', 'accept-ranges',
  'content-range', 'cache-control', 'last-modified', 'etag',
];
```

## 9. Response Patterns

### Consistent JSON Error Responses
All API errors use `{ error: string }` shape, defined in `types/api/common.ts`:
```typescript
interface ApiErrorResponse {
  error: string;
  message?: string;
  details?: string;
}

// Usage
res.status(400).json({ error: "Missing scene ID" });
res.status(404).json({ error: "Scene not found" });
res.status(500).json({ error: "Internal server error" });
res.status(503).json({ error: "Server is initializing", message: "Cache is still loading.", ready: false });
```

### Success Responses with Entity Data
```typescript
// Direct entity return
res.json({ success: true, rating: sceneRating });

// Health check pattern
res.json({ status: "healthy", timestamp: new Date().toISOString(), version: "3.3.5" });
```

### Streaming Responses
Two patterns for streaming: Node.js http module pipe and fetch-to-Express pipeline.

**http module pipe (proxy.ts):**
```typescript
proxyRes.pipe(res);
```

**fetch + Readable.fromWeb (video.ts, streamProxy.ts):**
```typescript
const nodeStream = Readable.fromWeb(fetchResponse.body as ReadableStream);
await pipeline(nodeStream, res);
```

### Guard Against Double-Send
Always check `res.headersSent` before sending error responses in catch blocks or event handlers:
```typescript
if (!res.headersSent) {
  res.status(500).json({ error: "Internal server error" });
}
```

## 10. Middleware Organization

### App-Level Middleware Order (`server/initializers/api.ts`)
1. `app.set("trust proxy", ...)` -- must be first for rate limiting / IP detection
2. `cors({ credentials: true, origin: [...] })` -- CORS
3. `express.json()` -- body parsing
4. `cookieParser()` -- needed for JWT extraction from cookies
5. Public routes (no auth) -- health, version, media proxy endpoints
6. Auth routes (public) -- login/register via `app.use("/api/auth", authRoutes)`
7. Protected routes -- each router applies `authenticate` internally
8. Video/streaming routes (last) -- catch-all patterns via `app.use("/api", videoRoutes)`

### Router-Level Auth Pattern
Apply auth to all routes in a router, then use `authenticated()` wrapper for type safety:
```typescript
const router = express.Router();
router.use(authenticate);
router.put("/scene/:sceneId", authenticated(updateSceneRating));
router.put("/performer/:performerId", authenticated(updatePerformerRating));
export default router;
```

### Mixed Auth Routers
Some routers have both public and protected endpoints:
```typescript
// Setup routes — some public for initial setup, some admin-only
router.get("/status", getSetupStatus);                      // public
router.post("/complete", authenticate, requireAdmin, completeSetup); // admin
```

### Middleware Factories
```typescript
// Rate limiter with config
import rateLimit from "express-rate-limit";
const authLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 10 });
router.post("/login", authLimiter, loginHandler);
```

### Conditional Middleware
```typescript
// Trust proxy only if configured
const trustProxy = process.env.TRUST_PROXY;
if (trustProxy) {
  if (trustProxy === "true") app.set("trust proxy", true);
  else if (/^\d+$/.test(trustProxy)) app.set("trust proxy", parseInt(trustProxy, 10));
  else app.set("trust proxy", trustProxy);
}
```

### Service Readiness Guard
Block API access until cache is warm:
```typescript
export const requireCacheReady = async (_req: Request, res: Response, next: NextFunction) => {
  const isReady = await stashEntityService.isReady();
  if (!isReady) {
    return res.status(503).json({ error: "Server is initializing", ready: false });
  }
  next();
};
```
