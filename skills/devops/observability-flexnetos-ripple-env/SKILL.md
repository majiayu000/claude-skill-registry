---
name: observability
description: Monitoring and observability tools including Prometheus, OpenTelemetry, and Netdata
icon: 📊
category: infrastructure
tools:
  - prometheus
  - promtool
  - alertmanager
  - grafana
  - netdata
  - otel-collector
---

# Observability Skills

## Overview

This skill provides expertise in monitoring, metrics collection, and observability for robotics systems and distributed infrastructure.

## Prometheus - Metrics and Alerting

Prometheus is the standard for metrics collection in cloud-native environments.

### Installation (Nix)

```nix
{ pkgs, ... }:
{
  packages = with pkgs; [
    prometheus
    alertmanager
    prometheus-node-exporter
    grafana
  ];
}
```

### Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']

rule_files:
  - "alerts/*.yml"

scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # ROS2 nodes (custom exporter)
  - job_name: 'ros2_nodes'
    static_configs:
      - targets: ['localhost:9100']
    metrics_path: /metrics

  # NATS server
  - job_name: 'nats'
    static_configs:
      - targets: ['localhost:8222']
    metrics_path: /varz

  # Node exporter (system metrics)
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

### Alert Rules

```yaml
# alerts/robot_alerts.yml
groups:
  - name: robot_alerts
    rules:
      - alert: RobotOffline
        expr: up{job="ros2_nodes"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Robot {{ $labels.instance }} is offline"

      - alert: LowBattery
        expr: robot_battery_percent < 20
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Robot {{ $labels.robot_id }} battery low ({{ $value }}%)"

      - alert: HighLatency
        expr: ros2_topic_latency_seconds > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High latency on topic {{ $labels.topic }}"
```

### Python Prometheus Client

```python
from prometheus_client import start_http_server, Gauge, Counter, Histogram
import rclpy
from rclpy.node import Node

# Define metrics
ROBOT_BATTERY = Gauge('robot_battery_percent', 'Battery level', ['robot_id'])
COMMANDS_TOTAL = Counter('robot_commands_total', 'Total commands', ['robot_id', 'command'])
TOPIC_LATENCY = Histogram('ros2_topic_latency_seconds', 'Topic latency', ['topic'])

class MetricsNode(Node):
    def __init__(self):
        super().__init__('metrics_exporter')

        # Start Prometheus HTTP server
        start_http_server(9100)

        # Subscribe to battery topic
        self.create_subscription(
            BatteryState,
            '/battery',
            self.battery_callback,
            10
        )

    def battery_callback(self, msg):
        ROBOT_BATTERY.labels(robot_id='robot_1').set(msg.percentage * 100)

    def record_command(self, command: str):
        COMMANDS_TOTAL.labels(robot_id='robot_1', command=command).inc()

    def record_latency(self, topic: str, latency: float):
        TOPIC_LATENCY.labels(topic=topic).observe(latency)
```

### PromQL Examples

```promql
# Average CPU usage over 5 minutes
avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)

# Robot battery levels
robot_battery_percent

# Message rate per topic
rate(ros2_messages_total[1m])

# 95th percentile latency
histogram_quantile(0.95, rate(ros2_topic_latency_seconds_bucket[5m]))

# Robots with low battery
robot_battery_percent < 20
```

## OpenTelemetry - Unified Observability

OpenTelemetry provides traces, metrics, and logs in a vendor-neutral format.

### Installation

```bash
pixi add opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

### Python Integration

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Setup metrics
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="localhost:4317", insecure=True)
)
metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))
meter = metrics.get_meter(__name__)

# Usage in ROS2 node
class TracedNode(Node):
    def __init__(self):
        super().__init__('traced_node')
        self.command_counter = meter.create_counter(
            "robot_commands",
            description="Number of robot commands"
        )

    def execute_command(self, command: str):
        with tracer.start_as_current_span("execute_command") as span:
            span.set_attribute("command", command)
            self.command_counter.add(1, {"command": command})

            # Your logic here
            result = self._do_command(command)

            span.set_attribute("result", result)
            return result
```

