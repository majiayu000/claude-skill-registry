---
name: kubernetes-deployer
description: Package and deploy applications to Kubernetes with Dockerfiles, Helm charts, and local Minikube deployment. Use when containerizing applications, creating Kubernetes manifests, setting up Helm charts, deploying to Minikube, or preparing cloud-ready configurations. Focuses on local-first deployment with stateless services.
---

# Kubernetes Deployer

Deploy applications to Kubernetes with production-ready configurations, starting locally with Minikube.

## Deployment Workflow

```
1. Dockerfile     → Containerize application
2. Helm Chart     → Package Kubernetes manifests
3. Local Deploy   → Test in Minikube
4. Cloud Ready    → Configure for production
```

## Quick Start: Local Deployment

### 1. Create Dockerfile

```dockerfile
# Python example (see references for other languages)
FROM python:3.11-slim AS builder
WORKDIR /build
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

FROM python:3.11-slim
WORKDIR /app
RUN useradd -m -u 1000 appuser
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY app ./app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Copy Helm Chart Template

Copy `assets/helm-template/` to `charts/<app-name>/` and customize:

```bash
cp -r assets/helm-template charts/myapp
# Edit Chart.yaml: name, description
# Edit values.yaml: image, ports, resources
```

### 3. Deploy to Minikube

```bash
# Start Minikube
minikube start

# Build image in Minikube's Docker
eval $(minikube docker-env)
docker build -t myapp:local .

# Deploy with Helm
helm upgrade --install myapp ./charts/myapp \
  --set image.repository=myapp \
  --set image.tag=local \
  --set image.pullPolicy=Never

# Access service
kubectl port-forward svc/myapp 8080:80
```

## Core Principles

1. **Local-first** - Test everything in Minikube before cloud
2. **Stateless services** - No local state; use external databases
3. **Config via env vars** - All configuration through environment
4. **12-factor ready** - Portable between environments

## Helm Chart Structure

```
charts/<app-name>/
├── Chart.yaml        # Metadata
├── values.yaml       # Default config
└── templates/
    ├── _helpers.tpl  # Template functions
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml  # Optional
    └── hpa.yaml      # Optional
```

## Configuration Patterns

### Environment Variables

```yaml
# values.yaml
env:
  - name: DATABASE_URL
    value: "postgresql://..."
  - name: LOG_LEVEL
    value: "info"

# From secrets
envFrom:
  - secretRef:
      name: app-secrets
```

### Create Secret

```bash
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_PASSWORD=secret123 \
  --from-literal=API_KEY=key456
```

### Health Checks

```yaml
# values.yaml
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 5
```

## Common Commands

### Minikube

```bash
minikube start                    # Start cluster
minikube dashboard                # Open dashboard
eval $(minikube docker-env)       # Use Minikube Docker
minikube service myapp --url      # Get service URL
```

### Helm

```bash
helm lint ./charts/myapp                    # Validate chart
helm template myapp ./charts/myapp          # Preview manifests
helm upgrade --install myapp ./charts/myapp # Deploy
helm uninstall myapp                        # Remove
```

### Kubectl

```bash
kubectl get pods                  # List pods
kubectl logs <pod>                # View logs
kubectl describe pod <pod>        # Debug pod
kubectl port-forward svc/myapp 8080:80  # Access locally
```

## Environment-Specific Values

```yaml
# values-dev.yaml
replicaCount: 1
resources:
  limits:
    cpu: 200m
    memory: 256Mi

# values-prod.yaml
replicaCount: 3
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
```

Deploy with environment:
```bash
helm upgrade --install myapp ./charts/myapp \
  -f values.yaml \
  -f values-prod.yaml
```

## Troubleshooting

| Issue | Command |
|-------|---------|
| Pod not starting | `kubectl describe pod <name>` |
| Image not found | `minikube ssh docker images` |
| Service unreachable | `kubectl get endpoints` |
| Logs | `kubectl logs <pod> -f` |

## References

- [references/dockerfile-patterns.md](references/dockerfile-patterns.md) - Multi-stage builds, language templates, security
- [references/helm-charts.md](references/helm-charts.md) - Chart structure, templates, values configuration
- [references/minikube-local.md](references/minikube-local.md) - Local images, service access, debugging

## Assets

- [assets/helm-template/](assets/helm-template/) - Ready-to-use Helm chart template