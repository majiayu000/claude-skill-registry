---
name: tron-dashboard-creating
description: Create production-ready Grafana dashboards for TRON team services including consumer dashboards, task metadata, RQ rules manager, and Kafka metrics. Use when building dashboards for task event consumers or RMS TRON services.
version: 1.0.0
---

# TRON Dashboard Creation

## Purpose

Create on-call friendly Grafana dashboards for TRON team services using grafanalib and axon_helpers. Implements Grafana best practices including health overview panels, tiered information design, and service-specific alert annotations.

## When NOT to Use

- Generic API dashboards without Kafka consumers (use standard rms_helpers patterns)
- Non-RMS services (use cd/ or common/ helpers)
- Simple metric additions to existing dashboards

---

## Quick Start: Minimal TRON Consumer Dashboard

```python
from grafanalib.core import Template, Threshold
from axon_helpers.graph_helpers import AxonGraph, AxonSingleStat, GenDashboard, UNITS
from axon_helpers.rms_helpers import generate_dashboard_template_values

# Template variable for filtering by deployment type
deployment_type_template = Template(
    name="deployment_type",
    label="Deployment Type",
    type="custom",
    default="All",
    includeAll=False,
    query="All : .*,Internal : .*-internal.*,Customer : .*-customer.*",
    options=[
        {"selected": True, "text": "All", "value": ".*"},
        {"selected": False, "text": "Internal", "value": ".*-internal.*"},
        {"selected": False, "text": "Customer", "value": ".*-customer.*"},
    ],
)

rows = {
    "Health Overview": [
        AxonSingleStat(
            title="Consumer Lag",
            expressions=[{"expr": 'sum(kafka_consumergroup_group_topic_sum_lag{topic="task-events-public",group=~".*taskmetadatasvc-task-event-consumer.*"})'}],
            thresholds=[
                Threshold("green", 0, 0.0),
                Threshold("orange", 1, 2500),
                Threshold("red", 2, 5000),
            ],
            reduceCalc="lastNotNull",
            graphMode="area",
            format="short",
            span=4,
        ),
    ],
}

dashboard = GenDashboard(
    title="My TRON Consumer Dashboard",
    uid="my-tron-consumer-dashboard",
    templating=generate_dashboard_template_values(
        additional_templates_list=[deployment_type_template]
    ),
    rows=rows,
)
```

---

## Core Workflows

### Workflow 1: Health Overview Dashboard (On-Call Triage)

Create a health overview row for instant on-call triage. This follows the KubeCon "Foolproof K8s Dashboards for Sleep-Deprived On-Calls" pattern.

**Step 1: Define SLO Thresholds**

```python
# Define SLO constants at top of file (not hardcoded in panels)
CUSTOMER_LATENCY_WARNING_MS = 120000   # 2 minutes
CUSTOMER_LATENCY_CRITICAL_MS = 300000  # 5 minutes
CUSTOMER_LAG_WARNING = 2500
CUSTOMER_LAG_CRITICAL = 5000
DLQ_WARNING = 5
DLQ_CRITICAL = 10
```

**Step 2: Create Health Stat Panels**

```python
from grafanalib.core import Threshold

def health_stat(title, description, expr, unit, thresholds, span=2):
    """Create a stat panel showing current metric value with thresholds."""
    return AxonSingleStat(
        title=title,
        description=description,
        expressions=[{"expr": expr, "legendFormat": title}],
        thresholds=thresholds,
        reduceCalc="lastNotNull",
        graphMode="area",
        format=unit,
        decimals=1,
        span=span,
    )

# Health Overview panels (6 stat panels + timeline)
health_panels = [
    health_stat(
        title="Overall Health",
        description="Health score 0-100% based on Kafka lag",
        expr='(1 - clamp_max(sum(kafka_consumergroup_group_topic_sum_lag{...}) / 5000, 1)) * 100',
        unit="percent",
        thresholds=[
            Threshold("red", 0, 0.0),
            Threshold("orange", 1, 50.0),
            Threshold("green", 2, 90.0),
        ],
    ),
    health_stat(
        title="Max Latency",
        description="Max consumer latency in minutes",
        expr='max(rms_taskmetadatasvc_task_event_consumer_read_latency{...}) / 60000',
        unit="m",
        thresholds=[
            Threshold("green", 0, 0.0),
            Threshold("orange", 1, 2.0),
            Threshold("red", 2, 5.0),
        ],
    ),
    # ... Consumer Lag, DLQ Rate, Throughput panels
]
```

