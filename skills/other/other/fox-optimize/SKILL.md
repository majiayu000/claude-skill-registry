---
name: fox-optimize
description: Hunt performance bottlenecks with swift precision. Stalk the slow paths, pinpoint the prey, streamline the code, catch the gains, and celebrate the win. Use when optimizing performance, profiling code, or hunting for speed.
---

# Fox Optimize 🦊

The fox doesn't lumber through the forest. It moves with swift precision, finding the fastest paths between trees. When something slows the hunt, the fox notices immediately. It stalks the problem, isolates it, and strikes. The forest flows better after the fox passes through.

## When to Activate

- User asks to "optimize this" or "make it faster"
- User says "it's slow" or "performance issue"
- User calls `/fox-optimize` or mentions fox/performance
- Page load times are unacceptable
- Database queries are sluggish
- Bundle size is too large
- Memory leaks detected
- Animations are janky
- API response times are slow

**Pair with:** `bloodhound-scout` to find slow code paths

---

## The Hunt

```
STALK → PINPOINT → STREAMLINE → CATCH → CELEBRATE
   ↓         ↲           ↲           ↓          ↓
Watch for  Find the    Optimize   Capture   Enjoy the
Slowness   Bottleneck  Hot Paths  Gains     Win
```

### Phase 1: STALK

_The fox pads silently, watching for what moves too slowly..._

Identify where performance matters:

**What feels slow?**

- Initial page load (First Contentful Paint)
- Interactions (Time to Interactive)
- Scrolling (frame drops)
- Data loading (API latency)
- Transitions (animation jank)

**Measure before optimizing:**

```bash
# Web vitals
npm install -g lighthouse
lighthouse https://yoursite.com --output=json

# Bundle analysis
npm run build
npm run analyze

# Database query times
# Check your ORM's query logging
```

**Set a target:**

- First Contentful Paint: < 1.8s
- Time to Interactive: < 3.8s
- API response: < 200ms (p95)
- Animation: 60fps consistently

**Output:** Baseline metrics and target goals defined

---

### Phase 2: PINPOINT

_Ears perk. The fox isolates exactly where the prey hides..._

Find the bottleneck:

**Frontend Performance:**

```javascript
// Chrome DevTools Performance tab
// Look for:
// - Long tasks (>50ms)
// - Layout thrashing (forced reflows)
// - Memory leaks (growing heap)

// Lighthouse report flags:
// - Unused JavaScript
// - Render-blocking resources
// - Unoptimized images
// - Third-party scripts
```

**Database Queries:**

```sql
-- Find slow queries (SQLite example)
-- Enable query logging in your ORM

-- Check for missing indexes
EXPLAIN QUERY PLAN
SELECT * FROM posts WHERE tenant_id = 'x' AND status = 'published';
-- Look for "SCAN" instead of "SEARCH" - needs index

-- Add index
CREATE INDEX idx_posts_tenant_status ON posts(tenant_id, status);
```

**Bundle Analysis:**

```bash
# Visualize what's in your bundle
npm install --save-dev rollup-plugin-visualizer

# Add to vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

plugins: [
  visualizer({ open: true })
]

# Look for:
# - Large dependencies (can you tree-shake?)
# - Duplicate code
# - Unnecessary polyfills
```

**Common Bottlenecks:**

| Area         | Common Issues                                         |
| ------------ | ----------------------------------------------------- |
| **Frontend** | Unoptimized images, blocking JS, large bundles        |
| **Database** | Missing indexes, N+1 queries, full table scans        |
| **API**      | Synchronous blocking, no caching, heavy computation   |
| **Network**  | Too many requests, no compression, large payloads     |
| **Memory**   | Leaks from unsubscribed listeners, retained DOM nodes |

**Output:** Specific bottleneck identified with evidence

---

### Phase 3: STREAMLINE

_The fox finds the fastest path through the thicket..._

Apply targeted optimizations:

**Image Optimization:**

