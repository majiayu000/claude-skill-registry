---
name: performance-optimization
description: Optimize application performance through code splitting, lazy loading, caching strategies, bundle size reduction, render optimization, and profiling. Use when improving page load times, reducing bundle sizes, optimizing React rendering, implementing code splitting, configuring caching strategies, lazy loading components and routes, optimizing images and assets, profiling performance bottlenecks, implementing virtual scrolling for large lists, or improving Core Web Vitals and Lighthouse scores.
---

# Performance Optimization - Making Software Fast

## When to use this skill

- Improving slow page load times and performance
- Reducing JavaScript bundle sizes
- Optimizing React component rendering with memoization
- Implementing code splitting and lazy loading
- Configuring browser and server-side caching
- Optimizing images with next/image or similar
- Profiling performance bottlenecks with DevTools
- Implementing virtual scrolling for large datasets
- Optimizing database queries and N+1 problems
- Improving Core Web Vitals (LCP, FID, CLS)
- Implementing progressive image loading
- Reducing Time to Interactive (TTI)

## When to use this skill

- Applications are slow, users complain about lag, or you need to improve response times, throughput, or resource usage.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Applications are slow, users complain about lag, or you need to improve response times, throughput, or resource usage.

## Core Principles

1. **Measure First, Optimize Second** - Never guess at bottlenecks
2. **80/20 Rule** - 20% of code causes 80% of performance issues
3. **Premature Optimization is Evil** - Make it work, make it right, then make it fast
4. **Profile, Don't Assume** - Surprises await; your intuition is often wrong
5. **Set Performance Budgets** - Define acceptable limits before optimizing

## Performance Measurement

### Establish Baselines

```bash
# Web Vitals (Frontend)
- FCP (First Contentful Paint): < 1.8s
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1
- TTFB (Time to First Byte): < 600ms

# Backend
- API Response Time: < 200ms (p95)
- Database Query Time: < 50ms (p95)
- Throughput: requests per second
- Error Rate: < 0.1%
```

### Profiling Tools

```bash
# Frontend
- Chrome DevTools Performance tab
- Lighthouse CI
- WebPageTest
- webpack-bundle-analyzer

# Backend
- Node.js: node --prof, clinic.js
- Python: cProfile, py-spy
- Database: EXPLAIN ANALYZE, slow query logs
- APM: New Relic, Datadog, Sentry Performance

# System
- top, htop (CPU/Memory)
- iostat (Disk I/O)
- netstat, iftop (Network)
```

## Frontend Performance

### 1. **Reduce JavaScript Bundle Size**

```javascript
// Before - importing entire library
import _ from 'lodash'; // 70KB
import moment from 'moment'; // 230KB

// After - tree-shaking friendly imports
import debounce from 'lodash/debounce'; // 2KB
import { format } from 'date-fns'; // 13KB

// Code splitting - load on demand
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Dynamic imports
button.onclick = async () => {
  const module = await import('./analytics');
  module.trackEvent('button_click');
};
```

### 2. **Optimize Images**

```html
<!-- Before - unoptimized -->
<img src="photo.jpg" alt="Product" />

<!-- After - responsive & modern formats -->
<picture>
  <source srcset="photo.avif" type="image/avif">
  <source srcset="photo.webp" type="image/webp">
  <img 
    src="photo.jpg" 
    alt="Product"
    loading="lazy"
    width="800" 
    height="600"
    srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1200.jpg 1200w"
    sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  />
</picture>

<!-- Or use Next.js Image component -->
<Image
  src="/photo.jpg"
  alt="Product"
  width={800}
  height={600}
  placeholder="blur"
  quality={85}
/>
```

### 3. **Lazy Load & Code Split**

```typescript
// React - lazy load routes
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}

// Next.js - automatic code splitting
// Just use dynamic imports
import dynamic from 'next/dynamic';

const DynamicChart = dynamic(() => import('./Chart'), {
  loading: () => <Spinner />,
  ssr: false // Don't render on server
});
```

