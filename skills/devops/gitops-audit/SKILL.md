---
name: gitops-audit
description: Comprehensive GitOps compliance verification that detects configuration drift and policy violations through three audit types - (1) Cluster Drift (resources in cluster not tracked in git), (2) Spec Drift (differences between git manifests and cluster state), (3) Code Violations (hardcoded Kubernetes configs in application code). Automatically triggered when code review detects changes to *.yaml/*.yml in charts/, manifests/, k8s/, kubernetes/, deployment scripts, Helm charts, Kustomize files, or Kubernetes client library imports. Use manually for investigating cluster drift, auditing GitOps compliance, before production deployments, troubleshooting sync issues, or regular compliance checks.
---

# GitOps Audit Skill

## Quick Start

GitOps audit verifies that your cluster state matches your git state by running three checks:

1. **Cluster Drift**: Find resources in cluster that aren't in git
2. **Spec Drift**: Find differences between git manifests and live cluster state
3. **Code Violations**: Find hardcoded Kubernetes configs in application code

**Run the audit:**

```bash
/gitops-audit
```

**Expected flow:**

1. Skill detects GitOps repository location
2. Runs three audit checks in parallel
3. Generates comprehensive report with severity levels (CRITICAL, WARNING, INFO)
4. Provides remediation steps

---

## When to Load Additional References

The core workflow below is sufficient for most audits. Load these references for detailed patterns and troubleshooting:

**For detailed drift patterns and examples:**

```
Read `~/.claude/skills/gitops-audit/references/DRIFT-PATTERNS.md`
```

Use when: You need detailed examples of what each audit type detects, or want to understand specific drift patterns

**For configuration and resource handling:**

```
Read `~/.claude/skills/gitops-audit/references/KUBERNETES-RESOURCES.md`
```

Use when: Setting up configuration, handling CRDs/operators, or understanding exclusion patterns

**For troubleshooting and edge cases:**

```
Read `~/.claude/skills/gitops-audit/references/TROUBLESHOOTING.md`
```

Use when: Encountering issues, dealing with false positives, or handling special cases (HPA, operators, multi-cluster)

---

## Core Workflow

### Step 1: Detect GitOps Repository

**Automatic detection methods:**

- Check environment variable: `GITOPS_REPO_PATH`
- Search common locations: `~/gitops-repo`, `~/projects/gitops`, `~/k8s-manifests`
- Parse git remotes: `git remote -v | grep -E "(gitops|k8s|kubernetes|manifests)"`

**Ask user if not found:**

```
GitOps repository not automatically detected.

Please provide the path to your GitOps repository:
- Local path: /path/to/gitops-repo
- Or I can clone it: git@github.com:org/gitops-repo.git
```

**Detect repository structure:**

- **Helm**: Check for `charts/` directory
- **Kustomize**: Check for `kustomization.yaml` or `base/` directory
- **Plain YAML**: Check for `manifests/` or `k8s/` directory

---

### Step 2: Run Cluster Drift Check

**Objective:** Find resources in cluster that don't exist in git

**Process:**

```bash
# Get all resources in namespace
RESOURCES=$(kubectl api-resources --verbs=list --namespaced -o name | \
  xargs -n 1 kubectl get --show-kind --ignore-not-found -o name -n $NAMESPACE)

# For each resource
for RESOURCE in $RESOURCES; do
  KIND=$(echo $RESOURCE | cut -d'/' -f1)
  NAME=$(echo $RESOURCE | cut -d'/' -f2)

  # Search git for manifest
  FOUND=$(find $GITOPS_REPO -name "*.yaml" -o -name "*.yml" | \
    xargs grep -l "kind: $KIND" | \
    xargs grep -l "name: $NAME")

  if [ -z "$FOUND" ]; then
    echo "DRIFT: $RESOURCE not in git"
  fi
done
```

**Report format:**

```
🚨 CRITICAL: Resources in cluster NOT tracked in git

Namespace: production
- Deployment/debug-pod (created manually, age: 2 days)
  Action: Delete OR add manifest to gitops-repo/production/

- ConfigMap/temp-config (no manifest found, age: 5 hours)
  Action: Delete OR formalize in charts/app/config/
```

---

### Step 3: Run Spec Drift Analysis

**Objective:** Find differences between git manifests and live cluster state

**Process:**

```bash
# Render manifest from git
if [ "$TYPE" = "helm" ]; then
  RENDERED=$(helm template $CHART -f $VALUES_FILE)
elif [ "$TYPE" = "kustomize" ]; then
  RENDERED=$(kustomize build $PATH)
else
  RENDERED=$(cat $MANIFEST)
fi

# Get live resource
LIVE=$(kubectl get $KIND $NAME -n $NAMESPACE -o yaml)

# Diff them
DIFF=$(kubectl diff -f <(echo "$RENDERED") 2>&1)

if [ -n "$DIFF" ]; then
  echo "SPEC DRIFT: $KIND/$NAME"
fi
```

**Report format:**

```
⚠️  WARNING: Spec drift detected (git ≠ cluster)

Deployment/api-service (production):
  Git: replicas=3
  Cluster: replicas=5 (DRIFT)
  Action: Reconcile via gitops-apply skill

ConfigMap/app-config (staging):
  Git: LOG_LEVEL=info
  Cluster: LOG_LEVEL=debug (DRIFT)
  Action: Update git OR revert cluster
```

---

### Step 4: Run Code Violations Scan

**Objective:** Find hardcoded Kubernetes configs in application code

**Process:**

```bash
# Scan for inline YAML
grep -r -E "(apiVersion|kind:.*Deployment|kind:.*Service)" \
  --include="*.py" --include="*.go" --include="*.js" --include="*.ts" \
  --include="*.sh" --exclude-dir=tests --exclude-dir=node_modules

# Scan for kubectl commands
grep -r -E "kubectl\s+(apply|create|delete|patch|edit)" \
  --include="*.sh" --include="*.py" --include="*.js" --include="*.go" \
  --exclude-dir=tests

# Scan for hardcoded resource creation (Go)
grep -r -E "(CreateDeployment|CreateService|client\.Create\()" \
  --include="*.go" --exclude-dir=vendor

# Scan for hardcoded resource creation (Python)
grep -r -E "(create_namespaced_deployment|create_namespaced_service)" \
  --include="*.py"
```

**Report format:**

```
❌ CRITICAL: Hardcoded Kubernetes configs in application code

scripts/deploy.sh:45
  kubectl apply -f - <<EOF
    apiVersion: apps/v1
    kind: Deployment
    ...
  EOF

  Issue: Inline YAML in deployment script
  Action: Move to GitOps repo → charts/my-app/templates/deployment.yaml
```

---

### Step 5: Generate Comprehensive Report

**Report structure:**

```markdown
# GitOps Audit Report

**Status:** ❌ FAILED (3 CRITICAL, 5 WARNING issues)
**Date:** 2024-01-16 14:30:25 UTC
**Repository:** /home/user/gitops-repo
**Namespaces Audited:** production, staging

## Summary

| Check           | Status  | Critical | Warning | Info  |
| --------------- | ------- | -------- | ------- | ----- |
| Cluster drift   | ❌ FAIL | 2        | 0       | 0     |
| Spec drift      | ⚠️ WARN | 0        | 5       | 0     |
| Code violations | ❌ FAIL | 1        | 1       | 1     |
| **TOTAL**       | ❌ FAIL | **3**    | **6**   | **1** |

---

## 🚨 CRITICAL Issues (Must Fix)

[Detailed findings...]

## ⚠️ WARNING Issues (Should Fix)

[Detailed findings...]

## ℹ️ INFO Issues (Informational)

[Documented exceptions, test fixtures...]

---

## Remediation Steps

**Immediate Actions (CRITICAL - Do Today):**

- Delete or formalize debug-pod
- Refactor deploy.sh to use GitOps

**Recommended Actions (WARNING - This Week):**

- Reconcile all spec drift
- Document manual changes

**Prevention (Ongoing):**

- Enable kubectl mutation blocking hook
- Run weekly drift audits
- Monitor ArgoCD sync status
```

---

## Configuration

### Essential Configuration

```yaml
# Namespaces to audit (auto-detected if not specified)
namespaces:
  - production
  - staging
  - dev

# GitOps repository (auto-detected if not specified)
gitops_repos:
  - path: /path/to/gitops-repo
    type: helm # helm | kustomize | plain-yaml

# System namespace exclusions (default)
exclude_namespaces:
  - kube-system
  - kube-public
  - kube-node-lease
  - argocd
  - flux-system

# Ephemeral resource exclusions (default)
exclude_resource_types:
  - Event
  - EndpointSlice
  - Lease
  - Pod
  - ReplicaSet
```

**For detailed configuration options, read** `references/KUBERNETES-RESOURCES.md`

---

## Severity Classification

### CRITICAL (Block Commit/PR)

**Must be fixed immediately:**

- Resources in cluster not tracked in git
- Hardcoded kubectl mutations in production code
- Inline Kubernetes YAML in application code (not tests)
- Secrets not encrypted in git

**Why:** Breaks GitOps single source of truth, prevents rollback, no audit trail

### WARNING (Report But Don't Block)

**Should be fixed soon:**

- Spec drift (minor differences between git and cluster)
- Missing resource requests/limits
- ConfigMap/Secret content drift
- Hardcoded resources in operator code (verify it's an operator)

**Why:** Doesn't break GitOps entirely, may be temporary, has valid exceptions

### INFO (Informational)

**No action required:**

- Resources in git not deployed to cluster (expected if feature-flagged)
- Test fixture resources
- kubectl commands in test code
- Properly documented exceptions

**Why:** Expected behavior, documented exceptions, no compliance risk

---

## Integration with Other Skills

### Automatic Invocation

**Code Review Integration:**

When code review detects Kubernetes-related changes, this skill runs automatically:

- Changes to `*.yaml`, `*.yml` in `charts/`, `manifests/`, `k8s/`, `kubernetes/`
- Changes to `values*.yaml`, `Chart.yaml`, `kustomization.yaml`
- Kubernetes client library imports (Go, Python, Node.js, TypeScript)

### create-pr Skill Integration

**Before creating PR:**

- Run gitops-audit
- Block PR creation if CRITICAL issues found
- Include WARNING issues in PR description
- Proceed if clean

### gitops-apply Skill Integration

**After applying changes:**

- Modify manifest → Commit → Push to git
- Wait for ArgoCD/Flux sync
- Run gitops-audit to verify cluster state matches git

---

## Dependencies

### Required Tools

- **kubectl** - Cluster access (REQUIRED)
- **git** - GitOps repository access (REQUIRED)

### Optional Tools (Enhanced Functionality)

- **helm** - For Helm-based GitOps repos
- **kustomize** - For Kustomize-based repos
- **yq** or **jq** - YAML/JSON parsing
- **argocd** CLI - For ArgoCD integration
- **flux** CLI - For Flux integration

**Fallback strategies:**

- If helm not available: Parse Chart.yaml and values.yaml as plain YAML
- If yq/jq not available: Use grep/awk for basic field extraction
- If ArgoCD CLI not available: Use kubectl to check Applications

---

## Best Practices

### 1. Run Regularly

- **Production:** Weekly (automated)
- **Staging:** Daily (automated)
- **Development:** On-demand
- **Before Production Deploy:** Always

### 2. Act on CRITICAL Issues Immediately

CRITICAL issues must be resolved before:

- Merging PRs
- Deploying to production
- Closing sprint/iteration

### 3. Document Exceptions

If allowing spec drift or hardcoded resources:

```yaml
allowed_exceptions:
  - resource: "Deployment/feature-flag-service"
    namespace: "production"
    field: "replicas"
    reason: "Auto-scaled by HPA, drift expected"
    reviewed: "2024-01-15"
```

### 4. Monitor ArgoCD/Flux Sync Status

Complement audit with sync monitoring:

- Check ArgoCD dashboard regularly
- Set up Slack/email alerts for OutOfSync
- Review sync history for patterns

---

## Related Skills

- **gitops-apply**: Apply changes via GitOps workflow (use instead of kubectl)
- **helm-chart-writing**: Create Helm charts for GitOps
- **helm-argocd-gitops**: Configure ArgoCD Applications
- **safe-commit**: Commit GitOps manifest changes safely
- **create-pr**: Create PRs for GitOps changes

---

## Emergency Override

If user explicitly states "I acknowledge these drift findings":

1. Document the acknowledgment
2. Include findings in PR description
3. Create follow-up tickets for remediation
4. Set reminders for cleanup

**This should be RARE - GitOps compliance is not optional.**
