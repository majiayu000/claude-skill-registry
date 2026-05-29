---
name: grafana
description: |
  Observability visualization with Grafana and LGTM stack. Dashboard design, panel configuration, alerting, variables/templating, and data sources.

  USE WHEN: Creating Grafana dashboards, configuring panels and visualizations, writing LogQL/TraceQL queries, setting up Grafana data sources, configuring dashboard variables and templates, building Grafana alerts.
  DO NOT USE: For writing PromQL queries (use /prometheus), for alerting rule strategy (use /prometheus), for general observability architecture (use senior-infrastructure-engineer).

  TRIGGERS: grafana, dashboard, panel, visualization, logql, traceql, loki, tempo, mimir, data source, annotation, variable, template, row, stat, graph, table, heatmap, gauge, bar chart, pie chart, time series, logs panel, traces panel, LGTM stack.
triggers:
  - grafana
  - dashboard
  - panel
  - visualization
  - logql
  - traceql
  - loki
  - tempo
  - mimir
  - data source
  - annotation
  - variable
  - template
  - row
  - stat
  - graph
  - table
  - heatmap
  - gauge
  - bar chart
  - pie chart
  - time series
  - logs panel
  - traces panel
  - LGTM stack
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Grafana and LGTM Stack Skill

## Overview

The LGTM stack provides a complete observability solution with comprehensive visualization and dashboard capabilities:

- **Loki**: Log aggregation and querying (LogQL)
- **Grafana**: Visualization, dashboarding, alerting, and exploration
- **Tempo**: Distributed tracing (TraceQL)
- **Mimir**: Long-term metrics storage (Prometheus-compatible)

This skill covers setup, configuration, dashboard creation, panel design, querying, alerting, templating, and production observability best practices.

## When to Use This Skill

### Primary Use Cases
- Creating or modifying Grafana dashboards
- Designing panels and visualizations (graphs, stats, tables, heatmaps, etc.)
- Writing queries (PromQL, LogQL, TraceQL)
- Configuring data sources (Prometheus, Loki, Tempo, Mimir)
- Setting up alerting rules and notification policies
- Implementing dashboard variables and templates
- Dashboard provisioning and GitOps workflows
- Troubleshooting observability queries
- Analyzing application performance, errors, or system behavior

### Who Uses This Skill
- **senior-infrastructure-engineer** (PRIMARY): Production observability setup, LGTM stack deployment, dashboard architecture
- **software-engineer**: Application dashboards, service metrics visualization
- **devops-engineer**: Infrastructure monitoring, deployment dashboards

## LGTM Stack Components

### Loki - Log Aggregation

#### Architecture - Loki

Horizontally scalable log aggregation inspired by Prometheus

- Indexes only metadata (labels), not log content
- Cost-effective storage with object stores (S3, GCS, etc.)
- LogQL query language similar to PromQL

#### Key Concepts - Loki

- Labels for indexing (low cardinality)
- Log streams identified by unique label sets
- Parsers: logfmt, JSON, regex, pattern
- Line filters and label filters

### Grafana - Visualization

#### Features

- Multi-datasource dashboarding
- Panel types: Graph, Stat, Table, Heatmap, Bar Chart, Pie Chart, Gauge, Logs, Traces, Time Series
- Templating and variables for dynamic dashboards
- Alerting (unified alerting with contact points and notification policies)
- Dashboard provisioning and GitOps integration
- Role-based access control (RBAC)
- Explore mode for ad-hoc queries
- Annotations for event markers
- Dashboard folders and organization

### Tempo - Distributed Tracing

#### Architecture - Tempo

Scalable distributed tracing backend

- Cost-effective trace storage
- TraceQL for trace querying
- Integration with logs and metrics (trace-to-logs, trace-to-metrics)
- OpenTelemetry compatible

### Mimir - Metrics Storage

#### Architecture - Mimir

Horizontally scalable long-term Prometheus storage

- Multi-tenancy support
- Query federation
- High availability
- Prometheus remote_write compatible

## Dashboard Design and Best Practices

### Dashboard Organization Principles

