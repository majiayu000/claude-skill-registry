---
name: memory-optimization
description: Profile and optimize application memory usage. Identify memory leaks, reduce memory footprint, and improve efficiency for better performance and reliability.
---

# Memory Optimization

## Overview

Memory optimization improves application performance, stability, and reduces infrastructure costs. Efficient memory usage is critical for scalability.

## When to Use

- High memory usage
- Memory leaks suspected
- Slow performance
- Out of memory crashes
- Scaling challenges

## Instructions

### 1. **Memory Profiling**

```javascript
// Browser memory profiling

// Check memory usage
performance.memory: {
  jsHeapSizeLimit: 2190000000,    // Max available
  totalJSHeapSize: 1300000000,    // Total allocated
  usedJSHeapSize: 950000000       // Currently used
}

// React DevTools Profiler
- Open React DevTools → Profiler
- Record interaction
- See component renders and time
- Identify unnecessary renders

// Chrome DevTools
1. Open DevTools → Memory
2. Take heap snapshot
3. Compare before/after
4. Look for retained objects
5. Check retained sizes

// Node.js profiling
node --inspect app.js
// Open chrome://inspect
// Take heap snapshots
// Compare growth over time
```

### 2. **Memory Leak Detection**

```python
# Identify and fix memory leaks

class MemoryLeakDebug:
    def identify_leaks(self):
        """Common patterns"""
        return {
            'circular_references': {
                'problem': 'Objects reference each other, prevent GC',
                'example': 'parent.child = child; child.parent = parent',
                'solution': 'Use weak references or cleaner code'
            },
            'event_listeners': {
                'problem': 'Listeners not removed',
                'example': 'element.addEventListener(...) without removeEventListener',
                'solution': 'Always remove listeners on cleanup'
            },
            'timers': {
                'problem': 'setInterval/setTimeout not cleared',
                'example': 'setInterval(() => {}, 1000) never clearInterval',
                'solution': 'Store ID and clear on unmount'
            },
            'cache_unbounded': {
                'problem': 'Cache grows without bounds',
                'example': 'cache[key] = value (never deleted)',
                'solution': 'Implement TTL or size limits'
            },
            'dom_references': {
                'problem': 'Removed DOM elements still referenced',
                'example': 'var x = document.getElementById("removed")',
                'solution': 'Clear references after removal'
            }
        }

    def detect_in_browser(self):
        """JavaScript detection"""
        return """
// Monitor memory growth
setInterval(() => {
  const mem = performance.memory;
  const used = mem.usedJSHeapSize / 1000000;
  console.log(`Memory: ${used.toFixed(1)} MB`);
}, 1000);

// If grows over time without plateau = leak
"""
```

### 3. **Optimization Techniques**

```yaml
Memory Optimization:

Object Pooling:
  Pattern: Reuse objects instead of creating new
  Example: GameObject pool in games
  Benefits: Reduce GC, stable memory
  Trade-off: Complexity

Lazy Loading:
  Pattern: Load data only when needed
  Example: Infinite scroll
  Benefits: Lower peak memory
  Trade-off: Complexity

Pagination:
  Pattern: Process data in chunks
  Example: 1M records → 1K per page
  Benefits: Constant memory
  Trade-off: More requests

Stream Processing:
  Pattern: Process one item at a time
  Example: fs.createReadStream()
  Benefits: Constant memory for large data
  Trade-off: Slower if cached

Memoization:
  Pattern: Cache expensive calculations
  Benefits: Faster, reuse results
  Trade-off: Memory for speed

---

Framework-Specific:

React:
  - useMemo for expensive calculations
  - useCallback to avoid creating functions
  - Code splitting / lazy loading
  - Windowing for long lists (react-window)

Node.js:
  - Stream instead of loadFile
  - Limit cluster workers
  - Set heap size: --max-old-space-size=4096
  - Monitor with clinic.js

---

GC (Garbage Collection):

Minimize:
  - Object creation
  - Large allocations
  - Frequent new objects
  - String concatenation

Example (Bad):
let result = "";
for (let i = 0; i < 1000000; i++) {
  result += i.toString() + ",";
  // Creates new string each iteration
}

Example (Good):
const result = Array.from(
  {length: 1000000},
  (_, i) => i.toString()
).join(",");
// Single allocation
```

### 4. **Monitoring & Targets**

```yaml
Memory Targets:

Web App:
  Initial: <10MB
  After use: <50MB
  Peak: <100MB
  Leak check: Should plateau

Node.js API:
  Per-process: 100-500MB
  Cluster total: 1-4GB
  Heap size: Monitor vs available RAM

Mobile:
  Initial: <20MB
  Working: <50MB
  Peak: <100MB (device dependent)

---

Tools:

Browser:
  - Chrome DevTools Memory
  - Firefox DevTools Memory
  - React DevTools Profiler
  - Redux DevTools

Node.js:
  - node --inspect
  - clinic.js
  - nodemon --exec with monitoring
  - New Relic / DataDog

Monitoring:
  - Application Performance Monitoring (APM)
  - Prometheus + Grafana
  - CloudWatch
  - New Relic

---

Checklist:

[ ] Profile baseline memory
[ ] Identify heavy components
[ ] Remove event listeners on cleanup
[ ] Clear timers on cleanup
[ ] Implement lazy loading
[ ] Use pagination for large lists
[ ] Monitor memory trends
[ ] Set up GC monitoring
[ ] Test with production data volume
[ ] Stress test for leaks
[ ] Establish memory budget
[ ] Set up alerts
```

## Key Points

- Take baseline memory measurements
- Use profilers to identify issues
- Remove listeners and timers on cleanup
- Implement streaming for large data
- Use lazy loading and pagination
- Monitor GC pause times
- Set heap size appropriate for workload
- Object pooling for frequent allocations
- Regular memory testing with real data
- Alert on memory growth trends
