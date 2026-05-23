---
name: profiling-guide
description: >
  Profile and diagnose performance bottlenecks in web and backend applications. Activate
  whenever the user reports slow performance, asks about profiling tools, investigates
  memory leaks, needs to generate flame graphs, or is optimizing CPU or memory usage.
  Also activate when mentioning Chrome DevTools, cProfile, py-spy, pprof, or heap snapshots.
---

# Profiling Guide

Measure before optimizing. Use profiling tools to identify actual bottlenecks instead
of guessing. This guide covers profiling for JavaScript/Node.js, Python, and Go.

## When to Use
- Application or endpoint is slow and you need to find the bottleneck
- Investigating memory leaks or growing memory usage
- Optimizing hot paths in CPU-intensive code
- Generating flame graphs for visual performance analysis
- Comparing performance before and after a change

## Core Patterns

### Chrome DevTools Profiling (Frontend)

Profile rendering, JavaScript execution, and memory in the browser.

```markdown
## Performance Tab Workflow
1. Open DevTools (Cmd+Option+I / F12)
2. Go to Performance tab
3. Click Record, perform the slow action, click Stop
4. Analyze the flame chart:
   - Yellow = JavaScript execution
   - Purple = Rendering/layout
   - Green = Painting
   - Look for long tasks (>50ms, marked with red triangle)

## Key Metrics
- First Contentful Paint (FCP): < 1.8s
- Largest Contentful Paint (LCP): < 2.5s
- Total Blocking Time (TBT): < 200ms
- Cumulative Layout Shift (CLS): < 0.1

## Memory Tab Workflow
1. Go to Memory tab
2. Take Heap Snapshot
3. Perform suspected leaking action
4. Take another Heap Snapshot
5. Compare snapshots (select "Comparison" view)
6. Sort by "Delta" to find growing object counts
```

Programmatic performance measurement:

```typescript
// Measure specific operations
performance.mark('fetch-start');
const data = await fetchLargeDataset();
performance.mark('fetch-end');
performance.measure('data-fetch', 'fetch-start', 'fetch-end');

const measure = performance.getEntriesByName('data-fetch')[0];
// measure.duration gives you milliseconds

// React component profiling
import { Profiler } from 'react';

function onRenderCallback(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
) {
  if (actualDuration > 16) { // Longer than one frame at 60fps
    console.warn(`Slow render: ${id} took ${actualDuration.toFixed(2)}ms`);
  }
}

<Profiler id="UserList" onRender={onRenderCallback}>
  <UserList users={users} />
</Profiler>
```

### Node.js Profiling

Profile server-side JavaScript with built-in and third-party tools.

```bash
# Built-in V8 profiler - generates a CPU profile
node --prof app.js
# Process the log
node --prof-process isolate-*.log > profile.txt

# Generate a Chrome-compatible CPU profile
node --cpu-prof --cpu-prof-dir=./profiles app.js
# Open the .cpuprofile file in Chrome DevTools > Performance tab

# Heap snapshot for memory analysis
node --heapsnapshot-signal=SIGUSR2 app.js
# Send signal to generate snapshot: kill -USR2 <pid>
# Open .heapsnapshot in Chrome DevTools > Memory tab
```

### Python Profiling (cProfile and py-spy)

Profile Python applications with minimal overhead.

```python
# cProfile - built-in deterministic profiler
import cProfile
import pstats

# Profile a function
cProfile.run('expensive_function()', 'output.prof')

# Analyze results
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions by cumulative time

# Context manager for targeted profiling
import cProfile
import io

def profile_block():
    pr = cProfile.Profile()
    pr.enable()
    try:
        result = expensive_operation()
    finally:
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(15)
        print(s.getvalue())
    return result
```

```bash
# py-spy - sampling profiler with minimal overhead (production-safe)
pip install py-spy
py-spy top --pid 12345                          # Live top-like view
py-spy record -o flame.svg -- python app.py     # Generate flame graph
```

### Go pprof

Profile Go applications with the standard library pprof package.

```go
import (
    "net/http"
    _ "net/http/pprof" // Register pprof handlers
)

func main() {
    // Start pprof HTTP server on a separate port
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()

    // Your application code
    startApp()
}
```

```bash
# CPU profile (30-second sample)
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Heap profile (current allocations)
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine profile (find goroutine leaks)
go tool pprof http://localhost:6060/debug/pprof/goroutine

# Interactive commands inside pprof
# (pprof) top 20        # Top 20 functions by CPU/memory
# (pprof) list funcName  # Source-annotated profile for a function
# (pprof) web           # Open flame graph in browser

# Generate flame graph directly
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/profile?seconds=30
```

### Memory Leak Detection

Common patterns for finding and fixing memory leaks.

```typescript
// Node.js: Track heap usage over time
function logMemory() {
  const usage = process.memoryUsage();
  return {
    rss: Math.round(usage.rss / 1024 / 1024),       // Total memory
    heapUsed: Math.round(usage.heapUsed / 1024 / 1024), // Used heap
    heapTotal: Math.round(usage.heapTotal / 1024 / 1024), // Total heap
    external: Math.round(usage.external / 1024 / 1024),  // C++ objects
  };
}

// Common leak sources:
// 1. Event listeners not removed
// 2. Closures holding references to large objects
// 3. Growing caches without eviction
// 4. Uncleared timers/intervals
// 5. Accumulating promises

// Fix: Ensure cleanup
class ResourceManager {
  private listeners: Array<() => void> = [];

  addEventListener(target: EventEmitter, event: string, handler: Function) {
    target.on(event, handler);
    this.listeners.push(() => target.off(event, handler));
  }

  dispose() {
    this.listeners.forEach(cleanup => cleanup());
    this.listeners = [];
  }
}
```

## Anti-Patterns
- Optimizing without profiling first ("premature optimization")
- Profiling in debug mode instead of production-like configuration
- Using `console.time` for everything instead of proper profiling tools
- Taking a single measurement instead of averaging multiple runs
- Profiling with unrealistic data sizes (10 items vs 10,000 in production)
- Ignoring memory profiles and only looking at CPU
- Leaving profiling endpoints (`/debug/pprof`) exposed in production

## Quick Reference

| Language | CPU Profiler | Memory Profiler | Flame Graph |
|----------|-------------|----------------|-------------|
| JavaScript (browser) | DevTools Performance tab | DevTools Memory tab | Built into DevTools |
| Node.js | `--cpu-prof`, inspector API | `--heapsnapshot-signal` | Speedscope, 0x |
| Python | cProfile, py-spy | tracemalloc, objgraph | py-spy `record -o flame.svg` |
| Go | pprof `/profile` | pprof `/heap` | `go tool pprof -http` |

| Rule of Thumb | Threshold |
|---------------|-----------|
| API response time | < 200ms (p95) |
| Page load (LCP) | < 2.5s |
| Single frame (60fps) | < 16.67ms |
| Long task | > 50ms |
| Memory growth per request | Should stabilize, not grow linearly |
