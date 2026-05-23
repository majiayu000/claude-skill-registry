---
name: performance
description: Comprehensive performance specialist covering analysis, optimization,
  load testing, and framework-specific performance. Use when identifying bottlenecks,
  optimizing code, conducting load tests, analyzing Core Web Vitals, fixing memory
  leaks, or improving application performance across all layers (application, database,
  frontend). Includes React-specific optimization patterns.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# Performance

This skill provides comprehensive performance capabilities including performance analysis, optimization, load testing, stress testing, capacity planning, and framework-specific performance patterns.

## When to Use This Skill

- When identifying performance bottlenecks
- When investigating memory leaks or high memory usage
- When optimizing slow database queries
- When analyzing frontend performance (Core Web Vitals, bundle size)
- When setting up performance monitoring
- When conducting performance audits before deployment
- When creating load test scenarios
- When analyzing performance under stress
- When identifying system bottlenecks under load
- When planning capacity
- When setting up performance benchmarks
- When optimizing React rendering performance
- When reducing bundle size
- When improving Core Web Vitals (LCP, FID, CLS)
- When fixing memory leaks in React apps
- When implementing advanced React patterns

## What This Skill Does

1. **Performance Profiling**: Analyzes CPU, memory, and network performance
2. **Bottleneck Identification**: Pinpoints specific performance issues
3. **Memory Analysis**: Detects memory leaks and high memory usage
4. **Database Optimization**: Identifies slow queries and optimization opportunities
5. **Frontend Analysis**: Analyzes bundle size, rendering performance, Core Web Vitals
6. **Load Testing**: Creates and executes load test scenarios
7. **Stress Testing**: Identifies breaking points and limits
8. **Capacity Planning**: Analyzes scalability and capacity
9. **React Optimization**: Optimizes React rendering, bundle size, and Core Web Vitals
10. **Monitoring Setup**: Creates performance monitoring and alerting

## How to Use

### Analyze Performance

```
Analyze the performance of this application and identify bottlenecks
```

```
Profile the memory usage and find any leaks
```

### Create Load Tests

```
Create load test scenarios for this API
```

```
Test performance under 1000 concurrent users
```

### Optimize React Apps

```
Optimize this React app for better performance
```

```
Analyze bundle size and reduce it
```

## Analysis Areas

### Application Performance

**Metrics to Track:**

- Response times and latency
- Throughput (requests per second)
- Error rates
- CPU utilization
- Memory usage patterns

**Common Issues:**

- Slow API endpoints
- High CPU usage
- Memory leaks
- Inefficient algorithms
- Blocking operations

### Database Performance

**Analysis Focus:**

- Slow query identification
- Missing indexes
- N+1 query problems
- Connection pool exhaustion
- Lock contention

**Tools:**

- Query execution plans (EXPLAIN ANALYZE)
- Slow query logs
- Database monitoring tools
- Connection pool metrics

### Frontend Performance

**Core Web Vitals:**

- Largest Contentful Paint (LCP) < 2.5s
- First Input Delay (FID) < 100ms
- Cumulative Layout Shift (CLS) < 0.1

**Bundle Analysis:**

- Bundle size optimization
- Code splitting opportunities
- Unused code removal
- Asset optimization

### React Performance

**Rendering Optimization:**

- React.memo for component memoization
- useMemo for expensive computations
- useCallback for function memoization
- Virtualization for long lists
- Code splitting and lazy loading

**Bundle Optimization:**

- Code splitting by route
- Component lazy loading
- Tree shaking unused code
- Dynamic imports
- Bundle analysis

## Performance Testing

### Load Testing

**Purpose**: Test system under expected load
**Metrics**: Response time, throughput, error rate
**Tools**: k6, Artillery, JMeter, Locust

**Example (k6):**

```javascript
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Stay at 100
    { duration: '2m', target: 200 }, // Ramp up to 200
    { duration: '5m', target: 200 }, // Stay at 200
    { duration: '2m', target: 0 },   // Ramp down
  ],
};

export default function() {
  const res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
```

### Stress Testing

**Purpose**: Find breaking points
**Metrics**: Maximum capacity, failure points
**Approach**: Gradually increase load until failure

### Capacity Planning

**Purpose**: Determine resource needs
**Metrics**: Resource utilization, scaling requirements
**Analysis**: Current capacity vs. future needs

## Analysis Process

### 1. Establish Baseline

**Measure Current Performance:**

- Response time percentiles (p50, p90, p95, p99)
- Throughput metrics
- Error rates
- Resource utilization (CPU, memory, network)

**Set Targets:**

- Define acceptable performance thresholds
- Set SLA targets
- Identify critical paths

### 2. Identify Bottlenecks

**Profiling Techniques:**

- CPU profiling to find hot functions
- Memory profiling to find leaks
- Network analysis for API calls
- Database query analysis

