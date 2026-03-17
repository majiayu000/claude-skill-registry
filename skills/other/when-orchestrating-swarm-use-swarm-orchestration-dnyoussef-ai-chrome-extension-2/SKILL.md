---
name: when-orchestrating-swarm-use-swarm-orchestration
description: Complex multi-agent swarm orchestration with task decomposition, distributed execution, and result synthesis
version: 1.0.0
tags:
  - swarm
  - orchestration
  - coordination
  - task-decomposition
  - result-synthesis
category: workflow
agents:
  - task-orchestrator
  - hierarchical-coordinator
  - adaptive-coordinator
complexity: advanced
estimated_duration: 60-120 minutes
prerequisites:
  - Claude Flow installed and configured
  - Understanding of task decomposition
  - Multi-agent coordination experience
outputs:
  - Orchestrated swarm execution
  - Task decomposition tree
  - Synthesized results
  - Performance metrics
---

# Swarm Orchestration SOP

## Overview

This skill implements complex multi-agent swarm orchestration with intelligent task decomposition, distributed execution, progress monitoring, and result synthesis. It enables coordinated execution of complex workflows across multiple specialized agents.

## Agents & Responsibilities

### task-orchestrator
**Role:** Central orchestration and task decomposition
**Responsibilities:**
- Decompose complex tasks into subtasks
- Assign tasks to appropriate agents
- Monitor execution progress
- Synthesize results from multiple agents

### hierarchical-coordinator
**Role:** Hierarchical task delegation and coordination
**Responsibilities:**
- Manage task hierarchy
- Coordinate parent-child task relationships
- Handle task dependencies
- Ensure proper execution order

### adaptive-coordinator
**Role:** Dynamic workload balancing and optimization
**Responsibilities:**
- Monitor agent workloads
- Rebalance task assignments
- Optimize resource allocation
- Adapt to changing conditions

## Phase 1: Plan Orchestration

### Objective
Analyze complex task requirements and create detailed decomposition plan with dependency mapping.

### Evidence-Based Validation
- [ ] Task decomposition tree created
- [ ] Dependencies mapped
- [ ] Agent assignments planned
- [ ] Execution strategy defined

### Scripts

```bash
# Analyze task complexity
npx claude-flow@alpha task analyze --task "Build full-stack application" --output task-analysis.json

# Generate decomposition tree
npx claude-flow@alpha task decompose \
  --task "Build full-stack application" \
  --max-depth 3 \
  --output decomposition.json

# Visualize decomposition
npx claude-flow@alpha task visualize --input decomposition.json --output task-tree.png

# Store decomposition in memory
npx claude-flow@alpha memory store \
  --key "orchestration/decomposition" \
  --file decomposition.json

# Identify dependencies
npx claude-flow@alpha task dependencies \
  --input decomposition.json \
  --output dependencies.json

# Plan agent assignments
npx claude-flow@alpha task plan \
  --decomposition decomposition.json \
  --available-agents 12 \
  --output execution-plan.json
```

### Task Decomposition Strategy

**Level 1: High-Level Goals**
```json
{
  "task": "Build full-stack application",
  "subtasks": [
    "Design architecture",
    "Implement backend",
    "Implement frontend",
    "Setup infrastructure",
    "Testing and QA"
  ]
}
```

**Level 2: Component Tasks**
```json
{
  "task": "Implement backend",
  "subtasks": [
    "Design API endpoints",
    "Implement authentication",
    "Setup database",
    "Create business logic",
    "API documentation"
  ]
}
```

**Level 3: Atomic Tasks**
```json
{
  "task": "Implement authentication",
  "subtasks": [
    "Setup JWT library",
    "Create user model",
    "Implement login endpoint",
    "Implement registration endpoint",
    "Add password hashing",
    "Create auth middleware"
  ]
}
```

### Memory Patterns

```bash
# Store orchestration plan
npx claude-flow@alpha memory store \
  --key "orchestration/plan" \
  --value '{
    "totalTasks": 45,
    "levels": 3,
    "estimatedDuration": "2h 30m",
    "requiredAgents": 12
  }'

# Store dependency graph
npx claude-flow@alpha memory store \
  --key "orchestration/dependencies" \
  --value '{
    "task-003": ["task-001", "task-002"],
    "task-008": ["task-003", "task-004"],
    "task-012": ["task-008", "task-009"]
  }'
```

### Validation Criteria
1. Task tree depth ≤ 3 levels
2. All tasks have clear success criteria
3. Dependencies correctly identified
4. No circular dependencies
5. Agent capacity sufficient for load

## Phase 2: Initialize Swarm

### Objective
Setup swarm infrastructure with appropriate topology and coordinator agents.

