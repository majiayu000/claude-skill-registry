---
name: Performance Optimizer
description: Optimize application performance and scalability. Use when investigating slow applications, scaling bottlenecks, or improving response times. Covers profiling, caching, database optimization, and frontend performance.
version: 1.0.0
---

# Performance Optimizer

Make applications fast, scalable, and cost-efficient.

## Core Principle

**Measure first, optimize second.** Don't guess at bottlenecks—profile, measure, then fix the slowest parts.

## Performance Budget

### Web Vitals (Target Metrics)

```yaml
Core Web Vitals:
  Largest Contentful Paint (LCP): < 2.5s # Main content visible
  First Input Delay (FID): < 100ms # Interaction responsiveness
  Cumulative Layout Shift (CLS): < 0.1 # Visual stability

Additional Metrics:
  First Contentful Paint (FCP): < 1.8s # First content rendered
  Time to Interactive (TTI): < 3.8s # Fully interactive
  Total Blocking Time (TBT): < 200ms # Main thread blocked
  Speed Index: < 3.4s # Visual progress

Backend Metrics:
  API Response Time (P95): < 500ms
  Database Query Time (P95): < 100ms
  Server Response Time (TTFB): < 600ms
```

---

## Phase 1: Profiling & Measurement

**Goal**: Identify actual bottlenecks, not perceived ones

### Frontend Profiling

**Chrome DevTools**:

```javascript
// 1. Performance tab → Record → Reload page
// 2. Analyze:
//    - Main thread activity
//    - Network waterfall
//    - JavaScript execution time
//    - Rendering time

// 3. Lighthouse audit
// Run: chrome://lighthouse or `npm i -g lighthouse`
lighthouse https://yoursite.com --view
```

**React DevTools Profiler**:

```javascript
// Wrap component to profile
import { Profiler } from 'react'

function onRenderCallback(id, phase, actualDuration) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`)
}

;<Profiler id="ExpensiveComponent" onRender={onRenderCallback}>
  <ExpensiveComponent />
</Profiler>
```

### Backend Profiling

**Node.js Profiling**:

```bash
# Generate CPU profile
node --prof app.js

# Process profile
node --prof-process isolate-0x*.log > processed.txt

# Flame graphs (better visualization)
npm i -g 0x
0x app.js
```

**Python Profiling**:

```python
import cProfile
import pstats

# Profile function
cProfile.run('slow_function()', 'output.prof')

# Analyze
p = pstats.Stats('output.prof')
p.sort_stats('cumulative').print_stats(20)
```

### Database Profiling

**PostgreSQL**:

```sql
-- Enable query logging
ALTER DATABASE yourdb SET log_min_duration_statement = 100; -- Log queries >100ms

-- Analyze query
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users WHERE email = 'test@example.com';

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

**MongoDB**:

```javascript
// Enable profiling
db.setProfilingLevel(1, { slowms: 100 })

// View slow queries
db.system.profile.find({ millis: { $gt: 100 } }).sort({ ts: -1 })

// Explain query
db.collection.find({ email: 'test@example.com' }).explain('executionStats')
```

---

## Phase 2: Database Optimization

### Add Strategic Indexes

```sql
-- Before: Table scan (slow)
SELECT * FROM users WHERE email = 'user@example.com';
-- Execution time: 2000ms on 1M rows

-- After: Index scan (fast)
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';
-- Execution time: 5ms

-- Composite index for multi-column queries
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at DESC);
SELECT * FROM posts WHERE user_id = 123 ORDER BY created_at DESC;

-- Partial index for filtered queries
CREATE INDEX idx_active_users ON users(created_at) WHERE is_active = true;
```

### Eliminate N+1 Queries

```typescript
// ❌ Bad: N+1 query problem (101 database queries)
const users = await User.findAll() // 1 query
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } }) // N queries
}

// ✅ Good: Eager loading (2 queries)
const users = await User.findAll({
  include: [{ model: Post }]
})

// ✅ Better: DataLoader (batching + caching)
const userLoader = new DataLoader(async userIds => {
  const users = await User.findAll({ where: { id: userIds } })
  return userIds.map(id => users.find(u => u.id === id))
})
```

### Query Optimization

```sql
-- Avoid SELECT *
-- ❌ Bad
SELECT * FROM users WHERE id = 1;

-- ✅ Good
SELECT id, name, email FROM users WHERE id = 1;

-- Use LIMIT
-- ❌ Bad
SELECT * FROM posts ORDER BY created_at DESC;

-- ✅ Good
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20;

-- Avoid functions in WHERE clause
-- ❌ Bad (can't use index)
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- ✅ Good (can use index)
SELECT * FROM users WHERE email = 'user@example.com';
-- Store email as lowercase, or use generated column + index
```

### Connection Pooling

```typescript
// PostgreSQL connection pool
import { Pool } from 'pg'

const pool = new Pool({
  max: 20, // Maximum connections
  min: 5, // Minimum connections
  idleTimeoutMillis: 30000, // Close idle connections after 30s
  connectionTimeoutMillis: 2000 // Error if can't connect in 2s
})

// Always release connections
const client = await pool.connect()
try {
  const result = await client.query('SELECT * FROM users')
  return result.rows
} finally {
  client.release()
}
```