### OTel Collector Configuration

```yaml
# otel-collector.yml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"

  jaeger:
    endpoint: "jaeger:14250"
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

## Netdata - Real-Time Monitoring

Netdata provides instant visibility into system and application metrics.

### Installation

```bash
# One-line install
bash <(curl -Ss https://get.netdata.cloud/kickstart.sh)

# Or via Nix
nix profile install nixpkgs#netdata
```

### Custom ROS2 Plugin

```python
#!/usr/bin/env python3
# /etc/netdata/python.d/ros2.chart.py

from bases.FrameworkServices.SimpleService import SimpleService
import subprocess
import json

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ['topics', 'nodes', 'latency']
        self.definitions = {
            'topics': {
                'options': [None, 'ROS2 Topics', 'count', 'ros2', 'ros2.topics', 'line'],
                'lines': [['active_topics', 'topics', 'absolute']]
            },
            'nodes': {
                'options': [None, 'ROS2 Nodes', 'count', 'ros2', 'ros2.nodes', 'line'],
                'lines': [['active_nodes', 'nodes', 'absolute']]
            }
        }

    def get_data(self):
        data = {}
        try:
            # Count topics
            result = subprocess.run(['ros2', 'topic', 'list'], capture_output=True, text=True)
            data['active_topics'] = len(result.stdout.strip().split('\n'))

            # Count nodes
            result = subprocess.run(['ros2', 'node', 'list'], capture_output=True, text=True)
            data['active_nodes'] = len(result.stdout.strip().split('\n'))
        except Exception:
            pass
        return data
```

## Grafana Dashboards

### ROS2 Dashboard JSON

```json
{
  "title": "ROS2 Robotics Dashboard",
  "panels": [
    {
      "title": "Robot Battery Levels",
      "type": "gauge",
      "targets": [
        {
          "expr": "robot_battery_percent",
          "legendFormat": "{{ robot_id }}"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              {"color": "red", "value": 0},
              {"color": "yellow", "value": 20},
              {"color": "green", "value": 50}
            ]
          },
          "max": 100,
          "min": 0,
          "unit": "percent"
        }
      }
    },
    {
      "title": "Message Rate by Topic",
      "type": "timeseries",
      "targets": [
        {
          "expr": "rate(ros2_messages_total[1m])",
          "legendFormat": "{{ topic }}"
        }
      ]
    },
    {
      "title": "Topic Latency (p95)",
      "type": "timeseries",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, rate(ros2_topic_latency_seconds_bucket[5m]))",
          "legendFormat": "{{ topic }}"
        }
      ]
    }
  ]
}
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Grafana Dashboard                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        v                  v                  v
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  Prometheus   │  │    Jaeger     │  │     Loki      │
│   (Metrics)   │  │   (Traces)    │  │    (Logs)     │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                  ┌────────┴────────┐
                  │  OTel Collector │
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        v                  v                  v
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   Robot 1     │  │   Robot 2     │  │   Services    │
│   (ROS2)      │  │   (ROS2)      │  │   (Backend)   │
└───────────────┘  └───────────────┘  └───────────────┘
```

## Best Practices

1. **Use labels wisely** - Don't create high-cardinality metrics
2. **Set retention policies** - Balance storage vs history needs
3. **Alert on symptoms** - Alert on user-facing issues, not causes
4. **Instrument at boundaries** - Trace requests across services
5. **Use dashboards** - Visualize trends, not just current state

## Related Skills

- [Distributed Systems](../distributed-systems/SKILL.md) - NATS metrics
- [DevOps](../devops/SKILL.md) - CI/CD monitoring
- [ROS2 Development](../ros2-development/SKILL.md) - ROS2 metrics
