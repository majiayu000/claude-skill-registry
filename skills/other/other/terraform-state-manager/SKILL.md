---
name: terraform-state-manager
description: Эксперт по Terraform state. Используй для управления состоянием, remote backends, state migration и troubleshooting.
---

# Terraform State Manager

Эксперт по управлению Terraform state файлами, remote backends, state operations и troubleshooting.

## Core Principles

### State File Security

```yaml
state_security_principles:
  - principle: "Never commit state to version control"
    reason: "State files contain sensitive information including secrets"

  - principle: "Use remote backends for team environments"
    reason: "Enables collaboration and prevents state corruption"

  - principle: "Enable encryption at rest and in transit"
    reason: "Protects sensitive data in state files"

  - principle: "Implement state locking"
    reason: "Prevents concurrent modifications and corruption"

  - principle: "Regular backups with retention policy"
    reason: "Enables recovery from accidental deletions or corruption"
```

---

## Backend Configuration

### AWS S3 Backend (Recommended)

```hcl
# backend.tf

terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "environments/prod/infrastructure/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "alias/terraform-state-key"
    dynamodb_table = "terraform-state-lock"

    # Optional: Assume role for cross-account access
    role_arn       = "arn:aws:iam::123456789012:role/TerraformStateAccess"

    # Optional: Workspace-based key prefix
    workspace_key_prefix = "workspaces"
  }
}
```

### S3 Backend Infrastructure Setup

```hcl
# state-backend/main.tf - Run this first with local backend

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# S3 Bucket for State
resource "aws_s3_bucket" "terraform_state" {
  bucket = "${var.company}-terraform-state-${var.region}"

  tags = {
    Name        = "Terraform State"
    Environment = "shared"
    ManagedBy   = "terraform"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.terraform_state.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    id     = "state-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 90
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }
  }
}

# DynamoDB Table for State Locking
resource "aws_dynamodb_table" "terraform_lock" {
  name           = "terraform-state-lock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name        = "Terraform State Lock"
    Environment = "shared"
    ManagedBy   = "terraform"
  }
}

# KMS Key for State Encryption
resource "aws_kms_key" "terraform_state" {
  description             = "KMS key for Terraform state encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow Terraform Role"
        Effect = "Allow"
        Principal = {
          AWS = var.terraform_role_arn
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    Name = "Terraform State Key"
  }
}

resource "aws_kms_alias" "terraform_state" {
  name          = "alias/terraform-state-key"
  target_key_id = aws_kms_key.terraform_state.key_id
}

data "aws_caller_identity" "current" {}

# Outputs
output "state_bucket_name" {
  value = aws_s3_bucket.terraform_state.id
}

output "lock_table_name" {
  value = aws_dynamodb_table.terraform_lock.name
}

output "kms_key_arn" {
  value = aws_kms_key.terraform_state.arn
}
```

### Azure Backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "mycompanytfstate"
    container_name       = "tfstate"
    key                  = "prod/infrastructure.tfstate"

    # Enable encryption
    use_azuread_auth = true
  }
}
```

### Google Cloud Backend

```hcl
terraform {
  backend "gcs" {
    bucket  = "mycompany-terraform-state"
    prefix  = "terraform/state"

    # Enable encryption
    encryption_key = "projects/myproject/locations/global/keyRings/terraform/cryptoKeys/state-key"
  }
}
```

---

## State Operations

### Essential State Commands

```bash
# View all resources in state
terraform state list

# View specific resource details
terraform state show aws_instance.web

# View state as JSON
terraform show -json | jq '.values.root_module.resources'

# Pull remote state to local file
terraform state pull > terraform.tfstate.backup

# Push local state to remote (use with caution!)
terraform state push terraform.tfstate

# Get outputs from state
terraform output -json
```

### Resource Refactoring (terraform state mv)

```bash
# Rename a resource
terraform state mv aws_instance.web aws_instance.app_server

# Move resource to a module
terraform state mv aws_instance.web module.compute.aws_instance.web

# Move resource from module to root
terraform state mv module.compute.aws_instance.web aws_instance.web

