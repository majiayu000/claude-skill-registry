---
name: check-metrics
description: Query Prometheus metrics, check resource usage, and analyze platform performance in the Kagenti platform
---

# Check Metrics Skill

This skill helps you query Prometheus metrics and analyze platform performance.

## When to Use

- User asks about resource usage (CPU, memory, disk)
- Investigating performance issues
- Checking service health metrics
- After deployments to verify metrics collection
- Analyzing platform capacity and scaling needs

## What This Skill Does

1. **Query Metrics**: Execute PromQL queries against Prometheus
2. **Resource Usage**: Check CPU, memory, disk usage
3. **Service Health**: Verify service metrics and availability
4. **Performance Analysis**: Analyze request rates, latency, errors
5. **Capacity Planning**: Review resource trends

## Examples

### Access Prometheus UI

**Prometheus UI**: Port-forward to access locally
```bash
kubectl port-forward -n observability svc/prometheus 9090:9090 &
# Open http://localhost:9090
```

**Grafana Explore**: https://grafana.localtest.me:9443/explore
- Select **Prometheus** datasource
- Enter PromQL queries

### Query Metrics via CLI

```bash
# Basic query
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://prometheus.observability.svc:9090/api/v1/query' \
  --data-urlencode 'query=up' | python3 -m json.tool

# Query with time range
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://prometheus.observability.svc:9090/api/v1/query_range' \
  --data-urlencode 'query=rate(container_cpu_usage_seconds_total[5m])' \
  --data-urlencode 'start='$(date -u -v-1H +%s) \
  --data-urlencode 'end='$(date -u +%s) \
  --data-urlencode 'step=60' | python3 -m json.tool
```

## Common PromQL Queries

### Service Health

```promql
# Check if services are up
up{job="kubernetes-pods"}

# Count running pods by namespace
count by (kubernetes_namespace) (up == 1)

# Check deployment replicas
kube_deployment_status_replicas_available

# Check StatefulSet replicas
kube_statefulset_status_replicas_ready
```

### CPU Usage

```promql
# Pod CPU usage (percentage of limit)
sum(rate(container_cpu_usage_seconds_total{container!="",container!="POD"}[5m])) by (namespace, pod, container)
/ sum(container_spec_cpu_quota{container!="",container!="POD"} / container_spec_cpu_period{container!="",container!="POD"}) by (namespace, pod, container) * 100

# Node CPU usage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Top CPU consuming pods
topk(10,
  sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (namespace, pod)
)
```

### Memory Usage

```promql
# Pod memory usage (percentage of limit)
sum(container_memory_working_set_bytes{container!="",container!="POD"}) by (namespace, pod, container)
/ sum(container_spec_memory_limit_bytes{container!="",container!="POD"}) by (namespace, pod, container) * 100

# Pod memory usage in bytes
container_memory_working_set_bytes{container!="",container!="POD"}

# Top memory consuming pods
topk(10,
  sum(container_memory_working_set_bytes{container!=""}) by (namespace, pod)
)
```

### Network Traffic

```promql
# Network receive rate
rate(container_network_receive_bytes_total[5m])

# Network transmit rate
rate(container_network_transmit_bytes_total[5m])

# Total network I/O by pod
sum by (pod) (
  rate(container_network_receive_bytes_total[5m]) +
  rate(container_network_transmit_bytes_total[5m])
)
```

### Disk Usage

```promql
# Filesystem usage percentage
(kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes) * 100

# PVC usage by namespace
sum by (namespace, persistentvolumeclaim) (
  kubelet_volume_stats_used_bytes
)

# Disk I/O rate
rate(container_fs_writes_bytes_total[5m])
```

### Pod Status

```promql
# Pods not running
kube_pod_status_phase{phase!="Running"}

# Pod restart count
kube_pod_container_status_restarts_total

# Pods waiting (pending)
kube_pod_status_phase{phase="Pending"}

# Pods in crash loop
kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}
```

### Request Metrics (if instrumented)

```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Request latency (p95)
histogram_quantile(0.95,
  rate(http_request_duration_seconds_bucket[5m])
)
```

## Check Specific Components

### Prometheus Metrics
```bash
# Check Prometheus scrape targets
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://prometheus.observability.svc:9090/api/v1/targets' | python3 -m json.tool

# Prometheus storage size
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://prometheus.observability.svc:9090/api/v1/status/tsdb' | python3 -m json.tool
```

### Grafana Metrics
```promql
# Grafana datasource queries
grafana_datasource_request_total

# Grafana dashboard loads
grafana_page_response_status_total
```

