---
name: when-profiling-performance-use-performance-profiler
version: 1.0.0
description: Comprehensive performance profiling, bottleneck detection, and optimization system
author: Claude Code
category: performance
complexity: HIGH
tags: [performance, profiling, optimization, benchmarking, mece]
agents:
  - performance-analyzer
  - performance-benchmarker
  - coder
  - optimizer
components:
  - subagent
  - slash-command
  - mcp-tool
dependencies:
  - claude-flow@alpha
  - perf (Linux)
  - instruments (macOS)
  - clinic.js (Node.js)
---

# Performance Profiler Skill

## Overview

**When profiling performance, use performance-profiler** to measure, analyze, and optimize application performance across CPU, memory, I/O, and network dimensions.

## MECE Breakdown

### Mutually Exclusive Components:
1. **Baseline Phase**: Establish current performance metrics
2. **Detection Phase**: Identify bottlenecks and hot paths
3. **Analysis Phase**: Root cause analysis and impact assessment
4. **Optimization Phase**: Generate and prioritize recommendations
5. **Implementation Phase**: Apply optimizations with agent assistance
6. **Validation Phase**: Benchmark improvements and verify gains

### Collectively Exhaustive Coverage:
- **CPU Profiling**: Function execution time, hot paths, call graphs
- **Memory Profiling**: Heap usage, allocations, leaks, garbage collection
- **I/O Profiling**: File system, database, network latency
- **Network Profiling**: Request timing, bandwidth, connection pooling
- **Concurrency**: Thread utilization, lock contention, async operations
- **Algorithm Analysis**: Time complexity, space complexity
- **Cache Analysis**: Hit rates, cache misses, invalidation patterns
- **Database**: Query performance, N+1 problems, index usage

## Features

### Core Capabilities:
- Multi-dimensional performance profiling (CPU, memory, I/O, network)
- Automated bottleneck detection with prioritization
- Real-time profiling and historical analysis
- Flame graph generation for visual analysis
- Memory leak detection and heap snapshots
- Database query optimization
- Algorithmic complexity analysis
- A/B comparison of before/after optimizations
- Production-safe profiling with minimal overhead
- Integration with APM tools (New Relic, DataDog, etc.)

### Profiling Modes:
- **Quick Scan**: 30-second lightweight profiling
- **Standard**: 5-minute comprehensive analysis
- **Deep**: 30-minute detailed investigation
- **Continuous**: Long-running production monitoring
- **Stress Test**: Load-based profiling under high traffic

## Usage

### Slash Command:
```bash
/profile [path] [--mode quick|standard|deep] [--target cpu|memory|io|network|all]
```

### Subagent Invocation:
```javascript
Task("Performance Profiler", "Profile ./app with deep CPU and memory analysis", "performance-analyzer")
```

### MCP Tool:
```javascript
mcp__performance-profiler__analyze({
  project_path: "./app",
  profiling_mode: "standard",
  targets: ["cpu", "memory", "io"],
  generate_optimizations: true
})
```

## Architecture

### Phase 1: Baseline Measurement
1. Establish current performance metrics
2. Define performance budgets
3. Set up monitoring infrastructure
4. Capture baseline snapshots

### Phase 2: Bottleneck Detection
1. CPU profiling (sampling or instrumentation)
2. Memory profiling (heap analysis)
3. I/O profiling (syscall tracing)
4. Network profiling (packet analysis)
5. Database profiling (query logs)

### Phase 3: Root Cause Analysis
1. Correlate metrics across dimensions
2. Identify causal relationships
3. Calculate performance impact
4. Prioritize issues by severity

### Phase 4: Optimization Generation
1. Algorithmic improvements
2. Caching strategies
3. Parallelization opportunities
4. Database query optimization
5. Memory optimization
6. Network optimization

### Phase 5: Implementation
1. Generate optimized code with coder agent
2. Apply database optimizations
3. Configure caching layers
4. Implement parallelization

### Phase 6: Validation
1. Run benchmark suite
2. Compare before/after metrics
3. Verify no regressions
4. Generate performance report

## Output Formats

### Performance Report:
```json
{
  "project": "my-app",
  "profiling_mode": "standard",
  "duration_seconds": 300,
  "baseline": {
    "requests_per_second": 1247,
    "avg_response_time_ms": 123,
    "p95_response_time_ms": 456,
    "p99_response_time_ms": 789,
    "cpu_usage_percent": 67,
    "memory_usage_mb": 512,
    "error_rate_percent": 0.1
  },
  "bottlenecks": [
    {
      "type": "cpu",
      "severity": "high",
      "function": "processData",
      "time_percent": 34.5,
      "calls": 123456,
      "avg_time_ms": 2.3,
      "recommendation": "Optimize algorithm complexity from O(n²) to O(n log n)"
    }
  ],
  "optimizations": [...],
  "estimated_improvement": {
    "throughput_increase": "3.2x",
    "latency_reduction": "68%",
    "memory_reduction": "45%"
  }
}
```

### Flame Graph:
Interactive SVG flame graph showing call stack with time proportions

### Heap Snapshot:
Memory allocation breakdown with retention paths

### Optimization Report:
Prioritized list of actionable improvements with code examples

## Examples

### Example 1: Quick CPU Profiling
```bash
/profile ./my-app --mode quick --target cpu
```

### Example 2: Deep Memory Analysis
```bash
/profile ./my-app --mode deep --target memory --detect-leaks
```

