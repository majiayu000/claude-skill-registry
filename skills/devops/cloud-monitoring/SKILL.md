---
name: cloud-monitoring
description: Monitor cloud infrastructure and applications using metrics, logs, and traces to provide real-time observability into performance, health, and reliability. Use when the user requests cloud monitoring or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Cloud Monitoring

This skill enables the agent to design and configure comprehensive monitoring and observability solutions for cloud infrastructure and applications. The agent understands the three pillars of observability — metrics, logs, and traces — and can set up dashboards, alerting rules, SLIs, SLOs, and SLAs using tools like Prometheus, Grafana, CloudWatch, Datadog, and OpenTelemetry. The agent also applies alerting best practices to minimize alert fatigue while ensuring critical issues are surfaced promptly.

## Workflow

1. **Identify Monitoring Objectives:** The agent works with the user to define what needs to be monitored and why. This includes identifying critical services, establishing Service Level Indicators (SLIs) such as request latency, error rate, and throughput, and setting Service Level Objectives (SLOs) that define acceptable performance thresholds. SLAs (Service Level Agreements) are documented as contractual commitments to customers.

2. **Select Monitoring Tools and Instrumentation:** Based on the cloud provider and application architecture, the agent recommends an appropriate monitoring stack. This may include Prometheus for metrics collection, Grafana for visualization, Loki or CloudWatch Logs for log aggregation, and Jaeger or AWS X-Ray for distributed tracing. The agent configures OpenTelemetry SDKs in application code to emit standardized telemetry data.

3. **Configure Metrics Collection and Dashboards:** The agent defines and deploys metric scrapers, exporters, and custom metrics. It builds dashboards that visualize the golden signals (latency, traffic, errors, saturation) and infrastructure metrics (CPU, memory, disk, network). Dashboards are organized by service tier so teams can quickly triage issues.

4. **Establish Alerting Rules:** The agent configures alerts that trigger on meaningful conditions — such as error budget burn rate exceeding thresholds, sustained latency spikes, or pod restarts — rather than raw metric thresholds alone. Multi-window, multi-burn-rate alerting is used to balance detection speed with false-positive suppression. Alert routing is configured to send critical alerts to PagerDuty or Opsgenie and warnings to Slack.

5. **Set Up Log Aggregation and Trace Correlation:** The agent configures centralized log collection with structured logging formats (JSON), log retention policies, and log-based alerts for error patterns. Distributed traces are correlated with logs and metrics using shared trace IDs so that a single alert can link directly to the relevant request trace and log entries.

6. **Review and Iterate:** The agent periodically audits alert noise levels, dashboard usage, and SLO compliance. Unused alerts are pruned, thresholds are adjusted based on observed baselines, and new services are onboarded into the monitoring stack as the system evolves.

## Supported Technologies

- **Metrics:** Prometheus, AWS CloudWatch, Google Cloud Monitoring, Azure Monitor, Datadog, New Relic
- **Visualization:** Grafana, CloudWatch Dashboards, Datadog Dashboards, Kibana
- **Logs:** Loki, CloudWatch Logs, Elasticsearch/Fluentd/Kibana (EFK), Splunk
- **Traces:** Jaeger, Zipkin, AWS X-Ray, Tempo, Datadog APM
- **Instrumentation:** OpenTelemetry, Prometheus client libraries, StatsD
- **Alerting:** Alertmanager, PagerDuty, Opsgenie, Slack Webhooks, SNS

## Usage

Provide the agent with your cloud provider, the services to monitor, your preferred monitoring stack, and any existing SLOs or alerting requirements.

**Example prompt:**

```
Set up monitoring for our Kubernetes microservices on AWS.
- Use Prometheus and Grafana for metrics and dashboards
- Monitor API latency (p99 < 500ms) and error rate (< 1%)
- Send critical alerts to PagerDuty, warnings to Slack
- Aggregate logs with CloudWatch Logs
```

## Examples

### Example 1: Prometheus + Grafana with Alerting Rules

**prometheus.yml** — Prometheus scrape configuration:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

scrape_configs:
  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]

  - job_name: "app"
    metrics_path: /metrics
    static_configs:
      - targets: ["app:8080"]

  - job_name: "kubernetes-pods"
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)
        replacement: $1
