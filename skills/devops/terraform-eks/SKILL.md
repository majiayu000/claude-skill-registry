---
name: terraform-eks
description: Provision production-ready AWS EKS clusters with Terraform. Covers cluster configuration, managed node groups, Fargate profiles, IRSA, EKS add-ons (CoreDNS, kube-proxy, VPC CNI, EBS CSI), VPC integration, and security best practices. Use when provisioning EKS, setting up Kubernetes on AWS, configuring node groups, implementing IRSA, or managing EKS infrastructure as code.
---

# Terraform EKS Cluster Provisioning

Production-ready patterns for provisioning AWS EKS clusters with Terraform using the official terraform-aws-modules/eks module.

## Quick Reference

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize Terraform working directory |
| `terraform plan` | Preview infrastructure changes |
| `terraform apply` | Create/update EKS cluster |
| `terraform destroy` | Delete EKS cluster and resources |
| `aws eks update-kubeconfig --name <cluster>` | Configure kubectl access |
| `terraform output` | View cluster outputs |
| `terraform state list` | List managed resources |

## Version Requirements

```hcl
terraform {
  required_version = ">= 1.11.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.35"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.16"
    }
  }
}
```

## Basic EKS Cluster Example

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  cluster_name    = "production-eks"
  cluster_version = "1.33"

  # VPC configuration
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Cluster access
  cluster_endpoint_public_access  = false
  cluster_endpoint_private_access = true

  # Enable IRSA
  enable_irsa = true

  # Cluster encryption
  cluster_encryption_config = {
    resources        = ["secrets"]
    provider_key_arn = aws_kms_key.eks.arn
  }

  # EKS add-ons
  cluster_addons = {
    coredns = {
      addon_version     = "v1.11.3-eksbuild.2"
      resolve_conflicts = "OVERWRITE"
    }
    kube-proxy = {
      addon_version = "v1.33.1-eksbuild.1"
    }
    vpc-cni = {
      addon_version = "v1.19.2-eksbuild.1"
      configuration_values = jsonencode({
        env = {
          ENABLE_PREFIX_DELEGATION = "true"
        }
      })
    }
    aws-ebs-csi-driver = {
      addon_version            = "v1.38.2-eksbuild.1"
      service_account_role_arn = module.ebs_csi_irsa.iam_role_arn
    }
  }

  # Managed node groups
  eks_managed_node_groups = {
    general = {
      instance_types = ["t3.large"]
      min_size       = 2
      max_size       = 10
      desired_size   = 3

      labels = {
        role = "general"
      }
    }
  }

  tags = {
    Environment = "production"
    Terraform   = "true"
  }
}
```

## Managed Node Groups

### On-Demand Nodes

```hcl
eks_managed_node_groups = {
  general = {
    name           = "general-nodes"
    instance_types = ["m5.xlarge"]

    min_size     = 3
    max_size     = 20
    desired_size = 5

    capacity_type = "ON_DEMAND"
    ami_type      = "AL2023_x86_64_STANDARD"

    # Disk configuration
    block_device_mappings = {
      xvda = {
        device_name = "/dev/xvda"
        ebs = {
          volume_size = 100
          volume_type = "gp3"
          encrypted   = true
        }
      }
    }

    labels = {
      role = "general"
    }

    tags = {
      "k8s.io/cluster-autoscaler/enabled" = "true"
    }
  }
}
```

### Spot Instances

```hcl
spot = {
  instance_types = ["t3.large", "t3a.large"]
  min_size       = 0
  max_size       = 5
  desired_size   = 2

  capacity_type = "SPOT"

  labels = {
    workload = "batch"
  }

  taints = [{
    key    = "spot"
    value  = "true"
    effect = "NoSchedule"
  }]
}
```

## Fargate Profiles

```hcl
fargate_profiles = {
  kube_system = {
    name = "kube-system"
    selectors = [
      {
        namespace = "kube-system"
        labels = {
          k8s-app = "kube-dns"
        }
      }
    ]
    subnet_ids = module.vpc.private_subnets
  }

  application = {
    name = "app"
    selectors = [
      {
        namespace = "production"
      },
      {
        namespace = "staging"
        labels = {
          compute = "fargate"
        }
      }
    ]
  }
}
```

## IRSA (IAM Roles for Service Accounts)

```hcl
# Enable IRSA in EKS module
module "eks" {
  enable_irsa = true
}

