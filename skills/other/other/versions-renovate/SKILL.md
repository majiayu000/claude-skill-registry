---
name: versions-renovate
description: |
  Managing platform versions and Renovate annotations in the homelab.

  Use when: (1) Adding a new version entry to versions.env, (2) Configuring Renovate to track a new dependency,
  (3) Debugging why Renovate ignores or mis-detects a version, (4) Understanding annotation syntax for versions.env,
  (5) Adding container image tracking to YAML files, (6) Configuring package rules or grouping in Renovate.

  Triggers: "versions.env", "renovate annotation", "renovate not updating", "add version",
  "renovate ignore", "datasource", "extractVersion", "package rule", "automerge",
  "renovate validate", "dependency tracking", "version management"
user-invocable: false
---

# Versions and Renovate Management

This skill covers adding and maintaining version entries in `kubernetes/platform/versions.env` and configuring Renovate to automatically update them.

## How Version Updates Flow

```
Renovate detects new version --> Updates versions.env in a PR
  --> PR merges --> OCI artifact built --> integration cluster deploys
  --> Flux substitutes ${var} into HelmRelease specs
  --> Tuppr reads Talos/K8s versions for rolling upgrades
```

Every entry in `versions.env` needs a `# renovate:` annotation on the line above it. Renovate's custom regex manager in `.github/renovate.json5` parses these annotations to determine how to check for updates.

---

## Annotation Syntax

```env
# renovate: datasource=<source> depName=<name> [packageName=<pkg>] [extractVersion=<regex>] [registryUrl=<url>] [versioning=<scheme>]
variable_name=<value>
```

**Key ordering is fixed**: `datasource`, `depName`, `packageName`, `extractVersion`, `registryUrl`, `versioning`. Rearranging keys causes Renovate to silently skip the entry.

| Field | Required | Purpose |
|-------|----------|---------|
| `datasource` | Yes | Where Renovate looks for versions (`helm`, `docker`, `github-releases`, `github-tags`) |
| `depName` | Yes | Human-readable name shown in Renovate PRs |
| `packageName` | No | Registry-specific lookup path (OCI registries, GitHub repos) |
| `extractVersion` | No | Regex to transform upstream version (e.g., strip `v` prefix) |
| `registryUrl` | No | HTTP Helm repository URL (not for OCI) |
| `versioning` | No | Version scheme override for non-semver (e.g., `loose`) |

---

## Adding a New Version Entry

### Step 1: Select Datasource

```
What kind of dependency?
|
+-- Helm chart from HTTP registry    --> datasource=helm + registryUrl=<url>
+-- Helm chart from OCI registry     --> datasource=docker + packageName=<full-path>
+-- GitHub release (Talos, Flux)      --> datasource=github-releases + packageName=<org/repo>
+-- GitHub tag (no release object)    --> datasource=github-tags + packageName=<org/repo>
```

### Step 2: Write the Annotation

**HTTP Helm registry** -- use `registryUrl`, `depName` is the chart name:

```env
# renovate: datasource=helm depName=grafana registryUrl=https://grafana.github.io/helm-charts
grafana_version=10.5.15
```

**OCI Helm registry** -- use `packageName` with the full image path (no `oci://` prefix):

```env
# renovate: datasource=docker depName=app-template packageName=ghcr.io/bjw-s-labs/helm/app-template
app_template_version=4.6.2
```

**GitHub releases** -- use `packageName` as `org/repo`:

```env
# renovate: datasource=github-releases depName=talos packageName=siderolabs/talos
talos_version=v1.12.2
```

**GitHub tags** -- same pattern, different datasource:

```env
# renovate: datasource=github-tags depName=kubernetes packageName=kubernetes/kubernetes extractVersion=^v(?<version>.*)$
kubernetes_version=1.35.0
```

### Step 3: Handle Version Prefix

If the upstream releases as `v1.0.0` but your stored value omits the `v`, add `extractVersion`:

```env
# renovate: datasource=helm depName=cert-manager extractVersion=^v(?<version>.*)$ registryUrl=https://charts.jetstack.io
cert_manager_version=1.19.3
```

