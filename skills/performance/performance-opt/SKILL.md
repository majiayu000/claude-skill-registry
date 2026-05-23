---
name: performance-opt
description: Analyze and optimize application performance including bundle size, render performance, and API response times. Use when investigating slow pages or optimizing production builds.
allowed-tools: Read, Grep, Glob, Bash
---

# Performance Optimization Skill

This skill helps you identify and fix performance bottlenecks across the platform.

## When to Use This Skill

- Investigating slow page loads
- Optimizing bundle size
- Reducing API response times
- Improving database query performance
- Optimizing React re-renders
- Before production deployments

## Performance Metrics

### Web Vitals (Next.js)

**Core Web Vitals:**
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1

**Other Metrics:**
- **FCP** (First Contentful Paint): < 1.8s
- **TTFB** (Time to First Byte): < 600ms
- **TTI** (Time to Interactive): < 3.8s

### Measure Performance

```bash
# Run Lighthouse
npx lighthouse https://sgcarstrends.com --view

# Or use Chrome DevTools:
# 1. Open DevTools
# 2. Lighthouse tab
# 3. Generate report
```

## Bundle Size Optimization

### Analyze Bundle

```bash
# Next.js bundle analyzer
cd apps/web

# Add to next.config.js temporarily
ANALYZE=true pnpm build

# Or use bundle-analyzer package
pnpm add -D @next/bundle-analyzer

# View analysis
open .next/analyze/client.html
```

### Reduce Bundle Size

**1. Dynamic Imports**

```typescript
// ❌ Static import (loads immediately)
import { HeavyComponent } from "./heavy-component";

export default function Page() {
  return <HeavyComponent />;
}

// ✅ Dynamic import (lazy load)
import dynamic from "next/dynamic";

const HeavyComponent = dynamic(() => import("./heavy-component"), {
  loading: () => <div>Loading...</div>,
  ssr: false,  // Disable SSR if not needed
});

export default function Page() {
  return <HeavyComponent />;
}
```

**2. Tree Shaking**

```typescript
// ❌ Imports entire library
import _ from "lodash";
const result = _.uniq(array);

// ✅ Import only what you need
import uniq from "lodash/uniq";
const result = uniq(array);

// ✅ Or use modern alternative
const result = [...new Set(array)];
```

**3. Optimize Dependencies**

```bash
# Find large dependencies
npx npkill

# Or analyze with bundlephobia
# Visit: https://bundlephobia.com

# Replace large libs with smaller alternatives:
# moment.js (70kb) → date-fns (13kb) or dayjs (2kb)
# lodash (71kb) → lodash-es + tree shaking
```

**4. Code Splitting**

```typescript
// Split by route (automatic in Next.js)
// Each page is a separate chunk

// Split by component
const AdminPanel = dynamic(() => import("./admin-panel"));

// Split by condition
const Chart = dynamic(() =>
  import(userPreference === "advanced" ? "./advanced-chart" : "./simple-chart")
);
```

## React Performance

### Prevent Unnecessary Re-renders

**1. useMemo**

```typescript
// ❌ Recalculates on every render
function Component({ data }) {
  const processed = expensiveOperation(data);
  return <div>{processed}</div>;
}

// ✅ Memoized calculation
function Component({ data }) {
  const processed = useMemo(
    () => expensiveOperation(data),
    [data]
  );
  return <div>{processed}</div>;
}
```

**2. useCallback**

```typescript
// ❌ New function on every render
function Parent() {
  return <Child onClick={() => console.log("clicked")} />;
}

// ✅ Memoized function
function Parent() {
  const handleClick = useCallback(() => {
    console.log("clicked");
  }, []);

  return <Child onClick={handleClick} />;
}
```

**3. React.memo**

```typescript
// ❌ Re-renders even when props unchanged
function ChildComponent({ name }) {
  return <div>{name}</div>;
}

// ✅ Only re-renders when props change
const ChildComponent = React.memo(function ChildComponent({ name }) {
  return <div>{name}</div>;
});
```

### Virtualize Long Lists

```bash
# Install virtualization library
pnpm add -D react-window
```

```typescript
import { FixedSizeList } from "react-window";

// ❌ Renders all items (slow for 1000+ items)
function CarList({ cars }) {
  return (
    <div>
      {cars.map(car => <CarCard key={car.id} car={car} />)}
    </div>
  );
}

// ✅ Only renders visible items
function CarList({ cars }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      <CarCard car={cars[index]} />
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={cars.length}
      itemSize={100}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

### Debounce User Input

```typescript
import { useDeferredValue, useState } from "react";

