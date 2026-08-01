---
name: kaizen-infrastructure
description: '- Creating or modifying Kubernetes manifests'
---

---
name: kaizen-infrastructure
description: Kaizen infrastructure management. Use when working on Kubernetes manifests, Talos configuration, Flux GitOps, or cluster operations. Triggers on: k8s, kubernetes, flux, talos, cluster, node, deployment, helm, kustomize.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Kaizen Infrastructure Skill

## When to Use
- Creating or modifying Kubernetes manifests
- Configuring Talos Linux nodes
- Setting up Flux GitOps resources
- Deploying applications to the cluster
- Troubleshooting cluster issues

## Key Directories
- `k8s/` — All Kubernetes manifests
- `talos/` — Talos Linux configuration
- `specs/architecture.md` — System design decisions
- `specs/hardware-inventory.md` — Available hardware

## Conventions

### Manifest Structure
Follow the Flux monorepo pattern:
```
k8s/
├── clusters/<cluster>/     # Bootstrap per cluster
├── infrastructure/base/    # Shared infrastructure
├── infrastructure/overlays/<env>/
├── apps/base/              # Application definitions
└── apps/overlays/<env>/
```

### Naming
- Namespaces: lowercase, hyphenated (`inference`, `mcp-gateway`)
- Resources: `<app>-<component>` (e.g., `sglang-server`, `qdrant-cluster`)
- ConfigMaps: `<app>-config`
- Secrets: `<app>-secret`

### Labels (Required)
```yaml
metadata:
  labels:
    app.kubernetes.io/name: <app>
    app.kubernetes.io/component: <component>
    app.kubernetes.io/part-of: kaizen
```

### GPU Workloads
```yaml
nodeSelector:
  nvidia.com/gpu.present: "true"
resources:
  limits:
    nvidia.com/gpu: 1
```

## Flux Patterns

### HelmRelease
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: <app>
  namespace: <namespace>
spec:
  interval: 5m
  chart:
    spec:
      chart: <chart>
      version: "<version>"
      sourceRef:
        kind: HelmRepository
        name: <repo>
  values:
    # Inline values or reference valuesFrom
```

### Kustomization
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: <name>
  namespace: flux-system
spec:
  interval: 10m
  path: ./k8s/apps/<path>
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
```

## Talos Patterns

### Machine Config Patches
Store per-node patches in `talos/patches/`:
```yaml
# talos/patches/interface.yaml
machine:
  install:
    disk: /dev/nvme0n1
  network:
    hostname: interface
```

### Apply Configuration
```bash
talosctl apply-config -n <node-ip> -f controlplane.yaml --config-patch @patches/interface.yaml
```

## Common Tasks

### Add a new application
1. Create base in `k8s/apps/base/<app>/`
2. Add kustomization.yaml
3. Create overlay in `k8s/apps/overlays/<env>/<app>/`
4. Add to cluster kustomization

### Check cluster health
```bash
kubectl get nodes
kubectl get pods -A | grep -v Running
flux get all
```

### Force Flux sync
```bash
flux reconcile source git flux-system
flux reconcile kustomization flux-system
```

## Validation

Before committing:
1. `yamllint` on all YAML files
2. `kubectl diff` if cluster is available
3. Verify Flux can parse: `flux diff kustomization`

## Reference Docs
- Read `k8s/README.md` for detailed conventions
- Check `specs/architecture.md` for design decisions
