/*============================================================================*/
/* WHEN-PROFILING-PERFORMANCE-USE-PERFORMANCE-PROFILER SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-profiling-performance-use-performance-profiler
version: 1.0.0
description: |
  [assert|neutral] Comprehensive performance profiling, bottleneck detection, and optimization system [ground:given] [conf:0.95] [state:confirmed]
category: performance
tags:
- performance
- profiling
- optimization
- benchmarking
- mece
author: Claude Code
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-profiling-performance-use-performance-profiler workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic performance processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-profiling-performance-use-performance-profiler",
  category: "performance",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Evidential",
  source: "Turkish",
  force: "How do you know?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["when-profiling-performance-use-performance-profiler", "performance", "workflow"],
  context: "user needs when-profiling-performance-use-performance-profiler capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Performance Profiler Skill

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



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
    "error_

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/performance/when-profiling-performance-use-performance-profiler/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-profiling-performance-use-performance-profiler-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>WHEN_PROFILING_PERFORMANCE_USE_PERFORMANCE_PROFILER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
