---
name: infrastructure-as-code
description: Provides Infrastructure as Code best practices for Terraform, Pulumi, CloudFormation, and OpenTofu. Use when provisioning infrastructure, writing IaC modules, managing cloud resources, scanning for misconfigurations, or when user mentions 'terraform', 'pulumi', 'cloudformation', 'IaC', 'opentofu', 'infrastructure', 'tfsec', 'checkov', 'drift'.
---

# Infrastructure as Code

Best practices for managing cloud infrastructure declaratively with Terraform, Pulumi, CloudFormation, and OpenTofu. Covers module composition, state management, security scanning, and drift prevention.

## IaC Tool Comparison

Choose the right tool based on team skills, cloud strategy, and operational requirements.

| Tool | Language | State Management | Multi-Cloud | Learning Curve | Ecosystem |
|------|----------|-----------------|-------------|----------------|-----------|
| Terraform | HCL | Remote backend (S3, GCS, etc.) | Excellent | Medium | Largest provider ecosystem |
| OpenTofu | HCL | Same as Terraform | Excellent | Medium | Fork-compatible with Terraform |
| Pulumi | TypeScript, Python, Go, C# | Pulumi Cloud or self-managed | Excellent | Low for developers | Growing, SDK-based |
| CloudFormation | YAML/JSON | AWS-managed | AWS only | Medium | Native AWS integration |
| CDK | TypeScript, Python, Java, Go | AWS-managed (synths to CFN) | AWS only | Low for developers | Leverages CFN resources |

| Decision Factor | Recommendation |
|-----------------|---------------|
| Multi-cloud required | Terraform or Pulumi |
| AWS-only shop | CloudFormation or CDK |
| Team knows TypeScript | Pulumi or CDK |
| Need open-source license | OpenTofu |
| Existing Terraform codebase | Stay Terraform or migrate to OpenTofu |
| Complex logic and loops | Pulumi (general-purpose language) |

## State Management Patterns

State is the source of truth for what IaC has provisioned. Mismanaging state causes orphaned resources, duplicate deployments, and data loss.

```
+------------------+       +------------------+       +------------------+
|  Developer CLI   | ----> |  Remote Backend  | <---- |   CI/CD Pipeline  |
+------------------+       +------------------+       +------------------+
                           |  - S3 + DynamoDB |
                           |  - GCS + Lock    |
                           |  - Terraform Cloud|
                           +------------------+
```

| Pattern | When to Use | Implementation |
|---------|------------|----------------|
| Single state file | Small projects, <20 resources | One backend config |
| State per environment | Separate dev/staging/prod | Workspace or directory per env |
| State per component | Large infra, team boundaries | Separate root modules with data sources |
| Hierarchical state | Complex multi-team orgs | Layers: network -> compute -> app |

### Terraform Remote State Configuration

```hcl
# backend.tf -- Remote state with locking
terraform {
  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

# State locking table -- provision FIRST with a bootstrap module
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

# Cross-stack references via remote state data source
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "myorg-terraform-state"
    key    = "prod/network/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.network.outputs.private_subnet_ids[0]
}
```

## Module Composition and Versioning

Modules are the unit of reuse in Terraform and OpenTofu. Good module design follows the single-responsibility principle.

```
modules/
  vpc/
    main.tf          # Resources
    variables.tf     # Input variables with validation
    outputs.tf       # Output values for consumers
    versions.tf      # Required providers and versions
environments/
  dev/
    main.tf          # Calls modules with dev parameters
    backend.tf       # Dev state backend
    terraform.tfvars # Dev variable values
  prod/
    main.tf
    backend.tf
    terraform.tfvars
```

### Terraform Module Example

```hcl
# modules/vpc/variables.tf
variable "name" {
  description = "Name prefix for all VPC resources"
  type        = string
  validation {
    condition     = length(var.name) <= 24
    error_message = "Name must be 24 characters or fewer."
  }
}

variable "cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "Must be a valid CIDR block."
  }
}

variable "availability_zones" {
  type = list(string)
}

variable "tags" {
  type    = map(string)
  default = {}
}

# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = merge(var.tags, { Name = "${var.name}-vpc" })
}

resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.cidr_block, 8, count.index)
  availability_zone = var.availability_zones[count.index]
  tags = merge(var.tags, {
    Name = "${var.name}-public-${var.availability_zones[count.index]}"
    Tier = "public"
  })
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.cidr_block, 8, count.index + length(var.availability_zones))
  availability_zone = var.availability_zones[count.index]
  tags = merge(var.tags, {
    Name = "${var.name}-private-${var.availability_zones[count.index]}"
    Tier = "private"
  })
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.this.id
}
output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}
output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

# environments/prod/main.tf -- Consuming the module
module "vpc" {
  source  = "git::https://github.com/myorg/terraform-modules.git//vpc?ref=v2.1.0"

  name               = "prod"
  cidr_block         = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  tags = { Environment = "production", Team = "platform" }
}
```

