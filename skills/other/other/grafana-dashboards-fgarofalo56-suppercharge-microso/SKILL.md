---
name: grafana-dashboards
description: Build monitoring dashboards with Grafana. Covers panel types, queries, variables, alerting, provisioning, and data sources like Prometheus and InfluxDB. Use for infrastructure monitoring, observability, and metrics visualization.
---

# Grafana Dashboards

Build powerful monitoring and observability dashboards.

## Instructions

1. **Start with key metrics** - CPU, memory, latency, error rates
2. **Use consistent time ranges** - All panels should sync
3. **Add context with variables** - Filter by environment, service, host
4. **Set up alerts** - Proactive monitoring, not reactive
5. **Use templates** - Consistent dashboard styling

## Dashboard Structure

### Dashboard JSON

```json
{
  "dashboard": {
    "id": null,
    "uid": "my-dashboard",
    "title": "Service Overview",
    "tags": ["production", "service-name"],
    "timezone": "browser",
    "schemaVersion": 39,
    "version": 1,
    "refresh": "30s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "templating": {
      "list": []
    },
    "panels": [],
    "annotations": {
      "list": []
    }
  }
}
```

### Panel Types

```json
// Time series (line chart)
{
  "type": "timeseries",
  "title": "Request Rate",
  "gridPos": { "x": 0, "y": 0, "w": 12, "h": 8 },
  "fieldConfig": {
    "defaults": {
      "unit": "reqps",
      "custom": {
        "lineWidth": 2,
        "fillOpacity": 10,
        "gradientMode": "opacity"
      }
    }
  },
  "targets": [
    {
      "expr": "rate(http_requests_total{job=\"$job\"}[5m])",
      "legendFormat": "{{method}} {{status}}"
    }
  ]
}

// Stat panel (single value)
{
  "type": "stat",
  "title": "Total Requests",
  "gridPos": { "x": 0, "y": 0, "w": 4, "h": 4 },
  "options": {
    "colorMode": "value",
    "graphMode": "area",
    "justifyMode": "auto",
    "orientation": "auto",
    "reduceOptions": {
      "calcs": ["lastNotNull"],
      "fields": "",
      "values": false
    }
  },
  "targets": [
    {
      "expr": "sum(http_requests_total{job=\"$job\"})",
      "legendFormat": ""
    }
  ]
}

// Gauge
{
  "type": "gauge",
  "title": "CPU Usage",
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "min": 0,
      "max": 100,
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "color": "green", "value": null },
          { "color": "yellow", "value": 70 },
          { "color": "red", "value": 90 }
        ]
      }
    }
  }
}

// Table
{
  "type": "table",
  "title": "Top Endpoints",
  "transformations": [
    {
      "id": "sortBy",
      "options": {
        "fields": {},
        "sort": [{ "field": "Value", "desc": true }]
      }
    }
  ]
}
```

## Prometheus Queries (PromQL)

### Basic Queries

```promql
# Instant rate (requests per second)
rate(http_requests_total[5m])

# Sum by label
sum by (status_code) (rate(http_requests_total[5m]))

# Average latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m])) * 100

# CPU usage percentage
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) /
node_memory_MemTotal_bytes * 100

# Disk usage
(node_filesystem_size_bytes - node_filesystem_avail_bytes) /
node_filesystem_size_bytes * 100
```

### Aggregation & Filtering

```promql
# Filter by label
http_requests_total{job="api", environment="production"}

# Regex match
http_requests_total{path=~"/api/v[0-9]+/.*"}

# Not equal
http_requests_total{status!="200"}

# Rate over time window
rate(metric[5m])   # 5 minute rate
irate(metric[5m])  # Instant rate (last 2 points)

# Aggregations
sum(metric)              # Total
avg(metric)              # Average
max(metric)              # Maximum
min(metric)              # Minimum
count(metric)            # Count of series
topk(5, metric)          # Top 5 series
bottomk(5, metric)       # Bottom 5 series

# Group by label
sum by (instance) (metric)
avg without (instance) (metric)
```

