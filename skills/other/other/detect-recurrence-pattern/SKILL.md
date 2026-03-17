---
name: detect-recurrence-pattern
version: "1.0.0"
description: >
  Detect recurring patterns in issues and events. Identifies temporal,
  resource-based, cluster, and cascading patterns. Suggests prevention
  strategies. Keywords: recurrence, pattern, detection, trending, recurring,
  prevention, issue, analysis.
metadata:
  domain: general
  category: analytics
  requires-approval: false
  confidence: 0.85
  mcp-servers: []
---

# Detect Recurrence Pattern

## Preconditions

Before applying this skill, verify:

- Issue records available for analysis
- Minimum 3 occurrences in analysis window
- Timestamp data available for temporal analysis

## Actions

### 1. Collect Issue Records

Gather issue data for analysis:
```yaml
issue_record:
  issue_type: string       # e.g., "CrashLoopBackOff", "OOMKilled"
  resource: string         # e.g., "pod/app-123"
  namespace: string        # e.g., "production"
  timestamp: datetime
  metadata: object
  resolved: boolean
```

### 2. Detect Resource Patterns

Group issues by base resource name:
```python
# Group by namespace/kind/base-name
by_base_name = group_issues_by_resource_base()

for key, group in by_base_name.items():
    if len(group) >= min_occurrences:
        # Pattern detected: same resource having recurring issues
        pattern = RecurrencePattern(
            pattern_type="resource",
            description=f"Recurring issues on {key}",
            confidence=min(1.0, len(group) / 10),
            severity=calculate_severity(group)
        )
```

### 3. Detect Temporal Patterns

Analyze time intervals between issues:
```python
# Calculate intervals between consecutive issues
intervals = [issues[i].timestamp - issues[i-1].timestamp for i in range(1, len(issues))]

# Check for periodic patterns (low variance = regular occurrence)
avg_interval = mean(intervals)
std_dev = standard_deviation(intervals)

if std_dev / avg_interval < 0.3:
    # Periodic pattern detected
    pattern_type = "periodic"
    period_desc = format_period(avg_interval)  # "every 2 hours"
```

### 4. Detect Cluster Patterns

Find issues occurring together:
```python
# Group issues by 5-minute windows
windows = group_by_time_window(issues, window_seconds=300)

for window, group in windows.items():
    if len(group) >= 3:
        # Cluster pattern: multiple issues at same time
        pattern = RecurrencePattern(
            pattern_type="cluster",
            description=f"Cluster of {len(group)} issues occurring together",
            severity="high" if len(group) >= 5 else "medium"
        )
```

### 5. Calculate Pattern Severity

Determine severity based on issue types:
```yaml
severity_mapping:
  critical:
    - OOMKilled
    - NodeNotReady
    - FailedScheduling
    - Evicted
  high:
    - CrashLoopBackOff
    - ImagePullBackOff
    - CreateContainerError
  medium:
    - 5+ occurrences
  low:
    - default
```

### 6. Generate Prevention Suggestions

Create actionable prevention strategies:
```yaml
suggestions:
  periodic:
    - "Issue recurs at regular intervals"
    - "Investigate time-based triggers (cron jobs, scheduled tasks)"
  resource:
    - "Resource has recurring issues"
    - "Consider: resource limits, deployment config, infrastructure"
  cluster:
    - "Multiple issues occurring together"
    - "Check: common dependencies, shared resources, cascading failures"
  issue_specific:
    OOMKilled: "Increase memory limits or investigate memory leaks"
    CrashLoopBackOff: "Check application logs for startup errors"
    ImagePullBackOff: "Verify image exists and registry credentials"
```

## Success Criteria

The skill succeeds when:

- [ ] Issues grouped and analyzed for patterns
- [ ] Pattern types identified (temporal, resource, cluster)
- [ ] Confidence scores calculated
- [ ] Prevention suggestions generated

## Failure Handling

If analysis fails:

1. Insufficient data: Return empty patterns, note minimum not met
2. Missing timestamps: Skip temporal analysis
3. No patterns found: Return empty result with statistics

## Examples

**Input Context:**
```json
{
  "issues": [
    {"issue_type": "CrashLoopBackOff", "resource": "pod/app-123", "namespace": "prod"},
    {"issue_type": "CrashLoopBackOff", "resource": "pod/app-456", "namespace": "prod"},
    {"issue_type": "OOMKilled", "resource": "pod/app-789", "namespace": "prod"}
  ],
  "temporal_window_hours": 24
}
```

**Expected Output:**
```json
{
  "patterns": [
    {
      "pattern_type": "resource",
      "description": "Recurring CrashLoopBackOff in prod (3 resources)",
      "confidence": 0.3,
      "occurrences": 3,
      "severity": "high",
      "affected_resources": ["pod/app-123", "pod/app-456", "pod/app-789"],
      "issue_types": ["CrashLoopBackOff", "OOMKilled"]
    }
  ],
  "prevention_suggestions": [
    "Container crash loop detected. Check application logs for startup errors.",
    "Memory issues detected. Consider increasing memory limits."
  ],
  "statistics": {
    "total_issues": 3,
    "unique_issue_types": 2,
    "unique_resources": 3,
    "patterns_detected": 1
  }
}
```