**Bottleneck Patterns:**

- Single slow operation (algorithmic complexity)
- Many small operations (N+1 queries)
- Resource contention (locks, connection pools)
- Memory leaks (gradual growth)

### 3. Analyze Root Cause

**Investigation Steps:**

1. Identify the slow operation
2. Measure its performance
3. Analyze why it's slow
4. Check for optimization opportunities
5. Verify the fix improves performance

### 4. Provide Optimization Recommendations

**Recommendations Should Include:**

- Specific code changes
- Before/after performance metrics
- Implementation steps
- Expected impact
- Risk assessment

## Examples

### Example 1: API Performance Analysis

**Input**: API endpoint `/api/users` is slow

**Output**:

```markdown
## Performance Analysis: /api/users

### Current Performance
- **Average Response Time**: 2.3s
- **P95 Response Time**: 4.1s
- **Throughput**: 45 req/s
- **Error Rate**: 2%

### Bottleneck Identified
**Issue**: N+1 query problem in user data fetching
- **Location**: `src/routes/users.js:34`
- **Pattern**: One query for users, then N queries for each user's posts

### Root Cause
```javascript
// Current implementation
const users = await db.users.findAll();
for (const user of users) {
  user.posts = await db.posts.findByUserId(user.id); // N+1 queries
}
```

### Optimization

```javascript
// Optimized with eager loading
const users = await db.users.findAll({
  include: [{ model: Post, as: 'posts' }] // Single query with JOIN
});
```

### Expected Impact

- **Response Time**: 2.3s → 0.3s (87% improvement)
- **Database Queries**: 101 → 1 (99% reduction)
- **Throughput**: 45 → 200+ req/s

```

### Example 2: React Component Optimization

**Input**: Optimize expensive component

**Output**:
```markdown
## React Performance: Component Optimization

### Issue
Component re-renders on every parent update, even when props haven't changed.

### Optimization
```javascript
// Before: Re-renders unnecessarily
function ExpensiveComponent({ data, config }) {
  const processed = data
    .filter(item => item.active)
    .map(item => processComplex(item, config));

  return <Chart data={processed} />;
}

// After: Memoized to prevent unnecessary re-renders
const ExpensiveComponent = React.memo(({ data, config }) => {
  const processed = useMemo(() => {
    return data
      .filter(item => item.active)
      .map(item => processComplex(item, config));
  }, [data, config]);

  return <Chart data={processed} />;
});
```

### Impact

- Re-renders reduced: 100% → 5%
- Performance improvement: 80% faster

```

## Reference Files

For framework-specific performance patterns and detailed guidance, load reference files as needed:

- **`references/framework_patterns.md`** - Performance patterns for Node.js, React, databases, APIs, frontend, and monitoring strategies (from performance-analysis)
- **`references/react_patterns.md`** - React-specific performance optimization patterns, memoization strategies, bundle optimization, and Core Web Vitals improvements
- **`references/load_testing.md`** - Load testing and stress testing patterns, tools, scenarios, and capacity planning strategies
- **`references/PERFORMANCE_ANALYSIS.template.md`** - Performance analysis report template with load profiles, bottlenecks, and recommendations

When analyzing performance for specific frameworks or conducting load tests, load the appropriate reference file.

## Best Practices

### Performance Analysis Approach

1. **Measure First**: Always establish baseline metrics
2. **Profile Before Optimizing**: Identify actual bottlenecks
3. **Optimize Incrementally**: Make one change at a time
4. **Verify Improvements**: Measure after each optimization
5. **Monitor Continuously**: Set up ongoing performance monitoring

### Common Optimizations

**Application:**
- Optimize algorithms (reduce complexity)
- Add caching layers
- Use connection pooling
- Implement request batching
- Add rate limiting

**Database:**
- Add appropriate indexes
- Optimize queries (avoid N+1)
- Use query result caching
- Implement read replicas
- Optimize connection pooling

**Frontend:**
- Code splitting and lazy loading
- Image optimization
- Bundle size reduction
- Minimize re-renders
- Optimize asset loading

**React:**
- Measure before optimizing
- Memoize strategically (don't over-memoize)
- Code split by route and feature
- Lazy load components on demand
- Monitor performance metrics

### Monitoring Setup

**Key Metrics:**
- Response time percentiles
- Error rates
- Throughput
- Resource utilization
- Custom business metrics

**Alerting:**
- Alert on performance degradation
- Alert on error rate spikes
- Alert on resource exhaustion
- Alert on SLA violations

## Related Use Cases

- Performance audits
- Optimization projects
- Capacity planning
- Performance regression detection
- Production performance monitoring
- Load testing analysis
- React app optimization
- Bundle size reduction
- Core Web Vitals improvement
- Memory leak fixes
- Rendering performance optimization
