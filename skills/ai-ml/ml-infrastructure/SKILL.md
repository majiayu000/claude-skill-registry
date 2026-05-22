---
name: ml-infrastructure
description: Production-grade ML infrastructure with Kubernetes, auto-scaling, and cost optimization
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 07-ml-infrastructure
bond_type: PRIMARY_BOND

input_schema:
  type: object
  required:
    - infrastructure_task
  properties:
    infrastructure_task:
      type: string
      enum: [cluster_setup, auto_scaling, cost_optimization, security_hardening, disaster_recovery]
    cloud_provider:
      type: string
      enum: [aws, gcp, azure, on_premise]
    workload_type:
      type: string
      enum: [training, inference, batch, streaming]
    scale_requirements:
      type: object
      properties:
        min_replicas:
          type: integer
          default: 1
        max_replicas:
          type: integer
          default: 100
        target_gpu_utilization:
          type: number
          default: 0.8

output_schema:
  type: object
  properties:
    infrastructure_config:
      type: object
    deployment_manifests:
      type: array
      items:
        type: object
    cost_estimate:
      type: object
    security_report:
      type: object
    runbooks:
      type: array
      items:
        type: string

validation:
  pre_conditions:
    - kubernetes_cluster_accessible
    - cloud_credentials_valid
    - quota_available
  post_conditions:
    - infrastructure_deployed
    - health_checks_passing
    - monitoring_configured

error_handling:
  common_errors:
    - type: quota_exceeded
      recovery: request_quota_increase_or_optimize
    - type: node_provisioning_failure
      recovery: fallback_to_alternative_instance_type
    - type: network_policy_conflict
      recovery: audit_and_reconcile_policies
---

# ML Infrastructure

Production-grade ML infrastructure with Kubernetes, auto-scaling, and cost optimization.

## Learning Objectives

By mastering this skill, you will be able to:
- Design and deploy Kubernetes clusters for ML workloads
- Implement intelligent auto-scaling for training and inference
- Optimize cloud costs for ML operations
- Implement security best practices for ML systems
- Build disaster recovery and high availability architectures

---

## Module 1: Kubernetes for ML Workloads

### Cluster Architecture

```yaml
ml_cluster_architecture:
  control_plane:
    components:
      - kube-apiserver (HA: 3 replicas)
      - etcd (HA: 3 replicas)
      - kube-scheduler
      - kube-controller-manager

  node_pools:
    cpu_training:
      instance_type: c6i.8xlarge
      min_nodes: 2
      max_nodes: 50
      labels:
        workload-type: training
        accelerator: cpu

    gpu_training:
      instance_type: p4d.24xlarge
      min_nodes: 0
      max_nodes: 20
      labels:
        workload-type: training
        accelerator: nvidia-a100
      taints:
        - nvidia.com/gpu=present:NoSchedule

    inference:
      instance_type: g5.xlarge
      min_nodes: 2
      max_nodes: 100
      labels:
        workload-type: inference
        accelerator: nvidia-a10g
```

### Implementation: EKS Cluster with Terraform

```hcl
# terraform/eks-ml-cluster/main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Variables
variable "cluster_name" {
  default = "ml-production"
}

variable "region" {
  default = "us-west-2"
}

# VPC for ML Cluster
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.cluster_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b", "${var.region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = false
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.29"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  # Cluster addons
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  # Node groups
  eks_managed_node_groups = {
    # CPU Training Node Group
    cpu_training = {
      name           = "cpu-training"
      instance_types = ["c6i.8xlarge"]

      min_size     = 2
      max_size     = 50
      desired_size = 2

      labels = {
        workload-type = "training"
        accelerator   = "cpu"
      }

      tags = {
        "k8s.io/cluster-autoscaler/enabled"         = "true"
        "k8s.io/cluster-autoscaler/${var.cluster_name}" = "owned"
      }
    }

    # GPU Training Node Group
    gpu_training = {
      name           = "gpu-training"
      instance_types = ["p4d.24xlarge"]
      ami_type       = "AL2_x86_64_GPU"

      min_size     = 0
      max_size     = 20
      desired_size = 0

      labels = {
        workload-type = "training"
        accelerator   = "nvidia-a100"
      }

      taints = [{
        key    = "nvidia.com/gpu"
        value  = "present"
        effect = "NO_SCHEDULE"
      }]

      tags = {
        "k8s.io/cluster-autoscaler/enabled"         = "true"
        "k8s.io/cluster-autoscaler/${var.cluster_name}" = "owned"
      }
    }

    # Inference Node Group
    inference = {
      name           = "inference"
      instance_types = ["g5.xlarge"]
      ami_type       = "AL2_x86_64_GPU"

      min_size     = 2
      max_size     = 100
      desired_size = 3

      labels = {
        workload-type = "inference"
        accelerator   = "nvidia-a10g"
      }

      tags = {
        "k8s.io/cluster-autoscaler/enabled"         = "true"
        "k8s.io/cluster-autoscaler/${var.cluster_name}" = "owned"
      }
    }
  }

  # IRSA for various components
  enable_irsa = true

  tags = {
    Environment = "production"
    Team        = "ml-platform"
  }
}

# NVIDIA Device Plugin
resource "kubernetes_daemon_set" "nvidia_device_plugin" {
  depends_on = [module.eks]

  metadata {
    name      = "nvidia-device-plugin-daemonset"
    namespace = "kube-system"
  }

  spec {
    selector {
      match_labels = {
        name = "nvidia-device-plugin-ds"
      }
    }

    template {
      metadata {
        labels = {
          name = "nvidia-device-plugin-ds"
        }
      }

      spec {
        toleration {
          key      = "nvidia.com/gpu"
          operator = "Exists"
          effect   = "NoSchedule"
        }

        container {
          name  = "nvidia-device-plugin-ctr"
          image = "nvcr.io/nvidia/k8s-device-plugin:v0.14.3"

          env {
            name  = "FAIL_ON_INIT_ERROR"
            value = "false"
          }

          security_context {
            allow_privilege_escalation = false
            capabilities {
              drop = ["ALL"]
            }
          }

          volume_mount {
            name       = "device-plugin"
            mount_path = "/var/lib/kubelet/device-plugins"
          }
        }

        volume {
          name = "device-plugin"
          host_path {
            path = "/var/lib/kubelet/device-plugins"
          }
        }
      }
    }
  }
}

# Outputs
output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "cluster_name" {
  value = module.eks.cluster_name
}
```

