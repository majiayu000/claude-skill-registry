---
name: eks-observability
description: EKS observability with metrics, logging, and tracing. Use when setting up monitoring, configuring logging pipelines, implementing distributed tracing, building production dashboards, troubleshooting EKS issues, optimizing observability costs, or establishing SLOs.
---

# EKS Observability

## Overview

Complete observability solution for Amazon EKS using AWS-native managed services and open-source tools. This skill implements the three-pillar approach (metrics, logs, traces) with 2025 best practices including ADOT, Amazon Managed Prometheus, Fluent Bit, and OpenTelemetry.

**Keywords**: EKS monitoring, CloudWatch Container Insights, Prometheus, Grafana, ADOT, Fluent Bit, X-Ray, OpenTelemetry, distributed tracing, log aggregation, metrics collection, observability stack

**Status**: Production-ready with 2025 best practices

## When to Use This Skill

- Setting up monitoring for EKS clusters
- Implementing centralized logging pipelines
- Configuring distributed tracing
- Building production dashboards in Grafana
- Troubleshooting application performance
- Establishing SLOs and error budgets
- Optimizing observability costs
- Migrating from X-Ray SDKs to OpenTelemetry
- Correlating metrics, logs, and traces
- Setting up alerting and on-call runbooks

## The Three-Pillar Approach (2025 Recommendation)

### 1. Metrics
**CloudWatch Container Insights + Amazon Managed Prometheus (AMP)**
- Dual monitoring provides complete visibility
- CloudWatch for AWS-native integration and quick setup
- Prometheus for advanced queries and community dashboards
- Amazon Managed Grafana for visualization

### 2. Logs
**Fluent Bit → CloudWatch Logs**
- Lightweight log forwarder (AWS deprecated FluentD in Feb 2025)
- DaemonSet deployment for automatic collection
- Structured logging with JSON parsing
- Optional aggregation to OpenSearch for analytics

### 3. Traces
**ADOT → AWS X-Ray**
- OpenTelemetry standard (X-Ray SDKs entering maintenance mode 2026)
- ADOT Collector converts OTLP to X-Ray format
- Distributed tracing across microservices
- Integration with CloudWatch ServiceLens

## Quick Start Workflow

### Step 1: Enable CloudWatch Container Insights

**Using EKS Add-on (Recommended):**
```bash
# Create IAM policy for CloudWatch access
aws iam create-policy \
  --policy-name CloudWatchAgentServerPolicy \
  --policy-document file://cloudwatch-policy.json

# Create IRSA for CloudWatch
eksctl create iamserviceaccount \
  --name cloudwatch-agent \
  --namespace amazon-cloudwatch \
  --cluster my-cluster \
  --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
  --approve \
  --override-existing-serviceaccounts

# Install Container Insights add-on
aws eks create-addon \
  --cluster-name my-cluster \
  --addon-name amazon-cloudwatch-observability \
  --service-account-role-arn arn:aws:iam::ACCOUNT_ID:role/CloudWatchAgentRole
```

**Verify Installation:**
```bash
# Check add-on status
aws eks describe-addon \
  --cluster-name my-cluster \
  --addon-name amazon-cloudwatch-observability

# Verify pods running
kubectl get pods -n amazon-cloudwatch
```

**What You Get:**
- Node-level metrics (CPU, memory, disk, network)
- Pod-level metrics (resource usage, restart counts)
- Namespace-level aggregations
- Automatic CloudWatch Logs integration
- Pre-built CloudWatch dashboards

### Step 2: Deploy Amazon Managed Prometheus

**Create AMP Workspace:**
```bash
# Create workspace
aws amp create-workspace \
  --alias my-cluster-metrics \
  --region us-west-2

# Get workspace ID
WORKSPACE_ID=$(aws amp list-workspaces \
  --alias my-cluster-metrics \
  --query 'workspaces[0].workspaceId' \
  --output text)

# Create IRSA for AMP ingestion
eksctl create iamserviceaccount \
  --name amp-ingest \
  --namespace prometheus \
  --cluster my-cluster \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonPrometheusRemoteWriteAccess \
  --approve
```

