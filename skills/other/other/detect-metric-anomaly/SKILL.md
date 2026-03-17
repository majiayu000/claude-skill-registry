---
name: detect-metric-anomaly
version: "1.0.0"
description: >
  Analyze a metric for statistical anomalies using z-score analysis and threshold
  checking. Detects spikes, drops, and trends. Use for proactive monitoring and
  early warning. Keywords: anomaly, detection, metric, z-score, threshold, alert,
  statistical.
metadata:
  domain: general
  category: analytics
  requires-approval: false
  confidence: 0.85
  mcp-servers: []
---

# Detect Metric Anomaly

## Preconditions

Before applying this skill, verify:

- Metric name and current value available
- Historical baseline exists (or can be established)
- Threshold configuration available

## Actions

### 1. Retrieve Baseline Statistics

Get or calculate baseline from history:
```yaml
metric: $metric_name
window_size: 1000  # Last N data points
statistics:
  - mean
  - std_dev
  - percentile_95
```

### 2. Calculate Z-Score

Determine how far current value deviates from baseline:
```python
z_score = (current_value - baseline.mean) / baseline.std_dev
```

Interpret z-score:
- |z| < 2: Normal variation
- 2 <= |z| < 3: Warning (unusual)
- |z| >= 3: Critical (anomaly)

### 3. Check Absolute Thresholds

Compare against configured thresholds:
```yaml
cpu_percent:
  warning: 80
  critical: 95
memory_percent:
  warning: 80
  critical: 90
error_rate:
  warning: 0.01
  critical: 0.05
```

### 4. Detect Trends

Analyze recent window for sustained deviation:
```python
if 80% of last 10 values > baseline.mean:
    trend = "increasing"
elif 80% of last 10 values < baseline.mean:
    trend = "decreasing"
else:
    trend = "stable"
```

### 5. Generate Alert

If anomaly detected:
```yaml
alert:
  metric: $metric_name
  severity: $calculated_severity
  type: $anomaly_type  # spike, drop, trend
  z_score: $z_score
  current_value: $current_value
  baseline_mean: $mean
  recommendation: $suggested_action
```

## Success Criteria

The skill succeeds when:

- [ ] Metric analyzed against baseline
- [ ] Z-score calculated correctly
- [ ] Alert generated if anomaly present

## Failure Handling

If analysis fails:

1. Insufficient data: Wait for more samples
2. No baseline: Initialize with current values
3. Calculation error: Log and skip this check

## Examples

**Input Context:**
```json
{
  "metric": "cpu_percent",
  "current_value": 92,
  "node": "worker-1"
}
```

**Expected Output:**
```json
{
  "anomaly_detected": true,
  "severity": "warning",
  "type": "threshold_breach",
  "z_score": 2.3,
  "baseline_mean": 45,
  "baseline_std_dev": 15,
  "percentile_rank": 97,
  "recommendation": "Investigate high CPU usage on worker-1"
}
```
