---
name: Knack Cache Optimizer
description: Caches API results and enforces Knack's 10-requests-per-second rate limit. Critical for dashboard performance and cost reduction.
allowed-tools: Read, Edit
---

# Knack Cache Optimizer

## Purpose
Caches API results and enforces Knack's 10-requests-per-second rate limit. Critical for dashboard performance and cost reduction.

## Core Constraint
**Knack Rate Limit**: 10 requests/second = 100ms minimum between requests

## Cache Strategy

### What to Cache
1. **Frequently accessed data**: Dashboard metrics, dropdown options
2. **Slow queries**: Paginated full datasets (3,500+ laptops)
3. **Computed aggregates**: County totals, quarterly summaries
4. **Static reference data**: County lists, status options

### What NOT to Cache
1. **User-specific data**: Individual training registrations
2. **Real-time critical data**: Live donation notifications
3. **Sub-second updates**: Active editing sessions

## Core Functions

### cache_results
**Purpose**: Store API response with TTL (time-to-live)

**Parameters**:
- `data_key` (string, required): Unique identifier for cached data
- `data_value` (object, required): Data to cache
- `ttl_seconds` (integer, optional): Cache lifetime (default: 300 = 5 minutes)

**Example**:
```javascript
// Cache all laptops for 5 minutes
const laptops = await fetch_all_pages("object_1");
cache_results({
  data_key: "all_laptops",
  data_value: laptops,
  ttl_seconds: 300
});
```

**Implementation**:
```javascript
const cache = new Map();

function cache_results({ data_key, data_value, ttl_seconds = 300 }) {
  const expiry = Date.now() + (ttl_seconds * 1000);
  cache.set(data_key, {
    data: data_value,
    expiry: expiry
  });
}

function get_cached(data_key) {
  const cached = cache.get(data_key);

  if (!cached) return null;

  if (Date.now() > cached.expiry) {
    cache.delete(data_key);
    return null;
  }

  return cached.data;
}
```

### get_or_fetch
**Purpose**: Check cache first, fetch if miss

**Example**:
```javascript
const laptops = await get_or_fetch({
  data_key: "all_laptops",
  fetch_function: async () => await fetch_all_pages("object_1"),
  ttl_seconds: 300
});
```

**Logic**:
```javascript
async function get_or_fetch({ data_key, fetch_function, ttl_seconds }) {
  const cached = get_cached(data_key);

  if (cached) {
    console.log(`Cache HIT: ${data_key}`);
    return cached;
  }

  console.log(`Cache MISS: ${data_key}, fetching...`);
  const data = await fetch_function();
  cache_results({ data_key, data_value: data, ttl_seconds });

  return data;
}
```

### invalidate_cache
**Purpose**: Clear specific or all cached data

**Example**:
```javascript
// Invalidate specific cache entry
invalidate_cache("all_laptops");

// Clear all cache
invalidate_all_cache();
```

### handle_rate_limits
**Purpose**: Enforce 10 req/sec limit with auto-retry

**Implementation**:
```javascript
class RateLimiter {
  constructor(requests_per_second = 10) {
    this.delay = 1000 / requests_per_second; // 100ms for 10 req/s
    this.last_request = 0;
  }

  async throttle() {
    const now = Date.now();
    const time_since_last = now - this.last_request;

    if (time_since_last < this.delay) {
      const wait = this.delay - time_since_last;
      await sleep(wait);
    }

    this.last_request = Date.now();
  }
}

const limiter = new RateLimiter(10);

async function rate_limited_fetch(object_key) {
  await limiter.throttle();
  return await get_records(object_key);
}
```

### exponential_backoff
**Purpose**: Retry failed requests with increasing delays

**Example**:
```javascript
const data = await exponential_backoff(async () => {
  return await get_records("object_1");
}, {
  max_retries: 3,
  initial_delay: 1000 // Start with 1 second
});
```

**Implementation**:
```javascript
async function exponential_backoff(fn, { max_retries = 3, initial_delay = 1000 }) {
  for (let i = 0; i < max_retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429) {
        const delay = initial_delay * Math.pow(2, i);
        console.warn(`Rate limit hit, retrying in ${delay}ms...`);
        await sleep(delay);
      } else {
        throw error;
      }
    }
  }
  throw new Error("Max retries exceeded");
}
```

## HTI-Specific Cache Patterns

### Dashboard Metrics (5-minute TTL)
```javascript
// Cache county breakdown
const county_totals = await get_or_fetch({
  data_key: "county_breakdown",
  fetch_function: async () => {
    const all = await fetch_all_pages("object_1");
    return groupBy(all, "county");
  },
  ttl_seconds: 300
});
```