**Step 3: Add Timeline Graph**

```python
timeline = AxonGraph(
    title="Kafka Lag Timeline",
    expressions=[{
        "expr": 'sum(kafka_consumergroup_group_topic_sum_lag{topic="task-events-public",...})',
        "legendFormat": "Total Consumer Lag",
    }],
    thresholds=[
        Threshold("green", 0, 0.0),
        Threshold("orange", 1, float(CUSTOMER_LAG_WARNING)),
        Threshold("red", 2, float(CUSTOMER_LAG_CRITICAL)),
    ],
    thresholdsStyleMode="line+area",
    span=12,
    unit=UNITS.SHORT,
)
```

**Validation:**

- [ ] Health overview is first row (not collapsed)
- [ ] 5-6 stat panels cover: Health, Latency, Lag, DLQ, Throughput
- [ ] Thresholds use SLO constants (not hardcoded values)
- [ ] Timeline shows historical context

---

### Workflow 2: Consumer Dashboard (Using ConsumerMetrics)

Use the `ConsumerMetrics` class for standard consumer dashboard sections.

**Step 1: Import and Configure**

```python
from axon_helpers.rms_helpers import ConsumerMetrics, Query
from axon_helpers.utils import flatten

# Filter tags for internal vs customer
isInternalServiceTag = ', service=~".*-internal.*"'
isCustomerServiceTag = ', service!~".*-internal.*"'
isNotDLQTag = ', is_dlq!="true"'
```

**Step 2: Create Consumer Section**

```python
# For Task Metadata Consumer (Internal)
internal_consumer_graphs = flatten(
    ConsumerMetrics(
        service_name="Task Metadata Consumer (Internal)",
        container_name="taskmetadatasvc-task-event-consumer-internal",
        consumer_group=".*taskmetadatasvc-task-event-consumer-internal",
        fetch_latency_query=Query(
            "rms_taskmetadatasvc_task_event_consumer_read_latency",
            additional_expressions=isNotDLQTag + isInternalServiceTag,
        ),
        process_latency_query=Query(
            "rms_taskmetadatasvc_task_event_consumer_sync_latency",
            additional_expressions=isNotDLQTag + isInternalServiceTag,
        ),
        dlq_submitted_query=Query(
            "rms_taskmetadatasvc_task_event_consumer_dlq_submitted_count",
            additional_expressions=isNotDLQTag + isInternalServiceTag,
        ),
        message_volume_query=Query(
            "rms_taskmetadatasvc_task_event_consumer_processed_count",
            additional_expressions=isNotDLQTag + isInternalServiceTag,
        ),
    ).generate_consumer_graphs()
)
```

**Step 3: Add to Dashboard Rows**

```python
rows = {
    "Health Overview": health_panels + [timeline],
    "TASK Events: Task Metadata Consumer (Internal)": internal_consumer_graphs,
    "TASK Events: Task Metadata Consumer (Customer)": customer_consumer_graphs,
}
```

**Validation:**

- [ ] Internal and Customer are separate rows (not combined)
- [ ] Proper filter tags applied (isInternalServiceTag, isCustomerServiceTag)
- [ ] DLQ metrics excluded from main consumer (is_dlq!="true")

---

### Workflow 3: Alert-Linked Dashboard

Link dashboards to alerts for directed browsing (Grafana best practice).

**Step 1: Define Service-Specific Alert Pattern**

```python
import grafanalib.core as G

# CRITICAL: Use narrow patterns, NOT generic like ".*[Ll]ag.*"
# Generic patterns match 90+ alerts and create solid annotation blocks
SERVICE_ALERT_PATTERN = (
    "RMS.*TaskMetadataSvc.*|"
    "RMS.*RQ.*Rule.*Manager.*|"
    "RMS.*RuleManager.*"
)
```

**Step 2: Create Alert Annotations**

