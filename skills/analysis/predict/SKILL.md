---
name: predict
description: Forecast future states or outcomes based on current data and trends. Use when estimating future values, projecting trajectories, forecasting outcomes, or anticipating system behavior.
argument-hint: "[target] [horizon] [conditions]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
layer: UNDERSTAND
---

## Intent

Forecast future states or outcomes for a target based on current state, historical patterns, and assumed conditions. This capability consolidates all forecasting tasks (risk, impact, time, etc.) into a single parameterized operation.

**Success criteria:**
- Prediction for requested target and horizon provided
- Probability or confidence assigned to prediction
- Alternative outcomes considered
- Assumptions explicitly stated

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `target` | Yes | string | What to predict (metric, state, outcome, event) |
| `horizon` | No | string | Prediction timeframe (e.g., "1 week", "next release", "end of sprint") |
| `conditions` | No | object | Assumed conditions for prediction |
| `method` | No | string | Prediction approach (trend, model, heuristic) |

## Procedure

1) **Define prediction target**: Clarify what outcome is being predicted
   - Specify the metric, state, or event to forecast
   - Establish the prediction horizon
   - Note any boundary conditions

2) **Gather historical data**: Collect relevant past observations
   - Identify patterns and trends
   - Note data quality and coverage
   - Look for relevant precedents

3) **Establish conditions**: Document assumptions about the future
   - Note what must remain constant
   - Identify key variables that could change
   - Consider external factors

4) **Generate prediction**: Forecast the most likely outcome
   - Apply trend analysis or modeling
   - Calculate probability of primary prediction
   - Identify alternative outcomes

5) **Consider alternatives**: Evaluate other possible outcomes
   - List plausible alternative scenarios
   - Assign rough probabilities to alternatives
   - Note what would cause each alternative

6) **Ground prediction**: Document evidence and reasoning
   - Reference data supporting the prediction
   - Note the reasoning chain
   - Explicitly state all assumptions

## Output Contract

Return a structured object:

```yaml
prediction:
  outcome: any  # Predicted value, state, or event
  probability: number  # 0.0-1.0 likelihood of this outcome
  horizon: string  # When this prediction applies
alternatives:
  - outcome: any  # Alternative outcome
    probability: number  # Likelihood
    trigger: string  # What would cause this
trajectory:  # Optional: predicted path to outcome
  - timestamp: string
    state: any
reasoning: string  # Explanation of prediction logic
confidence: 0..1  # Confidence in prediction methodology
evidence_anchors: ["file:line", "data:source"]
assumptions: []  # Critical assumptions
invalidation_conditions: []  # What would invalidate this prediction
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `prediction.outcome` | any | The predicted future state or value |
| `prediction.probability` | number | Likelihood of primary outcome |
| `prediction.horizon` | string | Timeframe for prediction |
| `alternatives` | array | Other possible outcomes with triggers |
| `trajectory` | array | Path from current to predicted state |
| `reasoning` | string | Explanation of prediction logic |
| `invalidation_conditions` | array | What would make prediction invalid |

## Examples

### Example 1: Predict Sprint Completion

**Input:**
```yaml
target: "sprint story completion"
horizon: "end of sprint (5 days)"
conditions:
  team_size: 4
  no_major_blockers: true
```

**Output:**
```yaml
prediction:
  outcome: "7 of 10 stories completed (70%)"
  probability: 0.65
  horizon: "end of sprint (5 days)"
alternatives:
  - outcome: "10 of 10 stories completed (100%)"
    probability: 0.15
    trigger: "No unexpected blockers, all estimates accurate"
  - outcome: "5 of 10 stories completed (50%)"
    probability: 0.20
    trigger: "Major blocker or team member unavailable"
trajectory:
  - timestamp: "Day 2"
    state: "3 stories completed"
  - timestamp: "Day 4"
    state: "5-6 stories completed"
  - timestamp: "Day 5"
    state: "7 stories completed"
reasoning: "Based on team velocity of 1.5 stories/day and current progress, projecting linear completion. Historical sprints show 70% completion rate."
confidence: 0.7
evidence_anchors:
  - "tool:jira:sprint-history"
  - "tool:jira:current-burndown"
assumptions:
  - "Team velocity remains consistent"
  - "Story estimates are accurate"
  - "No unplanned work introduced"
invalidation_conditions:
  - "Team member becomes unavailable"
  - "Critical production incident"
  - "Scope change to sprint"
```

### Example 2: Predict System Failure

**Input:**
```yaml
target: "disk space exhaustion"
horizon: "next 30 days"
conditions:
  growth_rate: "current trend"
```

**Output:**
```yaml
prediction:
  outcome: "Disk will reach 95% capacity"
  probability: 0.85
  horizon: "18-22 days"
alternatives:
  - outcome: "Disk reaches 100% (service outage)"
    probability: 0.60
    trigger: "No cleanup or expansion action taken"
  - outcome: "Capacity remains stable"
    probability: 0.10
    trigger: "Log rotation reduces growth rate"
trajectory:
  - timestamp: "Day 7"
    state: "85% capacity"
  - timestamp: "Day 14"
    state: "90% capacity"
  - timestamp: "Day 20"
    state: "95% capacity"
reasoning: "Current growth rate of 0.5% per day on 80% utilized 500GB disk. Linear projection shows critical threshold in ~20 days."
confidence: 0.8
evidence_anchors:
  - "command:df -h /data"
  - "tool:monitoring:disk-trend-7d"
assumptions:
  - "Growth rate continues at current pace"
  - "No bulk data imports or exports"
  - "Log retention policy unchanged"
invalidation_conditions:
  - "Growth rate changes significantly"
  - "Disk expanded or data archived"
  - "Application behavior changes"
```

## Verification

- [ ] Prediction includes specific outcome and probability
- [ ] Horizon is clearly specified
- [ ] At least one alternative outcome considered
- [ ] Assumptions are explicitly documented
- [ ] Evidence supports the prediction reasoning

**Verification tools:** Read (to verify historical data references)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Always provide probability, never claim certainty about future
- Document assumptions that could invalidate prediction
- Consider alternative outcomes, especially failure modes
- Do not predict beyond available data horizon without noting extrapolation
- Flag when prediction confidence is too low to be actionable

## Composition Patterns

**Commonly follows:**
- `measure` - Measurements provide basis for predictions
- `observe` - Current state observations inform predictions
- `discover` - Discovered patterns enable predictions

**Commonly precedes:**
- `plan` - Predictions inform planning decisions
- `compare` - Predicted outcomes can be compared
- `simulate` - Predictions guide simulation scenarios

**Anti-patterns:**
- Never use predict for current state (use `measure` or `observe`)
- Avoid predict when historical data is insufficient

**Workflow references:**
- See `reference/workflow_catalog.yaml#digital_twin_sync_loop` for forecasting in digital twins
