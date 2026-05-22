---
name: karpenter
description: Kubernetes node autoscaling and cost optimization with Karpenter. Use when implementing node provisioning, spot instance management, cluster right-sizing, node consolidation, or reducing compute costs. Covers NodePool configuration, EC2NodeClass setup, disruption budgets, spot/on-demand mix strategies, multi-architecture support, and capacity-type selection.
triggers:
  - karpenter
  - node autoscaling
  - nodepool
  - ec2nodeclass
  - provisioner
  - spot instances
  - on-demand instances
  - node consolidation
  - node termination
  - cluster autoscaling
  - right-sizing
  - capacity-type
  - node disruption
  - compute costs
  - instance selection
  - graviton
  - arm64
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Karpenter

## Overview

Karpenter is a Kubernetes node autoscaler that provisions right-sized compute resources in response to changing application load. Unlike Cluster Autoscaler which scales predefined node groups, Karpenter provisions nodes based on aggregate pod resource requirements, enabling better bin-packing and cost optimization.

### Key Differences from Cluster Autoscaler

- **Direct provisioning**: Talks directly to cloud provider APIs (no node groups required)
- **Fast scaling**: Provisions nodes in seconds vs minutes
- **Flexible instance selection**: Chooses from all available instance types automatically
- **Consolidation**: Actively replaces nodes with cheaper alternatives
- **Spot instance optimization**: First-class support with automatic fallback

### When to Use Karpenter

- Running workloads with diverse resource requirements
- Need for fast scaling (sub-minute response)
- Cost optimization with spot instances and Graviton (ARM64)
- Consolidation to reduce cluster waste and over-provisioning
- Clusters with unpredictable or bursty workloads
- Right-sizing infrastructure to actual usage patterns
- Managing mixed capacity types (spot/on-demand) automatically

## Instructions

### 1. Installation and Setup

- Install Karpenter controller in cluster
- Configure cloud provider credentials (IAM roles)
- Set up instance profiles and security groups
- Create NodePools for different workload types
- Define EC2NodeClass (AWS) or equivalent for your provider

### 2. Design NodePool Strategy

- Separate NodePools for different workload classes
- Define instance type families and sizes
- Configure spot/on-demand mix
- Set resource limits per NodePool
- Plan for multi-AZ distribution

### 3. Configure Disruption Management

- Set disruption budgets to control churn
- Configure consolidation policies
- Define expiration windows for node lifecycle
- Handle workload-specific disruption constraints
- Test disruption scenarios

### 4. Optimize for Cost and Performance

- Enable consolidation for cost savings
- Use spot instances with fallback strategies
- Set appropriate resource requests on pods (Karpenter depends on accurate requests)
- Monitor node utilization and waste
- Adjust instance type restrictions based on usage
- Leverage Graviton (ARM64) instances for 20% cost reduction
- Configure capacity-type weighting to prefer spot over on-demand

### 5. Cost Optimization Strategies

- **Spot instances**: Configure 70-90% spot mix for fault-tolerant workloads
- **Graviton (ARM64)**: Use c7g, m7g, r7g families for lower costs
- **Consolidation**: Enable WhenUnderutilized policy to replace expensive nodes
- **Instance diversity**: Wide instance family selection improves spot availability
- **Right-sizing**: Let Karpenter bin-pack efficiently instead of over-provisioning

### 6. Spot Instance Management

- Use wide instance type selection (10+ families) for better spot availability
- Configure automatic fallback to on-demand when spot unavailable
- Implement Pod Disruption Budgets to control blast radius
- Set graceful termination handlers in applications (preStop hooks)
- Monitor spot interruption rates and adjust instance selection
- Use diverse availability zones to reduce correlated failures

### 7. Node Consolidation

- **WhenUnderutilized**: Replaces nodes with cheaper/smaller alternatives actively
- **WhenEmpty**: Only consolidates completely empty nodes (conservative)
- Configure consolidateAfter delay to prevent churn (30s-600s typical)
- Use disruption budgets to limit consolidation rate (5-20% per window)
- Respect Pod Disruption Budgets during consolidation
- Set expiration windows to force periodic node refresh

## Best Practices

