---
name: k8s:pods
description: Debug and troubleshoot pod issues including crashes, failures, networking, and resource problems
---

# Troubleshoot Pods Skill

This skill provides systematic approaches to debugging pod issues in the Kagenti platform.

## When to Use

- Pods are crashlooping or failing
- Pods stuck in Pending, ImagePullBackOff, or other error states
- User reports application not working
- After `kagenti:deploy` to verify pods are healthy
- Investigating resource issues

## Quick Pod Status Check

```bash
# All pods with status
kubectl get pods -A -o wide

# Only problematic pods
kubectl get pods -A | grep -vE "Running|Completed"

# Pods sorted by restarts
kubectl get pods -A --sort-by='.status.containerStatuses[0].restartCount' | tail -20

# Pods with high restart count
kubectl get pods -A | awk '$4 > 3 {print $0}'

# Recent pod events
kubectl get events -A --sort-by='.lastTimestamp' | tail -30
```

## Common Pod States

### Running - Healthy ✓
Pod is running normally. Check if app inside is working correctly.

### Pending - Waiting for resources ⏳
```bash
# Check why pod is pending
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# - Insufficient CPU/memory on nodes
# - Unbound PersistentVolumeClaim
# - Node selector not matching any nodes
# - Image pull in progress

# Check node resources
kubectl top nodes
kubectl describe nodes
```

### CrashLoopBackOff - Application crashing ❌
```bash
# Check logs before crash
kubectl logs -n <namespace> <pod-name> --previous

# Check current logs
kubectl logs -n <namespace> <pod-name>

# Check pod events
kubectl describe pod -n <namespace> <pod-name>

# Common causes:
# - Application error on startup
# - Missing configuration/secrets
# - Failed liveness probe
# - Dependency not available
```

### ImagePullBackOff - Cannot pull image ❌
```bash
# Check pod events for exact error
kubectl describe pod -n <namespace> <pod-name>

# Check if image exists in registry
docker pull <image-name>

# For Kind cluster, load image manually
kind load docker-image <image-name> --name agent-platform

# Check if image is in Kind cluster
docker exec agent-platform-control-plane crictl images | grep <image-name>

# Common causes:
# - Image doesn't exist
# - Wrong image tag
# - No access to registry (auth)
# - Network issues
```

### Error - Container exited with error ❌
```bash
# Check exit code and reason
kubectl describe pod -n <namespace> <pod-name> | grep -A5 "State:"

# Check logs
kubectl logs -n <namespace> <pod-name> --previous

# Common exit codes:
# 0 - Success
# 1 - General error
# 137 - SIGKILL (OOM killed)
# 143 - SIGTERM (terminated)
```

### OOMKilled - Out of memory ❌
```bash
# Check for OOM in events
kubectl get events -A | grep -i "OOMKilled"

# Check pod memory limits
kubectl describe pod -n <namespace> <pod-name> | grep -A10 "Limits:"

# Check actual memory usage
kubectl top pod -n <namespace> <pod-name>

# Fix: Increase memory limits
kubectl edit deployment -n <namespace> <deployment-name>
# Increase resources.limits.memory and resources.requests.memory
```

## Systematic Troubleshooting

### Step 1: Get Pod Details

```bash
# Get pod status
kubectl get pod -n <namespace> <pod-name>

# Get full pod description
kubectl describe pod -n <namespace> <pod-name>

# Check pod YAML
kubectl get pod -n <namespace> <pod-name> -o yaml

# Check pod events
kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>
```

### Step 2: Check Logs

```bash
# Current logs
kubectl logs -n <namespace> <pod-name>

# Previous logs (if crashed)
kubectl logs -n <namespace> <pod-name> --previous

# All containers (including sidecars)
kubectl logs -n <namespace> <pod-name> --all-containers=true

# Specific container
kubectl logs -n <namespace> <pod-name> -c <container-name>

# Follow logs
kubectl logs -n <namespace> <pod-name> -f --tail=20
```

### Step 3: Check Resource Constraints

```bash
# Check resource usage
kubectl top pod -n <namespace> <pod-name>

# Check resource limits
kubectl describe pod -n <namespace> <pod-name> | grep -A10 "Limits:"
kubectl describe pod -n <namespace> <pod-name> | grep -A10 "Requests:"

# Check node resources
kubectl top nodes
```

### Step 4: Check Configuration

