---
name: attribute
description: Establish cause-effect relationships between events or states. Use when analyzing root causes, mapping dependencies, tracing effects, or building causal models.
argument-hint: "[effect] [candidates] [context]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
layer: MODEL
---

## Intent

Establish causal relationships between observed effects and potential causes. This capability supports root cause analysis, dependency mapping, and causal reasoning for planning and debugging.

**Success criteria:**
- Causes identified for observed effects
- Causal strength estimated for each relationship
- Causal mechanism explained
- Alternative causes considered and ruled out

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `effect` | Yes | any | The observed effect to attribute |
| `candidates` | No | array | Potential causes to evaluate |
| `context` | No | object | Situational context for attribution |
| `depth` | No | string | Analysis depth: immediate, chain, comprehensive |

## Procedure

1) **Characterize the effect**: Understand what needs to be explained
   - Document the observed effect precisely
   - Note timing and circumstances
   - Identify what changed

2) **Identify candidate causes**: Generate list of potential causes
   - Use provided candidates if available
   - Generate additional candidates from context
   - Consider proximate and distal causes

3) **Evaluate causal strength**: Assess each candidate
   - Check temporal precedence (cause before effect)
   - Verify mechanism plausibility
   - Look for correlation evidence
   - Consider counterfactual (would effect occur without cause?)

4) **Trace causal chain**: Map the path from cause to effect
   - Identify intermediate steps
   - Note amplifying or dampening factors
   - Document the causal mechanism

5) **Rule out alternatives**: Eliminate unlikely causes
   - Document why alternatives are less likely
   - Note any confounding factors
   - Flag when multiple causes may contribute

6) **Quantify confidence**: Assess attribution certainty
   - Rate strength of causal evidence
   - Note missing evidence
   - Identify what would confirm/refute attribution

## Output Contract

Return a structured object:

```yaml
causes:
  - cause: string  # Identified cause
    strength: number  # 0.0-1.0 causal strength
    mechanism: string  # How cause produces effect
    evidence: array[string]  # Supporting evidence
    type: string  # direct, contributing, enabling
strengths:  # Comparative strengths
  cause_1: number
  cause_2: number
causal_chain:
  - step: string  # Intermediate step
    from: string  # Prior state/event
    to: string  # Resulting state/event
alternatives_ruled_out:
  - cause: string
    reason: string  # Why ruled out
confidence: 0..1
evidence_anchors: ["file:line", "log:entry"]
assumptions: []
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `causes` | array | Identified causes with strength and mechanism |
| `causes[].strength` | number | Causal strength (0-1) |
| `causes[].mechanism` | string | Explanation of causal pathway |
| `causes[].type` | string | Direct, contributing, or enabling cause |
| `causal_chain` | array | Steps from cause to effect |
| `alternatives_ruled_out` | array | Rejected alternatives with reasons |

## Examples

### Example 1: Attribute Performance Degradation

**Input:**
```yaml
effect: "API response time increased from 200ms to 2000ms"
candidates:
  - "recent deployment"
  - "database load increase"
  - "memory leak"
context:
  timing: "started 2024-01-15 14:30"
  affected: "/api/users endpoint"
```

**Output:**
```yaml
causes:
  - cause: "N+1 query introduced in recent deployment"
    strength: 0.85
    mechanism: "New eager loading removed; each user now triggers 3 additional queries"
    evidence:
      - "Deployment at 14:25, issue started 14:30"
      - "Query count per request increased from 2 to 50+"
      - "Database CPU correlates with API latency"
    type: "direct"
  - cause: "Database connection pool saturation"
    strength: 0.40
    mechanism: "Increased queries exhaust connection pool, causing wait times"
    evidence:
      - "Pool utilization at 95%"
      - "Connection wait time increased"
    type: "contributing"
strengths:
  n_plus_1_query: 0.85
  connection_pool: 0.40
  memory_leak: 0.05
causal_chain:
  - step: "Code deployed"
    from: "eager_load(:profile)"
    to: "no eager loading"
  - step: "Query multiplication"
    from: "2 queries/request"
    to: "50+ queries/request"
  - step: "Database overload"
    from: "normal CPU"
    to: "90% CPU"
  - step: "Response delay"
    from: "200ms"
    to: "2000ms"
alternatives_ruled_out:
  - cause: "memory leak"
    reason: "Memory usage stable, no growth pattern"
  - cause: "external service latency"
    reason: "No external calls in affected endpoint"
confidence: 0.85
evidence_anchors:
  - "git log --since='2024-01-15 14:00'"
  - "app/models/user.rb:45 (diff)"
  - "monitoring:query_count"
  - "monitoring:db_cpu"
assumptions:
  - "Monitoring data is accurate"
  - "No other deployments in window"
```

### Example 2: Attribute Test Failure

**Input:**
```yaml
effect: "UserService#create test failing with 'Email already taken'"
candidates:
  - "test data pollution"
  - "code change"
  - "database state"
```

**Output:**
```yaml
causes:
  - cause: "Missing database cleanup between tests"
    strength: 0.90
    mechanism: "Test creates user, doesn't clean up, subsequent test finds duplicate"
    evidence:
      - "Test passes in isolation"
      - "Test fails when run after create_user_test"
      - "No database_cleaner configuration"
    type: "direct"
strengths:
  test_pollution: 0.90
  code_change: 0.05
  fixture_issue: 0.05
causal_chain:
  - step: "First test runs"
    from: "empty database"
    to: "user 'test@example.com' exists"
  - step: "Second test attempts create"
    from: "user exists"
    to: "uniqueness validation fails"
alternatives_ruled_out:
  - cause: "code change"
    reason: "No recent changes to UserService"
  - cause: "fixture issue"
    reason: "Test doesn't use fixtures"
confidence: 0.90
evidence_anchors:
  - "spec/services/user_service_spec.rb:45"
  - "spec/rails_helper.rb (no database_cleaner)"
  - "command:rspec spec/services/user_service_spec.rb:45 --order defined"
assumptions:
  - "Test failure is deterministic with this order"
  - "No parallel test execution"
```

## Verification

- [ ] At least one cause identified with strength > 0.3
- [ ] Mechanism explains how cause produces effect
- [ ] Temporal precedence verified (cause before effect)
- [ ] Alternative causes considered
- [ ] Evidence supports attribution

**Verification tools:** Read, Grep (to verify evidence)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Distinguish correlation from causation
- Consider multiple causes (multi-causality)
- Note when attribution is uncertain
- Do not assume causation without mechanism

## Composition Patterns

**Commonly follows:**
- `detect` - Detect anomalies then attribute causes
- `observe` - Observations reveal effects to attribute
- `measure` - Measurements quantify effects

**Commonly precedes:**
- `plan` - Causal understanding informs remediation
- `explain` - Attribution enables explanation
- `critique` - Causal model enables critique

**Anti-patterns:**
- Never use attribute for prediction (use `predict`)
- Avoid attribution without sufficient evidence

**Workflow references:**
- See `reference/workflow_catalog.yaml#debug_code_change` for attribution in debugging
- See `reference/workflow_catalog.yaml#world_model_build` for causal modeling
