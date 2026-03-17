---
name: ecs-fargate
description: AWS Fargate serverless container compute for ECS. Covers Fargate vs EC2 decision guide, CPU/memory sizing, platform versions, Fargate Spot cost optimization, Graviton/ARM architecture, networking, and EFS integration. Use when deploying serverless containers, optimizing Fargate costs, sizing Fargate tasks, or choosing between Fargate and EC2 launch types.
---

# AWS Fargate for ECS

Complete guide to AWS Fargate serverless container compute, including sizing, optimization, and best practices.

## Quick Reference

| Aspect | Fargate | EC2 |
|--------|---------|-----|
| Management | Serverless | Manual |
| Scaling | Automatic | ASG-based |
| Pricing | Per vCPU-second | Per instance-hour |
| Overhead | None | High |
| Control | Limited | Full |
| Best For | Variable load | Steady state |

## When to Use Fargate

**Use Fargate when:**
- Team prioritizes operational simplicity
- Variable or unpredictable traffic
- Microservices architecture
- Rapid scaling needed
- Development/testing environments
- No specific instance type requirements

**Use EC2 when:**
- Steady-state, predictable workloads
- Cost optimization is critical (>60% utilization)
- Need specific instance types (GPU, high memory)
- Existing Reserved Instance commitments
- Custom AMI requirements

## CPU and Memory Configurations

### Valid Combinations

| CPU (vCPU) | Memory Options |
|------------|----------------|
| 0.25 | 512 MB, 1 GB, 2 GB |
| 0.5 | 1 GB - 4 GB (1 GB increments) |
| 1 | 2 GB - 8 GB (1 GB increments) |
| 2 | 4 GB - 16 GB (1 GB increments) |
| 4 | 8 GB - 30 GB (1 GB increments) |
| 8 | 16 GB - 60 GB (4 GB increments) |
| 16 | 32 GB - 120 GB (8 GB increments) |

### Sizing Guidelines

```python
# Sizing decision tree
def recommend_fargate_size(app_type: str, expected_memory_mb: int):
    """Recommend Fargate CPU/Memory based on workload"""

    if app_type == "web_api":
        # Typically CPU-bound
        if expected_memory_mb <= 512:
            return {"cpu": "256", "memory": "512"}
        elif expected_memory_mb <= 1024:
            return {"cpu": "512", "memory": "1024"}
        else:
            return {"cpu": "1024", "memory": str(min(expected_memory_mb, 2048))}

    elif app_type == "worker":
        # Typically memory-bound
        return {"cpu": "256", "memory": str(max(512, expected_memory_mb))}

    elif app_type == "batch":
        # Need burst capacity
        return {"cpu": "1024", "memory": str(max(2048, expected_memory_mb))}

    # Default conservative
    return {"cpu": "512", "memory": "1024"}
```

### Cost-Effective Sizing

```hcl
# Development: Minimum viable
cpu    = "256"
memory = "512"

# Small API: Balanced
cpu    = "512"
memory = "1024"

# Production API: Standard
cpu    = "1024"
memory = "2048"

# Memory-intensive: Data processing
cpu    = "1024"
memory = "4096"

# Compute-intensive: ML inference
cpu    = "4096"
memory = "8192"
```

## Platform Versions

### Current Versions (2025)

| Version | Status | Features |
|---------|--------|----------|
| 1.4.0 | **Recommended** | containerd runtime, jumbo frames, UDP support |
| 1.3.0 | Deprecated (Mar 2026) | Docker runtime |
| LATEST | Auto-updates | Always latest revision |

### Configuration

```hcl
# Always pin explicitly
resource "aws_ecs_service" "app" {
  platform_version = "1.4.0"  # NOT "LATEST"
  # ...
}
```

```python
# Boto3
ecs.create_service(
    platformVersion='1.4.0',
    # ...
)
```

## Fargate Spot (Cost Optimization)

### Overview

- **Up to 70% savings** vs on-demand
- **2-minute termination notice** when capacity needed
- **Best for:** Batch jobs, CI/CD, fault-tolerant workloads

### Configuration

```hcl
# Mixed strategy: reliable baseline + cost-effective scaling
resource "aws_ecs_service" "app" {
  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 1
    base              = 2  # Always keep 2 on-demand
  }

  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = 4  # 4x weight = ~80% on Spot
  }
}
```

```python
# Boto3
ecs.create_service(
    capacityProviderStrategy=[
        {'capacityProvider': 'FARGATE', 'weight': 1, 'base': 2},
        {'capacityProvider': 'FARGATE_SPOT', 'weight': 4}
    ],
    # ...
)
```

### Handling Spot Interruptions

```python
# Application-level graceful shutdown
import signal
import sys

def shutdown_handler(signum, frame):
    print("Received termination signal, shutting down gracefully...")
    # Drain connections
    # Complete in-flight requests
    # Save state if needed
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
```

## ARM/Graviton (20% Cost Savings)

### Benefits

- **~20% cost reduction** vs x86
- **Up to 40% better performance** for many workloads
- **Same API** - just change task definition

### Configuration

```hcl
resource "aws_ecs_task_definition" "app" {
  family                   = "my-app"
  requires_compatibilities = ["FARGATE"]

  # ARM architecture
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"  # or "X86_64"
  }

  # ...
}
```

### Multi-Architecture Images

