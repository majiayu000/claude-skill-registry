---
name: k8s:health
description: Check comprehensive platform health including deployments, pods, services, certificates, and resources across the Kagenti platform
---

# Platform Health Check Skill

This skill helps you perform comprehensive platform health checks and identify issues quickly.

## When to Use

- After deployments or cluster restarts
- Before making changes (baseline health)
- During incident investigation
- Regular health monitoring
- After running tests
- User asks "check platform" or "is everything working"

## Quick Health Check

### Automated Health Check Script

```bash
# Run the comprehensive health check (from CI)
chmod +x .github/scripts/verify_deployment.sh
.github/scripts/verify_deployment.sh

# What it checks:
# ✓ Resource usage (RAM, disk, CPU, Docker containers)
# ✓ Deployment status (weather-tool, weather-service, keycloak, operator)
# ✓ Pod health summary (running, pending, failed, crashloop)
# ✓ Failed pod details with events and error logs
# ✓ Iterates until healthy or timeout (default: 20 iterations × 15s = 5 minutes)

# Configure timeout
MAX_ITERATIONS=30 POLL_INTERVAL=20 .github/scripts/verify_deployment.sh
```

**Expected Output**:
```
===================================================================
  Kagenti Deployment Health Monitor
===================================================================

Configuration:
  Max Iterations: 20
  Poll Interval: 15s
  Total Timeout: 300s (5m)

━━━ Resource Usage ━━━
  Memory: 8.23/15.50 GB (53.1% used)
  Disk: 45G/234G (20% used)
  Load Avg (1/5/15m): 2.1 1.8 1.5
  Docker Containers: 12 running

━━━ Deployment Status ━━━
  ✓ weather-tool: 1/1 ready
  ✓ weather-service: 1/1 ready
  ✓ keycloak: 1/1 ready
  ✓ platform-operator: 1 ready

━━━ Pod Health Summary ━━━
  Total Pods: 45
  Running: 43
  Pending: 2

====================================================================
✓ Deployment is HEALTHY
====================================================================
```

### Run E2E Tests

```bash
cd kagenti

# Install test dependencies (first time)
uv pip install -r tests/requirements.txt

# Run all deployment health tests
uv run pytest tests/e2e/test_deployment_health.py -v

# Run only critical tests
uv run pytest tests/e2e/test_deployment_health.py -v --only-critical

# Exclude specific apps
uv run pytest tests/e2e/test_deployment_health.py -v --exclude-app=keycloak
```

**Tests check**:
- ✓ No failed pods
- ✓ No crashlooping pods (>3 restarts)
- ✓ weather-tool deployment ready
- ✓ weather-service deployment ready
- ✓ Keycloak deployment ready
- ✓ Platform Operator ready
- ✓ Services have endpoints

## Manual Health Checks

### Quick Status Commands

```bash
# All pods across all namespaces
kubectl get pods -A

# All pods sorted by status
kubectl get pods -A --sort-by=.status.phase

# Only failing pods
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded

# Pods with high restart count
kubectl get pods -A | awk '$4 > 3 {print $0}'

# All deployments
kubectl get deployments -A

# All services
kubectl get svc -A

# All namespaces
kubectl get ns
```

### Platform Components Status

```bash
# Core platform namespaces
kubectl get pods -n kagenti-system       # Platform Operator
kubectl get pods -n keycloak              # Keycloak
kubectl get pods -n istio-system          # Istio
kubectl get pods -n spire-server          # SPIRE
kubectl get pods -n tekton-pipelines      # Tekton
kubectl get pods -n cert-manager          # Cert-Manager

# Agent namespaces
kubectl get pods -n team1                 # Team1 agents/tools
kubectl get pods -n team2                 # Team2 agents/tools

# Optional observability (if addons installed)
kubectl get pods -n observability         # Prometheus, Kiali, Phoenix
```

### Check Specific Components

#### Weather Tool & Service (Demo Agents)

```bash
# Deployments
kubectl get deployment -n team1 weather-tool
kubectl get deployment -n team1 weather-service

# Pods
kubectl get pods -n team1 -l app=weather-tool
kubectl get pods -n team1 -l app=weather-service

# Services & Endpoints
kubectl get svc -n team1 weather-tool
kubectl get endpoints -n team1 weather-tool
kubectl get svc -n team1 weather-service
kubectl get endpoints -n team1 weather-service

# Check logs
kubectl logs -n team1 deployment/weather-tool --tail=50
kubectl logs -n team1 deployment/weather-service --tail=50
```

#### Keycloak (Authentication)