1. **Start Conservative**: Begin with restrictive instance types, expand based on observation
2. **Use Disruption Budgets**: Prevent too many nodes from being disrupted simultaneously
3. **Set Pod Resource Requests**: Karpenter relies on accurate requests for scheduling
4. **Enable Consolidation**: Let Karpenter optimize node utilization automatically
5. **Separate Workload Classes**: Use multiple NodePools for different requirements
6. **Monitor Provisioning**: Track provisioning latency and failures
7. **Test Spot Interruptions**: Ensure graceful handling of spot instance terminations
8. **Use Topology Spread**: Combine with pod topology constraints for availability

## Examples

### Example 1: Basic NodePool with Multiple Instance Types

```yaml
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: default
spec:
  # Template for nodes created by this NodePool
  template:
    spec:
      # Reference to EC2NodeClass (AWS-specific configuration)
      nodeClassRef:
        name: default

      # Requirements that constrain instance selection
      requirements:
        # Use amd64 or arm64 architectures
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64", "arm64"]

        # Allow multiple instance families
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values:
            ["c6a", "c6i", "c7i", "m6a", "m6i", "m7i", "r6a", "r6i", "r7i"]

        # Allow a range of instance sizes
        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["large", "xlarge", "2xlarge", "4xlarge"]

        # Use 80% spot, 20% on-demand
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]

        # Spread across availability zones
        - key: topology.kubernetes.io/zone
          operator: In
          values: ["us-west-2a", "us-west-2b", "us-west-2c"]

      # Kubelet configuration
      kubelet:
        # Set max pods based on instance size
        maxPods: 110
        # Memory reservation for system components
        systemReserved:
          cpu: 100m
          memory: 100Mi
          ephemeral-storage: 1Gi
        # Eviction thresholds
        evictionHard:
          memory.available: 5%
          nodefs.available: 10%
        # Image garbage collection
        imageGCHighThresholdPercent: 85
        imageGCLowThresholdPercent: 80

      # Taints and labels
      taints:
        - key: workload-type
          value: general
          effect: NoSchedule

      # Metadata applied to nodes
      metadata:
        labels:
          workload-type: general
          managed-by: karpenter

  # Limits for this NodePool
  limits:
    cpu: 1000
    memory: 1000Gi

  # Disruption controls
  disruption:
    # Consolidation policy
    consolidationPolicy: WhenUnderutilized

    # Time window for when disruptions are allowed
    consolidateAfter: 30s

    # Budgets control the rate of disruptions
    budgets:
      - nodes: 10%
        duration: 5m

  # Node weight for scheduling decisions (higher = preferred)
  weight: 10
```

### Example 2: EC2NodeClass for AWS-Specific Configuration

```yaml
apiVersion: karpenter.k8s.aws/v1beta1
kind: EC2NodeClass
metadata:
  name: default
spec:
  # AMI selection
  amiFamily: AL2

  # Alternative: Use specific AMI selector
  # amiSelectorTerms:
  #   - id: ami-0123456789abcdef0
  #   - tags:
  #       karpenter.sh/discovery: my-cluster

  # IAM role for nodes (instance profile)
  role: KarpenterNodeRole-my-cluster

  # Subnet selection - use tags to identify subnets
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster
        kubernetes.io/role/internal-elb: "1"

  # Security group selection
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster
    - name: my-cluster-node-security-group

  # User data for node initialization
  userData: |
    #!/bin/bash
    echo "Custom node initialization"
    # Configure container runtime
    # Set up logging
    # Install monitoring agents

  # Block device mappings for EBS volumes
  blockDeviceMappings:
    - deviceName: /dev/xvda
      ebs:
        volumeSize: 100Gi
        volumeType: gp3
        iops: 3000
        throughput: 125
        encrypted: true
        deleteOnTermination: true

  # Metadata options for IMDS
  metadataOptions:
    httpEndpoint: enabled
    httpProtocolIPv6: disabled
    httpPutResponseHopLimit: 2
    httpTokens: required

  # Detailed monitoring
  detailedMonitoring: true

  # Tags applied to EC2 instances
  tags:
    Name: karpenter-node
    Environment: production
    ManagedBy: karpenter
    ClusterName: my-cluster
```

