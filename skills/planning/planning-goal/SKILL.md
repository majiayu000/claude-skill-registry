---
name: planning-goal
description: Goal-Oriented Action Planning (GOAP) specialist that dynamically creates intelligent plans to achieve complex objectives. Use for multi-step tasks with dependencies, adaptive replanning, complex deployment workflows, or when a high-level goal needs systematic breakdown into achievable actions.
version: 1.0.0
category: development
type: hybrid
capabilities:
  - dynamic_planning
  - precondition_analysis
  - effect_prediction
  - adaptive_replanning
  - goal_decomposition
  - cost_optimization
  - novel_solution_discovery
  - mixed_execution
tools:
  - Read
  - Write
  - Bash
  - Task
  - mcp__claude-flow__task_orchestrate
  - mcp__claude-flow__memory_usage
related_skills:
  - planning-code-goal
  - sparc-workflow
  - agent-orchestration
hooks:
  pre: |
    echo "Starting GOAP planning session..."
    echo "Analyzing current state and goal state..."
  post: |
    echo "GOAP planning complete - action sequence generated"
---

# Goal-Oriented Action Planning (GOAP)

> Dynamic planning system using A* search to find optimal action sequences for complex objectives

## Quick Start

```bash
# Define goal state and current state
Current: {code_written: true, tests_written: false, deployed: false}
Goal: {deployed: true, monitoring: true}

# GOAP generates optimal plan:
1. write_tests -> tests_written: true
2. run_tests -> tests_passed: true
3. build_application -> built: true
4. deploy_application -> deployed: true
5. setup_monitoring -> monitoring: true
```

## When to Use

- Complex multi-step tasks with dependencies requiring optimal ordering
- High-level goals needing systematic breakdown into concrete actions
- Deployment workflows with many prerequisites
- Refactoring projects requiring incremental, safe transformations
- Any task where conditions must be met before actions can execute

## Prerequisites

- Clear definition of current state (what is true now)
- Clear definition of goal state (what should be true)
- Available actions with known preconditions and effects

## Core Concepts

### GOAP Algorithm

GOAP uses A* pathfinding through state space:

1. **State Space**: All possible combinations of world facts
2. **Actions**: Transforms with preconditions and effects
3. **Heuristic**: Estimated cost to reach goal from current state
4. **Optimal Path**: Lowest-cost action sequence achieving goal

### Action Definition

```
Action: action_name
  Preconditions: {condition1: true, condition2: value}
  Effects: {new_condition: true, changed_value: new_value}
  Cost: numeric_value
  Execution: llm|code|hybrid
  Fallback: alternative_action
```

### Execution Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| Focused | Direct action execution | Specific requested actions |
| Closed | Single-domain planning | Defined action set |
| Open | Creative problem solving | Novel solution discovery |

## Implementation Pattern

```typescript
interface WorldState {
  [key: string]: boolean | string | number;
}

interface Action {
  name: string;
  preconditions: Partial<WorldState>;
  effects: Partial<WorldState>;
  cost: number;
  execution: 'llm' | 'code' | 'hybrid';
  tools?: string[];
  fallback?: string;
}

interface Plan {
  actions: Action[];
  totalCost: number;
  estimatedTime: string;
}

function generatePlan(
  currentState: WorldState,
  goalState: WorldState,
  availableActions: Action[]
): Plan {
  // A* search through state space
  // Returns optimal action sequence
}
```

## Configuration

```yaml
goap_config:
  planning:
    algorithm: a_star
    max_depth: 50
    timeout_ms: 5000

  execution:
    mode: adaptive  # focused | closed | open
    parallel_actions: true
    replan_on_failure: true

  monitoring:
    ooda_loop: true
    observe_interval_ms: 1000

  cost_weights:
    time: 1.0
    risk: 2.0
    resource: 1.5
```

## Usage Examples

### Example 1: Software Deployment

```yaml
current_state:
  code_written: true
  tests_written: false
  tests_passed: false
  built: false
  deployed: false
  monitoring: false

goal_state:
  deployed: true
  monitoring: true

available_actions:
  - name: write_tests
    preconditions: {code_written: true}
    effects: {tests_written: true}
    cost: 3

  - name: run_tests
    preconditions: {tests_written: true}
    effects: {tests_passed: true}
    cost: 1

  - name: build_application
    preconditions: {tests_passed: true}
    effects: {built: true}
    cost: 2

  - name: deploy_application
    preconditions: {built: true}
    effects: {deployed: true}
    cost: 2

  - name: setup_monitoring
    preconditions: {deployed: true}
    effects: {monitoring: true}
    cost: 1

# Generated Plan (cost: 9)
plan:
  1. write_tests
  2. run_tests
  3. build_application
  4. deploy_application
  5. setup_monitoring
```