**Deploy kube-prometheus-stack:**
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install with AMP remote write
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace prometheus \
  --create-namespace \
  --set prometheus.prometheusSpec.remoteWrite[0].url=https://aps-workspaces.us-west-2.amazonaws.com/workspaces/${WORKSPACE_ID}/api/v1/remote_write \
  --set prometheus.prometheusSpec.remoteWrite[0].sigv4.region=us-west-2 \
  --set prometheus.serviceAccount.annotations."eks\.amazonaws\.com/role-arn"="arn:aws:iam::ACCOUNT_ID:role/AMPIngestRole"
```

**What You Get:**
- Prometheus Operator for CRD-based monitoring
- Node Exporter for hardware metrics
- kube-state-metrics for cluster state
- Alertmanager for alert routing
- 100+ pre-built Grafana dashboards

### Step 3: Deploy Fluent Bit for Logging

**Create IRSA for Fluent Bit:**
```bash
eksctl create iamserviceaccount \
  --name fluent-bit \
  --namespace logging \
  --cluster my-cluster \
  --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
  --approve
```

**Deploy Fluent Bit:**
```bash
helm repo add fluent https://fluent.github.io/helm-charts

helm install fluent-bit fluent/fluent-bit \
  --namespace logging \
  --create-namespace \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"="arn:aws:iam::ACCOUNT_ID:role/FluentBitRole" \
  --set cloudWatch.enabled=true \
  --set cloudWatch.region=us-west-2 \
  --set cloudWatch.logGroupName=/aws/eks/my-cluster/logs \
  --set cloudWatch.autoCreateGroup=true
```

**What You Get:**
- Automatic log collection from all pods
- Structured JSON log parsing
- CloudWatch Logs integration
- Multi-line log support
- Kubernetes metadata enrichment

### Step 4: Deploy ADOT for Distributed Tracing

**Install ADOT Operator:**
```bash
# Create IRSA for ADOT
eksctl create iamserviceaccount \
  --name adot-collector \
  --namespace adot \
  --cluster my-cluster \
  --attach-policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess \
  --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
  --approve

# Install ADOT add-on
aws eks create-addon \
  --cluster-name my-cluster \
  --addon-name adot \
  --service-account-role-arn arn:aws:iam::ACCOUNT_ID:role/ADOTCollectorRole
```

**Deploy ADOT Collector:**
```yaml
# adot-collector.yaml
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: adot-collector
  namespace: adot
spec:
  mode: deployment
  serviceAccount: adot-collector
  config: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318

    processors:
      batch:
        timeout: 30s
        send_batch_size: 50
      memory_limiter:
        check_interval: 1s
        limit_mib: 512

    exporters:
      awsxray:
        region: us-west-2
      awsemf:
        region: us-west-2
        namespace: EKS/Observability

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [awsxray]
        metrics:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [awsemf]
```

```bash
kubectl apply -f adot-collector.yaml
```

**What You Get:**
- OTLP receiver for OpenTelemetry traces
- Automatic X-Ray integration
- Service map visualization
- Trace sampling and filtering
- CloudWatch ServiceLens integration

### Step 5: Setup Amazon Managed Grafana

**Create AMG Workspace:**
```bash
# Create workspace (via AWS Console recommended)
# Or use AWS CLI:
aws grafana create-workspace \
  --workspace-name my-cluster-grafana \
  --account-access-type CURRENT_ACCOUNT \
  --authentication-providers AWS_SSO \
  --permission-type SERVICE_MANAGED
```

**Add Data Sources:**
1. Navigate to AMG workspace URL
2. Configuration → Data Sources → Add data source
3. Add **Amazon Managed Service for Prometheus**
   - Region: us-west-2
   - Workspace: Select your AMP workspace
4. Add **CloudWatch**
   - Default region: us-west-2
   - Namespaces: ContainerInsights, EKS/Observability
5. Add **AWS X-Ray**
   - Default region: us-west-2

**Import Dashboards:**
```bash
# EKS Container Insights Dashboard
Dashboard ID: 16028

# Node Exporter Full Dashboard
Dashboard ID: 1860

