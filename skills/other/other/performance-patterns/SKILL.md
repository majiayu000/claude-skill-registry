---
name: performance-patterns
description: Performance profiling and optimization patterns. React optimization, bundle analysis, memory leaks, API latency, database queries. Use when optimizing application performance.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Performance Patterns - Optimization Best Practices

## Purpose

Expert guidance for performance:

- **React Optimization** - Re-renders, memoization, lazy loading
- **Bundle Analysis** - Code splitting, tree shaking
- **Memory Management** - Leak detection and prevention
- **API Performance** - Latency reduction, caching
- **Database Optimization** - Query efficiency, indexing

---

## React Performance

### Prevent Unnecessary Re-renders

```typescript
// WRONG - New object on every render
<Component style={{ color: 'red' }} />

// CORRECT - Stable reference
const style = useMemo(() => ({ color: 'red' }), []);
<Component style={style} />
```

### React.memo for Pure Components

```typescript
// Memoize component that receives stable props
const UserCard = React.memo(function UserCard({ user }: { user: User }) {
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
});

// Custom comparison for complex props
const ExpensiveList = React.memo(
  function ExpensiveList({ items }: { items: Item[] }) {
    return <>{items.map(item => <Item key={item.id} {...item} />)}</>;
  },
  (prev, next) => prev.items.length === next.items.length
);
```

### useMemo for Expensive Computations

```typescript
function Analytics({ data }: { data: DataPoint[] }) {
  // Memoize expensive calculation
  const statistics = useMemo(() => {
    return {
      total: data.reduce((sum, d) => sum + d.value, 0),
      average: data.reduce((sum, d) => sum + d.value, 0) / data.length,
      max: Math.max(...data.map(d => d.value)),
    };
  }, [data]);

  return <StatsDisplay stats={statistics} />;
}
```

### useCallback for Event Handlers

```typescript
function TodoList({ todos, onToggle }: Props) {
  // Stable callback reference
  const handleToggle = useCallback((id: string) => {
    onToggle(id);
  }, [onToggle]);

  return todos.map(todo => (
    <TodoItem key={todo.id} todo={todo} onToggle={handleToggle} />
  ));
}
```

### Lazy Loading Components

```typescript
import { lazy, Suspense } from 'react';

// Lazy load heavy components
const HeavyChart = lazy(() => import('./components/HeavyChart'));
const AdminPanel = lazy(() => import('./components/AdminPanel'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <HeavyChart data={chartData} />
    </Suspense>
  );
}
```

