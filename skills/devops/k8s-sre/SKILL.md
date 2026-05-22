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
❌ WRONG: "Helm timed out → increase timeout to 15m"
✅ CORRECT: "Helm timed out → ... → Kustomization type error → fix YAML"
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

## Common Failure Chains

**Storage failures cascade:**
```
StorageClass missing → PVC Pending → Pod Pending → Helm timeout
```

**Network failures cascade:**
```
DNS failure → Service unreachable → Health check fails → Pod restarted
```

**Secret failures cascade:**
```
ExternalSecret fails → Secret missing → Pod CrashLoopBackOff
```

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

❌ Jump to logs without checking events first
✅ Events provide context, then investigate logs

❌ Look only at current pod state
✅ Check `--previous` logs if pod restarted

❌ Assume first error is root cause
✅ Apply 5 Whys to find true root cause

❌ Investigate without confirming cluster
✅ ALWAYS confirm cluster before any kubectl command

## Keywords

kubernetes, debugging, crashloopbackoff, oomkilled, pending, root cause analysis, 5 whys, incident investigation, pod logs, events, kubectl, flux, gitops, troubleshooting
