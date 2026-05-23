---
name: cpu-profiling
description: Profile CPU usage to identify hot spots and bottlenecks. Optimize code paths consuming most CPU time for better performance and resource efficiency.
---

# CPU Profiling

## Overview

CPU profiling identifies which functions consume most CPU time, enabling targeted optimization of expensive code paths.

## When to Use

- High CPU usage
- Slow execution
- Performance regression
- Before optimization
- Production monitoring

## Instructions

### 1. **Profiling Tools**

```yaml
Browser Profiling:

Chrome DevTools:
  Steps:
    1. DevTools → Performance
    2. Click record
    3. Perform action
    4. Stop recording
    5. Analyze flame chart
  Metrics:
    - Function call duration
    - Call frequency
    - Total time vs self time

Firefox Profiler:
  - Built-in performance profiler
  - Flame graphs
  - Timeline view
  - Export and share

React Profiler:
  - DevTools → Profiler
  - Component render times
  - Phase: render vs commit
  - Why component re-rendered

---

Node.js Profiling:

node --prof app.js
node --prof-process isolate-*.log > profile.txt

Clinic.js:
  clinic doctor -- node app.js
  clinic flame -- node app.js
  Shows: functions, memory, delays

V8 Inspector:
  node --inspect app.js
  Open chrome://inspect
  Profiler tab
  Take CPU profile
```

### 2. **Analysis & Interpretation**

```javascript
// Understanding profiles

Flame Graph Reading:
- Wider = more time spent
- Taller = deeper call stack
- Hot path = wide tall bars
- Idle = gaps

Self Time vs Total Time:
- Self: time in function itself
- Total: self + children
- Example:
  main() calls work() for 1s
  work() itself = 0.5s (self)
  work() itself + children = 1s (total)

Hot Spots Identification:
- Find widest bars (most time)
- Check if avoidable
- Check if optimizable
- Profile before/after changes

Example (V8 Analysis):
Function: dataProcessing
  Self time: 500ms (50%)
  Total time: 1000ms
  Calls: 1000 times
  Time per call: 0.5ms
  Optimization: Reduce call frequency
```

### 3. **Optimization Process**

```yaml
Steps:

1. Establish Baseline
  - Profile current behavior
  - Note hottest functions
  - Record total time
  - Check system resources

2. Identify Bottlenecks
  - Find top 5 time consumers
  - Analyze call frequency
  - Understand what they do
  - Check if necessary

3. Create Hypothesis
  - Why is function slow?
  - Can algorithm improve?
  - Can we cache results?
  - Can we parallelize?

4. Implement Changes
  - Single change at a time
  - Measure impact
  - Profile after change
  - Compare flame graphs

5. Verify Improvement
  - Baseline: 1s
  - After optimization: 500ms
  - Confirmed 50% improvement

---

Common Optimizations:

Algorithm Improvement:
  Before: O(n²) nested loop = 100ms for 1000 items
  After: O(n log n) with sort+search = 10ms
  Impact: 10x faster

Caching:
  Before: Recalculate each call
  After: Cache result, return instantly
  Impact: 1000x faster for repeated calls

Memoization:
  Before: fib(40) recalculates each branch
  After: Cache computed values
  Impact: Exponential to linear

Lazy Evaluation:
  Before: Calculate all values upfront
  After: Calculate only needed values
  Impact: 90%+ reduction for partial results

Parallelization:
  Before: Sequential processing, 1000ms
  After: 4 cores, 250ms
  Impact: 4x faster (8 cores = 8x)
```

### 4. **Monitoring & Best Practices**

```yaml
Monitoring:

Production Profiling:
  - Lightweight sampling profiler
  - 1-5% overhead typical
  - Tools: New Relic, DataDog, Clinic
  - Alert on CPU spikes

Key Metrics:
  - CPU usage % per function
  - Call frequency
  - Time per call
  - GC pause times
  - P95/P99 latency

---

Best Practices:

Before Optimizing:
  [ ] Profile to find actual bottleneck
  [ ] Don't guess (verify with data)
  [ ] Establish baseline
  [ ] Measure improvement

During Optimization:
  [ ] Change one thing at a time
  [ ] Profile after each change
  [ ] Verify improvement
  [ ] Don't prematurely optimize

Premature Optimization:
  - Profile first
  - Hot path only (80/20 rule)
  - Measure impact
  - Consider readability

---

Tools Summary:

Framework: Chrome DevTools, Firefox, Node Profiler
Analysis: Flame graphs, Call trees, Timeline
Monitoring: APM tools, Clinic.js
Comparison: Before/after profiles

---

Red Flags:

- Unexpected high CPU
- GC pauses >100ms
- Function called 1M times per request
- Deep call stacks
- Synchronous I/O in loops
- Repeated calculations
- Memory allocation in hot loop
```

## Key Points

- Profile before optimizing (measure, not guess)
- Look for wide/tall bars in flame graphs
- Distinguish self time vs total time
- Optimize top bottlenecks first
- Verify improvements with measurement
- Consider caching and memoization
- Use production profiling for real issues
- Algorithm improvements beat micro-optimizations
- Measure before and after
- Focus on hot paths (80/20 rule)
