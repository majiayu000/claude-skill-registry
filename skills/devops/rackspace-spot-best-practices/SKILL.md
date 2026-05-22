---
name: rackspace-spot-best-practices
description: Best practices for running GitHub Actions ARC runners on Rackspace Spot Kubernetes. Covers spot instance management, preemption handling, cost optimization, and resilience strategies. Activates on "rackspace spot", "spot instances", "preemption", "cost optimization", or "spot interruption".
allowed-tools: Read, Grep, Glob, Bash
---

# Rackspace Spot Best Practices for ARC Runners

## Overview

This guide covers best practices for running GitHub Actions ARC (Actions Runner Controller) runners on Rackspace Spot Kubernetes. Rackspace Spot is a managed Kubernetes platform that leverages spot pricing through a unique auction-based marketplace.

## What is Rackspace Spot?

Rackspace Spot is the world's only open market auction for cloud servers, delivered as turnkey, fully managed Kubernetes clusters.

### Key Differentiators from AWS/GCP/Azure Spot

| Feature | Rackspace Spot | AWS EC2 Spot | Other Cloud Spot |
|---------|----------------|--------------|------------------|
| Pricing Model | True market auction | AWS-controlled floor price | Provider-controlled |
| Cost Savings | Up to 90%+ | 50-90% | 50-90% |
| Control Plane | Free (included) | $72/month (EKS) | $70-150/month |
| Interruption Notice | Managed transparently | 2 minutes | 2-30 seconds (varies) |
| Management | Fully managed K8s | Self-managed | Self-managed or managed |
| Lock-in | Multi-cloud capable | AWS-specific | Cloud-specific |
| Min Cluster Cost | $0.72/month | Much higher | Much higher |

### Rackspace Spot Architecture

```
GitHub Actions
      ↓
ARC (Actions Runner Controller)
      ↓
Kubernetes Cluster (Rackspace Spot)
      ↓
Spot Instance Pool (Auction-based)
      ↓
Rackspace Global Datacenters
```

**Key Features:**
- Cluster-API based Kubernetes control plane (deployed and managed)
- Auto-scaling node pools
- Terraform provider for IaC
- Persistent storage with transparent migration
- Built-in storage classes (SSD, SATA)
- Calico CNI with network policies
- Built-in load balancers

## Cost Optimization

### Understanding Rackspace Spot Pricing

**Market-Driven Auction:**
- Bid on compute capacity based on real-time supply and demand
- Visibility into market prices and capacity levels
- Even if you overbid, you only pay the market price
- Prices slide with the market automatically

**ROI Examples:**

| Configuration | Rackspace Spot Cost | AWS EKS Equivalent | Savings |
|---------------|---------------------|-------------------|---------|
| Control Plane | $0 (included) | $72/month | 100% |
| 2 t3.medium runners (24/7) | ~$15-30/month | ~$100-150/month | 75-85% |
| 5 t3.large runners (24/7) | ~$50-80/month | ~$300-400/month | 75-85% |
| Full ARC setup (2 min + scale to 20) | ~$150-300/month | ~$800-1200/month | 75-80% |

### Bidding Strategy for CI/CD Runners

**Best Practice Bidding:**

1. **Analyze Historical Capacity:**
   - View market prices in Rackspace Spot console
   - Check available capacity at different price points
   - Set bids based on predictable patterns

2. **Set Safe Bid Thresholds:**
   ```
   Conservative: Set bid at 50% of on-demand equivalent
   Balanced: Set bid at 70% of on-demand equivalent
   Aggressive: Set bid at 90% of on-demand equivalent
   ```

3. **Ensure Capacity Availability:**
   - Bid higher than floor to guarantee capacity
   - Even with high bids, you pay market price
   - For critical CI/CD, bid conservatively to avoid interruption

### Cost Optimization for ARC Runners

**minRunners Configuration:**

| Strategy | minRunners | Cost Impact | Use Case |
|----------|-----------|-------------|----------|
| Zero Idle Cost | 0 | $0 when idle, 2-5 min cold start | Low-traffic repos, dev |
| Fast Start | 2 | ~$15-30/month, <10 sec start | Production, active repos |
| Enterprise | 5 | ~$50-80/month, instant | High-volume CI/CD |

**Recommendation for ARC on Rackspace Spot:**
- **minRunners: 2** provides best balance of cost and performance
- Cold start penalty eliminated (120-300 sec → 5-10 sec)
- Developer time saved >> marginal runner cost
- Rackspace Spot pricing makes this affordable

