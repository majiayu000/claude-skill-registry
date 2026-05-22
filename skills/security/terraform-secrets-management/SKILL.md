---
name: terraform-secrets-management
description: |
  Handle sensitive data securely in Terraform. Use when managing passwords, API keys, database credentials,
  encryption keys, or other secrets. Covers Google Secret Manager integration, preventing secrets in state,
  IAM-based secret access, encryption, and security best practices.
---

# Terraform Secrets Management Skill

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#quick-start)

**How to Implement** → [Step-by-Step](#instructions) | [Examples](#examples)

**Help** → [Requirements](#requirements) | [See Also](#see-also)

## Purpose

Manage sensitive data securely without storing secrets in Terraform code or state files. Learn to use Google Secret Manager, IAM bindings, sensitive outputs, and secure secret workflows.

## When to Use

Use this skill when you need to:

- **Manage passwords securely** - Database passwords, admin credentials
- **Handle API keys** - External service authentication tokens
- **Store database credentials** - Connection strings, usernames, passwords
- **Manage encryption keys** - KMS keys, JWT secrets
- **Pass secrets to applications** - Environment variables, Kubernetes secrets
- **Rotate secrets safely** - Update secret versions without downtime
- **Prevent secrets in state** - Keep sensitive data out of Terraform state files

**Security Requirements:**
- Never hardcode secrets in .tf files
- Never commit secrets to Git
- Use Google Secret Manager for all sensitive values
- Apply least privilege IAM permissions

**Trigger Phrases:**
- "Store database password in Secret Manager"
- "Retrieve secret from Google Secret Manager"
- "Pass secrets to Kubernetes deployment"
- "Rotate secrets safely"
- "Prevent secrets in Terraform state"

## Quick Start

Retrieve a secret from Google Secret Manager safely in 3 steps:

```bash
# 1. Create secret in GCP
echo -n "MySecretPassword123" | gcloud secrets create db-password --data-file=-

# 2. Grant service account access
gcloud secrets add-iam-policy-binding db-password \
  --member="serviceAccount:app-runtime@project.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# 3. Use in Terraform
data "google_secret_manager_secret_version" "db_password" {
  secret = "db-password"
}

resource "google_sql_database_instance" "main" {
  settings {
    database_flags {
      name  = "password"
      value = data.google_secret_manager_secret_version.db_password.secret_data
    }
  }
}
```

## Instructions

### Step 1: Understand Secret Management Problem

**The Problem**:
```hcl
# ❌ NEVER DO THIS
variable "db_password" {
  type    = string
  default = "SuperSecret123"  # Now in Git history forever!
}

# Even worse
resource "google_sql_database_instance" "main" {
  settings {
    database_flags {
      name  = "password"
      value = "SuperSecret123"  # Hardcoded secret!
    }
  }
}
```

**Why This is Bad**:
- ✗ Secrets exposed in Git history (impossible to remove)
- ✗ Secrets in `.tfstate` file
- ✗ Secrets visible in plan output
- ✗ Secrets accessible to anyone with Git access
- ✗ Violates compliance (SOC2, PCI-DSS)

**The Solution**: Use Google Secret Manager

### Step 2: Set Up Google Secret Manager

**Create Secrets**:
```bash
# Create secret
echo -n "database-password-here" | gcloud secrets create db-password \
  --data-file=-

# Or create empty secret
gcloud secrets create api-key

# Update secret value
echo -n "new-password-value" | gcloud secrets versions add db-password \
  --data-file=-

# List secrets
gcloud secrets list

# View secret value (be careful!)
gcloud secrets versions access latest --secret="db-password"
```

**Secret Naming Convention**:
- Use lowercase with hyphens: `db-password`, `api-key`, `jwt-secret`
- Include environment: `db-password-prod`, `api-key-labs`
- Be specific: `github-pat` (Personal Access Token) instead of `github-key`

### Step 3: Configure IAM for Secrets

**Principle**: Only grant access to secrets that services actually need.

```bash
# Grant service account access to specific secret
gcloud secrets add-iam-policy-binding db-password \
  --member="serviceAccount:app-runtime@ecp-wtr-supplier-charges-prod.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Grant access to multiple secrets
gcloud secrets add-iam-policy-binding db-password \
  --member="serviceAccount:app-runtime@..." \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding api-key \
  --member="serviceAccount:app-runtime@..." \
  --role="roles/secretmanager.secretAccessor"

# View who has access
gcloud secrets get-iam-policy db-password
```

**Terraform IAM**:
```hcl
# Grant service account secret access
data "google_service_account" "app_runtime" {
  account_id = "app-runtime"
}

resource "google_secret_manager_secret_iam_member" "db_password_access" {
  secret_id = "db-password"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${data.google_service_account.app_runtime.email}"
}
```

### Step 4: Read Secrets in Terraform

**Read Secret Value**:
```hcl
# Data source to read secret
data "google_secret_manager_secret_version" "db_password" {
  secret = "db-password"
  # version defaults to "latest"
}

# Use secret in resource
resource "google_sql_database_instance" "main" {
  settings {
    database_flags {
      name  = "password"
      value = data.google_secret_manager_secret_version.db_password.secret_data
    }
  }
}

# Output (marks as sensitive to hide in logs)
output "db_instance_connection_string" {
  value     = google_sql_database_instance.main.connection_name
  sensitive = true  # Won't print to console
}
```

**Secret Versions**:
```hcl
# Read latest version
data "google_secret_manager_secret_version" "latest" {
  secret = "db-password"
  version = "latest"
}

# Read specific version
data "google_secret_manager_secret_version" "v1" {
  secret = "db-password"
  version = "1"
}

# Read all versions
data "google_secret_manager_secret" "db_password" {
  secret_id = "db-password"
}

# List versions
data "google_secret_manager_secret_version" "versions" {
  for_each = data.google_secret_manager_secret.db_password.versions
  secret   = "db-password"
  version  = each.key
}
```

### Step 5: Pass Secrets to Applications

**Method 1: Environment Variables**:
```hcl
# GKE deployment
resource "kubernetes_deployment" "app" {
  spec {
    template {
      spec {
        container {
          env {
            name = "DB_PASSWORD"
            value_from {
              secret_key_ref {
                name = "db-credentials"
                key  = "password"
              }
            }
          }
        }
      }
    }
  }
}
```

**Method 2: Kubernetes Secrets**:
```hcl
# Create Kubernetes secret from Google Secret Manager
resource "kubernetes_secret" "db_credentials" {
  metadata {
    name      = "db-credentials"
    namespace = "default"
  }

  data = {
    "password" = data.google_secret_manager_secret_version.db_password.secret_data
    "username" = "postgres"
    "host"     = google_sql_database_instance.main.private_ip_address
  }

  type = "Opaque"
}

# Use in deployment
resource "kubernetes_deployment" "app" {
  spec {
    template {
      spec {
        container {
          env_from {
            secret_ref {
              name = kubernetes_secret.db_credentials.metadata[0].name
            }
          }
        }
      }
    }
  }
}
```

**Method 3: Cloud Run Environment**:
```hcl
resource "google_cloud_run_service" "api" {
  template {
    spec {
      containers {
        env {
          name = "DATABASE_PASSWORD"
          value_from {
            secret_key_ref {
              name = "db-password"
            }
          }
        }
      }
    }
  }
}
```

### Step 6: Rotate Secrets Safely

**Update Secret Version**:
```bash
# Create new secret version
echo -n "new-password-value" | gcloud secrets versions add db-password \
  --data-file=-

# List versions
gcloud secrets versions list db-password

# Destroy old version (optional, usually keep for rollback)
gcloud secrets versions destroy 1 --secret="db-password"
```

**Terraform Handling of Rotation**:
```hcl
# Terraform will update to latest version automatically
data "google_secret_manager_secret_version" "db_password" {
  secret = "db-password"
  # Always uses latest
}

# After secret rotation, Kubernetes will pick up automatically
# but other applications may need restart
```

### Step 7: Prevent Secrets in State

**Validate Configuration**:
```bash
# Check if terraform plan would expose secrets
terraform plan | grep -i "secret\|password\|key" | grep -v "secret_manager"

# Mark outputs as sensitive
output "connection_string" {
  value     = "Server=${google_sql_database_instance.main.private_ip_address};..."
  sensitive = true  # Prevents display in console
}
```

**Exclude from Logging**:
```hcl
# Mark variables as sensitive
variable "api_key" {
  type      = string
  sensitive = true  # Won't appear in logs/plan output
}

# Don't echo secrets in outputs
output "api_key" {
  value     = var.api_key
  sensitive = true
}

# But do provide endpoint information
output "api_endpoint" {
  value = google_cloud_run_service.api.status[0].url
}
```

### Step 8: Secret Security Best Practices

**Least Privilege**:
```hcl
# ❌ Grant broad access
resource "google_secret_manager_secret_iam_member" "all_access" {
  secret_id = "db-password"
  role      = "roles/secretmanager.admin"  # Too powerful
  member    = "serviceAccount:..."
}

# ✅ Grant only what's needed
resource "google_secret_manager_secret_iam_member" "reader" {
  secret_id = "db-password"
  role      = "roles/secretmanager.secretAccessor"  # Read-only
  member    = "serviceAccount:..."
}
```

**Rotation Schedule**:
- Database passwords: Every 30 days
- API keys: Every 90 days
- JWTs: As needed
- Document rotation schedule in runbooks

**Audit Trail**:
```bash
# View secret access logs
gcloud logging read "resource.type=secretmanager.googleapis.com" \
  --limit 50 \
  --format=json | jq '.[] | {timestamp: .timestamp, protoPayload}'
```

## Examples

### Example 1: Complete Cloud SQL Setup with Secret Manager

```hcl
# variables.tf
variable "environment" {
  type = string
}

# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.26"
    }
  }
}

provider "google" {
  project = "ecp-wtr-supplier-charges-${var.environment}"
  region  = "europe-west2"
}

# Read database password from Secret Manager
data "google_secret_manager_secret_version" "db_password" {
  secret = "database-password-${var.environment}"
}

# Get service account for Cloud SQL
data "google_service_account" "cloudsql_instance" {
  account_id = "cloudsql-instance"
}

# Create Cloud SQL instance
resource "google_sql_database_instance" "charges_db" {
  name             = "supplier-charges-db-${var.environment}"
  database_version = "POSTGRES_15"
  region           = "europe-west2"

  settings {
    tier = var.environment == "prod" ? "db-custom-2-7680" : "db-f1-micro"

    backup_configuration {
      enabled = true
    }

    # Encrypted with service account
    user_labels = {
      environment = var.environment
      managed_by  = "terraform"
    }
  }
}

# Create database
resource "google_sql_database" "charges" {
  name     = "supplier_charges"
  instance = google_sql_database_instance.charges_db.name
}

# Create user with secret password
resource "google_sql_user" "app_user" {
  name     = "app_user"
  instance = google_sql_database_instance.charges_db.name
  password = data.google_secret_manager_secret_version.db_password.secret_data
}

# Grant service account access to secret
resource "google_secret_manager_secret_iam_member" "db_password" {
  secret_id = "database-password-${var.environment}"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${data.google_service_account.cloudsql_instance.email}"
}

# Outputs (marked sensitive)
output "database_connection" {
  value = {
    host     = google_sql_database_instance.charges_db.private_ip_address
    port     = 5432
    database = google_sql_database.charges.name
    user     = google_sql_user.app_user.name
  }
  sensitive = true
}

output "database_name" {
  value = google_sql_database.charges.name
}
```

### Example 2: GKE Deployment with Secrets

```hcl
# secrets.tf
data "google_secret_manager_secret_version" "db_password" {
  secret = "db-password-${var.environment}"
}

data "google_secret_manager_secret_version" "jwt_secret" {
  secret = "jwt-secret-${var.environment}"
}

# kubernetes_secrets.tf
resource "kubernetes_secret" "app_secrets" {
  metadata {
    name      = "app-secrets"
    namespace = "production"
  }

  data = {
    "DB_PASSWORD" = data.google_secret_manager_secret_version.db_password.secret_data
    "JWT_SECRET"  = data.google_secret_manager_secret_version.jwt_secret.secret_data
    "DB_HOST"     = google_sql_database_instance.charges_db.private_ip_address
  }

  type = "Opaque"
}

# deployment.tf
resource "kubernetes_deployment" "charges_service" {
  metadata {
    name      = "charges-service"
    namespace = "production"
  }

  spec {
    replicas = 3

    template {
      spec {
        container {
          name  = "charges-service"
          image = "gcr.io/project/charges:1.0.0"

          # Mount secrets as environment variables
          env_from {
            secret_ref {
              name = kubernetes_secret.app_secrets.metadata[0].name
            }
          }

          # Override specific values
          env {
            name  = "LOG_LEVEL"
            value = var.environment == "prod" ? "info" : "debug"
          }
        }
      }
    }
  }
}
```

### Example 3: Secret Rotation Pipeline

```bash
# rotate_secrets.sh
#!/bin/bash
set -e

SECRET_NAME=$1
ENVIRONMENT=$2

if [ -z "$SECRET_NAME" ] || [ -z "$ENVIRONMENT" ]; then
  echo "Usage: ./rotate_secrets.sh SECRET_NAME ENVIRONMENT"
  echo "Example: ./rotate_secrets.sh db-password prod"
  exit 1
fi

FULL_SECRET_NAME="${SECRET_NAME}-${ENVIRONMENT}"

echo "Rotating secret: $FULL_SECRET_NAME"

# 1. Generate new value
NEW_SECRET=$(openssl rand -base64 32)

# 2. Create new version in Secret Manager
echo -n "$NEW_SECRET" | gcloud secrets versions add "$FULL_SECRET_NAME" \
  --data-file=-

echo "New version created"

# 3. Update Terraform state (plan shown first)
cd terraform/
terraform plan

# 4. Apply to update applications
terraform apply -auto-approve

# 5. Wait for rollout
kubectl rollout restart deployment/charges-service -n production

echo "Secret rotation complete"
```

## Requirements

- Terraform 1.x+
- Google Cloud provider v5.26+
- Google Secret Manager enabled in GCP
- Service account with secretmanager.secretAccessor role
- gcloud CLI for secret management

**Enable APIs**:
```bash
gcloud services enable secretmanager.googleapis.com
```

## See Also

- [terraform skill](../terraform/SKILL.md) - General reference
- [terraform-gcp-integration](../terraform-gcp-integration/SKILL.md) - GCP resources
- [terraform-troubleshooting](../terraform-troubleshooting/SKILL.md) - Debugging secrets
