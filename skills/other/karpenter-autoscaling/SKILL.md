---
name: karpenter-autoscaling
description: Karpenter for intelligent Kubernetes node autoscaling on EKS. Use when configuring node provisioning, optimizing costs with Spot instances, replacing Cluster Autoscaler, implementing consolidation, or achieving 20-70% cost savings.
---

# Karpenter Autoscaling for Amazon EKS

Intelligent, high-performance node autoscaling for Amazon EKS that provisions nodes in seconds, automatically selects optimal instance types, and reduces costs by 20-70% through Spot integration and consolidation.

## Overview

Karpenter is the **recommended autoscaler for production EKS workloads** (2025), replacing Cluster Autoscaler with:

- **Speed**: Provisions nodes in seconds (vs minutes with Cluster Autoscaler)
- **Intelligence**: Automatically selects optimal instance types based on pod requirements
- **Flexibility**: No need to configure node groups - direct EC2 instance provisioning
- **Cost Optimization**: 20-70% cost reduction through better bin-packing and Spot integration
- **Consolidation**: Automatic node consolidation when underutilized or empty

**Real-World Results**:
- 20% overall AWS bill reduction
- Up to 90% savings for CI/CD workloads
- 70% reduction in monthly compute costs
- 15-30% waste reduction with faster scale-up

## When to Use

- Replacing Cluster Autoscaler with faster, smarter autoscaling
- Optimizing EKS cluster costs (target: 20%+ savings)
- Implementing Spot instance strategies (30-70% Spot mix)
- Need sub-minute node provisioning (seconds vs minutes)
- Workloads with variable resource requirements
- Multi-instance-type flexibility without node group management
- GPU or specialized instance provisioning
- Consolidating underutilized nodes automatically

## Prerequisites

- **EKS cluster** running Kubernetes 1.23+
- **Terraform** or Helm for installation
- **IRSA or EKS Pod Identity** enabled
- **Small node group** for Karpenter controller (2-3 nodes)
- **VPC subnets and security groups** tagged for Karpenter discovery

---

## Quick Start

### 1. Install Karpenter (Helm)

```bash
# Add Karpenter Helm repo
helm repo add karpenter https://charts.karpenter.sh
helm repo update

# Install Karpenter v1.0+
helm upgrade --install karpenter karpenter/karpenter \
  --namespace kube-system \
  --set settings.clusterName=my-cluster \
  --set settings.interruptionQueue=my-cluster \
  --set controller.resources.requests.cpu=1 \
  --set controller.resources.requests.memory=1Gi \
  --set controller.resources.limits.cpu=1 \
  --set controller.resources.limits.memory=1Gi \
  --wait
```

**See**: [`references/installation.md`](references/installation.md) for complete setup including IRSA/Pod Identity

### 2. Create NodePool and EC2NodeClass

**NodePool** (defines scheduling requirements and limits):
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]  # Compute, general, memory-optimized
        - key: karpenter.k8s.aws/instance-generation
          operator: Gt
          values: ["4"]  # Gen 5+
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
  limits:
    cpu: "1000"
    memory: "1000Gi"
  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 30s
    budgets:
      - nodes: "10%"
---
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiFamily: AL2023  # Amazon Linux 2023
  role: KarpenterNodeRole-my-cluster
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster
  blockDeviceMappings:
    - deviceName: /dev/xvda
      ebs:
        volumeSize: 100Gi
        volumeType: gp3
        encrypted: true
        deleteOnTermination: true
```

```bash
kubectl apply -f nodepool.yaml
```

**See**: [`references/nodepools.md`](references/nodepools.md) for advanced NodePool patterns

### 3. Deploy Workload and Watch Autoscaling

```bash
# Deploy test workload
kubectl create deployment inflate --image=public.ecr.aws/eks-distro/kubernetes/pause:3.7 \
  --replicas=0

# Scale up to trigger node provisioning
kubectl scale deployment inflate --replicas=10

# Watch Karpenter provision nodes (seconds!)
kubectl logs -f -n kube-system -l app.kubernetes.io/name=karpenter -c controller