**Cost Comparison Example:**

```
AWS EKS with minRunners: 2
- Control plane: $72/month
- 2 t3.medium spot: ~$30-50/month
- Total: ~$100-120/month

Rackspace Spot with minRunners: 2
- Control plane: $0/month (included)
- 2 equivalent runners: ~$15-30/month
- Total: ~$15-30/month

Savings: 75-85%
```

## Handling Spot Instance Preemption

### Understanding Preemption on Rackspace Spot

**Key Differences:**

Unlike AWS/GCP/Azure where spot instances can be terminated with 2 minutes notice:
- Rackspace Spot manages preemption transparently
- Persistent storage migrates automatically during spot server recycling
- Built for stateful applications, not just batch processing
- Focus is on availability rather than interruption warnings

**User Testimonials:**
> "Running Airflow in Spot with fault-tolerant Kubernetes components means preemption wasn't a concern" - OpsMx case study

### ARC-Specific Preemption Considerations

**The Challenge:**

GitHub Actions jobs don't fit typical Kubernetes workload patterns:
- Cannot be safely terminated mid-job
- Job is lost if pod terminated before completion
- Each job needs dedicated resources (concurrency: 1)
- ARC autoscaler constantly scales runners up/down

**Best Practices for ARC on Spot:**

#### 1. Use Pod Disruption Budgets (PDBs)

```yaml
# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: arc-runner-pdb
  namespace: arc-beta-runners-new
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app.kubernetes.io/component: runner
```

**Note:** PDBs protect against voluntary evictions (drains, upgrades) but NOT spot interruptions. However, Rackspace Spot's transparent migration may handle this better than traditional spot providers.

#### 2. Configure Do-Not-Disrupt Annotations (Karpenter)

If using Karpenter for node provisioning:

```yaml
# runner-template.yaml
apiVersion: v1
kind: Pod
metadata:
  name: runner
  annotations:
    karpenter.sh/do-not-disrupt: "true"
spec:
  # runner spec
```

**When this helps:**
- Prevents Karpenter from consolidating/evicting active runners
- Protects runners during cluster optimization
- Does NOT prevent cloud-level spot interruption

#### 3. Configure Tolerations for Spot Nodes

```yaml
# arc-runner-values.yaml
spec:
  template:
    spec:
      tolerations:
        - key: "spot"
          operator: "Equal"
          value: "true"
          effect: "NoSchedule"
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              preference:
                matchExpressions:
                  - key: "capacity-type"
                    operator: In
                    values:
                      - spot
```

**Benefits:**
- Runners explicitly tolerate spot nodes
- Can prefer spot over on-demand for cost savings
- Can require spot for guaranteed spot pricing

#### 4. Set Graceful Shutdown Timeouts

```yaml
# arc-runner-values.yaml
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 300  # 5 minutes
      containers:
        - name: runner
          env:
            - name: RUNNER_GRACEFUL_STOP_TIMEOUT
              value: "300"
```

**Limitations:**
- AWS spot: Only 2 minutes warning
- GCP spot: Only 30 seconds before force termination
- Rackspace Spot: Transparent migration may make this less critical

#### 5. Diversify Node Pools

**Strategy: Mix of instance types**

```yaml
# Multiple instance types for availability
nodeSelector:
  node.kubernetes.io/instance-type: "t3.medium,t3a.medium,t2.medium"
```

**Benefits:**
- Reduces likelihood of capacity exhaustion
- If one instance type unavailable, others can scale
- Increases overall availability
- Lower interruption rate

### Rackspace Spot Advantages for ARC

**Why Rackspace Spot is Better for CI/CD:**

1. **Transparent Migration:**
   - Persistent storage migrates even if spot server recycled
   - Less disruptive than AWS 2-minute termination
   - Better for stateful workloads like CI/CD runners

2. **Managed Kubernetes:**
   - Control plane managed for you
   - Auto-healing built-in
   - Less operational overhead

3. **Auction Model:**
   - More predictable capacity
   - Can view availability before bidding
   - Less sudden interruptions

4. **Cost Efficiency:**
   - Free control plane saves $72/month minimum
   - True auction pricing (not artificial floor)
   - Can run persistent workloads affordably

## Resilience Strategies

### 1. Mixed On-Demand/Spot Strategy

