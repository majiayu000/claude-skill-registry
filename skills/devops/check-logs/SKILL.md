---
name: check-logs
description: Query and analyze logs using Grafana Loki for the Kagenti platform, search for errors, and investigate issues
---

# Check Logs Skill

This skill helps you query and analyze logs from the Kagenti platform using Loki via Grafana.

## When to Use

- User asks "show me logs for X"
- Investigating errors or failures
- After deployments to check for issues
- Debugging pod crashes or restarts
- Analyzing application behavior

## What This Skill Does

1. **Query Logs**: Search logs by namespace, pod, container, or log level
2. **Error Detection**: Find errors and warnings in logs
3. **Log Aggregation**: View logs across multiple pods
4. **Time-based Queries**: Query logs for specific time ranges
5. **Log Patterns**: Detect common issues from log patterns

## Examples

### Query Logs in Grafana UI

**Access Grafana**: https://grafana.localtest.me:9443
**Navigate**: **Explore** → Select **Loki** datasource

**Log Dashboard**: https://grafana.localtest.me:9443/d/loki-logs/loki-logs

**Query Examples in Grafana Explore**:

```logql
# All logs from observability namespace
{kubernetes_namespace_name="observability"}

# Logs from specific pod
{kubernetes_pod_name=~"prometheus.*"}

# Logs with errors
{kubernetes_namespace_name="observability"} |= "error"

# Logs from last 5 minutes with level=error
{kubernetes_namespace_name="observability"} | json | level="error"

# Count errors per namespace
sum by (kubernetes_namespace_name) (count_over_time({kubernetes_namespace_name=~".+"} |= "error" [5m]))
```

### Query Logs via CLI (Promtail/Loki)

```bash
# Query Loki for recent errors in observability namespace
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://loki.observability.svc:3100/loki/api/v1/query_range' \
  --data-urlencode 'query={kubernetes_namespace_name="observability"} |= "error"' \
  --data-urlencode 'limit=100' \
  --data-urlencode 'start='$(date -u -v-5M +%s)000000000 \
  --data-urlencode 'end='$(date -u +%s)000000000 | python3 -m json.tool
```

### Check Logs for Specific Pod

```bash
# Get logs for a specific pod using kubectl
kubectl logs -n observability deployment/prometheus --tail=100

# Get logs from previous container (if crashed)
kubectl logs -n observability pod/prometheus-xxx --previous

# Follow logs in real-time
kubectl logs -n observability deployment/grafana -f --tail=20

# Get logs from specific container in pod
kubectl logs -n observability pod/alertmanager-xxx -c alertmanager --tail=50
```

### Search for Errors Across Platform

```bash
# Get recent error logs from all namespaces
for ns in observability keycloak oauth2-proxy istio-system kiali-system; do
  echo "=== Errors in $ns ==="
  kubectl logs -n $ns --all-containers=true --tail=50 2>&1 | grep -i "error\|fatal\|exception" | head -5
  echo
done
```

### Check Logs for Failed Pods

```bash
# Find pods with issues and check their logs
kubectl get pods -A | grep -E "Error|CrashLoop|ImagePull" | while read ns pod rest; do
  echo "=== Logs for $pod in $ns ==="
  kubectl logs -n $ns $pod --tail=30 --previous 2>/dev/null || kubectl logs -n $ns $pod --tail=30
  echo
done
```

### Query Log Volume by Namespace

```logql
# In Grafana Explore (Loki datasource)
sum by (kubernetes_namespace_name) (
  rate({kubernetes_namespace_name=~".+"}[5m])
)
```

### Search for Specific Error Pattern

```logql
# Find connection errors
{kubernetes_namespace_name="observability"} |~ "connection (refused|timeout|reset)"

# Find authentication failures
{kubernetes_namespace_name=~"keycloak|oauth2-proxy"} |~ "auth.*fail|unauthorized|forbidden"

# Find OOM kills
{kubernetes_namespace_name=~".+"} |~ "OOM|out of memory|oom.*kill"
```

## Log Levels and Filtering

### Standard Log Levels
- **error**: Critical errors requiring attention
- **warn/warning**: Warnings that may indicate issues
- **info**: Informational messages
- **debug**: Detailed debugging information
- **trace**: Very detailed trace information

### Filter by Log Level