### Keycloak Metrics (if exposed)
```promql
# Keycloak sessions
keycloak_sessions

# Keycloak login failures
keycloak_failed_login_attempts
```

### Istio Metrics
```promql
# Istio requests
istio_requests_total

# Istio request duration
histogram_quantile(0.95,
  rate(istio_request_duration_milliseconds_bucket[5m])
)

# Istio error rate
rate(istio_requests_total{response_code=~"5.."}[5m])
```

## Resource Monitoring via kubectl

### Quick Resource Check
```bash
# Node resources
kubectl top nodes

# Pod resources (all namespaces)
kubectl top pods -A --sort-by=memory

# Pod resources (specific namespace)
kubectl top pods -n observability --sort-by=cpu

# Container resources in pod
kubectl top pod <pod-name> -n <namespace> --containers
```

### Resource Limits and Requests
```bash
# Show resource requests/limits for deployment
kubectl describe deployment <name> -n <namespace> | grep -A 5 "Limits\|Requests"

# Show all pod resource requests
kubectl get pods -n <namespace> -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources}{"\n"}{end}'
```

## Grafana Dashboards

**Access**: https://grafana.localtest.me:9443/dashboards

**Key Dashboards**:
1. **Kubernetes / Compute Resources / Cluster** - Overall cluster metrics
2. **Kubernetes / Compute Resources / Namespace (Pods)** - Per-namespace pod resources
3. **Kubernetes / Compute Resources / Pod** - Individual pod metrics
4. **Prometheus** - Prometheus self-monitoring
5. **Loki Logs** - Log volume and patterns
6. **Istio Mesh** - Service mesh metrics

### Create Custom Queries in Grafana

1. Navigate to **Explore** (compass icon in sidebar)
2. Select **Prometheus** datasource
3. Enter PromQL query
4. Click "Run query"
5. Optionally save to dashboard

## Troubleshooting with Metrics

### Issue: High CPU Usage
```promql
# Find pods using >80% CPU
sum(rate(container_cpu_usage_seconds_total[5m])) by (namespace, pod, container)
/ sum(container_spec_cpu_quota / container_spec_cpu_period) by (namespace, pod, container) * 100 > 80
```

### Issue: High Memory Usage
```promql
# Find pods using >80% memory
sum(container_memory_working_set_bytes) by (namespace, pod, container)
/ sum(container_spec_memory_limit_bytes) by (namespace, pod, container) * 100 > 80
```

### Issue: Service Not Responding
```promql
# Check if service endpoints are up
up{job="kubernetes-service-endpoints"}

# Check scrape failures
up == 0
```

### Issue: Disk Full
```promql
# Find PVCs >80% full
(kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes) * 100 > 80
```

## Alert Query Testing

When investigating alerts, test the PromQL query:

```bash
# Get alert query from Grafana
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://localhost:3000/api/v1/provisioning/alert-rules' \
  -u admin:admin123 | python3 -c "
import sys, json
rules = json.load(sys.stdin)
alert_uid = 'prometheus-down'  # Change this
rule = next((r for r in rules if r.get('uid') == alert_uid), None)
if rule:
    query = rule['data'][0]['model']['expr']
    print(f'Query: {query}')
"

# Test the query
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://prometheus.observability.svc:9090/api/v1/query' \
  --data-urlencode "query=<QUERY_FROM_ABOVE>" | python3 -m json.tool
```

## Metrics Collection Issues

### Check if Metrics Are Being Scraped
```promql
# Check last scrape time
time() - timestamp(up)

# Check scrape duration
scrape_duration_seconds
```

### Verify Metric Exists
```bash
# List all metrics
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://prometheus.observability.svc:9090/api/v1/label/__name__/values' | python3 -m json.tool

# Search for specific metric
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://prometheus.observability.svc:9090/api/v1/label/__name__/values' | grep "your_metric"
```

## Related Documentation

- [PromQL Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Explore](https://grafana.com/docs/grafana/latest/explore/)
- [Alert Testing Guide](../../../docs/04-observability/ALERT_TESTING_GUIDE.md)
- [CLAUDE.md Monitoring](../../../CLAUDE.md#monitoring--access)

## Pro Tips

1. **Use rate() for counters**: `rate(metric[5m])` instead of raw counter values
2. **Aggregate with by/without**: `sum by (namespace) (metric)` to group metrics
3. **Use recording rules**: For frequently used complex queries
4. **Set appropriate time ranges**: Use `[5m]` for rate calculations
5. **Test queries in Explore first**: Before adding to dashboards or alerts

🤖 Generated with [Claude Code](https://claude.com/claude-code)