**When to Use:**
- Critical production workloads
- Jobs that cannot tolerate interruption
- Compliance/regulatory requirements

**Implementation:**

```yaml
# Create separate runner scale sets
---
# Spot runners (most jobs)
apiVersion: actions.summerwind.dev/v1alpha1
kind: RunnerDeployment
metadata:
  name: spot-runners
spec:
  replicas: 2-20
  template:
    spec:
      nodeSelector:
        capacity-type: spot
      labels:
        - "self-hosted"
        - "linux"
        - "spot"

---
# On-demand runners (critical jobs)
apiVersion: actions.summerwind.dev/v1alpha1
kind: RunnerDeployment
metadata:
  name: ondemand-runners
spec:
  replicas: 0-5
  template:
    spec:
      nodeSelector:
        capacity-type: on-demand
      labels:
        - "self-hosted"
        - "linux"
        - "on-demand"
```

**Workflow Usage:**

```yaml
# .github/workflows/deploy-production.yml
jobs:
  build:
    runs-on: [self-hosted, linux, spot]  # Cost-effective

  deploy-production:
    runs-on: [self-hosted, linux, on-demand]  # Reliable
```

### 2. Topology Spread Constraints

**Spread pods across failure domains:**

```yaml
spec:
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: ScheduleAnyway
      labelSelector:
        matchLabels:
          app.kubernetes.io/component: runner
```

**Benefits:**
- Prevents all runners in single availability zone
- If one zone loses capacity, others continue
- Increases overall availability

### 3. Namespace Isolation

**Best Practice: Separate namespaces for isolation**

```
arc-systems                 → ARC controllers
arc-beta-runners-new        → Org-level runners
arc-frontend-runners        → Frontend-specific
arc-api-runners             → API-specific
```

**Benefits:**
- Resource quotas per namespace
- Network policies for security
- Blast radius containment
- Independent scaling

### 4. Resource Quotas and Limits

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: runner-quota
  namespace: arc-beta-runners-new
spec:
  hard:
    requests.cpu: "40"
    requests.memory: "80Gi"
    pods: "25"
```

**Prevents:**
- Runaway scaling
- Resource exhaustion
- Cost overruns

## Monitoring and Observability

### Key Metrics for Spot Runners

**1. Runner Availability:**
```bash
# Check available runners
kubectl get pods -n arc-beta-runners-new -l app.kubernetes.io/component=runner

# Check scaling events
kubectl get events -n arc-beta-runners-new --sort-by='.lastTimestamp' | grep -i scale
```

**2. Spot Interruptions:**
```bash
# Track pod evictions/terminations
kubectl get events -A --field-selector reason=Evicted

# Check node status
kubectl get nodes -o wide | grep -i spot
```

**3. Job Queue Times:**
```bash
# GitHub Actions queue times
gh run list --repo Matchpoint-AI/project-beta-api --status queued --json createdAt,name

# Calculate average queue time
gh run list --json createdAt,startedAt,conclusion --jq '.[] | select(.conclusion != null) | (.startedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)'
```

**4. Cost Tracking:**
```bash
# Via Rackspace Spot console
# - View real-time billing
# - Track instance hours
# - Compare bid vs actual prices paid
```

### Alert Thresholds

| Metric | Normal | Warning | Critical | Action |
|--------|--------|---------|----------|--------|
| Avg Queue Time | <30s | 30-120s | >120s | Check minRunners, scaling |
| Available Runners | 2+ | 1 | 0 | Scale up, check capacity |
| Pod Restart Rate | <1/day | 1-5/day | >5/day | Investigate interruptions |
| Failed Jobs % | <2% | 2-5% | >5% | Check resource limits, OOM |
| Spot Interruptions | 0-2/week | 2-5/week | >5/week | Review bid strategy, diversify |

## Configuration Best Practices

### Helm Values Structure

```yaml
# examples/beta-runners-values.yaml
githubConfigUrl: "https://github.com/Matchpoint-AI"
githubConfigSecret: arc-runner-token

minRunners: 2              # Keep 2 pre-warmed (RECOMMENDED for Rackspace Spot)
maxRunners: 20             # Scale to 20 for parallel jobs

runnerGroup: "default"

