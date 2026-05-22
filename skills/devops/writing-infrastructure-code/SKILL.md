---
name: writing-infrastructure-code
description: Managing cloud infrastructure using declarative and imperative IaC tools. Use when provisioning cloud resources (Terraform/OpenTofu for multi-cloud, Pulumi for developer-centric workflows, AWS CDK for AWS-native infrastructure), designing reusable modules, implementing state management patterns, or establishing infrastructure deployment workflows.
---

# Infrastructure as Code

Provision and manage cloud infrastructure using code-based automation tools. This skill covers tool selection, state management, module design, and operational patterns across Terraform/OpenTofu, Pulumi, and AWS CDK.

## When to Use

Use this skill when:
- Provisioning cloud infrastructure (compute, networking, databases, storage)
- Migrating from manual infrastructure to code-based workflows
- Designing reusable infrastructure modules
- Implementing multi-cloud or hybrid-cloud deployments
- Establishing state management and drift detection patterns
- Integrating infrastructure provisioning into CI/CD pipelines
- Evaluating IaC tools (Terraform vs Pulumi vs CDK)

Common requests:
- "Create a Terraform module for VPC provisioning"
- "Set up remote state with locking for team collaboration"
- "Compare Pulumi vs Terraform for our use case"
- "Design composable infrastructure modules"
- "Implement drift detection for existing infrastructure"

## Core Concepts

### Infrastructure as Code Fundamentals

**Key Principles:**
1. **Declarative vs Imperative** - Describe desired state (Terraform) or program infrastructure (Pulumi)
2. **Idempotency** - Same input produces same output, safe to re-run
3. **Version Control** - Infrastructure changes tracked in Git
4. **State Management** - Track actual infrastructure state
5. **Module Composition** - Reusable, versioned infrastructure components

**Benefits:**
- Reproducibility (same code = same infrastructure)
- Auditability (Git history shows all changes)
- Collaboration (code reviews for infrastructure changes)
- Automation (CI/CD deploys infrastructure)
- Disaster recovery (rebuild from code)

### Tool Selection Framework

Choose IaC tools based on team composition and cloud strategy:

**Terraform/OpenTofu** - Declarative, HCL-based
- Multi-cloud and hybrid-cloud deployments
- Operations/SRE teams prefer declarative approach
- Largest provider ecosystem (AWS, GCP, Azure, 3000+ providers)
- Mature module registry and community

**Pulumi** - Imperative, programming language-based
- Developer-centric teams familiar with TypeScript/Python/Go
- Complex logic requires programming constructs (loops, conditionals, functions)
- Native unit testing using familiar test frameworks
- Strong typing and IDE support

**AWS CDK** - AWS-native, programming language-based
- AWS-only infrastructure
- Tight integration with AWS services
- L1/L2/L3 construct abstractions
- CloudFormation under the hood

**Decision Tree:**
```
Multi-cloud required?
├─ YES → Team composition?
│  ├─ Ops/SRE focused → Terraform/OpenTofu
│  └─ Developer focused → Pulumi
└─ NO → AWS only?
   ├─ YES → Language preference?
   │  ├─ HCL/declarative → Terraform
   │  ├─ TypeScript/Python → AWS CDK
   │  └─ YAML/simple → CloudFormation
   └─ NO → GCP/Azure only?
      └─ Terraform or Pulumi
```

### State Management Architecture

Remote state with locking enables team collaboration:

**Backend Selection:**

| Cloud Provider | Recommended Backend | Locking Mechanism |
|----------------|---------------------|-------------------|
| AWS | S3 + DynamoDB | DynamoDB table |
| GCP | Google Cloud Storage | Native |
| Azure | Azure Blob Storage | Lease-based |
| Multi-cloud | Terraform Cloud/Enterprise | Built-in |
| Pulumi | Pulumi Service | Built-in |

**State Isolation Strategies:**

1. **Directory Separation** (recommended for most teams)
   - Separate directories per environment (`prod/`, `staging/`, `dev/`)
   - Complete state file isolation
   - No risk of cross-environment contamination

2. **Workspaces**
   - Single codebase, multiple environments
   - Shared state backend, environment namespacing
   - Risk: accidental cross-environment operations

3. **Layered Architecture**
   - Separate state files for networking, compute, data layers
   - Blast radius reduction
   - Cross-layer references via remote state data sources

**Critical State Management Rules:**
- Always use remote state for team environments
- Enable state file encryption at rest
- Enable versioning on state storage
- Use state locking to prevent concurrent modifications
- Never commit state files to Git
- Mark sensitive outputs as `sensitive = true`

### Module Design Patterns

**Composable Module Structure:**
```
modules/
├── vpc/              # Network foundation
├── security-group/   # Reusable security group patterns
├── rds/              # Database with backups, encryption
├── ecs-cluster/      # Container orchestration base
├── ecs-service/      # Individual microservice
└── alb/              # Application load balancer
```

**Module Versioning:**
- Pin module versions in production (`version = "5.1.0"`)
- Use semantic versioning for internal modules
- Test module updates in non-prod first
- Maintain CHANGELOG for module releases

