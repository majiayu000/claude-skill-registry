---
name: analyze-prod
description: Analyze production environment — collect Kubernetes pod status, managed database health, logs, metrics, networking, and diagnose issues. Supports GCP, Azure, and AWS via the `cloud-platforms` skill. Applies SRE or DevOps roles. Use standalone or as part of production incident investigation.
context: fork
allowed-tools: Read, Grep, Glob, Bash
---

# Analyze Production Environment

Systematic analysis of the production environment. Collects cluster status, pod health, database metrics, logs, and diagnoses issues. Works standalone or as an entry point for production bugfixing.

**Cloud platform detection**: Read `CLAUDE.md` to identify which cloud platform is used. Consult `cloud-platforms` skill and load the corresponding reference module (GCP, Azure, or AWS) for platform-specific CLI commands.

**⚠️ SAFETY: This workflow runs READ-ONLY commands only. No mutations (scale, delete, restart, deploy) without explicit user approval at Step 6.**

## 1. Clarify the Scope

Ask the user:

- **What is the problem or question?** (e.g., "pods crashlooping", "high latency on /api/orders", "DB connections exhausted", "general health check")
- **Which service(s) are affected?** (deployment name, namespace, or "all")
- **Cloud environment?** (project/subscription/account + cluster name)
- **When did the issue start?** (deploy, config change, traffic spike, or unknown)
- **Is there an active incident?** (P1–P4 severity, or no incident)

If invoked as part of a bugfix/incident flow — extract context from the parent conversation instead of asking.

## 2. Apply Appropriate Role

Select and apply the role based on the problem type:

| Problem Type | Primary Role | Rationale |
|---|---|---|
| Pod crashes, restarts, health check failures | `Agent(sre-engineer)` | Reliability, K8s troubleshooting, SLO impact |
| High latency, error rate spikes, SLO burn | `Agent(sre-engineer)` | Observability, SLI/SLO analysis |
| Managed DB issues (connections, replication, CPU) | `Agent(sre-engineer)` | Database reliability, capacity |
| Networking, ingress, DNS, connectivity | `Agent(sre-engineer)` + `Agent(devops-engineer)` | Network diagnostics + infra config |
| Deployment failures, rollback needed | `Agent(devops-engineer)` | CI/CD, Helm, K8s deployment |
| Terraform/infra drift, resource config | `Agent(devops-engineer)` | IaC, cloud resource management |
| Application errors visible in logs | Stack-specific role | `Agent(java-engineer)`, `Agent(python-engineer)`, `Agent(frontend-engineer)` |
| General / unclear | `Agent(sre-engineer)` | SRE debugging methodology as default for prod |

Announce the applied role(s) to the user. If this is a P1/P2 incident, always apply `Agent(sre-engineer)`.

## 3. Establish Context

Before collecting data, establish the environment context:

### 3a. Cloud Platform Context

Detect platform from `CLAUDE.md` and verify authentication. Consult `cloud-platforms` skill for platform-specific auth verification commands:
- **GCP**: `gcloud config get-value project` + `gcloud auth list`
- **Azure**: `az account show` + `az aks list`
- **AWS**: `aws sts get-caller-identity` + `aws eks list-clusters`

Confirm the active project/subscription/account matches the user's target.

### 3b. Kubernetes Cluster

```
// turbo
kubectl config current-context
kubectl cluster-info
```

Also run platform-specific cluster list command from `cloud-platforms` skill to verify cluster status.

**Record**: Cluster name, location, version, node count, current kubectl context.

## 4. Collect Production Snapshot

Run the following **read-only** diagnostic commands. Present results as a structured summary.

### 4a. Node Health

```
// turbo
kubectl get nodes -o wide
kubectl top nodes
```

**Flag**: Nodes in `NotReady` state, high CPU/memory utilization (>80%), version skew between nodes.

### 4b. Pod Status

For the affected namespace (or all namespaces if unspecified):

```
// turbo
kubectl get pods -n <namespace> -o wide --sort-by='.status.startTime'
kubectl get pods -n <namespace> --field-selector=status.phase!=Running
```

**Flag**:
- Pods in `CrashLoopBackOff`, `Error`, `Pending`, `ImagePullBackOff`
- Pods with high restart counts (>3 in last hour)
- Pods not matching expected replica count (check `kubectl get deployments`)

### 4c. Pod Details (for problematic pods)

```
kubectl describe pod <pod-name> -n <namespace>
kubectl logs --tail=200 --timestamps <pod-name> -n <namespace>
kubectl logs --previous --tail=50 <pod-name> -n <namespace>
```

**Look for**: OOMKilled (exit code 137), application exceptions, connection errors, startup failures, readiness probe failures.

### 4d. Resource Usage

```
// turbo
kubectl top pods -n <namespace> --sort-by=memory
kubectl get hpa -n <namespace>
```

**Flag**: Pods near memory limits, HPA at max replicas, CPU throttling.

### 4e. Managed Database Health

