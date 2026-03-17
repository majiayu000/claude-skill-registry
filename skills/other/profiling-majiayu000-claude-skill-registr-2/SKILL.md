---
name: profiling-optimization
description: Profile application performance, identify bottlenecks, and optimize hot paths using CPU profiling, flame graphs, and benchmarking. Use when investigating performance issues or optimizing critical code paths.
---

# Profiling & Optimization

## Overview

Profile code execution to identify performance bottlenecks and optimize critical paths using data-driven approaches.

## When to Use

- Performance optimization
- Identifying CPU bottlenecks
- Optimizing hot paths
- Investigating slow requests
- Reducing latency
- Improving throughput

## Implementation Examples

### 1. **Node.js Profiling**

```typescript
import { performance, PerformanceObserver } from 'perf_hooks';

class Profiler {
  private marks = new Map<string, number>();

  mark(name: string): void {
    this.marks.set(name, performance.now());
  }

  measure(name: string, startMark: string): number {
    const start = this.marks.get(startMark);
    if (!start) throw new Error(`Mark ${startMark} not found`);

    const duration = performance.now() - start;
    console.log(`${name}: ${duration.toFixed(2)}ms`);

    return duration;
  }

  async profile<T>(name: string, fn: () => Promise<T>): Promise<T> {
    const start = performance.now();

    try {
      return await fn();
    } finally {
      const duration = performance.now() - start;
      console.log(`${name}: ${duration.toFixed(2)}ms`);
    }
  }
}

// Usage
const profiler = new Profiler();

app.get('/api/users', async (req, res) => {
  profiler.mark('request-start');

  const users = await profiler.profile('fetch-users', async () => {
    return await db.query('SELECT * FROM users');
  });

  profiler.measure('total-request-time', 'request-start');

  res.json(users);
});
```

### 2. **Chrome DevTools CPU Profile**

```typescript
import inspector from 'inspector';
import fs from 'fs';

class CPUProfiler {
  private session: inspector.Session | null = null;

  start(): void {
    this.session = new inspector.Session();
    this.session.connect();

    this.session.post('Profiler.enable');
    this.session.post('Profiler.start');

    console.log('CPU profiling started');
  }

  async stop(outputFile: string): Promise<void> {
    if (!this.session) return;

    this.session.post('Profiler.stop', (err, { profile }) => {
      if (err) {
        console.error('Profiling error:', err);
        return;
      }

      fs.writeFileSync(outputFile, JSON.stringify(profile));
      console.log(`Profile saved to ${outputFile}`);

      this.session!.disconnect();
      this.session = null;
    });
  }
}

// Usage
const cpuProfiler = new CPUProfiler();

// Start profiling
cpuProfiler.start();

// Run code to profile
await runExpensiveOperation();

// Stop and save
await cpuProfiler.stop('./profile.cpuprofile');
```

### 3. **Python cProfile**

```python
import cProfile
import pstats
from pstats import SortKey
import io

class Profiler:
    def __init__(self):
        self.profiler = cProfile.Profile()

    def __enter__(self):
        self.profiler.enable()
        return self

    def __exit__(self, *args):
        self.profiler.disable()

    def print_stats(self, sort_by: str = 'cumulative'):
        """Print profiling statistics."""
        s = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=s)

        if sort_by == 'time':
            ps.sort_stats(SortKey.TIME)
        elif sort_by == 'cumulative':
            ps.sort_stats(SortKey.CUMULATIVE)
        elif sort_by == 'calls':
            ps.sort_stats(SortKey.CALLS)

        ps.print_stats(20)  # Top 20
        print(s.getvalue())

    def save_stats(self, filename: str):
        """Save profiling data."""
        self.profiler.dump_stats(filename)

# Usage
with Profiler() as prof:
    # Code to profile
    result = expensive_function()

prof.print_stats('cumulative')
prof.save_stats('profile.prof')
```

### 4. **Benchmarking**

```typescript
class Benchmark {
  async run(
    name: string,
    fn: () => Promise<any>,
    iterations: number = 1000
  ): Promise<void> {
    console.log(`\nBenchmarking: ${name}`);

    const times: number[] = [];

    // Warmup
    for (let i = 0; i < 10; i++) {
      await fn();
    }

    // Actual benchmark
    for (let i = 0; i < iterations; i++) {
      const start = performance.now();
      await fn();
      times.push(performance.now() - start);
    }

    // Statistics
    const sorted = times.sort((a, b) => a - b);
    const min = sorted[0];
    const max = sorted[sorted.length - 1];
    const avg = times.reduce((a, b) => a + b, 0) / times.length;
    const p50 = sorted[Math.floor(sorted.length * 0.5)];
    const p95 = sorted[Math.floor(sorted.length * 0.95)];
    const p99 = sorted[Math.floor(sorted.length * 0.99)];

    console.log(`  Iterations: ${iterations}`);
    console.log(`  Min: ${min.toFixed(2)}ms`);
    console.log(`  Max: ${max.toFixed(2)}ms`);
    console.log(`  Avg: ${avg.toFixed(2)}ms`);
    console.log(`  P50: ${p50.toFixed(2)}ms`);
    console.log(`  P95: ${p95.toFixed(2)}ms`);
    console.log(`  P99: ${p99.toFixed(2)}ms`);
  }

  async compare(
    implementations: Array<{ name: string; fn: () => Promise<any> }>,
    iterations: number = 1000
  ): Promise<void> {
    for (const impl of implementations) {
      await this.run(impl.name, impl.fn, iterations);
    }
  }
}

// Usage
const bench = new Benchmark();

await bench.compare([
  {
    name: 'Array.filter + map',
    fn: async () => {
      const arr = Array.from({ length: 1000 }, (_, i) => i);
      return arr.filter(x => x % 2 === 0).map(x => x * 2);
    }
  },
  {
    name: 'Single loop',
    fn: async () => {
      const arr = Array.from({ length: 1000 }, (_, i) => i);
      const result = [];
      for (const x of arr) {
        if (x % 2 === 0) {
          result.push(x * 2);
        }
      }
      return result;
    }
  }
]);
```

