---
name: planning-code-goal
description: Code-centric Goal-Oriented Action Planning integrated with SPARC methodology. Use for feature implementation planning, performance optimization goals, testing strategy development, or any software development objective requiring systematic breakdown with measurable success criteria.
version: 1.0.0
category: development
type: hybrid
capabilities:
  - feature_implementation_planning
  - performance_optimization
  - testing_strategy_design
  - sparc_integration
  - milestone_tracking
  - success_metrics
  - tdd_workflow
  - api_development
tools:
  - Read
  - Write
  - Bash
  - Task
  - mcp__claude-flow__task_orchestrate
  - mcp__claude-flow__memory_usage
  - mcp__claude-flow__agent_spawn
related_skills:
  - planning-goal
  - sparc-workflow
  - testing-tdd-london
hooks:
  pre: |
    echo "Starting SPARC-GOAP code planning session..."
    echo "Mapping SPARC phases to GOAP milestones..."
  post: |
    echo "Code goal planning complete - milestones defined"
---

# Code-Centric Goal-Oriented Action Planning

> SPARC-integrated planning for software development objectives with measurable outcomes

## Quick Start

```bash
# Define code goal
Goal: Implement OAuth2 authentication

# SPARC-GOAP generates phased plan:
Phase 1 (Specification): Define requirements, acceptance criteria
Phase 2 (Pseudocode): Design algorithms, state machines
Phase 3 (Architecture): Design components, API contracts
Phase 4 (Refinement): TDD implementation cycles
Phase 5 (Completion): Integration, validation, deployment

# Execute with SPARC commands
npx claude-flow sparc tdd "OAuth2 authentication"
```

## When to Use

- Feature implementation requiring systematic breakdown
- Performance optimization with measurable targets
- Testing strategy development with coverage goals
- API development with clear contract definitions
- Database evolution with migration planning
- Technical debt reduction with incremental milestones

## Prerequisites

- Understanding of SPARC methodology phases
- Clear definition of desired outcome
- Access to codebase for state analysis
- Measurable success criteria

## Core Concepts

### SPARC Phases in Goal Planning

| Phase | GOAP Role | Deliverables |
|-------|-----------|--------------|
| Specification | Define goal state | Requirements, acceptance criteria |
| Pseudocode | Plan actions | Algorithms, state transitions |
| Architecture | Structure solution | Components, interfaces |
| Refinement | Iterate with TDD | Tests, implementation |
| Completion | Validate goal | Deployment, metrics |

### Code State Analysis

```javascript
current_state = {
  test_coverage: 45,
  performance_score: 'C',
  tech_debt_hours: 120,
  features_complete: ['auth', 'user-mgmt'],
  bugs_open: 23
}

goal_state = {
  test_coverage: 80,
  performance_score: 'A',
  tech_debt_hours: 40,
  features_complete: [...current, 'payments', 'notifications'],
  bugs_open: 5
}
```

### Milestone Definition

```typescript
interface CodeMilestone {
  id: string;
  description: string;
  sparc_phase: 'specification' | 'pseudocode' | 'architecture' | 'refinement' | 'completion';
  preconditions: string[];
  deliverables: string[];
  success_criteria: Metric[];
  estimated_hours: number;
  dependencies: string[];
}
```

## Implementation Pattern

```typescript
class SPARCGoalPlanner {
  async achieveGoal(goal: CodeGoal): Promise<GoalResult> {
    // 1. SPECIFICATION: Define goal state
    const spec = await this.specifyGoal(goal);

    // 2. PSEUDOCODE: Plan action sequence
    const actionPlan = await this.planActions(spec);

    // 3. ARCHITECTURE: Structure solution
    const architecture = await this.designArchitecture(actionPlan);

    // 4. REFINEMENT: Iterate with TDD
    const implementation = await this.refineWithTDD(architecture);

    // 5. COMPLETION: Validate and deploy
    return await this.completeGoal(implementation, spec);
  }

  async findOptimalPath(
    currentState: CodeState,
    goalState: CodeState
  ): Promise<ActionPlan> {
    const actions = this.getAvailableSPARCActions();
    return this.aStarSearch(currentState, goalState, actions);
  }
}
```

## Configuration

