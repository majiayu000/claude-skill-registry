---
name: kubernetes-health
description: Comprehensive Kubernetes cluster health diagnostics using dynamic API discovery. Use when checking cluster health, troubleshooting K8s issues, or running health assessments.
allowed-tools: Read, Grep, Glob, Bash, Task
---

# Kubernetes Health Diagnostics

> Dynamic, discovery-driven health checks for any Kubernetes cluster configuration

## BEFORE YOU START

| Impact | Value |
|--------|-------|
| Token Savings | ~70% vs manual kubectl exploration |
| Setup Time | 0 min (uses existing kubectl config) |
| Coverage | Adapts to installed operators automatically |

### Known Issues Prevented

| Problem | Root Cause | How This Skill Helps |
|---------|------------|---------------------|
| Missing operator health | Static checklists miss CRDs | Dynamic API discovery detects all installed operators |
| Stale diagnostics | Manual checks become outdated | Real-time cluster API interrogation |
| Incomplete coverage | Unknown cluster configuration | Automatically activates relevant sub-agents |

## Quick Start

1. **Verify cluster access**: Ensure `kubectl` is configured and can reach your cluster
2. **Run discovery**: Execute `discover_apis.py` to detect installed operators
3. **Dispatch agents**: Use the orchestrator to run health checks based on discovery

```bash
# Step 1: Verify kubectl context
kubectl config current-context
kubectl cluster-info

# Step 2: Run API discovery
uv run .claude/skills/kubernetes-health/scripts/discover_apis.py

# Step 3: Review detected operators and dispatch health agents
```

## Critical Rules

### Always

- Verify kubectl context before running health checks
- Use read-only kubectl commands (get, describe, logs)
- Run core health checks before operator-specific checks
- Aggregate results using the provided scoring methodology

### Never

- Modify cluster resources during health checks
- Expose secret values in health reports (metadata only)
- Skip context verification for production clusters
- Assume operator presence without API discovery

### Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Hardcoding operator checks | Misses installed operators, checks missing ones | Use API discovery to detect what's installed |
| Sequential agent dispatch | Slow for multi-operator clusters | Run operator agents in parallel (same priority) |
| Raw kubectl output | Token inefficient, hard to parse | Use scripts for condensed JSON output |

## Bundled Resources

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/discover_apis.py` | Discovers all API groups and detects installed operators |
| `scripts/health_orchestrator.py` | Maps discovered APIs to specialized health agents |
| `scripts/aggregate_report.py` | Aggregates multi-agent results into unified report |

### References

| File | Contents |
|------|----------|
| `references/operator-checks.md` | Detailed health checks for each supported operator |
| `references/health-scoring.md` | Scoring methodology and weight assignments |

### Templates

| File | Purpose |
|------|---------|
| `templates/health-report.json` | JSON schema for health report output |

## Dependencies

### Required

| Package | Version | Purpose |
|---------|---------|---------|
| kubectl | Latest | Cluster interaction |
| Python | >= 3.11 | Script execution |
| uv | Latest | Python script runner |

### Optional

| Package | Version | Purpose |
|---------|---------|---------|
| kubernetes | >= 28.1.0 | Python client (for advanced discovery) |

## Supported Operators

The skill automatically detects and dispatches specialized agents for:

| Operator | API Group | Agent |
|----------|-----------|-------|
| Core K8s | (always) | k8s-core-health-agent |
| Crossplane | crossplane.io | k8s-crossplane-health-agent |
| ArgoCD | argoproj.io | k8s-argocd-health-agent |
| Cert-Manager | cert-manager.io | k8s-certmanager-health-agent |
| Prometheus | monitoring.coreos.com | k8s-prometheus-health-agent |

## Health Scoring

| Status | Score Range | Criteria |
|--------|-------------|----------|
| HEALTHY | 90-100 | All checks pass, no warnings |
| DEGRADED | 60-89 | Some warnings, no critical issues |
| CRITICAL | 0-59 | Critical issues affecting availability |

## Troubleshooting

### kubectl connection issues

```bash
# Verify context
kubectl config current-context

# Test connectivity
kubectl cluster-info

# Check permissions
kubectl auth can-i get pods --all-namespaces
```

### Discovery returns empty results

- Ensure cluster is reachable
- Check RBAC permissions for API discovery
- Verify kubectl version compatibility

### Agent dispatch failures

- Confirm discovered API group matches agent trigger
- Check agent file exists in `.claude/agents/specialized/kubernetes/`
- Review agent tool restrictions

## Setup Checklist

- [ ] kubectl configured and connected to cluster
- [ ] Python 3.11+ installed
- [ ] uv installed for script execution
- [ ] Read permissions on cluster resources
- [ ] Agent files present in `.claude/agents/specialized/kubernetes/`