**Module Design Principles:**
- Clear input contract (required vs optional variables)
- Documented outputs (what consumers can reference)
- Sane defaults where possible
- Validation rules for inputs
- Examples directory showing usage

**When to Create a Module:**
- Resource group is reused 3+ times
- Clear boundaries and responsibilities
- Stable interface contract
- Team has module maintenance capacity

**When to Keep Monolithic:**
- One-off infrastructure
- Rapid prototyping phase
- High coupling between resources
- Small team, simple infrastructure

## Quick Reference

### Terraform/OpenTofu Commands

```bash
# Initialize providers and backend
terraform init

# Plan changes (preview)
terraform plan

# Apply changes
terraform apply

# Destroy infrastructure
terraform destroy

# Format HCL files
terraform fmt

# Validate syntax
terraform validate

# Show state
terraform state list
terraform state show <resource>

# Import existing resources
terraform import <resource.name> <id>

# Workspace management
terraform workspace list
terraform workspace new staging
terraform workspace select prod
```

### Pulumi Commands

```bash
# Initialize new project
pulumi new aws-typescript

# Preview changes
pulumi preview

# Apply changes
pulumi up

# Destroy infrastructure
pulumi destroy

# Show stack outputs
pulumi stack output

# Manage stacks
pulumi stack ls
pulumi stack select prod

# Import existing resources
pulumi import <type> <name> <id>

# Export/import state
pulumi stack export > state.json
pulumi stack import < state.json
```

### AWS CDK Commands

```bash
# Initialize new app
cdk init app --language typescript

# Synthesize CloudFormation
cdk synth

# Preview changes
cdk diff

# Deploy stack
cdk deploy

# Destroy stack
cdk destroy

# Bootstrap account/region
cdk bootstrap

# List stacks
cdk list
```

### Common Patterns Checklist

**Infrastructure Provisioning:**
- [ ] Remote state configured with locking
- [ ] State file encryption enabled
- [ ] Provider versions pinned
- [ ] Module versions pinned (production)
- [ ] Variables have descriptions and types
- [ ] Sensitive outputs marked as sensitive
- [ ] Tagging strategy implemented
- [ ] Cost allocation tags applied

**Module Development:**
- [ ] Clear README with usage examples
- [ ] Required vs optional variables documented
- [ ] Outputs documented with descriptions
- [ ] Validation rules for critical inputs
- [ ] Examples directory with working code
- [ ] Tests for module behavior (Terratest/CDK assertions)
- [ ] CHANGELOG for version tracking
- [ ] Semantic versioning followed

**Operational Readiness:**
- [ ] Drift detection scheduled
- [ ] CI/CD pipeline for plan/apply
- [ ] State backup strategy
- [ ] Disaster recovery documented
- [ ] Team access controls configured (IAM/RBAC)
- [ ] Cost estimation integrated (Infracost)
- [ ] Security scanning integrated (Checkov/tfsec)
- [ ] Documentation kept current

## Detailed Documentation

For comprehensive patterns and implementation details:

**Tool-Specific Patterns:**
- `references/terraform-patterns.md` - Terraform/OpenTofu best practices, HCL patterns
- `references/pulumi-patterns.md` - Pulumi across TypeScript/Python/Go

**Architecture and Design:**
- `references/state-management.md` - Remote state, locking, isolation strategies
- `references/module-design.md` - Composable modules, versioning, registries

**Operations:**
- `references/drift-detection.md` - Detecting and remediating infrastructure drift

## Working Examples

Practical implementations demonstrating IaC patterns:

**Terraform Examples:**
- `examples/terraform/vpc-module/` - Multi-AZ VPC with public/private subnets
- `examples/terraform/ecs-service/` - ECS service with ALB, autoscaling
- `examples/terraform/rds-cluster/` - Aurora cluster with backups, encryption
- `examples/terraform/state-backend/` - S3 + DynamoDB backend setup

**Pulumi Examples:**
- `examples/pulumi/typescript/vpc/` - TypeScript VPC component
- `examples/pulumi/python/ecs-service/` - Python ECS service
- `examples/pulumi/go/rds-cluster/` - Go RDS cluster
- `examples/pulumi/testing/` - Unit tests for Pulumi programs

**AWS CDK Examples:**
- `examples/cdk/typescript/vpc-stack/` - VPC using L2 constructs
- `examples/cdk/typescript/ecs-fargate/` - Fargate service with ALB
- `examples/cdk/typescript/pipeline-stack/` - Self-mutating CDK pipeline
- `examples/cdk/testing/` - CDK assertions and snapshot tests

## Utility Scripts

Automated validation and operational tools:

- `scripts/validate-terraform.sh` - Terraform fmt, validate, tflint
- `scripts/cost-estimate.sh` - Infracost wrapper for cost analysis
- `scripts/drift-check.sh` - Scheduled drift detection
- `scripts/security-scan.sh` - Checkov/tfsec security scanning
- `scripts/state-backup.sh` - State file backup automation
- `scripts/module-release.sh` - Module versioning and publishing