```bash
# Check environment variables
kubectl describe pod -n <namespace> <pod-name> | grep -A20 "Environment:"

# Check mounted secrets
kubectl describe pod -n <namespace> <pod-name> | grep -A10 "Mounts:"

# Verify secret exists
kubectl get secret -n <namespace> <secret-name>

# Check configmap
kubectl get configmap -n <namespace> <configmap-name>
```

### Step 5: Check Networking

```bash
# Check service endpoints
kubectl get endpoints -n <namespace> <service-name>

# Check if pod is in service
kubectl get endpoints -n <namespace> <service-name> -o yaml

# Test connectivity FROM the pod
kubectl exec -n <namespace> <pod-name> -- curl -I http://<service-name>

# Test connectivity TO the pod
kubectl run debug-curl --image=curlimages/curl --rm -it -- \
  curl http://<pod-ip>:<port>

# Check network policies
kubectl get networkpolicy -n <namespace>
```

## Component-Specific Troubleshooting

### Weather Tool / Weather Service

```bash
# Check deployment
kubectl get deployment -n team1 weather-tool
kubectl describe deployment -n team1 weather-tool

# Check pods
kubectl get pods -n team1 -l app=weather-tool

# Check service endpoints
kubectl get endpoints -n team1 weather-tool

# Test MCP endpoint (weather-tool)
kubectl exec -n team1 deployment/weather-tool -- \
  curl -I http://localhost:8000/health || echo "Health check failed"

# Check for API errors (weather service)
kubectl logs -n team1 deployment/weather-service | grep -iE "api|error|openai"
```

### Keycloak

```bash
# Check if Keycloak is deployment or statefulset
kubectl get deployment -n keycloak keycloak 2>/dev/null || kubectl get statefulset -n keycloak keycloak

# Check pod status
kubectl get pods -n keycloak -l app=keycloak

# Check readiness
kubectl exec -n keycloak deployment/keycloak -c keycloak -- \
  curl -sf http://localhost:8080/health/ready || echo "Not ready"

# Check PostgreSQL dependency
kubectl get pods -n keycloak -l app=postgresql
kubectl logs -n keycloak deployment/postgresql --tail=50 2>/dev/null

# Common issues:
# - PostgreSQL not ready
# - Database connection failures
# - Memory limits too low (increase to 1Gi)
```

### Platform Operator

```bash
# Check operator deployment
kubectl get deployment -n kagenti-system -l control-plane=controller-manager

# Check operator pods
kubectl get pods -n kagenti-system -l control-plane=controller-manager

# Check operator logs for errors
kubectl logs -n kagenti-system -l control-plane=controller-manager | \
  grep -iE "error|fail"

# Check Component CRD processing
kubectl get components -A
kubectl describe component -n <namespace> <component-name>

# Check if operator is reconciling
kubectl logs -n kagenti-system -l control-plane=controller-manager --tail=50 | \
  grep -i "reconcile"
```

### Istio Sidecars

```bash
# Check if sidecar is injected
kubectl get pod -n <namespace> <pod-name> -o jsonpath='{.spec.containers[*].name}'
# Should show: <app-container> istio-proxy

# Check sidecar status
kubectl get pod -n <namespace> <pod-name> -o jsonpath='{.status.containerStatuses[?(@.name=="istio-proxy")].ready}'
# Should show: true

# Check sidecar logs
kubectl logs -n <namespace> <pod-name> -c istio-proxy

# Common issues:
# - Sidecar not injected (check namespace label)
# - mTLS errors (check certificates)
# - Connection failures (check virtual services)
```

## Interactive Debugging

### Execute Commands in Pod

```bash
# Get shell access
kubectl exec -n <namespace> <pod-name> -it -- /bin/sh
# or
kubectl exec -n <namespace> <pod-name> -it -- /bin/bash

# Run specific command
kubectl exec -n <namespace> <pod-name> -- ls -la /app
kubectl exec -n <namespace> <pod-name> -- env
kubectl exec -n <namespace> <pod-name> -- cat /etc/resolv.conf

# Test network connectivity
kubectl exec -n <namespace> <pod-name> -- ping <service-name>
kubectl exec -n <namespace> <pod-name> -- curl http://<service-name>:<port>
kubectl exec -n <namespace> <pod-name> -- nslookup <service-name>
```

### Debug with Temporary Pods

