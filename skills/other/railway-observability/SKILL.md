---
name: railway-observability
description: Railway.com built-in metrics, monitoring dashboards, alerting (Pro plan), and external OTEL integration with Grafana. Use when setting up monitoring, creating dashboards, configuring alerts, integrating Prometheus/Loki/Tempo, deploying Grafana stack, or analyzing Railway service metrics.
---

# Railway Observability

Comprehensive guide for Railway.com observability including built-in metrics, customizable dashboards, alerting (Pro plan), and external OTEL integration with Grafana/Prometheus/Loki/Tempo.

## Overview

Railway provides multi-tier observability capabilities:
- Built-in metrics (CPU, memory, disk, network)
- Customizable dashboards with drag-and-drop widgets
- Alerting with email and webhook integrations (Pro plan)
- External OTEL integration via Grafana Alloy
- Full observability stack deployment (Grafana template)

**Keywords**: metrics, monitoring, observability, dashboard, alerts, Grafana, Prometheus, Loki, Tempo, OTEL, Alloy, Railway

## When to Use This Skill

- Setting up monitoring for Railway services
- Creating custom observability dashboards
- Configuring alerts for resource thresholds
- Integrating external monitoring systems
- Deploying Grafana observability stack
- Analyzing service performance metrics
- Troubleshooting resource issues
- Setting up distributed tracing

## Quick Start

### 1. Access Built-in Observability Dashboard

Navigate to your Railway project:

```
Railway Dashboard → Project → Service → Metrics Tab
```

**What you see**:
- CPU usage (% of allocated resources)
- Memory usage (MB/GB over time)
- Disk usage (storage consumption)
- Network I/O (ingress/egress)
- 30-day metric retention

### 2. Configure Custom Dashboard Widgets

Add and customize metric widgets:

```
Metrics Tab → Add Widget → Select Metric Type
```

**Available widgets**:
- Line charts (time-series metrics)
- Bar charts (deployment comparisons)
- Gauges (current values)
- Tables (multi-metric views)

**Customization**:
- Drag-and-drop layout
- Adjustable time ranges (1h, 6h, 24h, 7d, 30d)
- Multi-replica aggregation
- Deployment markers on charts

### 3. Set Up Alerting (Pro Plan Required)

Configure alerts for threshold violations:

```
Service Settings → Alerts → Create Alert Rule
```

**Alert types**:
- CPU threshold (e.g., > 80% for 5 minutes)
- Memory threshold (e.g., > 90% for 10 minutes)
- Disk usage (e.g., > 85%)
- Custom metric thresholds

**Notification channels**:
- Email (default)
- Discord webhook
- Slack webhook
- Custom webhook (JSON payload)

### 4. Integrate External OTEL Collectors

Export metrics to external systems:

```
Service Settings → Observability → OTEL Integration
```

**Configure environment variables**:
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=https://your-collector:4318
OTEL_EXPORTER_OTLP_HEADERS=Authorization=Bearer <token>
OTEL_SERVICE_NAME=my-railway-service
```

See `references/otel-integration.md` for complete setup.

### 5. Deploy Full Grafana Stack

Use Railway template for complete observability:

```bash
# Option 1: Deploy via Railway Dashboard
# Template ID: 8TLSQD (Grafana Stack)
# Includes: Grafana, Prometheus, Loki, Tempo, Alloy

