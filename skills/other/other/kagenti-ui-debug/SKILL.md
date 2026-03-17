---
name: kagenti:ui-debug
description: Debug Kagenti UI issues including 502 errors, API connectivity, and nginx proxy problems
---

# Kagenti UI Debugging

Debug UI issues including API errors, nginx proxy problems, and backend connectivity.

## Quick Diagnostics

```bash
# Set kubeconfig for your cluster
export KUBECONFIG=~/clusters/hcp/<MANAGED_BY_TAG>-<suffix>/auth/kubeconfig

# Example:
# export KUBECONFIG=~/clusters/hcp/kagenti-hypershift-custom-uitst/auth/kubeconfig
```

### 1. Check Pod Status

```bash
kubectl get pods -n kagenti-system -l 'app in (kagenti-ui,kagenti-backend)'
```

### 2. Check UI Nginx Logs for 502 Errors

```bash
# Recent errors
kubectl logs -n kagenti-system deployment/kagenti-ui --tail=100 | grep -E "(502|error|upstream)"

# All logs
kubectl logs -n kagenti-system deployment/kagenti-ui --tail=200
```

### 3. Check Backend Logs

```bash
kubectl logs -n kagenti-system deployment/kagenti-backend --tail=100

# Look for API requests (should see 200s for /api/v1/*)
kubectl logs -n kagenti-system deployment/kagenti-backend --tail=100 | grep "api/v1"
```

### 4. Check Recent Events

```bash
kubectl get events -n kagenti-system --sort-by='.lastTimestamp' | tail -20
```

## Common Issues

### 502 Bad Gateway - Connection Reset

**Symptom:** Nginx logs show:
```
recv() failed (104: Connection reset by peer) while reading response header from upstream
upstream prematurely closed connection while reading response header from upstream
```

**Causes:**
1. Backend pod restarting (check events for liveness probe failures)
2. Istio ambient mTLS misconfiguration
3. High CPU on worker nodes causing timeouts

**Diagnosis:**

```bash
# Check if backend was recently restarted
kubectl get events -n kagenti-system | grep -i "backend\|liveness\|restart"

# Check node CPU
kubectl top nodes

# Check Istio namespace labels
kubectl get namespace kagenti-system -o yaml | grep -A5 labels
```

### 502 Bad Gateway - Istio mTLS Issues

**Symptom:** Intermittent 502s, some requests work, others fail.

**Diagnosis:**

```bash
# Check if namespace has ambient mode
kubectl get namespace kagenti-system -o jsonpath='{.metadata.labels.istio\.io/dataplane-mode}'

# Check PeerAuthentication policies
kubectl get peerauthentication -n kagenti-system -o yaml

# Check if waypoint is deployed (for L7 policies)
kubectl get gateway -n kagenti-system -l istio.io/waypoint-for
```

**Fix:** If mTLS is causing issues between nginx and backend:

```bash
# Option 1: Add permissive policy for backend
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: backend-permissive
  namespace: kagenti-system
spec:
  selector:
    matchLabels:
      app: kagenti-backend
  mtls:
    mode: PERMISSIVE
EOF
```

### API Returns Empty or Wrong Data

**Diagnosis:**

```bash
# Test backend API directly (port-forward)
kubectl port-forward -n kagenti-system svc/kagenti-backend 8000:8000 &
curl http://localhost:8000/api/v1/namespaces?enabled_only=true

# Check if namespaces have correct labels
kubectl get namespaces -l kagenti-enabled=true
```

### Auth Config Errors

**Symptom:** `/api/v1/auth/config` returns 502 or wrong config.

**Diagnosis:**

```bash
# Check backend env vars
kubectl get deployment kagenti-backend -n kagenti-system -o jsonpath='{.spec.template.spec.containers[0].env}' | jq

# Check if ENABLE_AUTH is set correctly
kubectl get deployment kagenti-backend -n kagenti-system -o jsonpath='{.spec.template.spec.containers[0].env}' | jq '.[] | select(.name=="ENABLE_AUTH")'

# Check Keycloak connectivity
kubectl get route keycloak -n keycloak -o jsonpath='{.spec.host}'
```

## Verify UI is Working

```bash
# Get UI route
UI_HOST=$(kubectl get route kagenti-ui -n kagenti-system -o jsonpath='{.spec.host}')

# Test static content
curl -sk "https://$UI_HOST/" | head -20

# Test API through nginx proxy
curl -sk "https://$UI_HOST/api/v1/namespaces?enabled_only=true"
curl -sk "https://$UI_HOST/api/v1/auth/config"
```

## Quick Fixes

### Restart Backend

```bash
kubectl rollout restart deployment/kagenti-backend -n kagenti-system
kubectl rollout status deployment/kagenti-backend -n kagenti-system --timeout=60s
```

### Restart UI

```bash
kubectl rollout restart deployment/kagenti-ui -n kagenti-system
kubectl rollout status deployment/kagenti-ui -n kagenti-system --timeout=60s
```

### Check Nginx Config

```bash
kubectl exec -n kagenti-system deployment/kagenti-ui -- cat /etc/nginx/nginx.conf
```

## Related Skills

- `k8s:pods` - Pod troubleshooting
- `k8s:logs` - Log analysis
- `k8s:live-debugging` - Live cluster debugging
