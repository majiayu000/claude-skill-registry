---
name: kubesearch
description: |
  Search kubesearch.dev to research how other homelabs configure Helm charts.

  Use when: (1) Configuring a new Helm release, (2) Looking for configuration examples,
  (3) Comparing approaches across repositories, (4) Needing real-world values.yaml patterns,
  (5) Researching best practices for specific charts, (6) Finding example implementations.

  Triggers: "how do others configure", "show me examples", "helm chart examples",
  "configuration examples", "values.yaml examples", "kubesearch", "homelab examples",
  "how do other homelabs", "real-world config", "chart configuration", "helm values examples",
  "compare helm configs", "best practices for helm"
---

# KubeSearch - Homelab Helm Configuration Research

Search kubesearch.dev to find real-world Helm configurations from other homelab repositories.

## Workflow

### 1. Search for the Helm Chart

Fetch the search page to find available charts:

```
WebFetch: https://kubesearch.dev/?search=<chart-name>
Prompt: List all matching helm releases with their full registry paths
```

### 2. Get Chart Page with Direct Links

Convert the registry path to URL format (replace `/` with `-`):

| Registry Path | URL Path |
|---------------|----------|
| `ghcr.io/grafana-helm-charts/grafana` | `ghcr.io-grafana-helm-charts-grafana` |
| `charts.longhorn.io/longhorn` | `charts.longhorn.io-longhorn` |

Fetch the chart page:

```
WebFetch: https://kubesearch.dev/hr/<url-path>
Prompt: List repositories with their DIRECT LINKS to HelmRelease files. Include: repo name, stars, version, and the GitHub URL to the config file.
```

The page provides direct links to each repository's HelmRelease configuration:
- `https://github.com/angelnu/k8s-gitops/blob/main/apps/longhorn-system/app/helmrelease.yaml`
- `https://github.com/blackjid/home-ops/blob/main/kubernetes/apps/.../helmrelease.yaml`

### 3. Fetch Configurations

Use the direct links from Step 2. Convert blob URLs to raw URLs for fetching:

| URL Type | Format |
|----------|--------|
| Blob (view) | `github.com/<owner>/<repo>/blob/<branch>/<path>` |
| Raw (fetch) | `raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>` |

Fetch multiple configs in parallel for comparison:

```
WebFetch: https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>/helmrelease.yaml
Prompt: Extract all helm values configuration. Show the complete values section.
```

## Parallel Repository Research

When comparing multiple implementations, fetch 3-5 repositories in parallel using WebFetch.

**Selection criteria:**
- Recent activity (updated within 6 months)
- Higher star count (indicates community trust)
- Using similar chart version to target
- Similar infrastructure goals (bare-metal, GitOps, Talos, etc.)

## Common Homelab Repositories

High-quality references frequently appearing on kubesearch:

| Repository | Focus |
|------------|-------|
| `onedr0p/home-ops` | Flux GitOps, extensive automation |
| `bjw-s/home-ops` | App-template patterns |
| `buroa/k8s-gitops` | Talos + Flux |
| `mirceanton/home-ops` | Well-documented configs |

## Output Format

When presenting findings, structure as:

```markdown
## <Chart Name> Configuration Research

### Common Patterns
- Pattern 1: ...
- Pattern 2: ...

### Repository Examples

#### <repo-1> (X stars, vY.Z)
- Key configs: ...
- Notable: ...

#### <repo-2>
...

### Recommended Configuration
Based on findings, suggested values for this homelab:
```yaml
# values.yaml
...
```
```