### Example 2: Complex Refactoring

```yaml
current_state:
  legacy_code: true
  documented: false
  tested: false
  refactored: false

goal_state:
  refactored: true
  tested: true
  documented: true

generated_plan:
  1. analyze_codebase:
      effects: {understood: true}

  2. write_tests_for_legacy:
      requires: understood
      effects: {tested: true}

  3. document_current_behavior:
      requires: understood
      effects: {documented: true}

  4. plan_refactoring:
      requires: [documented, tested]
      effects: {plan_ready: true}

  5. execute_refactoring:
      requires: plan_ready
      effects: {refactored: true}

  6. verify_tests_pass:
      requires: refactored
      validates: goal_achieved
```

### Example 3: OODA Loop Monitoring

```typescript
// Observe-Orient-Decide-Act loop during execution
async function executeWithOODA(plan: Plan): Promise<Result> {
  for (const action of plan.actions) {
    // OBSERVE: Check current state
    const currentState = await observeState();

    // ORIENT: Analyze deviations
    const deviation = analyzeDeviation(currentState, expectedState);

    // DECIDE: Replan if needed
    if (deviation.significant) {
      const newPlan = await replan(currentState, goalState);
      return executeWithOODA(newPlan);
    }

    // ACT: Execute action
    await executeAction(action);
  }
}
```

## Execution Checklist

- [ ] Define current state completely
- [ ] Define goal state with all required conditions
- [ ] Inventory available actions with preconditions/effects
- [ ] Calculate action costs realistically
- [ ] Generate plan using A* search
- [ ] Review plan for feasibility
- [ ] Execute with OODA loop monitoring
- [ ] Handle failures with adaptive replanning
- [ ] Verify goal state achieved

## Best Practices

- **Atomic Actions**: Each action should have one clear purpose
- **Explicit Preconditions**: All requirements must be verifiable
- **Predictable Effects**: Action outcomes should be consistent
- **Realistic Costs**: Use costs to guide optimal path selection
- **Replan Early**: Detect failures quickly and adapt
- **Parallel Where Possible**: Execute independent actions concurrently

## Error Handling

### Plan Generation Failures

```typescript
// No valid path exists
if (!plan) {
  // Analyze which preconditions cannot be satisfied
  const unsatisfiable = findUnsatisfiablePreconditions(goalState);
  console.error(`Cannot reach goal: missing ${unsatisfiable}`);

  // Suggest partial goals that ARE achievable
  const partialGoals = suggestAchievableSubsets(goalState);
}
```

### Execution Failures

```typescript
// Action failed during execution
if (actionResult.failed) {
  // Check if alternative action available
  if (action.fallback) {
    await executeAction(action.fallback);
  } else {
    // Replan from current state
    const newPlan = await replan(currentState, goalState);
  }
}
```

## Metrics & Success Criteria

| Metric | Target | Description |
|--------|--------|-------------|
| Plan Generation Time | < 5s | Time to generate optimal plan |
| Goal Achievement Rate | > 95% | Percentage of goals fully achieved |
| Replanning Frequency | < 20% | Actions requiring replanning |
| Cost Accuracy | +/- 15% | Actual vs estimated cost |

## Integration Points

### MCP Tools

```javascript
// Orchestrate GOAP plan across swarm
mcp__claude-flow__task_orchestrate({
  task: "execute_goap_plan",
  strategy: "adaptive",
  priority: "high"
});

// Store successful patterns
mcp__claude-flow__memory_usage({
  action: "store",
  namespace: "goap-patterns",
  key: "deployment_plan_v1",
  value: JSON.stringify(successfulPlan)
});
```

### Hooks

```bash
# Pre-task: Initialize GOAP session
npx claude-flow@alpha hooks pre-task --description "GOAP planning for $GOAL"

# Post-task: Store learned patterns
npx claude-flow@alpha hooks post-task --task-id "goap-$SESSION_ID"
```

### Related Skills

- [planning-code-goal](../planning-code-goal/SKILL.md) - SPARC-enhanced code planning
- [sparc-workflow](../../../workspace-hub/sparc-workflow/SKILL.md) - Structured development
- [agent-orchestration](../../../workspace-hub/agent-orchestration/SKILL.md) - Swarm coordination

## References

- [GOAP in Game AI](https://en.wikipedia.org/wiki/Goal-oriented_action_planning)
- [A* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [OODA Loop](https://en.wikipedia.org/wiki/OODA_loop)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from goal-planner agent
