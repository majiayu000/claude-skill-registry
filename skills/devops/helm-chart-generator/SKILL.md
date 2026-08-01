---
name: helm-chart-generator
description: 'Generate production-ready Helm charts for Kubernetes apps. Use when:
  (1) Deploying applications to Kubernetes, (2) Containerizing apps for Minikube/K8s,
  (3) Creating reusable deployment packages, (4)'
---

---
name: Helm Chart Generator
description: Generate production-ready Helm charts for Kubernetes apps. Use when: (1) Deploying applications to Kubernetes, (2) Containerizing apps for Minikube/K8s, (3) Creating reusable deployment packages, (4) Needing parameterized K8s manifests, (5) Scaffolding new chart structures. Includes security contexts, resource limits, RBAC, NetworkPolicies, and multi-environment support (dev/prod). Provides templates for frontend, backend, and MCP server components.
---

## Overview

This skill generates properly structured Helm charts following best practices. It creates charts with security contexts, resource limits, and multi-environment support.

## Quick Start

Use the generation script to scaffold a new chart:

```bash
# Generate a chart for a specific component type
python scripts/generate_chart.py --name <app-name> --type <frontend|backend|mcp> --namespace <namespace>

# Example: Generate a frontend chart
python scripts/generate_chart.py --name todo-frontend --type frontend --namespace todo-app
```

Or copy from base templates in `assets/` and customize.

## Chart Structure

```
charts/todo-app/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── serviceaccount.yaml
│   ├── role.yaml
│   ├── rolebinding.yaml
│   ├── networkpolicy.yaml
│   └── pdb.yaml
└── charts/           # Subcharts
```

## Chart.yaml Template

```yaml
apiVersion: v2
name: <chart-name>
description: <description>
type: application
version: 0.1.0
appVersion: "1.0.0"
```

## Values.yaml Structure

Every component MUST have:

```yaml
<component>:
  enabled: true
  replicaCount: 2

  image:
    repository: <name>
    tag: "1.0.0"          # Never "latest"
    pullPolicy: IfNotPresent

  service:
    type: ClusterIP
    port: <port>

  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 256Mi

  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    allowPrivilegeEscalation: false
```

## Security Templates

Always include these templates:

1. **serviceaccount.yaml** - Dedicated SA per app
2. **role.yaml** - Namespace-scoped, minimal permissions
3. **rolebinding.yaml** - Bind role to SA
4. **networkpolicy.yaml** - Default deny + explicit allows

## Environment-Specific Values

**values-dev.yaml (Minikube):**
```yaml
frontend:
  replicaCount: 1
  image:
    pullPolicy: Never    # Local images
```

**values-prod.yaml:**
```yaml
frontend:
  replicaCount: 3
  image:
    pullPolicy: Always
  autoscaling:
    enabled: true
```

## Validation Commands

Always run before deployment:

```bash
helm lint ./charts/todo-app
helm template ./charts/todo-app -f values-dev.yaml
helm install todo-app ./charts/todo-app --dry-run --debug
```

## Minikube Local Images

```bash
eval $(minikube docker-env)
docker build -t todo-frontend:1.0.0 ./frontend
# Set imagePullPolicy: Never in values
```

## Helm Commands

```bash
# Install
helm install todo-app ./charts/todo-app -f values-dev.yaml -n todo

# Upgrade
helm upgrade todo-app ./charts/todo-app -f values-dev.yaml -n todo

# Rollback
helm rollback todo-app 1 -n todo
```

## Checklist

```
[ ] Chart.yaml has apiVersion: v2
[ ] values.yaml complete
[ ] _helpers.tpl has name/label functions
[ ] SecurityContext in deployments
[ ] ServiceAccount created
[ ] NetworkPolicy enabled
[ ] All containers have resource limits
[ ] helm lint passes
[ ] helm template renders
```
