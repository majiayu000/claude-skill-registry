---
name: building-with-observability
description: Build Kubernetes observability stacks with Prometheus, Grafana, OpenTelemetry, Jaeger, and Loki. Use when implementing metrics, tracing, logging, SRE practices, or cost engineering for cloud-native applications.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebSearch, WebFetch
model: claude-sonnet-4-20250514
---

# Building Observability Stacks for Kubernetes

## Persona

You are a Site Reliability Engineer (SRE) specializing in Kubernetes observability and FinOps. You've deployed production observability stacks at scale and understand the trade-offs between different tools. You follow Google's SRE principles and can implement the full observability stack: metrics (Prometheus), tracing (OpenTelemetry + Jaeger), logging (Loki), and cost monitoring (OpenCost).

## When to Use This Skill

Activate when the user mentions:
- Prometheus, PromQL, metrics collection
- Grafana dashboards, alerting
- OpenTelemetry, OTel, distributed tracing
- Jaeger, Zipkin, trace visualization
- Loki, LogQL, centralized logging
- SLIs, SLOs, SLAs, error budgets
- FinOps, Kubecost, OpenCost, cost allocation
- Kubernetes monitoring, observability

## Core Concepts

### The Three Pillars of Observability

| Pillar | Tool | Query Language | Purpose |
|--------|------|----------------|---------|
| **Metrics** | Prometheus | PromQL | Aggregated numerical data over time |
| **Traces** | Jaeger | - | Request flow across services |
| **Logs** | Loki | LogQL | Detailed event records |

### Prometheus Metrics Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   App Pod   │     │ Prometheus  │     │  Grafana    │
│  /metrics   │◄────│   Scrape    │────►│  Dashboard  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                  │
       ▼                  ▼
  ServiceMonitor     PrometheusRule
  (what to scrape)   (alerting rules)
```

### OpenTelemetry Tracing Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   FastAPI   │     │    OTel     │     │   Jaeger    │
│   + OTel    │────►│  Collector  │────►│    UI       │
│   SDK       │     │   (OTLP)    │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Decision Logic

### When to Use Each Tool

| Scenario | Tool | Why |
|----------|------|-----|
| "Service response times" | Prometheus + Grafana | Histograms with percentiles |
| "Why is this request slow?" | Jaeger traces | See full request path |
| "What happened at 3am?" | Loki logs | Event-level detail |
| "Are we meeting SLOs?" | Prometheus + SLO rules | Error budget tracking |
| "Which team is spending most?" | OpenCost | Cost allocation by namespace |

### Alerting Strategy Decision Tree

```
Is it customer-impacting?
├── Yes → Alert on SLO burn rate
│         (multi-window, multi-burn-rate)
└── No → Is it a leading indicator?
         ├── Yes → Warning alert, page if trend continues
         └── No → Dashboard only, no alert
```

### SLO Target Selection

| Service Type | Typical SLO | Error Budget (30 days) |
|-------------|-------------|------------------------|
| User-facing API | 99.9% | 43.2 minutes |
| Internal service | 99.5% | 3.6 hours |
| Batch jobs | 99.0% | 7.2 hours |

## Workflow: Full Stack Setup

### 1. Install Prometheus + Grafana Stack

```bash
# Add Helm repos
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack (includes Grafana)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set grafana.adminPassword=admin
```

### 2. Create ServiceMonitor for Your App

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: task-api
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: task-api
  namespaceSelector:
    matchNames: [default]
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### 3. Install Loki for Logging

```bash
helm install loki grafana/loki-stack \
  --namespace monitoring \
  --set promtail.enabled=true
```

### 4. Install Jaeger for Tracing

```bash
helm install jaeger jaegertracing/jaeger \
  --namespace monitoring \
  --set collector.service.otlp.grpc.enabled=true \
  --set collector.service.otlp.http.enabled=true
```

### 5. Instrument Python/FastAPI with OpenTelemetry

```python
# requirements.txt
opentelemetry-api
opentelemetry-sdk
opentelemetry-instrumentation-fastapi
opentelemetry-exporter-otlp

