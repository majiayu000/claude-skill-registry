/*============================================================================*/
/* WHEN-ANALYZING-PERFORMANCE-USE-PERFORMANCE-ANALYSIS SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-analyzing-performance-use-performance-analysis
version: 1.0.0
description: |
  [assert|neutral] Comprehensive performance analysis, bottleneck detection, and optimization recommendations for Claude Flow swarms [ground:given] [conf:0.95] [state:confirmed]
category: performance
tags:
- performance
- analysis
- bottleneck
- optimization
- profiling
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-analyzing-performance-use-performance-analysis workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic performance processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-analyzing-performance-use-performance-analysis",
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
  keywords: ["when-analyzing-performance-use-performance-analysis", "performance", "workflow"],
  context: "user needs when-analyzing-performance-use-performance-analysis capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Performance Analysis SOP

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

Comprehensive performance analysis for Claude Flow swarms including bottleneck detection, profiling, benchmarking, and actionable optimization recommendations.

## Agents & Responsibilities

### performance-analyzer
**Role:** Analyze system performance and identify issues
**Responsibilities:**
- Collect performance metrics
- Analyze resource utilization
- Identify bottlenecks
- Generate analysis reports

### performance-benchmarker
**Role:** Run performance benchmarks and comparisons
**Responsibilities:**
- Execute benchmark suites
- Compare performance across configurations
- Establish performance baselines
- Validate improvements

### perf-analyzer
**Role:** Deep performance profiling and optimization
**Responsibilities:**
- Profile code execution
- Analyze memory usage
- Optimize critical paths
- Recommend improvements

## Phase 1: Establish Baseline

### Objective
Measure current performance and establish baseline metrics.

### Scripts

```bash
# Collect baseline metrics
npx claude-flow@alpha performance baseline \
  --duration 300 \
  --interval 5 \
  --output baseline-metrics.json

# Run benchmark suite
npx claude-flow@alpha benchmark run \
  --type swarm \
  --iterations 10 \
  --output benchmark-results.json

# Profile system resources
npx claude-flow@alpha performance profile \
  --include-cpu \
  --include-memory \
  --include-network \
  --output resource-profile.json

# Collect agent metrics
npx claude-flow@alpha agent metrics --all --format json > agent-metrics.json

# Store baseline
npx claude-flow@alpha memory store \
  --key "performance/baseline" \
  --file baseline-metrics.json

# Generate baseline report
npx claude-flow@alpha performance report \
  --type baseline \
  --metrics baseline-metrics.json \
  --output baseline-report.md
```

### Key Baseline Metrics

**Swarm-Level:**
- Total throughput (tasks/min)
- Average latency (ms)
- Resource utilization (%)
- Error rate (%)
- Coordination overhead (ms)

**Agent-Level:**
- Task completion rate
- Response time (ms)
- CPU usage (%)
- Memory usage (MB)
- Idle time (%)

**System-Level:**
- Total CPU usage (%)
- Total memory usage (MB)
- Network bandwidth (MB/s)
- Disk I/O (MB/s)

### Memory Patterns

```bash
# Store performance baseline
npx claude-flow@alpha memory store \
  --key "performance/baseline/timestamp" \
  --value "$(date -Iseconds)"

npx claude-flow@alpha memory store \
  --key "performance/baseline/metrics" \
  --value '{
    "throughput": 145.2,
    "latency": 38.5,
    "utilization": 0.78,
    "errorRate": 0.012,
    "timestamp": "'$(date -Iseconds)'"
  }'
```

## Phase 2: Profile System

### Objective
Deep profiling of system components to identify performance characteristics.

### Scripts

```bash
# Profile swarm execution
npx claude-flow@alpha performance profile-swarm \
  --duration 300 \
  --sample-rate 100 \
  --output swarm-profile.json

# Profile individual agents
for AGENT in $(npx claude-flow@alpha agent list --format json | jq -r '.[].id'); do
  npx claude-flow@alpha performance profile-agent \
    --agent-id "$AGENT" \
    --duration 60 \
    --output "profiles/agent-$AGENT.json"
done

# Profile memory usage
npx claude-flow@alpha memory profile \
  --show-hotspots \
  --show-leaks \
  --output memory-profile.json

# Profile network communication
npx claude-flow@alpha performance profile-network \
  --show-latency \
  --show-bandwidth \
  --output network-profile.json

# Generate flamegraph
npx claude-flow@alpha performance flamegraph \
  --input swarm-profile.json \
  --output flamegraph.svg

# Analyze CPU hotspots
npx claude-flow@alpha performance hotspots \
  --type cpu \
  --threshold 5 \
  --output cpu-hotspots.json
```

### Profiling Analysis

```bash
# Identify slow functions
SLOW_FUNCTIONS=$(jq '[.profile[] | select(.time > 100)]' swarm-profile.json)

# Identify memory hogs
MEMORY_HOGS=$(jq '[.memory[] | sele

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
  pattern: "skills/performance/when-analyzing-performance-use-performance-analysis/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-analyzing-performance-use-performance-analysis-{session_id}",
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

[commit|confident] <promise>WHEN_ANALYZING_PERFORMANCE_USE_PERFORMANCE_ANALYSIS_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
