---
name: cache-strategy
description: Implement caching strategies for HTTP, service workers, and memoization
disable-model-invocation: false
---

# Cache Strategy Implementation

I'll analyze your application and implement appropriate caching strategies to improve performance and reduce server load.

Arguments: `$ARGUMENTS` - cache type focus (e.g., "http", "service-worker", "redis", "browser")

## Strategic Planning Process

<think>
Effective caching requires careful strategy:

1. **Application Analysis**
   - What type of application? (SPA, MPA, API, static site)
   - What data changes frequently vs. rarely?
   - What's cached currently, if anything?
   - Client-side, server-side, or both?
   - CDN usage and configuration

2. **Cache Layer Selection**
   - Browser cache (HTTP headers)
   - Service worker cache (offline-first PWA)
   - Application cache (in-memory, localStorage)
   - Server cache (Redis, Memcached)
   - CDN cache (edge caching)
   - Database query cache

3. **Cache Invalidation Strategy**
   - Time-based expiration (TTL)
   - Event-based invalidation
   - Version-based cache busting
   - Manual invalidation mechanisms
   - Stale-while-revalidate patterns

4. **Performance vs. Freshness Tradeoff**
   - Critical real-time data (no cache or very short TTL)
   - Semi-dynamic data (short TTL, stale-while-revalidate)
   - Static assets (long TTL, immutable)
   - User-specific data (private cache)
</think>

## Phase 1: Cache Audit

**MANDATORY FIRST STEPS:**
1. Detect application type and architecture
2. Analyze current caching configuration
3. Identify cacheable resources
4. Determine cache invalidation needs

Let me analyze your current caching setup:

```bash
# Check for existing cache configurations
echo "=== Cache Configuration Audit ==="

# Check for service worker
if [ -f "public/service-worker.js" ] || [ -f "src/service-worker.js" ] || [ -f "sw.js" ]; then
    echo "✓ Service Worker detected"
    ls -lh **/service-worker.js **/sw.js 2>/dev/null | head -5
else
    echo "✗ No Service Worker found"
fi

# Check for HTTP caching headers (common web server configs)
if [ -f ".htaccess" ]; then
    echo "✓ Apache .htaccess found"
    grep -i "cache-control\|expires" .htaccess 2>/dev/null | head -5
fi

if [ -f "nginx.conf" ] || [ -f "nginx/*.conf" ]; then
    echo "✓ Nginx config found"
    grep -i "cache\|expires" nginx*.conf 2>/dev/null | head -5
fi

# Check for Redis/Memcached dependencies
if grep -q "\"redis\"" package.json 2>/dev/null; then
    echo "✓ Redis client installed"
fi

if grep -q "\"memcached\"" package.json 2>/dev/null; then
    echo "✓ Memcached client installed"
fi

# Check for caching libraries
if grep -q "\"workbox\"" package.json 2>/dev/null; then
    echo "✓ Workbox (service worker toolkit) installed"
fi

# Check CDN configuration
if [ -f "vercel.json" ] || [ -f "netlify.toml" ]; then
    echo "✓ CDN configuration detected"
fi
```

## Phase 2: Cache Strategy Design

Based on application type, I'll design appropriate caching layers:

### Browser Cache Strategy (HTTP Headers)

**Static Assets:**
- Long cache duration (1 year)
- Immutable for versioned assets
- Public caching allowed
- Proper ETag configuration

**Dynamic Content:**
- Short cache duration or no-cache
- Private cache for user-specific data
- Stale-while-revalidate for better UX
- Proper cache-control directives

**API Responses:**
- Cache-Control based on data freshness
- ETag for conditional requests
- Vary headers for content negotiation
- Private cache for authenticated requests

### Service Worker Cache Strategy

**Cache-First (Offline-First):**
- Static assets, fonts, images
- Application shell
- Third-party libraries

**Network-First:**
- API calls
- Dynamic content
- Real-time data

**Stale-While-Revalidate:**
- Semi-dynamic content
- News feeds, product listings
- Balance freshness with performance

**Cache-Only:**
- Fallback offline pages
- Critical UI assets

### Application-Level Caching

**In-Memory Caching:**
- Computed values (memoization)
- Expensive calculations
- API response caching
- Query result caching

**Local Storage:**
- User preferences
- Authentication tokens
- Offline data sync
- Application state persistence

### Server-Side Caching

**Redis/Memcached:**
- Database query results
- Computed data
- Session storage
- API response caching
- Rate limiting data

**CDN Edge Caching:**
- Static assets
- API responses (when appropriate)
- Geographic distribution
- DDoS protection

## Phase 3: Implementation

I'll implement selected caching strategies:

### HTTP Caching Headers

