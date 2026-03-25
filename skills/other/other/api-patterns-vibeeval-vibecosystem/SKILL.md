---
name: api-patterns
description: API design, versioning, testing, schema validation, and contract testing patterns for REST and GraphQL APIs.
---

# API Patterns

REST and GraphQL API design patterns for consistent, versioned, and well-tested interfaces.

## API Versioning

### URL-Based Versioning

```typescript
// routes/v1/markets.ts
// routes/v2/markets.ts
// URL: /api/v1/markets, /api/v2/markets

// Express router setup
import { Router } from 'express'

const v1Router = Router()
const v2Router = Router()

app.use('/api/v1', v1Router)
app.use('/api/v2', v2Router)

// Deprecation header middleware
function deprecationWarning(version: string, sunsetDate: string) {
  return (_req: Request, res: Response, next: NextFunction) => {
    res.setHeader('Deprecation', 'true')
    res.setHeader('Sunset', sunsetDate)
    res.setHeader('Link', `</api/v${parseInt(version) + 1}>; rel="successor-version"`)
    next()
  }
}

v1Router.use(deprecationWarning('1', 'Sat, 01 Jan 2027 00:00:00 GMT'))
```

### Header-Based Versioning

```typescript
// Accept: application/vnd.api+json;version=2
function versionMiddleware(req: Request, res: Response, next: NextFunction) {
  const accept = req.headers['accept'] || ''
  const match = accept.match(/version=(\d+)/)
  req.apiVersion = match ? parseInt(match[1]) : 1
  next()
}
```

## Schema Validation with Zod

### Request + Response Validation

```typescript
import { z } from 'zod'

// Request schema
const CreateMarketSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().max(2000).optional(),
  category: z.enum(['sports', 'politics', 'crypto', 'tech']),
  closeAt: z.string().datetime(),
  initialLiquidity: z.number().positive().max(1_000_000)
})

// Response schema - strip internal fields
const MarketResponseSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  category: z.string(),
  status: z.enum(['open', 'closed', 'resolved']),
  volume: z.number(),
  createdAt: z.string().datetime()
})

type CreateMarketDto = z.infer<typeof CreateMarketSchema>
type MarketResponse = z.infer<typeof MarketResponseSchema>

// Validation middleware
function validate<T>(schema: z.ZodSchema<T>) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body)
    if (!result.success) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        code: 'VALIDATION_ERROR',
        details: result.error.flatten()
      })
    }
    req.validated = result.data
    next()
  }
}

// Usage
router.post('/markets', validate(CreateMarketSchema), async (req, res) => {
  const dto = req.validated as CreateMarketDto
  const market = await marketService.create(dto)
  const response = MarketResponseSchema.parse(market)
  res.status(201).json({ success: true, data: response })
})
```

## Standardized Error Responses

```typescript
// Always: { success, error, code, details? }
interface ApiError {
  success: false
  error: string
  code: string
  details?: unknown
  requestId?: string
}

interface ApiSuccess<T> {
  success: true
  data: T
  meta?: { total?: number; page?: number; limit?: number }
}

const ERROR_CODES = {
  VALIDATION_ERROR: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  RATE_LIMITED: 429,
  INTERNAL: 500
} as const

function apiError(
  res: Response,
  code: keyof typeof ERROR_CODES,
  message: string,
  details?: unknown
): Response {
  return res.status(ERROR_CODES[code]).json({
    success: false,
    error: message,
    code,
    details,
    requestId: res.locals.requestId
  } satisfies ApiError)
}
```

## Pagination Patterns

### Cursor-Based Pagination (Recommended for large datasets)

