---
name: k8s-operations
description: Kubernetes operations, deployment patterns, and cloud-native best practices. Auto-triggers when working with containers, K8s manifests, or cloud infrastructure.
---

# Kubernetes Operations Skill

## Core Resources

### Workload Resources

```yaml
# Deployment - Stateless applications
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:v1
        resources:
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 3
```

```yaml
# StatefulSet - Stateful applications
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: "db"
  replicas: 3
  selector:
    matchLabels:
      app: db
  template:
    spec:
      containers:
      - name: db
        image: postgres:15
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### Service Types

| Type | Use Case | Access |
|------|----------|--------|
| ClusterIP | Internal services | Within cluster only |
| NodePort | Development/testing | Node IP + port |
| LoadBalancer | Production external | Cloud LB IP |
| ExternalName | External DNS alias | DNS CNAME |

### Ingress Pattern
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app
            port:
              number: 80
```

## Deployment Strategies

### Rolling Update (Default)
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
```

### Blue-Green
1. Deploy new version alongside old
2. Switch service selector to new version
3. Verify, then delete old version

### Canary
```yaml
# Main deployment (90%)
replicas: 9
labels:
  version: stable

# Canary deployment (10%)
replicas: 1
labels:
  version: canary
```

## Resource Management

### Requests vs Limits
- **Requests**: Guaranteed resources, used for scheduling
- **Limits**: Maximum allowed, pod killed if exceeded (memory)

### Resource Quotas
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
```

### Pod Disruption Budgets
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

## ConfigMaps & Secrets

```yaml
# ConfigMap for non-sensitive config
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "db.default.svc.cluster.local"
  LOG_LEVEL: "info"

---
# Secret for sensitive data (base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DATABASE_PASSWORD: cGFzc3dvcmQ=  # base64 encoded
```

## Essential Commands

```bash
# Debugging
kubectl get pods -o wide
kubectl describe pod <name>
kubectl logs <pod> -f --tail=100
kubectl exec -it <pod> -- /bin/sh

# Resource management
kubectl top pods
kubectl top nodes

# Rollout management
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>

# Context switching
kubectl config get-contexts
kubectl config use-context <name>
```

## Security Best Practices

1. **Never run as root**: `securityContext.runAsNonRoot: true`
2. **Read-only filesystem**: `securityContext.readOnlyRootFilesystem: true`
3. **Drop capabilities**: `securityContext.capabilities.drop: ["ALL"]`
4. **Network policies**: Default deny, explicit allow
5. **Pod Security Standards**: Use restricted profile in production
