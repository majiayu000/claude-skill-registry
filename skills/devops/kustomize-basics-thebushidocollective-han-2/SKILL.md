---
name: kustomize-basics
description: Use when customizing Kubernetes configurations without templates using Kustomize overlays and patches.
allowed-tools: []
---

# Kustomize Basics

Kubernetes configuration customization without templates.

## Basic Structure

```
app/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── development/
    │   └── kustomization.yaml
    └── production/
        └── kustomization.yaml
```

## Base Kustomization

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml

commonLabels:
  app: myapp
  
namePrefix: myapp-

images:
  - name: myapp
    newTag: v1.0.0
```

## Overlay Kustomization

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

bases:
  - ../../base

replicas:
  - name: myapp-deployment
    count: 5

images:
  - name: myapp
    newTag: v2.0.0

patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: myapp-deployment
      spec:
        template:
          spec:
            containers:
            - name: myapp
              resources:
                limits:
                  memory: "1Gi"
                  cpu: "1000m"
```

## Common Commands

```bash
# Build kustomization
kustomize build base/

# Build overlay
kustomize build overlays/production/

# Apply with kubectl
kubectl apply -k overlays/production/

# Diff before apply
kubectl diff -k overlays/production/
```

## Transformers

### Common Labels

```yaml
commonLabels:
  app: myapp
  environment: production
```

### Name Prefix/Suffix

```yaml
namePrefix: prod-
nameSuffix: -v2
```

### Namespace

```yaml
namespace: production
```

### Config Map Generator

```yaml
configMapGenerator:
  - name: app-config
    files:
      - config.properties
    literals:
      - LOG_LEVEL=info
```

### Secret Generator

```yaml
secretGenerator:
  - name: app-secrets
    literals:
      - password=secret123
```

## Best Practices

### Use Bases for Common Configuration

Keep common configuration in base and environment-specific in overlays.

### Strategic Merge Patches

```yaml
patches:
  - path: patch-deployment.yaml
```

### JSON Patches

```yaml
patchesJson6902:
  - target:
      group: apps
      version: v1
      kind: Deployment
      name: myapp
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 3
```