# Verify nodes
kubectl get nodes -l karpenter.sh/nodepool=default

# Scale down to trigger consolidation
kubectl scale deployment inflate --replicas=0

# Watch Karpenter consolidate (30s after scale-down)
kubectl logs -f -n kube-system -l app.kubernetes.io/name=karpenter -c controller
```

### 4. Monitor and Optimize

```bash
# Check NodePool status
kubectl get nodepools

# View disruption metrics
kubectl describe nodepool default

# Monitor provisioning decisions
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter | grep -i "launched\|terminated"

# Cost optimization metrics
kubectl top nodes
```

**See**: [`references/optimization.md`](references/optimization.md) for cost optimization strategies

---

## Core Concepts

### Karpenter v1.0 Architecture

**Key Resources (v1.0+)**:
1. **NodePool**: Defines node scheduling requirements, limits, and disruption policies
2. **EC2NodeClass**: AWS-specific configuration (AMIs, instance types, subnets, security groups)
3. **NodeClaim**: Karpenter's representation of a node request (auto-created)

**How It Works**:
1. Pod becomes unschedulable
2. Karpenter evaluates pod requirements (CPU, memory, affinity, taints/tolerations)
3. Karpenter selects optimal instance type from 600+ options
4. Karpenter provisions EC2 instance directly (no node groups)
5. Node joins cluster in 30-60 seconds
6. Pod scheduled to new node

**Consolidation**:
- Continuously monitors node utilization
- Consolidates underutilized nodes (bin-packing)
- Drains and deletes empty nodes
- Replaces nodes with cheaper alternatives
- Respects Pod Disruption Budgets

### NodePool vs Cluster Autoscaler Node Groups

| Feature | Karpenter NodePool | Cluster Autoscaler |
|---------|-------------------|-------------------|
| Provisioning Speed | 30-60 seconds | 2-5 minutes |
| Instance Selection | Automatic (600+ types) | Manual (pre-defined) |
| Bin-Packing | Intelligent | Limited |
| Spot Integration | Built-in, intelligent | Requires node groups |
| Consolidation | Automatic | Manual |
| Configuration | Single NodePool | Multiple node groups |
| Cost Savings | 20-70% | 10-20% |

---

## Common Workflows

### Workflow 1: Install Karpenter with Terraform

**Use case**: Production-grade installation with infrastructure as code

```hcl
# Karpenter module
module "karpenter" {
  source = "terraform-aws-modules/eks/aws//modules/karpenter"
  version = "~> 20.0"

  cluster_name = module.eks.cluster_name
  irsa_oidc_provider_arn = module.eks.oidc_provider_arn

  # Enable Pod Identity (2025 recommended)
  enable_pod_identity = true

  # Additional IAM policies
  node_iam_role_additional_policies = {
    AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  }

  tags = {
    Environment = "production"
  }
}

# Helm release
resource "helm_release" "karpenter" {
  namespace        = "kube-system"
  name             = "karpenter"
  repository       = "oci://public.ecr.aws/karpenter"
  chart            = "karpenter"
  version          = "1.0.0"

  set {
    name  = "settings.clusterName"
    value = module.eks.cluster_name
  }

  set {
    name  = "settings.interruptionQueue"
    value = module.karpenter.queue_name
  }

  set {
    name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = module.karpenter.iam_role_arn
  }
}
```

**Steps**:
1. Review [`references/installation.md`](references/installation.md)
2. Configure Terraform module with cluster details
3. Apply infrastructure: `terraform apply`
4. Verify installation: `kubectl get pods -n kube-system -l app.kubernetes.io/name=karpenter`
5. Tag subnets and security groups for discovery
6. Deploy NodePool and EC2NodeClass

**See**: [`references/installation.md`](references/installation.md) for complete Terraform setup

---

### Workflow 2: Configure Spot/On-Demand Mix (30/70)

**Use case**: Optimize costs while maintaining availability (recommended: 30% On-Demand, 70% Spot)

**Critical NodePool (On-Demand only)**:
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: critical
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["m", "c"]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
      taints:
        - key: "critical"
          value: "true"
          effect: "NoSchedule"
  limits:
    cpu: "200"
  weight: 100  # Higher priority
```

