---
name: terraform-state
description: Use when managing Terraform state files, remote backends, and state locking for infrastructure coordination.
allowed-tools: []
---

# Terraform State

Managing Terraform state files and remote backends.

## State Basics

Terraform state tracks resource mappings and metadata.

### Local State

```bash
# Default location
terraform.tfstate
terraform.tfstate.backup
```

### Remote State

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

## State Commands

```bash
# List resources
terraform state list

# Show resource
terraform state show aws_instance.web

# Move resource
terraform state mv aws_instance.web aws_instance.app

# Remove resource
terraform state rm aws_instance.old

# Pull state
terraform state pull > terraform.tfstate

# Push state
terraform state push terraform.tfstate

# Replace provider
terraform state replace-provider hashicorp/aws registry.terraform.io/hashicorp/aws
```

## Remote Backends

### S3 Backend

```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "path/to/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    
    # Optional: state locking
    kms_key_id     = "arn:aws:kms:us-east-1:123456789:key/..."
  }
}
```

### Terraform Cloud

```hcl
terraform {
  cloud {
    organization = "my-org"
    
    workspaces {
      name = "my-workspace"
    }
  }
}
```

### Azure Backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "tfstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

## State Locking

Prevents concurrent modifications:

```hcl
# S3 + DynamoDB locking
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
  }
}
```

## Import Resources

```bash
# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Import with module
terraform import module.vpc.aws_vpc.main vpc-12345678
```

## Workspaces

```bash
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new staging

# Switch workspace
terraform workspace select production

# Delete workspace
terraform workspace delete staging
```

## Best Practices

### Enable State Locking

Always use state locking to prevent concurrent modifications.

### Encrypt State

```hcl
backend "s3" {
  encrypt = true
  kms_key_id = "arn:aws:kms:..."
}
```

### Separate State Files

Use different state files for different environments:

```
states/
├── prod/terraform.tfstate
├── staging/terraform.tfstate
└── dev/terraform.tfstate
```

### Backup State

```bash
# Backup before dangerous operations
cp terraform.tfstate terraform.tfstate.backup.$(date +%Y%m%d_%H%M%S)
```

### Never Edit State Manually

Always use `terraform state` commands.