### Example 3: Specialized NodePools for Different Workloads

```yaml
---
# GPU workload NodePool
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: gpu-workloads
spec:
  template:
    spec:
      nodeClassRef:
        name: gpu-nodes

      requirements:
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: ["g5", "g6", "p4", "p5"]

        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"] # GPU instances typically on-demand

        - key: karpenter.k8s.aws/instance-gpu-count
          operator: Gt
          values: ["0"]

      taints:
        - key: nvidia.com/gpu
          value: "true"
          effect: NoSchedule

      metadata:
        labels:
          workload-type: gpu
          nvidia.com/gpu: "true"

  limits:
    cpu: 500
    memory: 2000Gi
    nvidia.com/gpu: 16

  disruption:
    consolidationPolicy: WhenEmpty
    consolidateAfter: 300s

---
# Batch/Spot-heavy NodePool
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: batch-workloads
spec:
  template:
    spec:
      nodeClassRef:
        name: default

      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot"] # Only spot instances

        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: ["c6a", "c6i", "c7i", "m6a", "m6i"] # Compute-optimized

        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["2xlarge", "4xlarge", "8xlarge"]

      taints:
        - key: workload-type
          value: batch
          effect: NoSchedule

      metadata:
        labels:
          workload-type: batch
          spot-interruption-handler: enabled

  disruption:
    consolidationPolicy: WhenEmpty
    consolidateAfter: 60s
    budgets:
      - nodes: 20% # Allow more aggressive disruption for batch

---
# Stateful workload NodePool (on-demand only)
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: stateful-workloads
spec:
  template:
    spec:
      nodeClassRef:
        name: stateful-nodes

      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"] # Only on-demand for stability

        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: ["r6i", "r7i"] # Memory-optimized

        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["xlarge", "2xlarge", "4xlarge"]

        - key: topology.kubernetes.io/zone
          operator: In
          values: ["us-west-2a", "us-west-2b"]

      kubelet:
        maxPods: 50 # Lower density for stateful workloads

      taints:
        - key: workload-type
          value: stateful
          effect: NoSchedule

      metadata:
        labels:
          workload-type: stateful
          storage-optimized: "true"

  limits:
    cpu: 200
    memory: 800Gi

  disruption:
    consolidationPolicy: WhenEmpty # Only consolidate when completely empty
    consolidateAfter: 600s # Wait 10 minutes
    budgets:
      - nodes: 1 # Very conservative disruption
        duration: 30m
```

### Example 4: Disruption Budgets and Consolidation Policies

```yaml
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: production-apps
spec:
  template:
    spec:
      nodeClassRef:
        name: default

      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]

        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: ["c6i", "m6i", "r6i"]

  # Advanced disruption configuration
  disruption:
    # Consolidation policy options:
    # - WhenUnderutilized: Replace nodes with cheaper/smaller nodes
    # - WhenEmpty: Only replace completely empty nodes
    consolidationPolicy: WhenUnderutilized

    # How soon after a node becomes eligible for consolidation
    consolidateAfter: 30s

    # Expiration settings - force node replacement after time period
    expireAfter: 720h # 30 days

    # Multiple budget windows for different times/scenarios
    budgets:
      # During business hours: conservative disruption
      - nodes: 5%
        duration: 8h
        schedule: "0 8 * * MON-FRI"

      # During off-hours: more aggressive consolidation
      - nodes: 20%
        duration: 16h
        schedule: "0 18 * * MON-FRI"

      # Weekends: most aggressive
      - nodes: 30%
        duration: 48h
        schedule: "0 0 * * SAT"

      # Default budget (always active)
      - nodes: 10%
```