### GPU Training Job Manifest

```yaml
# kubernetes/training-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: distributed-training-job
  namespace: ml-training
spec:
  parallelism: 4
  completions: 4
  backoffLimit: 3
  template:
    metadata:
      labels:
        app: distributed-training
    spec:
      restartPolicy: OnFailure

      nodeSelector:
        workload-type: training
        accelerator: nvidia-a100

      tolerations:
        - key: nvidia.com/gpu
          operator: Exists
          effect: NoSchedule

      containers:
        - name: trainer
          image: my-registry/training-image:v1.0

          resources:
            requests:
              memory: "64Gi"
              cpu: "16"
              nvidia.com/gpu: 8
            limits:
              memory: "128Gi"
              cpu: "32"
              nvidia.com/gpu: 8

          env:
            - name: WORLD_SIZE
              value: "32"  # 4 nodes * 8 GPUs
            - name: MASTER_ADDR
              value: "distributed-training-job-0"
            - name: MASTER_PORT
              value: "29500"
            - name: NCCL_DEBUG
              value: "INFO"

          volumeMounts:
            - name: training-data
              mountPath: /data
            - name: model-checkpoints
              mountPath: /checkpoints
            - name: shm
              mountPath: /dev/shm

      volumes:
        - name: training-data
          persistentVolumeClaim:
            claimName: training-data-pvc
        - name: model-checkpoints
          persistentVolumeClaim:
            claimName: checkpoints-pvc
        - name: shm
          emptyDir:
            medium: Memory
            sizeLimit: "64Gi"
```

---

## Module 2: Auto-Scaling Strategies

### Karpenter Configuration

```yaml
# karpenter/provisioner.yaml
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: ml-gpu-nodepool
spec:
  template:
    spec:
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: node.kubernetes.io/instance-type
          operator: In
          values:
            - p4d.24xlarge
            - p4de.24xlarge
            - p5.48xlarge
        - key: karpenter.k8s.aws/instance-gpu-count
          operator: Gt
          values: ["0"]

      nodeClassRef:
        name: ml-gpu-nodeclass

      taints:
        - key: nvidia.com/gpu
          value: "present"
          effect: NoSchedule

  limits:
    cpu: 2000
    memory: 8000Gi
    nvidia.com/gpu: 200

  disruption:
    consolidationPolicy: WhenEmpty
    consolidateAfter: 30s
    budgets:
      - nodes: "10%"
---
apiVersion: karpenter.k8s.aws/v1beta1
kind: EC2NodeClass
metadata:
  name: ml-gpu-nodeclass
spec:
  amiFamily: AL2

  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: ml-production

  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: ml-production

  blockDeviceMappings:
    - deviceName: /dev/xvda
      ebs:
        volumeSize: 500Gi
        volumeType: gp3
        iops: 10000
        throughput: 500
        deleteOnTermination: true

  instanceStorePolicy: RAID0

  userData: |
    #!/bin/bash
    # Install NVIDIA drivers and container toolkit
    yum install -y nvidia-driver-latest-dkms
    yum install -y nvidia-container-toolkit
    systemctl restart containerd
```

### KEDA Scaling for Inference