```yaml
sparc_goap_config:
  phases:
    specification:
      command: "npx claude-flow sparc run spec-pseudocode"
      timeout_minutes: 30

    architecture:
      command: "npx claude-flow sparc run architect"
      timeout_minutes: 45

    refinement:
      command: "npx claude-flow sparc tdd"
      timeout_minutes: 120

    completion:
      command: "npx claude-flow sparc run integration"
      timeout_minutes: 60

  metrics:
    test_coverage_target: 80
    performance_target: "A"
    max_tech_debt_hours: 40

  risk_assessment:
    technical_weight: 0.3
    timeline_weight: 0.3
    quality_weight: 0.2
    security_weight: 0.2
```

## Usage Examples

### Example 1: Feature Implementation Plan

```yaml
goal: implement_payment_processing_with_sparc

sparc_phases:
  specification:
    command: "npx claude-flow sparc run spec-pseudocode 'payment processing'"
    deliverables:
      - requirements_doc
      - acceptance_criteria
      - test_scenarios
    success_criteria:
      - all_payment_types_defined
      - security_requirements_clear
      - compliance_standards_identified

  pseudocode:
    command: "npx claude-flow sparc run pseudocode 'payment flow algorithms'"
    deliverables:
      - payment_flow_logic
      - error_handling_patterns
      - state_machine_design

  architecture:
    command: "npx claude-flow sparc run architect 'payment system design'"
    deliverables:
      - system_components
      - api_contracts
      - database_schema

  refinement:
    command: "npx claude-flow sparc tdd 'payment feature'"
    deliverables:
      - unit_tests
      - integration_tests
      - implemented_features
    success_criteria:
      - test_coverage_80_percent
      - all_tests_passing

  completion:
    command: "npx claude-flow sparc run integration 'deploy payment system'"
    deliverables:
      - deployed_system
      - documentation
      - monitoring_setup

goap_milestones:
  - setup_payment_provider:
      sparc_phase: specification
      preconditions: [api_keys_configured]
      deliverables: [provider_client, test_environment]
      success_criteria: [can_create_test_charge]

  - implement_checkout_flow:
      sparc_phase: refinement
      preconditions: [payment_provider_ready, ui_framework_setup]
      deliverables: [checkout_component, payment_form]
      success_criteria: [form_validation_works, ui_responsive]

  - add_webhook_handling:
      sparc_phase: completion
      preconditions: [server_endpoints_available]
      deliverables: [webhook_endpoint, event_processor]
      success_criteria: [handles_all_event_types, idempotent_processing]
```

### Example 2: Performance Optimization Goal

```yaml
goal: reduce_api_latency_50_percent

analysis:
  - profile_current_performance:
      tools: [profiler, APM, database_explain]
      metrics: [p50_latency, p99_latency, throughput]

optimizations:
  - database_query_optimization:
      sparc_phase: refinement
      actions: [add_indexes, optimize_joins, implement_pagination]
      expected_improvement: 30%
      success_metric: "p99 < 100ms"

  - implement_caching_layer:
      sparc_phase: architecture
      actions: [redis_setup, cache_warming, invalidation_strategy]
      expected_improvement: 25%

  - code_optimization:
      sparc_phase: refinement
      actions: [algorithm_improvements, parallel_processing, batch_operations]
      expected_improvement: 15%
```

### Example 3: Testing Strategy Goal

```yaml
goal: achieve_80_percent_coverage
current_coverage: 45

test_pyramid:
  unit_tests:
    target: 60%
    sparc_phase: refinement
    focus: [business_logic, utilities, validators]

  integration_tests:
    target: 25%
    sparc_phase: completion
    focus: [api_endpoints, database_operations, external_services]

  e2e_tests:
    target: 15%
    sparc_phase: completion
    focus: [critical_user_journeys, payment_flow, authentication]

milestones:
  - milestone_55:
      actions: [add_unit_tests_for_core_services]
      deadline: "week 1"

  - milestone_65:
      actions: [add_integration_tests_for_api]
      deadline: "week 2"

  - milestone_80:
      actions: [add_e2e_tests, increase_unit_coverage]
      deadline: "week 3"
```

## Execution Checklist

