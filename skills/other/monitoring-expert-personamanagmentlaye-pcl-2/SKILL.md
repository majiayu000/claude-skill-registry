---
name: monitoring-expert
version: 1.0.0
description: Expert-level monitoring and observability with Prometheus, Grafana, logging, and alerting
category: devops
tags: [monitoring, observability, prometheus, grafana, logging, metrics, alerting, traces]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(docker:*, kubectl:*, promtool:*)
---

# Monitoring Expert

Expert guidance for monitoring, observability, and alerting using Prometheus, Grafana, logging systems, and distributed tracing.

## Core Concepts

### The Three Pillars of Observability
1. **Metrics** - Numerical measurements over time (Prometheus)
2. **Logs** - Discrete events (ELK, Loki)
3. **Traces** - Request flow through distributed systems (Jaeger, Tempo)

### Monitoring Fundamentals
- Golden Signals (Latency, Traffic, Errors, Saturation)
- RED Method (Rate, Errors, Duration)
- USE Method (Utilization, Saturation, Errors)
- Service Level Indicators (SLIs)
- Service Level Objectives (SLOs)
- Service Level Agreements (SLAs)

### Key Components
- Metric collection (exporters, agents)
- Time-series database
- Visualization (dashboards)
- Alerting (rules, receivers)
- Log aggregation
- Distributed tracing

## Prometheus

### Installation (Docker)
```bash
# docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerts.yml:/etc/prometheus/alerts.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
      - '--storage.tsdb.retention.time=30d'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    command:
      - '--path.rootfs=/host'
    volumes:
      - '/:/host:ro,rslave'

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager-data:/alertmanager

volumes:
  prometheus-data:
  grafana-data:
  alertmanager-data:
```

### Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# Load alert rules
rule_files:
  - 'alerts.yml'

# Scrape configurations
scrape_configs:
  # Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node exporter (system metrics)
  - job_name: 'node'
    static_configs:
      - targets:
          - 'node-exporter:9100'
        labels:
          instance: 'server-1'
          env: 'production'

  # Application metrics
  - job_name: 'app'
    static_configs:
      - targets:
          - 'app-1:8080'
          - 'app-2:8080'
          - 'app-3:8080'
    metrics_path: '/metrics'

  # Kubernetes service discovery
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

  # Blackbox exporter (endpoint monitoring)
  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - https://example.com
          - https://api.example.com/health
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115
```

### Alert Rules
```yaml
# alerts.yml
groups:
  - name: app_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m]) /
          rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.instance }}"
          description: "Error rate is {{ $value | humanizePercentage }} for 5 minutes"

      # API latency
      - alert: HighAPILatency
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High API latency on {{ $labels.instance }}"
          description: "95th percentile latency is {{ $value }}s"

      # Service down
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} down"
          description: "{{ $labels.instance }} has been down for 1 minute"

      # High memory usage
      - alert: HighMemoryUsage
        expr: |
          (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) /
          node_memory_MemTotal_bytes > 0.90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanizePercentage }}"

      # High CPU usage
      - alert: HighCPUUsage
        expr: |
          100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value }}%"

      # Disk space
      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes{mountpoint="/"} /
          node_filesystem_size_bytes{mountpoint="/"}) < 0.10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} disk space remaining"

      # Pod restarts
      - alert: PodRestarting
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.pod }} is restarting"
          description: "Pod has restarted {{ $value }} times in the last 15 minutes"
```

### PromQL Queries

```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Success rate
sum(rate(http_requests_total{status!~"5.."}[5m])) /
sum(rate(http_requests_total[5m]))

# P95 latency
histogram_quantile(0.95,
  rate(http_request_duration_seconds_bucket[5m])
)

# Average latency
rate(http_request_duration_seconds_sum[5m]) /
rate(http_request_duration_seconds_count[5m])

# CPU usage per pod
rate(container_cpu_usage_seconds_total{pod!=""}[5m])

