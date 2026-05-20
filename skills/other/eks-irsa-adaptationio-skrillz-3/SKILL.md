---
name: eks-irsa
description: IAM Roles for Service Accounts (IRSA) for EKS pod-level AWS permissions. Use when configuring pod IAM access, setting up AWS service integrations, implementing least-privilege security, troubleshooting OIDC trust relationships, or deploying AWS controllers.
---

# EKS IAM Roles for Service Accounts (IRSA)

## Overview

Comprehensive guide for implementing IAM Roles for Service Accounts (IRSA) in Amazon EKS. IRSA enables fine-grained IAM permissions at the pod level using OpenID Connect (OIDC) federation, eliminating the need for node-level IAM credentials and enabling least-privilege security.

**Keywords**: IRSA, IAM Roles for Service Accounts, EKS security, OIDC provider, pod IAM permissions, service account annotations, least privilege, AWS integration, trust policy, cross-account access

**Status**: Production-ready (2025 best practices)

## When to Use This Skill

- Setting up pod-level AWS permissions in EKS
- Configuring AWS service integrations (S3, DynamoDB, Secrets Manager, SQS, SNS)
- Installing EKS add-ons (AWS Load Balancer Controller, EBS CSI Driver, External DNS)
- Implementing least-privilege security architecture
- Troubleshooting OIDC trust relationship issues
- Cross-account IAM role assumption from EKS
- Migrating from node IAM roles to pod-level permissions
- Blue/green cluster upgrades with IRSA

## What is IRSA?

**IAM Roles for Service Accounts (IRSA)** allows Kubernetes workloads to assume IAM roles securely without relying on node-level credentials.

### How IRSA Works

```
1. Pod starts with annotated ServiceAccount
2. EKS mutating webhook injects AWS_WEB_IDENTITY_TOKEN_FILE
3. AWS SDK reads JWT token from injected file
4. SDK calls STS::AssumeRoleWithWebIdentity
5. OIDC provider validates token against trust policy
6. Temporary credentials issued (automatically rotated)
7. Pod uses scoped IAM permissions
```

### Key Benefits

**Security:**
- Pod-level permissions (not node-level)
- Prevents privilege escalation
- Automatic credential rotation
- No long-lived credentials

**Compliance:**
- Least-privilege principle
- Audit trail via CloudTrail
- Compliance requirements met
- Fine-grained access control

**Operational:**
- Each app gets own IAM role
- Modify permissions without node changes
- Better resource isolation
- Supports multi-tenancy

## Quick Start

### Prerequisites

1. **OIDC Provider Enabled** (automatic with terraform-aws-modules/eks)
2. **IAM Role Created** with trust policy for OIDC
3. **ServiceAccount Annotated** with role ARN
4. **Pod Configured** to use ServiceAccount

### 30-Second Setup (Terraform)

```hcl
# 1. Enable IRSA in EKS module (automatic OIDC setup)
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name = "production"
  enable_irsa  = true  # Creates OIDC provider automatically
}

# 2. Create IAM role for S3 access
module "s3_access_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = "my-app-s3-access"

  role_policy_arns = {
    s3_read = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
  }

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["production:my-app-sa"]
    }
  }
}

# 3. Create Kubernetes ServiceAccount
resource "kubernetes_service_account" "my_app" {
  metadata {
    name      = "my-app-sa"
    namespace = "production"
    annotations = {
      "eks.amazonaws.com/role-arn" = module.s3_access_irsa.iam_role_arn
    }
  }
}

# 4. Use ServiceAccount in pod
resource "kubernetes_deployment" "my_app" {
  spec {
    template {
      spec {
        service_account_name = "my-app-sa"  # ✅ IRSA enabled!

        containers {
          name  = "app"
          image = "my-app:latest"
          # AWS SDK automatically uses IRSA credentials
        }
      }
    }
  }
}
```

### Verify IRSA Setup

```bash
# Check OIDC provider exists
aws iam list-open-id-connect-providers

# Verify IAM role trust policy
aws iam get-role --role-name my-app-s3-access

# Test from pod
kubectl exec -it my-pod -- env | grep AWS
# Should show:
# AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
# AWS_ROLE_ARN=arn:aws:iam::123456789012:role/my-app-s3-access

# Test AWS access
kubectl exec -it my-pod -- aws s3 ls
```

