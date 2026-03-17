---
name: monitoring
description: 监控与告警
version: 1.0.0
author: terminal-skills
tags: [devops, monitoring, prometheus, grafana, alerting]
---

# 监控与告警

## 概述
Prometheus、Grafana、告警规则配置等技能。

## Prometheus

### 基础查询（PromQL）
```promql
# 即时向量
http_requests_total
http_requests_total{job="api", status="200"}

# 范围向量
http_requests_total[5m]

# 偏移
http_requests_total offset 1h

# 聚合
sum(http_requests_total)
sum by (job) (http_requests_total)
sum without (instance) (http_requests_total)

# 速率
rate(http_requests_total[5m])
irate(http_requests_total[5m])

# 增量
increase(http_requests_total[1h])

# 直方图分位数
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### 常用查询
```promql
# CPU 使用率
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 内存使用率
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100

# 磁盘使用率
(1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100

# 网络流量
rate(node_network_receive_bytes_total[5m])
rate(node_network_transmit_bytes_total[5m])

# HTTP 请求速率
sum(rate(http_requests_total[5m])) by (status)

# 错误率
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# 延迟 P99
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### 配置文件
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node1:9100', 'node2:9100']

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### 告警规则
```yaml
# rules/alerts.yml
groups:
  - name: node
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value }}%"

      - alert: HighMemoryUsage
        expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"

      - alert: DiskSpaceLow
        expr: (1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 > 85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space low on {{ $labels.instance }}"

  - name: application
    rules:
      - alert: HighErrorRate
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency"
```

## Alertmanager

### 配置
```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alertmanager@example.com'
  smtp_auth_username: 'alertmanager@example.com'
  smtp_auth_password: 'password'

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'
    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'default'
    email_configs:
      - to: 'team@example.com'

  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/xxx'
        channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'xxx'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
```

## Grafana

### 数据源配置
```yaml
# provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
```

### Dashboard JSON 示例
```json
{
  "dashboard": {
    "title": "Node Metrics",
    "panels": [
      {
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "gauge",
        "targets": [
          {
            "expr": "(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100"
          }
        ]
      }
    ]
  }
}
```

### 常用面板查询
```promql
# CPU 使用率（时间序列）
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 内存使用（仪表盘）
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100

# 请求速率（柱状图）
sum(rate(http_requests_total[5m])) by (status)

# 延迟热力图
sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
```

## 常见场景

### 场景 1：Kubernetes 监控
```yaml
# ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-monitor
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
    - port: metrics
      interval: 15s
      path: /metrics
```

### 场景 2：自定义指标
```python
# Python 应用
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])

@REQUEST_LATENCY.labels(method='GET', endpoint='/api').time()
def handle_request():
    REQUEST_COUNT.labels(method='GET', endpoint='/api', status='200').inc()
    # ...

start_http_server(8000)
```

### 场景 3：SLO 监控
```promql
# 可用性 SLO (99.9%)
1 - (sum(rate(http_requests_total{status=~"5.."}[30d])) / sum(rate(http_requests_total[30d])))

# 错误预算消耗
(1 - (sum(rate(http_requests_total{status=~"5.."}[7d])) / sum(rate(http_requests_total[7d])))) / 0.999

# 延迟 SLO (P99 < 500ms)
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[30d])) by (le)) < 0.5
```

### 场景 4：告警静默
```bash
# 创建静默
amtool silence add alertname=HighCPUUsage instance=node1 --duration=2h --comment="Maintenance"

# 查看静默
amtool silence query

# 删除静默
amtool silence expire <silence-id>
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 指标缺失 | 检查 scrape 配置、target 状态 |
| 告警不触发 | 检查规则语法、Alertmanager 配置 |
| 查询慢 | 优化 PromQL、增加采样间隔 |
| 存储满 | 调整 retention、清理旧数据 |

```bash
# 检查 Prometheus targets
curl http://prometheus:9090/api/v1/targets

# 检查告警规则
curl http://prometheus:9090/api/v1/rules

# 检查 Alertmanager 状态
curl http://alertmanager:9093/api/v1/status

# 测试 PromQL
curl 'http://prometheus:9090/api/v1/query?query=up'
```