| Versioning Strategy | Source Format | When to Use |
|---------------------|-------------|-------------|
| Git tag | `git::https://...?ref=v2.1.0` | Internal modules, full control |
| Terraform Registry | `source = "hashicorp/consul/aws"` version = `"0.1.0"` | Public modules |
| Local path | `source = "../../modules/vpc"` | Monorepo, development |
| S3/GCS archive | `source = "s3::https://..."` | Air-gapped environments |

## Pulumi TypeScript Example

Pulumi uses general-purpose languages, giving full IDE support, type checking, and testing capabilities.

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const env = pulumi.getStack();
const vpcCidr = config.get("vpcCidr") || "10.0.0.0/16";

class VpcComponent extends pulumi.ComponentResource {
  public readonly vpcId: pulumi.Output<string>;
  public readonly publicSubnetIds: pulumi.Output<string>[];
  public readonly privateSubnetIds: pulumi.Output<string>[];

  constructor(name: string, args: {
    cidr: string; azCount: number; enableNat: boolean;
  }, opts?: pulumi.ComponentResourceOptions) {
    super("custom:network:Vpc", name, {}, opts);

    const vpc = new aws.ec2.Vpc(`${name}-vpc`, {
      cidrBlock: args.cidr,
      enableDnsHostnames: true,
      enableDnsSupport: true,
      tags: { Name: `${name}-vpc`, Environment: env },
    }, { parent: this });

    this.vpcId = vpc.id;
    this.publicSubnetIds = [];
    this.privateSubnetIds = [];
    const azs = aws.getAvailabilityZones({ state: "available" });

    for (let i = 0; i < args.azCount; i++) {
      const pub = new aws.ec2.Subnet(`${name}-public-${i}`, {
        vpcId: vpc.id,
        cidrBlock: `10.0.${i}.0/24`,
        availabilityZone: azs.then(az => az.names[i]),
        mapPublicIpOnLaunch: true,
        tags: { Name: `${name}-public-${i}`, Tier: "public" },
      }, { parent: this });

      const priv = new aws.ec2.Subnet(`${name}-private-${i}`, {
        vpcId: vpc.id,
        cidrBlock: `10.0.${i + args.azCount}.0/24`,
        availabilityZone: azs.then(az => az.names[i]),
        tags: { Name: `${name}-private-${i}`, Tier: "private" },
      }, { parent: this });

      this.publicSubnetIds.push(pub.id);
      this.privateSubnetIds.push(priv.id);
    }
    this.registerOutputs({ vpcId: this.vpcId });
  }
}

// Usage
const network = new VpcComponent("main", {
  cidr: vpcCidr, azCount: 3, enableNat: env === "prod",
});

export const vpcId = network.vpcId;
```

## CloudFormation YAML Example

CloudFormation is AWS-native and requires no external state management. Ideal for AWS-only environments with strict compliance requirements.

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Production VPC with public and private subnets

Parameters:
  EnvironmentName:
    Type: String
    Default: prod
    AllowedValues: [dev, staging, prod]
  VpcCIDR:
    Type: String
    Default: '10.0.0.0/16'

Conditions:
  IsProduction: !Equals [!Ref EnvironmentName, prod]

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCIDR
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${EnvironmentName}-vpc'

  PublicSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: !Select [0, !Cidr [!Ref VpcCIDR, 6, 8]]
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true

  PrivateSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: !Select [3, !Cidr [!Ref VpcCIDR, 6, 8]]
      AvailabilityZone: !Select [0, !GetAZs '']

  NatGateway:
    Type: AWS::EC2::NatGateway
    Condition: IsProduction
    Properties:
      AllocationId: !GetAtt NatEIP.AllocationId
      SubnetId: !Ref PublicSubnetA

  NatEIP:
    Type: AWS::EC2::EIP
    Condition: IsProduction
    Properties:
      Domain: vpc

Outputs:
  VpcId:
    Value: !Ref VPC
    Export:
      Name: !Sub '${EnvironmentName}-VpcId'
```

## Security Scanning with Checkov and tfsec

Scan IaC before apply to catch misconfigurations, policy violations, and security risks.

| Tool | Focus | Language | Integration |
|------|-------|----------|-------------|
| Checkov | Multi-framework (TF, CFN, K8s, Helm) | Python | CLI, CI/CD, IDE |
| tfsec | Terraform-specific, fast | Go | CLI, CI/CD, pre-commit |
| Terrascan | Policy-as-code (OPA/Rego) | Go | CLI, CI/CD |
| Snyk IaC | Commercial, wide coverage | SaaS | CLI, CI/CD, IDE |

### Checkov Scanning Example

```bash
# Scan a Terraform directory
checkov -d ./environments/prod/ --framework terraform --compact

# Scan with specific checks only
checkov -d ./environments/prod/ --check CKV_AWS_18,CKV_AWS_19

# Inline suppression in .tf files:
# resource "aws_s3_bucket" "logs" {
#   # checkov:skip=CKV_AWS_18:Logging bucket does not need access logging
#   bucket = "my-logs-bucket"
# }

# Generate SARIF output for GitHub Security tab
checkov -d ./environments/prod/ --output sarif --output-file results.sarif
```