```logql
# Only errors
{kubernetes_namespace_name="observability"} | json | level="error"

# Errors and warnings
{kubernetes_namespace_name="observability"} | json | level=~"error|warn"

# Everything except debug
{kubernetes_namespace_name="observability"} | json | level!="debug"
```

## Common Log Queries for Platform Components

### Prometheus Logs
```bash
kubectl logs -n observability deployment/prometheus --tail=100

# Check for scrape errors
kubectl logs -n observability deployment/prometheus | grep -i "scrape\|error"
```

### Grafana Logs
```bash
kubectl logs -n observability deployment/grafana --tail=100

# Check for datasource errors
kubectl logs -n observability deployment/grafana | grep -i "datasource\|error"
```

### Keycloak Logs
```bash
kubectl logs -n keycloak statefulset/keycloak --tail=100

# Check for authentication errors
kubectl logs -n keycloak statefulset/keycloak | grep -i "auth\|login\|error"
```

### Istio Proxy (Sidecar) Logs
```bash
# Check sidecar logs for a specific pod
POD=$(kubectl get pod -n observability -l app=alertmanager -o jsonpath='{.items[0].metadata.name}')
kubectl logs -n observability $POD -c istio-proxy --tail=50
```

### AlertManager Logs
```bash
kubectl logs -n observability deployment/alertmanager -c alertmanager --tail=100

# Check for notification errors
kubectl logs -n observability deployment/alertmanager -c alertmanager | grep -i "notif\|error\|fail"
```

## Log Analysis Patterns

### Detect Crash Loops
```bash
# Find pods restarting frequently
kubectl get pods -A | awk '{if ($4 > 5) print $0}'

# Check logs before crash
kubectl logs -n <namespace> <pod-name> --previous | tail -50
```

### Find HTTP Errors
```logql
{kubernetes_namespace_name=~".+"} |~ "HTTP.*[45]\\d{2}"
```

### Find Timeout Errors
```logql
{kubernetes_namespace_name=~".+"} |~ "timeout|timed out|deadline exceeded"
```

### Find Database Connection Issues
```logql
{kubernetes_namespace_name=~".+"} |~ "database.*error|connection.*refused|SQL.*error"
```

## Troubleshooting with Logs

### Issue: Service Not Starting
1. Check pod events: `kubectl describe pod <pod-name> -n <namespace>`
2. Check container logs: `kubectl logs <pod-name> -n <namespace>`
3. Check init container logs: `kubectl logs <pod-name> -n <namespace> -c <init-container>`

### Issue: High Error Rate
1. Query error logs: `{kubernetes_namespace_name="X"} |= "error" [5m]`
2. Group by component: `sum by (kubernetes_pod_name) (count_over_time({...} |= "error" [5m]))`
3. Identify pattern in error messages

### Issue: Performance Degradation
1. Check for warnings: `{kubernetes_namespace_name="X"} |= "warn"`
2. Look for timeout messages
3. Check for resource exhaustion messages

## Grafana Loki Dashboard Features

**Loki Logs Dashboard**: https://grafana.localtest.me:9443/d/loki-logs/loki-logs

**Features**:
- **Namespace filter**: Select specific namespace
- **Pod filter**: Filter by pod name
- **Log level**: Filter by error/warn/info/debug
- **Time range**: Select time window
- **Log volume graphs**: See log rate over time
- **Log table**: Browse actual log lines

**Panels**:
1. **Log Volume by Level**: See errors vs warnings over time
2. **Log Volume by Namespace**: Compare activity across namespaces
3. **Logs per Second**: Current log ingestion rate
4. **Log Lines**: Actual log content with search

## Related Documentation

- [Loki Documentation](https://grafana.com/docs/loki/)
- [LogQL Query Language](https://grafana.com/docs/loki/latest/logql/)
- [CLAUDE.md Troubleshooting](../../../CLAUDE.md#troubleshooting)
- [Alert Runbooks](../../../docs/runbooks/alerts/) - Many reference logs

## Pro Tips

1. **Use time ranges**: Always specify time range to limit data
2. **Filter early**: Add namespace/pod filters before log level filters (more efficient)
3. **Use regex carefully**: Complex regex can be slow on large log volumes
4. **Check both current and previous**: For crashed pods, use `--previous`
5. **Tail first**: Use `--tail=N` to limit output, then increase if needed

🤖 Generated with [Claude Code](https://claude.com/claude-code)
