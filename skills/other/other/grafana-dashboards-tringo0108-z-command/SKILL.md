---
name: grafana-dashboards
description: Create and manage production Grafana dashboards with multiple data sources (Prometheus, InfluxDB, Elasticsearch, CloudWatch, Loki, Tempo) for real-time visualization of system and application metrics. Use when building monitoring dashboards, visualizing metrics, or creating operational observability interfaces.
---

# Grafana Dashboards

Create and manage production-ready Grafana dashboards with multi-source observability for comprehensive system monitoring.

## Purpose

Design effective Grafana dashboards for monitoring applications, infrastructure, and business metrics across multiple data sources with proper correlations and performance optimization.

## When to Use

- Visualize metrics from multiple data sources
- Create custom multi-source dashboards
- Implement SLO dashboards with traces and logs
- Monitor infrastructure with correlated views
- Track business KPIs across systems
- Build unified observability dashboards

---

## Supported Data Sources

| Data Source       | Purpose             | Query Language    |
| ----------------- | ------------------- | ----------------- |
| **Prometheus**    | Metrics collection  | PromQL            |
| **InfluxDB**      | Time series metrics | InfluxQL / Flux   |
| **Elasticsearch** | Logs and search     | Lucene / KQL      |
| **CloudWatch**    | AWS metrics/logs    | CloudWatch Syntax |
| **Loki**          | Log aggregation     | LogQL             |
| **Tempo**         | Distributed tracing | TraceQL           |
| **PostgreSQL**    | Business data       | SQL               |
| **MySQL**         | Business data       | SQL               |

---

## Dashboard Design Principles

### 1. Hierarchy of Information

```
┌─────────────────────────────────────┐
│  Critical Metrics (Big Numbers)     │  ← SLIs, Error rates
├─────────────────────────────────────┤
│  Key Trends (Time Series)           │  ← Request rates, latency
├─────────────────────────────────────┤
│  Detailed Metrics (Tables/Heatmaps) │  ← Per-service breakdown
├─────────────────────────────────────┤
│  Correlated Views (Logs/Traces)     │  ← Debug information
└─────────────────────────────────────┘
```

### 2. RED Method (Services)

- **Rate** - Requests per second
- **Errors** - Error rate
- **Duration** - Latency/response time

### 3. USE Method (Resources)

- **Utilization** - % time resource is busy
- **Saturation** - Queue length/wait time
- **Errors** - Error count

---

## Multi-Source Dashboards

### Using Mixed Data Source

The **Mixed** data source enables combining queries from different sources in a single panel:

```json
{
  "title": "Service Health Overview",
  "type": "timeseries",
  "datasource": {
    "type": "mixed",
    "uid": "-- Mixed --"
  },
  "targets": [
    {
      "datasource": { "type": "prometheus" },
      "expr": "sum(rate(http_requests_total{service=\"$service\"}[5m]))",
      "refId": "A",
      "legendFormat": "Requests/s (Prometheus)"
    },
    {
      "datasource": { "type": "cloudwatch" },
      "namespace": "AWS/ApplicationELB",
      "metricName": "RequestCount",
      "dimensions": { "LoadBalancer": "$loadbalancer" },
      "refId": "B",
      "legendFormat": "ALB Requests (CloudWatch)"
    },
    {
      "datasource": { "type": "influxdb" },
      "query": "from(bucket: \"metrics\") |> filter(fn: (r) => r._measurement == \"requests\")",
      "refId": "C",
      "legendFormat": "Requests (InfluxDB)"
    }
  ]
}
```

### Cross-Source Correlations

Correlate metrics, logs, and traces using shared dimensions:

```json
{
  "panels": [
    {
      "title": "Metrics: Error Rate",
      "type": "timeseries",
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\", service=\"$service\"}[5m]))",
          "legendFormat": "5xx Errors"
        }
      ],
      "gridPos": { "x": 0, "y": 0, "w": 12, "h": 8 }
    },
    {
      "title": "Logs: Error Messages",
      "type": "logs",
      "datasource": "Loki",
      "targets": [
        {
          "expr": "{service=\"$service\"} |= \"error\" | json | level=\"error\"",
          "refId": "A"
        }
      ],
      "gridPos": { "x": 12, "y": 0, "w": 12, "h": 8 }
    },
    {
      "title": "Traces: Failed Requests",
      "type": "traces",
      "datasource": "Tempo",
      "targets": [
        {
          "query": "{ status = error && resource.service.name = \"$service\" }",
          "refId": "A"
        }
      ],
      "gridPos": { "x": 0, "y": 8, "w": 24, "h": 8 }
    }
  ]
}
```

---

## Data Source Examples

### Prometheus Queries

```promql
# Request rate per service
sum(rate(http_requests_total[5m])) by (service)

# Error percentage
(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100

# P95 Latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

# CPU usage per pod
100 - (avg by (pod) (rate(container_cpu_usage_seconds_total[5m])) * 100)
```

### Loki LogQL Queries

```logql
# Error logs for a service
{namespace="$namespace", app="$service"} |= "error"

# Parse JSON logs and filter by level
{app="$service"} | json | level="error" | line_format "{{.message}}"

# Count errors over time
sum(rate({app="$service"} |= "error" [5m]))

# Top error messages
{app="$service"} | json | level="error" | line_format "{{.error}}"
  | pattern `<error>` | topk 10 by (error)
```

### Tempo TraceQL Queries

```
# Traces with errors
{ status = error }

# Traces for specific service with high latency
{ resource.service.name = "$service" && duration > 500ms }

# Find traces by span name
{ name = "HTTP GET /api/users" }

# Traces with specific attributes
{ span.http.status_code = 500 }
```

### InfluxDB Flux Queries

```flux
from(bucket: "metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "http_requests")
  |> filter(fn: (r) => r.service == "${service}")
  |> aggregateWindow(every: v.windowPeriod, fn: mean)

// Join multiple measurements
metrics = from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu")

errors = from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "errors")

join(tables: {m: metrics, e: errors}, on: ["host"])
```

### CloudWatch Queries

```json
{
  "datasource": "CloudWatch",
  "namespace": "AWS/EC2",
  "metricName": "CPUUtilization",
  "dimensions": {
    "InstanceId": ["$instance"]
  },
  "statistics": ["Average"],
  "period": "300"
}
```

### Elasticsearch Queries

```json
{
  "datasource": "Elasticsearch",
  "query": "level:error AND service:$service",
  "timeField": "@timestamp",
  "metrics": [{ "type": "count", "id": "1" }],
  "bucketAggs": [
    {
      "type": "date_histogram",
      "field": "@timestamp",
      "id": "2",
      "settings": { "interval": "auto" }
    }
  ]
}
```

---

## Variables and Templating

### Data Source Variable

Allow users to switch between data sources dynamically:

```json
{
  "templating": {
    "list": [
      {
        "name": "datasource",
        "type": "datasource",
        "query": "prometheus",
        "multi": false,
        "label": "Data Source"
      }
    ]
  }
}
```

### Query Variables Across Sources

```json
{
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_pod_info, namespace)",
        "refresh": 1,
        "multi": false
      },
      {
        "name": "service",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_service_info{namespace=\"$namespace\"}, service)",
        "refresh": 2,
        "multi": true
      },
      {
        "name": "log_stream",
        "type": "query",
        "datasource": "Loki",
        "query": "label_values({namespace=\"$namespace\"}, app)",
        "refresh": 2
      },
      {
        "name": "aws_region",
        "type": "query",
        "datasource": "CloudWatch",
        "query": "regions()",
        "refresh": 1
      }
    ]
  }
}
```

### Ad-Hoc Filters

Enable dynamic filtering across all panels:

```json
{
  "name": "Filters",
  "type": "adhoc",
  "datasource": "Prometheus"
}
```

Usage in queries:

```promql
sum(rate(http_requests_total{$Filters}[5m]))
```

---

## Panel Types