### Quarterly Reports (1-hour TTL)
```javascript
// Cache quarterly data once generated
const q1_report = await get_or_fetch({
  data_key: "q1_2025_report",
  fetch_function: async () => await generate_quarterly_report("Q1", "2025"),
  ttl_seconds: 3600 // 1 hour
});
```

### Reference Data (24-hour TTL)
```javascript
// Cache static lists
const counties = await get_or_fetch({
  data_key: "county_list",
  fetch_function: async () => await get_records("object_counties"),
  ttl_seconds: 86400 // 24 hours
});
```

### Real-Time Critical (30-second TTL)
```javascript
// Short TTL for near-real-time data
const ready_devices = await get_or_fetch({
  data_key: "ready_devices",
  fetch_function: async () => {
    return await get_records("object_1", {
      filters: { status: "Ready for Donation" }
    });
  },
  ttl_seconds: 30
});
```

## Cache Storage Options

### 1. In-Memory (Development)
```javascript
const cache = new Map();
// Pros: Fast, simple
// Cons: Lost on restart, not shared across instances
```

### 2. Redis (Production)
```javascript
import Redis from 'ioredis';
const redis = new Redis(process.env.REDIS_URL);

async function cache_results({ data_key, data_value, ttl_seconds }) {
  await redis.setex(data_key, ttl_seconds, JSON.stringify(data_value));
}

async function get_cached(data_key) {
  const cached = await redis.get(data_key);
  return cached ? JSON.parse(cached) : null;
}
```

### 3. Vercel KV (Serverless)
```javascript
import { kv } from '@vercel/kv';

async function cache_results({ data_key, data_value, ttl_seconds }) {
  await kv.set(data_key, data_value, { ex: ttl_seconds });
}

async function get_cached(data_key) {
  return await kv.get(data_key);
}
```

## Cache Invalidation Strategies

### Time-Based (TTL)
```javascript
// Automatic expiration after TTL
cache_results({
  data_key: "laptops",
  data_value: data,
  ttl_seconds: 300 // Expires in 5 minutes
});
```

### Event-Based (Webhooks)
```javascript
// Invalidate when Knack data changes
register_webhook({
  trigger: "record_updated",
  object_key: "object_1",
  url: "/api/cache-invalidate",
  on_receive: () => {
    invalidate_cache("all_laptops");
    invalidate_cache("county_breakdown");
  }
});
```

### Manual Refresh
```javascript
// User-triggered refresh
app.post('/api/refresh-cache', async (req, res) => {
  invalidate_cache("all_laptops");
  const fresh = await fetch_all_pages("object_1");
  cache_results({ data_key: "all_laptops", data_value: fresh });
  res.json({ refreshed: true });
});
```

## Performance Metrics

### Cache Hit Rate
```javascript
let hits = 0;
let misses = 0;

function get_cached(data_key) {
  const cached = cache.get(data_key);

  if (cached && Date.now() < cached.expiry) {
    hits++;
    return cached.data;
  }

  misses++;
  return null;
}

function cache_hit_rate() {
  const total = hits + misses;
  return total > 0 ? (hits / total) * 100 : 0;
}

console.log(`Cache hit rate: ${cache_hit_rate().toFixed(1)}%`);
```

### API Cost Savings
```javascript
// Track API calls saved by caching
let api_calls_saved = 0;

async function get_or_fetch({ data_key, fetch_function }) {
  const cached = get_cached(data_key);

  if (cached) {
    api_calls_saved++;
    console.log(`API calls saved: ${api_calls_saved}`);
    return cached;
  }

  return await fetch_function();
}
```

## Monitoring

### Cache Statistics
```javascript
function cache_stats() {
  return {
    size: cache.size,
    hit_rate: cache_hit_rate(),
    api_calls_saved: api_calls_saved,
    memory_usage: process.memoryUsage().heapUsed
  };
}

// Log every 5 minutes
setInterval(() => {
  console.log("Cache stats:", cache_stats());
}, 300000);
```

## Best Practices

1. **Cache expensive operations**: Full pagination, complex filters
2. **Use appropriate TTLs**: 5min for dashboards, 1hr for reports, 24hr for static
3. **Invalidate on updates**: Use webhooks to clear stale cache
4. **Monitor hit rate**: Target >80% for dashboard queries
5. **Implement rate limiting**: Always, even with cache
6. **Handle cache failures**: Gracefully fall back to API

## Integration Points

- **knack_reader**: Wrap all get_records calls with caching
- **knack_pagination**: Cache full paginated datasets
- **knack_realtime**: Invalidate cache on webhook triggers
- **knack_dashboard_ai**: Cache computed metrics
- **knack_reporting_sync**: Cache quarterly report data

## Grant Compliance
- Reduce API costs to stay within NCDIT budget
- Improve dashboard responsiveness for stakeholder demos
- Enable offline report generation from cached data
- Log cache metrics for performance reporting
