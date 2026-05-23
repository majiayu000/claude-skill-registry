---
name: performance-auditor
description: Expert assistant for monitoring and optimizing performance in the KR92 Bible Voice project. Use when analyzing query performance, optimizing database indexes, reviewing React Query caching, monitoring AI call costs, or identifying N+1 queries.
---

# Performance Auditor

## Capabilities
- Analyze query performance
- Suggest index improvements
- Review React Query usage
- Identify expensive AI calls
- Monitor database metrics

## Performance Targets

| Operation | Target | Current |
|-----------|--------|---------|
| Single verse lookup | <20ms | Check with `EXPLAIN ANALYZE` |
| Chapter load | <50ms | Check with `EXPLAIN ANALYZE` |
| Text search | <100ms | Check with `EXPLAIN ANALYZE` |
| AI translation | <500ms | Monitor in `ai_usage_logs` |
| Page load (FCP) | <1.5s | Chrome DevTools |
| API response | <200ms | Network tab |

## Usage Examples

### Example 1: Analyze Query Performance
**User:** "Check performance of verse lookup queries"

**Assistant:**
```sql
-- Test single verse lookup performance
EXPLAIN ANALYZE
SELECT * FROM public.get_verse_by_ref(
  'John', 3, 16, 'finstlk201', 'fi'
);

-- Test chapter lookup performance
EXPLAIN ANALYZE
SELECT * FROM public.get_chapter_by_ref(
  'Genesis', 1, 'finstlk201', 'fi'
);

-- Test search performance
EXPLAIN ANALYZE
SELECT * FROM public.search_text('rakkaus', 'finstlk201', 50);

-- Check execution time statistics
SELECT
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  max_exec_time
FROM pg_stat_statements
WHERE query LIKE '%get_verse_by_ref%'
  OR query LIKE '%get_chapter_by_ref%'
  OR query LIKE '%search_text%'
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Example 2: Identify Missing Indexes
**User:** "Find queries that need indexes"

**Assistant:**
```sql
-- Check for sequential scans (potential missing indexes)
SELECT
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  seq_tup_read / NULLIF(seq_scan, 0) as avg_seq_tup_read,
  CASE
    WHEN seq_scan > idx_scan THEN 'Consider index'
    ELSE 'OK'
  END as recommendation
FROM pg_stat_user_tables
WHERE schemaname IN ('public', 'bible_schema')
ORDER BY seq_scan DESC
LIMIT 20;

-- Check index usage
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname IN ('public', 'bible_schema')
ORDER BY idx_scan ASC
LIMIT 20;

-- Suggest indexes for frequently queried columns
SELECT
  'CREATE INDEX idx_' || table_name || '_' || column_name ||
  ' ON ' || table_schema || '.' || table_name || '(' || column_name || ');' as suggested_index
FROM information_schema.columns
WHERE table_schema IN ('public', 'bible_schema')
  AND table_name IN (
    SELECT tablename
    FROM pg_stat_user_tables
    WHERE seq_scan > 1000 AND seq_scan > idx_scan
  )
  AND column_name IN ('user_id', 'verse_id', 'created_at', 'osis', 'status');
```

### Example 3: Monitor AI Call Performance
**User:** "Analyze AI call latency and costs"

**Assistant:**
```sql
-- AI performance metrics (last 7 days)
SELECT
  feature,
  ai_vendor,
  ai_model,
  COUNT(*) as call_count,
  ROUND(AVG(latency_ms), 2) as avg_latency_ms,
  ROUND(MAX(latency_ms), 2) as max_latency_ms,
  ROUND(MIN(latency_ms), 2) as min_latency_ms,
  ROUND(AVG(total_tokens), 0) as avg_tokens,
  ROUND(SUM(cost_usd), 4) as total_cost_usd,
  ROUND(AVG(cost_usd), 6) as avg_cost_per_call,
  COUNT(CASE WHEN status = 'error' THEN 1 END) as errors,
  ROUND(100.0 * COUNT(CASE WHEN status = 'error' THEN 1 END) / COUNT(*), 2) as error_rate_percent
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY feature, ai_vendor, ai_model
ORDER BY call_count DESC;