1. **Hierarchy**: Overview -> Service -> Component -> Deep Dive
2. **Golden Signals**: Latency, Traffic, Errors, Saturation (RED/USE method)
3. **Variable-driven**: Use templates for flexibility across environments
4. **Consistent Layouts**: Grid alignment (24-column grid), logical top-to-bottom flow
5. **Performance**: Limit queries, use query caching, appropriate time intervals

### Panel Types and When to Use Them

| Panel Type | Use Case | Best For |
|------------|----------|----------|
| **Time Series / Graph** | Trends over time | Request rates, latency, resource usage |
| **Stat** | Single metric value | Error rates, current values, percentage |
| **Gauge** | Progress toward limit | CPU usage, memory, disk space |
| **Bar Gauge** | Comparative values | Top N items, distribution |
| **Table** | Structured data | Service lists, error details, resource inventory |
| **Pie Chart** | Proportions | Traffic distribution, error breakdown |
| **Heatmap** | Distribution over time | Latency percentiles, request patterns |
| **Logs** | Log streams | Error investigation, debugging |
| **Traces** | Distributed tracing | Performance analysis, dependency mapping |

### Panel Configuration Best Practices

#### Titles and Descriptions
- **Clear, descriptive titles**: Include units and metric context
- **Tooltips**: Add description fields for panel documentation
- **Examples**:
  - Good: "P95 Latency (seconds) by Endpoint"
  - Bad: "Latency"

#### Legends and Labels
- Show legends only when needed (multiple series)
- Use `{{label}}` format for dynamic legend names
- Place legends appropriately (bottom, right, or hidden)
- Sort by value when showing Top N

#### Axes and Units
- Always label axes with units
- Use appropriate unit formats (seconds, bytes, percent, requests/sec)
- Set reasonable min/max ranges to avoid misleading scales
- Use logarithmic scales for wide value ranges

#### Thresholds and Colors
- Use thresholds for visual cues (green/yellow/red)
- Standard threshold pattern:
  - Green: Normal operation
  - Yellow: Warning (action may be needed)
  - Red: Critical (immediate attention required)
- Examples:
  - Error rate: 0% (green), 1% (yellow), 5% (red)
  - P95 latency: <1s (green), 1-3s (yellow), >3s (red)

#### Links and Drilldowns
- Link panels to related dashboards
- Use data links for context (logs, traces, related services)
- Create drill-down paths: Overview -> Service -> Component -> Details
- Link to runbooks for alert panels

### Dashboard Variables and Templating

Dashboard variables enable reusable, dynamic dashboards that work across environments, services, and time ranges.

#### Variable Types

| Type | Purpose | Example |
|------|---------|---------|
| **Query** | Populate from data source | Namespaces, services, pods |
| **Custom** | Static list of options | Environments (prod/staging/dev) |
| **Interval** | Time interval selection | Auto-adjusted query intervals |
| **Datasource** | Switch between data sources | Multiple Prometheus instances |
| **Constant** | Hidden values for queries | Cluster name, region |
| **Text box** | Free-form input | Custom filters |

#### Common Variable Patterns

```json
{
  "templating": {
    "list": [
      {
        "name": "datasource",
        "type": "datasource",
        "query": "prometheus",
        "description": "Select Prometheus data source"
      },
      {
        "name": "namespace",
        "type": "query",
        "datasource": "${datasource}",
        "query": "label_values(kube_pod_info, namespace)",
        "multi": true,
        "includeAll": true,
        "description": "Kubernetes namespace filter"
      },
      {
        "name": "app",
        "type": "query",
        "datasource": "${datasource}",
        "query": "label_values(kube_pod_info{namespace=~\"$namespace\"}, app)",
        "multi": true,
        "includeAll": true,
        "description": "Application filter (depends on namespace)"
      },
      {
        "name": "interval",
        "type": "interval",
        "auto": true,
        "auto_count": 30,
        "auto_min": "10s",
        "options": ["1m", "5m", "15m", "30m", "1h", "6h", "12h", "1d"],
        "description": "Query resolution interval"
      },
      {
        "name": "environment",
        "type": "custom",
        "options": [
          { "text": "Production", "value": "prod" },
          { "text": "Staging", "value": "staging" },
          { "text": "Development", "value": "dev" }
        ],
        "current": { "text": "Production", "value": "prod" }
      }
    ]
  }
}
```