```dockerfile
# Dockerfile supporting both architectures
FROM --platform=$TARGETPLATFORM python:3.11-slim

# Build for multiple platforms
# docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

```bash
# Build and push multi-arch image
docker buildx create --use
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest .
```

## Networking (awsvpc Mode)

### Task-Level Networking

Each Fargate task gets its own ENI with:
- Unique private IP
- Dedicated security group
- Full network isolation

```hcl
resource "aws_ecs_service" "app" {
  network_configuration {
    subnets          = var.private_subnets
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false  # Use NAT for outbound
  }
}
```

### VPC Endpoints (Recommended)

```hcl
# Avoid NAT costs for AWS services
resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id            = module.vpc.vpc_id
  service_name      = "com.amazonaws.${var.region}.ecr.api"
  vpc_endpoint_type = "Interface"
  subnet_ids        = module.vpc.private_subnets
}

resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id            = module.vpc.vpc_id
  service_name      = "com.amazonaws.${var.region}.ecr.dkr"
  vpc_endpoint_type = "Interface"
  subnet_ids        = module.vpc.private_subnets
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id       = module.vpc.vpc_id
  service_name = "com.amazonaws.${var.region}.s3"
}

resource "aws_vpc_endpoint" "logs" {
  vpc_id            = module.vpc.vpc_id
  service_name      = "com.amazonaws.${var.region}.logs"
  vpc_endpoint_type = "Interface"
  subnet_ids        = module.vpc.private_subnets
}
```

## EFS Integration (Persistent Storage)

### Configuration

```hcl
# EFS File System
resource "aws_efs_file_system" "app" {
  creation_token = "app-storage"
  encrypted      = true

  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS"
  }
}

resource "aws_efs_mount_target" "app" {
  count           = length(var.private_subnets)
  file_system_id  = aws_efs_file_system.app.id
  subnet_id       = var.private_subnets[count.index]
  security_groups = [aws_security_group.efs.id]
}

# Task Definition with EFS
resource "aws_ecs_task_definition" "app" {
  family = "my-app"

  volume {
    name = "app-storage"

    efs_volume_configuration {
      file_system_id          = aws_efs_file_system.app.id
      root_directory          = "/app-data"
      transit_encryption      = "ENABLED"
      authorization_config {
        access_point_id = aws_efs_access_point.app.id
        iam             = "ENABLED"
      }
    }
  }

  container_definitions = jsonencode([
    {
      name = "my-app"
      mountPoints = [
        {
          sourceVolume  = "app-storage"
          containerPath = "/data"
          readOnly      = false
        }
      ]
      # ...
    }
  ])
}
```

## Ephemeral Storage

### Default and Configurable

```hcl
# Default: 20 GB, configurable up to 200 GB
resource "aws_ecs_task_definition" "app" {
  ephemeral_storage {
    size_in_gib = 100  # For large temp files
  }
}
```

## Cost Optimization Summary

| Strategy | Savings | Effort |
|----------|---------|--------|
| Fargate Spot | 70% | Low |
| ARM/Graviton | 20% | Medium |
| Right-sizing | 10-50% | Medium |
| Compute Savings Plans | 50% | Low |
| Schedule-based scaling | 30-60% | Medium |

### Cost Calculation

```python
def estimate_monthly_cost(cpu_vcpu: float, memory_gb: float,
                          hours_per_month: int = 730,
                          spot_percentage: float = 0.0):
    """Estimate monthly Fargate cost (us-east-1 pricing)"""

    # On-demand pricing (approximate)
    cpu_rate = 0.04048  # per vCPU-hour
    memory_rate = 0.004445  # per GB-hour

    on_demand_hours = hours_per_month * (1 - spot_percentage)
    spot_hours = hours_per_month * spot_percentage

    # Spot is ~70% cheaper
    cpu_cost = (cpu_vcpu * cpu_rate * on_demand_hours) + \
               (cpu_vcpu * cpu_rate * 0.3 * spot_hours)
    memory_cost = (memory_gb * memory_rate * on_demand_hours) + \
                  (memory_gb * memory_rate * 0.3 * spot_hours)

    return cpu_cost + memory_cost

# Example: 1 vCPU, 2 GB, 50% Spot
cost = estimate_monthly_cost(1, 2, spot_percentage=0.5)
print(f"Estimated monthly cost: ${cost:.2f}")  # ~$25
```

## Progressive Disclosure

### Quick Start (This File)
- Fargate vs EC2 decision
- CPU/Memory sizing
- Platform versions
- Cost optimization basics

### Detailed References
- **[Sizing Guide](references/sizing-guide.md)**: Detailed sizing strategies
- **[Networking](references/networking.md)**: VPC, security groups, endpoints
- **[Storage](references/storage.md)**: EFS, ephemeral storage patterns

## Related Skills

- **boto3-ecs**: SDK patterns for ECS
- **terraform-ecs**: Infrastructure as Code
- **ecs-deployment**: Deployment strategies
- **ecs-troubleshooting**: Debugging guide

## Best Practices

1. **Start small, scale up** - Begin with 0.25 vCPU/512 MB and increase based on metrics
2. **Use Fargate Spot** for non-critical workloads (70% savings)
3. **Consider ARM/Graviton** for compatible workloads (20% savings)
4. **Pin platform version** explicitly (e.g., "1.4.0")
5. **Use VPC endpoints** to reduce NAT costs
6. **Enable Container Insights** for visibility
7. **Right-size continuously** using CloudWatch metrics
8. **Use capacity provider strategy** instead of launch type
