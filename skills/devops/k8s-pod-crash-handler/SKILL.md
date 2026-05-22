# Skill: Kubernetes Pod Crash Handler

**Purpose**: Diagnose and resolve Kubernetes pod crashes and deployment issues for Phase IV/V.

## Trigger Conditions

Invoke this skill when:
- Pod status is `CrashLoopBackOff`, `Error`, or `ImagePullBackOff`
- User mentions "pod crashing", "deployment failing", or "container restarting"
- Kubernetes deployment not reaching Ready state

## Capabilities

### 1. Diagnostic Commands

```bash
# Check pod status
kubectl get pods -n <namespace>

# Get detailed pod info
kubectl describe pod <pod-name> -n <namespace>

# Check pod logs
kubectl logs <pod-name> -n <namespace>

# Check previous container logs (if restarting)
kubectl logs <pod-name> -n <namespace> --previous

# Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

### 2. Common Crash Causes & Solutions

#### CrashLoopBackOff

| Cause | Diagnosis | Solution |
|-------|-----------|----------|
| App error on startup | Check logs for Python/Node errors | Fix application code |
| Missing env vars | Logs show "KeyError" or "undefined" | Add ConfigMap/Secret |
| DB connection fail | Logs show connection errors | Check DB service/credentials |
| Wrong command | Container exits immediately | Fix Dockerfile CMD/ENTRYPOINT |

**Fix ConfigMap for env vars**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-backend-config
data:
  CORS_ORIGINS: "https://your-frontend.vercel.app"
  DEBUG: "false"
---
apiVersion: v1
kind: Secret
metadata:
  name: todo-backend-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgresql+asyncpg://user:pass@host/db?sslmode=require"
  BETTER_AUTH_SECRET: "your-secret-key-min-32-chars"
```

**Reference in Deployment**:
```yaml
spec:
  containers:
  - name: backend
    envFrom:
    - configMapRef:
        name: todo-backend-config
    - secretRef:
        name: todo-backend-secrets
```

#### ImagePullBackOff

| Cause | Diagnosis | Solution |
|-------|-----------|----------|
| Wrong image name | Check `describe pod` output | Fix image name in deployment |
| Private registry | "unauthorized" in events | Add imagePullSecrets |
| Image doesn't exist | "not found" in events | Build and push image |

**Fix for private registry**:
```bash
# Create secret for Docker Hub
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=docker.io \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email>

# Add to deployment
spec:
  imagePullSecrets:
  - name: dockerhub-secret
```

#### OOMKilled (Out of Memory)

**Solution - Increase memory limits**:
```yaml
spec:
  containers:
  - name: backend
    resources:
      requests:
        memory: "256Mi"
        cpu: "100m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

### 3. Health Check Configuration

```yaml
spec:
  containers:
  - name: backend
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 30
      periodSeconds: 10
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 5
      failureThreshold: 3
```

### 4. Quick Recovery Scripts

**restart-deployment.sh**:
```bash
#!/bin/bash
NAMESPACE=${1:-default}
DEPLOYMENT=${2:-todo-backend}

echo "Restarting $DEPLOYMENT in $NAMESPACE..."
kubectl rollout restart deployment/$DEPLOYMENT -n $NAMESPACE
kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE
echo "Restart complete!"
```

**debug-pod.sh**:
```bash
#!/bin/bash
POD=$1
NAMESPACE=${2:-default}

echo "=== Pod Status ==="
kubectl get pod $POD -n $NAMESPACE

echo -e "\n=== Pod Description ==="
kubectl describe pod $POD -n $NAMESPACE | tail -50

echo -e "\n=== Pod Logs ==="
kubectl logs $POD -n $NAMESPACE --tail=100

echo -e "\n=== Previous Logs (if any) ==="
kubectl logs $POD -n $NAMESPACE --previous --tail=50 2>/dev/null || echo "No previous logs"
```

### 5. Pod Crash Decision Tree

```
Pod Not Running
├── CrashLoopBackOff
│   ├── Check logs → App error → Fix code
│   ├── "KeyError"/"undefined" → Missing env → Add ConfigMap/Secret
│   └── Connection error → Check service/DB
│
├── ImagePullBackOff
│   ├── "unauthorized" → Add imagePullSecrets
│   ├── "not found" → Build and push image
│   └── Wrong name → Fix image reference
│
├── OOMKilled
│   └── Increase memory limits
│
├── Pending
│   ├── "Insufficient cpu" → Reduce requests or scale cluster
│   └── "Unschedulable" → Check node resources
│
└── Error
    └── Check events with kubectl get events
```

## Checklist

- [ ] Check pod status: `kubectl get pods`
- [ ] Read pod logs: `kubectl logs <pod>`
- [ ] Check events: `kubectl get events`
- [ ] Verify environment variables in ConfigMap/Secret
- [ ] Check resource limits (memory/CPU)
- [ ] Verify image exists and is pullable
- [ ] Check health probe configuration
- [ ] Test locally with same env vars before deploying