#### Variable Usage in Queries

Variables are referenced with `$variable_name` or `${variable_name}` syntax:

```promql
# Simple variable reference
rate(http_requests_total{namespace="$namespace"}[5m])

# Multi-select with regex match
rate(http_requests_total{namespace=~"$namespace"}[5m])

# Variable in legend
rate(http_requests_total{app="$app"}[5m]) by (method)
# Legend format: "{{method}}"

# Using interval variable for adaptive queries
rate(http_requests_total[$__interval])

# Chained variables (app depends on namespace)
rate(http_requests_total{namespace="$namespace", app="$app"}[5m])
```

#### Advanced Variable Techniques

**Regex filtering**:
```json
{
  "name": "pod",
  "type": "query",
  "query": "label_values(kube_pod_info{namespace=\"$namespace\"}, pod)",
  "regex": "/^$app-.*/",
  "description": "Filter pods by app prefix"
}
```

**All option with custom value**:
```json
{
  "name": "status",
  "type": "custom",
  "options": ["200", "404", "500"],
  "includeAll": true,
  "allValue": ".*",
  "description": "HTTP status code filter"
}
```

**Dependent variables** (variable chain):
1. `$datasource` (datasource type)
2. `$cluster` (query: depends on datasource)
3. `$namespace` (query: depends on cluster)
4. `$app` (query: depends on namespace)
5. `$pod` (query: depends on app)

### Annotations

Annotations display events as vertical markers on time series panels:

```json
{
  "annotations": {
    "list": [
      {
        "name": "Deployments",
        "datasource": "Prometheus",
        "expr": "changes(kube_deployment_spec_replicas{namespace=\"$namespace\"}[5m])",
        "tagKeys": "deployment,namespace",
        "textFormat": "Deployment: {{deployment}}",
        "iconColor": "blue"
      },
      {
        "name": "Alerts",
        "datasource": "Loki",
        "expr": "{app=\"alertmanager\"} | json | alertname!=\"\"",
        "textFormat": "Alert: {{alertname}}",
        "iconColor": "red"
      }
    ]
  }
}
```

### Dashboard Performance Optimization

#### Query Optimization
- Limit number of panels (< 15 per dashboard)
- Use appropriate time ranges (avoid queries over months)
- Leverage `$__interval` for adaptive sampling
- Avoid high-cardinality grouping (too many series)
- Use query caching when available

#### Panel Performance
- Set max data points to reasonable values
- Use instant queries for current-state panels
- Combine related metrics into single queries when possible
- Disable auto-refresh on heavy dashboards

## Dashboard as Code and Provisioning

### Dashboard Provisioning

Dashboard provisioning enables GitOps workflows and version-controlled dashboard definitions.

#### Provisioning Provider Configuration

File: `/etc/grafana/provisioning/dashboards/dashboards.yaml`

```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards

  - name: 'application'
    orgId: 1
    folder: 'Applications'
    type: file
    disableDeletion: true
    editable: false
    options:
      path: /var/lib/grafana/dashboards/application

  - name: 'infrastructure'
    orgId: 1
    folder: 'Infrastructure'
    type: file
    options:
      path: /var/lib/grafana/dashboards/infrastructure
```

#### Dashboard JSON Structure

Complete dashboard JSON with metadata and provisioning:

```json
{
  "dashboard": {
    "title": "Application Observability - ${app}",
    "uid": "app-observability",
    "tags": ["observability", "application"],
    "timezone": "browser",
    "editable": true,
    "graphTooltip": 1,
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "30s",
    "templating": { "list": [] },
    "panels": [],
    "links": []
  },
  "overwrite": true,
  "folderId": null,
  "folderUid": null
}
```

#### Kubernetes ConfigMap Provisioning

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  application-dashboard.json: |
    {
      "dashboard": {
        "title": "Application Metrics",
        "uid": "app-metrics",
        "tags": ["application"],
        "panels": []
      }
    }