### 4. **Memoization & Caching**

```typescript
// React - prevent unnecessary re-renders
const ExpensiveComponent = memo(({ data }) => {
  return <div>{/* Complex rendering */}</div>;
});

// Memoize expensive calculations
function ProductList({ products, filters }) {
  const filteredProducts = useMemo(() => {
    return products.filter(p => matchesFilters(p, filters));
  }, [products, filters]); // Only recalculate when dependencies change
  
  return <div>{filteredProducts.map(renderProduct)}</div>;
}

// Memoize callbacks to prevent child re-renders
function Parent() {
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []); // Stable function reference
  
  return <Child onClick={handleClick} />;
}
```

### 5. **Virtualization for Long Lists**

```typescript
// Before - renders 10,000 items (slow!)
function ProductList({ products }) {
  return (
    <div>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

// After - only renders visible items
import { FixedSizeList } from 'react-window';

function ProductList({ products }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={products.length}
      itemSize={100}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          <ProductCard product={products[index]} />
        </div>
      )}
    </FixedSizeList>
  );
}
```

## Backend Performance

### 1. **Database Query Optimization**

```sql
-- Before - N+1 query problem
-- Fetches users, then makes separate query for each user's posts
SELECT * FROM users;
-- Then for each user:
SELECT * FROM posts WHERE user_id = ?;

-- After - join or eager loading
SELECT 
  users.*, 
  posts.id as post_id,
  posts.title as post_title
FROM users
LEFT JOIN posts ON posts.user_id = users.id;

-- Add indexes for frequently queried columns
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at);

-- Composite index for common query patterns
CREATE INDEX idx_posts_user_created 
ON posts(user_id, created_at DESC);
```

### 2. **Caching Strategies**

```typescript
// Memory cache for expensive computations
const cache = new Map();

async function getExpensiveData(key) {
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const data = await expensiveComputation(key);
  cache.set(key, data);
  
  // Expire after 5 minutes
  setTimeout(() => cache.delete(key), 5 * 60 * 1000);
  
  return data;
}

// Redis cache for distributed systems
import Redis from 'ioredis';
const redis = new Redis();

async function getCachedUserProfile(userId) {
  const cacheKey = `user:${userId}:profile`;
  
  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // Cache miss - fetch from database
  const profile = await db.users.findById(userId);
  
  // Store in cache (expire after 1 hour)
  await redis.setex(cacheKey, 3600, JSON.stringify(profile));
  
  return profile;
}

// HTTP caching headers
app.get('/api/products', (req, res) => {
  res.set({
    'Cache-Control': 'public, max-age=300', // 5 minutes
    'ETag': generateETag(data)
  });
  res.json(products);
});
```

### 3. **Database Connection Pooling**

```typescript
// Before - new connection per query (slow!)
async function getUser(id) {
  const connection = await mysql.createConnection(config);
  const [rows] = await connection.execute('SELECT * FROM users WHERE id = ?', [id]);
  await connection.end();
  return rows[0];
}

// After - connection pool
import mysql from 'mysql2/promise';

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  database: 'mydb',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

async function getUser(id) {
  const [rows] = await pool.execute('SELECT * FROM users WHERE id = ?', [id]);
  return rows[0];
}

// NeonDB serverless - use @neondatabase/serverless
import { Pool } from '@neondatabase/serverless';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
```

### 4. **Pagination & Limiting**

```typescript
// Before - fetches all records (memory explosion!)
async function getProducts() {
  return await db.products.findAll(); // Could be millions of rows
}

// After - cursor-based pagination
async function getProducts({ cursor, limit = 20 }) {
  return await db.products.findMany({
    take: limit,
    skip: cursor ? 1 : 0,
    cursor: cursor ? { id: cursor } : undefined,
    orderBy: { createdAt: 'desc' }
  });
}

// Offset pagination (simpler but slower for deep pages)
async function getProducts({ page = 1, limit = 20 }) {
  const offset = (page - 1) * limit;
  return await db.products.findMany({
    take: limit,
    skip: offset,
    orderBy: { createdAt: 'desc' }
  });
}
```

