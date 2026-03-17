---
name: k8s
description: |
  Kubernetes operational knowledge for accessing clusters, running kubectl, understanding Flux status,
  and navigating the homelab Kubernetes environment.

  Use when: (1) Accessing a cluster or checking connectivity, (2) Running kubectl commands or checking resource status,
  (3) Checking Flux reconciliation status or triggering reconciliation, (4) Finding internal service URLs,
  (5) Understanding cluster layout or resource types, (6) Researching unfamiliar Helm charts or services.

  Triggers: "kubectl", "kubeconfig", "flux get", "flux reconcile", "flux status", "cluster access",
  "internal URL", "service URL", "prometheus URL", "grafana URL", "helm release status",
  "check flux", "which cluster", "how to access", "port-forward"
user-invocable: false
---

# ACCESSING CLUSTERS

**CRITICAL:** Always prefix kubectl/flux commands with inline KUBECONFIG assignment. Do NOT use `export` or `&&` - the variable must be set in the same command:

```bash
# CORRECT - inline assignment
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get pods

# WRONG - export with && breaks in some shell contexts
export KUBECONFIG=~/.kube/<cluster>.yaml && kubectl get pods
```

## Cluster Context

**CRITICAL:** Always confirm cluster before running commands.

| Cluster | Purpose | Kubeconfig |
|---------|---------|------------|
| `dev` | Manual testing | `~/.kube/dev.yaml` |
| `integration` | Automated testing | `~/.kube/integration.yaml` |
| `live` | Production | `~/.kube/live.yaml` |

```bash
KUBECONFIG=~/.kube/<cluster>.yaml kubectl <command>
```

## Accessing Internal Services

Platform services are exposed through the internal ingress gateway over HTTPS. DNS URLs are useful for **browser-based access** (Grafana, Hubble UI, Longhorn UI).

**OAuth2 Proxy caveat:** Prometheus, Alertmanager, and some other services are behind OAuth2 Proxy. DNS URLs redirect to an OAuth login page and **cannot be used for API queries via curl**. Use `kubectl exec` or port-forward instead for programmatic access.

| Service | Live | Auth | API Access |
|---------|------|------|------------|
| Prometheus | `https://prometheus.internal.tomnowak.work` | OAuth2 Proxy | `kubectl exec` or port-forward |
| Alertmanager | `https://alertmanager.internal.tomnowak.work` | OAuth2 Proxy | `kubectl exec` or port-forward |
| Grafana | `https://grafana.internal.tomnowak.work` | Built-in auth | Browser only |
| Hubble UI | `https://hubble.internal.tomnowak.work` | None | Browser |
| Longhorn UI | `https://longhorn.internal.tomnowak.work` | None | Browser |
| Garage Admin | `https://garage.internal.tomnowak.work` | None | Browser |

**Domain pattern:** `<service>.internal.<cluster-suffix>.tomnowak.work`
- live: `internal.tomnowak.work`
- integration: `internal.integration.tomnowak.work`
- dev: `internal.dev.tomnowak.work`

### Querying Prometheus/Alertmanager API

```bash
# Option 1: kubectl exec (quick, no setup)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/query?query=up' | jq '.data.result'

KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/alerts' | jq '.data.alerts[] | select(.state == "firing")'

KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring alertmanager-kube-prometheus-stack-0 -c alertmanager -- \
  wget -qO- 'http://localhost:9093/api/v2/alerts' | jq .

# Option 2: Port-forward (for scripts and repeated queries)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090 &
curl -s "http://localhost:9090/api/v1/query?query=up" | jq '.data.result'
```

**Using the helper scripts:**

```bash
# Prometheus (start port-forward first; script defaults to http://localhost:9090)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090 &
.claude/skills/prometheus/scripts/promql.sh alerts --firing

# Loki (no HTTPRoute — always requires port-forward)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/loki-headless 3100:3100 &
export LOKI_URL=http://localhost:3100
.claude/skills/loki/scripts/logql.sh tail '{namespace="monitoring"}' --since 15m
```

# Common kubectl Patterns

Read-only commands used during daily operations and investigations:

| Command | Purpose |
|---------|---------|
| `kubectl get pods -n <ns>` | List pods in a namespace |
| `kubectl get pods -A` | List pods across all namespaces |
| `kubectl describe pod <pod> -n <ns>` | Detailed pod info with events |
| `kubectl logs <pod> -n <ns> --tail=100` | Recent logs from a pod |
| `kubectl logs <pod> -n <ns> --previous` | Logs from previous container instance |
| `kubectl get events -n <ns> --sort-by='.lastTimestamp'` | Recent events timeline |
| `kubectl top pods -n <ns>` | CPU/memory usage per pod |
| `kubectl top nodes` | CPU/memory usage per node |
| `kubectl get ns <ns> --show-labels` | Namespace labels (network policy profiles) |
| `kubectl explain <resource>` | API schema reference for a resource type |

# Flux GitOps Commands

## Status and Reconciliation

```bash
# Check status
KUBECONFIG=~/.kube/<cluster>.yaml flux get all
KUBECONFIG=~/.kube/<cluster>.yaml flux get kustomizations
KUBECONFIG=~/.kube/<cluster>.yaml flux get helmreleases -A

# Trigger reconciliation
KUBECONFIG=~/.kube/<cluster>.yaml flux reconcile source git flux-system
KUBECONFIG=~/.kube/<cluster>.yaml flux reconcile kustomization <name>
KUBECONFIG=~/.kube/<cluster>.yaml flux reconcile helmrelease <name> -n <namespace>
```

## Flux Status Interpretation

| Status | Meaning | Action |
|--------|---------|--------|
| `Ready: True` | Resource is reconciled and healthy | None - operating normally |
| `Ready: False` | Resource failed to reconcile | Check the message/reason for details |
| `Stalled: True` | Resource has stopped retrying after repeated failures | Suspend/resume to reset (see `sre` skill) |
| `Suspended: True` | Resource is intentionally paused | Resume when ready: `flux resume <type> <name>` |
| `Reconciling` | Resource is actively being applied | Wait for completion |

# Researching Unfamiliar Services

When investigating unknown services, spawn a haiku agent to research documentation:

```
Task tool:
- subagent_type: "general-purpose"
- model: "haiku"
- prompt: "Research [service] troubleshooting docs. Focus on:
  1. Common failure modes
  2. Health indicators
  3. Configuration gotchas
  Start with: [docs-url]"
```

**Chart URL to Docs mapping:**
| Chart Source | Documentation |
|--------------|---------------|
| `charts.jetstack.io` | cert-manager.io/docs |
| `charts.longhorn.io` | longhorn.io/docs |
| `grafana.github.io` | grafana.com/docs |
| `prometheus-community.github.io` | prometheus.io/docs |

# Common Confusions

BAD: Use `helm list` to check Helm release status
GOOD: Use `kubectl get helmrelease -A` - Flux manages releases via CRDs, not Helm CLI

## Keywords

kubernetes, kubectl, kubeconfig, flux, flux status, cluster access, internal URL, service URL, port-forward, helm release, gitops, reconciliation
