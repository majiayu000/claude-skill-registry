---
name: terraform-workspace
description: Terraform workspace management for multi-environment deployments
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 03-terraform-state
bond_type: SECONDARY_BOND
---

# Terraform Workspace Skill

Manage multiple environments with Terraform workspaces.

## Workspace Commands

```bash
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Switch workspace
terraform workspace select prod

# Show current
terraform workspace show

# Delete workspace
terraform workspace delete dev
```

## Configuration Patterns

### Environment-Specific Variables
```hcl
locals {
  env_config = {
    dev = {
      instance_type = "t3.micro"
      min_size      = 1
      max_size      = 2
    }
    staging = {
      instance_type = "t3.small"
      min_size      = 2
      max_size      = 4
    }
    prod = {
      instance_type = "t3.medium"
      min_size      = 3
      max_size      = 10
    }
  }

  config = local.env_config[terraform.workspace]
}

resource "aws_autoscaling_group" "app" {
  min_size = local.config.min_size
  max_size = local.config.max_size
  # ...
}
```

### Workspace-Aware Naming
```hcl
locals {
  name_prefix = "${var.project}-${terraform.workspace}"
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name        = "${local.name_prefix}-vpc"
    Environment = terraform.workspace
  }
}
```

### Conditional Resources
```hcl
resource "aws_cloudwatch_alarm" "cpu" {
  count = terraform.workspace == "prod" ? 1 : 0

  alarm_name = "${local.name_prefix}-cpu-alarm"
  # ...
}

resource "aws_db_instance" "main" {
  multi_az            = terraform.workspace == "prod"
  deletion_protection = terraform.workspace == "prod"
  # ...
}
```

## Backend Configuration

### S3 with Workspace Prefix
```hcl
terraform {
  backend "s3" {
    bucket               = "company-terraform-state"
    key                  = "app/terraform.tfstate"
    region               = "us-east-1"
    workspace_key_prefix = "workspaces"
    dynamodb_table       = "terraform-locks"
  }
}
# State paths:
# - workspaces/dev/app/terraform.tfstate
# - workspaces/prod/app/terraform.tfstate
```

## Directory-Based Alternative

```
infrastructure/
├── modules/
│   └── app/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── backend.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
```

```hcl
# environments/prod/main.tf
module "app" {
  source = "../../modules/app"

  environment   = "prod"
  instance_type = "t3.medium"
  min_size      = 3
}
```

## Best Practices

| Approach | Use Case | Pros | Cons |
|----------|----------|------|------|
| Workspaces | Simple environments | Single codebase | Same config |
| Directories | Complex differences | Full customization | Code duplication |
| Hybrid | Mixed needs | Flexible | More complexity |

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Workspace not found` | Not created | `terraform workspace new` |
| `State mismatch` | Wrong workspace | Check `terraform workspace show` |
| `Cannot delete` | Has resources | Destroy first or use `-force` |

## Usage

```python
Skill("terraform-workspace")
```

## Related

- **Agent**: 03-terraform-state (SECONDARY_BOND)
- **Skill**: terraform-state (PRIMARY on same agent)
