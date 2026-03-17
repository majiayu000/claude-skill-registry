---
name: workers-performance
description: Cloudflare Workers performance optimization with CPU, memory, caching, bundle size. Use for slow workers, high latency, cold starts, or encountering CPU limits, memory issues, timeout errors.
---

# Cloudflare Workers Performance Optimization

Techniques for maximizing Worker performance and minimizing latency.

## Quick Wins

```typescript
// 1. Avoid unnecessary cloning
// ❌ Bad: Clones entire request
const body = await request.clone().json();

// ✅ Good: Parse directly when not re-using body
const body = await request.json();

// 2. Use streaming instead of buffering
// ❌ Bad: Buffers entire response
const text = await response.text();
return new Response(transform(text));

// ✅ Good: Stream transformation
return new Response(response.body.pipeThrough(new TransformStream({
  transform(chunk, controller) {
    controller.enqueue(process(chunk));
  }
})));

// 3. Cache expensive operations
const cache = caches.default;
const cached = await cache.match(request);
if (cached) return cached;
```

## Critical Rules

1. **Stay under CPU limits** - 10ms (free), 30ms (paid), 50ms (unbound)
2. **Minimize cold starts** - Keep bundles < 1MB, avoid dynamic imports
3. **Use Cache API** - Cache responses at the edge
4. **Stream large payloads** - Don't buffer entire responses
5. **Batch operations** - Combine multiple KV/D1 calls

## Top 10 Performance Errors

| Error | Symptom | Fix |
|-------|---------|-----|
| CPU limit exceeded | Worker terminated | Optimize hot paths, use streaming |
| Cold start latency | First request slow | Reduce bundle size, avoid top-level await |
| Memory pressure | Slow GC, timeouts | Stream data, avoid large arrays |
| KV latency | Slow reads | Use Cache API, batch reads |
| D1 slow queries | High latency | Add indexes, optimize SQL |
| Large bundles | Slow cold starts | Tree-shake, code split |
| Blocking operations | Request timeouts | Use Promise.all, streaming |
| Unnecessary cloning | Memory spike | Only clone when needed |
| Missing cache | Repeated computation | Implement caching layer |
| Sync operations | CPU spikes | Use async alternatives |

## CPU Optimization

### Profile Hot Paths

```typescript
async function profiledHandler(request: Request): Promise<Response> {
  const timing: Record<string, number> = {};

  const time = async <T>(name: string, fn: () => Promise<T>): Promise<T> => {
    const start = Date.now();
    const result = await fn();
    timing[name] = Date.now() - start;
    return result;
  };

  const data = await time('fetch', () => fetchData());
  const processed = await time('process', () => processData(data));
  const response = await time('serialize', () => serialize(processed));

  console.log('Timing:', timing);
  return new Response(response);
}
```

### Optimize JSON Operations

```typescript
// For large JSON, use streaming parser
import { JSONParser } from '@streamparser/json';

async function parseStreamingJSON(stream: ReadableStream): Promise<unknown[]> {
  const parser = new JSONParser();
  const results: unknown[] = [];

  parser.onValue = (value) => results.push(value);

  for await (const chunk of stream) {
    parser.write(chunk);
  }

  return results;
}
```

## Memory Optimization

### Avoid Large Arrays

```typescript
// ❌ Bad: Loads all into memory
const items = await db.prepare('SELECT * FROM items').all();
const processed = items.results.map(transform);

// ✅ Good: Process in batches
async function* batchProcess(db: D1Database, batchSize = 100) {
  let offset = 0;
  while (true) {
    const { results } = await db
      .prepare('SELECT * FROM items LIMIT ? OFFSET ?')
      .bind(batchSize, offset)
      .all();

    if (results.length === 0) break;

    for (const item of results) {
      yield transform(item);
    }
    offset += batchSize;
  }
}
```

## Caching Strategies

### Multi-Layer Cache

```typescript
interface CacheLayer {
  get(key: string): Promise<unknown | null>;
  set(key: string, value: unknown, ttl?: number): Promise<void>;
}

// Layer 1: In-memory (request-scoped)
const memoryCache = new Map<string, unknown>();

// Layer 2: Cache API (edge-local)
const edgeCache: CacheLayer = {
  async get(key) {
    const response = await caches.default.match(new Request(`https://cache/${key}`));
    return response ? response.json() : null;
  },
  async set(key, value, ttl = 60) {
    await caches.default.put(
      new Request(`https://cache/${key}`),
      new Response(JSON.stringify(value), {
        headers: { 'Cache-Control': `max-age=${ttl}` }
      })
    );
  }
};

// Layer 3: KV (global)
// Use env.KV.get/put
```

## Bundle Optimization

```typescript
// 1. Tree-shake imports
// ❌ Bad
import * as lodash from 'lodash';

// ✅ Good
import { debounce } from 'lodash-es';

// 2. Lazy load heavy dependencies
let heavyLib: typeof import('heavy-lib') | undefined;

async function getHeavyLib() {
  if (!heavyLib) {
    heavyLib = await import('heavy-lib');
  }
  return heavyLib;
}
```

## When to Load References

Load specific references based on the task:

- **Optimizing CPU usage?** → Load `references/cpu-optimization.md`
- **Memory issues?** → Load `references/memory-optimization.md`
- **Implementing caching?** → Load `references/caching-strategies.md`
- **Reducing bundle size?** → Load `references/bundle-optimization.md`
- **Cold start problems?** → Load `references/cold-starts.md`

## Templates

| Template | Purpose | Use When |
|----------|---------|----------|
| `templates/performance-middleware.ts` | Performance monitoring | Adding timing/profiling |
| `templates/caching-layer.ts` | Multi-layer caching | Implementing cache |
| `templates/optimized-worker.ts` | Performance patterns | Starting optimized worker |

## Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `scripts/benchmark.sh` | Load testing | `./benchmark.sh <url>` |
| `scripts/profile-worker.sh` | CPU profiling | `./profile-worker.sh` |

## Resources

- Performance: https://developers.cloudflare.com/workers/platform/performance/
- Limits: https://developers.cloudflare.com/workers/platform/limits/
- Caching: https://developers.cloudflare.com/workers/runtime-apis/cache/