```bash
# Check deployment/statefulset
kubectl get deployment -n keycloak keycloak 2>/dev/null || kubectl get statefulset -n keycloak keycloak

# Check pods
kubectl get pods -n keycloak -l app=keycloak

# Check logs
kubectl logs -n keycloak deployment/keycloak --tail=50 2>/dev/null || \
kubectl logs -n keycloak statefulset/keycloak --tail=50

# Test Keycloak endpoint
kubectl exec -n keycloak deployment/keycloak -c keycloak -- \
  curl -sf http://localhost:8080/health/ready || echo "Keycloak not ready"

# Access Keycloak UI
open http://keycloak.localtest.me:8080
```

#### Platform Operator

```bash
# Check operator deployment
kubectl get deployment -n kagenti-system -l control-plane=controller-manager

# Check operator pods
kubectl get pods -n kagenti-system -l control-plane=controller-manager

# Check operator logs
kubectl logs -n kagenti-system deployment/<operator-name> --tail=100

# Check Component CRDs
kubectl get components -A
```

#### Istio Service Mesh

```bash
# Istio control plane
kubectl get pods -n istio-system

# Check sidecar injection (should show 2/2 for injected pods)
kubectl get pods -A -o wide | grep "2/2"

# Istio gateway
kubectl get gateway -A

# Virtual services
kubectl get virtualservice -A

# Destination rules
kubectl get destinationrule -A
```

#### SPIRE (Workload Identity)

```bash
# SPIRE Server
kubectl get pods -n spire-server

# SPIRE Agents (should be running on nodes)
kubectl get pods -n spire-mgmt

# Check SPIRE Server logs
kubectl logs -n spire-server deployment/spire-server --tail=50
```

#### Tekton Pipelines (Build System)

```bash
# Tekton components
kubectl get pods -n tekton-pipelines

# Pipeline runs
kubectl get pipelineruns -A

# Task runs
kubectl get taskruns -A

# Recent pipeline runs status
kubectl get pipelineruns -A --sort-by=.metadata.creationTimestamp | tail -10
```

### Resource Usage

```bash
# Node resources (if metrics-server installed)
kubectl top nodes

# Pod resources
kubectl top pods -A --sort-by=memory | head -20
kubectl top pods -A --sort-by=cpu | head -20

# Namespace resource usage
kubectl top pods -n team1
kubectl top pods -n keycloak
kubectl top pods -n kagenti-system

# Docker container stats
docker stats --no-stream
```

### Events (Recent Issues)

```bash
# All recent events
kubectl get events -A --sort-by='.lastTimestamp' | tail -30

# Events in specific namespace
kubectl get events -n team1 --sort-by='.lastTimestamp'

# Warning events only
kubectl get events -A --field-selector type=Warning

# Events for specific pod
kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>
```

## Component-Specific Health Checks

### Keycloak Authentication

```bash
# Check Keycloak readiness
kubectl exec -n keycloak deployment/keycloak -c keycloak -- \
  curl -sf http://localhost:8080/health/ready && echo "✓ Keycloak Ready" || echo "✗ Keycloak Not Ready"

# Get admin credentials
KEYCLOAK_USER=$(kubectl get secret -n keycloak keycloak-initial-admin -o jsonpath='{.data.username}' | base64 -d)
KEYCLOAK_PASS=$(kubectl get secret -n keycloak keycloak-initial-admin -o jsonpath='{.data.password}' | base64 -d)
echo "Username: $KEYCLOAK_USER"
echo "Password: $KEYCLOAK_PASS"

# Test Keycloak OIDC endpoint
curl -k "http://keycloak.localtest.me:8080/realms/master/.well-known/openid-configuration" | python3 -m json.tool
```

### Kagenti UI

```bash
# Check UI deployment
kubectl get deployment -n kagenti-system kagenti-ui

# Check UI pods
kubectl get pods -n kagenti-system -l app=kagenti-ui

# Check UI logs
kubectl logs -n kagenti-system deployment/kagenti-ui --tail=50

# Access UI
open http://kagenti-ui.localtest.me:8080
```

### Observability Stack (if addons installed)

```bash
# Prometheus
kubectl get pods -n observability -l app=prometheus
kubectl exec -n observability deployment/prometheus -- \
  curl -sf http://localhost:9090/-/ready && echo "✓ Prometheus Ready" || echo "✗ Not Ready"

# Port-forward to access
kubectl port-forward -n observability svc/prometheus 9090:9090 &
open http://localhost:9090

# Kiali
kubectl get pods -n observability -l app=kiali
kubectl port-forward -n observability svc/kiali 20001:20001 &
open http://localhost:20001

# Phoenix (LLM tracing)
kubectl get pods -n observability -l app=phoenix
open http://phoenix.localtest.me:8080
```

## Health Check Checklists

### Post-Deployment Health Check

- [ ] All critical deployments ready (weather-tool, weather-service, keycloak, operator)
- [ ] No pods in CrashLoopBackOff/ImagePullBackOff/Error
- [ ] All services have endpoints
- [ ] Resource usage within limits (< 80% memory, < 70% CPU)
- [ ] No warning/error events in last 5 minutes
- [ ] E2E tests passing
- [ ] Platform services accessible