---

## Phase 3: Caching Strategy

### Multi-Layer Caching

```
Browser Cache (HTTP headers)
  ↓
CDN Cache (Cloudflare, CloudFront)
  ↓
Application Cache (Redis, Memcached)
  ↓
Database Query Cache
  ↓
Database
```

### Redis Caching

```typescript
import Redis from 'ioredis'

const redis = new Redis({
  maxRetriesPerRequest: 3,
  enableReadyCheck: true
})

async function getUser(id: string): Promise<User> {
  const cacheKey = `user:${id}`

  // 1. Check cache
  const cached = await redis.get(cacheKey)
  if (cached) {
    return JSON.parse(cached)
  }

  // 2. Cache miss - fetch from database
  const user = await db.users.findById(id)

  // 3. Store in cache (expire in 1 hour)
  await redis.setex(cacheKey, 3600, JSON.stringify(user))

  return user
}

// Cache invalidation
async function updateUser(id: string, data: Partial<User>) {
  await db.users.update(id, data)
  await redis.del(`user:${id}`) // Invalidate cache
}
```

### HTTP Caching Headers

```typescript
// Express middleware
app.use((req, res, next) => {
  // Static assets: cache for 1 year
  if (req.url.match(/\.(js|css|png|jpg|jpeg|gif|svg|woff|woff2)$/)) {
    res.setHeader('Cache-Control', 'public, max-age=31536000, immutable')
  }

  // HTML: no cache (always revalidate)
  if (req.url.endsWith('.html') || req.url === '/') {
    res.setHeader('Cache-Control', 'no-cache, must-revalidate')
  }

  // API responses: cache for 5 minutes
  if (req.url.startsWith('/api/')) {
    res.setHeader('Cache-Control', 'public, max-age=300')
    res.setHeader('ETag', generateETag(req.url))
  }

  next()
})
```

### CDN Configuration

```yaml
Static Assets to CDN:
  - Images: /images/**
  - JavaScript: /js/**
  - CSS: /css/**
  - Fonts: /fonts/**

CDN Settings:
  - Cache duration: 1 year (with versioned URLs)
  - Gzip/Brotli compression: enabled
  - Image optimization: WebP conversion
  - Purge on deploy: yes (via API)

Recommended CDNs:
  - Cloudflare (free tier excellent)
  - CloudFront (AWS integration)
  - Fastly (enterprise, very fast)
```

---

## Phase 4: Frontend Optimization

### Code Splitting & Lazy Loading

```typescript
// React lazy loading
import { lazy, Suspense } from 'react'

// ❌ Bad: Load everything upfront
import Dashboard from './Dashboard'
import AdminPanel from './AdminPanel'

// ✅ Good: Lazy load routes
const Dashboard = lazy(() => import('./Dashboard'))
const AdminPanel = lazy(() => import('./AdminPanel'))

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
    </Suspense>
  )
}

// Next.js dynamic imports
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <LoadingSpinner />,
  ssr: false // Skip SSR for this component
})
```

### Image Optimization

```jsx
// Next.js Image component (automatic optimization)
import Image from 'next/image'

<Image
  src="/photo.jpg"
  width={800}
  height={600}
  alt="Description"
  loading="lazy"        // Lazy load off-screen images
  placeholder="blur"    // Blur placeholder while loading
  quality={75}          // 75% quality (good balance)
/>

// WebP format with fallback
<picture>
  <source srcset="image.webp" type="image/webp" />
  <source srcset="image.jpg" type="image/jpeg" />
  <img src="image.jpg" alt="Description" loading="lazy" />
</picture>

// Responsive images
<img
  srcset="
    small.jpg 480w,
    medium.jpg 768w,
    large.jpg 1200w
  "
  sizes="(max-width: 480px) 480px, (max-width: 768px) 768px, 1200px"
  src="medium.jpg"
  alt="Description"
/>
```

### Bundle Size Optimization

```bash
# Analyze bundle
npm run build -- --analyze

# Reduce bundle size:
# 1. Remove unused dependencies
npm uninstall unused-package

# 2. Use tree-shaking compatible imports
# ❌ Bad
import _ from 'lodash'
# ✅ Good
import debounce from 'lodash/debounce'

# 3. Dynamic imports for large libraries
const moment = await import('moment')

# 4. Minification (automatic in production builds)
# Vite/Next.js handle this automatically
```

### React Performance

```typescript
// 1. Memoize expensive calculations
import { useMemo } from 'react'

function DataTable({ data }) {
  const sortedData = useMemo(
    () => data.sort((a, b) => a.name.localeCompare(b.name)),
    [data]
  )

  return <Table data={sortedData} />
}

// 2. Memoize components
import { memo } from 'react'

const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  // Only re-renders if data changes
  return <div>{/* expensive rendering */}</div>
})

// 3. useCallback for stable function references
import { useCallback } from 'react'

function Parent() {
  const handleClick = useCallback(() => {
    console.log('Clicked')
  }, [])

  return <ExpensiveChild onClick={handleClick} />
}

// 4. Virtualize long lists
import { FixedSizeList } from 'react-window'

<FixedSizeList
  height={600}
  itemCount={10000}
  itemSize={50}
>
  {({ index, style }) => (
    <div style={style}>Row {index}</div>
  )}
</FixedSizeList>
```

