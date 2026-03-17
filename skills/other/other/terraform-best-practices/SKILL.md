---
name: terraform-best-practices
description: Terraform infrastructure-as-code best practices for scalable and maintainable cloud infrastructure. Use when writing Terraform modules, managing infrastructure state, or implementing infrastructure automation at scale.
---

# Terraform Best Practices

Expert guidance for building production-grade Terraform infrastructure with enterprise patterns for module design, state management, security, testing, and multi-environment deployments.

## When to Use This Skill

- Writing reusable Terraform modules for teams or organizations
- Setting up secure remote state management and backend configuration
- Designing multi-environment infrastructure (dev/staging/prod)
- Implementing infrastructure CI/CD pipelines with automated validation
- Managing infrastructure at scale across multiple teams or projects
- Migrating from manual infrastructure to infrastructure-as-code
- Refactoring existing Terraform for better maintainability
- Implementing security best practices for infrastructure code

## Core Concepts

### Module Design Philosophy
- **Composition over monoliths**: Break infrastructure into reusable child modules
- **Standard structure**: main.tf, variables.tf, outputs.tf, versions.tf, README.md
- **Type constraints**: Use validation blocks and complex types for safety
- **Dynamic blocks**: Enable flexible configuration without duplication

### State Management Principles
- **Remote backends**: S3+DynamoDB or Terraform Cloud for team collaboration
- **State encryption**: KMS encryption at rest and in transit (mandatory)
- **State locking**: Prevent concurrent modifications with DynamoDB
- **Workspace strategy**: Directory-based for production, workspaces for similar envs

### Security Fundamentals
- **Secret management**: AWS Secrets Manager, HashiCorp Vault (never hardcode)
- **Least privilege**: Separate IAM roles per environment
- **Security scanning**: tfsec, Checkov, Terrascan in CI/CD
- **Resource tagging**: Enable cost tracking, ownership, compliance

### Testing & Validation
- **Pre-commit hooks**: Format, validate, lint before commits
- **Plan review**: Always save and review plans before apply
- **Automated testing**: Terratest for critical infrastructure modules
- **Policy as code**: OPA/Sentinel for compliance enforcement

## Quick Reference

| Task | Load reference |
| --- | --- |
| Module structure, variables, outputs, dynamic blocks | `skills/terraform-best-practices/references/module-design.md` |
| Remote backends, state encryption, workspace strategies | `skills/terraform-best-practices/references/state-management.md` |
| Variable precedence, tfvars, Terragrunt DRY config | `skills/terraform-best-practices/references/environment-management.md` |
| Secrets, IAM, scanning tools, resource tagging | `skills/terraform-best-practices/references/security.md` |
| Pre-commit hooks, Terratest, policy as code | `skills/terraform-best-practices/references/testing-validation.md` |
| Comprehensive checklist for all areas | `skills/terraform-best-practices/references/best-practices-summary.md` |

## Workflow

### 1. Project Setup
```bash
# Initialize directory structure
mkdir -p {modules,environments/{dev,staging,prod}}

# Set up remote backend (bootstrap S3 + DynamoDB first)
# Configure backend.tf with encryption and locking
```

### 2. Module Development
```bash
# Create module with standard structure
cd modules/my-module
touch main.tf variables.tf outputs.tf versions.tf README.md

# Add validation to variables
# Use complex types for structured inputs
# Document outputs with descriptions
```

### 3. Security Hardening
```bash
# Mark sensitive variables
# Use secret management for credentials
# Configure state encryption
# Set up security scanning in CI/CD
```

### 4. Testing Pipeline
```bash
# Install pre-commit hooks
pre-commit install

# Run validation locally
terraform init
terraform validate
terraform fmt -check

# Security scanning
tfsec .
checkov -d .

# Automated tests (critical modules)
cd tests && go test -v
```

### 5. Deployment Process
```bash
# Plan with output file
terraform plan -out=tfplan

# Review plan thoroughly
terraform show tfplan

# Apply only after approval
terraform apply tfplan

# Verify deployment
terraform output
```

### 6. Multi-Environment Management
```bash
# Use directory-based isolation for production
cd environments/prod
terraform init
terraform workspace list

# Or use Terragrunt for DRY backend config
terragrunt plan
```

## Common Mistakes

❌ **Hardcoding secrets in code** → Use secret management services
❌ **No state locking** → Enable DynamoDB locking to prevent conflicts
❌ **Skipping plan review** → Always save and review execution plans
❌ **No version constraints** → Pin provider and module versions
❌ **Local state in teams** → Use remote backends for collaboration
❌ **No security scanning** → Integrate tfsec/Checkov in CI/CD
❌ **Missing resource tags** → Tag all resources for cost/ownership tracking
❌ **No automated testing** → Write Terratest for critical modules
❌ **Monolithic modules** → Break into composable child modules
❌ **No backup strategy** → Enable S3 versioning on state buckets

## Resources

- **Official Docs**: https://developer.hashicorp.com/terraform/docs
- **Style Guide**: https://developer.hashicorp.com/terraform/language/syntax/style
- **Module Registry**: https://registry.terraform.io/
- **Terragrunt**: https://terragrunt.gruntwork.io/
- **Terratest**: https://terratest.gruntwork.io/
- **tfsec**: https://aquasecurity.github.io/tfsec/
- **Checkov**: https://www.checkov.io/
- **Best Practices**: https://www.terraform-best-practices.com/
- **AWS Provider**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
