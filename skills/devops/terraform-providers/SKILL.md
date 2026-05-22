---
name: terraform-providers
description: Provider configuration, versioning, and multi-provider patterns
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 01-terraform-fundamentals
bond_type: SECONDARY_BOND
---

# Terraform Providers Skill

Configure and manage Terraform providers for single and multi-cloud deployments.

## Provider Requirements

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.24"
    }
  }
}
```

## Version Constraints

```hcl
version = "5.0.0"           # Exact version
version = ">= 5.0"          # Minimum version
version = "~> 5.0"          # >= 5.0.0, < 6.0.0
version = ">= 5.0, < 6.0"   # Explicit range
version = "!= 5.1.0"        # Exclude version
```

## Provider Configuration

### AWS
```hcl
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }

  assume_role {
    role_arn     = var.assume_role_arn
    session_name = "TerraformSession"
  }
}
```

### Azure
```hcl
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}
```

### GCP
```hcl
provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}
```

## Provider Aliases

### Multi-Region
```hcl
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

provider "aws" {
  alias  = "us_west_2"
  region = "us-west-2"
}

resource "aws_s3_bucket" "primary" {
  provider = aws.us_east_1
  bucket   = "${var.project}-primary"
}

resource "aws_s3_bucket" "replica" {
  provider = aws.us_west_2
  bucket   = "${var.project}-replica"
}
```

### Multi-Account
```hcl
provider "aws" {
  alias  = "prod"
  region = "us-east-1"

  assume_role {
    role_arn = "arn:aws:iam::PROD_ACCOUNT:role/TerraformRole"
  }
}

provider "aws" {
  alias  = "dev"
  region = "us-east-1"

  assume_role {
    role_arn = "arn:aws:iam::DEV_ACCOUNT:role/TerraformRole"
  }
}
```

## Module Provider Inheritance

```hcl
# Root module
provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

module "vpc" {
  source = "./modules/vpc"

  providers = {
    aws = aws.west
  }

  cidr_block = "10.0.0.0/16"
}
```

## Lock File

```hcl
# .terraform.lock.hcl (auto-generated)
provider "registry.terraform.io/hashicorp/aws" {
  version     = "5.31.0"
  constraints = "~> 5.0"
  hashes = [
    "h1:xyz...",
    "zh:abc...",
  ]
}
```

```bash
# Update lock file
terraform init -upgrade

# Platform-specific locks
terraform providers lock \
  -platform=linux_amd64 \
  -platform=darwin_amd64 \
  -platform=darwin_arm64
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Provider not found` | Not in required_providers | Add provider block |
| `Version constraint` | Incompatible version | Update constraint |
| `Configuration missing` | No provider block | Add configuration |
| `Alias not found` | Wrong alias reference | Check alias name |

### Debug Commands
```bash
# Show providers
terraform providers

# Show provider versions
terraform version

# Initialize providers
terraform init -upgrade
```

## Usage

```python
Skill("terraform-providers")
```

## Related

- **Agent**: 01-terraform-fundamentals (SECONDARY_BOND)
- **Skill**: terraform-fundamentals (PRIMARY on same agent)