# Option 2: Deploy via script
.claude/skills/railway-observability/scripts/deploy-grafana-stack.sh
```

**Stack components**:
- Grafana (visualization)
- Prometheus (metrics)
- Loki (logs)
- Tempo (traces)
- Alloy (collector)

## Workflow

### Step 1: Access Built-in Metrics

Railway provides instant metrics without configuration.

**Navigate to metrics**:
```
Project → Service → Metrics
```

**Available metrics**:
- CPU: % usage, allocated cores
- Memory: MB used, % of limit
- Disk: GB used, read/write IOPS
- Network: MB/s ingress/egress

**Retention**: 30 days for all metrics

### Step 2: Customize Dashboard

Create personalized monitoring views.

**Add widgets**:
1. Click "Add Widget"
2. Select metric type
3. Configure aggregation
4. Set time range
5. Position via drag-and-drop

**Best practices**:
- Group related metrics (CPU + Memory)
- Use deployment markers for correlation
- Configure multi-replica views
- Set appropriate time ranges

### Step 3: Configure Alerts (Pro Plan)

Set up proactive monitoring.

**Create alert rule**:
```
Service → Settings → Alerts → New Rule
```

**Alert configuration**:
```yaml
Metric: CPU Usage
Condition: Greater than 80%
Duration: 5 minutes
Notification: Slack webhook
```

**Webhook payload example**:
```json
{
  "service": "backend-production",
  "metric": "cpu_usage",
  "threshold": 80,
  "current": 87.5,
  "timestamp": "2025-11-26T10:30:00Z"
}
```

See `references/dashboard-widgets.md` for all alert types.

### Step 4: Integrate OTEL Exporters

Send metrics to external systems.

**Configure Alloy collector**:
```bash
# Use template from templates/alloy-config.river
# Deploy as Railway service
# Configure OTEL endpoints
```

**Environment setup**:
```bash
# In your Railway service
OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_TRACES_EXPORTER=otlp
```

**Verify integration**:
```bash
# Check Alloy logs
railway logs -s alloy

# Should show: "Successfully received OTLP metrics"
```

See `references/otel-integration.md` for complete guide.

### Step 5: Deploy Grafana Observability Stack

Full monitoring solution on Railway.

**Deploy stack**:
```bash
# Run deployment script
cd .claude/skills/railway-observability/scripts
./deploy-grafana-stack.sh

# Or deploy manually via Railway Dashboard
# Template: 8TLSQD (Grafana Stack)
```

**Stack includes**:
- Grafana (port 3000) - Dashboards
- Prometheus (port 9090) - Metrics storage
- Loki (port 3100) - Log aggregation
- Tempo (port 3200) - Distributed tracing
- Alloy (port 4318) - OTLP collector

**Access Grafana**:
```
URL: https://<grafana-service>.up.railway.app
Username: admin
Password: (set during deployment)
```

## Architecture

### Progressive Disclosure Structure

1. **SKILL.md** (this file): Quick start and workflow
2. **references/**: Detailed documentation
   - `metrics-reference.md` - Complete metrics catalog
   - `dashboard-widgets.md` - Widget configuration guide
   - `otel-integration.md` - External integration setup
3. **scripts/**: Automation tools
   - `deploy-grafana-stack.sh` - Deploy observability stack
4. **templates/**: Configuration files
   - `alloy-config.river` - Grafana Alloy collector config

## Key Features

### Built-in Metrics (Always Available)

| Metric | Description | Units | Retention |
|--------|-------------|-------|-----------|
| CPU | % of allocated cores | Percentage | 30 days |
| Memory | RAM usage | MB/GB | 30 days |
| Disk | Storage consumption | GB | 30 days |
| Network I/O | Ingress/egress traffic | MB/s | 30 days |

**No configuration required** - Metrics collected automatically for all services.

### Dashboard Customization

**Drag-and-drop widgets**:
- Resize and reposition
- Multiple chart types
- Custom time ranges
- Deployment markers

**Multi-replica support**:
- Aggregated views (avg, min, max, sum)
- Per-replica breakdowns
- Replica scaling events

**Time range options**:
- Last 1 hour
- Last 6 hours
- Last 24 hours
- Last 7 days
- Last 30 days
- Custom range

### Alerting (Pro Plan Only)

**Threshold alerts**:
- CPU > X% for Y minutes
- Memory > X MB for Y minutes
- Disk > X% capacity
- Network > X MB/s

**Notification channels**:
```bash
# Email
alert@example.com

# Discord webhook
https://discord.com/api/webhooks/...

# Slack webhook
https://hooks.slack.com/services/...