---

## Phase 5: Backend Optimization

### Async Background Processing

```typescript
// ❌ Bad: Synchronous (slow response)
app.post('/send-email', async (req, res) => {
  await sendEmail(req.body) // 3 seconds
  res.json({ success: true })
})

// ✅ Good: Queue job (fast response)
import Bull from 'bull'

const emailQueue = new Bull('emails', 'redis://localhost:6379')

app.post('/send-email', async (req, res) => {
  await emailQueue.add('send', req.body)
  res.json({ success: true, message: 'Email queued' })
})

// Process jobs in background worker
emailQueue.process('send', async job => {
  await sendEmail(job.data)
})
```

### API Response Optimization

```typescript
// 1. Compression
import compression from 'compression'
app.use(compression()) // Gzip responses

// 2. Pagination
app.get('/api/posts', async (req, res) => {
  const page = parseInt(req.query.page) || 1
  const limit = parseInt(req.query.limit) || 20

  const posts = await db.posts.findAll({
    offset: (page - 1) * limit,
    limit: limit
  })

  res.json({
    data: posts,
    pagination: {
      page,
      limit,
      total: await db.posts.count()
    }
  })
})

// 3. Field filtering (GraphQL-style)
app.get('/api/users/:id', async (req, res) => {
  const fields = req.query.fields?.split(',') || ['id', 'name', 'email']

  const user = await db.users.findById(req.params.id, {
    attributes: fields
  })

  res.json(user)
})
```

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit'

// General API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests, please try again later'
})

app.use('/api/', apiLimiter)

// Stricter limit for expensive endpoints
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 requests per hour
  skipSuccessfulRequests: true
})

app.post('/api/auth/login', authLimiter, loginHandler)
```

---

## Phase 6: Monitoring & Alerting

### Application Performance Monitoring (APM)

**Tools**:

- **Sentry**: Error tracking + performance
- **New Relic**: Full-stack APM
- **Datadog**: Infrastructure + APM
- **Vercel Analytics**: Next.js optimized

**Custom Monitoring**:

```typescript
// Track response times
app.use((req, res, next) => {
  const start = Date.now()

  res.on('finish', () => {
    const duration = Date.now() - start

    // Log to monitoring service
    metrics.recordResponseTime(req.path, duration)

    // Alert on slow requests
    if (duration > 1000) {
      logger.warn(`Slow request: ${req.path} took ${duration}ms`)
    }
  })

  next()
})

// Track database query times
db.on('query', (query, duration) => {
  if (duration > 100) {
    logger.warn(`Slow query: ${query} took ${duration}ms`)
  }
})
```

### Performance Dashboards

```yaml
Key Metrics to Track:
  - Response time (P50, P95, P99)
  - Throughput (requests/second)
  - Error rate (%)
  - Database query times
  - Cache hit ratio
  - Memory usage
  - CPU usage

Alerting Thresholds:
  - P95 response time > 1s
  - Error rate > 1%
  - Cache hit ratio < 80%
  - Memory usage > 80%
```

---

## Optimization Checklist

### Frontend ✅

- [ ] Lighthouse score > 90
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] Bundle size < 200KB (initial)
- [ ] Images optimized (WebP, lazy loading)
- [ ] Code splitting implemented
- [ ] Critical CSS inlined

### Backend ✅

- [ ] P95 response time < 500ms
- [ ] Database queries indexed
- [ ] N+1 queries eliminated
- [ ] Connection pooling enabled
- [ ] Background jobs async
- [ ] Rate limiting configured
- [ ] API responses compressed

### Database ✅

- [ ] Slow query log enabled
- [ ] All queries < 100ms (P95)
- [ ] Indexes on foreign keys
- [ ] Indexes on WHERE/ORDER BY columns
- [ ] Query explain plans reviewed
- [ ] Connection pool sized correctly

### Caching ✅

- [ ] Redis/Memcached configured
- [ ] CDN for static assets
- [ ] HTTP cache headers set
- [ ] Cache hit ratio > 80%
- [ ] Cache invalidation strategy

### Infrastructure ✅

- [ ] Auto-scaling configured
- [ ] Load balancer healthy
- [ ] Monitoring/alerting active
- [ ] Logs centralized
- [ ] Backups automated

---

## Related Resources

**Related Skills**:

- `deployment-advisor` - For infrastructure optimization
- `frontend-builder` - For React performance patterns
- `api-designer` - For API optimization

**Related Patterns**:

- `META/DECISION-FRAMEWORK.md` - Scaling decisions
- `STANDARDS/architecture-patterns/caching-patterns.md` - Caching strategies (when created)

**Related Playbooks**:

- `PLAYBOOKS/optimize-database-performance.md` - DB optimization steps (when created)
- `PLAYBOOKS/frontend-performance-audit.md` - Frontend audit procedure (when created)