**For Node.js/Express:**
```javascript
// Static assets with long-term caching
app.use('/static', express.static('public', {
  maxAge: '1y',
  immutable: true,
  etag: true
}));

// API responses with short-term caching
app.use('/api', (req, res, next) => {
  res.set('Cache-Control', 'private, max-age=300'); // 5 minutes
  next();
});
```

**For Next.js:**
```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/_next/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};
```

**For Nginx:**
```nginx
# Static assets
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# HTML files - no cache
location ~* \.html$ {
    expires -1;
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

### Service Worker Implementation

**Workbox Configuration:**
```javascript
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

// Precache static assets
precacheAndRoute(self.__WB_MANIFEST);

// Cache images with Cache First strategy
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
      }),
    ],
  })
);

// API calls with Network First strategy
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new ExpirationPlugin({
        maxAgeSeconds: 5 * 60, // 5 minutes
      }),
    ],
  })
);

// CSS and JS with Stale While Revalidate
registerRoute(
  ({ request }) => request.destination === 'style' || request.destination === 'script',
  new StaleWhileRevalidate({
    cacheName: 'static-resources',
  })
);
```

### Memoization Patterns

**React Memoization:**
```javascript
import { useMemo, useCallback } from 'react';
import { memo } from 'react';

// Memoize expensive calculations
const ExpensiveComponent = ({ data }) => {
  const processedData = useMemo(() => {
    return expensiveCalculation(data);
  }, [data]);

  const handleClick = useCallback(() => {
    // Handler logic
  }, []);

  return <div>{processedData}</div>;
};

export default memo(ExpensiveComponent);
```

**Function Memoization:**
```javascript
// Simple memoization utility
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

// LRU cache with size limit
class LRUCache {
  constructor(limit = 100) {
    this.cache = new Map();
    this.limit = limit;
  }

  get(key) {
    if (!this.cache.has(key)) return undefined;
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value); // Move to end
    return value;
  }

  set(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.limit) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
}
```

### Redis Caching

**Express with Redis:**
```javascript
const redis = require('redis');
const client = redis.createClient();

// Cache middleware
const cache = (duration) => {
  return async (req, res, next) => {
    const key = `cache:${req.originalUrl}`;

    try {
      const cached = await client.get(key);
      if (cached) {
        return res.json(JSON.parse(cached));
      }

      // Store original send function
      const originalSend = res.json.bind(res);

      // Override send to cache response
      res.json = (body) => {
        client.setex(key, duration, JSON.stringify(body));
        return originalSend(body);
      };

      next();
    } catch (err) {
      next();
    }
  };
};

