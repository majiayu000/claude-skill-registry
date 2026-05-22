---
name: opentofu-provider-setup
description: Configure OpenTofu with cloud providers, manage authentication, and setup state backends
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: infrastructure-provisioning
---

# OpenTofu Provider Setup

## What I do

I guide you through configuring OpenTofu with various cloud providers by leveraging official OpenTofu and Terraform provider documentation. I help you:

- **Provider Configuration**: Set up provider blocks with required and optional parameters
- **Authentication**: Configure authentication methods (access keys, service principals, etc.)
- **State Management**: Configure remote state backends (S3, Azure Storage, GCS, etc.)
- **Best Practices**: Follow provider-specific configuration patterns from official docs

## When to use me

Use this skill when you need to:
- Initialize a new OpenTofu project with provider configuration
- Configure authentication for cloud providers (AWS, Azure, GCP, etc.)
- Set up remote state backends for team collaboration
- Understand provider configuration options and best practices
- Troubleshoot provider connection or authentication issues

## Prerequisites

- **OpenTofu CLI installed**: Install from https://opentofu.org/docs/intro/install/
- **Cloud Provider Account**: Valid credentials for your target provider
- **Basic Terraform Knowledge**: Understanding of HCL syntax and configuration structure
- **Provider Documentation**: Reference to your provider's official documentation

## Steps

### Step 1: Install OpenTofu CLI

```bash
# Verify OpenTofu installation
tofu version

# If not installed, install using package manager or download from:
# https://opentofu.org/docs/intro/install/
```

### Step 2: Initialize OpenTofu Project

```bash
# Create new project directory
mkdir my-opentofu-project
cd my-opentofu-project

# Initialize OpenTofu
tofu init
```

### Step 3: Configure Provider

Create `versions.tf` to specify required provider versions:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    # Or for Azure:
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    # Or for GCP:
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Configure state backend (see Step 4)
  backend "s3" {
    bucket = "my-opentofu-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### Step 4: Configure Provider Authentication

#### AWS Provider

```hcl
provider "aws" {
  region = "us-east-1"

  # Method 1: Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
  # Method 2: Shared credentials file (~/.aws/credentials)
  # Method 3: Assume role
  assume_role {
    role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
  }

  # Reference: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
}
```

#### Azure Provider

```hcl
provider "azurerm" {
  features {}

  # Method 1: Environment variables (ARM_CLIENT_ID, ARM_CLIENT_SECRET, etc.)
  # Method 2: Managed Identity
  # Method 3: Service Principal with Certificate

  # Reference: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
}
```

#### GCP Provider

```hcl
provider "google" {
  project = "my-project-id"
  region  = "us-central1"

  # Method 1: Application Default Credentials
  # Method 2: Service Account Key (GOOGLE_CREDENTIALS env var)
  # Method 3: Workload Identity

  # Reference: https://registry.terraform.io/providers/hashicorp/google/latest/docs
}
```

### Step 5: Configure State Backend

#### AWS S3 Backend

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

#### Azure Storage Backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-storage-rg"
    storage_account_name = "terraformstate123"
    container_name       = "terraform-state"
    key                  = "prod.terraform.tfstate"
  }
}
```

#### GCS Backend

```hcl
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "prod"
  }
}
```

### Step 6: Initialize and Verify Configuration

```bash
# Initialize provider and backend
tofu init

# Verify provider configuration
tofu init -upgrade

# Test provider connection
tofu plan -out=tfplan
```

## Best Practices

### Configuration Best Practices

1. **Use Provider Version Constraints**: Pin provider versions to avoid breaking changes
2. **Store State Securely**: Use encrypted remote backends with versioning
3. **Use Environment Variables**: Never hardcode credentials in configuration files
4. **Enable State Locking**: Use DynamoDB (AWS) or similar for state locking
5. **Separate State per Environment**: Use different state files for dev/staging/prod

### Security Best Practices

```bash
# Use AWS Vault for credential management
# Reference: https://github.com/99designs/aws-vault

# Example with aws-vault
aws-vault exec my-profile -- tofu plan

# Use environment variables in production
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
tofu apply
```

### Organization Best Practices

```hcl
# Organize providers in separate files
# providers/aws.tf
provider "aws" {
  region = var.aws_region
}

# providers/azure.tf
provider "azurerm" {
  features {}
}
```

## Common Issues

### Issue: Provider Not Found

**Symptom**: Error `Error: Failed to query available provider packages`

**Solution**:
```bash
# Update provider versions
tofu init -upgrade

# Check provider source and version in versions.tf
# Reference: https://www.terraform.io/docs/language/providers/requirements.html
```

### Issue: Authentication Failed

**Symptom**: Error `Error: error configuring Terraform AWS Provider`

**Solution**:
```bash
# Verify credentials
aws sts get-caller-identity

# Check environment variables
echo $AWS_ACCESS_KEY_ID

# Reference provider authentication docs:
# AWS: https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication
# Azure: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs#authenticating-to-azure
# GCP: https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started
```

### Issue: State Backend Access Denied

**Symptom**: Error `Error: error acquiring the state lock`

**Solution**:
```bash
# Verify IAM/permissions for state bucket
# AWS: Check S3 bucket policy and IAM user permissions
# Azure: Check Storage Account access control
# GCP: Check GCS bucket IAM permissions

# Force unlock if necessary (caution!)
tofu force-unlock <LOCK_ID>
```

### Issue: Provider Version Conflict

**Symptom**: Error `Provider "aws" has an inconsistent lock file`

**Solution**:
```bash
# Remove lock file and reinitialize
rm -rf .terraform/
rm .terraform.lock.hcl
tofu init -upgrade
```

## Reference Documentation

- **OpenTofu Documentation**: https://opentofu.org/docs/
- **Terraform Registry**: https://registry.terraform.io/
- **AWS Provider**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **Azure Provider**: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
- **GCP Provider**: https://registry.terraform.io/providers/hashicorp/google/latest/docs
- **State Backends**: https://www.terraform.io/docs/language/settings/backends/index.html

## Examples

### Complete AWS Setup

```bash
# Create project structure
mkdir -p aws-infrastructure/{modules,environments/{dev,prod}}
cd aws-infrastructure

# Create versions.tf
cat > versions.tf <<EOF
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
EOF

# Initialize
export AWS_PROFILE="my-profile"
tofu init
```

### Multi-Provider Setup

```hcl
# versions.tf
terraform {
  required_providers {
    aws     = { source = "hashicorp/aws", version = "~> 5.0" }
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.0" }
  }

  backend "s3" {}
}

# providers.tf
provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
}
```

## Tips and Tricks

- **Use Provider Blocks**: Even for single-provider projects, it improves clarity
- **Version Constraints**: Use `~>` for minor version updates, `>=` for major versions
- **State Backups**: Enable versioning on state storage buckets
- **Workspace Management**: Use Terraform workspaces for multiple environments
- **Validation**: Use `tofu validate` to check configuration syntax

## Next Steps

After configuring providers, explore:
- **opentofu-provisioning-workflow**: Create and manage infrastructure resources
- **terraform-modules**: Create reusable infrastructure components
- **CI/CD Integration**: Automate infrastructure provisioning in pipelines