template:
  spec:
    containers:
      - name: runner
        image: summerwind/actions-runner:latest
        resources:
          limits:
            cpu: "2"
            memory: "4Gi"
          requests:
            cpu: "1"
            memory: "2Gi"

    # Spot tolerations
    tolerations:
      - key: "spot"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"

    # Node affinity for spot
    affinity:
      nodeAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            preference:
              matchExpressions:
                - key: "capacity-type"
                  operator: In
                  values:
                    - spot

    # Graceful shutdown
    terminationGracePeriodSeconds: 300
```

### Terraform Configuration

```hcl
# terraform/main.tf
module "cloudspace" {
  source = "./modules/cloudspace"

  name              = "matchpoint-runners-prod"
  region            = "us-east-1"
  kubernetes_version = "1.28"

  # Spot configuration
  node_pools = {
    spot_runners = {
      instance_type  = "t3.medium"
      capacity_type  = "spot"
      min_size       = 2
      max_size       = 20
      spot_max_price = "0.05"  # Bid price
    }
  }
}

# Get kubeconfig from spot provider
data "spot_kubeconfig" "runners" {
  cloudspace_id = module.cloudspace.cloudspace_id
}

output "kubeconfig_raw" {
  value     = data.spot_kubeconfig.runners.raw
  sensitive = true
}
```

**Getting Kubeconfig:**

```bash
# Always get fresh kubeconfig from terraform
export TF_HTTP_PASSWORD="<github-token>"
cd matchpoint-github-runners-helm/terraform
terraform init
terraform output -raw kubeconfig_raw > /tmp/runners-kubeconfig.yaml
export KUBECONFIG=/tmp/runners-kubeconfig.yaml
kubectl get pods -A
```

## Critical Configuration Issues

### ArgoCD releaseName vs runnerScaleSetName Mismatch (P0)

**Issue #112 Root Cause (Dec 12, 2025)**

When ArgoCD `releaseName` doesn't match `runnerScaleSetName` in values files, runners register with **empty labels**, causing all CI jobs to queue indefinitely.

**Symptoms:**
```json
{"labels":[],"name":"arc-beta-runners-xxxxx","os":"unknown","status":"offline"}
```

**Root Cause:**
- ArgoCD tracks Helm resources under `releaseName`
- ARC creates AutoscalingRunnerSet with `runnerScaleSetName`
- When mismatched, resource tracking breaks → broken registration → empty labels

**CRITICAL: These MUST match:**
```yaml
# argocd/apps-live/arc-runners.yaml
helm:
  releaseName: arc-beta-runners  # MUST match runnerScaleSetName!

# examples/runners-values.yaml
gha-runner-scale-set:
  runnerScaleSetName: "arc-beta-runners"  # MUST match releaseName!
```

**CI Validation Added:**
- `scripts/validate-release-names.sh` - Validates alignment
- `.github/workflows/validate.yaml` - Runs on PRs to prevent recurrence

**Diagnosis:**
```bash
# Check runner labels
gh api /orgs/Matchpoint-AI/actions/runners --jq '.runners[] | {name, labels: [.labels[].name], os}'

# Run validation script
cd matchpoint-github-runners-helm
./scripts/validate-release-names.sh
```

**Fix:**
1. Align `releaseName` in ArgoCD Application with `runnerScaleSetName` in values
2. Update `ignoreDifferences` secret name (format: `{releaseName}-gha-rs-github-secret`)
3. Merge and wait for ArgoCD sync
4. Runners will re-register with proper labels

**Related Issues:** #89, #91, #93, #97, #98, #112, #113

---

## Troubleshooting Spot-Specific Issues

### Issue: High Spot Interruption Rate

**Symptoms:**
- Frequent pod restarts
- Jobs failing mid-execution
- "Node not found" errors

**Diagnosis:**
```bash
# Check pod restart counts
kubectl get pods -n arc-beta-runners-new -o json | jq '.items[] | {name: .metadata.name, restarts: .status.containerStatuses[0].restartCount}'

# Check node events
kubectl get events -A --field-selector involvedObject.kind=Node | grep -i "spot"
```

**Solutions:**
1. Increase spot bid price (more headroom)
2. Diversify instance types
3. Add on-demand pool for critical jobs
4. Review capacity availability in Rackspace console

### Issue: Spot Capacity Unavailable

**Symptoms:**
- Pods stuck in "Pending" state
- "Insufficient spot capacity" events
- Jobs queued but not starting

**Diagnosis:**
```bash
# Check pending pods
kubectl get pods -n arc-beta-runners-new -o wide | grep Pending

