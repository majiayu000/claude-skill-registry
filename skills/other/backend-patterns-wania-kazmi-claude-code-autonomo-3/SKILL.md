---
name: backend-patterns
description: |
  Backend architecture patterns, API design, database optimization, and server-side best practices.
  Use when building APIs, services, or server-side functionality.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Backend Development Patterns

## API Design Patterns

### RESTful API Structure

```typescript
GET    /api/markets              # List resources
GET    /api/markets/:id          # Get single resource
POST   /api/markets              # Create resource
PUT    /api/markets/:id          # Replace resource
PATCH  /api/markets/:id          # Update resource
DELETE /api/markets/:id          # Delete resource

// Query parameters for filtering
GET /api/markets?status=active&sort=volume&limit=20&offset=0
```

### Repository Pattern

```typescript
interface MarketRepository {
  findAll(filters?: MarketFilters): Promise<Market[]>
  findById(id: string): Promise<Market | null>
  create(data: CreateMarketDto): Promise<Market>
  update(id: string, data: UpdateMarketDto): Promise<Market>
  delete(id: string): Promise<void>
}

class SupabaseMarketRepository implements MarketRepository {
  async findAll(filters?: MarketFilters): Promise<Market[]> {
    let query = supabase.from('markets').select('*')

    if (filters?.status) {
      query = query.eq('status', filters.status)
    }

    const { data, error } = await query
    if (error) throw new Error(error.message)
    return data
  }
}
```

### Service Layer Pattern

```typescript
class MarketService {
  constructor(private marketRepo: MarketRepository) {}

  async searchMarkets(query: string, limit: number = 10): Promise<Market[]> {
    const embedding = await generateEmbedding(query)
    const results = await this.vectorSearch(embedding, limit)
    const markets = await this.marketRepo.findByIds(results.map(r => r.id))
    return markets
  }
}
```

## Database Patterns

### Query Optimization

```typescript
// GOOD: Select only needed columns
const { data } = await supabase
  .from('markets')
  .select('id, name, status, volume')
  .eq('status', 'active')
  .order('volume', { ascending: false })
  .limit(10)

// BAD: Select everything
const { data } = await supabase
  .from('markets')
  .select('*')
```

### N+1 Query Prevention

```typescript
// BAD: N+1 query problem
const markets = await getMarkets()
for (const market of markets) {
  market.creator = await getUser(market.creator_id)  // N queries
}

// GOOD: Batch fetch
const markets = await getMarkets()
const creatorIds = markets.map(m => m.creator_id)
const creators = await getUsers(creatorIds)  // 1 query
const creatorMap = new Map(creators.map(c => [c.id, c]))

markets.forEach(market => {
  market.creator = creatorMap.get(market.creator_id)
})
```

## Caching Strategies

### Redis Caching Layer

```typescript
async function getMarketWithCache(id: string): Promise<Market> {
  const cacheKey = `market:${id}`

  // Try cache
  const cached = await redis.get(cacheKey)
  if (cached) return JSON.parse(cached)

  // Cache miss - fetch from DB
  const market = await db.markets.findUnique({ where: { id } })

  if (!market) throw new Error('Market not found')

  // Update cache (5 minutes)
  await redis.setex(cacheKey, 300, JSON.stringify(market))

  return market
}
```

## Error Handling Patterns

### Centralized Error Handler

```typescript
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string
  ) {
    super(message)
  }
}

export function errorHandler(error: unknown): Response {
  if (error instanceof ApiError) {
    return NextResponse.json({
      success: false,
      error: error.message
    }, { status: error.statusCode })
  }

  console.error('Unexpected error:', error)

  return NextResponse.json({
    success: false,
    error: 'Internal server error'
  }, { status: 500 })
}
```

### Retry with Exponential Backoff

```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  let lastError: Error

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error

      if (i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000  // 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
  }

  throw lastError!
}
```

## Authentication & Authorization

### JWT Token Validation

```typescript
export async function requireAuth(request: Request) {
  const token = request.headers.get('authorization')?.replace('Bearer ', '')

  if (!token) {
    throw new ApiError(401, 'Missing authorization token')
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!)
    return payload
  } catch {
    throw new ApiError(401, 'Invalid token')
  }
}
```

### Role-Based Access Control

```typescript
type Permission = 'read' | 'write' | 'delete' | 'admin'

const rolePermissions: Record<string, Permission[]> = {
  admin: ['read', 'write', 'delete', 'admin'],
  moderator: ['read', 'write', 'delete'],
  user: ['read', 'write']
}

export function hasPermission(user: User, permission: Permission): boolean {
  return rolePermissions[user.role].includes(permission)
}
```

## Rate Limiting

```typescript
class RateLimiter {
  private requests = new Map<string, number[]>()

  async checkLimit(
    identifier: string,
    maxRequests: number,
    windowMs: number
  ): Promise<boolean> {
    const now = Date.now()
    const requests = this.requests.get(identifier) || []

    const recentRequests = requests.filter(time => now - time < windowMs)

    if (recentRequests.length >= maxRequests) {
      return false  // Rate limit exceeded
    }

    recentRequests.push(now)
    this.requests.set(identifier, recentRequests)

    return true
  }
}
```

## Logging

```typescript
interface LogContext {
  userId?: string
  requestId?: string
  [key: string]: unknown
}

class Logger {
  log(level: 'info' | 'warn' | 'error', message: string, context?: LogContext) {
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      level,
      message,
      ...context
    }))
  }

  info(message: string, context?: LogContext) {
    this.log('info', message, context)
  }

  error(message: string, error: Error, context?: LogContext) {
    this.log('error', message, {
      ...context,
      error: error.message,
      stack: error.stack
    })
  }
}
```

## Checklist

- [ ] API follows RESTful conventions
- [ ] Repository pattern for data access
- [ ] Service layer for business logic
- [ ] Proper error handling with error classes
- [ ] Caching for expensive queries
- [ ] Rate limiting on public endpoints
- [ ] Authentication on protected routes
- [ ] Structured logging
- [ ] Input validation with Zod