# Create IAM role for service account
module "ebs_csi_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name             = "ebs-csi-controller"
  attach_ebs_csi_policy = true

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:ebs-csi-controller-sa"]
    }
  }
}

# Kubernetes service account
resource "kubernetes_service_account" "ebs_csi" {
  metadata {
    name      = "ebs-csi-controller-sa"
    namespace = "kube-system"
    annotations = {
      "eks.amazonaws.com/role-arn" = module.ebs_csi_irsa.iam_role_arn
    }
  }
}
```

## EKS Add-ons

```hcl
cluster_addons = {
  # CoreDNS for cluster DNS
  coredns = {
    addon_version     = "v1.11.3-eksbuild.2"
    resolve_conflicts = "OVERWRITE"
    configuration_values = jsonencode({
      computeType = "Fargate"
      resources = {
        limits = {
          cpu    = "100m"
          memory = "150Mi"
        }
      }
    })
  }

  # VPC CNI for pod networking
  vpc-cni = {
    addon_version = "v1.19.2-eksbuild.1"
    configuration_values = jsonencode({
      env = {
        ENABLE_PREFIX_DELEGATION = "true"
        ENABLE_POD_ENI          = "true"
      }
    })
    service_account_role_arn = module.vpc_cni_irsa.iam_role_arn
  }

  # EBS CSI Driver for persistent volumes
  aws-ebs-csi-driver = {
    addon_version            = "v1.38.2-eksbuild.1"
    service_account_role_arn = module.ebs_csi_irsa.iam_role_arn
  }

  # EFS CSI Driver for shared storage
  aws-efs-csi-driver = {
    addon_version            = "v2.1.3-eksbuild.1"
    service_account_role_arn = module.efs_csi_irsa.iam_role_arn
  }
}
```

## VPC Integration

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "eks-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false  # One per AZ for HA

  # Required tags for EKS
  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
}
```

## Private Cluster Configuration

```hcl
module "eks" {
  source = "terraform-aws-modules/eks/aws"

  # Private cluster
  cluster_endpoint_public_access  = false
  cluster_endpoint_private_access = true

  # Control plane subnets
  control_plane_subnet_ids = module.vpc.intra_subnets
  subnet_ids               = module.vpc.private_subnets
}

# VPC endpoints required for private clusters
module "vpc_endpoints" {
  source = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"

  vpc_id = module.vpc.vpc_id

  endpoints = {
    s3 = {
      service      = "s3"
      service_type = "Gateway"
    }
    ecr_api = {
      service             = "ecr.api"
      private_dns_enabled = true
      subnet_ids          = module.vpc.private_subnets
    }
    ecr_dkr = {
      service             = "ecr.dkr"
      private_dns_enabled = true
      subnet_ids          = module.vpc.private_subnets
    }
  }
}
```

## Detailed Documentation

For comprehensive guides, see:

- **[Cluster Configuration](references/cluster-config.md)** - Complete cluster setup, authentication modes, encryption
- **[Node Groups](references/node-groups.md)** - Managed, self-managed, and Fargate patterns
- **[Add-ons & IRSA](references/addons-irsa.md)** - EKS add-ons, IRSA setup, service account configuration

## Common Patterns

### Update kubeconfig

```bash
aws eks update-kubeconfig --name production-eks --region us-east-1
```

### Access Private Cluster

```bash
# Via AWS Systems Manager (no SSH)
aws ssm start-session --target i-bastion-instance-id

# Configure kubectl on bastion
aws eks update-kubeconfig --name production-eks --region us-east-1
kubectl get nodes
```

### Check Cluster Status

```bash
# Get cluster info
terraform output cluster_name
terraform output cluster_endpoint

# Verify add-ons
kubectl get daemonsets -n kube-system
kubectl get pods -n kube-system
```

## Best Practices

1. **Always use private clusters** for production (public_access = false)
2. **Enable IRSA** for pod-level IAM permissions (enable_irsa = true)
3. **Encrypt secrets** with KMS (cluster_encryption_config)
4. **Use managed node groups** unless you need custom AMIs
5. **Tag everything** for cost tracking and organization
6. **Separate state files** by component (VPC, EKS, add-ons)
7. **Use VPC endpoints** for private cluster access
8. **Implement lifecycle policies** (prevent_destroy for critical resources)

## References

- [terraform-aws-modules/eks](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest)
- [HashiCorp EKS Tutorial](https://developer.hashicorp.com/terraform/tutorials/kubernetes/eks)
- [AWS EKS Best Practices](https://aws.github.io/aws-eks-best-practices/)