function SearchComponent() {
  const [input, setInput] = useState("");
  const deferredInput = useDeferredValue(input);  // Defers update

  return (
    <>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <SearchResults query={deferredInput} />
    </>
  );
}
```

## Database Query Optimization

### Identify Slow Queries

```typescript
// Add query timing
const start = Date.now();
const result = await db.query.cars.findMany();
const duration = Date.now() - start;

if (duration > 100) {
  console.warn(`Slow query: ${duration}ms`);
}
```

### Optimize Queries

**1. Add Indexes**

```typescript
// packages/database/src/db/schema/cars.ts
import { pgTable, text, index } from "drizzle-orm/pg-core";

export const cars = pgTable("cars", {
  id: text("id").primaryKey(),
  make: text("make").notNull(),
  month: text("month").notNull(),
}, (table) => ({
  // Add indexes for frequently queried columns
  makeIdx: index("cars_make_idx").on(table.make),
  monthIdx: index("cars_month_idx").on(table.month),
}));
```

**2. Avoid N+1 Queries**

```typescript
// ❌ N+1 queries (slow)
const posts = await db.query.posts.findMany();
for (const post of posts) {
  post.author = await db.query.users.findFirst({
    where: eq(users.id, post.authorId),
  });
}

// ✅ Single query with join (fast)
const posts = await db.query.posts.findMany({
  with: {
    author: true,
  },
});
```

**3. Select Only Needed Columns**

```typescript
// ❌ Selects all columns
const users = await db.query.users.findMany();

// ✅ Select only what's needed
const users = await db
  .select({
    id: users.id,
    name: users.name,
    email: users.email,
  })
  .from(users);
```

**4. Use Pagination**

```typescript
// ❌ Loads all records
const cars = await db.query.cars.findMany();

// ✅ Paginated query
const cars = await db.query.cars.findMany({
  limit: 20,
  offset: (page - 1) * 20,
});
```

**5. Batch Queries**

```typescript
// ❌ Multiple separate queries
const user1 = await db.query.users.findFirst({ where: eq(users.id, "1") });
const user2 = await db.query.users.findFirst({ where: eq(users.id, "2") });
const user3 = await db.query.users.findFirst({ where: eq(users.id, "3") });

// ✅ Single batched query
const userIds = ["1", "2", "3"];
const users = await db.query.users.findMany({
  where: inArray(users.id, userIds),
});
```

## Caching Strategies

### Server-Side Caching

```typescript
import { redis } from "@sgcarstrends/utils";

export async function getCarsWithCache(make: string) {
  const cacheKey = `cars:${make}`;

  // Check cache
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached as string);
  }

  // Fetch from database
  const cars = await db.query.cars.findMany({
    where: eq(cars.make, make),
  });

  // Cache for 1 hour
  await redis.set(cacheKey, JSON.stringify(cars), { ex: 3600 });

  return cars;
}
```

### Next.js Caching

```typescript
// Cache with revalidation
export const revalidate = 3600;  // Revalidate every hour

export async function getData() {
  const res = await fetch("https://api.example.com/data", {
    next: { revalidate: 3600 },
  });
  return res.json();
}

// Cache indefinitely, revalidate on demand
export const dynamic = "force-static";

export async function getStaticData() {
  // This data is cached until manually revalidated
  const data = await db.query.cars.findMany();
  return data;
}
```

## Image Optimization

### Use Next.js Image Component

```typescript
import Image from "next/image";

// ❌ Regular img tag
<img src="/logo.png" alt="Logo" />

// ✅ Optimized image
<Image
  src="/logo.png"
  alt="Logo"
  width={200}
  height={200}
  priority  // For above-the-fold images
/>

// ✅ Responsive image
<Image
  src="/hero.jpg"
  alt="Hero"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  priority
/>
```

### Image Formats

```typescript
// Use modern formats
<Image
  src="/image.webp"  // WebP for smaller size
  alt="Image"
  width={800}
  height={600}
/>

