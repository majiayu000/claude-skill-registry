---
name: framework-health
description: "Evaluate Mycelium's own process effectiveness. Measures cycle velocity, discard trends, confidence calibration, gate effectiveness, regression rate. Run quarterly or every 20 cycles."
instruction_budget: 42
---

# Framework Health Check

Mycelium evaluates its own process. This is triple-loop learning — the framework assessing whether it is getting better at producing good outcomes.

## When to Use

- Quarterly review (scheduled)
- After 20 completed leaf cycles (triggered by cycle-history.yml count)
- When process friction is suspected
- Before major framework changes (baseline measurement)

## Workflow

### 1. Load Cycle Data

Read `canvas/cycle-history.yml`. If fewer than 5 cycles recorded, report:
"Insufficient cycle data for framework health assessment. [N] cycles recorded; minimum 5 needed. Continue recording outcomes."

### 2. Measure Five Dimensions

For each dimension, compute the metric and compare against trend (if prior assessments exist):

**Cycle Velocity**:
- Average days from diamond creation to completion, grouped by scale
- Trend: improving / stable / degrading
- If degrading: flag for investigation

**Discard Rate**:
- Count of discards per lifecycle phase
- Average discard phase (1-10 scale)
- Trend: shifting earlier (good) / shifting later (bad) / stable
- If >50% of discards at Phase 7+: flag "late discard pattern"

**Confidence Calibration**:
- For all cycles with predicted confidence and actual outcome:
  - Compute: actual success rate per confidence band (0.3-0.5, 0.5-0.7, 0.7-0.9)
  - Compare with expected rate (confidence 0.7 should succeed ~70%)
  - Report calibration factor: actual/expected
- If calibration factor < 0.8 or > 1.2: flag miscalibration

**Gate Effectiveness**:
- For each theory gate, count: times checked, times passed, times failed
- Compute hit rate: failures / total checks
- Flag rubber stamps (0% failure rate) and hard blocks (>80% failure rate)

**Regression Rate**:
- Count diamonds that regressed at least once / total diamonds
- Trend: decreasing (good) / increasing (bad) / stable

### 3. Run Threshold Calibration

If cycle count ≥ minimum_n for any threshold in `canvas/thresholds.yml`:
- Apply calibration rules from `engine/adaptive-thresholds.md`
- Update calibrated values
- Log changes in decision-log.md

### 4. Check Goodhart Counter-Metrics

For each dimension, verify the counter-metric is not degrading:
- Velocity improving BUT outcome quality declining? Flag.
- Earlier discards BUT false positive rate rising? Flag.
- Better calibration BUT decision speed dropping? Flag.

### 5. Generate Dashboard

## Output

```
## Framework Health Dashboard

Assessment date: [date]
Cycles analyzed: [N]
Period: [date range]

### Dimensions

| Dimension | Current | Trend | Status | Counter-Metric |
|-----------|---------|-------|--------|----------------|
| Cycle velocity | [X days avg] | [improving/stable/degrading] | [healthy/warning/critical] | Outcome quality: [OK/degrading] |
| Discard rate | [avg phase X] | [earlier/stable/later] | [healthy/warning/critical] | False positive rate: [OK/rising] |
| Confidence calibration | [factor X.XX] | [improving/stable/diverging] | [healthy/warning/critical] | Decision speed: [OK/slowing] |
| Gate effectiveness | [see detail] | — | [healthy/warning/critical] | Flow speed: [OK/slowing] |
| Regression rate | [X%] | [decreasing/stable/increasing] | [healthy/warning/critical] | Innovation rate: [OK/declining] |

### Threshold Calibration

| Threshold | Default | Calibrated | Based On | Change |
|-----------|---------|-----------|----------|--------|
| ICE advance | 100 | [value or "insufficient data"] | N cycles | [+/-] |
| Confidence factor | 1.0 | [value or "insufficient data"] | N cycles | [+/-] |
| Bakeoff delta | 20% | [value or "insufficient data"] | N bakeoffs | [+/-] |

### Pattern Signals Active

[List any active pattern detector signals from engine/pattern-detector.md]

### Recommendations

[Specific actions based on findings — not generic advice]
```

## Rules

- Never modify thresholds without sufficient data (respect minimum_n)
- Always check counter-metrics before celebrating improvement
- Log all threshold changes in decision-log.md
- If all dimensions are healthy, say so and suggest next review date

## Theory Citations

- Argyris: Triple-loop learning (learning how to learn)
- Forsgren: Accelerate (measuring capabilities, not just outputs)
- Goodhart: Counter-metrics for every metric
- Deming: Statistical process control (data-driven threshold adjustment)
