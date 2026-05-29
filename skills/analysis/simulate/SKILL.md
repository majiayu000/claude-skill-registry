---
name: simulate
description: Run what-if scenarios to explore outcomes and test hypotheses. Use when evaluating alternatives, stress-testing designs, exploring edge cases, or predicting system behavior under different conditions.
argument-hint: "[scenario] [initial_state] [steps]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Bash
context: fork
agent: explore
layer: MODEL
---

## Intent

Execute mental simulations of scenarios to explore outcomes without making real changes. This capability enables safe exploration of "what-if" questions and helps identify risks before action.

**Success criteria:**
- Scenario executed through logical steps
- Multiple outcomes considered
- Key decision points identified
- Assumptions made explicit

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `scenario` | Yes | object | Scenario to simulate (intervention, change, event) |
| `initial_state` | No | object | Starting state for simulation |
| `steps` | No | integer | Number of simulation steps/iterations |
| `explore` | No | string | What to explore: single_path, branches, exhaustive |

## Procedure

1) **Set up scenario**: Define what is being simulated
   - Clarify the intervention or change being tested
   - Establish initial conditions
   - Define simulation boundaries

2) **Initialize state**: Establish starting point
   - Use provided initial_state or current system state
   - Validate state is consistent
   - Note any simplifications

3) **Execute simulation**: Step through scenario
   - Apply changes specified in scenario
   - Propagate effects through state
   - Track state at each step

4) **Explore branches**: Consider alternative paths
   - Identify decision points
   - Explore likely alternative outcomes
   - Note probability of each branch

5) **Evaluate outcomes**: Assess simulation results
   - Compare final states across branches
   - Identify risks and opportunities
   - Note unexpected behaviors

6) **Document simulation**: Record process and results
   - List assumptions made
   - Note limitations of simulation
   - Provide evidence for conclusions

## Output Contract

Return a structured object:

```yaml
outcomes:
  - branch_id: string  # Unique branch identifier
    probability: number  # Estimated likelihood
    final_state: object  # State after simulation
    key_events: array[string]  # Notable events during simulation
    risks: array[string]  # Identified risks
trajectory:
  - step: number
    state: object  # State at this step
    changes: array[string]  # What changed
final_state: object  # Most likely final state
insights:
  - type: string  # risk, opportunity, surprise
    description: string
    severity: string  # low, medium, high
simulation_meta:
  steps_executed: number
  branches_explored: number
  assumptions: array[string]
confidence: 0..1
evidence_anchors: ["model:component", "assumption:id"]
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `outcomes` | array | Possible outcomes with probabilities |
| `trajectory` | array | State changes over simulation |
| `final_state` | object | Most likely end state |
| `insights` | array | Risks, opportunities, and surprises found |
| `simulation_meta` | object | Simulation parameters and assumptions |

## Examples

### Example 1: Simulate Dependency Upgrade

**Input:**
```yaml
scenario:
  type: "dependency_upgrade"
  change: "Upgrade Rails from 6.1 to 7.0"
initial_state:
  rails_version: "6.1.7"
  ruby_version: "3.1.0"
  gems_count: 85
steps: 5
```

**Output:**
```yaml
outcomes:
  - branch_id: "success_path"
    probability: 0.60
    final_state:
      rails_version: "7.0.8"
      breaking_changes_resolved: true
      tests_passing: true
    key_events:
      - "ActiveStorage API changes detected"
      - "Zeitwerk autoloading adjustments needed"
      - "Deprecation warnings resolved"
    risks:
      - "Minor performance regression in asset pipeline"
  - branch_id: "partial_failure"
    probability: 0.30
    final_state:
      rails_version: "7.0.8"
      breaking_changes_resolved: true
      tests_passing: false
    key_events:
      - "ActiveRecord callback order changed"
      - "3 test failures in UserService"
    risks:
      - "Subtle behavior changes in model callbacks"
      - "Extended debugging time required"
  - branch_id: "blocked"
    probability: 0.10
    final_state:
      rails_version: "6.1.7"
      upgrade_blocked: true
    key_events:
      - "Incompatible gem: devise_token_auth requires Rails < 7"
    risks:
      - "Upgrade blocked until gem updated"