```typescript
interface CursorPage<T> {
  items: T[]
  nextCursor: string | null
  prevCursor: string | null
  hasMore: boolean
}

async function paginateWithCursor<T extends { id: string; createdAt: Date }>(
  query: (cursor: string | null, limit: number) => Promise<T[]>,
  cursor: string | null,
  limit = 20
): Promise<CursorPage<T>> {
  // Fetch one extra to detect hasMore
  const items = await query(cursor, limit + 1)
  const hasMore = items.length > limit
  const page = hasMore ? items.slice(0, limit) : items

  return {
    items: page,
    nextCursor: hasMore ? Buffer.from(page[page.length - 1].id).toString('base64') : null,
    prevCursor: cursor,
    hasMore
  }
}

// GET /api/markets?cursor=<base64>&limit=20
router.get('/markets', async (req, res) => {
  const cursor = req.query.cursor as string | null
  const limit = Math.min(parseInt(req.query.limit as string) || 20, 100)
  const decoded = cursor ? Buffer.from(cursor, 'base64').toString() : null

  const page = await paginateWithCursor(
    (c, l) => db.market.findMany({
      take: l,
      skip: c ? 1 : 0,
      cursor: c ? { id: c } : undefined,
      orderBy: { createdAt: 'desc' }
    }),
    decoded,
    limit
  )

  res.json({ success: true, ...page })
})
```

### Offset Pagination (Simple use cases)

```typescript
interface OffsetPage<T> {
  items: T[]
  total: number
  page: number
  limit: number
  totalPages: number
}

// GET /api/markets?page=2&limit=20
```

## Rate Limiting

### Token Bucket with Redis

```typescript
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL!)

async function tokenBucket(
  key: string,
  capacity: number,
  refillRate: number   // tokens per second
): Promise<{ allowed: boolean; remaining: number; resetIn: number }> {
  const now = Date.now()
  const bucketKey = `ratelimit:${key}`

  const script = `
    local key = KEYS[1]
    local capacity = tonumber(ARGV[1])
    local refill_rate = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])

    local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
    local tokens = tonumber(bucket[1]) or capacity
    local last_refill = tonumber(bucket[2]) or now

    local elapsed = (now - last_refill) / 1000
    tokens = math.min(capacity, tokens + elapsed * refill_rate)

    if tokens >= 1 then
      tokens = tokens - 1
      redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
      redis.call('EXPIRE', key, math.ceil(capacity / refill_rate) + 1)
      return {1, math.floor(tokens)}
    else
      return {0, 0}
    end
  `

  const [allowed, remaining] = await redis.eval(
    script, 1, bucketKey, capacity, refillRate, now
  ) as [number, number]

  return {
    allowed: allowed === 1,
    remaining,
    resetIn: allowed ? 0 : Math.ceil(1 / refillRate)
  }
}

function rateLimitMiddleware(capacity: number, refillRate: number) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const key = req.user?.id || req.ip || 'anonymous'
    const result = await tokenBucket(key, capacity, refillRate)

    res.setHeader('X-RateLimit-Limit', capacity)
    res.setHeader('X-RateLimit-Remaining', result.remaining)

    if (!result.allowed) {
      res.setHeader('Retry-After', result.resetIn)
      return apiError(res, 'RATE_LIMITED', 'Too many requests')
    }
    next()
  }
}
```

## API Endpoint Testing

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import supertest from 'supertest'
import { app } from '../app'
import { db } from '../db'

const request = supertest(app)

describe('POST /api/v1/markets', () => {
  let authToken: string

  beforeAll(async () => {
    authToken = await getTestToken()
  })

  it('creates a market with valid payload', async () => {
    const payload = {
      name: 'Will BTC reach 100k?',
      category: 'crypto',
      closeAt: new Date(Date.now() + 86400000).toISOString(),
      initialLiquidity: 1000
    }

    const res = await request
      .post('/api/v1/markets')
      .set('Authorization', `Bearer ${authToken}`)
      .send(payload)
      .expect(201)

    expect(res.body.success).toBe(true)
    expect(res.body.data).toMatchObject({
      id: expect.any(String),
      name: payload.name,
      status: 'open'
    })
  })

  it('rejects invalid payload with 400', async () => {
    const res = await request
      .post('/api/v1/markets')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ name: '' })   // invalid
      .expect(400)

    expect(res.body.success).toBe(false)
    expect(res.body.code).toBe('VALIDATION_ERROR')
  })

  it('returns 401 without auth token', async () => {
    const res = await request.post('/api/v1/markets').send({}).expect(401)
    expect(res.body.code).toBe('UNAUTHORIZED')
  })
})
```

## Breaking Change Detection Checklist

```
Before releasing a new API version, verify:

BREAKING changes (require version bump):
  [ ] Removed a field from response
  [ ] Changed field type (string → number)
  [ ] Renamed a field
  [ ] Changed HTTP method
  [ ] Removed an endpoint
  [ ] Changed required → optional (ok) vs optional → required (breaking)
  [ ] Changed error codes/format

NON-BREAKING changes (safe to ship):
  [ ] Added new optional fields to response
  [ ] Added new optional query parameters
  [ ] Added new endpoints
  [ ] Added new enum values (check client handling)
  [ ] Relaxed validation rules
```

## OpenAPI Spec Generation

```typescript
// Use zod-to-openapi or tsoa
import { extendZodWithOpenApi } from 'zod-to-openapi'
import { z } from 'zod'

extendZodWithOpenApi(z)

const MarketSchema = z.object({
  id: z.string().uuid().openapi({ example: 'abc-123' }),
  name: z.string().openapi({ example: 'Will BTC hit 100k?' }),
  status: z.enum(['open', 'closed', 'resolved'])
}).openapi('Market')

// Auto-generate spec at /api/docs.json
```

## Plan-Based Authorization

### Tier-Aware Middleware

```typescript
enum PlanTier {
  FREE = 'free',
  PRO = 'pro',
  ENTERPRISE = 'enterprise'
}

interface PlanLimits {
  tier: PlanTier
  rateLimit: number          // requests per minute
  maxItems: number           // max resources
  features: Set<string>      // enabled features
}

const PLAN_LIMITS: Record<PlanTier, PlanLimits> = {
  [PlanTier.FREE]:       { tier: PlanTier.FREE, rateLimit: 60, maxItems: 100, features: new Set(['read']) },
  [PlanTier.PRO]:        { tier: PlanTier.PRO, rateLimit: 600, maxItems: 10_000, features: new Set(['read', 'write', 'export']) },
  [PlanTier.ENTERPRISE]: { tier: PlanTier.ENTERPRISE, rateLimit: 6000, maxItems: Infinity, features: new Set(['read', 'write', 'export', 'audit', 'sso']) },
}

function requireFeature(feature: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const plan = PLAN_LIMITS[req.user.planTier as PlanTier]
    if (!plan.features.has(feature)) {
      return apiError(res, 'FORBIDDEN', `Feature "${feature}" requires ${PlanTier.PRO} plan or higher`)
    }
    next()
  }
}

function requireQuota(countFn: (userId: string) => Promise<number>) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const plan = PLAN_LIMITS[req.user.planTier as PlanTier]
    const current = await countFn(req.user.id)
    if (current >= plan.maxItems) {
      return apiError(res, 'FORBIDDEN', `Plan limit reached (${plan.maxItems} items). Upgrade to increase.`)
    }
    next()
  }
}

// Usage
router.post('/exports', requireFeature('export'), async (req, res) => { /* ... */ })
router.post('/projects', requireQuota(countUserProjects), async (req, res) => { /* ... */ })
```

## Serverless Rate Limiting

### Sliding Window without Redis

```typescript
// In-memory sliding window — single-instance only
// WARNING: Resets on cold start (serverless). For production multi-instance,
// use Redis/Upstash. Add MAX_ENTRIES cap to prevent memory exhaustion from IP flooding.
const windows = new Map<string, number[]>()

