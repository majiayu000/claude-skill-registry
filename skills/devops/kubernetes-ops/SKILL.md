---
name: kubernetes-ops
description: Kubernetes deployments, troubleshooting, and operational best practices.
---

# Kubernetes Ops

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: myapp:v1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "200m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
```

## Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

## Troubleshooting

```bash
# Pod status
kubectl get pods -o wide
kubectl describe pod <name>

# Logs
kubectl logs <pod> -f
kubectl logs <pod> -c <container> --previous

# Shell access
kubectl exec -it <pod> -- /bin/sh

# Events
kubectl get events --sort-by='.lastTimestamp'

# Resource usage
kubectl top pods
kubectl top nodes
```

## Common Issues

| Symptom | Check |
|---------|-------|
| ImagePullBackOff | Image name, registry auth |
| CrashLoopBackOff | Logs, resource limits |
| Pending | Resources, node selector |
| OOMKilled | Memory limits |

## Helm

```bash
# Install
helm install myapp ./chart -f values.yaml

# Upgrade
helm upgrade myapp ./chart -f values.yaml

# Rollback
helm rollback myapp 1
```