### Evidence-Based Validation
- [ ] Swarm initialized successfully
- [ ] Topology optimized for workload
- [ ] Coordinator agents active
- [ ] Memory coordination established

### Scripts

```bash
# Determine optimal topology
TASK_COUNT=$(jq '.totalTasks' decomposition.json)

if [ "$TASK_COUNT" -gt 30 ]; then
  TOPOLOGY="mesh"
elif [ "$TASK_COUNT" -gt 15 ]; then
  TOPOLOGY="hierarchical"
else
  TOPOLOGY="star"
fi

# Initialize swarm with optimal topology
npx claude-flow@alpha swarm init \
  --topology $TOPOLOGY \
  --max-agents 15 \
  --strategy adaptive

# Spawn task orchestrator
npx claude-flow@alpha agent spawn \
  --type coordinator \
  --role "task-orchestrator" \
  --capabilities "task-decomposition,assignment,synthesis"

# Spawn hierarchical coordinator
npx claude-flow@alpha agent spawn \
  --type coordinator \
  --role "hierarchical-coordinator" \
  --capabilities "hierarchy-management,delegation"

# Spawn adaptive coordinator
npx claude-flow@alpha agent spawn \
  --type coordinator \
  --role "adaptive-coordinator" \
  --capabilities "workload-balancing,optimization"

# Verify swarm status
npx claude-flow@alpha swarm status --show-agents --show-topology
```

### MCP Integration

```javascript
// Initialize swarm
mcp__claude-flow__swarm_init({
  topology: "hierarchical",
  maxAgents: 15,
  strategy: "adaptive"
})

// Spawn coordinators
mcp__claude-flow__agent_spawn({
  type: "coordinator",
  name: "task-orchestrator",
  capabilities: ["task-decomposition", "assignment", "synthesis"]
})

mcp__claude-flow__agent_spawn({
  type: "coordinator",
  name: "hierarchical-coordinator",
  capabilities: ["hierarchy-management", "delegation"]
})

mcp__claude-flow__agent_spawn({
  type: "coordinator",
  name: "adaptive-coordinator",
  capabilities: ["workload-balancing", "optimization"]
})
```

### Memory Patterns

```bash
# Store swarm configuration
npx claude-flow@alpha memory store \
  --key "orchestration/swarm" \
  --value '{
    "swarmId": "swarm-12345",
    "topology": "hierarchical",
    "maxAgents": 15,
    "coordinators": ["task-orchestrator", "hierarchical-coordinator", "adaptive-coordinator"]
  }'
```

### Validation Criteria
1. Swarm operational
2. All coordinators active
3. Topology matches requirements
4. Memory coordination functional
5. Health checks passing

## Phase 3: Orchestrate Execution

### Objective
Coordinate distributed task execution across swarm agents with proper dependency handling.

### Evidence-Based Validation
- [ ] All tasks assigned to agents
- [ ] Dependencies respected
- [ ] Execution in progress
- [ ] Progress tracked continuously

### Scripts

```bash
# Spawn specialized agents based on task requirements
npx claude-flow@alpha agent spawn --type researcher --count 2
npx claude-flow@alpha agent spawn --type coder --count 5
npx claude-flow@alpha agent spawn --type reviewer --count 2
npx claude-flow@alpha agent spawn --type tester --count 2

# Orchestrate task execution
npx claude-flow@alpha task orchestrate \
  --plan execution-plan.json \
  --strategy adaptive \
  --max-agents 12 \
  --priority high

# Alternative: Orchestrate with MCP
# mcp__claude-flow__task_orchestrate({
#   task: "Execute full-stack application build",
#   strategy: "adaptive",
#   maxAgents: 12,
#   priority: "high"
# })

# Monitor orchestration status
npx claude-flow@alpha task status --detailed --json > task-status.json

# Track individual task progress
npx claude-flow@alpha task list --filter "in_progress" --show-timing

# Monitor agent workloads
npx claude-flow@alpha agent metrics --metric tasks --format table
```

### Task Assignment Algorithm

```bash
#!/bin/bash
# assign-tasks.sh

# Read decomposition
TASKS=$(jq -r '.tasks[] | @json' decomposition.json)

for TASK in $TASKS; do
  TASK_ID=$(echo $TASK | jq -r '.id')
  TASK_TYPE=$(echo $TASK | jq -r '.type')
  DEPENDENCIES=$(echo $TASK | jq -r '.dependencies[]')

  # Check if dependencies completed
  DEPS_COMPLETE=true
  for DEP in $DEPENDENCIES; do
    DEP_STATUS=$(npx claude-flow@alpha task status --task-id $DEP --format json | jq -r '.status')
    if [ "$DEP_STATUS" != "completed" ]; then
      DEPS_COMPLETE=false
      break
    fi
  done

  # Assign task if dependencies complete
  if [ "$DEPS_COMPLETE" = true ]; then
    # Find least loaded agent of required type
    AGENT_ID=$(npx claude-flow@alpha agent list \
      --filter "type=$TASK_TYPE" \
      --sort-by load \
      --format json | jq -r '.[0].id')

    # Assign task
    npx claude-flow@alpha task assign \
      --task-id $TASK_ID \
      --agent-id $AGENT_ID

    echo "Assigned task $TASK_ID to agent $AGENT_ID"
  fi
done
```