function slidingWindowRateLimit(
  key: string,
  maxRequests: number,
  windowMs: number
): { allowed: boolean; remaining: number; retryAfter: number } {
  const now = Date.now()
  const windowStart = now - windowMs

  // Get or create timestamps array
  const timestamps = windows.get(key) ?? []
  const valid = timestamps.filter(t => t > windowStart)

  if (valid.length >= maxRequests) {
    const oldestInWindow = valid[0]
    const retryAfter = Math.ceil((oldestInWindow + windowMs - now) / 1000)
    return { allowed: false, remaining: 0, retryAfter }
  }

  valid.push(now)
  windows.set(key, valid)
  return { allowed: true, remaining: maxRequests - valid.length, retryAfter: 0 }
}

// Cleanup stale entries periodically
setInterval(() => {
  const cutoff = Date.now() - 60_000
  for (const [key, timestamps] of windows) {
    const valid = timestamps.filter(t => t > cutoff)
    if (valid.length === 0) windows.delete(key)
    else windows.set(key, valid)
  }
}, 60_000)
```

## API Key Authentication

```typescript
import { randomBytes, createHash, timingSafeEqual } from 'crypto'

// SECURITY: For in-memory secret comparison, always use timingSafeEqual
// DB lookups by hash are safe (constant-time at DB level)

// Generate: give raw key to user, store hash
function generateApiKey(prefix: string): { raw: string; hash: string } {
  const raw = `${prefix}_${randomBytes(24).toString('base64url')}`
  const hash = createHash('sha256').update(raw).digest('hex')
  return { raw, hash }
}

// Verify: hash incoming key, compare with stored hash
async function verifyApiKey(rawKey: string): Promise<ApiKeyRecord | null> {
  const hash = createHash('sha256').update(rawKey).digest('hex')
  return db.apiKey.findFirst({
    where: { hash, revokedAt: null, expiresAt: { gt: new Date() } }
  })
}

// Middleware
async function apiKeyAuth(req: Request, res: Response, next: NextFunction) {
  const key = req.headers['x-api-key'] as string
  if (!key) return apiError(res, 'UNAUTHORIZED', 'API key required')

  const record = await verifyApiKey(key)
  if (!record) return apiError(res, 'UNAUTHORIZED', 'Invalid or expired API key')

  // Scope check
  if (!record.scopes.includes(req.method.toLowerCase())) {
    return apiError(res, 'FORBIDDEN', 'API key lacks required scope')
  }

  req.user = { id: record.ownerId, keyId: record.id }
  next()
}
```

## Usage Metering and Quota Management

```typescript
interface UsageRecord {
  tenantId: string
  metric: string      // 'api_calls' | 'storage_bytes' | 'ai_tokens'
  value: number
  period: string      // '2026-03' (monthly bucket)
}

async function trackUsage(tenantId: string, metric: string, increment: number): Promise<void> {
  const period = new Date().toISOString().slice(0, 7) // YYYY-MM
  await db.usage.upsert({
    where: { tenantId_metric_period: { tenantId, metric, period } },
    update: { value: { increment } },
    create: { tenantId, metric, period, value: increment }
  })
}

async function checkQuota(tenantId: string, metric: string, limit: number): Promise<boolean> {
  const period = new Date().toISOString().slice(0, 7)
  const usage = await db.usage.findUnique({
    where: { tenantId_metric_period: { tenantId, metric, period } }
  })
  return (usage?.value ?? 0) < limit
}

// Middleware
function meteringMiddleware(metric: string, increment = 1) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const plan = PLAN_LIMITS[req.user.planTier as PlanTier]
    const withinQuota = await checkQuota(req.user.tenantId, metric, plan.rateLimit * 60 * 24)
    if (!withinQuota) {
      return apiError(res, 'RATE_LIMITED', `Monthly ${metric} quota exceeded. Upgrade plan.`)
    }
    await trackUsage(req.user.tenantId, metric, increment)
    next()
  }
}
```

**Remember**: Consistent versioning and validation contracts make APIs maintainable across client teams and breaking-change deployments.
