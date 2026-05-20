---
name: Kubernetes & Container Orchestration
description: "Kubernetes deployment and management. Activate when: (1) Creating or modifying K8s manifests, (2) Working with Helm charts, (3) Configuring ArgoCD GitOps, (4) Managing cluster resources, or (5) Troubleshooting pod/service issues."
---

# Kubernetes & Container Orchestration

## Overview

Kubernetes (K8s) is a container orchestration platform for deploying, scaling, and managing containerized applications.

## Core Resources

| Resource | Purpose | Short Name |
|----------|---------|------------|
| Pod | Smallest deployable unit | po |
| Deployment | Manages ReplicaSets | deploy |
| Service | Network endpoint | svc |
| ConfigMap | Configuration data | cm |
| Secret | Sensitive data | secret |
| Ingress | External access | ing |
| PersistentVolumeClaim | Storage request | pvc |
| Namespace | Resource isolation | ns |

## Quick Reference

### kubectl Commands

```bash
# Context & Cluster
kubectl config get-contexts
kubectl config use-context <name>
kubectl cluster-info

# Resources
kubectl get pods -A                    # All namespaces
kubectl get deploy,svc,ing -n <ns>     # Multiple resources
kubectl describe pod <name>            # Detailed info
kubectl logs <pod> -f --tail=100       # Stream logs
kubectl exec -it <pod> -- /bin/sh      # Shell into pod

# Apply/Delete
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
kubectl apply -k ./kustomize/          # Kustomize

# Debug
kubectl get events --sort-by=.lastTimestamp
kubectl top pods                       # Resource usage
kubectl port-forward svc/<name> 8080:80
```

## Manifest Templates

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
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
        - name: myapp
          image: myapp:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
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

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP  # or LoadBalancer, NodePort
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - myapp.example.com
      secretName: myapp-tls
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

## Helm

### Chart Structure

```
mychart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── charts/          # Dependencies
```

### Helm Commands

```bash
# Repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo postgres

# Install/Upgrade
helm install myrelease mychart/ -f values.yaml -n namespace
helm upgrade myrelease mychart/ -f values.yaml
helm upgrade --install myrelease mychart/  # Install or upgrade

# Debug
helm template mychart/ -f values.yaml      # Render locally
helm install --dry-run --debug myrelease mychart/
helm lint mychart/

# Management
helm list -A                               # All releases
helm history myrelease                     # Release history
helm rollback myrelease 1                  # Rollback to revision
helm uninstall myrelease
```

## ArgoCD GitOps

### Application Manifest

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: HEAD
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### ArgoCD CLI

```bash
# Login
argocd login argocd.example.com

# Applications
argocd app list
argocd app get myapp
argocd app sync myapp
argocd app diff myapp

# Rollback
argocd app history myapp
argocd app rollback myapp <revision>
```

## Kustomize

### Structure

```
base/
├── kustomization.yaml
├── deployment.yaml
└── service.yaml

overlays/
├── development/
│   ├── kustomization.yaml
│   └── replica-patch.yaml
└── production/
    ├── kustomization.yaml
    └── replica-patch.yaml
```

### kustomization.yaml

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml

# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
patchesStrategicMerge:
  - replica-patch.yaml
namespace: production
namePrefix: prod-
```

## Troubleshooting

### Pod Issues

```bash
# Pod not starting
kubectl describe pod <name>
kubectl logs <pod> --previous  # Previous container logs

# Common issues:
# - ImagePullBackOff: Check image name/registry access
# - CrashLoopBackOff: Check logs, liveness probe
# - Pending: Check resources, node selector, PVC
```

### Service Issues

```bash
# Service not reachable
kubectl get endpoints <svc>    # Check endpoints exist
kubectl get pods -l app=<label> # Check pod labels match
kubectl port-forward svc/<name> 8080:80  # Test directly
```

## External Links

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Kustomize Documentation](https://kustomize.io/)
