---
name: k8s-sre
description: |
  Kubernetes SRE debugging and incident investigation for pod failures, crashes, and service issues.

  Use when: (1) Pods not starting, stuck, or failing (CrashLoopBackOff, ImagePullBackOff, OOMKilled, Pending),
  (2) Debugging Kubernetes errors or investigating "why is my pod...", (3) Service degradation or unavailability,
  (4) Reading pod logs or events, (5) Troubleshooting deployments, statefulsets, or daemonsets,
  (6) Root cause analysis for any Kubernetes incident.

  Triggers: "pod not starting", "pod stuck", "CrashLoopBackOff", "ImagePullBackOff", "OOMKilled",
  "Pending pod", "why is my pod", "kubernetes error", "k8s error", "service not available",
  "can't reach service", "pod logs", "debug kubernetes", "troubleshoot k8s", "what's wrong with my pod",
  "deployment not working", "helm install failed", "flux not reconciling"
---

# ACCESSING CLUSTERS

**CRITICAL:** Always prefix kubectl/flux commands with inline KUBECONFIG assignment. Do NOT use `export` or `&&` - the variable must be set in the same command:

```bash
# CORRECT - inline assignment
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get pods

# WRONG - export with && breaks in some shell contexts
export KUBECONFIG=~/.kube/<cluster>.yaml && kubectl get pods
```

## Accessing Internal Services via DNS (Preferred)

Platform services are exposed through the internal ingress gateway over HTTPS. **Always use DNS-based access instead of port-forwarding** when querying Prometheus, Grafana, Alertmanager, and other internal services.

| Service | Live | Integration | Dev |
|---------|------|-------------|-----|
| Prometheus | `https://prometheus.internal.tomnowak.work` | `https://prometheus.internal.integration.tomnowak.work` | `https://prometheus.internal.dev.tomnowak.work` |
| Grafana | `https://grafana.internal.tomnowak.work` | `https://grafana.internal.integration.tomnowak.work` | `https://grafana.internal.dev.tomnowak.work` |
| Alertmanager | `https://alertmanager.internal.tomnowak.work` | `https://alertmanager.internal.integration.tomnowak.work` | `https://alertmanager.internal.dev.tomnowak.work` |
| Hubble UI | `https://hubble.internal.tomnowak.work` | `https://hubble.internal.integration.tomnowak.work` | `https://hubble.internal.dev.tomnowak.work` |
| Longhorn UI | `https://longhorn.internal.tomnowak.work` | `https://longhorn.internal.integration.tomnowak.work` | `https://longhorn.internal.dev.tomnowak.work` |
| Garage Admin | `https://garage.internal.tomnowak.work` | `https://garage.internal.integration.tomnowak.work` | `https://garage.internal.dev.tomnowak.work` |

**Domain pattern:** `<service>.internal.<cluster-suffix>.tomnowak.work`
- live: `internal.tomnowak.work`
- integration: `internal.integration.tomnowak.work`
- dev: `internal.dev.tomnowak.work`

**Usage with curl (use `-k` for self-signed TLS):**

```bash
# Query Prometheus API
curl -sk "https://prometheus.internal.tomnowak.work/api/v1/query?query=up" | jq '.data.result'

# Check firing alerts
curl -sk "https://prometheus.internal.tomnowak.work/api/v1/alerts" | jq '.data.alerts[] | select(.state == "firing")'

# Query Alertmanager
curl -sk "https://alertmanager.internal.tomnowak.work/api/v2/alerts" | jq .
```

**Using the helper scripts with internal DNS:**

```bash
# Prometheus (live cluster)
export PROMETHEUS_URL=https://prometheus.internal.tomnowak.work
.claude/skills/prometheus/scripts/promql.sh alerts --firing

# Loki (no HTTPRoute - requires port-forward, see fallback below)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/loki-headless 3100:3100 &
export LOKI_URL=http://localhost:3100
.claude/skills/loki/scripts/logql.sh tail '{namespace="monitoring"}' --since 15m
```

**Note:** Loki does not have an HTTPRoute on the internal gateway. Use port-forward for Loki access.

### Fallback: Port-Forward Access

Use port-forwarding only when DNS-based access is unavailable (e.g., network issues, local development without VPN):

```bash
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090 &
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/loki-headless 3100:3100 &
```

# Debugging Kubernetes Incidents

## Core Principles

- **5 Whys Analysis** - NEVER stop at symptoms. Ask "why" until you reach the root cause.
- **Read-Only Investigation** - Observe and analyze, never modify resources
- **Multi-Source Correlation** - Combine logs, events, metrics for complete picture
- **Research Unknown Services** - Check documentation before deep investigation