### Example 5: Pod Scheduling with Karpenter

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-application
spec:
  replicas: 5
  selector:
    matchLabels:
      app: my-application
  template:
    metadata:
      labels:
        app: my-application
    spec:
      # Tolerations to allow scheduling on Karpenter nodes
      tolerations:
        - key: workload-type
          operator: Equal
          value: general
          effect: NoSchedule

      # Node selector to target specific NodePool
      nodeSelector:
        workload-type: general
        karpenter.sh/capacity-type: spot # Prefer spot

      # Affinity rules for better placement
      affinity:
        # Spread across zones for availability
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: my-application
                topologyKey: topology.kubernetes.io/zone

        # Node affinity for instance type preferences
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            # Prefer ARM instances (cheaper)
            - weight: 50
              preference:
                matchExpressions:
                  - key: kubernetes.io/arch
                    operator: In
                    values: ["arm64"]

            # Prefer larger instances (better bin-packing)
            - weight: 30
              preference:
                matchExpressions:
                  - key: karpenter.k8s.aws/instance-size
                    operator: In
                    values: ["2xlarge", "4xlarge"]

      # Topology spread constraints
      topologySpreadConstraints:
        # Spread across zones
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app: my-application

        # Spread across nodes
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app: my-application

      containers:
        - name: app
          image: my-app:latest

          # CRITICAL: Accurate resource requests for Karpenter
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 2Gi

          # Graceful shutdown for spot interruptions
          lifecycle:
            preStop:
              exec:
                command:
                  - /bin/sh
                  - -c
                  - sleep 15 # Allow time for deregistration

      # Termination grace period for spot interruptions
      terminationGracePeriodSeconds: 30
```

### Example 6: Spot Instance Handling and Fallback

```yaml
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: spot-with-fallback
spec:
  template:
    spec:
      nodeClassRef:
        name: default

      requirements:
        # Prioritize spot, but allow on-demand as fallback
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]

        # Wide instance type selection for better spot availability
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values:
            - "c5a"
            - "c6a"
            - "c6i"
            - "c7i"
            - "m5a"
            - "m6a"
            - "m6i"
            - "m7i"
            - "r5a"
            - "r6a"
            - "r6i"
            - "r7i"

        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["large", "xlarge", "2xlarge", "4xlarge"]

        # Support both architectures for more spot options
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64", "arm64"]

      # Metadata to track spot usage
      metadata:
        labels:
          spot-enabled: "true"
        annotations:
          karpenter.sh/spot-to-spot-consolidation: "true"

  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 30s

    # More aggressive for spot since they can be interrupted anyway
    budgets:
      - nodes: 25%

  # Weight influences Karpenter's NodePool selection
  # Higher weight = more preferred
  # Use lower weight so other NodePools are tried first
  weight: 5
```

### Example 7: Karpenter with Pod Disruption Budget

```yaml
# Application Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: critical-service
spec:
  replicas: 6
  selector:
    matchLabels:
      app: critical-service
  template:
    metadata:
      labels:
        app: critical-service
    spec:
      tolerations:
        - key: workload-type
          operator: Equal
          value: general
          effect: NoSchedule

      containers:
        - name: app
          image: critical-service:latest
          resources:
            requests:
              cpu: 1000m
              memory: 2Gi
            limits:
              cpu: 2000m
              memory: 4Gi

---
# Pod Disruption Budget to protect during consolidation
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: critical-service-pdb
spec:
  minAvailable: 4 # Always keep at least 4 replicas running
  selector:
    matchLabels:
      app: critical-service
# Karpenter respects PDBs during consolidation
# It will not disrupt nodes if doing so would violate the PDB
```

### Example 8: Multi-Architecture NodePool

```yaml
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: multi-arch
spec:
  template:
    spec:
      nodeClassRef:
        name: default

      requirements:
        # Support both AMD64 and ARM64
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64", "arm64"]

        # ARM instances (Graviton) - typically 20% cheaper
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values:
            # ARM (Graviton2)
            - "c6g"
            - "m6g"
            - "r6g"
            # ARM (Graviton3)
            - "c7g"
            - "m7g"
            - "r7g"
            # AMD64 alternatives
            - "c6i"
            - "m6i"
            - "r6i"

        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]

      metadata:
        labels:
          multi-arch: "true"

  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 60s

---
# EC2NodeClass with multi-architecture AMI support
apiVersion: karpenter.k8s.aws/v1beta1
kind: EC2NodeClass
metadata:
  name: default