# Kubernetes Cluster Monitoring
Dashboard ID: 15760
```

## Production Deployment Checklist

### Infrastructure
- [ ] CloudWatch Container Insights enabled (EKS add-on)
- [ ] Amazon Managed Prometheus workspace created
- [ ] kube-prometheus-stack deployed with remote write
- [ ] Fluent Bit DaemonSet running on all nodes
- [ ] ADOT Collector deployed (deployment or daemonset)
- [ ] Amazon Managed Grafana workspace created
- [ ] All IRSA roles configured with least-privilege policies

### Configuration
- [ ] Prometheus scrape configs include all targets
- [ ] Fluent Bit log groups created and structured
- [ ] ADOT sampling configured (5-10% for high traffic)
- [ ] Grafana data sources connected (AMP, CloudWatch, X-Ray)
- [ ] Log retention policies set (7-90 days typical)
- [ ] Metric retention configured (AMP default 150 days)

### Dashboards
- [ ] Cluster overview dashboard (nodes, pods, namespaces)
- [ ] Application performance dashboard (latency, errors, throughput)
- [ ] Resource utilization dashboard (CPU, memory, disk)
- [ ] Cost monitoring dashboard (resource waste, right-sizing)
- [ ] Network performance dashboard (CNO metrics)

### Alerting
- [ ] Critical alerts: Pod crash loops, node not ready
- [ ] Performance alerts: High latency, error rate spikes
- [ ] Resource alerts: CPU/memory pressure, disk full
- [ ] Cost alerts: Budget thresholds, waste detection
- [ ] SNS topics configured for notifications
- [ ] PagerDuty/Opsgenie integration (optional)

### Application Instrumentation
- [ ] OpenTelemetry SDK integrated in applications
- [ ] Trace context propagation configured
- [ ] Custom metrics exported via OTLP
- [ ] Structured logging with JSON format
- [ ] Log correlation with trace IDs

## Modern Observability Stack (2025)

```
┌─────────────────────────────────────────────────────────────┐
│                      EKS Cluster                            │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Application  │  │ Application  │  │ Application  │     │
│  │ + OTel SDK   │  │ + OTel SDK   │  │ + OTel SDK   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
│                   ┌────────▼────────┐                       │
│                   │ ADOT Collector  │                       │
│                   │ (OTel)          │                       │
│                   └────────┬────────┘                       │
│                            │                                │
│         ┌──────────────────┼──────────────────┐            │
│         │                  │                  │            │
│    ┌────▼─────┐      ┌────▼─────┐      ┌────▼─────┐      │
│    │Prometheus│      │Fluent Bit│      │Container │      │
│    │  (local) │      │DaemonSet │      │ Insights │      │
│    └────┬─────┘      └────┬─────┘      └────┬─────┘      │
└─────────┼──────────────────┼──────────────────┼────────────┘
          │                  │                  │
          │                  │                  │
    ┌─────▼─────┐      ┌────▼─────┐      ┌────▼─────┐
    │   AMP     │      │CloudWatch│      │ X-Ray    │
    │(Managed   │      │  Logs    │      │          │
    │Prometheus)│      └────┬─────┘      └────┬─────┘
    └─────┬─────┘           │                  │
          │                 │                  │
          └─────────────────┴──────────────────┘
                            │
                   ┌────────▼────────┐
                   │Amazon Managed   │
                   │    Grafana      │
                   └─────────────────┘
```

## Detailed Documentation

For comprehensive guides on each observability component:

- **Metrics Collection**: [references/metrics.md](references/metrics.md)
  - CloudWatch Container Insights setup
  - Amazon Managed Prometheus configuration
  - kube-prometheus-stack deployment
  - Custom metrics and ServiceMonitors
  - Cost optimization strategies

- **Centralized Logging**: [references/logging.md](references/logging.md)
  - Fluent Bit configuration and parsers
  - CloudWatch Logs integration
  - OpenSearch aggregation (optional)
  - Log retention and lifecycle policies
  - Troubleshooting log collection

- **Distributed Tracing**: [references/tracing.md](references/tracing.md)
  - ADOT Collector deployment patterns
  - OpenTelemetry SDK instrumentation
  - X-Ray integration and migration
  - Trace sampling strategies
  - ServiceLens and trace analysis

## Cost Optimization

### Metrics
- Sample high-cardinality metrics (5-10% of labels)
- Use metric relabeling to drop unnecessary labels
- Aggregate metrics before remote write to AMP
- Set appropriate retention periods (30-90 days typical)

### Logs
- Implement log sampling for verbose applications
- Use CloudWatch Logs Insights instead of exporting to S3
- Set aggressive retention for debug logs (7 days)
- Keep audit logs longer (90+ days)

### Traces
- Sample traces based on traffic (5-10% default)
- Increase sampling for errors (100%)
- Use tail-based sampling for important transactions
- Clean up old X-Ray traces (default 30 days)

**Typical Monthly Costs:**
- Small cluster (10 nodes): $50-150/month
- Medium cluster (50 nodes): $200-500/month
- Large cluster (200+ nodes): $1000-2000/month

## Integration Patterns

### Correlation Between Pillars

**Metrics → Logs:**
```promql
# Find pods with high error rates
rate(http_requests_total{status=~"5.."}[5m]) > 0.1
# Then search CloudWatch Logs for those pod names
```

**Logs → Traces:**
```json
// Include trace_id in structured logs
{
  "timestamp": "2025-01-27T10:30:00Z",
  "level": "error",
  "message": "Database connection failed",
  "trace_id": "1-67a2f3b1-12456789abcdef012345678",
  "span_id": "abcdef0123456789"
}
```

**Traces → Metrics:**
- Use trace data to identify slow endpoints
- Create SLIs from trace latency percentiles
- Alert on trace error rates

### CloudWatch ServiceLens

Unified view combining:
- X-Ray traces (request flow)
- CloudWatch metrics (performance)
- CloudWatch Logs (detailed context)

```bash
# Enable ServiceLens (automatic with Container Insights + X-Ray)
aws servicelens get-service-lens-metrics \
  --service-name my-app \
  --start-time 2025-01-27T00:00:00Z \
  --end-time 2025-01-27T23:59:59Z
