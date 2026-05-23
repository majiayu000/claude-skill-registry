---
name: performance-auditing
description: Audit web applications for performance issues and optimize for speed, especially on Cloudflare Workers edge runtime. Use when diagnosing slow pages, optimizing load times, reducing bundle size, improving Core Web Vitals, or optimizing for edge deployment. Triggers on requests like "audit performance", "optimize speed", "improve load time", "reduce bundle size", "Core Web Vitals", or "edge optimization".
---

# Performance Auditing

Audit and optimize performance for Cloudflare Workers edge deployment.

## Process

1. **Measure baseline** - Current metrics and bottlenecks
2. **Analyze bundle** - JavaScript size and splitting
3. **Optimize loading** - Critical path, lazy loading
4. **Database queries** - D1 optimization
5. **Caching strategy** - Edge and browser caching

## Core Web Vitals

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | ≤4.0s | >4.0s |
| FID (First Input Delay) | ≤100ms | ≤300ms | >300ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | ≤0.25 | >0.25 |
| INP (Interaction to Next Paint) | ≤200ms | ≤500ms | >500ms |

## JavaScript Optimization

### Bundle Analysis

```bash
# Analyze bundle size
npx @next/bundle-analyzer

# Or use built-in Next.js analysis
ANALYZE=true npm run build
```

### Code Splitting

```tsx
// Dynamic imports for heavy components
import dynamic from 'next/dynamic';

const HeavyEditor = dynamic(() => import('@/components/Editor'), {
  loading: () => <EditorSkeleton />,
  ssr: false,  // Client-only if needed
});

// Route-based splitting (automatic with App Router)
// Each route segment is a separate chunk
```

### Tree Shaking

```typescript
// Bad: imports entire library
import _ from 'lodash';
_.debounce(fn, 300);

// Good: imports only what's needed
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

## Image Optimization

### Next.js Image Component

```tsx
import Image from 'next/image';

// Optimized with automatic sizing
<Image
  src={`/api/media/${path}`}
  alt={alt}
  width={800}
  height={600}
  sizes="(max-width: 768px) 100vw, 800px"
  priority={isAboveFold}  // Preload LCP images
/>
```

### Cloudflare Image Transformations

```tsx
// Use existing image.ts helper for transformations
import { getImageUrl } from '@/lib/image';

// Resize on the fly via Cloudflare
const optimizedUrl = getImageUrl(path, { width: 400, quality: 80 });
```

### Lazy Loading

```tsx
// Below-fold images
<Image loading="lazy" ... />

// Native lazy loading for img
<img loading="lazy" decoding="async" ... />
```

## React Optimization

### Memoization

```tsx
// Expensive computations
const sortedArticles = useMemo(
  () => articles.sort((a, b) => new Date(b.date) - new Date(a.date)),
  [articles]
);

// Callback stability
const handleClick = useCallback((id) => {
  setSelected(id);
}, []);

// Component memoization (use sparingly)
const ArticleCard = memo(({ article }) => { ... });
```

### Avoiding Re-renders

```tsx
// Bad: creates new object every render
<Component style={{ color: 'red' }} />

// Good: stable reference
const style = { color: 'red' };
<Component style={style} />

// Bad: inline function
<Button onClick={() => handleClick(id)} />

// Good: stable callback
const handleButtonClick = useCallback(() => handleClick(id), [id]);
<Button onClick={handleButtonClick} />
```

## D1 Database Optimization

### Indexing

```sql
-- Ensure indexes exist for common queries
CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published);
CREATE INDEX IF NOT EXISTS idx_articles_authored_on ON articles(authored_on);
CREATE INDEX IF NOT EXISTS idx_articles_slug ON articles(slug);

-- Composite indexes for common filters
CREATE INDEX IF NOT EXISTS idx_articles_pub_date
  ON articles(published, authored_on DESC);
```

### Query Optimization

```typescript
// Bad: fetching all then filtering
const all = await db.prepare('SELECT * FROM articles').all();
const published = all.results.filter(a => a.published);

// Good: filter in query
const published = await db.prepare(
  'SELECT * FROM articles WHERE published = 1 ORDER BY authored_on DESC LIMIT ?'
).bind(limit).all();

// Bad: N+1 queries
for (const article of articles) {
  const tags = await db.prepare('SELECT * FROM tags WHERE article_id = ?').bind(article.id).all();
}

// Good: JOIN or batch query
const articlesWithTags = await db.prepare(`
  SELECT a.*, GROUP_CONCAT(t.name) as tags
  FROM articles a
  LEFT JOIN article_tags at ON a.id = at.article_id
  LEFT JOIN tags t ON at.tag_id = t.id
  WHERE a.published = 1
  GROUP BY a.id
`).all();
```

### Pagination

```typescript
// Offset pagination (simple but slower for large offsets)
const page = parseInt(searchParams.get('page') || '1');
const limit = 10;
const offset = (page - 1) * limit;

// Cursor pagination (better for large datasets)
const cursor = searchParams.get('cursor');
const query = cursor
  ? 'SELECT * FROM articles WHERE id < ? ORDER BY id DESC LIMIT ?'
  : 'SELECT * FROM articles ORDER BY id DESC LIMIT ?';
```

## Caching Strategy

### Static Generation

```tsx
// Force static for public pages
export const dynamic = 'force-static';
export const revalidate = 3600; // Revalidate every hour

// Or use ISR
export const revalidate = 60; // Revalidate every minute
```

### Data Caching

```typescript
// Cache database results
const cached = await caches.default.match(cacheKey);
if (cached) return cached;

const data = await fetchData();
const response = new Response(JSON.stringify(data));
await caches.default.put(cacheKey, response.clone());
return response;
```

### Browser Caching Headers

```typescript
// For static assets
return new Response(body, {
  headers: {
    'Cache-Control': 'public, max-age=31536000, immutable',
  },
});

// For dynamic content
return new Response(body, {
  headers: {
    'Cache-Control': 'public, max-age=60, s-maxage=300',
  },
});
```

## Workers-Specific Optimization

### CPU Time Limits

```typescript
// Workers have CPU time limits (10-50ms typically)
// Avoid synchronous heavy computation

// Bad: blocking computation
const result = heavyComputation(data);

// Good: break into smaller chunks or use Durable Objects
```

### Memory Limits

```typescript
// Workers have memory limits (128MB typical)
// Stream large responses instead of buffering

// Bad: buffer entire file
const file = await bucket.get(key);
const body = await file.arrayBuffer();

// Good: stream the response
const file = await bucket.get(key);
return new Response(file.body, { headers });
```

## Output

Provide performance audit results:
1. Core Web Vitals measurements
2. Bundle size analysis
3. Database query analysis
4. Caching recommendations
5. Priority fixes with implementation code