-- Slowest AI calls (last 24 hours)
SELECT
  feature,
  ai_model,
  latency_ms,
  total_tokens,
  cost_usd,
  context_ref,
  created_at,
  status,
  error_message
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '24 hours'
  AND status = 'success'
ORDER BY latency_ms DESC
LIMIT 20;

-- High-cost AI calls
SELECT
  feature,
  ai_model,
  cost_usd,
  total_tokens,
  latency_ms,
  context_ref,
  created_at
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY cost_usd DESC
LIMIT 20;

-- AI cache effectiveness (for translations)
WITH cache_stats AS (
  SELECT
    COUNT(*) as total_requests,
    COUNT(CASE WHEN source IN ('topic', 'manual') THEN 1 END) as cache_hits,
    COUNT(CASE WHEN source = 'ai' THEN 1 END) as ai_calls
  FROM bible_schema.term_translations
  WHERE created_at > NOW() - INTERVAL '30 days'
)
SELECT
  total_requests,
  cache_hits,
  ai_calls,
  ROUND(100.0 * cache_hits / total_requests, 2) as cache_hit_rate_percent,
  ROUND(100.0 * ai_calls / total_requests, 2) as ai_call_rate_percent
FROM cache_stats;
```

### Example 4: Optimize React Query Usage
**User:** "Review React Query configuration for optimal caching"

**Assistant:**

Create performance monitoring hook:
```typescript
// hooks/usePerformanceMonitor.ts
import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';

export const usePerformanceMonitor = () => {
  const queryClient = useQueryClient();

  useEffect(() => {
    // Log cache statistics
    const cache = queryClient.getQueryCache();
    const queries = cache.getAll();

    console.log('React Query Cache Stats:', {
      totalQueries: queries.length,
      activeQueries: queries.filter(q => q.state.fetchStatus === 'fetching').length,
      staleQueries: queries.filter(q => q.isStale()).length,
      cacheSize: JSON.stringify(queries).length / 1024 + ' KB'
    });

    // Monitor slow queries
    queries.forEach(query => {
      if (query.state.dataUpdateCount > 0) {
        const lastFetchTime = query.state.dataUpdatedAt - (query.state.dataUpdatedAt - 1000);
        if (lastFetchTime > 1000) {
          console.warn('Slow query detected:', {
            queryKey: query.queryKey,
            fetchTime: lastFetchTime + 'ms'
          });
        }
      }
    });
  }, [queryClient]);
};

// Usage in main component
import { usePerformanceMonitor } from '@/hooks/usePerformanceMonitor';

function App() {
  usePerformanceMonitor(); // Monitor in dev mode
  // ...
}
```

Optimize query configuration:
```typescript
// Recommended React Query configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
      refetchOnMount: false,
    },
  },
});

// Bible verses - longer cache (rarely change)
const { data: verses } = useQuery({
  queryKey: ['chapter', book, chapter, version],
  queryFn: () => fetchChapter(book, chapter, version),
  staleTime: 30 * 60 * 1000, // 30 minutes
  gcTime: 60 * 60 * 1000, // 1 hour
});

// User data - shorter cache (may change frequently)
const { data: bookmarks } = useQuery({
  queryKey: ['bookmarks', userId],
  queryFn: () => fetchBookmarks(userId),
  staleTime: 1 * 60 * 1000, // 1 minute
  gcTime: 5 * 60 * 1000, // 5 minutes
});