```yaml
# keda/inference-scaler.yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: inference-scaler
  namespace: ml-inference
spec:
  scaleTargetRef:
    name: model-server
    kind: Deployment

  pollingInterval: 15
  cooldownPeriod: 60
  minReplicaCount: 2
  maxReplicaCount: 100

  triggers:
    # Scale based on pending requests in queue
    - type: prometheus
      metadata:
        serverAddress: http://prometheus-server.monitoring:9090
        metricName: inference_queue_depth
        threshold: "100"
        query: |
          sum(rate(inference_requests_total{status="pending"}[1m]))

    # Scale based on GPU utilization
    - type: prometheus
      metadata:
        serverAddress: http://prometheus-server.monitoring:9090
        metricName: gpu_utilization
        threshold: "80"
        query: |
          avg(DCGM_FI_DEV_GPU_UTIL{pod=~"model-server.*"})

    # Scale based on request latency
    - type: prometheus
      metadata:
        serverAddress: http://prometheus-server.monitoring:9090
        metricName: inference_latency_p99
        threshold: "200"
        query: |
          histogram_quantile(0.99,
            sum(rate(inference_latency_seconds_bucket[5m])) by (le)
          ) * 1000

  advanced:
    horizontalPodAutoscalerConfig:
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
          policies:
            - type: Percent
              value: 10
              periodSeconds: 60
        scaleUp:
          stabilizationWindowSeconds: 0
          policies:
            - type: Percent
              value: 100
              periodSeconds: 15
            - type: Pods
              value: 10
              periodSeconds: 15
          selectPolicy: Max
```

### Custom Metrics Adapter

```python
"""
Custom metrics adapter for ML-specific scaling.
"""
from kubernetes import client, config
from prometheus_client import start_http_server, Gauge
import time
from typing import Dict
import numpy as np

class MLMetricsAdapter:
    """Expose ML-specific metrics for scaling decisions."""

    def __init__(self):
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()
        self.custom_api = client.CustomObjectsApi()

        # Define Prometheus metrics
        self.gpu_memory_utilization = Gauge(
            'ml_gpu_memory_utilization_percent',
            'GPU memory utilization percentage',
            ['pod', 'gpu_index']
        )

        self.model_throughput = Gauge(
            'ml_model_throughput_requests_per_second',
            'Model inference throughput',
            ['model_name', 'model_version']
        )

        self.batch_queue_depth = Gauge(
            'ml_batch_queue_depth',
            'Number of pending batch requests',
            ['model_name']
        )

        self.estimated_wait_time = Gauge(
            'ml_estimated_wait_time_seconds',
            'Estimated wait time for new requests',
            ['model_name']
        )

    def collect_gpu_metrics(self) -> Dict[str, float]:
        """Collect GPU metrics from DCGM exporter."""
        # In production, query DCGM exporter or nvidia-smi
        # This is a simplified example
        pods = self.v1.list_namespaced_pod(
            namespace="ml-inference",
            label_selector="app=model-server"
        )

        metrics = {}
        for pod in pods.items:
            pod_name = pod.metadata.name
            # Query GPU metrics (simplified)
            for gpu_idx in range(8):  # Assuming 8 GPUs per pod
                util = np.random.uniform(60, 95)  # Placeholder
                self.gpu_memory_utilization.labels(
                    pod=pod_name,
                    gpu_index=str(gpu_idx)
                ).set(util)
                metrics[f"{pod_name}_gpu_{gpu_idx}"] = util

        return metrics

    def calculate_scaling_recommendation(
        self,
        current_replicas: int,
        target_utilization: float = 80.0,
        queue_depth: int = 0,
        throughput_per_replica: float = 100.0
    ) -> int:
        """Calculate recommended replica count."""
        # Based on queue depth
        queue_based = max(1, int(np.ceil(queue_depth / throughput_per_replica)))

        # Based on utilization (from GPU metrics)
        gpu_metrics = self.collect_gpu_metrics()
        avg_util = np.mean(list(gpu_metrics.values())) if gpu_metrics else 0
        util_based = int(np.ceil(
            current_replicas * (avg_util / target_utilization)
        ))

        # Take maximum of both signals
        recommended = max(queue_based, util_based, 1)

        return recommended

    def run(self, port: int = 8080):
        """Run metrics server."""
        start_http_server(port)
        print(f"Metrics server started on port {port}")

        while True:
            self.collect_gpu_metrics()
            time.sleep(15)


if __name__ == "__main__":
    adapter = MLMetricsAdapter()
    adapter.run()
```

---

## Module 3: Cost Optimization

### Cost Analysis Framework