```bash
# Create debug pod in same namespace
kubectl run debug-pod -n <namespace> --image=busybox --rm -it -- sh

# Test network connectivity
kubectl run debug-curl -n <namespace> --image=curlimages/curl --rm -it -- \
  curl -v http://<service-name>:<port>

# Test DNS resolution
kubectl run debug-dns -n <namespace> --image=busybox --rm -it -- \
  nslookup <service-name>

# Check pod-to-pod connectivity
kubectl run debug-net -n <namespace> --image=nicolaka/netshoot --rm -it -- \
  curl http://<pod-ip>:<port>
```

## Restart and Recovery

### Restart Pod

```bash
# Delete pod (deployment will recreate)
kubectl delete pod -n <namespace> <pod-name>

# Restart deployment (all pods)
kubectl rollout restart deployment -n <namespace> <deployment-name>

# Scale to zero and back (forces recreation)
kubectl scale deployment -n <namespace> <deployment-name> --replicas=0
kubectl scale deployment -n <namespace> <deployment-name> --replicas=1
```

### Force Redeploy

```bash
# Update deployment to force new pods
kubectl patch deployment -n <namespace> <deployment-name> \
  -p "{\"spec\":{\"template\":{\"metadata\":{\"annotations\":{\"kubectl.kubernetes.io/restartedAt\":\"$(date +%Y-%m-%dT%H:%M:%S)\"}}}}}"

# Check rollout status
kubectl rollout status deployment -n <namespace> <deployment-name>
```

### Rollback Deployment

```bash
# Check deployment history
kubectl rollout history deployment -n <namespace> <deployment-name>

# Rollback to previous version
kubectl rollout undo deployment -n <namespace> <deployment-name>

# Rollback to specific revision
kubectl rollout undo deployment -n <namespace> <deployment-name> --to-revision=2
```

## Resource Adjustments

### Increase Memory/CPU

```bash
# Edit deployment
kubectl edit deployment -n <namespace> <deployment-name>

# Find resources section and update:
# resources:
#   requests:
#     memory: "256Mi"
#     cpu: "100m"
#   limits:
#     memory: "512Mi"
#     cpu: "500m"

# Or patch directly
kubectl patch deployment -n <namespace> <deployment-name> -p \
  '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","resources":{"limits":{"memory":"1Gi"}}}]}}}}'
```

## Common Issues and Fixes

### Issue: Pod stuck in Pending

**Cause**: Insufficient resources

**Fix**:
```bash
kubectl top nodes
kubectl describe nodes
# Scale down other pods or add resources to Kind cluster
```

### Issue: CrashLoopBackOff

**Cause**: Application startup failure

**Fix**:
```bash
kubectl logs -n <namespace> <pod-name> --previous
# Fix configuration, secrets, or application code
# Redeploy
```

### Issue: ImagePullBackOff

**Cause**: Image not available

**Fix**:
```bash
# Load image into Kind
kind load docker-image <image-name> --name agent-platform

# Or fix image name in deployment
kubectl edit deployment -n <namespace> <deployment-name>
```

### Issue: Service has no endpoints

**Cause**: Pods not matching service selector

**Fix**:
```bash
# Check service selector
kubectl get svc -n <namespace> <service-name> -o yaml | grep -A5 selector

# Check pod labels
kubectl get pods -n <namespace> --show-labels

# Fix labels in deployment
kubectl edit deployment -n <namespace> <deployment-name>
```

### Issue: Pod can't connect to other services

**Cause**: Network policy or DNS issues

**Fix**:
```bash
# Test DNS
kubectl exec -n <namespace> <pod-name> -- nslookup <service-name>

# Test connectivity
kubectl exec -n <namespace> <pod-name> -- curl http://<service-name>:<port>

# Check network policies
kubectl get networkpolicy -n <namespace>
kubectl describe networkpolicy -n <namespace> <policy-name>
```

## Pro Tips

1. **Start with describe**: `kubectl describe pod` shows most common issues
2. **Check previous logs**: For crashes, `--previous` is essential
3. **Use debug pods**: Temporary pods help test networking
4. **Check events**: Recent events often reveal the issue
5. **Verify resources**: Memory/CPU limits cause many issues
6. **Test step by step**: Isolate each component
7. **Check dependencies**: Pods may fail if dependencies aren't ready
8. **Look at sidecars**: Istio proxy logs show networking issues
9. **Use exec for testing**: Run commands in pods to debug
10. **Restart if stuck**: Sometimes restart clears transient issues

## Related Skills

- **k8s:health**: Check overall platform health
- **k8s:logs**: Detailed log analysis
- **kagenti:deploy**: Full cluster redeploy if needed
