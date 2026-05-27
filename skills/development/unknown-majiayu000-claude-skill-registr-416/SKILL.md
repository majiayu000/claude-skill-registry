---
name: platform-health
description: Check comprehensive platform health including ArgoCD apps, pods, services, certificates, and resources across the Kagenti platform
---

# Platform Health Check Skill

This skill helps you perform comprehensive platform health checks and identify issues quickly.

## When to Use

- After deployments or cluster restarts
- Before making changes (baseline health)
- During incident investigation
- Regular health monitoring
- After running tests
- User requests "check platform" or "is everything working"

## What This Skill Does

1. **Quick Health Overview**: One-command platform status
2. **ArgoCD Apps**: Health and sync status of all applications
3. **Pod Health**: Check pods across all namespaces
4. **Service Accessibility**: Test Gateway routes and certificates
5. **Resource Usage**: CPU/memory consumption
6. **Component-Specific Checks**: Detailed validation per component

## Quick Health Check

### Comprehensive Platform Status

```bash
# Single command for full platform health (includes pytest tests)
./scripts/platform-status.sh

# What it checks:
# ✓ ArgoCD applications (health & sync status)
# ✓ Platform pods (all namespaces)
# ✓ Gateway & certificates
# ✓ Istio mTLS configuration
# ✓ Service accessibility (via Gateway)
# ✓ OAuth authentication
# ✓ Integration tests (pytest)
```

**Expected Output**:
```
=== ArgoCD Applications Status ===
✓ gateway-api: Healthy, Synced
✓ cert-manager: Healthy, Synced
✓ istio-base: Healthy, Synced
...

=== Platform Pods ===
observability    grafana-xxx         2/2     Running
observability    prometheus-xxx      2/2     Running
...

=== Gateway & Certificates ===
✓ external-gateway: Programmed
✓ grafana-cert: Ready
...

=== Integration Tests ===
PASSED tests/validation/test_app_state.py::test_critical_apps
...
```

### Quick Status Commands

```bash
# ArgoCD apps summary
argocd app list --port-forward --port-forward-namespace argocd --grpc-web

# All pods summary
kubectl get pods -A

# Failing pods only
kubectl get pods -A | grep -vE "Running|Completed"

# Service endpoints
kubectl get svc -A

# Gateway status
kubectl get gateway -A

# Certificate status
kubectl get certificate -A
```

## Detailed Health Checks

### 1. ArgoCD Application Health

```bash
# List all apps with health status
argocd app list --port-forward --port-forward-namespace argocd --grpc-web \
  -o json | jq -r '.[] | "\(.metadata.name): \(.status.health.status), \(.status.sync.status)"'

# Check for unhealthy apps
argocd app list --port-forward --port-forward-namespace argocd --grpc-web \
  | grep -E "Degraded|OutOfSync|Unknown|Missing"

# Get details for specific app
argocd app get <app-name> --port-forward --port-forward-namespace argocd --grpc-web

# Check app sync history
argocd app history <app-name> --port-forward --port-forward-namespace argocd --grpc-web
```

**Expected States**:
- **Health**: `Healthy` (✓), `Progressing` (⚠️), `Degraded` (❌), `Missing` (❌)
- **Sync**: `Synced` (✓), `OutOfSync` (⚠️)

**Critical Apps** (must be Healthy):
- gateway-api
- cert-manager
- istio-base, istiod
- tekton-pipelines
- keycloak
- kagenti-operator, kagenti-platform-operator
- kagenti-platform
- kagenti-ui

**Optional Apps** (can be Progressing):
- observability (large images, slow startup)
- kiali
- ollama

### 2. Pod Health by Namespace

```bash
# All pods with status
kubectl get pods -A -o wide

# Pods sorted by restarts
kubectl get pods -A --sort-by='.status.containerStatuses[0].restartCount' | tail -20

# Pods with issues
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded

# Pod resource usage
kubectl top pods -A --sort-by=memory
kubectl top pods -A --sort-by=cpu

# Specific namespace health
kubectl get pods -n observability
kubectl get pods -n keycloak
kubectl get pods -n kagenti-system
```

**Check for these statuses**:
- ❌ **CrashLoopBackOff**: Application crashes on startup
- ❌ **ImagePullBackOff**: Image not available
- ❌ **Error**: Container exited with error
- ⚠️ **Pending**: Waiting for resources or scheduling
- ⚠️ **Init**: Init containers still running
- ✓ **Running**: Pod healthy
- ✓ **Completed**: Job finished successfully

### 3. Service Accessibility