```python
"""
ML infrastructure cost analysis and optimization.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import boto3

@dataclass
class ResourceUsage:
    """Resource usage metrics."""
    resource_type: str
    instance_type: str
    hours_used: float
    avg_utilization: float
    cost_usd: float

@dataclass
class CostOptimizationRecommendation:
    """Cost optimization recommendation."""
    category: str
    current_cost: float
    projected_savings: float
    implementation_effort: str
    recommendation: str
    action_items: List[str]

class MLCostOptimizer:
    """Analyze and optimize ML infrastructure costs."""

    def __init__(self, aws_region: str = "us-west-2"):
        self.ce_client = boto3.client('ce', region_name=aws_region)
        self.ec2_client = boto3.client('ec2', region_name=aws_region)

        # Instance pricing (simplified - use AWS Price List API in production)
        self.on_demand_pricing = {
            "p4d.24xlarge": 32.77,
            "p4de.24xlarge": 40.97,
            "p5.48xlarge": 98.32,
            "g5.xlarge": 1.006,
            "g5.2xlarge": 1.212,
            "c6i.8xlarge": 1.36,
        }

        self.spot_discount = 0.7  # 70% average spot discount

    def get_cost_breakdown(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """Get cost breakdown by service and resource."""
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'TAG', 'Key': 'workload-type'}
            ]
        )

        records = []
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            for group in result['Groups']:
                service = group['Keys'][0]
                workload = group['Keys'][1] if len(group['Keys']) > 1 else 'untagged'
                cost = float(group['Metrics']['UnblendedCost']['Amount'])
                records.append({
                    'date': date,
                    'service': service,
                    'workload_type': workload,
                    'cost': cost
                })

        return pd.DataFrame(records)

    def analyze_gpu_utilization(
        self,
        utilization_data: pd.DataFrame
    ) -> Dict[str, float]:
        """Analyze GPU utilization patterns."""
        analysis = {
            'avg_utilization': utilization_data['gpu_util'].mean(),
            'p50_utilization': utilization_data['gpu_util'].quantile(0.5),
            'p90_utilization': utilization_data['gpu_util'].quantile(0.9),
            'idle_hours': len(utilization_data[utilization_data['gpu_util'] < 10]),
            'underutilized_hours': len(utilization_data[utilization_data['gpu_util'] < 50]),
        }

        total_hours = len(utilization_data)
        analysis['idle_percentage'] = analysis['idle_hours'] / total_hours * 100
        analysis['underutilized_percentage'] = analysis['underutilized_hours'] / total_hours * 100

        return analysis

    def generate_recommendations(
        self,
        cost_data: pd.DataFrame,
        utilization_analysis: Dict[str, float]
    ) -> List[CostOptimizationRecommendation]:
        """Generate cost optimization recommendations."""
        recommendations = []

        # Spot instance recommendation
        if utilization_analysis['idle_percentage'] > 20:
            on_demand_cost = cost_data[
                cost_data['service'] == 'Amazon Elastic Compute Cloud - Compute'
            ]['cost'].sum()

            spot_savings = on_demand_cost * self.spot_discount * 0.3  # Conservative

            recommendations.append(CostOptimizationRecommendation(
                category="Spot Instances",
                current_cost=on_demand_cost,
                projected_savings=spot_savings,
                implementation_effort="medium",
                recommendation="Use Spot instances for fault-tolerant training workloads",
                action_items=[
                    "Enable Spot instances in Karpenter provisioner",
                    "Implement checkpointing in training scripts",
                    "Configure interruption handling",
                    "Set up Spot instance diversification"
                ]
            ))

        # Right-sizing recommendation
        if utilization_analysis['avg_utilization'] < 50:
            recommendations.append(CostOptimizationRecommendation(
                category="Right-sizing",
                current_cost=cost_data['cost'].sum(),
                projected_savings=cost_data['cost'].sum() * 0.3,
                implementation_effort="low",
                recommendation="Downsize GPU instances due to low utilization",
                action_items=[
                    "Analyze workload requirements",
                    "Test with smaller instance types",
                    "Update node pool configurations",
                    "Monitor performance after changes"
                ]
            ))

        # Reserved capacity recommendation
        base_load = utilization_analysis['p50_utilization']
        if base_load > 30:
            recommendations.append(CostOptimizationRecommendation(
                category="Reserved Instances",
                current_cost=cost_data['cost'].sum(),
                projected_savings=cost_data['cost'].sum() * 0.4,
                implementation_effort="low",
                recommendation="Purchase Reserved Instances for baseline capacity",
                action_items=[
                    "Calculate baseline GPU requirements",
                    "Evaluate 1-year vs 3-year commitments",
                    "Purchase RIs for 50% of average usage",
                    "Set up RI utilization monitoring"
                ]
            ))

        # Scheduled scaling recommendation
        recommendations.append(CostOptimizationRecommendation(
            category="Scheduled Scaling",
            current_cost=cost_data['cost'].sum() * 0.2,
            projected_savings=cost_data['cost'].sum() * 0.15,
            implementation_effort="medium",
            recommendation="Implement scheduled scaling for predictable workloads",
            action_items=[
                "Analyze traffic patterns by hour/day",
                "Configure KEDA cron triggers",
                "Scale down during off-peak hours",
                "Test scaling policies"
            ]
        ))

        return recommendations

    def generate_cost_report(self) -> str:
        """Generate cost optimization report."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        cost_data = self.get_cost_breakdown(start_date, end_date)

        # Simulated utilization data
        utilization_data = pd.DataFrame({
            'timestamp': pd.date_range(start=start_date, end=end_date, freq='h'),
            'gpu_util': np.random.uniform(20, 80, 720)
        })

        utilization_analysis = self.analyze_gpu_utilization(utilization_data)
        recommendations = self.generate_recommendations(cost_data, utilization_analysis)

        report = f"""
# ML Infrastructure Cost Report
Generated: {datetime.now().isoformat()}
Period: {start_date.date()} to {end_date.date()}

## Summary
- Total Cost: ${cost_data['cost'].sum():,.2f}
- Average Daily Cost: ${cost_data.groupby('date')['cost'].sum().mean():,.2f}
- GPU Utilization: {utilization_analysis['avg_utilization']:.1f}%

## Utilization Analysis
- Average: {utilization_analysis['avg_utilization']:.1f}%
- P50: {utilization_analysis['p50_utilization']:.1f}%
- P90: {utilization_analysis['p90_utilization']:.1f}%
- Idle Time: {utilization_analysis['idle_percentage']:.1f}%

## Recommendations
"""

        total_savings = 0
        for i, rec in enumerate(recommendations, 1):
            report += f"""
### {i}. {rec.category}
- Current Cost: ${rec.current_cost:,.2f}
- Projected Savings: ${rec.projected_savings:,.2f}
- Effort: {rec.implementation_effort}
- Recommendation: {rec.recommendation}
- Action Items:
"""
            for item in rec.action_items:
                report += f"  - {item}\n"
            total_savings += rec.projected_savings

        report += f"\n## Total Projected Savings: ${total_savings:,.2f}/month"

        return report


# Usage
if __name__ == "__main__":
    import numpy as np
    optimizer = MLCostOptimizer()
    report = optimizer.generate_cost_report()
    print(report)
```