## Integration with Other Skills

**Deployment Pipeline:**
- `building-ci-pipelines` - Automate terraform plan/apply in CI/CD
- `gitops-workflows` - GitOps-based infrastructure deployment

**Platform Engineering:**
- `kubernetes-operations` - Provision EKS, GKE, AKS clusters
- `platform-engineering` - Internal developer platform infrastructure

**Security:**
- `secret-management` - Provision Vault, External Secrets Operator
- `security-hardening` - Implement infrastructure security controls
- `compliance-frameworks` - Policy-as-code for compliance

**Operations:**
- `observability` - Provision monitoring infrastructure (Prometheus, Grafana)
- `disaster-recovery` - Infrastructure rebuild procedures
- `cost-optimization` - Implement cost controls via IaC

**Data Platform:**
- `data-architecture` - Provision data lakes, warehouses
- `streaming-data` - Provision Kafka, Kinesis infrastructure

## Best Practices

**Development Workflow:**
1. Write infrastructure code in feature branches
2. Run `terraform plan` / `pulumi preview` locally
3. Submit pull request with plan output
4. Code review focuses on security, cost, blast radius
5. CI runs automated tests and security scans
6. Apply only after approval and CI passes
7. Monitor for drift post-deployment

**State Management:**
- Use remote state from day one (never local state for teams)
- Separate state files per environment
- Enable state locking to prevent concurrent modifications
- Version state storage for rollback capability
- Encrypt state at rest (contains sensitive data)
- Regular state backups to separate location

**Module Development:**
- Start with monolithic code, extract modules when patterns emerge
- Design for reusability but avoid premature abstraction
- Document all inputs and outputs
- Provide working examples in `examples/` directory
- Pin provider versions in modules
- Test modules before publishing
- Use semantic versioning for releases

**Security:**
- Scan IaC for security issues before apply (Checkov, tfsec)
- Never commit secrets to code (use secret references)
- Mark sensitive outputs as `sensitive = true`
- Implement least-privilege IAM policies
- Enable resource encryption by default
- Use private module registries for internal modules

**Cost Management:**
- Estimate costs before applying changes (Infracost)
- Tag all resources for cost allocation
- Review cost impact in pull requests
- Set up cost alerts for drift
- Rightsize resources based on usage

**Operational Excellence:**
- Schedule regular drift detection
- Document disaster recovery procedures
- Maintain runbooks for common operations
- Monitor state file access logs
- Practice infrastructure rebuilds periodically
- Keep provider versions current with testing

## Common Pitfalls

**State File Issues:**
- **Manual state editing** - Use terraform state commands, not direct edits
- **No state locking** - Race conditions corrupt state
- **Local state for teams** - State divergence across team members
- **Large state files** - Break into multiple state files by layer

**Module Design:**
- **Over-abstraction** - Too generic, hard to understand
- **Under-abstraction** - Copy-paste code everywhere
- **No version pinning** - Unexpected breaking changes
- **No examples** - Users don't know how to consume module

**Operations:**
- **No drift detection** - Manual changes go unnoticed
- **Direct resource modification** - Bypassing IaC creates drift
- **No rollback plan** - Can't recover from failed apply
- **Ignoring plan output** - Surprises during apply

**Security:**
- **Secrets in code** - Hard-coded credentials
- **No security scanning** - Vulnerabilities in production
- **Overly permissive IAM** - Excessive privileges
- **No state encryption** - Sensitive data exposed

## Troubleshooting Guide

**State Lock Issues:**
```bash
terraform force-unlock <lock-id>  # Use only if certain no other process running
```

**Import Existing Resources:**
```bash
terraform import aws_vpc.main vpc-12345678
pulumi import aws:ec2/vpc:Vpc main vpc-12345678
```

**Drift Detection:**
```bash
terraform plan -detailed-exitcode  # Exit 2 = drift detected
pulumi preview --diff
```

For detailed drift remediation, see `references/drift-detection.md`.

**State Recovery:**
```bash
# Terraform: Restore from S3 versioning
aws s3 cp s3://bucket/backup/terraform.tfstate terraform.tfstate

# Pulumi: Restore from checkpoint
pulumi stack export --version <timestamp> | pulumi stack import
```

## Related Skills

For cloud-specific implementations:
- `aws-patterns` - AWS-specific resource patterns
- `gcp-patterns` - GCP-specific resource patterns
- `azure-patterns` - Azure-specific resource patterns

For infrastructure operations:
- `kubernetes-operations` - Manage Kubernetes clusters provisioned via IaC
- `gitops-workflows` - GitOps-based infrastructure deployment
- `platform-engineering` - Internal developer platforms

For security and compliance:
- `security-hardening` - Infrastructure security controls
- `secret-management` - Secret injection and rotation
- `compliance-frameworks` - Policy-as-code for compliance

For deployment automation:
- `building-ci-pipelines` - CI/CD for infrastructure code
- `deploying-applications` - Application deployment to provisioned infrastructure

For cost and observability:
- `cost-optimization` - FinOps practices for infrastructure
- `observability` - Monitoring infrastructure health