```

#### Grafana Operator (CRD)

```yaml
apiVersion: grafana.integreatly.org/v1beta1
kind: GrafanaDashboard
metadata:
  name: application-observability
  namespace: monitoring
spec:
  instanceSelector:
    matchLabels:
      dashboards: "grafana"
  json: |
    {
      "dashboard": {
        "title": "Application Observability",
        "panels": []
      }
    }
```

### Data Source Provisioning

#### Loki Data Source

File: `/etc/grafana/provisioning/datasources/loki.yaml`

```yaml
apiVersion: 1

datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    jsonData:
      maxLines: 1000
      derivedFields:
        - datasourceUid: tempo_uid
          matcherRegex: "trace_id=(\\w+)"
          name: TraceID
          url: "$${__value.raw}"
    editable: false
```

#### Tempo Data Source

File: `/etc/grafana/provisioning/datasources/tempo.yaml`

```yaml
apiVersion: 1

datasources:
  - name: Tempo
    type: tempo
    access: proxy
    url: http://tempo:3200
    uid: tempo_uid
    jsonData:
      httpMethod: GET
      tracesToLogs:
        datasourceUid: loki_uid
        tags: ["job", "instance", "pod", "namespace"]
        mappedTags: [{ key: "service.name", value: "service" }]
        spanStartTimeShift: "1h"
        spanEndTimeShift: "1h"
      tracesToMetrics:
        datasourceUid: prometheus_uid
        tags: [{ key: "service.name", value: "service" }]
      serviceMap:
        datasourceUid: prometheus_uid
      nodeGraph:
        enabled: true
    editable: false
```

#### Mimir/Prometheus Data Source

File: `/etc/grafana/provisioning/datasources/mimir.yaml`

```yaml
apiVersion: 1

datasources:
  - name: Mimir
    type: prometheus
    access: proxy
    url: http://mimir:8080/prometheus
    uid: prometheus_uid
    jsonData:
      httpMethod: POST
      exemplarTraceIdDestinations:
        - datasourceUid: tempo_uid
          name: trace_id
      prometheusType: Mimir
      prometheusVersion: 2.40.0
      cacheLevel: "High"
      incrementalQuerying: true
      incrementalQueryOverlapWindow: 10m
    editable: false
```

## Alerting

### Alert Rule Configuration

Grafana unified alerting supports multi-datasource alerts with flexible evaluation and routing.

#### Prometheus/Mimir Alert Rule

File: `/etc/grafana/provisioning/alerting/rules.yaml`

```yaml
apiVersion: 1

groups:
  - name: application_alerts
    interval: 1m
    rules:
      - uid: error_rate_high
        title: High Error Rate
        condition: A
        data:
          - refId: A
            queryType: ""
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: prometheus_uid
            model:
              expr: |
                sum(rate(http_requests_total{status=~"5.."}[5m]))
                /
                sum(rate(http_requests_total[5m]))
                > 0.05
              intervalMs: 1000
              maxDataPoints: 43200
        noDataState: NoData
        execErrState: Error
        for: 5m
        annotations:
          description: 'Error rate is {{ printf "%.2f" $values.A.Value }}% (threshold: 5%)'
          summary: Application error rate is above threshold
          runbook_url: https://wiki.company.com/runbooks/high-error-rate
        labels:
          severity: critical
          team: platform
        isPaused: false

      - uid: high_latency
        title: High P95 Latency
        condition: A
        data:
          - refId: A
            datasourceUid: prometheus_uid
            model:
              expr: |
                histogram_quantile(0.95,
                  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint)
                ) > 2
        for: 10m
        annotations:
          description: "P95 latency is {{ $values.A.Value }}s on endpoint {{ $labels.endpoint }}"
          runbook_url: https://wiki.company.com/runbooks/high-latency
        labels:
          severity: warning
```

#### Loki Alert Rule

```yaml
apiVersion: 1