### Cost Dashboard Queries (Grafana)

```yaml
# grafana/dashboards/ml-cost-dashboard.yaml
apiVersion: 1
providers:
  - name: 'ML Cost Dashboard'
    type: file
    options:
      path: /var/lib/grafana/dashboards

---
# Dashboard JSON
{
  "title": "ML Infrastructure Cost Dashboard",
  "panels": [
    {
      "title": "Daily GPU Cost by Workload",
      "type": "timeseries",
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "sum(rate(kube_pod_container_resource_requests{resource='nvidia_com_gpu'}[1h])) by (workload_type) * 32.77",
          "legendFormat": "{{workload_type}}"
        }
      ]
    },
    {
      "title": "GPU Utilization vs Cost Efficiency",
      "type": "gauge",
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "avg(DCGM_FI_DEV_GPU_UTIL) / 100",
          "legendFormat": "GPU Efficiency"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              {"value": 0, "color": "red"},
              {"value": 0.5, "color": "yellow"},
              {"value": 0.8, "color": "green"}
            ]
          }
        }
      }
    },
    {
      "title": "Spot vs On-Demand Savings",
      "type": "stat",
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "sum(karpenter_nodes_total_pod_requests{capacity_type='spot'}) / sum(karpenter_nodes_total_pod_requests) * 70",
          "legendFormat": "Spot Savings %"
        }
      ]
    }
  ]
}
```

---

## Module 4: Security Hardening

### Security Architecture

```yaml
ml_security_layers:
  network:
    - private_subnets_only
    - network_policies
    - service_mesh_mtls
    - vpc_endpoints

  identity:
    - irsa_for_pods
    - least_privilege_rbac
    - pod_security_standards
    - secrets_management

  data:
    - encryption_at_rest
    - encryption_in_transit
    - data_classification
    - access_logging

  runtime:
    - container_scanning
    - runtime_protection
    - audit_logging
    - anomaly_detection
```

### Network Policies

```yaml
# kubernetes/network-policies/ml-inference-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ml-inference-network-policy
  namespace: ml-inference
spec:
  podSelector:
    matchLabels:
      app: model-server
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Allow traffic from ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080

    # Allow metrics scraping from monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 9090

  egress:
    # Allow access to model registry
    - to:
        - namespaceSelector:
            matchLabels:
              name: mlflow
      ports:
        - protocol: TCP
          port: 5000

    # Allow access to feature store
    - to:
        - namespaceSelector:
            matchLabels:
              name: feast
      ports:
        - protocol: TCP
          port: 6566

    # Allow DNS resolution
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### RBAC Configuration

```yaml
# kubernetes/rbac/ml-platform-rbac.yaml
---
# ML Engineer Role - Can manage training jobs
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ml-engineer
  namespace: ml-training