### Virtual Lists for Large Data

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <ItemRow item={items[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Bundle Optimization

### Code Splitting

```typescript
// Route-based splitting
const routes = [
	{
		path: '/dashboard',
		component: lazy(() => import('./pages/Dashboard')),
	},
	{
		path: '/settings',
		component: lazy(() => import('./pages/Settings')),
	},
];

// Feature-based splitting
const HeavyEditor = lazy(() => import(/* webpackChunkName: "editor" */ './components/HeavyEditor'));
```

### Bundle Analysis

```bash
# Analyze bundle size
bunx vite-bundle-analyzer

# Alternative: source-map-explorer
bunx source-map-explorer dist/assets/*.js

# Check specific package size
bunx bundlephobia zod
```

### Tree Shaking

```typescript
// WRONG - Imports entire library
import _ from 'lodash';
const result = _.debounce(fn, 300);

// CORRECT - Import only what you need
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// BEST - Use native or smaller alternative
function debounce<T extends (...args: any[]) => any>(fn: T, ms: number) {
	let timeoutId: ReturnType<typeof setTimeout>;
	return (...args: Parameters<T>) => {
		clearTimeout(timeoutId);
		timeoutId = setTimeout(() => fn(...args), ms);
	};
}
```

---

## Memory Leak Prevention

### Common Leak Patterns

```typescript
// LEAK - Event listener not removed
useEffect(() => {
	window.addEventListener('resize', handleResize);
	// Missing cleanup!
}, []);

// FIXED - Proper cleanup
useEffect(() => {
	window.addEventListener('resize', handleResize);
	return () => window.removeEventListener('resize', handleResize);
}, []);
```

### Abort Controllers for Fetch

```typescript
useEffect(() => {
	const controller = new AbortController();

	async function fetchData() {
		try {
			const response = await fetch('/api/data', {
				signal: controller.signal,
			});
			const data = await response.json();
			setData(data);
		} catch (error) {
			if (error instanceof Error && error.name === 'AbortError') {
				return; // Ignore abort errors
			}
			throw error;
		}
	}

	fetchData();

	return () => controller.abort();
}, []);
```

### Closure Leaks

```typescript
// LEAK - Timer holds reference after unmount
function Component() {
	const [count, setCount] = useState(0);

	useEffect(() => {
		const id = setInterval(() => {
			setCount((c) => c + 1); // Uses stale closure
		}, 1000);
		return () => clearInterval(id); // MUST cleanup
	}, []);
}
```

### WeakMap for Object References

```typescript
// Use WeakMap to avoid holding strong references
const cache = new WeakMap<object, ComputedValue>();

function getComputed(obj: object): ComputedValue {
	if (cache.has(obj)) {
		return cache.get(obj)!;
	}
	const computed = expensiveComputation(obj);
	cache.set(obj, computed);
	return computed;
}
```

---

## API Latency Optimization

### Response Caching

```typescript
// In-memory cache with TTL
const cache = new Map<string, { data: unknown; expires: number }>();

async function cachedFetch<T>(url: string, ttl = 60000): Promise<T> {
	const cached = cache.get(url);
	if (cached && cached.expires > Date.now()) {
		return cached.data as T;
	}

	const response = await fetch(url);
	const data = await response.json();

	cache.set(url, { data, expires: Date.now() + ttl });
	return data;
}
```

### Request Deduplication

```typescript
const pending = new Map<string, Promise<Response>>();

async function dedupedFetch(url: string): Promise<Response> {
	if (pending.has(url)) {
		return pending.get(url)!;
	}

	const promise = fetch(url).finally(() => {
		pending.delete(url);
	});

	pending.set(url, promise);
	return promise;
}
```

### Parallel Requests

```typescript
// SLOW - Sequential requests
const user = await fetchUser(id);
const posts = await fetchPosts(id);
const comments = await fetchComments(id);

// FAST - Parallel requests
const [user, posts, comments] = await Promise.all([
	fetchUser(id),
	fetchPosts(id),
	fetchComments(id),
]);
```

### Response Compression

```typescript
// Enable compression in server
import compression from 'compression';
app.use(compression());

// Or in Bun
Bun.serve({
	fetch(request) {
		const response = Response.json(largeData);
		// Bun auto-compresses based on Accept-Encoding
		return response;
	},
});
```

---

## MongoDB Query Optimization

### Use Indexes

```typescript
// Create indexes for frequent queries
const userSchema = new Schema({
	email: { type: String, unique: true, index: true },
	createdAt: { type: Date, index: true },
	status: { type: String, index: true },
});

// Compound index for common query pattern
userSchema.index({ status: 1, createdAt: -1 });
```

### Avoid N+1 Queries

```typescript
// WRONG - N+1 problem
const posts = await Post.find();
for (const post of posts) {
	post.author = await User.findById(post.authorId);
}

// CORRECT - Use populate
const posts = await Post.find().populate('author');

// CORRECT - Manual batch fetch
const posts = await Post.find();
const authorIds = [...new Set(posts.map((p) => p.authorId))];
const authors = await User.find({ _id: { $in: authorIds } });
const authorMap = new Map(authors.map((a) => [a._id.toString(), a]));
posts.forEach((p) => (p.author = authorMap.get(p.authorId.toString())));
```

### Projection - Select Only Needed Fields

```typescript
// WRONG - Fetches all fields
const users = await User.find({ status: 'active' });

// CORRECT - Select only needed fields
const users = await User.find({ status: 'active' }).select('name email avatar').lean();
```

### Use .lean() for Read-Only

```typescript
// Returns plain JS objects (faster)
const users = await User.find().lean();

// vs Mongoose documents (slower, but has methods)
const users = await User.find();
```

### Aggregation Pipeline

```typescript
// Efficient aggregation
const stats = await Order.aggregate([
	{ $match: { status: 'completed' } },
	{
		$group: {
			_id: '$userId',
			totalOrders: { $sum: 1 },
			totalSpent: { $sum: '$amount' },
		},
	},
	{ $sort: { totalSpent: -1 } },
	{ $limit: 10 },
]);
```

---

## Profiling Tools

### React DevTools Profiler

```typescript
// Wrap component to profile
import { Profiler } from 'react';

function onRender(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
) {
  console.log(`${id} ${phase}: ${actualDuration.toFixed(2)}ms`);
}

<Profiler id="ExpensiveComponent" onRender={onRender}>
  <ExpensiveComponent />
</Profiler>
```

### Performance API

```typescript
// Measure operation time
performance.mark('fetch-start');
await fetchData();
performance.mark('fetch-end');

performance.measure('fetch-duration', 'fetch-start', 'fetch-end');
const measure = performance.getEntriesByName('fetch-duration')[0];
console.log(`Fetch took ${measure?.duration.toFixed(2)}ms`);
```

### MongoDB Query Explain

```bash
# In MongoDB shell
db.users.find({ email: "test@example.com" }).explain("executionStats")

# Check if using index
# "winningPlan.inputStage.stage" should be "IXSCAN" not "COLLSCAN"
```

---

## Core Web Vitals

### LCP (Largest Contentful Paint) < 2.5s

```typescript
// Preload critical resources
<link rel="preload" href="/hero-image.webp" as="image" />

// Use priority hints
<img src="/hero.webp" fetchpriority="high" />
```

### FID (First Input Delay) < 100ms

```typescript
// Break up long tasks
async function processLargeArray(items: Item[]) {
	for (let i = 0; i < items.length; i += 100) {
		const chunk = items.slice(i, i + 100);
		await processChunk(chunk);
		// Yield to main thread
		await new Promise((r) => setTimeout(r, 0));
	}
}
```

### CLS (Cumulative Layout Shift) < 0.1

```typescript
// Always set dimensions on images
<img src="/photo.jpg" width={800} height={600} alt="Photo" />

// Use aspect-ratio CSS
<div style={{ aspectRatio: '16/9' }}>
  <img src="/video-thumb.jpg" />
</div>
```

---

## Agent Integration

This skill is used by:

- **performance-profiler** agent
- **bundle-analyzer** agent
- **memory-leak-detector** agent
- **api-latency-analyzer** agent
- **query-optimizer** agent
- **render-optimizer** agent

---

## FORBIDDEN

1. **Premature optimization** - Measure first, optimize second
2. **Missing cleanup in useEffect** - Always return cleanup function
3. **N+1 queries** - Use batch fetching or populate
4. **Fetching all fields** - Use projection/select
5. **Blocking main thread** - Use web workers for heavy computation
6. **Ignoring Core Web Vitals** - Monitor LCP, FID, CLS

---

## Version

- **v1.0.0** - Initial implementation based on 2024-2025 performance patterns