### Memory Patterns

```bash
# Store task assignments
npx claude-flow@alpha memory store \
  --key "orchestration/assignments" \
  --value '{
    "task-001": {"agent": "agent-researcher-1", "status": "in_progress", "started": "2025-10-30T10:00:00Z"},
    "task-002": {"agent": "agent-coder-1", "status": "in_progress", "started": "2025-10-30T10:01:00Z"}
  }'

# Store execution timeline
npx claude-flow@alpha memory store \
  --key "orchestration/timeline" \
  --value '{
    "started": "2025-10-30T10:00:00Z",
    "tasksCompleted": 12,
    "tasksInProgress": 8,
    "tasksPending": 25
  }'
```

### Validation Criteria
1. All agents assigned tasks
2. No dependency violations
3. Task execution progressing
4. No agent overload
5. Error handling active

## Phase 4: Monitor Progress

### Objective
Track execution progress, identify blockers, and maintain real-time visibility.

### Evidence-Based Validation
- [ ] Progress metrics collected
- [ ] Blockers identified quickly
- [ ] Agents responding properly
- [ ] Timeline on track

### Scripts

```bash
# Start continuous monitoring
npx claude-flow@alpha swarm monitor \
  --interval 10 \
  --duration 3600 \
  --output orchestration-monitor.log &

# Track task completion rate
while true; do
  COMPLETED=$(npx claude-flow@alpha task list --filter "completed" | wc -l)
  TOTAL=$(npx claude-flow@alpha task list | wc -l)
  PROGRESS=$((COMPLETED * 100 / TOTAL))

  echo "Progress: $PROGRESS% ($COMPLETED/$TOTAL tasks)"

  npx claude-flow@alpha memory store \
    --key "orchestration/progress" \
    --value "{\"completed\": $COMPLETED, \"total\": $TOTAL, \"percentage\": $PROGRESS}"

  sleep 30
done &

# Monitor for blocked tasks
npx claude-flow@alpha task detect-blocked \
  --threshold 300 \
  --notify-on-block

# Monitor agent health
npx claude-flow@alpha agent health-check --all --interval 60

# Generate progress report
npx claude-flow@alpha orchestration report \
  --include-timeline \
  --include-agent-metrics \
  --output progress-report.md
```

### Progress Visualization

```bash
# Generate Gantt chart
npx claude-flow@alpha task gantt \
  --input task-status.json \
  --output gantt-chart.png

# Generate network diagram
npx claude-flow@alpha task network \
  --show-dependencies \
  --show-progress \
  --output network-diagram.png
```

### Memory Patterns

```bash
# Store progress snapshots
npx claude-flow@alpha memory store \
  --key "orchestration/snapshot-$(date +%s)" \
  --value '{
    "timestamp": "'$(date -Iseconds)'",
    "completed": 18,
    "inProgress": 12,
    "pending": 15,
    "blocked": 0,
    "failed": 0
  }'

# Store blocker information
npx claude-flow@alpha memory store \
  --key "orchestration/blockers" \
  --value '{
    "task-015": {"reason": "dependency-failed", "since": "2025-10-30T10:15:00Z"},
    "task-022": {"reason": "agent-unresponsive", "since": "2025-10-30T10:20:00Z"}
  }'
```

### Validation Criteria
1. Progress tracking accurate
2. Blockers detected within 5 minutes
3. No stalled tasks unnoticed
4. Agent failures handled
5. Progress reports generated

## Phase 5: Synthesize Results

### Objective
Aggregate and synthesize results from all completed tasks into coherent outputs.

### Evidence-Based Validation
- [ ] All task results collected
- [ ] Results synthesized successfully
- [ ] Output validated
- [ ] Final report generated

### Scripts

```bash
# Collect all task results
npx claude-flow@alpha task results --all --format json > all-results.json

# Synthesize results by category
npx claude-flow@alpha task synthesize \
  --input all-results.json \
  --group-by category \
  --output synthesized-results.json

# Generate final outputs
npx claude-flow@alpha orchestration finalize \
  --results synthesized-results.json \
  --output final-output/

# Validate outputs
npx claude-flow@alpha orchestration validate \
  --output final-output/ \
  --criteria validation-criteria.json

# Generate final report
npx claude-flow@alpha orchestration report \
  --type final \
  --include-metrics \
  --include-timeline \
  --include-outputs \
  --output final-orchestration-report.md

# Archive orchestration data
npx claude-flow@alpha orchestration archive \
  --output orchestration-archive-$(date +%Y%m%d-%H%M%S).tar.gz
```

