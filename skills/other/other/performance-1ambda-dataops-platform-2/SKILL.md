---
name: performance
description: Performance optimization and bottleneck detection. Identifies N+1 queries, memory leaks, async issues, and caching opportunities. Use when investigating slow operations, optimizing response times, or detecting performance issues.
---

# Performance

Systematic analysis focusing on queries, memory, async patterns, and caching.

## When to Use

- N+1 query detection
- Memory leak investigation
- Response time optimization
- Caching strategy design
- Async code review

## MCP Workflow

```
# 1. Search for anti-patterns
serena.search_for_pattern(
  "for.*in.*find|map.*repository",
  restrict_search_to_code_files=True
)

# 2. Analyze suspicious method
serena.find_symbol("SlowService/method", include_body=True)

# 3. Trace hot paths
serena.find_referencing_symbols("FrequentlyCalledMethod")

# 4. Past optimizations
claude-mem.search(query="performance", project="<project>")

# 5. Framework patterns
context7.get-library-docs("<framework>", topic="performance")
```

## Common Issues

### N+1 Queries
```
PROBLEM:
for item in collection:
    fetch related_data(item.id)  # N queries

SOLUTION:
ids = collection.map(item => item.id)
all_data = fetch_all_by_ids(ids)  # 1 query
lookup = create_map(all_data)
```

### Missing Pagination
```
PROBLEM: fetch_all()  # No limit

SOLUTION: fetch_paginated(page, size)
```

### Missing Caching
```
PROBLEM: get_user(id)  # Called repeatedly

SOLUTION:
@cacheable(key="user:{id}", ttl=300)
get_user(id)
```

### Blocking in Async
```
PROBLEM:
async function process():
    result = sync_blocking_call()

SOLUTION:
async function process():
    result = await async_call()
```

### Memory Leaks
```
PROBLEM:
global_cache.add(item)  # Never removed

SOLUTION:
cache = LRUCache(max_size=1000)
```

## Detection Patterns

```
# N+1 - queries in loops
serena.search_for_pattern("for.*find|map.*query|loop.*fetch")

# Unbounded fetches
serena.search_for_pattern("findAll|SELECT.*FROM.*(?!.*LIMIT)")

# Blocking in async
serena.search_for_pattern("block|wait|sleep.*async")

# Memory leaks
serena.search_for_pattern("static.*list|global.*cache")
```

## Output Format

```markdown
## Performance: [Scope]

### Metrics
| Metric | Current | Target |
|--------|---------|--------|
| p95 Latency | 500ms | <200ms |
| Throughput | 100 rps | 500 rps |

### Issues

#### 1. [Title]
**Severity:** High / Medium / Low
**Location:** `file:line`
**Type:** N+1 / Memory / Blocking

**Problem:** [description]
**Impact:** [quantified]
**Fix:** [solution]
**Improvement:** [estimate]

### Recommendations
1. **[High]** Fix N+1 queries
2. **[Medium]** Add caching
```

## Caching Strategies

| Type | Use Case | TTL |
|------|----------|-----|
| Local | Hot data, single instance | Seconds |
| Distributed | Shared, multi-instance | Minutes |
| CDN | Static assets | Hours |

### Patterns
```
# Read-through
get(key): cache.get(key) or (fetch + cache.set)

# Write-through
set(key, value): cache.set + source.save

# Invalidation
on_update(entity): cache.invalidate(entity.key)
```

## Database Optimization

```
# Select only needed columns
SELECT id, name FROM users  # Not SELECT *

# Add indexes
CREATE INDEX idx_users_email ON users(email)

# Use EXPLAIN
EXPLAIN SELECT ...

# Limit results
SELECT ... LIMIT 100

# Use joins
SELECT u.*, o.* FROM users u
JOIN orders o ON u.id = o.user_id
```

## Checklist

### Database
- [ ] No N+1 queries
- [ ] Pagination on lists
- [ ] Indexes on queried columns

### Memory
- [ ] No growing static collections
- [ ] Resources properly closed
- [ ] Cache has eviction policy

### Async
- [ ] No blocking in async
- [ ] Timeouts on external calls
- [ ] Backpressure handling