// AI results - cache aggressively
const { data: translation } = useQuery({
  queryKey: ['translation', term],
  queryFn: () => translateTerm(term),
  staleTime: Infinity, // Never goes stale
  gcTime: 24 * 60 * 60 * 1000, // 24 hours
});
```

### Example 5: Identify N+1 Query Problems
**User:** "Find N+1 query issues in the codebase"

**Assistant:**

Common N+1 patterns to avoid:
```typescript
// ❌ BAD: N+1 queries
const { data: topics } = useQuery(['topics'], fetchTopics);

// For each topic, fetch verses separately
topics?.forEach(topic => {
  const { data: verses } = useQuery(
    ['verses', topic.id],
    () => fetchTopicVerses(topic.id) // N queries!
  );
});

// ✅ GOOD: Single query with JOIN
const { data: topicsWithVerses } = useQuery(
  ['topics-with-verses'],
  async () => {
    const { data } = await supabase
      .from('topics')
      .select(`
        *,
        topic_verses(
          verse:verses(*)
        )
      `);
    return data;
  }
);

// ✅ BETTER: Use RPC function
const { data: topicsWithVerses } = useQuery(
  ['topics-with-verses'],
  async () => {
    const { data } = await supabase.rpc('get_topics_with_verses');
    return data;
  }
);
```

Detect N+1 in logs:
```typescript
// Add query logging in development
if (process.env.NODE_ENV === 'development') {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        onSuccess: (data, query) => {
          console.log('Query executed:', {
            queryKey: query.queryKey,
            dataSize: JSON.stringify(data).length,
            timestamp: Date.now()
          });
        }
      }
    }
  });

  // Alert on rapid sequential queries
  let queryTimes: number[] = [];
  setInterval(() => {
    if (queryTimes.length > 10) {
      console.warn('Potential N+1 detected: ', queryTimes.length, 'queries in short succession');
    }
    queryTimes = [];
  }, 1000);
}
```

## Performance Optimization Checklist

### Database
- [ ] Indexes on foreign keys
- [ ] Indexes on frequently filtered columns
- [ ] GIN indexes for full-text search
- [ ] Composite indexes for common query patterns
- [ ] VACUUM and ANALYZE run regularly
- [ ] Connection pooling configured

### React Query
- [ ] Appropriate staleTime for each query type
- [ ] No unnecessary refetches
- [ ] Prefetching for predictable navigation
- [ ] Query invalidation on mutations
- [ ] No N+1 query patterns
- [ ] Cache size monitored

### AI Calls
- [ ] Caching enabled for translations
- [ ] Appropriate model selection (cost vs performance)
- [ ] Token limits set
- [ ] Timeout handling
- [ ] Retry logic with exponential backoff
- [ ] Batch processing where possible

### Frontend
- [ ] Code splitting for routes
- [ ] Lazy loading components
- [ ] Image optimization
- [ ] Debouncing for search inputs
- [ ] Virtual scrolling for long lists
- [ ] Service worker for caching

## Monitoring Tools

### Supabase Dashboard
- Database → Performance
- Database → Query Performance
- Edge Functions → Logs

### Browser DevTools
```javascript
// Measure page load performance
window.addEventListener('load', () => {
  const perfData = performance.getEntriesByType('navigation')[0];
  console.log('Page Performance:', {
    domContentLoaded: perfData.domContentLoadedEventEnd - perfData.fetchStart,
    loadComplete: perfData.loadEventEnd - perfData.fetchStart,
    firstPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime
  });
});

// Monitor API calls
const originalFetch = window.fetch;
window.fetch = async (...args) => {
  const start = performance.now();
  const result = await originalFetch(...args);
  const duration = performance.now() - start;

  if (duration > 500) {
    console.warn('Slow API call:', {
      url: args[0],
      duration: duration.toFixed(2) + 'ms'
    });
  }

  return result;
};
```

## Related Documentation
- See `Docs/02-DESIGN.md` for architecture
- See `Docs/05-DEV.md` for query patterns
- See `Docs/06-AI-ARCHITECTURE.md` for AI optimization
