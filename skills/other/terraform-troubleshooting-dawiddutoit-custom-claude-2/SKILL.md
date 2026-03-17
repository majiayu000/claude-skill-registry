---
name: terraform-troubleshooting
description: |
  Debugs and fixes Terraform errors systematically. Use when encountering Terraform failures, state lock issues, provider errors, syntax problems, or unexpected infrastructure changes. Includes debugging workflows, error categorization, common GCP-specific issues, and recovery procedures.

---

# Terraform Troubleshooting Skill

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#quick-start)

**How to Implement** → [Step-by-Step](#instructions) | [Examples](#examples)

**Help** → [Requirements](#requirements) | [See Also](#see-also)

## Purpose

Troubleshoot Terraform errors efficiently using systematic debugging workflows, detailed error analysis, and proven solutions for common problems.

## When to Use

Use this skill when you encounter:

- **Terraform failures** - Apply or plan commands fail with errors
- **State lock issues** - Lock timeout or concurrent modification errors
- **Provider errors** - GCP API errors, authentication failures
- **Syntax problems** - Invalid HCL, type mismatches, missing arguments
- **Unexpected infrastructure changes** - State drift, unintended modifications
- **Version conflicts** - Provider or Terraform version incompatibilities
- **Permission errors** - GCP IAM or service account issues

**Error Categories:**
1. **Language Errors** - Syntax, configuration, type mismatches
2. **State Errors** - Lock timeouts, corruption, concurrent access
3. **Core Errors** - Terraform version, plugin issues
4. **Provider Errors** - GCP API, permissions, authentication

**Trigger Phrases:**
- "Terraform apply failed"
- "Fix state lock error"
- "Debug Terraform syntax error"
- "Resolve GCP permission denied"
- "Fix state drift"
- "Terraform version incompatibility"

## Quick Start

Diagnose a Terraform error in 5 minutes:

```bash
# 1. Enable debug logging
export TF_LOG=DEBUG
export TF_LOG_PATH=/tmp/terraform.log

# 2. Validate syntax
terraform validate

# 3. Run plan with detailed output
terraform plan -out=tfplan

# 4. Review logs for errors
cat /tmp/terraform.log | grep -i error

# 5. Disable logging when done
unset TF_LOG
unset TF_LOG_PATH
```

## Instructions

### Step 1: Categorize the Error

Terraform errors fall into four categories. Identify which type you're dealing with:

**1. Language Errors** (Syntax, configuration)
- Invalid HCL syntax
- Type mismatches
- Missing required arguments
- Example: `Error: Invalid value for module argument`

**2. State Errors** (State lock, corruption)
- Lock timeouts
- Concurrent modifications
- State file corruption
- Example: `Error: Error acquiring the state lock`

**3. Core Errors** (Terraform version, plugins)
- Version incompatibility
- Missing plugins
- Initialize issues
- Example: `Error: Unsupported Terraform version`

**4. Provider Errors** (GCP API, permissions)
- GCP API errors
- Authentication issues
- Permission denied
- Example: `Error: Error creating PubSub topic: googleapi: Error 403`

### Step 2: Enable Detailed Logging

```bash
# Set debug logging
export TF_LOG=DEBUG
export TF_LOG_PATH=/tmp/terraform.log

# Available levels: TRACE, DEBUG, INFO, WARN, ERROR
# TRACE: Most verbose, includes all operations
# DEBUG: Detailed, good for troubleshooting
# INFO: General information
```

**Reading Logs**:
```bash
# Filter for errors
cat /tmp/terraform.log | grep -i error

# Filter for specific resource
cat /tmp/terraform.log | grep "google_pubsub"

# Filter for timestamps
cat /tmp/terraform.log | grep "2025-11-14"
```

### Step 3: Execute Troubleshooting Workflow

Follow this sequence for systematic debugging:

```bash
# 1. Validate HCL syntax
terraform validate
# ✓ Catches syntax, type, and required argument errors
# ✗ Does NOT validate against actual cloud state

# 2. Format code (catches formatting issues)
terraform fmt -check -recursive
terraform fmt -recursive  # Fix formatting

# 3. Refresh state (sync with actual infrastructure)
terraform refresh
# ✓ Updates Terraform state to match real infrastructure
# ✗ Does NOT make changes, only reads

# 4. Re-initialize (if provider issues)
terraform init -upgrade
# ✓ Updates provider versions to latest compatible
# ✗ Requires time for downloads

# 5. Plan with detailed output
terraform plan -out=tfplan
# ✓ Shows exactly what will change
# ✗ Does NOT make changes

# 6. Check logs
grep -i error /tmp/terraform.log
```

### Step 4: Handle Specific Error Types

#### State Lock Errors

**Problem**: Another Terraform operation is running or left a stale lock.

```bash
# Option 1: Wait for lock (if operation is legitimately running)
terraform apply -lock-timeout=10m

# Option 2: Force unlock (use with caution!)
terraform force-unlock LOCK_ID
# Get LOCK_ID from error message

# Option 3: Manual recovery (last resort)
# Delete lock file from GCS backend
gsutil rm gs://bucket/prefix/default.tflock
```

**Prevention**:
- Use CI/CD with job queuing (prevents concurrent runs)
- Communicate with team before applying
- Use Terraform Cloud/Enterprise for automatic locking

#### Cycle Errors (Circular Dependencies)

**Problem**: Resources depend on each other in a circle.

```
Error: Cycle: resource_a, resource_b, resource_a
```

**Solution**: Break the cycle by using `depends_on` or reordering:

```hcl
# ❌ BAD: Circular reference
resource "google_compute_firewall" "allow_app" {
  source_tags = [google_compute_instance.app.tags[0]]
}
resource "google_compute_instance" "app" {
  tags = [google_compute_firewall.allow_app.name]
}

# ✅ GOOD: Break dependency
resource "google_compute_firewall" "allow_app" {
  source_tags = ["app"]  # Use explicit string instead
}
resource "google_compute_instance" "app" {
  tags = ["app"]  # Explicit value
}
```

#### Provider Version Conflicts

**Problem**: Provider version constraint conflict.

```
Error: Incompatible provider version

Terraform requires >= 5.26.0, < 5.27.0
You have 6.0.0 installed
```

**Solution**:
```bash
# 1. Check current version
terraform version

# 2. Lock to compatible version
# In main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.26.0"  # Allows 5.26.x, not 5.27.0
    }
  }
}

# 3. Re-initialize
terraform init -upgrade

# 4. Commit .terraform.lock.hcl
git add .terraform.lock.hcl
git commit -m "lock: pin Google provider to 5.26.0"
```

#### GCP Permission Errors

**Problem**: Service account lacks required GCP permissions.

```
Error: Error creating PubSub topic: googleapi: Error 403:
The caller does not have permission
```

**Solution**:
```bash
# 1. Check current authentication
gcloud auth list
gcloud config get-value project

# 2. Verify service account permissions
gcloud projects get-iam-policy ecp-wtr-supplier-charges-prod \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:app-runtime@*"

# 3. Grant required role
gcloud projects add-iam-policy-binding ecp-wtr-supplier-charges-prod \
  --member="serviceAccount:app-runtime@project.iam.gserviceaccount.com" \
  --role="roles/pubsub.editor"

# 4. Re-plan
terraform plan
```

#### State Out of Sync

**Problem**: Terraform state doesn't match actual infrastructure.

```bash
# Detect drift
terraform plan
# Shows changes that don't exist in your .tf files

# Sync state
terraform refresh
# Updates state to match real infrastructure

# Manual fix (if refresh fails)
terraform import google_pubsub_topic.incoming \
  projects/ecp-wtr-supplier-charges-prod/topics/my-topic

# Remove from state (if resource manually deleted)
terraform state rm google_pubsub_topic.incoming
```

### Step 5: Review and Recover

```bash
# View recent state changes
terraform state list
terraform state show google_pubsub_topic.incoming

# See what changed in last apply
terraform show tfplan | head -50

# Rollback by re-applying previous configuration
git checkout HEAD~1  # Go back one commit
terraform plan
terraform apply
```

## Examples

### Example 1: Debugging State Lock

```bash
# Error occurs
# Error: Error acquiring the state lock
# Lock Info:
#   ID:        abc123def456
#   Path:      gs://terraform-state-prod/supplier-charges-hub/default.tflock
#   Created:   2025-11-14 10:30:00 UTC

# Step 1: Check if operation is running
gcloud compute operations list --filter="status:RUNNING"

# Step 2: If no running operation, force unlock
terraform force-unlock abc123def456

# Step 3: If force-unlock fails, delete lock file
gsutil rm gs://terraform-state-prod/supplier-charges-hub/default.tflock

# Step 4: Re-plan to verify state is correct
terraform refresh
terraform plan
```

### Example 2: Fixing Syntax Error

```bash
# Error occurs
# Error: Invalid value for module argument

# Step 1: Validate syntax
terraform validate

# Output shows exactly what's wrong:
# Error: Missing required argument
#   on pubsub.tf line 5, in resource "google_pubsub_topic" "topics":
#    5: resource "google_pubsub_topic" "topics" {
# The argument "name" is required, but was not set.

# Step 2: Review and fix the file
# Add missing argument:
resource "google_pubsub_topic" "topics" {
  name = "my-topic"  # Add this
}

# Step 3: Validate again
terraform validate
```

### Example 3: GCP Permission Recovery

```bash
# Error occurs
# Error creating PubSub topic: googleapi: Error 403

# Step 1: Check authentication
gcloud auth list
gcloud config get-value project

# Step 2: Get current IAM bindings
gcloud projects get-iam-policy ecp-wtr-supplier-charges-prod

# Step 3: Add Pub/Sub Editor role
gcloud projects add-iam-policy-binding ecp-wtr-supplier-charges-prod \
  --member="serviceAccount:terraform@project.iam.gserviceaccount.com" \
  --role="roles/pubsub.editor"

# Step 4: Re-run Terraform
terraform plan
terraform apply
```

## Requirements

- Terraform 1.x+ installed
- GCP credentials configured (gcloud auth or service account key)
- Logging environment (for TF_LOG_PATH)
- GCP CLI tools installed (`gcloud`, `gsutil`)

## See Also

- [terraform-basics](../terraform-basics/SKILL.md) - General Terraform reference
- [terraform-state-management](../terraform-state-management/SKILL.md) - Advanced state patterns
- [terraform-gcp-integration](../terraform-gcp-integration/SKILL.md) - GCP-specific issues