trajectory:
  - step: 1
    state: { phase: "analysis" }
    changes: ["Identified 12 deprecation warnings", "Found 3 incompatible gems"]
  - step: 2
    state: { phase: "gem_updates" }
    changes: ["Updated 8 gems", "1 gem requires replacement"]
  - step: 3
    state: { phase: "code_changes" }
    changes: ["Modified 15 files for API changes"]
  - step: 4
    state: { phase: "testing" }
    changes: ["Tests executed", "85% passing initially"]
  - step: 5
    state: { phase: "resolution" }
    changes: ["Fixed remaining issues"]
final_state:
  rails_version: "7.0.8"
  breaking_changes_resolved: true
  tests_passing: true
  effort_estimate: "2-3 days"
insights:
  - type: "risk"
    description: "devise_token_auth compatibility is the main blocker"
    severity: "high"
  - type: "opportunity"
    description: "Rails 7 Hotwire enables simpler frontend code"
    severity: "medium"
  - type: "surprise"
    description: "More callback order dependencies than expected"
    severity: "medium"
simulation_meta:
  steps_executed: 5
  branches_explored: 3
  assumptions:
    - "Test suite provides good coverage"
    - "No undocumented monkey patches"
    - "CI environment matches production"
confidence: 0.75
evidence_anchors:
  - "Gemfile:dependencies"
  - "rails upgrade guide:7.0"
  - "gem:devise_token_auth:compatibility"
```

### Example 2: Simulate Failure Scenario

**Input:**
```yaml
scenario:
  type: "failure_injection"
  change: "Database becomes unavailable for 5 minutes"
initial_state:
  database: "available"
  cache: "warm"
  queue_depth: 0
steps: 10
explore: "branches"
```

**Output:**
```yaml
outcomes:
  - branch_id: "graceful_degradation"
    probability: 0.40
    final_state:
      service_status: "degraded"
      data_loss: false
      user_impact: "read_only_mode"
    key_events:
      - "Circuit breaker activates at t+30s"
      - "Cache serves stale reads"
      - "Writes queued for retry"
    risks:
      - "Cache expires during outage"
  - branch_id: "cascade_failure"
    probability: 0.35
    final_state:
      service_status: "down"
      data_loss: false
      user_impact: "complete_outage"
    key_events:
      - "Connection pool exhausted at t+60s"
      - "Health checks fail"
      - "Load balancer removes all instances"
    risks:
      - "Recovery requires manual intervention"
  - branch_id: "data_inconsistency"
    probability: 0.25
    final_state:
      service_status: "recovered"
      data_loss: "possible"
      user_impact: "partial_data_loss"
    key_events:
      - "In-flight transactions lost"
      - "Retry logic creates duplicates"
    risks:
      - "Data reconciliation needed"
trajectory:
  - step: 1
    state: { db: "available", errors: 0 }
    changes: []
  - step: 2
    state: { db: "unavailable", errors: "increasing" }
    changes: ["First connection timeout"]
  - step: 3
    state: { db: "unavailable", circuit: "open" }
    changes: ["Circuit breaker triggered"]
final_state:
  database: "available"
  service_status: "recovering"
  queue_depth: 1250
insights:
  - type: "risk"
    description: "No circuit breaker on write path"
    severity: "high"
  - type: "risk"
    description: "Connection pool timeout too long (30s)"
    severity: "medium"
  - type: "opportunity"
    description: "Add read replica failover"
    severity: "medium"
simulation_meta:
  steps_executed: 10
  branches_explored: 3
  assumptions:
    - "Database failure is total, not partial"
    - "No manual intervention during outage"
    - "Cache TTL is 5 minutes"
confidence: 0.65
evidence_anchors:
  - "config/database.yml:pool_settings"
  - "app/services/circuit_breaker.rb"
  - "architecture:failure_modes"
```

## Verification

- [ ] Scenario clearly defined
- [ ] At least one outcome path explored
- [ ] Probabilities assigned to outcomes
- [ ] Key assumptions documented
- [ ] Insights identify actionable findings

**Verification tools:** Read (to verify model components)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Simulation does not modify real state
- Note when model may be incomplete
- Flag high-uncertainty outcomes
- Do not present simulation as prediction

## Composition Patterns

**Commonly follows:**
- `state` - State model provides simulation basis
- `transition` - Transition rules drive simulation
- `plan` - Simulate plan outcomes before execution

**Commonly precedes:**
- `compare` - Compare simulation outcomes
- `plan` - Inform planning with simulation insights
- `critique` - Critique designs based on simulation

**Anti-patterns:**
- Never treat simulation as certainty (use `verify` for real testing)
- Avoid simulating without state/transition models

**Workflow references:**
- See `reference/workflow_catalog.yaml#world_model_build` for simulation in modeling