- [ ] Analyze current code state (coverage, performance, debt)
- [ ] Define goal state with measurable criteria
- [ ] Map goal to SPARC phases
- [ ] Generate GOAP milestones for each phase
- [ ] Estimate effort and dependencies
- [ ] Execute SPARC commands for each phase
- [ ] Track metrics throughout execution
- [ ] Validate goal achievement with success criteria
- [ ] Document patterns for future goals

## Best Practices

- **Measurable Goals**: Every goal needs quantifiable success criteria
- **Phase Alignment**: Map GOAP actions to appropriate SPARC phases
- **TDD Integration**: Use refinement phase for test-first development
- **Incremental Progress**: Track metrics at each milestone
- **Risk Assessment**: Evaluate technical, timeline, quality, security risks
- **Pattern Learning**: Store successful plans for reuse

## Error Handling

### Goal Infeasibility

```typescript
// Goal cannot be achieved with available resources
if (!canAchieveGoal(currentState, goalState, constraints)) {
  // Suggest achievable subset
  const achievableGoal = findMaximalAchievableSubset(goalState);
  console.log(`Full goal not achievable. Suggested: ${achievableGoal}`);

  // Identify blocking constraints
  const blockers = identifyBlockers(goalState);
  console.log(`Blocked by: ${blockers}`);
}
```

### Phase Failures

```typescript
// SPARC phase did not complete successfully
if (phaseResult.failed) {
  // Identify specific failures
  const failures = phaseResult.failedCriteria;

  // Attempt retry with adjusted parameters
  if (canRetry(failures)) {
    await retryPhase(phase, adjustedConfig);
  } else {
    // Replan from current state
    await replanFromPhase(phase);
  }
}
```

## Metrics & Success Criteria

### Code Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cyclomatic Complexity | < 10 | Per function |
| Code Duplication | < 3% | Codebase-wide |
| Test Coverage | > 80% | Line coverage |
| Technical Debt Ratio | < 5% | SonarQube |

### Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response Time (p99) | < 200ms | APM |
| Throughput | > 1000 req/s | Load test |
| Error Rate | < 0.1% | Monitoring |
| Availability | > 99.9% | Uptime |

### Delivery Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Lead Time | < 1 day | Deploy tracking |
| Deploy Frequency | > 1/day | CI/CD |
| MTTR | < 1 hour | Incident tracking |
| Change Failure Rate | < 5% | Rollback rate |

## Integration Points

### MCP Tools

```javascript
// Initialize SPARC-enhanced swarm
mcp__claude-flow__swarm_init({
  topology: "hierarchical",
  maxAgents: 5
});

// Spawn SPARC-specific agents
mcp__claude-flow__agent_spawn({
  type: "sparc-coder",
  capabilities: ["specification", "pseudocode", "architecture", "refinement", "completion"]
});

// Orchestrate development tasks
mcp__claude-flow__task_orchestrate({
  task: "implement_oauth_system",
  strategy: "adaptive",
  priority: "high"
});

// Store successful patterns
mcp__claude-flow__memory_usage({
  action: "store",
  namespace: "code-patterns",
  key: "oauth_implementation_plan",
  value: JSON.stringify(successfulPlan)
});
```

### SPARC Commands

```bash
# Full SPARC-GOAP workflow
npx claude-flow sparc run spec-pseudocode "user authentication feature"
npx claude-flow sparc run architect "authentication system design"
npx claude-flow sparc tdd "authentication feature" --track-goals
npx claude-flow sparc run integration "deploy authentication" --validate-goals
npx claude-flow sparc verify "authentication feature complete"

# Batch processing
npx claude-flow sparc batch spec,arch,refine "user management system"
npx claude-flow sparc concurrent tdd tasks.json
```

### Related Skills

- [planning-goal](../planning-goal/SKILL.md) - General GOAP planning
- [sparc-workflow](../../../workspace-hub/sparc-workflow/SKILL.md) - SPARC methodology
- [testing-tdd-london](../../testing/testing-tdd-london/SKILL.md) - TDD implementation

## References

- [SPARC Methodology](https://github.com/ruvnet/claude-flow)
- [GOAP in Game AI](https://en.wikipedia.org/wiki/Goal-oriented_action_planning)
- [TDD Best Practices](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from code-goal-planner agent