Run platform-specific database diagnostic commands from `cloud-platforms` skill:
- **GCP**: `gcloud sql instances list` + `gcloud sql instances describe`
- **Azure**: `az postgres flexible-server show` or `az sql server list`
- **AWS**: `aws rds describe-db-instances`

**Key metrics** (from cloud monitoring or CLI):
- CPU utilization, memory utilization, disk usage
- Active connections vs max connections
- Replication lag (if HA/read replicas)
- Failed connections count

### 4f. Networking and Ingress

```
// turbo
kubectl get ingress -n <namespace>
kubectl get svc -n <namespace>
kubectl get endpoints -n <namespace>
```

**Flag**: Services with 0 endpoints (no healthy backends), Ingress with no address, port mismatches.

### 4g. Recent Events

```
// turbo
kubectl get events -n <namespace> --sort-by='.lastTimestamp' --field-selector type!=Normal
```

**Record**: Warning/Error events — especially `FailedScheduling`, `OOMKilled`, `FailedMount`, `Unhealthy`, `BackOff`.

### 4h. Cloud Monitoring (if available)

Run platform-specific monitoring commands from `cloud-platforms` skill to list dashboards and check metrics.

Guide the user to check relevant dashboards for:
- **SLI metrics**: Error rate, latency (p50/p95/p99), availability
- **Error budget burn rate**: Is the SLO at risk?
- **Alerting policies**: Which alerts fired?

## 5. Analyze Findings

Using the applied role's expertise:

1. **Correlate** the user's problem with collected data
2. **Identify root cause** using the role's debugging methodology
3. **Assess SLO impact** (if `Agent(sre-engineer)` active): error budget consumed, burn rate

<common_prod_issues>
- **Pod CrashLoopBackOff**: OOM (check limits), app startup failure (check logs), missing config/secret, failed dependency (DB not reachable)
- **High latency**: Database slow queries, connection pool exhaustion, CPU throttling (check requests vs limits), upstream dependency timeout
- **Managed DB connection exhaustion**: Too many connections from pods, connection leak in app, pool size misconfigured, proxy/pooler not configured
- **Pods Pending**: Insufficient cluster resources (node autoscaler max reached), node affinity/taint mismatch, PVC not bound
- **5xx errors**: Application exception (check logs), upstream timeout, readiness probe failing (traffic to unhealthy pod), resource exhaustion
- **Deployment stuck**: Image pull error (wrong tag, registry auth), failed readiness probe, PDB blocking rollout, insufficient quota
- **Network unreachable**: NetworkPolicy blocking traffic, service selector mismatch, DNS resolution failure, VPC/firewall rule
</common_prod_issues>

## 6. Present Diagnosis

Structure the diagnosis:

```
## Production Environment Summary
- Cloud: [GCP/Azure/AWS] | Project/Sub/Account: [id] | Cluster: [name] ([location])
- Nodes: [count] ([healthy]/[total]) | K8s version: [version]
- Managed DB: [instance] ([state], [tier])

## SLO Impact (if applicable)
- SLO: [target] | Current: [actual] | Error budget: [remaining]%
- Burn rate: [Nx] | Time to budget exhaustion: [duration]

## Findings
### [Issue 1: title]
- **Symptom**: what was observed
- **Evidence**: specific log lines, metrics, pod status
- **Root cause**: why it's happening
- **Severity**: P1 (outage) / P2 (degraded) / P3 (minor) / P4 (cosmetic)
- **Blast radius**: affected users, services, regions

## Recommendations
1. [Immediate mitigation] — [command] ⚠️ REQUIRES APPROVAL
2. [Root cause fix] — [change description]
3. [Prevention] — [long-term improvement]

## Environment Health: [HEALTHY | DEGRADED | OUTAGE]
```

## 7. Fix or Escalate

**⚠️ All production mutations require explicit user approval.**

Based on the diagnosis:

- **Immediate mitigation** (rollback, restart, scale): Present the exact command. Wait for user approval. Execute and verify
- **Application code fix**: Transition to stack-specific role. Fix code, test locally (optionally `/analyze-local`), then deploy through normal CI/CD
- **Infrastructure fix** (Terraform, Helm, K8s config): Apply with `Agent(devops-engineer)` patterns via PR, never direct apply
- **Root cause unclear**: Propose additional diagnostics (increase log verbosity, tracing, profiling, query analysis)

After any fix, re-run relevant diagnostic commands from Step 4 to verify resolution.

## 8. Summary

Present the completed analysis:

- **Problem**: original report / incident ID
- **Severity**: P1–P4
- **Role(s) applied**: which roles were used
- **Root cause**: what was found
- **SLO impact**: error budget consumed
- **Fix applied**: what was changed (or "investigation only — no fix applied")
- **Verification**: confirmation the issue is resolved
- **Action items**: postmortem (if P1/P2), prevention measures, monitoring improvements

## Integration

- **Called by**: `/bugfix` (production environment diagnostics)
- **Roles**: `Agent(sre-engineer)`, `Agent(devops-engineer)`
- **Skills**: `cloud-platforms` skill (platform-specific CLI commands, managed service diagnostics)
