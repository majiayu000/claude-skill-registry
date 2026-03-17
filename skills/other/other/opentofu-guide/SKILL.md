---
name: opentofu-guide
description: Comprehensive OpenTofu expertise including migration from Terraform, state encryption, OpenTofu 1.10/1.11 features (OCI registry, native S3 locking, ephemeral resources, enabled meta-argument), and CI/CD integration. Covers when to use OpenTofu vs Terraform with decision matrix.
---

<!--
Progressive Disclosure References:
- references/opentofu-1.10-features.md - OCI registry, native S3 locking, deprecation warnings
- references/opentofu-1.11-features.md - Ephemeral resources, enabled meta-argument
- references/state-encryption.md - Complete state encryption guide with KMS integration
-->

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation

---


# OpenTofu Expertise and Migration Guide

## Overview

OpenTofu is the open-source fork of Terraform, created in 2023 after HashiCorp changed Terraform's license from MPL 2.0 to BSL (Business Source License). OpenTofu is stewarded by the Linux Foundation and maintains full compatibility with Terraform 1.5.x while adding community-driven features.

## Key Differences (2025)

### Licensing

**Terraform (HashiCorp):**
- BSL (Business Source License) since August 2023
- Restrictions on commercial use for competing products
- IBM acquired HashiCorp in 2024

**OpenTofu:**
- MPL 2.0 (Mozilla Public License)
- True open-source
- Linux Foundation governance
- Community-driven development

### Feature Innovations (2025)

**OpenTofu 1.7 Features:**
- **State Encryption**: Client-side encryption (community requested for 5+ years)
- **Loop-able Import Blocks**: for_each in import blocks
- **Dynamic Provider Functions**: Provider-defined functions support
- **Early Variable Evaluation**: Variables in terraform block

**OpenTofu 1.8 Features (Latest):**
- **OpenTofu-Specific Overrides**: Balance compatibility with innovation
- **Early Variable Evaluation Expanded**: Use variables/locals in module sources
- **Enhanced Provider Support**: Improved provider SDK

**Terraform Advantages:**
- **HCP Terraform**: Cloud platform with Stacks, HYOK, Private VCS Access
- **Enterprise Support**: Direct HashiCorp/IBM support
- **Larger Ecosystem**: More established marketplace
- **Sentinel Policies**: Policy-as-code framework (350+ NIST policies)

### Compatibility

**100% Compatible:**
- HCL syntax (same language)
- Provider ecosystem (same registry access)
- State file format (Terraform 1.5.x)
- Module structure
- CLI commands

**Migration Path:**
- Drop-in replacement for Terraform 1.5.x
- No code changes required
- State files portable (with encryption consideration)

## When to Use OpenTofu vs Terraform

### Choose OpenTofu When:

1. **Open-Source Requirements:**
   - Organization policy requires open-source tools
   - Want vendor neutrality
   - Concerned about future license changes

2. **State Encryption Needed:**
   - Compliance requires client-side encryption
   - Want encryption without HCP Terraform
   - Multi-cloud encryption requirements

3. **Cost Optimization:**
   - Want free state encryption
   - No need for HCP Terraform features
   - Budget constraints on tooling

4. **Community-Driven:**
   - Want to influence roadmap
   - Prefer Linux Foundation governance
   - Value community contributions

### Choose Terraform When:

1. **Enterprise Features Required:**
   - Need HCP Terraform Stacks
   - Require HYOK (Hold Your Own Key)
   - Want Private VCS Access
   - Need Sentinel policy enforcement

2. **Enterprise Support:**
   - Want direct HashiCorp/IBM support
   - Need SLA guarantees
   - Require compliance certifications

3. **Advanced Features:**
   - Ephemeral values (1.10+)
   - Terraform Query (1.14+)
   - Actions blocks (1.14+)
   - Latest provider features first

4. **Established Ecosystem:**
   - Existing HCP Terraform investment
   - Tight integration needs
   - Mature tooling requirements