## Common IRSA Patterns

### 1. AWS Load Balancer Controller

**What it needs**: Create/manage ALBs and NLBs

```hcl
module "lb_controller_irsa" {
  source = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"

  role_name                              = "aws-load-balancer-controller"
  attach_load_balancer_controller_policy = true  # Pre-built policy!

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:aws-load-balancer-controller"]
    }
  }
}
```

### 2. EBS CSI Driver

**What it needs**: Create/attach/delete EBS volumes

```hcl
module "ebs_csi_irsa" {
  source = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"

  role_name             = "ebs-csi-controller"
  attach_ebs_csi_policy = true  # Pre-built policy!

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:ebs-csi-controller-sa"]
    }
  }
}
```

### 3. External DNS

**What it needs**: Manage Route53 records

```hcl
module "external_dns_irsa" {
  source = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"

  role_name                     = "external-dns"
  attach_external_dns_policy    = true  # Pre-built policy!
  external_dns_hosted_zone_arns = ["arn:aws:route53:::hostedzone/Z123456789"]

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:external-dns"]
    }
  }
}
```

### 4. Cluster Autoscaler

**What it needs**: Modify Auto Scaling Groups

```hcl
module "cluster_autoscaler_irsa" {
  source = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"

  role_name                        = "cluster-autoscaler"
  attach_cluster_autoscaler_policy = true  # Pre-built policy!
  cluster_autoscaler_cluster_names = [module.eks.cluster_name]

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:cluster-autoscaler"]
    }
  }
}
```

### 5. Karpenter (Recommended Autoscaler)

**What it needs**: Provision EC2 instances, manage instance profiles

```hcl
module "karpenter" {
  source = "terraform-aws-modules/eks/aws//modules/karpenter"

  cluster_name           = module.eks.cluster_name
  irsa_oidc_provider_arn = module.eks.oidc_provider_arn

  # Includes pre-configured IRSA role!
}
```

### 6. External Secrets Operator

**What it needs**: Read secrets from AWS Secrets Manager

```hcl
module "external_secrets_irsa" {
  source = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"

  role_name                      = "external-secrets"
  attach_external_secrets_policy = true  # Pre-built policy!

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:external-secrets"]
    }
  }
}
```

### 7. Custom Application (S3 + DynamoDB)

```hcl
module "app_irsa" {
  source = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"

  role_name = "my-app"

  role_policy_arns = {
    s3       = aws_iam_policy.app_s3_policy.arn
    dynamodb = aws_iam_policy.app_dynamodb_policy.arn
  }

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["production:my-app-sa"]
    }
  }
}

# Custom policies with least privilege
resource "aws_iam_policy" "app_s3_policy" {
  name = "my-app-s3-access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "arn:aws:s3:::my-bucket/my-app/*"
      }
    ]
  })
}
```

## Application Code Examples

### Python (Boto3)

```python
import boto3

# AWS SDK automatically detects IRSA credentials
# No configuration needed!

s3 = boto3.client('s3')
response = s3.list_buckets()
print(response['Buckets'])

# The SDK:
# 1. Reads AWS_WEB_IDENTITY_TOKEN_FILE env var
# 2. Reads AWS_ROLE_ARN env var
# 3. Calls STS::AssumeRoleWithWebIdentity
# 4. Uses temporary credentials automatically
```

### Node.js (AWS SDK v3)

```javascript
import { S3Client, ListBucketsCommand } from "@aws-sdk/client-s3";

// AWS SDK automatically detects IRSA credentials
const s3Client = new S3Client({ region: "us-east-1" });

const response = await s3Client.send(new ListBucketsCommand({}));
console.log(response.Buckets);
```

### Go (AWS SDK v2)

```go
import (
    "context"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/service/s3"
)

func main() {
    // AWS SDK automatically detects IRSA credentials
    cfg, _ := config.LoadDefaultConfig(context.TODO())
    client := s3.NewFromConfig(cfg)

    resp, _ := client.ListBuckets(context.TODO(), &s3.ListBucketsInput{})
    fmt.Println(resp.Buckets)
}
```

## Detailed Documentation

For in-depth guides on specific IRSA topics:

- **OIDC Setup**: [references/oidc-setup.md](references/oidc-setup.md)
  - OIDC provider configuration
  - Trust relationship anatomy
  - Thumbprint calculation
  - Blue/green cluster upgrades