# Check node status
kubectl describe node <node-name>
```

**Solutions:**
1. Increase spot bid in Rackspace console
2. Add multiple instance types to node pool
3. Temporarily use on-demand capacity
4. Check Rackspace Spot marketplace for capacity

### Issue: Transparent Migration Failing

**Symptoms:**
- Runner job fails during execution
- Storage not accessible
- Pod crash loops

**Diagnosis:**
```bash
# Check persistent volumes
kubectl get pv,pvc -A

# Check pod events
kubectl describe pod <pod-name> -n arc-beta-runners-new
```

**Solutions:**
1. Verify storage class configuration
2. Check volume mount paths
3. Ensure PV reclaim policy is "Retain"
4. Contact Rackspace support (managed service)

## Security Best Practices

### 1. Isolate Runner Namespaces

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: arc-beta-runners-new
  labels:
    pod-security.kubernetes.io/enforce: restricted
```

### 2. Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: runner-network-policy
  namespace: arc-beta-runners-new
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/component: runner
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: TCP
          port: 443  # HTTPS only
```

### 3. Service Account Permissions

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: arc-runner
  namespace: arc-beta-runners-new
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: arc-runner
  namespace: arc-beta-runners-new
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]  # Minimal permissions
```

### 4. Secrets Management

```bash
# Use GitHub secrets for ARC token
kubectl create secret generic arc-runner-token \
  --from-literal=github_token=$GITHUB_TOKEN \
  -n arc-beta-runners-new

# Seal secrets for GitOps
kubeseal --format=yaml < secret.yaml > sealed-secret.yaml
```

## Migration Guide: AWS EKS → Rackspace Spot

### Pre-Migration Checklist

- [ ] Document current EKS configuration (node groups, instance types, scaling)
- [ ] Export ARC runner configurations (Helm values)
- [ ] Identify all GitHub repositories using self-hosted runners
- [ ] Calculate current costs (EKS control plane + spot instances)
- [ ] Determine downtime tolerance for migration

### Migration Steps

1. **Set up Rackspace Spot Cloudspace:**
   ```bash
   cd matchpoint-github-runners-helm/terraform
   terraform init
   terraform plan
   terraform apply
   ```

2. **Deploy ARC to Rackspace Spot:**
   ```bash
   # Get kubeconfig
   terraform output -raw kubeconfig_raw > /tmp/rs-kubeconfig.yaml
   export KUBECONFIG=/tmp/rs-kubeconfig.yaml

   # Deploy ARC controllers
   helm install arc-controller oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller \
     -n arc-systems --create-namespace

   # Deploy runner scale sets
   helm install arc-beta-runners ./charts/github-actions-runners \
     -n arc-beta-runners-new --create-namespace \
     -f examples/beta-runners-values.yaml
   ```

3. **Parallel Testing Period:**
   - Run both EKS and Rackspace Spot in parallel
   - Route 10% of jobs to new runners (using labels)
   - Monitor for 1-2 weeks
   - Verify cost savings and reliability

4. **Gradual Migration:**
   - Week 1: 25% of repos to Rackspace Spot
   - Week 2: 50% of repos
   - Week 3: 75% of repos
   - Week 4: 100%, decomission EKS

5. **Cost Validation:**
   ```
   Before (EKS):
   - Control plane: $72/month
   - Spot instances: ~$200/month
   - Total: ~$272/month

   After (Rackspace Spot):
   - Control plane: $0/month
   - Spot instances: ~$50/month
   - Total: ~$50/month

   Savings: ~$220/month (81%)
   ```

## References and Resources