```svelte
<!-- Use proper formats and sizes -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description" loading="lazy" decoding="async">
</picture>

<!-- Or use a component -->
<OptimizedImage
  src="photo.jpg"
  alt="Description"
  widths={[400, 800, 1200]}
  sizes="(max-width: 800px) 100vw, 800px"
/>
```

**Code Splitting:**

```typescript
// Before: Everything in main bundle
import HeavyChart from './HeavyChart.svelte';

// After: Lazy load
const HeavyChart = lazy(() => import('./HeavyChart.svelte'));

// Or in SvelteKit
{#await import('./HeavyChart.svelte') then { default: HeavyChart }}
  <HeavyChart data={chartData} />
{/await}
```

**Database Optimization:**

```typescript
// Before: N+1 query problem
const posts = await db.query.posts.findMany();
for (const post of posts) {
  post.author = await db.query.users.findFirst({
    where: eq(users.id, post.authorId),
  });
}

// After: Single query with join
const postsWithAuthors = await db.query.posts.findMany({
  with: {
    author: true,
  },
});
```

**Caching Strategy:**

```typescript
// API route caching
export const GET: RequestHandler = async ({ platform }) => {
  const cache = platform?.env?.CACHE;
  const cacheKey = "popular-posts";

  // Check cache first
  let data = await cache?.get(cacheKey);
  if (data) {
    return json(JSON.parse(data));
  }

  // Fetch fresh
  data = await fetchPopularPosts();

  // Cache for 5 minutes
  await cache?.put(cacheKey, JSON.stringify(data), { expirationTtl: 300 });

  return json(data);
};
```

**Memoization:**

```svelte
<script>
  import { memoize } from '$lib/utils/memoize';

  // Expensive computation
  const calculateStats = memoize((data) => {
    return data.reduce(/* complex logic */);
  });

  // Only recalculates when data changes
  $: stats = calculateStats($dataStore);
</script>
```

**Virtual Scrolling:**

```svelte
<!-- For long lists -->
<VirtualList items={largeArray} let:item>
  <ListItem {item} />
</VirtualList>

<!-- Only renders visible items -->
```

**Output:** Optimizations applied with minimal code changes

---

### Phase 4: CATCH

_The fox snaps its jaws—speed captured..._

**MANDATORY: Verify the optimization didn't break anything:**

```bash
# Sync dependencies
pnpm install

# Verify ONLY the packages the fox touched — lint, check, test, build
gw ci --affected --fail-fast --diagnose
```

**If verification fails:** The fox moved too fast and broke something. Read the diagnostics, fix the regression, re-run verification. Speed without correctness is worthless.

**Once CI passes**, measure the improvement:

**Before/After Comparison:**

```
Metric          Before    After    Improvement
─────────────────────────────────────────────
FCP             2.4s      1.1s     54% faster
Bundle size     340kb     180kb    47% smaller
Query time      450ms     85ms     81% faster
Memory usage    180MB     95MB     47% less
```

**Profile again:**

```bash
# Re-run Lighthouse
lighthouse https://yoursite.com

# Check new bundle
npm run build && npm run analyze
```

**Output:** Documented gains with verification

---

### Phase 5: CELEBRATE

_The fox yips with joy, the hunt complete..._

**Performance Report:**

```markdown
## 🦊 FOX OPTIMIZATION COMPLETE

### Target

Home page load time

### Bottleneck Found

Unoptimized hero image (2.1MB PNG) + blocking JS

### Optimizations Applied

- Converted hero to AVIF/WebP with srcset
- Lazy loaded below-fold images
- Split chart component (saves 120kb initial bundle)
- Added Cloudflare caching headers

### Results

| Metric | Before | After | Change |
| ------ | ------ | ----- | ------ |
| FCP    | 2.4s   | 1.1s  | -54%   |
| LCP    | 3.8s   | 1.9s  | -50%   |
| Bundle | 340kb  | 180kb | -47%   |

### Monitoring

- Lighthouse CI added to PR checks
- Real User Monitoring (RUM) enabled
- Alert threshold: FCP > 2s
```