groups:
  - name: log_based_alerts
    interval: 1m
    rules:
      - uid: error_spike
        title: Error Log Spike
        condition: A
        data:
          - refId: A
            queryType: ""
            datasourceUid: loki_uid
            model:
              expr: |
                sum(rate({app="api"} | json | level="error" [5m]))
                > 10
        for: 2m
        annotations:
          description: "Error log rate is {{ $values.A.Value }} logs/sec"
          summary: Spike in error logs detected
        labels:
          severity: warning

      - uid: critical_error_pattern
        title: Critical Error Pattern Detected
        condition: A
        data:
          - refId: A
            datasourceUid: loki_uid
            model:
              expr: |
                sum(count_over_time({app="api"}
                  |~ "OutOfMemoryError|StackOverflowError|FatalException" [5m]
                )) > 0
        for: 0m
        annotations:
          description: "Critical error pattern found in logs"
        labels:
          severity: critical
          page: true
```

### Contact Points and Notification Policies

File: `/etc/grafana/provisioning/alerting/contactpoints.yaml`

```yaml
apiVersion: 1

contactPoints:
  - orgId: 1
    name: slack-critical
    receivers:
      - uid: slack_critical
        type: slack
        settings:
          url: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
          title: "{{ .GroupLabels.alertname }}"
          text: |
            {{ range .Alerts }}
            *Alert:* {{ .Labels.alertname }}
            *Summary:* {{ .Annotations.summary }}
            *Description:* {{ .Annotations.description }}
            *Severity:* {{ .Labels.severity }}
            {{ end }}
        disableResolveMessage: false

  - orgId: 1
    name: pagerduty-oncall
    receivers:
      - uid: pagerduty_oncall
        type: pagerduty
        settings:
          integrationKey: YOUR_INTEGRATION_KEY
          severity: critical
          class: infrastructure

  - orgId: 1
    name: email-team
    receivers:
      - uid: email_team
        type: email
        settings:
          addresses: team@company.com
          singleEmail: true

notificationPolicies:
  - orgId: 1
    receiver: slack-critical
    group_by: ["alertname", "namespace"]
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4h
    routes:
      - receiver: pagerduty-oncall
        matchers:
          - severity = critical
          - page = true
        group_wait: 10s
        repeat_interval: 1h
        continue: true

      - receiver: email-team
        matchers:
          - severity = warning
          - team = platform
        group_interval: 10m
        repeat_interval: 12h
```

## LogQL Query Patterns

### Basic Log Queries

#### Stream Selection

```logql
# Simple label matching
{namespace="production", app="api"}

# Regex matching
{app=~"api|web|worker"}

# Not equal
{env!="staging"}

# Multiple conditions
{namespace="production", app="api", level!="debug"}
```

#### Line Filters

```logql
# Contains
{app="api"} |= "error"

# Does not contain
{app="api"} != "debug"

# Regex match
{app="api"} |~ "error|exception|fatal"

# Case insensitive
{app="api"} |~ "(?i)error"

# Chaining filters
{app="api"} |= "error" != "timeout"
```

### Parsing and Extraction

#### JSON Parsing

```logql
# Parse JSON logs
{app="api"} | json

# Extract specific fields
{app="api"} | json message="msg", level="severity"

# Filter on extracted field
{app="api"} | json | level="error"

# Nested JSON
{app="api"} | json | line_format "{{.response.status}}"
```

#### Logfmt Parsing

```logql
# Parse logfmt (key=value)
{app="api"} | logfmt

# Extract specific fields
{app="api"} | logfmt level, caller, msg

# Filter parsed fields
{app="api"} | logfmt | level="error"
```

#### Pattern Parsing

```logql
# Extract with pattern
{app="nginx"} | pattern `<ip> - - <_> "<method> <uri> <_>" <status> <_>`

# Filter on extracted values
{app="nginx"} | pattern `<_> <status> <_>` | status >= 400

# Complex pattern
{app="api"} | pattern `level=<level> msg="<msg>" duration=<duration>ms`
```

### Aggregations and Metrics

#### Count Queries

```logql
# Count log lines over time
count_over_time({app="api"}[5m])

# Rate of logs
rate({app="api"}[5m])

# Errors per second
sum(rate({app="api"} |= "error" [5m])) by (namespace)