### 5. **Database Query Profiling**

```typescript
import { Pool } from 'pg';

class QueryProfiler {
  constructor(private pool: Pool) {}

  async profileQuery(query: string, params: any[] = []): Promise<{
    result: any;
    planningTime: number;
    executionTime: number;
    plan: any;
  }> {
    // Enable timing
    await this.pool.query('SET track_io_timing = ON');

    // Get query plan
    const explainResult = await this.pool.query(
      `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ${query}`,
      params
    );

    const plan = explainResult.rows[0]['QUERY PLAN'][0];

    // Execute actual query
    const start = performance.now();
    const result = await this.pool.query(query, params);
    const duration = performance.now() - start;

    return {
      result: result.rows,
      planningTime: plan['Planning Time'],
      executionTime: plan['Execution Time'],
      plan
    };
  }

  formatPlan(plan: any): string {
    let output = 'Query Plan:\n';
    output += `Planning Time: ${plan['Planning Time']}ms\n`;
    output += `Execution Time: ${plan['Execution Time']}ms\n\n`;

    const formatNode = (node: any, indent: number = 0) => {
      const prefix = '  '.repeat(indent);
      output += `${prefix}${node['Node Type']}\n`;
      output += `${prefix}  Cost: ${node['Total Cost']}\n`;
      output += `${prefix}  Rows: ${node['Actual Rows']}\n`;
      output += `${prefix}  Time: ${node['Actual Total Time']}ms\n`;

      if (node.Plans) {
        node.Plans.forEach((child: any) => formatNode(child, indent + 1));
      }
    };

    formatNode(plan.Plan);
    return output;
  }
}

// Usage
const profiler = new QueryProfiler(pool);

const { result, planningTime, executionTime, plan } = await profiler.profileQuery(
  'SELECT * FROM users WHERE age > $1',
  [25]
);

console.log(profiler.formatPlan(plan));
```

### 6. **Flame Graph Generation**

```bash
# Generate flame graph using 0x
npx 0x -o flamegraph.html node server.js

# Or using clinic.js
npx clinic doctor --on-port 'autocannon localhost:3000' -- node server.js
npx clinic flame --on-port 'autocannon localhost:3000' -- node server.js
```

## Optimization Techniques

### 1. **Caching**

```typescript
class LRUCache<K, V> {
  private cache = new Map<K, V>();
  private maxSize: number;

  constructor(maxSize: number = 100) {
    this.maxSize = maxSize;
  }

  get(key: K): V | undefined {
    if (!this.cache.has(key)) return undefined;

    // Move to end (most recently used)
    const value = this.cache.get(key)!;
    this.cache.delete(key);
    this.cache.set(key, value);

    return value;
  }

  set(key: K, value: V): void {
    // Remove if exists
    if (this.cache.has(key)) {
      this.cache.delete(key);
    }

    // Add to end
    this.cache.set(key, value);

    // Evict oldest if over capacity
    if (this.cache.size > this.maxSize) {
      const oldest = this.cache.keys().next().value;
      this.cache.delete(oldest);
    }
  }
}
```

### 2. **Lazy Loading**

```typescript
class LazyValue<T> {
  private value?: T;
  private loaded = false;

  constructor(private loader: () => T) {}

  get(): T {
    if (!this.loaded) {
      this.value = this.loader();
      this.loaded = true;
    }
    return this.value!;
  }
}

// Usage
const expensive = new LazyValue(() => {
  console.log('Computing expensive value...');
  return computeExpensiveValue();
});

// Only computed when first accessed
const value = expensive.get();
```

## Best Practices

### ✅ DO
- Profile before optimizing
- Focus on hot paths
- Measure impact of changes
- Use production-like data
- Consider memory vs speed tradeoffs
- Document optimization rationale

### ❌ DON'T
- Optimize without profiling
- Ignore readability for minor gains
- Skip benchmarking
- Optimize cold paths
- Make changes without measurement

## Tools

- **Node.js**: 0x, clinic.js, node --prof
- **Python**: cProfile, py-spy, memory_profiler
- **Visualization**: Flame graphs, Chrome DevTools
- **Database**: EXPLAIN ANALYZE, pg_stat_statements

## Resources

- [0x Flame Graph Profiler](https://github.com/davidmarkclements/0x)
- [Chrome DevTools Profiling](https://developer.chrome.com/docs/devtools/performance/)
- [Python cProfile](https://docs.python.org/3/library/profile.html)