## Migration from Terraform to OpenTofu

### Step 1: Assess Compatibility

```bash
# Check Terraform version
terraform version
# Must be 1.5.x or compatible

# Check provider versions
terraform providers
# All providers compatible (same registry)
```

### Step 2: Install OpenTofu

**Windows:**
```powershell
# Chocolatey
choco install opentofu

# Scoop
scoop install opentofu

# Manual
# Download from https://github.com/opentofu/opentofu/releases
```

**macOS:**
```bash
# Homebrew
brew install opentofu

# Manual
curl -L https://github.com/opentofu/opentofu/releases/download/v1.8.0/tofu_1.8.0_darwin_amd64.tar.gz | tar xz
sudo mv tofu /usr/local/bin/
```

**Linux:**
```bash
# Snap
snap install opentofu --classic

# Debian/Ubuntu
curl -fsSL https://get.opentofu.org/install-opentofu.sh | sh

# Manual
wget https://github.com/opentofu/opentofu/releases/download/v1.8.0/tofu_1.8.0_linux_amd64.tar.gz
tar -xzf tofu_1.8.0_linux_amd64.tar.gz
sudo mv tofu /usr/local/bin/
```

### Step 3: Test Compatibility

```bash
# Navigate to Terraform directory
cd /path/to/terraform/project

# Initialize with OpenTofu (non-destructive)
tofu init

# Validate configuration
tofu validate

# Generate plan (compare with Terraform plan)
tofu plan
```

### Step 4: Migrate State (Optional)

**If NOT using state encryption:**
```bash
# State is compatible - no migration needed
# Just switch from 'terraform' to 'tofu' commands

# Verify state
tofu show
```

**If ENABLING state encryption:**
```bash
# Configure encryption in .tofu file
cat > .tofu <<EOF
encryption {
  state {
    method = "aes_gcm"
    keys {
      name = "my_key"
      passphrase = env.TOFU_ENCRYPTION_KEY
    }
  }

  plan {
    method = "aes_gcm"
    keys {
      name = "my_key"
      passphrase = env.TOFU_ENCRYPTION_KEY
    }
  }
}
EOF

# Set encryption key
export TOFU_ENCRYPTION_KEY="your-secure-passphrase"

# Migrate state (automatically encrypts)
tofu init -migrate-state
```

### Step 5: Update CI/CD

**GitHub Actions:**
```yaml
# Before (Terraform)
- uses: hashicorp/setup-terraform@v3
  with:
    terraform_version: 1.5.0

# After (OpenTofu)
- uses: opentofu/setup-opentofu@v1
  with:
    tofu_version: 1.8.0

# Or manual install
- name: Install OpenTofu
  run: |
    curl -fsSL https://get.opentofu.org/install-opentofu.sh | sh
    tofu version
```

**Azure DevOps:**
```yaml
# Before
- task: TerraformInstaller@0
  inputs:
    terraformVersion: '1.5.0'

# After
- task: Bash@3
  displayName: 'Install OpenTofu'
  inputs:
    targetType: 'inline'
    script: |
      curl -fsSL https://get.opentofu.org/install-opentofu.sh | sh
      tofu version
```

**GitLab CI:**
```yaml
# Before
image: hashicorp/terraform:1.5.0

# After
image: ghcr.io/opentofu/opentofu:1.8.0
```

## State Encryption (OpenTofu Exclusive)

### Configuration

**Basic Encryption:**
```hcl
# .tofu or terraform.tf
encryption {
  state {
    method = "aes_gcm"
    keys {
      name = "primary_key"
      passphrase = env.TOFU_STATE_ENCRYPTION_KEY
    }
  }
}
```

**Key Rotation:**
```hcl
encryption {
  state {
    method = "aes_gcm"
    keys {
      # New key
      name = "key_v2"
      passphrase = env.TOFU_KEY_V2

      # Old key (for decryption)
      fallback {
        name = "key_v1"
        passphrase = env.TOFU_KEY_V1
      }
    }
  }
}
```

