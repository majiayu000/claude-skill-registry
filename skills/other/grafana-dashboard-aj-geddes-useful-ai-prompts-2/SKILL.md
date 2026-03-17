---
name: grafana-dashboard
description: Create professional Grafana dashboards with visualizations, templating, and alerts. Use when building monitoring dashboards, creating data visualizations, or setting up operational insights.
---

# Grafana Dashboard

## Overview

Design and implement comprehensive Grafana dashboards with multiple visualization types, variables, and drill-down capabilities for operational monitoring.

## When to Use

- Creating monitoring dashboards
- Building operational insights
- Visualizing time-series data
- Creating drill-down dashboards
- Sharing metrics with stakeholders

## Instructions

### 1. **Grafana Dashboard JSON**

```json
{
  "dashboard": {
    "title": "Application Performance",
    "description": "Real-time application metrics",
    "tags": ["production", "performance"],
    "timezone": "UTC",
    "refresh": "30s",
    "templating": {
      "list": [
        {
          "name": "datasource",
          "type": "datasource",
          "datasource": "prometheus"
        },
        {
          "name": "service",
          "type": "query",
          "datasource": "prometheus",
          "query": "label_values(requests_total, service)"
        }
      ]
    },
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
        "targets": [
          {
            "expr": "sum(rate(requests_total{service=\"$service\"}[5m]))",
            "legendFormat": "{{ method }}"
          }
        ],
        "yaxes": [
          {
            "format": "rps",
            "label": "Requests per Second"
          }
        ]
      },
      {
        "id": 2,
        "title": "Error Rate",
        "type": "graph",
        "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
        "targets": [
          {
            "expr": "sum(rate(requests_total{status_code=~\"5..\",service=\"$service\"}[5m])) / sum(rate(requests_total{service=\"$service\"}[5m]))",
            "legendFormat": "Error Rate"
          }
        ]
      },
      {
        "id": 3,
        "title": "Response Latency (p95)",
        "type": "graph",
        "gridPos": {"x": 0, "y": 8, "w": 12, "h": 8},
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(request_duration_seconds_bucket{service=\"$service\"}[5m]))",
            "legendFormat": "p95"
          }
        ]
      },
      {
        "id": 4,
        "title": "Active Connections",
        "type": "stat",
        "gridPos": {"x": 12, "y": 8, "w": 12, "h": 8},
        "targets": [
          {
            "expr": "sum(active_connections{service=\"$service\"})"
          }
        ]
      }
    ]
  }
}
```

### 2. **Grafana Provisioning Configuration**

```yaml
# /etc/grafana/provisioning/dashboards/dashboards.yaml
apiVersion: 1

providers:
  - name: 'Dashboards'
    orgId: 1
    folder: 'Production'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    options:
      path: /var/lib/grafana/dashboards
```

```yaml
# /etc/grafana/provisioning/datasources/prometheus.yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    orgId: 1
    url: http://prometheus:9090
    isDefault: true
    editable: true
    jsonData:
      timeInterval: '30s'
```

### 3. **Grafana Alert Configuration**

```yaml
# /etc/grafana/provisioning/alerting/alerts.yaml
groups:
  - name: application_alerts
    interval: 1m
    rules:
      - uid: alert_high_error_rate
        title: High Error Rate
        condition: B
        data:
          - refId: A
            model:
              expr: 'sum(rate(requests_total{status_code=~"5.."}[5m]))'
          - refId: B
            conditions:
              - evaluator:
                  params: [0.05]
                  type: gt
                query:
                  params: [A, 5m, now]
        for: 5m
        annotations:
          description: 'Error rate is {{ $values.A }}'
        labels:
          severity: critical
          team: platform
```

### 4. **Grafana API Client**

```javascript
// grafana-api-client.js
const axios = require('axios');

class GrafanaClient {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl;
    this.client = axios.create({
      baseURL: baseUrl,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      }
    });
  }

  async createDashboard(dashboard) {
    const response = await this.client.post('/api/dashboards/db', {
      dashboard: dashboard,
      overwrite: true
    });
    return response.data;
  }

  async getDashboard(uid) {
    const response = await this.client.get(`/api/dashboards/uid/${uid}`);
    return response.data;
  }

  async createAlert(alert) {
    const response = await this.client.post('/api/alerts', alert);
    return response.data;
  }

  async listDashboards() {
    const response = await this.client.get('/api/search?query=');
    return response.data;
  }
}

module.exports = GrafanaClient;
```

### 5. **Docker Compose Setup**

```yaml
version: '3.8'
services:
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD:-admin}
      GF_USERS_ALLOW_SIGN_UP: 'false'
      GF_SERVER_ROOT_URL: http://grafana.example.com
    volumes:
      - ./provisioning:/etc/grafana/provisioning
      - grafana_storage:/var/lib/grafana
    depends_on:
      - prometheus

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_storage:/prometheus

volumes:
  grafana_storage:
  prometheus_storage:
```

## Best Practices

### ✅ DO
- Use meaningful dashboard titles
- Add documentation panels
- Implement row-based organization
- Use variables for flexibility
- Set appropriate refresh intervals
- Include runbook links in alerts
- Test alerts before deploying
- Use consistent color schemes
- Version control dashboard JSON

### ❌ DON'T
- Overload dashboards with too many panels
- Mix different time ranges without justification
- Create without runbooks
- Ignore alert noise
- Use inconsistent metric naming
- Set refresh too frequently
- Forget to configure datasources
- Leave default passwords

## Visualization Types

- **Graph**: Time-series trends
- **Stat**: Single value with thresholds
- **Gauge**: Percentage or usage
- **Heatmap**: Pattern detection
- **Bar Chart**: Category comparison
- **Pie Chart**: Composition