### 5. **Async Processing & Job Queues**

```typescript
// Before - blocks request until email sent
app.post('/signup', async (req, res) => {
  const user = await createUser(req.body);
  await sendWelcomeEmail(user.email); // Blocks for 2-3 seconds!
  res.json({ success: true });
});

// After - queue job, respond immediately
import { Queue } from 'bullmq';

const emailQueue = new Queue('emails', {
  connection: { host: 'localhost', port: 6379 }
});

app.post('/signup', async (req, res) => {
  const user = await createUser(req.body);
  
  // Queue email to be sent asynchronously
  await emailQueue.add('welcome', {
    to: user.email,
    userId: user.id
  });
  
  res.json({ success: true }); // Fast response!
});

// Worker processes jobs in background
const worker = new Worker('emails', async (job) => {
  await sendEmail(job.data.to, 'welcome', { userId: job.data.userId });
});
```

## Algorithm Optimization

### Choose Right Data Structure

```typescript
// Before - O(n) lookup
const activeUsers = [];
function isActive(userId) {
  return activeUsers.includes(userId); // Linear search
}

// After - O(1) lookup
const activeUsers = new Set();
function isActive(userId) {
  return activeUsers.has(userId); // Constant time
}

// Before - O(n) for frequent insertions/deletions at start
const queue = [];
queue.unshift(item); // O(n) - shifts entire array

// After - O(1) with proper data structure
class Queue {
  constructor() {
    this.items = {};
    this.head = 0;
    this.tail = 0;
  }
  
  enqueue(item) {
    this.items[this.tail] = item;
    this.tail++;
  }
  
  dequeue() {
    const item = this.items[this.head];
    delete this.items[this.head];
    this.head++;
    return item;
  }
}
```

### Reduce Computational Complexity

```typescript
// Before - O(n²) nested loops
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) {
        duplicates.push(arr[i]);
      }
    }
  }
  return duplicates;
}

// After - O(n) with Set
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  
  for (const item of arr) {
    if (seen.has(item)) {
      duplicates.add(item);
    }
    seen.add(item);
  }
  
  return Array.from(duplicates);
}
```

## Monitoring & Alerting

### Add Performance Metrics

```typescript
import { performance } from 'perf_hooks';

async function processOrder(order) {
  const startTime = performance.now();
  
  try {
    const result = await expensiveProcessing(order);
    
    const duration = performance.now() - startTime;
    
    // Log slow operations
    if (duration > 1000) {
      logger.warn('Slow order processing', { 
        orderId: order.id, 
        duration 
      });
    }
    
    // Send metrics to monitoring service
    metrics.histogram('order_processing_time', duration, {
      status: 'success'
    });
    
    return result;
  } catch (error) {
    const duration = performance.now() - startTime;
    metrics.histogram('order_processing_time', duration, {
      status: 'error'
    });
    throw error;
  }
}
```

## Performance Checklist

```
Frontend:
□ Bundle size < 200KB (gzipped)
□ Images optimized (WebP/AVIF)
□ Lazy loading for below-fold content
□ Code splitting for routes
□ Long lists virtualized
□ Expensive computations memoized
□ HTTP caching headers set
□ Critical CSS inlined

Backend:
□ Database queries indexed
□ N+1 queries eliminated
□ Connection pooling configured
□ Responses paginated
□ Heavy operations queued
□ Response caching implemented
□ Gzip compression enabled
□ CDN for static assets

General:
□ Performance budgets defined
□ Monitoring & alerting configured
□ Regular performance testing in CI
□ Profiling done on realistic data
```

## Resources

- [Web Vitals](https://web.dev/vitals/)
- [High Performance Browser Networking](https://hpbn.co/)
- [Database Indexing Explained](https://use-the-index-luke.com/)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)

---

**Remember**: Fast software delights users. Measure, optimize bottlenecks, and monitor continuously.
