---
name: terraform-state-management
description: |
  Manages Terraform state safely and efficiently. Use when setting up remote state, migrating between backends, handling state locks, preventing state drift, backing up state, or understanding state dependencies and locking mechanisms. Covers GCS backend configuration, state operations, and recovery procedures.

---

# Terraform State Management Skill

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#quick-start)

**How to Implement** → [Step-by-Step](#instructions) | [Examples](#examples)

**Help** → [Requirements](#requirements) | [See Also](#see-also)

## Purpose

Master Terraform state management including remote backends, state locking, drift detection, migrations, and safe recovery procedures. Critical for team collaboration and production safety.

## When to Use

Use this skill when you need to:

- **Set up remote state** - Configure GCS backend for team collaboration
- **Migrate between backends** - Move state from local to remote or between buckets
- **Handle state locks** - Resolve lock timeouts and stale locks
- **Prevent state drift** - Detect when infrastructure differs from state
- **Back up state** - Create and restore state file backups
- **Understand state operations** - View, modify, import, or remove resources from state
- **Recover from state issues** - Fix corrupted or out-of-sync state

**Critical For:**
- Team projects (multiple developers)
- Production environments
- CI/CD pipelines
- State safety and auditability

**Trigger Phrases:**
- "Set up remote state with GCS"
- "Migrate Terraform state to new backend"
- "Fix state lock timeout"
- "Detect state drift"
- "Import existing resource into state"
- "Backup and restore Terraform state"

## Quick Start

Set up remote state with GCS in 3 steps:

```bash
# 1. Create GCS bucket for state
gsutil mb gs://terraform-state-prod
gsutil versioning set on gs://terraform-state-prod

# 2. Configure backend in main.tf
terraform {
  backend "gcs" {
    bucket = "terraform-state-prod"
    prefix = "supplier-charges-hub"
  }
}

# 3. Initialize Terraform
terraform init
# Terraform creates lock file automatically
```

## Instructions

### Step 1: Understand Terraform State

**What is State?**

Terraform's "memory" - a JSON file tracking:
- What resources exist
- Their current configuration
- Metadata and dependencies
- Sensitive data (passwords, keys)

**Why It Matters**:
- State is the source of truth (Terraform compares desired state in .tf files vs current state)
- State file contains secrets (never commit to Git!)
- State determines what Terraform will create/update/delete

**State Example**:
```json
{
  "resources": [
    {
      "type": "google_pubsub_topic",
      "name": "incoming",
      "instances": [
        {
          "attributes": {
            "name": "supplier-charges-hub-incoming",
            "id": "projects/ecp-wtr-supplier-charges-prod/topics/..."
          }
        }
      ]
    }
  ]
}
```

### Step 2: Configure Remote State (Critical!)

Always use remote state for team projects:

```hcl
# main.tf
terraform {
  backend "gcs" {
    bucket = "terraform-state-prod"  # Must exist
    prefix = "supplier-charges-hub"   # Organizes state
  }
}
```

**Why Remote State?**
- ✅ Team collaboration (single source of truth)
- ✅ Automatic state locking (prevents concurrent modifies)
- ✅ Backup and versioning
- ✅ Secrets not in Git
- ✅ Auditable (who changed what, when)

**Local State (Only for local development)**:
```bash
# Default: stores in terraform.tfstate (NOT for team projects!)
terraform init -backend=false
```

### Step 3: Set Up State Locking

State locking prevents concurrent modifications:

```hcl
# main.tf - GCS automatically locks on apply/destroy
terraform {
  backend "gcs" {
    bucket = "terraform-state-prod"
    prefix = "supplier-charges-hub"
    # Lock is created automatically in gs://bucket/prefix/default.tflock
  }
}
```

**How Locking Works**:
```
User A runs "terraform apply"
├─ GCS creates lock file (.tflock)
├─ User A makes changes
└─ GCS deletes lock file

User B tries to run "terraform apply" (during User A's operation)
├─ Terraform detects lock file
├─ Waits for timeout (default 10 minutes)
└─ Fails with "Error acquiring state lock"
```

**Lock Configuration**:
```bash
# Increase lock timeout (default 10m)
terraform apply -lock-timeout=15m

# Disable locking (dangerous - only for testing!)
terraform apply -lock=false
```

### Step 4: Work with State Files

**View State**:
```bash
# List all resources
terraform state list

# Show specific resource
terraform state show google_pubsub_topic.incoming
# Output: Displays current config from state

# Show as JSON
terraform state show -json google_pubsub_topic.incoming | jq
```

**Modify State** (use with caution!):
```bash
# Rename resource (update references in .tf files too!)
terraform state mv google_pubsub_topic.old google_pubsub_topic.new

# Remove resource from state (don't delete it in GCP!)
terraform state rm google_pubsub_topic.incoming
# Use when Terraform should stop managing a resource

# Import existing resource into state
terraform import google_pubsub_topic.incoming \
  projects/ecp-wtr-supplier-charges-prod/topics/existing-topic
```

**Pull/Push State** (rarely needed):
```bash
# Download state locally
terraform state pull > backup.tfstate

# Upload state (careful!)
terraform state push backup.tfstate

# Back up state
gsutil cp gs://terraform-state-prod/supplier-charges-hub/default.tfstate ./backup.tfstate
```

### Step 5: Detect and Fix State Drift

**State Drift**: When actual infrastructure differs from Terraform state.

**Causes**:
- Manual changes in GCP console
- Deletion outside Terraform
- Failed Terraform run
- Provider bugs

**Detection**:
```bash
# Refresh state (read actual infrastructure)
terraform refresh
# Updates state to match reality, shows changes

# Plan shows drift
terraform plan
# If plan shows changes you didn't make, you have drift
```

**Resolution**:
```bash
# Option 1: Accept reality (update state)
terraform refresh
terraform apply
# Applies any missing resource definitions

# Option 2: Revert infrastructure to match state
terraform destroy
terraform apply
# Deletes and recreates everything

# Option 3: Selective fix
terraform import google_pubsub_topic.incoming \
  projects/ecp-wtr-supplier-charges-prod/topics/my-topic
# Imports actual resource back into state
```

### Step 6: Migrate State Between Backends

**Scenario**: Moving from local state to GCS backend.

```bash
# 1. Add backend configuration
# main.tf
terraform {
  backend "gcs" {
    bucket = "terraform-state-prod"
    prefix = "supplier-charges-hub"
  }
}

# 2. Initialize with state migration
terraform init -migrate-state

# Terraform prompts:
# Do you want to copy existing state to the new backend?
# > yes

# 3. Verify migration
terraform state list
# Should show all your resources

# 4. Delete local state (optional)
rm -f terraform.tfstate*
```

**Migrating Between GCS Buckets**:
```bash
# 1. Update backend config
terraform {
  backend "gcs" {
    bucket = "terraform-state-new-bucket"
    prefix = "supplier-charges-hub"
  }
}

# 2. Migrate
terraform init -migrate-state

# 3. Verify
terraform state list
```

### Step 7: Backup and Restore State

**Regular Backups**:
```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="./state-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
gsutil cp gs://terraform-state-prod/supplier-charges-hub/default.tfstate \
  $BACKUP_DIR/tfstate_$TIMESTAMP.json

# Keep only last 30 days
find $BACKUP_DIR -mtime +30 -delete
```

**Restore from Backup**:
```bash
# 1. Check available backups
ls -lh state-backups/

# 2. Restore specific backup
gsutil cp ./state-backups/tfstate_20251114_100000.json \
  gs://terraform-state-prod/supplier-charges-hub/default.tfstate

# 3. Verify
terraform state list
terraform plan
```

## Examples

### Example 1: Setting Up GCS Backend from Scratch

```bash
# 1. Create bucket
gsutil mb gs://terraform-state-production
gsutil versioning set on gs://terraform-state-production

# 2. Enable access logging
gsutil logging set on -b gs://terraform-logs gs://terraform-state-production

# 3. Add backend config to main.tf
cat >> main.tf << 'EOF'
terraform {
  backend "gcs" {
    bucket = "terraform-state-production"
    prefix = "supplier-charges-hub/prod"
  }
}
EOF

# 4. Initialize
rm -rf .terraform/  # Clean local state
terraform init

# Output:
# Initializing the backend...
# bucket: terraform-state-production
# prefix: supplier-charges-hub/prod
# Successfully configured the backend "gcs"!
```

### Example 2: Recovering from Stale Lock

```bash
# Error occurs
# Error: Error acquiring the state lock
# Lock Info:
#   ID: 1234567890
#   Created: 2025-11-14 10:00:00 UTC

# 1. Check if operation is actually running
gcloud compute operations list --filter="status:RUNNING"
# No output = no operation running

# 2. Force unlock
terraform force-unlock 1234567890

# 3. Re-plan to verify state
terraform refresh
terraform plan
# Should succeed
```

### Example 3: Detecting and Fixing State Drift

```bash
# Someone manually created a Pub/Sub topic in GCP console

# 1. Detect drift
terraform plan
# Output shows: google_pubsub_topic.incoming created outside terraform

# 2. Option A: Import into state
terraform import google_pubsub_topic.incoming \
  projects/ecp-wtr-supplier-charges-prod/topics/manual-topic

terraform state show google_pubsub_topic.incoming
# Now Terraform knows about it

# 3. Option B: Delete from state (if should be managed elsewhere)
terraform state rm google_pubsub_topic.incoming
```

### Example 4: State Migration Timeline

```bash
# Project grows, want centralized state management

# Current: Local state
terraform state list
# Stored in ./terraform.tfstate

# Step 1: Create centralized backend
gsutil mb gs://company-terraform-state
gsutil versioning set on gs://company-terraform-state

# Step 2: Configure in main.tf
terraform {
  backend "gcs" {
    bucket = "company-terraform-state"
    prefix = "supplier-charges-hub"
  }
}

# Step 3: Migrate
terraform init -migrate-state
# Terraform: "Do you want to copy existing state to the new backend?"
# Yes

# Step 4: Verify
terraform state list
# All resources present

# Step 5: Remove local state (now safe)
rm -f .gitignore  # Remove terraform.tfstate* from ignore
rm -f terraform.tfstate terraform.tfstate.backup
git add .gitignore
git commit -m "migrate: move state to centralized GCS backend"
```

## Requirements

- Terraform 1.x+
- GCP credentials (gcloud auth or service account)
- GCS bucket (for remote state)
- gsutil CLI tool installed
- Git (for version control)

## See Also

- [terraform skill](../terraform-basics/SKILL.md) - General Terraform reference
- [terraform-troubleshooting](../terraform-troubleshooting/SKILL.md) - Fixing state errors
- [terraform-gcp-integration](../terraform-gcp-integration/SKILL.md) - GCP backend details