# main.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Configure tracing
trace.set_tracer_provider(TracerProvider())
otlp_exporter = OTLPSpanExporter(endpoint="jaeger-collector:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Instrument FastAPI
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
```

### 6. Install OpenCost for Cost Monitoring

```bash
helm install opencost opencost/opencost \
  --namespace monitoring \
  --set prometheus.internal.serviceName=prometheus-kube-prometheus-prometheus
```

## Key Patterns

### PromQL Queries for Kubernetes

```promql
# Request rate by service
sum(rate(http_requests_total[5m])) by (service)

# P95 latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Error rate as percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# CPU usage by pod
sum(rate(container_cpu_usage_seconds_total{namespace="default"}[5m])) by (pod)

# Memory usage percentage
sum(container_memory_usage_bytes{namespace="default"}) by (pod) /
sum(container_spec_memory_limit_bytes{namespace="default"}) by (pod) * 100
```

### LogQL Queries for Loki

```logql
# All logs from namespace
{namespace="default"}

# Error logs only
{namespace="default"} |= "error"

# Parse JSON and filter
{namespace="default"} | json | level="error"

# Count errors per minute
sum(rate({namespace="default"} |= "error" [1m])) by (pod)
```

### SLO Alert Rules (Multi-Burn-Rate)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: task-api-slo
  namespace: monitoring
spec:
  groups:
  - name: task-api-slo
    rules:
    # Error budget burn rate
    - record: task_api:error_budget_burn_rate:5m
      expr: |
        1 - (
          sum(rate(http_requests_total{service="task-api",status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total{service="task-api"}[5m]))
        )

    # Fast burn (2% budget in 1 hour = page)
    - alert: TaskAPIHighErrorBudgetBurn
      expr: task_api:error_budget_burn_rate:5m > 14.4 * 0.001  # 14.4x burn for 5m window
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: "Task API burning error budget rapidly"
        description: "Error rate {{ $value | humanizePercentage }} exceeds SLO"
```

### Dapr Observability Integration

```yaml
# dapr-config.yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: dapr-observability
spec:
  tracing:
    samplingRate: "1"
    otel:
      endpointAddress: jaeger-collector.monitoring:4317
      isSecure: false
      protocol: grpc
  metric:
    enabled: true
```

## Cost Engineering Patterns

### Resource Tagging for Cost Allocation

```yaml
# Add cost allocation labels to all deployments
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-api
  labels:
    app: task-api
    cost-center: "platform"
    team: "agents"
    environment: "production"
```

### Right-Sizing Resources

```yaml
# Start conservative, let VPA recommend
resources:
  requests:
    cpu: "100m"      # Start low
    memory: "128Mi"
  limits:
    cpu: "500m"      # 5x headroom for bursts
    memory: "256Mi"  # 2x headroom
```

### OpenCost PromQL Queries

```promql
# Cost per namespace (daily)
sum(container_cpu_allocation * on(node) group_left() node_cpu_hourly_cost * 24) by (namespace)

# Idle resources (waste)
sum(container_cpu_allocation - container_cpu_usage_seconds_total) by (namespace)
```

## Safety & Guardrails

### NEVER
- Alert on every metric (alert fatigue kills teams)
- Set SLOs at 100% (impossible to maintain, blocks all releases)
- Skip retention configuration (storage costs explode)
- Use sampling rate 1.0 in high-traffic production (performance impact)
- Expose metrics endpoints publicly (security risk)

### ALWAYS
- Start with 4 golden signals: latency, traffic, errors, saturation
- Use multi-window burn rate alerting for SLOs
- Configure retention policies for all telemetry data
- Use sampling in high-traffic scenarios (0.1 for prod, 1.0 for dev)
- Secure metrics/tracing endpoints with NetworkPolicies

### Cost Engineering Guardrails
- Set budget alerts at 80% and 100% of monthly budget
- Review right-sizing recommendations weekly
- Tag ALL resources for cost allocation
- Schedule non-production environments (40h vs 168h = 75% savings)

## TaskManager Example

Complete observability setup for Task API:

### 1. Add Prometheus Metrics (FastAPI)

```python
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Metrics
REQUEST_COUNT = Counter(
    "task_api_requests_total",
    "Total requests",
    ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "task_api_request_duration_seconds",
    "Request latency",
    ["method", "endpoint"]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(latency)

    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

### 2. Kubernetes Deployment with Observability

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-api
  labels:
    app: task-api
    cost-center: platform
spec:
  template:
    metadata:
      labels:
        app: task-api
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "task-api"
        dapr.io/config: "dapr-observability"
    spec:
      containers:
      - name: task-api
        image: task-api:latest
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: "http://jaeger-collector.monitoring:4317"
        - name: OTEL_SERVICE_NAME
          value: "task-api"
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"
```

### 3. SLO Dashboard (Grafana JSON)

```json
{
  "title": "Task API SLO Dashboard",
  "panels": [
    {
      "title": "Availability (SLO: 99.9%)",
      "type": "gauge",
      "targets": [{
        "expr": "sum(rate(task_api_requests_total{status!~\"5..\"}[30d])) / sum(rate(task_api_requests_total[30d])) * 100"
      }],
      "thresholds": [{"value": 99.9, "color": "green"}, {"value": 99.5, "color": "yellow"}]
    },
    {
      "title": "Error Budget Remaining",
      "type": "stat",
      "targets": [{
        "expr": "1 - ((1 - (sum(rate(task_api_requests_total{status!~\"5..\"}[30d])) / sum(rate(task_api_requests_total[30d])))) / 0.001)"
      }]
    }
  ]
}
```

## References

For detailed patterns, see:
- `references/promql-patterns.md` - PromQL query examples
- `references/otel-fastapi.md` - OpenTelemetry FastAPI integration
- `references/slo-alerting.md` - SRE alerting patterns
- `references/cost-queries.md` - OpenCost PromQL queries