**Flexible NodePool (Spot preferred)**:
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: flexible
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]
        - key: karpenter.k8s.aws/instance-generation
          operator: Gt
          values: ["4"]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
  limits:
    cpu: "800"
  disruption:
    consolidationPolicy: WhenUnderutilized
    budgets:
      - nodes: "20%"
  weight: 10  # Lower priority (use after critical)
```

**Pod tolerations for critical workloads**:
```yaml
spec:
  tolerations:
    - key: "critical"
      operator: "Equal"
      value: "true"
      effect: "NoSchedule"
  nodeSelector:
    karpenter.sh/capacity-type: on-demand
```

**Steps**:
1. Create critical NodePool for databases, stateful apps (On-Demand)
2. Create flexible NodePool for stateless apps (Spot preferred)
3. Use taints/tolerations to separate critical workloads
4. Monitor Spot interruptions: `kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter | grep -i interrupt`

**See**: [`references/nodepools.md`](references/nodepools.md) for Spot strategies

---

### Workflow 3: Enable Consolidation for Cost Savings

**Use case**: Reduce costs by automatically consolidating underutilized nodes

**Aggressive consolidation** (development/staging):
```yaml
spec:
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 30s  # Consolidate quickly
    budgets:
      - nodes: "50%"  # Allow disrupting 50% of nodes
```

**Conservative consolidation** (production):
```yaml
spec:
  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 5m  # Wait 5 minutes before consolidating
    budgets:
      - nodes: "10%"  # Limit disruption to 10% of nodes at a time
      - schedule: "0 9-17 * * MON-FRI"  # Only during business hours
        nodes: "20%"
      - schedule: "0 0-8,18-23 * * *"  # Off-hours
        nodes: "5%"
```

**Pod Disruption Budget** (protect critical pods):
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: critical-app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: critical-app
```

**Steps**:
1. Review [`references/optimization.md`](references/optimization.md)
2. Set consolidation policy (WhenEmpty, WhenUnderutilized, WhenEmptyOrUnderutilized)
3. Configure consolidateAfter delay (30s-5m)
4. Set disruption budgets (% of nodes)
5. Create PodDisruptionBudgets for critical apps
6. Monitor consolidation: `kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter | grep consolidat`

**Expected savings**: 15-30% additional reduction beyond Spot savings

**See**: [`references/optimization.md`](references/optimization.md) for consolidation best practices

---

### Workflow 4: Migrate from Cluster Autoscaler

**Use case**: Upgrade from Cluster Autoscaler to Karpenter for better performance and cost savings

**Migration strategy** (zero-downtime):

1. **Install Karpenter** (runs alongside Cluster Autoscaler)
   ```bash
   helm install karpenter karpenter/karpenter --namespace kube-system
   ```

2. **Create NodePool with distinct labels**
   ```yaml
   spec:
     template:
       metadata:
         labels:
           provisioner: karpenter
   ```

3. **Migrate workloads gradually**
   ```yaml
   # Add node selector to new deployments
   spec:
     nodeSelector:
       provisioner: karpenter
   ```

4. **Monitor both autoscalers**
   ```bash
   # Watch Karpenter
   kubectl logs -f -n kube-system -l app.kubernetes.io/name=karpenter

   # Watch Cluster Autoscaler
   kubectl logs -f -n kube-system -l app=cluster-autoscaler
   ```

5. **Gradually scale down CA node groups**
   ```bash
   # Reduce desired size of CA node groups
   aws eks update-nodegroup-config \
     --cluster-name my-cluster \
     --nodegroup-name ca-nodes \
     --scaling-config desiredSize=1,minSize=0,maxSize=3
   ```

6. **Remove Cluster Autoscaler tags**
   ```bash
   # Remove tags from node groups
   # k8s.io/cluster-autoscaler/enabled
   # k8s.io/cluster-autoscaler/<cluster-name>
   ```