### MCP Integration

```javascript
// Get task results
mcp__claude-flow__task_results({
  taskId: "all",
  format: "detailed"
})

// Check final status
mcp__claude-flow__task_status({
  detailed: true
})
```

### Result Synthesis Strategy

**1. Collect Results:**
```bash
# Get results from each agent type
RESEARCHER_RESULTS=$(npx claude-flow@alpha task results --agent-type researcher --format json)
CODER_RESULTS=$(npx claude-flow@alpha task results --agent-type coder --format json)
REVIEWER_RESULTS=$(npx claude-flow@alpha task results --agent-type reviewer --format json)
```

**2. Aggregate by Phase:**
```bash
# Architecture phase results
ARCHITECTURE=$(jq '[.[] | select(.phase=="architecture")]' all-results.json)

# Implementation phase results
IMPLEMENTATION=$(jq '[.[] | select(.phase=="implementation")]' all-results.json)

# Testing phase results
TESTING=$(jq '[.[] | select(.phase=="testing")]' all-results.json)
```

**3. Synthesize Final Output:**
```bash
# Combine all results
jq -s '{
  architecture: .[0],
  implementation: .[1],
  testing: .[2],
  metadata: {
    totalTasks: (.[0] + .[1] + .[2] | length),
    duration: "'$(date -Iseconds)'",
    successRate: 0.98
  }
}' \
  <(echo "$ARCHITECTURE") \
  <(echo "$IMPLEMENTATION") \
  <(echo "$TESTING") \
  > final-synthesis.json
```

### Memory Patterns

```bash
# Store final results
npx claude-flow@alpha memory store \
  --key "orchestration/results/final" \
  --file final-synthesis.json

# Store performance metrics
npx claude-flow@alpha memory store \
  --key "orchestration/metrics/final" \
  --value '{
    "totalTasks": 45,
    "completed": 44,
    "failed": 1,
    "duration": "2h 18m",
    "avgTaskTime": "3m 5s",
    "throughput": "0.32 tasks/min"
  }'
```

### Validation Criteria
1. All task results accounted for
2. Synthesis logic correct
3. Outputs validated successfully
4. No data loss
5. Final report comprehensive

## Success Criteria

### Overall Validation
- [ ] Task decomposition accurate
- [ ] Swarm orchestration successful
- [ ] All tasks completed (≥95%)
- [ ] Results synthesized correctly
- [ ] Performance targets met

### Performance Targets
- Task success rate: ≥95%
- Average task completion time: Within estimates ±20%
- Agent utilization: 70-90%
- Coordination overhead: <15%
- Result synthesis time: <5 minutes

## Common Issues & Solutions

### Issue: Task Dependencies Not Resolved
**Symptoms:** Tasks blocked waiting for dependencies
**Solution:** Verify dependency graph, check for circular dependencies

### Issue: Agent Overload
**Symptoms:** Some agents at 100% utilization, others idle
**Solution:** Rebalance task assignments, spawn additional agents

### Issue: Task Execution Stalled
**Symptoms:** Tasks remain in-progress indefinitely
**Solution:** Implement timeout mechanism, restart stuck agents

### Issue: Result Synthesis Incomplete
**Symptoms:** Missing results in final output
**Solution:** Verify all tasks completed, check result collection logic

## Best Practices

1. **Clear Decomposition:** Break tasks into atomic units
2. **Explicit Dependencies:** Document all task dependencies
3. **Progress Tracking:** Monitor continuously
4. **Error Handling:** Implement retry logic
5. **Result Validation:** Verify outputs at each phase
6. **Memory Coordination:** Use shared memory for state
7. **Agent Specialization:** Assign tasks to appropriate agents
8. **Performance Monitoring:** Track metrics throughout

## Integration Points

### With Other Skills
- **advanced-swarm:** For topology optimization
- **performance-analysis:** For bottleneck detection
- **cascade-orchestrator:** For workflow chaining
- **hive-mind:** For collective decision-making

### With External Systems
- CI/CD pipelines for automated execution
- Project management tools for tracking
- Monitoring systems for observability
- Storage systems for result archival

## Next Steps

After completing this skill:
1. Analyze orchestration metrics
2. Optimize task decomposition strategy
3. Experiment with different topologies
4. Implement custom synthesis logic
5. Create reusable orchestration templates

## References

- Claude Flow Documentation
- Task Decomposition Patterns
- Multi-Agent Orchestration Theory
- Distributed Systems Coordination