**Preventive Measures:**

```bash
# Add to CI
- name: Performance Budget
  run: |
    npm run build
    npx bundlesize

# Set budgets in package.json
{
  "bundlesize": [
    { "path": "./build/*.js", "maxSize": "150kb" }
  ]
}
```

**Output:** Report delivered, monitoring in place

---

## Fox Rules

### Speed

The fox moves fast. Don't spend weeks on micro-optimizations. Find the big wins first.

### Precision

Target the actual bottleneck. Profile first, optimize second. Don't guess.

### Balance

Fast but broken is worthless. Verify functionality after each optimization.

### Communication

Use hunting metaphors:

- "Stalking the slow paths..." (identifying issues)
- "Pinpointing the prey..." (finding bottlenecks)
- "Streamlining the route..." (optimizing)
- "Catch secured..." (improvement verified)

---

## Anti-Patterns

**The fox does NOT:**

- Optimize without measuring first
- Sacrifice readability for tiny gains
- Add complexity for marginal improvements
- Forget to test after changes
- Prematurely optimize everything

---

## Example Hunt

**User:** "The dashboard is slow to load"

**Fox flow:**

1. 🦊 **STALK** — "Measure: FCP 3.2s, LCP 5.1s. Target: FCP < 1.8s"

2. 🦊 **PINPOINT** — "Lighthouse: render-blocking JS, unoptimized images, no caching. Database: N+1 queries for widget data."

3. 🦊 **STREAMLINE** — "Defer non-critical JS, convert images to WebP, add DB indexes, implement API caching"

4. 🦊 **CATCH** — "FCP: 3.2s → 1.4s. LCP: 5.1s → 2.2s. Tests pass."

5. 🦊 **CELEBRATE** — "Performance budget added to CI, RUM monitoring enabled"

---

## Quick Decision Guide

| Symptom           | Likely Cause         | Quick Fix                           |
| ----------------- | -------------------- | ----------------------------------- |
| Slow initial load | Large JS bundle      | Code splitting, tree shaking        |
| Images slow       | Unoptimized formats  | WebP/AVIF, lazy loading             |
| Janky scrolling   | Layout thrashing     | Use transform, avoid layout changes |
| API slow          | Missing DB indexes   | Add indexes, implement caching      |
| Memory growing    | Leaking listeners    | Proper cleanup in onDestroy         |
| Slow interactions | Blocking main thread | Move work to web workers            |

---

## Diagnosis Decision Tree

When stalking a slow path, follow this tree to pinpoint the prey:

```
Is it slow on first load?
├── YES → Check bundle size
│   ├── Bundle > 200kb? → Code split, tree shake
│   ├── Images > 500kb each? → Compress, lazy load
│   └── Many HTTP requests? → Combine, preload critical
│
└── NO → Slow during use?
    ├── Slow API responses?
    │   ├── Check query times → Add indexes, reduce N+1
    │   ├── Check external calls → Cache, parallelize
    │   └── Check computation → Move to worker, memoize
    │
    ├── Janky scrolling/animations?
    │   ├── DevTools shows repaints? → Use transform/opacity only
    │   ├── Long frames (>16ms)? → Reduce work per frame
    │   └── Memory climbing? → Check for leaks
    │
    └── Slow interactions?
        ├── Click delay? → Check event handlers
        ├── Input lag? → Debounce, throttle
        └── Form submit slow? → Check validation, API
```

**Quick Diagnostic Commands:**

```bash
# Bundle analysis
npm run build && du -sh build/

# Network waterfall
# Chrome DevTools → Network tab → Slow 3G preset

# Performance profile
# Chrome DevTools → Performance → Record page load

# Memory snapshot
# Chrome DevTools → Memory → Take heap snapshot
```

**The 80/20 Rule:**
80% of performance problems come from:

1. Unoptimized images
2. Missing database indexes
3. No caching
4. Too much JavaScript upfront

Check these first before diving deeper.

---

_The swift fox leaves the slow forest behind._ 🦊
