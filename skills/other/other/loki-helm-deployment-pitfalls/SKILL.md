---
name: loki-helm-deployment-pitfalls
description: |
  Fix common Loki Helm chart deployment failures on Kubernetes with Terraform.
  Use when: (1) Loki pod fails with "mkdir: read-only file system" for compactor
  or ruler paths, (2) Helm chart fails with "Helm test requires the Loki Canary
  to be enabled", (3) Helm install fails with "cannot re-use a name that is still
  in use" after a failed atomic deploy, (4) PV stuck in Released state after failed
  Helm install, (5) "entry too far behind" errors flooding Loki logs after initial
  Alloy deployment. Covers single-binary mode with filesystem storage on NFS.
author: Claude Code
version: 1.0.0
date: 2026-02-13
---

# Loki Helm Chart Deployment Pitfalls

## Problem
Deploying the Grafana Loki Helm chart in single-binary mode with Terraform hits
multiple non-obvious failures that aren't documented together.

## Context / Trigger Conditions
- Deploying Loki via `helm_release` in Terraform
- Using `deploymentMode: SingleBinary` with filesystem storage on NFS
- First-time deployment or redeployment after failures

## Pitfall 1: Read-Only Root Filesystem

**Error:** `mkdir /loki/compactor: read-only file system`

**Cause:** The Loki Helm chart runs containers with a read-only root filesystem
for security. The compactor `working_directory` and ruler `rule_path` default to
paths under `/loki/` which is on the read-only root FS.

**Fix:** Use paths under `/var/loki/` — the Helm chart mounts the persistence
volume there:
```yaml
compactor:
  working_directory: /var/loki/compactor    # NOT /loki/compactor
ruler:
  rule_path: /var/loki/scratch              # NOT /loki/scratch
```

## Pitfall 2: Canary Required

**Error:** `Helm test requires the Loki Canary to be enabled`

**Cause:** The Loki Helm chart's validation template requires `lokiCanary.enabled`
to be true. You cannot disable it.

**Fix:** Leave `lokiCanary` enabled (default). You can disable `gateway`,
`chunksCache`, and `resultsCache` to reduce resource usage:
```yaml
gateway:
  enabled: false
chunksCache:
  enabled: false
resultsCache:
  enabled: false
# Do NOT add: lokiCanary: enabled: false
```

## Pitfall 3: Stale Helm Release After Failed Atomic Deploy

**Error:** `cannot re-use a name that is still in use`

**Cause:** When `atomic = true` and the deploy fails, Helm rolls back but
sometimes leaves a stale release secret in Kubernetes. Terraform then can't
create a new release with the same name.

**Fix:** Delete the stale Helm secret:
```bash
kubectl delete secret -n monitoring sh.helm.release.v1.loki.v1
```
Also consider removing `atomic = true` for initial deployments and adding it
back after the first successful install. Use a longer `timeout` (600s+) for
first deploy since image pulls take time.

## Pitfall 4: PV Stuck in Released State

**Symptom:** PV shows `Released` status, PVC can't bind, Loki pod stuck in Pending.

**Cause:** After a failed Helm deploy, the PVC is deleted but the PV retains a
`claimRef` to the old PVC. New PVCs can't bind to a `Released` PV.

**Fix:** Clear the stale claimRef:
```bash
kubectl patch pv loki --type json -p '[{"op": "remove", "path": "/spec/claimRef"}]'
```
The PV will transition from `Released` to `Available` and can be bound again.

## Pitfall 5: "Entry Too Far Behind" Log Spam

**Error:** `entry too far behind, entry timestamp is: ... oldest acceptable timestamp is: ...`

**Cause:** Alloy reads all historical log files from the Kubernetes API on first
startup. Old entries are rejected by Loki's ingester because they're behind the
newest entry for that stream.

**Fix:** This is harmless and self-resolving — Alloy catches up to present time
and errors stop. To clear immediately:
```bash
kubectl rollout restart ds -n monitoring alloy
```
After restart, Alloy tails from approximately "now" for each container.

## Pitfall 6: Alertmanager Service Name

**Symptom:** Loki ruler alerts never fire despite correct LogQL rules.

**Cause:** The Prometheus Helm chart names the Alertmanager service
`prometheus-alertmanager`, not `alertmanager`. Using the wrong name causes
silent alert delivery failures.

**Fix:**
```yaml
ruler:
  alertmanager_url: http://prometheus-alertmanager.monitoring.svc.cluster.local:9093
```
Verify the actual service name: `kubectl get svc -n monitoring | grep alertmanager`

## Verification
```bash
# Loki pod running
kubectl get pods -n monitoring -l app.kubernetes.io/name=loki

# Loki receiving logs
kubectl port-forward -n monitoring svc/loki 3100:3100 &
curl -s 'http://localhost:3100/loki/api/v1/labels'
# Should return JSON with namespace, pod, container labels

# PV bound
kubectl get pv loki
# STATUS should be "Bound"
```

## Notes
- Always check PV status before retrying a failed deploy
- The Loki Helm chart creates many components by default (gateway, canary,
  memcached caches) — disable what you don't need for single-binary mode
- WAL directory can be on tmpfs (emptyDir with `medium: Memory`) for
  disk-friendly setups, but data is lost on pod crash
- See also: `helm-release-force-rerender` for Helm values not updating resources