### 1. Stat Panel (Single Value)

```json
{
  "type": "stat",
  "title": "Total Requests",
  "targets": [
    {
      "expr": "sum(http_requests_total)"
    }
  ],
  "options": {
    "reduceOptions": {
      "values": false,
      "calcs": ["lastNotNull"]
    },
    "orientation": "auto",
    "textMode": "auto",
    "colorMode": "value"
  },
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "value": 0, "color": "green" },
          { "value": 80, "color": "yellow" },
          { "value": 90, "color": "red" }
        ]
      }
    }
  }
}
```

### 2. Time Series Graph

```json
{
  "type": "timeseries",
  "title": "CPU Usage",
  "targets": [
    {
      "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "min": 0,
      "max": 100
    }
  }
}
```

### 3. Logs Panel

```json
{
  "type": "logs",
  "title": "Application Logs",
  "datasource": "Loki",
  "targets": [
    {
      "expr": "{namespace=\"$namespace\", app=\"$service\"}"
    }
  ],
  "options": {
    "showTime": true,
    "showLabels": true,
    "wrapLogMessage": true,
    "enableLogDetails": true
  }
}
```

### 4. Traces Panel

```json
{
  "type": "traces",
  "title": "Distributed Traces",
  "datasource": "Tempo",
  "targets": [
    {
      "query": "{ resource.service.name = \"$service\" }"
    }
  ]
}
```

### 5. Table with Transformations

```json
{
  "type": "table",
  "title": "Service Status (Multi-Source)",
  "datasource": { "type": "mixed" },
  "targets": [
    {
      "datasource": "Prometheus",
      "expr": "up{job=~\"$service\"}",
      "format": "table",
      "instant": true,
      "refId": "A"
    },
    {
      "datasource": "CloudWatch",
      "namespace": "AWS/ECS",
      "metricName": "CPUUtilization",
      "refId": "B"
    }
  ],
  "transformations": [
    {
      "id": "merge"
    },
    {
      "id": "organize",
      "options": {
        "excludeByName": { "Time": true },
        "renameByName": {
          "instance": "Instance",
          "Value #A": "Status",
          "Value #B": "CPU %"
        }
      }
    }
  ]
}
```

### 6. Heatmap

```json
{
  "type": "heatmap",
  "title": "Latency Distribution",
  "targets": [
    {
      "expr": "sum(rate(http_request_duration_seconds_bucket[5m])) by (le)",
      "format": "heatmap"
    }
  ],
  "options": {
    "yAxis": { "unit": "s" },
    "color": { "scheme": "Turbo" }
  }
}
```

---

## Transformations for Multi-Source Data

### Join by Field

Join data from different sources by common field:

```json
{
  "transformations": [
    {
      "id": "joinByField",
      "options": {
        "byField": "instance",
        "mode": "outer"
      }
    }
  ]
}
```

### Merge

Combine all series into single frame:

```json
{
  "transformations": [
    {
      "id": "merge"
    }
  ]
}
```

### Rename and Organize

```json
{
  "transformations": [
    {
      "id": "organize",
      "options": {
        "renameByName": {
          "Value #A": "Prometheus Requests",
          "Value #B": "CloudWatch Requests"
        },
        "excludeByName": {
          "__name__": true
        }
      }
    }
  ]
}
```

---

## Dashboard Provisioning

### datasources.yml

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    isDefault: true

  - name: Loki
    type: loki
    url: http://loki:3100
    jsonData:
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: "traceID=(\\w+)"
          name: TraceID
          url: "$${__value.raw}"

  - name: Tempo
    type: tempo
    url: http://tempo:3200
    jsonData:
      tracesToLogs:
        datasourceUid: loki
        tags: ["service.name", "pod"]

  - name: InfluxDB
    type: influxdb
    url: http://influxdb:8086
    database: metrics
    jsonData:
      version: Flux
      organization: myorg
      defaultBucket: metrics
    secureJsonData:
      token: ${INFLUXDB_TOKEN}

  - name: CloudWatch
    type: cloudwatch
    jsonData:
      authType: default
      defaultRegion: us-west-2

  - name: Elasticsearch
    type: elasticsearch
    url: http://elasticsearch:9200
    database: "logs-*"
    jsonData:
      esVersion: "8.0.0"
      timeField: "@timestamp"