```python
alert_annotations = G.Annotations(
    list=[
        {
            "builtIn": 0,
            "datasource": {"type": "prometheus", "uid": "${DataSource}"},
            "enable": True,
            "expr": f'ALERTS{{alertname=~"{SERVICE_ALERT_PATTERN}", alertstate="firing", axon_cluster=~"$axon_cluster"}}',
            "hide": False,
            "iconColor": "rgba(255, 120, 50, 0.25)",  # Orange with 25% opacity
            "name": "Service Alerts",
            "titleFormat": "{{alertname}}",
            "useValueForTime": False,
        },
    ]
)
```

**Step 3: Apply to Dashboard**

```python
dashboard = GenDashboard(
    title="RMS TRON Consumer Dashboard",
    # ... other config
    annotations=alert_annotations,
)
```

**Validation:**

- [ ] Alert pattern is service-specific (not generic)
- [ ] Includes `axon_cluster=~"$axon_cluster"` for environment filtering
- [ ] Icon color has transparency (25% opacity for subtle background)
- [ ] Alert annotations appear on relevant panels only

---

## Panel Selection Guide

| Metric Type           | Panel                       | Best Practice Source    |
| --------------------- | --------------------------- | ----------------------- |
| Current health/status | `AxonSingleStat`            | KubeCon: instant triage |
| Latency (p50/p90/p99) | `AxonGraph` (lines)         | RED Method: Duration    |
| Message volume/rate   | `AxonGraph` (bars)          | RED Method: Rate        |
| Error/fault counts    | `AxonGraph` (bars, stacked) | USE Method: Errors      |
| Kafka consumer lag    | `AxonGraph` (lines)         | USE Method: Saturation  |
| Top-K operations      | `AxonBarGauge`              | Grafana best practices  |
| HPA replica status    | `AxonGraph` (lines)         | KubeCon: normalization  |

See **PATTERNS.md** for complete code examples for each pattern.

---

## Template Variables

**Always include these variables:**

```python
from axon_helpers.rms_helpers import generate_dashboard_template_values

# Standard RMS template variables
templating = generate_dashboard_template_values(
    additional_templates_list=[
        deployment_type_template,  # Internal vs Customer
        consumer_group_template,   # Kafka consumer group filter
    ]
)
```

**Standard variables provided by `generate_dashboard_template_values()`:**

- `$DataSource` - Prometheus/Cortex datasource
- `$axon_cluster` - Cluster/environment selector

See **REFERENCE.md** for custom template variable patterns.

---

## Alert Setup

**CRITICAL: Use service-specific patterns, NOT generic patterns**

```python
# WRONG - matches 90+ alerts, creates solid annotation blocks
ALERT_PATTERN = ".*[Ll]ag.*"

# CORRECT - matches only TRON service alerts
SERVICE_ALERT_PATTERN = (
    "RMS.*TaskMetadataSvc.*|"
    "RMS.*RQ.*Rule.*Manager.*|"
    "RMS.*RuleManager.*"
)
```

See **ALERTS.md** for complete alert annotation patterns and threshold integration.

---

## Row Organization (Best Practice)

```python
rows = {
    # TIER 1: Health Overview - NOT collapsed (on-call triage)
    "Health Overview": health_panels + [timeline],

    # TIER 2: Infrastructure - Collapsed by default
    "Overview: Kafka Infrastructure": kafka_panels,
    "Overview: Consumer Pod Replicas": replica_panels,

    # TIER 3: Service-specific - Collapsed by default
    "TASK Events: Rules Manager Consumers": task_event_panels,
    "TASK Events: Task Metadata Consumer (Internal)": internal_panels,
    "TASK Events: Task Metadata Consumer (Customer)": customer_panels,

    # TIER 4: Advanced/DLQ - Collapsed by default
    "DLQ Processors: All Event Types": dlq_panels,
}

dashboard = GenDashboard(
    rows=rows,
    rows_to_collapse_by_title={
        "Overview: Kafka Infrastructure",
        "Overview: Consumer Pod Replicas",
        "TASK Events: Rules Manager Consumers",
        "DLQ Processors: All Event Types",
    },
)
```

---

## Common Issues

### Issue: Kafka metrics don't filter by $axon_cluster

**Cause:** Kafka exporter metrics don't have `axon_cluster` label
**Solution:** Use explicit consumer group patterns instead:

```python
# Instead of axon_cluster, use explicit group pattern
kafka_lag_expr = 'kafka_consumergroup_group_topic_sum_lag{group=~".*taskmetadatasvc-task-event-consumer.*"}'
```

### Issue: Alert annotations create solid blocks

**Cause:** Generic alert pattern matches too many alerts
**Solution:** Use service-specific pattern (see ALERTS.md)

### Issue: Internal and customer metrics overlap

**Cause:** Missing deployment type filter
**Solution:** Add `service=~"$deployment_type"` filter and split into separate rows

---

## Resources

- **REFERENCE.md** - API reference for axon_helpers classes
- **PATTERNS.md** - Dashboard patterns with code examples
- **ALERTS.md** - Alert annotation patterns (PRIMARY)
- **METRICS.md** - RMS metric naming conventions
- **EXAMPLES.md** - Complete dashboard examples

---

## Quick Reference

```bash
# Dashboard file location
/Users/mriley/projects/ops/grafana-telemetry/dashboards/default/services/rms/

# Generate dashboard
cd /Users/mriley/projects/ops/grafana-telemetry
make rms.rms_tron_consumers_v2.dashboard

# Example dashboard to reference
rms.rms_tron_consumers_v2.dashboard.py
```

---

## Test Scenarios

Use these scenarios to validate skill invocation and output quality.

### Scenario 1: Create Health Overview

**Input:** "Create a health overview for task metadata consumer"

**Expected Output:**

- Uses `health_stat()` helper function pattern
- 5-6 stat panels (Health, Latency, Lag, DLQ, Throughput, Pods)
- Timeline graph with threshold lines
- Thresholds use SLO constants (e.g., `CUSTOMER_LAG_CRITICAL = 5000`)
- Row is NOT collapsed (health always visible)

**Validation:**

```python
# Should see patterns like:
health_stat(title="Consumer Health", ...)
health_stat(title="P99 Latency", ...)
AxonGraph(title="Health Timeline", thresholds=[...])
```

### Scenario 2: Add Alert Annotations

**Input:** "Add alert annotations to my TRON dashboard"

**Expected Output:**

- Uses `SERVICE_ALERT_PATTERN` constant (service-specific)
- Pattern matches: `RMS.*TaskMetadataSvc.*|RMS.*RQ.*Rule.*Manager.*`
- Includes `axon_cluster=~"$axon_cluster"` filter
- Icon color has transparency (`rgba(255, 120, 50, 0.25)`)

**Anti-patterns (should NOT see):**

- ❌ Generic patterns like `.*[Ll]ag.*` or `.*[Cc]onsumer.*`
- ❌ Missing `axon_cluster` filter
- ❌ Solid colors without transparency

### Scenario 3: Create Consumer Section

**Input:** "Add task metadata consumer metrics to dashboard"

**Expected Output:**

- Uses `ConsumerMetrics` class from `axon_helpers.rms_helpers`
- Separates internal and customer into different rows
- Applies filter tags (`isNotDLQTag`, `isInternalServiceTag`, `isCustomerServiceTag`)
- Uses `flatten()` wrapper for panel lists
- Includes latency (p50/p90/p99), volume, and DLQ panels

**Validation:**

```python
# Should see patterns like:
from axon_helpers.rms_helpers import ConsumerMetrics

internal_metrics = ConsumerMetrics(
    metric_prefix="rms_taskmetadatasvc_task_event_consumer",
    filter_tags=isNotDLQTag + isInternalServiceTag,
)
```

### Scenario 4: Kafka Lag Graph

**Input:** "Add Kafka lag graph for TRON consumers"

**Expected Output:**

- Uses `kafka_consumergroup_group_topic_sum_lag` metric
- Does NOT filter by `axon_cluster` (Kafka metrics don't have this label)
- Filters by explicit consumer group pattern instead
- Groups by `group` label for breakdown

**Validation:**

```promql
# Should see pattern like:
sum by (group) (
    kafka_consumergroup_group_topic_sum_lag{
        group=~".*taskmetadatasvc-task-event-consumer.*"
    }
)
```

**Anti-pattern (should NOT see):**

- ❌ `axon_cluster=~"$axon_cluster"` on Kafka metrics (will return no data)
