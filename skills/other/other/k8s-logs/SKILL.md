---
name: k8s:logs
description: Query and analyze logs from Kagenti platform components, search for errors, and investigate issues
---

# Check Logs Skill

This skill helps you query and analyze logs from the Kagenti platform components.

## When to Use

- User asks "show me logs for X"
- Investigating errors or failures
- After deployments to check for issues
- Debugging pod crashes or restarts
- Analyzing application behavior
- Finding root cause of incidents

## Quick Log Access

### View Logs for Common Components

```bash
# Weather Tool
kubectl logs -n team1 deployment/weather-tool --tail=100
kubectl logs -n team1 deployment/weather-tool --tail=100 -f  # Follow

# Weather Service
kubectl logs -n team1 deployment/weather-service --tail=100

# Keycloak
kubectl logs -n keycloak deployment/keycloak --tail=100 2>/dev/null || \
kubectl logs -n keycloak statefulset/keycloak --tail=100

# Platform Operator
kubectl logs -n kagenti-system -l control-plane=controller-manager --tail=100

# Istio Control Plane
kubectl logs -n istio-system deployment/istiod --tail=100

# SPIRE Server
kubectl logs -n spire-server deployment/spire-server --tail=100

# Tekton Controller
kubectl logs -n tekton-pipelines deployment/tekton-pipelines-controller --tail=100

# Kagenti UI
kubectl logs -n kagenti-platform deployment/kagenti-ui --tail=100
```

### Check Logs from Previous Container (After Crash)

```bash
# If pod is crashlooping, check logs before the crash
kubectl logs -n <namespace> <pod-name> --previous

# Example for weather-tool
kubectl logs -n team1 deployment/weather-tool --previous
```

### Follow Logs in Real-Time

```bash
# Follow logs
kubectl logs -n <namespace> <pod-name> -f --tail=20

# Follow multiple containers
kubectl logs -n <namespace> <pod-name> --all-containers=true -f --tail=20
```

## Search for Errors

### Find Errors Across All Namespaces

```bash
# Search for errors in all pods
for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}'); do
  echo "=== Checking namespace: $ns ==="
  kubectl logs -n $ns --all-containers=true --tail=100 2>&1 | \
    grep -iE "error|fatal|exception|panic" | head -10
done
```

### Find Errors in Specific Namespace

```bash
# Team1 namespace
kubectl logs -n team1 --all-containers=true --tail=200 | \
  grep -iE "error|fatal|exception"

# Keycloak namespace
kubectl logs -n keycloak --all-containers=true --tail=200 | \
  grep -iE "error|fatal|exception"

# Platform operator
kubectl logs -n kagenti-system -l control-plane=controller-manager --tail=200 | \
  grep -iE "error|fatal|exception"
```

### Search for Specific Error Patterns

```bash
# Connection errors
kubectl logs -n <namespace> <pod-name> | \
  grep -iE "connection (refused|timeout|reset|failed)"

# Authentication failures
kubectl logs -n keycloak --all-containers=true | \
  grep -iE "auth.*fail|unauthorized|forbidden|invalid.*token"

# OOM (Out of Memory) errors
kubectl logs -n <namespace> <pod-name> --previous | \
  grep -iE "OOM|out of memory|oom.*kill"

# Image pull errors (check events instead of logs)
kubectl get events -n <namespace> | grep -i "pull"

# Network errors
kubectl logs -n <namespace> <pod-name> | \
  grep -iE "network|dns|timeout|unreachable"
```

## Component-Specific Log Checks

### Weather Tool & Service (Demo Agents)

```bash
# Check weather-tool logs
kubectl logs -n team1 deployment/weather-tool --tail=100

# Check for errors
kubectl logs -n team1 deployment/weather-tool | grep -iE "error|fail"

# Check weather-service logs (agent)
kubectl logs -n team1 deployment/weather-service --tail=100

# Check for LLM/API errors
kubectl logs -n team1 deployment/weather-service | grep -iE "api|llm|openai|error"

# Check sidecar (Istio proxy) logs
POD=$(kubectl get pod -n team1 -l app=weather-tool -o jsonpath='{.items[0].metadata.name}')
kubectl logs -n team1 $POD -c istio-proxy --tail=50
```

### Keycloak (Authentication)