# Memory usage percentage
(container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100

# QPS per endpoint
sum by(endpoint) (rate(http_requests_total[5m]))

# Top 5 slowest endpoints
topk(5, histogram_quantile(0.95,
  sum by(endpoint, le) (rate(http_request_duration_seconds_bucket[5m]))
))

# Predict disk full in 4 hours
predict_linear(node_filesystem_free_bytes[1h], 4*3600) < 0

# Network I/O
rate(node_network_receive_bytes_total[5m])
rate(node_network_transmit_bytes_total[5m])
```

## Application Instrumentation

### Node.js (Express)
```typescript
// Install: npm install prom-client express-prom-bundle
import express from 'express';
import promBundle from 'express-prom-bundle';
import { register, Counter, Histogram, Gauge } from 'prom-client';

const app = express();

// Automatic metrics for all endpoints
const metricsMiddleware = promBundle({
  includeMethod: true,
  includePath: true,
  includeStatusCode: true,
  includeUp: true,
  customLabels: { app: 'myapp' },
  promClient: { collectDefaultMetrics: {} },
});

app.use(metricsMiddleware);

// Custom metrics
const ordersTotal = new Counter({
  name: 'orders_total',
  help: 'Total number of orders',
  labelNames: ['status', 'payment_method'],
});

const orderValue = new Histogram({
  name: 'order_value_dollars',
  help: 'Order value in dollars',
  buckets: [10, 50, 100, 500, 1000, 5000],
});

const activeUsers = new Gauge({
  name: 'active_users',
  help: 'Number of active users',
});

// Use metrics in your code
app.post('/orders', async (req, res) => {
  const order = await createOrder(req.body);

  ordersTotal.inc({ status: 'created', payment_method: order.paymentMethod });
  orderValue.observe(order.total);

  res.json(order);
});

// Expose metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(8080, () => {
  console.log('Server running on :8080');
  console.log('Metrics available at http://localhost:8080/metrics');
});
```

### Python (Flask)
```python
# Install: pip install prometheus-flask-exporter
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram, Gauge

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Custom metrics
orders_total = Counter(
    'orders_total',
    'Total number of orders',
    ['status', 'payment_method']
)

order_value = Histogram(
    'order_value_dollars',
    'Order value in dollars',
    buckets=[10, 50, 100, 500, 1000, 5000]
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

@app.route('/orders', methods=['POST'])
def create_order():
    order = process_order(request.json)

    orders_total.labels(
        status='created',
        payment_method=order['payment_method']
    ).inc()

    order_value.observe(order['total'])

    return jsonify(order)

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    # Metrics available at /metrics
```

### Go
```go
package main

import (
    "net/http"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    ordersTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "orders_total",
            Help: "Total number of orders",
        },
        []string{"status", "payment_method"},
    )

    orderValue = promauto.NewHistogram(
        prometheus.HistogramOpts{
            Name:    "order_value_dollars",
            Help:    "Order value in dollars",
            Buckets: []float64{10, 50, 100, 500, 1000, 5000},
        },
    )

    activeUsers = promauto.NewGauge(
        prometheus.GaugeOpts{
            Name: "active_users",
            Help: "Number of active users",
        },
    )
)

func createOrderHandler(w http.ResponseWriter, r *http.Request) {
    order := processOrder(r.Body)

    ordersTotal.WithLabelValues(
        "created",
        order.PaymentMethod,
    ).Inc()

    orderValue.Observe(order.Total)

    json.NewEncoder(w).Encode(order)
}

func main() {
    http.HandleFunc("/orders", createOrderHandler)
    http.Handle("/metrics", promhttp.Handler())

    http.ListenAndServe(":8080", nil)
}
```

## Alertmanager

### Configuration
```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 5m
  repeat_interval: 4h

  routes:
    # Critical alerts to PagerDuty
    - match:
        severity: critical
      receiver: pagerduty
      continue: true

    # Warning alerts to Slack
    - match:
        severity: warning
      receiver: slack

    # Database alerts
    - match_re:
        service: database
      receiver: database-team

receivers:
  - name: 'default'
    email_configs:
      - to: 'team@example.com'
        from: 'alerts@example.com'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'alerts@example.com'
        auth_password: 'password'

  - name: 'slack'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        send_resolved: true

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
        description: '{{ .GroupLabels.alertname }}'

  - name: 'database-team'
    slack_configs:
      - channel: '#database-alerts'
    email_configs:
      - to: 'dba-team@example.com'

inhibit_rules:
  # Suppress warning if critical alert is firing
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
```

## Grafana

### Dashboard Configuration (JSON)
```json
{
  "dashboard": {
    "title": "Application Metrics",
    "tags": ["app", "production"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "gridPos": { "x": 0, "y": 0, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (status)",
            "legendFormat": "{{ status }}"
          }
        ]
      },
      {
        "title": "P95 Latency",
        "type": "graph",
        "gridPos": { "x": 12, "y": 0, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "p95"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "stat",
        "gridPos": { "x": 0, "y": 8, "w": 6, "h": 4 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "thresholds": {
              "steps": [
                { "value": 0, "color": "green" },
                { "value": 0.01, "color": "yellow" },
                { "value": 0.05, "color": "red" }
              ]
            }
          }
        }
      }
    ]
  }
}
```

### Provisioning Data Sources
```yaml
# grafana/provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: false
```

## Logging with Loki

### Loki Configuration
```yaml
# loki-config.yml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2020-05-15
      store: boltdb
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 168h