**Cloud KMS Integration:**
```hcl
# AWS KMS
encryption {
  state {
    method = "aws_kms"
    keys {
      name = "aws_key"
      kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"
    }
  }
}

# Azure Key Vault
encryption {
  state {
    method = "azurerm_key_vault"
    keys {
      name = "azure_key"
      key_vault_key_id = "https://myvault.vault.azure.net/keys/mykey/version"
    }
  }
}

# GCP KMS
encryption {
  state {
    method = "gcp_kms"
    keys {
      name = "gcp_key"
      kms_crypto_key = "projects/PROJECT_ID/locations/LOCATION/keyRings/RING/cryptoKeys/KEY"
    }
  }
}
```

### Best Practices

1. **Store Keys Securely:**
   ```bash
   # Never commit keys
   echo "TOFU_ENCRYPTION_KEY=xxx" >> .env
   echo ".env" >> .gitignore

   # Use CI/CD secrets
   # GitHub: Repository Settings → Secrets
   # Azure DevOps: Pipeline → Variables → Secret
   ```

2. **Rotate Keys Regularly:**
   ```bash
   # Generate new key
   NEW_KEY=$(openssl rand -base64 32)

   # Add to fallback, update configs
   # Migrate state
   tofu init -migrate-state
   ```

3. **Backup Unencrypted State:**
   ```bash
   # Before enabling encryption
   terraform state pull > backup-unencrypted.tfstate

   # Enable encryption
   tofu init -migrate-state

   # Verify
   tofu state pull  # Should be encrypted in backend
   ```

## Loop-able Import Blocks (OpenTofu 1.7+)

**Terraform 1.5+ (Single Imports):**
```hcl
import {
  to = azurerm_resource_group.example
  id = "/subscriptions/.../resourceGroups/my-rg"
}
```

**OpenTofu 1.7+ (Loop Imports):**
```hcl
# Import multiple resource groups
locals {
  resource_groups = {
    "rg1" = "/subscriptions/.../resourceGroups/rg1"
    "rg2" = "/subscriptions/.../resourceGroups/rg2"
    "rg3" = "/subscriptions/.../resourceGroups/rg3"
  }
}

import {
  for_each = local.resource_groups
  to       = azurerm_resource_group.imported[each.key]
  id       = each.value
}

resource "azurerm_resource_group" "imported" {
  for_each = local.resource_groups
  name     = each.key
  location = "eastus"
}
```

## Early Variable Evaluation (OpenTofu 1.7+)

**Terraform 1.5.x:**
```hcl
# Variables NOT allowed in terraform block
terraform {
  required_version = ">= 1.5.0"  # Static only

  backend "azurerm" {
    resource_group_name  = "terraform-state"  # Static only
    storage_account_name = "tfstate"
  }
}
```

**OpenTofu 1.7+:**
```hcl
# Variables allowed in terraform block
variable "environment" {
  type = string
}

terraform {
  required_version = ">= 1.7.0"

  backend "azurerm" {
    resource_group_name  = "terraform-state-${var.environment}"
    storage_account_name = "tfstate${var.environment}"
    key                  = "${var.environment}.tfstate"
  }
}
```

**OpenTofu 1.8+ (Module Sources):**
```hcl
variable "module_version" {
  type    = string
  default = "v1.0.0"
}

module "networking" {
  source  = "git::https://github.com/org/module.git?ref=${var.module_version}"
  # Dynamic module version!
}
```

## Practical Migration Examples

### Example 1: Small Project Migration

```bash
# 1. Backup existing state
terraform state pull > backup.tfstate

# 2. Install OpenTofu
brew install opentofu

# 3. Test compatibility
tofu init
tofu plan

# 4. Switch to OpenTofu
alias terraform=tofu  # Optional: maintain muscle memory

# 5. Verify everything works
tofu apply
```

### Example 2: Enterprise Migration with Encryption