```bash
# Keycloak application logs
kubectl logs -n keycloak deployment/keycloak -c keycloak --tail=100 2>/dev/null || \
kubectl logs -n keycloak statefulset/keycloak --tail=100

# Search for authentication errors
kubectl logs -n keycloak --all-containers=true | \
  grep -iE "login.*fail|authentication.*error|invalid.*credential"

# Search for startup errors
kubectl logs -n keycloak --all-containers=true --tail=500 | \
  grep -iE "error|exception|fail" | head -20

# PostgreSQL logs (Keycloak backend)
kubectl logs -n keycloak deployment/postgresql --tail=100 2>/dev/null
```

### Platform Operator

```bash
# Operator logs
kubectl logs -n kagenti-system -l control-plane=controller-manager --tail=100

# Search for reconciliation errors
kubectl logs -n kagenti-system -l control-plane=controller-manager | \
  grep -iE "error|fail|reconcile"

# Check Component CRD processing
kubectl logs -n kagenti-system -l control-plane=controller-manager | \
  grep -i "component"
```

### Istio Service Mesh

```bash
# Istiod (control plane) logs
kubectl logs -n istio-system deployment/istiod --tail=100

# Search for certificate/mTLS errors
kubectl logs -n istio-system deployment/istiod | \
  grep -iE "tls|certificate|mtls|error"

# Check specific pod's sidecar logs
kubectl logs -n <namespace> <pod-name> -c istio-proxy --tail=50

# Search for connection errors in sidecar
kubectl logs -n <namespace> <pod-name> -c istio-proxy | \
  grep -iE "error|upstream|connection"
```

### Tekton Pipelines (Build System)

```bash
# Tekton controller logs
kubectl logs -n tekton-pipelines deployment/tekton-pipelines-controller --tail=100

# Tekton webhook logs
kubectl logs -n tekton-pipelines deployment/tekton-pipelines-webhook --tail=100

# Check pipeline run logs
PIPELINERUN=$(kubectl get pipelinerun -A -o jsonpath='{.items[-1:].metadata.name}')
NAMESPACE=$(kubectl get pipelinerun -A -o jsonpath='{.items[-1:].metadata.namespace}')
kubectl logs -n $NAMESPACE pipelinerun/$PIPELINERUN

# Check for build errors
kubectl get pipelineruns -A -o json | \
  jq -r '.items[] | select(.status.conditions[]?.type=="Succeeded" and .status.conditions[]?.status=="False") | .metadata.name'
```

### SPIRE (Workload Identity)

```bash
# SPIRE Server logs
kubectl logs -n spire-server deployment/spire-server --tail=100

# SPIRE Agent logs (runs on nodes)
kubectl logs -n spire-mgmt daemonset/spire-agent --tail=50

# Search for identity/attestation errors
kubectl logs -n spire-server deployment/spire-server | \
  grep -iE "error|attest|identity|fail"
```

## Log Analysis Patterns

### Detect Crash Loops

```bash
# Find pods with high restart counts
kubectl get pods -A | awk '$4 > 3 {print $0}'

# For each crashlooping pod, check previous logs
kubectl get pods -A --field-selector=status.phase=Running | \
  awk '$4 > 3 {print $1, $2}' | \
  while read ns pod; do
    echo "=== Logs for $pod in $ns (before crash) ==="
    kubectl logs -n $ns $pod --previous --tail=30 2>&1
    echo
  done
```

### Find HTTP Errors

```bash
# Search for HTTP error codes in logs
kubectl logs -n <namespace> <pod-name> | \
  grep -oE "HTTP/[0-9.]+ [4-5][0-9]{2}" | sort | uniq -c

# Example: Weather service HTTP errors
kubectl logs -n team1 deployment/weather-service | \
  grep -oE "[4-5][0-9]{2}" | sort | uniq -c
```

### Timeline Analysis

```bash
# Get logs with timestamps
kubectl logs -n <namespace> <pod-name> --timestamps=true --tail=200

# Filter logs by time window (last 10 minutes)
kubectl logs -n <namespace> <pod-name> --since=10m

# Logs since specific time
kubectl logs -n <namespace> <pod-name> --since-time='2025-11-21T12:00:00Z'
```

### Aggregate Logs from Multiple Pods

```bash
# Get logs from all pods with same label
kubectl logs -n <namespace> -l app=<label> --all-containers=true --tail=50

# Example: All weather-tool pods
kubectl logs -n team1 -l app=weather-tool --all-containers=true --tail=100

# Save to file for analysis
kubectl logs -n team1 -l app=weather-tool --all-containers=true --tail=500 > weather-tool-logs.txt
```