- **Role Creation**: [references/role-creation.md](references/role-creation.md)
  - IAM role patterns for common services
  - Custom policy examples
  - Session tags for ABAC
  - Cross-account access

- **Pod Configuration**: [references/pod-configuration.md](references/pod-configuration.md)
  - ServiceAccount annotations
  - Pod specifications
  - Environment variables
  - Troubleshooting

## Security Best Practices

### 1. Use Dedicated Service Accounts
```yaml
# ❌ BAD: Sharing service account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: shared-sa  # Used by multiple apps
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123:role/shared-role

# ✅ GOOD: One service account per app
apiVersion: v1
kind: ServiceAccount
metadata:
  name: payment-service-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123:role/payment-service
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: email-service-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123:role/email-service
```

### 2. Restrict IMDS Access

```hcl
# Prevent pods from accessing node IAM credentials
module "eks" {
  source = "terraform-aws-modules/eks/aws"

  eks_managed_node_groups = {
    main = {
      # Require IMDSv2 (prevents container escape to node credentials)
      metadata_options = {
        http_endpoint               = "enabled"
        http_tokens                 = "required"  # IMDSv2 only
        http_put_response_hop_limit = 1
      }
    }
  }
}
```

### 3. Least Privilege Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/my-app/*",
      "Condition": {
        "StringEquals": {
          "aws:PrincipalAccount": "123456789012"
        }
      }
    }
  ]
}
```

### 4. Regular Auditing

```bash
# Find all IRSA roles
aws iam list-roles --query 'Roles[?contains(AssumeRolePolicyDocument.Statement[0].Principal.Federated, `oidc-provider`)]'

# Check CloudTrail for AssumeRoleWithWebIdentity calls
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRoleWithWebIdentity \
  --max-results 50
```

## Troubleshooting Quick Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| `AccessDenied` | Missing IAM permissions | Check role policy allows action |
| `AssumeRoleWithWebIdentity failed` | Trust policy mismatch | Verify OIDC provider ARN matches cluster |
| `InvalidIdentityToken` | Wrong namespace/SA in trust | Check `StringEquals` condition |
| Pod can't assume role | ServiceAccount not annotated | Add `eks.amazonaws.com/role-arn` annotation |
| Using node credentials | Pod not using ServiceAccount | Set `serviceAccountName` in pod spec |
| OIDC provider not found | IRSA not enabled | Set `enable_irsa = true` in EKS module |

## eksctl Quick Setup

```bash
# Create cluster with OIDC enabled
eksctl create cluster \
  --name production \
  --region us-east-1 \
  --with-oidc

# Create IRSA role + ServiceAccount in one command
eksctl create iamserviceaccount \
  --name my-app-sa \
  --namespace production \
  --cluster production \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess \
  --approve

# Verify
kubectl get sa my-app-sa -n production -o yaml
```

## Blue/Green Cluster Upgrades

**Problem**: IRSA trust policies include cluster OIDC endpoint

**Solution**: Update trust policies during upgrade

```hcl
# Support both blue and green clusters temporarily
resource "aws_iam_role" "app" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = [
            module.eks_blue.oidc_provider_arn,   # Old cluster
            module.eks_green.oidc_provider_arn   # New cluster
          ]
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "${module.eks_blue.oidc_provider}:sub"  = "system:serviceaccount:prod:app-sa"
            "${module.eks_green.oidc_provider}:sub" = "system:serviceaccount:prod:app-sa"
          }
        }
      }
    ]
  })
}
```

## EKS Pod Identity (New Alternative)

**Note**: EKS Pod Identity is the new simplified alternative to IRSA (GA 2024).

**Differences**:
- No OIDC provider needed
- Simpler trust policies
- Managed by AWS entirely
- Recommended for new deployments

**IRSA vs Pod Identity**:
- IRSA: Proven, mature, widely used (2019+)
- Pod Identity: Simpler, newer, AWS-managed (2024+)
- Both work, Pod Identity is easier for new clusters

**Migration Path**: Keep IRSA for existing clusters, use Pod Identity for new ones.

---

**Version**: 2025 Best Practices
**Terraform Module**: `terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks`
**Status**: Production-ready
**Last Updated**: November 2025