```bash
# 1. Generate encryption key
ENCRYPTION_KEY=$(openssl rand -base64 32)
echo "TOFU_ENCRYPTION_KEY=$ENCRYPTION_KEY" >> .env.production

# 2. Create encryption config
cat > .tofu <<EOF
encryption {
  state {
    method = "aes_gcm"
    keys {
      name = "prod_key"
      passphrase = env.TOFU_ENCRYPTION_KEY
    }
  }

  plan {
    method = "aes_gcm"
    keys {
      name = "prod_key"
      passphrase = env.TOFU_ENCRYPTION_KEY
    }
  }
}
EOF

# 3. Migrate with encryption
source .env.production
tofu init -migrate-state

# 4. Verify encryption
tofu state pull  # State is now encrypted in backend
```

### Example 3: CI/CD Migration

```yaml
# .github/workflows/terraform.yml
name: Infrastructure

on: [push, pull_request]

jobs:
  opentofu:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup OpenTofu
        uses: opentofu/setup-opentofu@v1
        with:
          tofu_version: 1.8.0

      - name: Init
        run: tofu init
        env:
          TOFU_ENCRYPTION_KEY: ${{ secrets.TOFU_ENCRYPTION_KEY }}

      - name: Plan
        run: tofu plan
        env:
          ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
          ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.ARM_SUBSCRIPTION_ID }}
          ARM_TENANT_ID: ${{ secrets.ARM_TENANT_ID }}
          TOFU_ENCRYPTION_KEY: ${{ secrets.TOFU_ENCRYPTION_KEY }}

      - name: Apply
        if: github.ref == 'refs/heads/main'
        run: tofu apply -auto-approve
        env:
          ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
          ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.ARM_SUBSCRIPTION_ID }}
          ARM_TENANT_ID: ${{ secrets.ARM_TENANT_ID }}
          TOFU_ENCRYPTION_KEY: ${{ secrets.TOFU_ENCRYPTION_KEY }}
```

## Command Compatibility

All Terraform commands work identically in OpenTofu (just replace `terraform` with `tofu`):

```bash
# Terraform          # OpenTofu
terraform init      → tofu init
terraform plan      → tofu plan
terraform apply     → tofu apply
terraform destroy   → tofu destroy
terraform state     → tofu state
terraform import    → tofu import
terraform validate  → tofu validate
terraform fmt       → tofu fmt
terraform output    → tofu output
```

## Community and Support

**OpenTofu Community:**
- GitHub: https://github.com/opentofu/opentofu
- Slack: OpenTofu Workspace
- Forum: OpenTofu Discussions
- Registry: registry.opentofu.org

**Terraform Community:**
- Forum: HashiCorp Discuss
- GitHub: hashicorp/terraform
- Registry: registry.terraform.io
- Support: HashiCorp Support Portal

## Decision Matrix

| Factor | Terraform | OpenTofu |
|--------|-----------|----------|
| **License** | BSL (Proprietary) | MPL 2.0 (Open Source) |
| **State Encryption** | Via HCP Terraform (paid) | Built-in (free) |
| **Enterprise Features** | HCP Terraform (Stacks, HYOK) | Community alternatives |
| **Governance** | HashiCorp/IBM | Linux Foundation |
| **Support** | Commercial support available | Community-driven |
| **Innovation** | HCP-focused | Community-focused |
| **Cost** | Free CLI, paid cloud | Completely free |
| **Compatibility** | Forward-compatible | Terraform 1.5.x compatible |

## Recommendations

**Start with OpenTofu if:**
- Building new infrastructure
- No need for HCP Terraform features
- Want state encryption without cloud costs
- Prefer open-source tools
- Budget-conscious

**Stay with Terraform if:**
- Using HCP Terraform Stacks
- Need Sentinel policies
- Require enterprise support
- Want latest features first (1.10+)
- Established HCP investment

**Easy to Switch:**
- Both are viable long-term
- Migration takes < 1 hour for most projects
- State files portable
- Can evaluate both without commitment

This skill provides comprehensive OpenTofu knowledge for the terraform-expert agent.