### Documentation
- [Rackspace Spot Official Site](https://spot.rackspace.com)
- [ARC GitHub Repository](https://github.com/actions/actions-runner-controller)
- [ARC Documentation](https://docs.github.com/en/actions/concepts/runners/actions-runner-controller)

### Related Skills
- `/home/pselamy/repositories/project-beta-dev-workspace/.claude/skills/arc-runner-troubleshooting/SKILL.md` - ARC troubleshooting
- `/home/pselamy/repositories/project-beta-dev-workspace/.claude/skills/project-beta-infrastructure/SKILL.md` - Infrastructure patterns

### Case Studies
- [OpsMx + Rackspace Spot Case Study](https://spot.rackspace.com/case-studies/using-spot-instances-to-maximize-cloud-cost-efficiency-and-performance-opsmxs-experience) - 83% cost reduction

### Community Resources
- [WarpBuild ARC Setup Guide](https://www.warpbuild.com/blog/setup-actions-runner-controller)
- [AWS Best Practices for Self-Hosted Runners](https://aws.amazon.com/blogs/devops/best-practices-working-with-self-hosted-github-action-runners-at-scale-on-aws/)
- [Chargebee: Save Cost with Spot Instances](https://medium.com/chargebee-engineering/save-cost-by-running-github-actions-on-spot-instances-inside-an-eks-cluster-342f02ee2320)

## Kubeconfig Token Expiration (CRITICAL - Dec 13, 2025 Discovery)

### The Problem

Rackspace Spot kubeconfig JWT tokens expire after **3 days**. This causes:
- kubectl commands to fail with auth errors
- Misleading "no such host" DNS errors (actually token expiration)
- Agents unable to access cluster for diagnostics

### Verify Token Expiration

```bash
# Decode JWT to check when token expires
TOKEN=$(grep "token:" kubeconfig.yaml | head -1 | awk '{print $2}')
echo $TOKEN | cut -d. -f2 | base64 -d 2>/dev/null | python3 -c "
import json, sys
from datetime import datetime
payload = json.load(sys.stdin)
exp = datetime.fromtimestamp(payload['exp'])
print(f'Token expires: {exp}')
print(f'Expired: {datetime.now() > exp}')
"
```

### Solution: Scheduled Terraform Refresh

A GitHub Actions workflow (`refresh-kubeconfig.yml`) runs every 2 days to refresh the terraform state before the 3-day token expiration.

**How it works:**
1. Workflow runs `terraform refresh` with RACKSPACE_SPOT_API_TOKEN
2. Terraform's `data.spot_kubeconfig` fetches fresh token from Rackspace API
3. Fresh token stored in terraform state (tfstate.dev)
4. Users can get fresh kubeconfig via `terraform output`

**Reference:** Issue #135, PR #137

### Getting Fresh Kubeconfig

**Option A: From Terraform State (RECOMMENDED)**

The state is auto-refreshed every 2 days:

```bash
# Get GitHub token from gh CLI config
export TF_HTTP_PASSWORD=$(cat ~/.config/gh/hosts.yml | grep oauth_token | awk '{print $2}')

cd matchpoint-github-runners-helm/terraform
terraform init -input=false
terraform output -raw kubeconfig_raw > /tmp/kubeconfig.yaml
export KUBECONFIG=/tmp/kubeconfig.yaml
kubectl get nodes
```

**Option B: Manual Refresh (if token expired)**

If the scheduled workflow hasn't run recently:

```bash
# Requires RACKSPACE_SPOT_API_TOKEN
cd matchpoint-github-runners-helm/terraform
terraform refresh -var="rackspace_spot_token=$RACKSPACE_SPOT_API_TOKEN"
terraform output -raw kubeconfig_raw > /tmp/kubeconfig.yaml
```

**Option C: OIDC Context (interactive)**

The kubeconfig includes an OIDC context that auto-refreshes via browser login:

```bash
kubectl --kubeconfig=kubeconfig.yaml --context=matchpoint-ai-matchpoint-runners-oidc get pods
```

Requires: `kubectl oidc-login` plugin (`kubectl krew install oidc-login`)

## Quick Reference Commands

```bash
# Get fresh kubeconfig (using gh CLI token)
export TF_HTTP_PASSWORD=$(cat ~/.config/gh/hosts.yml | grep oauth_token | awk '{print $2}')
cd matchpoint-github-runners-helm/terraform
terraform init -input=false
terraform output -raw kubeconfig_raw > /tmp/rs-kubeconfig.yaml
export KUBECONFIG=/tmp/rs-kubeconfig.yaml

# Check runner status
kubectl get pods -n arc-beta-runners-new -l app.kubernetes.io/component=runner

# Check scaling
kubectl get autoscalingrunnerset -A

# View spot node status
kubectl get nodes -o wide | grep spot

# Check for interruptions
kubectl get events -A --field-selector reason=Evicted --sort-by='.lastTimestamp'

# Monitor GitHub Actions queue
gh run list --repo Matchpoint-AI/project-beta-api --status queued

# Check runner registration
gh api /orgs/Matchpoint-AI/actions/runners --jq '.runners[] | {name, status, busy}'
```