```bash
# Test all platform services via Gateway
for service in grafana prometheus tempo phoenix kiali keycloak kagenti; do
  echo "=== Testing https://$service.localtest.me:9443/ ==="
  curl -k -I -m 5 "https://$service.localtest.me:9443/" 2>&1 | head -3
  echo
done

# Check Gateway status
kubectl get gateway -A
kubectl describe gateway external-gateway -n default

# Check HTTPRoutes
kubectl get httproute -A
kubectl describe httproute <route-name> -n <namespace>

# Check service endpoints (should have IP addresses)
kubectl get endpoints -A | grep -v "<none>"
```

**Expected Results**:
- Grafana: HTTP/2 302 (redirect to /login)
- Prometheus: HTTP/2 302 (OAuth redirect)
- Keycloak: HTTP/2 200
- Kagenti UI: HTTP/2 200

### 4. Certificate Health

```bash
# All certificates status
kubectl get certificate -A

# Check certificate details
kubectl describe certificate <cert-name> -n <namespace>

# Check cert-manager logs for issues
kubectl logs -n cert-manager deployment/cert-manager --tail=50

# Verify certificate expiration
kubectl get certificate -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): expires \(.status.notAfter)"'
```

**Expected State**: All certificates show `Ready=True`

### 5. Istio Service Mesh Health

```bash
# Check Istio components
kubectl get pods -n istio-system

# Verify sidecar injection (should show 2/2 containers)
kubectl get pods -A -o wide | grep "2/2"

# Check mTLS policies
kubectl get peerauthentication -A
kubectl get destinationrule -A

# Istio proxy status
istioctl proxy-status

# Check specific pod mesh config
istioctl x describe pod <pod-name> -n <namespace>
```

### 6. Resource Usage

```bash
# Node resources
kubectl top nodes

# Cluster-wide pod resources
kubectl top pods -A --sort-by=memory | head -20
kubectl top pods -A --sort-by=cpu | head -20

# Namespace resource usage
kubectl top pods -n observability
kubectl top pods -n keycloak
kubectl top pods -n kagenti-system

# Check for resource pressure
kubectl get nodes -o json | jq -r '.items[] | "\(.metadata.name): \(.status.conditions[] | select(.type=="MemoryPressure" or .type=="DiskPressure") | .type)=\(.status)"'
```

### 7. Storage Health

```bash
# PersistentVolumes
kubectl get pv

# PersistentVolumeClaims
kubectl get pvc -A

# Check PVC usage via metrics
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://prometheus.observability.svc:9090/api/v1/query' \
  --data-urlencode 'query=(kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes) * 100' \
  | python3 -m json.tool
```

## Component-Specific Health Checks

### Observability Stack

```bash
# Prometheus
kubectl get pods -n observability -l app=prometheus
kubectl exec -n observability deployment/grafana -- \
  curl -s http://prometheus.observability.svc:9090/-/ready

# Grafana
kubectl get pods -n observability -l app=grafana
curl -k -I https://grafana.localtest.me:9443/api/health

# Loki
kubectl get pods -n observability -l app=loki
kubectl exec -n observability deployment/grafana -- \
  curl -s http://loki.observability.svc:3100/ready

# Tempo
kubectl get pods -n observability -l app=tempo
kubectl exec -n observability deployment/grafana -- \
  curl -s http://tempo-query-frontend.observability.svc:3100/ready

# Phoenix
kubectl get pods -n observability -l app=phoenix
curl -k -I https://phoenix.localtest.me:9443/

# AlertManager
kubectl get pods -n observability -l app=alertmanager
kubectl exec -n observability deployment/alertmanager -c alertmanager -- \
  wget -qO- http://localhost:9093/-/ready
```

### Authentication & Authorization

```bash
# Keycloak
kubectl get pods -n keycloak -l app=keycloak
kubectl exec -n keycloak statefulset/keycloak -- \
  curl -s http://localhost:8080/health/ready | python3 -m json.tool

# OAuth2-Proxy instances
kubectl get pods -n oauth2-proxy
kubectl get deployment -n oauth2-proxy

# Test Keycloak SSO
curl -k "https://keycloak.localtest.me:9443/realms/master/.well-known/openid-configuration"
```

### Platform Components

```bash
# Kagenti Operator
kubectl get pods -n kagenti-operator
kubectl logs -n kagenti-operator deployment/kagenti-operator --tail=20

# Kagenti Platform Operator
kubectl get pods -n kagenti-platform-operator
kubectl logs -n kagenti-platform-operator deployment/kagenti-platform-operator --tail=20

# Kagenti UI
kubectl get pods -n kagenti-platform -l app=kagenti-ui
curl -k -I https://kagenti.localtest.me:9443/

# Tekton Pipelines
kubectl get pods -n tekton-pipelines
kubectl get pipelineruns -A
```