# Move resource between modules
terraform state mv module.old.aws_instance.web module.new.aws_instance.web

# Move entire module
terraform state mv module.old module.new

# Move resource to different state file
terraform state mv -state-out=other.tfstate aws_instance.web aws_instance.web
```

### Import Existing Resources

```bash
# Basic import
terraform import aws_instance.web i-1234567890abcdef0

# Import with provider alias
terraform import -provider=aws.west aws_instance.web i-1234567890abcdef0

# Import into module
terraform import module.vpc.aws_vpc.main vpc-12345678

# Import with for_each
terraform import 'aws_instance.servers["web"]' i-1234567890abcdef0

# Generate import blocks (Terraform 1.5+)
terraform plan -generate-config-out=generated.tf
```

### Import Block (Terraform 1.5+)

```hcl
# imports.tf

import {
  to = aws_instance.web
  id = "i-1234567890abcdef0"
}

import {
  to = aws_vpc.main
  id = "vpc-12345678"
}

import {
  to = module.rds.aws_db_instance.main
  id = "mydb-instance"
}

# With for_each
import {
  for_each = var.existing_buckets
  to       = aws_s3_bucket.imported[each.key]
  id       = each.value
}
```

### Remove Resources from State

```bash
# Remove single resource (doesn't destroy actual resource)
terraform state rm aws_instance.web

# Remove resource in module
terraform state rm module.compute.aws_instance.web

# Remove entire module
terraform state rm module.old_module

# Remove with for_each
terraform state rm 'aws_instance.servers["web"]'

# Dry run - show what would be removed
terraform state rm -dry-run aws_instance.web
```

### Replace/Recreate Resources

```bash
# Force replacement of resource (Terraform 0.15.2+)
terraform apply -replace="aws_instance.web"

# Taint resource (legacy, use -replace instead)
terraform taint aws_instance.web

# Untaint resource
terraform untaint aws_instance.web
```

---

## Workspace Management

### Workspace Commands

```bash
# List all workspaces
terraform workspace list

# Create new workspace
terraform workspace new staging

# Select workspace
terraform workspace select prod

# Show current workspace
terraform workspace show

# Delete workspace (must not be current)
terraform workspace delete staging
```

### Workspace-Aware Configuration

```hcl
# locals.tf

locals {
  environment = terraform.workspace

  # Environment-specific configurations
  config = {
    dev = {
      instance_type = "t3.small"
      min_size      = 1
      max_size      = 2
      multi_az      = false
    }
    staging = {
      instance_type = "t3.medium"
      min_size      = 2
      max_size      = 4
      multi_az      = true
    }
    prod = {
      instance_type = "t3.large"
      min_size      = 3
      max_size      = 10
      multi_az      = true
    }
  }

  env_config = local.config[local.environment]
}

# Use in resources
resource "aws_instance" "app" {
  instance_type = local.env_config.instance_type

  tags = {
    Environment = local.environment
  }
}
```

### Backend with Workspace Prefix

```hcl
terraform {
  backend "s3" {
    bucket               = "terraform-state"
    key                  = "app/terraform.tfstate"
    region               = "us-east-1"
    workspace_key_prefix = "workspaces"
    dynamodb_table       = "terraform-lock"
    encrypt              = true
  }
}

# Results in state paths:
# - workspaces/dev/app/terraform.tfstate
# - workspaces/staging/app/terraform.tfstate
# - workspaces/prod/app/terraform.tfstate
```

---

## State Locking

### DynamoDB Lock Table Schema

```hcl
resource "aws_dynamodb_table" "terraform_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  # Enable encryption
  server_side_encryption {
    enabled = true
  }

  # Enable point-in-time recovery
  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name = "Terraform State Lock Table"
  }
}
```

### Force Unlock

```bash
# Force unlock (use only when you're sure no operation is running)
terraform force-unlock LOCK_ID

