---
name: gcp-gke-monitoring-observability
description: |
  Configures comprehensive logging, metrics, distributed tracing, and alerting for
  GKE applications. Use when setting up Cloud Logging, creating dashboards in Cloud
  Monitoring, instrumenting Spring Boot with metrics, configuring alerts for error
  rates or resource usage, or implementing distributed tracing with Cloud Trace.
  Includes Prometheus integration, structured logging patterns, and observability
  best practices for microservices.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# GKE Monitoring and Observability

## Purpose

Implement comprehensive observability for GKE applications. This skill covers logging, metrics collection, visualization, distributed tracing, and alerting strategies for Spring Boot microservices.

## When to Use

Use this skill when you need to:
- Set up Cloud Logging and Cloud Monitoring for GKE applications
- Instrument Spring Boot applications with Actuator metrics
- Configure Prometheus scraping for custom metrics
- Create dashboards to visualize application performance
- Set up alerts for error rates, resource usage, or SLOs
- Enable distributed tracing with Cloud Trace
- Debug production issues using logs and metrics

Trigger phrases: "set up monitoring", "GKE observability", "configure Prometheus", "create dashboard", "set up alerts", "enable tracing"

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Enable Cloud Operations Integration](#step-1-enable-cloud-operations-integration)
  - [Step 2: Configure Spring Boot Actuator](#step-2-configure-spring-boot-actuator)
  - [Step 3: Annotate Pods for Prometheus Scraping](#step-3-annotate-pods-for-prometheus-scraping)
  - [Step 4: View Logs](#step-4-view-logs)
  - [Step 5: Create Monitoring Dashboard](#step-5-create-monitoring-dashboard)
  - [Step 6: Set Up Alerts](#step-6-set-up-alerts)
  - [Step 7: Enable Distributed Tracing](#step-7-enable-distributed-tracing)
- [Examples](#examples)
- [Requirements](#requirements)
- [See Also](#see-also)

## Quick Start

Enable observability in three steps:

```bash
# 1. Enable Cloud Monitoring and Logging on cluster
gcloud container clusters update CLUSTER_NAME \
  --region=europe-west2 \
  --logging=SYSTEM,WORKLOAD \
  --monitoring=SYSTEM,WORKLOAD \
  --enable-managed-prometheus

# 2. Deploy Prometheus scrape config for Spring Boot Actuator
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: supplier-charges-hub
  namespace: wtr-supplier-charges
spec:
  ports:
  - name: metrics
    port: 8080
    targetPort: 8080
EOF

# 3. View logs and metrics in Cloud Console
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=wtr-supplier-charges" --limit=50
```

## Instructions

### Step 1: Enable Cloud Operations Integration

Configure the cluster to collect logs and metrics:

```bash
gcloud container clusters update shared-gke-labs-01-euw2 \
  --region=europe-west2 \
  --logging=SYSTEM,WORKLOAD \
  --monitoring=SYSTEM,WORKLOAD \
  --enable-managed-prometheus \
  --enable-cloud-logging \
  --enable-cloud-monitoring
```

**Components:**
- **Cloud Logging**: Captures container stdout/stderr
- **Cloud Monitoring**: System metrics (CPU, memory, disk)
- **Managed Service for Prometheus**: Application metrics (requires annotation)

### Step 2: Configure Spring Boot Actuator

Enable metrics and health endpoints in Spring Boot:

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,env,configprops
  endpoint:
    health:
      probes:
        enabled: true
      show-details: always
    metrics:
      enabled: true
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true
    tags:
      application: supplier-charges-hub
      environment: labs
  health:
    livenessState:
      enabled: true
    readinessState:
      enabled: true
logging:
  pattern:
    console: '{"timestamp":"%d{ISO8601}","level":"%p","logger":"%c{1}","message":"%m"}%n'
```

### Step 3: Annotate Pods for Prometheus Scraping

Mark pods for metrics collection:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supplier-charges-hub
spec:
  template:
    metadata:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/actuator/prometheus"
    spec:
      containers:
      - name: supplier-charges-hub-container
        ports:
        - name: metrics
          containerPort: 8080
          protocol: TCP
```

### Step 4: View Logs

Query container logs from Cloud Logging:

```bash
# View recent logs
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=wtr-supplier-charges" \
  --limit=50 \
  --format=json | jq '.[] | {timestamp: .timestamp, message: .textPayload}'

# View logs with severity filter
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=wtr-supplier-charges AND severity=ERROR" \
  --limit=20

# View logs from specific pod
gcloud logging read "resource.type=k8s_pod AND resource.labels.pod_name=supplier-charges-hub-xyz123 AND resource.labels.namespace_name=wtr-supplier-charges" \
  --limit=50
```

**Alternative: View via kubectl:**

```bash
# Stream logs
kubectl logs -f deployment/supplier-charges-hub -n wtr-supplier-charges

# View logs from specific container (for multi-container pods)
kubectl logs deployment/supplier-charges-hub -c supplier-charges-hub-container -n wtr-supplier-charges

# View previous logs (after pod restart)
kubectl logs deployment/supplier-charges-hub -n wtr-supplier-charges --previous
```

### Step 5: Create Monitoring Dashboard

Visualize key metrics:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: supplier-charges-hub-metrics
  namespace: wtr-supplier-charges
spec:
  groups:
  - name: application-metrics
    interval: 30s
    rules:
    - alert: HighErrorRate
      expr: rate(http_server_requests_seconds_count{status=~"5.."}[5m]) > 0.05
      for: 5m
      annotations:
        summary: "High error rate detected"
    - alert: HighMemoryUsage
      expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.85
      for: 10m
      annotations:
        summary: "Pod memory usage > 85%"
```

### Step 6: Set Up Alerts

Create alert policies for critical metrics:

```bash
# Create alert for high error rate
cat > alert-policy.yaml <<EOF
displayName: "Supplier Charges Hub - High Error Rate"
conditions:
  - displayName: "Error rate > 5%"
    conditionThreshold:
      filter: |
        resource.type="k8s_container"
        resource.namespace_name="wtr-supplier-charges"
        metric.type="logging.googleapis.com/user_defined_metric"
        metric.labels.severity="ERROR"
      comparison: COMPARISON_GT
      thresholdValue: 5
      duration: 300s
notificationChannels:
  - projects/ecp-wtr-supplier-charges-labs/notificationChannels/12345
EOF

# Deploy via gcloud (requires proper setup)
gcloud alpha monitoring policies create --policy-from-file=alert-policy.yaml
```

### Step 7: Enable Distributed Tracing

Add Spring Cloud Sleuth for request tracing:

```gradle
// build.gradle.kts
dependencies {
    implementation("org.springframework.cloud:spring-cloud-starter-sleuth")
    implementation("org.springframework.cloud:spring-cloud-sleuth-zipkin")
}
```

**Configuration:**

```yaml
# application.yml
spring:
  sleuth:
    sampler:
      probability: 0.1  # Sample 10% of requests
  zipkin:
    baseUrl: https://cloudtrace.googleapis.com  # Cloud Trace endpoint
```

**View traces:**

```bash
gcloud traces list --limit=10
gcloud traces describe TRACE_ID
```

## Examples

See [examples/examples.md](examples/examples.md) for comprehensive examples including:
- Complete observability setup script
- Log analysis and error tracking
- Health check endpoint testing
- Custom metrics dashboard creation

## Requirements

- GKE cluster with Cloud Logging and Cloud Monitoring enabled
- Spring Boot application with Actuator dependency
- `kubectl` access to the cluster
- `gcloud` CLI configured
- Service account with monitoring permissions: `roles/monitoring.metricWriter`

## See Also

- [gcp-gke-deployment-strategies](../gcp-gke-deployment-strategies/SKILL.md) - Understand health checks
- [gcp-gke-troubleshooting](../gcp-gke-troubleshooting/SKILL.md) - Use logs to debug issues
- [gcp-gke-cost-optimization](../gcp-gke-cost-optimization/SKILL.md) - Monitor resource costs