## Health Check Checklists

### Post-Deployment Health Check

- [ ] All ArgoCD apps Healthy and Synced
- [ ] No pods in CrashLoopBackOff/ImagePullBackOff
- [ ] All services have endpoints
- [ ] All certificates Ready
- [ ] All Gateway routes Programmed
- [ ] Services accessible via browser
- [ ] Integration tests passing
- [ ] No firing critical alerts

### Pre-Change Health Check

- [ ] Capture platform snapshot: `./scripts/capture-platform-snapshot.sh before-change`
- [ ] All critical apps Healthy
- [ ] No existing incidents in TODO_INCIDENTS.md
- [ ] Resource usage within limits
- [ ] Recent Git commits validated

### Incident Investigation Health Check

- [ ] Identify degraded components
- [ ] Check recent events
- [ ] Collect logs from affected pods
- [ ] Query metrics for anomalies
- [ ] Check for correlated failures
- [ ] Review recent changes (Git history)

## Common Health Issues

### Issue: Pods stuck in Pending

```bash
# Check pod description for reason
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# - Insufficient CPU/memory
# - No nodes matching nodeSelector
# - Unbound PersistentVolumeClaim
```

### Issue: Pods CrashLoopBackOff

```bash
# Check previous logs
kubectl logs <pod-name> -n <namespace> --previous

# Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20

# Common causes:
# - Application error on startup
# - Missing configuration
# - Dependency not available
```

### Issue: Service not accessible

```bash
# Check pod status
kubectl get pods -n <namespace> -l app=<service>

# Check service endpoints
kubectl get endpoints -n <namespace> <service-name>

# Check HTTPRoute
kubectl get httproute -n <namespace>

# Test from inside cluster
kubectl run debug-curl -n <namespace> --image=curlimages/curl --rm -it \
  -- curl http://<service-name>.<namespace>.svc:PORT
```

### Issue: Certificate not Ready

```bash
# Check certificate status
kubectl describe certificate <cert-name> -n <namespace>

# Check cert-manager logs
kubectl logs -n cert-manager deployment/cert-manager

# Common causes:
# - DNS validation failing
# - Rate limit reached
# - Invalid configuration
```

### Issue: High resource usage

```bash
# Find top consumers
kubectl top pods -A --sort-by=memory | head -10
kubectl top pods -A --sort-by=cpu | head -10

# Check for memory leaks
kubectl logs <pod-name> -n <namespace> | grep -i "out of memory"

# Check resource limits
kubectl describe pod <pod-name> -n <namespace> | grep -A5 "Limits:"
```

## Automation & Monitoring

### Continuous Health Monitoring

```bash
# Watch pod status
watch -n 5 'kubectl get pods -A | grep -vE "Running|Completed"'

# Watch ArgoCD apps
watch -n 10 'argocd app list --port-forward --port-forward-namespace argocd --grpc-web | grep -vE "Healthy.*Synced"'

# Monitor specific namespace
watch -n 5 'kubectl get pods -n observability'
```

### Scheduled Health Checks

```bash
# Cron job for periodic health checks (local dev)
# Add to crontab: crontab -e
*/15 * * * * /path/to/kagenti-demo-deployment/scripts/platform-status.sh > /tmp/health-$(date +\%Y\%m\%d-\%H\%M).log 2>&1

# Compare snapshots over time
./scripts/capture-platform-snapshot.sh hourly-check
```

## Related Documentation

- [CLAUDE.md Platform Status](../../../CLAUDE.md#monitoring--access) - Monitoring commands
- [scripts/platform-status.sh](../../../scripts/platform-status.sh) - Automated health check
- [TODO_INCIDENTS.md](../../../TODO_INCIDENTS.md) - Active incidents
- [docs/INTEGRATION_TESTS.md](../../../docs/INTEGRATION_TESTS.md) - Test strategy

## Integration with Other Skills

**After health check, if issues found**:
- Use **investigate-incident** skill for RCA
- Use **check-logs** skill to examine error logs
- Use **check-metrics** skill for performance analysis
- Use **check-alerts** skill to see if alerts fired

## Pro Tips

1. **Always baseline first**: Run health check BEFORE making changes
2. **Use platform-status.sh**: Single command for comprehensive check
3. **Capture snapshots**: Use `capture-platform-snapshot.sh` for historical comparison
4. **Check critical apps first**: Focus on gateway-api, istio, keycloak, operators
5. **Look for patterns**: Multiple pods failing often indicates cluster-wide issue
6. **Check Git history**: Recent commits may explain new issues
7. **Verify after fixes**: Always re-run health check after remediation

🤖 Generated with [Claude Code](https://claude.com/claude-code)
