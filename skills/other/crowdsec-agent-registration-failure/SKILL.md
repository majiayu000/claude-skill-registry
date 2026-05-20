---
name: crowdsec-agent-registration-failure
description: |
  Fix CrowdSec agent pods stuck in CrashLoopBackOff after LAPI restart due to stale
  machine registrations. Use when: (1) CrowdSec agent init container fails with
  "user already exist" error during cscli lapi register, (2) agent pods show hundreds
  of init container restarts, (3) LAPI was restarted or redeployed but agents kept
  running with old credentials, (4) cscli machines list shows stale entries for
  current agent pod names. Covers deleting stale registrations to allow re-registration.
author: Claude Code
version: 1.0.0
date: 2026-02-15
---

# CrowdSec Agent Registration Failure

## Problem
After a CrowdSec LAPI restart or redeployment, agent DaemonSet pods lose their
credentials but LAPI retains the old machine registrations. When agents try to
re-register with the same pod name, the `wait-for-lapi-and-register` init container
fails with `user already exist`, causing CrashLoopBackOff with hundreds of restarts.

## Context / Trigger Conditions
- Agent init container logs show: `Error: cscli lapi register: api client register: api register ... user 'crowdsec-agent-xxxxx': user already exist`
- Agent pods show status `CrashLoopBackOff` or `Init:CrashLoopBackOff` with many restarts
- `kubectl describe pod` shows `BackOff restarting failed container wait-for-lapi-and-register`
- LAPI pods were recently restarted or redeployed
- `cscli machines list` on LAPI shows entries matching the stuck agent pod names

## Solution

### Step 1: Identify stuck agents
```bash
kubectl --kubeconfig $(pwd)/config get pods -n crowdsec
```
Note the pod names that are in CrashLoopBackOff (e.g., `crowdsec-agent-jr5q7`).

### Step 2: Confirm the init container error
```bash
kubectl --kubeconfig $(pwd)/config logs -n crowdsec <agent-pod> -c wait-for-lapi-and-register --tail=5
```
Should show `user already exist` error.

### Step 3: Find a running LAPI pod
```bash
kubectl --kubeconfig $(pwd)/config get pods -n crowdsec | grep lapi
```

### Step 4: Delete stale machine registrations from LAPI
```bash
kubectl --kubeconfig $(pwd)/config exec -n crowdsec <lapi-pod> -- cscli machines delete <agent-pod-name>
```
Repeat for each stuck agent.

### Step 5: Wait for agents to recover
The agents are in CrashLoopBackOff with exponential backoff (up to 5 minutes). They'll
automatically retry registration and succeed after the stale entry is deleted. This can
take up to 5 minutes per agent depending on where they are in the backoff cycle.

## Verification
```bash
# All agents should show Running status
kubectl --kubeconfig $(pwd)/config get pods -n crowdsec | grep agent
# DaemonSet should show all pods READY
kubectl --kubeconfig $(pwd)/config get ds -n crowdsec
```

## Example
```bash
# Identify stuck agents
$ kubectl get pods -n crowdsec | grep agent
crowdsec-agent-jr5q7  0/1  CrashLoopBackOff  485  3d
crowdsec-agent-jw76q  1/1  Running            8    3d
crowdsec-agent-mtgxh  0/1  CrashLoopBackOff  483  3d
crowdsec-agent-pfw2l  0/1  CrashLoopBackOff  481  3d

# Delete stale registrations
$ kubectl exec -n crowdsec crowdsec-lapi-xxx -- cscli machines delete crowdsec-agent-jr5q7
level=info msg="machine 'crowdsec-agent-jr5q7' deleted successfully"
$ kubectl exec -n crowdsec crowdsec-lapi-xxx -- cscli machines delete crowdsec-agent-mtgxh
$ kubectl exec -n crowdsec crowdsec-lapi-xxx -- cscli machines delete crowdsec-agent-pfw2l

# Wait ~5 minutes, then verify
$ kubectl get pods -n crowdsec | grep agent
crowdsec-agent-jr5q7  1/1  Running  1  3d
crowdsec-agent-jw76q  1/1  Running  8  3d
crowdsec-agent-mtgxh  1/1  Running  1  3d
crowdsec-agent-pfw2l  1/1  Running  1  3d
```

## Notes
- This is a known limitation of the CrowdSec Helm chart — the init container registration
  script is not idempotent (it doesn't handle "already exists" by deleting and re-registering).
- The `cscli machines list` output will show many historical stale entries from past
  DaemonSet rollouts. These are harmless but can be cleaned up if desired.
- This issue also causes the CrowdSec blocklist import CronJob to fail, since it selects
  agent pods alphabetically and may pick a non-running one. Fixing the agents also fixes
  the blocklist import.
- See also: `k8s-nfs-mount-troubleshooting` for other common pod startup failures.
