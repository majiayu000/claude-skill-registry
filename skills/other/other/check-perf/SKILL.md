---
name: check-perf
description: Analyze code for performance issues and suggest optimizations
disable-model-invocation: true
context: fork
agent: Explore
allowed-tools: Bash(git diff*), Bash(git show*), Read, Grep, Glob
---

# Performance Analysis

Analyze code changes for performance implications and optimization opportunities.

## Scope

Review changes from: `!git diff --name-only HEAD~1` or files specified in $ARGUMENTS

## Performance Checklist

### 1. Database Operations
- [ ] **N+1 queries**: Check for loops that execute individual queries
- [ ] **Missing indexes**: Verify queries use indexed columns in WHERE/JOIN clauses
- [ ] **Large result sets**: Check for unbounded queries without LIMIT
- [ ] **Transaction scope**: Verify transactions are as short as possible
- [ ] **Connection pooling**: Ensure proper connection handling

### 2. Memory Usage
- [ ] **Large object allocation**: Check for unnecessary large arrays/objects
- [ ] **Memory leaks**: Look for unclosed connections, streams, or event listeners
- [ ] **Buffer handling**: Verify streaming for large files instead of loading into memory
- [ ] **Caching strategy**: Check if frequently accessed data could be cached

### 3. API Performance
- [ ] **Response size**: Check for over-fetching data
- [ ] **Compression**: Verify gzip is enabled for large responses
- [ ] **Pagination**: Confirm list endpoints are paginated
- [ ] **Async operations**: Check if operations can be parallelized

### 4. Algorithmic Complexity
- [ ] **Loop efficiency**: Look for O(n^2) or worse patterns
- [ ] **Data structure choice**: Verify appropriate use of Map/Set vs Array
- [ ] **Unnecessary iterations**: Check for redundant loops over same data
- [ ] **Early returns**: Verify functions exit early when possible

### 5. Caching
- [ ] **Redis usage**: Check if cacheable data is being cached
- [ ] **Cache invalidation**: Verify cache keys are invalidated on updates
- [ ] **TTL settings**: Confirm appropriate expiration times
- [ ] **Route caching**: Check if expensive endpoints use route caching

### 6. Geographic/Spatial Operations
- [ ] **PostGIS queries**: Verify spatial indexes are used
- [ ] **H3 resolution**: Check appropriate H3 resolution for use case
- [ ] **Geometry simplification**: Confirm geometries are simplified for display

### 7. Deno-Specific
- [ ] **Module loading**: Check for dynamic imports that could be static
- [ ] **Worker threads**: Consider if CPU-intensive work should use workers
- [ ] **Streaming**: Use Deno streams for file/network operations

## Metrics to Consider

| Operation | Target | Warning |
|-----------|--------|---------|
| API response time | < 200ms | > 500ms |
| Database query | < 50ms | > 200ms |
| Memory per request | < 10MB | > 50MB |
| Batch size | 100-1000 | > 10000 |

## Output Format

```markdown
## Performance Analysis Summary

**Impact Level**: [LOW | MEDIUM | HIGH]
**Files Reviewed**: X files

### Performance Issues

#### [IMPACT] Issue Title
- **File**: path/to/file.ts:line
- **Issue**: Description of the performance problem
- **Current complexity**: O(n^2) / Memory: ~XMB / Time: ~Xms
- **Suggested improvement**: How to optimize
- **Expected improvement**: X% faster / X% less memory

### Optimization Opportunities
- Optional improvements that aren't blocking

### Approved Changes
- List of changes with acceptable performance characteristics

### Benchmarks Suggested
- [ ] Specific scenarios that should be load tested
```

## Invocation

```
/check-perf                        # Review uncommitted changes
/check-perf src/pdc/services/      # Review specific directory
/check-perf --focus=database       # Focus on database operations
```