## The 5 Whys Analysis (CRITICAL)

**You MUST apply 5 Whys before concluding any investigation.** Stopping at symptoms leads to ineffective fixes.

### How to Apply

1. Start with the observed symptom
2. Ask "Why did this happen?" for each answer
3. Continue until you reach an actionable root cause (typically 5 levels)

### Example

```
Symptom: Helm install failed with "context deadline exceeded"

Why #1: Why did Helm timeout?
  → Pods never became Ready

Why #2: Why weren't pods Ready?
  → Pods stuck in Pending state

Why #3: Why were pods Pending?
  → PVCs couldn't bind (StorageClass "fast" not found)

Why #4: Why was StorageClass missing?
  → longhorn-storage Kustomization failed to apply

Why #5: Why did the Kustomization fail?
  → numberOfReplicas was integer instead of string

ROOT CAUSE: YAML type coercion issue
FIX: Use properly typed variable for StorageClass parameters
```

### Red Flags You Haven't Reached Root Cause

- Your "fix" is increasing a timeout or retry count
- Your "fix" addresses the symptom, not what caused it
- You can still ask "but why did THAT happen?"
- Multiple issues share the same underlying cause

```
BAD:  "Helm timed out → increase timeout to 15m"
GOOD: "Helm timed out → ... → Kustomization type error → fix YAML"
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

## Investigation Phases

### Phase 1: Triage

1. **Confirm cluster** - Ask user: "Which cluster? (dev/integration/live)"
2. **Assess severity** - P1 (down) / P2 (degraded) / P3 (minor) / P4 (cosmetic)
3. **Identify scope** - Pod / Deployment / Namespace / Cluster-wide

### Phase 2: Data Collection

```bash
# Pod status and events
kubectl get pods -n <namespace>
kubectl describe pod <pod> -n <namespace>

# Logs (current and previous)
kubectl logs <pod> -n <namespace> --tail=100
kubectl logs <pod> -n <namespace> --previous

# Events timeline
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Resource usage
kubectl top pods -n <namespace>
```

**Metrics and alerts via internal gateway (preferred over port-forward):**

```bash
# Check firing alerts
curl -sk "https://prometheus.internal.tomnowak.work/api/v1/alerts" | jq '.data.alerts[] | select(.state == "firing")'

# Pod restart metrics
curl -sk "https://prometheus.internal.tomnowak.work/api/v1/query?query=increase(kube_pod_container_status_restarts_total[1h])>0" | jq '.data.result'
```

### Phase 3: Correlation

1. Extract timestamps from logs, events, metrics
2. Identify what happened FIRST (root cause)
3. Trace the cascade of effects

### Phase 4: Root Cause (5 Whys)

Apply 5 Whys analysis. Validate:
- **Temporal**: Did it happen BEFORE the symptom?
- **Causal**: Does it logically explain the symptom?
- **Evidence**: Is there supporting data?
- **Complete**: Have you asked "why" enough times?

### Phase 5: Remediation

Use **AskUserQuestion** tool to present fix options when multiple valid approaches exist.

Provide recommendations only (read-only investigation):
- **Immediate**: Rollback, scale, restart
- **Permanent**: Code/config fixes
- **Prevention**: Alerts, quotas, tests

## Quick Diagnosis

| Symptom | First Check | Common Cause |
|---------|-------------|--------------|
| `ImagePullBackOff` | `describe pod` events | Wrong image/registry auth |
| `Pending` | Events, node capacity | Insufficient resources |
| `CrashLoopBackOff` | `logs --previous` | App error, missing config |
| `OOMKilled` | Memory limits | Memory leak, limits too low |
| `Unhealthy` | Probe config | Slow startup, wrong endpoint |
| Service unreachable | Hubble dropped traffic | **Network policy blocking** |
| Can't reach database | Hubble + namespace labels | Missing access label |
| Gateway returns 503 | Hubble from istio-gateway | Missing profile label |

## Common Failure Chains

**Storage failures cascade:**
```
StorageClass missing → PVC Pending → Pod Pending → Helm timeout
```

**Network failures cascade:**
```
DNS failure → Service unreachable → Health check fails → Pod restarted
```

**Network policy failures cascade:**
```
Missing namespace profile label → No ingress allowed → Service unreachable from gateway
Missing access label → Can't reach database → App fails health checks → CrashLoopBackOff
```

**Secret failures cascade:**
```
ExternalSecret fails → Secret missing → Pod CrashLoopBackOff
```

## Network Policy Debugging (Cilium + Hubble)

**Network policies are ENFORCED - all traffic is implicitly denied unless allowed.**

### Check for Blocked Traffic

```bash
# Setup Hubble access (run once per session)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n kube-system svc/hubble-relay 4245:80 &

