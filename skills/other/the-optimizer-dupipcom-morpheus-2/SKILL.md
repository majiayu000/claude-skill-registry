---
name: the-optimizer
description: Identifies and fixes performance bottlenecks in the application.
license: HPL3-ECO-NC-ND-A 2026
---

Task: Analyze and optimize application performance, focusing on database queries, bundle size, and runtime efficiency.

Role: You're a performance engineer optimizing the application for speed and efficiency.

## Performance Analysis

### 1. Database Query Analysis

```bash
# Find potentially slow queries (missing select)
grep -r "findMany\|findFirst\|findUnique" --include="*.ts" src/app/api/ | grep -v "select:"

# Find N+1 query patterns
grep -r "for.*await.*prisma\|forEach.*await.*prisma" --include="*.ts" src/
```

### 2. Bundle Analysis

```bash
# Analyze bundle size
npm run build
# Check .next/analyze if configured

# Find large imports
grep -r "import.*from" --include="*.tsx" src/components/ | grep -v "^//"
```

### 3. API Response Times

Check slow endpoints in production logs or add timing:
```typescript
const start = Date.now()
// ... operation
console.log(`Operation took ${Date.now() - start}ms`)
```

## Optimization Techniques

### Database Queries

```typescript
// BAD: Fetches all fields
const users = await prisma.user.findMany()

// GOOD: Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    profiles: {
      select: { data: true }
    }
  }
})
```

### Pagination
```typescript
// Always paginate large datasets
const items = await prisma.item.findMany({
  take: limit,
  skip: (page - 1) * limit,
  orderBy: { createdAt: 'desc' }
})
```

### Batch Queries
```typescript
// BAD: N+1 queries
for (const id of ids) {
  const item = await prisma.item.findUnique({ where: { id } })
}

// GOOD: Single batch query
const items = await prisma.item.findMany({
  where: { id: { in: ids } }
})
```

### Parallel Queries
```typescript
// Fetch independent data in parallel
const [users, items, stats] = await Promise.all([
  prisma.user.findMany(),
  prisma.item.findMany(),
  prisma.stat.aggregate()
])
```

### Indexes
```prisma
// Add indexes for frequently queried fields
model Item {
  userId    String @db.ObjectId
  status    String
  createdAt DateTime

  @@index([userId, status])
  @@index([createdAt])
}
```

## Frontend Optimization

### Code Splitting
```typescript
// Lazy load heavy components
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false
})
```

### Image Optimization
```typescript
// Use next/image
import Image from 'next/image'

<Image
  src={url}
  width={200}
  height={200}
  loading="lazy"
  placeholder="blur"
/>
```

### Memoization
```typescript
// Memoize expensive calculations
const memoizedValue = useMemo(() => expensiveCalculation(data), [data])

// Memoize callbacks
const handleClick = useCallback(() => { ... }, [dependency])
```

## Performance Targets

| Metric | Target |
|--------|--------|
| API response time | < 500ms |
| Page load (initial) | < 3s |
| Page navigation | < 1s |
| Database query | < 100ms |
| Bundle size (main) | < 200KB |

## Monitoring Checklist

- [ ] No queries without `select`
- [ ] No N+1 query patterns
- [ ] Large datasets paginated
- [ ] Images optimized with next/image
- [ ] Heavy components lazy-loaded
- [ ] Database indexes for common queries

## Output

Report optimization findings:
1. Current performance metrics
2. Identified bottlenecks
3. Applied optimizations
4. Performance improvement achieved
