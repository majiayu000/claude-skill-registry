---
name: measure
description: Quantify values with uncertainty bounds. Use when estimating metrics, calculating risk scores, assessing magnitude, or measuring any quantifiable property.
argument-hint: "[target] [metric] [unit]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Bash
context: fork
agent: explore
layer: UNDERSTAND
---

## Intent

Quantify a specific metric for a target, providing a numerical value with explicit uncertainty bounds. This capability consolidates all estimation tasks (risk, impact, effort, etc.) into a single parameterized operation.

**Success criteria:**
- Numerical value provided for requested metric
- Uncertainty bounds explicitly stated
- Measurement method documented
- Units clearly specified

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `target` | Yes | any | What to measure (system, code, entity, process) |
| `metric` | Yes | string | The metric to quantify (risk, complexity, effort, size, etc.) |
| `unit` | No | string | Unit of measurement (optional, inferred if not provided) |
| `method` | No | string | Measurement approach (heuristic, statistical, model-based) |

## Procedure

1) **Define the metric**: Clarify exactly what is being measured
   - Establish clear definition of the metric
   - Identify appropriate unit of measurement
   - Determine measurement methodology

2) **Gather measurement inputs**: Collect data needed for measurement
   - Read relevant files, logs, or data sources
   - Identify quantifiable indicators
   - Note data quality and completeness

3) **Calculate measurement**: Apply measurement method to inputs
   - Use appropriate calculation for the metric type
   - For risk: probability * impact assessment
   - For complexity: cyclomatic, cognitive, or structural metrics
   - For effort: decomposition and estimation techniques

4) **Establish uncertainty bounds**: Quantify measurement confidence
   - Calculate or estimate lower and upper bounds
   - Consider data quality, method limitations
   - Express as confidence interval or range

5) **Ground the measurement**: Document evidence and method
   - Reference specific data points used
   - Note any assumptions in calculation
   - Document measurement methodology

## Output Contract

Return a structured object:

```yaml
value: number  # The measured value
uncertainty:
  lower: number  # Lower bound (confidence interval)
  upper: number  # Upper bound (confidence interval)
  type: string  # Type of uncertainty (confidence_interval, range, std_dev)
unit: string  # Unit of measurement
metric: string  # What was measured
method: string  # How it was measured
breakdown:  # Optional component breakdown
  - component: string
    value: number
confidence: 0..1  # Confidence in measurement accuracy
evidence_anchors: ["file:line", "data:source"]
assumptions: []
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `value` | number | Primary measurement value |
| `uncertainty` | object | Bounds and type of uncertainty |
| `unit` | string | Unit of measurement |
| `metric` | string | Name of measured property |
| `method` | string | Measurement methodology used |
| `breakdown` | array | Optional decomposition of measurement |

## Examples

### Example 1: Measure Code Complexity

**Input:**
```yaml
target: "src/services/order_processor.rb"
metric: "complexity"
unit: "cyclomatic"
```

**Output:**
```yaml
value: 24
uncertainty:
  lower: 22
  upper: 26
  type: "range"
unit: "cyclomatic complexity"
metric: "complexity"
method: "counted decision points (if, case, loops, &&, ||)"
breakdown:
  - component: "process_order method"
    value: 12
  - component: "validate_items method"
    value: 8
  - component: "calculate_totals method"
    value: 4
confidence: 0.9
evidence_anchors:
  - "src/services/order_processor.rb:15-120"
assumptions:
  - "Ruby control flow statements counted as decision points"
  - "Exception handling counted as branches"
```

### Example 2: Measure Risk

**Input:**
```yaml
target: "database migration: add user_preferences column"
metric: "risk"
method: "probability_impact"
```

**Output:**
```yaml
value: 0.35
uncertainty:
  lower: 0.25
  upper: 0.50
  type: "confidence_interval_90"
unit: "risk score (0-1)"
metric: "risk"
method: "probability (0.5) * impact (0.7) normalized"
breakdown:
  - component: "probability_of_failure"
    value: 0.5
  - component: "impact_if_failed"
    value: 0.7
  - component: "data_loss_risk"
    value: 0.2
  - component: "downtime_risk"
    value: 0.4
confidence: 0.7
evidence_anchors:
  - "migrations/20240115_add_preferences.rb:1-25"
  - "tool:grep:similar_migrations"
assumptions:
  - "Table has ~1M rows based on user count"
  - "Migration will lock table during ALTER"
  - "No concurrent deployments during migration"
```

## Verification

- [ ] Numerical value provided
- [ ] Uncertainty bounds are reasonable (lower < value < upper)
- [ ] Unit of measurement specified
- [ ] Method documented
- [ ] Evidence anchors reference measurement inputs

**Verification tools:** Read (to verify measurement inputs)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Always provide uncertainty bounds, never claim false precision
- Document measurement methodology for reproducibility
- Flag when data is insufficient for reliable measurement
- Do not extrapolate beyond available data without noting assumptions

## Composition Patterns

**Commonly follows:**
- `observe` - Measure properties of observed state
- `detect` - Measure characteristics of detected items
- `retrieve` - Measure retrieved data

**Commonly precedes:**
- `predict` - Measurements feed into predictions
- `compare` - Measurements enable quantitative comparison
- `plan` - Measurements inform risk-aware planning

**Anti-patterns:**
- Never use measure for binary detection (use `detect`)
- Avoid measure for categorical assessment (use `classify`)

**Workflow references:**
- See `reference/workflow_catalog.yaml#digital_twin_sync_loop` for risk measurement