spec:
  # AL2 automatically selects the right AMI for architecture
  amiFamily: AL2

  # Alternative: Explicit AMI selection by architecture
  # amiSelectorTerms:
  #   - tags:
  #       karpenter.sh/discovery: my-cluster
  #       kubernetes.io/arch: amd64
  #   - tags:
  #       karpenter.sh/discovery: my-cluster
  #       kubernetes.io/arch: arm64

  role: KarpenterNodeRole-my-cluster

  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster

  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster
```

## Monitoring and Troubleshooting

### Key Metrics to Monitor

```text
# Provisioning metrics
karpenter_nodes_created_total
karpenter_nodes_terminated_total
karpenter_provisioner_scheduling_duration_seconds

# Disruption metrics
karpenter_disruption_replacement_node_initialized_seconds
karpenter_disruption_consolidation_actions_performed_total
karpenter_disruption_budgets_allowed_disruptions

# Cost metrics
karpenter_provisioner_instance_type_price_estimate
karpenter_cloudprovider_instance_type_offering_price_estimate

# Pod metrics
karpenter_pods_state (pending, running, etc.)
```

### Common Issues and Solutions

#### Issue: Pods stuck in Pending

- Check NodePool requirements match pod node selectors/tolerations
- Verify cloud provider limits not exceeded
- Check instance type availability in selected zones
- Ensure subnet capacity available

#### Issue: Excessive node churn

- Adjust consolidation delay (consolidateAfter)
- Review disruption budgets
- Check if pod resource requests are accurate
- Consider using WhenEmpty instead of WhenUnderutilized

#### Issue: High costs despite using Karpenter

- Enable consolidation if not already active
- Verify spot instances are being used
- Check if pods have unnecessarily large resource requests
- Review instance type selection (allow more variety)

#### Issue: Spot interruptions causing service disruption

- Implement Pod Disruption Budgets
- Use diverse instance types for better spot availability
- Configure appropriate replica counts
- Implement graceful shutdown in applications

## Integration with Terraform

```hcl
# Install Karpenter via Terraform
resource "helm_release" "karpenter" {
  namespace        = "karpenter"
  create_namespace = true
  name             = "karpenter"
  repository       = "oci://public.ecr.aws/karpenter"
  chart            = "karpenter"
  version          = "v0.33.0"

  values = [
    <<-EOT
    settings:
      clusterName: ${var.cluster_name}
      clusterEndpoint: ${var.cluster_endpoint}
      interruptionQueue: ${var.interruption_queue_name}

    serviceAccount:
      annotations:
        eks.amazonaws.com/role-arn: ${var.karpenter_irsa_arn}

    controller:
      resources:
        requests:
          cpu: 1
          memory: 1Gi
        limits:
          cpu: 2
          memory: 2Gi
    EOT
  ]

  depends_on = [
    aws_iam_role_policy_attachment.karpenter_controller
  ]
}

# Deploy default NodePool
resource "kubectl_manifest" "karpenter_nodepool_default" {
  yaml_body = <<-YAML
    apiVersion: karpenter.sh/v1beta1
    kind: NodePool
    metadata:
      name: default
    spec:
      template:
        spec:
          nodeClassRef:
            name: default
          requirements:
            - key: karpenter.sh/capacity-type
              operator: In
              values: ["spot", "on-demand"]
            - key: karpenter.k8s.aws/instance-family
              operator: In
              values: ["c6i", "m6i", "r6i"]
      limits:
        cpu: 1000
        memory: 1000Gi
      disruption:
        consolidationPolicy: WhenUnderutilized
        consolidateAfter: 30s
  YAML

  depends_on = [helm_release.karpenter]
}
```

## Migration from Cluster Autoscaler

1. **Plan the migration**

   - Identify current node groups and their characteristics
   - Map workloads to new NodePool configurations
   - Plan for coexistence period

2. **Deploy Karpenter alongside Cluster Autoscaler**

   - Install Karpenter in the cluster
   - Create NodePools with distinct labels
   - Test with non-critical workloads first

3. **Migrate workloads incrementally**

   - Update pod specs with Karpenter tolerations/node selectors
   - Monitor provisioning and consolidation behavior
   - Validate cost and performance metrics

4. **Remove Cluster Autoscaler**

   - Once all workloads migrated, scale down CA node groups
   - Remove Cluster Autoscaler deployment
   - Clean up CA-specific resources