```

## Troubleshooting Quick Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| No metrics in AMP | Missing IRSA or remote write config | Check Prometheus pod logs, verify IAM role |
| Logs not appearing | Fluent Bit not running or wrong IAM | `kubectl logs -n logging fluent-bit-xxx` |
| Traces not in X-Ray | ADOT not deployed or app not instrumented | Verify ADOT pods, check OTel SDK setup |
| High costs | Too much data ingestion | Enable sampling, reduce log verbosity |
| Missing pod metrics | kube-state-metrics not running | Check kube-prometheus-stack installation |
| Grafana can't connect | Data source IAM permissions | Add CloudWatch/AMP read policies to AMG role |

## Production Runbooks

### Incident Response
1. **Check Grafana overview dashboard** - Identify affected services
2. **Review X-Ray service map** - Find bottleneck in request flow
3. **Query CloudWatch Logs Insights** - Get detailed error messages
4. **Correlate with metrics spike** - Understand timeline and scope
5. **Execute remediation** - Scale, restart, or rollback

### Performance Investigation
1. **Start with RED metrics** (Rate, Errors, Duration)
2. **Check USE metrics** (Utilization, Saturation, Errors) for infrastructure
3. **Analyze trace percentiles** (p50, p95, p99)
4. **Review log patterns** during slow periods
5. **Identify optimization opportunities**

## SLO Implementation

**Define SLIs (Service Level Indicators):**
```yaml
# Availability SLI
- metric: probe_success
  target: 99.9%
  window: 30d

# Latency SLI
- metric: http_request_duration_seconds
  percentile: p99
  target: < 500ms
  window: 30d

# Error Rate SLI
- metric: http_requests_total{status=~"5.."}
  target: < 0.1%
  window: 30d
```

**Calculate Error Budget:**
```
Error Budget = 100% - SLO Target
Example: 99.9% SLO = 0.1% error budget
         = 43.2 minutes downtime/month
```

**Burn Rate Alerts:**
```promql
# Fast burn (5% budget in 1 hour)
(1 - slo:availability:ratio_rate_1h) > 0.05

# Slow burn (10% budget in 6 hours)
(1 - slo:availability:ratio_rate_6h) > 0.1
```

## Best Practices Summary

1. **Use Dual Monitoring**: CloudWatch Container Insights + Prometheus
2. **Standardize on OpenTelemetry**: Future-proof instrumentation
3. **Enable IRSA for Everything**: No node IAM roles
4. **Deploy ADOT Collector**: Vendor-neutral observability
5. **Sample Intelligently**: 5-10% traces, 100% errors
6. **Structure Your Logs**: JSON format with trace correlation
7. **Set Retention Policies**: Balance cost and compliance
8. **Build Actionable Dashboards**: Focus on SLIs and anomalies
9. **Implement Progressive Alerting**: Warn before critical
10. **Regularly Review Costs**: Optimize based on actual usage

---

**Stack**: CloudWatch Container Insights, AMP, Fluent Bit, ADOT, AMG, X-Ray
**Standards**: OpenTelemetry, IRSA, EKS Add-ons
**Last Updated**: January 2025 (2025 Best Practices)