### Example 3: Full Stack Optimization
```bash
/profile ./my-app --mode standard --target all --optimize --benchmark
```

### Example 4: Database Query Optimization
```bash
/profile ./my-app --mode standard --target io --database --explain-queries
```

## Integration with Claude-Flow

### Coordination Pattern:
```javascript
// Step 1: Initialize profiling swarm
mcp__claude-flow__swarm_init({ topology: "star", maxAgents: 5 })

// Step 2: Spawn specialized agents
[Parallel Execution]:
  Task("CPU Profiler", "Profile CPU usage and identify hot paths in ./app", "performance-analyzer")
  Task("Memory Profiler", "Analyze heap usage and detect memory leaks", "performance-analyzer")
  Task("I/O Profiler", "Profile file system and database operations", "performance-analyzer")
  Task("Network Profiler", "Analyze network requests and identify slow endpoints", "performance-analyzer")
  Task("Optimizer", "Generate optimization recommendations based on profiling data", "optimizer")

// Step 3: Implementation agent applies optimizations
[Sequential Execution]:
  Task("Coder", "Implement recommended optimizations from profiling analysis", "coder")
  Task("Benchmarker", "Run benchmark suite and validate improvements", "performance-benchmarker")
```

## Configuration

### Default Settings:
```json
{
  "profiling": {
    "sampling_rate_hz": 99,
    "stack_depth": 128,
    "include_native_code": false,
    "track_allocations": true
  },
  "thresholds": {
    "cpu_hot_path_percent": 10,
    "memory_leak_growth_mb": 10,
    "slow_query_ms": 100,
    "slow_request_ms": 1000
  },
  "optimization": {
    "auto_apply": false,
    "require_approval": true,
    "run_tests_before": true,
    "run_benchmarks_after": true
  },
  "output": {
    "flame_graph": true,
    "heap_snapshot": true,
    "call_tree": true,
    "recommendations": true
  }
}
```

## Profiling Techniques

### CPU Profiling:
- **Sampling**: Periodic stack sampling (low overhead)
- **Instrumentation**: Function entry/exit hooks (accurate but higher overhead)
- **Tracing**: Event-based profiling

### Memory Profiling:
- **Heap Snapshots**: Point-in-time memory state
- **Allocation Tracking**: Record all allocations
- **Leak Detection**: Compare snapshots over time
- **GC Analysis**: Garbage collection patterns

### I/O Profiling:
- **Syscall Tracing**: Track system calls (strace, dtrace)
- **File System**: Monitor read/write operations
- **Database**: Query logging and EXPLAIN ANALYZE
- **Network**: Packet capture and request timing

### Concurrency Profiling:
- **Thread Analysis**: CPU utilization per thread
- **Lock Contention**: Identify blocking operations
- **Async Operations**: Promise/callback timing

## Performance Optimization Strategies

### Algorithmic:
- Reduce time complexity (O(n²) → O(n log n))
- Use appropriate data structures
- Eliminate unnecessary work
- Memoization and dynamic programming

### Caching:
- In-memory caching (Redis, Memcached)
- CDN for static assets
- HTTP caching headers
- Query result caching

### Parallelization:
- Multi-threading
- Worker pools
- Async I/O
- Batching operations

### Database:
- Add missing indexes
- Optimize queries
- Reduce N+1 queries
- Connection pooling
- Read replicas

### Memory:
- Object pooling
- Reduce allocations
- Stream processing
- Compression

### Network:
- Connection keep-alive
- HTTP/2 or HTTP/3
- Compression
- Request batching
- Rate limiting

## Performance Budgets

### Frontend:
- Time to First Byte (TTFB): < 200ms
- First Contentful Paint (FCP): < 1.8s
- Largest Contentful Paint (LCP): < 2.5s
- Time to Interactive (TTI): < 3.8s
- Total Blocking Time (TBT): < 200ms
- Cumulative Layout Shift (CLS): < 0.1

### Backend:
- API Response Time (p50): < 100ms
- API Response Time (p95): < 500ms
- API Response Time (p99): < 1000ms
- Throughput: > 1000 req/s
- Error Rate: < 0.1%
- CPU Usage: < 70%
- Memory Usage: < 80%

### Database:
- Query Time (p50): < 10ms
- Query Time (p95): < 50ms
- Query Time (p99): < 100ms
- Connection Pool Utilization: < 80%

## Best Practices

1. Profile production workloads when possible
2. Use production-like data volumes
3. Profile under realistic load
4. Measure multiple times for consistency
5. Focus on p95/p99, not just averages
6. Optimize bottlenecks in order of impact
7. Always benchmark before and after
8. Monitor for regressions in CI/CD
9. Set up continuous profiling
10. Track performance over time

## Troubleshooting

### Issue: High CPU usage but no obvious hot path
**Solution**: Check for excessive small function calls, increase sampling rate, or use instrumentation

### Issue: Memory grows continuously
**Solution**: Run heap snapshot comparison to identify leak sources

### Issue: Slow database queries
**Solution**: Use EXPLAIN ANALYZE, check for missing indexes, analyze query plans

### Issue: High latency but low CPU
**Solution**: Profile I/O operations, check for blocking synchronous calls

## See Also

- PROCESS.md - Detailed step-by-step profiling workflow
- README.md - Quick start guide
- subagent-performance-profiler.md - Agent implementation details
- slash-command-profile.sh - Command-line interface
- mcp-performance-profiler.json - MCP tool schema