```

### dashboards.yml

```yaml
apiVersion: 1

providers:
  - name: "default"
    orgId: 1
    folder: "Production"
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/dashboards
```

---

## Alerts with Multi-Source Context

```json
{
  "alert": {
    "name": "High Error Rate with Log Context",
    "conditions": [
      {
        "evaluator": { "params": [5], "type": "gt" },
        "operator": { "type": "and" },
        "query": { "params": ["A", "5m", "now"] },
        "reducer": { "type": "avg" },
        "type": "query"
      }
    ],
    "executionErrorState": "alerting",
    "for": "5m",
    "frequency": "1m",
    "message": "Error rate is above 5%\n\nCheck logs: ${__dashboard_url__}?var-service=$service&tab=logs\nTraces: ${__dashboard_url__}?var-service=$service&tab=traces",
    "noDataState": "no_data",
    "notifications": [{ "uid": "slack-oncall" }]
  }
}
```

---

## Performance Best Practices

### 1. Query Optimization

| Data Source   | Optimization                                   |
| ------------- | ---------------------------------------------- |
| Prometheus    | Use recording rules for complex queries        |
| Loki          | Add stream selectors before filter expressions |
| Tempo         | Limit by time range and attributes             |
| InfluxDB      | Push aggregations down to query level          |
| CloudWatch    | Use appropriate period (min 60s)               |
| Elasticsearch | Use index patterns and time filters            |

### 2. Dashboard Settings

```json
{
  "refresh": "30s",
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {
    "refresh_intervals": ["5s", "10s", "30s", "1m", "5m"],
    "time_options": ["5m", "15m", "1h", "6h", "12h", "24h", "7d"]
  }
}
```

### 3. Reduce Panel Load

- Use `$__interval` for automatic resolution
- Set reasonable `maxDataPoints`
- Use instant queries for non-time-series data
- Lazy load panels (only visible in viewport)

---

## Dashboard Organization

### Folder Structure

```
Production/
├── Infrastructure/
│   ├── Node Overview
│   ├── Kubernetes Cluster
│   └── Network
├── Applications/
│   ├── API Gateway
│   ├── User Service
│   └── Payment Service
├── Databases/
│   ├── PostgreSQL
│   ├── Redis
│   └── Elasticsearch
└── Business/
    ├── Revenue Dashboard
    └── User Analytics
```

### Tagging Convention

- Environment: `production`, `staging`, `development`
- Team: `platform`, `backend`, `frontend`
- Service: `api`, `database`, `cache`
- Source: `prometheus`, `loki`, `cloudwatch`

---

## Common Pitfalls

| Pitfall                  | Problem         | Solution                     |
| ------------------------ | --------------- | ---------------------------- |
| Too many panels          | Slow load times | Focus on key metrics         |
| Mixed source overload    | Query conflicts | Use transformations to align |
| Missing time alignment   | Mismatched data | Use consistent time filters  |
| High cardinality queries | Memory issues   | Filter early, aggregate      |
| No variable cascading    | Stale filters   | Chain variables with refresh |

## Best Practices Summary

1. **Use Mixed data source** for multi-source panels
2. **Correlate with shared dimensions** (service, pod, instance)
3. **Chain variables** from coarse to fine (region → cluster → service)
4. **Optimize queries at source** (filters first, aggregations early)
5. **Use transformations** for joining and organizing data
6. **Set appropriate refresh rates** (not too frequent)
7. **Version control dashboards** as JSON/code
8. **Link traces to logs** via derived fields
9. **Add context to alerts** with dashboard URLs
10. **Organize with folders and tags**


## Parent Hub
- [_devops-cloud-mastery](../_devops-cloud-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-data-pipeline](../_workflow-data-pipeline/SKILL.md)