# The lock ID is shown in the error message when locked:
# "Error: Error locking state: Error acquiring the state lock: ConditionalCheckFailedException..."
# Lock ID: 12345678-1234-1234-1234-123456789012
```

### Lock Troubleshooting

```bash
# Check for existing locks in DynamoDB
aws dynamodb scan \
  --table-name terraform-state-lock \
  --projection-expression "LockID, Info" \
  --output table

# Delete stale lock manually (last resort)
aws dynamodb delete-item \
  --table-name terraform-state-lock \
  --key '{"LockID": {"S": "terraform-state/path/to/terraform.tfstate"}}'
```

---

## State Migration

### Migrate from Local to Remote Backend

```bash
# Step 1: Add backend configuration to your Terraform files
# backend.tf (see S3 backend example above)

# Step 2: Initialize with migration
terraform init -migrate-state

# Terraform will prompt:
# Do you want to copy existing state to the new backend?
# Enter "yes"

# Step 3: Verify migration
terraform state list
terraform plan  # Should show no changes
```

### Migrate Between Remote Backends

```bash
# Step 1: Pull current state
terraform state pull > terraform.tfstate.backup

# Step 2: Update backend configuration
# Change backend.tf to new backend

# Step 3: Reinitialize with migration
terraform init -migrate-state -force-copy

# Step 4: Verify
terraform state list
terraform plan
```

### Split State into Multiple States

```bash
# Scenario: Split monolithic state into separate states for each environment

# Step 1: Create backup
terraform state pull > full-state.backup.json

# Step 2: Create new state file for specific resources
terraform state mv -state-out=env/prod/terraform.tfstate \
  module.prod_vpc module.prod_vpc

terraform state mv -state-out=env/prod/terraform.tfstate \
  module.prod_app module.prod_app

# Step 3: Initialize new state directories with appropriate backends
cd env/prod
terraform init
terraform state push terraform.tfstate
```

---

## Recovery Procedures

### Recover from Corrupted State

```bash
# Step 1: Check S3 bucket versioning for previous versions
aws s3api list-object-versions \
  --bucket terraform-state \
  --prefix "path/to/terraform.tfstate" \
  --max-keys 10

# Step 2: Download previous version
aws s3api get-object \
  --bucket terraform-state \
  --key "path/to/terraform.tfstate" \
  --version-id "versionId123" \
  recovered-state.json

# Step 3: Validate the recovered state
terraform show -json recovered-state.json | jq '.values'

# Step 4: Push recovered state
terraform state push recovered-state.json
```

### Recover from Deleted State

```bash
# Option 1: Recover from S3 versioning
aws s3api list-object-versions \
  --bucket terraform-state \
  --prefix "path/to/terraform.tfstate"

# Look for DeleteMarker and recover the version before it

# Option 2: Recover from DynamoDB backup (if PITR enabled)
aws dynamodb restore-table-to-point-in-time \
  --source-table-name terraform-state-lock \
  --target-table-name terraform-state-lock-recovered \
  --restore-date-time 2024-01-15T10:00:00Z

# Option 3: Reimport all resources
# Create import blocks for each resource and run terraform apply
```

### Rebuild State from Scratch

```hcl
# imports.tf - Generate these by examining your infrastructure

# Use AWS CLI to discover resources
# aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId, Tags]'

import {
  to = aws_vpc.main
  id = "vpc-12345678"
}

import {
  to = aws_subnet.public["a"]
  id = "subnet-aaaaaaaa"
}

import {
  to = aws_subnet.public["b"]
  id = "subnet-bbbbbbbb"
}

import {
  to = aws_instance.web
  id = "i-1234567890abcdef0"
}

# Then run:
# terraform plan -generate-config-out=generated_resources.tf
# Review and merge generated_resources.tf into your configuration
# terraform apply
```

---

## Drift Detection

### Detect Configuration Drift

```bash
# Standard drift detection
terraform plan -detailed-exitcode
# Exit codes:
# 0 = No changes
# 1 = Error
# 2 = Changes detected (drift)

# Machine-readable drift detection
terraform plan -json | jq '.resource_changes[] | select(.change.actions != ["no-op"])'