```

**alert_rules.yml** — SLO-based alerting rules:

```yaml
groups:
  - name: slo-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate exceeds 1% SLO"
          description: "{{ $labels.job }} error rate is {{ $value | humanizePercentage }}"

      - alert: HighP99Latency
        expr: |
          histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
          > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency exceeds 500ms SLO"

      - alert: PodCrashLooping
        expr: increase(kube_pod_container_status_restarts_total[1h]) > 3
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod {{ $labels.pod }} is crash looping"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.9
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Node memory usage above 90%"
```

### Example 2: AWS CloudWatch Dashboard with Custom Metrics and Alarms

**cloudwatch-dashboard.json** — CloudFormation template for a monitoring stack:

```json
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Resources": {
    "ApiDashboard": {
      "Type": "AWS::CloudWatch::Dashboard",
      "Properties": {
        "DashboardName": "api-service-dashboard",
        "DashboardBody": "{\"widgets\":[{\"type\":\"metric\",\"properties\":{\"metrics\":[[\"AWS/ApplicationELB\",\"TargetResponseTime\",\"TargetGroup\",\"my-tg\",{\"stat\":\"p99\"}],[\"AWS/ApplicationELB\",\"HTTPCode_Target_5XX_Count\",\"TargetGroup\",\"my-tg\"]],\"period\":300,\"title\":\"API Latency & Errors\"}},{\"type\":\"metric\",\"properties\":{\"metrics\":[[\"Custom/App\",\"ActiveConnections\"],[\"Custom/App\",\"QueueDepth\"]],\"period\":60,\"title\":\"Application Metrics\"}}]}"
      }
    },
    "HighLatencyAlarm": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "AlarmName": "api-high-latency",
        "MetricName": "TargetResponseTime",
        "Namespace": "AWS/ApplicationELB",
        "Statistic": "p99",
        "Period": 300,
        "EvaluationPeriods": 3,
        "Threshold": 0.5,
        "ComparisonOperator": "GreaterThanThreshold",
        "AlarmActions": ["arn:aws:sns:us-east-1:123456789012:ops-alerts"],
        "Dimensions": [
          {"Name": "TargetGroup", "Value": "my-tg"}
        ]
      }
    },
    "HighErrorRateAlarm": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "AlarmName": "api-high-error-rate",
        "MetricName": "HTTPCode_Target_5XX_Count",
        "Namespace": "AWS/ApplicationELB",
        "Statistic": "Sum",
        "Period": 300,
        "EvaluationPeriods": 2,
        "Threshold": 50,
        "ComparisonOperator": "GreaterThanThreshold",
        "AlarmActions": ["arn:aws:sns:us-east-1:123456789012:ops-alerts"]
      }
    }
  }
}
```

## Best Practices

- **Alert on symptoms, not causes:** Alert on user-facing impact (high error rate, slow responses) rather than low-level infrastructure metrics (CPU at 80%). High CPU is only a problem if it degrades user experience.
- **Use multi-window burn rates:** Instead of alerting on a single threshold, use SLO burn-rate alerts with fast (5m) and slow (1h) windows. This detects real incidents quickly while ignoring brief transient spikes.
- **Minimize alert fatigue:** Every alert should be actionable. If an alert fires and the on-call engineer has no clear action to take, the alert should be removed or converted to a dashboard widget. Aim for fewer than five pages per on-call shift.
- **Implement structured logging:** Use JSON-formatted logs with consistent fields (timestamp, level, service, trace_id, message) across all services. This enables efficient log querying and correlation with traces.
- **Set retention policies:** Configure tiered retention — high-resolution metrics for 15 days, downsampled metrics for 1 year, logs for 30-90 days depending on compliance requirements. This controls storage costs while maintaining historical visibility.
- **Tag and label everything:** Apply consistent labels (service, environment, team, version) to all metrics, logs, and traces so they can be filtered, grouped, and correlated across the observability stack.

## Edge Cases

- **Metric cardinality explosion:** Custom metrics with high-cardinality labels (e.g., user IDs, request URLs) can overwhelm Prometheus and cause out-of-memory crashes. Limit label values to bounded sets and use recording rules to pre-aggregate high-cardinality queries.
- **Clock skew in distributed traces:** If service clocks are out of sync, trace spans may appear out of order or have negative durations. Ensure all hosts use NTP synchronization and tolerate small timing inconsistencies in trace visualization.
- **Alert storms during outages:** A single infrastructure failure can trigger dozens of correlated alerts simultaneously. Configure alert grouping and inhibition rules in Alertmanager so that a parent alert (e.g., "node down") suppresses child alerts (e.g., "pod unhealthy on that node").
- **Missing metrics during deployments:** Rolling deployments cause pods to restart, creating gaps in time-series data. Use `rate()` functions that tolerate missing scrapes and configure absent-metric alerts with appropriate `for` durations to avoid false positives during rollouts.
- **CloudWatch API throttling:** Querying too many custom metrics or dashboards can hit CloudWatch API rate limits. Batch metric retrieval using `GetMetricData` instead of `GetMetricStatistics` and cache dashboard data on the client side.