# Custom webhook
https://your-api.com/alerts
```

**Alert states**:
- Pending (condition met, waiting duration)
- Firing (threshold exceeded)
- Resolved (back to normal)

### OTEL Integration

**Supported protocols**:
- OTLP/HTTP (port 4318)
- OTLP/gRPC (port 4317)

**Signal types**:
- Metrics (Prometheus format)
- Logs (JSON structured)
- Traces (Jaeger/Zipkin format)

**Collector options**:
- Grafana Alloy (recommended)
- OpenTelemetry Collector
- Custom OTLP exporters

## Grafana Stack Details

### Template Deployment (8TLSQD)

**One-click deployment**:
```
Railway Dashboard → New Project → Deploy Template → Search "8TLSQD"
```

**Services deployed**:
1. Grafana (visualization)
2. Prometheus (time-series DB)
3. Loki (log aggregation)
4. Tempo (trace storage)
5. Alloy (OTLP collector)

**Configuration**:
- Pre-configured data sources
- Sample dashboards included
- Persistent storage volumes
- Internal networking enabled

### Alloy Collector

**Purpose**: Receive OTLP signals from Railway services and forward to Grafana stack.

**Configuration** (templates/alloy-config.river):
```river
// OTLP receiver
otelcol.receiver.otlp "default" {
  grpc {
    endpoint = "0.0.0.0:4317"
  }
  http {
    endpoint = "0.0.0.0:4318"
  }

  output {
    metrics = [otelcol.exporter.prometheus.default.input]
    logs    = [otelcol.exporter.loki.default.input]
    traces  = [otelcol.exporter.otlp.tempo.input]
  }
}

// Prometheus exporter
otelcol.exporter.prometheus "default" {
  forward_to = [prometheus.remote_write.railway.receiver]
}

// Loki exporter
otelcol.exporter.loki "default" {
  forward_to = [loki.write.railway.receiver]
}

// Tempo exporter
otelcol.exporter.otlp "tempo" {
  client {
    endpoint = "tempo:4317"
  }
}
```

### Grafana Dashboards

**Pre-built dashboards**:
- Railway Service Metrics (CPU, Memory, Disk, Network)
- OTLP Metrics Overview
- Log Analytics (Loki)
- Trace Explorer (Tempo)

**Custom dashboards**:
- Create via Grafana UI
- Import from Grafana.com
- Build with JSON models

## Integration Examples

### Example 1: Monitor Node.js Service

```bash
# Install OTEL SDK
npm install @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node

# Configure OTEL (in Railway service)
export OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy:4318
export OTEL_SERVICE_NAME=nodejs-backend
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_TRACES_EXPORTER=otlp

# Auto-instrumentation
node --require @opentelemetry/auto-instrumentations-node/register app.js
```

**View in Grafana**:
- Metrics: Grafana → Dashboards → Railway Service Metrics
- Logs: Grafana → Explore → Loki
- Traces: Grafana → Explore → Tempo

### Example 2: Alert on High Memory

```yaml
# Pro Plan: Service → Alerts → New Rule
Name: High Memory Alert
Metric: Memory Usage
Condition: Greater than 512 MB
Duration: 10 minutes
Notification: Slack webhook
Webhook URL: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**Slack notification**:
```json
{
  "text": "🚨 High Memory Alert",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Service*: backend-production\n*Memory*: 567 MB (> 512 MB threshold)\n*Duration*: 12 minutes"
      }
    }
  ]
}
```

### Example 3: Custom Metrics from Python

```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# Configure OTLP exporter
exporter = OTLPMetricExporter(
    endpoint="http://alloy:4318/v1/metrics"
)

# Create meter provider
provider = MeterProvider(metric_readers=[
    PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
])
metrics.set_meter_provider(provider)

# Create custom metrics
meter = metrics.get_meter(__name__)
request_counter = meter.create_counter("api_requests_total")
response_time = meter.create_histogram("api_response_time_seconds")

# Record metrics
request_counter.add(1, {"endpoint": "/api/users", "method": "GET"})
response_time.record(0.125, {"endpoint": "/api/users"})
```

