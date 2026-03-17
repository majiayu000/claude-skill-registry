---
name: k8s-hpa-scaling-storm
description: |
  Fix and prevent HPA (HorizontalPodAutoscaler) scaling storms where pods scale to
  maxReplicas uncontrollably. Use when: (1) HPA shows memory or CPU utilization at
  200%+ causing rapid scale-up, (2) dozens or hundreds of pods created by HPA in minutes,
  (3) cluster becomes unstable due to resource exhaustion from too many pods,
  (4) etcd timeouts or API server crashes from pod churn, (5) adding resource requests
  to a deployment that previously had none causes HPA to miscalculate utilization.
  Covers emergency response and prevention patterns.
author: Claude Code
version: 1.0.0
date: 2026-02-15
---

# Kubernetes HPA Scaling Storm

## Problem
When an HPA is configured with a memory or CPU utilization target but the underlying
deployment has insufficient resource requests, the HPA calculates artificially high
utilization percentages (e.g., 220% of a 256Mi request when actual usage is 570Mi).
This causes the HPA to scale pods to maxReplicas (often 100) within minutes, exhausting
cluster resources and potentially crashing etcd and the API server.

## Context / Trigger Conditions
- `kubectl get hpa` shows `<unknown>/70%` or very high percentages (200%+)
- Pod count for a deployment rapidly increases to maxReplicas
- etcd timeout errors in `kubectl` or `terraform apply`
- API server becomes unreachable (`connection refused` or `network is unreachable`)
- Adding resource requests to a Helm chart that previously had none
- Memory-based HPA targets with real usage far exceeding requests

## Solution

### Emergency Response (stop the storm)

**Step 1: Delete the HPA immediately**
```bash
kubectl --kubeconfig $(pwd)/config delete hpa <hpa-name> -n <namespace>
```

**Step 2: Scale the deployment down**
```bash
kubectl --kubeconfig $(pwd)/config scale deployment <name> -n <namespace> --replicas=2
```

**Step 3: Wait for pods to terminate and cluster to stabilize**
```bash
# Watch pod count decrease
kubectl --kubeconfig $(pwd)/config get pods -n <namespace> -l <label> | wc -l
```

If the API server is unresponsive, wait 3-5 minutes for it to self-recover. The kubelet
will restart static pods (etcd, kube-apiserver) automatically.

### Prevention

**Rule 1: Set resource requests to match actual usage**
Before enabling HPA, check actual resource consumption:
```bash
kubectl top pods -n <namespace> -l <label>
```
Set requests to the baseline (idle) usage, not the minimum possible value.

**Rule 2: Set reasonable maxReplicas**
Never use maxReplicas > 10 unless you've verified the cluster can handle it.
Default of 100 is almost never appropriate for a home/small cluster.

**Rule 3: Prefer CPU-only HPA targets**
Memory-based scaling is problematic because:
- Memory usage grows over time and rarely decreases
- Memory-based scaling creates pods that never scale down
- CPU is more responsive to load changes

**Rule 4: Test HPA changes on a deployment with 0 existing pods first**
If adding resource requests to a deployment managed by HPA, temporarily disable
the HPA first, set the requests, verify utilization is reasonable, then re-enable.

## Cascade Effects
A scaling storm can cause:
1. etcd storage exhaustion (too many pod objects)
2. API server OOM or connection limits
3. VPN/network connectivity loss (if VPN runs in the cluster)
4. Kyverno webhook failures (admission controller overwhelmed)
5. Other pods evicted or unable to schedule

## Verification
- `kubectl get hpa -n <namespace>` shows reasonable utilization (< 100%)
- Pod count is stable at expected replicas
- `kubectl get nodes` responds promptly
- No etcd timeout errors

## Example
```bash
# Observed: HPA scaling Collabora to 100 pods
$ kubectl get hpa -n nextcloud
NAME                 TARGETS                          MINPODS  MAXPODS  REPLICAS
nextcloud-collabora  cpu: 0%/70%, memory: 220%/50%   2        100      83

# Emergency fix
$ kubectl delete hpa nextcloud-collabora -n nextcloud
$ kubectl scale deployment nextcloud-collabora -n nextcloud --replicas=2

# Root cause: 256Mi memory request, actual usage 570Mi
# Fix: increase request to 1Gi or disable memory target
```

## Notes
- If the HPA is managed by a Helm chart, deleting it via kubectl is temporary—the next
  Helm upgrade will recreate it. You must also update the Helm values.
- In this project, Collabora was ultimately disabled in favor of OnlyOffice to avoid
  the HPA issue entirely.
- See also: `helm-stuck-release-recovery` for fixing Helm releases broken by the storm.