# See dropped traffic in a namespace
hubble observe --verdict DROPPED --namespace <namespace> --since 5m

# See what's trying to reach a service
hubble observe --to-namespace <namespace> --verdict DROPPED --since 5m

# Check specific traffic flow
hubble observe --from-namespace <source> --to-namespace <dest> --since 5m
```

### Common Network Policy Issues

| Symptom | Check | Fix |
|---------|-------|-----|
| Service unreachable from gateway | `kubectl get ns <ns> --show-labels` | Add profile label |
| Can't reach database | Check `access.network-policy.homelab/postgres` label | Add access label |
| Pods can't resolve DNS | Hubble DNS drops (rare - baseline allows) | Check for custom egress blocking |
| Inter-pod communication fails | Hubble intra-namespace drops | Baseline should allow - check for overrides |

### Namespace Labels Checklist

```bash
# Check namespace has required labels
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get ns <namespace> -o jsonpath='{.metadata.labels}' | jq

# Required for app namespaces:
# - network-policy.homelab/profile: standard|internal|internal-egress|isolated

# Optional access labels:
# - access.network-policy.homelab/postgres: "true"
# - access.network-policy.homelab/garage-s3: "true"
# - access.network-policy.homelab/kube-api: "true"
```

### Emergency: Disable Network Policies

```bash
# Escape hatch - disables enforcement for namespace (triggers alert after 5m)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl label namespace <ns> network-policy.homelab/enforcement=disabled

# Re-enable after fixing
KUBECONFIG=~/.kube/<cluster>.yaml kubectl label namespace <ns> network-policy.homelab/enforcement-
```

See `docs/runbooks/network-policy-escape-hatch.md` for full procedure.

## Flux GitOps Commands

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

## Kickstarting Stalled HelmReleases

HelmReleases can get stuck in a `Stalled` state with `RetriesExceeded` even after the underlying issue is resolved. This happens because:

1. The HR hit its retry limit (default: 4 attempts)
2. The failure counter persists even if pods are now healthy
3. Flux won't auto-retry once `Stalled` condition is set

**Symptoms:**
```
STATUS: Stalled
MESSAGE: Failed to install after 4 attempt(s)
REASON: RetriesExceeded
```

**Diagnosis:** Check if the underlying resources are actually healthy:
```bash
# HR shows Failed, but check if pods are running
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get pods -n <namespace> -l app.kubernetes.io/name=<app>

# If pods are Running but HR is Stalled, the HR just needs a reset
```

**Fix:** Suspend and resume to reset the failure counter:
```bash
KUBECONFIG=~/.kube/<cluster>.yaml flux suspend helmrelease <name> -n flux-system
KUBECONFIG=~/.kube/<cluster>.yaml flux resume helmrelease <name> -n flux-system
```

**Common causes of initial failure (that may have self-healed):**
- Missing Secret/ConfigMap (ExternalSecret eventually created it)
- Missing CRD (operator finished installing)
- Transient network issues during image pull
- Resource quota temporarily exceeded

**Prevention:** Ensure proper `dependsOn` ordering so prerequisites are ready before HelmRelease installs.

## Researching Unfamiliar Services

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

**Chart URL → Docs mapping:**
| Chart Source | Documentation |
|--------------|---------------|
| `charts.jetstack.io` | cert-manager.io/docs |
| `charts.longhorn.io` | longhorn.io/docs |
| `grafana.github.io` | grafana.com/docs |
| `prometheus-community.github.io` | prometheus.io/docs |

## Common Confusions

BAD: Jump to logs without checking events first
GOOD: Events provide context, then investigate logs

BAD: Look only at current pod state
GOOD: Check `--previous` logs if pod restarted

BAD: Assume first error is root cause
GOOD: Apply 5 Whys to find true root cause

BAD: Investigate without confirming cluster
GOOD: ALWAYS confirm cluster before any kubectl command

BAD: Use `helm list` to check Helm release status
GOOD: Use `kubectl get helmrelease -A` - Flux manages releases via CRDs, not Helm CLI

## Keywords

kubernetes, debugging, crashloopbackoff, oomkilled, pending, root cause analysis, 5 whys, incident investigation, pod logs, events, kubectl, flux, gitops, troubleshooting