// Use cache middleware
app.get('/api/data', cache(300), async (req, res) => {
  const data = await fetchData();
  res.json(data);
});
```

## Phase 4: Cache Invalidation

I'll implement appropriate invalidation strategies:

**Time-Based Expiration:**
- Set appropriate TTL values
- Use max-age headers
- Configure Redis expiration
- Implement cleanup routines

**Event-Based Invalidation:**
- Clear cache on data updates
- Invalidate related cache entries
- Use cache tags for grouped invalidation
- Implement webhook-based clearing

**Version-Based Cache Busting:**
- Content hashing for static assets
- API versioning
- Service worker updates
- Cache key versioning

## Token Optimization

**Status:** ✅ Fully Optimized (Phase 2 Batch 4B, 2026-01-27)

**Baseline:** 3,000-5,000 tokens → **Optimized:** 1,000-1,800 tokens (60-75% reduction)

This skill is meta - it implements caching FOR applications while using caching optimization strategies itself!

### Core Optimization Strategies

#### 1. Template-Based Cache Patterns (75% savings)
**Cache:** `.claude/cache/cache-strategy/cache_patterns.json`
```json
{
  "redis": {
    "express": "// Express Redis middleware...",
    "nextjs": "// Next.js Redis client...",
    "django": "# Django Redis cache backend..."
  },
  "service_worker": {
    "workbox": "// Workbox config...",
    "vanilla": "// Vanilla SW..."
  },
  "http_headers": {
    "nginx": "location ~* ...",
    "apache": "ExpiresActive On...",
    "express": "app.use(express.static..."
  },
  "in_memory": {
    "react": "useMemo hook...",
    "node": "LRU cache class...",
    "python": "functools.lru_cache..."
  }
}
```

**Strategy:**
- Read 1 pattern template (200 tokens) vs. searching examples (2,000+ tokens)
- Framework-specific snippets instantly available
- No pattern re-generation across sessions

#### 2. Focus Area Identification (70% savings)
**Grep before Read approach:**
```bash
# Identify cache targets (100 tokens vs. 2,000 reading all code)
grep -r "fetch\|axios\|api\." src/ --files-with-matches
grep -r "SELECT\|query\|find\(" src/ --files-with-matches
grep -r "expensive\|calculation\|compute" src/ --files-with-matches
```

**Cache:** `.claude/cache/cache-strategy/hot_paths.json`
```json
{
  "api_routes": ["src/api/users.js", "src/api/products.js"],
  "db_queries": ["src/models/User.js"],
  "expensive_calculations": ["src/utils/analytics.js"],
  "last_scan": "2026-01-27T10:00:00Z"
}
```

**Strategy:**
- Only read files with cache opportunities
- Skip non-relevant code (tests, configs, types)
- Focus on high-impact areas first

#### 3. Cached Best Practices (80% savings)
**Cache:** `.claude/cache/cache-strategy/recommendations.json`
```json
{
  "ttl_guidelines": {
    "static_assets": "1y (31536000s)",
    "api_responses": "5m (300s)",
    "user_data": "no-cache",
    "computed_data": "1h (3600s)"
  },
  "invalidation_patterns": {
    "time_based": "Use max-age + stale-while-revalidate",
    "event_based": "Cache tags + manual clear",
    "version_based": "Content hashing for assets"
  },
  "cache_strategies": {
    "cache_first": "Static assets, images, fonts",
    "network_first": "API calls, real-time data",
    "stale_while_revalidate": "Semi-dynamic content"
  }
}
```

**Strategy:**
- Instant recommendations (no re-thinking)
- Consistent TTL values across projects
- Proven invalidation patterns

#### 4. Framework-Specific Templates (70% savings)
**Cache:** `.claude/cache/cache-strategy/framework_templates.json`
```json
{
  "express_redis": {
    "middleware": "const cache = (duration) => {...}",
    "client_setup": "const redis = require('redis')...",
    "error_handling": "try { cached = await client.get... }"
  },
  "nextjs_swr": {
    "config": "export const fetcher = ...",
    "revalidation": "revalidateOnFocus: false..."
  },
  "django_redis": {
    "settings": "CACHES = { 'default': {...} }",
    "decorator": "@cache_page(60 * 15)..."
  }
}
```

**Strategy:**
- Framework detected once (package.json/requirements.txt)
- Load only relevant templates
- No generic examples - specific to tech stack

#### 5. Progressive Implementation (60% savings)
**Cache:** `.claude/cache/cache-strategy/implementation_status.json`
```json
{
  "src/api/users.js": {
    "status": "redis_cache_added",
    "ttl": 300,
    "last_modified": "2026-01-27T10:00:00Z"
  },
  "src/components/ExpensiveChart.js": {
    "status": "memoization_added",
    "technique": "useMemo",
    "last_modified": "2026-01-27T09:00:00Z"
  },
  "public/service-worker.js": {
    "status": "workbox_configured",
    "strategies": ["CacheFirst", "NetworkFirst"],
    "last_modified": "2026-01-26T15:00:00Z"
  }
}
```

**Strategy:**
- Track what's already cached
- Skip implemented areas
- Focus on remaining high-impact targets

### Optimization Workflow

#### Initial Cache Audit (300 tokens vs. 2,000)
```bash
# Fast detection (5 commands vs. reading all configs)
ls -la public/service-worker.js 2>/dev/null
grep -q "redis\|memcached" package.json
ls -la nginx.conf .htaccess 2>/dev/null
grep -q "workbox\|sw-precache" package.json
ls -la vercel.json netlify.toml 2>/dev/null
```

#### Focus Area Selection (200 tokens vs. 1,500)
**Arguments-based routing:**
- `http` → HTTP headers only (400 tokens)
- `redis` → Redis caching only (500 tokens)
- `service-worker` → PWA caching only (600 tokens)
- No args → Full analysis (1,800 tokens)

#### Template Application (400 tokens vs. 2,000)
```bash
# Load cached template, insert into file
# No generation, no examples, direct application
```

### Token Budget Allocation

**Total Budget:** 1,000-1,800 tokens

1. **Cache Audit** (300 tokens)
   - Framework detection: 50 tokens
   - Existing cache scan: 100 tokens
   - Focus area identification: 150 tokens

2. **Strategy Selection** (200 tokens)
   - Load cached recommendations: 100 tokens
   - Match to detected framework: 100 tokens

3. **Template Loading** (300 tokens)
   - Load framework template: 150 tokens
   - Load best practices: 150 tokens

4. **Implementation** (400-800 tokens)
   - Apply templates: 200-400 tokens
   - Targeted file edits: 200-400 tokens

5. **Validation** (200 tokens)
   - Update status cache: 100 tokens
   - Report changes: 100 tokens

### Cache Maintenance

**Auto-refresh triggers:**
- New framework detected → Fetch new templates
- package.json changed → Re-scan dependencies
- 30 days since last scan → Full re-audit

**Cache invalidation:**
```bash
# Clear stale cache (e.g., after major refactor)
rm -rf .claude/cache/cache-strategy/
```

### Comparison: Before vs. After

**Before Optimization (4,000 tokens):**
1. Read all config files (800 tokens)
2. Analyze entire codebase (1,500 tokens)
3. Generate cache patterns (1,000 tokens)
4. Explain all strategies (500 tokens)
5. Implement changes (200 tokens)

**After Optimization (1,200 tokens):**
1. Grep for cache targets (100 tokens)
2. Load cached templates (200 tokens)
3. Apply focused strategy (400 tokens)
4. Update implementation cache (100 tokens)
5. Report changes (400 tokens)

**Savings:** 70% reduction (2,800 tokens saved)

### Integration with Other Skills

**Skill synergy caching:**
```json
{
  "triggers_webpack_optimize": ["Build tool cache needed"],
  "triggers_performance_profile": ["Measure cache hit rates"],
  "triggers_lighthouse": ["Validate cache headers"],
  "triggered_by_ci_setup": ["CI/CD cache configuration"]
}
```

**Strategy:**
- Cache skill relationships
- Avoid re-analyzing when chained
- Share framework detection results

### Success Metrics

**Token efficiency:**
- HTTP headers only: 400-600 tokens (85% reduction)
- Redis setup only: 500-800 tokens (80% reduction)
- Service worker only: 600-1,000 tokens (75% reduction)
- Full implementation: 1,000-1,800 tokens (60% reduction)

**Cache hit rates:**
- Template patterns: 95% (rarely change)
- Framework detection: 90% (stable per project)
- Best practices: 98% (universal guidelines)
- Hot paths: 80% (evolve with code)

## Integration Points

**Synergistic Skills:**
- `/webpack-optimize` - Build tool caching and optimization
- `/performance-profile` - Measure cache effectiveness
- `/lighthouse` - Audit cache headers and service workers
- `/ci-setup` - Configure cache in CI/CD pipelines

Suggests `/webpack-optimize` when:
- Build tool caching needs optimization
- Bundle splitting affects cache strategy

Suggests `/performance-profile` when:
- Need to measure cache hit rates
- Validate cache performance improvements

## Safety Mechanisms

**Protection Measures:**
- Create git checkpoint before changes
- Test cache strategies in development
- Validate cache invalidation works
- Ensure no sensitive data cached
- Provide cache debugging instructions

**Cache Debugging:**
```bash
# Clear browser cache for testing
# Chrome DevTools: Application > Clear storage