# Error ratio
sum(rate({app="api"} |= "error" [5m]))
/
sum(rate({app="api"}[5m]))
```

#### Extracted Metrics

```logql
# Average duration
avg_over_time({app="api"}
  | logfmt
  | unwrap duration [5m]) by (endpoint)

# P95 latency
quantile_over_time(0.95, {app="api"}
  | regexp `duration=(?P<duration>[0-9.]+)ms`
  | unwrap duration [5m]) by (method)

# Top 10 error messages
topk(10,
  sum by (msg) (
    count_over_time({app="api"}
      | json
      | level="error" [1h]
    )
  )
)
```

## TraceQL Query Patterns

### Basic Trace Queries

```traceql
# Find traces by service
{ .service.name = "api" }

# HTTP status codes
{ .http.status_code = 500 }

# Combine conditions
{ .service.name = "api" && .http.status_code >= 400 }

# Duration filter
{ duration > 1s }
```

### Advanced TraceQL

```traceql
# Parent-child relationship
{ .service.name = "frontend" }
  >> { .service.name = "backend" && .http.status_code = 500 }

# Descendant spans
{ .service.name = "api" }
  >>+ { .db.system = "postgresql" && duration > 1s }

# Failed database queries
{ .service.name = "api" }
  >> { .db.system = "postgresql" && status = "error" }
```

## Complete Dashboard Examples

### Application Observability Dashboard

```json
{
  "dashboard": {
    "title": "Application Observability - ${app}",
    "tags": ["observability", "application"],
    "timezone": "browser",
    "editable": true,
    "graphTooltip": 1,
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "templating": {
      "list": [
        {
          "name": "app",
          "type": "query",
          "datasource": "Mimir",
          "query": "label_values(up, app)",
          "current": {
            "selected": false,
            "text": "api",
            "value": "api"
          }
        },
        {
          "name": "namespace",
          "type": "query",
          "datasource": "Mimir",
          "query": "label_values(up{app=\"$app\"}, namespace)",
          "multi": true,
          "includeAll": true
        }
      ]
    },
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "datasource": "Mimir",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{app=\"$app\", namespace=~\"$namespace\"}[$__rate_interval])) by (method, status)",
            "legendFormat": "{{method}} - {{status}}"
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 0,
          "y": 0
        },
        "yaxes": [
          {
            "format": "reqps",
            "label": "Requests/sec"
          }
        ]
      },
      {
        "id": 2,
        "title": "P95 Latency",
        "type": "graph",
        "datasource": "Mimir",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{app=\"$app\", namespace=~\"$namespace\"}[$__rate_interval])) by (le, endpoint))",
            "legendFormat": "{{endpoint}}"
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 12,
          "y": 0
        },
        "yaxes": [
          {
            "format": "s",
            "label": "Duration"
          }
        ],
        "thresholds": [
          {
            "value": 1,
            "colorMode": "critical",
            "fill": true,
            "line": true,
            "op": "gt"
          }
        ]
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "graph",
        "datasource": "Mimir",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{app=\"$app\", namespace=~\"$namespace\", status=~\"5..\"}[$__rate_interval])) / sum(rate(http_requests_total{app=\"$app\", namespace=~\"$namespace\"}[$__rate_interval]))",
            "legendFormat": "Error %"
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 0,
          "y": 8
        },
        "yaxes": [
          {
            "format": "percentunit",
            "max": 1,
            "min": 0
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {
                "params": [0.01],
                "type": "gt"
              },
              "operator": {
                "type": "and"
              },
              "query": {
                "params": ["A", "5m", "now"]
              },
              "reducer": {
                "type": "avg"
              },
              "type": "query"
            }
          ],
          "frequency": "1m",
          "handler": 1,
          "name": "Error Rate Alert",
          "noDataState": "no_data",
          "notifications": []
        }
      },
      {
        "id": 4,
        "title": "Recent Error Logs",
        "type": "logs",
        "datasource": "Loki",
        "targets": [
          {
            "expr": "{app=\"$app\", namespace=~\"$namespace\"} | json | level=\"error\"",
            "refId": "A"
          }
        ],
        "options": {
          "showTime": true,
          "showLabels": false,
          "showCommonLabels": false,
          "wrapLogMessage": true,
          "dedupStrategy": "none",
          "enableLogDetails": true
        },
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 12,
          "y": 8
        }
      }
    ],
    "links": [
      {
        "title": "Explore Logs",
        "url": "/explore?left={\"datasource\":\"Loki\",\"queries\":[{\"expr\":\"{app=\\\"$app\\\",namespace=~\\\"$namespace\\\"}\"}]}",
        "type": "link",
        "icon": "doc"
      },
      {
        "title": "Explore Traces",
        "url": "/explore?left={\"datasource\":\"Tempo\",\"queries\":[{\"query\":\"{resource.service.name=\\\"$app\\\"}\",\"queryType\":\"traceql\"}]}",
        "type": "link",
        "icon": "gf-traces"
      }
    ]
  }
}
```

## LGTM Stack Configuration

### Loki Configuration

File: `loki.yaml`

```yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096
  log_level: info

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: s3
      schema: v13
      index:
        prefix: index_
        period: 24h

