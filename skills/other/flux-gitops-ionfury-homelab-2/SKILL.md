---
name: flux-gitops
description: |
  Flux GitOps patterns for the homelab Kubernetes platform using ResourceSets.

  Use when: (1) Adding new Helm releases or applications to the platform, (2) Deploying a new service to Kubernetes,
  (3) Debugging Flux reconciliation issues or sync problems, (4) Understanding ResourceSet patterns,
  (5) Configuring Kustomizations and variable substitution, (6) Questions about helm-charts.yaml or platform structure,
  (7) GitOps workflow questions.

  Triggers: "add helm release", "deploy to kubernetes", "add new service", "add application",
  "flux resourceset", "flux reconciliation", "flux not syncing", "flux stuck", "gitops",
  "helm-charts.yaml", "platform values", "flux debug", "HelmRelease not ready", "kustomization",
  "helmrelease", "add chart", "deploy helm chart"
---

# Flux GitOps Platform

The homelab Kubernetes platform uses Flux ResourceSets for centralized, declarative management of Helm releases and configurations.

For ResourceSet patterns, version management, and platform architecture, see [kubernetes/platform/CLAUDE.md](../../kubernetes/platform/CLAUDE.md).

## How to Add a New Helm Release

### Step 1: Add to helm-charts.yaml

Add an entry to the `inputs` array:

```yaml
inputs:
  - name: "my-new-chart"           # Unique release name (kebab-case)
    namespace: "my-namespace"       # Target namespace
    chart:
      name: "actual-chart-name"    # Chart name in repository
      version: "1.0.0"             # Pinned version
      url: "https://example.com/charts"  # Helm repository URL
    dependsOn: [cilium]            # Array of release names this depends on
```

For OCI registries:
```yaml
    chart:
      name: "app-template"
      version: "3.6.1"
      url: "oci://ghcr.io/bjw-s/helm"  # Prefix with oci://
```

### Step 2: Create Values File

Create `charts/<release-name>.yaml` with Helm values:

```yaml
# yaml-language-server: $schema=<chart-schema-url>
---
# Helm values for the chart
replicas: 1
image:
  repository: myapp
  tag: v1.0.0
```

### Step 3: Add to kustomization.yaml

Add the values file to the `configMapGenerator`:

```yaml
configMapGenerator:
  - name: platform-values
    files:
      # ... existing entries
      - charts/my-new-chart.yaml
```

### Step 4: Add Config Resources (Optional)

If the chart needs additional resources (secrets, configs), add to `config/`:

```
config/my-new-chart/
├── kustomization.yaml
├── secret.yaml
└── config.yaml
```

Then reference in `config.yaml` ResourceSet.

## ResourceSet Template Syntax

The `resourcesTemplate` uses Go text/template with `<<` `>>` delimiters:

```yaml
resourcesTemplate: |
  apiVersion: helm.toolkit.fluxcd.io/v2
  kind: HelmRelease
  metadata:
    name: << inputs.name >>
    namespace: << inputs.provider.namespace >>
  spec:
    <<- if inputs.dependsOn >>
    dependsOn:
    <<- range $dep := inputs.dependsOn >>
      - name: << $dep >>
    <<- end >>
    <<- end >>
    chart:
      spec:
        chart: << inputs.chart.name >>
        version: << inputs.chart.version >>
```

### Template Functions

- `<< inputs.field >>` - Access input field
- `<<- if condition >>` - Conditional (with `-` to trim whitespace)
- `<<- range $item := inputs.array >>` - Loop over array
- `hasPrefix "oci://" inputs.chart.url` - String prefix check

## Dependency Management

### Release Dependencies

```yaml
inputs:
  - name: "grafana"
    dependsOn: [kube-prometheus-stack, alloy]  # Waits for these
```

### ResourceSet Dependencies

```yaml
spec:
  dependsOn:
    - apiVersion: fluxcd.controlplane.io/v1
      kind: ResourceSet
      name: platform-namespaces  # Waits for namespaces ResourceSet
```

## Debugging Flux

### Check ResourceSet Status

```bash
kubectl get resourcesets -n flux-system
kubectl describe resourceset platform-resources -n flux-system
```

### Check HelmRelease Status

```bash
kubectl get helmreleases -A
kubectl describe helmrelease <name> -n <namespace>
```

### Check Reconciliation Logs

```bash
kubectl logs -n flux-system deploy/flux-controller -f | grep <release-name>
```

### Force Reconciliation

```bash
flux reconcile helmrelease <name> -n <namespace>
flux reconcile kustomization flux-system -n flux-system
```

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| `waiting for dependencies` | Dependency not ready | Check `dependsOn` releases |
| `values key not found` | Missing values file | Add to kustomization.yaml configMapGenerator |
| `chart not found` | Wrong chart name/URL | Verify chart exists in repository |
| `namespace not found` | Namespace not created | Add to namespaces.yaml |

## OCI Registry Specifics

When using OCI registries like GHCR:

```yaml
chart:
  name: "app-template"           # Just the chart name
  version: "3.6.1"
  url: "oci://ghcr.io/bjw-s/helm"  # Registry URL with oci:// prefix
```

The ResourceSet template automatically detects OCI URLs and sets `type: oci` on the HelmRepository.