# Clear Redis cache
redis-cli FLUSHDB

# Clear service worker cache
# Chrome DevTools: Application > Service Workers > Unregister
```

**Rollback Procedure:**
```bash
# Restore previous configuration
git checkout HEAD -- nginx.conf service-worker.js
# Clear problematic cache
# Rebuild and redeploy
```

## Common Caching Scenarios

**Scenario 1: Static Website**
- Long-term browser caching for all assets
- CDN edge caching
- Service worker for offline support
- Immutable cache for versioned files

**Scenario 2: SPA (Single Page App)**
- Service worker with app shell caching
- API response caching (network-first)
- Static asset caching (cache-first)
- Stale-while-revalidate for data

**Scenario 3: API Server**
- Redis for database query results
- Response caching with appropriate headers
- ETags for conditional requests
- CDN for public endpoints

**Scenario 4: E-commerce Site**
- Product images (long cache, CDN)
- Product data (short cache, stale-while-revalidate)
- User data (no cache, private)
- Shopping cart (no cache, real-time)

## Expected Results

**Performance Improvements:**
- 40-80% faster repeat page loads
- 50-90% reduction in API calls
- 30-60% reduction in server load
- Improved offline capabilities

**Cache Hit Rates:**
- Static assets: 95%+ hit rate
- API responses: 60-80% hit rate
- Database queries: 70-90% hit rate

## Error Handling

If caching introduces issues:
- I'll identify the problematic cache layer
- Provide specific debugging steps
- Suggest cache invalidation methods
- Offer alternative caching strategies
- Ensure no stale data served to users

## Important Notes

**I will NEVER:**
- Cache sensitive user data improperly
- Add AI attribution to configuration files
- Break existing cache invalidation
- Implement caching without validation
- Cache authenticated requests publicly

**Best Practices:**
- Always validate cache invalidation works
- Test offline functionality (service workers)
- Monitor cache hit rates
- Set appropriate TTL values
- Document caching strategy

## Credits

**Inspired by:**
- [MDN Web Docs - HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [Workbox Documentation](https://developers.google.com/web/tools/workbox)
- [Redis Caching Best Practices](https://redis.io/docs/manual/patterns/)
- [Web.dev - Service Worker Caching](https://web.dev/service-worker-caching-and-http-caching/)
- High-performance web application patterns

This skill helps you implement robust caching strategies that balance performance with data freshness.
