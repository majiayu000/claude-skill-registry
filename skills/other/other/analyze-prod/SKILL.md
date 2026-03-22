---
name: analyze-prod
description: Analyze a production environment by collecting cluster, database, log, and networking evidence, then producing a root-cause-oriented diagnosis and next actions.
---

# Analyze Production Environment

Perform read-only production diagnosis first. Do not mutate production without explicit approval.

## 1. Establish Scope

Capture:

- Problem statement
- Affected service or namespace
- Environment or cluster
- Approximate start time
- Incident severity if known

## 2. Detect Platform

Read root `AGENTS.md`, deployment files, and cloud config to determine whether the target is Azure, GCP, or AWS.

Load `cloud-platforms` for provider-specific commands.

## 3. Collect Read-Only Evidence

Gather the smallest useful snapshot:

- Cluster context and node health
- Pod and deployment status
- Logs for failing workloads
- Resource pressure signals
- Ingress, service, and endpoint status
- Managed database health
- Recent warning events

## 4. Analyze

Look for:

- Restart loops
- OOM or probe failures
- Dependency connectivity failures
- Capacity saturation
- Deployment regressions
- Database bottlenecks

Tie every conclusion to evidence.

## 5. Diagnose

Return:

- Environment summary
- Findings
- Suspected root cause
- Blast radius
- Recommended mitigation
- Recommended durable fix

If a production mutation is needed, present it separately and wait for approval.

## Integration

- Companion skill: `cloud-platforms`
- Common follow-up: `bugfix`