# Generate drift report
terraform plan -json > plan.json
jq '[.resource_changes[] | select(.change.actions != ["no-op"]) | {
  address: .address,
  actions: .change.actions,
  before: .change.before,
  after: .change.after
}]' plan.json > drift-report.json
```

### Refresh State (Sync with Reality)

```bash
# Refresh state without applying changes
terraform refresh

# Or use plan with refresh-only (Terraform 0.15.4+)
terraform apply -refresh-only

# This updates state to match actual infrastructure
# without making any changes to infrastructure
```

### Automated Drift Detection Script

```bash
#!/bin/bash
# drift-check.sh

set -e

WORKSPACES=("dev" "staging" "prod")
DRIFT_FOUND=false

for ws in "${WORKSPACES[@]}"; do
    echo "Checking drift in workspace: $ws"

    terraform workspace select "$ws"

    # Run plan with detailed exit code
    set +e
    terraform plan -detailed-exitcode -out=plan-$ws.tfplan > /dev/null 2>&1
    EXIT_CODE=$?
    set -e

    if [ $EXIT_CODE -eq 2 ]; then
        echo "⚠️  DRIFT DETECTED in $ws"
        terraform show -json plan-$ws.tfplan | jq '.resource_changes[] | select(.change.actions != ["no-op"]) | .address'
        DRIFT_FOUND=true
    elif [ $EXIT_CODE -eq 0 ]; then
        echo "✅ No drift in $ws"
    else
        echo "❌ Error checking $ws"
    fi

    rm -f plan-$ws.tfplan
done

if [ "$DRIFT_FOUND" = true ]; then
    exit 2
fi
```

---

## Security Best Practices

### IAM Policy for State Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "TerraformStateAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::terraform-state",
        "arn:aws:s3:::terraform-state/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:PrincipalTag/Team": "${aws:ResourceTag/Team}"
        }
      }
    },
    {
      "Sid": "TerraformStateLock",
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/terraform-state-lock"
    },
    {
      "Sid": "TerraformStateEncryption",
      "Effect": "Allow",
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:GenerateDataKey"
      ],
      "Resource": "arn:aws:kms:*:*:key/terraform-state-key-id"
    }
  ]
}
```

### State File Inspection

```bash
# Check for sensitive data in state
terraform state pull | jq '.resources[].instances[].attributes |
  to_entries[] |
  select(.key | test("password|secret|key|token"; "i")) |
  {resource: input.address, sensitive_field: .key}'

# List all sensitive values
terraform state pull | jq '[
  .resources[] |
  .instances[] |
  .attributes |
  to_entries[] |
  select(.value != null and (.key | test("password|secret|key|token|credential"; "i")))
] | length'
```

---

## CI/CD Integration

### GitHub Actions State Management

```yaml
# .github/workflows/terraform.yml

name: Terraform

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  TF_VAR_environment: ${{ github.ref == 'refs/heads/main' && 'prod' || 'staging' }}

jobs:
  terraform:
    runs-on: ubuntu-latest

    permissions:
      id-token: write
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0

      - name: Terraform Init
        run: terraform init -backend-config="key=envs/${{ env.TF_VAR_environment }}/terraform.tfstate"

      - name: Terraform Plan
        id: plan
        run: terraform plan -no-color -out=tfplan
        continue-on-error: true

      - name: Comment PR with Plan
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const output = `#### Terraform Plan 📖
            \`\`\`
            ${{ steps.plan.outputs.stdout }}
            \`\`\`
            `;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve tfplan
```

---

## Лучшие практики

1. **Всегда используй remote backend** — local state только для экспериментов
2. **Включай versioning для state bucket** — возможность recovery
3. **Используй state locking** — предотвращает коррупцию state
4. **Шифруй state at rest и in transit** — содержит sensitive data
5. **Регулярно тестируй recovery procedures** — до того как понадобится
6. **Автоматизируй drift detection** — в CI/CD pipeline
7. **Разделяй state по окружениям** — workspaces или отдельные backends
8. **Ограничивай доступ к state** — IAM policies с минимальными правами