**View in Grafana**:
```
Explore → Prometheus → Metrics Browser → api_requests_total
```

## Cross-References

- **railway-api**: Query metrics via GraphQL API
- **railway-logs**: Log aggregation (complements metrics)
- **railway-deployment**: Deployment marker correlation
- **observability-stack-setup**: Local LGTM stack (similar to Railway stack)

## Troubleshooting

### Metrics Not Showing

**Check service status**:
```bash
railway status -s <service-name>
```

**Verify metrics enabled**:
- Metrics are always enabled
- Check service is running
- Wait 1-2 minutes for first data points

### Alerts Not Firing

**Requirements**:
- Pro plan subscription required
- Alert rule properly configured
- Condition met for full duration
- Valid notification channel

**Debug checklist**:
```
1. Verify Pro plan active
2. Check threshold configuration
3. Confirm duration setting
4. Test webhook URL manually
5. Check Railway dashboard for alert status
```

### OTEL Integration Issues

**Common problems**:
- Incorrect endpoint URL
- Network connectivity (use internal Railway URLs)
- Authentication headers missing
- Protocol mismatch (HTTP vs gRPC)

**Verify Alloy receiving data**:
```bash
# Check Alloy logs
railway logs -s alloy

# Look for:
# ✅ "OTLP receiver started"
# ✅ "Received X metric points"
# ❌ "Connection refused" = endpoint issue
# ❌ "Unauthorized" = auth issue
```

See `references/otel-integration.md` for detailed troubleshooting.

## Best Practices

### Dashboard Design
1. Group related metrics (CPU + Memory together)
2. Use deployment markers to correlate changes
3. Set appropriate time ranges (7d for trends, 1h for incidents)
4. Create separate dashboards for different services
5. Use multi-replica views for scaled services

### Alerting Strategy
1. Set thresholds based on actual usage patterns
2. Use duration to avoid false positives (5-10 min)
3. Test notification channels before production
4. Document escalation procedures
5. Review and tune alerts regularly

### OTEL Integration
1. Use internal Railway URLs (no egress costs)
2. Batch metrics for efficiency (60s intervals)
3. Add service tags for filtering
4. Use sampling for high-volume traces
5. Monitor collector resource usage

### Grafana Stack
1. Enable persistent volumes for data retention
2. Configure backup strategy
3. Secure Grafana with strong password
4. Use Railway internal networking
5. Monitor stack resource consumption

## Quick Reference

### Accessing Observability

```bash
# Railway Dashboard
https://railway.app/project/<project-id>/service/<service-id>/metrics

# Via Railway CLI
railway status -s <service-name>
railway metrics -s <service-name>
```

### Common Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| CPU | 70% | 90% |
| Memory | 75% | 90% |
| Disk | 80% | 95% |
| Network | 80% bandwidth | 95% bandwidth |

### OTEL Environment Variables

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_SERVICE_NAME=my-service
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_TRACES_EXPORTER=otlp
```

### Grafana Stack Template

```
Template ID: 8TLSQD
Components: Grafana, Prometheus, Loki, Tempo, Alloy
Deployment: Railway Dashboard → New Project → Deploy Template
Cost: ~$20-30/month (depends on usage)
```

## Resources

- Railway Observability Docs: https://docs.railway.com/reference/observability
- Grafana Template: https://railway.app/template/8TLSQD
- OTEL Documentation: https://opentelemetry.io/docs/
- Grafana Alloy: https://grafana.com/docs/alloy/

## Notes

- Built-in metrics are free for all plans
- Alerting requires Pro plan ($20/month)
- OTEL integration works on all plans
- Grafana stack deploys as separate Railway services
- Metrics retained for 30 days
- Use internal Railway URLs for OTEL (no egress costs)
- Deployment markers automatically added to charts
- Multi-replica metrics aggregated automatically

---

**Updated**: November 26, 2025
**Template ID**: 8TLSQD (Grafana Stack)
**Retention**: 30 days (built-in metrics)