// Automatic format optimization with Next.js Image
// Next.js automatically serves WebP/AVIF when supported
```

## API Performance

### Response Time Optimization

```typescript
// Add response time logging
app.use(async (c, next) => {
  const start = Date.now();
  await next();
  const duration = Date.now() - start;

  c.header("X-Response-Time", `${duration}ms`);

  if (duration > 500) {
    console.warn(`Slow endpoint: ${c.req.path} (${duration}ms)`);
  }
});
```

### Compression

```typescript
// Enable compression in Hono
import { compress } from "hono/compress";

const app = new Hono();
app.use("*", compress());
```

### Pagination

```typescript
// Implement cursor-based pagination
export async function getCars(cursor?: string, limit = 20) {
  const query = db.query.cars.findMany({
    limit: limit + 1,  // Fetch one extra to determine if there's more
    orderBy: desc(cars.createdAt),
  });

  if (cursor) {
    query.where(lt(cars.id, cursor));
  }

  const results = await query;
  const hasMore = results.length > limit;
  const items = hasMore ? results.slice(0, -1) : results;

  return {
    items,
    nextCursor: hasMore ? items[items.length - 1].id : null,
  };
}
```

## Lambda Performance

### Cold Start Optimization

```typescript
// infra/api.ts
export function API({ stack, app }: StackContext) {
  const api = new Function(stack, "api", {
    handler: "apps/api/src/index.handler",
    runtime: "nodejs20.x",
    architecture: "arm64",  // Graviton2 for better performance
    memory: 1024,  // More memory = faster CPU
    nodejs: {
      esbuild: {
        minify: true,  // Smaller bundle = faster cold starts
        bundle: true,
      },
    },
  });
}
```

### Provisioned Concurrency

For production with consistent traffic:

```typescript
const api = new Function(stack, "api", {
  handler: "apps/api/src/index.handler",
  reservedConcurrentExecutions: 10,  // Reserve instances
});
```

## Performance Monitoring

### Web Vitals in Next.js

```typescript
// app/layout.tsx
import { SpeedInsights } from "@vercel/speed-insights/next";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### Custom Performance Marks

```typescript
export async function performanceTracked Operation() {
  performance.mark("operation-start");

  await doSomething();

  performance.mark("operation-end");
  performance.measure("operation", "operation-start", "operation-end");

  const measure = performance.getEntriesByName("operation")[0];
  console.log(`Operation took ${measure.duration}ms`);
}
```

## Performance Testing

### Load Testing

```bash
# Install Apache Bench
# or use k6, Artillery, etc.

# Test API endpoint
ab -n 1000 -c 10 https://api.sgcarstrends.com/health

# With k6
k6 run loadtest.js
```

### Performance Benchmarks

```typescript
// __tests__/performance/database.test.ts
import { performance } from "perf_hooks";

describe("Database Performance", () => {
  it("queries cars in < 100ms", async () => {
    const start = performance.now();

    await db.query.cars.findMany({ limit: 100 });

    const duration = performance.now() - start;
    expect(duration).toBeLessThan(100);
  });
});
```

## Performance Checklist

- [ ] Bundle size < 200KB (initial load)
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] API responses < 500ms
- [ ] Database queries < 100ms
- [ ] Images optimized (WebP/AVIF)
- [ ] Code splitting implemented
- [ ] Lazy loading for heavy components
- [ ] Caching strategy in place
- [ ] Long lists virtualized
- [ ] Compression enabled
- [ ] Indexes on frequently queried columns

## Quick Wins

1. **Enable Compression**: Instant 60-80% size reduction
2. **Add Image Optimization**: Use Next.js Image component
3. **Implement Caching**: Cache expensive operations
4. **Add Indexes**: Speed up database queries
5. **Code Splitting**: Lazy load heavy components
6. **Tree Shaking**: Import only what you need
7. **Memoization**: Prevent unnecessary calculations

## References

- Web Vitals: https://web.dev/vitals
- Next.js Performance: https://nextjs.org/docs/app/building-your-application/optimizing
- React Performance: https://react.dev/learn/render-and-commit
- Related files:
  - `apps/web/next.config.js` - Next.js configuration
  - Root CLAUDE.md - Performance guidelines

## Best Practices

1. **Measure First**: Use profiling before optimizing
2. **Focus on Impact**: Optimize bottlenecks, not everything
3. **Monitor Production**: Track real user performance
4. **Regular Audits**: Run Lighthouse monthly
5. **Test Performance**: Add performance tests
6. **Document Optimizations**: Note why and what was optimized
7. **Avoid Premature Optimization**: Profile first, then optimize
8. **Use Tools**: Leverage built-in Next.js optimizations
