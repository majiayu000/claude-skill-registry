---
name: sre
description: |
  SRE debugging methodology for Kubernetes incident investigation, root cause analysis,
  and failure diagnosis.

  Use when: (1) Pods not starting, stuck, or failing (CrashLoopBackOff, ImagePullBackOff, OOMKilled, Pending),
  (2) Debugging Kubernetes errors or investigating "why is my pod...", (3) Service degradation or unavailability,
  (4) Root cause analysis for any Kubernetes incident, (5) Network policy blocking traffic,
  (6) Stalled HelmReleases or Flux failures that need troubleshooting.

  Triggers: "pod not starting", "pod stuck", "CrashLoopBackOff", "ImagePullBackOff", "OOMKilled",
  "Pending pod", "why is my pod", "kubernetes error", "k8s error", "service not available",
  "can't reach service", "debug kubernetes", "troubleshoot k8s", "what's wrong with my pod",
  "deployment not working", "helm install failed", "flux not reconciling", "root cause",
  "5 whys", "incident", "network policy blocking", "hubble dropped", "stalled helmrelease",
  "live not updating", "promotion pipeline stuck", "artifact not promoted"
user-invocable: false
---

> **Cluster access, KUBECONFIG patterns, and internal service URLs** are in the `k8s` skill.

# Debugging Kubernetes Incidents

## Core Principles

- **5 Whys Analysis** - NEVER stop at symptoms. Ask "why" until you reach the root cause.
- **Read-Only Investigation** - Observe and analyze, never modify resources on integration/live. Dev cluster permits direct mutations for debugging (see troubleshooter agent boundaries)
- **Multi-Source Correlation** - Combine logs, events, metrics for complete picture
- **Research Unknown Services** - Check documentation before deep investigation
- **Zero Alert Tolerance** - Every firing alert must be addressed immediately: fix the root cause, or as a last resort, create a declarative Silence CR with justification. Never ignore, defer, or dismiss a firing alert.

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

**Metrics and alerts via kubectl exec (Prometheus is behind OAuth2 Proxy — DNS URLs won't work for API queries):**

```bash
# Check firing alerts
KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/alerts' | jq '.data.alerts[] | select(.state == "firing")'

# Pod restart metrics
KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/query?query=increase(kube_pod_container_status_restarts_total[1h])>0' | jq '.data.result'
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

## Promotion Pipeline Debugging

**Symptom: "Live cluster not updating after merge"**

The OCI artifact promotion pipeline has multiple stages where failures can stall deployment.
Walk through each stage in order to find where the pipeline is stuck.

### Diagnostic Steps

```
1. PR merged to main
   └─ Check: Did build-platform-artifact.yaml trigger?
      └─ GitHub Actions → "Build Platform Artifact" workflow
      └─ If missing: Was kubernetes/ modified? (paths filter)

2. OCI artifact built
   └─ Check: Is the artifact in GHCR with integration-* tag?
      └─ flux list artifact oci://ghcr.io/<repo>/platform | grep integration

3. Integration cluster picks up artifact
   └─ Check: Does OCIRepository see the new version?
      └─ KUBECONFIG=~/.kube/integration.yaml kubectl get ocirepository -n flux-system
      └─ Look at .status.artifact.revision — does it match the new RC tag?
      └─ If stale: Check semver constraint (must be ">= 0.0.0-0" to accept RCs)

4. Integration reconciliation succeeds
   └─ Check: Platform Kustomization healthy?
      └─ KUBECONFIG=~/.kube/integration.yaml flux get kustomizations -n flux-system
      └─ If failed: Read Kustomization events for the error

5. Flux Alert fires repository_dispatch
   └─ Check: Did the Alert fire?
      └─ KUBECONFIG=~/.kube/integration.yaml kubectl describe alert validation-success -n flux-system
      └─ Check Provider (GitHub) status:
         KUBECONFIG=~/.kube/integration.yaml kubectl get providers -n flux-system

6. tag-validated-artifact.yaml runs
   └─ Check: Did the workflow trigger?
      └─ GitHub Actions → "Tag Validated Artifact" workflow
      └─ If not triggered: repository_dispatch may not have fired
         (check Provider secret has repo scope)
      └─ If triggered but failed: Check workflow logs for tagging errors

7. Live cluster picks up validated artifact
   └─ Check: Does OCIRepository see the stable semver?
      └─ KUBECONFIG=~/.kube/live.yaml kubectl get ocirepository -n flux-system
      └─ Semver constraint must be ">= 0.0.0" (stable only, no RCs)
```

### Common Failure Modes

| Stage | Symptom | Common Cause |
|-------|---------|--------------|
| Build | Workflow did not trigger | `kubernetes/` not in changed paths |
| Build | Artifact push failed | GHCR auth issue (`GITHUB_TOKEN` permissions) |
| Integration | OCIRepository not updating | Semver constraint mismatch (not accepting RCs) |
| Validation | Kustomization failed | Actual config error in the merged PR |
| Promotion | `repository_dispatch` not received | Provider secret missing `repo` scope |
| Promotion | Workflow skipped (idempotency guard) | Artifact already tagged as validated |
| Live | OCIRepository not updating | Stable semver tag not created by tag workflow |

### Manual Promotion (Emergency)

If the pipeline is stuck and live needs the update:

```bash
# Authenticate to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USER --password-stdin

# Find the integration artifact
flux list artifact oci://ghcr.io/<repo>/platform | grep integration

# Manually tag as validated + stable semver
flux tag artifact oci://ghcr.io/<repo>/platform:<rc-tag> --tag <stable-semver>
```

See `.github/CLAUDE.md` for full pipeline architecture and rollback procedures.

## Common Confusions

BAD: Jump to logs without checking events first
GOOD: Events provide context, then investigate logs

BAD: Look only at current pod state
GOOD: Check `--previous` logs if pod restarted

BAD: Assume first error is root cause
GOOD: Apply 5 Whys to find true root cause

BAD: Investigate without confirming cluster
GOOD: ALWAYS confirm cluster before any kubectl command

## Keywords

kubernetes, debugging, crashloopbackoff, oomkilled, pending, root cause analysis, 5 whys, incident investigation, pod logs, events, troubleshooting, network policy, hubble, stalled helmrelease, promotion pipeline, live not updating