rules:
  - apiGroups: ["batch"]
    resources: ["jobs"]
    verbs: ["create", "delete", "get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list"]
    resourceNames: ["training-config", "model-credentials"]
  - apiGroups: ["kubeflow.org"]
    resources: ["pytorchjobs", "tfjobs"]
    verbs: ["create", "delete", "get", "list", "watch"]
---
# ML Platform Admin - Full access to ML namespaces
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ml-platform-admin
rules:
  - apiGroups: [""]
    resources: ["namespaces"]
    verbs: ["get", "list"]
    resourceNames: ["ml-training", "ml-inference", "mlflow", "feast"]
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["*"]
---
# Read-only access for data scientists
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ml-readonly
  namespace: ml-training
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["get", "list", "watch"]
---
# Service Account for inference pods
apiVersion: v1
kind: ServiceAccount
metadata:
  name: model-server-sa
  namespace: ml-inference
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/model-server-role
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: model-server-binding
  namespace: ml-inference
subjects:
  - kind: ServiceAccount
    name: model-server-sa
    namespace: ml-inference
roleRef:
  kind: Role
  name: ml-inference-role
  apiGroup: rbac.authorization.k8s.io
```

### Secrets Management with External Secrets

```yaml
# kubernetes/secrets/external-secrets.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: ml-model-credentials
  namespace: ml-inference
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore

  target:
    name: model-credentials
    creationPolicy: Owner

  data:
    - secretKey: mlflow_tracking_token
      remoteRef:
        key: ml-platform/mlflow
        property: tracking_token

    - secretKey: s3_access_key
      remoteRef:
        key: ml-platform/s3
        property: access_key

    - secretKey: s3_secret_key
      remoteRef:
        key: ml-platform/s3
        property: secret_key
---
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-west-2
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
            namespace: external-secrets
```

---

## Module 5: Disaster Recovery

### Backup Strategy

```yaml
backup_strategy:
  model_artifacts:
    storage: s3://ml-backups/models
    retention: 90_days
    replication: cross_region

  training_data:
    storage: s3://ml-backups/data
    retention: 365_days
    incremental: daily
    full: weekly

  cluster_state:
    tool: velero
    schedule: "0 */6 * * *"
    retention: 30_days

  secrets:
    tool: external_secrets
    backup: aws_secrets_manager
    replication: multi_region
```

### Velero Backup Configuration

```yaml
# velero/backup-schedule.yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: ml-platform-backup
  namespace: velero
spec:
  schedule: "0 */6 * * *"
  template:
    includedNamespaces:
      - ml-training
      - ml-inference
      - mlflow
      - feast
    excludedResources:
      - pods
      - events
    storageLocation: aws-backup
    volumeSnapshotLocations:
      - aws-snapshots
    ttl: 720h  # 30 days
    hooks:
      resources:
        - name: mlflow-backup-hook
          includedNamespaces:
            - mlflow
          pre:
            - exec:
                container: mlflow
                command:
                  - /bin/sh
                  - -c
                  - "mlflow gc --backend-store-uri $MLFLOW_BACKEND_STORE"
---
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: aws-backup
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: ml-platform-backups
    prefix: velero
  config:
    region: us-west-2
    s3ForcePathStyle: "true"
