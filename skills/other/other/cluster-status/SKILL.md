---
name: cluster-status
description: "Show GKE cluster health dashboard — nodes, agents, app pods, ingress, certs, analytics. Use when user asks about cluster status, pod health, node count, or infrastructure state."
---

# Cluster Status — GKE Health Dashboard

Shows a comprehensive status dashboard for the Fenrir Ledger GKE Autopilot cluster.

## Usage

```
/cluster-status
```

## Instructions

Run the following kubectl commands and render as a formatted dashboard.

### Step 1 — Gather data (single parallel batch)

```bash
echo "=== Nodes ===" && \
kubectl get nodes -o custom-columns='NAME:.metadata.name,STATUS:.status.conditions[-1].type,AGE:.metadata.creationTimestamp,VERSION:.status.nodeInfo.kubeletVersion' --no-headers 2>&1 && \
echo "=== Agent Jobs ===" && \
kubectl get jobs -n fenrir-agents --sort-by=.metadata.creationTimestamp -o custom-columns='NAME:.metadata.name,ACTIVE:.status.active,OK:.status.succeeded,FAIL:.status.failed' --no-headers 2>&1 && \
echo "=== Agent Pods ===" && \
kubectl get pods -n fenrir-agents --no-headers 2>&1 && \
echo "=== App Pods ===" && \
kubectl get pods -n fenrir-app -l 'app.kubernetes.io/name in (fenrir-app,redis)' --no-headers 2>&1 && \
echo "=== Analytics ===" && \
kubectl get pods -n fenrir-analytics --no-headers 2>&1 && \
echo "=== Ingresses ===" && \
kubectl get ingress -A -o custom-columns='NS:.metadata.namespace,NAME:.metadata.name,HOSTS:.spec.rules[*].host,ADDRESS:.status.loadBalancer.ingress[*].ip' --no-headers 2>&1 && \
echo "=== Certs ===" && \
kubectl get managedcertificate -A -o custom-columns='NS:.metadata.namespace,NAME:.metadata.name,STATUS:.status.certificateStatus' --no-headers 2>&1
```

### Step 2 — Render dashboard

Format as markdown tables:

```
## GKE Cluster Dashboard

### Nodes (N total)
| Node | Status | Age |
|------|--------|-----|

### Agent Jobs
| # | Agent | Status |
|---|-------|--------|
(Parse issue number + agent from job name: agent-issue-N-stepS-agent-hash)
Active = running, Succeeded = completed, Failed = failed

### Application
| Pod | Status | Restarts |
|-----|--------|----------|

### Analytics (Umami)
| Pod | Status | Restarts |
|-----|--------|----------|

### Ingress & TLS
| Service | Host | IP | Cert |
|---------|------|----|------|
(Render Host as a clickable markdown link: [host](https://host))
```

### Step 3 — Summary

Add a one-line summary at the top:
- "All green" if everything is Running/Active/Ready
- "Issues detected" with bullet list if anything is unhealthy

## Notes

- Requires `kubectl` configured for the GKE cluster
- Agent job names follow pattern: `agent-issue-<N>-step<S>-<agent>-<hash>`
- Warm node pool pods and idle detector cronjobs can be excluded from the app table for clarity