7. **Uninstall Cluster Autoscaler**
   ```bash
   helm uninstall cluster-autoscaler -n kube-system
   ```

**Testing checklist**:
- [ ] Karpenter provisions nodes successfully
- [ ] Pods schedule on Karpenter nodes
- [ ] Consolidation works as expected
- [ ] Spot interruptions handled gracefully
- [ ] No unschedulable pods
- [ ] Cost metrics show improvement

**Rollback plan**: Keep CA node groups at min size until confident in Karpenter

---

### Workflow 5: GPU Node Provisioning

**Use case**: Automatically provision GPU instances for ML workloads

**GPU NodePool**:
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: gpu
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]  # GPU typically on-demand
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: ["g4dn", "g5", "p3", "p4d"]
        - key: karpenter.k8s.aws/instance-gpu-count
          operator: Gt
          values: ["0"]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: gpu
      taints:
        - key: "nvidia.com/gpu"
          value: "true"
          effect: "NoSchedule"
  limits:
    cpu: "1000"
    nvidia.com/gpu: "8"
---
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: gpu
spec:
  amiFamily: AL2  # AL2 with GPU drivers
  amiSelectorTerms:
    - alias: al2@latest  # Latest GPU-enabled AMI
  role: KarpenterNodeRole-my-cluster
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster
  userData: |
    #!/bin/bash
    # Install NVIDIA device plugin
    /etc/eks/bootstrap.sh my-cluster
```

**GPU workload**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  tolerations:
    - key: "nvidia.com/gpu"
      operator: "Exists"
      effect: "NoSchedule"
  containers:
  - name: cuda-container
    image: nvidia/cuda:11.8.0-base-ubuntu22.04
    command: ["nvidia-smi"]
    resources:
      limits:
        nvidia.com/gpu: 1
```

**See**: [`references/nodepools.md`](references/nodepools.md) for GPU configuration details

---

## Key Configuration

### NodePool Resource Limits

Prevent runaway scaling:

```yaml
spec:
  limits:
    cpu: "1000"       # Max 1000 CPUs across all nodes in pool
    memory: "1000Gi"  # Max 1000Gi memory
    nvidia.com/gpu: "8"  # Max 8 GPUs
```

### Disruption Controls

Balance cost savings with stability:

```yaml
spec:
  disruption:
    # When to consolidate
    consolidationPolicy: WhenUnderutilized | WhenEmpty | WhenEmptyOrUnderutilized

    # Delay before consolidating (prevent flapping)
    consolidateAfter: 30s  # Default: 30s

    # Node expiration (security patching)
    expireAfter: 720h  # 30 days

    # Disruption budgets (rate limiting)
    budgets:
      - nodes: "10%"  # Max 10% of nodes disrupted at once
        reasons:
          - Underutilized
          - Empty
      - schedule: "0 0-8 * * *"  # Off-hours: more aggressive
        nodes: "50%"
```

### Instance Type Flexibility

Maximize Spot availability and cost savings:

```yaml
spec:
  template:
    spec:
      requirements:
        # Architecture
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64", "arm64"]  # Include ARM for savings

        # Instance categories (c=compute, m=general, r=memory)
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]

        # Instance generation (5+ for best performance/cost)
        - key: karpenter.k8s.aws/instance-generation
          operator: Gt
          values: ["4"]

        # Instance size (exclude large sizes if not needed)
        - key: karpenter.k8s.aws/instance-size
          operator: NotIn
          values: ["metal", "32xlarge", "24xlarge"]

        # Capacity type
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
```

**Result**: Karpenter selects from 600+ instance types, maximizing Spot availability

---

## Monitoring and Troubleshooting

### Key Metrics

```bash
# NodePool status
kubectl get nodepools

# NodeClaim status (pending provisions)
kubectl get nodeclaims

# Node events
kubectl get events --field-selector involvedObject.kind=Node

# Karpenter controller logs
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter -c controller --tail=100

# Filter for provisioning decisions
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter | grep "launched instance"

# Filter for consolidation events
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter | grep "consolidating"

# Spot interruption warnings
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter | grep "interrupt"
```