## Variables (Templating)

```json
{
  "templating": {
    "list": [
      {
        "name": "datasource",
        "type": "datasource",
        "query": "prometheus",
        "current": {},
        "hide": 0
      },
      {
        "name": "environment",
        "type": "query",
        "datasource": "${datasource}",
        "query": "label_values(up, environment)",
        "refresh": 1,
        "multi": false,
        "includeAll": true,
        "allValue": ".*"
      },
      {
        "name": "instance",
        "type": "query",
        "datasource": "${datasource}",
        "query": "label_values(up{environment=\"$environment\"}, instance)",
        "refresh": 2,
        "multi": true,
        "includeAll": true
      },
      {
        "name": "interval",
        "type": "interval",
        "options": [
          { "selected": false, "text": "1m", "value": "1m" },
          { "selected": true, "text": "5m", "value": "5m" },
          { "selected": false, "text": "15m", "value": "15m" }
        ]
      }
    ]
  }
}
```

Usage in queries:
```promql
rate(http_requests_total{environment=~"$environment", instance=~"$instance"}[$interval])
```

## Alerting

### Alert Rule

```json
{
  "alert": "HighErrorRate",
  "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) > 0.05",
  "for": "5m",
  "labels": {
    "severity": "critical"
  },
  "annotations": {
    "summary": "High error rate detected",
    "description": "Error rate is {{ $value | humanizePercentage }} for the last 5 minutes"
  }
}
```

### Grafana Alerting (v8+)

```yaml
# provisioning/alerting/alerts.yaml
apigroups:
  - name: service-alerts
    folder: Alerts
    interval: 1m
    rules:
      - uid: high-error-rate
        title: High Error Rate
        condition: C
        data:
          - refId: A
            datasourceUid: prometheus
            model:
              expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100
          - refId: C
            datasourceUid: __expr__
            model:
              type: threshold
              conditions:
                - evaluator:
                    type: gt
                    params: [5]
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: Error rate above 5%
```

## Dashboard Provisioning

### File Structure

```
grafana/
├── provisioning/
│   ├── dashboards/
│   │   └── dashboards.yaml
│   ├── datasources/
│   │   └── datasources.yaml
│   └── alerting/
│       └── alerts.yaml
└── dashboards/
    ├── overview.json
    └── service-details.json
```

### Datasources Config

```yaml
# provisioning/datasources/datasources.yaml
apidatasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false

  - name: InfluxDB
    type: influxdb
    access: proxy
    url: http://influxdb:8086
    database: metrics
    user: admin
    secureJsonData:
      password: ${INFLUXDB_PASSWORD}
```

### Dashboard Provider

```yaml
# provisioning/dashboards/dashboards.yaml
apiproviders:
  - name: default
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /var/lib/grafana/dashboards
```

## Common Dashboard Patterns

### RED Method (Request, Error, Duration)

```promql
# Request Rate
sum(rate(http_requests_total[5m]))

# Error Rate
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m]))

# Duration (95th percentile)
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### USE Method (Utilization, Saturation, Errors)

```promql
# CPU Utilization
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory Saturation
node_memory_SwapCached_bytes / node_memory_SwapTotal_bytes

# Network Errors
rate(node_network_receive_errs_total[5m])
```

## Best Practices

1. **Use consistent colors** - Red for errors, green for success
2. **Add descriptions** - Panel descriptions explain what's shown
3. **Set meaningful thresholds** - Color changes at important values
4. **Link related dashboards** - Drill-down from overview to details
5. **Version control dashboards** - Store JSON in git
6. **Use dashboard folders** - Organize by team or service

## When to Use

- Infrastructure monitoring
- Application performance monitoring
- Business metrics dashboards
- Real-time operational dashboards
- SLA/SLO tracking

## Notes

- Grafana Cloud offers managed hosting
- Use Terraform provider for IaC
- Consider Grafana Loki for logs
- Grafana Tempo for distributed tracing