Real examples from the codebase:
- Talos: stores `v1.12.2` (keeps `v`) -- no extractVersion needed
- Cilium: stores `1.18.6` (strips `v`) -- extractVersion required
- Cert-manager: stores `1.19.3` (strips `v`) -- extractVersion required

### Step 4: Handle Non-Semver Versions

For versions that don't follow semver, add `versioning=loose`:

```env
# renovate: datasource=docker depName=cloudnative-vectorchord packageName=ghcr.io/tensorchord/cloudnative-vectorchord versioning=loose
vectorchord_version=18.1-1.0.0
```

### Step 5: Add Package Rule (if needed)

If the dependency should be grouped or has special automerge needs, add to `.github/renovate.json5`:

```json5
{
  "matchDepNames": ["my-chart", "related-chart"],
  "groupName": "my stack"
}
```

### Step 6: Validate

```bash
task renovate:validate
```

---

## YAML Container Image Annotations

For container image tags hardcoded in Helm values files (not in versions.env), annotate directly in the YAML. The custom regex manager matches these patterns.

**Tag field pattern:**

```yaml
image:
  repository: ghcr.io/kashalls/kromgo
  # renovate: datasource=docker depName=ghcr.io/kashalls/kromgo
  tag: v0.7.5
```

**Inline image:tag pattern:**

```yaml
initContainers:
  # renovate: datasource=docker depName=ghcr.io/home-operations/postgres-init
  image: ghcr.io/home-operations/postgres-init:18
```

**When to use which:**
- **versions.env**: Helm chart versions (Flux-substituted into HelmRelease specs)
- **YAML annotations**: Container image tags in values files (sidecars, init containers)

---

## Package Rules

Package rules in `.github/renovate.json5` control grouping and automerge. By default, minor/patch updates automerge after 3 days (`.renovate/automerge.json5`).

### Existing Groups

| Group | Dependencies | Automerge |
|-------|-------------|-----------|
| infrastructure versions | talos, kubernetes, cilium, gateway-api, flux | Never |
| grafana stack | grafana, loki, alloy | Default |
| prometheus stack | kube-prometheus-stack, prometheus-operator-crds | Default |
| istio mesh | base, cert-manager-istio-csr | Default |
| mittwald utilities | kubernetes-replicator, kubernetes-secret-generator | Default |
| authelia stack | authelia, lldap | Default |
| hardware monitoring exporters | prometheus-snmp-exporter, prometheus-ipmi-exporter, prometheus-smartctl-exporter | Default |

**When to add a rule:**
- Multiple related charts that should update together (grouping)
- Infrastructure-critical dependencies that must not automerge
- The `matchDepNames` values must match the `depName` in the annotation

---

## Debugging

### Dependency Not Being Updated

1. **Check key order**: Must be `datasource depName [packageName] [extractVersion] [registryUrl] [versioning]`
2. **Run `task renovate:validate`**: Catches config syntax errors
3. **Check dependency dashboard**: Look for the dep in the Renovate dashboard issue on GitHub
4. **Verify datasource**: Ensure registry URL or package name is correct and accessible
5. **Check ignorePaths**: Confirm the file isn't excluded in `renovate.json5`

### Wrong Version Detected

- **extractVersion mismatch**: Regex doesn't match upstream tag format
- **Wrong datasource**: `helm` vs `docker` vs `github-releases` produce different version lists
- **Non-semver**: Missing `versioning=loose` causes Renovate to skip

### Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Wrong key order | Silently ignored | Follow exact order above |
| `oci://` prefix in packageName | Can't find package | Remove `oci://` prefix |
| Missing `extractVersion` | Version has unwanted `v` | Add `extractVersion=^v(?<version>.*)$` |
| `datasource=helm` for OCI | Can't find chart | Use `datasource=docker` |
| Missing `versioning=loose` | Skips non-semver versions | Add `versioning=loose` |
| Annotation not on line above | Regex doesn't match | Must be immediately above `key=value` |