```

### Disaster Recovery Runbook

```python
"""
Disaster recovery automation for ML infrastructure.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import subprocess
import json

@dataclass
class RecoveryStep:
    """Single recovery step."""
    name: str
    command: str
    timeout_seconds: int
    rollback_command: Optional[str] = None
    validation_command: Optional[str] = None

@dataclass
class RecoveryPlan:
    """Complete recovery plan."""
    name: str
    rto_minutes: int  # Recovery Time Objective
    rpo_minutes: int  # Recovery Point Objective
    steps: List[RecoveryStep]

class DisasterRecoveryAutomation:
    """Automate disaster recovery procedures."""

    def __init__(self):
        self.recovery_plans = self._define_plans()
        self.execution_log: List[Dict] = []

    def _define_plans(self) -> Dict[str, RecoveryPlan]:
        """Define recovery plans."""
        return {
            "cluster_failure": RecoveryPlan(
                name="Full Cluster Recovery",
                rto_minutes=60,
                rpo_minutes=360,
                steps=[
                    RecoveryStep(
                        name="Verify backup availability",
                        command="velero backup get --selector app=ml-platform",
                        timeout_seconds=60
                    ),
                    RecoveryStep(
                        name="Create new EKS cluster",
                        command="terraform apply -auto-approve -target=module.eks",
                        timeout_seconds=1800,
                        rollback_command="terraform destroy -auto-approve -target=module.eks"
                    ),
                    RecoveryStep(
                        name="Install cluster addons",
                        command="helm upgrade --install -f values.yaml",
                        timeout_seconds=300
                    ),
                    RecoveryStep(
                        name="Restore from Velero backup",
                        command="velero restore create --from-backup ml-platform-backup-latest",
                        timeout_seconds=600,
                        validation_command="kubectl get pods -A | grep -v Running"
                    ),
                    RecoveryStep(
                        name="Verify model serving",
                        command="curl -f http://model-server/health",
                        timeout_seconds=60
                    ),
                    RecoveryStep(
                        name="Run smoke tests",
                        command="pytest tests/smoke/ -v",
                        timeout_seconds=300
                    )
                ]
            ),
            "model_corruption": RecoveryPlan(
                name="Model Artifact Recovery",
                rto_minutes=15,
                rpo_minutes=60,
                steps=[
                    RecoveryStep(
                        name="Identify last good model version",
                        command="mlflow models list --filter 'status=READY'",
                        timeout_seconds=30
                    ),
                    RecoveryStep(
                        name="Rollback model deployment",
                        command="kubectl rollout undo deployment/model-server -n ml-inference",
                        timeout_seconds=120,
                        validation_command="kubectl rollout status deployment/model-server"
                    ),
                    RecoveryStep(
                        name="Verify model predictions",
                        command="python scripts/validate_model.py",
                        timeout_seconds=60
                    )
                ]
            ),
            "data_pipeline_failure": RecoveryPlan(
                name="Data Pipeline Recovery",
                rto_minutes=30,
                rpo_minutes=1440,
                steps=[
                    RecoveryStep(
                        name="Check pipeline status",
                        command="kubectl get workflows -n ml-training",
                        timeout_seconds=30
                    ),
                    RecoveryStep(
                        name="Restore feature store state",
                        command="feast apply --skip-source-validation",
                        timeout_seconds=120
                    ),
                    RecoveryStep(
                        name="Replay failed data",
                        command="python scripts/replay_data_pipeline.py --from-checkpoint",
                        timeout_seconds=1800
                    )
                ]
            )
        }

    def execute_recovery(
        self,
        plan_name: str,
        dry_run: bool = True
    ) -> Dict:
        """Execute recovery plan."""
        if plan_name not in self.recovery_plans:
            raise ValueError(f"Unknown recovery plan: {plan_name}")

        plan = self.recovery_plans[plan_name]
        start_time = datetime.now()
        results = []

        print(f"\n{'='*60}")
        print(f"Executing Recovery Plan: {plan.name}")
        print(f"RTO: {plan.rto_minutes} minutes | RPO: {plan.rpo_minutes} minutes")
        print(f"{'='*60}\n")

        for i, step in enumerate(plan.steps, 1):
            step_result = {
                "step": i,
                "name": step.name,
                "started_at": datetime.now().isoformat(),
                "dry_run": dry_run
            }

            print(f"[{i}/{len(plan.steps)}] {step.name}")

            if dry_run:
                print(f"  [DRY RUN] Would execute: {step.command}")
                step_result["status"] = "skipped"
            else:
                try:
                    result = subprocess.run(
                        step.command,
                        shell=True,
                        capture_output=True,
                        timeout=step.timeout_seconds
                    )

                    if result.returncode == 0:
                        step_result["status"] = "success"
                        step_result["output"] = result.stdout.decode()
                        print(f"  [SUCCESS]")
                    else:
                        step_result["status"] = "failed"
                        step_result["error"] = result.stderr.decode()
                        print(f"  [FAILED] {result.stderr.decode()}")

                        if step.rollback_command:
                            print(f"  Executing rollback...")
                            subprocess.run(step.rollback_command, shell=True)

                        break

                except subprocess.TimeoutExpired:
                    step_result["status"] = "timeout"
                    print(f"  [TIMEOUT] Step exceeded {step.timeout_seconds}s")
                    break

            step_result["completed_at"] = datetime.now().isoformat()
            results.append(step_result)

        elapsed = (datetime.now() - start_time).total_seconds() / 60

        summary = {
            "plan": plan_name,
            "started_at": start_time.isoformat(),
            "elapsed_minutes": elapsed,
            "within_rto": elapsed <= plan.rto_minutes,
            "steps": results,
            "success": all(r.get("status") in ["success", "skipped"] for r in results)
        }

        self.execution_log.append(summary)

        print(f"\n{'='*60}")
        print(f"Recovery {'completed' if summary['success'] else 'FAILED'}")
        print(f"Elapsed: {elapsed:.1f} minutes (RTO: {plan.rto_minutes} min)")
        print(f"{'='*60}\n")

        return summary


# Usage
if __name__ == "__main__":
    dr = DisasterRecoveryAutomation()

    # Dry run cluster recovery
    result = dr.execute_recovery("cluster_failure", dry_run=True)
    print(json.dumps(result, indent=2))
```

---

## Troubleshooting Guide

### Common Issues

#### Issue: GPU Nodes Not Scaling

**Symptoms**:
- Pending pods with GPU requests
- Karpenter not provisioning GPU nodes

**Diagnosis**:
```bash
# Check Karpenter logs
kubectl logs -n karpenter -l app.kubernetes.io/name=karpenter -c controller

# Check node pool status
kubectl get nodepools
kubectl describe nodepool ml-gpu-nodepool

# Check instance availability
aws ec2 describe-instance-type-offerings \
  --location-type availability-zone \
  --filters Name=instance-type,Values=p4d.24xlarge
```

**Resolution**:
1. Verify GPU quota in AWS account
2. Check instance type availability in AZs
3. Add fallback instance types to node pool
4. Review Karpenter provisioner constraints

#### Issue: High Inference Latency

**Symptoms**:
- P99 latency exceeding SLA
- Model server showing high queue depth

**Diagnosis**:
```bash
# Check pod resource usage
kubectl top pods -n ml-inference

# Check GPU utilization
kubectl exec -it model-server-xxx -- nvidia-smi

# Review HPA status
kubectl get hpa -n ml-inference
kubectl describe hpa inference-hpa
```

**Resolution**:
1. Increase replica count or adjust HPA thresholds
2. Enable GPU memory optimization
3. Review batch size configuration
4. Check for cold start issues

#### Issue: Cost Overruns

**Symptoms**:
- Monthly bill exceeding budget
- Unused resources running

**Diagnosis**:
```bash
# Check idle resources
kubectl get pods --all-namespaces -o json | \
  jq '.items[] | select(.status.phase=="Running") |
  {name: .metadata.name, cpu: .spec.containers[].resources.requests.cpu}'

# Review Spot instance usage
kubectl get nodes -l karpenter.sh/capacity-type=spot

# Check for orphaned resources
aws ec2 describe-volumes --filters Name=status,Values=available
```

**Resolution**:
1. Implement scheduled scaling for non-production hours
2. Increase Spot instance usage for training
3. Enable cluster autoscaler aggressive scale-down
4. Set up cost alerts and budgets

### Debug Checklist

```yaml
infrastructure_debug_checklist:
  cluster_health:
    - [ ] All control plane components healthy
    - [ ] Node pools have available capacity
    - [ ] CNI plugin functioning
    - [ ] CoreDNS resolving correctly

  gpu_workloads:
    - [ ] NVIDIA device plugin running
    - [ ] GPU resources visible in nodes
    - [ ] CUDA drivers compatible
    - [ ] NCCL communication working

  networking:
    - [ ] Network policies not blocking traffic
    - [ ] Service mesh healthy (if used)
    - [ ] Ingress controller functioning
    - [ ] DNS resolution working

  storage:
    - [ ] PVCs bound successfully
    - [ ] EBS CSI driver healthy
    - [ ] S3 access configured
    - [ ] Storage quotas not exceeded

  security:
    - [ ] RBAC policies correct
    - [ ] Service accounts configured
    - [ ] Secrets accessible
    - [ ] Pod security standards enforced
```

---

## Quick Reference

### Essential Commands

```bash
# Cluster management
eksctl get cluster
kubectl get nodes -o wide
kubectl top nodes

# GPU debugging
kubectl get nodes -l nvidia.com/gpu.present=true
kubectl describe node <gpu-node> | grep -A10 "Allocated resources"

# Karpenter operations
kubectl get nodeclaims
kubectl get nodepools
kubectl logs -n karpenter -l app.kubernetes.io/name=karpenter

# Cost analysis
kubectl cost --show-all-resources
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-01-31

# Backup/restore
velero backup get
velero restore create --from-backup <backup-name>
```

### Instance Type Reference

```yaml
gpu_instances:
  training:
    - p4d.24xlarge: "8x A100 40GB, 96 vCPU, 1.5TB RAM"
    - p4de.24xlarge: "8x A100 80GB, 96 vCPU, 1.5TB RAM"
    - p5.48xlarge: "8x H100, 192 vCPU, 2TB RAM"

  inference:
    - g5.xlarge: "1x A10G 24GB, 4 vCPU, 16GB RAM"
    - g5.2xlarge: "1x A10G 24GB, 8 vCPU, 32GB RAM"
    - inf2.xlarge: "1x Inferentia2, 4 vCPU, 16GB RAM"

  cost_per_hour:
    p4d.24xlarge: $32.77
    p5.48xlarge: $98.32
    g5.xlarge: $1.01
```

### Integration Points

```yaml
upstream_dependencies:
  - cloud_provider: AWS/GCP/Azure
  - container_registry: ECR/GCR/ACR
  - secrets_manager: AWS Secrets Manager

downstream_consumers:
  - ml_training: Kubeflow
  - ml_inference: BentoML, Triton
  - monitoring: Prometheus, Grafana
  - ci_cd: GitHub Actions, ArgoCD
```