```yaml
# .github/workflows/iac-security.yml
name: IaC Security Scan

on:
  pull_request:
    paths: ['**/*.tf', '**/*.tfvars']

jobs:
  checkov:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: bridgecrewio/checkov-action@v12
        with:
          directory: ./environments/
          framework: terraform
          output_format: sarif
          output_file_path: results.sarif
          soft_fail: false
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: results.sarif

  tfsec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/tfsec-action@v1.0.3
        with:
          working_directory: ./environments/
```

## Drift Detection and Prevention

Drift occurs when actual infrastructure diverges from IaC state. Left unchecked, drift causes failed applies, security gaps, and configuration inconsistencies.

| Drift Cause | Prevention |
|-------------|-----------|
| Manual console changes | Lock down console write access; read-only for debugging |
| Auto-scaling events | Use `lifecycle { ignore_changes }` for dynamic attributes |
| External automation | Coordinate with IaC or import resources |
| Incomplete IaC coverage | Import existing resources before managing them |

### Drift Detection Strategy

```yaml
# .github/workflows/drift-detection.yml
name: Drift Detection

on:
  schedule:
    - cron: '0 6 * * *'   # Daily at 6 AM UTC

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.7.0

      - name: Terraform Init
        working-directory: ./environments/${{ matrix.environment }}
        run: terraform init -input=false

      - name: Detect Drift
        id: plan
        working-directory: ./environments/${{ matrix.environment }}
        run: |
          terraform plan -detailed-exitcode -input=false 2>&1 | tee plan_output.txt
          echo "exit_code=${PIPESTATUS[0]}" >> "$GITHUB_OUTPUT"
          # Exit code 0 = no changes, 1 = error, 2 = drift detected
        continue-on-error: true

      - name: Alert on Drift
        if: steps.plan.outputs.exit_code == '2'
        run: echo "::warning::Drift detected in ${{ matrix.environment }}!"
```

### Preventing Drift with Lifecycle Rules

```hcl
resource "aws_autoscaling_group" "app" {
  lifecycle {
    ignore_changes = [desired_capacity]  # Managed by auto-scaling, not Terraform
  }
  min_size = 2
  max_size = 10
}

resource "aws_security_group" "critical" {
  lifecycle {
    prevent_destroy = true  # Prevent accidental deletion
  }
  name   = "critical-sg"
  vpc_id = module.vpc.vpc_id
}
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Local state files | No locking, no team access, easy to lose | Use remote backend with locking (S3+DynamoDB, GCS) |
| Hardcoded provider credentials | Secrets in version control | Use environment variables, OIDC, or vault |
| Monolithic root module | Slow plans, blast radius covers everything | Split into composable modules per service or layer |
| No variable validation | Invalid inputs cause cryptic errors at apply | Add `validation` blocks on all input variables |
| `terraform apply` without plan | No review of changes before execution | Always `plan -out=plan.tfplan` then `apply plan.tfplan` |
| Ignoring state drift | Manual changes accumulate, next apply fails | Schedule daily drift detection; alert and remediate |
| No module versioning | Breaking changes propagate immediately | Pin module versions with git tags or registry versions |
| Inline resources instead of modules | Copy-paste across environments, divergence | Extract reusable modules, parameterize with variables |
| Storing secrets in tfvars | Credentials committed to git | Use vault, SSM Parameter Store, or Secrets Manager |
| No import before manage | Terraform tries to create existing resources | `terraform import` existing resources first |
| Wildcard provider versions | Upgrades break without warning | Pin versions with `~>` constraints in `versions.tf` |
| No `prevent_destroy` on stateful resources | Accidental deletion of databases, buckets | Add `lifecycle { prevent_destroy = true }` |
| Running apply from laptops | No audit trail, credential exposure | Run all applies through CI/CD with approval gates |

## Security and Compliance Checklist

- [ ] Remote state backend with encryption at rest enabled
- [ ] State locking configured (DynamoDB, GCS, or equivalent)
- [ ] No credentials or secrets in `.tf` files or `.tfvars`
- [ ] Provider versions pinned with constraints in `versions.tf`
- [ ] Module versions pinned to specific tags or registry versions
- [ ] Checkov or tfsec runs on every pull request
- [ ] `terraform plan` output reviewed before every apply
- [ ] Production applies gated behind CI/CD approval
- [ ] `prevent_destroy` set on stateful resources (databases, storage)
- [ ] Drift detection runs on a daily schedule
- [ ] Least-privilege IAM roles for Terraform execution
- [ ] State file access restricted to CI/CD service accounts
- [ ] All resources tagged with `Environment`, `Team`, and `ManagedBy`
- [ ] Sensitive outputs marked with `sensitive = true`
- [ ] No use of `local-exec` or `remote-exec` provisioners
- [ ] Import existing resources before writing IaC to manage them