### Pre-Change Health Check

- [ ] Capture current pod list: `kubectl get pods -A > baseline-pods.txt`
- [ ] All critical components healthy
- [ ] No existing issues in logs
- [ ] Resource headroom available
- [ ] Recent Git commits validated

### Incident Investigation Health Check

- [ ] Identify degraded components
- [ ] Check recent events: `kubectl get events -A --sort-by='.lastTimestamp' | tail -30`
- [ ] Collect logs from affected pods
- [ ] Check for resource exhaustion
- [ ] Review recent changes

## Common Health Issues

### Issue: Pods stuck in Pending

```bash
# Check pod description for reason
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# - Insufficient CPU/memory
# - No nodes available
# - Unbound PersistentVolumeClaim
# - Image pull errors

# Check node resources
kubectl top nodes
kubectl describe node <node-name>
```

### Issue: Pods in CrashLoopBackOff

```bash
# Check previous logs (before crash)
kubectl logs <pod-name> -n <namespace> --previous

# Check current logs
kubectl logs <pod-name> -n <namespace>

# Check events
kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>

# Describe pod for error details
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# - Application error on startup
# - Missing configuration/secrets
# - Dependency not available
# - Liveness/readiness probe failing
```

### Issue: Deployment not ready

```bash
# Check deployment status
kubectl get deployment -n <namespace> <deployment-name>
kubectl describe deployment -n <namespace> <deployment-name>

# Check replica set
kubectl get rs -n <namespace>
kubectl describe rs -n <namespace> <replicaset-name>

# Check pods
kubectl get pods -n <namespace> -l app=<label>

# Force rollout restart
kubectl rollout restart deployment/<deployment-name> -n <namespace>

# Check rollout status
kubectl rollout status deployment/<deployment-name> -n <namespace>
```

### Issue: Service has no endpoints

```bash
# Check service
kubectl get svc -n <namespace> <service-name>
kubectl describe svc -n <namespace> <service-name>

# Check endpoints
kubectl get endpoints -n <namespace> <service-name>

# Common causes:
# - No pods with matching labels
# - Pods not ready (failing health checks)
# - Selector mismatch

# Verify pod labels match service selector
kubectl get pods -n <namespace> --show-labels
kubectl get svc -n <namespace> <service-name> -o yaml | grep -A5 selector
```

### Issue: High resource usage

```bash
# Find top consumers
kubectl top pods -A --sort-by=memory | head -10
kubectl top pods -A --sort-by=cpu | head -10

# Check resource limits
kubectl describe pod <pod-name> -n <namespace> | grep -A10 "Limits:"

# Check for OOM kills
kubectl get events -A | grep -i "OOMKilled"

# Increase resources (edit deployment)
kubectl edit deployment -n <namespace> <deployment-name>
```

### Issue: ImagePullBackOff

```bash
# Check pod events
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# - Image doesn't exist
# - Wrong image tag
# - No access to registry
# - Network issues

# For Kind cluster, check if image is loaded
docker exec agent-platform-control-plane crictl images | grep <image-name>

# Load image into Kind
kind load docker-image <image-name> --name agent-platform
```

## Automated Monitoring

### Watch Commands

```bash
# Watch all pods
watch -n 5 'kubectl get pods -A'

# Watch failing pods only
watch -n 5 'kubectl get pods -A | grep -vE "Running|Completed"'

# Watch deployments
watch -n 5 'kubectl get deployments -A'

# Watch specific namespace
watch -n 5 'kubectl get pods -n team1'

# Watch events
watch -n 10 'kubectl get events -A --sort-by=.lastTimestamp | tail -20'
```

### Continuous Health Monitoring

```bash
# Run health check in loop
while true; do
  echo "=== Health Check $(date) ==="
  .github/scripts/verify_deployment.sh
  echo "Waiting 5 minutes..."
  sleep 300
done
```

## Integration with Other Skills

**After health check, if issues found**:
- Use **k8s:logs** skill to examine error logs
- Use **k8s:pods** skill for pod debugging
- Use **kagenti:deploy** skill if full redeploy needed

## Pro Tips

1. **Always baseline first**: Run health check BEFORE making changes
2. **Use automated script**: `.github/scripts/verify_deployment.sh` for comprehensive check
3. **Run E2E tests**: Tests validate end-to-end functionality
4. **Check critical components first**: weather-tool, keycloak, operator
5. **Look for patterns**: Multiple pods failing indicates cluster-wide issue
6. **Check events**: Recent events often reveal root cause
7. **Verify after fixes**: Always re-run health check after remediation
8. **Use --previous logs**: For crashlooping pods, check logs before crash

## Related Skills

- **kagenti:deploy**: Deploy or redeploy the platform
- **k8s:logs**: Query and analyze logs
- **k8s:pods**: Debug specific pod issues