## Advanced Log Queries

### Compare Logs Before and After Event

```bash
# Save logs before change
kubectl logs -n <namespace> <pod-name> --tail=500 > before.log

# Make change, wait, then capture after
kubectl logs -n <namespace> <pod-name> --tail=500 > after.log

# Compare
diff before.log after.log
```

### Extract Structured Logs (JSON)

```bash
# If logs are in JSON format
kubectl logs -n <namespace> <pod-name> --tail=100 | \
  while read line; do echo "$line" | python3 -m json.tool 2>/dev/null || echo "$line"; done

# Extract specific JSON fields
kubectl logs -n <namespace> <pod-name> --tail=100 | \
  grep -E '^\{' | jq -r '.level, .message'
```

### Log Volume Analysis

```bash
# Count log lines per pod
for pod in $(kubectl get pods -n <namespace> -o jsonpath='{.items[*].metadata.name}'); do
  count=$(kubectl logs -n <namespace> $pod --tail=1000 2>/dev/null | wc -l)
  echo "$pod: $count lines"
done
```

## Troubleshooting with Logs

### Issue: Pod not starting

```bash
# Check init container logs
kubectl logs -n <namespace> <pod-name> -c <init-container-name>

# Check events + logs together
kubectl describe pod -n <namespace> <pod-name>
kubectl logs -n <namespace> <pod-name> --all-containers=true
```

### Issue: Intermittent failures

```bash
# Follow logs and watch for errors
kubectl logs -n <namespace> <pod-name> -f | grep -iE "error|fail"

# Capture logs over time
while true; do
  kubectl logs -n <namespace> <pod-name> --since=1m --timestamps >> captured-logs.txt
  sleep 60
done
```

### Issue: Performance degradation

```bash
# Look for slow query logs
kubectl logs -n <namespace> <pod-name> | grep -iE "slow|timeout|latency"

# Look for resource warnings
kubectl logs -n <namespace> <pod-name> | grep -iE "memory|cpu|resource"
```

## Log Retention and Export

### Export Logs for Analysis

```bash
# Export all logs from namespace
kubectl logs -n <namespace> --all-containers=true --tail=10000 > namespace-logs.txt

# Export logs from multiple components
mkdir -p logs
kubectl logs -n team1 deployment/weather-tool > logs/weather-tool.log
kubectl logs -n team1 deployment/weather-service > logs/weather-service.log
kubectl logs -n keycloak --all-containers=true > logs/keycloak.log
kubectl logs -n kagenti-system -l control-plane=controller-manager > logs/operator.log

# Create tarball
tar -czf logs-$(date +%Y%m%d-%H%M%S).tar.gz logs/
```

### Share Logs for Support

```bash
# Create debug bundle
./scripts/collect-debug-logs.sh  # If script exists

# Or manually collect key logs
mkdir -p debug-bundle
kubectl get pods -A > debug-bundle/pods.txt
kubectl get events -A --sort-by='.lastTimestamp' > debug-bundle/events.txt
kubectl logs -n team1 --all-containers=true --tail=500 > debug-bundle/team1-logs.txt
kubectl logs -n keycloak --all-containers=true --tail=500 > debug-bundle/keycloak-logs.txt
tar -czf debug-bundle-$(date +%Y%m%d-%H%M%S).tar.gz debug-bundle/
```

## Pro Tips

1. **Always check previous logs**: For crashlooping pods, `--previous` shows what caused the crash
2. **Use grep filters**: Don't dump all logs, filter for errors/warnings first
3. **Check timestamps**: Use `--timestamps=true` to correlate logs with events
4. **Check all containers**: Use `--all-containers=true` for pods with sidecars
5. **Tail appropriately**: Start with `--tail=100`, increase if needed
6. **Follow for real-time**: Use `-f` to watch logs as they happen
7. **Save to files**: For complex analysis, save logs to files
8. **Combine with events**: Logs + events give complete picture
9. **Check sidecar logs**: Istio proxy logs often reveal network issues
10. **Use since flags**: `--since=10m` for recent logs only

## Related Skills

- **k8s:health**: Check overall platform health first
- **k8s:pods**: Debug specific pod issues
- **kagenti:deploy**: Redeploy if logs show persistent issues