storage_config:
  aws:
    s3: s3://us-east-1/my-loki-bucket
    s3forcepathstyle: true
  tsdb_shipper:
    active_index_directory: /loki/tsdb-index
    cache_location: /loki/tsdb-cache
    shared_store: s3

limits_config:
  retention_period: 744h # 31 days
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
  max_query_series: 500
  max_query_lookback: 30d
  reject_old_samples: true
  reject_old_samples_max_age: 168h

compactor:
  working_directory: /loki/compactor
  shared_store: s3
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
```

### Tempo Configuration

File: `tempo.yaml`

```yaml
server:
  http_listen_port: 3200
  grpc_listen_port: 9096

distributor:
  receivers:
    otlp:
      protocols:
        http:
        grpc:
    jaeger:
      protocols:
        thrift_http:
        grpc:

ingester:
  max_block_duration: 5m

compactor:
  compaction:
    block_retention: 720h # 30 days

storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-traces
      endpoint: s3.amazonaws.com
      region: us-east-1
    wal:
      path: /var/tempo/wal

metrics_generator:
  registry:
    external_labels:
      source: tempo
      cluster: primary
  storage:
    path: /var/tempo/generator/wal
    remote_write:
      - url: http://mimir:9009/api/v1/push
        send_exemplars: true
```

## Production Best Practices

### Performance Optimization

#### Query Optimization
- Use label filters before line filters
- Limit time ranges for expensive queries
- Use `unwrap` instead of parsing when possible
- Cache query results with query frontend

#### Dashboard Performance
- Limit number of panels (< 15 per dashboard)
- Use appropriate time intervals
- Avoid high-cardinality grouping
- Use `$__interval` for adaptive sampling

#### Storage Optimization
- Configure retention policies
- Use compaction for Loki and Tempo
- Implement tiered storage (hot/warm/cold)
- Monitor storage growth

### Security Best Practices

#### Authentication
- Enable auth (`auth_enabled: true` in Loki/Tempo)
- Use OAuth/LDAP for Grafana
- Implement multi-tenancy with org isolation

#### Authorization
- Configure RBAC in Grafana
- Limit datasource access by team
- Use folder permissions for dashboards

#### Network Security
- TLS for all components
- Network policies in Kubernetes
- Rate limiting at ingress

### Troubleshooting

#### Common Issues

1. **High Cardinality**: Too many unique label combinations
   - Solution: Reduce label dimensions, use log parsing instead

2. **Query Timeouts**: Complex queries on large datasets
   - Solution: Reduce time range, use aggregations, add query limits

3. **Storage Growth**: Unbounded retention
   - Solution: Configure retention policies, enable compaction

4. **Missing Traces**: Incomplete trace data
   - Solution: Check sampling rates, verify instrumentation

## Resources

- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Tempo Documentation](https://grafana.com/docs/tempo/latest/)
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [LogQL Cheat Sheet](https://grafana.com/docs/loki/latest/logql/)
- [TraceQL Guide](https://grafana.com/docs/tempo/latest/traceql/)
- [Grafana Operator](https://github.com/grafana-operator/grafana-operator)