storage_config:
  boltdb:
    directory: /tmp/loki/index
  filesystem:
    directory: /tmp/loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h
```

### Promtail Configuration
```yaml
# promtail-config.yml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Application logs
  - job_name: app
    static_configs:
      - targets:
          - localhost
        labels:
          job: app
          __path__: /var/log/app/*.log

  # Docker logs
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        target_label: 'container'

  # Kubernetes logs
  - job_name: kubernetes
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      - docker: {}
    relabel_configs:
      - source_labels:
          - __meta_kubernetes_pod_name
        target_label: pod
      - source_labels:
          - __meta_kubernetes_namespace
        target_label: namespace
```

### LogQL Queries
```logql
# All logs for a job
{job="app"}

# Filter by level
{job="app"} |= "error"

# JSON parsing
{job="app"} | json | level="error"

# Rate of errors
rate({job="app"} |= "error" [5m])

# Count by pod
sum by (pod) (count_over_time({namespace="production"}[5m]))

# Extract and filter
{job="app"}
  | json
  | line_format "{{.timestamp}} {{.level}} {{.message}}"
  | level="error"

# Metrics from logs
sum(rate({job="app"} |= "status=500" [5m])) by (endpoint)
```

## Distributed Tracing

### Jaeger Setup
```yaml
# docker-compose.yml
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "5778:5778"
      - "16686:16686"  # UI
      - "14268:14268"  # Collector
      - "9411:9411"    # Zipkin compatible
    environment:
      - COLLECTOR_ZIPKIN_HTTP_PORT=9411
```

### Application Instrumentation (Node.js)
```typescript
// Install: npm install jaeger-client opentracing
import { initTracer } from 'jaeger-client';

const config = {
  serviceName: 'my-app',
  sampler: {
    type: 'probabilistic',
    param: 1.0, // Sample 100% of traces
  },
  reporter: {
    logSpans: true,
    agentHost: 'localhost',
    agentPort: 6831,
  },
};

const tracer = initTracer(config);

// Trace HTTP request
app.get('/api/users/:id', async (req, res) => {
  const span = tracer.startSpan('get_user');
  span.setTag('user_id', req.params.id);

  try {
    // Database query
    const dbSpan = tracer.startSpan('db_query', { childOf: span });
    const user = await db.user.findById(req.params.id);
    dbSpan.finish();

    // External API call
    const apiSpan = tracer.startSpan('external_api', { childOf: span });
    const profile = await fetchUserProfile(user.id);
    apiSpan.finish();

    span.setTag('http.status_code', 200);
    res.json({ user, profile });
  } catch (error) {
    span.setTag('error', true);
    span.setTag('http.status_code', 500);
    span.log({ event: 'error', message: error.message });
    res.status(500).json({ error: error.message });
  } finally {
    span.finish();
  }
});
```

## Best Practices

### Metric Naming
- Use descriptive names: `http_requests_total` not `requests`
- Use units in name: `duration_seconds`, `bytes_total`
- Use `_total` suffix for counters
- Use `_bucket` suffix for histograms
- Use consistent label names

### Cardinality
- Avoid high-cardinality labels (user IDs, emails)
- Use bounded label values
- Aggregate when possible
- Monitor metric count

### Alert Design
- Alert on symptoms, not causes
- Set appropriate thresholds
- Include actionable annotations
- Group related alerts
- Use inhibition rules

### Dashboard Design
- One purpose per dashboard
- Use consistent time ranges
- Include SLOs/SLIs
- Add context with annotations
- Use appropriate visualization types

## Anti-Patterns to Avoid

❌ **No SLOs**: Define service level objectives
❌ **Alert fatigue**: Too many non-actionable alerts
❌ **High cardinality**: Labels with unbounded values
❌ **Missing instrumentation**: Instrument all critical paths
❌ **No runbooks**: Alerts should have clear remediation steps
❌ **Ignoring trends**: Monitor trends, not just current values
❌ **No log structure**: Use structured logging (JSON)
❌ **Missing context**: Include relevant labels and tags

## Resources

- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/
- Loki: https://grafana.com/docs/loki/
- Jaeger: https://www.jaegertracing.io/docs/
- OpenTelemetry: https://opentelemetry.io/docs/
- SRE Book: https://sre.google/books/