### Common Issues

**1. Nodes not provisioning**:
```bash
# Check NodePool status
kubectl describe nodepool default

# Check for unschedulable pods
kubectl get pods -A --field-selector=status.phase=Pending

# Review Karpenter logs for errors
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter | grep -i error
```

**Common causes**:
- Insufficient IAM permissions
- Subnet/security group tags missing
- Resource limits exceeded
- No instance types match requirements

**2. Excessive consolidation (pod restarts)**:
```yaml
# Increase consolidateAfter delay
spec:
  disruption:
    consolidateAfter: 5m  # Increase from 30s
```

**3. Spot interruptions causing issues**:
```yaml
# Reduce Spot ratio
- key: karpenter.sh/capacity-type
  operator: In
  values: ["on-demand"]  # Use more on-demand
```

---

## Best Practices

### Cost Optimization
- ✅ Use 30% On-Demand, 70% Spot for optimal cost/stability balance
- ✅ Enable consolidation (WhenUnderutilized)
- ✅ Include ARM instances (Graviton) for 20% additional savings
- ✅ Set instance generation > 4 for best price/performance
- ✅ Use multiple instance families (c, m, r) for Spot diversity

### Reliability
- ✅ Set Pod Disruption Budgets for critical applications
- ✅ Use multiple availability zones
- ✅ Configure disruption budgets (10-20% for production)
- ✅ Test Spot interruption handling
- ✅ Use On-Demand for stateful workloads (databases)

### Security
- ✅ Use IRSA or Pod Identity (not node IAM roles)
- ✅ Enable EBS encryption in EC2NodeClass
- ✅ Set expireAfter for regular node rotation (720h/30 days)
- ✅ Use Amazon Linux 2023 (AL2023) AMIs
- ✅ Tag resources for cost allocation

### Performance
- ✅ Use dedicated NodePool for Karpenter controller (On-Demand, no consolidation)
- ✅ Set appropriate resource limits to prevent runaway scaling
- ✅ Monitor provisioning latency (should be <60s)
- ✅ Use topology spread constraints for pod distribution

---

## Reference Documentation

**Detailed Guides** (load on-demand):
- [`references/installation.md`](references/installation.md) - Complete installation with Helm, Terraform, IRSA, Pod Identity
- [`references/nodepools.md`](references/nodepools.md) - NodePool and EC2NodeClass configuration patterns
- [`references/optimization.md`](references/optimization.md) - Cost optimization, consolidation, disruption budgets

**Official Resources**:
- [Karpenter Documentation](https://karpenter.sh/)
- [AWS Karpenter Best Practices](https://aws.github.io/aws-eks-best-practices/karpenter/)
- [Karpenter GitHub](https://github.com/aws/karpenter)

**Community Examples**:
- [Terraform EKS Karpenter Module](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest/submodules/karpenter)
- [Karpenter Blueprints](https://github.com/aws-samples/karpenter-blueprints)

---

## Quick Reference

### Installation
```bash
helm upgrade --install karpenter oci://public.ecr.aws/karpenter/karpenter \
  --version 1.0.0 \
  --namespace kube-system \
  --set settings.clusterName=my-cluster
```

### Basic NodePool
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
      nodeClassRef:
        kind: EC2NodeClass
        name: default
  limits:
    cpu: "1000"
  disruption:
    consolidationPolicy: WhenUnderutilized
```

### Monitor
```bash
kubectl logs -f -n kube-system -l app.kubernetes.io/name=karpenter
```

### Cost Savings Formula
- **Spot instances**: 70-80% savings vs On-Demand
- **Consolidation**: Additional 15-30% reduction
- **Better bin-packing**: 10-20% waste reduction
- **Total**: 20-70% overall cost reduction

---

**Next Steps**: Install Karpenter using [`references/installation.md`](references/installation.md), then configure NodePools with [`references/nodepools.md`](references/nodepools.md)
